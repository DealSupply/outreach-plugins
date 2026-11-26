---
name: enrichment-waterfall
description: Letzter Anreicherungs-Baustein des Datenbeschaffungs-Pakets — kostenpflichtiger Waterfall (FullEnrich/BetterContact, eigenes Konto beim Anbieter), der für wenige wertvolle Leads die persönliche Arbeits-E-Mail (selten die Mobilnummer) holt, wenn der Ansprechpartner bekannt ist (mit DealSupply aus der Recherche, ohne DealSupply aus dem Impressum), aber keine persönliche Adresse. Ausnahme, keine Lückenfüllung; nie direkt.
---

# Enrichment-Waterfall — die letzte, teuerste Stufe

Ein Waterfall-Tool fragt je Kontakt ein gutes Dutzend Datenanbieter nacheinander ab, bis ein Treffer
kommt. Der Kurs nennt dafür 80–98 % Abdeckung gegenüber 40–60 % bei einem einzelnen Anbieter.
Ergebnis: die persönliche Arbeits-E-Mail des Entscheiders (`vorname.nachname@`) statt der
Sammeladresse — und, deutlich teurer, seine Mobilnummer bzw. Durchwahl.

**Dieser Skill ist nie der erste Anreicherungsschritt.**

## Die Reihenfolge (Kurs-Regel, nicht verhandelbar)

Kurshandbuch Kap. 10: erst sammeln, dann das Impressum, erst danach der Premium-Weg. Je nach Modus:

**Mit DealSupply**

1. Leads sammeln (Weg-Skill), eine Adresse je Lead reicht (info@), ab MCP 4.0.0 auch nur
   die eigene Website →
2. Import und Recherche in der Plattform: Sie liest das Impressum, findet den Ansprechpartner und
   ersetzt die Rollen-Adresse durch die persönliche, wenn sie eine findet →
3. dieser Skill, **optional**, nur für qualifizierte, wertvolle Leads, bei denen die Recherche einen
   Namen, aber keine persönliche Adresse gefunden hat. Ab MCP 4.0.0 auch für wertvolle
   Leads, die ohne E-Mail importiert wurden und mangels Adresse ausgeschieden sind
   (`contactEmailState: not_found`), sofern die Recherche einen Namen fand.

Wer vor der Recherche anreichert, zahlt für Namen und Adressen, die die Plattform ohnehin findet,
und reichert auch Leads an, die die Qualifizierung danach aussortiert.

