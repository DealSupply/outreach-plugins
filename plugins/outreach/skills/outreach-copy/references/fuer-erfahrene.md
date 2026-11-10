# Für Erfahrene: Tests in Mail 1 und „Angebot je Lead“

> Referenz zu `outreach-copy` und `outreach-campaign`. Beides ist optional und standardmäßig aus,
> wie in der App (Weg A, seit outreach 0.7.0). Eine neue Kampagne startet ohne Tests, mit einem
> Angebot für alle Leads und dem festen zweiten Satz ihrer Karte. Dieses Dokument beschreibt, was
> das Plugin auf ausdrücklichen Wunsch zusätzlich anlegt, mit denselben Feldern, Vorlagen und
> Namen wie die App.

Die Texte in „…“, die der Kunde zu sehen bekommt, sind die Texte der App bzw. die beim Bau
abgenommenen Ergänzungen (Kundentexte Weg A, „Ergänzt beim Bau“, W18, W20). Wortgetreu übernehmen,
nicht umformulieren. Englische Kampagnen nehmen die englische Spalte.

## Die eine Frage beim Anlegen

`outreach-campaign` stellt sie genau einmal, nach dem Briefing und bevor der Blueprint entsteht,
unter der Überschrift „Für Erfahrene“ („For experienced users“). Beim Bearbeiten einer bestehenden
Kampagne wird nicht gefragt und nichts umgestellt.

**Tests in Mail 1** („Für Erfahrene: Tests in Mail 1“ · „For experienced users: tests in email 1“),
je Test eine Zeile mit dem Satz der App:

| Test | Deutsch | Englisch |
|---|---|---|
| Betreff | „Betreff testen“: „Ein Teil der Leads bekommt „Frage zu“ mit dem Firmennamen statt „kurze Frage“.“ | “Test the subject”: “Some leads get “question about” with the company name instead of “quick question”.” |
| Intro | „Intro testen“: „Ein Teil der Leads bekommt ein zweites Intro mit anderem Detail.“ | “Test the intro”: “Some leads get a second intro with a different detail.” |

Empfehlung ist „Ohne Tests (empfohlen)“ („Without tests (recommended)“) und ist vorausgewählt. Wer
beide wählt, bekommt beide.

**„Angebot je Lead“** („Offer per lead“), nur bei Karte A (Kostenlose Teildienstleistung, in der App
„Kostenlose Teilleistung“) und Karte C (Konkretes Deliverable, in der App „Schon erledigte
Vorarbeit“), nur ab ListM8-MCP 4.15.0 (`ping`):

| Ort | Deutsch | Englisch |
|---|---|---|
| Zeile zur Option | „Die KI wählt je Lead aus deinen Angeboten das passende und schreibt den Angebotsteil von Mail 1.“ | “For each lead, the AI picks the matching offer from yours and writes the offer part of email 1.” |
| Auswahl | „Angebot je Lead“ oder „Ein Angebot für alle (Standard)“ | “Offer per lead” or “One offer for all (default)” |
| Karte B (Pilot) und D (Förderung), statt der Option | „Bei {Form} steht in Mail 1 für alle Leads derselbe Angebotsteil.“ | “With {form}, email 1 has the same offer part for all leads.” |
| Karte E (Partner), statt der Option | „Bei Partner steht in Mail 1 für alle Leads derselbe Satz.“ | “With Partner, email 1 has the same sentence for all leads.” |

`{Form}` ist der Name der Karte in der App: „Pilotprojekt“, „Förderung“ („Pilot project“,
„Funding“). Den Satz für B, D und E nur nennen, wenn der Nutzer nach „Angebot je Lead“ fragt.

Ohne Wahl gilt: keine Tests, ein Angebot für alle.

## Teil 1: Tests in Mail 1

Gleich gebaut wie im Assistenten der App: Variante A ist Mail 1, wie sie ist. Der Betreff-Test kommt
zuerst und ist Variante B, der Intro-Test die nächste freie Variante. Beide zusammen ergeben A, B und
C. Die Follow-ups sind für alle Varianten gleich; außer Betreff bzw. Intro ändert sich nichts.

| Gewählt | Varianten von Step 1 | Neue Variablen |
|---|---|---|
| nur Betreff | B: Betreff `{{ai.betreff_b}}`, Body wörtlich wie A | `betreff_b` |
| nur Intro | B: Betreff wie A, Body wie A mit `{{ai.intro_b}}` statt `{{ai.intro}}` | `intro_b` |
| beide | B wie „nur Betreff“, C: Betreff wie A, Body wie A mit `{{ai.intro_c}}` statt `{{ai.intro}}` | `betreff_b`, `intro_c` |

Im Blueprint (ab MCP 4.11.0) stehen sie unter `sequence.steps[0].variants`, je
`{"subject": …, "body": …, "active": true}`. Die Variablen:

