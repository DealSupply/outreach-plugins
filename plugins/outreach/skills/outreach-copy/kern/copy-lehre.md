# Cold-Mail-Copy: die Lehre

Die verbindlichen Regeln für Cold-Mail-Copy im deutschsprachigen B2B: Entry Mail, individueller
Bezug (Intro), Follow-ups, Betreff, Verbote und Selbstprüfung. Unabhängig vom Versandtool.

Grundlage: Kurs Outbound 3.0 (Copywriting-Class, Marketing Offers, Master-Formel), abgenommene
Kundenkampagnen und Antwortdaten echter Kampagnen bis 23.10.2026. Die Offer-Lehre steht in
`marketing-offer.md`, vollständige Beispiele in `beispiele.md`.

---

## Grundhaltung

Eine Cold Mail ist keine kurze Version deiner Website. Sie ist eine Nachricht an einen Menschen,
der dich nicht kennt und dessen Tag voll ist. Deshalb gilt: wenige Bausteine, ein CTA, und kein
Satz über die eigene Firma.

Der häufigste Reflex ist, sich erst vorzustellen. Genau der killt die Mail. Wer sich vorstellt,
bevor er einen Grund geliefert hat, weiterzulesen, hat die Mail an die Stelle geschrieben, wo der
Empfänger sie löscht.

Und eine Mail reicht nicht. Ein großer Teil der Antworten kommt auf die Nachfass-Mails. Wer nach
Mail 1 aufgibt, hat die ganze Arbeit gemacht und die Ernte verschenkt.

Ziel der ersten Mail ist eine Antwort. Kein Klick, kein Termin.

Nichts erfinden: keine Zahlen, Namen, Referenzen, Fristen oder Kapazitäten, die nicht aus den
Angaben des Absenders oder aus der Recherche zum Lead stammen. Fehlt eine Angabe, allgemeiner
formulieren oder nachfragen.

## Platzhalter

Die Copy ist eine Vorlage für viele Leads. Was je Lead wechselt, steht als Platzhalter in
doppelten geschweiften Klammern:

| Platzhalter | Inhalt | Hinweis |
|:------------|:-------|:--------|
| `{{Vorname}}` | Vorname der Person, der die Versandadresse gehört | Leads ohne belastbaren Vornamen bekommen „Hallo,“ (eigenes Segment oder Fallback im Versandtool), nie „Hallo ,“ |
| `{{Intro}}` | der individuelle Bezug je Lead (Teil 2) | steht nur in der Entry Mail |
| `{{Firma}}` | bereinigter Kurzname der Firma, so wie ein Kollege ihn sagen würde | nur, wenn die Liste dieses Feld sauber führt; rohe Importnamen sind oft Google-Titel, Domains oder tragen Rechtsform und Leistungsliste |

Vor dem Einfügen ins Versandtool die Namen an dessen Variablen anpassen (in Instantly etwa
`{{firstName}}`). Jeder Platzhalter muss für jeden Lead gefüllt sein, sonst sieht der Empfänger
eine Lücke oder Rohtext. Andere sichtbare Platzhalter („[Branche]“, „[Name]“) stehen im fertigen
Text nie.

## Tonalität und Form

- Du-Form als Standard: direkt, konkret, kein Beratersprech, keine Floskeln. Deutsch.
- Knapp und menschlich: kurze Sätze, ein klarer CTA pro Mail. Die Mail klingt wie eine kurze
  Nachricht an einen Bekannten, nicht wie eine Agentur-Website.
- Keine Gedankenstriche: weder Halbgeviertstrich noch Geviertstrich, auch kein Bindestrich mit
  Leerzeichen als Trenner. Komma, Punkt oder neuer Satz. Bindestriche nur innerhalb von Wörtern
  (E-Mail, Smart-Home); Ausnahme ist die Signaturzeile „Rolle - Firma“.
- Anführungszeichen nur als deutsches Paar „…“, geschlossen mit “, nie mit dem geraden Zeichen.
- Echte Umlaute und ß in jedem Feld: „für“, „Grüße“, „über“, nie „fuer“, „Gruesse“, „ueber“.
- Plain Text: kein Fettdruck, keine Aufzählungszeichen, keine Emojis, kein HTML-Layout, keine
  Bilder, keine Anhänge.

## Anrede und Ansprache

| Modus | Pronomen | Gruß | Ohne benennbare Person |
|:------|:---------|:-----|:-----------------------|
| du (Standard) | du/dich/dir/dein; Tatsachen über den Betrieb auch ihr/euer | „Hallo {{Vorname}},“ | „Hallo,“ |
| Sie (Ausnahme) | Sie/Ihnen/Ihre | „Hallo Frau Nachname,“ / „Hallo Herr Nachname,“ | „Guten Tag,“ |

- **Standard ist du, Singular**, auch bei Praxen, Kanzleien, Finanz und generischen Adressen. Die
  Mail richtet sich an die Person, die entscheidet, nicht an den Betrieb. Sie gilt nur, wenn der
  Absender sie für die ganze Kampagne wählt (Kampagnen an sehr große Unternehmen), nie je Lead.
  Dass eine alte Vorlage oder die Branche siezt, ist kein Grund für eine Abweichung.
- **Die Person nie mit ihr/euch ansprechen**, auch nicht im Gruß: kein „Hallo <Firma> Team,“, kein
  „Hallo zusammen,“, kein „Hey …“, nie Sie und du gemischt.
- **Tatsachen über einen Betrieb mit mehreren Personen** dürfen mit ihr/euer stehen („dass ihr nach
  ISO 9001 zertifiziert seid“, „auf eurer Website“) oder mit „dein Team“, „deine Firma“, je
  nachdem, was natürlicher klingt. Innerhalb eines Satzes nicht zwischen du und ihr wechseln
  („deine Bewertungen …, dass ihr …“ ist falsch). Bei Solo-Selbstständigen nur du/dein.
- **Firmenleistungen gehören dem Betrieb:** nie „du hast die Anlage gebaut“ an eine
  Geschäftsführerin oder einen Vertriebsleiter. „du hast …“ nur, wenn die Person es nachweislich
  selbst getan hat, oder bei Ein-Personen-Betrieben, Personenmarken und kleinen Inhaberbetrieben,
  die sie verkörpert.
- **Wer bekommt den Vornamen?** Die Person, der die Versandadresse gehört. Bei allgemeinen Adressen
  (info@, kontakt@, office@, hallo@ …) der Entscheider aus der Recherche (Inhaber,
  Geschäftsführung), damit die Mail dort ankommt oder weitergeleitet wird. Personenmarken und
  Ein-Personen-Betriebe immer mit Vornamen, auch hinter info@. Ist keine Person klar erkennbar,
  steht nur „Hallo,“ und der Text bleibt im Singular („dein Team“, „dein Betrieb“).
- **Gemischte Zielgruppen:** Der feste Text nennt den Empfänger nur mit einer Bezeichnung, die auf
  jeden Lead passt. Mischt die Liste Firmen und Einzelpersonen, „dein Business“ oder „für dich“
  statt „deine Agentur“.
- Titel („Dr.“) nur in der Sie-Form und nur, wenn er belegt ist.
- Bei Sie-Kampagnen jeden festen Text der Vorlagen umschreiben, nicht mischen.

---

# TEIL 1: Die Entry Mail

## Anatomie

```
Hallo {{Vorname}},            1. Anrede
{{Intro}}                     2. individueller Bezug: Lob am konkreten Detail (Teil 2)
Überleitung + Offer           3. fester Text, für alle Leads gleich, benennt KEIN lead-spezifisches
                                 Problem; bei Karte C als erledigte Arbeit, bei A als Angebot
Zweiter Satz zum Angebot      4. eigener Absatz, je Karte: A, B und C je Lead geschrieben wie
                                 das Intro (C der Feinheiten-Satz), D und E keiner
EIN Frage-CTA                 5. niedrige Hürde
Signatur im Klartext          6. Grußformel, Name, „Rolle - Firma“
Abmeldezeile                  7. nach einer Leerzeile unter der Signatur, in Step 1 und Step 3
```

Jeder Baustein steht als eigener kurzer Absatz. **Die Mail soll klingen wie eine WhatsApp von
einem Bekannten, nicht wie eine Agentur-Website.**

Die Master-Formel (Kurs Outbound 3.0, Lektion 2.4) in fünf Bausteinen: Lob → „Deswegen …“ →
konkretes Offer → Fertigstellung → CTA mit wenig Verpflichtung. Im Kurs trägt der Halbsatz „… und
werde morgen mit dem Entwurf fertig.“ die Fertigstellung, hier trägt sie das „morgen“ im
Schlusssatz („… wenn ich es dir morgen zusende?“). „Morgen“ wirkt stärker als „schon fertig“: Der
Lead sieht, dass gerade noch für ihn gearbeitet wird.

