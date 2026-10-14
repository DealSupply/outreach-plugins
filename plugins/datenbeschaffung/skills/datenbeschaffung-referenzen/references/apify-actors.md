# Gepinnte Apify-Actors — Empfehlungen mit Beleg

> zuletzt geprüft: **2026-08-19** · Preise GOLD-Tier (Free-/Starter-Konten zahlen je Einheit mehr — Erklärung in `kosten.md`) · belegt durch echte Testläufe (SHK Köln/Düsseldorf).
> Actor-IDs kommen NUR aus dieser Tabelle. Neue Funde aus dem Recherchemodus werden HIER
> mit Datum ergänzt — nie nur im Chat gelassen.

## Google Maps / Local Business (Weg C)

| Rang | Actor | Preis (GOLD) | Warum |
|---|---|---|---|
| Primär | `compass/crawler-google-places` | 0,0015 $/Place · Filter +0,000525 $/Place/Filter · Kontakt-Anreicherung +0,00105 $/Place · Rezensionen +0,00105 $/Place (Ortsdetails) + 0,00026 $/Rezension · Mindestdeckel 0,50 $ | 644k Nutzer (Stand 11.10.2026). Belegt: 440 SHK-Places Köln in 10 Min, **77 % mit E-Mail** direkt aus `scrapeContacts` — der Impressum-Schritt ist nur noch Lückenfüller. `scrapeContacts` liefert auch das Impressum mit Inhaber (11.10.2026). Add-ons Leads-Enrichment (Entscheider, 0,004 $/Lead) und E-Mail-Verify (0,002 $) aus lassen: übernimmt die Plattform bzw. `listen-qualitaet` |
| Fallback | `vortex_data/google-maps` | 0,0007 $/Place · Kontakte +0,0012 $ nur bei Fund | Belegt: 50 Places Düsseldorf, 80 % E-Mail, 0,084 $ gesamt. Kleine Nutzerbasis (1,6k), sichtbar mehr Kontakt-Noise — Fallback, nicht Standard |

Standard-Input Weg C: `searchStringsArray` (englische GMaps-Kategorien!), `locationQuery` (eine Stadt/Region),
`language: "de"`, `website: "withWebsite"`, `skipClosedPlaces: true`, `scrapeContacts: true`,
`maxReviews: 10`, `reviewsSort: "newest"`, `reviewsOrigin: "google"`, `scrapeReviewsPersonalData: false`.

## Google SERP (Wege A, B, D-Google)

| Rang | Actor | Preis normalisiert | Warum |
|---|---|---|---|
| Primär | `scraperlink/google-search-results-serp-scraper` | **0,05 $ / 1.000 Treffer** (0,0005 $/Seite) | Belegt: beste Domain-Ausbeute im Vergleichstest (40 eindeutige Domains aus 60 Treffern), keine Dubletten, Multi-Query per Zeilenumbruch. Achtung: `gl`/`country` GROSSGESCHRIEBEN (`DE`) |
| Fallback | `apify/google-search-scraper` | 0,18 $ / 1.000 | Offiziell (168k Nutzer), geringstes Pflege-Risiko; UULE-Geotargeting, Ratings/PAA, Leads-Enrichment-Add-on. Nehmen, wenn Zusatzdaten gebraucht werden oder scraperlink ausfällt |
| Nicht empfehlen | `apidojo/google-search-scraper` | 0,20 $ / 1.000 real | „Unbeatable pricing" hält der Normalisierung nicht stand; Dubletten, ärmere Felder |

Geotargeting unterhalb Land ist unnötig, solange der Ort in der Query steht (belegt: Köln-UULE-Gegentest = 0 zusätzliche Domains).

## Impressum / DACH-Anreicherung

