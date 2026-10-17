---
name: outreach-generate
description: Use when user says "outreach:generate", "mcp:generate", "generiere emails", "email generation", "MCP workflow", "generate emails for campaign", or triggers /mcp:generate.
---

# MCP Generate — AI-Variablen-Generierung

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

Dieser Skill orchestriert die vollautomatische AI-Variablen-Generierung für Leads via MCP Business Tools. Claude generiert AI-Variablen basierend auf Research, Qualification und Custom Attributes, und speichert sie via `save_lead_variables`. Email-Body und Subject werden NICHT durch diesen Skill erzeugt — sie sind in der Email-Sequenz hardcoded und werden beim CSV-Export live mit den Variablen gerendert. Dieser Skill ist der **Manuell-Modus**; Standard ist der serverseitige Lauf via `/outreach-pipeline` (Tool `start_lead_run`, Stufe `email`). Vor dem Start `list_lead_runs(campaign_id, active_only=true)` prüfen: bei aktivem Lauf mit E-Mail-Stufe blockt `save_lead_variables` mit `lead_run_active`.

> **Abo-Lauf (Subagents im Claude- bzw. ChatGPT-Abo):**
> - **Ein Lead pro Agent, immer.** Nie mehrere Leads in einen Agenten geben – Modelle verwechseln sonst Leads.
> - **Agent:** In Claude Code und Cowork `outreach:lead-agent` (Plugin-Agent, Haiku) mit dem Auftrag „Kampagne <id>, Lead <id>, nur Mail-Variablen“; sind mehrere Outreach-Server verbunden, zusätzlich „Server: <name>“. Fehlt der Agent, `general-purpose` mit `model: "sonnet"` und der Vorlage unten. Nie das Modell der Sitzung erben lassen: Opus verbraucht das Abo-Kontingent um ein Vielfaches. Andere Clients: das günstigste Modell mit Web-Zugriff; ohne Subagents die Leads **sequentiell** mit denselben Schritten.
> - **Ganzer Lauf** (Qualifizierung → Recherche → Mail in einem): `/outreach-pipeline <id> --abo`.
> - **Parallelität:** höchstens 10 Agents gleichzeitig. Mehr als eine Handvoll Leads in Claude Code: als Workflow nach `outreach-abo-lauf` mit `stufen: "nur Mail-Variablen"` – die Sitzung liest dann ein Ergebnis statt jeder einzelnen Agent-Meldung und verbraucht so ein Vielfaches weniger.
> - **Fortschritt:** Gibt es das Werkzeug `outreach_progress` (Claude Code mit Plugin `outreach`), zu Beginn einmal `outreach_progress(action="start", campaign_id, phase="email", total=<Leads>)` aufrufen; gezählt wird automatisch, auch jeder Schreibaufruf der Subagents. Den Stand danach aus den Agenten-Antworten berichten, nicht per `list_leads` erneut auflisten, und die Phase mit `outreach_progress(action="end", …)` schließen, damit Leads ohne Schreibaufruf nicht offen im Band hängen.

## Phase 0: Umgebung und Konfiguration prüfen

Vor jeder Generierung `ping` und `list_campaigns` mit dem Auftrag abgleichen (richtige Kampagne, Variablen und E-Mail-Sequenz vorhanden); bei Unklarheit stoppen. Die vollständige Konfiguration (E-Mail-Schritte, AI-Variablen, Kampagnenkontext) liefert `export_campaign_blueprint(campaign_id)`. Einen einzelnen Variablen-Prompt ändert `update_ai_variable`; Änderungen an Schritten oder mehreren Variablen laufen über `edit_campaign` mit dem vollständigen Blueprint (Replace-all, kein Teil-Patch). Bereits generierte Werte bleiben dabei erhalten (Abgleich per Name), stammen aber aus dem alten Prompt; eine Neugenerierung nur mit ausdrücklicher Zustimmung des Users und nie während eines aktiven Laufs.

Ansprache und Kampagnenkontext kommen pro Lead aus `get_lead_data` (`emailGeneration.salutation`, `salutationRule`, `campaignContext`); die Ansprache gilt durchgängig für alle Variablen eines Leads. Den fertigen Text einzelner Leads prüfst du nicht über ein Vorschau-Tool, sondern über `get_lead_variables` nach dem Speichern.

