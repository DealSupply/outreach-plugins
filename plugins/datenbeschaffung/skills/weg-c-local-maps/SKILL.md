---
name: weg-c-local-maps
description: Weg C des Datenbeschaffungs-Pakets — lokale Betriebe (Handwerk, Praxen, Gastro, Dienstleister mit Google-Maps-Eintrag) über Google-Maps-Scraping beim Anbieter (manueller Weg über Apify, CSV, Import) mit eingebauter Kontaktanreicherung. Wird vom Datenbeschaffungs-Master geladen, nie direkt vom Nutzer ausgelöst.
---

# Weg C — Local Business über Google Maps

Der Standardweg für die meisten DACH-Zielgruppen. Belegt (19.08.2026, SHK Köln): 440 Places in
10 Minuten, **77 % mit E-Mail direkt aus dem Scrape** — einstufig für die große Mehrheit,
Impressum nur noch als Lückenfüller. Der zweite Vorteil dieses Wegs: **Google-Bewertung und
Rezensionen kommen gleich mit** und sind der Einstieg, den die Plattform selbst nicht abrufen kann
(`../datenbeschaffung-referenzen/references/datenumfang.md`).
Der Lauf geschieht im eigenen Apify-Konto des Kunden, das Ergebnis geht als CSV über
`listen-qualitaet` nach ListM8 (Oberfläche oder MCP `import_leads`).

Voraussetzungen vom Master: bestätigter ICP-Satz, Zugriffsweg steht (`../datenbeschaffung-referenzen/references/zugriff.md`),
Vorab-Abgleich gelaufen (`check_leads_exist` bzw. `export_leads(format="index")` + `dedup.py`, falls MCP verbunden). Der Lauf beim Anbieter (Apify o. ä.) geschieht im eigenen Konto des Kunden außerhalb von ListM8; Kosten fallen dort an, kostenpflichtige Läufe nur nach ausdrücklicher Freigabe genau dieses Umfangs.

## Schritt 1 — Kategorien statt Freitext

**Nie Freitext-Queries.** Google Maps arbeitet mit Kategorien — Freitext liefert überwiegend
Beifang. Englische Kategorienamen treffen oft, aber nicht immer; das deutsche Branchenwort ist der
Gegentest, `categoryFilterWords` die strenge Variante. 3–5 verwandte Kategorien je Lauf, nicht 20
(belegte Treffer: `erfahrungswerte.md`):

| Zielgruppe | Kategorien (searchStringsArray) |
|---|---|
| SHK / Sanitär / Heizung | `plumber`, `heating contractor`, `hvac contractor` |
| Elektro | `electrician`, `electrical installation service` |
| Dachdecker | `Dachdecker` (deutsch: 57 % Treffer statt 12 % mit `roofing contractor`) oder `roofing contractor` mit `categoryFilterWords` |
| Bau allgemein | `general contractor` |
| Agenturen | `marketing agency`, `advertising agency`, `website designer` (~90 % passend) |
| Maschinenbau / Industrie | `Maschinenbau` mit Bundesland als Ort (~85 % passend, 95 % mit E-Mail) |
| Zahnärzte / Praxen | `dentist`, `dental clinic` (Vorsicht: `doctor` ist zu breit) |
| Gastro | `restaurant` gezielt mit Küche/Stadtteil eingrenzen — sonst Massen-Beifang |
| Kfz | `auto repair shop`, `car dealer` |

Unbekannte Zielgruppe: die Kategorie eines bekannten Ziel-Betriebs auf Google Maps nachschlagen
(dort steht sie unter dem Namen) — nicht raten. Jede Kategorie ist ein eigener Suchbegriff und
kostet entsprechend; die Liste nicht mit Synonymen aufblähen.

## Schritt 2 — Pilot (Pflicht)

Actor: **Primär aus `../datenbeschaffung-referenzen/references/apify-actors.md`** (Maps-Kategorie). Standard-Input:

```json
{
  "searchStringsArray": ["<kategorie-1>", "<kategorie-2>"],
  "locationQuery": "<Pilotstadt>, <Land>",
  "maxCrawledPlacesPerSearch": 30,
  "language": "de",
  "website": "withWebsite",
  "skipClosedPlaces": true,
  "scrapeContacts": true,
  "maxReviews": 10,
  "reviewsSort": "newest",
  "reviewsOrigin": "google",
  "reviewsStartDate": "18 months",
  "scrapeReviewsPersonalData": false
}
```

