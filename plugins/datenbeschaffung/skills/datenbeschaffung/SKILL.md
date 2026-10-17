---
name: datenbeschaffung
description: Dieser Skill wird bei „Datenbeschaffung“, „Leads beschaffen“, „Leadliste aufbauen“, „Leads scrapen“, „Liste bauen“ oder „wo finde ich Leads“ verwendet. Einziger Einstieg des Datenbeschaffungs-Pakets. Führt über ICP, Bestandsabgleich, Kostenfreigabe und den manuellen Weg (Apify oder Outscraper mit eigenem Konto, Bereinigung, CSV) zum Import in ListM8. weg-* nicht direkt starten.
---

# Datenbeschaffung mit ListM8

Vom bestätigten Zielkundenprofil zur geprüften Lead-Liste in ListM8 führen. ListM8 selbst scrapt
nicht: Der Kunde nutzt Apify (bzw. Outscraper) mit **eigenem Konto und eigenem Token außerhalb von
ListM8**, scrapt dort, bereinigt die Ergebnisse, exportiert CSV oder JSON und lädt sie in ListM8
hoch (Oberfläche oder MCP-Tool `import_leads`). Kosten fallen beim Anbieter an, nicht in ListM8.

## Leitsätze

1. **Trichter-Prinzip.** Beschaffung liefert Kandidaten, keine garantierten Wunschkunden. Die
   fachliche Qualifizierung und der spätere Review bleiben eigene Schritte.
2. **Nur beschaffen, was die Plattform nicht selbst findet.** Die Recherche liest Website und
   Impressum, findet den Ansprechpartner und dessen persönliche Adresse. Die Beschaffung liefert
   die Liste, je Lead eine Adresse (info@ reicht) **oder** die eigene Website (ab ListM8 MCP
   3.0.0: fehlt die Adresse, sucht die Recherche sie; ein Profil-Link wie Instagram oder Linktree
   reicht nicht) und das, was nur auf der Quelle steht: Google-Bewertung und Rezensionen,
   Follower, Plattform-Bewertung, Shop-Technologie. Details je Quelle:
   `../datenbeschaffung-referenzen/references/datenumfang.md`.
3. **Kosten vorab bestätigen lassen.** Vor jedem kostenpflichtigen Lauf beim Anbieter die erwarteten
   Kosten nennen, einen harten Deckel setzen und die ausdrückliche Freigabe des Nutzers einholen.
   Gilt auch für Piloten und Wiederholungen.
4. **Pilot vor Skalierung.** Mit einer Stadt und etwa 50 Treffern beginnen. Ab rund 70 bis 80 %
   ICP-Fit hochskalieren; darunter Query oder Filter schärfen.
5. **Kontaktstatus respektieren.** `do_not_contact` niemals überschreiben oder umgehen. Auch andere
   kontaktierte Bestandsleads nicht ungeprüft erneut anschreiben. Ein Listenmitglied ist keine
   Versandfreigabe.
6. **Deutsch mit korrekten Umlauten.** Keine Gedankenstriche in Kunden-Copy verwenden.
7. **Token bleiben beim Kunden.** Apify- oder Outscraper-Token nicht im Chat abfragen, ausgeben oder
   an einen anderen Dienst senden.

## Phase 0: Voraussetzungen prüfen

Erstes Mal oder Zweifel am Zugang? Zuerst `datenbeschaffung-setup` ausführen (prüft
Outreach-Verbindung, Apify-Zugang und optional Outscraper, ohne Kosten). Sonst kurz:

- **ListM8-MCP verbunden?** `ping` aufrufen. Mit MCP sind Bestandsabgleich und direkter Import
  möglich; ohne MCP am Ende CSV-Übergabe über die Oberfläche und den fehlenden Bestandsabgleich
  ausdrücklich melden. Fehlen die Tools, zuerst Verbindung und Berechtigungen klären.
- **Server-Version merken:** `ping.version` ab `3.0.0` heißt Übergabemodus `kontakt` (E-Mail oder
  eigene Website je Lead), darunter oder ohne Version `email` (jede Zeile braucht eine Adresse).
  Den Modus an `listen-qualitaet` weitergeben (`build_csv.py --uebergabe …`).
- **Scraping-Zugang:** erst nach der Wahl des Wegs (Phase 2) prüfen und nur, wenn der Weg ihn
  braucht. Fast alle Wege laufen über ein eigenes Apify-Konto samt Token (Details:
  `../datenbeschaffung-referenzen/references/setup.md`); Apollo mit eigenem Zugang und StoreLeads
  brauchen ihn nicht. Fehlt er, Setup durchgehen, nicht improvisieren.
- Scopes: Lesen (`check_leads_exist`, `export_leads`, `list_lists`, `get_list`, `search_leads`,
  `get_job_status`) braucht `leads:read`; Importieren, Listen anlegen/löschen und Zuordnen braucht
  `leads:write`.

