---
name: datenbeschaffung
description: Dieser Skill wird bei „Datenbeschaffung“, „Leads beschaffen“, „Leadliste aufbauen“, „Leads scrapen“, „Liste bauen“, „Liste für Instantly“ oder „wo finde ich Leads“ verwendet. Einziger Einstieg des Plugins datenbeschaffung. Standard ist DealSupply selbst: Mit verbundenem DealSupply führt er zuerst zu Leads finden, Personensuche und ähnlichen Firmen, ohne eigenes Apify-Konto. Externe Quellen (eigenes Apify- oder Outscraper-Konto, Bereinigung, CSV) nur als Ausnahme, wenn DealSupply die Zielgruppe nicht abdeckt oder der Pilot dort schlecht liefert, und für alle ohne DealSupply-Konto (Ende mit einer Datei für Instantly). weg-* nicht direkt starten.
---

# Datenbeschaffung: DealSupply zuerst, externe Quellen als Ausnahme

Vom bestätigten Zielkundenprofil zur geprüften Lead-Liste führen. Dieser Skill gehört zum eigenen
Plugin **„datenbeschaffung“** aus dem Marketplace `outreach-plugins`.

**Der Standardweg ist DealSupply selbst** (ab MCP 4.16.0, Skills im Plugin `outreach`): lokale
Betriebe über `outreach-leads-finden`, Entscheider nach Rolle über `outreach-personensuche`, mehr
Firmen wie die guten Leads über `outreach-aehnliche-firmen`. Dafür braucht der Nutzer kein eigenes
Apify-Konto und zahlt in Credits. Eine externe Quelle empfiehlt dieser Skill nur, wenn DealSupply
die Zielgruppe nicht abdeckt oder ein Pilot dort schlecht liefert (Weiche in Phase 0). Sonst zahlt
der Nutzer doppelt.

Der externe Weg läuft mit **eigenem Apify- (bzw. Outscraper-)Konto und eigenem Token**: scrapen,
bereinigen, übergeben.

- **Mit DealSupply-Konto:** Import in DealSupply (MCP-Tool `import_leads` oder Oberfläche).
- **Ohne DealSupply-Konto** (etwa aus einem Kurs): Das Plugin funktioniert auch dann. Es holt
  Adresse und Geschäftsführer selbst, gleicht gegen eine eigene Sperrliste ab und endet mit einer
  Datei für Instantly (`../datenbeschaffung-referenzen/references/ohne-dealsupply.md`).

Kosten des externen Wegs fallen beim Anbieter an, nicht in DealSupply.

## Leitsätze

1. **Trichter-Prinzip.** Beschaffung liefert Kandidaten, keine garantierten Wunschkunden. Die
   fachliche Qualifizierung und der spätere Review bleiben mit DealSupply eigene Schritte. Ohne
   DealSupply gibt es sie nicht: Dann sind Pilot und 20er-Stichprobe die einzigen Prüfungen, ob ein
   Lead passt, und der Anti-ICP gehört streng in Query und Filter.
2. **Mit DealSupply nur beschaffen, was die Plattform nicht selbst findet.** Die Recherche liest
   Website und Impressum, findet den Ansprechpartner und dessen persönliche Adresse. Die
   Beschaffung liefert die Liste, je Lead eine Adresse (info@ reicht) **oder** die eigene Website
   (ab MCP 4.0.0: fehlt die Adresse, sucht die Recherche sie; ein Profil-Link wie Instagram oder
   Linktree reicht nicht) und das, was nur auf der Quelle steht: Google-Bewertung und
   Rezensionen, Follower, Plattform-Bewertung, Shop-Technologie. Details je Quelle:
   `../datenbeschaffung-referenzen/references/datenumfang.md`. **Ohne DealSupply** gibt es keine
   Recherche: Jede Zeile braucht eine Adresse, und der Geschäftsführer kommt aus dem Impressum
   (`ohne-dealsupply.md`). Nie von „der Recherche der Plattform“ sprechen, wenn kein DealSupply da
   ist.
