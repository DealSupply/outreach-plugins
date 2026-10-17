# ListM8-MCP: Import- und Bestands-Tools

Vertragsstand: ListM8 MCP 3.0.0 (16.10.2026: Leads ohne E-Mail). Die Referenz deckt die Tools ab,
die in der Datenbeschaffung gebraucht werden. Die vollständige Werkzeugliste liefert die
Tool-Discovery des MCP-Servers; jede Werkzeugbeschreibung dort ist der aktuelle Vertrag und geht
dieser Referenz im Zweifel vor.

**Versionsprüfung:** `ping` liefert `version`. Ab `3.0.0` gilt diese Referenz („E-Mail ODER eigene
Website“). Älterer Server oder `ping` ohne Version: Jede Zeile braucht weiter eine gültige E-Mail
(alter Kontrakt, `build_csv.py --uebergabe email`), und `import_leads` lehnt den ganzen Aufruf ab,
sobald eine Zeile ohne gültige E-Mail dabei ist. Meldet ein 3.0.0-Server trotzdem
`validation_failed … "email"`, ebenfalls auf den alten Kontrakt zurückfallen und es dem Nutzer sagen.

## Was ListM8 heute (nicht) kann

- ListM8 scrapt **nicht**. Es gibt keinen Quellenkatalog, keine serverseitigen Quellenläufe, keine
  Beschaffungsaufträge und kein serverseitiges Impressum oder Verifizieren.
- Der Kunde scrapt mit **eigenem Apify- oder Outscraper-Konto** außerhalb von ListM8, bereinigt die
  Ergebnisse und lädt sie hoch: über die Oberfläche (Leads, CSV-Import) oder per MCP `import_leads`,
  optional in eine Liste (`create_list`, `list_id`).
- Kosten fallen beim Anbieter an. ListM8 erfasst sie nicht; wer sie festhalten will, trägt sie in
  `source` der Liste ein (`costUsd`).
- Es gibt keinen Probelauf als Produktfunktion. Der Pilot ist ein kleiner, freigegebener Scrape beim
  Anbieter.

## Konventionen

- Argumente der Tools sind snake_case (`list_id`, `lead_ids`, `attribute_mappings`).
- Fehler kommen als Tool-Ergebnis mit `isError: true` und dem Text `<code>: <Meldung>`. Die Codes
  stehen unten bei den Tools.
- Scopes: `leads:read` zum Lesen, `leads:write` zum Schreiben (schließt Lesen ein). Fehlt der Scope,
  Verbindung und Berechtigungen der MCP-Verbindung klären.
- Antworten tragen teils ein Feld `appUrl` mit einem Link in die App; dem Nutzer gern weitergeben.

## Überblick

| Tool | Zweck | Scope |
|---|---|---|
| `check_leads_exist` | E-Mails und Domains gegen den Bestand prüfen (Dedup vor Anreicherung und Import) | read |
| `export_leads` | Bestand als `json`, `csv` oder kompakter Index (`index`) | read |
| `list_lists` | Eigene Listen mit Zählern und Herkunft | read |
| `get_list` | Eine Liste mit Metadaten und Leads (paginiert) | read |
| `search_leads` | Globale Suche im Lead-Bestand | read |
| `create_list` | Liste mit Herkunft anlegen | write |
| `import_leads` | Leads importieren (asynchron, `job_id`) | write |
| `get_job_status` | Status eines asynchronen Jobs | read |
| `bulk_set_lead_attributes` | Dieselben Attributwerte auf viele Leads setzen | write |
| `add_leads_to_campaign` | Vorhandene Leads einer Kampagne zuordnen | write |
| `mark_leads_contacted` | Kontaktstatus mehrerer Leads setzen | write |
| `delete_list` | Liste löschen, optional sichere Leads mit | write |

## Signaturen

```text
check_leads_exist(emails?: string[], domains?: string[])
export_leads(format?: "json"|"csv"|"index" = "json", list_id?: integer,
             contact_status?: string = "", limit?: integer, offset?: integer = 0)
list_lists(limit?: integer = 25, offset?: integer = 0)
get_list(list_id: integer, limit?: integer = 25, offset?: integer = 0)
search_leads(query?: string = "", contact_status?: string = "", attribute_key?: string = "",
             attribute_value?: string = "", in_campaign?: string = "",
             limit?: integer = 20, offset?: integer = 0)
create_list(name: string, description?: string = "", source?: object)
import_leads(leads: object[], campaign_id?: integer, list_id?: integer,
             attribute_mappings?: object)
get_job_status(job_id: string)
bulk_set_lead_attributes(lead_ids: integer[], attributes: object, create_missing?: boolean = false)
add_leads_to_campaign(campaign_id: integer, list_id?: integer, lead_ids?: integer[])
mark_leads_contacted(emails?: string[], lead_ids?: integer[], status?: string = "contacted",
                     source?: string = "mcp", confirm_reset?: boolean = false)
delete_list(list_id: integer, delete_leads?: boolean = false, confirm_delete?: boolean = false)
```