## Das Marketing Offer in Mail 1

- GENAU EIN Marketing Offer mit GENAU EINEM CTA. Karte und Tests: `marketing-offer.md`.
- Bei Karte C als bereits erledigte Arbeit formulieren („war so frei und habe … erstellt“),
  nicht als Absicht. Reziprozität wirkt erst, wenn das Geschenk schon existiert. Bei Karte A ist
  das Deliverable ein Angebot („bieten … an“), nie erledigte Arbeit.
- Kein „Lass uns mal sprechen“ ohne vorbereiteten Mehrwert.
- Das Offer steht NUR in Mail 1. Follow-ups wiederholen es nicht.

## Die universelle Überleitung

Der statische Satz NACH dem Intro. Er verbindet jeden möglichen Bezug nahtlos mit dem Offer,
ohne Pitch. Weil er für alle Leads gleich ist, muss er zu JEDEM Intro passen.

- schließt an jedes mögliche Intro an, egal ob es über Bewertungen, die Website oder die Branche
  spricht
- leitet direkt zum Offer über
- benennt kein lead-spezifisches Problem
- kein „Wir sind …“, „Wir machen …“, „Seit X Jahren …“
- 1-2 Sätze

| Karte | Überleitung |
|:------|:------------|
| **A: Kostenlose Teildienstleistung** | „Genau deshalb bieten wir aktuell für [Anzahl] Unternehmen in [Region] ein kostenloses [Deliverable] an.“ |
| **B: Tester/Pilotprojekt** | „Genau solche Unternehmen suchen wir gerade. Wir starten [Projekt] mit [Anzahl] Betrieben in [Region].“ |
| **C: Konkretes Deliverable (Reziprozität)** | „Deswegen war ich so frei und habe [Deliverable] für dich erstellt.“ |
| **D: Förder-Hook** | „Wusstest du, dass der Staat aktuell bis zu [Prozent] der [Kosten] übernimmt?“ (mit Träger, wenn der Nutzer ihn nennt: „dass das Land Baden-Württemberg …“) |
| **E: Partner gesucht** | „Genau solche [Branche] suchen wir als Partner. Wir haben regelmäßig [Anfragen], die zu dir passen würden.“ |

Die Klammern füllst du beim Schreiben aus den Angaben des Absenders; im fertigen Text steht keine
Klammer mehr. Beginnt der feste Text mit einem eigenen Lob („Das hat mich neugierig gemacht.“),
darf das Intro diese Aussage nicht vorwegnehmen.

## Der zweite Satz zum Angebot

Stand 05.11.2026: Nach dem Angebotssatz folgt in Mail 1 immer ein zweiter Satz zum Angebot, als
eigener Absatz zwischen Offer und CTA, passend zur Karte. KEIN zweites Offer, KEIN zweiter CTA:
Der Satz beschreibt dasselbe Deliverable, nur eine Schicht tiefer.

| Karte | Zweiter Satz | Wer schreibt ihn |
|:------|:-------------|:-----------------|
| **C: Konkretes Deliverable** | Fortschritt: der Feinheiten-Satz, genau ein Detail je Lead | je Lead, wie das Intro |
| **A: Kostenlose Teildienstleistung** | Inhalt: was für diesen Lead konkret drin wäre, im Konjunktiv | je Lead, wie das Intro |
| **B: Tester/Pilotprojekt** | Rahmen: was der Empfänger im Pilot bekommt und was er dafür gibt | je Lead, wie das Intro |
| **D: Förder-Hook, E: Partner gesucht** | kein weiterer Satz, die Überleitung hat schon zwei Sätze | entfällt |

### Karte C: der Feinheiten-Satz (Value Stacking)

Der Satz wird je Lead geschrieben (Stand 05.11.2026), nicht mehr als fester Text mit einer Lücke
für die ganze Liste. Regel, wörtlich: Ein Satz, der genau so beginnt: „Ich bin gerade noch an den
letzten Feinheiten dran, vor allem“ und dann genau ein Detail des schon erstellten Ergebnisses
nennt, an dem noch gefeilt wird, passend zu diesem Lead (aus seiner Recherche oder dem Detail des
Schwerpunkts), grammatisch vollständig (z. B. „an der …“). Kein „morgen“, kein „fertig werden“,
keine neue Leistung. Englisch: „I'm just finishing up the last few details, mainly …“.

- Der Anfang bleibt wörtlich, nicht umformulieren, nicht „Feinschliff“. Nichts erfinden: Das
  Detail gehört zu dem, was schon erstellt ist.
- Das „morgen“ der Fertigstellung steht im Schlusssatz, nicht im Feinheiten-Satz, sonst stünde es
  zweimal da.

```
Deswegen war ich so frei und habe dir einen kompletten Webseitenentwurf inklusive
Buchungssystem erstellt.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an der Optimierung für Google
und KI-Suchmaschinen.

Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.
```

### Karte A und B: der Satz je Lead

Bei A und B gibt es keinen Feinheiten-Satz: Er behauptet Arbeit, die es vor der Antwort nicht
gibt. Der Satz wird je Lead neu geschrieben, passend zu Recherche und Website des Leads.

- **A, Inhaltssatz:** „Darin wären deine drei meistgebuchten Behandlungen mit Preis, Ablauf und
  Buchungsknopf, gebaut aus den Texten und Fotos, die du schon online hast.“
- **B, Rahmensatz:** macht den Pilot an diesem Lead fest: was er konkret bekäme, bezogen auf etwas
  aus seiner Recherche (Leistung, Zielkunden, Region), und was er dafür gibt (ehrliches
  Feedback), nicht bei jedem Lead derselbe Satz. „Im Pilot schreibe ich dir die erste Mail an
  einen deiner Wunschkunden aus dem Maschinenbau, du sagst mir dafür ehrlich, was du davon
  hältst.“
- Nie als erledigte Arbeit: kein „erstellt“, „vorbereitet“, „liegt bereit“, kein
  Feinheiten-Wortlaut. A steht im Konjunktiv.
- Nur Inhalte, die die Lieferzusage des Absenders deckt: keine Zahl, die weder Lieferzusage noch
  Recherche belegt, keine Frist, kein Gespräch, Termin oder Call.
- Ein Satz, höchstens 25 Wörter, keine Frage (der CTA folgt fest), kein zweites Offer.

## Der CTA

Genau EIN CTA pro Mail. Nie zwei Optionen.

Standard bei Karte A und C (Stand 05.11.2026):
„Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“
Sie-Form: „Wäre es in Ordnung, wenn ich es Ihnen morgen zusende? Völlig unverbindlich natürlich.“

Der Zusatz „Völlig unverbindlich natürlich.“ senkt die Hürde und ist kein zweiter CTA. Er ist an
echten Kampagnen belegt: In der besten ausgewerteten Kampagne (20,5 % Antwortquote) reagierten
84 % der positiven Antworten direkt auf diesen Erlaubnis-CTA. „unverbindlich“ gilt deshalb im Body
nicht als Spam-Wort, im Betreff hat es nichts zu suchen.

Hat die Kampagne Schwerpunkte mit einem Wort für die Sache (etwa „den Entwurf“, „das Setup“),
steht das Wort an der Stelle von „es“, mit anderer Wortstellung: „Wäre es in Ordnung, wenn ich dir
morgen den Entwurf zusende? Völlig unverbindlich natürlich.“ Jede Kampagne hat außerdem ein eigenes Wort für die Sache (in ListM8 auf der Angebots-Seite unter der Schlussfrage, vom Assistenten vorgeschlagen): Es steht nur in der Frage von Mail 3 und gilt dort, solange Mail 3 nicht das Wort des Schwerpunkts trägt (Variable `{{ai.offer_noun}}`); Mail 1 behält „es“ bzw. „das“; ohne Wort nimmt Mail 3 die Frage aus Mail 1 wörtlich (06.11.2026). Kein „Link“ im Schlusssatz (nicht
„… den Link dazu schicke?“), die Sache wird zugesendet. „morgen“ nur, wenn der Absender das
Deliverable nach der Antwort wirklich bis zum nächsten Tag liefern kann, sonst „… wenn ich es dir
zusende?“.

| Gut | Warum |
|:----|:------|
| „Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“ | Reziprozität plus Ja/Nein |
| „Wäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich natürlich.“ | Karte A, Ja/Nein ohne Verpflichtung |
| „Wärst du grundsätzlich offen dafür?“ | Karte B, Pilot |
| „Wäre es in Ordnung, wenn ich dir kurz aufschreibe, welches Programm für dich infrage kommt? Völlig unverbindlich natürlich.“ | Karte D, Förderung |
| „Wäre das grundsätzlich interessant?“ | Karte E, verpflichtet zu nichts |