3. **Kosten vorab bestätigen lassen.** Vor jedem kostenpflichtigen Lauf beim Anbieter die erwarteten
   Kosten nennen, einen harten Deckel setzen und die ausdrückliche Freigabe des Nutzers einholen.
   Gilt auch für Piloten und Wiederholungen.
4. **Pilot vor Skalierung.** Mit einer Stadt und etwa 50 Treffern beginnen. Ab rund 70 bis 80 %
   ICP-Fit hochskalieren; darunter Query oder Filter schärfen.
5. **Kontaktstatus respektieren.** `do_not_contact` niemals überschreiben oder umgehen. Auch andere
   kontaktierte Bestandsleads nicht ungeprüft erneut anschreiben. Ein Listenmitglied ist keine
   Versandfreigabe. Ohne DealSupply übernimmt das die eigene Sperrliste (Kunden, Ex-Kunden,
   Abmeldungen, Beschwerden).
6. **Deutsch mit korrekten Umlauten.** Keine Gedankenstriche in Kunden-Copy verwenden.
7. **Token bleiben beim Kunden.** Apify- oder Outscraper-Token nicht im Chat abfragen, ausgeben oder
   an einen anderen Dienst senden.

## Phase 0: Weiche: DealSupply oder externe Quelle

Zuerst `ping` aufrufen und, wenn er antwortet, `get_credit_balance` lesen (nur lesend). Für die
Weiche reicht die Zielgruppe in einem Halbsatz („Elektriker in Stuttgart“, „Shopify-Shops für
Tierbedarf“). Den genauen ICP-Satz klärt danach der DealSupply-Skill bzw. beim externen Weg
Phase 1.

**1. DealSupply verbunden, Konto rechnet in Credits** (`billing_mode` nicht `byok`, ein aktiver
Plan): Erst klären, ob DealSupply die Zielgruppe selbst findet. Ist das so, dorthin führen und
diesen Skill hier beenden; der Nutzer braucht kein Apify.

| Zielgruppe | Zuerst in DealSupply | Extern nur, wenn |
|---|---|---|
| Lokale Betriebe mit Google-Maps-Eintrag in Deutschland, Österreich, Schweiz (Handwerk, Praxen, Gastro, Kanzleien, Agenturen, auch Industrie und Hersteller) | `outreach-leads-finden` | der Pilot dort schlecht liefert (siehe unten), mehr als 50 Gebiete in einer Suche nötig sind oder sehr große Mengen gewünscht sind (`outscraper-bulk`) |
| Entscheider nach Rolle in Firmen (Geschäftsführer, Marketingleitung, Vertrieb), auch B2B-Coaches und Berater mit Firma, auch in Software-Firmen | `outreach-personensuche` | die Probe der Suche zu wenig passende Personen zeigt; für eine möglichst vollständige Liste aller SaaS-Firmen einer Region `weg-f-saas` |
| Mehr Firmen wie die besten Kunden oder wie Leads, die geantwortet haben | `outreach-aehnliche-firmen` | dafür gibt es im Plugin keinen externen Weg; DealSupply findet ähnliche Firmen nur in Deutschland, Österreich, Schweiz |
| Onlineshops ohne Maps-Eintrag | nicht abgedeckt | extern: `weg-b-ecom-google`, `weg-b-storeleads` |
| B2C-Coaches und Personal Brands, vor allem auf Instagram | nicht abgedeckt | extern: Weg D (Tabelle in Phase 2) |
| Händler auf Amazon, Etsy, eBay | nicht abgedeckt | extern: `weg-e-plattform` |
| Ziele außerhalb von Deutschland, Österreich und der Schweiz | Leads finden und ähnliche Firmen nicht; ob die Personensuche Orte im Zielland kennt, mit `search_people_filter_values` prüfen (kostet nichts) | extern mit `ausserhalb-dach.md` |

