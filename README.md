# Outreach Plugins

Ein Marketplace mit drei Plugins für Kunden der Outreach-Plattform – für Claude (App, claude.ai,
Cowork, Claude Code) und für ChatGPT Desktop und Codex.

| Plugin | Inhalt | Für wen |
|---|---|---|
| **outreach** | Kampagnen anlegen und ändern, Cold-Mail-Copy nach SOP, Leads importieren, qualifizieren, recherchieren, Mails generieren und prüfen, Launch vorbereiten. Bringt die MCP-Verbindung `akquise` (`outreach.akquise.de`) und in Claude Code die Live-Ansicht (Lead-Vorschau, Fortschritt der Läufe) mit. | alle |
| **datenbeschaffung** | Neue Leads finden: lokale Betriebe in DACH über Google Maps direkt in der App (Credits), alles andere mit Apify oder Outscraper im eigenen Konto, Liste prüfen, als CSV bzw. per `import_leads` übernehmen. | wer neue Leads braucht |
| **fulfillment** | Das Marketing-Offer liefern: prüfen, welches Offer sich mit KI liefern lässt, und für Leads, die geantwortet haben, die versprochene Demo bauen (Webseiten-Entwurf, SEO-Ergebnis, Anzeigen, Leadliste, Muster-Akquise-Kampagne), nicht auffindbar bei Netlify veröffentlichen und den Link als `demo-url` am Lead speichern. Optional mit RankM8 für SEO-Daten. | wer Karte A oder C nutzt |

Die Skills passen zum Outreach-MCP mit **32 Tools** und **7 Prompts**. Der MCP verarbeitet
Leads, verwaltet Kampagnen und Listen und findet ab Version 4.7.0 lokale Betriebe über Google Maps; andere Quellen scrapt er nicht. Versand läuft beim Kunden
(Instantly o. Ä.), nicht in der Plattform.

## Installation

**Claude Code**

```
/plugin marketplace add RankM8/outreach-plugins
/plugin install outreach@outreach-plugins
/plugin install datenbeschaffung@outreach-plugins     (optional)
/plugin install fulfillment@outreach-plugins          (optional)
```

**Claude App / claude.ai / Cowork:** Customize → Plugins → Add marketplace →
`RankM8/outreach-plugins` → `outreach` (und optional `datenbeschaffung`, `fulfillment`) installieren →
im Plugin unter „Connectors“ die Verbindung `akquise` verbinden.

**ChatGPT Desktop / Codex**

```
codex plugin marketplace add RankM8/outreach-plugins
```

danach unter `/plugins` installieren und neue Session starten.

**Cursor & andere Agenten (nur Skills):** `npx skills add RankM8/outreach-plugins`, die
MCP-Verbindung separat über die App-Seite „MCP & Skills“.

Nach der Installation: Skill **`outreach-setup`** aufrufen (bzw. **`datenbeschaffung-setup`** für das
Plugin datenbeschaffung, **`fulfillment-setup`** für das Plugin fulfillment). Er prüft die Verbindung, räumt alte Skill-Kopien auf und zeigt die ersten Schritte.

**Kunden einer anderen Outreach-App als Akquise:** Die mitgelieferte Verbindung `akquise`
unverbunden lassen und den MCP der eigenen App über deren Seite „MCP & Skills“ hinzufügen.
Skills und Live-Ansicht erkennen ihn an seinen Tools.

**Updates:** Skill `outreach-update`. In Claude Code am besten Auto-Update einschalten
(`/plugin` → Marketplaces → `outreach-plugins`).

## Aufbau

