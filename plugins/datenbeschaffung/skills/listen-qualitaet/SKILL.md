---
name: listen-qualitaet
description: Dieser Skill wird nach jedem Datenbeschaffungs-Lauf oder bei „Liste prüfen“, „Liste bereinigen“, „Leads qualitätssichern“, „Liste importieren“ und „Liste für Instantly“ verwendet. Macht aus der Roh-CSV eines manuellen Scrapes (Apify oder Outscraper) eine bereinigte, gegen den Bestand bzw. die eigene Sperrliste abgeglichene und rückverfolgbare Liste und importiert sie in DealSupply oder baut ohne DealSupply die Datei für Instantly.
---

# Listen-Qualität: die Pflicht-Endstation

Nimmt die Roh-CSV eines Weg-Skills (Format: `../datenbeschaffung-referenzen/references/csv-spalten.md`) und macht daraus
eine übergebene, rückverfolgbare Liste. Kein Weg endet ohne diesen Skill.

Trichter-Prinzip beachten: Diese Stufe sortiert MECHANISCH (Duplikate, Sperren, kaputte Daten) und
prüft per Stichprobe. Sie beurteilt NICHT die inhaltliche Passung einzelner Leads: das macht mit
DealSupply die Qualifizierung in der App, und die arbeitet bewusst offen. Ohne DealSupply gibt es
keine Qualifizierung; dann ist die 20er-Stichprobe die einzige inhaltliche Prüfung.

**Was Handarbeit bleibt** (dem Nutzer so sagen, nicht „passiert von selbst“): Die 20 Leads der
Stichprobe sieht der Nutzer selbst an, die KI legt sie ihm vor. Bestandskunden, die nie als Lead in
DealSupply standen, kennt nur sein CRM: Den Export zieht er selbst. Alles andere (Format,
Dubletten, Sperren, Prüfung der Adressen) macht die KI.

