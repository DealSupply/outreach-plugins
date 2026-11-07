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
- **Kein Outreach-Tool verfügbar oder Anmeldung nötig:**
  - **DealSupply-Kunden:** Das Plugin bringt die Verbindung `dealsupply` mit (`app.dealsupply.ai`).
    - Claude Code: `/mcp` öffnen → `dealsupply` → anmelden.
    - Claude App / claude.ai: Customize → Plugins → `outreach` → Reiter „Connectors“ → bei `dealsupply`
      „Connect“ → bei DealSupply anmelden und „Autorisieren“ bestätigen.
    - ChatGPT Desktop / Codex: beim ersten Aufruf anmelden, in Codex alternativ `codex mcp login dealsupply`.
  - **Kunden einer anderen Outreach-App:** Die mitgelieferte Verbindung `dealsupply` nicht hinzufügen.
    Den MCP der eigenen App über deren Seite „MCP & Skills“ hinzufügen; Skills und Live-Ansicht
    erkennen ihn automatisch an seinen Tools, der Name ist egal.
  - Danach `list_campaigns` erneut aufrufen.
- **Zwei Verbindungen zur selben Adresse** (eine von Hand angelegt, eine aus dem Plugin): Eine reicht.
  Dem Nutzer empfehlen, die von Hand angelegte zu entfernen.
- **Alte Verbindung `akquise`** (`outreach.akquise.de`, bis Plugin 0.5.1): Die Adresse entfällt, das
  Plugin bringt sie nicht mehr mit. Steht sie trotzdem noch da (von Hand angelegt), dem Nutzer
  empfehlen, sie zu entfernen (Claude Code `/mcp`, Codex `codex mcp remove akquise`, Claude App unter
  Connectors) und `dealsupply` anzumelden.

Steht die Verbindung, zwei weitere lesende Aufrufe:

- `ping`: Server-Version. Diese Skills setzen MCP 3.0.0 voraus. Liegt die Version darunter, kennt der
  Server noch keine Credits; das dem Nutzer sagen, Server-Läufe rechnen dann über das eigene
  OpenRouter-Konto ab. Abgestimmt sind die Skills auf MCP 4.12.0. Was neuer ist als 3.0.0, nutzen sie
  nur, wenn der Server es kennt:
  - ab 4.0.0 Leads ohne E-Mail (E-Mail oder eigene Website je Lead), ab 4.4.0 der Kampagnen-Export als
    Datei, ab 4.5.0 Workspaces, ab 4.6.0 Power-ups, ab 4.7.0 englische Kampagnen (`campaign.language`;
    auf älteren Servern ist jede Kampagne deutsch);
  - ab 4.8.0 die Close-Werkzeuge (`get_close_status`, `set_close_sync`), ab 4.9.0 die Freigabe einer in
    der App eingerichteten Kampagne (`release_campaign`, Fehler `setup_open`);
  - ab 4.10.0 Intro-Varianten mit Tags (`<name>__anker`, `<name>__schluss`; ältere Server nennen sie nicht
    in `expectedOutput`, dann werden sie auch nicht mitgeschickt);
  - ab 4.11.0 Schwerpunkte und Angebotsblöcke, zwei Personen je Firma, A/B-Varianten im Blueprint und
    `set_offer_focus`; ab 4.12.0 nennt `save_lead_variables` die Korrekturen des Servers (`server_adjusted`).
- `get_credit_balance`: Abrechnungsmodus und Konto. Bei `billing_mode: credits` die verfügbaren Credits
  (`available`) nennen; ein eigener OpenRouter-Key ist dann nicht nötig. Bei `billing_mode: byok`
  zahlt das Konto die KI mit dem eigenen OpenRouter-Key, der in den KI-Modell-Einstellungen der App
  hinterlegt sein muss. In beiden Modi aus `account` die Leads im Account (`leads_in_account` von
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
und Rolle, bei mehreren der gewählte), Abrechnungsmodus (Credits mit verfügbarem Guthaben oder eigener
OpenRouter-Key), Leads im Account, aufgeräumte Kopien, Datenbeschaffung installiert ja/nein,
Auto-Update ja/nein.