Was die Felder bringen:

- `scrapeContacts`: E-Mail, Telefon und Social-Links von der Website, dazu das Impressum mit
  Inhaber bzw. Geschäftsführer. Den Inhaber übernimmt `build_csv.py`; einen eigenen
  Entscheider-Lauf braucht es nicht.
- `maxReviews: 10` mit `newest`: Etwa ein Drittel der Rezensionen hat keinen Text, zehn ergeben
  meist die fünf Texte, die der Import nutzt. Bewertung und Anzahl kommen auch ohne diese Option
  und kosten nichts extra; die Rezensions-Stichworte nur mit Rezensionen.
- `reviewsStartDate: "18 months"`: Ältere Rezensionen nutzt die Plattform nicht als Einstieg. Mit
  der Grenze kamen im Test weniger als halb so viele Rezensionen je Place (3,3 statt 7,7); bezahlt
  wird nur, was als Einstieg zählt.
- `scrapeReviewsPersonalData: false`: keine Namen und Profile der Verfasser. Sie dürfen nicht in die
  Liste und werden auch nicht gebraucht.
- Nicht einschalten: die Zusätze für Business-Leads (Entscheider), E-Mail-Verifizierung, Social-
  Profile, Bilder. Begründung und Preise in `datenumfang.md`.

Kosten (Testläufe 11.10.2026, Stufe GOLD): ohne Rezensionen 0,0036 $ je Place, mit Rezensionen
0,0054 bis 0,0067 $ (mit 18-Monats-Grenze am unteren Ende). Im kostenlosen Apify-Plan etwa das Doppelte (rund 0,013 $ je Place). Ein
Pilot mit 30 Places kostet also 0,11 bis 0,39 $. Deckel 0,50 $ (Mindestdeckel dieses Actors, kleinere lehnt Apify ab);
die Menge begrenzt `maxCrawledPlacesPerSearch`. Kosten vorher nennen (`kosten.md`).

Rezensionen nur weglassen, wenn der Nutzer es ausdrücklich will oder ein Massenlauf über
`outscraper-bulk` geplant ist. Dann im Bericht sagen, dass die Recherche Bewertungen selbst
suchen muss (eine Websuche mehr je Lead, häufiger ein neutraler Ersatz-Einstieg).
Auswertung: `categoryName` gegen den ICP halten — **ab ~70 % Fit skalieren**, darunter Kategorien
schärfen und Pilot wiederholen. Nicht jede englische Kategorie trifft: `roofing contractor` lieferte
in Freiburg 12 % Dachdecker und sonst Bau, Boden und Garten; das deutsche Suchwort `Dachdecker`
57 %, mit `categoryFilterWords: ["roofing contractor"]` 86 % (Filter kostet je Place extra und
liefert weniger Treffer). Bei schwachem Fit zuerst das deutsche Suchwort probieren
(`erfahrungswerte.md`, Testreihe vom 11.10.2026). Beifang-Kategorien (Baumärkte, Handel, Ketten) notieren: sie werden
in Schritt 4 herausgefiltert und wandern in den Anti-ICP.

Hinweis zum `website`-Filter: `withWebsite` ist für Cold Mail fast immer richtig (ohne Website kein
Personalisierungs-Anker). Ausnahme nur, wenn der ICP gerade Betriebe OHNE Website sucht
(z. B. Webdesign-Angebote) — dann `allPlaces` und die Lücke ist das Verkaufsargument.

## Schritt 3 — Skalierung

Gleicher Input, `maxCrawledPlacesPerSearch` hoch (250–500 je Kategorie), `locationQuery` kann
direkt Bundesland oder Land sein (der Actor teilt intern — keine Stadt-Schleife nötig, siehe
`staedte.md`). Ein Land pro Lauf. Deckel: kalkulierte Kosten + 50 %.
Laufzeit: mehrere Minuten je 100 Places — alle 2–4 Minuten pollen.

## Schritt 4 — Roh-CSV bauen

