# Kosten — belegte Größenordnungen

> zuletzt geprüft: **2026-10-11** (Google Maps) bzw. **2026-08-19** (übrige) · GOLD-Tier · Quelle: echte Läufe (SHK Köln/Düsseldorf, Elektro Stuttgart).
> Die Kosten fallen beim Anbieter (Apify/Outscraper) auf dem Konto des Kunden an, nicht in ListM8.
> Regel: Vor JEDEM kostenpflichtigen Lauf die erwarteten Kosten aus dieser Tabelle kalkulieren
> und dem Nutzer nennen. Jeder Lauf bekommt einen harten Deckel (`maxTotalChargeUsd`) und die ausdrückliche Freigabe des Nutzers.
>
> **Was „GOLD-Tier" heißt:** Apify staffelt die Pay-per-Event-Preise nach Konto-Tier
> (FREE/BRONZE/SILVER/GOLD — abhängig vom Monatsumsatz). Diese Tabelle nennt GOLD-Preise;
> **Free-/Starter-Konten zahlen je Einheit MEHR** (teils 20–50 %). Bei der Pflicht-Kostennennung
> für einen Neukunden deshalb dazusagen: „Zahlen sind GOLD-Tier — dein Konto zahlt anfangs etwas
> mehr; das eigene Tier steht in der Apify-Konsole unter Billing."

## Belegte Ist-Kosten

| Schritt | Kosten real | Beleg |
|---|---|---|
| 440 Maps-Places (Köln) inkl. Kontakt-Anreicherung + 2 Filter | ~1,60 $ (≈ 0,0036 $/Place) | Lauf 19.08.2026 |
| 50 Maps-Places (vortex, Düsseldorf) inkl. Kontakte | 0,084 $ (≈ 0,0017 $/Place) | Lauf 19.08.2026 |
| 15 Maps-Places (Elektro Stuttgart) inkl. Kontakte + 2 Filter, ohne Rezensionen | 0,054 $ (0,0036 $/Place) | Lauf 11.10.2026 |
| dieselben mit den 10 neuesten Rezensionen (85 geliefert) | 0,092 $ (0,0061 $/Place): + 0,00105 $/Place Ortsdetails, + 0,00026 $/Rezension | Lauf 11.10.2026 |
| 1.000 SERP-Treffer (scraperlink) | 0,05 $ | Lauf 19.08.2026 |
| Impressum je erfolgreicher Domain (winningsolutions) | 0,0076 $ + 0,04 $ Startgebühr je Lauf | Lauf 19.08.2026 |
| Impressum je Domain (haketa, Fallback) | 0,0017 $ | Lauf 19.08.2026 |
| E-Mail-Verifizierung | 0,0006 $/Adresse | Metadaten 19.08.2026 |
| LinkedIn Short-Profil | 0,002 $ (bei voller Suchseite) | Lauf 19.08.2026 |

## Daumenregeln für die Vorab-Kalkulation

| Vorhaben | Größenordnung |
|---|---|
| Pilot (eine Stadt, ~30 bis 50 Ergebnisse, Weg C mit Rezensionen) | **0,20 bis 0,30 $** (kostenloser Plan: bis ~0,65 $) |
| Eine Großstadt komplett, Weg C (300–500 Places, Kontakte, Filter) | **1–2 $**, mit Rezensionen **2–3 $** |
| 1.000 versandfertige Leads Weg C (Scrape + Impressum-Lücke + Verify) | **5–8 $** |
| SERP-Discovery für eine Nische DACH-weit (Wege A/B) | **unter 1 $** |
| 500 LinkedIn-Profile Full | **~1,60 $** |

## Was Kosten unnötig treibt (vermeiden)

1. **Bekannte Leads erneut anreichern** → Vorab-Abgleich fahren (`outreach-uebergabe.md`, dedup.py) —
   der Bestand wird VOR der Anreicherung abgezogen, nicht danach.
2. **Portale im Impressum-Lauf** → `domainBlacklist` aus `noise-domains.md` setzen; Portale werden
   sonst voll berechnet.
3. **Tröpfel-Läufe beim Impressum-Actor** → 0,04 $ Startgebühr je Lauf: Batches fahren.
4. **Filter stapeln ohne Not** (Maps) → jeder Filter kostet je Place extra; nur `withWebsite` +
   `skipClosedPlaces` sind fast immer ihr Geld wert.
5. **Freie LinkedIn-Queries** → ⅔ Noise = ⅔ verbranntes Geld; strukturierte Filter nutzen.
6. **Zusätze des Maps-Actors, die die Plattform übernimmt** → Business-Leads-Anreicherung
   (Entscheider, 0,004 $/Lead) und E-Mail-Verifizierung im Actor (0,002 $/Adresse) aus lassen;
   Ansprechpartner findet die Recherche, verifiziert wird günstiger in `listen-qualitaet`
   (`datenumfang.md`).

## Preisstufen am Beispiel Google Maps (Stand 2026-10-11)

| Ereignis | FREE | BRONZE | SILVER | GOLD |
|---|---|---|---|---|
| Place | 0,004 $ | 0,003 $ | 0,002 $ | 0,0015 $ |
| Filter je Place | 0,001 $ | 0,001 $ | 0,00075 $ | 0,000525 $ |
| Kontaktanreicherung je Place | 0,002 $ | 0,002 $ | 0,0015 $ | 0,00105 $ |
| Ortsdetails je Place (fällt mit Rezensionen an) | 0,002 $ | 0,002 $ | 0,0015 $ | 0,00105 $ |
| Rezension | 0,0005 $ | 0,0005 $ | 0,00037 $ | 0,00026 $ |

Im kostenlosen Plan kostet ein Place mit zwei Filtern, Kontakten und rund sechs Rezensionen etwa
0,013 $, also gut doppelt so viel wie bei GOLD. Bewertung, Anzahl und Rezensions-Stichworte sind in
jeder Stufe im Place-Preis enthalten.
