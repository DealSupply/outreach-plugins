---
name: fulfillment-setup
description: Richtet das Plugin fulfillment ein und prüft die Voraussetzungen. Verwenden bei „Fulfillment einrichten“, „Demos einrichten“, „Netlify verbinden“, „RankM8 verbinden“, „funktioniert mein Fulfillment“ oder direkt nach der Installation des Plugins. Prüft Outreach-Verbindung, die Plugins outreach und datenbeschaffung, Netlify, optional RankM8, räumt alte Skill-Kopien auf – ohne kostenpflichtige Schritte.
---

# Fulfillment einrichten

Ziel: Alles steht, damit `fulfillment` und die `demo-*`-Skills ohne Hänger durchlaufen. **Nichts
Kostenpflichtiges** in diesem Ablauf; nur lesende Prüfungen.

## 1. Umgebung erkennen

Claude Code (Shell und Dateisystem), Claude App / claude.ai / Cowork (keine Shell), ChatGPT
Desktop / Codex oder ein anderes KI-Werkzeug. In einem Satz nennen; was je Umgebung geht, steht in
`../fulfillment-referenzen/references/umgebungen.md`.

## 2. Outreach-Verbindung prüfen

- `list_campaigns` aufrufen (nur lesend).
  - **Antwort kommt:** Verbindung steht, Anzahl der Kampagnen nennen.
  - **Kein Outreach-Tool:** Das Plugin `outreach` aus demselben Marketplace installieren (bringt die
    Verbindung mit) und dort `outreach-setup` ausführen. Ohne Verbindung geht Fulfillment trotzdem,
    aber Offer und Lead-Daten kommen dann vom Nutzer, und der Demo-Link wird von Hand eingetragen.
- Schreibrecht für den Demo-Link: Der Link wird über `bulk_set_lead_attributes` gespeichert
  (Berechtigung `leads:write`). Nicht testweise schreiben; erst beim ersten echten Link zeigt sich,
  ob das Recht fehlt.

## 3. Plugins im selben Marketplace

| Plugin | Gebraucht von | Fehlt es |
|---|---|---|
| `outreach` | `demo-akquise-kampagne` (Regeln aus `outreach-copy`), Offer-Formulierung | installieren: `outreach@outreach-plugins` |
| `datenbeschaffung` | `demo-leadliste` | nur nötig, wenn Leadlisten als Offer geplant sind |

## 4. Netlify (für das Veröffentlichen)

Frage: „Hast du ein Netlify-Konto?“ Ohne Konto werden Demos nach einer Stunde entfernt
(`../fulfillment-referenzen/references/netlify.md`).

- **Kein Konto:** auf netlify.com anlegen lassen. Der Gratisplan reicht für etwa 20
  Veröffentlichungen im Monat; bei mehr Demos den Personal-Plan erwähnen (`netlify.md`).
- **Connector (optional, empfohlen in claude.ai und Claude Code):** Netlify-Tools vorhanden? Wenn
  nein: claude.ai/App → Customize → Connectors → Netlify; Claude Code →
  `claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp`, dann `/mcp`.
- **Ohne Connector:** Netlify Drop (Drag & Drop) reicht völlig.

## 5. RankM8 (optional, für `demo-seo`)

Nur nötig für Suchbegriffe, Positionen und lokale Suche. Erkennbar an den Tools `domain_keywords`
und `serp_search`; mit dem Tool `quick_check` (Schnellcheck mit fertigem Report-Link) geht
`demo-seo` am schnellsten.

- **Kein RankM8-Konto:** `demo-seo` liefert dann nur die Bausteine ohne Messdaten (Titel,
  KI-Suchmaschinen). Ein Konto gibt es auf rankm8.com.
- **Konto vorhanden, Tools fehlen:** Verbindung hinzufügen.
  - claude.ai / App: Customize → Connectors → eigenen Connector hinzufügen → Adresse
    `https://app.rankm8.com/_mcp/v1` → anmelden.
  - Claude Code: `claude mcp add --transport http rankm8 https://app.rankm8.com/_mcp/v1`, dann `/mcp`.
- Prüfen ohne Kosten: `list_projects` aufrufen. Antwort kommt = verbunden.

## 6. Alte Skill-Kopien aufräumen (nur Claude Code, Codex, Cursor)

Frühere Installationen per `npx skills add` liegen als Kopien z. B. in `~/.claude/skills/`,
`~/.agents/skills/`, `~/.codex/skills/` oder im Projektordner unter `.claude/skills/`.

1. Ordner mit den Namen `fulfillment*` und `demo-*` suchen.
2. Liste zeigen und fragen, ob sie gelöscht werden sollen.
3. Erst nach Bestätigung löschen, danach in Claude Code `/reload-plugins`.

## 7. Updates

In Claude Code sind Updates fremder Marketplaces standardmäßig aus. Empfehlen: `/plugin` →
Marketplaces → `outreach-plugins` → Auto-Update einschalten. Sonst `fulfillment-update`.

## Abschluss

Kurz berichten: Umgebung, Outreach-Verbindung ja/nein, Plugins outreach/datenbeschaffung ja/nein,
Netlify-Konto und Weg (Connector, CLI oder Drop), RankM8 ja/nein, aufgeräumte Kopien, Auto-Update.
Danach weiter mit dem Einstieg `fulfillment`.
