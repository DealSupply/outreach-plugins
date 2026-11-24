---
name: outreach-setup
description: Richtet das Outreach-Plugin ein und prüft die Einrichtung. Verwenden bei „outreach einrichten“, „setup“, „Plugin einrichten“, „MCP verbinden“, „funktioniert die Verbindung“, „welche Workspaces habe ich“, „Workspace wechseln“, „alte Skills aufräumen“ oder direkt nach der Installation. Führt durch Verbindung, Workspace-Wahl, Prüfung, Aufräumen alter Skill-Kopien und erste Schritte – ohne kostenpflichtige Aktionen.
---

# Outreach einrichten

Ziel: Das Plugin ist installiert, die Verbindung zur Outreach-App steht, es gibt keine doppelten
alten Skills, und der Nutzer weiß, wo er anfängt. **Nichts Kostenpflichtiges** in diesem Ablauf –
keine Lead-Läufe, kein Scraping, keine Generierung. Nur lesende Prüfungen.

## 1. Umgebung erkennen

Stelle fest, wo du läufst, und nenne es dem Nutzer in einem Satz:

| Umgebung | Woran erkennbar | Besonderheit |
|---|---|---|
| Claude Code (Terminal, Desktop-Code-Tab) | Zugriff auf Dateisystem und Shell | Live-Ansicht (Band, Lead-Vorschau) verfügbar |
| Claude App / claude.ai / Cowork | keine lokale Shell | Verbindung im Plugin `outreach`, Reiter „Connectors“ |
| ChatGPT Desktop / Codex | OpenAI-Umgebung | Verbindung beim ersten Aufruf |
| ChatGPT im Browser | OpenAI ohne Plugins | keine Skills aus dem Marketplace; nur die Verbindung über „Plugins“ → „+“ als eigener MCP-Server |
| Cursor & andere | Skills ohne Plugin | MCP separat über die App-Seite „MCP & Skills“ |

## 2. Verbindung prüfen

Rufe `list_campaigns` auf (nur lesend).

- **Antwort kommt:** Verbindung steht. Zusätzlich `ping` aufrufen und die Server-Version nennen. Ab
  `4.0.0` lassen sich Leads auch nur mit Website (ohne E-Mail) importieren; darunter (auch auf 3.x)
  braucht jeder Lead eine E-Mail. Nenne die Zahl der Kampagnen und weiter mit Schritt 3.
- **Kein Outreach-Tool verfügbar oder Anmeldung nötig:** Das Plugin bringt die Verbindung `dealsupply`
  mit (`app.dealsupply.ai`). Angemeldet wird mit den Zugangsdaten von DealSupply.
  **Konto aus Akquise:** Wer bisher nur über Akquise in die App kam, hat oft kein eigenes Passwort,
  und die Anmeldeseite der Verbindung bietet keinen Akquise-Knopf. Dann erst in der App über Akquise
  anmelden (`https://app.dealsupply.ai/sso/akquise` öffnen oder in Akquise auf den Link zu Outreach
  klicken) und danach im selben Browser die Verbindung anmelden. Geht das nicht, auf der Anmeldeseite
  „Passwort vergessen“ wählen und ein Passwort setzen.
  - Claude Code: `/mcp` öffnen → `plugin:outreach:dealsupply` (so heißt die vom Plugin mitgebrachte
    Verbindung dort) → anmelden.
  - Claude App / claude.ai: Customize → Plugins → `outreach` → Reiter „Connectors“ → bei `dealsupply`
    „Connect“ → bei DealSupply anmelden und „Autorisieren“ bestätigen.
  - ChatGPT Desktop / Codex: beim ersten Aufruf anmelden, in Codex alternativ `codex mcp login dealsupply`.
  - Danach `list_campaigns` erneut aufrufen.
- **Zwei Verbindungen zur selben Adresse** (eine von Hand angelegt, eine aus dem Plugin): Eine reicht.
  Dem Nutzer empfehlen, die von Hand angelegte zu entfernen. In Claude Code entsteht sie mit dem
  Befehl aus der App,
  `claude mcp add --scope user --transport http dealsupply https://app.dealsupply.ai/_mcp/v1`,
  und verschwindet mit `claude mcp remove dealsupply` (`claude mcp list` zeigt die Namen). Die
  Verbindung des Plugins (`plugin:outreach:dealsupply`) bleibt dabei bestehen.
- **Alte Verbindung `akquise`** (`outreach.akquise.de`, bis Plugin 0.5.1): Das Plugin bringt sie nicht
  mehr mit; sie wird nicht mehr gepflegt und zeigt noch die alte Marke Akquise. Steht sie noch da (von
  Hand angelegt), dem Nutzer empfehlen, sie zu entfernen (Claude Code `claude mcp remove akquise`, Codex
  `codex mcp remove akquise`, Claude App unter Connectors) und `dealsupply` anzumelden.

