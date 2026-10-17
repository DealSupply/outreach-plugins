# Erfahrungswerte — belegte Trefferquoten und Query-Effekte

> Alles hier ist gemessen, nicht geschätzt. Neue Läufe ergänzen Zeilen mit Datum; Werte ohne
> Quelle gehören nicht in diese Datei. Die Wege verweisen hierher, statt Zahlen zu wiederholen.
>
> Lesart „Trefferquote": Anteil der SERP-Domains, die nach dem Filtern (`process_serp.py`)
> wirklich zum ICP passen. Die Pilot-Schwelle des Pakets (~70 %) gilt gegen genau diese Zahl.

## Query-Varianten mit belegter Trefferquote

| Nische | Query-Muster | Trefferquote | Quelle |
|---|---|---|---|
| Ernährungs-/Health-Coaching | `Ernährungscoach <Stadt>` | ~42 % | Kurs-Testläufe, übernommen 19.08.2026 |
| Ernährungs-/Health-Coaching | `Ernährungsberatung <Stadt>` | ~36 % — zieht massiv Arztpraxen und Kliniken | Kurs-Testläufe, übernommen 19.08.2026 |
| Ernährungs-/Health-Coaching | `Health Coach <Stadt>` | ~30 % — Corporate Health und Ausbildungsanbieter | Kurs-Testläufe, übernommen 19.08.2026 |
| Ernährungs-/Health-Coaching | Nische gesamt nach Filterung | 60–70 % ist hier ein gutes Ergebnis, unter 50 % nachschärfen | Kurs-Testläufe, übernommen 19.08.2026 |
| Spirituelles Coaching | `Spiritueller Coach <Stadt>` | bester Anteil einzelner Coaches der drei Varianten | Kurs-Testläufe, übernommen 19.08.2026 |
| Spirituelles Coaching | `Spirituelles Coaching <Stadt>` | schwächer — zieht Coaching-Ausbildungen | Kurs-Testläufe, übernommen 19.08.2026 |
| Spirituelles Coaching | `Bewusstseinscoach <Stadt>` | eigenes Publikum, mehr Netzwerk-Noise | Kurs-Testläufe, übernommen 19.08.2026 |
| Spirituelles Coaching | Nische gesamt nach Filterung | ~60–70 % | Kurs-Testläufe, übernommen 19.08.2026 |
| Vertriebscoaching | `Vertriebscoach` / `Vertriebstrainer <Stadt>` schlägt `Vertriebscoaching` / `Sales Coaching` deutlich | letztere liefern AVGS-, Karriere- und Sprechcoaching statt Vertrieb | Kurs-Testläufe, übernommen 19.08.2026 |
| SERP allgemein | 60 Treffer (scraperlink) | 40 eindeutige Firmen-Domains, keine Dubletten | Lauf 19.08.2026 |
| Google Maps | SHK Köln, `scrapeContacts` | 440 Places, 77 % mit E-Mail direkt aus dem Scrape | Lauf 19.08.2026 |

## Google Maps: Testreihe vom 11.10.2026

Alle Läufe mit `withWebsite`, `skipClosedPlaces`, `scrapeContacts`; „mit E-Mail“ nach
`build_csv.py` (Impressum-Adresse der eigenen Domain eingerechnet, Portale entfernt).

| Suche | Places | passt zur Zielgruppe | mit E-Mail | mit Rezensionstext < 18 Mon. | Inhaber aus Impressum | Kosten je Place |
|---|---|---|---|---|---|---|
| `electrician`, Stuttgart | 15 | 100 % | 53 % | 53 % | 47 % | 0,0061 $ |
| `plumber` + `heating contractor`, Karlsruhe | 50 | ~95 % | 90 % | 66 % | 53 % | 0,0067 $ |
| `marketing agency` + `advertising agency` + `website designer`, Stuttgart | 60 | ~90 % | 80 % | 47 % | 40 % | 0,0062 $ |
| `roofing contractor`, Freiburg | 50 | **12 %** (Bau, Boden, Garten) | 75 % | 58 % | 31 % | 0,0055 $ |
| `Dachdecker`, Freiburg | 30 | 57 % (+17 % Zimmerer) | 93 % | 57 % | – | 0,0054 $ |
| `roofing contractor` + `categoryFilterWords`, Freiburg | 14 | 86 % | 83 % | – | – | 0,0059 $ |
| `Maschinenbau`, Baden-Württemberg (ohne Rezensionen) | 40 | ~85 % | 95 % | – | 56 % | 0,0036 $ |

