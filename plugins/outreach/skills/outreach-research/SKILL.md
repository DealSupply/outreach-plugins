---
name: outreach-research
description: Use when user says "outreach:research", "mcp:research", "recherchiere leads", "lead research", "research leads", "leads recherchieren", or triggers /mcp:research.
---

# MCP Research — Lead-Research durch Claude-Subagents

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

Dieser Skill orchestriert das Lead-Research via MCP Business Tools. Claude-Subagents recherchieren jeden Lead (Website, öffentliche Quellen) nach den Kampagnen-Vorgaben (aus `get_lead_data.researchGeneration`) und schreiben den Report via `write_lead_details` zurück. Die serverseitige Research-Pipeline (OpenRouter, serverseitiges Website-Scraping) wird dabei bewusst NICHT verwendet — dieser Skill ist der **Manuell-Modus** (eigenes Modell/eigene Quellen); entsprechend entstehen keine Screenshot-Artefakte. Der serverseitige Lauf (`/outreach-pipeline`, Tool `start_lead_run`) erzeugt sie dagegen. Vor dem Start `list_lead_runs(campaign_id, active_only=true)` prüfen: bei aktivem Lauf mit Research- ODER Qualifizierungs-Stufe blockt `write_lead_details` mit `lead_run_active`.

> **Abo-Lauf (Subagents im Claude- bzw. ChatGPT-Abo):**
> - **Ein Lead pro Agent, immer.** Nie mehrere Leads in einen Agenten geben – Modelle verwechseln sonst Leads.
> - **Agent:** In Claude Code und Cowork `outreach:lead-agent` (Plugin-Agent, Haiku) mit dem Auftrag „Kampagne <id>, Lead <id>, nur Recherche“; sind mehrere Outreach-Server verbunden, zusätzlich „Server: <name>“. Fehlt der Agent, `general-purpose` mit `model: "sonnet"` und der Vorlage unten. Nie das Modell der Sitzung erben lassen: Opus verbraucht das Abo-Kontingent um ein Vielfaches. Andere Clients: das günstigste Modell mit Web-Zugriff; ohne Subagents die Leads **sequentiell** mit denselben Schritten.
> - **Ganzer Lauf** (Qualifizierung → Recherche → Mail in einem): `/outreach-pipeline <id> --abo`.
> - **Parallelität:** höchstens 10 Agents gleichzeitig. Mehr als eine Handvoll Leads in Claude Code: als Workflow nach `outreach-abo-lauf` mit `stufen: "nur Recherche"` – die Sitzung liest dann ein Ergebnis statt jeder einzelnen Agent-Meldung und verbraucht so ein Vielfaches weniger.
> - **Fortschritt:** Gibt es das Werkzeug `outreach_progress` (Claude Code mit Plugin `outreach`), zu Beginn einmal `outreach_progress(action="start", campaign_id, phase="research", total=<Leads>)` aufrufen; gezählt wird automatisch, auch jeder Schreibaufruf der Subagents. Den Stand danach aus den Agenten-Antworten berichten, nicht per `list_leads` erneut auflisten, und die Phase mit `outreach_progress(action="end", …)` schließen, damit Leads ohne Schreibaufruf nicht offen im Band hängen.

## Websitehinweise und gespeicherte Sperren getrennt halten

Vor dem Workflow `ping` und `list_campaigns` mit dem Auftrag abgleichen. Allgemeine Hinweise gegen Werbung in Website, Impressum oder AGB nur informativ mit Quelle im Report erfassen. Sie allein begründen weder Score-Abwertung noch fachliches `not_qualified` oder das Unterdrücken weiterer Research. Sie niemals in einen Kontaktstatus (`do_not_contact`) umdeuten. Echte gespeicherte Kontaktstatus bleiben verbindlich; nicht entsperren. Opt-in, rechtliche Prüfung und Versandentscheidung liegen beim Kunden, nicht in der Research-Klassifizierung.

## Workflow-Übersicht