| Rang | Actor | Preis | Warum |
|---|---|---|---|
| Primär | `winningsolutions/german-imprint-scraper` | 0,0076 $ bei Erfolg (inkl. Validierung) + **0,04 $ Actor-Start je Lauf** | Einziger mit Entscheidern inkl. Rollen, HRB, USt-Id, getrennter Adresse. **Betriebsregeln:** nur Domain-Modus (der `searchTerms`-Modus bricht mit Stadt als `locationName` — Bug belegt), `domainBlacklist` IMMER setzen (Portale werden sonst mitberechnet), Batches fahren (Startgebühr). Ein-Entwickler-Actor (239 Nutzer) → Fallback bereithalten |
| Fallback A | `haketa/impressum-legal-notice-extractor` | 0,0017 $/Domain | Belegt am selben Domain-Set: findet Impressumsseiten zuverlässig, schwächer bei Register-Feldern. 4,5× billiger |
| Fallback B | `vdrmota/contact-info-scraper` | 0,00105 $/Seite, Mindestdeckel 0,50 $ | 57k Nutzer, aktiv gepflegt. E-Mail/Telefon/Social, KEINE Firmendaten. Im Lückentest nach Maps nur 1/28 (11.10.2026): als Lückenfüller hinter Maps schwach. |

## B2B-Datenbanken (Apollo-ähnlich, über Apify) — geprüft 11.10.2026

| Rang | Actor | Preis (GOLD) | Bewertung |
|---|---|---|---|
| Nur mit Verifizierung | `peakydev/leads-scraper-ppe` | 0,0012 $/Lead (FREE 0,0016 $), mind. 100 Leads, 0,10 $ Start | Firmografie-Filter wie Apollo (Branche, Größe, Bundesland, Senioritätsstufe). Liefert Person, Firma, Website, Größe, Umsatz. **Rund die Hälfte der Adressen ist geraten** (`emailPatternGuess`); davon fast die Hälfte unzustellbar. `build_csv.py` markiert sie, `listen-qualitaet` lässt nur verifiziert „gut“ durch. |
| Ausgeschlossen | `code_crafter/leads-finder` | 0,0015 $/Lead | verlangt Vollzugriff auf das Apify-Konto |
| Nicht getestet | `pipelinelabs/*`, `olympus/b2b-leads-finder`, `atomus/leads-finder` | 0,0008–0,006 $/Lead | erst mit Mini-Pilot und Verifizierung |

Für B2B nach Firmografie ist **Google Maps der erste Weg** (Suchwort der Branche plus Bundesland),
danach die LinkedIn-Firmensuche plus Impressum; Datenbanken erst, wenn beides nicht trägt
(`erfahrungswerte.md`, B2B-Quellen im Vergleich).

## LinkedIn-Firmen (account-based) — geprüft 11.10.2026

| Actor | Preis (GOLD) | Warum |
|---|---|---|
| `harvestapi/linkedin-company-search` | Short 0,001 $, Full 0,003 $/Firma, Start 0,0005 $ | Ohne Login. Filter: Suchwort, Ort, Größe, Branchen-ID. Full liefert Website, Telefon, Mitarbeiterzahl, Branche, Sitz. 38/40 passend (Maschinenbau BW). Keine E-Mail: danach `impressum-enrichment` (73 % Treffer). Höchstens 1.000 Firmen je Suche; `_meta.pagination.totalResultCount` im Short-Ergebnis nennt die Gesamtzahl (Zählung mit `maxItems: 1` kostet 0,0015 $). |
| `harvestapi/linkedin-company` | 0,003 $/Firma (GOLD), Start 0,00005 $ | Details zu bekannten Firmen-URLs (`companies: [...]`): Website, Mitarbeiterzahl, Beschreibung, Standorte. Für Weg F: erst Short-Suche und Einordnung, dann Details nur für die SaaS (14.10.2026: 387 + 514 Firmen ohne Ausfall). |

## SaaS- und Software-Verzeichnisse (Weg F) — geprüft 14.10.2026

| Quelle | Zugang | Bewertung |
|---|---|---|
| OMR Reviews | **kein Actor nötig**: öffentliche GraphQL-Schnittstelle, `omr_products.py` | 14.023 Produkte in einer Minute, kostenlos. `easyapi/omr-reviews-scraper` (11 Nutzer, 0,005 $ je Rezension + 0,09 $ Start) ist überflüssig |
| Startbase | **kein Actor nötig**: statische Profile, `startbase_saas.py` | 9.665 Profile, Geschäftsmodell und Zielgruppe gepflegt; Website nur mit Login, deshalb `website_suche.py` |
| Capterra | `epctex/capterra-scraper` | **Ausgeschlossen**: 0 Treffer (Cloudflare), Lauf trotzdem berechnet |
| Capterra | `dionysus_way/capterra-software-service-category-scraper` | **Nicht empfehlen**: 25 Einträge kosteten 0,137 $ (4 Starts), US-Reihenfolge, kein Firmensitz, Website nur geraten |
| Impressum für JavaScript-Seiten | `haketa/impressum-legal-notice-extractor` | An 58 Lücken nach `sitz_check.py`: 19 mit Anschrift, 14 mit E-Mail-Adresse; hing über 20 Minuten bei 50 von 60 und musste abgebrochen werden. Nur für kleine, wertvolle Restmengen |