Kein Terminvorschlag und kein Link in Mail 1. Der CTA ist die Antwort, nicht der Klick.

## Kein Pitch, keine Selbstvorstellung

**Proof-Block raus:** „Nach über 200 Kampagnen …“, „Wir sind seit 10 Jahren …“, „Als Google
Premium Partner …“ hat in der Entry Mail keinen Platz. Es schreckt ab und wirkt wie ein Pitch.

- Über den Empfänger schreiben, nie über den Absender („Du bekommst …“, nicht „Wir bieten …“).
- Verboten im Body: „Wir helfen [Zielgruppe] dabei …“, „Das machen wir seit X Jahren …“, „Als
  [Zertifizierung/Partner] …“, „mein Name ist“, „unser Unternehmen“, jeder Satz, der die eigene
  Firma beschreibt.
- Authority gehört in die Signatur, Social Proof in Step 3.

## Signatur

Name, Rolle und Firma des Absenders als Klartext. Mehr nicht. Ohne bekannten Absendernamen nur die
Grußformel. Vor der Grußformel stehen zwei Leerzeilen, eine mehr als zwischen den Absätzen; die
Signatur folgt direkt darunter (05.11.2026).

**So:**

```
Viele Grüße
Lena Brandt
Geschäftsführerin - Brandt Online Marketing GmbH
```

**Auch ok (wenn wirklich beeindruckend):**

```
Viele Grüße
Paul Wagner
Geschäftsführer - Wagner Digital GmbH
M.Sc. Informatik, TU Wien
```

**NICHT so:**

```
Viele Grüße
Lena Brandt
Geschäftsführerin - Brandt Online Marketing GmbH
Google Premium Partner | 2.200+ Seminarteilnehmer
Ausgezeichnet als Top SEO Agentur 2025
www.brandt-online-marketing.de | Tel: 0221 123 456
Folge uns auf LinkedIn | Instagram
```

Eine aufgeblähte Signatur macht denselben Fehler wie ein Pitch-Block im Body: Sie schreit „Ich
will dir was verkaufen“.

## Abmeldezeile

In Step 1 und Step 3 steht nach einer Leerzeile unter der
Signatur genau diese Zeile, ohne „PS:“ und nie vor dem CTA:

```
Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.
```

Sie-Form: „Falls das gerade kein Thema für Sie ist, geben Sie mir kurz Bescheid.“ Gekürzt am
05.11.2026; die frühere Zeile „…, dann melde ich mich nicht mehr.“ steht nur noch in bestehenden
Kampagnen und zählt bei der Prüfung weiter als Abmeldezeile.

Sie klingt wie ein Mensch, der Rücksicht nimmt, und gibt trotzdem einen klaren Weg hinaus. Nie
Opt-out-Fachsprache in der Copy: kein „STOPP“ oder „Stop“, kein „abmelden“, „abbestellen“,
„austragen“, „unsubscribe“ oder „Opt-out“. Das klingt nach Massenversand und Newsletter. Den
technischen Abmeldelink (List-Unsubscribe) setzt das Versandtool zusätzlich. Die Zeile zählt nicht
zum Wortlimit.

## Zwei Varianten für den A/B-Test

Kann das Versandtool A/B-Tests (etwa Instantly), entstehen zwei Entry-Mail-Varianten:

- gleiche Offer-Karte, gleiches Offer, nie zwei verschiedene Karten in einem Test
- Variante B ändert genau EINEN Hebel: Blickwinkel der Offer-Formulierung, das On-Top-Detail im
  Feinheiten-Satz (Karte C) bzw. die Vorgabe für den zweiten Satz (A, B) oder die CTA-Form. So
  zeigt der Test, was gewirkt hat
- beide Varianten halten alle Regeln dieser Lehre
- die Follow-ups sind für beide Varianten gleich

Ein echter Offer-Test ist ein Kartenwechsel (A gegen C), aber dann als eigene Kampagne, nicht als
Variante.

In ListM8 legt der Assistent die Varianten von Mail 1 selbst an: den Betreff-Test (B mit
persönlichem Betreff, ab Werk an, siehe Teil 4) und auf Wunsch den Intro-Test (C mit dem
zweitbesten Intro). Eigene Varianten wie oben kommen im Reiter Sequenzen dazu.

---

# TEIL 2: Der individuelle Bezug (Intro)

Das Intro ist der eine Satz, der entscheidet, ob die Mail als persönliche Nachricht oder als
Massenmail gelesen wird. Gut gemachte Personalisierung hebt die Antwortquote spürbar, falsche
schadet. Wer sicher gehen will, schickt einem Teil der Leads die Mail ohne Intro als
Kontrollgruppe.

Das Intro ist kein Kompliment-Generator, sondern ein Beweis: Es beweist, dass jemand hingeschaut
hat. Deshalb entscheidet nicht die Formulierung, sondern das Detail. Wo es kein Detail gibt, ist
der ehrliche Fallback-Satz besser als eine erfundene Beobachtung.

Das Intro entsteht je Lead: von Hand, mit einem Personalisierungs-Tool oder durch einen Assistenten
mit Recherche. Die Regeln gelten für jeden Weg.

## Lob, keine Kritik

Das Intro ist Lob oder eine anerkennende Beobachtung, getragen von einem konkreten Detail. KEINE
Kritik und KEIN Verbesserungsvorschlag. Das Problem sind leere Lobadjektive ohne Inhalt, nicht das
Lob selbst.

Wer mit einem Mangel einsteigt, macht den Empfänger klein und muss ihn danach überzeugen. Wer mit
Lob einsteigt, hat ihn auf seiner Seite und muss nur noch das Offer nennen.

## Abhebung und Austauschtest

### Abhebung statt Leistungsnennung

Das Intro nennt, was diesen Betrieb von anderen seiner Branche abhebt:

| Typ | Beispiel für den Fund (nicht für den Satz) |
|:----|:-------------------------------------------|
| Eigenname oder eigenes Konzept | ein Behandlungs- oder Servicekonzept mit eigenem Namen |
| Ungewöhnliche Zeit oder Zahl | Sprechstunde donnerstags bis 20 Uhr, Angebot 48 Stunden nach dem Aufmaß |
| Eigenes Verfahren | jedes Bad vorab als begehbarer 3D-Rundgang |
| Seltene Spezialisierung | nur Holzfenster im Denkmalschutz |
| Auszeichnung | ein Branchenpreis, ein Siegel mit Jahr |
| Lob aus Bewertungen | was Kunden über DIESEN Betrieb schreiben |
| Auffällige Bewertungszahlen | über 200 Rezensionen mit einem Schnitt von 4,8 (siehe Rangfolge) |

Projekte, Referenzen, Firmengeschichte oder Gründungsjahr (mit seinem Ereignis), Lage und
Ausstattung zählen ebenfalls, wenn sie den Austauschtest bestehen. Eine Aufzählung von Leistungen
(„A, B und C“) besteht ihn nie.

### Der Austauschtest

Passt der Satz auf zehn andere Betriebe derselben Branche in der Stadt, ist er kein Aufhänger.
Dann den nächsten Anker nehmen, zuletzt den Fallback.

- Ein Nutzen rettet keine Standardleistung: „du scannst digital, das hilft bei Würgereiz“ fällt
  durch, weil der digitale Scan in vielen Praxen Standard ist.
- Dasselbe Thema besteht als Lob aus Bewertungstexten (was Kunden über DIESEN Betrieb schreiben),
  nicht als Zeile aus der Leistungsliste.

| Branche | Fällt durch | Besteht | Warum |
|:--------|:------------|:--------|:------|
| Dental | Lachgas für Angstpatienten | ein Kronen-Konzept mit eigenem Namen, Krone am selben Termin | Lachgas steht bei vielen Praxen auf der Leistungsseite, ein eigenes Konzept nicht |
| Dental | digitaler Scan statt Abdruck, „hilft bei Würgereiz“ | Sprechstunde donnerstags bis 20 Uhr | der Nutzen rettet die Standardleistung nicht; die ungewöhnliche Zeit ist selbst die Abhebung |
| Dental | „du behandelst Angstpatienten“ von der Leistungsseite | mehrere Bewertungen schreiben, dass Patienten trotz Angst ruhig durch die Behandlung kamen | gleiches Thema, aber als Lob über diesen Betrieb |
| Handwerk | du bietest Badsanierung an | jedes Bad vorab als begehbarer 3D-Rundgang | Badsanierung macht jeder Sanitärbetrieb, den Rundgang kaum einer |

### Sperrliste je Kampagne