**Ohne DealSupply** (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`)

1. Leads sammeln (Weg-Skill) →
2. `impressum-enrichment` auf die ganze Liste: Geschäftsführer, Geschäfts-E-Mail, Telefon →
3. 20er-Stichprobe in `listen-qualitaet` bestanden →
4. dieser Skill, **optional**, nur für die wertvollsten Leads, bei denen das Impressum einen Namen
   geliefert hat, die Adresse aber eine Rollen-Adresse (info@) ist oder fehlt. Bei kleinen Firmen
   ist die Impressums-Adresse oft schon die des Inhabers; dann lohnt kein Lauf (Kap. 10).

Wer vor dem Impressum anreichert, zahlt für Namen, die das Impressum fast umsonst liefert.

## Werkzeug

FullEnrich oder BetterContact. FullEnrich lässt sich laut Kurs-Lektion per MCP anbinden: steht der
Connector, läuft die Anreicherung ohne Oberfläche. Sonst CSV hochladen, Ergebnis herunterladen.
Beide bündeln dieselbe Idee, die Auswahl entscheidet der Preis am Tag des Kaufs. Konto, Abrechnung
und Lauf liegen beim Anbieter, nicht in DealSupply; das Ergebnis kommt als CSV zurück und geht über
`listen-qualitaet` in den Import.

## Kostenlogik (ehrlich, und vor jedem Lauf nennen)

| Posten | Kosten |
|---|---|
| Gefundene E-Mail | **1 Credit** |
| Gefundene Mobilnummer | **10 Credits** |
| Credit-Preis (Stand der Kurs-Lektion) | ~55 $ je 1.000 Credits → E-Mail ≈ 5,5 Cent, Mobilnummer ≈ 55 Cent |
| Einstiegspaket | ab ~29 $ für rund 500 E-Mails |

Bezahlt wird nur der Treffer — kein Fund, kein Credit.

Preis ab laut Kurshandbuch (Kap. 10, Stand 19.08.2026): BetterContact ab rund 49 $ im Monat,
FullEnrich ab rund 29 $ im Monat, beide 1 Credit je E-Mail und 10 Credits je Mobilnummer. Bei
2.000 Leads im Monat: nur E-Mails rund 2.000 Credits, etwa 104 $; mit Mobilnummern bis zu 22.000
Credits, 500 bis über 1.000 $.

Rechenbeispiel: 500 qualifizierte Leads nur mit E-Mail = 500 Credits. Dieselben 500 zusätzlich mit
Mobilnummer = 5.500 Credits, also gut das Zehnfache. Diese Preise sind ein Stand, kein Fakt: vor
dem Kauf auf der Tool-Seite nachsehen und mit dem aktuellen Preis rechnen.

## Wann es sich lohnt — und wann nicht

- **Nur geprüfte Zielkontakte.** Nie eine Rohliste durchjagen. Input sind Leads, die die
  Qualifizierung (ohne DealSupply: die 20er-Stichprobe) bestanden haben und je Zeile einen
  Personennamen und eine Domain tragen.
- **Ohne Personennamen kein Lauf.** Das Tool sucht die Adresse einer bestimmten Person. Leere
  Namensfelder kosten zwar keinen Credit, liefern aber auch nichts — den Namen liefert die
  Recherche bzw. ohne DealSupply das Impressum (`firstName`/`lastName` oder `inhaber`).
- **Budget knapp oder Angebot noch nicht validiert:** Masse über die Recherche der Plattform bzw.
  ohne DealSupply über das Impressum abwickeln (Kap. 10), Waterfall nur für die 50–100 Top-Prospects, und dort nur E-Mails.
- **Angebot validiert, hoher Deckungsbeitrag, Engpass ist der Entscheiderzugang:** E-Mails für die
  ganze qualifizierte Liste sind vertretbar; Mobilnummern bleiben trotzdem der Spitze vorbehalten.
- **Mobilnummern** sind die eine Entscheidung, die einzeln begründet wird: rund 55 Cent für einen
  Kontakt. Standard ist nein — Ausnahme ist ein bereits qualifizierter Lead, den man über E-Mail
  und Zentrale nachweislich nicht erreicht.

Budget-Variante ohne gebündeltes Tool: der **manuelle Waterfall** — dieselbe Liste nacheinander
durch mehrere Einzelanbieter schicken, zwischen den Runden die Treffer abziehen. Reihenfolge laut
Kurshandbuch Kap. 10: Hunter (Domain-Suche mit Filter auf Entscheider), dann Apollo (Seniorität
Owner, C-Level, Director), dann Findymail für den Rest; die Exporte über die Domain zusammenführen
und vor dem Versand prüfen. Je Treffer günstiger, aber jede Runde bedeutet Export, Filtern, Re-Upload, das
Zusammenführen ist fehleranfällig, es gibt kein Tracking, welcher Anbieter geliefert hat, und
Mobilnummern kommen praktisch keine heraus. Nur bei kleinen Mengen und knappem Budget wählen.

## Ablauf

1. **Lücke bestimmen.** Mit DealSupply aus der Kampagne die qualifizierten Leads ziehen, bei denen
   die Recherche einen Ansprechpartner gefunden hat, die Versandadresse aber noch eine
   Rollen-Adresse ist, **und** die im ICP oben stehen. Ohne DealSupply dieselbe Auswahl aus der
   eigenen CSV: Zeilen mit Name aus dem Impressum und Rollen-Adresse (`hinweis` enthält
   `rollen-adresse`). Anzahl nennen — sie ist die Rechengrundlage.
2. **Kalkulieren und freigeben lassen.** n × 1 Credit für E-Mails, dazu nur bei ausdrücklichem
   Wunsch m × 10 Credits für Mobilnummern; in Dollar umrechnen, Deckel nennen. Ohne Freigabe des
   Nutzers kein Lauf (Kostenfreigabe im Master).
3. **Input bauen.** Je Zeile Vorname, Nachname, Firma und Domain — mehr braucht das Tool nicht.
   Steht der Name nur in `inhaber`, ihn nur übernehmen, wenn er eindeutig aus Vor- und Nachname
   besteht (dieselbe Regel wie in `instantly_csv.py`), sonst die Zeile weglassen.
4. **Lauf fahren** mit ausschließlich „Work Email", solange Mobilnummern nicht freigegeben sind.
5. **Ergebnis mergen.** Die persönliche Adresse ersetzt die Rollen-Adresse, die alte bleibt in der
   Zusatzspalte `email_rollen` stehen (die info@ zusätzlich anzuschreiben erhöht laut Kurs die
   Kontaktchance). `quelle` um `+waterfall` ergänzen, `hinweis` um `persoenliche-adresse`, und die
   Provider-Angabe je Treffer als Zusatzspalte mitführen — sie macht den Lauf nachvollziehbar.
6. **Zurück an `listen-qualitaet`** (Qualitätsstufe, Import per Oberfläche oder `import_leads`,
   ohne DealSupply die Datei für Instantly). Auch dieser Baustein übergibt nichts selbst. Neue
   Adressen laufen durch die Verifizierung, sofern das Tool keinen eigenen Zustellbarkeits-Status
   mitliefert. Nur mit DealSupply: Bereits importierte Leads nicht neu importieren (ein Re-Import überschreibt keine Kernfelder), sondern die gefundene Adresse am Lead ergänzen: per `write_lead_details(bestEmail=…)` oder in der App. Bei einem Lead ohne E-Mail wird sie dabei auch seine Identität, und die Sperre `no_contact_email` fällt weg; meldet die Antwort `address_conflict`, gehört die Adresse schon einem anderen Lead. Vorher `check_leads_exist` mit den neuen Adressen.

## Bekannte Fallen

- **Ganze Rohlisten durchjagen** — der teuerste Fehler dieses Wegs. Erst qualifizieren, dann anreichern.
- **Mobilnummern in Masse:** zehnfacher Preis für einen Kanal, den die wenigsten Kampagnen nutzen.
- **Doppelt anreichern:** Leads, die schon eine persönliche Adresse haben, vor dem Upload herausfiltern.
- **Preise aus dieser Datei als gesetzt behandeln.** Sie sind der Stand der Kurs-Lektion; die
  Kalkulation gegenüber dem Nutzer läuft immer mit dem tagesaktuellen Preis.
