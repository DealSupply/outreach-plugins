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
export_leads(format="index")            # kompakter Index: {e: email, d: Website-Host, s: status, se: Zweitadressen}
→ als bestand-index.json speichern
python3 ../datenbeschaffung-referenzen/scripts/dedup.py --index bestand-index.json --in roh.csv --out neu.csv
```

`dedup.py` entfernt: exakte E-Mail-Treffer (inkl. secondaryEmails),
`do_not_contact`-Leads (hart, landen in einer eigenen Report-Zeile) und Zeilen ohne E-Mail, deren
Website-Host schon ein Lead ohne E-Mail im Bestand trägt (derselbe Lead, nur bei exakt gleichem
Host). Domains vergleicht es wie `check_leads_exist` nach ganzen Labels (ohne `www.`, Umlaut-Domains
als Punycode): `mueller.de` trifft nie `baeckerei-mueller.de`, ein Bestands-Lead auf
`shop.mueller.de` macht eine Zeile `mueller.de` nur zur Warnung. Übrige Domain-Treffer
markiert es als Warnung („Firma schon im Bestand“): KEIN automatischer Ausschluss, neue
Ansprechpartner sind legitim. Bei Zeilen ohne E-Mail ist ein Domain-Treffer meist dieselbe Firma;
dann `--drop-known-domains-ohne-email`. `e` ist bei Leads ohne E-Mail leer (auch null möglich);
`dedup.py` verträgt beides. Bekannte Domains zusätzlich in die Query-Ausschlüsse des nächsten
Laufs geben.

**Warum vorab:** Jeder bekannte Lead, der trotzdem durch Impressum/Verify läuft, ist verbranntes
Geld. Der Import würde ihn später ohnehin deduplizieren — aber dann ist das Geld schon weg.

### 1. Autoritäts-Check unmittelbar vor dem Import

Der Index kann Minuten alt sein — die Übergabe prüft gegen die Wahrheit:

```
check_leads_exist(emails=[...], domains=[...])     # bis 1.000 Einträge je Call (E-Mails und Domains zusammen)
```

E-Mails aller Zeilen mit Adresse und die Domains aller Zeilen ohne Adresse prüfen (ab ListM8 MCP
3.0.0). Für eine Zeile ohne E-Mail ist ein Domain-Treffer mit `match_kind: website_identity`
derselbe Lead (wird nur verlinkt); `company_known` heißt „Firma bekannt“ (Warnung, kein
Ausschluss). Liefert der Server kein `match_kind` (älterer Server, Teilstring-Vergleich), selbst
nachprüfen: derselbe Lead nur, wenn der Host der `website` des Treffers (ohne `www.`) gleich der
geprüften Domain ist.
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

**Kernfelder:** Jede Zeile braucht eine gültige `email` **oder** eine eigene `website` (ab ListM8
MCP 3.0.0; Profil-Links wie Instagram oder Linktree zählen nicht, Baukasten-Subdomains schon). Fehlt
die E-Mail, das Feld weglassen. Ältere Server verlangen die E-Mail in jeder Zeile und lehnen sonst
den ganzen Aufruf ab (`listm8-mcp.md`, Versionsprüfung).

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

Die Antwort von `import_leads` meldet sofort `accepted` und `rejected_total` mit den ersten
`rejected_rows` (Zeile, Code, Grund): Abgelehnte Zeilen nennen, nicht wiederholen. Der Job-Report
(`result` aus `get_job_status`) liefert die Zahlen `imported`, `created` (davon `created_without_email` ohne E-Mail, auf neueren Servern), `relinked`,
`consolidated`, `email_filled`, `total`, `rejected_count` (mit `rejected_by_code`) und
`notices_count`, dazu `linked_to_list` und die **Listen** `duplicates` (nur verlinkt, nie doppelt),
`internalDuplicates`, `do_not_contact_hits` und `errors` – davon die Anzahl
der Einträge berichten. Importieren startet keine KI-Verarbeitung.

### 4. Optional: direkt in eine Kampagne

Nur wenn der Nutzer es will — Rohmaterial darf als Liste liegen bleiben (Quarantäne by design):

```
add_leads_to_campaign(campaign_id=<id>, list_id=<id>)
```

`do_not_contact`-Leads werden vom Tool selbst übersprungen und gemeldet. Mit `list_id` nimmt das
Tool höchstens 1000 Leads je Aufruf (sonst `limit_reached`); größere Listen in `lead_ids`-Chunks
verlinken (siehe `outreach-lists`) oder in der Oberfläche über „Zur Kampagne hinzufügen“ an der
Liste ganz zuordnen. Danach startet
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
Der App-Import folgt derselben Regel wie `import_leads` (E-Mail oder eigene Website, abgelehnte
Zeilen mit Grund im Ergebnis). Läuft die App noch mit einem älteren Server (unter 3.0.0), die
Übergabe-CSV mit `build_csv.py --uebergabe email` bauen.
Der Vorab-Abgleich entfällt dann — im Bericht ausdrücklich sagen, dass Duplikate erst der
App-Import abfängt und `do_not_contact` NICHT vorab geprüft werden konnte.