```
python3 ../datenbeschaffung-referenzen/scripts/build_csv.py --in maps.json \
  --quelle "apify:<actor-id> <datum>" --land <de|at|ch> --out leads-<nische>-<region>-<datum>.csv
```

Danach ICP-Fremde Kategorien aussortieren (die notierten Beifang-Kategorien) — mechanisch nach
`kategorie`-Spalte, nicht Lead für Lead.

Das Skript schreibt neben den Kernspalten `rating`, `reviews_count`, `place_id`, `reviews_tags`,
`google_rezensionstexte` sowie `inhaber`/`inhaber_rolle` und berichtet, wie viele Leads Bewertung,
Rezensionstext und Inhaber haben. Fehlt der Rezensionstext bei mehr als der Hälfte, war
`maxReviews` aus oder die Zielgruppe hat kaum Rezensionen: im Bericht nennen, nicht nachkaufen.
Bei mehreren Adressen wählt es die persönliche vor info@ und nie bewerbung@ o. Ä., solange es eine
andere gibt; fehlt die Adresse im Scrape, nimmt es die aus dem Impressum.

## Schritt 5 — Die Kontaktlücke (die Leads ohne E-Mail)

Ab ListM8 MCP 3.0.0 dürfen Leads mit eigener Website ohne Adresse importiert werden; die Recherche
sucht die Adresse dann selbst (Impressum, Kontaktseite). Nach Maps ist die Lücke aber meist echt:
Im Test fanden Impressum- und Kontakt-Actors für 28 Domains ohne Adresse nur 1 bis 5
(`erfahrungswerte.md`). Dem Nutzer die Zahl nennen und fragen: importieren (kostet Qualifizierung
und Recherche je Lead, der Lead scheidet ohne Fund aus) oder abspalten. Einen zusätzlichen
`impressum-enrichment`-Lauf nur bei großem Volumen anbieten, nur für die Adresse und mit dem
günstigsten passenden Actor (Entscheidungstabelle: `datenumfang.md`, „Die Kontaktlücke“).
Leads mit `keine-website` oder nur einem Profil-Link (Facebook, Instagram, Portal) kann niemand
recherchieren: ohne Adresse fallen sie bei der Übergabe heraus. Auf älteren Servern braucht der
Import eine Adresse je Lead (info@ reicht). Keine Entscheider-, Register- oder
Mobilnummern-Daten dazukaufen: Den Ansprechpartner und seine persönliche Adresse sucht die
Recherche der Plattform.

## Schritt 6 — Übergabe

An `listen-qualitaet` — immer, ohne Ausnahme: Qualitätsstufe, Verifizierung und Import (Oberfläche
oder `import_leads`, optional mit `create_list`/`list_id`). Diesem Skill gehört kein Qualitäts-Urteil
und keine Übergabe.

## Bekannte Fallen

- Duplikate über Kategorien hinweg dedupliziert der Actor per placeId selbst; über LÄUFE hinweg
  fängt es `dedup.py` (Bestand-Index) — deshalb Vorab-Abgleich nicht überspringen.
- Ballungsräume doppeln Betriebe mit mehreren Standorten: gleiche E-Mail = ein Lead, ohne E-Mail
  gleiche Website = ein Lead (macht build_csv.py automatisch, der Import ebenso; 440 Places →
  ~308 eindeutige E-Mail-Leads ist normal).
- Große Flächen (Bundesland, Land) lassen sich beim Anbieter in einem Lauf angeben, werden aber teuer
  und lang: erst Pilot, dann in Abschnitten (z. B. je Bundesland) fahren, jeweils mit eigenem
  Deckel und Freigabe.
- Jeder zusätzliche Filter kostet je Place extra — nur nutzen, was der ICP wirklich braucht.
- Rezensionen älter als 18 Monate sind für die Plattform kein aktueller Einstieg; `newest` holt
  deshalb die neuesten zuerst. Betriebe mit wenigen Rezensionen bringen wenig Text, das ist normal.
- Der E-Mail-Anteil schwankt stark je Branche und Stadt (Köln SHK 77 %, Stuttgart Elektro 47 % im
  Test vom 11.10.2026). Im Pilot messen und die Kosten der Lücke danach planen.
