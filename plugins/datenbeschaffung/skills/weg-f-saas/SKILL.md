---
name: weg-f-saas
description: Weg F des Datenbeschaffungs-Pakets: B2B-Software- und SaaS-Firmen mit Sitz in Deutschland, Österreich und der Schweiz, möglichst vollständig. Stapelt kostenlose Verzeichnisse (OMR Reviews, Startbase) mit der LinkedIn-Firmensuche, führt auf die Domain zusammen und prüft den Firmensitz im Impressum. Invoked by the datenbeschaffung master; never triggered directly by the user.
---

# Weg F: SaaS- und Software-Firmen in DACH

Für alle, die Software-Anbietern etwas verkaufen: Marketing, SEO und GEO, Vertrieb, Recruiting,
Finanzierung, Integrationen. Ziel ist nicht eine Stichprobe, sondern **möglichst alle**
SaaS-Firmen einer Region.

**Der Kernbefund (Vollerhebung Hamburg, 14.10.2026):** Keine Quelle findet allein mehr als etwa
ein Viertel. In Hamburg lieferte LinkedIn 387 B2B-SaaS, OMR Reviews 246 Anbieter mit Hamburger
Impressum und Startbase 135 B2B-SaaS. LinkedIn und OMR teilten sich nur 62 Firmen, LinkedIn und
Startbase 27. Hochgerechnet gibt es in Hamburg 1.500 bis 2.000 SaaS-Firmen (Lincoln-Petersen
über beide Paare). Wer nur OMR und Capterra nimmt, erreicht etwa ein Sechstel. Deshalb stapelt
dieser Weg Quellen und führt sie über die Domain zusammen. Die Überschneidung ist zugleich ein
Qualitätssignal: Wer in zwei Quellen steht, verkauft sicher ein Produkt.

Voraussetzungen vom Master: bestätigter ICP-Satz mit Größe und Region, Zugriffsweg steht
(`../datenbeschaffung-referenzen/references/zugriff.md`), Vorab-Abgleich gelaufen
(`check_leads_exist` bzw. `export_leads(format="index")` + `dedup.py`, falls MCP verbunden).

**Was kostet, was nicht:** OMR, Startbase, Sitzprüfung, Zusammenführen und das Einordnen durch
Claude kosten nichts und brauchen kein Apify. Drei Stufen laufen im eigenen Apify-Konto des Kunden
und brauchen **je eine eigene Freigabe mit genanntem Preis und hartem Deckel**: LinkedIn-Suche
(Schritt 3), LinkedIn-Details (Schritt 4), Website-Suche (Schritt 5). Die Skripte brauchen Python 3
und Internetzugang (Claude Code, Codex, Terminal). Fehlt das, nur die LinkedIn-Stufen über den
Apify-Zugriffsweg fahren und ausdrücklich sagen, dass OMR und Startbase fehlen.

## Schritt 0: ICP in Größe und Region übersetzen

| ICP-Merkmal | Wirkung |
|---|---|
| Größe | Bestimmt die LinkedIn-Segmente und damit die Kosten: 11 bis 200 Mitarbeiter sind in DACH rund 10.000 Software-Firmen, 1 bis 10 noch einmal rund 20.000 (überwiegend Freelancer und Kleinstagenturen) |
| Region | DACH, ein Land, ein Bundesland oder eine Stadt |
| Kategorie | Optional: OMR-Kategorien (z. B. `crm`, `time-tracking`) grenzen den OMR-Teil ein |
| Anti-ICP | Agenturen, Softwareentwicklung im Auftrag, Systemhäuser, Spielestudios, internationale Konzerne mit Büro in DACH. Sie fallen in Schritt 4 und 6 heraus |

## Schritt 1: OMR Reviews (kostenlos, immer zuerst)

OMR Reviews ist das größte deutschsprachige Software-Verzeichnis und hat eine öffentliche
Schnittstelle ohne Anmeldung. Ein Abruf holt alle Produkte in etwa einer Minute.