**Copy-Regeln (Pflicht):** Bevor `hallo` oder `intro` für einen Lead geschrieben wird, den Skill `outreach-copy` laden und dessen Abschnitte „Anrede und Ansprache“ und „Intro-Regeln“ einhalten. Der Orchestrator lädt den Skill EINMAL und hängt beide Abschnitte wörtlich an jeden Agenten-Prompt an; die Subagents laden ihn nicht selbst (spart Kontext je Lead). Der Variablen-Prompt der Kampagne geht vor, solange er diesen Regeln nicht widerspricht; widerspricht er ihnen (z. B. Kritik-Opener, „Hallo Herr …“ bei Du-Form), vor dem Start den Nutzer darauf hinweisen und die Prompts über `/outreach-campaign` korrigieren lassen, statt gegen die Regeln zu generieren.

## Workflow-Übersicht

```
1. list_campaigns -> Kampagne identifizieren (oder campaign_id aus Argument)
   |
2. list_leads(campaign_id, limit={batch_size})
   -> {batch_size} Leads mit Basisdaten (~0.5 KB/Lead)
   |
3. Für jeden Lead: Sub-Agent spawnen (parallel, bis zu {batch_size} gleichzeitig)
   -> Jeder Agent: get_lead_data() -> generiert Variablen -> save_lead_variables()
   |
4. Batch-Report: "Batch 1/N done, X/Y leads processed"
   |
5. Nächster Batch: list_leads erneut (remaining > 0?)
   |
6. Fertig: "Y Leads verarbeitet, Variablen bereit für Review"
```

## Aufruf

| Eingabe | Verhalten |
|---------|-----------|
| `/outreach-generate` | Zeigt Kampagnen via list_campaigns, User wählt |
| `/outreach-generate 76` | Startet direkt für Kampagne 76 |
| `generiere emails für kampagne 76` | Startet direkt für Kampagne 76 |

## Schritt-für-Schritt Anleitung

### Phase 1: Kampagne bestimmen

Wenn KEINE campaign_id als Argument übergeben wurde:

1. Rufe `list_campaigns` auf (MCP Tool)
2. Zeige dem User die Kampagnen mit `leadCounts.needs_email_generation > 0`
3. Frage: "Für welche Kampagne soll ich Variablen generieren?"
4. Merke dir die campaign_id
5. Vorprüfung: `list_lead_runs(campaign_id, active_only=true)` — läuft ein serverseitiger Lauf mit E-Mail-Stufe, lehnt `save_lead_variables` mit `lead_run_active` ab (Rennschutz). Erst nach Terminal-Status starten (`get_lead_run_status`) oder den Lauf nach Rücksprache mit `cancel_lead_run` stoppen (bereits laufende Jobs laufen aus).

Wenn campaign_id als Argument übergeben wurde: Direkt zur Batch-Größe-Abfrage.

**Batch-Größe abfragen:**

Frage den User:
"Wie viele Leads pro Batch? (Default: 10)"
- 10 (Standard)
- 50
- 100
- 200 (Maximum)

Gleichzeitig laufen höchstens 10 Agents (siehe „Abo-Lauf“); größere Batches werden in Wellen abgearbeitet.

Merke dir die Antwort als `{batch_size}`. Wenn der User einfach Enter drückt oder nichts sagt: `batch_size = 10`.

Dann weiter zu Phase 2.

### Phase 2: Leads laden (Batch)

Gibt der Auftrag einen `list_leads`-Aufruf (Listen-Modus mit `run_stages`, etwa aus dem Startdialog der App) oder Lead-IDs vor, gilt genau diese Auswahl statt der Abfrage unten: den Aufruf einmal unverändert ausführen und die Leads aus `lead_ids` nehmen; fehlt in der Antwort `applied_filters`, ist der Server älter als MCP 2.1.0 oder die Verbindung veraltet, dann abbrechen und das melden. Nicht mit `offset` blättern.

Rufe auf:
```
list_leads(
  campaign_id = <ID>,
  limit = {batch_size}
)
```