```
1. list_campaigns -> Kampagne identifizieren (oder campaign_id aus Argument)
   |
2. list_leads(campaign_id, limit={batch_size}, fit_level="qualified",
              research_status="pending", campaign_status="processing")
   -> {batch_size} qualifizierte, unrecherchierte Leads
   |
3. Für jeden Lead: Sub-Agent spawnen (parallel)
   -> get_lead_data() -> Research-Vorgaben lesen -> Website/Quellen analysieren
   -> write_lead_details(research=<Report>, bestEmail, decisionMaker, ..., status="researched")
   |
4. Batch-Report -> nächster Batch (Queue idempotent: recherchierte Leads
   fallen aus research_status="pending" heraus)
```

## Aufruf

| Eingabe | Verhalten |
|---------|-----------|
| `/outreach-research` | Zeigt Kampagnen via list_campaigns, User wählt |
| `/outreach-research 80` | Startet direkt für Kampagne 80 |
| `recherchiere leads für kampagne 80` | Startet direkt für Kampagne 80 |

**Batch-Größe abfragen** (wie /outreach-generate): Default 10, Optionen 50/100/200.

**Vorbedingung:** Leads sollten qualifiziert sein (`/outreach-qualify` zuerst). Wer bewusst unqualifizierte Leads recherchieren will: `fit_level=""` verwenden.

## Phase 0: Vorprüfung — kein paralleler Server-Lauf

`list_lead_runs(campaign_id, active_only=true)` aufrufen. Ist ein serverseitiger Lauf aktiv, der Research ODER Qualifizierung abdeckt, lehnt `write_lead_details` jeden Schreibvorgang mit `lead_run_active` ab (Rennschutz — das Tool prüft beide Stufen gemeinsam). Dann: auf den Terminal-Status warten (`get_lead_run_status`) oder den Lauf nach Rücksprache mit `cancel_lead_run` stoppen — NICHT parallel losarbeiten.

## Phase 1: Leads laden

Gibt der Auftrag einen `list_leads`-Aufruf (Listen-Modus mit `run_stages`, etwa aus dem Startdialog der App) oder Lead-IDs vor, gilt genau diese Auswahl statt der Abfrage unten: den Aufruf einmal unverändert ausführen und die Leads aus `lead_ids` nehmen; fehlt in der Antwort `applied_filters`, ist der Server älter als MCP 2.1.0 oder die Verbindung veraltet, dann abbrechen und das melden. Nicht mit `offset` blättern.

```
list_leads(
  campaign_id = <ID>,
  limit = {batch_size},
  fit_level = "qualified",
  research_status = "pending",
  campaign_status = "processing"
)
```

Wenn `leads` leer: "Keine Leads mit ausstehendem Research." -> STOP.

## Phase 2: Sub-Agents spawnen (parallel)

Für JEDEN Lead genau einen Agent spawnen (Typ und Modell nach „Abo-Lauf“ oben, `run_in_background: true`, höchstens 10 gleichzeitig in EINEM Message-Block, `name`: "res-{lead.company}" gekürzt).

### Sub-Agent Prompt Template