Signaturen und Felder der ListM8-Tools stehen in
`../datenbeschaffung-referenzen/references/listm8-mcp.md`.

## Phase 1: ICP und Anti-ICP bestätigen

`../datenbeschaffung-referenzen/references/icp.md` lesen. Ergebnis als einen Satz mit Ausschlüssen
bestätigen lassen, bevor gescrapt wird:

> „[Rolle] in [Branche] mit [Größe] in [Region], erkennbar an [Trigger]. Nicht: [Anti-ICP].“

Bei unklarer Zielgruppe die 10-Wunschkunden-Frage aus der Referenz verwenden. Was die Liste über
den ICP hinaus versandfähig macht (Quellen außerhalb der Weg-Skills, Datenqualität, Sperrliste,
Volumenplanung), steht in `../datenbeschaffung-referenzen/references/listen-und-icp.md`.

## Phase 2: Weg auswählen

Die Kernfrage: **Wo trifft man diese Zielgruppe am wahrscheinlichsten?** Dem Nutzer die Wahl mit
einem Satz Begründung vorlegen, nicht den ganzen Baum erklären.

| Zielgruppe | Weg-Skill |
|---|---|
| Lokale Betriebe, Handwerk, Praxen, Gastro, auch Agenturen und Kanzleien mit Google-Maps-Eintrag | `weg-c-local-maps` (bringt Bewertung und Rezensionen mit, deshalb erste Wahl, wo ein Maps-Eintrag üblich ist) |
| B2B-Firmen ohne typischen Maps-Eintrag (Beratungen, IT-Dienstleister, Web-präsent) | `weg-a-b2b-google` |
| Software- und SaaS-Firmen, auch „alle SaaS in DACH“ | `weg-f-saas` (OMR Reviews und Startbase kostenlos, dazu LinkedIn-Firmen; keine Quelle allein findet mehr als etwa ein Viertel) |
| Industrie, Hersteller, Maschinenbau | zuerst `weg-c-local-maps` mit deutschem Branchenwort und Bundesland (Test: 85 % passend, 95 % mit Adresse); trägt Maps nicht, LinkedIn-Firmensuche plus `impressum-enrichment` oder `weg-a-apollo` (Datenbank) |
| E-Commerce, Onlineshops | `weg-b-ecom-google`; Beratung ohne Scrape: `weg-b-storeleads` |
| Coaches und Personal Brands | `weg-d-coaches-google`, `weg-d-coaches-linkedin`, `weg-d-instagram-google`, `weg-d-instagram-hashtag` |
| Plattform-Verkäufer (Amazon, Etsy, eBay) | `weg-e-plattform` |
| Sehr große Volumina (>10.000, Laufzeit egal) | `outscraper-bulk`, nie als Erstes anbieten (Jobs dauern 12 bis 24 h) |

Passt kein Weg, **Recherchemodus:** Apify-Store durchsuchen, Kandidaten nach den Kriterien in
`../datenbeschaffung-referenzen/references/apify-actors.md` bewerten, Mini-Pilot mit hartem Deckel
(höchstens 0,50 $) fahren, Ergebnis vorlegen und den Fund mit Datum in `apify-actors.md`
eintragen. Findet Apify nichts, Outscraper prüfen (Laufzeitwarnung). Auch dann leer: zurück zur
10-Wunschkunden-Frage.

## Phase 2b: Datenumfang festlegen

`../datenbeschaffung-referenzen/references/datenumfang.md` lesen und dem Nutzer in einem Satz sagen,
was dieser Weg mitbringt und was bewusst nicht beschafft wird, z. B.: „Wir holen Firma, Website,
eine Adresse, Google-Bewertung und die neuesten Rezensionen. Ansprechpartner und persönliche
Adresse sucht danach die Recherche der Plattform.“

- Was die Quelle im Preis oder für einen kleinen Aufschlag mitliefert und einen Einstieg trägt,
  kommt mit (bei Google Maps immer Bewertung und Rezensionen).
- Entscheider-Namen, persönliche Adressen, Register- und Mobilnummern werden nicht beschafft.
  Wünscht der Nutzer sie trotzdem, den Grund nennen (die Recherche findet und prüft sie) und erst
  nach ausdrücklichem Ja einen Anreicherungs-Lauf planen.
- Der Weg-Skill schreibt die Spalten über `build_csv.py`; nur Rohfelder mit Einstieg zusätzlich
  per `--keep`.
- **Kontaktlücke** (Leads mit eigener Website, aber ohne Adresse): ab ListM8 3.0.0 entscheidet der
  Nutzer, ob vorab angereichert wird oder die Recherche sucht. Entscheidungstabelle in
  `datenumfang.md`, Abschnitt „Die Kontaktlücke“. Dem Nutzer sinngemäß sagen: „N Leads haben eine
  eigene Website, aber keine Adresse. Ich kann sie so importieren, dann sucht die Recherche in
  ListM8 die Kontaktadresse; findet sie keine, scheidet der Lead aus und bekommt keine Mail. Bis
  dahin kostet er im Server-Lauf etwa 2 bis 3 Cent bzw. Abo-Kontingent und einen Platz im
  Lead-Kontingent. Vorab das Impressum über dein Apify-Konto auszulesen kostet rund 0,2 Cent je
  Domain, lohnt ab etwa 50 Domains und liefert geprüfte Adressen vor dem Import. Vorab anreichern
  oder direkt importieren?“