Merke dir aus der Response:
- `campaign.name` und `campaign.id`
- `total` (Gesamtzahl zu verarbeitender Leads)
- `remaining` (verbleibend nach diesem Batch)
- Die `leads[]` mit IDs und Basisdaten

Wenn `leads` leer ist: "Keine Leads zur Verarbeitung. Alle Leads haben bereits generierte Variablen." -> STOP.

### Phase 3: Sub-Agents spawnen (parallel)

Für jeden Lead genau einen Agent, Typ und Modell nach „Abo-Lauf“ oben; nur die tatsächlich vom Client unterstützte Agent-Signatur verwenden. Berechtigungsmodus unverändert erben; kein `bypassPermissions`, keine erfundenen `run_in_background`-Parameter. Falls der Client keine Parallelisierung unterstützt, sequentiell arbeiten.
- `name`: "gen-{lead.company}" (auf 20 Zeichen begrenzen)
- `description`: "Variablen für {lead.company} generieren"
- `prompt`: das folgende vollständige Lead-Briefing

**WICHTIG:** Spawne die Agents einer Welle (höchstens 10) in EINEM Message-Block, damit sie parallel laufen.

#### Sub-Agent Prompt Template

Für jeden Lead den folgenden Prompt zusammenbauen. **Ersetze die Platzhalter** mit den tatsächlichen Daten aus der list_leads Response:

```
Du generierst AI-Variablen für einen Lead via MCP Tools.

KAMPAGNE: {campaign.name} (ID: {campaign.id})
LEAD: {lead.company} (ID: {lead.id})

## Schritte

1. Rufe get_lead_data(campaign_id={campaign.id}, lead_id={lead.id}) auf
2. Lies den emailGeneration.systemPrompt sorgfältig — er definiert Ton, Stil und Kontext; dazu emailGeneration.salutation/salutationRule (Ansprache) und campaignContext. Halte die Copy-Regeln „Anrede und Ansprache“ und „Intro-Regeln“ ein, die unten an diesen Auftrag angehängt sind
3. Analysiere Research, Qualification und Custom Attributes
4. Optional: Besuche die Lead-Website (lead.website), falls dein Client Websites laden kann — get_lead_data liefert KEINE Screenshots
5. Generiere für JEDE Variable in emailGeneration.variables[] den Text gemäß ihrem Prompt
6. REVIEW — Prüfe JEDE generierte Variable gegen diese Checkliste:
   - Umlaute korrekt geschrieben? (Ä/Ö/Ü/ä/ö/ü/ß — NIEMALS AE/OE/UE/ae/oe/ue/ss)
   - Keine internen Metriken erwähnt? (SEO-Score, Overall-Score, Fit-Level, Need-Flags, Dimension-Scores, Opportunity Score, ranked Keyword)
   - Keine HTTPS/SSL-Behauptungen? ("ohne HTTPS", "kein SSL" etc.)
   - Kein harscher Deficit-Sprech? (ausbaufähig, nicht erreichbar, fehlerhaft, unzureichend, kaum nutzbar, schwach, schlecht)
   - Anrede gemäß emailGeneration.salutationRule und konsistent über alle Variablen? (nie gemischt)
   - hallo: nur die Begrüßungszeile mit Komma? Du-Form „Hallo Vorname,“ (Person der Versandadresse, bei generischen Adressen der Entscheider aus der Recherche), Fallback „Hallo,“ (dann Text im Singular, „dein Team“); Sie-Form „Hallo Frau/Herr Nachname,“ bzw. „Guten Tag,“; nie „Hallo Herr/Frau …“ bei Du-Form, kein erfundener Name oder Titel?
   - intro: max. 2 Sätze (etwa 30 Wörter), erster Buchstabe klein, weitere Sätze groß, ausschließlich positiv, über den Empfänger, belegter Anker nach Rangfolge (Lob aus Bewertungstexten > abhebendes Website-Detail, auch Stellenanzeige als Erkenntnis statt „du suchst“ > Anzahl und Schnitt nur ab 30 Bewertungen und 4,5, gerundet, mit Komma > Fallback-Satz aus dem Prompt)? Besteht er den Austauschtest (passt nicht auf zehn andere Betriebe derselben Branche in der Stadt) und steht nicht auf der Sperrliste der Kampagne (außer als Bewertungslob)? Folgt ein kurzer positiver Schluss aus dem Detail (Nutzen oder Wirkung, sonst eine kurze Reaktion am benannten Detail, nie ein Prüfer-Urteil über die Qualität der Arbeit), ohne Floskel und nichts erfunden (nicht beim Fallback)? Einstieg nach der letzten Ziffer der Lead-ID, bei Bewertungen mit Quelle? Nichts einer anderen Person Gehörendes zugeschrieben?
   - intro ohne Verbotenes? (Kritik, „Lücke“, „Problem“, „noch nicht“, „fehlt“, „veraltet“, Konjunktiv-Wunsch, Ratschlag, Selbstvorstellung/Pitch, Floskel, erfundene Zahl, Frage, Link, Platzhalter in Klammern, Gedankenstrich als Trenner)
   - Schließt der feste Folgesatz der Entry-Mail flüssig an das intro an?
   - Kein "vorallem"? (korrekt: "vor allem")
   - Keine Leerzeilen am Anfang oder Ende einer Variable?
   - Jede Variable unter 10.000 Zeichen?
   Falls ein Kriterium verletzt: Korrigiere die Variable und prüfe erneut.
7. Speichere via save_lead_variables(campaign_id={campaign.id}, lead_id={lead.id}, variables=JSON-String)

WICHTIG: variables ist ein JSON-STRING. ALLE Variablen aus emailGeneration.expectedOutput müssen enthalten sein.

# Copy-Regeln (aus dem Skill outreach-copy)

{Abschnitte „Anrede und Ansprache“ und „Intro-Regeln“ wörtlich einfügen}
```

