---
name: weg-b-ecom-google
description: Weg B des Datenbeschaffungs-Pakets — independent D2C online shops (Mode, Supplements, Beauty, Food, Tierbedarf, CBD …) via Google SERP scraping, filtered against marketplaces, chains and comparison portals. Invoked by the datenbeschaffung master; never triggered directly by the user.
---

# Weg B — E-Commerce über Google

Sucht **einzelne Shops mit eigener Marke** — keine Marktplätze, keine Ketten, keine
Vergleichsportale. Der Filter ist hier die eigentliche Arbeit: die Nischen-Queries treffen
zuverlässig, aber die ersten Seiten gehören strukturell Amazon, Otto und Idealo.

Voraussetzungen vom Master: bestätigter ICP-Satz, Zugriffsweg steht (`../datenbeschaffung-referenzen/references/zugriff.md`),
Vorab-Abgleich gelaufen (`check_leads_exist` bzw. `export_leads(format="index")` + `dedup.py`, falls MCP verbunden). Der Lauf beim Anbieter (Apify o. ä.) geschieht im eigenen Konto des Kunden außerhalb von DealSupply; Kosten fallen dort an, kostenpflichtige Läufe nur nach ausdrücklicher Freigabe genau dieses Umfangs. Ohne DealSupply (Modus vom Master) ersetzt die eigene Sperrliste den Vorab-Abgleich, jede Zeile braucht am Ende eine Adresse, und wo hier steht, dass die Recherche die Adresse sucht, schließen `impressum-enrichment` bzw. `kontaktseiten-fallback` die Lücke (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`).

Will der Nutzer nach Shop-Technologie, Umsatzklasse oder Traffic filtern statt nach Nische:
`weg-b-storeleads` erwähnen — das ist Beratung ohne Scrape. Sonst hier weiter.

## Schritt 1 — Query-Strategie je Nische

Maximal drei Varianten je Nische. Ort ist optional: Shops verkaufen überregional, die Stadt
schneidet eher nützliche Treffer weg. Ohne Stadt arbeiten und stattdessen mehr Nischen-Varianten
fahren — Städte nur, wenn der ICP ausdrücklich regional ist.

| Nische | Query-Varianten (für `--keywords`) |
|---|---|
| Mode / D2C-Fashion | Mode Online Shop, Fashion Brand Shop, nachhaltige Mode Online Shop |
| Supplements | Nahrungsergänzung Online Shop, Supplements Shop, Proteinpulver online kaufen |
| Beauty & Kosmetik | Naturkosmetik Online Shop, Beauty Shop online, Skincare Shop |
| Food & Getränke | Kaffee Online Shop, Tee Online Shop, Feinkost Online Shop |
| Tierbedarf | Tierbedarf Online Shop, Hundezubehör Online-Shop, Tiernahrung online bestellen |
| Einrichtung | Möbel Online Shop, Deko Online-Shop, Interior Shop |
| Sport | Sport Online Shop, Fitness Shop, Outdoor Shop online |
| Schmuck | Schmuck Online Shop, Handmade Schmuck Shop, Uhren Online-Shop |
| CBD | CBD Online Shop, CBD Öl kaufen, Hanf Shop |

Weitere Nischen (Richtung der über 25 Nischen aus dem Kurshandbuch, Kap. 5) nach demselben
Muster bauen: `<Produktwort> Online Shop`, `<Produktwort> online kaufen`, `<Produktwort> Shop`.
Die Tabelle oben ist erprobt, die folgenden Varianten sind es noch nicht: im Piloten messen und das
Ergebnis in `erfahrungswerte.md` eintragen.

| Nische (ungeprüft) | Query-Varianten |
|---|---|
| Baby und Kind | Babyausstattung Online Shop, Kindermode Online Shop, Spielzeug Online Shop |
| Wein und Spirituosen | Wein Online Shop, Gin online kaufen, Spirituosen Shop |
| Fahrrad | Fahrrad Online Shop, E-Bike Zubehör Shop, Fahrradteile online kaufen |
| Garten | Gartenbedarf Online Shop, Pflanzen online kaufen, Gartenmöbel Shop |
| Papeterie und Geschenke | Papeterie Online Shop, Geschenkideen Shop, Notizbuch online kaufen |
| Brillen und Accessoires | Brillen Online Shop, Sonnenbrillen Shop, Taschen Online Shop |
| Bademode und Wäsche | Bademode Online Shop, Unterwäsche Online Shop, Dessous Shop |
| Haushalt und Küche | Küchenzubehör Online Shop, Messer online kaufen, Haushaltswaren Shop |
| Gesundheit und Pflege | Bio Pflege Online Shop, Zahnpflege Shop, Aromatherapie Shop |
| Bio-Lebensmittel | Bio Lebensmittel Online Shop, Müsli online kaufen, Gewürze Online Shop |
| Musik und Hobby | Musikinstrumente Online Shop, Bastelbedarf Shop, Modellbau Online Shop |
| Nachhaltige Produkte | Zero Waste Shop, nachhaltige Produkte online kaufen, plastikfrei Shop |
| Auto und Motorrad | Autozubehör Online Shop, Motorradbekleidung Shop, Autopflege online kaufen |
| Tierbedarf Pferd | Reitsport Online Shop, Pferdezubehör Shop, Pferdefutter online kaufen |
| Schuhe | Schuhe Online Shop, Sneaker Shop, nachhaltige Schuhe online kaufen |
| Mode für Männer | Herrenmode Online Shop, Bartpflege Shop, Männer Accessoires Shop |

Shopify-Fokus gewünscht: `site:myshopify.com <nische>` als vierte Query — trifft nur Shops auf
Shopify-Subdomain, also klein und jung, aber sehr sauber.

```
python3 ../datenbeschaffung-referenzen/scripts/build_queries.py --keywords "Naturkosmetik Online Shop,Beauty Shop online,Skincare Shop" \
  --cities "" --exclude 8
```

Für E-Commerce die Kern-Ausschlüsse gegen die Marktplätze tauschen (`amazon.de`, `otto.de`,
`zalando.de`, `idealo.de`) — Begründung und Obergrenze in `../datenbeschaffung-referenzen/references/erfahrungswerte.md`.

## Schritt 2 — Pilot (Pflicht)

Die Alt-Vorlage dieses Wegs ließ den Piloten bewusst weg („sofort loslegen"). Das war ein Fehler:
gerade hier entscheidet der Filter über die Ausbeute, und ohne Piloten merkt man erst nach dem
skalierten Lauf, dass 60 % Portal-Unterseiten in der Liste stehen.

Also: eine Nische, alle Query-Varianten, EIN Lauf, 4 Seiten je Query (`erfahrungswerte.md`).
Actor: **Primär aus `../datenbeschaffung-referenzen/references/apify-actors.md`** (SERP-Kategorie). Kosten vorab nennen
(`kosten.md`), Deckel ≤ 0,50 $.

```
python3 ../datenbeschaffung-referenzen/scripts/process_serp.py --in serp-pilot.json --out shops-pilot.csv --report
```

**Ab ~70 % Shop-Fit skalieren**, darunter Queries schärfen. Der `--report` zeigt, welche Portale
durchgerutscht sind — die gehören in `noise-domains.md`, bevor skaliert wird. Genau daran wächst
die Ausbeute dieses Wegs von Lauf zu Lauf.

## Schritt 3 — Shop-Prüfliste für die Pilot-Stichprobe

Domain-Filter und Muster für geschlossene Shops laufen mechanisch in `process_serp.py`. Diese
Liste ist für die 10–15 Treffer, die man im Piloten selbst anschaut — sie bestimmt, was in den
Anti-ICP und in `noise-domains.md` wandert:

- **Geschlossen oder unfertig:** „Onlineshop entsteht", „Online-Pause", „Coming soon",
  „Wartungsarbeiten", passwortgeschützter Shop. Kein Lead — der Betreiber ist raus.
- **Fitnessstudio-Muster:** „Mitgliedschaft ab X €/Monat", „Probetraining", „kostenlos starten".
  Das ist ein Studio mit Shop-Anmutung, kein E-Commerce.
- **B2B-only / Private Label:** „nur für Fachhändler", „Großhandel für", „Private Label".
  Verkauft nicht an Endkunden — anderer ICP, meist Anti-ICP.
- **Portal-Unterseite statt Shop:** tiefe Kategorieseite eines großen Händlers oder Marktplatzes.
  Die Root-Domain entscheidet, nicht die Unterseite.
- **Kein eigener Verkauf:** Blog, Coupon- und Testseite, Dropshipping-Verzeichnis,
  Agentur, Vergleichsportal.
- **Dropshipping- und Print-on-Demand-Shop:** Fremdware ohne eigene Marke oder bedruckte
  Standardware über einen Druckdienst. Diese Shops haben meistens kein Budget für zusätzliche
  Dienstleistungen (Kurshandbuch Kap. 5): Anti-ICP, außer der Nutzer zielt genau auf sie.
- **Kette statt Marke:** Filialist oder Konzern-Shop — kein Ansprechpartner mit Entscheidungsmacht.

Drin bleibt: eigener Shop mit Warenkorb, eigene Marke, eigenständige Domain, Verkauf an Endkunden.

**Shop-Signale** (aus dem Shop-Score des alten Kurs-Skills, Kap. 5): Woran man einen echten,
aktiven Shop erkennt, wenn man ihn öffnet: ein Warenkorb, Hinweise wie „versandkostenfrei ab“,
Preise in Euro. Fehlen alle drei, ist es eher ein Blog, ein Ladengeschäft mit Website oder ein
Shop im Aufbau. Dazu die Plattform notieren, wenn sie erkennbar ist (Shopify, WooCommerce,
Shopware, Magento): Sie ist ein Personalisierungs-Hebel und erlaubt später Segmente. Eine feste
Punktzahl gibt es dafür nicht; die Signale entscheiden in der Stichprobe, nicht als harter Filter.

## Schritt 4 — Skalierung

Weitere Nischen-Varianten und, falls regional gewollt, die Städte aus `staedte.md`. Ein Land je
Lauf (der Länder-Code gilt pro Lauf); DE/AT/CH getrennt, gern parallel. Shops außerhalb DACH:
Suchbegriffe in der Landessprache und Ländercode des Ziellands (`ausserhalb-dach.md`). Alle
Datasets danach zusammenführen und einmal durch `process_serp.py` — der Dedup auf Root-Domain
wirkt so über alle Queries hinweg. Deckel: kalkulierte Kosten + 50 %.

**Kosten** laut Kurshandbuch (Kap. 5, Stand 19.08.2026): eine typische Nischen-Suche rund 0,02 $,
eine komplette DACH-Suche rund 1,60 $, **500 Shops mit Impressum-Daten insgesamt rund 4 bis 5 $**.
Im Kurs fand eine Nische zwischen 200 und über 2.600 eigenständige Shops. Für die Freigabe mit
`kosten.md` und dem Actor-Preis rechnen.

## Schritt 5 — Kontaktdaten holen (mit DealSupply optional, ohne Pflicht)

Die Shop-Domains an `impressum-enrichment` geben (Actor, Betriebsregeln und Kosten stehen dort).
Shops sind impressumspflichtig und liefern hier überdurchschnittlich gut (Kurs: 80 bis 90 % mit
E-Mail, 70 bis 80 % mit Geschäftsführer). `.com`-Marken ohne deutsches Impressum gehen in den
`kontaktseiten-fallback`. Mit DealSupply ist das ab MCP 4.0.0 optional (Entscheidung nach
`datenumfang.md`, „Die Kontaktlücke“): Ohne Anreicherung die Domain-CSV direkt in `build_csv.py`
geben (`--in domains.csv`), dann sucht die Recherche die Adresse. Ohne DealSupply ist dieser
Schritt Pflicht, denn die Google-Suche liefert keine einzige Adresse.

**Personalisierungs-Hebel** (Kap. 5): Sortiment, Plattform, fehlende Technologie, eine
Kundenbewertung zitieren, Saisonalität. Dieser Weg liefert davon nur die Nische (`kategorie`) und,
aus der Stichprobe, die Plattform; den Rest notiert der Nutzer beim Ansehen der Shops
(`../datenbeschaffung-referenzen/references/personalisierung.md`).

## Schritt 6 — Roh-CSV bauen

```
python3 ../datenbeschaffung-referenzen/scripts/build_csv.py --in impressum.json \
  --quelle "apify:<serp-actor>+impressum <datum>" --land <de|at|ch> \
  --out leads-<nische>-<region>-<datum>.csv
```

## Schritt 7 — Übergabe

An `listen-qualitaet` — immer, ohne Ausnahme. Diesem Skill gehört kein Qualitäts-Urteil und
keine Übergabe.

## Bekannte Fallen

- **Ort in der Query kostet Ausbeute.** Shops ranken überregional; „Kaffee Online Shop Köln"
  liefert Cafés und Röstereien mit Ladengeschäft statt Versandhändler.
- **Marktplatz-Ausschlüsse gehören in die Query, alles andere in den Filter** — die 8–10er-Grenze
  gilt auch hier, sonst kommt der Lauf leer zurück.
- **Ketten kommen über Unterseiten wieder rein.** Wenn `process_serp.py` eine Filialisten-Domain
  durchlässt, ist meist die Root-Domain neu — einmal in `noise-domains.md` eintragen und der
  ganze Filialist ist für alle künftigen Läufe erledigt.
- **Die Nischenzuordnung aus dem Google-Titel ist unzuverlässig** (Mönchspfeffer ist kein Wein,
  Mikronährstoffe kein DIY). Die `kategorie`-Spalte hier nicht zum harten Filtern nutzen —
  die Qualifizierung entscheidet.