- **Betreff von B** `betreff_b` mit `"role": "subject_variant"`, `"title": "Betreff Variante B"`,
  `"description": "Betreff der Variante B von Mail 1: „Frage zu <Kurzname>“ mit dem Kurznamen der Firma. Ohne sicheren Kurznamen der Betreff von Variante A, als Rückfall markiert."`
  (englisch `"Subject variant B"`, `"Subject of variant B of email 1: \"question about <short name>\" with the company's short name. Without a reliable short name the subject of variant A, marked as a fallback."`).
  Der Prompt ist wörtlich der des Servers. Die Zeile „- FORM: …“ muss genau so stehen: An ihr
  erkennt ListM8, dass B „Frage zu <Kurzname>“ heißt und den Betreff selbst aus `firma` setzt.

  Deutsch:

  ```
  Betreff von Variante B in Mail 1 (Betreff-Test): die Frage zur Firma des Leads. Variante A trägt den Betreff von Mail 1 (im festen Mailtext), sonst sind A und B gleich.
  - FORM: Der Betreff lautet immer „Frage zu <Kurzname>“, kein Detail, kein Vorname und kein anderer Wortlaut.
  - KURZNAME: derselbe wie unter firma, so, wie ein Mensch die Firma nennt: ohne Rechtsform (GmbH, GmbH & Co. KG, e.K., UG, Ltd), ohne Zusätze wie „Meisterbetrieb“ und ohne Ort, in normaler Schreibweise statt in Großbuchstaben, außer die Firma führt ihren Namen als Kürzel („ZAR“). Steckt der Vorname der angeschriebenen Person im Firmennamen, fällt er weg („Immobilien Thomas Braun“ wird „Immobilien Braun“).
  - PRÜFUNG: Der Server setzt den Betreff aus dem Kurznamen zusammen und prüft ihn gegen Firmennamen und Website; ohne sicheren Kurznamen bekommt der Lead den Betreff von Variante A.
  - MELDUNG (Pflicht): Unter dem Schlüssel betreff_b__rueckfall meldest du "ja", wenn es keinen sicheren Kurznamen gibt, sonst "nein". Er ist keine Variable und kommt nie in die Mail.
  Gut: „Frage zu Becker Bäder“, „Frage zu Immobilien Braun“, „Frage zu ZAR“.
  Schlecht: „Frage zu Becker Bäder GmbH & Co. KG“ (Rechtsform), „Frage zu MÜLLER BAU“ (Großbuchstaben), „Frage zu Immobilien Thomas Braun“ (Vorname), „Dachsanierung am Hansmeyerhof“ (Detail statt Firma).
  Gib nur den Betreff aus.
  ```

  Englisch:

  ```
  Subject of variant B in email 1 (subject test): the question about the lead's company. Variant A carries the subject of email 1 (in the fixed email text), otherwise A and B are the same.
  - FORM: the subject is always "question about <short name>", no detail, no first name and no other wording.
  - SHORT NAME: the same as under firma, as a person names the company: without the legal form (LLC, Inc, Ltd, GmbH), without additions and without the place, in normal case instead of capitals unless the company goes by an abbreviation ("ZAR"). If the first name of the person the email goes to is part of the company name, it is left out ("Thomas Brown Realty" becomes "Brown Realty").
  - CHECK: the server builds the subject from the short name and checks it against the company name and the website; without a reliable short name the lead gets the subject of variant A.
  - REPORT (mandatory): under the key betreff_b__rueckfall report "ja" when there is no reliable short name, otherwise "nein". It is not a variable and never appears in the email.
  Good: "question about Acme Roofing", "question about Brown Realty", "question about ZAR".
  Bad: "question about Acme Roofing Services LLC" (legal form), "question about ACME ROOFING" (capitals), "question about Thomas Brown Realty" (first name), "storm repairs at Acme Roofing" (detail instead of the company).
  Return only the subject.
  ```

- **Zweites Intro** `intro_b` (bzw. `intro_c` neben dem Betreff-Test) mit `"role": "intro_variant"`,
  wörtlich dem Prompt von `intro` und `"description": "Intro der Variante B von Mail 1: das nächstbeste Intro mit einem anderen Anker. Gibt es keinen weiteren guten Anker, steht hier wörtlich das Intro aus Variante A."`
  (bei `intro_c` „Variante C“; englisch `"Intro of variant B of email 1: the next best intro with a different anchor. Without another good anchor it carries the intro of variant A word for word."`).
  Welches Intro wohin gehört, regelt der Server bei der Generierung (`emailGeneration.introVariables`).

Regeln für einen sauberen Test bleiben: genau ein Hebel je Variante, gleiches Angebot, gleiche
Follow-ups. Die Launch-Checkliste (`outreach-launch`) nennt den Test nur, wenn er gewählt ist.

## Teil 2: „Angebot je Lead“

Eine KI-Variable mit Vorlage statt eines Systems: Die KI wählt je Lead eines der Angebote des
Kunden und schreibt den zweiten Absatz; den ersten und dritten Absatz des gewählten Angebots setzt
ListM8 selbst ein. Ohne die Option bleibt Mail 1 beim festen Angebotssatz, dem festen zweiten Satz
und der Schlussfrage.

### Wann

- Nur Karte A und C (W1). Bei B, D und E gibt es die Option nicht.
- Beim Anlegen einer neuen Kampagne (`create_campaign`) oder beim Füllen einer genannten leeren
  Kampagne. Eine bestehende Kampagne nur auf ausdrücklichen Wunsch und nur, solange noch kein Lead
  Mails hat (`list_leads` mit `campaign_status` `"pending_review"`, `"approved"` und `"rejected"` leer;
  auch ein abgelehnter Lead hat Werte): dann per
  `edit_campaign` (Vollersatz aus dem Export) genauso gebaut wie beim Anlegen. Haben Leads schon
  Mails, ginge das über den Blueprint nicht: Diese Leads zeigten „[NOT GENERATED]“. Dann geht es nur
  in der App (Angebots-Blatt, Schalter „Angebot je Lead“, dort trägt ListM8 die bisherigen Absätze
  als Werte ein), und den Schalter gibt es dort nur, wenn die Kampagne eine Station trägt (im Export
  steht `campaign.station`). Standard-Kampagnen aus dem Plugin haben keine; das dem Nutzer so sagen.
- Nie zusammen mit Schwerpunkten (`campaign.offerFocuses`) oder Angebotsblöcken (Variablen mit
  `offerRole`). Eine Kampagne mit beidem nimmt ListM8 nicht in „Angebot je Lead“.