Lehren:
1. **Kategorie im Pilot prüfen, nicht der Übersetzung trauen.** Englische Kategorien treffen bei
   SHK und Elektro, bei `roofing contractor` kamen fast nur Fremdgewerke. Das deutsche Suchwort oder
   `categoryFilterWords` (kostet einen Filter je Place, liefert weniger, aber passende Treffer) lösen es.
2. **E-Mail-Quote schwankt mit Branche und Stadt** (53 bis 95 %); im Pilot messen.
3. **Industrie ist auf Maps gut vertreten:** Maschinenbau in Baden-Württemberg lieferte 95 % mit
   Adresse, günstiger als jede B2B-Datenbank (siehe unten).
4. **1 bis 3 von 50 Einträgen haben ein Branchenportal als Website**; `build_csv.py` erkennt sie
   über `noise-domains.md` und verwirft deren Adressen.

## B2B-Quellen im Vergleich (Maschinenbau Baden-Württemberg, 11.10.2026)

| Quelle | passt | mit Adresse | zustellbar (Verifier) | Kosten |
|---|---|---|---|---|
| Google Maps `Maschinenbau` | ~85 % | 95 % | (Maps-Adressen allgemein: 60 % gut, 33 % unsicher, 7 % schlecht) | 0,0036 $/Place |
| LinkedIn-Firmensuche + Impressum (haketa) | 95 % | 73 % | nicht gemessen | 0,003 + 0,0017 $ |
| `peakydev/leads-scraper-ppe` (Personen) | 78 % (Branche „Mechanical or Industrial Engineering“ liefert Bauingenieure) | 100 % | **37 % gut, 40 % unsicher, 23 % schlecht** | 0,0012 $/Lead, mind. 100 Leads + 0,10 $ Start |

Bei `peakydev` waren 51 von 100 Adressen nur aus dem Namensmuster geraten (`emailPatternGuess`):
davon 6 gut und 23 schlecht. Die übrigen 49: 31 gut, 0 schlecht. 8 Adressen hatten Umlaute vor dem @.

## E-Mail-Lücke nach Maps (11.10.2026)

28 Domains, für die Maps (mit Impressum-Auswertung) keine Adresse fand:

| Actor | gefunden | Kosten |
|---|---|---|
| `winningsolutions/german-imprint-scraper` | 5/28 | 0,12 $ |
| `haketa/impressum-legal-notice-extractor` | 4/28 | 0,04 $ |
| `vdrmota/contact-info-scraper` (5 Seiten je Domain) | 1/28 | 0,07 $ |

Lehre: Nach Maps ist die Lücke meist echt (keine Adresse auf der Website). Ein zweiter Lauf
lohnt nur bei großem Volumen. Auf Quellen ohne Kontaktdaten (LinkedIn-Firmen) brachte derselbe
haketa-Lauf dagegen 29/40 (73 %).

## Fundquote der ListM8-Recherche bei Leads ohne Adresse (ab MCP 3.0.0)

Noch nicht gemessen. Nach den ersten Läufen hier je Quelle eintragen: Leads ohne E-Mail
importiert, davon mit gefundener Adresse (`contactEmailState: present`), ausgeschieden
(`not_found`, im Lauf `skipReasons.no_contact_email`), Recherche-Stufe. Die Entscheidung
„vorab anreichern oder der Recherche überlassen“ (`datenumfang.md`) hängt an dieser Zahl.

| Quelle | Leads ohne E-Mail | Adresse gefunden | ausgeschieden | Stufe | Datum |
|---|---|---|---|---|---|

## Coaches (11.10.2026)