**Schlecht geliefert** heißt: Das Angebot nennt deutlich weniger Betriebe als gebraucht, die
Probe der Personensuche zeigt überwiegend Unpassende, oder die 20er-Stichprobe der in DealSupply
gefundenen Leads liegt unter 16 von 20 und lässt sich mit anderen Branchen oder Filtern nicht
beheben. Dann sagen, was DealSupply geliefert hat, und den externen Weg mit Kosten vorschlagen.
Auch ein ausdrücklicher Wunsch des Nutzers nach einer eigenen Quelle zählt; dann einmal sagen,
dass DealSupply dieselbe Zielgruppe ohne eigenes Konto abdeckt.

**2. DealSupply verbunden, aber `billing_mode: byok`** (eigener KI-Schlüssel), ohne aktiven Plan
oder mit einem Server unter MCP 4.16.0: Leads finden, Personensuche und ähnliche Firmen gehen dort
nicht. Bei fehlendem Plan erst einen Plan wählen lassen; sonst den externen Weg nehmen, Import in
DealSupply.

**3. Kein DealSupply-MCP:** fragen, ob der Nutzer ein DealSupply-Konto hat. Mit Konto zuerst die
Verbindung einrichten (`datenbeschaffung-setup`), dann Weiche 1. Ohne Konto: Modus **ohne
DealSupply**, externer Weg, Ende mit einer Datei für Instantly.

Erst wenn der externe Weg feststeht, geht es hier weiter.

## Phase 0b: Voraussetzungen für den externen Weg

Erstes Mal oder Zweifel am Zugang? `datenbeschaffung-setup` ausführen (prüft Apify-Zugang samt
Preisstufe, sobald ein externer Weg gewählt ist, und optional Outscraper, ohne Kosten). Sonst kurz:

- **Modus nennen** (Tabelle in `../datenbeschaffung-referenzen/references/ohne-dealsupply.md`):
  mit DealSupply (Bestandsabgleich und Import; ohne Verbindung als CSV über die Oberfläche, dann
  den fehlenden Bestandsabgleich ausdrücklich melden) oder ohne DealSupply (Datei für Instantly).
  Den Modus in einem Satz nennen und an alle folgenden Skills weitergeben.
- **Workspace** (nur mit DealSupply): Abgleich, Liste und Import laufen im gewählten Workspace der App. Vor dem ersten
  Abgleich klären, welcher es ist (Regel: `../datenbeschaffung-referenzen/references/dealsupply-mcp.md`,
  Abschnitt „Workspace“).
- **Server-Version merken:** `ping.version` ab `4.0.0` heißt Übergabemodus `kontakt` (E-Mail oder
  eigene Website je Lead), darunter, ohne Version und **immer ohne DealSupply** `email` (jede Zeile
  braucht eine Adresse). Den Modus an `listen-qualitaet` weitergeben (`build_csv.py --uebergabe …`).
- **Scraping-Zugang:** erst nach der Wahl des Wegs (Phase 2) prüfen und nur, wenn der Weg ihn
  braucht. Fast alle Wege laufen über ein eigenes Apify-Konto samt Token (Details:
  `../datenbeschaffung-referenzen/references/setup.md`); Apollo mit eigenem Zugang und StoreLeads
  brauchen ihn nicht. Fehlt er, Setup durchgehen, nicht improvisieren. Im kostenlosen
  Apify-Plan kostet das Prüfen der Adressen ein Vielfaches (`kosten.md`, Preisfalle): Das vor dem
  ersten Lauf sagen.
- Scopes (nur mit DealSupply): Lesen (`check_leads_exist`, `export_leads`, `list_lists`, `get_list`, `search_leads`,
  `get_job_status`) braucht `leads:read`; Importieren, Listen anlegen/löschen und Zuordnen braucht
  `leads:write`.

Signaturen und Felder der DealSupply-Tools stehen in
`../datenbeschaffung-referenzen/references/dealsupply-mcp.md`.

