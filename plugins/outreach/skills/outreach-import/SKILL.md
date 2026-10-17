---
name: outreach-import
description: Use when user says "outreach:import", "mcp:import", "importiere leads via mcp", "leads hochladen mcp", "csv leads importieren", "outscraper import mcp", "apify export importieren", or triggers /mcp:import. Importiert extern beschaffte Lead-Listen (CSV/JSON, z. B. Apify- oder Outscraper-Export) per import_leads.
---

# MCP Import — Lead-Listen hochladen

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

Dieser Skill lädt Lead-Listen über das MCP-Tool `import_leads` (Scope `leads:write`) in ListM8 — aus CSV-Dateien (z. B. Apify- oder Outscraper-Exporte), JSON oder Inline-Daten. Das Scraping selbst passiert außerhalb von ListM8 (der Kunde nutzt Apify, Outscraper o. Ä.); der MCP bekommt nur das Ergebnis. Mit `campaign_id` werden die Leads der Kampagne zugeordnet (Status `processing`); ohne entstehen unkategorisierte Leads im globalen Bestand. Der Import startet KEINE Verarbeitung — anschließend `/outreach-pipeline` (serverseitiger Lauf via `start_lead_run`) oder die Einzel-Skills.

## Aufruf

| Eingabe | Verhalten |
|---------|-----------|
| `/outreach-import <datei> 80` | Datei parsen, in Kampagne 80 importieren |
| `/outreach-import <datei>` | Kampagne via `list_campaigns` wählen (oder „ohne Kampagne") |
| `importiere diese leads: ...` | Inline-Daten importieren |

## Phase 1: Daten lokal lesen und vorbereiten

Keine Dateipfade oder URLs an den Server übergeben: `import_leads` erhält ein JSON-Array von Lead-Objekten (max. 10.000 pro Call).

**Menge realistisch einschätzen:** Jeder Lead steht als Text im Tool-Aufruf und kostet Kontext (grob 50–100 Tokens je Lead). Bis etwa 300 Leads pro Aufruf ist das unproblematisch. Bei mehreren Tausend Zeilen ist der Weg über den Chat unpraktisch – dann dem Nutzer den CSV-Import in der App empfehlen (Leads → Importieren; gleicher Import samt Dedup im Hintergrund) und nur die Vorbereitung (Spalten-Mapping, Bereinigung, Vorab-Dedup) hier erledigen.

0. **Server-Version prüfen:** `ping` aufrufen. Diese Version allein entscheidet über den Kontrakt, nie der Wortlaut einer Fehlermeldung. Ab `version` 3.0.0 gilt „E-Mail ODER eigene Website“ je Zeile und ein Teilimport (Punkt 4). Älterer Server oder keine Version: alter Kontrakt, jede Zeile braucht eine gültige `email`, und eine einzige Zeile ohne gültige E-Mail lässt den ganzen Aufruf scheitern. Dann die Zeilen ohne E-Mail abspalten und dem Nutzer sagen, dass sein Server den Import ohne E-Mail noch nicht kennt.
1. CSV/XLSX mit Read/Bash lesen; Trennzeichen und Encoding prüfen (UTF-8 sicherstellen, Umlaute!). XLSX lokal in JSON umwandeln.
2. Spalten auf Kernfelder mappen: `email` **oder** `website` (eins davon je Zeile, ab 3.0.0), `company`, `phoneNumber`, `city`. Fehlt die E-Mail, das Feld weglassen. Ohne E-Mail sucht die Recherche die Kontaktadresse auf der Website; findet sie keine, scheidet der Lead aus und bekommt nie eine Mail. Ein Profil-Link (Instagram, Facebook, Linktree, Doctolib, Branchenportal) ist keine Website: ohne E-Mail wird die Zeile abgelehnt. Baukasten-Subdomains (`praxis.jimdosite.com`) zählen als Website.
   Outscraper-Referenz-Mapping: `name`→company, `site`→website, `phone`→phoneNumber, `city`→city. Bei Apify-Exporten die Spaltennamen des jeweiligen Actors prüfen.
3. Zusätzliche Spalten, die erhalten bleiben sollen (Rating, Kategorie, Adresse …): als flache Extra-Keys am Lead-Objekt lassen und in `attribute_mappings` deklarieren (ohne Deklaration werden Extra-Keys nicht gespeichert):
   ```json
   { "rating": {"action": "create_new", "name": "Google Rating", "fieldType": "text"},
     "branche": {"action": "map_existing", "fieldKey": "branche"} }
   ```
   `create_new` braucht `name` und `fieldType`, `map_existing` einen `fieldKey`; sonst `validation_failed`.
4. Vorab-Check Kontakt:
   - **Ab 3.0.0:** Lokal nur Zeilen ohne jedes Kontaktmerkmal (weder E-Mail noch Website) entfernen, zählen und mit Grund ausweisen. Alles Übrige schickt man; der Server lehnt nicht importierbare Zeilen einzeln ab (`rejected_rows` in der Antwort, Codes `missing_contact`, `invalid_email`, `invalid_website`, `platform_only_website`, `website_too_long`, `not_an_object`) und importiert den Rest. Nur wenn KEINE Zeile importierbar ist, kommt `validation_failed`; dessen Meldung nennt ebenfalls `"email"` („needs a valid "email" or a usable "website"“) und ist kein Zeichen für einen alten Server. `limit_reached` steht nie in `rejected_rows`: In der Tool-Antwort scheitert damit der ganze Aufruf (mehr als 10.000 Zeilen oder Kontingent erschöpft), als Zeilencode erscheint es nur im Job-Ergebnis `rejected` (Zeilen, die erst im Job am Kontingent scheiterten). Eine ungültige E-Mail neben einer brauchbaren Website importiert er ohne E-Mail (Hinweis `invalid_email_ignored`).
   - **Älterer Server:** Das Tool weist den GESAMTEN Call ab, wenn eine Zeile keine gültige `email` hat. Die ersten 20 Zeilendiagnosen stehen im `isError`-Text nach dem Prefix `validation_failed:` („row N: …"). Zeilen ohne gültige E-Mail vor dem Call entfernen, zählen und im Report ausweisen.
5. Vorab-Dedup: VOR dem Import `check_leads_exist` (E-Mails und/oder Domains, bis 1.000 je Call, in Chunks) fahren: Bestands-Leads und `do_not_contact`-Treffer dem Nutzer zeigen, bevor Kampagnenplätze oder Verarbeitungskosten draufgehen. Zeilen ohne E-Mail nur über `domains` prüfen. Domain-Treffer gehen nach ganzen Labels (`mueller.de` trifft `shop.mueller.de`, nie `baeckerei-mueller.de`). Für eine Zeile ohne E-Mail ist ein Treffer mit `match_kind: website_identity` derselbe Lead (der Import verlinkt ihn nur); `company_known` heißt „Firma bekannt" (Warnung, kein Ausschluss). Ohne `match_kind` (älterer Server, Teilstring-Vergleich) selbst nachprüfen: derselbe Lead nur, wenn der Host der `website` des Treffers (ohne `www.`) gleich der geprüften Domain ist. Den kompletten Listen-Flow beschreibt `/outreach-lists`.

## Phase 2: Import

```text
import_leads(leads=[…], campaign_id=…, list_id=…, attribute_mappings={…})
```

- `list_id` für beschaffte Listen immer setzen (Herkunft + späteres Aufräumen via `delete_list`); die Liste vorher mit `create_list` anlegen und die Herkunft in `source` festhalten. Listen-Verwaltung: `/outreach-lists`.
- Mehrere Pakete sequentiell importieren (Größe siehe Phase 1, im Chat etwa 100–300 je Aufruf) und jeweils den Job abwarten; so bleibt ein Fehler eingrenzbar.
- Response: `job_id` (der Import läuft asynchron), `received`, ab 3.0.0 auch `accepted`, `rejected_total`, `rejected_rows` (höchstens 100, `[{row, code, field, reason}]`, `row` = nullbasierter Index der Eingabe; im Job-Ergebnis `rejected` heißt dasselbe Feld `rowIndex`, die Werte sind gleich) und `notices_count`; bei den Links der Antwort (`appUrl`) kann der Nutzer den Stand in der Oberfläche sehen. Abgelehnte Zeilen nicht erneut senden, sondern mit Grund berichten.
- Dedup macht das Backend: listenintern und gegen bestehende Leads, mit E-Mail über die Adresse, ohne E-Mail über die Website (Host); bestehende Leads werden nur zur Kampagne bzw. Liste verlinkt (kein Duplikat, keine Feld-Überschreibung). `do_not_contact`-Leads werden nicht in Kampagnen aufgenommen und im Ergebnis gemeldet.

## Phase 3: Job pollen & Report

Der Import ist ERST fertig, wenn der Job es sagt — nie nach festem Warten zählen:

1. `get_job_status(job_id)` pollen (anfangs alle ~5 s, bei großen Imports alle 15–30 s), bis `status` = `completed` oder `failed`. Kleine Imports sind oft nach Sekunden fertig, ein 10.000er kann mehrere Minuten laufen. Einen Prozentwert meldet der Import nicht – nicht auf einen Fortschritt warten, nur auf den Status. In Claude Code mit Plugin `outreach` zeigt das Band den Stand selbst an; dort reicht eine Abfrage am Ende für den Report.
2. Das Job-Result enthält die Wahrheit:
   - Zahlen: `imported`, `consolidated` (bereits bekannte Leads, die mit dem Bestand zusammengeführt wurden), `total`; ab 3.0.0 zusätzlich `created`, `relinked`, `email_filled` (Bestands-Leads ohne E-Mail, deren Website eine Zeile mit E-Mail trug), `rejected_count` mit `rejected_by_code` und `notices_count`.
   - **Listen, keine Zahlen:** `duplicates` (Zeilen, die als Bestands-Lead nur verlinkt wurden; `email` kann null sein, `matchedVia` sagt `email` oder `domain`), `internalDuplicates` (doppelt in der Datei), `do_not_contact_hits` (Bestands-Leads mit Kontaktsperre), `rejected` (abgelehnte Zeilen mit Code), `errors` (Zeilenfehler als Text). Im Report die **Anzahl** der Einträge nennen, bei wenigen Treffern auch Adresse bzw. Website.
   - `linked_to_list` (bei `list_id`: `list_id`, `name`, `newly_linked`).
   Diese Werte an den Nutzer berichten — NICHT stattdessen `list_leads` zählen (während der Job läuft, fehlen Leads, und der Report würde Doppel-Importe provozieren).
3. Optional zur Sichtkontrolle danach: `list_leads(campaign_id, fit_level="", research_status="", campaign_status="processing")`.
4. Report: übergeben / importiert / davon ohne E-Mail (die Recherche sucht die Adresse) / abgelehnt je Grund / Duplikate / do_not_contact-Treffer / vorab entfernte Zeilen / `job_id`.

## Fehlerbehandlung

Erwartete Tool-Fehler sind MCP-Tool-Results mit `isError: true`; ihr Text beginnt mit `<lowercase_code>:`. Es gibt kein strukturiertes Fehler-Payload.

| Code | Aktion |
|------|--------|
| `validation_failed` mit inline aufgeführten Zeilen | Ab 3.0.0: keine einzige Zeile war importierbar, Codes lesen und die Daten korrigieren. Älterer Server: genannte Zeilen fixen/entfernen, erneut senden |
| `validation_failed` zu `attribute_mappings` | Mapping nach dem Schema oben korrigieren |
| `limit_reached` | Chunk verkleinern (max. 10.000 pro Call) bzw. Nutzer informieren (Plan-Limit `max_leads`) |
| `campaign_not_found` / `list_not_found` | IDs prüfen (`list_campaigns` / `list_lists`) |
| `import_failed` | Meldung berichten, Import nicht blind wiederholen |
| `insufficient_scope` / `access_denied` | Token mit Scope `leads:write` verwenden |
| Job `failed` in `get_job_status` | Fehlertext aus dem Job-Result berichten; Import NICHT blind wiederholen (Teilzustand prüfen via `list_leads`) |

## Hinweise

- `secondaryEmails` wird vom Bulk-Import-Pfad nicht verarbeitet (nur via `write_lead_details`).
- **Kosten bei Leads ohne E-Mail:** Sie durchlaufen Qualifizierung und Recherche, auch wenn am Ende keine Adresse gefunden wird (Server-Lauf etwa 2 bis 3 Cent je Lead bzw. Abo-Kontingent), und belegen einen Platz im `max_leads`-Kontingent. Bei großen Listen dem Nutzer anbieten, die Adressen vorab zu beschaffen (Plugin `datenbeschaffung`, `impressum-enrichment`).
- Import und Verarbeitung sind getrennt: Nach dem Job-Ende `start_lead_run` (vorher `list_lead_runs(active_only=true)` prüfen).

## Verwandt

- `/outreach-lists` (Vorab-Dedup, Listen-Verwaltung, Liste→Kampagne)
- `/outreach-campaign` (Kampagne zuerst), `/outreach-pipeline` (nächster Schritt)
- die Tool-Beschreibungen des MCP-Servers