| Quelle | Ergebnis |
|---|---|
| LinkedIn-Personensuche (Short), Vertriebs- und Business-Coaches BW | 50 Profile, ~68 % selbstständig, 32 % angestellt (z. B. Bank); ohne Website und E-Mail |
| Instagram-Hashtags `businesscoaching`, `vertriebscoach` | 27 Konten, 31 von 50 Beiträgen deutsch; Profile: 15/27 mit Website, 0 mit Adresse in der Bio, Follower-Median 136 |

Lehre: Beide Quellen liefern Kandidaten, keine Kontakte. Der zweite Schritt läuft über die
Website und das Impressum; bei LinkedIn zusätzlich nach selbstständigen Coaches filtern
(Firma = eigener Name, „Selbstständig“, „Freiberuflich“, „Coaching“ im Firmennamen).

## SaaS-Firmen in DACH (14.10.2026, Weg F)

Vollerhebung Hamburg plus Berlin und München (11 bis 200 Mitarbeiter), dazu alle OMR-Produkte.

| Quelle | Menge | Sitz in DACH | B2B-SaaS-Anteil | Kosten |
|---|---|---|---|---|
| LinkedIn Branche 4, Standort Berlin, 11–200 MA (Full) | 50 | 30 % | – | 0,145 $ |
| LinkedIn Branche 4, Standort „Germany“, 11–50 MA (Full) | 50 | 24 % | – | 0,145 $ |
| LinkedIn Suchwort „SaaS“, „Germany“ (Full) | 50 | 16 % | hoch, aber viele Agenturen | 0,15 $ |
| LinkedIn Suchwort „SaaS“ + Branche 4, drei BW-Städte (Full) | 47 | 83 % | fast alle | 0,115 $ |
| LinkedIn Branche 4, Hamburg alle Größen (Short, segmentiert) | 1.427 | 81 % Sitz Hamburg | 34 % | 1,36 $ |
| LinkedIn Branche 4, Berlin + München 11–200 MA (Short) | 2.745 | 51 % Sitz in der Stadt | 50 % | 2,64 $ |
| OMR Reviews, alle Produkte | 12.593 Domains | 4.640 mit Sitz in DACH (37 %; DE 4.023, AT 343, CH 274), davon 1.565 mit .com | Software-Verzeichnis | 0 $ |
| Startbase, alle Profile | 9.665 | 100 % DE | 23 % aktive B2B-SaaS (2.209) | 0 $ |
| Google-Footprints („kostenlos testen“, „Demo vereinbaren“ + Hamburg), 6 Queries | 237 Domains | 44 mit Sitz Hamburg | gemischt | 0,014 $ |

**Abdeckung Hamburg:** LinkedIn 387 B2B-SaaS, OMR 246 mit Hamburger Impressum, Startbase 135
B2B-SaaS. LinkedIn und OMR teilen 62, LinkedIn und Startbase 27; von den 135 Startbase-Firmen
stehen 90 in keiner der beiden anderen Quellen. Schätzung (Lincoln-Petersen) 1.500 bis 2.000 SaaS
mit Sitz Hamburg; jede Quelle allein findet 7 bis 26 %. Irgendwo auf OMR (unabhängig vom
Impressum) stehen 23 % der Hamburger und 27 % der Berliner und Münchner LinkedIn-SaaS. Die Google-Footprints
fanden 30 Hamburger SaaS, davon etwa 20 auch auf LinkedIn; die übrigen stehen dort unter anderer
Branche (IT Services, Technology/Internet) oder haben keine Firmenseite.

**Sitzprüfung im Impressum** (`sitz_check.py`, 379 Hamburger SaaS-Websites, 27 s): 71 % Sitz in
DACH erkannt, 73 % mit Adresse, 15 % Impressum nur per JavaScript, 7 % nicht erreichbar.

**Startbase komplett** (9.665 Profile, 25 min): 2.209 aktive B2B-SaaS; Berlin 529, Bayern 423,
NRW 357, Baden-Württemberg 252, Hessen 140, Hamburg 135; 54 % mit 1 bis 10, 35 % mit 11 bis 50
Mitarbeitern.

