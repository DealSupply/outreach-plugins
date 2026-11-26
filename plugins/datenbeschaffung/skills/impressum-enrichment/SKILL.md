---
name: impressum-enrichment
description: Anreicherungs-Baustein des Datenbeschaffungs-Pakets: holt für Domains ohne E-Mail-Adresse die Adresse und den Geschäftsführer aus dem deutschen Impressum, über einen Apify-Actor im eigenen Konto (unter 20 Domains kostenlos durch die KI selbst). Mit DealSupply optional (seit MCP 4.0.0 dürfen Leads mit eigener Website ohne E-Mail importiert werden, die Recherche sucht dann), ohne DealSupply Pflicht. Wird von weg-*-Skills für Leads ohne E-Mail geladen, nie direkt.
---

# Impressum-Enrichment: der DACH-Lückenfüller

Holt aus deutschen Impressumsseiten eine E-Mail-Adresse je Lead (info@ reicht) und, wo der Actor
ihn liefert, den Geschäftsführer oder Inhaber. Wird von Weg-Skills für die Kontaktlücke gerufen:
er ist KEIN eigener Weg.

- **Mit DealSupply** ist er ab MCP 4.0.0 **optional**: Leads mit eigener Website dürfen ohne
  E-Mail importiert werden, dann sucht die Recherche die Adresse. Er lohnt, wenn er billiger ist
  als die Recherche und vor der Qualifizierung liegt (Kriterien unten unter „Wann es sich lohnt“).
  Auf älteren Servern ist er der Weg, Leads ohne Adresse überhaupt importierbar zu machen. Den
  Ansprechpartner, seine persönliche Adresse und Registerdaten sucht danach die Recherche der
  Plattform; dafür lohnt kein eigener Lauf (`../datenbeschaffung-referenzen/references/datenumfang.md`).