Vor dem Schreiben der Intros eine Sperrliste festlegen: Was steht bei fast jedem Betrieb dieser
Branche auf der Leistungsseite? Diese Begriffe (meist 6 bis 10) tragen kein Intro, außer als Lob
aus Bewertungstexten.

Beispiel Dental: Angstpatienten, Lachgas, Sedierung/Narkose, Kinderbehandlung, Notdienst,
Prophylaxe/Dentalhygiene, digitaler Scan/Abdruck, Implantate allgemein.

## Rangfolge der Anker

1. **Lob aus Bewertungstexten** (Paraphrase). Plural oder „immer wieder“ nur, wenn mindestens zwei
   Bewertungen das Lob tragen. Der Einstieg nennt die Quelle („ich hab mir deine Bewertungen
   angeschaut, und …“); ein nacktes „jemand schreibt, dass …“ wirkt wie aus dem Nichts.
2. **Abhebendes Detail von der Website**, auch Wachstum oder eine Stellenanzeige als Erkenntnis über
   den Betrieb (Wachstum, Spezialisierung, Projekt). Nie „ich hab gesehen, dass du gerade …
   suchst“, nie „du stellst ein“.
3. **Anzahl und Schnitt der Bewertungen** als eigener Anker: erst ab mindestens 30 Bewertungen und
   einem Schnitt ab 4,5. Zahl gerundet („über 200“), Schnitt mit Komma („4,8“). Widersprechen sich
   Quellen, gilt der kleinere Wert. Darunter keine Bewertungszahlen. Die Zahl kommt erst, wenn
   weder Bewertungslob noch ein abhebendes Website-Detail besteht.
4. **Fallback der Kampagne.**

Bewertungen werden deshalb zuerst recherchiert, nicht erst, wenn die Website wenig hergibt. Jeder
Anker muss den Austauschtest bestehen, sonst gilt der nächste.

## Aufbau: Einstieg, Anker, Abschluss

### Einstiege abwechseln

Einstiegsrahmen sind erlaubt und keine Selbstvorstellung, keiner ist Standard: „mir ist
aufgefallen, dass …“, „ich hab mir … angeschaut“, „beim Stöbern auf deiner Website …“, „ich war
gerade auf deiner Website: …“ oder direkt mit dem Detail. Über eine Kampagne gleichmäßig
abwechseln. Beginnt mehr als ein Drittel gleich oder trägt mehr als ein Drittel denselben Anker,
ist das ein systematischer Befund: dann Regeln oder Sperrliste nachschärfen, nicht einzeln
nachbessern.

### Positiver Schluss

Der Abschluss ist keine Pflicht. Rangfolge (Entscheidung 23.10.2026 nach Blindtest und
Antwortdaten: Würdigungen gerieten in 18 von 77 Mails zum Gutachten oder wiederholten das Detail,
Reaktionen kaum; in einer der stärksten Kampagnen kamen alle Interessenten aus Intros ohne
Schluss):

1. **Kein Schluss**, wenn das Detail schon selbst ein Lob ist (was Kunden in Bewertungen schreiben,
   eine Auszeichnung, ein Preis) oder der erste Satz des festen Texts selbst lobt. Nie zweimal
   loben.
2. **Sonst eine kurze persönliche Reaktion** direkt hinter dem Detail, bei einem neutralen Faktum
   (Öffnungszeit, Verfahren, Spezialisierung, Projekt) oder einer Bewertungszahl. In der
   Vergangenheit erzählt, wie unter Kollegen. Richtung und Tonlage aus den Antwortdaten (725
   kontaktierte Intros, Antwortquote 13,0 bis 6,1 %): „das fand ich richtig schön“, „das ist mir
   direkt hängen geblieben“, „das hat mir gut gefallen“, „das fand ich richtig sympathisch“, „das
   hat mich angesprochen“. Passt eine eigene kurze Reaktion besser zum Detail, im selben Ton bilden
   (bei einer historischen Kegelbahn etwa „da musste ich direkt schmunzeln“), höchstens etwa sechs
   Wörter. „richtig“ ist erlaubt, Übertreibung („total begeistert“) nicht. Die Reaktion wechselt
   von Lead zu Lead, nie derselbe Satz in allen Mails. Hinter einer Bewertungszahl steht immer eine
   Reaktion. Hinter Firmengeschichte, Gründung oder Alter des Betriebs heißt die Reaktion immer „das hab ich richtig gern gelesen“ (Sie-Form gleich, englisch „That was really nice to read.“), auch wenn der Vorschlag eine andere nennt; „das fand ich richtig sympathisch“ passt dort nicht (E54, 06.11.2026).
3. **Eine Würdigung nur ausnahmsweise**, wenn sie etwas Neues und Konkretes sagt, das nicht schon im
   Detail steht: Anerkennung mit Inhalt („da steckt richtig viel Handarbeit drin“), Seltenheit als
   eigene Erfahrung („so eine Nachsorge ist mir noch nicht begegnet“), ein Superlativ am Detail nur
   bei wirklich beeindruckendem Anker. Im Zweifel die Reaktion; klingt auch sie nicht, bleibt das
   Faktum ohne Schluss.

Verboten im Schluss:

- **Mechanik-Nutzen:** ein Schluss, der erklärt, was Kunden dank des Details tun können oder sich
  sparen („so können sich Interessierte vorab ein Bild machen“, „so bekommen Kunden schneller einen
  Termin“, „so weiß jeder Hausmeister, wer morgens kommt“, „das spart Berufstätigen den Urlaubstag
  für den Reifenwechsel“). Er beschreibt eine Funktion, statt den Betrieb zu würdigen, und stand in
  etwa einem Drittel der geprüften Intros.
- **Gutachten-Ton und Folgerungen:** „das zeigt, wie …“, „das zeigt, dass …“, „das spricht für …“
  über Ausrichtung, Erfahrung oder Qualität („seit 2004 in der Branche, das spricht für viel
  Branchenerfahrung“, „macht das Angebot schön konkret“).
- **Leeres Prüfer-Urteil**, das auf jeden Betrieb passt: „das wirkt vertrauenswürdig“, „da machst
  du vieles richtig“, „so einen Schnitt hält man nur, wenn die Arbeit stimmt“.
- **Vergleich ohne Beleg:** „hebt dich von jeder anderen Agentur ab“, „bietet sonst kaum ein
  Studio an“. Seltenheit nur als eigene Erfahrung am Detail, nie im allgemeinen „man“ („erlebt man
  nicht oft“).
- **Lob ohne Detail, doppeltes Lob, Würdigung und Reaktion hintereinander.**
- Nichts erfinden, nur was direkt aus dem Detail folgt (nie „deine Patienten lieben das“).

## MUSS und NIEMALS

**MUSS:**

- besteht den Austauschtest und nennt nichts von der Sperrliste (außer als Bewertungslob)
- EIN Detail: nie zwei oder drei Lobpunkte, Projekte, Titel oder Jahreszahlen aneinandergereiht;
  wird es zu lang, das schwächere Detail streichen
- höchstens 2 Sätze und zusammen höchstens 30 Wörter; meist ist es ein Satz, und der Schluss hängt
  mit einem Komma am Detail
- beginnt mit Kleinbuchstaben, weil es direkt auf „Hallo …,“ folgt; nur der erste Buchstabe ist
  klein, Substantive und Namen bleiben groß („Kunden loben …“)
- schreibt über den Empfänger, nie über den Absender
- Zuschreibung stimmt: der angeschriebenen Person nie etwas zuschreiben, das einer anderen gehört
  (der Podcast der Inhaberin in einer Mail an eine Mitarbeiterin). Meint eine Bewertung jemanden
  ohne Namen und hat der Betrieb mehrere davon, das Lob dem Betrieb zuschreiben („in deiner Praxis
  nimmt man sich Zeit“). Wachstum, Auszeichnungen oder Konzepte eines Franchisegebers oder einer
  Kette gehören nicht dem einzelnen Standort
- ein zweiter Satz ist konkret und nimmt nicht vorweg, was der feste Text danach sagt
- geht nahtlos in die feste Überleitung über, ohne ein Problem zu benennen
- locker und authentisch, wie eine kurze Nachricht an einen Bekannten

**NIEMALS:**

- Kritik, Defizit, Mangel, „Lücke“, „Hürde“, „Problem“, „leider“, „schade“
- Konjunktiv-Wunsch: „wäre (doch) schön/besser/sinnvoll, wenn …“
- „noch nicht“, „fehlt“, „begrenzt“, „veraltet“, „ausbaufähig“, „verschenkt Potenzial“,
  auditartige Formulierungen, Ratschläge