## Phase 1: ICP und Anti-ICP bestätigen

`../datenbeschaffung-referenzen/references/icp.md` lesen. Ergebnis als einen Satz mit Ausschlüssen
bestätigen lassen, bevor gescrapt wird:

> „[Rolle] in [Branche] mit [Größe] in [Region], erkennbar an [Trigger]. Nicht: [Anti-ICP].“

Bei unklarer Zielgruppe die 10-Wunschkunden-Frage aus der Referenz verwenden. Was die Liste über
den ICP hinaus versandfähig macht (Quellen außerhalb der Weg-Skills, Datenqualität, Sperrliste,
Volumenplanung), steht in `../datenbeschaffung-referenzen/references/listen-und-icp.md`.

Liegt die Region außerhalb von Deutschland, Österreich und der Schweiz, vor der Wegwahl
`../datenbeschaffung-referenzen/references/ausserhalb-dach.md` lesen und dem Nutzer sagen, was dort
belegt ist und was nicht: Alle Messwerte des Plugins stammen aus DACH, ohne Impressumspflicht
kommen weniger Adressen.

## Phase 2: Externen Weg auswählen

Die Kernfrage: **Wo trifft man diese Zielgruppe am wahrscheinlichsten?** Dem Nutzer die Wahl mit
einem Satz Begründung vorlegen, nicht den ganzen Baum erklären. Mit DealSupply-Konto gilt die
Tabelle nur für Zielgruppen, die die Weiche in Phase 0 nach außen geschickt hat: Lokale Betriebe
und Entscheider in DACH laufen dann über DealSupply, die Zeilen dafür sind der Weg ohne
DealSupply-Konto oder nach einem schwachen Pilot.

| Zielgruppe | Weg-Skill |
|---|---|
| Lokale Betriebe, Handwerk, Praxen, Gastro, auch Agenturen und Kanzleien mit Google-Maps-Eintrag | `weg-c-local-maps` (bringt Bewertung und Rezensionen mit, deshalb erste Wahl, wo ein Maps-Eintrag üblich ist) |
| B2B-Firmen ohne typischen Maps-Eintrag (Beratungen, IT-Dienstleister, Web-präsent) | `weg-a-b2b-google` |
| Software- und SaaS-Firmen, auch „alle SaaS in DACH“ | `weg-f-saas` (OMR Reviews und Startbase kostenlos, dazu LinkedIn-Firmen; keine Quelle allein findet mehr als etwa ein Viertel) |
| Industrie, Hersteller, Maschinenbau | zuerst `weg-c-local-maps` mit deutschem Branchenwort und Bundesland (Test: 85 % passend, 95 % mit Adresse); trägt Maps nicht, LinkedIn-Firmensuche plus `impressum-enrichment` oder `weg-a-apollo` (Datenbank) |
| E-Commerce, Onlineshops | `weg-b-ecom-google`; Beratung ohne Scrape: `weg-b-storeleads` |
| Coaches und Personal Brands | `weg-d-coaches-google`, `weg-d-coaches-linkedin`, `weg-d-instagram-google`, `weg-d-instagram-hashtag` (welcher für wen: Tabelle unten) |
| Plattform-Verkäufer (Amazon, Etsy, eBay) | `weg-e-plattform` |
| Sehr große Volumina (>10.000, Laufzeit egal) | `outscraper-bulk`, nie als Erstes anbieten (Jobs dauern 12 bis 24 h) |

### Coaches: welcher der fünf Wege für wen

Aus dem Kurshandbuch, Kap. 7 (Kosten je 1.000 Leads Stand 19.08.2026, Richtwert; vor dem Lauf mit
`kosten.md` und dem Actor-Preis rechnen). Zuerst klären: B2B-Coach (tritt als Firma auf, Kunden sind
Unternehmen) oder B2C-Coach (Personenmarke, Kunden sind Privatpersonen)?

