# Technisches Setup — Domains, Zapmail, Warmup, Sendelimits

> Referenz zu `outreach-launch`. Alles hier passiert beim Kunden, außerhalb von DealSupply: DealSupply
> versendet nichts, legt keine Domains oder Postfächer an und wärmt nichts auf. Bei einem
> Widerspruch zu `outreach-copy` gilt `outreach-copy`, bei einem Widerspruch zur `SKILL.md` von
> `outreach-launch` gilt diese.

## Grundhaltung

Setup ist 60 % der Arbeit. Copy ist 30 %. Send-Strategie ist 10 %. Wer die Reihenfolge umdreht, scheitert.

90 % der Cold Mailer machen den gleichen Fehler: Sie senden, ohne Setup. Ergebnis: Mails landen im Spam, niemand antwortet, die Kampagne wird als „funktioniert nicht" abgeschrieben. Dabei hat sie nie stattgefunden - die Mails wurden nie gelesen.

Das Setup ist der Teil, den niemand sieht und der über alles entscheidet. Es kostet im empfohlenen Zuschnitt rund 125 EUR im Monat und zwei bis drei Stunden Arbeit - und ohne es ist jede Stunde Copy-Arbeit verschwendet.

**Zeitrahmen:** 2-3 Stunden Setup, dann mindestens 14 Tage Warmup. Alles andere (Listen, Kampagne und Personalisierung in DealSupply) läuft parallel.

**Die Reihenfolge ist nicht beliebig:** Domains beim Domain-Anbieter kaufen → mit Zapmail verbinden → Postfächer anlegen → nach Instantly exportieren → Warmup starten, Limits und „Campaign slow ramp“ setzen. Erst am Ende dieser Kette beginnen die 14 Tage. Wer Instantly zuerst kauft, hat zwei Wochen lang ein leeres Tool.

## Schritt 1: Domains kaufen

- [ ] **5 separate Domains** kaufen (NICHT die Hauptdomain!)
- [ ] Endungen: .de, .at, .com, .info, auch .org (Erfahrung DealSupply). Zapmail selbst verkauft kein .de, deshalb beim Domain-Anbieter kaufen
- [ ] Name möglichst nah an der echten Hauptdomain, mit einem Zusatz davor oder dahinter (z. B. getfirmenname.de, firmenname-team.de, firmenname-consulting.com). Instantly rät ebenso zu Domains, die der Hauptdomain ähneln, und nennt Präfixe wie „get“ und „try“; Endungen mit schlechtem Ruf meiden (Liste bei Spamhaus)
- [ ] KEINE 301-Weiterleitung auf die Hauptdomain (sonst verbrennt man die Hauptdomain mit)
- [ ] Anbieter muss **Nameserver-Änderungen** zulassen - das braucht Zapmail im nächsten Schritt. Ausnahme Cloudflare: Dort lassen sich die Nameserver nicht ändern, stattdessen wird das Cloudflare-Konto mit Zapmail verbunden (Schritt 2)
- [ ] Keine Upsells mitkaufen (Domainschutz, KI-Landingpage, Hosting). Es braucht nur die nackte Domain

**Wo kaufen:** GoDaddy, Hostinger, Namecheap, Checkdomain, Strato, Ionos, All-Inkl oder der bestehende Hoster - fast alle bieten DNS- und Nameserver-Einstellungen vollständig. Auch Cloudflare geht, mit Verbindung statt Nameservern. Nach dem Kauf dauert die Registrierung 30 bis 60 Minuten.

**Warum niemals die Hauptdomain:** Wenn die Cold-Mailing-Domain in eine Blacklist rutscht, ist bei einer Sekundärdomain eine Domain verbrannt. Bei der Hauptdomain kommen ab dann auch Rechnungen, Angebote und Kundenmails nicht mehr an. Das ist der teuerste vermeidbare Fehler im ganzen Kanal.

## Schritt 2: Zapmail einrichten und die Domains verbinden