```
python3 ../datenbeschaffung-referenzen/scripts/omr_products.py --out omr.json
```

- 14.023 Produkte, 12.593 Anbieter-Domains. `--dach` behält nur .de/.at/.ch oder deutsche
  Rechtsform (3.745 Domains), verliert aber die vielen DACH-Anbieter mit .com, .io oder .ai.
  Für „alle“ deshalb ohne `--dach` laden; den Sitz klärt Schritt 6. Belegt: 4.640 OMR-Anbieter
  haben ihren Sitz in DACH (DE 4.023, AT 343, CH 274), 1.565 davon mit .com-Domain, 1.546 mit
  mindestens einer Bewertung.
- Je Anbieter kommen Produktname, Kategorie, OMR-Bewertung, Anzahl der Bewertungen, Link zum
  OMR-Profil und ob es einen Testzugang gibt. **Das ist der Einstieg für die Mail** (Kategorie und
  Bewertung sind öffentlich und nachprüfbar).
- `--kategorie crm,time-tracking` grenzt auf Kategorien ein, `--min-reviews 1` auf bewertete
  Produkte (aktiv gepflegte Einträge, Hinweis auf Marketing-Budget).
- **Fallen:** Das Feld „Serverstandort Deutschland“ ist nicht der Firmensitz; der Sitz steht nur
  im Impressum. Der Titel ist der Produktname, nicht die Firma.

## Schritt 2: Startbase (kostenlos, nur Deutschland)

Startbase pflegt je Firma das Geschäftsmodell (SaaS) und die Zielgruppe (B2B). Von 9.665 Profilen
sind 2.209 aktive B2B-SaaS (Stand 14.10.2026), mit Rechtsträger, Ort, Teamgröße und
Gründungsjahr; 54 % haben 1 bis 10 Mitarbeiter, 35 % 11 bis 50.

```
python3 ../datenbeschaffung-referenzen/scripts/startbase_saas.py --out startbase.json [--bundesland Hamburg]
```

Alle Profile zu lesen dauert gedrosselt rund 25 Minuten. `--bundesland` filtert erst nach dem
Lesen; für eine Stadt also trotzdem alle Profile lesen, nicht `--max` (eine Zufallsstichprobe aus
ganz Deutschland, nur zum Schätzen der Quote). Die Website gibt Startbase nur mit Login heraus;
sie kommt in Schritt 5.

## Schritt 3: LinkedIn-Firmensuche (Apify, die Masse)

LinkedIn findet die Firmen, die in keinem Verzeichnis stehen. Actor und Preise:
`apify-actors.md`, Abschnitt LinkedIn-Firmen.

**Regeln aus den Tests (14.10.2026):**
- Branche `industryIds: ["4"]` (Software Development) plus **Region** plus **Größenklasse**.
  Ohne Region („Germany“) waren nur 24 % der Treffer in DACH ansässig; die Standortsuche liefert
  jede Firma mit irgendeinem Büro dort, sortiert nach Größe, also zuerst Google und Microsoft.
- Keine freie Suche „SaaS“: Nur 16 % der Treffer saßen in DACH, viele Agenturen und Berater.
- Eine Suche liefert höchstens 1.000 Firmen (20 Seiten zu 50). Deshalb segmentieren: Bundesland
  bzw. Stadt × Größenklasse. Die Trefferzahl je Segment kostet fast nichts (`maxItems: 1` im
  Short-Modus, 0,0015 $), die Zahl steht in `_meta.pagination.totalResultCount`. Erst zählen,
  dann die Summe als Kosten nennen.
- Größenordnungen (Branche 4): Deutschland 1 bis 10 Mitarbeiter 13.900, 11 bis 50 Mitarbeiter
  5.200; Berlin 11 bis 50 Mitarbeiter 904, München 11 bis 50 Mitarbeiter 1.060, Hamburg alle
  Größen 1.493. Österreich 3.080 und Schweiz 6.568 über alle Größen.

