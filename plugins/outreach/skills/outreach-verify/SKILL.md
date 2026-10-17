---
name: outreach-verify
description: Use when user says "outreach:verify", "mcp:verify", "verify emails", "email verification", "prüfe emails", "email review", "emails prüfen", or triggers /mcp:verify.
---

# MCP Verify — AI-Variablen-Review

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

Dieser Skill orchestriert den automatischen Review von AI-generierten Variablen via MCP Business Tools. Claude reviewt jede Variable, gibt qualifizierte Variablen frei (`approve_lead_variables`) oder lehnt unbrauchbare ab (`reject_lead_variables`). Behebbare Fehler werden dabei direkt nachgebessert und gegengeprüft, statt sie dem Nutzer vorzulegen.

> **Hinweis zur Parallelisierung:** Wenn dein Client parallele Subagents unterstützt (z.B. Claude Code), spawne pro Lead einen Subagent wie beschrieben. Andernfalls arbeite die Leads **sequentiell** mit exakt denselben Schritten ab — das Ergebnis ist identisch, nur langsamer.

> **Wichtig:** Vor dem Review `ping` und `list_campaigns` prüfen: Konto und Kampagne müssen zum Auftrag passen. Der fertige Mailtext entsteht erst beim Export aus E-Mail-Schritten und Variablen; geprüft werden hier die gespeicherten Variablenwerte (`get_lead_variables`), nicht ein gerenderter Gesamttext. `approve_lead_variables` setzt nur den Status `approved` (bereit für den CSV-Export, `export_leads`) und überträgt nichts nach Instantly; Push und Export sind eigene Schritte. Während aktiver E-Mail-Läufe warten. Korrigiert wird nie inline: inhaltliche Korrekturen von Werten laufen über eine vollständige neue Version mit `save_lead_variables` oder eine ausdrücklich gestartete Neugenerierung (`start_lead_run`, Stufe `email`); Änderungen an einem Variablen-Prompt über `update_ai_variable`, an der Vorlage über `export_campaign_blueprint` + `edit_campaign` (Replace-all der Schritte). Generierte Werte bleiben dabei stehen; sie neu zu erzeugen kostet erneut und braucht die ausdrückliche Zustimmung.

## Standard: Stichprobe statt Vollprüfung

Die meisten Fehler sind systematisch (falsche Anrede-Regel, Adressfrage, Prompt-Rangfolge) und zeigen sich
schon an wenigen Leads; eine Vollprüfung kostet etwa so viel wie das Generieren und findet darüber hinaus
nur wenige Einzelfälle. Darum:

- **Stichprobe von 10 Leads** bei einer neuen Kampagne, nach einer Änderung an Prompts oder Plugin und vor
  dem ersten Export. Die 10 über die Liste streuen (verschiedene Scores, persönliche und Sammeladressen).
- Findet die Stichprobe einen Fehler, der sich wiederholen kann: die Ursache beheben (Variablen-Prompt über
  `/outreach-campaign`, sonst im Generator) und die betroffenen Leads neu generieren, nicht alle prüfen.
- **Vollprüfung nur auf ausdrücklichen Wunsch** des Nutzers (z. B. für eine besonders wertvolle Liste).
- Export und Push nehmen nur freigegebene Leads (`approved`). Nach bestandener Stichprobe den Rest nur
  auf ausdrückliche Bestätigung freigeben: gesammelt in der App oder mit `approve_lead_variables` je Lead
  aus der Hauptsitzung, ohne Prüf-Agenten. Leads mit offenem Hinweis (`fit`, `recht` oder nach dem
  Nachbessern noch offen) bleiben draußen.

## Mit dem verify-agent (Claude Code, Cowork)

Steht der Agent `outreach:verify-agent` zur Verfügung, prüft je Lead genau EIN solcher Agent (Sonnet).
Er schreibt nie Texte, liest `get_lead_variables` und `export_campaign_blueprint`, prüft Fakten gegen
die Recherche, Person, Kampagnenregeln, Copy und Versandhinweise und antwortet mit einer Zeile
`URTEIL lead=… ergebnis=<freigeben|ablehnen|hinweis> art=<text|recherche|adresse|fit|recht|-> geschrieben=… grund=…`.
Die Art sagt, wer einen Befund behebt: `text`, `recherche` und `adresse` werden nachgebessert (Schritt 4),
`fit` und `recht` entscheidet der Nutzer.

