---
name: impressum-enrichment
description: Optionaler Anreicherungs-Baustein des Datenbeschaffungs-Pakets: holt für Domains ohne E-Mail-Adresse die Adresse aus dem deutschen Impressum, manuell über einen Apify-Actor im eigenen Konto. Spart Recherche-Kosten und liefert geprüfte Adressen vor dem Import; seit ListM8 MCP 3.0.0 keine Pflicht mehr (Leads mit eigener Website dürfen ohne E-Mail importiert werden). Entscheider, Register und persönliche Adressen findet die Recherche der Plattform. Wird von weg-*-Skills für Leads ohne E-Mail geladen, nie direkt.
---

# Impressum-Enrichment — der DACH-Lückenfüller

Holt aus deutschen Impressumsseiten eine E-Mail-Adresse je Lead (info@ reicht). Wird von
Weg-Skills für die Kontaktlücke gerufen: er ist KEIN eigener Weg. Ab ListM8 MCP 3.0.0 ist er
**optional**: Leads mit eigener Website dürfen ohne E-Mail importiert werden, dann sucht die
Recherche die Adresse. Er lohnt, wenn er billiger ist als die Recherche und vor der Qualifizierung
liegt (Kriterien unten unter „Wann es sich lohnt“). Auf älteren Servern ist er der Weg, Leads ohne
Adresse überhaupt importierbar zu machen. Den
Ansprechpartner, seine persönliche Adresse und Registerdaten sucht danach die Recherche der
Plattform; dafür lohnt kein eigener Lauf (`../datenbeschaffung-referenzen/references/datenumfang.md`).
Bei Google Maps steckt das Impressum schon in der Kontaktanreicherung des Scrapes, `build_csv.py`
nimmt die Adresse von dort: Diese Stufe läuft nur noch für die Domains, bei denen beides leer blieb. ListM8 selbst reichert nichts per Impressum an: der Lauf findet
beim Anbieter (Apify, eigenes Konto) statt, das Ergebnis wird in die Roh-CSV gemerged und läuft
über `listen-qualitaet` in den Import.

Input: Liste von Domains/Websites (z. B. die `keine-email`-Teilmenge aus Weg C, oder die
Domain-CSV aus `process_serp.py`). Vorher gegen den Bestand abgleichen (`check_leads_exist` mit
`domains`, oder `dedup.py` gegen `export_leads(format="index")`) — Domains bekannter Leads kosten
sonst unnötig Geld; `do_not_contact` nie anreichern.

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
4. **Actor nach Zweck wählen.** Für die reine Adresse genügt der günstigste Actor, der sie
   liefert: Fallback A kostet rund ein Viertel des Primär-Actors, die Verifizierung folgt in
   `listen-qualitaet`. Vor dem ersten Einsatz mit fünf Domains prüfen, ob er die Adressen liefert.
   Den Primär-Actor nehmen, wenn Fallback A leer bleibt oder die Validierung im selben Lauf
   gewünscht ist. Fallback B ist der Ausweg, wenn beide ausfallen (Ein-Entwickler-Risiko).

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
  Geschäftsführer/Inhaber `firstName`/`lastName` (die Recherche bestätigt sie im Impressum).
  Weitere Entscheider, `register_number` und `vat_id` nicht übernehmen: kein Einstieg für die
  Mail, die Recherche findet sie bei Bedarf.
- Merge zurück in die Roh-CSV über die Root-Domain (`build_csv.py`-Format bleibt erhalten;
  `quelle` um `+impressum` ergänzen).

## Wann es sich lohnt

Entscheidungstabelle: `../datenbeschaffung-referenzen/references/datenumfang.md`, Abschnitt „Die
Kontaktlücke“. Kurz: Quelle ohne Kontaktdaten (Google-Suche, LinkedIn-Firmen,
Instagram-Websites) **und** ab etwa 50 Domains; `max_leads` knapp; großer Abo-Lauf mit knappem
Kontingent; oder der Nutzer will verifizierte Adressen vor dem Import. Rund 0,2 Cent je Domain
gegen 2 bis 3 Cent für Qualifizierung und Recherche eines Leads, der danach mangels Adresse
ausscheiden kann.

## Wann NICHT anreichern

- Kleine Liste oder Pilot auf einem 3.0.0-Server → direkt mit Website importieren, die Recherche
  sucht die Adresse.
- Nach einem Maps-Lauf mit Kontaktanreicherung bringt ein Impressum-Lauf wenig: Im Test vom
  11.10.2026 fanden drei Actors für 28 Domains ohne Adresse nur 1 bis 5. Nur bei großem Volumen
  anbieten. Bei Quellen ohne Kontaktdaten (LinkedIn-Firmen, Google-Suche) ist er dagegen der
  Normalfall: 29 von 40 LinkedIn-Firmen bekamen eine Adresse (haketa, 0,0017 $ je Domain).

- Lead hat schon eine E-Mail aus dem Scrape → kein Impressum-Lauf, auch nicht für
  Entscheider-Namen: die findet die Recherche der Plattform.
- Nicht-DACH-Domains → der Actor ist auf deutsche Impressumspflicht gebaut; für .com/.co.uk den
  `kontaktseiten-fallback` nehmen.
- < 20 Domains → Startgebühr frisst den Nutzen; Lücke akzeptieren oder sammeln bis zum Batch.