- [ ] **Zapmail** (zapmail.ai) buchen - der Starter-Plan trägt 10 Postfächer, Google und Microsoft aus denselben Plätzen
- [ ] Domains verbinden: **Domains** → **Connect Existing Domains** → Domains eintragen → **Connect Domain** → im Fenster „Connect domain for which provider?“ **Google Workspace** oder **Microsoft 365** wählen → **Confirm**. Eine Domain gehört immer nur zu einem der beiden
- [ ] Die angezeigten Zapmail-Nameserver beim Domain-Anbieter eintragen, dann in Zapmail **Recheck** (meist bis 24 Stunden, je nach Anbieter bis 48)
- [ ] Domains bei Cloudflare: statt Nameservern **Domain Registrar** → **Add Registrar** → **Cloudflare**, mit API-Token (vier Rechte: Account Settings Read, Zone Edit, DNS Edit, Single Redirect Edit) und Account ID; danach die Domains wählen und **Connect**. Anleitung: https://help.zapmail.ai/en/articles/11875451-connect-existing-domains-from-cloudflare-to-zapmail
- [ ] Zapmails Domain-Check abwarten: er prüft jede Domain auf Blacklist-Einträge und bereits verknüpfte Workspaces

**Warum Zapmail und nicht von Hand:** Zapmail setzt SPF, DKIM und DMARC selbst, sobald die Domain verbunden ist. Der Teil, der früher pro Domain drei DNS-Einträge und einen Check bedeutete, fällt damit weg. Dazu der Preis: Der Starter-Plan kostet 39 USD im Monat und enthält 10 Postfächer, also rund 3,90 USD pro Postfach; jedes weitere kostet 3,50 USD (Stand 26.10.2026, zapmail.ai). Einzeln gebucht wären es 6 bis 10 EUR pro Postfach. Bis 30 Postfächer skaliert der Growth-Plan (99 USD im Monat).

Was Zapmail dabei setzt - und was man kennen sollte, wenn ein Kunde fragt, warum eine Mail trotzdem im Spam landet:

| Record | Aufgabe |
|:-------|:--------|
| **SPF** | Legt fest, welche Server überhaupt für die Domain senden dürfen |
| **DKIM** | Signiert jede Mail kryptografisch, damit der Empfänger die Echtheit prüfen kann |
| **DMARC** | Sagt dem Empfänger, was mit Mails passieren soll, die SPF oder DKIM nicht bestehen |

**DMARC nicht leer lassen:** Ein Record allein reicht nicht, er braucht eine Policy und eine Reporting-Adresse. Für den Start ist `p=none` mit einer `rua`-Adresse richtig - dann wird nichts abgewiesen, aber du bekommst Berichte darüber, wer in deinem Namen sendet und ob die Authentifizierung greift. Verschärfen (`p=quarantine`, später `p=reject`) erst, wenn die Berichte sauber sind. Prüf nach dem Verbinden einmal nach, dass Zapmail eine Policy gesetzt hat und der Record nicht leer steht.

Ohne diese drei Einträge geht ein großer Teil der Mails direkt in den Spam - unabhängig von Copy, Offer oder Zielgruppe.

## Schritt 3: Postfächer anlegen

- [ ] Pro Domain **2 Postfächer** = **10 Inboxen total**, direkt in Zapmail: **Mailboxes** → **Assigned** → oben rechts den Plattform-Schalter auf denselben Anbieter wie beim Verbinden → **Assign Mailboxes**
- [ ] **Google oder Microsoft:** beides geht in Zapmail mit demselben Ablauf. Im DACH-Mittelstand läuft oft Outlook, deshalb ist Microsoft 365 ein guter Standard
- [ ] Absender ist **eine echte Person** (am besten die, die auch antwortet und verkauft) in verschiedenen Schreibweisen: `vorname@`, `v.nachname@`, `vorname.nachname@`, `nachname@`; keine Fantasienamen, keine Rollenadressen als Absender
- [ ] **Profilbild** je Postfach hochladen: wirkt persönlicher; manche Postfächer zeigen es erst, nachdem der Empfänger reagiert hat
- [ ] **24-Stunden-Regel:** Alle Postfächer am selben Tag anlegen. Zapmail lässt Postfächer nur in den ersten 24 Stunden nach Anlage des Workspace zuweisen, danach erst im nächsten Abrechnungszeitraum oder mit neuer Domain
- [ ] Zapmail kann die Namenskombinationen für alle verbundenen Domains auf einen Schlag erzeugen (Reiter **AI Generation**)