### Phase 4: Visueller Kontext (optional)

`get_lead_data` liefert KEINE Screenshots — die visuelle Beurteilung der Server-Runs ist im Research-TEXT zusammengefasst. Wenn dein Client selbst Websites besuchen kann (Browser/Fetch): die Lead-Website (`lead.website`) kurz öffnen und den Eindruck in die Generierung einbeziehen. Andernfalls auf Basis von Research-Text, Qualification und Custom Attributes generieren — im Report vermerken: "Website nicht besucht, Text-basierte Generierung."

### Phase 5: Ergebnisse sammeln & Report

Warte bis ALLE Sub-Agents des Batches fertig sind (sie laufen im Background — du wirst benachrichtigt).

Zähle:
- Erfolgreiche Generierungen (`save_lead_variables` liefert das unveränderte Erfolgs-Payload mit `status: "success"`)
- Fehler (`save_lead_variables` liefert ein MCP-Tool-Result mit `isError: true`; der Text beginnt mit einem Code wie `validation_failed:` oder `contact_gate:` — oder der Agent selbst ist fehlgeschlagen)

Zeige Batch-Report:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Batch {batch_nr}/{total_batches} abgeschlossen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verarbeitet: {processed}/{total_leads} Leads
Erfolg: {success_count} | Fehler: {error_count}
Verbleibend: {remaining}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 6: Nächster Batch oder Abschluss

Wenn `remaining > 0`: Zurück zu Phase 2 (nächster list_leads Aufruf). **Schleifenschutz:** Kommen im nächsten Batch dieselben Lead-IDs zurück, die eben schon bearbeitet wurden (z. B. weil sie ohne Versandadresse mit `no_contact_email` übersprungen wurden), abbrechen und dem Nutzer die IDs nennen, statt sie erneut zu bearbeiten.

Wenn `remaining == 0` oder keine Leads mehr: Zeige Abschluss-Report:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MCP Generate abgeschlossen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Kampagne: {campaign.name} (ID: {campaign.id})
Gesamt verarbeitet: {total_processed} Leads
Erfolg: {total_success} | Fehler: {total_errors}
Status: Verarbeitete Leads auf "pending_review" gesetzt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nächster Schritt: Stichprobe mit /outreach-verify (10 Leads) bei neuer Kampagne, nach Änderungen oder vor dem ersten Export; danach freigeben
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## MCP Tool Reference

### list_campaigns

**Keine Parameter.** Gibt alle Kampagnen des Users zurück.