**Modus:** Der Master gibt mit oder ohne DealSupply weiter (`ping`, sonst Nachfrage). Ohne
DealSupply gelten die Abschnitte „Ohne DealSupply“ in den Schritten unten, und am Ende steht die
Datei für Instantly (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`).

**Übergabemodus:** Der Master merkt sich `ping.version`. Ab MCP 4.0.0 gilt `kontakt`
(E-Mail oder eigene Website je Zeile), darunter, ohne Version und immer ohne DealSupply `email`
(jede Zeile braucht eine Adresse). Fehlt die Angabe, hier selbst `ping` aufrufen.

**Vorprüfungsmodus vor `enrichment-waterfall`:** Nur Schritte 1, 2 und 4 auf der noch nicht
importierten Datei durchführen. Zeilen ohne E-Mail für die gezielte Anreicherung separat
behalten. Schritt 3 erst nach der Adressergänzung und Schritt 5 ausschließlich bei der finalen
Übergabe ausführen. Danach neue Adressen gegen den Bestand prüfen und nur bisher ungeprüfte
Adressen verifizieren. Dieser Modus ist keine abgeschlossene Übergabe.

## Schritt 1: Format & Datenqualität

`build_csv.py` hat das meiste erledigt; hier nur verifizieren:

- Header exakt wie `csv-spalten.md`, UTF-8, korrekte Umlaute
- `quelle`-Spalte gefüllt (Actor + Datum): ohne Herkunft keine Übergabe. **Aktualität:** Stammt
  die Liste oder ihr Rohscrape aus einer Zeit vor mehr als sechs Monaten, nicht übergeben, sondern
  frisch beschaffen oder mindestens alle Adressen neu prüfen (Kurshandbuch Kap. 2 und FAQ: Personen
  wechseln, Firmen schließen, Adressen verfallen)
- Einstiegsdaten prüfen (`../datenbeschaffung-referenzen/references/datenumfang.md`): Bei einer
  Google-Maps-Liste müssen `rating`, `reviews_count` und `google_rezensionstexte` als Spalten da
  sein. Fehlen sie ganz, wurden sie beim Bauen verloren: CSV mit `build_csv.py` neu bauen, nicht
  ohne sie importieren. Anteil mit Rezensionstext berichten. Bei LinkedIn, Instagram,
  Verkaufsplattformen und StoreLeads entsprechend die Plattformspalten.
- Auffälligkeiten aus `hinweis` zusammenfassen: Anteil `rollen-adresse` (info@ ist ok, mit
  DealSupply sucht die Recherche die persönliche Adresse; ohne DealSupply bleibt info@ die
  Versandadresse, bei kleinen Betrieben unter 20 bis 30 Mitarbeitern liest der Chef sie oft selbst,
  Kurshandbuch FAQ; berichten), Anteil `keine-website` (die bekommen zwangsläufig den schwächsten
  Personalisierungs-Anker: bei > 30 % dem Nutzer anbieten, sie in eine eigene Datei abzuspalten),
  Anteil `keine-email` (mit eigener Website sucht ab 4.0.0 die Recherche die Adresse; ohne
  DealSupply erst `impressum-enrichment`, sonst fallen sie weg) und `nur-plattform-url` (ohne
  E-Mail nicht importierbar)

## Schritt 2: Dedup + Bestand-Abgleich

MIT MCP nach `../datenbeschaffung-referenzen/references/outreach-uebergabe.md`, Schritt 0,
sofern im Master (Phase 3) noch nicht geschehen:

```
export_leads(format="index")  →  bestand-index.json
python3 ../datenbeschaffung-referenzen/scripts/dedup.py --index bestand-index.json --in roh.csv --out neu.csv
```

Index, Prüfung und Import im selben Workspace (`dealsupply-mcp.md`, Abschnitt „Workspace“).

Der Report nennt: behalten / schon im Bestand / **do_not_contact entfernt** (namentlich, die werden
NIE angeschrieben) / Domain-Warnungen / ohne E-Mail behalten. Zeilen ohne E-Mail, deren Website
schon ein Lead ohne E-Mail im Bestand trägt, entfernt `dedup.py` als Dublette. Mit DealSupply-Konto,
aber OHNE MCP entfällt dieser Schritt. Duplikate innerhalb der Datei hat `build_csv.py` bereits
entfernt; im Bericht ausdrücklich sagen, dass der Bestand-Abgleich fehlte.

**Ohne DealSupply:** Abgleich gegen die eigene Sperrliste statt gegen den Bestand, sofern das im
Master (Phase 3) noch nicht geschehen ist. Den CRM-Export (Kunden, Ex-Kunden, Blacklist,
Abmeldungen, optional Wettbewerber) liefert der Nutzer:

```
python3 ../datenbeschaffung-referenzen/scripts/sperrliste.py --crm kunden.csv --blocklist instantly-blocklist.csv \
  --in roh.csv --out neu.csv
```

Der Report nennt die gesperrten Leads; sie werden NIE angeschrieben. Die Blocklist-Datei geht mit
der Liste an den Nutzer (Schritt 5). Hat der Nutzer kein CRM und keine Bestandskunden, ausdrücklich
festhalten, dass ohne Sperrliste übergeben wird.

**Kontakt-Gate** (ab MCP 4.0.0): Zeilen mit E-Mail **oder** eigener Website gehen in die
Übergabe. Zeilen nur mit Plattform-Link oder ganz ohne Kontaktmerkmal in eine eigene Datei
abspalten und die Zahl je Grund berichten:

```
python3 ../datenbeschaffung-referenzen/scripts/build_csv.py --in neu.csv --out leads-….csv \
  --quelle "<wie roh>" --uebergabe kontakt --verworfen leads-…-ohne-kontakt.csv
```

Auf älteren Servern und **immer ohne DealSupply** (Modus `email`) gilt das **E-Mail-Gate**: Zeilen,
die nach der Anreicherung immer noch keine E-Mail haben, in `leads-…-ohne-email.csv` abspalten
(`--uebergabe email`); sie gehen NICHT in Verifizierung und Übergabe.

## Schritt 3: Verifizierung

Verifizierung ist ein eigener Schritt mit dem gepinnten E-Mail-Verifier aus
`../datenbeschaffung-referenzen/references/apify-actors.md` (Actor-ID und Preis NUR von dort,
nie aus dem Gedächtnis): **außer** der Weg hat schon validiert (Impressum-Primär liefert
`email_status` mit; dann nur UNDELIVERABLE aussortieren). Kosten vorher nennen (Freigabe
im Master, Zahlen aus `kosten.md`; Abrechnung beim Anbieter). Ergebnis: nur zustellbare Adressen bleiben; Bounce-Ziel < 3 %.

So wird das Ergebnis des Verifiers gelesen (Test vom 11.10.2026, 200 Adressen):

| `status` / `reason` | Entscheidung |
|---|---|
| `good` | behalten |
| `bad` | Adresse verwerfen. Ab MCP 4.0.0: Zeile mit eigener Website ohne Adresse behalten (Hinweis `adresse-verworfen`, die Recherche sucht neu), ohne Website verwerfen. Darunter und ohne DealSupply: Zeile verwerfen |
| `risky` + `catch_all_domain` | behalten, wenn die Adresse zur eigenen Domain gehört (bei Maps-Adressen ein Drittel; die Domain nimmt alles an, info@ kommt an) |
| `risky` + `smtp_unreachable` | wie `bad` |
| Hinweis `geratene-adresse` | nur `good` behalten (geratene Adressen: 23 von 51 unzustellbar) |

Verifiziert werden nur importierte Adressen. Adressen, die erst die Recherche der Plattform
findet, laufen nicht durch den Verifier: vor dem Versand die Verifizierung in Instantly einschalten
oder diese Adressen nachträglich prüfen (`export_leads`, Spalte `email`).

**Ohne DealSupply** gibt es eine zweite Möglichkeit: die Prüfung beim Import in Instantly
(„Verify leads“, laut Instantly 0,25 Credits je Lead, mit Catch-all-Erkennung; der alte Kurs
empfahl sie, Kap. 9). Eine von beiden wählen, nicht beide bezahlen: Wer Instantly-Credits hat,
lässt dort prüfen und überspringt den Verifier; sonst den Verifier hier. Adressen aus dem
`kontaktseiten-fallback` sind ungeprüft und müssen durch eine der beiden Prüfungen.

Im kostenlosen Apify-Plan kostet der Verifier 0,10 $ je Adresse statt 0,0006 $ (200 Adressen 20 $
statt 0,12 $). Dort den Preis nennen und nur die riskanten Gruppen prüfen: geratene Adressen,
fremde Domains, Adressen aus Datenbanken, Funde von Kontaktseiten. Von den Maps-Adressen waren im
Test nur 7 % unzustellbar. Für laufende Beschaffung einen bezahlten Apify-Plan empfehlen
(`datenbeschaffung-setup`).

## Schritt 4: 20er-Sample (die eine strenge Prüfung)

20 zufällige Leads von Hand prüfen: Website öffnen ist erlaubt und erwünscht. Je Lead eine Frage:
**Ist das plausibel ein potenzieller Kunde laut ICP-Satz?**

- **≥ 16 / 20 passen** → Liste ist gut. Weiter.
- **< 16 / 20** → NICHT nachpolieren, sondern die Ursache beheben: Query/Filter im Weg-Skill
  nachschärfen, den neuen Lauf schätzen und freigeben lassen. Erst dann wiederholen. Handpolieren einer
  schiefen Liste ist verlorene Zeit: Trichter-Prinzip heißt nicht „Müll durchwinken".

Dem Nutzer die Stichprobe zeigen (Firma, Website, passt/passt-nicht mit einem Halbsatz). Das
Urteil gehört dem Nutzer: Er öffnet die Websites selbst, die KI liefert die Vorlage. Dabei auch
fragen, welcher Personalisierungs-Hebel bei diesen Leads trägt
(`../datenbeschaffung-referenzen/references/personalisierung.md`), und das notieren.

## Schritt 5: Übergabe

Mit DealSupply `../datenbeschaffung-referenzen/references/outreach-uebergabe.md` folgen, ohne
DealSupply den letzten Punkt:

- MIT MCP: `check_leads_exist` (Autoritäts-Check) → Platzprüfung wie in `datenbeschaffung`, Phase 3,
  wiederholen, wenn die bereinigte Liste mehr neue Adressen hat als geplant (`get_credit_balance`,
  `account.free_slots`; passt sie nicht, den Nutzer fragen, nie ungefragt `allow_partial=true`) → `create_list` (mit Herkunft + realen Kosten) →
  `import_leads(leads, list_id, attribute_mappings)` (Attributnamen genau wie in `outreach-uebergabe.md`, Schritt 3; die Google-Spalten erkennt der Import selbst) → `get_job_status` bis `completed` → Report-Zahlen
  berichten: `imported`, `linked_to_list`, abgelehnte Zeilen (`rejected_total` aus der Antwort,
  `rejected_by_code` aus dem Job) sowie die Anzahl der Einträge in den Listen `duplicates` und
  `do_not_contact_hits`. Abgelehnte Zeilen nicht wiederholen, sondern mit Grund nennen.
  Signaturen: `dealsupply-mcp.md`. In eine Kampagne (`add_leads_to_campaign`) nur auf ausdrücklichen Wunsch.
- Mit DealSupply-Konto, aber OHNE MCP: finale CSV liefern + Import-Anleitung für die App, mit dem
  ehrlichen Hinweis, welche Prüfungen (Bestand, do_not_contact) erst der App-Import übernimmt.
- **OHNE DealSupply:** aus der geprüften Übergabe-CSV der Schritte 2 und 3 (hier
  `leads-final.csv`) die Datei für Instantly bauen und mit der Blocklist übergeben:

  ```
  python3 ../datenbeschaffung-referenzen/scripts/instantly_csv.py --in leads-final.csv \
    --out instantly-<nische>-<datum>.csv
  ```

  Dem Nutzer die Anleitung aus `../datenbeschaffung-referenzen/references/ohne-dealsupply.md`
  geben (Abschnitt „So lädst du sie in Instantly“): erst die Blocklist importieren, dann die Leads
  hochladen, Zuordnung nach der Zeile „Zuordnung beim Import“, Dubletten-Prüfung anlassen, „Verify
  leads“ nur, wenn in Schritt 3 nicht schon geprüft wurde. Die Zahl der Leads ohne Vorname nennen.
  Die eigene CSV (`leads-final.csv`, mit `quelle` und `hinweis`) bleibt beim Nutzer als Nachweis.

## Schritt 6: Abschlussbericht

Eine Tabelle: roh → nach Dedup/Bestand bzw. Sperrliste → nach Verifizierung → Sample-Quote →
übergeben (davon ohne E-Mail, mit Website; ohne DealSupply: davon mit Vorname) → abgelehnt je Grund.

Zum Einordnen die Kaskade aus dem Kurshandbuch (Kap. 9, Richtwerte): Rohliste 100 %, nach
Bestandskunden und Blacklist etwa 92 %, nach Prüfung der Adressen etwa 78 %, nach der Stichprobe
etwa 70 %, versandbereit etwa 55 %. Aus 5.500 Rohzeilen werden so rund 3.000 versandbereite Leads;
das ist normal. Für den nächsten Lauf die Rohmenge danach planen.

Dazu reale Kosten des Gesamtlaufs und die eine Lernnotiz für den nächsten Lauf (z. B. „Kategorie X
war Beifang → in den Anti-ICP" oder „Portal Y in noise-domains.md ergänzt").