- Selbstvorstellung oder Pitch („Wir sind …“, „Mein Name ist …“, „Wir helfen …“)
- Floskeln: „Ich bin auf deine Webseite gestoßen“, „Tolle Webseite“, „das spricht für sich“, „das
  sieht man selten“, „hat man nicht alle Tage“, „finde ich stark“, „finde ich spannend“, „finde ich
  bemerkenswert“, „Hammer“, „beeindruckend“ ohne Detail. Auch nicht als Beispiel in Vorlagen:
  Beispiele werden kopiert
- erfundene Fakten, Personen, Rollen oder Zahlen; Kunden-, Projekt- oder Ergebniszahlen, die nur
  als Selbstangabe auf der Website stehen. Gründungsjahr mit seinem Ereignis und Teamgröße sind
  Tatsachen und erlaubt
- Quellenangaben im Behördenton („auf deiner Seite steht“); besser „ich hab gelesen, dass …“
- Fragezeichen, Ausrufezeichen, Links, Gedankenstriche, sichtbare Platzhalter
- Heikles als Aufhänger, auch wenn eine Bewertung es lobt: Preis, „günstig“, „faire Preise“;
  persönliche Merkmale von Rezensierenden (Alter, Herkunft, Sprache), ihre Familie und Umstände;
  sensible Gesundheitsdetails (Eingriffe, Diagnosen, Körperteile); negative Wörter aus Zitaten.
  Steht so etwas neben anderem Lob in derselben Bewertung, nur das andere Lob nehmen

## Beispiele (nicht wörtlich übernehmen)

| Anker | Intro |
|:------|:------|
| Eigenes Verfahren (Handwerk), Reaktion | „ich war gerade auf deiner Website: Du zeigst jedes Bad vorab als begehbaren 3D-Rundgang, das fand ich richtig schön.“ |
| Ungewöhnliche Zeit (Dental), Reaktion | „mir ist aufgefallen, dass deine Praxis donnerstags bis 20 Uhr Termine hat, das hat mich angesprochen.“ |
| Seltene Spezialisierung (Handwerk), Reaktion | „du baust ausschließlich Holzfenster für denkmalgeschützte Häuser, das ist mir direkt hängen geblieben.“ |
| Auszeichnung (Handwerk), ohne Schluss | „ich hab mir deine Website angeschaut und den Handwerkspreis für deine Fachwerksanierung entdeckt.“ |
| Lob aus Bewertungen (Dental), ohne Schluss | „ich hab mir deine Bewertungen angeschaut, und mehrere Patienten schreiben, dass du jeden Schritt vorher erklärst.“ |
| Lob aus Bewertungen (Shop), ohne Schluss | „ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, dass deine Lieferung schneller war als bei Amazon.“ |
| Bewertungszahl, Reaktion | „ich hab mir deine Bewertungen angeschaut: über 200 Rezensionen mit einem Schnitt von 4,8, das hat mir gut gefallen.“ |
| Stellenanzeige als Erkenntnis, Reaktion | „mir ist aufgefallen, dass du künftig deutlich mehr Eigenmarken ins Sortiment nimmst, das fand ich richtig sympathisch.“ |
| Eigenes Konzept (Dental), Würdigung als Ausnahme | „beim Stöbern auf deiner Website hab ich dein Kronen-Konzept entdeckt, die Krone am selben Termin. Respekt, dass du das an einem Tag hinbekommst.“ |

Gegenbeispiel gestapelte Lobpunkte (42 Wörter): „ich hab mir deine Bewertungen angeschaut, und
jemand schreibt, dass du ihm eine moderne, übersichtliche Website gebaut hast, die genau auf seine
Bedürfnisse abgestimmt war, und dass sich seine Sichtbarkeit bei Google spürbar verbessert hat,
dazu schnelle, zuverlässige Arbeit.“ Besser ein Detail: „ich hab mir deine Bewertungen angeschaut,
und jemand schreibt, dass nach der neuen Website spürbar mehr Anfragen über Google kamen.“

Gegenbeispiel Mechanik-Nutzen: „mir ist aufgefallen, dass auf deiner Website alle Preise offen
stehen, so können sich Interessierte vorab ein Bild machen.“ Besser: „…, das fand ich richtig
sympathisch.“

Gegenbeispiel Gutachten-Ton: „du betreibst ein Herren-Kosmetikstudio mit separatem Eingang, das
zeigt, wie klar der Betrieb auf seine Kundschaft ausgerichtet ist.“ Besser ohne Schluss oder: „…,
das hat mich angesprochen.“

## Der Fallback-Satz

Für Leads ohne belastbares Detail gibt es einen festen Satz je Kampagne, z. B. „als
[Branche]-Unternehmen in [Region] bist du genau die Art Firma, die wir suchen“ (ausgefüllt, ohne
Klammern). Er bleibt wörtlich, ohne angehängten Schluss, und behauptet nichts Unbelegtes über den
Lead („so gut bewertet“, „seit Jahren“, „viele zufriedene Kunden“).

**Lieber Fallback als Floskel.** Ein generischer Opener („deine Website macht einen professionellen
Eindruck“) verbrennt die einzige persönliche Stelle der Mail. Der Fallback ist trotzdem der
schwächste Weg (Antwortdaten: 4,5 % gegen 7,4 % mit Reaktion). Größter Hebel ist deshalb eine
bessere Anker-Suche, nicht ein schönerer Fallback.

Damit ein Intro entstehen kann, braucht jeder Lead eine Website oder Bewertungen. Ohne Grundlage
bleibt es zwangsläufig beim Fallback.

## Sonderfall: Storytelling mit Dialekt

Nur bei regionaler Zielgruppe und Dialekt-Tonalität, und nur, wenn der Absender selbst aus der
Region kommt. Nicht als Standard.

„Servus {{Vorname}}, i hab mi' vor kurzem mit einem Unternehmer aus unserer Region über Marketing
unterhalten. Er hat mir erzählt, dass es immer schwieriger wird, online aufzufallen. I dad mi'
interessieren, wie läuft die Neukundengewinnung bei dir?“

## Stichprobe vor dem Versand

Mindestens 10 fertige Intros von Hand lesen. Verwerfen und neu schreiben, wenn:

| Prüfung | Verwerfen wenn |
|:--------|:---------------|
| Länge | mehr als 2 Sätze, über 30 Wörter oder mehrere Lobpunkte aneinandergereiht |
| Schreibung | beginnt mit Großbuchstaben |
| Ton | Kritik, Mangel, Konjunktiv-Wunsch, Ratschlag |
| Austauschtest | passt auf zehn andere Betriebe der Branche, nennt eine Standardleistung, Lob nur als Adjektiv |
| Sperrliste | Anker steht auf der Sperrliste und ist kein Bewertungslob |
| Schluss | doppeltes Lob, Gutachten-Ton, „das zeigt, wie …“, Floskel, Mechanik-Nutzen, Vergleich ohne Beleg, leeres Prüfer-Urteil, Schluss am Fallback |
| Bewertungen | Zahlen unter 30 Bewertungen oder unter 4,5, ungerundet, Schnitt mit Punkt, „mehrere“ ohne zwei Belege, Einstieg ohne Quelle |
| Zuschreibung | schreibt der Person etwas zu, das einer anderen gehört |
| Wahrheit | Zahl, Name oder Fakt, der nicht aus der Recherche kommt |
| Form | Fragezeichen, Ausrufezeichen, Link, Gedankenstrich, Platzhalter |
| Übergang | die feste Überleitung schließt nicht flüssig an |

Fallen mehr als 2 von 10 durch, ist die Vorgabe das Problem, nicht der Lead: Regeln, Sperrliste
oder Recherche nachschärfen, dann neu schreiben.

---

# TEIL 3: Die Follow-ups

## Die Sequenz auf einen Blick

| Step | Rolle | Tag (Abstand) | Wörter max. | Betreff / Thread |
|:-----|:------|:--------------|:------------|:-----------------|
| 1 | Entry Mail | 0 | 120 (Ziel 50-90) | eigener Betreff, öffnet den Thread |
| 2 | Erinnerung | 3 (+3) | 50 | leer, antwortet im Thread von Step 1 |
| 3 | Neuer Winkel mit Social Proof | 8 (+5) | 80 | leer, antwortet im Thread von Step 1 |
| 4 | Abschied mit Routing-Hinweis | 15 (+7) | 60 | leer, antwortet im Thread von Step 1 |

Standard sind vier Steps. Praxis-Belege: Eric Nowoslawski arbeitet mit zwei bis drei Mails, Jay
mit vier Steps und Routing, ohne künstliche Knappheit; Step 3 im selben oder einem neuen Thread
ist bei Jay ein Test. Seit 05.11.2026 laufen alle vier Mails in einem Thread (Giuliano): Step 3
hat keinen eigenen Betreff mehr, Step 4 verabschiedet sich mit dem Routing-Hinweis.

