# Outreach-Übergabe — vom Scrape in die App

> Der EINE Übergabe-Ablauf. `listen-qualitaet` führt ihn aus; kein Weg-Skill implementiert ihn selbst.
> Voraussetzung: ListM8-MCP verbunden (Tools `check_leads_exist`, `create_list`, `import_leads`,
> `get_job_status`, `add_leads_to_campaign`, `export_leads`; Signaturen in `listm8-mcp.md`).
> Ohne MCP: CSV-Weg über die Oberfläche am Ende. Gescrapt wird beim Kunden mit eigenem Apify- oder
> Outscraper-Konto; ListM8 importiert nur das fertige Ergebnis.

## Der Ablauf (E2E-verifiziert am 19.08.2026)

### 0. Vorab-Abgleich — VOR der kostenpflichtigen Anreicherung

Einmal je Lauf den Bestandsindex ziehen und lokal matchen:

```
export_leads(format="index")            # kompakter Index: {e: email, d: root-domain, s: status}
→ als bestand-index.json speichern
python3 ../datenbeschaffung-referenzen/scripts/dedup.py --index bestand-index.json --in roh.csv --out neu.csv
```

`dedup.py` entfernt: exakte E-Mail-Treffer (inkl. secondaryEmails), `do_not_contact`-Leads
(hart, landen in einer eigenen Report-Zeile) und markiert Domain-Treffer („Firma schon im
Bestand") als Warnung — Domain-Treffer sind KEIN automatischer Ausschluss, neue Ansprechpartner
sind legitim. Bekannte Domains zusätzlich in die Query-Ausschlüsse des nächsten Laufs geben.

**Warum vorab:** Jeder bekannte Lead, der trotzdem durch Impressum/Verify läuft, ist verbranntes
Geld. Der Import würde ihn später ohnehin deduplizieren — aber dann ist das Geld schon weg.

### 1. Autoritäts-Check unmittelbar vor dem Import

Der Index kann Minuten alt sein — die Übergabe prüft gegen die Wahrheit:

```
check_leads_exist(emails=[...], domains=[...])     # bis 1.000 Einträge je Call (E-Mails und Domains zusammen)
```

Ergebnis dem Nutzer zeigen: „X neu, Y schon im Bestand (werden nur verlinkt), Z do_not_contact
(werden nie angeschrieben)."

### 2. Liste anlegen — mit Herkunft

```
create_list(
  name="<Nische> <Region> — <Datum>",
  description="<Weg> / <Query-Kurzfassung>",
  source={tool:"apify", actor:"<actor-id>", query:"<query>", runAt:"<iso>", costUsd:<real>}
)
```

Die Herkunft beantwortet später „was habe ich schon gescrapt?" (`list_lists`) — sie ersetzt jedes
manuelle Scrape-Log.

### 3. Import in die Liste

**WICHTIG — was ohne Mapping verloren geht:** `import_leads` kennt als Kernfelder nur
`email`, `company`, `website`, `phoneNumber`, `city`, `status`. Die Google-Spalten aus
`build_csv.py` (`rating`, `reviews_count`, `place_id`, `reviews_tags`,
`google_rezensionstexte`) erkennt der Import von selbst und legt die passenden Attribute an.
JEDE andere Spalte — auch `firstName`/`lastName`, `inhaber`, `companyClean`, `hinweis` und alle
Plattform-Spalten — überlebt den Import NUR, wenn sie in `attribute_mappings` deklariert ist.
Nicht deklarierte Spalten werden stillschweigend verworfen. Deshalb: vor dem Import die
CSV-Header auflisten und für jede weitere Spalte ein Mapping setzen.

Die Attributnamen entscheiden, wie die KI der Plattform den Wert liest (Kontaktperson,
Bewertung, Reichweite, Kategorie). Deshalb genau diese Namen verwenden:

```
import_leads(leads=[...], list_id=<id>, attribute_mappings={
  "firstName":     {"action":"create_new","name":"Vorname","fieldType":"text"},
  "lastName":      {"action":"create_new","name":"Nachname","fieldType":"text"},
  "inhaber":       {"action":"create_new","name":"Inhaber","fieldType":"text"},
  "inhaber_rolle": {"action":"create_new","name":"Inhaber Rolle","fieldType":"text"},
  "kategorie":     {"action":"create_new","name":"Kategorie","fieldType":"text"},
  "quelle":        {"action":"create_new","name":"Quelle","fieldType":"text"},
  "companyClean":  {"action":"create_new","name":"Firma (Ansprache)","fieldType":"text"},
  "hinweis":       {"action":"create_new","name":"Hinweis","fieldType":"text"}
  // je nach Weg zusätzlich, nur wenn die Spalte in der CSV steht:
  // "position": "Position" · "headline": "LinkedIn Headline" · "linkedin_url": "LinkedIn-Profil" (url)
  // "connections": "LinkedIn Kontakte" (number) · "mitarbeiter": "Mitarbeiter" (number)
  // "instagram_url": "Instagram-Profil" (url) · "follower": "Instagram Follower" (number)
  // "bio": "Instagram Bio" · "link_typ": "Bio-Link" · "gefunden_via_hashtag": "Instagram Hashtag"
  // "plattform": "Verkaufsplattform" · "seller_url": "Shop-Seite" (url) · "verkaeufe": "Verkäufe"
  // "bewertung": "<Plattform>-Bewertung" (number) · "bewertungen_anzahl": "<Plattform>-Bewertungen Anzahl" (number)
  // "umsatz_geschaetzt": "Umsatz geschätzt" · "apps": "Shop-Apps"
})
→ get_job_status(job_id) pollen bis completed (höchstens 10.000 Zeilen je Call, größere Dateien in Blöcke teilen)
```

Beim Umwandeln der CSV in `leads=[...]`: leere Zellen weglassen, Zahlen (`rating`,
`reviews_count`, `follower`) als Zahl senden, `google_rezensionstexte` als Text mit
Zeilenumbrüchen übernehmen. Eine Plattform-Bewertung heißt nie `rating`: Dieser Name ist der
Google-Bewertung vorbehalten.

Existiert ein Attribut aus einem früheren Lauf bereits, statt `create_new` auf das
vorhandene Attribut mappen: `{"action":"map_existing","fieldKey":"<bestehender_key>"}`.

Der Job-Report (`result` aus `get_job_status`) liefert die Zahlen `imported`, `consolidated` und
`total`, dazu `linked_to_list` und die **Listen** `duplicates` (nur verlinkt, nie doppelt),
`internalDuplicates`, `do_not_contact_hits` und `errors` – davon die Anzahl der Einträge berichten.
Importieren startet keine KI-Verarbeitung.

### 4. Optional: direkt in eine Kampagne

Nur wenn der Nutzer es will — Rohmaterial darf als Liste liegen bleiben (Quarantäne by design):

```
add_leads_to_campaign(campaign_id=<id>, list_id=<id>)
```

`do_not_contact`-Leads werden vom Tool selbst übersprungen und gemeldet. Mit `list_id` nimmt das
Tool höchstens 1000 Leads je Aufruf (sonst `limit_reached`); größere Listen in `lead_ids`-Chunks
verlinken (siehe `outreach-lists`). Die Oberfläche kennt Listen noch nicht, eine Liste lässt sich
dort nicht ganz einer Kampagne zuordnen. Danach startet
`start_lead_run` die Qualifizierung — NICHT automatisch, der Nutzer entscheidet.

### 5. Aufräumen nach Test-Läufen

Ein misslungener Test-Import ist kein Dauerschaden:

```
delete_list(list_id=<id>, delete_leads=true, confirm_delete=true)
```

Gelöscht werden nur nie kontaktierte Leads ohne Kampagne und ohne andere Liste — alles andere wird
entkoppelt und gemeldet. Das gibt auch das `max_leads`-Limit wieder frei.

## CSV-Fallback (kein MCP verbunden)

Die geprüfte Liste als CSV im Format aus `csv-spalten.md` liefern, dazu die Anleitung:
„In der App: Leads → CSV-Import, Datei hochladen und Spalten zuordnen; die Zusatzspalten werden als Attribute angeboten."
Der Vorab-Abgleich entfällt dann — im Bericht ausdrücklich sagen, dass Duplikate erst der
App-Import abfängt und `do_not_contact` NICHT vorab geprüft werden konnte.