```
.claude-plugin/marketplace.json     Marketplace für Claude (liest Codex mit)
.agents/plugins/marketplace.json    Marketplace für ChatGPT/Codex
plugins/
  outreach/
    .claude-plugin/plugin.json      Manifest Claude
    plugin.json                     Manifest portabel (OpenAI)
    .mcp.json / mcp.json            MCP-Verbindung akquise (Claude / OpenAI)
    hooks/                          Live-Ansicht für Claude Code (register.tsx, model.ts)
    types/  tests/                  Typen und Tests der Live-Ansicht
    skills/
      outreach            Einstieg, leitet weiter
      outreach-setup      Einrichtung und Prüfung
      outreach-update     Aktualisieren
      outreach-campaign   Kampagne bauen und ändern nach der Cold-Mailing-SOP
      outreach-copy       Cold-Mail-Copy-Regeln (verbindlich für campaign, generate, verify)
      outreach-import     Leads importieren
      outreach-lists      Listen verwalten
      outreach-qualify    Leads qualifizieren
      outreach-research   Leads recherchieren
      outreach-generate   Mail-Variablen erzeugen
      outreach-verify     Review (approve/reject)
      outreach-pipeline   voller Durchlauf, Einstieg für Server-Lauf und Abo-Lauf
      outreach-abo-lauf   Abo-Lauf als Workflow (Haiku baut, Sonnet prüft, nachbessern)
      outreach-launch     Domains, Postfächer, Warm-up, Instantly, Auswertung, Optimierung
  datenbeschaffung/
    .claude-plugin/plugin.json  plugin.json
    skills/
      datenbeschaffung    Einstieg: Setup → ICP → Weg A–E → Weg → Qualität
      datenbeschaffung-setup   Einrichtung: Outreach-Verbindung, Apify, Outscraper prüfen
      datenbeschaffung-update  Aktualisieren
      weg-*               die Beschaffungswege (Google, Apollo, Maps, Instagram, Plattformen …)
      outscraper-bulk     sehr große Volumina
      impressum-enrichment  kontaktseiten-fallback  enrichment-waterfall
      listen-qualitaet    Pflicht-Endstation: Dedup → Verifizierung → Stichprobe → Übergabe
      datenbeschaffung-referenzen   geteilte Referenzen und Skripte
                                    (die Skills lesen über ../datenbeschaffung-referenzen/)
  fulfillment/
    .claude-plugin/plugin.json  plugin.json
    skills/
      fulfillment          Einstieg: Offer finden (vor der Kampagne) oder Demo liefern (nach der Antwort)
      fulfillment-setup    Einrichtung: Outreach-Verbindung, Plugins, Netlify, optional RankM8
      fulfillment-update   Aktualisieren
      demo-webseite        Webseiten-Entwurf aus der bestehenden Website des Leads (eine index.html)
      demo-seo             SEO-Ergebnis: Suchbegriffe auf Seite 2, lokale Suche, Titel, KI-Suchmaschinen
      demo-anzeigen        Meta-/Google-Anzeigen, Stellenanzeige, Content-Plan
      demo-leadliste       Lead-System mit 30–50 passenden Wunschkunden (datenbeschaffung im Geschenk-Modus)
      demo-akquise-kampagne  Muster-Kampagne mit Sequenz und 3 Beispiel-Mails (nach outreach-copy)
      demo-ausliefern      Netlify (Connector, CLI oder Drop), noindex, demo-url am Lead, Antwort-Text
      fulfillment-referenzen   Demo-Katalog, Lead-Kontext, Umgebungen, Netlify, Qualität, Recht, Webseiten-Bauplan
```

## Pflege

- Jede Änderung, die Kunden erreichen soll: `version` in **beiden** Manifesten des betroffenen
  Plugins erhöhen (`.claude-plugin/plugin.json` und `plugin.json`) und `CHANGELOG.md` ergänzen.
  Ohne neue Version bekommen installierte Plugins nichts Neues.
- MCP-Tool-Änderungen im Produkt → betroffene Skills im selben Zug nachziehen.
- Live-Ansicht: `claude plugin test plugins/outreach`; Manifeste: `claude plugin validate .`;
  CSV-Skript der Datenbeschaffung: `python3 -I plugins/datenbeschaffung/tests/test_build_csv.py`
- Kein `bin/`-Ordner in einem Plugin (claude.ai lehnt das ganze Plugin sonst ab), keine Symlinks.
- Actor-Empfehlungen/Preise (`datenbeschaffung-referenzen/references/apify-actors.md`,
  `kosten.md`) tragen ein „zuletzt geprüft“-Datum.
