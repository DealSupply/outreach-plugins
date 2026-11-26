---
name: weg-e-plattform
description: Weg E des Datenbeschaffungs-Pakets — sellers on Amazon, Etsy and eBay as leads (the merchant behind the listing, never the product). Invoked by the datenbeschaffung master; never triggered directly by the user.
---

# Weg E — Plattform-Verkäufer als Leads

Zielgruppe: Händler, die ihr Geschäft auf einem Marktplatz betreiben — Amazon-Seller,
Etsy-Manufakturen, gewerbliche eBay-Verkäufer. **Ergebnis dieses Wegs ist immer ein Verkäufer mit
Kontaktweg, nie eine Produktliste.** Eine Zeile ohne identifizierbaren Händler ist kein Lead.

Voraussetzungen vom Master: bestätigter ICP-Satz, Zugriffsweg steht (`../datenbeschaffung-referenzen/references/zugriff.md`),
Vorab-Abgleich gelaufen (`check_leads_exist` bzw. `export_leads(format="index")` + `dedup.py`, falls MCP verbunden). Der Lauf beim Anbieter (Apify o. ä.) geschieht im eigenen Konto des Kunden außerhalb von DealSupply; Kosten fallen dort an, kostenpflichtige Läufe nur nach ausdrücklicher Freigabe genau dieses Umfangs. Ohne DealSupply (Modus vom Master) ersetzt die eigene Sperrliste den Vorab-Abgleich, jede Zeile braucht am Ende eine Adresse, und wo hier steht, dass die Recherche die Adresse sucht, schließen `impressum-enrichment` bzw. `kontaktseiten-fallback` die Lücke (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`).

**Belegstand:** Grundlage sind das Kapitel 8 „Weg E: Plattformverkäufer“ des Kurshandbuchs
(Stand 19.08.2026) und die Actor-Recherche vom 19.08.2026 (Plattform-Verkäufer-Sektion in
`../datenbeschaffung-referenzen/references/apify-actors.md`). Eigene Ist-Kosten wie bei Weg C gibt es
im Plugin noch nicht: Die Kostentabelle unten ist der Richtwert des Kurses; vor dem Lauf mit dem
Actor-Preis rechnen, Deckel setzen, die echten Zahlen im Piloten messen und in `kosten.md`
nachtragen — keine Zahlen raten.

Warum ein eigener Weg (Kap. 8): Plattform-Händler haben oft keine eigene Domain, Google-Suche und
Shop-Datenbanken finden sie deshalb nicht, und manches Impressum übernimmt die Plattform. Tools wie
SmartScout liefern Umsatz und Marken, aber keine Kontaktdaten; deshalb ist Apify hier der Weg.

## Schritt 1 — Plattform wählen (eine je Lauf)

| Zielgruppe | Plattform | Was zu erwarten ist |
|---|---|---|
| Handelsmarken, Distributoren, Private-Label-Seller | Amazon | EU-Verkäufer sind über die Händlerangaben identifizierbar; DACH gut abgedeckt, Kontaktdaten teils ab Werk. **EU-Marktplätze vor amazon.com:** Auf amazon.de, .at, .fr, .it und .es gilt die Impressumspflicht, dort stehen E-Mail, Telefon, Adresse und USt-IdNr. im Verkäuferprofil; auf amazon.com fehlen sie oft ganz (Kap. 8) |
| Manufaktur, Handmade, Deko, Papeterie, kleine Marken | Etsy | Shops sind leicht zu finden, **Kontaktdaten nicht ab Werk** — zweistufig |
| Gewerbliche Händler mit Trader-Disclosure (EU/UK) | eBay | Bestes Kontaktschema auf dem Papier, kaum Marktevidenz → **Pilotkandidat** |

## Schritt 2 — Actor-Rollen (IDs ausschließlich aus `apify-actors.md`)

- **Amazon:** Primär ist eine Bulk-Abfrage über eine Verkäufer-Datenbank (Filter: Kategorie,
  Verkäuferland, Erfassungsdatum) mit Kontaktfeldern ab Werk. Das ist eine Datenbank, kein
  Live-Crawl je Lauf — deshalb das Erfassungsdatum als Frischefilter setzen. Fallback ist die
  Live-Discovery über Keyword, Kategorie oder Seller-URL; sie liest die deutschen Händlerangaben
  mit und ist für DACH der interessantere, aber jüngere Weg.
- **Etsy:** Zweistufig. Der Discovery-Actor findet Shops (Keyword, Standort, Verkäufe, Rating,
  Shopalter), liefert aber keine E-Mail. Erst qualifizieren, dann **nur die priorisierten
  Shop-URLs** in den Kontakt-Actor geben — nie die ganze Discovery-Menge anreichern.
- **eBay:** Der funktional beste Actor hat praktisch keine Nutzungshistorie. Er wird nur im
  Pilotmodus eingesetzt (Schritt 3), Fallbacks liefern Seller-URLs ohne Kontakte.

## Schritt 3 — Pilot (Pflicht; bei eBay doppelt)

Maximal ~50 Verkäufer, Deckel ≤ 0,50 $, Kosten vorher nennen.

Kosten laut Kurshandbuch (Kap. 8, Stand 19.08.2026; Abrechnung je Ergebnis, kein Abo):

| Listengröße | Amazon | Etsy | eBay |
|---|---|---|---|
| 100 Seller | ca. 0,40 $ | ca. 0,50 $ | ca. 0,60 $ |
| 500 Seller | ca. 2 $ | ca. 2,50 $ | ca. 3 $ |
| 1.000 Seller | ca. 4 $ | ca. 5 $ | ca. 6 $ |

Dazu kommen die Anreicherung der Händler-Websites (`impressum-enrichment`) und die Prüfung der
Adressen. Ausgewertet wird:

- Anteil mit brauchbarem Kontaktweg (E-Mail oder eigene Shop-Website)
- Anteil im Zielland — Marktplätze mischen Länder gnadenlos
- Anteil echter Händler im Sinne des ICP (kein Wiederverkäufer-Rauschen, keine Dropshipper)
- Dubletten je Firma über mehrere Listings hinweg

**Ab ~70 % ICP-Fit skalieren**, darunter Kategorien/Keywords schärfen und den Piloten wiederholen.

**Qualitäts-Einschätzung je Seller** (aus dem Kurs, Kap. 8): Der Amazon-Skill des alten Kurses gab
jedem Seller einen Quality Score von 0 bis 100 aus drei Merkmalen: **Aktivität** (Verkäufe,
aktuelle Bewertungen), **Reputation** (Plattform-Bewertung) und **Vollständigkeit der Daten**
(E-Mail, Telefon, Adresse, eigene Website). Eine feste Gewichtung ist nicht überliefert. Deshalb die
Seller nach diesen drei Merkmalen ordnen und dem Nutzer die Spitze zuerst zeigen, aber keine
erfundene Punktzahl als harte Schwelle nutzen. Hohe Einschätzung heißt: aktiver Händler mit guten
Daten.

**eBay-Sonderregel:** Vor dem ersten Kunden-Einsatz ein eigener Testlauf mit ~20 deutschen
gewerblichen Verkäufern. Geprüft werden: Sind die E-Mails verifiziert? Wird je Firma dedupliziert?
Kommen USt-Id/Handelsregister mit? Stimmt das Verkäuferland? Treffen die Keywords wirklich Händler?
Fällt der Actor durch, liefert der Fallback nur Seller-/Shop-URLs — die Kontakte holt dann
`impressum-enrichment` (DACH-Shops mit eigener Website) bzw. `kontaktseiten-fallback`. Das Ergebnis
des Pilotlaufs mit Datum in `apify-actors.md` nachtragen.

## Schritt 4 — Skalierung

Eine Plattform, ein Land, Kategorie für Kategorie. Bei Datenbank-Actors zusätzlich das
Erfassungsdatum eingrenzen, sonst wandern Karteileichen in die Liste. Deckel: kalkulierte Kosten
+ 50 %.

## Schritt 5 — Roh-CSV bauen

```
python3 ../datenbeschaffung-referenzen/scripts/build_csv.py --in seller.json \
  --quelle "apify:<actor-id> <datum>" --land <de|at|ch> --out leads-<nische>-<plattform>-<datum>.csv
```

Zusatzspalten mitführen, sie tragen später die Personalisierung: `plattform`, `seller_url`,
`bewertung` und `bewertungen_anzahl` (die Bewertung auf der Plattform, nie unter dem Namen
`rating`, der Google vorbehalten ist), `verkaeufe`. `kategorie` bekommt die Plattform-Kategorie.
Die Plattform selbst liest diese Seiten nicht; ohne Import fehlen sie der Mail
(`../datenbeschaffung-referenzen/references/datenumfang.md`). Eine Seller-ID oder USt-Id nur zum
Deduplizieren nutzen, nicht hochladen.
Deduplizierung: `build_csv.py` dedupliziert auf E-Mail, ohne E-Mail auf die Website; liefert der
Actor eine Seller-ID oder einen Firmennamen, zusätzlich darauf prüfen: derselbe Händler taucht
über mehrere Listings auf. Als `website` zählt nur die eigene Händler-Domain: Seller- und
Shop-Seiten auf dem Marktplatz (amazon.de, etsy.com, ebay.de) sind Profil-Links, sie gehören in
`seller_url`, nie in `website`.

**Personalisierungs-Hebel:** Plattform-Bewertung, Verkäufe und Kategorie aus den Spalten oben
(`../datenbeschaffung-referenzen/references/personalisierung.md`).

## Schritt 6 — Die Kontakt-Lücke

Etsy und die eBay-Fallbacks liefern oft nur Shop-URLs. Dann `impressum-enrichment` (deutsche Shops
mit eigener Website) oder `kontaktseiten-fallback` (internationale Domains) über die **eigenen
Domains der Händler** laufen lassen; mit DealSupply ab MCP 4.0.0 optional, dann sucht die
Recherche die Adresse auf der Händler-Domain (Entscheidung nach `datenumfang.md`, „Die
Kontaktlücke“); ohne DealSupply Pflicht. Händler ohne eigene Domain und ohne Adresse sind nicht
importierbar.

**Die eigene Website finden** (Kap. 8): Viele erfolgreiche Plattform-Händler haben neben dem Shop
auf dem Marktplatz eine eigene Website. Zwei Wege, die billigste zuerst:

1. **Social-Links im Shop-Profil** (Etsy liefert sie über ShopHound mit): Instagram oder Facebook
   führen oft zur Website. Kostet nichts extra.
2. **Google-Suche nach dem Seller-Namen** mit `website_suche.py` (JSON-Liste, Firmenname in
   `company`, Ort in `city`, wenn bekannt; für Händler außerhalb Deutschlands `--land FR --sprache
   fr` usw.): eine Suchseite je Händler, Kosten wie dort genannt. Übernommen wird nur eine Domain,
   die zum Namen passt und kein Portal ist.

Sobald die Website steht, greift der normale Weg über das Impressum. Die Marktplatz-Domains selbst (amazon.de, etsy.com, ebay.de)
werden **nie** angereichert — sie gehören in die `domainBlacklist` aus `noise-domains.md`, sonst
werden sie voll berechnet.

## Schritt 7 — Übergabe

An `listen-qualitaet` — immer, ohne Ausnahme.

## Bekannte Fallen

- **Produkte statt Verkäufer** in der Ausgabe: Keyword-Discovery liefert oft Listings. Vor dem
  CSV-Bau auf Verkäuferebene zusammenfassen.
- **Plattform-Support-Adressen** und generische Marktplatz-Kontakte sind keine Leads, auch wenn der
  Actor sie ausgibt.
- **Ein-Entwickler-Actors ohne Rating** dominieren diese Kategorie — nie ohne benannten Fallback
  starten, nie ohne Pilot beim Kunden einsetzen.
- **Datenbank statt Live-Daten:** Der Amazon-Primärweg kann Datensätze zeigen, die den Shop längst
  nicht mehr abbilden. Erfassungsdatum begrenzen und im Sample gegenprüfen.