Steht die Verbindung, zwei weitere lesende Aufrufe:

- `ping`: Server-Version. Diese Skills setzen MCP 3.0.0 voraus. Liegt die Version darunter, kennt der
  Server noch keine Credits; das dem Nutzer sagen, Server-Läufe rechnen dann über das eigene
  OpenRouter-Konto ab. Abgestimmt sind die Skills auf MCP 4.22.0. Was neuer ist als 3.0.0, nutzen sie
  nur, wenn der Server es kennt:
  - ab 4.0.0 Leads ohne E-Mail (E-Mail oder eigene Website je Lead), ab 4.4.0 der Kampagnen-Export als
    Datei, ab 4.5.0 Workspaces, ab 4.6.0 Power-ups, ab 4.7.0 englische Kampagnen (`campaign.language`;
    auf älteren Servern ist jede Kampagne deutsch);
  - ab 4.8.0 die Close-Werkzeuge (`get_close_status`, `set_close_sync`), ab 4.9.0 die Freigabe einer in
    der App eingerichteten Kampagne (`release_campaign`, Fehler `setup_open`);
  - ab 4.10.0 Intro-Varianten mit Tags (`<name>__anker`, `<name>__schluss`; ältere Server nennen sie nicht
    in `expectedOutput`, dann werden sie auch nicht mitgeschickt);
  - ab 4.11.0 Schwerpunkte und Angebotsblöcke, zwei Personen je Firma, A/B-Varianten im Blueprint und
    `set_offer_focus`; ab 4.12.0 nennt `save_lead_variables` die Korrekturen des Servers (`server_adjusted`);
  - ab 4.15.0 „Angebot je Lead“ (Station-Antworten `offerPerLead`, `offerCards` im Blueprint, Schlüssel
    `angebot` in `get_lead_data` und `save_lead_variables`, Haupt-Angebot als Nummer 1, ungültige
    Nummer abgelehnt, `offer_per_lead_inconsistent` beim halben Umschalten); auf älteren Servern
    (auch 4.14.x, dort war das Haupt-Angebot die letzte Nummer) legt `outreach-campaign` neue
    Kampagnen immer mit einem Angebot für alle an;
  - ab 4.16.0 das Budget eines Server-Laufs in Credits (`budget_credits`, `remove_budget`), das
    Fortsetzen nach einem Budget-Stopp (`resume_lead_run` mit neuem `budget_credits`), offene Leads in
    `lead_counts.open`, neue Fehlercodes (etwa `budget_used_up`, `budget_too_low`, `lead_mutation_busy`
    bei `delete_list`) und die
    Google-Bewertungen am Lead (`lead.googleReviews`). Auf 4.15.0 gelten die bisherigen Regeln; die
    Skills nennen diese Stellen mit „ab 4.16.0 (laut `ping`)“;
  - ab 4.16.0 außerdem Leads finden über Google Maps (`outreach-leads-finden`) und die Personensuche
    (`outreach-personensuche`) und die ähnlichen Firmen (`outreach-aehnliche-firmen`). Auf älteren
    Servern fehlen diese Werkzeuge; die Skills sagen das dem Nutzer dann. Dazu die Google-Kennungen am Lead (`googlePlaceId`, `googleCid`) und `personKey` bei
    Leads aus der Personensuche;
  - ab 4.17.0 Website-Fakten und Firmenfakten am Lead (`lead.websiteFacts`, `lead.companyFacts`); ab
    4.18.0 trägt `agent.additionalPrompt` nur noch die Anweisung des Agenten-Profils; ab 4.19.0 lehnt die
    E-Mail-Suche der Personensuche ohne aktives Abo ab; ab 4.20.0 ist `credits_so_far` einer Suche das
    Berechnete; ab 4.21.0 meldet eine Suche Störungen der Datenquelle (`disrupted_areas`); ab 4.22.0 läuft
    ein Gebiet an der Obergrenze als Rest-Gebiet weiter;
  - ab 4.24.0 tragen Leads aus Leads finden die Attribute `maps_claim_status` und `maps_star_scores` und
    `get_lead_data` die Liste `lead.mapsRanks` (reine Information); ab 4.25.0 kann eine neue
    Personensuche Credits kosten (`search_cost`), ein Tageslimit gibt es dort nicht mehr; ab 4.28.0
    verwirft eine gestoppte E-Mail-Suche die Adresse, die gerade gesucht wird; ab 4.29.0 die Probe je
    Firma (`one_per_company`) und abgeschaltete Stichworte (`keywords_off`) der Personensuche; ab 4.30.0
    speichert `save_lead_variables` einen Gedankenstrich als Komma;
  - ab 4.26.0 fragt `edit_campaign` eigens nach, bevor es Mails ersetzt, die schon in Instantly stehen
    (`confirm_pushed_sequence_change`), und nennt unter `removed`, was es entfernt hat; ab 4.27.0 ändern
    `update_campaign_mail` und `update_campaign_setting` eine einzelne Mail bzw. Einstellung, ohne die
    Kampagne zu ersetzen, und `get_campaign_part` liest einen Teil samt Stand (`outreach-campaign`,
    „Gezielt ändern“). Auf älteren Servern geht das nur über den Vollersatz oder in der App;
  - ab 4.31.0 wählt die App die KI-Modelle, der Nutzer stellt nur Denktiefe und Recherche-Stufe ein
    (Seite Agents); `model_not_priced` und `model_missing` sind dann ein Fall für den Support;
  - ab 4.32.0 der Filter der App für Leads: `describe_lead_filters`, `count_leads`, `list_lead_views`,
    `save_lead_view`, `delete_lead_view` und die Parameter `filter` und `view_id` an den Lead-Werkzeugen
    (`outreach-lists`, „Filter und Ansichten“; Auswahl eines Laufs in `outreach-pipeline`). Auf älteren
    Servern `filter` und `view_id` nie mitschicken;
  - ab 4.37.0 die Option „Eigener KI-Schlüssel“ eines Credit-Kontos (`own_ai_key` in
    `get_credit_balance`, `list_workspaces`, `quote_lead_run` und `start_lead_run`);
  - ab 4.33.0 Fehler und Wünsche an DealSupply melden (`report_feedback`, Melde-Regel im Skill
    `outreach`), nur wenn der Server das Werkzeug anbietet; sonst verweisen die Skills auf „Melden“ in der App;
  - ab 4.34.0 nennt `find_similar_companies` bei Überlast eine Wartezeit (`rate_limited` mit
    `retry_after`); ab 4.36.0 gibt das Zurücksetzen exportierter Leads ältere Übertragungen nur
    gemeinsam frei (`outreach-launch`);
  - ab 4.38.0 lässt der Import einer Kampagne einen Agenten weg, den das Konto nicht hat (`warnings`),
    und Angebot, Start und Fortsetzen eines Laufs nennen ihn (`agent_unavailable`);
  - ab 4.39.0 reicht der Umkreis einer Suche über Leads finden bis 100 km (vorher 50), und weitere
    Gebiete einer Suche dürfen eigene Rezensionen und Filter haben (`search_settings_differ` entfällt);
  - ab 4.40.0 nennt `approve_lead_variables` bei automatischer Übertragung an Instantly die ungeprüften
    Versandadressen (`instantly.unchecked_addresses`, `instantly.only_deliverable`);
  - ab 4.41.0 nennt das Angebot von Leads finden eine Spanne statt einer Zahl (`estimate.range`,
    `credits.expected_low`, `credits.expected_high`), der Status die Spanne je Lauf (`runs[].estimate`)
    und `budget_left`;
  - ab 4.48.0 den Autopiloten einer Kampagne (`outreach-autopilot`): `get_autopilot`,
    `set_up_autopilot`, `suggest_autopilot_search_order`, `start_autopilot_trial`, `switch_autopilot`
    und `answer_autopilot_proposal`. Der Server bietet diese sechs Werkzeuge nur Konten an, für die der
    Autopilot freigeschaltet ist; fehlen sie in der Tool-Liste, sagt der Skill das dem Nutzer.