- Nur ab ListM8-MCP 4.15.0 (`ping`). Ältere Server kennen die Option nicht oder zählen das
  Haupt-Angebot noch als letzte Nummer (4.14.x): dann ein Angebot für alle.

### Was abgefragt wird (dieselben Felder wie die Karten der App)

Überschrift „Deine Angebote“ („Your offers“). Das Haupt-Angebot ist das Angebot aus dem Briefing
und steht zuerst, mit dem Etikett „Haupt-Angebot · gilt, wenn keine Bedingung passt“ („Main offer ·
applies if no condition fits“). Dazu höchstens drei weitere Angebote („Weiteres Angebot
hinzufügen · höchstens drei“).

Je Angebot drei Felder:

| Feld | Karte C (Vorarbeit) | Karte A (Teilleistung) |
|---|---|---|
| Die Sache, als Lücke im Satz der Mail | „Deswegen war ich so frei und habe dir ___ erstellt.“ (“So I went ahead and put together ___ for you.”) | „Genau deshalb bieten wir aktuell für eine Handvoll {Empfänger} in {Region} ___ an.“ (“That's exactly why we're currently offering ___ to a handful of {recipients} in {region}.”) |
| Das Wort für die Sache, als Lücke in der Schlussfrage (optional) | „Wäre es in Ordnung, wenn ich dir morgen ___ zusende?“ (“Mind if I send over ___ tomorrow?”) | „Wäre es in Ordnung, wenn ich ___ auch für dich erstelle?“ (“Mind if I put ___ together for you too?”) |
| „Was ist konkret drin?“ (“What's in it?”) | Grundlage des zweiten Absatzes | Grundlage des zweiten Absatzes |

Hinweis der Karte C: „Nur Angebote, die du jedem passenden Lead wirklich bis morgen schicken
kannst.“ (“Only offers you can really send every matching lead by tomorrow.”) Hinweis der Karte A:
„Was du nach der Antwort lieferst.“ (“What you deliver after a reply.”)

Je weiteres Angebot eine Bedingung, „Passt, wenn“ („Fits if“): „Die Website {hat · hat keine}
{Merkmal}“ („The website {has · has no} {feature}“) mit genau einem der sieben Merkmale der
Recherche. Das Haupt-Angebot braucht keine Bedingung, es ist immer der Ersatz.

| Merkmal (Deutsch) | Englisch | `feature` |
|---|---|---|
| Online-Buchung | online booking | `booking` |
| Bewertungen | reviews | `website_reviews` |
| Kontaktformular | contact form | `contact_form` |
| Seiten zu einzelnen Projekten | pages for individual projects | `project_pages` |
| Karriereseite | careers page | `career_page` |
| Galerie | gallery | `gallery` |
| Vertriebsrollen im Team | sales roles on the team | `sales_roles` |

Optional je weiteres Angebot ein Freitext „Zusätzlich“ („Also“) mit dem Hinweis „Optional. Nur, was
man auf der Website sieht.“ („Optional. Only what you can see on the website.“)

Hat der Kunde nur das Haupt-Angebot: „Du hast nur das Haupt-Angebot. Es gilt für jeden Lead; eine
Bedingung braucht es nicht.“ („You only have the main offer. It applies to every lead; no condition
needed.“) Auch das ist eine gültige Einrichtung: Dann schreibt die KI den zweiten Absatz je Lead.

### Vorschläge (W12)

Wie in der App schlägt das Plugin weitere Angebote vor, bevor der Kunde sie eintippt: aus dem
Briefing und der Website des Kunden (seine Leistungen, was er nach einer Antwort liefern kann)
höchstens drei, je mit Sache, Wort, Detail und einer Bedingung aus den sieben Merkmalen. Darüber
steht „Vorschlag der Recherche. Prüf, ändere oder wähl ab.“ („Suggested by the research. Check,
change or deselect.“), je Vorschlag „Nicht verwenden“ („Don't use“). Nichts davon geht ungeprüft in
die Kampagne. Ohne passende Vorschläge steht nur das Haupt-Angebot da.

Regeln für Vorschläge wie für jedes Angebot: ein Deliverable, kein Gespräch, keine Analyse und kein
Audit; bei C nur, was wirklich bis morgen lieferbar ist; die Bedingung beschreibt, wofür das
Angebot passt, nie einen Mangel, den die Mail ausspricht. Sache und Wort ohne eckige Klammern und
ohne `{{`, keine Gedankenstriche.

### Die Anweisung (Vorlage, abgenommen am 10.11.2026, Wortlaut seit DS-206)

Die Anweisung ist der Prompt von `angebot_ausfuehrung`. ListM8 baut sie selbst aus den Karten: Ein
Blueprint mit „Angebot je Lead“ und ohne `offerPrompt` bekommt beim Import die Anweisung des
Servers, was auch immer das Plugin als Prompt schickt. Das Plugin baut sie deshalb nur, um sie dem
Kunden zu zeigen, und schickt dieselbe Fassung als Prompt mit (der Server braucht die Variable,
der Prompt muss mindestens 10 Zeichen haben).

Bevor angelegt wird, zeigt das Plugin dem Kunden die Anweisung unter der Überschrift „So schreibt
die KI den Angebotsteil“ („How the AI writes the offer part“), zusammen mit den Angeboten. Erst
nach seinem Ja wird angelegt.

Aufbau wie in der App: Nummeriert wie die Karten, das Haupt-Angebot ist Angebot 1, die weiteren
folgen ab 2 in der Reihenfolge des Kunden. Unter „WAHL DES ANGEBOTS“ stehen zuerst die Bedingungen
der weiteren Angebote, zuletzt das Haupt-Angebot; ohne weitere Angebote heißt diese Zeile „Angebot 1
(Haupt-Angebot): gilt für jeden Lead.“ („Offer 1 (main offer): applies to every lead.“). Unter „DIE
ANGEBOTE“ steht das Haupt-Angebot zuerst. Eine Zeile `konkret drin` entfällt, wenn das Angebot kein
Detail hat; „ Zusätzlich: …“ nur mit Freitext. Zeilen mit `\n` trennen, Abschnitte mit einer
Leerzeile.

**Deutsch, Du-Fassung** (ein weiteres Angebot; mit mehr Angeboten je Angebot eine Zeile unter WAHL
und ein Block unter DIE ANGEBOTE):

```
Schreib den Angebotsteil von Mail 1 für diesen Lead. Er hat drei Absätze: Absatz 1 und 3 stehen bei jedem Angebot fest und werden zum gewählten Angebot automatisch eingesetzt. Du schreibst nur Absatz 2 und gibst die Nummer des gewählten Angebots unter „angebot“ an. Gib nur Absatz 2 aus und sonst nichts: keinen Namen eines Angebots, keine Begründung, keine Überschrift.

WAHL DES ANGEBOTS
Angebot 2 passt, wenn die Recherche belegt: {Bedingung} Zusätzlich: {Freitext}
Angebot 1 (Haupt-Angebot): gilt nur, wenn keine dieser Bedingungen belegt ist.
Eine Bedingung ist nur belegt, wenn die Recherche sie für diesen Lead feststellt; „unklar“ oder nicht erwähnt zählt als nicht belegt. Passen mehrere Angebote, nimm unter ihnen das mit der kleinsten Nummer.

DIE ANGEBOTE
Angebot 1 (Haupt-Angebot):
- Absatz 1: „{Satz der Form mit der Sache des Haupt-Angebots}“
- Absatz 3: „{Schlussfrage der Form mit seinem Wort}“
- konkret drin: „{Detail}“
Angebot 2:
- Absatz 1: „{Satz der Form mit der Sache}“
- Absatz 3: „{Schlussfrage der Form mit dem Wort für die Sache}“
- konkret drin: „{Detail}“

ABSATZ 1 UND 3
Absatz 1 und Absatz 3 des gewählten Angebots stehen fest und werden wörtlich eingesetzt; schreib sie nicht.

ABSATZ 2
{Regel der Form für den zweiten Satz}
Grundlage ist, was beim gewählten Angebot konkret drin ist, zugeschnitten auf das, was die Recherche über den Lead weiß.
Absatz 2 greift nichts auf, was das Intro dieses Leads schon nennt (kein Projekt, keinen Kunden, kein Produkt, keine Auszeichnung, keinen Ort und keine Zahl daraus): Das Intro steht direkt darüber, eine Wiederholung liest sich wie ein Echo. Nimm ein anderes Detail aus der Recherche oder nur, was beim Angebot konkret drin ist.
LÄNGE: genau ein Satz mit höchstens 25 Wörtern, am besten 15 bis 20. Ein vorgegebener Satzanfang zählt mit. 25 ist eine harte Grenze: Ein Satz mit 26 Wörtern ist falsch, auch wenn er sonst gut ist. Zähl die Wörter vor der Antwort einzeln (ein Wort mit Bindestrich zählt als eins); hat der Satz mehr als 25, kürze das Detail, statt den Satz abzugeben (ein Strichpunkt macht keine zwei Sätze daraus, er zählt mit). Mail 1 hat insgesamt höchstens 100 Wörter.
Lieferzusage, über die der Satz nie hinausgeht: {Lieferzusage der Form} {Lieferzusage des Kunden}
Keine Zahl, die die Lieferzusage nicht nennt, auch keine aus der Recherche (keine Bewertung, keine Punkte, keine Jahre, keine Kundenzahl), keine Frist (ein „morgen“ steht nur in der Schlussfrage), kein Gespräch und kein Termin, keine zweite Leistung, keine Frage, kein Lob (das steht schon im Intro), keine Wiederholung von Absatz 1. Keine Gedankenstriche.

FÜR ALLE DREI ABSÄTZE
Die Bedingung steht nie im Text, und nichts klingt nach einem Mangel des Leads.
Alle Texte dieses Leads folgen dem gewählten Angebot; nenn nirgends ein anderes.
Anrede: Sprich die Person mit du an (du, dich, dein). Für Tatsachen über den Betrieb darfst du ihr und euer nutzen, aber nie du und ihr im selben Satz. Nie Sie.
```

**Deutsch, Sie-Fassung:** wie die Du-Fassung, Absatz 1 und 3 in der Sie-Form, nur die letzte Zeile lautet:

```
Anrede: Sprich die Person mit Sie an (Sie, Ihnen, Ihre). Nie du oder ihr, nie Sie und du gemischt.
```

**Englisch:**

```
Write the offer part of email 1 for this lead. It has three paragraphs: paragraphs 1 and 3 are fixed for each offer and are inserted automatically for the offer you choose. You write paragraph 2 only and give the number of the chosen offer under "angebot". Output nothing but paragraph 2: no name of an offer, no reasoning, no heading.

CHOOSING THE OFFER
Offer 2 fits if the research shows: {condition} Also: {free text}
Offer 1 (main offer): applies only if none of these conditions is shown.
A condition only counts as shown if the research states it for this lead; "unclear" or not mentioned counts as not shown. If several offers fit, take the one with the lowest number among them.

THE OFFERS
Offer 1 (main offer):
- Paragraph 1: "{the form's sentence with the main offer's thing}"
- Paragraph 3: "{the form's closing question with its word}"
- what's in it: "{detail}"
Offer 2:
- Paragraph 1: "{the form's sentence with the thing}"
- Paragraph 3: "{the form's closing question with the word for the thing}"
- what's in it: "{detail}"

PARAGRAPHS 1 AND 3
Paragraphs 1 and 3 of the chosen offer are fixed and inserted word for word; do not write them.

PARAGRAPH 2
{the form's rule for the second sentence}
Base it on what's in the chosen offer, tailored to what the research knows about the lead.
Paragraph 2 picks up nothing the intro of this lead already names (no project, client, product, award, place or number from it): the intro sits right above, so a repeat reads like an echo. Take another detail from the research, or only what's in the chosen offer.
LENGTH: exactly one sentence of at most 25 words, ideally 15 to 20. A given opening counts. 25 is a hard limit: a sentence of 26 words is wrong, however good it is otherwise. Count the words one by one before you answer (a hyphenated word counts as one); if the sentence has more than 25, shorten the detail instead of handing it in (a semicolon doesn't make it two sentences, it counts). Email 1 has 100 words at most in total.
Delivery promise the sentence never goes beyond: {the form's delivery promise} {the customer's delivery promise}
No number the delivery promise doesn't name, none from the research either (no rating, no score, no years, no client count), no deadline (a "tomorrow" only appears in the closing question), no call and no meeting, no second service, no question, no praise (that is already in the intro), no repeat of paragraph 1. No dashes.

FOR ALL THREE PARAGRAPHS
The condition never appears in the text, and nothing sounds like something the lead is missing.
All texts for this lead follow the chosen offer; never mention another one.
Write in English, in the same casual tone as email 1.
```

### So werden die Lücken gefüllt

**Bedingung:** „Die Website hat {mit}.“ bzw. „Die Website hat {ohne}.“ (englisch „The website has
{…}.“):

| `feature` | hat | hat keine | has | has no |
|---|---|---|---|---|
| `booking` | eine Online-Buchung | keine Online-Buchung | online booking | no online booking |
| `website_reviews` | Bewertungen | keine Bewertungen | reviews | no reviews |
| `contact_form` | ein Kontaktformular | kein Kontaktformular | a contact form | no contact form |
| `project_pages` | Seiten zu einzelnen Projekten | keine Seiten zu einzelnen Projekten | pages for individual projects | no pages for individual projects |
| `career_page` | eine Karriereseite | keine Karriereseite | a careers page | no careers page |
| `gallery` | eine Galerie | keine Galerie | a gallery | no gallery |
| `sales_roles` | Vertriebsrollen im Team | keine Vertriebsrollen im Team | sales roles on the team | no sales roles on the team |

**Absatz 1** ist der Satz der Karte mit der Sache des Angebots:

- C: „Deswegen war ich so frei und habe dir {Sache} erstellt.“ · Sie „… habe Ihnen {Sache}
  erstellt.“ · englisch “So I went ahead and put together {thing} for you.”
- A: „Genau deshalb bieten wir aktuell für eine Handvoll {Empfänger} in {Region} {Sache} an.“ (Sie
  gleich) · englisch “That's exactly why we're currently offering {thing} to a handful of
  {recipients} in {region}.” `{Empfänger}` ist `recipientWord` (ohne Angabe „Betriebe“,
  “businesses”), `{Region}` die Region aus dem Briefing (ohne Angabe „deiner Region“, Sie „Ihrer
  Region“, “your area”).

**Absatz 3** ist die Schlussfrage der Karte, mit dem Wort für die Sache, wo es eins gibt:

- C ohne Wort: „Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“
  · mit Wort: „Wäre es in Ordnung, wenn ich dir morgen {Wort} zusende? Völlig unverbindlich
  natürlich.“ · Sie „… wenn ich es Ihnen morgen zusende? …“ bzw. „… wenn ich Ihnen morgen {Wort}
  zusende? …“ · englisch “Mind if I send it over tomorrow? No strings attached.” bzw. “Mind if I
  send over {word} tomorrow? No strings attached.”
- A ohne Wort: „Wäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich
  natürlich.“ · mit Wort: „Wäre es in Ordnung, wenn ich {Wort} auch für dich erstelle? Völlig
  unverbindlich natürlich.“ · Sie „… das auch für Sie erstelle? …“ bzw. „… {Wort} auch für Sie
  erstelle? …“ · englisch “Mind if I put that together for you too? No strings attached.” bzw.
  “Mind if I put {word} together for you too? No strings attached.”

**Regel der Form** (wörtlich):

- C, deutsch: `Ein Satz, der genau so beginnt: „Ich bin gerade noch an den letzten Feinheiten dran, vor allem“ und dann genau ein Detail des schon erstellten Ergebnisses nennt, an dem noch gefeilt wird, passend zu diesem Lead (aus seiner Recherche oder dem Detail des Schwerpunkts), grammatisch vollständig (z. B. „an der …“). Kein „morgen“, kein „fertig werden“, keine neue Leistung.`
- A, deutsch: `Ein Satz, der für diesen Lead konkret sagt, was in der Teilleistung drin wäre, gebaut aus dem, was die Recherche über den Lead weiß (seine Leistungen, Website, Bewertungen). Im Konjunktiv („Darin wären …“), nie als erledigte Arbeit (kein „erstellt“, „vorbereitet“, „liegt bereit“).`
- C, englisch: `One sentence that starts exactly with “I'm just finishing up the last few details, mainly” and then names exactly one detail of the result already put together that is still being refined, fitting this lead (from their research or the focus detail), grammatically complete (e.g. “the selection of …”). No “tomorrow”, no “getting it done”, no new service.`
- A, englisch: `One sentence that says specifically for this lead what the partial service would include, built from what the research knows about the lead (their services, website, reviews). Phrased as a possibility (“It would include …”), never as finished work (no “created”, “prepared” or “ready”).`

**Lieferzusage der Form** (wörtlich, danach mit einem Leerzeichen die Lieferzusage des Kunden aus
dem Briefing, ohne Angabe nichts):

- C, deutsch: `Bis morgen nach der Antwort lieferbar, nach dem Fulfillment-Maßstab (5 bis 10 Minuten Nutzerzeit je Antwort mit KI).`
- A, deutsch: `Geliefert wird erst nach der Antwort. Formuliert als Angebot, nie als erledigte Arbeit (kein „erstellt“, „vorbereitet“, „liegt bereit“).`
- C, englisch: `Deliverable by tomorrow after a reply, within 5 to 10 minutes of user time per reply with AI.`
- A, englisch: `Delivered only after a reply. Phrased as an offer, never as finished work (no “created”, “prepared” or “ready”).`

Absatz 3 des Haupt-Angebots trägt sein Wort aus der Karte, ohne eigenes Wort das Wort für die Sache
der Kampagne (`ctaNoun`).

### Was im Blueprint steht

Fünf Teile gehören zusammen. Fehlt einer, ist „Angebot je Lead“ nicht eingerichtet.

1. **`campaign.station`** mit den Antworten, aus denen ListM8 die Angebote kennt (optionaler,
   tolerant gelesener Schlüssel ab MCP 4.15.0):

   ```json
   "station": {
     "path": "ai",
     "answers": {
       "companyName": "<Firma des Absenders>",
       "offer": "<was der Absender verkauft, ein Satz>",
       "audience": "<Zielgruppe>",
       "region": "<Region, nur bei Karte A nötig>",
       "salutation": "<du oder sie, wie emailAgentConfig.salutation>",
       "openerForm": "C",
       "prepared": "<Sache des Haupt-Angebots, wie sie im Satz steht>",
       "delivery": "<Lieferzusage des Kunden, optional>",
       "ctaNoun": "<Wort für die Sache des Haupt-Angebots, optional>",
       "subjectTest": false,
       "introTest": false,
       "elaborationPerLead": false,
       "offerPerLead": true,
       "offerCards": {
         "main": {"noun": "<Wort für die Sache oder null>", "detail": "<konkret drin>"},
         "more": [
           {"phrase": "<Sache>", "noun": "<Wort oder null>", "detail": "<konkret drin>", "feature": "booking", "has": false, "note": null}
         ]
       }
     },
     "recipientWord": "<Empfänger im Plural, z. B. Praxen>"
   }
   ```

   `openerForm` ist `"C"` für Karte C und `"A"` für Karte A (dieselben Buchstaben wie in der App).
   `companyName`, `offer`, `audience`, `openerForm` und `prepared` sind Pflicht: Ohne sie nimmt
   ListM8 den ganzen Block still als nicht gesetzt, und die Variable bekäme keine Angebote.
   `salutation` ist dieselbe Ansprache wie `emailAgentConfig.salutation`: Ohne `"sie"` setzt ListM8
   Absatz 1 und 3 auch in einer Sie-Kampagne in der Du-Form ein. Englische Kampagnen setzen `"du"`.
   `subjectTest` und `introTest` stehen so, wie der Nutzer die Tests gewählt hat (ohne Schlüssel
   gälte der Betreff-Test als an, falls die Mails später in der App neu erzeugt werden).
   `elaborationPerLead: false` und `ctaNoun` sorgen dafür, dass Mail 1 und Mail 3 beim Ausschalten in
   der App den festen zweiten Satz und die Schlussfrage mit dem Wort bekommen. `offerPrompt` (eigene
   Anweisung) schickt das Plugin nie. Längen: Sache höchstens 200 Zeichen, Wort 120, Detail 1000,
   Zusatz 500, ohne eckige Klammern und ohne `{{`; eine ungültige Karte lässt ListM8 alle Karten
   still fallen.

2. **Mail 1** mit den drei Platzhaltern in eigenen Absätzen (W17), an der Stelle von Angebotssatz,
   zweitem Satz und Schlussfrage:

   ```
   {{ai.hallo}}\n\n{{ai.intro}}\n\n{{ai.offer_text}}\n\n{{ai.angebot_ausfuehrung}}\n\n{{ai.offer_cta}}\n\n\nViele Grüße\n<Signatur>\n\nFalls das gerade kein Thema für dich ist, gib mir kurz Bescheid.
   ```

3. **Drei Variablen** direkt nach `intro` (bzw. `firma`), ohne `offerRole`:

   | Name | Prompt |
   |---|---|
   | `offer_text` | „Vom Server gesetzt: Absatz 1 des Angebots, das die KI für den Lead gewählt hat (Angebot je Lead). Schreibt nie die KI.“ (englisch “Set by the server: paragraph 1 of the offer the AI picked for the lead (offer per lead). Never written by the AI.”) |
   | `angebot_ausfuehrung` | die Anweisung oben, wie sie dem Kunden gezeigt wurde (ListM8 ersetzt sie beim Import durch die eigene) |
   | `offer_cta` | „Vom Server gesetzt: Absatz 3 des Angebots, das die KI für den Lead gewählt hat (Angebot je Lead). Schreibt nie die KI.“ (englisch “Set by the server: paragraph 3 of the offer the AI picked for the lead (offer per lead). Never written by the AI.”) |

4. **Mail 3 endet neutral** (W5) statt mit der Schlussfrage aus Mail 1, damit sie keinem Angebot
   widerspricht: „Melde dich gerne, wenn das Thema für dich relevant ist.“ · Sie „Melden Sie sich
   gerne, wenn das Thema für Sie relevant ist.“ · englisch “Feel free to get in touch if this is
   relevant for you.” Mail 2 bis 4 nennen kein einzelnes Angebot.

5. **Keine** `campaign.offerFocuses`, keine Variable mit `offerRole`, kein `offerPrompt`.

Tests lassen sich dazu wählen: Die Varianten übernehmen Mail 1 mit den drei Platzhaltern.

**Antworten des Servers beim Anlegen und Bearbeiten (ab MCP 4.15.0):**

- `offer_per_lead_inconsistent`: Der Blueprint würde „Angebot je Lead“ einer Kampagne mit Station
  ein- oder ausschalten, ohne dass Mail 1 und die Variablen dazu passen; nichts wurde übernommen.
  Nicht unverändert erneut senden. Einschalten: Mail 1 mit den drei Platzhaltern und die drei
  Variablen mitschicken. Ausschalten: Mail 1 mit Angebotssatz, festem zweitem Satz und Schlussfrage
  statt der Platzhalter. Oder den Nutzer in der App umschalten lassen (Angebots-Blatt, Schalter
  „Angebot je Lead“); die Meldung nennt, was fehlt.
- `warnings` nennen Station-Antworten, die nicht übernommen wurden (etwa mehr als drei weitere
  Angebote, ein unbekanntes `feature`, Karte für Karte begründet), und Lücken, die nichts
  umschalten. Die gespeicherten Werte bleiben. Dem Nutzer zeigen und den Blueprint korrigieren.

### Beispiel (Karte C, du)

Weber Webdesign aus `beispiel-blueprint.md`, Haupt-Angebot der Startseiten-Entwurf, zwei weitere
Angebote aus den Vorschlägen, vom Kunden geprüft:

| Nr. | Sache | Wort | konkret drin | Passt, wenn |
|---|---|---|---|---|
| 1 | einen Entwurf für deine neue Startseite | den Entwurf | Startseite mit den Behandlungen, die die Praxis hervorhebt, echten Bewertungen und Buchungsknopf | Haupt-Angebot |
| 2 | eine Seite für die Online-Terminbuchung | die Buchungsseite | Behandlungen mit Dauer und Buchungsknopf, aus den Texten der Website | Die Website hat keine Online-Buchung. |
| 3 | eine Galerie mit deinen Vorher-nachher-Fällen | die Galerie | Vorher-nachher-Fälle aus dem Material der Praxis, sortiert nach Behandlung | Die Website hat keine Galerie. |

Die Anweisung, die das Plugin daraus baut und vor dem Anlegen zeigt:

```
Schreib den Angebotsteil von Mail 1 für diesen Lead. Er hat drei Absätze: Absatz 1 und 3 stehen bei jedem Angebot fest und werden zum gewählten Angebot automatisch eingesetzt. Du schreibst nur Absatz 2 und gibst die Nummer des gewählten Angebots unter „angebot“ an. Gib nur Absatz 2 aus und sonst nichts: keinen Namen eines Angebots, keine Begründung, keine Überschrift.

WAHL DES ANGEBOTS
Angebot 2 passt, wenn die Recherche belegt: Die Website hat keine Online-Buchung.
Angebot 3 passt, wenn die Recherche belegt: Die Website hat keine Galerie.
Angebot 1 (Haupt-Angebot): gilt nur, wenn keine dieser Bedingungen belegt ist.
Eine Bedingung ist nur belegt, wenn die Recherche sie für diesen Lead feststellt; „unklar“ oder nicht erwähnt zählt als nicht belegt. Passen mehrere Angebote, nimm unter ihnen das mit der kleinsten Nummer.

DIE ANGEBOTE
Angebot 1 (Haupt-Angebot):
- Absatz 1: „Deswegen war ich so frei und habe dir einen Entwurf für deine neue Startseite erstellt.“
- Absatz 3: „Wäre es in Ordnung, wenn ich dir morgen den Entwurf zusende? Völlig unverbindlich natürlich.“
- konkret drin: „Startseite mit den Behandlungen, die die Praxis hervorhebt, echten Bewertungen und Buchungsknopf“
Angebot 2:
- Absatz 1: „Deswegen war ich so frei und habe dir eine Seite für die Online-Terminbuchung erstellt.“
- Absatz 3: „Wäre es in Ordnung, wenn ich dir morgen die Buchungsseite zusende? Völlig unverbindlich natürlich.“
- konkret drin: „Behandlungen mit Dauer und Buchungsknopf, aus den Texten der Website“
Angebot 3:
- Absatz 1: „Deswegen war ich so frei und habe dir eine Galerie mit deinen Vorher-nachher-Fällen erstellt.“
- Absatz 3: „Wäre es in Ordnung, wenn ich dir morgen die Galerie zusende? Völlig unverbindlich natürlich.“
- konkret drin: „Vorher-nachher-Fälle aus dem Material der Praxis, sortiert nach Behandlung“

ABSATZ 1 UND 3
Absatz 1 und Absatz 3 des gewählten Angebots stehen fest und werden wörtlich eingesetzt; schreib sie nicht.

ABSATZ 2
Ein Satz, der genau so beginnt: „Ich bin gerade noch an den letzten Feinheiten dran, vor allem“ und dann genau ein Detail des schon erstellten Ergebnisses nennt, an dem noch gefeilt wird, passend zu diesem Lead (aus seiner Recherche oder dem Detail des Schwerpunkts), grammatisch vollständig (z. B. „an der …“). Kein „morgen“, kein „fertig werden“, keine neue Leistung.
Grundlage ist, was beim gewählten Angebot konkret drin ist, zugeschnitten auf das, was die Recherche über den Lead weiß.
Absatz 2 greift nichts auf, was das Intro dieses Leads schon nennt (kein Projekt, keinen Kunden, kein Produkt, keine Auszeichnung, keinen Ort und keine Zahl daraus): Das Intro steht direkt darüber, eine Wiederholung liest sich wie ein Echo. Nimm ein anderes Detail aus der Recherche oder nur, was beim Angebot konkret drin ist.
LÄNGE: genau ein Satz mit höchstens 25 Wörtern, am besten 15 bis 20. Ein vorgegebener Satzanfang zählt mit. 25 ist eine harte Grenze: Ein Satz mit 26 Wörtern ist falsch, auch wenn er sonst gut ist. Zähl die Wörter vor der Antwort einzeln (ein Wort mit Bindestrich zählt als eins); hat der Satz mehr als 25, kürze das Detail, statt den Satz abzugeben (ein Strichpunkt macht keine zwei Sätze daraus, er zählt mit). Mail 1 hat insgesamt höchstens 100 Wörter.
Lieferzusage, über die der Satz nie hinausgeht: Bis morgen nach der Antwort lieferbar, nach dem Fulfillment-Maßstab (5 bis 10 Minuten Nutzerzeit je Antwort mit KI). Gebaut aus den Texten und Fotos, die die Praxis schon online hat.
Keine Zahl, die die Lieferzusage nicht nennt, auch keine aus der Recherche (keine Bewertung, keine Punkte, keine Jahre, keine Kundenzahl), keine Frist (ein „morgen“ steht nur in der Schlussfrage), kein Gespräch und kein Termin, keine zweite Leistung, keine Frage, kein Lob (das steht schon im Intro), keine Wiederholung von Absatz 1. Keine Gedankenstriche.

FÜR ALLE DREI ABSÄTZE
Die Bedingung steht nie im Text, und nichts klingt nach einem Mangel des Leads.
Alle Texte dieses Leads folgen dem gewählten Angebot; nenn nirgends ein anderes.
Anrede: Sprich die Person mit du an (du, dich, dein). Für Tatsachen über den Betrieb darfst du ihr und euer nutzen, aber nie du und ihr im selben Satz. Nie Sie.
```

So kommt Mail 1 für eine Praxis ohne Online-Buchung beim Empfänger an (Angebot 2, Absatz 2 von der
KI, Absatz 1 und 3 von ListM8):

```
Hallo Lena,

ich hab mir deine Bewertungen angeschaut, und mehrere Patienten schreiben, dass du jeden Schritt vorher erklärst.

Deswegen war ich so frei und habe dir eine Seite für die Online-Terminbuchung erstellt.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an der Reihenfolge deiner Veneers und Bleachings.

Wäre es in Ordnung, wenn ich dir morgen die Buchungsseite zusende? Völlig unverbindlich natürlich.


Viele Grüße
Jonas Weber
Inhaber - Weber Webdesign

Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.
```

### Nach dem Anlegen prüfen (Pflicht, vor den Leads)

`export_campaign_blueprint(campaign_id)`:

- `campaign.station.answers` trägt `offerPerLead: true`, die `salutation` der Kampagne und
  `offerCards` mit allen Angeboten (nur das Haupt-Angebot ohne Wort und Detail kommt ohne
  `offerCards` aus). Fehlt der Block, war eine Pflichtantwort leer; fehlen Karten, war eine Karte
  ungültig: mit `edit_campaign` (Vollersatz aus dem Export) nachreichen.
- Step 1 hat `{{ai.offer_text}}`, `{{ai.angebot_ausfuehrung}}` und `{{ai.offer_cta}}` je in einem
  eigenen Absatz; Step 3 endet mit dem neutralen Satz.
- Die drei Variablen stehen ohne `offerRole` da; es gibt keine `offerFocuses`.

### Generierung und Prüfung

- **Generieren** (`outreach-generate`, `lead-agent`): `get_lead_data` nennt in `expectedOutput` den
  Schlüssel `angebot` (die Nummern der Angebote) und für `offer_text` und `offer_cta` „set by the
  server“. Die KI wählt nach „WAHL DES ANGEBOTS“ anhand des Abschnitts `WEBSITE-BEFUND` der
  Recherche: unter den Angeboten, deren Bedingung belegt ist, das mit der kleinsten Nummer, sonst
  das Haupt-Angebot (Nummer 1). Sie meldet die Nummer unter `angebot`, schreibt
  `angebot_ausfuehrung` (nur Absatz 2) und schickt `offer_text` und `offer_cta` leer. Ab MCP 4.15.0
  lehnt `save_lead_variables` eine fehlende oder unbekannte Nummer mit `validation_failed` ab und
  nennt die gültigen Nummern: Nummer korrigieren und erneut speichern. `offer_instruction_outdated`
  heißt, die Kampagne trägt eine eigene Anweisung in der alten Nummerierung: Lead überspringen und
  dem Nutzer melden (bestätigen oder ersetzen in der App). Person 2 übernimmt Absatz 1 und 3 von
  Person 1.
- **Prüfen** (`outreach-verify`, `verify-agent`): `offer_text` und `offer_cta` sind Serverwerte,
  kein Befund zum Wortlaut. `angebot_ausfuehrung` wird nach den Regeln der Anweisung geprüft (Regel
  der Form, ein Satz mit höchstens 25 Wörtern, nichts über die Lieferzusage hinaus, keine Zahl, Frist,
  Frage, kein Termin, kein Lob, keine Wiederholung von Absatz 1, keine Bedingung im Text, kein
  Mangel, passend zum gewählten Angebot). Ob das gewählte Angebot zum Lead passt, zeigt `offer_text`
  zusammen mit dem `WEBSITE-BEFUND` der Recherche.
