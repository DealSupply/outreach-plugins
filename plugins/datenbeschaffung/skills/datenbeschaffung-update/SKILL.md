---
name: datenbeschaffung-update
description: Aktualisiert das Plugin datenbeschaffung. Verwenden bei „Datenbeschaffung aktualisieren“, „datenbeschaffung updaten“, „neue Version der Datenbeschaffung“ oder wenn ein Datenbeschaffungs-Skill auf veraltete Actors, Preise oder Tools verweist.
---

# Datenbeschaffung aktualisieren

Nenne dem Nutzer den Befehl für seine Umgebung und führe ihn aus, wo du das kannst.

| Umgebung | Aktualisieren |
|---|---|
| Claude Code | `/plugin marketplace update outreach-plugins` (immer mit dem Namen; ohne Namen wird nur der Katalog neu gelesen). Zeigt `/plugin` → „Installed“ danach noch die alte Version: dort „Update now“ oder `claude plugin update datenbeschaffung@outreach-plugins`. Dann `/reload-plugins` oder neue Sitzung |
| Claude App / claude.ai / Cowork | Customize → Plugins → Marketplace `outreach-plugins` → „Check for updates“ bzw. „Sync automatically“ |
| Codex | `codex plugin marketplace upgrade outreach-plugins`, danach neue Session |
| ChatGPT Desktop | App neu starten |
| Cursor & andere (Skills ohne Plugin) | `npx skills add DealSupply/outreach-plugins` |

Dauerhaft in Claude Code: `/plugin` → Reiter „Marketplaces“ → `outreach-plugins` → Auto-Update einschalten
(für Marketplaces von Drittanbietern standardmäßig aus). Weitere Plugins aus dem Marketplace
(`outreach`, `datenbeschaffung`, `fulfillment`) genauso aktualisieren.

- **Projekt-Scope:** Liegt das Plugin nur in einem Projekt, `claude plugin update datenbeschaffung@outreach-plugins
  --scope project` in diesem Projekt ausführen.
- **Mehrere Profile:** Wer Claude Code mit mehreren Konfigurationsprofilen nutzt (eigene
  Konfigurationsordner, etwa über `CLAUDE_CONFIG_DIR`), hat in jedem Profil eigene Plugins; die Schritte
  in jedem Profil ausführen, in dem `datenbeschaffung` installiert ist.
- **Alte Quelle:** Das Repo hieß bis Oktober 2026 `RankM8/outreach-plugins`; GitHub leitet weiter.
  `claude plugin marketplace list` zeigt die Quelle. Schlägt die Aktualisierung trotzdem fehl, den
  Marketplace neu hinzufügen: `/plugin marketplace remove outreach-plugins`, dann
  `/plugin marketplace add DealSupply/outreach-plugins` und die Plugins neu installieren
  (`/plugin install datenbeschaffung@outreach-plugins`).

## Was sich geändert hat

Die Änderungen stehen in `CHANGELOG.md` im Repo `DealSupply/outreach-plugins`. Nenne dem Nutzer die
Punkte seit seiner installierten Version, wenn er danach fragt.

## Wenn danach noch alte Skills auftauchen

Doppelte oder veraltete Skills stammen meist aus früheren `npx skills add`-Kopien →
`datenbeschaffung-setup`, Schritt 5 (Aufräumen).
