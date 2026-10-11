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

## Coaches (11.10.2026)

| Quelle | Ergebnis |
|---|---|
| LinkedIn-Personensuche (Short), Vertriebs- und Business-Coaches BW | 50 Profile, ~68 % selbstständig, 32 % angestellt (z. B. Bank); ohne Website und E-Mail |
| Instagram-Hashtags `businesscoaching`, `vertriebscoach` | 27 Konten, 31 von 50 Beiträgen deutsch; Profile: 15/27 mit Website, 0 mit Adresse in der Bio, Follower-Median 136 |

Lehre: Beide Quellen liefern Kandidaten, keine Kontakte. Der zweite Schritt läuft über die
Website und das Impressum; bei LinkedIn zusätzlich nach selbstständigen Coaches filtern
(Firma = eigener Name, „Selbstständig“, „Freiberuflich“, „Coaching“ im Firmennamen).

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