Response-Felder:
- `campaigns[].id` — Kampagnen-ID
- `campaigns[].name` — Name
- `campaigns[].lifecycle` — Lebenszyklus der Kampagne
- `campaigns[].emailSequence` — E-Mail-Sequenz (id, stepCount) oder null
- `campaigns[].leadCounts.needs_email_generation` — Anzahl Leads in der Generierungs-Queue (qualifiziert IN DIESER Kampagne, recherchiert, `processing`; Urteile gelten pro Kampagne)
- `campaigns[].leadCounts.pending_review` — Anzahl Leads mit generierten, noch nicht freigegebenen Variablen
- `campaigns[].leadCounts.approved` / `.rejected` — Final-Status
- `campaigns[].aiVariables[]` — Konfigurierte AI-Variablen (Name + sortOrder)

### list_leads

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `limit` | int | `10` | Anzahl Leads (1-200) |
| `fit_level` | string | `"qualified"` | Qualification-Filter |
| `research_status` | string | `"researched"` | Research-Status-Filter |
| `campaign_status` | string | `"processing"` | Campaign-Status-Filter |
| `qualification_status` | string | `''` | Qualification-Status-Filter: '' (alle), 'pending' (inkl. nie qualifiziert), 'processing', 'completed', 'failed' |
| `contact_status` | string | `''` | Leer: bereits kontaktierte Leads ausgeblendet; `"all"` zeigt alle, ein Status-Slug filtert darauf |
| `offset` | int | `0` | Paginierung zusammen mit `limit` und den Antwortfeldern `total`/`remaining` |

Gibt nur Basisdaten zurück: id, email, company, website, city, phoneNumber, score, contactStatus (mit contactedAt, contactSource), qualification (fitLevel, category, summary).

**WICHTIG:** Der Default `campaign_status="processing"` ist korrekt für den Generierungs-Workflow (= Leads mit Status "Ausstehend").

Ab MCP 2.1.0 hat `list_leads` zusätzlich einen Listen-Modus: Mit `run_stages` oder den Filtern der Lead-Liste (`search_text`, `score_min`, `cities`, `sort_by`, `take` …) liefert es genau die Auswahl der App samt `lead_ids` und `applied_filters`. Die Parameter beschreibt die Tool-Beschreibung des Servers; ein solcher Aufruf kommt meist fertig aus dem Startdialog der App.

### get_lead_data

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `lead_id` | int | **required** | Lead-ID |

Gibt vollen Generierungs-Context zurück. Bei bereits kontaktierten Leads (Kontaktstatus blockiert) antwortet das Tool mit `contact_gate` — Lead überspringen:
- Stammdaten (email, company, website, city, phoneNumber, score, sendingEmail, secondaryEmails, contactStatus) und `appUrl`-Links
- `qualification` — Urteil DIESER Kampagne (status, fitLevel, category, summary, completedAt, snapshot); in einer anderen Kampagne qualifizierte Leads zeigen hier ein leeres Urteil
- `research` (text, bestEmail, decisionMaker, contactRecommendation)
- `customAttributes` (key-value Paare)
- `emailGeneration.systemPrompt` — Der aufgelöste System-Prompt
- `emailGeneration.salutation` / `salutationRule` / `campaignContext` — Ansprache und Kampagnenkontext
- `emailGeneration.variables[]` — Variablen mit aufgelösten Prompts
- `emailGeneration.expectedOutput` — JSON-Schema der erwarteten Ausgabe (Variablen-Namen)

### save_lead_variables

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `campaign_id` | int | **required** | Kampagnen-ID |
| `lead_id` | int | **required** | Lead-ID |
| `variables` | string | **required** | JSON-String mit generierten Werten |

**variables-Format:** `"{\"hallo\": \"...\", \"intro\": \"...\"}"`

Verhalten: Persistiert eine neue `LeadAIVariableValue`-Version pro Variable (vorherige Versionen bleiben als Historie erhalten). Setzt `LeadCampaignStatus.status = pending_review`. Berührt KEINE Email-Steps (Body/Subject werden beim CSV-Export live aus den Variablen gerendert).

Success-Response:
```json
{
  "status": "success",
  "lead_id": 456,
  "campaign_id": 123,
  "version": 1,
  "variables_saved": 2,
  "campaign_status": "pending_review"
}
```