**Pilot (Pflicht):** ein Segment, z. B. eine Stadt mit 11 bis 50 Mitarbeitern, `maxItems: 100`,
Deckel 0,50 $. Ausgewertet werden Sitzquote (`vorbereiten`) und SaaS-Quote (Schritt 4). Belegte
Werte als Maßstab: Sitz in der Stadt 51 bis 93 % je nach Größe, `saas_b2b` 34 bis 50 %. Liegen
beide deutlich darunter, Region oder Größenklasse prüfen, bevor skaliert wird.

```json
{"scraperMode": "short", "maxItems": 1000, "takePages": 20,
 "locations": ["Hamburg"], "industryIds": ["4"], "companySize": ["11-50"]}
```

Alle Segmente zusammenlegen und auf den Sitz in der Region filtern. LinkedIn schreibt Orte meist
englisch, deshalb beide Formen angeben (`"München,Munich"`, `"Köln,Cologne"`, `"Wien,Vienna"`):

```
python3 ../datenbeschaffung-referenzen/scripts/linkedin_saas.py vorbereiten --orte "Hamburg" --out li-hamburg seg-*.json
```

Hamburg: 1.427 Firmen, 1.149 mit Sitz in Hamburg (bei 1 bis 10 Mitarbeitern 93 %, bei über 200
Mitarbeitern 21 %).

## Schritt 4: SaaS von Agentur trennen (Claude, kostenlos), dann Details (Apify)

Die Branche „Software Development“ trennt nicht zwischen Produkt und Auftragsarbeit. Claude ordnet
jede Zeile von `li-<region>.tsv` (Name, Tagline, Follower) einer Klasse zu und schreibt
`klassen.tsv` (`slug<TAB>klasse`). In Blöcken zu 150 Zeilen lesen, keine Zeile auslassen, am
Ende die Zeilenzahl prüfen. Für mehr als etwa 300 Zeilen einen Subagenten einsetzen.

| Klasse | Bedeutung |
|---|---|
| `saas_b2b` | eigenes Software-Produkt im Abo für Unternehmen, auch Branchen-Software und APIs |
| `saas_b2c` | Consumer-App |
| `software_produkt_unklar` | eigenes Produkt, aber Lizenz, On-Premise oder Hardware im Vordergrund |
| `dienstleister` | Agentur, Auftragsentwicklung, IT-Dienstleister, Systemhaus, Beratung, Recruiting |
| `games`, `sonstiges`, `unklar` | Spiele, Verbände, Events, Investoren, zu wenig Information |

Belegt: Hamburg alle Größen 34 % `saas_b2b`, Berlin und München 11 bis 200 Mitarbeiter 50 %.
Details (Website, Mitarbeiterzahl, Beschreibung) nur für `saas_b2b`, deren LinkedIn-Seite OMR
noch nicht nennt:

```
python3 ../datenbeschaffung-referenzen/scripts/linkedin_saas.py details --in li-hamburg.json \
  --klassen klassen.tsv --bekannt omr.json --out details-input.json
```

`details-input.json` ist der Input für den Details-Actor (`apify-actors.md`); Kosten je Firma aus
`kosten.md` nennen und freigeben lassen. Die schon bekannten Firmen landen ohne Kosten in
`details-input-bekannt.json` und gehen mit in den Abgleich. Wer `software_produkt_unklar`
mitnehmen will: `--klassen-behalten saas_b2b,software_produkt_unklar`.

## Schritt 5: Zusammenführen, dann Websites nachsuchen

Reihenfolge der Quellen: LinkedIn und Startbase zuerst (sie nennen die Firma), OMR zuletzt (es
nennt das Produkt).