Die Aufteilung auf viele Inboxen ist kein Komfort, sondern die Grundlage des Volumens: Kein einzelnes Postfach darf viel senden, aber zehn Postfächer zusammen schaffen die Zielmenge, ohne dass eines auffällt.

Die Freischaltung dauert laut Zapmail bei Google bis rund 3, bei Microsoft bis rund 12 Stunden.

## Schritt 4: Nach Instantly exportieren und Warmup starten

- [ ] **Instantly** buchen (empfohlen: Hypergrowth mit 25.000 Kontakten und 100.000 Mails im Monat)
- [ ] Postfächer über Zapmails Export-Funktion übertragen: **Mailboxes** → **Assigned** → alle anhaken → **Export Mailboxes** → **Instantly** → mit Instantly-E-Mail und Passwort anmelden → Workspace wählen → **Export** (dauert etwa 30 Minuten). Voraussetzungen laut Zapmail: bezahlter Instantly-Plan, ein Passwort (wer sich mit Google angemeldet hat, setzt erst eins), Zwei-Faktor-Anmeldung bei Instantly vorübergehend aus
- [ ] In Instantly unter **Email Accounts** auf **Test domain setup**: MX, SPF, DKIM und DMARC müssen stehen
- [ ] Warmup für ALLE Accounts aktivieren: alle Postfächer anhaken → drei Punkte → **Enable warmup**. Start ab 00:00 UTC des nächsten Tages
- [ ] **Nachsehen, dass er wirklich läuft:** Die Flamme am Postfach muss von Grau auf Grün springen. Steht sie grau, wärmt nichts - und das fällt sonst erst auf, wenn die erste Kampagne im Spam landet. Das ist der eine Handgriff, der nach dem Verbinden der Postfächer gerne vergessen wird
- [ ] Warmup-Werte so lassen, wie Instantly sie vorschlägt (für alle über **Edit Accounts**): Increase per day 1, Daily warmup limit 10, Reply rate 30 %, **Disable slow warmup** aus
- [ ] **Mindestens 14 Tage warten** bevor die erste Kampagne startet
- [ ] Freigabe zusätzlich am **Health Score** festmachen (Spalte in **Email Accounts**): über 90 %, am besten 98 bis 100 %
- [ ] Während dem Warmup: Listen bauen (`datenbeschaffung`) und die Kampagne in DealSupply vorbereiten (`outreach-campaign`, danach `outreach-pipeline`)

Warmup heißt: Die Postfächer schreiben sich gegenseitig, öffnen Mails und antworten. Für den Provider sieht das aus wie ein normal genutztes Postfach mit echter Interaktion. Ein Postfach, das an Tag 1 plötzlich 30 Mails an Fremde schickt, sieht aus wie ein gekapertes Konto.

14 Tage sind der Mindestwert. Bei frisch registrierten Domains ohne jede Historie darf es länger dauern - entscheidend ist der Health Score, nicht das Datum.

**Kein echter Versand vor Ablauf des Warmups.** Auch nicht „nur 20 Mails zum Testen".

## Schritt 5: Versand-Einstellungen