```
Du recherchierst einen Lead für eine Cold-Mailing-Kampagne via MCP Tools.

KAMPAGNE: {campaign.name} (ID: {campaign.id})
LEAD: {lead.company} (ID: {lead.id})

## Schritte

1. Rufe get_lead_data(campaign_id={campaign.id}, lead_id={lead.id}) auf.
2. Lies lead.researchGeneration:
   - "config" = Research-Ziele/Prioritäten der Kampagne (researchGoals, researchPriorities, additionalPrompt). Sie sind MASSGEBLICH dafür, WONACH du suchst.
   - "agent.additionalPrompt" = zusätzliche Anweisung des Research-Agents; ein "config.additionalPrompt" der Kampagne ergänzt sie, beide gelten.
   - "researchTier" = wirksame Recherche-Stufe ("tier": basis, smart oder deep; "origin": campaign, account, tools oder agent) mit "rules". Die Regeln sind VERBINDLICH dafür, WIE VIEL du im Netz suchen darfst; der Server-Lauf hält dieselben Grenzen ein, und die Kosten des Kunden hängen daran. Fehlt "researchTier" (älterer Server), gilt Deep.
   - "contactEmail" (ab MCP 3.0.0) = {required, rules}. Ist "required" true (der Lead hat noch keine Adresse, `lead.contactEmailState` ist nicht "present"), ist die eigene Kontaktadresse des Betriebs ZIEL 0 der Recherche; "rules" sagen, welche Adressen zählen, und gehen den Plugin-Regeln unten vor.
3. Recherchiere:
   - ZIEL 0, nur wenn der Lead keine Adresse hat: Impressum, Kontakt-, Team- und Datenschutzseite sowie den Footer der eigenen Website nach einer Adresse des Betriebs selbst durchsuchen (innerhalb von "researchTier.rules"; Basis erlaubt die Website, das genügt meist). Persönliche Adresse von Inhaber oder Geschäftsführung vor Funktionsadresse vor info@/kontakt@; info@ ist erlaubt. Nur wörtlich auf einer Seite stehende Adressen mit Fundstelle.
   - Website (lead.website) per WebFetch laden; relevante Unterseiten (Leistungen, Über uns, Team, Referenzen, Impressum, Kontakt) gezielt nachladen.
   - Suchen nur nach "researchTier.rules": Basis keine WebSearch und keine fremden Seiten (Bewertungszahlen nur aus den Lead-Attributen), außer genau einer Suche nach "<Firma> <Ort>", wenn die Website gar nichts liefert; Smart erst ohne Suche, dann höchstens eine Suche "<Firma> <Ort> Bewertungen", wenn kein starker Anker belegt ist und keine Rezensionstexte importiert sind; Deep nach Bedarf. Jede Suche unter "## Research Details" mit Suchanfrage vermerken.
   - Bewertungen (bei Deep zuerst, bei Smart nur in der einen erlaubten Suche): WebSearch liefert nur Links, die Treffer von Bewertungsportalen und Verzeichnissen per WebFetch öffnen (Google Maps und Google-Seiten sind so nicht lesbar). Anzahl und Schnitt aus den Lead-Attributen des Imports gelten als Quelle.
   - Die Sperrliste der Kampagne (Research-Vorgaben) beachten: gesperrte Standardleistungen nicht als Aufhänger vormerken, außer als Lob aus Bewertungstexten.
   - Qualifizierungs-Kontext (lead.qualification) als Ausgangspunkt nutzen.
4. Extrahiere gemäß den Research-Zielen, typischerweise:
   - Konkrete, verifizierbare Aufhänger, die den Betrieb von anderen seiner Branche abheben (Lob aus Bewertungen, eigenes Konzept, eigenes Verfahren, seltene Spezialisierung, Auszeichnung); was auf zehn andere Betriebe derselben Branche in der Stadt passt, ist kein Aufhänger.
   - Entscheider (Name/Rolle, meist im Impressum/Über-uns) und die Adresse, über die die Entscheidungsperson am wahrscheinlichsten erreicht wird (Regel in Schritt 5).
5. Schreibe das Ergebnis:
   write_lead_details(campaign_id={campaign.id}, lead_id={lead.id}, fields={
     "research": "<Markdown-Report: ## Unternehmen, ## Aufhänger (mit Quellen-URLs), ## Kontakt, ## Besonderheiten>",
     "bestEmail": "<gewählte Versandadresse nach der Regel unten>",
     "decisionMaker": "<Name, Rolle — nur wenn öffentlich belegt>",
     "contactRecommendation": "<1-2 Sätze: wen wie ansprechen>",
     "status": "researched"
   })
   Felder ohne belegte Erkenntnis WEGLASSEN (nicht mit Vermutungen füllen).
   `bestEmail` ist die gewählte Versandadresse. Gewählt wird die Adresse, über die die
   Entscheidungsperson am wahrscheinlichsten erreicht wird: belegte persönliche Adresse der
   Entscheidungsperson vor Funktionsadresse (vertrieb@, geschäftsführung@) vor allgemeiner
   Adresse (info@, kontakt@). Eine öffentlich belegte persönliche Adresse der empfohlenen
   Entscheidungsperson, auch Freemail, ersetzt deshalb eine allgemeine Importadresse; die
   Importadresse bleibt Zweitadresse. Eine persönliche Importadresse bleibt Versandadresse.
   Nur Adressen mit Fundstelle; nie eine aus Vor- und Nachname
   geratene, nie eine als unzustellbar bekannte (Bounce), nie Platzhalter wie "null". Ohne
   belegte Adresse `bestEmail` weglassen.
   Lead ohne Adresse (ab MCP 3.0.0): Eine gefundene eigene Adresse des Betriebs wird `bestEmail`
   (Reihenfolge wie oben: persönliche vor Funktionsadresse vor info@/kontakt@, Adressen auf der
   eigenen Domain oder Freemail mit Fundstelle). Der Server macht sie auch zur Identität des Leads
   (`warnings` meldet das). Nie Adressen einer Plattform, eines Verzeichnisses, des Webdesigners,
   Hosters, einer Kammer oder eines Portals, nie geraten, nie Platzhalter. Meldet `warnings`
   `address_conflict`, gehört die Adresse schon einem anderen Lead: nicht wiederholen, im Report
   vermerken. Findet sich keine Adresse: `bestEmail` WEGLASSEN, unter "## Kontakt" die geprüften
   URLs nennen und trotzdem status="researched" setzen. Der Lead scheidet dann mit dem Grund
   `no_contact_email` aus und bekommt keine Mail.
   Fremde Importadresse: Gehört die Importadresse laut Recherche belegt einem Dritten (Kammer,
   Verband, Portal, Agentur, andere Firma) und findest du keine eigene belegte Adresse des
   Betriebs, `bestEmail` weglassen und die fremde Adresse im Report vermerken. Der Lead bekommt
   dann keine Mail (der ListM8-Server überspringt ihn in der E-Mail-Stufe). Eine eigene DNS- oder
   MX-Prüfung der Adresse gibt es nicht und gehört nicht zur Recherche.
   Steht `bestEmail` danach in `skipped_fields`, hat ein Mensch die Versandadresse schon
   gewählt (Text in `warnings`). Die Wahl gilt: nicht erneut schreiben, nicht selbst per
   `switch_primary_email` ändern, im Report vermerken.
   Keinen Platzhalter-Entscheider ("unbekannt", "n/a") schreiben — Feld weglassen.
   Wenn Website UND Suche nichts hergeben: minimalen Report schreiben (was geprüft wurde,
   was nicht erreichbar war) und trotzdem status="researched" setzen — der Lead soll die
   Queue verlassen; die Bewertung übernimmt der Review-Schritt.

## Regeln

- NICHTS ERFINDEN: Jede Aussage im Report braucht eine Quelle (URL). Aus dem Namen abgeleitete Adressen (Muster) explizit als Vermutung kennzeichnen oder weglassen, nie als `bestEmail` schreiben.
- Keine internen Metriken/Scores in den Report-Text.
- Allgemeine Website-/Impressums-Werbehinweise ausschließlich als Information mit Quelle dokumentieren. Dadurch allein keinen Score/Fit abwerten, Research unterdrücken oder einen Kontaktstatus setzen. Echte gespeicherte Sperren erhalten; Opt-in und Versandentscheidung bleiben beim Kunden.
- Deutsch, korrekte Umlaute (Ä/Ö/Ü/ß — niemals AE/OE/UE/ss).
- Antworte am Ende NUR mit: "OK lead={lead.id} aufhänger=<kurz> adresse=<gefunden|keine|vorhanden>" oder "FEHLER lead={lead.id}: <Grund>".
```