1. Kampagnenprüfung (Copy-Prüfung unten) einmal vorab, nicht je Lead. Gibt es `outreach_progress`, die
   Phase mit `outreach_progress(action="start", campaign_id, phase="verify", total=<Leads>)` anmelden; jeder
   Agent meldet sein Urteil selbst (`action="verdict"`), das Band zeigt geprüft / frei / abgelehnt / Hinweis.
   Nach dem Bericht die Phase mit `action="end"` schließen.
2. Leads wie in Phase 2 laden, dann je Lead ein Agent mit dem Auftrag
   „Kampagne <id>, Lead <id> (<Firma>). Server: <name>. Modus: nur Urteil“ bzw. „Modus: entscheiden“.
   In Claude Code als Workflow nach `outreach-abo-lauf` mit `nur_pruefen: true` und den ausgewählten
   Leads (gleiche Kette: prüfen → nachbessern → gegenprüfen, Modus „nur Urteil“). Ohne Workflow höchstens
   10 gleichzeitig (`run_in_background: true`).
3. **Erste Läufe einer Kampagne im Modus „nur Urteil“:** Die Prüf-Agents setzen keinen Status. Erst wenn der
   Nutzer die Urteile gesehen hat, „entscheiden“; dann setzt der Agent `approved` bzw. `rejected`.
4. **Nachbessern (Standard, ohne Rückfrage):** Kleine Fehler werden behoben, nicht dem Nutzer vorgelegt.
   - Für jedes Urteil `ablehnen` oder `hinweis` mit `art=text|recherche|adresse` je Lead ein
     `outreach:lead-agent` (Haiku, Abo, keine Server-Kosten) mit dem Auftrag
     „Kampagne <id>, Lead <id> (<Firma>). Server: <name>. Nachbessern: art=<art>, Befund: <grund>“.
     Er schreibt eine neue Version (`save_lead_variables`), recherchiert bei `recherche` gezielt nach und
     stellt bei `adresse` die Versandadresse auf die belegte um. Höchstens 10 gleichzeitig. Gibt es
     `outreach_progress`, die Phase mit `phase="email"` und `total=<Anzahl>` anmelden.
   - **Gegenprüfung:** Je nachgebessertem Lead (`NACHGEBESSERT …`) ein NEUER `verify-agent` im selben Modus
     wie der Lauf. Wer geschrieben hat, prüft und gibt nie selbst frei, auch nicht die Hauptsitzung.
   - Höchstens eine Runde je Lead. Besteht die Gegenprüfung nicht oder meldet der Lead-Agent
     `UNVERÄNDERT`, geht der Lead mit Grund an den Nutzer.
   - Ist derselbe Befund bei drei oder mehr Leads aufgetreten, ist er systematisch: nicht einzeln
     nachbessern, sondern die Ursache beheben (Variablen-Prompt über `/outreach-campaign`) und die
     betroffenen Leads neu generieren (siehe Stichprobe oben).
   - Ohne Subagents bessert die Hauptsitzung selbst nach (gleiche Regeln, Skill `outreach-copy`), gibt die
     Leads aber nicht frei, sondern legt sie dem Nutzer zur Freigabe vor.
5. **An den Nutzer gehen nur `fit` und `recht`** sowie Leads, die nach einer Runde Nachbessern noch offen
   sind, jeweils mit einer Empfehlung. Im Bericht steht je nachgebessertem Lead kurz, was geändert wurde
   (alter und neuer Anker, umgestellte Adresse).

Ohne diesen Agenten gilt der Ablauf unten mit der Sub-Agent-Vorlage.

## Workflow-Übersicht

```
1. list_campaigns -> Kampagne identifizieren (oder campaign_id aus Argument)
   |
2. list_leads(campaign_id, campaign_status="pending_review", fit_level="", research_status="", limit={batch_size})
   -> Leads mit generierten, noch nicht freigegebenen Variablen
   |
3. Für jeden Lead: Sub-Agent spawnen (parallel, bis zu {batch_size} gleichzeitig)
   -> Jeder Agent: get_lead_variables() -> Review -> approve_lead_variables() oder reject_lead_variables()
   |
4. Batch-Report: "Batch 1/N done, X approved, Y rejected"
   |
5. Nächster Batch: list_leads erneut (remaining > 0?)
   |
6. Fertig: Abschluss-Report
```

