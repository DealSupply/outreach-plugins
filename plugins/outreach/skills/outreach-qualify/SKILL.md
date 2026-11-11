---
name: outreach-qualify
description: Use when user says "outreach:qualify", "mcp:qualify", "qualifiziere leads", "lead qualifizierung", "qualify leads", "leads bewerten", or triggers /mcp:qualify.
---

# MCP Qualify — Lead-Qualifizierung durch Claude-Subagents

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

> **Workspace:** Es gilt die Workspace-Regel aus dem Skill `outreach`: Workspace kennen, `workspace` nur bei Aufrufen ohne Objekt-ID mitgeben, vor jedem Schreiben oder Lauf den Workspace nennen.

Dieser Skill orchestriert die Lead-Qualifizierung via MCP Business Tools. Claude-Subagents bewerten jeden Lead gegen die Kampagnen-Kriterien (aus `get_lead_data.qualificationGeneration`) und schreiben das Ergebnis via `write_lead_details` zurück. Der Server-Lauf (kostet Credits je Lead, bei BYOK-Konten das eigene OpenRouter-Konto) wird dabei bewusst NICHT verwendet. Dieser Skill ist der **Manuell-Modus**: Dein Client denkt selbst, mit eigenem Modell und eigenen Quellen, und das kostet keine Credits. Standard für den kompletten Durchlauf ist der Server-Lauf via `/outreach-pipeline` (Tool `start_lead_run`). Vor dem Start `list_lead_runs(campaign_id, active_only=true)` prüfen: bei aktivem Lauf mit Qualifizierungs- ODER Research-Stufe blockt `write_lead_details` mit `lead_run_active` — warten (`get_lead_run_status`) oder `cancel_lead_run`.

> **Abo-Lauf (Subagents im Claude- bzw. ChatGPT-Abo):**
> - **Ein Lead pro Agent, immer.** Nie mehrere Leads in einen Agenten geben – Modelle verwechseln sonst Leads.
> - **Agent:** In Claude Code und Cowork `outreach:lead-agent` (Plugin-Agent, Haiku) mit dem Auftrag „Kampagne <id>, Lead <id>, nur Qualifizierung“; sind mehrere Outreach-Server verbunden, zusätzlich „Server: <name>“. Fehlt der Agent, `general-purpose` mit `model: "sonnet"` und der Vorlage unten. Nie das Modell der Sitzung erben lassen: Opus verbraucht das Abo-Kontingent um ein Vielfaches. Andere Clients: das günstigste Modell mit Web-Zugriff; ohne Subagents die Leads **sequentiell** mit denselben Schritten.
> - **Ganzer Lauf** (Qualifizierung → Recherche → Mail in einem): `/outreach-pipeline <id> --abo`.
> - **Parallelität:** höchstens 10 Agents gleichzeitig. Mehr als eine Handvoll Leads in Claude Code: als Workflow nach `outreach-abo-lauf` mit `stufen: "nur Qualifizierung"` – die Sitzung liest dann ein Ergebnis statt jeder einzelnen Agent-Meldung und verbraucht so ein Vielfaches weniger.
> - **Fortschritt:** Gibt es das Werkzeug `outreach_progress` (Claude Code mit Plugin `outreach`), zu Beginn einmal `outreach_progress(action="start", campaign_id, phase="qualification", total=<Leads>)` aufrufen; gezählt wird automatisch, auch jeder Schreibaufruf der Subagents. Den Stand danach aus den Agenten-Antworten berichten, nicht per `list_leads` erneut auflisten, und die Phase mit `outreach_progress(action="end", …)` schließen, damit Leads ohne Schreibaufruf nicht offen im Band hängen.

## Fachlicher Fit ist keine Kontaktfreigabe

Vor dem Workflow `ping` und `list_campaigns` mit dem Auftrag abgleichen. Ausschließlich den fachlichen ICP-/Angebots-Fit bewerten. Allgemeine Werbehinweise aus Website, Impressum, AGB oder Datenschutzerklärung nur als Hinweis mit Quelle in `qualificationSnapshotJson` festhalten (z. B. unter `contactNotices`): deswegen allein weder Score senken noch `not_qualified` setzen. Echte gespeicherte Kontaktstatus (kontaktiert, `do_not_contact` …) sind verbindlich und werden nie aus Website-Text abgeleitet oder entfernt. Opt-in, rechtliche Prüfung und Versandentscheidung bleiben beim Kunden; ein positiver Fit gibt keinen Versand frei.