## Bestand prüfen

### check_leads_exist

Bis zu 1000 Einträge je Aufruf (E-Mails und Domains zusammen).

- **E-Mail-Treffer** treffen jede bekannte Adresse eines Leads. `matched_via` sagt, welche:
  `primary` (Identität), `sending` (Versandadresse, z. B. von der Recherche gefunden),
  `handed_over` (an Instantly oder per CSV übergebene Adresse), `secondary` (Zweitadresse).
- **Domain-Treffer** (`firma.de`, ohne Protokoll und `www`) treffen Websites und E-Mail-Domains
  exakt (Subdomains zählen mit, `e.de` trifft nicht mehr `home.de`). `match_kind` unterscheidet:
  - `website_identity`: Ein Lead **ohne E-Mail** ist unter genau dieser Website bekannt. Der Import
    behandelt eine Zeile mit dieser Website als denselben Lead, also wie einen E-Mail-Treffer.
  - `company_known`: Die Firma ist unter einer anderen Adresse bekannt. Ein Warnsignal, kein
    automatischer Ausschluss.
- Zeilen ohne E-Mail lassen sich nur über `domains` prüfen.
- Treffer sind pro Eintrag auf 10 begrenzt; `summary.truncated=true` meldet das (meist eine zu breite
  Domain, Eingabe eingrenzen).

Antwort: `email_matches[]` (`query`, `lead_id`, `email` (kann null sein), `sending_email`,
`contact_status`, `in_campaigns`, `matched_via`), `domain_matches[]` (`domain`, `lead_id`, `email`,
`sending_email`, `website`, `contact_status`, `match_kind`) und `summary` mit `emails_checked`,
`emails_found`, `emails_new`, `domains_checked`, `domains_matched`, `website_identity_matches`,
`do_not_contact_hits`, `truncated`. Vor bezahlter Anreicherung und noch einmal unmittelbar vor
`import_leads` ausführen. `do_not_contact`-Leads niemals in eine Kampagne importieren.

### export_leads

- `format="index"`: je Lead nur `{e, d, s}` plus `se`:
  - `e`: die **Versandadresse** (sonst die Identität). Bei Leads ohne jede Adresse leer (`""`);
    ältere Server lieferten dort auch `null`. Skripte müssen beides vertragen (`dedup.py` tut das).
  - `se`: alle übrigen bekannten Adressen (Identität, falls abweichend, Zweitadressen, übergebene
    Adressen).
  - `d`: Domain der Website oder null; `s`: Kontaktstatus.
  Einmal vor einem Scrape ziehen, lokal gegen die Scrape-Ergebnisse matchen (über `e`, `se` UND `d`:
  ein Lead ohne E-Mail ist nur über seine Domain bekannt) und bekannte Domains in die
  Query-Ausschlüsse geben.
- `format="json"` liefert Zeilen (mit `sendingEmail` und `contactEmailState`), `format="csv"`
  CSV-Text (`email` = Versandadresse, `identity_email` als letzte Spalte). Beide ohne
  Qualifizierungsinfo (Urteile gelten pro Kampagne).
- `list_id` begrenzt auf eine Liste, ohne Angabe gilt der gesamte Bestand. `contact_status` filtert
  (leer = alle). `limit` 1 bis 10000 (Standard 1000, beim Index 10000), paginiert über `offset`;
  die Antwort trägt `total` und `remaining`.

### list_lists, get_list, search_leads

- `list_lists` (`limit` 1 bis 100): je Liste `id`, `name`, `description`, `source`, `leads_total`,
  `leads_in_campaigns`, `leads_contacted`. Beantwortet „was habe ich schon gescrapt?“; vor einem
  neuen Scrape ansehen.
