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
(`outreach`, `datenbeschaffung`, `fulfillment`) genauso aktualisieren. Mehrere Konfigurationsprofile,
Projekt-Scope und die alte Quelle `RankM8/outreach-plugins`: Skill `outreach-update`, Abschnitt
„Claude Code“.

## Was sich geändert hat

Die Änderungen stehen in `CHANGELOG.md` im Repo `DealSupply/outreach-plugins`. Nenne dem Nutzer die
Punkte seit seiner installierten Version, wenn er danach fragt.

## Wenn danach noch alte Skills auftauchen

Doppelte oder veraltete Skills stammen meist aus früheren `npx skills add`-Kopien →
`datenbeschaffung-setup`, Schritt 5 (Aufräumen).