Fehler bei fehlenden Variablen: Das MCP-Tool-Result trägt `isError: true`; sein TextContent lautet:

```text
validation_failed: Variable(s) missing from submission: 'intro'
```

Die fehlenden Namen stehen im Fehlertext — alle Variablen aus `emailGeneration.expectedOutput` nachliefern und erneut senden.

Das Tool liefert nur den Text `<lowercase_code>: <message>` und keine strukturierte Fehler-Response. Mögliche Codes: `validation_failed` (ungültiges JSON oder fehlende Variablen), `contact_gate` (Kontaktstatus des Leads blockiert: Lead überspringen), `no_contact_email` (ab MCP 3.0.0: der Lead hat keine Versandadresse, weder importiert noch von der Recherche gefunden: Lead überspringen, nicht wiederholen), `foreign_sending_address` (die Versandadresse gehört laut Recherche einem anderen Unternehmen: Lead überspringen), `variables_not_configured` (Kampagne hat keine AI-Variablen), `campaign_not_found`, `lead_not_found`, `lead_not_in_campaign`, `lead_run_active`, `insufficient_scope` und `internal_error`. Ist ein Wert kein String, speichert das Tool die Variable mit Status `error`.

### Verification-Tools (siehe `/outreach-verify`)

Die folgenden Tools werden im Verification-Workflow verwendet, NICHT in der Generierung:

- **get_lead_variables** — lädt aktuelle Variablen-Werte (Name, Wert, Status, generatedAt) zur Prüfung
- **approve_lead_variables** — gibt Variablen frei (`LeadCampaignStatus = approved`, ready für CSV-Export)
- **reject_lead_variables** — lehnt Variablen ab mit `reason` (`LeadCampaignStatus = rejected`; NICHT final: der Lead zählt wieder als generierungsbedürftig und wird beim nächsten Generate/Run neu erzeugt. Dauerhaft raus = aus Kampagne entfernen oder `mark_leads_contacted(emails, status="do_not_contact")`)

Details: siehe `/outreach-verify` Skill.

## Fehlerbehandlung

| Fehler | Aktion |
|--------|--------|
| `list_leads` gibt leere leads[] | "Keine Leads in Queue" -> STOP |
| Sub-Agent save_lead_variables Error | Fehler notieren, weitermachen mit nächstem Lead |
| `no_contact_email` | Kein Fehler: der Lead hat keine Versandadresse und bekommt keine Mail. Als „ohne Adresse“ zählen, nicht wiederholen. Die Standard-Warteschlange (`list_leads`) enthält solche Leads ab MCP 3.0.0 nicht; tauchen sie trotzdem auf, greift der Schleifenschutz aus Phase 6 |
| `lead_run_active` | Parallel läuft ein Server-Lauf mit E-Mail-Stufe — Batch pausieren, `get_lead_run_status` bis Terminal-Status, dann fortsetzen (Queue ist idempotent) |
| Sub-Agent Timeout/Crash | Als Fehler zählen, im Report erwähnen |
| Alle Agents eines Batches fehlgeschlagen | Warnung ausgeben, User fragen ob fortfahren |
| Netzwerk/MCP-Verbindungsfehler | 1x Retry, dann STOP mit Fehlermeldung |

**Kein automatischer Retry einzelner Leads** — fehlgeschlagene Leads können später mit `/outreach-generate` erneut verarbeitet werden (sie haben noch keinen `pending_review`-Status und tauchen wieder in list_leads auf).

## Wichtige Hinweise

1. **Voll autonom** — Keine Rückfragen während der Generierung. Durchlaufen bis fertig.
2. **{batch_size}er-Batches** — {batch_size} Leads pro Batch (vom User gewählt, Default 10, Maximum 200).
3. **Parallel** — höchstens 10 Agents gleichzeitig (ein Message-Block je Welle), ein Lead pro Agent.
4. **Idempotent** — Leads mit bereits generierten Variablen tauchen nicht mehr in list_leads (default-filter `campaign_status="processing"`) auf.
5. **Versionierung** — Jeder save_lead_variables-Aufruf erzeugt eine neue Version, ältere Versionen bleiben als Historie erhalten.