**Urteile gelten pro Kampagne und sind final:** Das Urteil wird nur für die angegebene `campaign_id` geschrieben; eine Qualifizierung aus einer anderen Kampagne zählt hier als „nie geprüft". Ein in dieser Kampagne bereits abgeschlossenes Urteil (`qualificationStatus=completed`) lässt sich mit `write_lead_details` nicht mehr ändern oder leeren (`verdict_final`); die Queue (`qualification_status="pending"`) zeigt solche Leads nicht mehr. Positive Urteile werden nie ersetzt.

**Neu urteilen (nur `not_qualified`, nur mit Zustimmung):** Hat der Nutzer die Kriterien geändert, lassen sich aussortierte Leads nach den neuen Kriterien noch einmal urteilen. Erst fragen, dann:
- Server-Lauf: `quote_lead_run(…, requalify_not_qualified=true)` nennt in `requalifiable_count`, wie viele es sind; Ablauf und Preis in `outreach-pipeline`, Schritt 3.
- Abo-Lauf bzw. dieser Skill: Auswahl mit `list_leads(campaign_id, run_stages=["qualification"], requalify_not_qualified=true, qualification_filter="not_qualified")` (Listen-Modus, `lead_ids` einmal festhalten), dann je Lead ein Agent mit dem Auftrag „neu urteilen“. Diese Auswahl enthält nur Urteile der Qualifizierung; Urteile, die die Recherche gesetzt hat, zählen erst mit `run_stages=["qualification", "research"]` als offen. Sollen auch sie neu geurteilt werden, so auswählen und den Auftrag „neu urteilen, nur Qualifizierung und Recherche“ geben. Er schreibt das neue Urteil mit `write_lead_details(…, replace_final_verdict=true)` und vollständigen Qualifizierungsfeldern (`qualificationStatus: "completed"` und `qualificationFitLevel` sind Pflicht; nicht gesendete Qualifizierungsfelder werden geleert). Ein Urteil, das die Recherche gesetzt hat, ersetzt der Server nur zusammen mit einer neuen Recherche im selben Aufruf (sonst `verdict_needs_research`); dann braucht der Auftrag auch die Recherche-Stufe. Kontaktierte Leads und Leads mit Mail im Review, freigegeben oder exportiert bleiben unberührt (`verdict_locked`).

**Urteilsregeln:** Die Agents urteilen wie der Server-Lauf als offener Vorfilter (Vorlage unten, Schritt 4): `not_qualified` nur mit konkretem Grund, im Zweifel `mid_qualified`. Ein falsch aussortierter Lead ist endgültig verloren, ein durchgelassener Grenzfall kostet nur eine Recherche.

## Workflow-Übersicht

```
1. list_campaigns -> Kampagne identifizieren (oder campaign_id aus Argument)
   |
2. list_leads(campaign_id, limit={batch_size}, fit_level="", research_status="",
              campaign_status="processing", qualification_status="pending")
   -> {batch_size} unqualifizierte Leads
   |
3. Für jeden Lead: Sub-Agent spawnen (parallel)
   -> get_lead_data() -> Kriterien lesen -> Website analysieren -> bewerten
   -> write_lead_details(qualificationStatus=completed, qualificationFitLevel, score, ...)
   |
4. Batch-Report -> nächster Batch (Queue ist idempotent: qualifizierte Leads
   fallen aus qualification_status="pending" heraus)
```

## Aufruf

| Eingabe | Verhalten |
|---------|-----------|
| `/outreach-qualify` | Zeigt Kampagnen via list_campaigns, User wählt |
| `/outreach-qualify 80` | Startet direkt für Kampagne 80 |
| `qualifiziere leads für kampagne 80` | Startet direkt für Kampagne 80 |

**Batch-Größe abfragen** (wie /outreach-generate): Default 10, Optionen 50/100/200.

## Phase 0: Vorprüfung — kein paralleler Server-Lauf

`list_lead_runs(campaign_id, active_only=true)` aufrufen. Ist ein serverseitiger Lauf aktiv, der Qualifizierung ODER Research abdeckt, lehnt `write_lead_details` jeden Schreibvorgang mit `lead_run_active` ab (Rennschutz — das Tool prüft beide Stufen gemeinsam). Dann: auf den Terminal-Status warten (`get_lead_run_status`) oder den Lauf nach Rücksprache mit `cancel_lead_run` stoppen — NICHT parallel losarbeiten.

## Phase 1: Leads laden