- `get_list` (`limit` 1 bis 200): Metadaten plus eine Seite Leads (`id`, `email` (null bei Leads ohne
  Adresse), `sendingEmail`, `contactEmailState`, `company`, `website`, `city`, Kontaktstatus,
  Kampagnenzugehörigkeit), ohne Qualifizierungsinfo; `total`, `remaining`.
- `search_leads`: Suchtext (mindestens 2 Zeichen, leer erlaubt bei gesetztem Strukturfilter) gegen
  E-Mail, Firma, Website und Ort. Filter `contact_status` (`not_contacted`,
  `exported_to_instantly`, `contacted`, `replied`, `opportunity`, `do_not_contact`),
  `attribute_key` plus `attribute_value` (Custom-Attribut, exakte Übereinstimmung ohne
  Groß-/Kleinschreibung), `in_campaign` (`none` oder `any`). `limit` 1 bis 100. Liefert Kontaktstatus
  sowie Kampagnen- und Listenzugehörigkeit. Für einzelne Existenzprüfungen im Bulk
  `check_leads_exist` bevorzugen.

## Importieren

### create_list

`name` (3 bis 255 Zeichen), `description` (bis 2000 Zeichen), `source` (freies Objekt für die
Herkunft). Empfohlene Form:

```json
{"tool": "apify", "actor": "compass/crawler-google-places", "query": "sanitär köln",
 "runAt": "2026-10-03", "costUsd": 1.6}
```

Antwort: `list` mit `id`, `name`, `description`, `source`. Die Herkunft beantwortet später „was habe
ich schon gescrapt?“ und ersetzt ein manuelles Scrape-Log.

### import_leads

Bis zu 10000 Leads je Aufruf; Aufruf asynchron, Antwort mit `job_id`.

- Jede Zeile ist ein JSON-Objekt mit **einer gültigen `email` ODER einer `website`**, die keine
  reine Plattform-URL ist (Facebook, Instagram, Linktree, Doctolib, Branchenportale …; Liste:
  `plattform-hosts.md`). Baukasten-Subdomains wie `praxis.jimdosite.com` zählen als eigene Website.
  Fehlt die E-Mail: `email` weglassen oder `null`. Optional: `company`, `phoneNumber`, `city`.
- Ohne E-Mail sucht die **Recherche** in ListM8 die Kontaktadresse auf der Website. Findet sie
  eine, wird sie Versand- und Identitätsadresse. Findet sie keine, scheidet der Lead aus
  (`no_contact_email`) und bekommt nie eine Mail. Bis dahin kostet er Qualifizierung und Recherche
  und belegt einen Platz im Lead-Kontingent.
- Eine ungültige E-Mail neben einer brauchbaren Website wird verworfen, der Lead kommt ohne E-Mail
  rein (Hinweis `invalid_email_ignored`).
- Zeilen ohne E-Mail werden über die Website (Host) dedupliziert: Eine zweite Zeile mit derselben
  Website und ein Bestands-Lead mit dieser Website gelten als derselbe Lead.
- **Bekannte Google-Maps-Schlüssel** behält der Import auch ohne Mapping: `place_id`/`placeId`,
  `cid`, `rating`/`totalScore`, `reviews_count`/`reviewsCount`, `reviews_tags`/`reviewsTags`,
  `google_rezensionstexte` (Zeilen `JJJJ-MM-TT · N★ · Text` oder Array aus `{text,
  publishedAtDate, stars}`, ohne Namen der Verfasser) und `business_status`. Die Rezensionen
  liest die Recherche als eigenen Block und sucht dann nicht noch einmal nach Bewertungen.
- **Alle anderen Schlüssel** (auch `firstName`, `lastName`, `inhaber`, `kategorie`,
  `companyClean`, `hinweis`, `quelle`) werden nur gespeichert, wenn sie in `attribute_mappings`
  deklariert sind; sonst gehen sie verloren. Empfohlene Namen: `outreach-uebergabe.md`, Schritt 3.
  Mapping je Spalte entweder
  `{"action":"create_new","name":"Anzeigename","fieldType":"text"}` oder
  `{"action":"map_existing","fieldKey":"bestehender_key"}`.
- `campaign_id` verknüpft die Leads mit einer Kampagne (Pipeline-Status `processing`); ohne Angabe
  liegen sie unkategorisiert im Bestand.
- `list_id` (aus `create_list`) sammelt ALLE Leads des Imports in der Liste, neue wie bereits
  bekannte.
