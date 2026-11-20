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

> **Fehler und Wünsche:** Es gilt die Melde-Regel aus dem Skill `outreach`: Nach einem Fehler, den du nicht selbst lösen kannst, fragen, ob du ihn an DealSupply melden sollst, und erst nach einem Ja `report_feedback` mit `attach_last_failure=true` aufrufen. Einen Wunsch, den DealSupply nicht kann, als Wunsch melden anbieten.

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
   - **Auswahl nach Filter oder Ansicht (ab MCP 4.32.0):** `export_campaign_leads` nimmt selbst keinen Filter.
     Will der Nutzer nur einen Teil („nur die aus Wien“, „die Ansicht Score über 70“), die Leads mit
     `list_leads(campaign_id, filter=…, view_id=…)` holen (Ort `campaign`; Aufbau des Ausdrucks: `outreach-lists`,
     „Filter und Ansichten“) und deren `lead_ids` mit `scope="selection"` übergeben. Vorher mit
     `count_leads(place="campaign", campaign_id, filter=…, view_id=…)` zählen: `list_leads` gibt höchstens 2000 IDs
     zurück (`lead_ids_truncated`), bei mehr den Filter teilen und die IDs sammeln. Die Sperren des Exports gelten
     weiter: Was nicht freigegeben oder gesperrt ist, nennt `dry_run` unter `excluded`. Auf älteren Servern die
     Auswahl über `list_leads` im Listen-Modus oder bekannte IDs.
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
- Ungeprüfte Adressen: Der Export prüft keine Adressen und hält dafür nichts zurück. Die Einstellung „Nur
  zustellbare Adressen“ einer Kampagne (ab DealSupply v4.22.0) gilt nur für die Übertragung an Instantly, nicht
  für die Datei. Beim Zweck `sending` dem Nutzer deshalb sagen, dass die Datei auch Leads mit ungeprüfter
  Versandadresse enthalten kann, und eine Prüfung der Adressen vor dem Versand empfehlen: in der App über die Auswahl
  der Leads („Adressen prüfen“, kostet Credits), als Power-up im Lauf oder im Versandwerkzeug. Siehe
  `outreach-launch`, Phase 2.
- Leads aus Leads finden tragen ab MCP 4.24.0 die Attribute `maps_claim_status` und `maps_star_scores`. In der
  Datei sind das die Spalten `attr_maps_claim_status` und `attr_maps_star_scores` (Zwecke `overview` und `crm`,
  nicht `sending`); eine leere Zelle heißt „nicht bekannt“.
- Höchstens 25.000 Leads je Datei (`too_large`): Umfang eingrenzen oder in Auswahlen teilen.
- Wie viele Leads in welchem Review-Reiter stehen (offen, freigegeben, exportiert, abgelehnt), nennt ab MCP 4.32.0
  `list_lead_views(place="review", campaign_id, with_counts=true)` in einem Aufruf; `dry_run` bleibt die Zahl, die
  für die Datei gilt.
- `mark_exported` braucht `leads:write`; ohne das Recht ohne Markieren exportieren.
- Zwei Personen je Firma (ab MCP 4.11.0): In solchen Kampagnen trägt die Datei die Spalten
  `second_person_email`, `_first_name`, `_last_name`, `_role` und `_status`. `rows_per_person=true` (nur CSV)
  gibt Person 2 eine eigene Zeile; für Instantly fragen, ob der Nutzer das will (jede Person ein eigener
  Kontakt), sonst bleibt eine Zeile je Firma.