Gibt der Auftrag einen `list_leads`-Aufruf (Listen-Modus mit `run_stages`, etwa aus dem Startdialog der App) oder Lead-IDs vor, gilt genau diese Auswahl statt der Abfrage unten: den Aufruf einmal unverändert ausführen und die Leads aus `lead_ids` nehmen; fehlt in der Antwort `applied_filters`, ist der Server älter als MCP 2.1.0 oder die Verbindung veraltet, dann abbrechen und das melden. Nicht mit `offset` blättern.

```
list_leads(
  campaign_id = <ID>,
  limit = {batch_size},
  fit_level = "",
  research_status = "",
  campaign_status = "processing",
  qualification_status = "pending"
)
```

Wenn `leads` leer: "Keine unqualifizierten Leads." -> STOP.

## Phase 2: Sub-Agents spawnen (parallel)

Für JEDEN Lead genau einen Agent spawnen (Typ und Modell nach „Abo-Lauf“ oben, `run_in_background: true`, höchstens 10 gleichzeitig in EINEM Message-Block, `name`: "qual-{lead.company}" gekürzt).

### Sub-Agent Prompt Template

```
Du qualifizierst einen Lead für eine Cold-Mailing-Kampagne via MCP Tools.

KAMPAGNE: {campaign.name} (ID: {campaign.id})
LEAD: {lead.company} (ID: {lead.id})

## Schritte

1. Rufe get_lead_data(campaign_id={campaign.id}, lead_id={lead.id}) auf.
2. Lies lead.qualificationGeneration:
   - "settings" = die Kampagnen-Kriterien (Zielkunde, Fit-Kriterien, Disqualifier). Sie sind MASSGEBLICH.
   - "agent.additionalPrompt" = zusätzliche Anweisung des Qualifizierungs-Agents; sie ergänzt die Kriterien, ersetzt sie nicht.
   - "writeBack" = erlaubte Werte für fitLevel/status, der Score-Bereich und "summaryLanguage" (Sprache der Kampagne, de oder en; ab MCP 4.7.0, fehlt es: de).
3. Analysiere den Lead:
   - Website (lead.website) per WebFetch laden; wichtige Unterseiten (Leistungen, Über uns, Impressum) bei Bedarf zusätzlich.
   - Custom Attributes (Google-Rating, Kategorie etc.) einbeziehen.
   - Website nicht erreichbar ist KEIN Disqualifier (eine fehlende/schwache Website kann je nach Angebot sogar FUER den Lead sprechen); dann urteilst du aus den Importdaten.
4. Bewerte gegen die Kriterien. Die Qualifizierung ist ein offener Vorfilter wie im Server-Lauf: ein falsch aussortierter Lead ist endgültig verloren, ein durchgelassener Grenzfall kostet nur eine Recherche. Im Zweifel durchlassen.
   - "not_qualified" nur mit konkretem, benennbarem Grund: ein Disqualifier der Kampagne trifft belegt zu, ein gelistetes No-Go, ein eindeutig falscher Geschäftstyp (Kerngeschäft außerhalb des Zielkunden; eine Zusatzleistung oder thematische Nähe ist keine Überschneidung) oder kein erkennbarer Geschäftsbetrieb. Ohne konkreten Grund keine Ablehnung. Allgemeine Website-/Impressums-Werbehinweise zählen ausdrücklich NICHT dazu; sie verändern weder Fit noch Score und werden nur als Hinweis (contactNotices) im Snapshot dokumentiert. Echte gespeicherte Kontaktstatus niemals entfernen oder aus Website-Text ableiten.
   - "mid_qualified": passt, aber die Evidenz ist dünn oder unsicher, oder nur teilweise Überschneidung. Unsicherheit oder „passt halbwegs“ ist nie ein Ablehnungsgrund.
   - "qualified": Fit positiv belegt (nicht nur keine No-Gos); "highly_qualified": besonders starker Fit.
   - Nur Importdaten (keine Website-Evidenz): passen sie, höchstens "mid_qualified" und "nur Importdaten" in der Zusammenfassung. Passen sie erkennbar nicht oder spräche nur aus ihnen ein Ausschlussgrund: KEIN Urteil schreiben (ohne Website-Evidenz zählt eine Ablehnung nicht als Urteil, der Server-Lauf lässt den Lead dann ebenfalls offen), Schritt 5 entfällt, Antwort "OFFEN lead={lead.id}: nur Importdaten, kein Urteil".
   - Geschmacksurteile (hässliche Website, wenig Inhalt) sind nie ein Disqualifier, außer die Kampagne sagt es.
   - score 0-100 konsistent zum fitLevel (not_qualified: 0-39, mid: 40-59, qualified: 60-79, highly: 80-100).
5. Schreibe das Ergebnis:
   write_lead_details(campaign_id={campaign.id}, lead_id={lead.id}, fields={
     "qualificationStatus": "completed",
     "qualificationFitLevel": "<fitLevel>",
     "score": <int>,
     "qualificationCategory": "<kurze Branchenkategorie, kein Fit-Wert wie not_qualified>",
     "qualificationSummary": "<2-4 Sätze in der Sprache aus writeBack.summaryLanguage: warum dieses fitLevel, welche Kriterien erfüllt/verletzt>",
     "qualificationSnapshotJson": { "businessFitLevel": "<fitLevel>", "contactNotices": [...], "criteria_matched": [...], "disqualifiers_hit": [...], "evidence": [{"claim": "...", "source": "<URL>"}] }
   })
   Nur beim Auftrag „neu urteilen“ (der Nutzer hat zugestimmt): denselben Aufruf mit replace_final_verdict=true und allen Feldern oben. Antwortet er verdict_needs_research, verdict_locked oder verdict_being_judged: nicht wiederholen, den Code melden.

## Regeln

- NICHTS ERFINDEN: Jede Behauptung in summary/snapshot braucht eine beobachtete Quelle (Website-Inhalt, Attribut). Unbelegtes weglassen.
- Die Kampagnen-Kriterien schlagen jede eigene Heuristik.
- Deutsch, korrekte Umlaute (Ä/Ö/Ü/ß — niemals AE/OE/UE/ss). Ausnahme: qualificationSummary steht in der Sprache aus writeBack.summaryLanguage (bei "en" auf Englisch); fitLevel, status und Schlüssel bleiben die festen Werte.
- Antworte am Ende NUR mit: "OK lead={lead.id} fitLevel=<...> score=<...>", "OFFEN lead={lead.id}: nur Importdaten, kein Urteil" oder "FEHLER lead={lead.id}: <Grund>".
```