| Weg | Für | Quelle | Skill | Kosten je 1.000 Leads |
|---|---|---|---|---|
| Google | B2B-Coaches | Google und Impressum | `weg-d-coaches-google` (Segment B2B) | ca. 10 bis 15 $ |
| LinkedIn | B2B-Coaches | LinkedIn-Profile | `weg-d-coaches-linkedin` | ca. 5 bis 10 $ |
| Google-Website | B2C-Coaches mit eigener Website | Google und Impressum | `weg-d-coaches-google` (Segment B2C) | ca. 10 bis 15 $ |
| Google-Instagram | B2C-Coaches auf Instagram | Google mit `site:instagram.com` | `weg-d-instagram-google` | ca. 5 bis 8 $ |
| Instagram-Hashtag | B2C-Coaches, die posten, aber nirgends ranken | Instagram-Beiträge | `weg-d-instagram-hashtag` | ca. 3 bis 5 $ |

Die Wege finden kaum dieselben Coaches, weil jeder eine andere Quelle anzapft (Kap. 7). Wer mehr
Menge braucht, kombiniert deshalb die Wege seines Segments, statt einen Weg zu überdehnen, und
führt die Listen danach über die Domain zusammen (`build_csv.py` dedupliziert). Coaches nur auf
Instagram haben oft keine Website: Ohne Website und ohne Adresse sind sie für Cold Mail verloren.

Passt kein Weg, **Recherchemodus:** Apify-Store durchsuchen, Kandidaten nach den Kriterien in
`../datenbeschaffung-referenzen/references/apify-actors.md` bewerten, Mini-Pilot mit hartem Deckel
(höchstens 0,50 $) fahren, Ergebnis vorlegen und den Fund mit Datum in `apify-actors.md`
eintragen. Findet Apify nichts, Outscraper prüfen (Laufzeitwarnung). Auch dann leer: zurück zur
10-Wunschkunden-Frage.

## Phase 2b: Datenumfang festlegen

`../datenbeschaffung-referenzen/references/datenumfang.md` lesen und dem Nutzer in einem Satz sagen,
was dieser Weg mitbringt und was bewusst nicht beschafft wird, z. B. mit DealSupply: „Wir holen
Firma, Website, eine Adresse, Google-Bewertung und die neuesten Rezensionen. Ansprechpartner und
persönliche Adresse sucht danach die Recherche in DealSupply.“ Ohne DealSupply: „Wir holen Firma,
Website, Google-Bewertung und Rezensionen, die Adresse und den Geschäftsführer aus dem Impressum.
Wer danach keine Adresse hat, fällt aus der Liste.“

Dazu den Personalisierungs-Hebel dieses Wegs nennen
(`../datenbeschaffung-referenzen/references/personalisierung.md`): was als Spalte mitkommt und was
der Nutzer sich beim Ansehen der Leads selbst notiert (bei Shops das Sortiment oder die
Bewertungen, bei Betrieben vor Ort die Region).

- Was die Quelle im Preis oder für einen kleinen Aufschlag mitliefert und einen Einstieg trägt,
  kommt mit (bei Google Maps immer Bewertung und Rezensionen).
- Entscheider-Namen, persönliche Adressen, Register- und Mobilnummern werden nicht beschafft.
  Wünscht der Nutzer sie trotzdem, den Grund nennen (die Recherche findet und prüft sie) und erst
  nach ausdrücklichem Ja einen Anreicherungs-Lauf planen.
- Der Weg-Skill schreibt die Spalten über `build_csv.py`; nur Rohfelder mit Einstieg zusätzlich
  per `--keep`.