## Phase 3: Report & nächster Batch

Wie /outreach-generate: Batch-Report, dann erneut `list_leads` bis `remaining == 0`. Fehlgeschlagene Leads bleiben `research_status=pending`. Im Report zählen, wie viele Leads ohne Adresse eine gefunden haben (`adresse=gefunden`) und wie viele ausscheiden (`adresse=keine`).

Abschluss-Report + Hinweis: "Nächster Schritt: /outreach-generate — AI-Variablen generieren".

## Versandadresse auf Wunsch des Users wechseln

`switch_primary_email(campaign_id, lead_id, email, reason?)` macht eine Adresse, die schon am Lead steht (`get_lead_data`: `lead.email`, `lead.sendingEmail`, `lead.secondaryEmails`, `lead.research.bestEmail`, `lead.research.contactProfile`), zur Versandadresse. Bei einem Lead ohne jede Adresse gibt es nichts zu wählen: `unknown_address` mit leerer Kandidatenliste ist dann erwartet. Die Wahl gilt danach als Menschenwahl: weder Research noch `write_lead_details` überschreiben sie. Nur auf ausdrückliche Entscheidung des Users aufrufen, nie aus einem Sub-Agent und nie, um eine gerade recherchierte Adresse "aufzuräumen". `unknown_address` nennt die wählbaren Adressen; bei `address_conflict` versendet schon ein anderer Lead an diese Adresse: die beiden Leads zusammenführen statt doppelt zu schreiben. Leads mit Kontaktstatus `do_not_contact` lehnt das Tool ab; bei bereits kontaktierten Leads meldet es `already_contacted` (die an Instantly übergebene Adresse ändert sich dort nicht).