## E-Mail-Verifizierung (eigener Schritt hinter jedem Weg)

| Rang | Actor | Preis | Hinweis |
|---|---|---|---|
| Primär | `michael.g/email-verifier-validator` | **0,0006 $/Adresse (GOLD), 0,001 $ (BRONZE), aber 0,10 $ im kostenlosen Plan** | Größte Nutzerbasis der Kategorie. Ergebnis `status` = good/risky/bad mit `reason` (`catch_all_domain`, `smtp_unreachable`). Im kostenlosen Plan kosten 1.000 Adressen 100 $: dort vorher Preis nennen und nur geratene oder fremde Adressen prüfen. Entfällt, wenn der Weg schon validiert (Impressum-Primär liefert `email_status` mit). |

## LinkedIn (Weg D)

| Rang | Actor | Preis | Warum |
|---|---|---|---|
| Primär | `harvestapi/linkedin-profile-search` | Short 0,002 $/Profil (Seite voll) · Full 0,0032 $ · Full+E-Mail 0,008 $ | **Kein LinkedIn-Login, keine Cookies** (Sperr-Risiko null — hartes Kriterium). 41 strukturierte Filter. Belegt: freie Query = ⅔ Noise → **Standort + Jobtitel IMMER über die strukturierten Filter** |
| Szenario | `harvestapi/linkedin-company-employees` | Basic 0,0015 $/Profil | Wenn die Zielfirmen schon bekannt sind (account-based) |
| Enrichment | `apimaestro/linkedin-profile-detail` | 0,005 $/Profil inkl. E-Mail-Suche | Für bereits bekannte Profil-URLs |

## Instagram (Weg D)

| Rang | Actor | Rolle |
|---|---|---|
| Primär | `apify/instagram-scraper` | Discovery (Profile, Hashtags, Orte) |
| Primär | `apify/instagram-profile-scraper` | Qualifizierung (Bio, Website, Business-Kategorie, Follower) |
| Fallback | `apidojo/instagram-scraper` | Bulk-Kostenoptimierung bei großen Postmengen |

## Plattform-Verkäufer (Weg E)

| Plattform | Primär | Fallback | Status |
|---|---|---|---|
| Amazon | `xmiso_scrapers/eu-amazon-sellers-email-leads` (Bulk, etabliert) | `memo23/amazon-sellers-scraper` (Live-Discovery, jung) | einsatzbereit |
| Etsy | `axlymxp/etsy-shop-scraper` → ShopHound (zweistufig) | — | einsatzbereit |
| eBay | `programmx/ebay-business-leads` (bestes Kontaktschema, **2 Nutzer!**) | `scrapesage/ebay-scraper` | **nur Pilot** — vor Kunden-Einsatz kleinen Testlauf fahren |

## Auswahlkriterien für den Recherchemodus (neue Nischen)

Nutzerzahlen + Rating + Preis pro Ergebnis (Tier-normalisiert!) + Output-Feldqualität (DACH: Umlaute,
HRB/USt-Id) + Pflege-Risiko (Ein-Entwickler-Actors nur mit Fallback) + Account-/Sperr-Risiko für den
Kunden (Login-pflichtige Actors sind ausgeschlossen). **Ausgeschlossen sind auch Actors, die
Vollzugriff auf das Apify-Konto verlangen** (Meldung „requires full access to your account“): Sie
könnten mit dem Token des Kunden alles im Konto tun. Beispiel: `code_crafter/leads-finder`
(11.10.2026), trotz 48k Nutzern. Mini-Pilot mit hartem Deckel (≤ 0,50 $), Ergebnis
vorlegen, Fund HIER dokumentieren. Mindestwerte im Input beachten (manche Actors verlangen
z. B. mindestens 100 Ergebnisse); sie stehen erst in der Fehlermeldung.