## Aufruf

| Eingabe | Verhalten |
|---------|-----------|
| `/outreach-verify` | Zeigt Kampagnen via list_campaigns, User wählt |
| `/outreach-verify 76` | Startet direkt für Kampagne 76 |
| `pruefe emails für kampagne 76` | Startet direkt für Kampagne 76 |

## Schritt-für-Schritt Anleitung

### Phase 1: Kampagne bestimmen

Wenn KEINE campaign_id als Argument übergeben wurde:

1. Rufe `list_campaigns` auf (MCP Tool)
2. Zeige dem User die Kampagnen mit `leadCounts.pending_review > 0`
3. Frage: "Für welche Kampagne soll ich Variablen reviewen?"
4. Merke dir die campaign_id
5. Vorprüfung: `list_lead_runs(campaign_id, active_only=true)` — solange für einen Lead ein Job der E-Mail- oder der Research-Stufe wartet oder läuft, lehnen `approve_lead_variables`/`reject_lead_variables` diesen Lead mit `lead_run_active` ab (Rennschutz). Erst nach dem Terminal-Status des Laufs reviewen. Nach einer Änderung der Kampagnenkonfiguration (Variablen, Schritte) vorhandene Werte nicht blind freigeben, sondern gegen die aktuelle Konfiguration prüfen (`export_campaign_blueprint`) und bei Abweichung neu generieren.

Wenn campaign_id als Argument übergeben wurde: Direkt zur Copy-Prüfung.

**Copy-Prüfung der Kampagne (Pflicht, einmal pro Kampagne):** Den Skill `outreach-copy` laden und die Sequenz aus `export_campaign_blueprint(campaign_id)` gegen dessen Selbstprüfung (14 Punkte) und Prüfliste halten: Wortlimits je Step (Anrede und ein Bezug von bis zu 2 Sätzen eingerechnet), EIN CTA, kein Pitch, Offer und `{{ai.intro}}` nur in Step 1, Feinheiten-Satz bei Karte A/C, kein Link in Step 1, Spam-Wörter, nur erlaubte Platzhalter, Betreffzeilen, Umlaute, `salutation` passend zu Text und `hallo`-Prompt. Funde dem User vor dem Review nennen: Fehler im festen Text oder in den Prompts behebt kein Approve, sie gehören über `/outreach-campaign` korrigiert. Ob trotzdem reviewt wird, entscheidet der User.

**Batch-Größe abfragen:**

Frage den User:
"Wie viele Leads pro Batch? (Default: 10)"
- 10 (Standard)
- 50 (Schneller, 50 parallele Agents)
- 100 (Aggressiv)
- 200 (Maximum)

Merke dir die Antwort als `{batch_size}`. Wenn der User einfach Enter drückt oder nichts sagt: `batch_size = 10`.

Dann weiter zu Phase 2.

### Phase 2: Leads laden (Batch)

Rufe auf:
```
list_leads(
  campaign_id = <ID>,
  campaign_status = "pending_review",
  fit_level = "",
  research_status = "",
  limit = {batch_size}
)
```

**WICHTIG:** `campaign_status="pending_review"` filtert auf Leads mit generierten, noch nicht freigegebenen Variablen. `fit_level=""` und `research_status=""` MUESSEN explizit gesetzt werden — die Defaults (`qualified`/`researched`) filtern sonst still mit, und pending_review-Leads aus Server-Runs ohne eigene Qualifizierung/Research tauchen NIE im Review auf ("Keine Leads zur Review" trotz pending_review > 0 in list_campaigns).

Merke dir aus der Response:
- `campaign.name` und `campaign.id`
- `total` (Gesamtzahl zu reviewender Leads)
- `remaining` (verbleibend nach diesem Batch)
- Die `leads[]` mit IDs und Basisdaten

Wenn `leads` leer ist: "Keine Leads zur Review. Alle Leads sind bereits freigegeben oder abgelehnt." -> STOP.