- **Kontaktlücke** (Leads mit eigener Website, aber ohne Adresse): ab MCP 4.0.0 entscheidet der
  Nutzer, ob vorab angereichert wird oder die Recherche sucht. Entscheidungstabelle in
  `datenumfang.md`, Abschnitt „Die Kontaktlücke“. Dem Nutzer sinngemäß sagen: „N Leads haben eine
  eigene Website, aber keine Adresse. Ich kann sie so importieren, dann sucht die Recherche in
  DealSupply die Kontaktadresse; findet sie keine, scheidet der Lead aus und bekommt keine Mail. Bis
  dahin kostet er im Server-Lauf etwa 2 bis 3 Cent bzw. Abo-Kontingent und einen Platz im
  Lead-Kontingent. Vorab das Impressum über dein Apify-Konto auszulesen kostet rund 0,2 Cent je
  Domain, lohnt ab etwa 50 Domains und liefert geprüfte Adressen vor dem Import. Vorab anreichern
  oder direkt importieren?“

**Ohne DealSupply** gelten die letzten beiden Punkte nicht: Die Kontaktlücke wird immer
geschlossen (`impressum-enrichment` ist Pflicht für Domains ohne Adresse), der Geschäftsführer aus
dem Impressum ist der Ansprechpartner, und Leads ohne Adresse fallen aus der Liste
(`ohne-dealsupply.md`). Die Kosten dafür gehören in die Freigabe in Phase 4.

## Phase 3: Vorab-Abgleich

**Ohne DealSupply:** Die eigene Sperrliste aus dem CRM bauen (`sperrliste.py`, Ablauf in
`ohne-dealsupply.md`): Den Export zieht der Nutzer selbst. Die Domains gehen in die
Query-Ausschlüsse, und die Liste läuft vor jeder bezahlten Anreicherung einmal durch
`sperrliste.py --in … --out …`. Das Folgende gilt nur mit MCP.

VOR dem ersten kostenpflichtigen Lauf den Bestand ziehen und bekannte Domains in die
Query-Ausschlüsse geben: `export_leads(format="index")` bzw. `check_leads_exist`, Ablauf in
`../datenbeschaffung-referenzen/references/outreach-uebergabe.md`, Schritt 0. Bekannte Leads sollen
gar nicht erst Geld kosten. `list_lists` zeigt außerdem, was bereits gescrapt und importiert wurde
(Herkunft steht in `source` der Liste).

Mit MCP auch `get_credit_balance` lesen (nur lesend): Die geplante Zahl **neuer** Leads muss in
`account.free_slots` passen (`null` = unbegrenzt; bekannte Adressen belegen keinen Platz), sonst
lehnt der Import ab. Das vor dem bezahlten Scrape klären: kleinere Menge, nicht benötigte Leads
löschen (gibt Plätze sofort frei) oder Plan wechseln. Steht `account.subscription_required` auf
`true`, gibt es kein aktives Abo und es lässt sich nichts importieren: erst einen Plan wählen, dann
scrapen. Import und Listen kosten in DealSupply keine Credits.

## Phase 4: Kosten nennen, Freigabe einholen, Weg-Skill ausführen

1. Erwartete Kosten aus `../datenbeschaffung-referenzen/references/kosten.md` kalkulieren und mit
   Actor-Preis (aktuell im Apify-Store prüfen) nennen: „Das kostet etwa X $ beim Anbieter, harter
   Deckel Y $. Ok?“ Die Abrechnung läuft über das eigene Konto des Kunden. Ohne DealSupply
   gehören die Anreicherung aller Domains ohne Adresse und die Prüfung der Adressen mit in die
   Summe.
2. Ausdrückliche Freigabe abwarten. Ohne Freigabe kein kostenpflichtiger Lauf. Die Schätzung ist
   keine Preisgarantie; den Deckel nie still erhöhen.
3. Den gewählten Weg-Skill laden und fahren. Er endet IMMER mit einer Roh-CSV im Format aus
   `../datenbeschaffung-referenzen/references/csv-spalten.md`, nie mit einer Übergabe und nie mit
   einem eigenen Qualitätsurteil. Zugriffsschicht (Apify-MCP, REST, CLI):
   `../datenbeschaffung-referenzen/references/zugriff.md`.