- Der Import startet **keine** KI-Verarbeitung. Qualifizierung, Recherche und E-Mail-Texte starten
  erst über `start_lead_run`.
- **Teilimport:** Zeilen, die die Regel nicht erfüllen, werden einzeln abgelehnt und sofort
  gemeldet; alle übrigen gehen in den Job.
- Antwort: `status`, `job_id`, `received`, `accepted`, `rejected_total`, `rejected_rows` (höchstens
  100: `[{row, code, field, reason}]`, `row` ist der nullbasierte Index der Eingabe),
  `notices_count`, `queued`, `campaign_id`, `list_id`, `appUrl`, `message`. Die vollständige Liste
  steht im Job-Ergebnis.
- Ablehnungscodes: `not_an_object`, `missing_contact` (weder E-Mail noch Website), `invalid_email`
  (ungültige E-Mail ohne brauchbare Website), `invalid_website`, `platform_only_website` (nur
  Plattform-URL, keine E-Mail), `website_too_long`, `limit_reached` (Kontingent im Lauf erschöpft).

Fehler: `validation_failed` (leere Liste, **keine einzige importierbare Zeile** mit Zeilennummern und
Codes der ersten 20, ungültiges Mapping), `limit_reached` (mehr als 10000 Zeilen oder
Plan-Kontingent erschöpft), `import_failed`. Zu große Dateien in Blöcke von höchstens 10000 teilen.

### get_job_status

`get_job_status(job_id)` bis zum Endzustand abfragen (nicht raten, wann der Import fertig ist).
Antwort: `job_id`, `appUrl`, `type`, `status` (`pending`, `processing`, `completed`, `failed`),
`result`, `error`, `created_at`, `updated_at` und, falls vorhanden, Fortschritt
(`progress_percent`, `progress_message`, `failure_reason`, `started_at`, `completed_at`).

`result` des Imports (die Zahlen 1:1 berichten):

| Feld | Bedeutung |
|---|---|
| `imported` | Neu angelegte plus neu verknüpfte Leads |
| `created` | Neu angelegte Leads, die die Zusammenführung überlebt haben |
| `relinked` | Bestands-Leads, die nur neu verknüpft wurden |
| `consolidated` | Mit bestehenden Leads zusammengeführte Zeilen |
| `email_filled` | Bestands-Leads ohne E-Mail, deren Website eine Zeile mit E-Mail trug |
| `total` | Zeilen im Aufruf |
| `duplicates` | Liste der Zeilen, die als Bestands-Lead nur verlinkt wurden (nie doppelt angelegt) – Anzahl = Länge. Je Eintrag `email` (kann null sein), `website`, `matchedVia` (`email` oder `domain`) |
| `internalDuplicates` | Liste der Dubletten innerhalb der Eingabe, mit `matchedVia` und `duplicateOfRowIndex` |
| `do_not_contact_hits` | Liste der Treffer mit `do_not_contact` (`leadId`, `email`, kann null sein) |
| `contact_blocked_hits` | Bestands-Leads, die schon kontaktiert sind und deshalb nicht neu verknüpft wurden |
| `rejected` / `rejected_count` / `rejected_by_code` | Abgelehnte Zeilen (`rowIndex`, `code`, `field`, `value`; höchstens 500) mit Gesamtzahl und Zahl je Code |
| `notices` / `notices_count` | Hinweise zu angenommenen Zeilen (`invalid_email_ignored`, `website_ignored`, `website_shortened`, `phone_dropped`, `field_truncated`) |
| `linked_to_list` | Bei `list_id`: `list_id`, `name`, `newly_linked`; sonst null |
| `errors` | Liste der Zeilenfehler (Text) |

## Nachbearbeiten

- `bulk_set_lead_attributes`: dieselben Attributwerte auf bis zu 1000 Leads (höchstens 10
  Attribute), z. B. `{"kategorie":"Sanitär","quelle":"apify 2026-10-03"}`. Attribute werden über
  den `fieldKey` angesprochen; unbekannte Keys schlagen fehl, außer `create_missing=true` (legt sie
  als Textattribute an). Bestehende Werte werden überschrieben. Antwort: `updated`,
  `missing_lead_ids`, `attributes_written`, `attributes_created`. Für unterschiedliche Werte je Lead
  `write_lead_details` verwenden.