```
python3 ../datenbeschaffung-referenzen/scripts/quellen_zusammenfuehren.py --out kandidaten.json \
  linkedin:linkedin-details.json linkedin:details-input-bekannt.json startbase:startbase.json omr:omr.json
```

Startbase-Firmen ohne Website, die keine andere Quelle kennt, sucht danach die Google-Suche nach
Rechtsträger und Ort. Nur diese Zeilen kosten:

```
python3 ../datenbeschaffung-referenzen/scripts/website_suche.py anfragen --in kandidaten.json --out serp-input.json
# SERP-Actor aus apify-actors.md mit diesem Input (Laufzeit-Limit hoch setzen, z. B. 3.600 s), Ergebnis als serp.json
python3 ../datenbeschaffung-referenzen/scripts/website_suche.py zuordnen --in kandidaten.json --serp serp.json --out kandidaten-web.json
```

Belegt: 52 % der Startbase-Firmen ohne Website bekamen so eine (871 von 1.670, 0,83 $), in der
Stichprobe 58 %. Der
Rest sind oft eingestellte oder umbenannte Firmen; sie bleiben ohne Website und fallen später
heraus.

## Schritt 6: Sitz prüfen (kostenlos)

```
python3 ../datenbeschaffung-referenzen/scripts/sitz_check.py --in kandidaten-web.json --out geprueft.json --nur-dach
```

`sitz_check.py` liest Startseite und Impressum je Domain und ergänzt Land, PLZ und Ort, alle
Adressen der Seite (die Versandadresse wählt `build_csv.py`) und Produkt-Signale (Preisseite,
Testzugang, Login, Demo). Als Anschrift zählt nur eine PLZ mit Straße davor. `--nur-dach` behält
Firmen mit Sitz in DACH; ohne erkannten Sitz bleiben nur Firmen aus LinkedIn oder Startbase (Sitz
dort schon gesichert), reine OMR-Einträge fallen heraus.

Belegt an 379 Hamburger SaaS-Websites (27 Sekunden): 71 % mit Sitz in DACH erkannt, 73 % mit
Adresse. Ohne Treffer bleiben Seiten, die das Impressum per JavaScript laden (15 %), und
eingestellte Firmen (7 %). Fehlt nur die Adresse, kann ab ListM8 MCP 3.0.0 die Recherche der
Plattform sie auf der Website suchen (Lead mit Website importieren). Diese Lücke füllt `impressum-enrichment` nur schlecht: Der
Impressum-Actor fand an 58 solchen Seiten 19 Anschriften und 14 Adressen und brauchte über
20 Minuten. Nur für kleine, wertvolle Restmengen.

## Schritt 7: Weitere Quellen je nach Region (optional, kostenlos)

Recherchiert und auf Abrufbarkeit geprüft (14.10.2026), noch nicht in einem Lauf gemessen. Erst
eine kleine Stichprobe gegen die bestehende Liste halten, dann ergänzen:

| Quelle | Umfang | Liefert | Zugang |
|---|---|---|---|
| Swiss Made Software | 1.633 Firmen (CH) | Adresse, Ansprechpartner mit Rolle und direkter E-Mail, Website | statisch, Sitemap `/.sitemap/google.xml` |
| Softguide.de | 780 Firmen | Adresse, Geschäftsführer, Telefon, Mitarbeiter | statisch, `firmen_sitemap.xml` |
| Software Made in Germany (BITMi) | 473 Siegelträger, 640 Mitglieder | Adresse, E-Mail, Website | WordPress-Sitemap |
| European Tech Map | 704 DACH-Firmen | Sitz, Website | statisch, Länderseiten |
| DATEV-Marktplatz | 238 Produkte | Sitz im Text, DATEV-Partnerschaft als Aufhänger | Detailseiten |
| HTGF-Portfolio | rund 540 Firmen | Website, Stadt, Investor als Aufhänger | WordPress-Schnittstelle |