- [ ] Sendelimit am Postfach: **Daily campaign limit** 30 Mails pro Inbox pro Tag, immer
- [ ] **Campaign slow ramp** am Postfach einschalten (Email Accounts → Postfach → **Settings** → **Campaign Settings**, für alle über **Edit Accounts**; Instantly markiert ihn als „Recommended“): Start mit 2 Kampagnenmails am Tag, jeden Tag 2 mehr, an Tag 15 bei 30. Die Kampagne bekommt dann gleich ihr volles Tageslimit (Postfächer mal 30, bei 10 Postfächern 300), die Treppe macht Instantly
- [ ] Sendefenster: Mo-Fr, 09:00-17:00 mitteleuropäische Zeit, so legt DealSupply die Kampagne an. Wochenenden aus
- [ ] **Open- und Link-Tracking aus, keine Links in den Mails.** Einschalten nur, wer Öffnungen als Signal nutzt, um sofort (in den ersten Minuten) anzurufen, also selbst Cold Calling macht oder ein Team dafür hat. Neue Instantly-Kampagnen haben Open Tracking aus; Instantly rät für die erste Mail ebenfalls zu „No links, No open tracking“
- [ ] Wer Tracking doch einschaltet: eine **eigene** Tracking-Domain verwenden, keine geteilte. Eine Tracking-Domain, über die viele fremde Absender laufen, überträgt deren Reputation auf deine Links
- [ ] **List-Unsubscribe-Header** im Versandtool aktivieren. Das ist der technische Abmeldeweg, den Mail-Anbieter im Client als Ein-Klick-Abmeldung anzeigen - eine Textzeile im Body allein erfüllt das nicht. Kostet eine Einstellung und senkt die Beschwerdequote messbar