- `add_leads_to_campaign`: genau eines von `list_id` oder `lead_ids` (höchstens 1000). Mit `list_id`
  darf die Liste höchstens 1000 Leads haben, sonst `limit_reached`; größere Listen in
  `lead_ids`-Blöcken verlinken oder in der Oberfläche über „Zur Kampagne hinzufügen“ an der Liste
  zuordnen. Bereits zugeordnete Leads werden übersprungen, `do_not_contact`-Leads **nie** verlinkt.
  Antwort: `added`, `already_in_campaign`, `skipped_do_not_contact`. Die Qualifizierung beginnt in
  der Zielkampagne von vorn (Urteile gelten pro Kampagne), vorhandene Recherche wird wiederverwendet.
  Danach `start_lead_run`.
- `mark_leads_contacted`: setzt den globalen Kontaktstatus (höchstens 1000), entweder `emails` oder
  `lead_ids`. `status` ist `contacted` (Standard), `replied`, `opportunity`, `do_not_contact` oder
  `not_contacted` (Zurücksetzen nur mit `confirm_reset=true`). Status werden nie herabgestuft;
  `exported_to_instantly` setzt nur der Instantly-Push. Eine Adresse trifft Identität,
  Versandadresse, übergebene Adressen und (nur beim Hochsetzen, nicht beim Zurücksetzen)
  Zweitadressen; trifft sie mehrere Leads, gilt der Status für alle (`leads_matched`, `matched_via`).
  Leads ganz ohne Adresse nur über `lead_ids`. Nicht gefundene Einträge stehen in
  `unmatched_emails` beziehungsweise `unmatched_lead_ids`. Dient dazu, extern kontaktierte Leads
  abzugleichen, damit niemand doppelt angeschrieben wird.
  Zurückgesetzt werden nur kontaktierte Leads ohne Reaktion (keine Antwort, kein Interesse, keine
  Abmeldung, kein Bounce) und mit beendeter Instantly-Sequenz. Ein zurückgesetzter Lead bekommt
  beim nächsten `start_lead_run` neue Recherche und neue E-Mail, braucht eine neue Freigabe und
  lässt sich danach nur in eine andere Instantly-Kampagne übertragen. Alle anderen bleiben
  unverändert und stehen je Grund in `reset_blocked`: `replied`, `opportunity`, `do_not_contact`,
  `exported` (hochgeladen, noch nicht angeschrieben), `reaction`, `sequence_active` (Sequenz läuft
  noch), `not_synced` (noch nicht mit Instantly abgeglichen).

## Aufräumen

`delete_list(list_id, delete_leads=false, confirm_delete=false)` entfernt standardmäßig nur die
Gruppierung, alle Leads bleiben. Mit `delete_leads=true` (verlangt `confirm_delete=true`, sonst
`confirmation_required`) werden zusätzlich nur Leads gelöscht, die nie kontaktiert wurden, in keiner
Kampagne und in keiner anderen Liste sind; alle übrigen werden nur gelöst. Das macht Test-Importe
rückgängig und gibt das `max_leads`-Kontingent wieder frei. Antwort: `deleted_list`,
`leads_deleted`, `leads_detached`. Das Löschen von Leads ist unwiderruflich: nur auf ausdrücklichen
Wunsch.

## Ausscheiden ohne Adresse

Findet die Recherche für einen Lead ohne E-Mail keine eigene Kontaktadresse, scheidet er mit dem
Grund `no_contact_email` aus: keine Mail-Generierung, keine Freigabe, kein Export, kein
Instantly-Push. `save_lead_variables` und `approve_lead_variables` lehnen ihn mit
`no_contact_email:` ab, `get_lead_data` bleibt erlaubt (die Abo-Recherche braucht es). Der Zustand
steht als `contactEmailState` (`present`, `searching`, `not_found`) an jedem Lead;
`get_lead_run_status` zählt ihn in `skipReasons`. Kommt später eine Adresse dazu (Nachrecherche,
App, `write_lead_details` mit `bestEmail`), fällt die Sperre von selbst weg.

## Weiterverarbeitung

Nach dem Import: Liste prüfen (`get_list`), auf Wunsch einer bestätigten Kampagne zuordnen
(`add_leads_to_campaign`) und über den Outreach-Workflow `start_lead_run` für `qualification`,
`research`, `email` verarbeiten. `start_lead_run` nimmt keine `list_id`; die Auswahl der Leads
erfolgt über die Kampagne. Vorher aktive Lead-Läufe prüfen (`list_lead_runs`). Kosten des KI-Laufs
sind getrennt vom Scrape beim Anbieter abzustimmen.
