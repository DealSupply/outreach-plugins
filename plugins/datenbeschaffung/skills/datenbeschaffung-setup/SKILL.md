---
name: datenbeschaffung-setup
description: Richtet das Plugin datenbeschaffung ein und prüft die Voraussetzungen, mit oder ohne DealSupply-Konto. Verwenden bei „Datenbeschaffung einrichten“, „Apify verbinden“, „Apify-Token“, „Outscraper einrichten“, „funktioniert mein Scraping-Zugang“ oder direkt nach der Installation des Plugins. Warnt vor der Preisfalle im kostenlosen Apify-Plan, prüft Outreach-Verbindung (optional), Apify-Zugang (kostenloser Selbsttest), optional Outscraper, räumt alte Skill-Kopien auf – ohne kostenpflichtige Läufe.
---

# Datenbeschaffung einrichten

Ziel: Alles steht, damit der Einstieg `datenbeschaffung` ohne Hänger durchläuft. **Nichts
Kostenpflichtiges** in diesem Ablauf – kein Actor-Lauf, kein Scrape, keine Verifizierung. Nur
kostenlose, lesende Prüfungen.

Die Details zu Konto, Token und Zugriffswegen stehen in
`../datenbeschaffung-referenzen/references/setup.md` und `zugriff.md`. Dieser Skill führt nur durch
die Prüfung, er wiederholt sie nicht.

## Zuerst sagen: die Preisfalle im kostenlosen Apify-Plan

Bevor irgendetwas eingerichtet wird, dem Nutzer das in eigenen Worten sagen (Zahlen aus
`../datenbeschaffung-referenzen/references/kosten.md`, „Preisfalle“, und `apify-actors.md`):

> Nimm für die Datenbeschaffung nicht den kostenlosen Apify-Plan. Dort kostet das Prüfen einer
> Adresse 0,10 $ statt 0,0006 $: 200 Adressen kosten 20 $ statt 12 Cent. Auch Google Maps kostet
> dort etwa das Doppelte, und Zusätze wie die Prüfung im Maps-Actor 0,10 $ je Treffer. Die 5 $
> Startguthaben reichen für einen ersten Test; für die laufende Beschaffung brauchst du einen
> bezahlten Plan (Starter rund 39 $ im Monat). Deine Preisstufe steht in der Apify-Konsole unter
> Billing.

Steht der Nutzer noch im kostenlosen Plan, das im Abschluss festhalten; `listen-qualitaet` prüft
dort dann nur die riskanten Adressen.

**Token bleiben beim Kunden:** Apify- oder Outscraper-Schlüssel nie im Chat abfragen, ausgeben oder
irgendwohin senden. Der Nutzer hinterlegt sie selbst (Apify-Connector, Umgebungsvariable, CLI-Login).

## 1. Umgebung erkennen

Claude Code (Shell und Dateisystem vorhanden), Claude App / claude.ai / Cowork (keine Shell) oder
ChatGPT Desktop / Codex. In einem Satz nennen; davon hängt der Apify-Zugriffsweg ab. Plugins gibt
es in den bezahlten Claude-Tarifen; die Skripte des Plugins (Bereinigung, Sperrliste, Datei für
Instantly) brauchen Python, also Claude Code, Codex oder die Claude-App mit eingeschalteter
Code-Ausführung. Fehlt das, sagen, welche Schritte die KI dann von Hand machen muss.

## 2. DealSupply-Verbindung prüfen (optional)