- **Ohne DealSupply** ist er **Pflicht** für jede Domain ohne Adresse, und der Geschäftsführer aus
  dem Impressum ist der Ansprechpartner der Liste (der alte Kurs verspricht genau das, Kap. 6 und
  10; bei kleineren Firmen ist er oft auch der Entscheider). Ohne diesen Schritt bleibt die Zeile
  ohne Adresse und fällt aus der Liste (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`).

Bei Google Maps steckt das Impressum schon in der Kontaktanreicherung des Scrapes, `build_csv.py`
nimmt die Adresse von dort: Diese Stufe läuft nur noch für die Domains, bei denen beides leer blieb. DealSupply selbst reichert nichts per Impressum an: der Lauf findet
beim Anbieter (Apify, eigenes Konto) statt, das Ergebnis wird in die Roh-CSV gemerged und läuft
über `listen-qualitaet` in den Import.

Input: Liste von Domains/Websites (z. B. die `keine-email`-Teilmenge aus Weg C, oder die
Domain-CSV aus `process_serp.py`). Vorher gegen den Bestand abgleichen (`check_leads_exist` mit
`domains`, oder `dedup.py` gegen `export_leads(format="index")`; ohne DealSupply `sperrliste.py`
gegen den CRM-Export) — Domains bekannter Leads kosten sonst unnötig Geld; `do_not_contact` und
gesperrte Firmen nie anreichern.

Kosten fallen beim Anbieter an; Betrag und Deckel vorab nennen, Lauf nur nach ausdrücklicher
Freigabe genau dieses Umfangs.

## Actor & Betriebsregeln (belegt 19.08.2026)

Primär + Fallbacks stehen in `../datenbeschaffung-referenzen/references/apify-actors.md` (Impressum-Kategorie).
Die Regeln sind NICHT optional:

1. **Nur Domain-Modus (`inputMode: "urls"`).** Der `searchTerms`-Modus bricht mit Städten als
   `locationName` (belegter Bug: `Invalid Field: 'location_name'` — nur „Germany" funktioniert)
   und scrapt ungefiltert Portale mit. Die Domain-Liste kommt aus dem Weg-Skill, nicht aus
   einer actor-internen Google-Suche.
2. **`domainBlacklist` IMMER setzen** — die Portal-Domains aus `../datenbeschaffung-referenzen/references/noise-domains.md`
   (kommagetrennt). Portale werden sonst voll berechnet: bares Geld.
3. **Batches fahren.** Jeder Lauf kostet die Actor-Startgebühr (`kosten.md`) — nie tröpfeln, minimal ~50 Domains je Lauf.
   Über 200 Domains in Batches von 200 teilen (Kurshandbuch Kap. 10): nicht wegen des Actors,
   sondern um nach jedem Batch die Trefferquote zu prüfen und bei Problemen nicht die ganze Liste
   zu verlieren.
4. **Actor nach Zweck wählen.** Für die reine Adresse genügt der günstigste Actor, der sie
   liefert: Fallback A kostet rund ein Viertel des Primär-Actors, die Verifizierung folgt in
   `listen-qualitaet`. Vor dem ersten Einsatz mit fünf Domains prüfen, ob er die Adressen liefert.
   Den Primär-Actor nehmen, wenn Fallback A leer bleibt oder die Validierung im selben Lauf
   gewünscht ist. Fallback B ist der Ausweg, wenn beide ausfallen (Ein-Entwickler-Risiko).
   **Ohne DealSupply** den Primär-Actor nehmen: Nur er liefert die Entscheider mit Rolle
   (`apify-actors.md`), und er prüft die Adressen im selben Lauf. Fallback A nur, wenn ein Test
   mit fünf Domains zeigt, dass er den Namen mitliefert.

## Standard-Input (Primär-Actor)

```json
{
  "inputMode": "urls",
  "targetUrls": [{"url": "https://<domain-1>/"}, {"url": "https://<domain-2>/"}],
  "languageCode": "de",
  "validateEmail": true
}
```

Kosten vorher nennen — die Zahlen (je erfolgreicher Domain inkl. Validierung + Startgebühr)
kommen NUR aus `../datenbeschaffung-referenzen/references/kosten.md`, nie aus dem Gedächtnis.
Deckel setzen.

## Auswertung

- `email_status` UNDELIVERABLE → Zeile verwerfen (die Validierung ist hier schon bezahlt —
  `listen-qualitaet` verifiziert diese Leads NICHT erneut).
- `decision_makers`: Liefert der Actor sie ohnehin mit, wird die erste Person mit Rolle
  Geschäftsführer/Inhaber `firstName`/`lastName` (mit DealSupply bestätigt die Recherche sie im
  Impressum). Kommt der Name nur als ein Feld (`managingDirector`), legt `build_csv.py` ihn in
  `inhaber`; `instantly_csv.py` teilt ihn später in Vor- und Nachname, wo das eindeutig ist. Bei
  mehreren Geschäftsführern nur den ersten nehmen, nie raten. Weitere Entscheider,
  `register_number` und `vat_id` nicht übernehmen: kein Einstieg für die Mail.
- Merge zurück in die Roh-CSV über die Root-Domain (`build_csv.py`-Format bleibt erhalten;
  `quelle` um `+impressum` ergänzen).

## Trefferquote prüfen (nach jedem Batch)

Erwartung laut Kurshandbuch (Kap. 10, Stand 19.08.2026; eigene Messung im Plugin: 29 von 40
LinkedIn-Firmen, siehe unten):

| Website-Typ | E-Mail | Telefon | Geschäftsführer | Adresse |
|---|---|---|---|---|
| Deutsche Online-Shops | 80 bis 90 % | 75 bis 85 % | 70 bis 80 % | 75 bis 85 % |
| Agenturen und Berater | 85 bis 95 % | 80 bis 90 % | 75 bis 85 % | 80 bis 90 % |
| Coaches und Trainer | 75 bis 85 % | 60 bis 75 % | 80 bis 90 % | 60 bis 75 % |
| Internationale Seiten | 50 bis 70 % | 40 bis 60 % | 30 bis 50 % | 40 bis 60 % |

**Qualitätsschwelle:** Bei deutschen Firmenwebsites sollen mindestens 60 bis 70 % eine E-Mail und
ein Telefon bekommen. Unter 50 % heißt: Die URLs sind veraltet, es sind keine deutschen Seiten, oder
sie haben kein Impressum. Dann nicht den nächsten Batch starten, sondern die Ursache suchen (Liste
mit Portal- oder Auslandsdomains, falscher Weg). Für Ziele außerhalb DACH gilt die Zeile
„Internationale Seiten“ (`../datenbeschaffung-referenzen/references/ausserhalb-dach.md`). Dazu 5 bis
10 Einträge stichprobenartig öffnen: Stimmen E-Mail, Telefon und Name? Die Domains ohne Fund gehen
in den `kontaktseiten-fallback` (laut Kurs 5 bis 15 % zusätzliche Treffer).

## Unter 20 Domains: kostenlos, ohne Apify

Für einzelne Checks mit weniger als 20 Domains liest die KI die Impressumsseiten selbst (in Claude
Code mit dem Web-Abruf, sonst mit dem Browser-Werkzeug der Umgebung): je Domain die Startseite,
den Link „Impressum“ (sonst `/impressum`), daraus E-Mail, Telefon, Geschäftsführer oder Inhaber und
Firmenname. Kostet nichts, braucht keinen Apify-Lauf und keine Startgebühr. Der Kurs empfiehlt ab
20 Domains den Actor, weil er mehr Adressen und vor allem mehr Telefonnummern findet (Kap. 10).
Funde gehen genauso in die Roh-CSV (`quelle` um `+impressum-selbst` ergänzen) und sind ungeprüft:
Sie laufen in `listen-qualitaet` durch die Prüfung der Adressen.

## Wann es sich lohnt (mit DealSupply)

Ohne DealSupply stellt sich die Frage nicht: Jede Domain ohne Adresse läuft hier durch.

Entscheidungstabelle: `../datenbeschaffung-referenzen/references/datenumfang.md`, Abschnitt „Die
Kontaktlücke“. Kurz: Quelle ohne Kontaktdaten (Google-Suche, LinkedIn-Firmen,
Instagram-Websites) **und** ab etwa 50 Domains; `max_leads` knapp; großer Abo-Lauf mit knappem
Kontingent; oder der Nutzer will verifizierte Adressen vor dem Import. Rund 0,2 Cent je Domain
gegen 2 bis 3 Cent für Qualifizierung und Recherche eines Leads, der danach mangels Adresse
ausscheiden kann.

## Wann NICHT anreichern

- Mit DealSupply: kleine Liste oder Pilot auf einem 4.0.0-Server → direkt mit Website importieren,
  die Recherche sucht die Adresse.
- Nach einem Maps-Lauf mit Kontaktanreicherung bringt ein Impressum-Lauf wenig: Im Test vom
  11.10.2026 fanden drei Actors für 28 Domains ohne Adresse nur 1 bis 5. Mit DealSupply nur bei
  großem Volumen anbieten; ohne DealSupply trotzdem fahren (unter 20 Domains kostenlos, siehe oben)
  und die niedrige Erwartung vorher nennen. Bei Quellen ohne Kontaktdaten (LinkedIn-Firmen, Google-Suche) ist er dagegen der
  Normalfall: 29 von 40 LinkedIn-Firmen bekamen eine Adresse (haketa, 0,0017 $ je Domain).

- Lead hat schon eine E-Mail aus dem Scrape → kein Impressum-Lauf, auch nicht für
  Entscheider-Namen: die findet mit DealSupply die Recherche. Ohne DealSupply nur auf Wunsch des
  Nutzers, wenn der Name fehlt und die Mail mit dem Vornamen beginnen soll, mit genannten Kosten.
- Nicht-DACH-Domains → der Actor ist auf deutsche Impressumspflicht gebaut; für .com/.co.uk den
  `kontaktseiten-fallback` nehmen.
- < 20 Domains → Startgebühr frisst den Nutzen: Mit DealSupply die Recherche suchen lassen oder
  sammeln bis zum Batch; ohne DealSupply den kostenlosen Weg oben nehmen.