- `get_credit_balance`: Abrechnungsmodus und Konto. Bei `billing_mode: credits` die verfügbaren Credits
  (`available`) nennen; ein eigener OpenRouter-Key ist dann nicht nötig. Bei `billing_mode: byok`
  zahlt das Konto die KI mit dem eigenen OpenRouter-Key, der in der App hinterlegt sein muss (Seite
  Agents, früher KI-Modell-Einstellungen). Steht bei `billing_mode: credits` zusätzlich `own_ai_key: true`
  (ab MCP 4.37.0), läuft die KI dieses Credit-Kontos über den eigenen OpenRouter-Schlüssel: Das Guthaben
  nennen und dazusagen, dass es Power-ups und Daten zahlt und die KI im Server-Lauf keine Credits kostet.
  Die Option gehört zum Tarif; ein Admin des Workspaces schaltet sie in den Workspace-Einstellungen,
  Reiter KI. Fragt der Nutzer danach und fehlt das Feld oder steht es auf `false`, dorthin verweisen;
  ohne die Option im Tarif fehlt die Kachel dort. In beiden Modi aus `account` die Leads im Account (`leads_in_account` von
  `lead_limit`, `-1` = unbegrenzt) nennen. Steht `subscription_required` auf `true`, gibt es kein
  aktives Abo: Der Nutzer wählt zuerst in der App einen Plan, sonst lässt sich nichts anlegen.