Das Plugin funktioniert auch ohne DealSupply-Konto. Für Bestandsabgleich und direkten Import
braucht es die Verbindung zur App; ohne Konto endet jeder Lauf mit einer Datei für Instantly und
einer eigenen Sperrliste (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`).

- `list_lists` aufrufen (nur lesend).
  - **Antwort kommt:** Verbindung steht, Anzahl der Listen nennen.
  - **Workspace:** Gibt es `list_workspaces`, aufrufen und den Workspace in einem Satz nennen. Bei
    mehreren fragen, in welchen importiert werden soll; ist es nicht der Standard, die Listen mit
    `list_lists(workspace=<uuid>)` neu zählen. Mit der Rolle `viewer` geht dort nur der Abgleich,
    kein Import. Fehlt das Tool (älterer Server), überspringen. Regel:
    `../datenbeschaffung-referenzen/references/dealsupply-mcp.md`, Abschnitt „Workspace“.
  - **Kein Outreach-Tool vorhanden:** fragen, ob der Nutzer ein DealSupply-Konto hat.
    - **Ja:** Das Plugin `outreach` aus demselben Marketplace installieren (bringt die Verbindung
      mit) und dort `outreach-setup` ausführen. Ohne Verbindung geht Datenbeschaffung trotzdem,
      aber ohne Bestandsabgleich; das Ergebnis kommt dann als CSV über die Oberfläche der App.
    - **Nein:** Modus ohne DealSupply. Nichts weiter einzurichten; sagen, dass für die Sperrliste
      ein Export aus dem eigenen CRM gebraucht wird (Bestandskunden, Ex-Kunden, Abmeldungen) und
      die Liste am Ende als Datei für Instantly kommt.

## 3. Apify-Zugang prüfen (Pflicht)

Den ersten verfügbaren Weg nehmen (Reihenfolge und Aufrufe: `zugriff.md`):

1. **Apify-MCP** vorhanden (`search-actors`, `call-actor` …)? → `search-actors` mit keywords
   „Google Maps“ ausführen. Treffer = verbunden.
2. **REST** mit `APIFY_TOKEN` in der Umgebung (Claude Code, Codex)? → `curl -s -o /dev/null -w "%{http_code}"
   -H "Authorization: Bearer $APIFY_TOKEN" "https://api.apify.com/v2/acts?limit=1"` → `200` = verbunden.
   Den Token dabei nie ausgeben.
3. **Apify-CLI** installiert? → `apify info` zeigt das Konto = verbunden.

Nichts davon: Den Nutzer durch `setup.md` führen (Konto anlegen, Token unter
https://console.apify.com/settings/integrations kopieren, Apify-Connector verbinden bzw. Token als
Umgebungsvariable setzen). Danach erneut prüfen.

Der E-Mail-Verifier für `listen-qualitaet` ist ebenfalls ein Apify-Actor; ein eigener Zugang ist
nicht nötig. Nach dem Selbsttest den Nutzer fragen, in welchem Apify-Plan er ist (Konsole →
Billing), und bei „kostenlos“ die Preisfalle oben noch einmal kurz nennen.

## 4. Outscraper (optional)

Nur nötig für sehr große Volumina (`outscraper-bulk`, ab etwa 10.000 Leads). Frage: „Planst du
Beschaffungen in dieser Größe?“

- **Ja:** prüfen, ob `OUTSCRAPER_API_KEY` gesetzt ist (nur ob vorhanden, nicht den Wert zeigen).
  Fehlt er, auf das Outscraper-Konto des Nutzers verweisen; der Schlüssel bleibt bei ihm.
- **Nein:** überspringen.

## 5. Alte Skill-Kopien aufräumen (nur Claude Code, Codex, Cursor)

Frühere Installationen per `npx skills add` liegen als Kopien z. B. in `~/.claude/skills/`,
`~/.agents/skills/`, `~/.codex/skills/` oder im Projektordner unter `.claude/skills/`.

1. Ordner suchen mit den Namen `datenbeschaffung*`, `weg-*`, `listen-qualitaet`,
   `impressum-enrichment`, `kontaktseiten-fallback`, `enrichment-waterfall`, `outscraper-bulk`.
2. Liste zeigen und fragen, ob sie gelöscht werden sollen.
3. Erst nach Bestätigung löschen, danach in Claude Code `/reload-plugins`.

## 6. Updates

In Claude Code sind Updates fremder Marketplaces standardmäßig aus. Empfehlen: `/plugin` →
Marketplaces → `outreach-plugins` → Auto-Update einschalten. Sonst `datenbeschaffung-update`.

## Abschluss

Kurz berichten: Umgebung, Modus (mit oder ohne DealSupply), DealSupply-Verbindung ja/nein
(Workspace, Anzahl Listen), Apify-Zugang ja/nein und über welchen Weg, Apify-Plan (kostenlos oder
bezahlt), Outscraper ja/nein/nicht nötig, aufgeräumte Kopien, Auto-Update ja/nein. Danach weiter
mit dem Einstieg `datenbeschaffung`.