### Phase 3: Sub-Agents spawnen (parallel)

Für jeden Lead ausschließlich die tatsächlich verfügbare Agent-Signatur nutzen und den Berechtigungsmodus erben. Keine Umgehungsmodi oder nicht unterstützten Background-Parameter setzen; ohne Parallelisierung sequentiell arbeiten.
- `name`: "verify-{lead.company}" (auf 20 Zeichen begrenzen)
- `description`: "Mailvorschau und Variablen für {lead.company} prüfen"

**WICHTIG:** Spawne ALLE Agents eines Batches in EINEM Message-Block, damit sie parallel laufen.

#### Sub-Agent Prompt Template

Für jeden Lead den folgenden Prompt zusammenbauen. **Ersetze die Platzhalter** mit den tatsächlichen Daten aus der list_leads Response:

```
Du reviewst AI-generierte Variablen für einen Lead via MCP Tools.

KAMPAGNE: {campaign.name} (ID: {campaign.id})
LEAD: {lead.company} (ID: {lead.id})
LEAD VERSANDADRESSE: {lead.sendingEmail || lead.email}
LEAD WEBSITE: {lead.website}

## Schritte

1. Rufe get_lead_variables(campaign_id={campaign.id}, lead_id={lead.id}) auf
2. Lies JEDE Variable in variables[] sorgfältig (name + value)
3. Prüfe Research-Daten und Lead-Stammdaten für Kontext
4. REVIEW — Prüfe JEDE Variable gegen die Verification-Checkliste (siehe unten)
5. ENTSCHEIDUNG (binär):
   a) ALLE Variablen OK -> approve_lead_variables(campaign_id={campaign.id}, lead_id={lead.id})
   b) MINDESTENS EINE Variable unbrauchbar -> reject_lead_variables(campaign_id={campaign.id}, lead_id={lead.id}, reason="...")

## Verification-Checkliste (pro Variable)

Grundlage sind die Abschnitte „Anrede und Ansprache“ und „Intro-Regeln“ des Skills outreach-copy (laden). Prüfe JEDE Variable gegen ALLE folgenden Kriterien:

### Personalisierung
- [ ] Bezug zu Research/Website erkennbar? (nicht generisch)
- [ ] Informationen stimmen mit Lead-Daten überein? (Company, Website, Branche, Stadt)

### Sprache & Stil
- [ ] Umlaute korrekt? (echte Ä/Ö/Ü/ä/ö/ü/ß, nicht AE/OE/UE/ae/oe/ue/ss)
- [ ] Kein "vorallem"? (korrekt: "vor allem")
- [ ] Anrede konsistent zwischen allen Variablen und passend zur Kampagnen-Ansprache (`get_lead_data` → `emailGeneration.salutationRule`)? Nie gemischt.
- [ ] Länge angemessen? (nicht zu kurz, nicht zu lang)
- [ ] Keine Leerzeilen am Anfang oder Ende?
- [ ] Keine M-dashes? (nur normale Bindestriche -)

### Copy-Regeln (outreach-copy)
- [ ] hallo: nur die Begrüßungszeile mit Komma. Gibt der Variablen-Prompt der Kampagne eine eigene Form vor, gilt diese; sonst Format passend zur Ansprache (Du: „Hallo Vorname,“ der Person der Versandadresse, bei generischen Adressen des Entscheiders aus der Recherche, Fallback „Hallo,“ (dann Text im Singular, „dein Team“); Sie: „Hallo Frau/Herr Nachname,“ bzw. „Guten Tag,“)? Nie „Hallo Herr/Frau …“, „Hallo <Firma> Team,“ oder „Hallo zusammen,“, keine Anrede mit ihr/euch, kein erfundener Name oder Titel? Tatsachen über einen Betrieb mit mehreren Personen mit ihr/euer („dass ihr … habt“) sind KEIN Fehler, ein du/ihr-Wechsel im selben Satz schon; Firmenleistungen nie als „du hast …“ an eine Person, die sie nicht selbst erbracht hat.
- [ ] intro: max. 2 Sätze, erster Buchstabe klein, weitere Sätze groß?
- [ ] intro: ausschließlich positiv (Lob/anerkennende Beobachtung), über den Empfänger, kein Problem benannt?
- [ ] intro: keine verbotenen Wörter/Formen („Lücke", „Hürde", „Problem", „leider", „schade", „noch nicht", „fehlt", „begrenzt", „veraltet", „ausbaufähig", „verschenkt Potenzial", Konjunktiv-Wunsch, Ratschlag, Selbstvorstellung/Pitch, Floskel wie „bin auf eure Webseite gestoßen")?
- [ ] intro: Anker nach Rangfolge (Lob aus Bewertungstexten als Paraphrase, Plural nur bei mindestens 2 tragenden Bewertungen > abhebendes Website-Detail > Anzahl und Schnitt nur ab 30 Bewertungen und 4,5, gerundet, mit Komma, bei Widerspruch der kleinere Wert > Fallback); Stellenanzeige als Erkenntnis über den Betrieb, nicht als „du suchst“; zweiter Satz konkret und ohne Vorwegnahme des festen Texts; nichts, das einer anderen Person gehört, der angeschriebenen Person zugeschrieben?
- [ ] intro: kurzer positiver Schluss aus dem Detail vorhanden (Nutzen oder Wirkung, sonst eine kurze Reaktion in der Vergangenheit direkt hinter dem benannten Detail, die es nicht wiederholen muss), kein Prüfer-Urteil über die Qualität der Arbeit („das wirkt vertrauenswürdig“, „da machst du vieles richtig“), ohne Floskel oder Superlativ und ohne Erfundenes (nicht beim Fallback-Satz)? Die Reaktion gibt der Server je Lead aus einer festen Liste vor: Wiederholungen über die Kampagne sind erwartet und kein Befund; gleich lautende Nutzen-Schlüsse (etwa „Interessierte können sich vorab orientieren“ bei Bewertungszahlen) sind einer.
- [ ] intro: besteht den Austauschtest (passt nicht auf zehn andere Betriebe derselben Branche in der Stadt) und nennt nichts von der Sperrliste der Kampagne außer als Bewertungslob, oder ist wörtlich der Fallback-Satz aus dem Prompt?
- [ ] Keine Frage, kein Ausrufezeichen, kein Link, keine sichtbaren Platzhalter ([…], {{…}}) in hallo/intro?
- [ ] Schließt der feste Folgesatz der Entry-Mail („Genau deshalb …" / „Deswegen war ich so frei …") flüssig an, und bleibt die Entry-Mail mit diesem intro unter 120 Wörtern?

### Inhaltliche Korrektheit
- [ ] Keine internen Metriken erwähnt? (SEO-Score, Overall-Score, Fit-Level, Need-Flags, Dimension-Scores, Opportunity Score, ranked Keywords)
- [ ] Keine HTTPS/SSL-Behauptungen? ("ohne HTTPS", "kein SSL" — selbst wenn die Website nur http erreichbar ist)
- [ ] Kein harscher Deficit-Sprech? (ausbaufähig, nicht erreichbar, fehlerhaft, unzureichend, kaum nutzbar, schwach, schlecht)
- [ ] Faktisch korrekt? (keine erfundenen Findings, keine vermeintlichen "Probleme" die nicht existieren)

### Technisch
- [ ] Variable hat Status "success" (nicht "error" oder "skipped")
- [ ] Inhalt ist nicht leer

## Entscheidungslogik

- **approve_lead_variables**: ALLE Variablen passen die Checkliste → freigegeben für CSV-Export
- **reject_lead_variables(reason=...)**: MINDESTENS EINE Variable bricht die Checkliste oder ist grundlegend unbrauchbar:
  - Komplett generischer Text (kein Personalisierungs-Bezug)
  - Falsche Lead-Informationen (falsches Unternehmen, falsche Branche)
  - Interne Metriken im Text (Score-Werte, Fit-Level etc.)
  - Erfundene Findings, die nicht in der Research stehen
  - Anrede-Mix oder andere Style-Bruch
  - Verstoß gegen die Copy-Regeln aus outreach-copy (Kritik-Opener, mehr als 2 Sätze, Großbuchstabe am Anfang, „Hallo Herr/Frau …" oder „Hallo zusammen," oder Anrede mit ihr/euch; ihr/euer für Tatsachen über den Betrieb ist erlaubt)
  - Falsche HTTPS/SSL-Behauptungen

`reason` muss konkret sein (nennt die problematische Variable + den Defekt). Er steht nur im Audit-Log: Beim manuellen Re-Generate via `/outreach-generate` oder `save_lead_variables` den Grund selbst mitgeben; der Server-Lauf liest ihn nicht.

Gib am Ende eine kurze Zusammenfassung zurück:
- Entscheidung: approved / rejected
- Bei rejection: welche Variable + warum
```