**Wortzahlen sind Obergrenzen, keine Ziele.** Gezählt wird der Body ohne Betreff und Signatur,
Anrede und Intro eingerechnet (das Intro mit bis zu 30 Wörtern). Bewährte Entry Mails liegen bei 55
bis 86 Wörtern, die kürzeste empfohlene Erinnerung hat 14. Wenn drüber: kürzen, nicht
umformulieren. Aufgefüllt wird nie.

Regeln für alle Follow-ups:

- Follow-ups sind keine Wiederholungen. Jedes hat eine Aufgabe und höchstens EINEN neuen Aspekt.
- Das Offer steht nur in Step 1. Step 3 nennt es nur in der Schlussfrage: dieselbe Frage wie in
  Step 1, mit dem Wort für die Sache statt „es“.
- Kein Intro in den Follow-ups. Ein zweiter personalisierter Bezug wirkt wie ein Skript.
- Jedes beginnt mit „Hallo {{Vorname}},“ und dann einem ganzen, weichen Satz, klein
  weitergeschrieben („du hast sicher …“). Kein Doppelpunkt-Opener („kurz nachgehakt:“, „kurzes
  Update:“, „zur Erinnerung:“).
- Der CTA wird von Step zu Step weicher: Erlaubnis erbitten → nur anstoßen → dieselbe Frage wie
  Step 1 mit der Sache → Tür offen lassen.

| Step | CTA-Charakter | Beispiel |
|:-----|:--------------|:---------|
| 1 | Erlaubnis erbitten | „Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“ |
| 2 | nur anstoßen | „Gib mir gerne kurz Bescheid.“ |
| 3 | Frage aus Step 1, mit der Sache | „Wäre es in Ordnung, wenn ich dir morgen den Entwurf zusende? Völlig unverbindlich natürlich.“ |
| 4 | Tür offen lassen | „Sag mir gern kurz Bescheid, falls ich mich besser bei jemand anderem melden sollte.“ |

## Step 2: Erinnerung

Nur nachhaken. Kein Offer, kein neuer Aspekt, kein Intro. Darf sich anfühlen wie eine Nachricht,
die in zehn Sekunden getippt wurde.

| Variante | Text |
|:---------|:-----|
| Weich | „Hallo {{Vorname}}, du hast sicher viel um die Ohren. Ich wollte nur sichergehen, dass meine Mail angekommen ist. Gib mir gerne kurz Bescheid.“ |
| Ultra-kurz | „Hallo {{Vorname}}, ist meine Mail von neulich angekommen? Gib mir gerne kurz Bescheid.“ |
| Locker | „Hallo {{Vorname}}, ich wollte nur kurz nachhaken, ob du meine Mail gesehen hast. Vielleicht ist sie im Trubel untergegangen. Gib mir gerne kurz Bescheid.“ |

„Letzte Woche“ nur schreiben, wenn der Abstand das hergibt. Bei drei Tagen „neulich“ oder „vor ein
paar Tagen“.

## Step 3: Neuer Winkel mit Social Proof

EIN neuer Aspekt, und **hier steht der Social Proof**, nie früher. In der Entry Mail wirkt Proof
wie ein Pitch, hier wie ein Beleg.

Betreff leer, die Mail läuft im Thread von Step 1 (seit 05.11.2026, vorher eigener Betreff „kurzes
Update“ und neuer Thread). Sie bleibt trotzdem ohne Mail 1 verständlich.

Aufbau: Anrede, der Beleg als erster Absatz (nach „Hallo {{Vorname}},“ klein weiter wie in Mail 1,
auch in der Sie-Form: „ein Bauunternehmen aus …“, „bei rund 80 Gründungen …“), höchstens ein kurzer eigener Satz, dann dieselbe Schlussfrage wie in
Mail 1, mit dem Wort für die Sache statt „es“ (Karte C: „Wäre es in Ordnung, wenn ich dir morgen den
Entwurf zusende? Völlig unverbindlich natürlich.“). Karten ohne Wort für die Sache (B, D, E, eine
eigene Frage ohne Stelle dafür oder eine Kampagne ohne Wort) nehmen die Frage aus Mail 1 wörtlich: Mail 3 endet immer mit einer Frage, eine bloße
Aufforderung wie „sag einfach kurz Bescheid“ reicht nicht (05.11.2026). Das Wort für die Sache steht nur in dieser Frage;
kein eigener Satz um das Angebot („Falls du den Entwurf sehen möchtest, antworte kurz“), kein neues
Offer, kein Pitch. Mail 3 endet mit genau einer Frage, nie mit einer Aussage („schick ich dir gern“)
oder Bitte; jede Variante unten endet mit der Frage aus Mail 1 ihrer Karte.

| Variante | Text |
|:---------|:-----|
| Case Study | „Hallo {{Vorname}}, letzte Woche hatte ich einen Händler im Gespräch, der zwei Jahre lang gekämpft hat, seinen Amazon-Account wieder freizuschalten. Am Ende hat ihn eine falsche Handynummer endgültig rausgeworfen. Genau solche Geschichten zeigen, warum ein starker eigener Shop so wichtig ist. Wäre es in Ordnung, wenn ich dir morgen den Shop-Entwurf zusende? Völlig unverbindlich natürlich.“ |
| Konkretes Ergebnis | „Hallo {{Vorname}}, wir haben gerade ein Pilotprojekt mit einem Handwerksbetrieb abgeschlossen. Der Betrieb spart jetzt über 15 Stunden pro Woche, weil die Auftragsabwicklung automatisiert läuft. Wärst du grundsätzlich offen dafür?“ |
| Relevanter Fakt | „Hallo {{Vorname}}, bei Unternehmen mit bis zu 49 Mitarbeitern liegt die Förderquote aktuell bei bis zu 100 % der Weiterbildungskosten. Dein Team lernt neue Skills und der Staat zahlt den größten Teil. Wäre es in Ordnung, wenn ich dir kurz aufschreibe, welches Programm für dich infrage kommt? Völlig unverbindlich natürlich.“ |

- Eine Geschichte, eine Zahl, ein Ergebnis. Keine Kundenliste, keine Logo-Parade.
- Nur Belege, die der Absender angegeben hat. Fehlt ein Beleg: nachfragen, nicht erfinden.
- Den Beleg wörtlich übernehmen, wie der Absender ihn angegeben hat: Zahlen genau so, kein „bis zu“,
  „über“ oder anderer Zusatz, der nicht in der Angabe steht (Lauf 4 am 06.11.2026: aus „neun“ wurde
  „bis zu neun“). Ein Ergebnis bleibt ein berichtetes Ergebnis, nie eine Zusage.
- Ab Step 3 höchstens ein Link (nur Kalender oder Website).

## Step 4: Abschied mit Routing-Hinweis

Tür offen lassen, ohne Druck und ohne Vorwurf, und mit einem Satz klären, ob jemand anderes der
bessere Ansprechpartner ist. Läuft im Thread von Step 1, Betreff leer.

„Hallo {{Vorname}}, da ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht
passt. Das ist absolut in Ordnung. Sag mir gern kurz Bescheid, falls ich mich damit besser bei
jemand anderem im Team melden sollte. Alles Gute!“

Kennt die Recherche die richtigen Ansprechpartner namentlich, geht auch: „Hallo {{Vorname}}, ich
bin mir nicht sicher, ob ich damit bei dir richtig bin oder eher bei Anna oder Tom. Gib mir gern
kurz Bescheid.“ Nur mit belegten Namen.

Kein Vorwurf, keine letzte Chance, keine künstliche Knappheit. Der Abschied bringt erfahrungsgemäß
mehr Antworten als eine Dringlichkeits-Mail, gerade weil er nichts will und eine leichte Antwort
erlaubt („schreib Anna“).

## Optional: Dringlichkeit als Zusatz-Step

Kein Standard. Nur wenn der Absender einen echten Zeit- oder Kapazitätsgrund nennt, kommt ein Step
zwischen Step 3 und den Abschied: dann fünf Steps (Tag 0, 3, 8, 15, 22), höchstens 60 Wörter,
Betreff leer, im Thread von Step 1.

| Variante | Text |
|:---------|:-----|
| Kapazität | „Hallo {{Vorname}}, für das Pilotprojekt in der Region ist aktuell noch ein Platz frei. Ich wollte kurz abklären, ob das Thema für dich relevant ist, bevor er vergeben ist. Gib mir einfach kurz Bescheid.“ |
| Zeitfenster | „Hallo {{Vorname}}, die Fördertöpfe werden jährlich neu vergeben und sind ab dem dritten Quartal erfahrungsgemäß knapper. Falls du dieses Jahr noch profitieren willst, melde dich gerne.“ |

Erfundene Dringlichkeit merkt der Empfänger, und dann ist auch die Entry Mail rückwirkend
unglaubwürdig. Ohne echten Grund entfällt der Step.

