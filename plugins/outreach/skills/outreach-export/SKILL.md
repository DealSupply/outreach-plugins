---
name: outreach-export
description: Use when user says "outreach:export", "Kampagne exportieren", "Leads exportieren" (einer Kampagne), "Freigaben exportieren", "als Excel", "als CSV", "Excel-Datei", "CSV für Instantly", "CSV fürs CRM", "Export herunterladen", "Download-Link", or wants the leads of a campaign as a file. Exportiert die Leads einer Kampagne als Excel oder CSV über den MCP (export_campaign_leads), mit denselben Zwecken und Sperren wie der Export-Dialog der App.
---

# Outreach Export — Leads einer Kampagne als Excel oder CSV

Liefert dieselbe Datei wie der Export-Dialog der App. Die Datei entsteht auf dem Server im Hintergrund; zurück
kommt ein Download-Link, keine Zeilen im Chat. Den Bestand oder eine Liste als Zeilen (oder den Abgleichsindex)
liefert `export_leads`, siehe `outreach-lists`.

Braucht MCP 4.4.0 (`ping`). Kennt der Server `export_campaign_leads` nicht, auf die App verweisen: Kampagne öffnen →
„Exportieren“.

## Ablauf

1. **Kampagne bestimmen:** `list_campaigns`, bei mehreren Treffern nachfragen.
2. **Zweck klären** (eine Frage, wenn nicht klar):
   - `sending`: CSV für Instantly und andere Versandwerkzeuge. Firma, Ansprechpartner, KI-Variablen und fertige
     Mails, nur Leads, die versendet werden dürfen.
   - `overview` (Standard): Excel zum Anschauen. Alle Spalten, Blatt „Zusammenfassung“, eigene Blätter für
     Personen, Mails und Recherche; nichts fällt weg, Probleme sind markiert.
   - `crm`: CSV fürs CRM. Firma, Ansprechpartner, Kontaktwege, Urteil, Status, eigene Felder.
3. **Welche Leads:** `scope` = `approved` (Standard), `approved_new` (Freigaben, die noch nicht exportiert sind),
   `all` (alle der Kampagne) oder `selection` mit `lead_ids`.
4. **Erst zählen:** `export_campaign_leads(campaign_id, purpose, scope, dry_run=true)`. Dem Nutzer kurz nennen:
   `leads` in der Datei, was mit welchem Grund fehlt (`excluded`: `not_approved`, `do_not_contact`, `contacted`,
   `no_address`, `foreign_address`) und was markiert ist (`flagged`).
5. **Markieren nur auf Wunsch:** `mark_exported=true` stempelt die Freigaben in der Datei beim ersten Download als
   exportiert, damit ein späterer `approved_new`-Export sie auslässt. Typisch beim Zweck `sending`, sonst nicht.
   Fragen, wenn unklar.
6. **Starten:** derselbe Aufruf ohne `dry_run`. Die Antwort trägt `export_id` und `download_url`.
7. **Warten:** `get_lead_export(export_id)` alle paar Sekunden, bis `status` = `ready`
   (`failed`: `error` nennen; `expired`: neu starten).
8. **Ausliefern:**
   - Mit Shell (Claude Code): `curl -fLo "<filename>" "<download_url>"` ins Arbeitsverzeichnis, Pfad nennen.
   - Ohne Shell (Claude Desktop, claude.ai): den Link zeigen.

## Regeln

- Der Link braucht keine Anmeldung und gilt 24 Stunden. Er gehört nur dem Nutzer: nicht in Tickets, Mails oder
  geteilte Dokumente kopieren.
- `get_lead_export` wiederholt den Link nicht. Ihn aus der Antwort von Schritt 6 nehmen.
- KI-Variablen und Mails stehen nur bei freigegebenen Leads. Fehlen Freigaben, zuerst `outreach-verify`.
- Spalten nur ändern, wenn der Nutzer es will: `dry_run` nennt in `columns` die Schlüssel; `columns` oder `preset`
  (`full`, `sending`, `crm`) überschreiben den Zweck, ebenso `format` (`xlsx`, `csv`) und `sendable_only`.
- Höchstens 25.000 Leads je Datei (`too_large`): Umfang eingrenzen oder in Auswahlen teilen.
- `mark_exported` braucht `leads:write`; ohne das Recht ohne Markieren exportieren.