Wird die Instantly-Kampagne aus DealSupply heraus angelegt (Reiter „Instantly" der Kampagne), setzt DealSupply einen Standard-Zeitplan (Mo-Fr 09:00-17:00, Zeitzone Europe/Belgrade, also mitteleuropäische Zeit); er bleibt so. In der Kampagne nur noch das Tageslimit (Postfächer mal 30) setzen.

Bei 10 Inboxen und 30 Mails ergibt das eine Obergrenze von 300 Mails pro Tag. Diese Grenze wird nicht ab Tag 1 gefahren, sondern über „Campaign slow ramp“ schrittweise erreicht: bei 10 Postfächern Tag 1 20, Tag 5 100, Tag 10 200, Tag 15 300 Mails - mehr in `launch-und-optimierung.md`.

Wer die Limits pro Inbox erhöht, statt Inboxen hinzuzufügen, verbrennt Domains. Mehr Volumen heißt immer: mehr Postfächer, nie mehr Mails pro Postfach.

## E-Mail-Verifizierung

Eine hohe Bounce Rate zerstört die Reputation schneller als schlechte Copy. Deshalb gehört Verifizierung zum Setup, nicht zur Optimierung:

- [ ] Alle Adressen vor dem Import verifizieren: im Datenbeschaffungs-Paket ist das Schritt 3 von `listen-qualitaet` (Verifier im eigenen Konto beim Anbieter), sonst in Instantly
- [ ] Zielwert: Bounce Rate unter 3 %, besser unter 1 %
- [ ] Adressen ohne klares Ergebnis („unknown", „risky") aussortieren, nicht mitsenden
- [ ] Rollen-Adressen wie info@, kontakt@, office@ nur bewusst nutzen - sie bouncen selten, landen aber oft bei niemandem

Der Zielwert liegt unter 3 %. Die Notbremse - Versand anhalten und Liste bereinigen - liegt bei 5 %.

## Tools: Versand, Research, Personalisierung

| Zweck | Tool |
|:------|:-----|
| Lead-Qualifizierung, Research und AI-Personalisierung | **DealSupply** |
| Versand und Warmup | Instantly |
| Domains | Domain-Anbieter (GoDaddy, Hostinger u. a.) oder Cloudflare, verbunden mit Zapmail |
| DNS und Postfächer | **Zapmail** (legt Google- oder Microsoft-Postfächer an und setzt SPF, DKIM, DMARC) |
| CRM | z. B. Close |

Instantly ist das Versandtool. DealSupply ist das Qualifizierungs-, Research- und Generierungstool und versendet nichts. Diese Trennung ist wichtig, wenn Kunden fragen, ob sie „das eine oder das andere" brauchen: Sie brauchen beides.

Was DealSupply bis zur Übergabe leistet (Qualifizierung, Research, Variablen, Review, CSV-Export oder Push nach Instantly), steht in der `SKILL.md` von `outreach-launch` unter „Wer macht was".

## Kosten-Übersicht

Zapmail geprüft am 26.10.2026, die übrigen Werte sind Richtwerte aus der Vorlage ohne Prüfdatum. Vor dem Kauf den aktuellen Preis beim Anbieter prüfen.

| Posten | Kosten |
|:-------|:-------|
| 5 Domains | ca. 50-80 EUR/Jahr |
| Zapmail (Starter, 10 Postfächer) | 39 USD/Monat, jedes weitere Postfach 3,50 USD (Stand 26.10.2026) |
| Instantly (Hypergrowth, empfohlen: 25.000 Kontakte, 100.000+ Mails/Monat) | ca. 97 USD/Monat, jährlich ca. 78 USD/Monat |
| **Gesamt** | **ca. 125 EUR/Monat im empfohlenen Hypergrowth-Zuschnitt**; mit dem kleineren Growth-Plan (47 USD, 1.000 Kontakte) als Einstieg rund 80 EUR |

Dazu kommen je nach Vorgehen die Kosten für Leads (beim Datenanbieter) und für die Verarbeitung in DealSupply (Credits je Lead im Server-Lauf, im Abo-Lauf keine Credits). Wer das Setup sparen will, spart am einzigen Teil, der nicht verhandelbar ist.

## Checkliste: Setup fertig?

- [ ] 5 Domains gekauft, keine davon die Hauptdomain
- [ ] Keine Weiterleitung von den Sekundärdomains auf die Hauptdomain
- [ ] Domains in Zapmail verbunden (Nameserver oder Cloudflare-Konto), Domain-Check ohne Befund
- [ ] 10 Postfächer angelegt, Google oder Microsoft (2 pro Domain, alle am selben Tag), echte Person, Profilbild
- [ ] SPF, DKIM, DMARC stehen, DMARC mit `p=none` und Reporting-Adresse
- [ ] Alle 10 Postfächer nach Instantly exportiert
- [ ] Warmup für alle 10 aktiv (Flamme grün), mindestens 14 Tage, Health Score über 90 %, am besten 98 bis 100 %
- [ ] Daily campaign limit 30 je Postfach, Campaign slow ramp an, Tageslimit der Kampagne Postfächer mal 30, Sendefenster Mo-Fr 09:00-17:00
- [ ] Open- und Link-Tracking aus (außer für sofortiges Anrufen nach Öffnung), keine Links in den Mails
- [ ] List-Unsubscribe-Header aktiviert
- [ ] Signatur genau einmal: Nach `outreach-copy` steht sie als schlanker Klartext in der Sequenz. Eine Postfach-Signatur in Instantly nur, wenn die Sequenz keine eigene trägt, sonst steht sie doppelt. Trägt die Sequenz `{{accountSignature}}` (Kampagne aus dem Start-Satz der App), hat jedes Versandpostfach in Instantly eine schlanke Signatur mit Name, Rolle und Firma, sonst endet die Mail nach der Grußformel
- [ ] Leadliste verifiziert, Bounce-Prognose unter 3 %

Erst wenn jeder Punkt steht, geht die erste Kampagne live.

## Optional, aber hilfreich

Diese Schritte gehören nicht zum Pflichtprogramm, ersparen aber Ärger:

- **Inbox-Placement-Test** nach dem Warmup und vor dem Hochfahren: eine Testmail an eigene Postfächer bei verschiedenen Anbietern senden und prüfen, wo sie landet
- **Reputations-Überwachung**: die Postmaster-Werkzeuge der großen Anbieter zeigen Zustellrate, Beschwerdequote und Authentifizierungsstatus pro Domain
- **Blacklist-Check** in größeren Abständen, damit eine Listung nicht erst an fallenden Antwortquoten auffällt
- **Wenn eine Domain gelistet ist**: aus der Rotation nehmen, Ursache prüfen (meist Bounces oder Beschwerden), und erst nach Klärung ein Delisting beantragen. Weitersenden verschlimmert es

## Das Wichtigste

Fünf Domains, zehn Postfächer, drei DNS-Einträge, 14 Tage Geduld und ein Health Score nahe 100. Wer diese vier Dinge macht, hat den Kanal. Wer eines davon überspringt, schreibt Mails, die niemand liest - und sucht den Fehler dann in der Copy.