Für Österreich gibt es keine gute kostenlose Quelle; dort tragen LinkedIn und OMR.

**Nicht empfohlen:** Capterra und GetApp (Cloudflare; ein Actor lieferte 0 Treffer, der andere
US-sortierte Listen ohne Sitz, real 0,005 $ je Eintrag, nur etwa 5 % DACH), G2, Crunchbase,
Product Hunt (gesperrt), Dealroom (nur 8 % Deutschland, keine Website).

## Schritt 8: Roh-CSV bauen

```
python3 ../datenbeschaffung-referenzen/scripts/build_csv.py --in geprueft.json \
  --quelle "linkedin+startbase+omr <datum>" \
  --keep produkt,omr_url,kostenlos_testen,quellen,gruendung --out leads-saas-<region>-<datum>.csv
```

Mit kommen Kategorie, OMR-Bewertung und Anzahl (`bewertung`, `bewertungen_anzahl`, `plattform`),
LinkedIn-Seite, Mitarbeiter und Follower. Die Plattform liest weder OMR noch LinkedIn; was nicht
importiert wird, fehlt der Mail.

## Schritt 9: Übergabe

An `listen-qualitaet`, immer. In der Kampagne gehören die Klassen aus Schritt 4 in die
Ausschlusskriterien der Qualifizierung (Agentur, Auftragsentwicklung, Systemhaus).

## Kosten (belegt 14.10.2026, Preise GOLD-Tier)

| Umfang | Apify-Kosten |
|---|---|
| OMR, Startbase, Sitzprüfung, Zusammenführen, Einordnen | 0 $ |
| Pilot ein Segment (100 Firmen Short, rund 40 Details) | etwa 0,25 $ |
| Eine Stadt, alle Größen (Hamburg: 1.427 Short + 387 Details) | 2,52 $ (1,36 + 1,16) |
| Berlin und München, 11 bis 200 Mitarbeiter (2.745 Short + 514 Details) | 4,18 $ |
| Website-Suche für 100 Startbase-Firmen | 0,05 $ |
| Testreihe 14.10.2026 gesamt (DACH-Liste mit 6.135 Firmen, siehe `erfahrungswerte.md`) | 8,67 $ |
| DACH, 11 bis 200 Mitarbeiter (rund 10.000 Short, rund 3.500 Details) | etwa 20 $ |
| DACH inklusive 1 bis 10 Mitarbeiter | etwa 45 bis 55 $ |

## Bekannte Fallen

- **Konzern-Büros:** Die LinkedIn-Standortsuche liefert jede Firma mit einem Büro in der Region.
  Ohne `vorbereiten` (Sitzfilter) zahlt man Details für Google, Microsoft und Salesforce.
- **Zählungen schwanken:** LinkedIns Trefferzahlen sind Schätzungen; `München` und `Bayern`
  lieferten dieselbe Zahl. Für Bundesländer mit über 1.000 Treffern je Größenklasse nach
  Großstädten aufteilen.
- **Produkt ist nicht Firma:** OMR listet Produkte. `omr_products.py` legt mehrere Produkte eines
  Anbieters auf die Domain zusammen; zusammengeführt wird über die Domain, nicht über den Namen.
- **Laufzeit der SERP-Suche:** Der Actor schafft etwa eine Anfrage in 4 Sekunden. Mit dem
  Standard-Zeitlimit brach ein Lauf mit 116 Anfragen nach 25 ab (TIMED-OUT, bezahlt wurde nur das
  Gelieferte); 1.664 Anfragen in einem Lauf hätten rund 2 Stunden gedauert. Zeitlimit hoch setzen
  und ab etwa 300 Anfragen auf mehrere parallele Läufe aufteilen (gleiche Kosten).
- **Agenturen auf OMR:** OMR führt auch Dienstleister-Kategorien. Die Qualifizierung sortiert sie
  aus (Trichter-Prinzip), nicht die Beschaffung.