**Website-Suche für Startbase** (Rechtsträger + Ort): Stichprobe 116 Firmen 58 %, alle 1.670
Firmen ohne Website 52 % (871).

**Gesamtliste DACH aus der Testreihe** (OMR komplett, Startbase komplett, LinkedIn Hamburg sowie
Berlin und München 11 bis 200 Mitarbeiter, alle mit Sitzprüfung): 6.135 Firmen, 5.333 mit
Adresse, 1.581 mit OMR-Bewertung; DE 5.512 (inkl. 457 aus LinkedIn und Startbase ohne erkannten
Sitz), AT 343, CH 280. Herkunft: nur OMR 4.112, nur Startbase 774, nur LinkedIn 625, mehrere
Quellen 624. Apify-Kosten der ganzen Testreihe 8,67 $.

## Query-Formulierung — was messbar wirkt

1. **„Coach" statt „Trainer".** „Coach" zieht Premium-Positionierung, „Trainer" günstige
   Freelancer und Kursanbieter.
2. **Zusammengesetzte Begriffe zusammenschreiben.** `Führungskräftecoaching` schlägt
   `Führungskräfte Coaching`: die Zwei-Wort-Variante liest Google als informationelle Suche und
   liefert Lexikon- und Ratgeberartikel statt Anbieter-Websites.
3. **Beide Schreibweisen abdecken, wo sie üblich sind** (`Marketingagentur` und
   `Marketing Agentur`, `SEO Agentur` und `SEO-Agentur`) — die Ergebnismengen überlappen nur zum Teil.
4. **Englische Begriffe im B2B mitnehmen** (`Executive Coach`, `Leadership Coach`) — viele
   B2B-Anbieter positionieren sich international. Rein englische Queries allein liefern im
   DACH-Raum aber oft leere oder internationale Treffer, deutsche Variante also immer dazu.
5. **Zu generische Queries kosten Trefferquote, nicht Geld** — der Filter wirft sie weg, aber die
   Liste wird kürzer als geplant. Spezifischer formulieren statt mehr Seiten scrapen.

## `-site:`-Ausschlüsse in der Query

**Maximal 8–10 Ausschlüsse pro Query-Zeile.** Belegt: längere Queries (25+ Ausschlüsse) bringen
den SERP-Actor dazu, leere Ergebnisse zurückzugeben. `build_queries.py --exclude` ist deshalb
auf wenige Domains voreingestellt.

Die Ausschlüsse in der Query decken nur die schlimmsten Treiber ab; die vollständige Filterung
macht `process_serp.py` gegen `noise-domains.md`. Bewährter Kern für Google-Wege:

```
-site:indeed.com -site:stepstone.de -site:kleinanzeigen.de -site:facebook.com
-site:instagram.com -site:linkedin.com -site:youtube.com -site:xing.com
```

So erzeugen (der `--exclude N`-Zähler nimmt nur die ERSTEN N Domains aus noise-domains.md,
nie diesen Kern — für den Kern und fürs Tauschen immer `--exclude-domains` verwenden):

```
python3 ../datenbeschaffung-referenzen/scripts/build_queries.py --keywords "..." \
  --exclude-domains "indeed.com,stepstone.de,kleinanzeigen.de,facebook.com,instagram.com,linkedin.com,youtube.com,xing.com"
```

Nischen-Ergänzung statt Verlängerung: den nischenspezifisch stärksten Treiber gegen einen der
Kern-Ausschlüsse tauschen (B2C-Coaching: `superprof.de` und `yelp.com`; B2B: `kununu.com` und
`glassdoor.com`; E-Commerce: `amazon.de`, `otto.de`, `zalando.de`, `idealo.de`).

## Seitenzahl je Query (Erfahrungswerte)

| Zielgruppe | Seiten | Warum |
|---|---|---|
| B2B-Dienstleister (Weg A) | 5 | schwächeres SEO als Coaches, ab Seite 6 kaum noch Neues |
| E-Commerce (Weg B) | 4 | die Shops mit eigener Marke stehen auf Seite 1–3 |
| Coaches (Weg D) | 7 | Seite 4–7 fängt Coaches mit schwachem SEO — genau die mit Bedarf |
