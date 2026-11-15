---
name: outreach-update
description: Aktualisiert die Outreach-Plugins (outreach, datenbeschaffung, fulfillment). Verwenden bei „outreach aktualisieren“, „Plugin updaten“, „gibt es eine neue Version“, „Skills sind veraltet“ oder wenn ein Skill ein Tool aufruft, das es nicht gibt.
---

# Outreach-Plugins aktualisieren

Nenne dem Nutzer die Schritte für seine Umgebung und führe sie aus, wo du das kannst.

| Umgebung | Aktualisieren |
|---|---|
| Claude Code | Schritte unten |
| Claude App / claude.ai / Cowork | Customize → Plugins → Marketplace `outreach-plugins` → „Check for updates“ bzw. „Sync automatically“ |
| Codex | `codex plugin marketplace upgrade outreach-plugins`, danach neue Session |
| ChatGPT Desktop | App neu starten |
| Cursor & andere (Skills ohne Plugin) | `npx skills add DealSupply/outreach-plugins` |

## Claude Code

Claude Code holt neue Versionen fremder Marketplaces nicht von selbst: Auto-Update ist für
Marketplaces von Drittanbietern standardmäßig aus. Wer eine ältere Version hat, aktualisiert einmal
von Hand:

1. **Marketplace aktualisieren:** `/plugin marketplace update outreach-plugins` (im Terminal:
   `claude plugin marketplace update outreach-plugins`). Immer mit dem Namen `outreach-plugins`.
2. **Plugin aktualisieren, falls nötig:** Zeigt `/plugin` → Reiter „Installed“ bei `outreach` noch die
   alte Version, dort „Update now“ wählen, oder im Terminal
   `claude plugin update outreach@outreach-plugins`. Ebenso `datenbeschaffung@outreach-plugins` und
   `fulfillment@outreach-plugins`, wenn installiert. Liegt ein Plugin nur in einem Projekt
   (Projekt-Scope), den Befehl in diesem Projekt mit `--scope project` ausführen.
3. **Laden:** `/reload-plugins` oder eine neue Sitzung starten.
4. **Auto-Update einschalten:** `/plugin` → Reiter „Marketplaces“ → `outreach-plugins` → Auto-Update
   einschalten. Danach holt Claude Code neue Versionen selbst.

**Mehrere Profile:** Wer Claude Code mit mehreren Konfigurationsprofilen nutzt (eigene
Konfigurationsordner, etwa über `CLAUDE_CONFIG_DIR`), hat in jedem Profil eigene Plugins. Die
Schritte dann in jedem Profil ausführen, in dem `outreach` installiert ist.

**Alte Quelle:** Das Repo hieß bis Oktober 2026 `RankM8/outreach-plugins`; GitHub leitet weiter.
`claude plugin marketplace list` zeigt die Quelle. Schlägt Schritt 1 trotzdem fehl, den
Marketplace neu hinzufügen: `/plugin marketplace remove outreach-plugins`, dann
`/plugin marketplace add DealSupply/outreach-plugins` und die Plugins neu installieren
(`/plugin install outreach@outreach-plugins`).

## Danach: einmal mit DealSupply anmelden

Seit outreach 0.6.0 bringt das Plugin die Verbindung `dealsupply` (`app.dealsupply.ai`) mit. Nach dem
Update von 0.5.x oder älter wird sie einmal angemeldet, mit den Zugangsdaten von DealSupply. Wer
bisher nur über Akquise in die App kam (oft ohne eigenes Passwort), meldet sich zuerst in der App über
Akquise an (`https://app.dealsupply.ai/sso/akquise`) und verbindet danach im selben Browser; sonst auf
der Anmeldeseite „Passwort vergessen“. Anmelden:

- Claude Code: `/mcp` öffnen → `plugin:outreach:dealsupply` → anmelden.
- Claude App / claude.ai: Customize → Plugins → `outreach` → Reiter „Connectors“ → bei `dealsupply` „Connect“.
- ChatGPT Desktop / Codex: beim ersten Aufruf anmelden, in Codex alternativ `codex mcp login dealsupply`.

Vor dem Prüfen ältere Verbindungen entfernen, sonst antwortet womöglich noch eine von ihnen und
nichts zeigt, ob die neue steht. Das betrifft eine von Hand angelegte Verbindung zu DealSupply und
eine alte Verbindung `akquise`:

- Claude Code: `claude mcp list` im Terminal zeigt die Verbindungen. Eine von Hand angelegte mit
  `claude mcp remove <name>` entfernen, zum Beispiel `claude mcp remove dealsupply` oder
  `claude mcp remove akquise`. Die Verbindung des Plugins (`plugin:outreach:dealsupply`) bleibt dabei
  bestehen.
- Claude App / claude.ai: unter Connectors den alten Eintrag entfernen.
- Codex: `codex mcp remove <name>`.

Erst danach `list_campaigns` aufrufen. Kommt die Liste der Kampagnen, steht die neue Verbindung.
Einzelheiten: `outreach-setup`, Schritt 2.

## Was sich geändert hat

Die Änderungen stehen in `CHANGELOG.md` im Repo `DealSupply/outreach-plugins`. Nenne dem Nutzer
die Punkte seit seiner installierten Version, wenn er danach fragt.

## Wenn danach noch alte Skills auftauchen

Doppelte oder veraltete Skills stammen meist aus früheren `npx skills add`-Kopien → `outreach-setup`,
Schritt 3 (Aufräumen).