### Phase 4: Ergebnisse sammeln & Report

Warte bis ALLE Sub-Agents des Batches fertig sind (sie laufen im Background — du wirst benachrichtigt).

Zähle:
- Freigegeben (approve_lead_variables erfolgreich)
- Abgelehnt (reject_lead_variables erfolgreich)
- Fehler (Agent-Fehler oder Tool-Fehler)

Zeige Batch-Report:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Batch {batch_nr}/{total_batches} abgeschlossen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verarbeitet: {processed}/{total_leads} Leads
Freigegeben: {approved_count} | Abgelehnt: {rejected_count} | Fehler: {error_count}
Verbleibend: {remaining}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 5: Nächster Batch oder Abschluss

Wenn `remaining > 0`: Zurück zu Phase 2 (nächster list_leads Aufruf).

Wenn `remaining == 0` oder keine Leads mehr: Zeige Abschluss-Report:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MCP Verify abgeschlossen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Kampagne: {campaign.name} (ID: {campaign.id})
Gesamt verarbeitet: {total_processed} Leads
Freigegeben: {total_approved} | Abgelehnt: {total_rejected} | Fehler: {total_errors}
Status: Freigegebene Leads auf "approved" gesetzt (ready für CSV-Export)
        Abgelehnte Leads auf "rejected" gesetzt (nicht im Export; siehe Hinweis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**WICHTIG — "rejected" ist NICHT final:** Ein rejected-Lead zählt als generierungsbedürftig — der nächste E-Mail-Run bzw. Re-Generate erzeugt neue Variablen und setzt ihn zurück auf pending_review. Der `reason` landet nur im Audit-Log; die Neu-Generierung des Servers sieht ihn nicht. Soll die Begründung künftige Mails beeinflussen, zusätzlich `set_lead_email_feedback(campaign_id, lead_id, liked=false, comment="<Grund>")` setzen: Die jeweils drei jüngsten Urteile je Richtung fließen als Beispiele in den E-Mail-Prompt der Kampagne (Übersicht mit `list_lead_email_feedback`, Rücknahme mit `delete_lead_email_feedback`). Das Urteil ist unabhängig von approve/reject und verlangt erzeugte Variablenwerte sowie einen E-Mail-Schritt. Soll ein Lead DAUERHAFT raus: aus der Kampagne entfernen oder `mark_leads_contacted(emails=[...], status="do_not_contact")` setzen — dann wird er global von allen AI-Jobs und Exporten ausgeschlossen.

## MCP Tool Reference

### list_campaigns

**Keine Parameter.** Gibt alle Kampagnen des Users zurück.

Response-Felder:
- `campaigns[].id` — Kampagnen-ID
- `campaigns[].name` — Name
- `campaigns[].leadCounts.pending_review` — Anzahl Leads zur Review
- `campaigns[].leadCounts.approved` / `.rejected` — Final-Status-Zähler

### list_leads

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `limit` | int | `10` | Anzahl Leads (1-200) |
| `campaign_status` | string | `"processing"` | Campaign-Status-Filter |

**WICHTIG:** Für den Verify-Workflow immer `campaign_status="pending_review"` verwenden!

### get_lead_variables

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `lead_id` | int | **required** | Lead-ID |

Gibt zurück:
- `campaign` (id, name)
- `lead` (id, email, company, website, score, research, qualification = Urteil DIESER Kampagne mit fitLevel und summary, sonst null)
- `version` — aktuelle Variablen-Version
- `variables[]` — Array mit:
  - `name` — Variablen-Name (z.B. "hallo", "intro")
  - `value` — der generierte Text
  - `status` — "success", "error", "skipped"
  - `errorMessage` — bei status=error
  - `generatedAt` — ISO-Timestamp
- `totalVariables` — Anzahl Variablen

### approve_lead_variables

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `lead_id` | int | **required** | Lead-ID |

Setzt `LeadCampaignStatus.status = approved`. Voraussetzung: mindestens eine `LeadAIVariableValue` muss existieren — sonst `variables_not_found`. Solange für die Kampagne ein Lauf mit E-Mail-Stufe aktiv ist, lehnt das Tool mit `lead_run_active` ab.

Success-Response:
```json
{
  "status": "success",
  "lead_id": 456,
  "campaign_id": 123,
  "variables_approved": 2,
  "campaign_status": "approved"
}
```

### reject_lead_variables

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `lead_id` | int | **required** | Lead-ID |
| `reason` | string | **required** | Ablehnungsgrund (non-empty) |

Setzt `LeadCampaignStatus.status = rejected`. `reason` wird nur im Logger-Audit-Trail festgehalten (leadId, campaignId, userId, reason). Leerer `reason` => `validation_failed`; ohne erzeugte Werte `variables_not_found`; bei aktivem E-Mail-Lauf `lead_run_active`.

Success-Response:
```json
{
  "status": "success",
  "lead_id": 456,
  "campaign_id": 123,
  "variables_rejected": 2,
  "reason": "Variable 'intro' enthält erfundene HTTPS-Behauptung",
  "campaign_status": "rejected"
}
```

## Fehlerbehandlung

| Fehler | Aktion |
|--------|--------|
| `list_leads` gibt leere leads[] | "Keine Leads zur Review" -> STOP |
| Sub-Agent approve/reject Error | Fehler notieren, weitermachen mit nächstem Lead |
| `variables_not_found` | Keine erzeugten Werte — Lead gehört in die Generierung, nicht ins Review |
| `no_contact_email` (approve) | Ab MCP 3.0.0: der Lead hat keine Versandadresse und darf nicht freigegeben werden. Überspringen, im Report nennen; mit `reject_lead_variables` ablehnen, wenn er aus dem Review verschwinden soll |
| `foreign_sending_address` (approve) | Die Versandadresse gehört laut Recherche einem anderen Unternehmen: überspringen, im Report nennen |
| `validation_failed` (reject) | `reason` fehlt oder ist leer — konkreten Grund nachliefern |
| `lead_run_active` | Parallel läuft ein Server-Lauf mit E-Mail-Stufe — Review pausieren, `get_lead_run_status` bis Terminal-Status, dann fortsetzen |
| Sub-Agent Timeout/Crash | Als Fehler zählen, im Report erwähnen |
| Alle Agents eines Batches fehlgeschlagen | Warnung ausgeben, User fragen ob fortfahren |
| Netzwerk/MCP-Verbindungsfehler | 1x Retry, dann STOP mit Fehlermeldung |

**Kein automatischer Retry einzelner Leads** — fehlgeschlagene Leads können später mit `/outreach-verify` erneut verarbeitet werden (sie behalten den Status `pending_review` und tauchen wieder in list_leads auf).

## Wichtige Hinweise

1. **Voll autonom** — Keine Rückfragen während der Review. Durchlaufen bis fertig.
2. **{batch_size}er-Batches** — {batch_size} Leads pro Batch (vom User gewählt, Default 10, Maximum 200).
3. **Parallel** — Alle Agents eines Batches gleichzeitig spawnen (ein Message-Block).
4. **Idempotent** — Freigegebene/abgelehnte Leads tauchen nicht mehr in list_leads(`pending_review`) auf.
5. **Prüfen und Schreiben getrennt** — Der Prüf-Agent urteilt nur (Approve oder Reject im Modus „entscheiden“). Behebbare Befunde (`text`, `recherche`, `adresse`) bessert ein Lead-Agent mit einer vollständigen neuen Version nach (`save_lead_variables`), danach prüft ein neuer Prüf-Agent (siehe „Mit dem verify-agent“, Schritt 4). Keine Inline-Korrektur einzelner Felder.
6. **Audit-Trail** — Reject-Reasons werden via Logger persistiert (siehe `RejectLeadVariablesTool`).