## Wenn Antworten kommen, aber keine Termine

Dann ist nicht die Sequenz das Problem, sondern meist das fehlende Nachtelefonieren. Das ist der
Schritt, den Kunden am häufigsten überspringen und der die Terminquote am stärksten verändert.

---

# TEIL 4: Betreffzeilen

Nur Step 1 trägt einen Betreff, weil nur er den Thread öffnet. Step 2, Step 3 und Step 4 (und ein
Dringlichkeits-Step) lassen ihn leer und laufen im Thread von Step 1. Kein eigener Text, kein „Re:“.

Regeln für jeden Betreff:

- 2-5 Wörter, klingt wie die harmlose Frage eines Menschen (der persönliche Betreff im Betreff-Test
  3 bis 6, siehe unten)
- keine Ankündigung und keine Ergebnisansage: nicht „Website für …“, „Entwurf für …“, „Idee für …“,
  „Website ist fertig“. Das Angebot gehört in den Body
- kein Spam-Wort, kein „kostenlos“, „kostenfrei“, „gratis“, „unverbindlich“
- keine Großschreibung ganzer Wörter, kein Ausrufezeichen, kein Prozentzeichen
- kein Vorname im Betreff. Ein Firmenname nur über `{{Firma}}` (bereinigter Kurzname); fehlt das
  Feld, steht kein Name im Betreff

| Betreff | Wann |
|:--------|:-----|
| „kurze Frage“ | Standard für jede Karte (seit 05.11.2026, wie die App) |
| „Frage zur Terminbuchung“ | wenn das Buchungssystem den Kern des Offers bildet |
| „Zugang freigeschaltet“ | nur, wenn es den Zugang wirklich gibt (etwa den Platz im Pilotprojekt). Enttäuschte Neugier ist der kürzeste Weg zur Spam-Beschwerde |

Nicht: „Kostenlose Beratung für …“ (zu lang, Spam), „Exklusives Angebot, jetzt zugreifen!“
(Spam-Trigger), „Re: Ihre Anfrage“ (Fake-Reply, zerstört Vertrauen).

## Betreff-Test: persönlicher Betreff in Variante B

Seit 05.11.2026 legt der Assistent von ListM8 einen Betreff-Test an (ab Werk an): Variante B von
Mail 1 ist wörtlich Variante A, nur mit dem Betreff `{{ai.betreff_b}}`, den die KI je Lead schreibt.
Variante A behält „kurze Frage“. Ist der Intro-Test zusätzlich an, läuft er als Variante C mit
„kurze Frage“ und `{{ai.intro_c}}`. Der Prompt der Variable kommt vom Server (`get_lead_data`,
`emailGeneration.subjectVariables`); Regeln für den persönlichen Betreff (SOP vom 05.11.2026):

- 3 bis 6 Wörter, Ziel 4 bis 5; der Firmenname zählt als ein Wort, kein ganzer Satz; zwei Wörter
  lesen sich wie ein Etikett und gelten als Verstoß
- genau ein belegtes Detail, und zwar dasselbe, mit dem das Intro beginnt (der Betreff stellt die
  Frage, die erste Zeile löst sie ein)
- beginnt direkt mit dem Detail („Dachsanierung am Hansmeyerhof“, „Traufblechmontage bei Nitz“),
  nie mit „Frage zu/zum/zur …“ oder „kurze Frage zu …“, englisch nie mit „question about …“: diese
  Form hat allein der Rückfall, damit echte Betreffs und Rückfälle in der Auswertung unterscheidbar
  sind; ListM8 zählt einen Betreff in dieser Form immer als Rückfall (E53, 06.11.2026)
- klingt wie die harmlose Frage oder Notiz eines Menschen: kein Angebot, kein Ergebnis, keine
  Ankündigung, kein Lob, auch kein wertendes Wort zum Detail („Pragmatische Lösungen von Artd“)
- nur der Gegenstand, wie das Intro ihn nennt, ohne Zusatz: keine Wirkung, kein Kanal, keine Anfragen
  oder Zahlen, die das Intro nicht nennt (nicht „Anfragen über Ads bei Flowers“, wenn das Intro nur
  die Anzeigen nennt)
- Firmenname nur als Kurzname ohne Rechtsform; erstes Wort klein, wenn es kein Substantiv ist
- höchstens ein Fragezeichen am Ende; kein Ausrufezeichen, kein %, keine Anführungszeichen, keine
  Gedankenstriche, kein Emoji, keine Großbuchstaben-Wörter
- am besten ohne Pronomen, sonst nach der Anrede (dein/euer bzw. Ihr); zeitlos, weil Mail 2 bis 4
  drei Wochen lang als „Re: …“ darunter laufen
- verboten: Vorname, vorgetäuschte Kundenanfrage („ich suche eine Fassadenfirma“), Privates,
  „Re:“/„AW:“/„Fwd:“, Spam-Wörter (auch „Angebot“, „unverbindlich“)
- Rückfall ohne belegtes Detail: „Frage zu {{Firma}}“ mit dem Kurznamen aus `firma`, „kurze Frage“
  nur ohne sicheren Kurznamen; gemeldet mit `betreff_b__rueckfall: "ja"`. Trägt das Intro ein Detail,
  ist es kein Rückfall. Nie leer, nie erfunden. Nur der Rückfall beginnt mit „Frage zu“.

Gut: „3D-Rundgang bei Bad Becker“, „Dachsanierung am Hansmeyerhof“, „Traufblechmontage bei Nitz“,
„Samstagskurse im Studio Mitte“. Schlecht: „Frage zur Dachsanierung am Hansmeyerhof“ (Form des
Rückfalls), „Mehr Patienten für Zahnarzt Müller“, „Anna, tolle Google-Bewertungen!“.
`save_lead_variables` ersetzt einen Betreff, der eine harte Regel bricht, durch „Frage zu
{{Firma}}“ mit dem Wert von `firma`, ohne nutzbaren Kurznamen durch den Betreff von Variante A
(„kurze Frage“), und markiert ihn als Rückfall; ebenso einen nackten Standard-Betreff, wenn `firma`
gesetzt ist (seit 06.11.2026). In `check_copy.py` steht er als Zeile
„Betreff B: …“ unter „Betreff: …“; den Kurznamen der Firma (zählt als ein Wort) gibt `--firma` oder
eine Zeile „Kurzname: …“ an.

---

# TEIL 5: Verbote und Zustellung

## Harte Verbote im Body jeder Mail

- Kein Pitch, keine Selbstvorstellung (siehe Teil 1).
- Kein zweiter CTA („Antworte mir oder buche hier …“).
- Kein Link in Mail 1. Ab Step 3 höchstens einer (nur Kalender oder Website).
- Kein Fettdruck, keine Aufzählungszeichen, keine Emojis, kein HTML-Layout, keine Bilder, keine
  Anhänge.
- Keine Gedankenstriche als Trenner (siehe Tonalität).
- Kein Doppelpunkt-Opener in Follow-ups.
- Keine sichtbaren Platzhalter („[Branche]“, „[Name]“).
- Social Proof und Case Studies NUR in Step 3.
- Verbotene Offer-Begriffe: „kostenlose Analyse“, „kostenlose Beratung“, „kostenloses
  Erstgespräch“, „unverbindliches Audit“, „Potenzial-Check“, „Strategiegespräch“, allgemein
  „Analyse“, „Audit“, „Beratung“, „Erstgespräch“ als Offer. Immer ein Deliverable statt eines
  Gesprächs.

## Spam-Wörter

Im Betreff komplett verboten, im Body vermeiden:

„gratis“, „100 %“, „garantiert“, „Garantie“, „jetzt zugreifen“, „jetzt handeln“, „begrenztes
Angebot“, „nur heute“, „exklusives Angebot“, „hier klicken“, „Rabatt“, „Sonderpreis“, „Gewinner“,
„Sie haben gewonnen“, „dringend“, „risikofrei“, „ohne Risiko“, „Geld verdienen“.

„unverbindlich“ ist im Body kein Spam-Wort, der Standard-CTA endet mit „Völlig unverbindlich
natürlich.“ Im Betreff bleibt es verboten.

**„kostenlos“:** im Betreff nie (auch nicht „kostenfrei“ oder „gratis“). Im Body höchstens einmal
und nur direkt am konkreten Deliverable („ein kostenloses Google Ads Setup“), nie als Eigenschaft
der Zusammenarbeit („ein kostenloses Erstgespräch“), nie zusammen mit einem zweiten Trigger. Ein
vages Angebot wird von dem Wort verdächtig, ein konkretes nicht.

**„100 %“:** im Body nur als Sachinformation und als Spanne („bis zu 100 %“), nie im Betreff.