## Phase 3: Vorab-Abgleich (nur mit MCP)

VOR dem ersten kostenpflichtigen Lauf den Bestand ziehen und bekannte Domains in die
Query-Ausschlüsse geben: `export_leads(format="index")` bzw. `check_leads_exist`, Ablauf in
`../datenbeschaffung-referenzen/references/outreach-uebergabe.md`, Schritt 0. Bekannte Leads sollen
gar nicht erst Geld kosten. `list_lists` zeigt außerdem, was bereits gescrapt und importiert wurde
(Herkunft steht in `source` der Liste).

## Phase 4: Kosten nennen, Freigabe einholen, Weg-Skill ausführen

1. Erwartete Kosten aus `../datenbeschaffung-referenzen/references/kosten.md` kalkulieren und mit
   Actor-Preis (aktuell im Apify-Store prüfen) nennen: „Das kostet etwa X $ beim Anbieter, harter
   Deckel Y $. Ok?“ Die Abrechnung läuft über das eigene Konto des Kunden.
2. Ausdrückliche Freigabe abwarten. Ohne Freigabe kein kostenpflichtiger Lauf. Die Schätzung ist
   keine Preisgarantie; den Deckel nie still erhöhen.
3. Den gewählten Weg-Skill laden und fahren. Er endet IMMER mit einer Roh-CSV im Format aus
   `../datenbeschaffung-referenzen/references/csv-spalten.md`, nie mit einer Übergabe und nie mit
   einem eigenen Qualitätsurteil. Zugriffsschicht (Apify-MCP, REST, CLI):
   `../datenbeschaffung-referenzen/references/zugriff.md`.
4. Bei Leads ohne Adresse **optional** `impressum-enrichment` (DACH) bzw. `kontaktseiten-fallback`
   nur für die Adresse nutzen, nach der Entscheidung aus Phase 2b und mit Kostenfreigabe (auf
   Servern unter 3.0.0 ist das der einzige Weg, sie zu importieren). `enrichment-waterfall` ist
   keine Lückenfüllung, sondern eine Ausnahme für wenige wertvolle Leads nach der Recherche
   (siehe dort).

## Phase 5: Pflicht-Endstation

`listen-qualitaet` laden und vollständig durchlaufen: Format prüfen, gegen den Bestand abgleichen,
E-Mails verifizieren, 20er-Stichprobe, Import in ListM8. Kein Lauf endet mit einer Roh-CSV.

Danach auf ausdrücklichen Verarbeitungsauftrag die Liste einer bestätigten Kampagne zuordnen
(`add_leads_to_campaign`) und über den Outreach-Workflow `start_lead_run` für `qualification`,
`research` und `email` verwenden. Vor dem Zuordnen ist der Agenten-Check aus `outreach-campaign`,
Phase 4, Pflicht: Wunschkunde, Angebot, Passt-Kriterien, Ausschlusskriterien und Hinweise sowie die
Recherche- und E-Mail-Anweisung müssen für diese Zielgruppe gesetzt sein. Ist die Kampagne neu,
gehört das schon in ihr Setup, bevor gescrapt wird. Das ist ein separater Lauf mit eigenem Budget.
Keine erfundene `list_id` an `start_lead_run` übergeben und nicht automatisch alle Kampagnenleads
auswählen. Beschaffung und Import allein starten keine Qualifizierung und versenden keine E-Mails.

Bei der Übergabe eine Recherche-Stufe für die Kampagne empfehlen (Tabelle in `datenumfang.md`):
lokale Betriebe mit Website und Rezensionstexten kommen meist mit `basis` aus, das senkt die
Recherchekosten deutlich; mit vielen Leads ohne Adresse `smart` (eine gezielte Impressum-Suche,
wenn die Website keine Adresse zeigt). Die Einstellung ändert der Nutzer in der Kampagne
(`outreach-campaign`).

## Berichtsform

Nach jedem Lauf ein kompakter Block: Weg, Query und Filter, Pilot-Trefferquote, Anteil mit Bewertung,
Rezensionstext bzw. Plattform-Einstieg (aus dem Bericht von `build_csv.py`), Stückzahlen je Stufe
(roh, nach Dedup, nach Verifizierung, übergeben, davon ohne E-Mail mit Website, verworfen je Grund),
reale Kosten beim Anbieter und was beim nächsten
Lauf anders gemacht würde. Die Herkunft steht dauerhaft an der Liste in ListM8 (`source` bei
`create_list`).