4. Bei Leads ohne Adresse `impressum-enrichment` (DACH) bzw. `kontaktseiten-fallback` nutzen:
   mit DealSupply **optional** und nur für die Adresse, nach der Entscheidung aus Phase 2b (auf
   Servern unter 4.0.0 ist das der einzige Weg, sie zu importieren); **ohne DealSupply Pflicht**,
   und der Geschäftsführer aus dem Impressum kommt mit. Immer mit Kostenfreigabe.
   `enrichment-waterfall` ist keine Lückenfüllung, sondern eine Ausnahme für wenige wertvolle
   Leads, deren Ansprechpartner schon bekannt ist (siehe dort).

## Phase 5: Pflicht-Endstation

`listen-qualitaet` laden und vollständig durchlaufen: Format prüfen, gegen den Bestand bzw. die
eigene Sperrliste abgleichen, E-Mails verifizieren, 20er-Stichprobe, Import in DealSupply bzw. Datei
für Instantly. Kein Lauf endet mit einer Roh-CSV. Dem Nutzer ehrlich sagen, was dabei Handarbeit
bleibt: die 20 Leads selbst ansehen und, ohne DealSupply, den CRM-Export für die Sperrliste.

**Ohne DealSupply** endet der Lauf hier mit der Datei für Instantly und der Anleitung zum Import
(`ohne-dealsupply.md`). Der Rest dieser Phase gilt nur mit DealSupply.

Danach auf ausdrücklichen Verarbeitungsauftrag die Liste einer bestätigten Kampagne zuordnen
(`add_leads_to_campaign`) und über den Outreach-Workflow `start_lead_run` für `qualification`,
`research` und `email` verwenden. Vor dem Zuordnen ist der Agenten-Check aus `outreach-campaign`,
Phase 4, Pflicht: Wunschkunde, Angebot, Passt-Kriterien, Ausschlusskriterien und Hinweise sowie die
Recherche- und E-Mail-Anweisung müssen für diese Zielgruppe gesetzt sein. Ist die Kampagne neu,
gehört das schon in ihr Setup, bevor gescrapt wird. Das ist ein separater Lauf mit eigenem Preis in
Credits (vorher `quote_lead_run`) oder ein Abo-Lauf ohne Credits.
Keine erfundene `list_id` an `start_lead_run` übergeben und nicht automatisch alle Kampagnenleads
auswählen. Beschaffung und Import allein starten keine Qualifizierung und versenden keine E-Mails.

Bei der Übergabe eine Recherche-Stufe für die Kampagne empfehlen (Tabelle in `datenumfang.md`):
lokale Betriebe mit Website und Rezensionstexten kommen meist mit `basis` aus, das senkt die
Recherchekosten deutlich; mit vielen Leads ohne Adresse `smart` (eine gezielte Impressum-Suche,
wenn die Website keine Adresse zeigt). Die Einstellung ändert der Nutzer in der Kampagne
(`outreach-campaign`). Den Credit-Preis je Lead im Server-Lauf bestimmt die Recherche-Stufe;
verbindlich ist `quote_lead_run`.

## Berichtsform

Nach jedem Lauf ein kompakter Block: Modus (mit oder ohne DealSupply), Weg, Query und Filter,
Pilot-Trefferquote, Anteil mit Bewertung,
Rezensionstext bzw. Plattform-Einstieg (aus dem Bericht von `build_csv.py`), Stückzahlen je Stufe
(roh, nach Dedup bzw. Sperrliste, nach Verifizierung, übergeben, davon ohne E-Mail mit Website,
ohne DealSupply: davon mit Vorname, verworfen je Grund), reale Kosten beim Anbieter und was beim
nächsten Lauf anders gemacht würde. Die Herkunft steht mit DealSupply dauerhaft an der Liste
(`source` bei `create_list`), ohne DealSupply in der Spalte `quelle` der eigenen CSV.