## KI-Sprache vermeiden

| Verdächtig | Besser |
|:-----------|:-------|
| „In der heutigen schnelllebigen Geschäftswelt …“ | weglassen |
| Gedankenstriche | Satz teilen oder Komma |
| „Ich hoffe, diese Nachricht erreicht dich gut“ | weglassen, direkt zum Bezug |
| „Lass mich wissen, wenn du Interesse hast“ | die Schlussfrage der Karte („Wäre das grundsätzlich interessant?“) |
| „Gerne möchte ich dir aufzeigen …“ | „Ich zeig dir kurz …“ |
| „Darüber hinaus“, „Nicht zuletzt“, „Zusammenfassend“ | in einer 100-Wort-Mail hat nichts davon Platz |
| „Synergien“, „ganzheitlich“, „nachhaltig skalieren“ | konkret sagen, was passiert |
| „Ich freue mich auf deine Rückmeldung“ | weglassen, die Schlussfrage reicht |
| drei Adjektive in einer Reihe | eines reicht, meistens keines |

## Zustellung

| Regel | Warum |
|:------|:------|
| Plain Text, kein HTML-Layout | gestaltete Mails sehen für Spam-Filter aus wie Newsletter |
| kein Link in der Entry Mail | der CTA ist die Antwort; ein Link im Erstkontakt ist ein Automations-Signal |
| keine Anhänge, keine Bilder, keine Logos | sofort verdächtig; Material erst nach der Antwort |
| keine Großschreibung ganzer Wörter | klassisches Spam-Merkmal, besonders im Betreff |
| Abmeldezeile unter der Signatur | der feste, menschliche Satz aus „Abmeldezeile“ (Teil 1), keine Opt-out-Fachsprache; den technischen Abmeldelink setzt das Versandtool zusätzlich. Wer keinen Abmeldeweg findet, klickt auf Spam |

Die Spam-Beschwerdequote muss unter **0,3 %** bleiben, das ist der Schwellenwert der großen
Postfach-Anbieter. Was sie treibt, ist fast immer Copy: irreführende Betreffs, ein Offer, das die
Mail nicht hält, kein erkennbarer Abmeldeweg oder eine Zielgruppe, für die die Mail keinen Sinn
ergibt.

---

# TEIL 6: Selbstprüfung

Prüfen ist kein Geschmacksurteil. Fast alles, was eine Mail killt, ist messbar: Wortzahl, Anzahl
der CTAs, verbotene Formulierungen, Sonderzeichen. Prüfen heißt fast immer streichen.

## Der Prüfdurchlauf

Jede Mail in dieser Reihenfolge. Bei jedem Fehler korrigieren und **von vorne** beginnen:
Korrekturen erzeugen neue Fehler, besonders beim Kürzen.

1. **Als Empfänger lesen.** Würdest du antworten? Wenn nein: warum nicht?
2. **Absender-Check.** Geht jeder Satz über den Empfänger? Jeder Satz über uns fliegt raus, außer
   der Signatur.
3. **Pitch-Scan.** „wir helfen“, „wir sind“, „wir machen“, „wir bieten“, „seit … Jahren“, „als …
   Partner“, „mein Name ist“, „unser Unternehmen“?
4. **CTA zählen.** Genau einer?
5. **Wörter zählen.** Step 1-4 höchstens 120 / 50 / 80 / 60, Dringlichkeit 60. Drüber: kürzen.
6. **Zeichen-Scan.** Gedankenstriche, Emojis, Fettdruck, Aufzählungen, Links in Step 1, gerade
   Anführungszeichen, Zeichen für Zeichen.
7. **Spam-Scan.** Betreff und Body gegen die Liste, „kostenlos“ höchstens einmal im Body.
8. **Struktur-Scan.** Offer nur in Step 1, Intro nur in Step 1, Social Proof nur in Step 3, Step 3
   endet mit der Schlussfrage aus Step 1 (Wort für die Sache statt „es“),
   zweiter Satz zum Angebot passend zur Karte (C Feinheiten-Satz, A und B Satz je Lead, D und E
   keiner), kein „Link“ im Schlusssatz, Betreff nur in Step 1 (Step 2 bis 4 im Thread), kein Doppelpunkt-Opener,
   Abmeldezeile unter der Signatur von Step 1 und 3, kein „STOPP“ und keine Opt-out-Fachsprache.
9. **Anrede-Scan.** Gruß und Pronomen passen zum Modus, kein du/ihr-Wechsel im Satz, Fallback
   „Hallo,“ für Leads ohne Vornamen geklärt.
10. **Platzhalter-Scan.** Keine [Klammer-Felder], jeder `{{…}}`-Platzhalter ist für jeden Lead
    gefüllt, Signatur als Klartext.
11. **Umlaut-Scan.** Kein „ae“, „oe“, „ue“, „ss“ als Ersatz für ä, ö, ü, ß.
12. **Austauschtest.** Würde das Intro genauso auf zehn andere Betriebe der Branche passen? Dann
    nächster Anker, zuletzt der Fallback.

## Mechanisch prüfbar

Diese Regeln prüft das Skript `check_copy.py`. „Hart“ ist ein Fehler, „weich“ ein Hinweis, der
begründet werden muss.

| Regel | Prüfung | Stufe |
|:------|:--------|:------|
| Wortlimit | Step 1-4 max. 120 / 50 / 80 / 60, Dringlichkeit 60 (Intro mit 30 Wörtern eingerechnet) | hart |
| Zielkorridor | Entry Mail unter 50 Wörtern | weich |
| Gedankenstrich | kein Halbgeviert- oder Geviertstrich | hart |
| Trenner | kein „ - “ außerhalb der Signaturzeile | weich |
| Anführungszeichen | jedes „ schließt mit “, kein gerades Zeichen | hart |
| Kein Pitch | „wir helfen“, „wir sind ein/eine/der/die/seit“, „wir bieten“, „seit (über) N Jahren“, „als … Partner“, „mein Name ist“, „unser Unternehmen“ | hart |
| Kein Platzhalter | kein sichtbares [Feld] | hart |
| Kein Emoji | keine Emojis oder Symbole | hart |
| Formatierung | kein Fettdruck, keine Zeile mit „-“, „*“ oder „•“ am Anfang | weich |
| „kostenlos“ | höchstens einmal pro Mail | weich |
| Spam im Body | Wort aus der Spam-Liste | weich |
| Betreff ohne Spam | kein Spam-Wort, kein „kostenlos“, „kostenfrei“, „unverbindlich“ | hart |
| Betreff-Länge | max. 5 Wörter | weich |
| Betreff-Platzhalter | kein Vorname im Betreff | hart |
| Betreff-Pflicht | Step 1 mit Betreff, Step 2 bis 4 und Dringlichkeit ohne (Thread von Step 1) | hart |
| Betreff ohne Schreien | kein Wort in Großbuchstaben (ab 4), kein „!“ | weich |
| Ankündigung im Betreff | „… für …“, „Entwurf“, „Idee“, „ist fertig“ | weich |
| Ein CTA | kein „oder … buchen/klicken/vereinbaren/anrufen/Termin“ neben der Antwort-Bitte | hart |
| Kein Link in Mail 1 | kein „http“, „www.“, „calendly“ in Step 1 | hart |
| Links ab Step 3 | höchstens einer | weich |
| Offer ist kein Gespräch | kein verbotener Offer-Begriff in Step 1 (außer verneint: „statt …“, „kein …“) | hart |
| Intro nur in Step 1 | `{{Intro}}` in keinem Step ab 2 | hart |
| Doppelpunkt-Opener | Follow-up beginnt nach dem Gruß nicht mit „…:“ | hart |
| Umlaute | keine Transliteration (fuer, ueber, gruess, koennen, moechte, persoenlich, waere …) | hart |
| Keine Opt-out-Fachsprache | kein „STOPP“, „Stop“, „abmelden“, „abbestellen“, „austragen“, „unsubscribe“, „Opt-out“, auch nicht unter der Signatur | hart |
| Abmeldezeile | Step 1 und 3 mit der festen Abmeldezeile unter der Signatur | weich |

## Das Wichtigste

Ohne Detail kein Beweis. Eine echte Bewertung, ein echtes Verfahren, eine echte Auszeichnung ist der
Unterschied zwischen einer Mail, die persönlich wirkt, und einer, die es nur behauptet.

Schreib über den Empfänger, nie über den Absender. Vier kurze Mails mit je einem Gedanken schlagen
zwei lange mit je fünf. Beim Prüfen sind zwei Drittel Streichungen und ein Drittel Zeichen zählen.
Nur der erste Schritt, „würde ich antworten?“, ist Ermessen, und der entscheidet am Ende trotzdem
alles.