## Fehlerbehandlung

| Fehler | Aktion |
|--------|--------|
| leads[] leer | "Keine Leads mit ausstehendem Research" -> STOP |
| `validation_failed` bei write_lead_details (z. B. ungültige E-Mail oder Website) | Feld aus dem Text korrigieren oder weglassen und einmal neu schreiben; klappt es nicht, Lead als Fehler notieren und weiter. Kein Verbindungsfehler, NIE den Batch stoppen |
| `contact_gate` | Kontaktstatus des Leads ist nicht `not_contacted` (kontaktiert, exportiert, gesperrt …) — Lead überspringen, nicht erneut schreiben |
| write_lead_details error (sonstiger Code) | Fehler notieren, weiter mit nächstem Lead |
| `bestEmail` in `skipped_fields` | Kein Fehler: eine manuell gewählte Versandadresse bleibt bestehen, oder (Warnung `address_conflict`, auch wenn ein paralleler Agent sie gerade übernommen hat) die Adresse gehört schon einem anderen Lead (Hinweis in `warnings`): respektieren, im Report vermerken, nicht wiederholen |
| `identity_immutable` bei `email` | Die Identitätsadresse eines Leads ist nicht änderbar; nur `bestEmail` schreiben |
| `validation_failed` bei `website` eines Leads ohne E-Mail | Die Website ist dann seine Identität: nicht leeren und nicht durch ein Plattform-Profil oder eine ungültige URL ersetzen. `website` weglassen und den Rest neu schreiben |
| `duplicate_website` | Ein anderer Lead trägt schon diese Website: `website` weglassen und den Rest neu schreiben, im Report vermerken, nicht wiederholen |
| `lead_run_active` | Parallel läuft ein Server-Lauf — Batch pausieren, `get_lead_run_status` bis Terminal-Status, dann fortsetzen (Queue ist idempotent) |
| Sub-Agent Timeout/Crash | Als Fehler zählen, Lead bleibt in der Queue |
| MCP-Verbindungsfehler (JSON-RPC-Fehler ohne Tool-Ergebnis, Transport weg) | 1x Retry, dann STOP |

## Verwandt

- `/outreach-qualify` — Qualifizierung (vorherige Phase)
- `/outreach-generate` — AI-Variablen (nächste Phase), `/outreach-verify` — Review