## 2b. Workspace wählen

Rufe `list_workspaces` auf (nur lesend). Eine Verbindung gilt für alle Workspaces des Nutzers.

- **Ein Workspace:** in einem Satz nennen („Du arbeitest im Workspace Muster GmbH.“) und weiter.
- **Mehrere:** kurz zeigen (Name, Rolle, Plan; den Standard mit `default: true` markieren) und
  fragen, in welchem gearbeitet wird. Die Wahl gilt für das ganze Gespräch. Ist es nicht der
  Standard, die Kampagnen mit `list_campaigns(workspace=<uuid>)` neu zählen und Guthaben und Plätze
  mit `get_credit_balance(workspace=<uuid>)` neu lesen (Credits gehören zum Workspace). Wie die Skills den
  Workspace mitgeben: Workspace-Regel im Skill `outreach`.
- **Rolle `viewer`:** sagen, dass dort nur Lesen geht (ansehen und exportieren, kein Import, kein
  Lauf, keine Freigabe).
- **Offene Einladungen** in der Antwort nur nennen; annehmen geht in der App.
- **Kein `list_workspaces`** (älterer Server): Schritt still überspringen, alles läuft im
  Standard-Workspace.

## 3. Alte Skill-Kopien aufräumen (nur Claude Code, Codex, Cursor)

Frühere Installationen per `npx skills add` liegen als Kopien z. B. in `~/.claude/skills/`,
`~/.agents/skills/`, `~/.codex/skills/` oder im Projektordner unter `.claude/skills/`. Sie laden
zusätzlich zum Plugin und sind oft veraltet.

1. Suche Ordner mit den Namen `outreach-*`, `datenbeschaffung*`, `weg-*`, `listen-qualitaet`,
   `impressum-enrichment`, `kontaktseiten-fallback`, `enrichment-waterfall`, `outscraper-bulk`.
2. Zeige die Liste und frage, ob sie gelöscht werden sollen.
3. Erst nach Bestätigung löschen. Danach in Claude Code `/reload-plugins`.

In der Claude App bzw. claude.ai gibt es keine Kopien; dort entfällt der Schritt.

## 4. Datenbeschaffung

Frage: „Willst du neue Leads selbst beschaffen (Apify oder Outscraper im eigenen Konto)?“

- **Ja:** Plugin `datenbeschaffung` aus demselben Marketplace installieren und danach
  `datenbeschaffung-setup` ausführen (Apify-Zugang prüfen)
  (Claude Code: `/plugin install datenbeschaffung@outreach-plugins`; Claude App: Customize →
  Plugins → `datenbeschaffung`; Codex: `/plugins`).
- **Nein:** überspringen. Leads lassen sich jederzeit per CSV importieren (`outreach-import`).

## 5. Updates einschalten (Claude Code)

In Claude Code sind Updates fremder Marketplaces standardmäßig aus. Empfehlen:
`/plugin` → Marketplaces → `outreach-plugins` → Auto-Update einschalten. Sonst `outreach-update`.

## 6. Erste Schritte

- **Claude Code:** Die Live-Ansicht zeigt Lead-Vorschauen und laufende Lead-Runs über dem Prompt;
  `/outreach-status` holt alle laufenden Läufe ins Band (`zu`/`auf` klappt es ein und aus).
- Weiter mit dem Einstieg `outreach` oder direkt mit `outreach-campaign`.
- Kam der Nutzer mit einem Start-Satz aus der App („Richte mit outreach die Kampagne #123 ein.“),
  nach der Einrichtung direkt damit weiter: `outreach-campaign`, Ablauf „Genannte leere Kampagne
  füllen“, mit der Nummer aus dem Satz.

## Abschluss

Kurz berichten: Umgebung, Verbindung (ja/nein, Anzahl Kampagnen, Server-Version), Workspace (Name
und Rolle, bei mehreren der gewählte), Abrechnungsmodus (Credits mit verfügbarem Guthaben, Credits mit eigenem
KI-Schlüssel oder eigener OpenRouter-Key), Leads im Account, aufgeräumte Kopien, Datenbeschaffung installiert ja/nein,
Auto-Update ja/nein.