## Phase 3: Report & nächster Batch

Wie /outreach-generate: Batch-Report (Erfolg/Fehler/Verbleibend), dann erneut `list_leads` bis `remaining == 0`. Fehlgeschlagene Leads bleiben `qualification_status=pending` und tauchen im nächsten Lauf wieder auf — kein automatischer Einzel-Retry. Leads mit `OFFEN` (nur Importdaten, kein Urteil) bleiben ebenfalls `pending`: ihre IDs festhalten, in diesem Lauf nicht erneut vergeben; die Schleife endet, sobald nur noch solche Leads übrig sind und im Abschluss-Report mit Grund nennen.

Abschluss-Report + Hinweis: "Nächster Schritt: /outreach-research — qualifizierte Leads recherchieren".

## Fehlerbehandlung

| Fehler | Aktion |
|--------|--------|
| leads[] leer | "Keine unqualifizierten Leads" -> STOP |
| `verdict_final` | In dieser Kampagne schon ein abgeschlossenes Urteil — Lead ist erledigt, nicht erneut schreiben (positive Urteile lassen sich nie ersetzen) |
| `verdict_locked` | Beim Neu-Urteilen: der Lead ist kontaktiert oder hat eine Mail im Review, freigegeben oder exportiert — Urteil bleibt, Lead überspringen |
| `verdict_needs_research` | Beim Neu-Urteilen: das alte Urteil hat die Recherche gesetzt — nur zusammen mit einer neuen Recherche im selben Aufruf ersetzbar; ohne Recherche-Stufe den Lead überspringen und melden |
| `verdict_being_judged` | Ein Qualifizierungs- oder Recherche-Job urteilt gerade über den Lead — nicht wiederholen, später prüfen |
| `validation_failed`, `invalid_enum`, `unknown_field` | Feld bzw. Wert aus dem Fehlertext korrigieren (erlaubte Werte stehen in `writeBack`) und einmal neu schreiben; sonst Lead als Fehler notieren |
| write_lead_details error (sonstiger Code) | Fehler notieren, weiter mit nächstem Lead |
| `contact_gate` | Kontaktstatus des Leads ist nicht `not_contacted` (kontaktiert, exportiert, gesperrt …) — Lead überspringen, nicht erneut schreiben |
| `lead_run_active` | Parallel läuft ein Server-Lauf — Batch pausieren, `get_lead_run_status` bis Terminal-Status, dann fortsetzen (Queue ist idempotent) |
| Sub-Agent Timeout/Crash | Als Fehler zählen, Lead bleibt in der Queue |
| MCP-Verbindungsfehler | 1x Retry, dann STOP |

## Verwandt

- `/outreach-research` — Research für qualifizierte Leads (nächste Phase)
- `/outreach-generate` — AI-Variablen (nach Research)
