---
name: listen-qualitaet
description: Dieser Skill wird nach jedem Datenbeschaffungs-Lauf oder bei „Liste prüfen“, „Liste bereinigen“, „Leads qualitätssichern“ und „Liste importieren“ verwendet. Macht aus der Roh-CSV eines manuellen Scrapes (Apify oder Outscraper) eine bereinigte, gegen den Bestand abgeglichene und rückverfolgbare Liste und importiert sie in ListM8.
---

# Listen-Qualität: die Pflicht-Endstation

Nimmt die Roh-CSV eines Weg-Skills (Format: `../datenbeschaffung-referenzen/references/csv-spalten.md`) und macht daraus
eine übergebene, rückverfolgbare Liste. Kein Weg endet ohne diesen Skill.

Trichter-Prinzip beachten: Diese Stufe sortiert MECHANISCH (Duplikate, Sperren, kaputte Daten) und
prüft per Stichprobe. Sie beurteilt NICHT die inhaltliche Passung einzelner Leads: das macht die
Qualifizierung in der App, und die arbeitet bewusst offen.

**Vorprüfungsmodus vor `enrichment-waterfall`:** Nur Schritte 1, 2 und 4 auf der noch nicht
importierten Datei durchführen. Zeilen ohne E-Mail für die gezielte Anreicherung separat
behalten. Schritt 3 erst nach der Adressergänzung und Schritt 5 ausschließlich bei der finalen
Übergabe ausführen. Danach neue Adressen gegen den Bestand prüfen und nur bisher ungeprüfte
Adressen verifizieren. Dieser Modus ist keine abgeschlossene Übergabe.

## Schritt 1: Format & Datenqualität

`build_csv.py` hat das meiste erledigt; hier nur verifizieren:

- Header exakt wie `csv-spalten.md`, UTF-8, korrekte Umlaute
- `quelle`-Spalte gefüllt (Actor + Datum): ohne Herkunft keine Übergabe
- Einstiegsdaten prüfen (`../datenbeschaffung-referenzen/references/datenumfang.md`): Bei einer
  Google-Maps-Liste müssen `rating`, `reviews_count` und `google_rezensionstexte` als Spalten da
  sein. Fehlen sie ganz, wurden sie beim Bauen verloren: CSV mit `build_csv.py` neu bauen, nicht
  ohne sie importieren. Anteil mit Rezensionstext berichten. Bei LinkedIn, Instagram,
  Verkaufsplattformen und StoreLeads entsprechend die Plattformspalten.
- Auffälligkeiten aus `hinweis` zusammenfassen: Anteil `rollen-adresse` (info@ ist ok, die
  Recherche sucht die persönliche Adresse; berichten), Anteil `keine-website` (die bekommen zwangsläufig den schwächsten
  Personalisierungs-Anker: bei > 30 % dem Nutzer anbieten, sie in eine eigene Datei abzuspalten)

## Schritt 2: Dedup + Bestand-Abgleich

MIT MCP nach `../datenbeschaffung-referenzen/references/outreach-uebergabe.md`, Schritt 0,
sofern im Master (Phase 3) noch nicht geschehen:

```
export_leads(format="index")  →  bestand-index.json
python3 ../datenbeschaffung-referenzen/scripts/dedup.py --index bestand-index.json --in roh.csv --out neu.csv
```

Index, Prüfung und Import im selben Workspace (`listm8-mcp.md`, Abschnitt „Workspace“).

Der Report nennt: behalten / schon im Bestand / **do_not_contact entfernt** (namentlich, die werden
NIE angeschrieben) / Domain-Warnungen / ohne E-Mail behalten. OHNE MCP entfällt dieser Schritt.
Duplikate innerhalb der Datei hat `build_csv.py` bereits entfernt; im Bericht ausdrücklich sagen,
dass der Bestand-Abgleich fehlte.

**E-Mail-Gate:** Zeilen, die nach der Anreicherung (Impressum-/Kontaktseiten-Stufe des Wegs)
immer noch keine E-Mail haben, jetzt in eine eigene Datei abspalten (`leads-…-ohne-email.csv`)
und die Zahl berichten: sie gehen NICHT in Verifizierung und Übergabe (der Import verlangt
eine gültige E-Mail pro Zeile).

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
| `bad` | verwerfen |
| `risky` + `catch_all_domain` | behalten, wenn die Adresse zur eigenen Domain gehört (bei Maps-Adressen ein Drittel; die Domain nimmt alles an, info@ kommt an) |
| `risky` + `smtp_unreachable` | verwerfen |
| Hinweis `geratene-adresse` | nur `good` behalten (geratene Adressen: 23 von 51 unzustellbar) |

Im kostenlosen Apify-Plan kostet der Verifier 0,10 $ je Adresse statt 0,0006 $. Dort den Preis
nennen und nur die riskanten Gruppen prüfen: geratene Adressen, fremde Domains, Adressen aus
Datenbanken. Von den Maps-Adressen waren im Test nur 7 % unzustellbar.

## Schritt 4: 20er-Sample (die eine strenge Prüfung)

20 zufällige Leads von Hand prüfen: Website öffnen ist erlaubt und erwünscht. Je Lead eine Frage:
**Ist das plausibel ein potenzieller Kunde laut ICP-Satz?**

- **≥ 16 / 20 passen** → Liste ist gut. Weiter.
- **< 16 / 20** → NICHT nachpolieren, sondern die Ursache beheben: Query/Filter im Weg-Skill
  nachschärfen, den neuen Lauf schätzen und freigeben lassen. Erst dann wiederholen. Handpolieren einer
  schiefen Liste ist verlorene Zeit: Trichter-Prinzip heißt nicht „Müll durchwinken".

Dem Nutzer die Stichprobe zeigen (Firma, Website, passt/passt-nicht mit einem Halbsatz).

## Schritt 5: Übergabe

`../datenbeschaffung-referenzen/references/outreach-uebergabe.md` folgen:

- MIT MCP: `check_leads_exist` (Autoritäts-Check) → `create_list` (mit Herkunft + realen Kosten) →
  `import_leads(leads, list_id, attribute_mappings)` (Attributnamen genau wie in `outreach-uebergabe.md`, Schritt 3; die Google-Spalten erkennt der Import selbst) → `get_job_status` bis `completed` → Report-Zahlen
  berichten: `imported`, `linked_to_list` sowie die Anzahl der Einträge in den Listen `duplicates`
  und `do_not_contact_hits`.
  Signaturen: `listm8-mcp.md`. In eine Kampagne (`add_leads_to_campaign`) nur auf ausdrücklichen Wunsch.
- OHNE MCP: finale CSV liefern + Import-Anleitung, mit dem ehrlichen Hinweis, welche Prüfungen
  (Bestand, do_not_contact) erst der App-Import übernimmt.

## Schritt 6: Abschlussbericht

Eine Tabelle: roh → nach Dedup/Bestand → nach Verifizierung → Sample-Quote → übergeben.
Dazu reale Kosten des Gesamtlaufs und die eine Lernnotiz für den nächsten Lauf (z. B. „Kategorie X
war Beifang → in den Anti-ICP" oder „Portal Y in noise-domains.md ergänzt").
