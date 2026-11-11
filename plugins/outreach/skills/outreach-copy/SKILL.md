---
name: outreach-copy
description: 'Use when user says "Cold-Mail schreiben", "Cold-Mail prüfen", "Copy prüfen", "Kampagnen-Copy", "Sequenz schreiben", "Betreffzeile", "Opener", "Intro-Prompt", "hallo-Prompt", "Marketing-Offer formulieren", "Offer schärfen", "Feinheiten-Satz", "zweiter Angebotssatz", "angebot_ausfuehrung", "Angebot je Lead", "A/B-Test", "Betreff-Test", "Intro-Test", "Für Erfahrene", "Follow-ups schreiben", or wants to write, review or fix the copy of an outreach campaign. Verbindliche Cold-Mail-Copy-Regeln (Anatomie der Entry-Mail, Offer-Karten A-E, fester zweiter Satz je Karte, für Erfahrene Tests und „Angebot je Lead“, 4er-Sequenz, Wortlimits, Intro- und Anrede-Regeln, Verbote, Selbstprüfung). outreach-campaign, outreach-generate und outreach-verify laden diesen Skill verbindlich.'
---

# Outreach Copy — die Cold-Mail-Regeln für Kampagnen

Dieser Skill ist die eine Copy-Doktrin für alles, was über den Outreach-MCP an Text entsteht:
Sequenz (Betreff und Body jedes Steps), die Prompts der AI-Variablen `hallo` und `intro` (mit
„Angebot je Lead“ dazu `angebot_ausfuehrung`) und die pro Lead erzeugten Werte. Er gilt verbindlich für:

| Skill | Wann diesen Skill laden |
|---|---|
| `outreach-campaign` | bevor eine Zeile Sequenz oder Variablen-Prompt entsteht (`create_campaign`, `edit_campaign`) |
| `outreach-generate` | bevor `hallo`/`intro` für einen Lead geschrieben werden (`save_lead_variables`) |
| `outreach-verify` | beim Prüfen der Werte (`get_lead_variables`) vor `approve_lead_variables`/`reject_lead_variables` |

Ausführliche Lehre mit allen Beispielen: `references/copy-lehre.md`. Offer-Lehre:
`references/marketing-offer.md`. Ein vollständig ausformulierter Blueprint:
`references/beispiel-blueprint.md`. Tests in Mail 1 und „Angebot je Lead“ (beides für Erfahrene,
standardmäßig aus): `references/fuer-erfahrene.md`. Bei einem Widerspruch zwischen diesen Dateien
gilt diese SKILL.md.

## Kampagnensprache

Jede Kampagne hat eine Sprache (`campaign.language`, ab MCP 4.7.0): `de` (Standard) oder
`en`. Bei der Generierung steht sie in `get_lead_data` → `emailGeneration.language`. Fehlt das
Feld (älterer Server), ist die Kampagne deutsch.

- **`de`:** Dieser Skill gilt vollständig, mit allen deutschen Sprachregeln.
- **`en`:** Englische Kampagnen haben eigene Regeln, natürliches US-Englisch, nie aus dem
  Deutschen übersetzen. Die deutschen Sprachregeln dieses Skills (du/Sie, Anführungszeichen „…“,
  Umlaute, deutsche Beispielsätze und Reaktionsformen) gelten dort nicht. Stattdessen:
  - Anrede `Hi {first name},` (nur Vorname, ohne du/Sie); ohne benennbare Person `Hi there,`.
  - Grußformel `Best,` über `{{accountSignature}}`.
  - Betreff klein, 2–5 Wörter: Mail 1 `quick question`; Mail 2 bis 4 ohne Betreff im Thread von Mail 1.
  - Der Opener beginnt groß.
  - Die Reaktion im Opener ist ein eigener kurzer Satz oder ein „which“-Nebensatz, nie Komma plus
    „that“.
  - Kein „free“ im Text, stattdessen „no strings attached“ oder „at no cost“.
  - Nie „Hope this email finds you well“ oder „I wanted to reach out“.
  - Mail 1 höchstens 100 Wörter, Ziel 50–90.
  - In Mail 1 und Mail 3 die Abmeldezeile, ohne „P.S.“:
    `If this isn't a priority right now, just let me know.`
  - Anführungszeichen “…”.

  Maßgeblich sind die Regeln, die der Server mitgibt (`emailGeneration.systemPrompt`,
  `salutationRule`). Die Regeln oben sind geprüft; eine ausführliche englische Copy-Lehre
  (Beispiele, Offer-Karten A–E) kann später folgen.

Der Recherchebericht bleibt in beiden Fällen deutsch.

## Ziel und Grundsatz

Aus den Angaben des Nutzers entsteht eine Cold-Mail-Kampagne für die erste Aussendung: eine
Entry-Mail, die wie eine persönliche Nachricht wirkt, und drei Follow-ups mit je einer Aufgabe.
Ziel ist eine Antwort, kein Klick und kein Termin in Mail 1.

- Nur verwenden, was der Nutzer im Gespräch angegeben hat (Angebot, Zielgruppe, Absender, Belege,
  Kapazitäten) oder was die Recherche pro Lead liefert. Keine Zahlen, Namen, Referenzen oder
  Fristen erfinden. Wo Angaben fehlen, allgemeiner formulieren oder beim Nutzer nachfragen.
- Der Marketing-Offer bestimmt 80 % der Reply Rate. Ohne konkretes Deliverable keine Copy:
  erst das Offer schärfen (siehe unten), dann schreiben.

## Tonalität und Formatierung

- Du-Form als Standard: direkt, konkret, kein Beratersprech, keine Floskeln. Deutsch
  (englische Kampagnen: siehe Kampagnensprache).
  Sie-Form nur, wenn der Nutzer sie für die Kampagne wählt (siehe Anrede).
- Knapp und menschlich: kurze Sätze, ein klarer CTA pro Mail. Die Mail klingt wie eine kurze
  Nachricht an einen Bekannten, nicht wie eine Agentur-Website.
- Keine M-Striche (—) und keine Gedankenstriche als Trenner, auch kein Bindestrich mit
  Leerzeichen („ - “). Bindestriche nur innerhalb von Wörtern (E-Mail, Smart-Home); Ausnahme ist
  die Signaturzeile „<Rolle> - <Firma>“.
- Anführungszeichen nur als deutsches Paar „…“, geschlossen immer mit “, nie mit dem geraden
  Zeichen ("). In einer Variable beendet ein gerades Zeichen den JSON-String, der Rest des Satzes
  geht verloren; `save_lead_variables` lehnt einen Wert mit offenem „ ab.
- Korrekte deutsche Rechtschreibung mit echten Umlauten und ß: „für“, „Grüße“, „über“, nie
  „fuer“, „Gruesse“, „ueber“. Das gilt für JEDES Feld: Sequenz, Variablen-Prompts,
  Kampagnenkonfiguration, Beispielwerte.
- Plain Text: kein Bold, keine Bulletpoints, keine Emojis, kein HTML-Layout, keine Bilder, keine
  Anhänge.

## Anrede und Ansprache

Die Ansprache steht in `campaign.emailAgentConfig.salutation` und gilt für jede generierte
Variable einer Mail (nur in deutschen Kampagnen; englische kennen kein du/Sie, siehe
Kampagnensprache). Immer explizit setzen. Der feste Sequenztext (Überleitung, CTA, Follow-ups)
muss dieselben Pronomen tragen wie der gewählte Modus.

| `salutation` | Pronomen im ganzen Text | `hallo` | Fallback ohne benennbare Person |
|---|---|---|---|
| `du` (Standard) | Person: du/dich/dir/dein, nie ihr/euch als Anrede; Tatsachen über den Betrieb auch ihr/euer (siehe unten) | „Hallo Vorname,“ | „Hallo,“ |
| `sie` (Ausnahme) | Sie/Ihnen/Ihre | „Hallo Frau Nachname,“ / „Hallo Herr Nachname,“ (Herr/Frau nur, wenn belegt; nie „Guten Tag Herr/Frau Nachname,“; ohne belegte Anrede „Guten Tag Vorname Nachname,“ (G18)) | „Guten Tag,“ |

**Standard ist immer `du`, Singular** – auch bei Praxen, Kanzleien, Finanz und generischen Adressen:
Die Mail richtet sich an den Ansprechpartner bzw. Entscheider, nicht an den Betrieb. Die Person wird nie mit ihr/euch angesprochen (keine Ihr- und keine Team-Form, auch nicht im Gruß). Tatsachen über einen Betrieb mit mehr als einer Person dürfen aber mit ihr/euer stehen („dass ihr nach ISO 9001 zertifiziert seid“, „auf eurer Website“) oder mit „dein Team“/„deine Firma“, je nachdem, was natürlicher klingt. Firmenleistungen (Projekte, Anlagen, Produkte, Zertifikate, Auszeichnungen) gehören dem Betrieb: nie „du hast die Anlage gebaut“ an eine Geschäftsführerin oder einen Vertriebsleiter; „du hast …“ nur, wenn die Person es nachweislich selbst getan hat, oder bei Ein-Personen-Betrieben, Personenmarken und kleinen Inhaberbetrieben, die sie verkörpert. Innerhalb eines Satzes nicht zwischen du und ihr wechseln („deine Bewertungen …, dass ihr …“ ist falsch). Ein „nie ihr/euch“ im Prompt einer Variable meint die Anrede der Person, nicht diese Tatsachen. Ohne benennbaren Ansprechpartner lautet der Gruß
„Hallo,“ und der Text bleibt im Singular („dein Team“, „dein Betrieb“, „deine Praxis“). `sie` gilt nur,
wenn der Nutzer es für die Kampagne wählt (Kampagnen, die gezielt sehr große Unternehmen
ansprechen), nie automatisch je Lead. Dass eine alte Vorlage, eine Bestandskampagne oder die Branche
siezt bzw. „ihr“ schreibt, ist KEIN Grund für eine Abweichung. Keine Mischform in der Anrede: „Hallo Max,“
vor „ich hab was für euch“ ist ein Fehler. Den Wert `team`, den der Server noch annimmt, setzt dieser Skill nie.

Der feste Text nennt den Empfänger nur mit einer Bezeichnung, die auf jeden Lead der Liste passt.
Mischt die Zielgruppe Firmen und Einzelpersonen (Agenturen und Freelancer, Praxen und
Einzelbehandler), schreibt er „dein Business“, „deine Kunden“ oder „für dich“ statt „deine Agentur“
bzw. „deine Praxis“.

- Wer wird in der Du-Form mit Vornamen angesprochen? Die Person, der die Versandadresse gehört.
  Trägt die Adresse nur einen Nachnamen (instagram.leitner@, leitner.coaching@), die Person mit diesem
  Namen, sobald Lead-Name oder Recherche sie eindeutig benennen.
  Bei allgemeinen Adressen (info@, kontakt@, office@, team@, hallo@, hello@, mail@, contact@,
  partnership@, business@, kooperation@, support@, Filialpostfach) der Vorname der Ansprechperson, die die
  Recherche als Entscheider nennt (Inhaber, Geschäftsführung, Verantwortliche), damit die Mail
  dort ankommt bzw. weitergeleitet wird. Nennt die Recherche mehrere gleichrangige Inhaber oder
  Geschäftsführer, gilt die Person, die sie als Ansprechpartner empfiehlt, sonst die erstgenannte
  im Impressum. Personenmarken und Ein-Personen-Betriebe (Creator, Coach, Freelancer,
  Solo-Selbstständige) immer mit Vornamen, auch hinter hello@, info@ oder partnership@ ihrer Marke;
  trägt der Lead selbst den Namen einer Person, ist sie gemeint, auch wenn die Recherche den
  Geschäftsführer einer Firma als Entscheider nennt. Ist keine Person klar erkennbar, steht nur
  „Hallo,“. Die Sie-Form geht analog mit Herr/Frau und Nachname, Fallback
  „Guten Tag,“; nie „Guten Tag Herr/Frau Nachname,“; ohne belegte Anrede „Guten Tag Vorname Nachname,“ (G18). Beide Personen einer Firma grüßen in derselben Form,
  sobald ihre Anrede belegt ist (DealSupply macht aus „Guten Tag Herr Schneider,“ „Hallo Herr Schneider,“).
- NIE „Hallo Herr/Frau Nachname,“ zusammen mit Du-Text (`du`), nie „Hallo <Firma> Team,“ oder
  „Hallo zusammen,“, nie „Hey …“, nie Sie und du gemischt.
- Die Anrede kommt immer aus `{{ai.hallo}}`. Kein `{{firstName}}`, kein `{{companyName}}`, kein
  `{{custom.vorname}}` direkt in Betreff oder Body: Es gibt kein Vornamen-Feld, und ein leeres
  Attribut ergibt „Hallo ,“. Liegt der Vorname als Custom-Attribut aus dem Import vor (Schlüssel
  zeigt `get_lead_data` unter `customAttributes`), nennt der `hallo`-Prompt ihn als Quelle.
- Keine Titel („Dr.“, „Prof.“), auch nicht in der Sie-Form (wie der Anrede-Prompt der App).

## Schritt 1: Offer-Typ wählen

Der Marketing-Offer ist nicht die Dienstleistung des Nutzers, sondern der Türöffner: das
konkrete, greifbare Ding, das den Erstkontakt trägt. Wähle GENAU EINE Karte und begründe die
Wahl dem Nutzer in einem Satz.

Empfohlen ist genau eine Karte, nach derselben Regel wie in der App: **C**, wenn das Ergebnis je Lead
mit KI in 5 bis 10 Minuten Nutzerzeit bis morgen lieferbar ist, **sonst A**. E nur, wenn der Absender
belegt regelmäßig Anfragen für die Zielgruppe hat, B nur bei einem neuen Angebot mit echt begrenzten
Plätzen, D nur mit Beleg. C, A, E und B stehen immer zur Wahl, auch wenn sie nicht empfohlen sind; D
ohne Beleg passt nicht.

| Karte | Passt, wenn | Passt nicht, wenn |
|---|---|---|
| C: Konkretes Deliverable (in der App „Schon erledigte Vorarbeit“) | das Ergebnis zum einzelnen Lead passt und mit KI in 5 bis 10 Minuten Nutzerzeit bis morgen lieferbar ist | es je Lead mehr als 5 bis 10 Minuten Nutzerzeit braucht oder nicht bis morgen lieferbar ist (dann A) |
| A: Kostenlose Teildienstleistung („Kostenlose Teilleistung“) | die Teilleistung nach der Antwort lieferbar ist, vorab für jeden Lead aber zu aufwendig | sich das Ergebnis je Lead schon bis morgen mit KI erstellen lässt (dann C) oder die Leistung ein Gespräch, eine Analyse oder ein Audit ist |
| E: Partner gesucht | der Absender nachweislich regelmäßig Anfragen für die Zielgruppe hat | es keinen Beleg für echte Anfragen gibt |
| B: Tester/Pilotprojekt („Pilotprojekt“) | das Angebot neu ist, mit wenigen Referenzen und echt begrenzten Plätzen | das Angebot schon breit läuft oder die Plätze nicht wirklich begrenzt sind (künstliche Knappheit) |
| D: Förder-Hook („Förderung“) | der Nutzer Programm und Quote nennt oder seine Website sie nennt | Programm oder Quote nicht belegt sind: eine Förderquote zu nennen wäre geraten |

Die Überleitung (der Angebotssatz) ist für alle Leads gleich und steht wörtlich wie in der App:

| Karte | du | Sie |
|---|---|---|
| C | „Deswegen war ich so frei und habe dir [Deliverable] erstellt.“ | „Deswegen war ich so frei und habe Ihnen [Deliverable] erstellt.“ |
| A | „Genau deshalb bieten wir aktuell für eine Handvoll [Empfänger] in [Region] [Deliverable] an.“ | gleich |
| B | „Genau solche [Empfänger] suchen wir gerade. Wir starten [Pilotprojekt] mit einer Handvoll [Empfänger] in [Region].“ | gleich |
| D | „Wusstest du, dass [Träger] aktuell bis zu [Quote] der Kosten für [Leistung] übernimmt?“ | „Wussten Sie, dass …“ |
| E | „Genau solche [Empfänger] suchen wir als Partner. Wir haben regelmäßig [Anfragen], die zu dir passen würden.“ | „… die zu Ihnen passen würden.“ |

Englisch: C “So I went ahead and put together [deliverable] for you.”, A “That's exactly why we're
currently offering [deliverable] to a handful of [recipients] in [region].”, B “That's exactly the kind
of [recipients] we're looking for right now. We're launching [pilot project] with a handful of them in
[region].”, D “Right now, businesses like yours can get up to [rate] of the cost of [service] covered
through [funder].”, E “That's exactly the kind of [recipients] we're looking for as partners. We
regularly get [inquiries] that would be a great fit for you.”

Die Klammern füllst du beim Schreiben der Sequenz aus den Angaben des Nutzers; im fertigen Text
steht keine Klammer mehr. [Empfänger] ist die Zielgruppe im Plural („Praxen“, ohne Angabe
„Betriebe“), [Region] die Region (ohne Angabe „deiner Region“, Sie „Ihrer Region“). Es heißt „eine
Handvoll“, nie eine erfundene Anzahl; eine Anzahl („20 Firmen“) nur, wenn die Lieferzusage des
Nutzers sie trägt. [Träger] nennt Programm oder Träger, wie der Nutzer sie schreibt („das Land
Baden-Württemberg“), ohne Angabe „der Staat“; [Quote] die belegte Quote ohne „bis zu“ („50 %“), das
„bis zu“ steht schon im Satz. [Deliverable], [Pilotprojekt] und [Anfragen] passen grammatisch in die
Lücke: bei B ohne eigenes „mit“ und ohne Wort aus dem Satz drumherum („starten“, „Handvoll“), bei E
ohne „regelmäßige“ und ohne eigenen Relativsatz, Anfragen von Kunden der Empfänger, nie von den
Empfängern selbst.

Das Offer muss ALLE drei Punkte erfüllen, sonst umformulieren:

- **No-Brainer:** Würde ich selbst auf diese Mail antworten?
- **Kein Commitment:** Der Empfänger muss NICHTS tun außer antworten. Kein Call buchen, kein
  Formular, kein Download.
- **Konkret:** „Kostenloses Google Ads Setup“ statt „Kostenlose Beratung“.

Werttest: Das Offer spart erkennbar Zeit, spart Geld oder bringt Geld.

VERBOTEN als Offer (Sales Calls in Verkleidung): „Analyse“, „Audit“, „Potenzial-Check“,
„Erstgespräch“, „Beratung“, „Strategiegespräch“. Immer ein Deliverable statt eines Gesprächs.
Bei Karte D Quoten immer als Spanne („bis zu 100 %“), nie als Zusage.

## Der Marketing-Offer (Türöffner)

Das konkrete, vorbereitete Asset, das sich mit AI-Unterstützung realistisch vorbereiten lässt
(z. B. „ein kompletter Webseitenentwurf inklusive Buchungssystem“, „eine fertige
Werbekampagnen-Struktur“, „eine Lead-Liste inklusive Outreach-Sequenz“, „ein
30-Tage-Content-Plan“). Quellen in dieser Reihenfolge:

1. Das Marketing-Offer, das der Nutzer im Gespräch selbst benennt: 1:1 übernehmen, nur
   sprachlich glätten.
2. Sonst aus dem Angebot des Nutzers abgeleitet (seine Leistungen und Kanäle aus dem Gespräch).
3. Sonst einen Vorschlag nach der Empfehlungsregel (C, sonst A) machen und vom Nutzer bestätigen lassen.

Regeln:

- In Mail 1 steht GENAU EIN Marketing-Offer mit GENAU EINEM CTA, der die Antwort auslöst.
- Bei Karte C als bereits erledigte Arbeit formulieren („war so frei und habe … erstellt“),
  nicht als Absicht. Reziprozität wirkt erst, wenn das Geschenk schon existiert. Bei Karte A ist
  das Deliverable ein Angebot („bieten … an“), nie erledigte Arbeit.
- Kein „Lass uns mal sprechen“ ohne vorbereiteten Mehrwert.
- Die Überleitung verbindet das Lob mit dem Offer („Genau deshalb …“, „Deswegen war ich so
  frei …“).
- Das Offer steht NUR in Mail 1. Follow-ups wiederholen es nicht.

## Anatomie der Entry-Mail

```
{{ai.hallo}}                     1. Anrede
{{ai.intro}}                     2. Lob / positiver Bezug (Intro-Regeln)
Feste Überleitung + Offer        3. statisch, benennt KEIN lead-spezifisches Problem;
                                    bei C als erledigte Arbeit, bei A als Angebot
Zweiter Satz zum Angebot         4. eigener Absatz, je Karte: A, B und C der feste
                                    Satz der Karte, D und E keiner
EIN Frage-CTA                    5. niedrige Hürde, eigener Absatz
Grußformel + Signatur            6. nach zwei Leerzeilen „Viele Grüße“, darunter
                                    {{accountSignature}}
Abmeldezeile                     7. nach einer Leerzeile unter der Signatur (Step 1 und 3)
```

**Zweiter Satz zum Angebot (Stand 10.11.2026, wie die App):** Nach dem Angebotssatz folgt in Mail 1
ein zweiter Satz zum Angebot, als eigener Absatz zwischen Offer und CTA. Er ist KEIN zweites Offer
und KEIN zweiter CTA. Standard ist der feste Satz der Karte, für alle Leads gleich, als Text im Body
(keine Variable). Angebotssatz, zweiter Satz und Schlussfrage stehen immer in drei eigenen Absätzen,
auch mit „Angebot je Lead“ und in jeder Variante (W17).

| Karte | Fester zweiter Satz, du | Sie | Englisch |
|---|---|---|---|
| C: Konkretes Deliverable | „Ich bin gerade noch an den letzten Feinheiten dran.“ | gleich | “I'm just finishing up the last few details.” |
| A: Kostenlose Teildienstleistung | „Darin wäre alles genau auf euch zugeschnitten.“ | „Darin wäre alles genau auf Sie zugeschnitten.“ | “Everything in it would be tailored to your business.” |
| B: Tester/Pilotprojekt | „Im Pilot bekommt ihr das kostenlos, dafür bräuchten wir nur ehrliches Feedback.“ | „Im Pilot bekommen Sie das kostenlos, dafür bräuchten wir nur ehrliches Feedback.“ | “You'd get it free during the pilot, all we'd ask for is honest feedback.” |
| D: Förder-Hook, E: Partner gesucht | kein zweiter Satz, die Überleitung hat schon zwei Sätze | | |

Die Sätze sind die der App (P12, P15) und gelten wörtlich; „euch“ bei A und „ihr“ bei B meinen den
Betrieb, nicht die Person, und sind deshalb kein Anrede-Fehler. Der Pilot-Satz der App trägt im
Englischen „free“; das ist die abgenommene Ausnahme von der Regel „kein „free“ im Text“.

**Kein Satz je Lead von selbst:** Eine neue Kampagne legt `angebot_ausfuehrung` nicht mehr an. Einen
zweiten Satz je Lead gibt es nur über „Angebot je Lead“ (Karte A und C, für Erfahrene, siehe unten);
wer nur den Satz je Lead will, richtet es mit dem Haupt-Angebot allein ein (W2).

**Bestehende Kampagnen** mit `{{ai.angebot_ausfuehrung}}` (angelegt bis outreach 0.6.0) behalten ihre
Variable und ihren Prompt; beim Bearbeiten wird nichts umgestellt. Für ihre Werte gelten weiter
diese Regeln:

- **C, Feinheiten-Satz:** Ein Satz, der genau so beginnt: „Ich bin gerade noch an den letzten
  Feinheiten dran, vor allem“ und dann genau ein Detail des schon erstellten Ergebnisses nennt, an
  dem noch gefeilt wird, passend zu diesem Lead, grammatisch vollständig (z. B. „an der …“). Kein
  „morgen“, kein „fertig werden“, keine neue Leistung. Englisch: „I'm just finishing up the last few
  details, mainly …“. Beispiel: „Ich bin gerade noch an den letzten Feinheiten dran, vor allem an den
  Vorher-nachher-Bildern deiner Implantat-Fälle.“
- **A, Inhaltssatz:** was für diesen Lead konkret im Deliverable drin wäre, im Konjunktiv. Beispiel:
  „Darin wären deine drei meistgebuchten Behandlungen mit Preis, Ablauf und Buchungsknopf, gebaut aus
  den Texten und Fotos, die du schon online hast.“
- **B, Rahmensatz:** was der Lead im Pilot konkret bekäme, bezogen auf etwas aus seiner Recherche,
  und was er dafür gibt (ehrliches Feedback), nicht bei jedem Lead derselbe Satz.
- **Mit Schwerpunkten** (Bestand mit `campaign.offerFocuses`): Grundlage des Satzes ist das Detail
  des Schwerpunkts, den die KI für den Lead wählt. Gewählt wird je Lead der Schwerpunkt, der nach
  Schwerpunkt-Prüfung und Recherche am besten passt; das Haupt-Offer (Rang 1) nur, wenn keiner klar
  besser passt. Ist nicht Rang 1 gewählt, nennen der zweite Satz und das Routing nichts vom
  Haupt-Offer. Der letzte Schwerpunkt ist der Auffang ohne Prüffrage (E59): dieselbe Leistung mit
  dem Fokus Sichtbarkeit, als Ergebnis für die Zielkunden formuliert, nie als „SEO“. Neue Kampagnen
  bekommen keine Schwerpunkte mehr.
- **Grenzen für alle:** bei A und B nie als erledigte Arbeit (kein „erstellt“, „vorbereitet“, „liegt
  bereit“, kein Feinheiten-Wortlaut), bei C nur das schon Erstellte; nur Inhalte, die die
  Lieferzusage des Nutzers deckt; keine Zahl, die weder Lieferzusage noch Recherche belegt; keine
  Frist; kein Gespräch, Termin oder Call; keine Frage; ein Satz mit höchstens 25 Wörtern, am besten
  15 bis 20 (nachzählen, ein Strichpunkt zählt mit); Pronomen gemäß `salutation`. Kein zweiter Prüf-
  oder Korrekturlauf.

**Für Erfahrene: „Angebot je Lead“ (nur Karte A und C, ab MCP 4.15.0):** Auf ausdrücklichen
Wunsch wählt die KI je Lead eines von bis zu vier Angeboten des Kunden (Haupt-Angebot plus höchstens
drei weitere, je mit einer Bedingung aus den sieben Website-Merkmalen der Recherche) und schreibt den
zweiten Absatz; Angebotssatz und Schlussfrage des gewählten Angebots setzt DealSupply ein. Es ist eine
KI-Variable mit der abgenommenen Vorlage, keine Zusatzlogik: Mail 1 trägt an der Stelle der drei
Sätze `{{ai.offer_text}}`, `{{ai.angebot_ausfuehrung}}` und `{{ai.offer_cta}}` in drei eigenen
Absätzen, die Antworten der Karten stehen im Station-Block des Blueprints, und Mail 3 endet neutral
(„Melde dich gerne, wenn das Thema für dich relevant ist.“). Felder, Vorschläge, Vorlage DE und EN,
Blueprint und Beispiel: `references/fuer-erfahrene.md`, Teil 2. Bei Karte B, D und E gibt es die
Option nicht.

**Schlusssatz (CTA):** Genau einer, nie zwei Optionen, immer eine Frage (keine Bitte wie „Antworte
mir einfach kurz.“). Je Karte gilt die Schlussfrage der App (Stand 05.11.2026), Sie-Form in Klammern:
A „Wäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich natürlich.“ („… das
auch für Sie erstelle? …“), B „Wärst du grundsätzlich offen dafür?“ („Wären Sie grundsätzlich offen
dafür?“), C „Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“
(„… es Ihnen morgen zusende? …“), D „Wäre es in Ordnung, wenn ich dir kurz aufschreibe, welches
Programm für dich infrage kommt? Völlig unverbindlich natürlich.“ („… wenn ich Ihnen kurz aufschreibe,
welches Programm für Sie infrage kommt? …“), E „Wäre das grundsätzlich interessant?“ (gleich für Sie).
Hat die Kampagne Schwerpunkte mit einem Wort für die Sache (etwa „den Entwurf“, „das Setup“, „die
Anzeigen“), steht es bei C an der Stelle von „es“, mit anderer Wortstellung: „Wäre es in Ordnung,
wenn ich dir morgen den Entwurf zusende? Völlig unverbindlich natürlich.“, bei A an der Stelle von
„das“. Jede Kampagne hat außerdem ein eigenes Wort für die Sache (in DealSupply auf der Angebots-Seite unter der Schlussfrage, vom Assistenten vorgeschlagen): Es steht nur in der Frage von Mail 3 und gilt dort, solange Mail 3 nicht das Wort des Schwerpunkts trägt (Variable `{{ai.offer_noun}}`); Mail 1 behält „es“ bzw. „das“; ohne Wort nimmt Mail 3 die Frage aus Mail 1 wörtlich (06.11.2026). Kein „Link“ im Schlusssatz (nicht „… wenn ich dir morgen den Link dazu schicke?“), die Sache
wird zugesendet. „morgen“ und „zusenden“ nur bei C, und nur, wenn der Nutzer das Deliverable nach der
Antwort wirklich bis zum nächsten Tag liefern kann, sonst „… wenn ich es dir zusende?“. Der Zusatz
„Völlig unverbindlich natürlich.“ senkt die Hürde und ist kein zweiter CTA. Eine Schlussfrage, die
der Nutzer selbst bestätigt hat, gilt wörtlich. Mit „Angebot je Lead“ hat jedes Angebot seine
eigene Schlussfrage mit seinem Wort für die Sache; DealSupply setzt die des gewählten Angebots ein
(`{{ai.offer_cta}}`). Der Betreff von Step 1 ist bei jeder Karte „kurze Frage“. Kein Terminvorschlag
und kein Link in Mail 1.

Die Master-Formel (Kurs Outbound 3.0, Lektion 2.4) in fünf Bausteinen: Lob → „Deswegen …“ →
konkretes Offer → Fertigstellung → CTA mit wenig Verpflichtung. Im Kurs trägt der Halbsatz „… und
werde morgen mit dem Entwurf fertig.“ die Fertigstellung, bei uns trägt sie das „morgen“ im
Schlusssatz. „Morgen“ wirkt stärker als „schon fertig“: Der Lead sieht, dass gerade noch für ihn
gearbeitet wird.

**Kein Pitch, keine Selbstvorstellung im Body.** Authority und Proof gehören in die Signatur bzw.
in Step 3. Über den Empfänger schreiben, nie über den Absender („Du bekommst …“, nicht „Wir
bieten …“).

Muster je Karte, direkt nach dem Lob-Intro, jeder Baustein ein eigener Absatz. Karte C:

```
Deswegen war ich so frei und habe dir einen kompletten Webseitenentwurf inklusive
Buchungssystem erstellt.

Ich bin gerade noch an den letzten Feinheiten dran.

Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.
```

Karte A:

```
Genau deshalb bieten wir aktuell für eine Handvoll Praxen in [Region] einen kostenlosen Entwurf
für eine neue Startseite mit Online-Terminbuchung an.

Darin wäre alles genau auf euch zugeschnitten.

Wäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich natürlich.
```

Karte B:

```
Genau solche Agenturen suchen wir gerade. Wir starten ein Pilotprojekt für persönliche
Erstmails mit einer Handvoll Agenturen in [Region].

Im Pilot bekommt ihr das kostenlos, dafür bräuchten wir nur ehrliches Feedback.

Wärst du grundsätzlich offen dafür?
```

Karte C mit „Angebot je Lead“ (Body von Step 1, die drei Absätze setzen KI und DealSupply je Lead):

```
{{ai.hallo}}

{{ai.intro}}

{{ai.offer_text}}

{{ai.angebot_ausfuehrung}}

{{ai.offer_cta}}
```

**Signatur:** Jede Mail endet mit der Grußformel und direkt darunter `{{accountSignature}}`:
„…?\n\n\nViele Grüße\n{{accountSignature}}“ (englisch „…?\n\n\nBest,\n{{accountSignature}}“).
Beim Versand setzt Instantly dort die Signatur des Versandpostfachs ein, mit Name, Rolle und Firma
des Absenders. Keine eigene Unterschrift mit Name, Rolle oder Firma im Mailtext, auch nicht, wenn der
Nutzer sie nennt, und nie `{{sender.firstName}}`, `{{sender.company}}` o. Ä. (gibt es nicht). Name,
Rolle und Firma trägt der Nutzer schlank in die Signatur jedes Versandpostfachs ein (keine
Auszeichnungen, Links, Telefonnummern oder Social-Leisten; siehe `outreach-launch`). So schreibt es
auch die App (Stand 10.11.2026).

**Abstand vor dem Gruß:** Zwischen dem letzten Satz (der Schlussfrage) und der Grußformel stehen
zwei Leerzeilen, eine mehr als zwischen den Absätzen; die Signatur folgt direkt unter der
Grußformel (Giuliano, 05.11.2026).

**Abmeldezeile:** In Step 1 und Step 3 steht nach einer
Leerzeile unter der Signatur genau diese Zeile, ohne „PS:“ und nie vor dem CTA: „Falls das gerade
kein Thema für dich ist, gib mir kurz Bescheid.“ Sie-Form: „Falls das gerade kein Thema für Sie
ist, geben Sie mir kurz Bescheid.“ (gekürzt am 05.11.2026; die frühere Zeile „…, dann melde ich
mich nicht mehr.“ steht nur noch in bestehenden Kampagnen). Sie zählt nicht zum Wortlimit. Den technischen Abmeldelink (List-Unsubscribe) setzt das
Versandtool zusätzlich.

## Intro-Regeln (`{{ai.intro}}`)

Das Intro ist Lob oder eine anerkennende Beobachtung: ein positiver Bezug auf den Lead, der
beweist, dass jemand hingeschaut hat, getragen von einem konkreten Detail. Es ist KEINE Kritik
und KEIN Verbesserungsvorschlag. Das Problem sind leere Lobadjektive ohne Inhalt, nicht das Lob.
Einzige Ausnahme sind KI-Variablen mit Winkel `chance` (Abschnitt „Chance-Winkel“ unten).
Gründe, Gegensatzpaare und Beispiele: `references/copy-lehre.md`, Abschnitt „Abhebung und
Austauschtest“.

MUSS:

- Abhebung statt Leistungsnennung: Das Intro nennt, was diesen Betrieb von anderen seiner Branche
  abhebt: einen Eigennamen oder ein eigenes Konzept, eine ungewöhnliche Zeit oder Zahl, ein eigenes
  Verfahren, eine seltene Spezialisierung, eine Auszeichnung, ein Lob aus Bewertungen, auffällige
  Bewertungszahlen.
- Austauschtest: Passt der Satz auf zehn andere Betriebe derselben Branche in der Stadt, ist er kein
  Aufhänger. Dann den nächsten Anker nehmen, zuletzt den Fallback der Kampagne. Ein Nutzen rettet
  keine Standardleistung. Dasselbe Thema besteht als Lob aus Bewertungstexten (was Kunden über
  DIESEN Betrieb schreiben), nicht als Zeile aus der Leistungsliste. Eine Aufzählung von Leistungen
  („A, B und C“) ist nie ein Aufhänger. Gegensatzpaar: „du bietest Badsanierung an“ fällt durch,
  „jedes Bad vorab als begehbarer 3D-Rundgang“ besteht.
- Sperrliste der Kampagne: Was in den Research-Vorgaben oder im `intro`-Prompt als branchenübliche
  Leistung gesperrt ist, trägt kein Intro, außer als Lob aus Bewertungstexten.
- Positiver Schluss: Das Intro besteht aus Einstieg, Anker und Abschluss; der Abschluss ist keine
  Pflicht. Rangfolge (Entscheidung 23.10.2026 nach Blindtests: Würdigungen gerieten in 18 von 77
  Mails zum Gutachten oder wiederholten das Detail, Reaktionen kaum; bei Kampagne 301 kamen alle
  Interessenten aus Intros ohne Schluss):
  1) Kein Schluss, wenn das Detail schon selbst ein Lob ist (was Kunden in Bewertungen schreiben,
  eine Auszeichnung, ein Preis) oder der erste Satz des festen Mailtexts selbst lobt: nie zweimal
  loben.
  2) Sonst, bei einem neutralen Faktum (Öffnungszeit, Verfahren, Spezialisierung, Projekt) oder einer
  Bewertungszahl, eine kurze persönliche Reaktion direkt hinter dem benannten Detail, in der
  Vergangenheit erzählt wie unter Kollegen, im Ton der Formen mit den besten Antwortquoten
  (Prod-Dump 23.10.2026): „das fand ich richtig schön“, „das hat mir gut gefallen“, „das fand ich richtig sympathisch“, „das hat mich angesprochen“; „richtig“ ist erlaubt, Übertreibung („total begeistert“)
  und Floskeln nicht; am Detail und nie ohne es. Sie wechselt von Lead zu Lead, nie steht in allen Mails
  derselbe Satz: Der Block `SCHLUSS DES OPENERS` im System-Prompt (`emailGeneration.systemPrompt`)
  schlägt je Lead eine Form vor, als Richtung und Tonlage, nicht als Pflicht. Passt eine eigene kurze Reaktion besser zum Detail, im selben Ton formulieren (bei einer historischen Kegelbahn etwa „da musste ich direkt schmunzeln“), höchstens etwa sechs Wörter, keine Floskel; passt der
  Vorschlag nicht („schön“ oder „sympathisch“ hinter einer Bewertungszahl oder einem technischen
  Detail), eine eigene bilden. Fehlt der Block (älterer Server), die Reaktion je Lead selbst variieren. Hinter einer Bewertungszahl ohne Worte zum Inhalt steht die Reaktion, außer der Satz ist schon lang.
  Hinter Firmengeschichte, Gründung oder Alter des Betriebs heißt die Reaktion immer „das hab ich richtig gern gelesen“ (Sie-Form gleich, englisch „That was really nice to read.“), auch wenn der Vorschlag eine andere nennt; „das fand ich richtig sympathisch“ passt dort nicht (E54, 06.11.2026).
  3) Eine Würdigung nur ausnahmsweise, wenn sie etwas Neues und Konkretes über den Betrieb sagt,
  das nicht schon im Detail steht (Anerkennung mit Inhalt „da steckt richtig viel Handarbeit drin“,
  Seltenheit als eigene Erfahrung „so eine Nachsorge ist mir noch nicht begegnet“; ebenso ein
  Superlativ am Detail nur bei wirklich beeindruckendem Anker). Nie Gutachten-Ton und nie eine
  Folgerung mit „das zeigt, wie …“, „das zeigt, dass …“ oder „das spricht für …“ über Ausrichtung,
  Erfahrung oder Qualität: „du betreibst ein Herren-Kosmetikstudio mit separatem Eingang, das zeigt,
  wie klar der Betrieb auf seine Kundschaft ausgerichtet ist“ und „seit 2004 in der Branche, das
  spricht für viel Branchenerfahrung“ sagen das Detail noch einmal, „macht das Angebot schön
  konkret“ urteilt wie ein Gutachten. Im Zweifel die Reaktion; klingt auch sie nicht, bleibt das
  Faktum ohne Schluss.
  Verboten: der Mechanik-Nutzen, also ein Schluss, der erklärt, was man dank des Details tun kann
  („so können sich Interessierte vorab ein Bild machen“, „so kann man unverbindlich nachfragen“,
  „so bekommen Kunden schneller einen Termin“), in jeder Satzform: ein Schluss, der ausmalt, was
  Kunden dank des Details tun können oder sich sparen (wer, wann, wofür), auch „das spart
  Berufstätigen den Urlaubstag für den Reifenwechsel“; Seltenheit im allgemeinen „man“ („erlebt man
  nicht oft“) und Vergleiche mit anderen Betrieben ohne Beleg („hebt dich von jeder anderen Agentur
  ab“, „bietet sonst kaum ein Studio an“); Lob ohne Detail („finde ich stark“, „Hammer“); doppeltes
  Lob; Würdigung und Reaktion hintereinander; das leere Prüfer-Urteil über die Qualität ihrer
  Arbeit, das aus dem Detail nicht folgt und auf jeden Betrieb passt („das wirkt vertrauenswürdig“,
  „so einen Schnitt hält man nur, wenn die Arbeit stimmt“, „da machst du vieles richtig“, „das
  schafft man nicht ohne sauberes Arbeiten“, „zeigt, dass die Behandlung ankommt“). Nichts
  erfinden, nur was direkt aus dem Detail folgt. Keine feste Wendung aus Beispielen. Der
  Fallback-Satz bleibt ohne Schluss.
- Ausschließlich positiv, getragen vom konkreten Detail selbst. Verboten sind austauschbare
  Bewertungsfloskeln und Superlative wie „das spricht für sich“, „das sieht man selten“, „das sieht
  man nicht immer“, „hat man nicht alle Tage“, „finde ich stark“, „finde ich spannend“, „finde ich
  bemerkenswert“, „Hammer“, „beeindruckend“ und „hängen geblieben“ in jeder Form (seit 31.10.2026). Abgrenzung: „finde ich stark“ ist eine Formel, ein
  gegenwärtiges Urteil ohne Inhalt; eine Würdigung oder Reaktion am benannten Detail ist erlaubt,
  Seltenheit und Superlativ nur mit dem Detail („so eine Nachsorge ist mir noch nicht begegnet“), nie allein
  („das sieht man selten“, „beeindruckend“) (siehe Positiver Schluss). Die Formeln machen alle Opener gleich (gilt zusätzlich
  zu den übrigen Opener-Regeln). Auch in Beispielen und Prompts nie als Muster stehen lassen:
  Modelle kopieren Beispiele.
- Anker-Rangfolge (wie der Server, Block ANKER-REIHENFOLGE; den ersten Anker nehmen, der den
  Austauschtest besteht):
  1) Anzahl und Schnitt der Bewertungen mit ein oder zwei Worten zum Inhalt, nur bei mindestens
  30 Bewertungen und einem Schnitt ab 4,5 und nur, wenn die Recherche ein Lob mit Inhalt belegt;
  ohne Schluss, weil die Worte zum Inhalt selbst ein Lob sind.
  2) Lob aus Bewertungstexten (Paraphrase), auch eine einzelne Rezension aus den letzten 18 Monaten.
  3) Abhebendes Detail: Besonderheit, Projekt, Auszeichnung oder Geschichte, untereinander
  gleichrangig; auch Wachstum oder Stellenanzeige als Erkenntnis.
  4) Anzahl und Schnitt allein, ohne Worte zum Inhalt (dieselben Schwellen), mit einer Reaktion als
  Schluss; nie vor einer Kundenstimme oder einem abhebenden Detail, auch wenn die Kampagne
  Bewertungen zuerst nennt.
  5) Ersatzsatz der Kampagne.
  Legt der Prompt der Variable eine eigene Reihenfolge fest, gilt diese (mit der Ausnahme bei Rang 4).
  **Bezug zum Angebot:** Bestehen mehrere belegte Anker, gewinnt der, der zum Angebot der Kampagne
  passt (Hotel, Angebot für Tagungsgäste: die Rezension zum Seminarraum, nicht das Lob fürs Essen);
  die Reihenfolge entscheidet nur unter den Ankern mit Bezug. Keinen Bezug erfinden.
  **Plural nur ab drei:** Verallgemeinerung („immer wieder“, „viele“, „mehrere“, „oft“, Plurale wie
  „Gäste loben“) nur, wenn mindestens drei Rezensionen genau dieses Lob tragen; bei einer oder zwei
  steht das Lob im Singular („jemand schreibt, dass …“). Keine Anzahl der Rezensionen zu einem Lob im
  Text („zwei Gäste“). Ein Ein-Wort-Kommentar, bloße Eigenschaftswörter („kompetent“, „freundlich“) oder
  eine einzelne Rezension, die älter als 18 Monate ist, tragen kein Lob.
  **Bewertungszahlen:** Anzahl genau oder abgerundet, nie zu hoch: „über“ nur, wenn die genannte Zahl
  kleiner ist als die echte („80 Bewertungen“ bei genau 80); unter 1.000 auf die Zehnerstelle darunter
  („über 60“ bei 63), ab 1.000 auf die Hunderterstelle („über 1.200“ bei 1.234). Schnitt mit Komma
  („4,8“, auch „5,0“). Werte aus dem Import (Google-Profil) gelten als Quelle, bei widersprüchlichen
  Quellen der kleinere Wert; nur unabhängige Plattformen. Reicht Google nicht (unter 30 Bewertungen
  oder unter 4,5), dürfen Anzahl und Schnitt eines anderen Bewertungsportals stehen, mit denselben
  Schwellen dort und dem Portal im Satz („bei Treatwell“, „bei Jameda“); reichen beide, hat Google
  Vorrang. Hinter einer Zahl ohne Worte zum Inhalt steht die Reaktion, nie „so können sich
  Interessierte vorab orientieren“.
- Einstiege abwechseln, keiner ist Standard: nach der letzten Ziffer der Lead-ID 0-2 „mir ist
  aufgefallen, dass …“, 3-5 „ich hab mir … angeschaut“, 6-7 „beim Stöbern auf deiner Website …“,
  8-9 direkt mit dem Detail. Ausnahme: Ein Bewertungsanker nennt im Einstieg die Quelle (siehe
  unten). Beginnt mehr als ein Drittel einer Kampagne gleich, ist das ein systematischer Befund.
- Auch ein Projekt, eine Referenz, die Firmengeschichte oder das Gründungsjahr (mit seinem
  Ereignis), Auszeichnungen und Siegel (ohne Altersgrenze), Lage und Ausstattung können tragen,
  jeweils mit EINEM konkreten Detail und nur, wenn sie den Austauschtest bestehen.
- Stellenanzeige: die Erkenntnis nutzen, die sie über den Betrieb verrät (Wachstum,
  Spezialisierung, Projekt), nicht „ich hab gesehen, dass du gerade … suchst“. Nie „du
  stellst ein“ ankündigen.
- Ein zweiter Satz ist konkret und wiederholt oder nimmt nicht vorweg, was der feste Text danach
  sagt (beginnt der feste Text mit „Das hat mich neugierig gemacht.“, darf der Satz nicht davor
  stehen).
- Zuschreibung stimmt: Der angeschriebenen Person nie etwas zuschreiben, das einer anderen
  gehört (der Podcast der Inhaberin bei einer Mail an eine Mitarbeiterin). Die Person beim
  Namen nennen oder einen Anker wählen, der zur angeschriebenen Person gehört. Meint eine
  Bewertung jemanden ohne Namen („die Zahnärztin“) und hat der Betrieb mehrere davon, das Lob
  dem Betrieb zuschreiben („in deiner Praxis nimmt man sich Zeit“), nie „bei dir“. Wachstum,
  Filialzahlen, Auszeichnungen oder Konzepte eines Franchisegebers, einer Kette oder einer
  Muttergesellschaft gehören nicht dem angeschriebenen Standort; was der Standort selbst anbietet
  (Verfahren, Geräte, Behandlungen) und was Kunden über ihn schreiben, bleibt ein Anker.
- Maximal 2 Sätze, zusammen höchstens 30 Wörter (nachzählen), ohne Gedankenstrich (Komma statt
  Strich). EIN Detail: nie zwei oder drei Lobpunkte, Projekte, Titel oder Jahreszahlen
  aneinandergereiht; wird es zu lang, das schwächere Detail streichen, statt zu verdichten. Meist
  ist es ein Satz, und der Schluss hängt mit einem Komma am Detail; einen zweiten Satz gibt es nur,
  wenn der Schluss als eigener kurzer Satz besser klingt, und er trägt dann nur den Schluss.
- Beginnt mit Kleinbuchstaben (folgt direkt auf „Hallo …,“). Nur der erste Buchstabe ist klein,
  jeder weitere Satz beginnt groß. Substantive und Namen bleiben auch am Anfang groß („Kunden
  loben …“, nie „kunden loben …“).
- Inhaltlich über den EMPFÄNGER schreiben, nie über den Absender. Einstiegsrahmen wie „ich hab
  mir … angeschaut“ oder „mir ist aufgefallen“ sind erlaubt und keine Selbstvorstellung.
- Locker und authentisch, Ton wie eine kurze Nachricht an einen Bekannten.
- Geht nahtlos in den festen Folgesatz über, ohne ein Problem zu benennen.

NIEMALS:

- Kritik, Defizit, Mangel, „Lücke“, „Hürde“, „Problem“, „leider“, „schade“.
- Konjunktiv-Wunsch: „wäre (doch) schön/besser/sinnvoll, wenn …“.
- „noch nicht“, „fehlt“, „begrenzt“, „veraltet“, „ausbaufähig“, „verschenkt Potenzial“,
  auditartige Formulierungen.
- Bevormundende Verbesserungsvorschläge oder Ratschläge.
- Selbstvorstellung/Pitch („Wir sind …“, „Mein Name ist …“, „Wir helfen …“).
- Floskeln („Ich bin auf Ihre Webseite gestoßen“, „Tolle Webseite“).
- Erfundene Fakten, Personen, Rollen oder Zahlen.
- Sichtbare Platzhalter ([Branche], [Name]) oder M-Striche (—).
- Heikles als Aufhänger, auch wenn eine Bewertung es lobt: Preis, „günstig“ oder „faire Preise“;
  persönliche Merkmale von Rezensierenden (Alter, Herkunft, Sprache), ihre Familie und Umstände;
  sensible Gesundheitsdetails (Eingriffe, Diagnosen, Körperteile); negative Wörter aus Zitaten.
  Steht so etwas neben anderem Lob in derselben Bewertung, nur das andere Lob nehmen.

Ein Bewertungsanker beginnt mit einem Einstieg, der die Quelle nennt („ich hab mir deine
Bewertungen angeschaut, und …“). Ein nacktes „jemand schreibt, dass …“ direkt nach der Anrede lässt
offen, wo das steht, und wirkt wie aus dem Nichts.

Lieber Fallback als Floskel: Ein generischer Opener („deine Website macht einen professionellen
Eindruck“) ist schlechter als der ehrliche Fallback-Satz.

Hinweis: Der DealSupply-Server legt beim Generieren zusätzlich eigene Intro-Regeln in den Prompt
(u. a. Empfänger direkt ansprechen statt „Die Praxis hat …“, keine Kunden-, Projekt-, Ergebnis-
oder Bewertungszahlen aus Selbstangaben der Website, den Befund selbst als Lob tragen statt mit
einer Bewertungsfloskel abzuschließen). Gründungsjahr mit seinem Ereignis und Teamgröße sind
Tatsachen und erlaubt. Sie
verschärfen die Regeln oben und gelten mit.

## Chance-Winkel (nur KI-Variablen mit Winkel `chance`)

Gilt NUR für KI-Variablen, die `get_lead_data` mit `angle` = `chance` nennt (etwa `intro_chance`).
So läuft ein A/B-Test der Intros: Mail 1 hat in Instantly mehrere Varianten, Variante A nutzt
`{{ai.intro}}`, Variante B die Chance-Variable; Instantly verteilt die Varianten beim Versand.
Jeder Lead bekommt alle Variablen. Alle anderen Variablen, auch das normale `intro`, folgen allein
den Intro-Regeln oben. Maßgeblich ist der Server: Hat die Kampagne eine Chance-Variable, enthält
`emailGeneration.systemPrompt` den Block „CHANCE-WINKEL (nur für KI-Variablen mit Winkel chance)“;
dieser Abschnitt ist die Gedächtnisstütze dazu. Die Chance-Variable steht in ihrer Variante
anstelle des normalen Intros direkt vor dem festen Folgesatz: für sich allein schreiben, ohne
Bezug auf `intro`.

Chance heißt: Lob für eine belegte Stärke plus genau EINE eigene, belegte Beobachtung zur
Website. Die Stärke ist dort kaum oder nicht zu sehen, oder Buchen (außerhalb der Hotellerie:
Termine) geht dort nur per Anfrage, Telefon oder Mail. Die Beobachtung ist der Grund für den
festen Folgesatz („Deswegen war ich so frei …“), kein Urteil.

Beide Seiten brauchen einen Beleg aus der Recherche:

- Stärke: ein Anker nach den Intro-Regeln oben, der den Austauschtest besteht (Lob aus
  Bewertungstexten mit Inhalt, Anzahl und Schnitt ab 30 Bewertungen und 4,5, Auszeichnung,
  belegtes abhebendes Detail). Quelle meist der Abschnitt `BEWERTUNGEN EXTERN` des Berichts.
- Beobachtung: steht so im Abschnitt `WEBSITE-BEFUND` des Berichts, als
  „Bewertungen oder Kundenstimmen auf der Website: nein“ (nur zusammen mit einer Stärke aus
  Bewertungen; eine Auszeichnung nur, wenn der Befund ausdrücklich sagt, dass die Website sie nicht
  nennt) oder als „Online-Buchung oder Terminbuchung: nur Anfrageformular“ bzw. „nur Telefon oder
  Mail“ (passt zu jeder belegten Stärke). Sie muss zum Angebot der Kampagne passen; sind beide belegt, genau eine.

**Rückfall auf Lob (Pflicht):** Fehlt einer der beiden Belege, entsteht ein Lob-Intro genau nach
den Intro-Regeln oben. Das gilt bei fehlendem `WEBSITE-BEFUND`, bei „unklar“, wenn die Website die
Stärke schon zeigt („ja“), wenn kein Anker trägt (dann der Fallback-Satz) und wenn die Beobachtung
nicht zum Angebot passt. Aus dem Schweigen eines Berichts wird nie ein „nein“. Der Wert bleibt in
der Chance-Variable und geht in Variante B hinaus; Instantly wertet nach Variante aus, DealSupply zeigt
den Anteil der Rückfälle.

Was bei einer Chance-Variable von den Intro-Regeln oben abweicht (nur für ein belegtes Chance-Intro):

- Kein Schluss, keine Reaktion, keine Würdigung: Das Intro endet mit der Beobachtung.
- Genau eine beobachtende Aussage zur Website ist erlaubt, als eigene Wahrnehmung oder schlichte
  Tatsache („auf eurer Website hab ich davon kaum etwas gefunden“, „bei dir geht Buchen bisher nur
  per Anfrage“). Nur darin dürfen „kaum“, „nichts“, „nicht“, „nur“, „bisher“, „noch nicht“ stehen.
- Höchstens 2 Sätze, zusammen höchstens 35 Wörter.

Was weiter gilt, auch in der Beobachtung: nie „Problem“, „Lücke“, „Hürde“, „leider“, „schade“,
„fehlt“, „verschenkt“, „Potenzial“; kein Rat, kein Konjunktiv-Wunsch („wäre schön“, „ihr
könntet“); kein „obwohl“, „trotzdem“, „dabei“ als Vorwurf; keine Folge („dadurch gehen Buchungen an
Booking“) und keine Vermutung über Gründe, Interna, Umsatz oder Provisionen; nie unwahre Nähe („ich
verfolge euch schon länger“, „ich kenne euch schon lange“). Einstieg nach `EINSTIEG DES OPENERS`,
Bewertungsanker mit Quelle im Einstieg, erster Buchstabe klein, Komma statt Strich, Pronomen nach
der Anrede (Person du, Betrieb mit Team ihr/euer, Sie-Kampagnen „auf Ihrer Website“, „bei Ihnen“).
Die Beobachtung gilt der Website, nie der begrüßten Person („du zeigst sie nicht“ ist falsch);
betreut laut Recherche eine Agentur die Website, wird sie nicht erwähnt.

Beispiele (erfunden, nur Struktur, nie wörtlich übernehmen):

- du, Hotel mit Team: „ich hab mir eure Bewertungen bei Google angeschaut, über 300 mit einem
  Schnitt von 4,8, auf eurer Website bin ich darauf nicht gestoßen.“
- du, Hotel mit Team: „ich hab mir eure Bewertungen bei HolidayCheck angeschaut, und jemand lobt den
  Blick vom Balkon auf den See, buchen kann man bei euch bisher nur per Anfrage.“
- Sie, Hotel: „ich habe mir Ihre Bewertungen bei Booking angeschaut, und jemand lobt das Brot aus
  der eigenen Backstube, gebucht wird bei Ihnen bisher nur per Anfrage.“
- falsch: „die Gäste lieben das Haus, leider fehlt auf der Website eine Online-Buchung, da wird viel
  Potenzial verschenkt.“ (Lob ohne Inhalt, Defizit-Wörter, Urteil)

**Speichern:** `save_lead_variables` nimmt für jede Chance-Variable den geschriebenen Winkel in
`angles` an (Pflicht), z. B. `angles: {"intro_chance": "chance"}`: `"chance"` nur für ein Intro
mit Stärke und Beobachtung, jeden Rückfall als `"lob"`. Der Winkel ist keine Variable und steht
nie im JSON der Variablen.

## Prompts der AI-Variablen `hallo`, `intro`, `routing` und `angebot_ausfuehrung`

Jede neue Kampagne hat `hallo`, `intro` und `routing`, wie in der App. `angebot_ausfuehrung` gibt es
in neuen Kampagnen nur mit „Angebot je Lead“, dann zusammen mit `offer_text` und `offer_cta` direkt
nach `intro`; mit Tests kommen `betreff_b` und das zweite Intro dazu (`references/fuer-erfahrene.md`);
`routing` steht zuletzt.
Weitere sind optional (z. B.
`proof`, `research_hook`, oder `firma` als Kurzname, wie `outreach-campaign` ihn vorsieht).
Namen: nur `a-zA-Z0-9_`, mit Buchstaben beginnend, eindeutig. Jede Variable wird pro Lead EINMAL
erzeugt: `{{ai.intro}}` steht deshalb NUR in Step 1; Follow-ups nutzen `{{ai.hallo}}` plus festen
Text; `{{ai.routing}}` steht nur im Abschied.

Bei der Generierung sieht das Modell den Prompt der Variable, die Lead-Daten, die Recherche, den
Kampagnenkontext und die Regeln, die der Server für Anrede und Opener mitgibt, nicht diesen
Skill (Server-Minimum 10 Zeichen je Prompt). Der Prompt trägt deshalb, was für diese Kampagne gilt;
was der Server ohnehin mitgibt, wird nicht kopiert.

Der `hallo`-Prompt MUSS enthalten:

- dass NUR die Begrüßungszeile ausgegeben wird, kein weiterer Satz, endet mit Komma;
- das Format passend zur `salutation` (Tabelle oben) samt Fallback („Hallo,“ in der Du-Form,
  „Guten Tag,“ in der Sie-Form);
- die Namensquelle: die Person, der die Versandadresse gehört; bei generischen Adressen
  (info@, kontakt@ …) der Entscheider/Inhaber aus der Recherche; ggf. Custom-Attribut mit dem
  Vornamen. Dazu das Verbot, Namen, Titel oder Rollen zu erfinden;
- das Verbot von Platzhaltern in Klammern, Gedankenstrichen und Emojis; echte Umlaute.

Der `intro`-Prompt enthält nur Kampagnenspezifisches, wie der Prompt der App
(`intro-station.md`) und der Blueprint-Guide es verlangen. Die allgemeinen Opener-Regeln (Abhebung,
Austauschtest, Anker-Reihenfolge, Bezug zum Angebot, positiver Schluss, Einstieg, Anrede, Verbote,
Form) legt der Server zur Laufzeit dazu; sie werden NICHT in den Prompt kopiert, auch keine
Floskel- oder Verbotslisten und keine Beispielsätze. Eine Kopie überstimmt den Server: Die
Anker-Reihenfolge im Prompt gilt vor der des Servers, und alte Regelstände blieben in der Kampagne
stehen. Aufbau:

- **Kontext:** Absender (Firma), Angebot, Zielgruppe, Ansprache (du oder Sie), dazu der feste
  Folgesatz der Mail 1, an den das Intro anschließt (z. B. „Deswegen war ich so frei …“), mit dem
  Hinweis, dass Angebot, Überleitung und Stand der Arbeit im festen Text stehen und das Intro sie
  nicht nennt und nicht vorwegnimmt; „Dies ist Email 1 von 4 der Sequenz.“
- **Sperrliste** der Kampagne (dieselbe wie in `researchAgentConfig.additionalPrompt`).
- **Ersatzsatz** für den Fall ohne Anker, der den Austauschtest besteht: genau ein Satz, ohne
  Einstieg und ohne Schluss, Branche und Region je Lead aus den Lead-Daten (nie als Klammer
  stehen lassen). Er behauptet nichts Unbelegtes über den Lead („so gut bewertet“, „seit Jahren“,
  „viele zufriedene Kunden“) und bezieht sich nur auf Branche oder Thema des Angebots. Standard der
  App: „als [Branche] in [Ort oder Region] bist du genau die Art Unternehmen, die wir suchen.“
- **Eigene Anker-Reihenfolge** nur, wenn die Kampagne bewusst von der des Servers abweichen soll.
- Schluss: „Schreibe jetzt nur den Opener. Nichts danach.“

Muster (die Vorlage der App, Platzhalter in `%…%` füllen):

```text
# Opener

Die allgemeinen Opener-Regeln (Abhebung, Austauschtest, Anker-Reihenfolge, positiver Schluss, Einstieg, Anrede) bekommst du zur Laufzeit. Hier steht nur, was für diese Kampagne gilt.

## Kontext

Du schreibst den Opener einer Cold-E-Mail.

- Absender: %firma%
- Angebot: %angebot%
- Zielgruppe: %zielgruppe%
- Ansprache: %ansprache%

Dein Text steht direkt unter der Anrede und wird im festen Mailtext %folgesatz% Das Angebot, die Überleitung und der Stand der Arbeit stehen also im festen Text. Du nennst sie nicht und nimmst sie nicht vorweg.

Dies ist Email 1 von 4 der Sequenz.

## Sperrliste

%sperrliste%

## Ersatzsatz

Gibt die Recherche keinen Anker her, der den Austauschtest besteht, schreibe genau diesen Satz, ohne Einstieg und ohne Schluss (Branche und Region pro Lead aus den Lead-Daten einsetzen, nie als Klammer stehen lassen): "%ersatzsatz%"

**Schreibe jetzt nur den Opener. Nichts danach.**
```

`%folgesatz%` ist der Rest eines Satzes, etwa „mit dem Satz „Deswegen war ich so frei …“
fortgesetzt.“ Die Intro-Regeln oben gelten trotzdem: für das Prüfen der Werte und überall, wo das
Plugin Intros selbst schreibt (`outreach-generate`, Abo-Lauf).

Der `routing`-Prompt ist wörtlich der ROUTING-PROMPT aus dem MCP-Prompt `campaign_blueprint_guide`
(deutsch je `salutation` die Du- oder die Sie-Fassung, englisch die eine Fassung), nicht selbst
formuliert oder gekürzt. Er schreibt je Lead den Routing-Absatz des Abschieds (höchstens 35 Wörter,
beginnt groß) in vier Fällen: A andere belegte Ansprechpartner mit Namen, B der feste Team-Satz,
C bei Einzelbetrieb oder eindeutig zuständigem Empfänger eine weiche Nachfrage zum Angebot der
ersten Mail, D bei einer zweiten angeschriebenen Person der Firma der Hinweis auf sie. Details:
`references/routing-baustein.md`.

Der `angebot_ausfuehrung`-Prompt einer neuen Kampagne ist immer die Anweisung von „Angebot je Lead“:
die abgenommene Vorlage (Deutsch Du, Deutsch Sie, Englisch), gefüllt aus den Karten des Kunden,
nach `references/fuer-erfahrene.md`, Teil 2. Nicht frei formulieren, nicht kürzen, keine eigenen
Regeln dazuschreiben; der Kunde sieht sie vor dem Anlegen. Beim Import ersetzt DealSupply den Prompt
durch die Anweisung, die es selbst aus den Karten baut (ohne `offerPrompt`); kleine Abweichungen der
gezeigten Fassung schaden deshalb nicht. `offer_text` und `offer_cta` tragen den
festen Prompt „Vom Server gesetzt: …“ und nie eine `offerRole`.

Bestehende Kampagnen mit einem eigenen `angebot_ausfuehrung`-Prompt (bis outreach 0.6.0) behalten
ihn. Wird er auf Wunsch des Nutzers überarbeitet, MUSS er enthalten:

- Kontext: Absender, Karte, den festen Angebotssatz davor, den festen Schlusssatz danach und die
  Lieferzusage des Nutzers (was er nach einer Antwort wirklich liefert);
- die Aufgabe je Karte: bei A ein Inhaltssatz, was für diesen Lead konkret im Deliverable drin
  wäre, im Konjunktiv; bei B ein Rahmensatz, der den Pilot an diesem Lead festmacht (was er
  konkret bekäme, bezogen auf seine Leistung, Zielkunden oder Region, und was er dafür gibt),
  nicht bei jedem Lead derselbe Satz; bei C der Feinheiten-Satz, der wörtlich mit „Ich bin gerade
  noch an den letzten Feinheiten dran, vor allem“ beginnt und genau ein Detail des schon
  erstellten Ergebnisses nennt, grammatisch vollständig, ohne „morgen“ und ohne „fertig werden“;
- die Quelle: Recherche und Website des Leads, für jeden Lead neu geschrieben; mit Schwerpunkten
  das Detail des gewählten Schwerpunkts als Grundlage; dazu einen ausformulierten Fallback-Satz
  aus der Lieferzusage für Leads ohne passenden Fund;
- die Grenzen: bei A und B nie als erledigte Arbeit (kein „erstellt“, „vorbereitet“, „liegt
  bereit“, kein „Ich bin gerade noch an den letzten Feinheiten dran“), bei C keine neue Leistung;
  nur Inhalte der Lieferzusage, keine Zahl,
  die weder Lieferzusage noch Recherche belegt, keine Frist, kein Gespräch oder Termin, kein
  zweites Angebot, keine Frage;
- Form: genau ein Satz, höchstens 25 Wörter (als eigene Zeile, mit der Anweisung nachzuzählen),
  beginnt groß (eigener Absatz), Pronomen gemäß
  `salutation`, keine Platzhalter, keine Gedankenstriche, echte Umlaute.

Ein vollständig ausformuliertes Paar `hallo`/`intro` steht in `references/beispiel-blueprint.md`;
die Anweisung von „Angebot je Lead“ mit Beispiel in `references/fuer-erfahrene.md`.

## Platzhalter in DealSupply

Aufgelöst werden nur diese Platzhalter (abschließende Liste für Betreff und Body):

- `{{ai.hallo}}`, `{{ai.intro}}`, `{{ai.<name>}}` (die Variablen der Kampagne)
- `{{lead.company}}`, `{{lead.website}}`, `{{lead.city}}` (der Server löst zusätzlich
  `lead.email` und `lead.phoneNumber` auf; in Copy nicht verwenden)
- `{{custom.<schlüssel>}}` (Custom-Attribute aus dem Import; leer, wenn der Lead keinen Wert hat)
- `{{accountSignature}}` nur im Body, in jeder Mail direkt unter der Grußformel (siehe Signatur)

Alles andere (`{{firstName}}`, `{{companyName}}`, `{{sender.*}}`, If-Blöcke, Default-Syntax)
landet als Rohtext beim Empfänger. Ein nicht erzeugter AI-Wert erscheint als „[NOT GENERATED]“.
Firmenname des Empfängers im Body: `{{lead.company}}` (bzw. `{{ai.firma}}`, wenn die Kampagne den
Kurznamen führt), nie `{{companyName}}`. Im Betreff nie das rohe `{{lead.company}}`, siehe
Betreffzeilen.

## Sequenz

Standard sind 4 Steps mit festen Rollen (Praxis-Belege: Eric Nowoslawski mit 2 bis 3 Mails; Jay mit
4 Steps und Routing, ohne künstliche Knappheit, Step 3 im selben oder einem neuen Thread als Test). `delayDays` ist die
Wartezeit VOR dem Step (kumuliert Tag 0, 3, 8, 15), eine ganze Zahl; `delayUnit` immer `"days"`.
Threads: Alle vier Mails laufen in EINEM Thread (Giuliano, 05.11.2026). Step 1 öffnet ihn, Step 2, 3
und 4 antworten darin, der Empfänger sieht sie als „Re: <Betreff von Step 1>“. Der Betreff steht
deshalb nur in Step 1, in Step 2, 3 und 4 bleibt er leer.

| Step | Rolle | `delayDays` | Wörter max. | Betreff | Inhalt |
|---|---|---|---|---|---|
| 1 | Entry Mail | 0 | 120 (Ziel 50-90; englisch 100), auch mit „Angebot je Lead“ | eigener, öffnet den Thread | `{{ai.hallo}}` + `{{ai.intro}}` + feste Überleitung mit Offer + zweiter Satz zum Angebot als eigener Absatz (A/B/C der feste Satz der Karte, D/E keiner) + EIN CTA, jeder als eigener Absatz + Grußformel und `{{accountSignature}}` + Abmeldezeile; mit „Angebot je Lead“ statt der drei Sätze `{{ai.offer_text}}`, `{{ai.angebot_ausfuehrung}}`, `{{ai.offer_cta}}` in drei Absätzen |
| 2 | Erinnerung | 3 | 50 | leer, Thread von Mail 1 | `{{ai.hallo}}` + nur nachhaken, weich wie eine schnell getippte Nachricht („du hast sicher viel um die Ohren, ich wollte nur sichergehen, dass meine Mail angekommen ist“). Kein Doppelpunkt-Opener, kein Offer, kein neuer Aspekt, kein `{{ai.intro}}` |
| 3 | Neuer Winkel (Mehrwert + Social Proof) | 5 | 80 | leer, Thread von Mail 1 | `{{ai.hallo}}` + EIN Beleg als erster Absatz, nach der Anrede klein weiter wie Mail 1: eine Case Story, eine Zahl, ein Ergebnis. HIER steht der Social Proof. Der Beleg steht als ganzer Satz aus Sicht des Absenders, mit ich oder wir, wie es zur Kampagne passt („wir haben schon über 1.000 Unternehmer begleitet“), nie dem Empfänger zugeschrieben (kein „ihr gebt an“, kein „du hast“). Zahlen und Fakten genau wie im Beleg des Nutzers: kein „bis zu“, „über“, „mehr als“ oder anderer Zusatz, der dort nicht steht; ein Ergebnis bleibt ein berichtetes Ergebnis, nie eine Zusage. Der Beleg steht für sich: kein Satz dahinter, der ihn erklärt, einordnet, relativiert oder abschwächt; eine kurze Geschichte mit Ergebnis hat höchstens zwei Sätze, ohne neue Zahl und ohne neue Tatsache. Fehlt ein Beleg, bringt Mail 3 einen neuen Winkel als ganzen Gedanken, ohne Zahl, ohne Fallbeispiel und ohne Kundennamen. Direkt nach dem Beleg dieselbe Schlussfrage wie Mail 1 mit dem Wort für die Sache statt „es“ (Karte C: „Wäre es in Ordnung, wenn ich dir morgen den Entwurf zusende? Völlig unverbindlich natürlich.“), damit die Mail ohne Mail 1 verständlich ist. Karten ohne Wort für die Sache (B, D, E, eigene Frage) nehmen die Frage aus Mail 1 wörtlich; Mail 3 endet mit einer Frage, nie mit einer bloßen Aufforderung („sag einfach kurz Bescheid“). Einzige Ausnahme ist „Angebot je Lead“: Dann endet Mail 3 neutral mit „Melde dich gerne, wenn das Thema für dich relevant ist.“ (Sie „Melden Sie sich gerne, wenn das Thema für Sie relevant ist.“, englisch “Feel free to get in touch if this is relevant for you.”), weil jeder Lead ein anderes Angebot bekommen haben kann (W5). Kein eigener Satz um das Angebot („Falls du … sehen möchtest, melde dich“), kein neues Offer, kein `{{ai.intro}}`. Eine eigene Schlussfrage weicht in DealSupply der Frage aus Mail 1 (seit 06.11.2026). Mit Schwerpunkten oder „Angebot je Lead“ nennen Mail 2 bis 4 nie einen Schwerpunkt oder ein einzelnes Angebot (sie gelten für alle Leads, das Angebot ist je Lead verschieden); DealSupply streicht einen Satz, der ein Schwerpunkt-Label enthält. Mit Grußformel, `{{accountSignature}}` und Abmeldezeile |
| 4 | Abschied mit Routing | 7 | 60 | leer, Thread von Mail 1 | `{{ai.hallo}}` + der feste Abschiedssatz der App („da ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung.“, in der Sie-Form gleich; englisch “Since I haven't heard back, I'll assume the timing isn't right, and that's completely fine.”) + `{{ai.routing}}` als eigener Absatz, nie ein fester Routing-Satz + Grußformel und `{{accountSignature}}`. Kein Offer |

- Gezählt wird der Body ohne Betreff und ohne Signatur, den Bezug aus `{{ai.intro}}` (bis zu
  2 Sätzen) eingerechnet. Die Limits sind Obergrenzen: kürzer ist erlaubt und meist besser.
  Bewährte Entry-Mails liegen bei 55 bis 86 Wörtern. Nie auffüllen.
- Der CTA wird von Step zu Step weicher: Erlaubnis erbitten → nur anstoßen → in Step 3 dieselbe
  Frage wie Step 1 mit dem Wort für die Sache → Tür offen lassen.
- Jedes Follow-up hat max. EINEN neuen Aspekt und beginnt mit einem ganzen, weichen Satz in der
  gewählten Ansprache. Das erste Wort nach `{{ai.hallo}}` (in jedem Step) schreibt man klein, weil
  es auf „Hallo …,“ folgt: „du hast sicher …“, nicht „Du hast sicher …“, auch in der Sie-Form („da ich
  bisher nichts gehört habe“, „ich wollte kurz nachfragen“, „bei rund 80 Gründungen …“); „Sie“, Namen
  und Substantive bleiben groß. DealSupply setzt ein solches Wort am Anfang des ersten Absatzes auch selbst
  klein (seit 06.11.2026).
- **Dringlichkeit** ist kein Standard-Step. Nur wenn der Nutzer einen echten Zeit- oder
  Kapazitätsgrund nennt, kommt sie als zusätzlicher Step zwischen Step 3 und den Abschied
  (dann 5 Steps, `delayDays` 0/3/5/7/7; Wortlimit 60; leerer Betreff, Thread von Mail 1). Ohne
  echten Grund entfällt sie, nichts Erfundenes und keine künstliche Knappheit.
- Fehlt dem Nutzer ein echter Beleg für Step 3: nachfragen, nicht erfinden; ohne Beleg bringt Step 3
  einen neuen Winkel ohne Zahl, ohne Fallbeispiel und ohne Kundennamen.
- Der Abschied trägt den Routing-Absatz immer als `{{ai.routing}}` (wie die App seit 31.10.2026):
  je Lead mit belegten Namen aus der Recherche („Ich bin mir nicht sicher, ob ich damit bei dir
  richtig bin oder eher bei Anna oder Tom. Gib mir gern kurz Bescheid.“), ohne belegte Namen der
  feste Team-Satz, bei Einzelbetrieb eine weiche Nachfrage zum Angebot. Body im JSON:
  `{{ai.hallo}}\n\nda ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung.\n\n{{ai.routing}}\n\n\nViele Grüße\n{{accountSignature}}`.
  Prompt und Fälle: `references/routing-baustein.md`. Bestehende Kampagnen mit festem Routing-Satz
  behalten ihn, außer der Nutzer will umstellen.

## Für Erfahrene: Tests in Mail 1 (A/B-Test)

Ein A/B-Test ist eine Option für Erfahrene, kein Standard (X1, X2, X5, X6). Neue Kampagnen haben
genau eine Fassung von Mail 1. Das Plugin fragt beim Anlegen einmal unter „Für Erfahrene: Tests in
Mail 1“ nach dem Betreff-Test und dem Intro-Test, je mit dem Satz der App, und empfiehlt „ohne
Tests“ (Wortlaut und Bau: `references/fuer-erfahrene.md`, Teil 1). Gewählt entstehen dieselben
Varianten wie in der App: Betreff-Test als B mit „Frage zu {{Firma}}“ (`{{ai.betreff_b}}`),
Intro-Test als nächste Variante mit dem zweiten Intro, beide zusammen A, B und C.

Regeln für einen sauberen Test, wenn der Nutzer ihn will: gleiche Karte und gleiches Angebot in
allen Varianten, genau EIN Hebel je Variante, gleiche Follow-ups, alle Varianten halten alle Regeln
dieses Skills. Ein echter Offer-Test ist ein Kartenwechsel und dann eine eigene Kampagne. Beim
Bearbeiten einer bestehenden Kampagne bleiben vorhandene Varianten stehen; nichts wird still
abgeschaltet.

## Betreffzeilen

Nur Step 1 trägt einen Betreff (er öffnet den Thread): 2-5 Wörter (der Firmenname zählt als ein Wort; gilt für A und B im Betreff-Test), keine Werbung, kein Spam-Wort, keine Großschreibung
ganzer Wörter, kein Ausrufezeichen, kein Prozentzeichen. Er klingt wie eine harmlose Frage eines
Menschen. Keine Ankündigung und keine Ergebnisansage („Website für …“, „Entwurf für …“, „Idee
für …“, „Website ist fertig“).

Firmenname im Betreff nur über `{{ai.firma}}` (bereinigter Kurzname, siehe `outreach-campaign`),
nie über das rohe `{{lead.company}}`: Importnamen sind oft Google-Titel oder Domains. Führt die
Kampagne keine Variable `firma`, steht im Betreff kein Firmenname, dann „kurze Frage“.

Bewährte Muster:

- „kurze Frage“ (Standard für jede Karte seit 05.11.2026, wie die App: Neugier, niedrige Hürde)
- „Frage zur Terminbuchung“ (wenn das Buchungssystem den Kern des Offers bildet)

Die früheren Karten-Betreffs („Meeting …“, „Anfrage für …“, „Deine Förderung“, „Partnerschaft …?“)
entfallen; weitere Varianten nur nach Copy-Beratung.

Step 2, Step 3 und Step 4 (und eine optionale Dringlichkeits-Mail): Betreff LEER, die Mails laufen im
Thread von Step 1. Kein neuer Betreff-Text, kein „Re:“. Ein eigener Betreff in Step 3 („kurzes
Update“) bricht den Thread; so lief es bis 05.11.2026, bestehende Kampagnen behalten das.

**Betreff-Test (für Erfahrene, standardmäßig aus; Betreff B seit 07.11.2026 „Frage zu {{Firma}}“):** Neue Kampagnen starten ohne Tests, in der App wie im Plugin (seit 10.11.2026). Nur auf Wunsch entsteht der Betreff-Test (Bau: `references/fuer-erfahrene.md`, Teil 1): Variante B von Mail 1 ist wörtlich Variante A, nur mit dem Betreff `{{ai.betreff_b}}`. Welche Variable der Betreff von B ist, sagt `emailGeneration.subjectVariables` (Rolle `subject_variant`), nicht der Name. Variante A behält „kurze Frage“. Ist der Intro-Test zusätzlich an, läuft er als Variante C mit „kurze Frage“ und `{{ai.intro_c}}`. Der Prompt der Variable kommt vom Server (`get_lead_data`, `emailGeneration.subjectVariables`) und sagt, welche Fassung gilt:

- **Kampagnen ab 07.11.2026 (E61):** Der Betreff von B lautet immer „Frage zu {{Firma}}“, englisch „question about {{Firma}}“, kein Detail und kein anderer Wortlaut. Der Kurzname steht unter `firma`: ohne Rechtsform (GmbH, GmbH & Co. KG, e.K., UG, Ltd), ohne Zusätze wie „Meisterbetrieb“ und ohne Ort, normal geschrieben statt in Großbuchstaben, außer die Firma führt ihren Namen als Kürzel („ZAR“). Steckt der Vorname der angeschriebenen Person im Firmennamen, fällt er weg („Immobilien Thomas Braun“ wird „Frage zu Immobilien Braun“); das gilt je Person, auch für Person 2. `save_lead_variables` setzt den Betreff selbst aus `firma` zusammen und prüft den Kurznamen gegen Firmennamen, Website und Ort; ohne sicheren Kurznamen bekommt der Lead den Betreff von Variante A (ohne eigenen Text gespeichert, beim Versand der aktuelle Betreff von A, als Rückfall markiert). Melde `firma` deshalb immer und `<name>__rueckfall: "ja"` nur ohne sicheren Kurznamen.
- **Ältere Kampagnen** behalten ihren gespeicherten Prompt mit dem persönlichen Betreff je Lead: 3 bis 6 Wörter, dasselbe Detail wie das Intro, beginnt direkt mit dem Detail, „Frage zu {{Firma}}“ nur als Rückfall (E22 bis E26, E53). Es gilt immer der Prompt der Variable.
- **Immer verboten:** der Vorname (E62), eine vorgetäuschte Kundenanfrage („ich suche eine Fassadenfirma“), Spam-Wörter (auch „Angebot“, „unverbindlich“), „Re:“/„AW:“/„Fwd:“, Großbuchstaben-Wörter außer einem Kürzel.

Gut: „Frage zu Becker Bäder“, „Frage zu Immobilien Braun“, „Frage zu ZAR“. Schlecht: „Frage zu Becker Bäder GmbH & Co. KG“ (Rechtsform), „Frage zu MÜLLER BAU“ (Großbuchstaben), „Frage zu Immobilien Thomas Braun“ (Vorname), „Dachsanierung am Hansmeyerhof“ (Detail statt Firma; so nur in älteren Kampagnen).

In `check_copy.py` steht er als Zeile
„Betreff B: …“ unter „Betreff: …“; den Kurznamen der Firma (zählt als ein Wort) gibt `--firma` oder
eine Zeile „Kurzname: …“ an; `--sprache en` prüft eine englische Entry Mail gegen 100 Wörter.

NICHT: „Kostenlose Beratung für …“ (zu lang, Spam), „Exklusives Angebot - jetzt zugreifen!“
(Spam-Trigger), „Re: Ihre Anfrage“ (Fake-Reply).

## Harte Verbote (jede Verletzung ist ein Fehler)

Im Body jeder Mail:

- Kein Pitch: „Wir helfen [Zielgruppe] dabei …“, „Das machen wir seit X Jahren …“, „Als
  [Zertifizierung/Partner] …“, kein Satz, der die eigene Firma beschreibt.
- Kein zweiter CTA („Antworte mir oder buche hier …“).
- Kein Link in Mail 1. Ab Mail 3 maximal einer (nur Kalender oder Website).
- Kein Bold, keine Bulletpoints, keine Emojis, kein HTML-Layout.
- Keine M-Striche (—) und keine Gedankenstriche als Trenner (siehe Tonalität).
- Kein Doppelpunkt-Opener direkt nach der Anrede in Follow-ups („kurz nachgehakt:“, „kurzes
  Update:“, „zur Erinnerung:“).
- Keine sichtbaren Platzhalter ([Branche], [Name], `{{firstName}}`).
- Social Proof und Case Studies NUR in Step 3, nie in Step 1.
- Keine Opt-out-Fachsprache, auch nicht unter der Signatur: kein „STOPP“ oder „Stop“, kein
  „abmelden“, „abbestellen“, „austragen“, „unsubscribe“ oder „Opt-out“. Stattdessen die feste
  Abmeldezeile (siehe Anatomie).

**Spam-Wörter** — im Betreff komplett verboten, im Body vermeiden: „gratis“, „100 %“,
„garantiert“, „Garantie“, „jetzt zugreifen“, „jetzt handeln“, „begrenztes Angebot“, „nur heute“,
„exklusives Angebot“, „hier klicken“, „Rabatt“, „Sonderpreis“, „Gewinner“, „Sie haben gewonnen“,
„dringend“, „risikofrei“, „ohne Risiko“, „Geld verdienen“.
„unverbindlich“ ist kein Spam-Wort; der Standard-CTA endet mit
„Völlig unverbindlich natürlich.“

**Verbotene Offer-Begriffe:** „kostenlose Analyse“, „kostenlose Beratung“, „kostenloses
Erstgespräch“, „unverbindliches Audit“, „Potenzial-Check“, „Strategiegespräch“ (und allgemein
„Analyse“, „Audit“, „Beratung“, „Erstgespräch“ als Offer).

**Sonderfall „kostenlos“:** im Betreff nie (auch nicht „kostenfrei“ oder „gratis“), im Body
höchstens einmal und nur direkt am konkreten Deliverable („ein kostenloses Google Ads Setup“),
nie als Eigenschaft der Zusammenarbeit („ein kostenloses Erstgespräch“), nie zusammen mit einem
zweiten Trigger.

## Selbstprüfung (vor dem Speichern, verbindlich)

Geh jede Mail einmal durch und korrigiere, bevor du `create_campaign`/`edit_campaign` aufrufst
oder Werte speicherst. Nach jeder Korrektur von vorne beginnen: Kürzungen erzeugen neue Fehler.

1. Wörter zählen: jeder Step im Limit? Wenn drüber: kürzen, nicht umformulieren.
2. Pitch-Scan: kommt „wir helfen“, „wir sind“, „wir machen“, „seit … Jahren“, „als … Partner“
   vor? Jeder Treffer fliegt raus.
3. CTA zählen: genau einer pro Mail?
4. Steht das Offer nur in Step 1 (Step 3 nennt es nur in der Schlussfrage, derselben wie in Step 1,
   mit dem Wort für die Sache, und geht nach der Anrede klein weiter)?
5. Steht `{{ai.intro}}` nur in Step 1?
6. Steht der Social Proof in Step 3 und nicht früher?
7. Zeichen-Scan: M-Striche, Emojis, Bold, Bulletpoints, Links in Step 1?
8. Spam-Scan: Betreff und Body gegen die Wortliste. „kostenlos“ höchstens einmal im Body?
9. Platzhalter-Scan: kein [Klammer-Feld]? Jede `{{…}}`-Variable gegen die abschließende Liste
   prüfen. Endet jede Mail mit der Grußformel und `{{accountSignature}}` darunter, ohne Unterschrift
   mit Name, Rolle oder Firma und ohne `{{sender.*}}`-Variablen?
10. Betreff von Step 1: 2-5 Wörter, kein Spam-Wort, keine Großschreibung, keine Ankündigung,
    Firmenname nur über `{{ai.firma}}`? Step 2, Step 3 und Step 4 ohne Betreff?
11. Trägt der `intro`-Prompt nur Kontext (mit dem festen Folgesatz), Sperrliste und einen
    Ersatzsatz, der keine unbelegte Tatsache behauptet, ohne kopierte Opener-Regeln, Verbotslisten
    oder Beispielsätze (eine eigene Anker-Reihenfolge nur, wenn die Kampagne bewusst abweicht)?
    Steht dieselbe Sperrliste in den Research-Vorgaben? Ist der `routing`-Prompt wörtlich der
    ROUTING-PROMPT zur `salutation`, und trägt der Abschied `{{ai.routing}}` als eigenen Absatz?
12. Passen `salutation`, `hallo`-Prompt und die Pronomen des festen Texts zusammen (kein
    „Hallo Herr/Frau …“, „… Team,“ oder „Hallo zusammen,“ mit Du-Text, kein du/ihr-Wechsel in einem Satz und keine Anrede mit ihr/euch, auch
    nicht ohne Ansprechpartner: „Hallo,“ und „dein Team“)?
13. Zeigst du dem Nutzer Beispielwerte für `hallo`/`intro`: fertiger Klartext ohne
    `{{…}}`-Platzhalter, Namen und Firmen erkennbar fiktiv, Angle-Reihenfolge und Verbote
    eingehalten?
14. Umlaut-Scan über ALLES (Sequenz, Prompts, Konfiguration): steht irgendwo „ae“, „oe“, „ue“
    oder „ss“ als Ersatz für ä, ö, ü, ß („fuer“, „Gruesse“, „groesser“, „heisst“)? Ersetzen.
15. Steht unter der Signatur von Step 1 und Step 3 die feste Abmeldezeile in der Anrede der
    Kampagne, ohne „PS:“, und nirgends „STOPP“ oder andere Opt-out-Fachsprache?
16. Zweiter Satz zum Angebot in Step 1 passend zur Karte: bei A, B und C der feste Satz der Karte
    wörtlich, bei D und E keiner, Angebotssatz, zweiter Satz und Schlussfrage je in einem eigenen
    Absatz? Mit „Angebot je Lead“ stattdessen `{{ai.offer_text}}`, `{{ai.angebot_ausfuehrung}}` und
    `{{ai.offer_cta}}` in drei Absätzen, die Anweisung nach der Vorlage und Mail 3 mit dem neutralen
    Schluss? Schlusssatz ohne „Link“?
17. Varianten von Mail 1 nur, wenn der Nutzer Tests gewählt hat, und dann genau wie in
    `references/fuer-erfahrene.md`, Teil 1?
18. Step 3: steht der Beleg als Ich- oder Wir-Satz mit den Zahlen genau wie vom Nutzer genannt,
    ohne Satz dahinter, der ihn erklärt oder einordnet, direkt gefolgt von der Schlussfrage?
    Opener-Regeln in Beispielwerten: Plural oder „immer wieder“ nur ab drei Rezensionen mit
    diesem Lob?

## Prüfliste nach Code-Regeln

Diese Regeln lassen sich mechanisch prüfen. DealSupply prüft sie beim Anlegen nicht, also prüfst du
sie: vor dem Anlegen der Sequenz und beim Review der Werte abhaken. „Hart“ = Fehler, „weich“ =
Hinweis, der begründet werden muss.

| Regel | Prüfung | Stufe |
|---|---|---|
| Wortlimit | Step 1-4 max. 120/50/80/60 Wörter (englisch Step 1 max. 100), ein zusätzlicher Dringlichkeits-Step max. 60 (Platzhalter zählen nicht mit, den Intro-Umfang einrechnen; gilt auch mit „Angebot je Lead“) | hart |
| Zielkorridor | Entry-Mail unter 50 Wörtern: trägt der Bezug? | weich |
| Kein Gedankenstrich | kein „—“ und kein „–“ im Text | hart |
| Anführungszeichen geschlossen | jedes „ schließt mit “, nie mit " | hart |
| Kein Pitch | kein „wir helfen“, „wir sind ein/eine/der/die/seit“, „wir bieten“, „seit (über) N Jahren“, „als zertifizierter/offizieller/Google/Meta … Partner“, „mein Name ist“, „unser Unternehmen“ | hart |
| Kein Platzhalter | kein sichtbares `[Feld]` | hart |
| Bekannte Variablen | nur `{{ai.*}}`, `{{lead.company}}`, `{{lead.website}}`, `{{lead.city}}`, `{{custom.*}}`, im Body `{{accountSignature}}` | hart |
| Signatur | jede Mail endet mit der Grußformel und `{{accountSignature}}` darunter, keine Unterschrift mit Name, Rolle oder Firma | hart |
| Routing | der Abschied trägt `{{ai.routing}}` als eigenen Absatz, kein fester Routing-Satz; die Variable `routing` existiert | hart |
| Kein Emoji | keine Emojis/Symbole | hart |
| Keine Formatierung | kein `**fett**`, keine Zeile, die mit „-“, „*“ oder „•“ beginnt | weich |
| „kostenlos“ | höchstens einmal pro Mail | weich |
| Betreff ohne Spam | kein Spam-Wort, kein „kostenlos“, „kostenlose“, „kostenloses“, „kostenfrei“ | hart |
| Betreff-Länge | max. 5 Wörter (Step 1) | weich |
| Betreff-Platzhalter | kein `{{lead.company}}` im Betreff; Firmenname nur als `{{ai.firma}}` | hart |
| Follow-up-Betreff | `subject` in Step 1 nicht leer, in Step 2, 3 und 4 (sowie in einem Dringlichkeits-Step) leer | hart |
| Schlussfrage in Step 3 | Step 3 endet mit einer Frage (dieselbe wie Step 1, mit dem Wort für die Sache, wo die Karte eins hat); mit „Angebot je Lead“ mit dem neutralen Schluss | hart |
| Betreff ohne Schreien | kein Wort mit 4+ Großbuchstaben, kein „!“ | weich |
| Ein CTA | kein „oder/alternativ … buchen/klicken/vereinbaren/reservieren/anrufen/Termin sichern“ neben der Antwort-Bitte | hart |
| Kein Link in Mail 1 | kein „http(s)://“, „www.“, „calendly.com“, „hier buchen“ in Step 1 | hart |
| Zweiter Angebotssatz | Step 1 bei Karte A/B/C mit dem festen Satz der Karte (oder mit „Angebot je Lead“ den drei Platzhaltern), bei D/E ohne; Angebotssatz, zweiter Satz und Schlussfrage je ein eigener Absatz; ein fehlendes `{{ai.angebot_ausfuehrung}}` ist kein Fehler | hart |
| Varianten | Varianten von Step 1 nur bei gewählten Tests; ohne Tests ist eine fehlende Variante kein Fehler | hart |
| Schlusssatz ohne Link | kein „Link“ im CTA von Step 1 | hart |
| Offer ist kein Gespräch | Step 1 enthält keinen verbotenen Offer-Begriff (außer verneint: „statt …“, „kein …“) | hart |
| Intro nur in Step 1 | `{{ai.intro}}` in keinem Step ab 2 | hart |
| Anrede überall | jeder Step enthält `{{ai.hallo}}` | weich |
| Umlaute | keine Transliteration (fuer, ueber, gruess, koennen, moechte, groess, persoenlich, moeglich, waere, haette …) in Sequenz, Prompts und Konfiguration | hart |
| Keine Opt-out-Fachsprache | kein „STOPP“, „Stop“, „abmelden“, „abbestellen“, „austragen“, „unsubscribe“, „Opt-out“ in Betreff, Body und unter der Signatur | hart |
| Abmeldezeile | Step 1 und 3 enden nach der Signatur mit der festen Abmeldezeile („Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.“; erkannt an „kein Thema für“, die frühere Fassung zählt auch) | weich |
| Abstand vor dem Gruß | zwei Leerzeilen zwischen dem letzten Satz und der Grußformel | weich |

## Verwandt

- `references/copy-lehre.md` — Abhebung und Austauschtest (zentrale Opener-Regel mit
  Gegensatzpaaren, Sperrliste, Einstiegswechsel), Goldene Formel, Angle-Hierarchie, Überleitungsbausteine,
  zweiter Satz zum Angebot je Karte, Beispiele A/B/C/E, Follow-ups mit Varianten, 12 Gebote, Anti-Patterns,
  Zustellregeln, Prüfdurchlauf.
- `references/marketing-offer.md` — Karten A-E im Detail, Werttest, Offer-Killer,
  Reziprozität, was kein Offer ist.
- `references/beispiel-blueprint.md` — vollständiger Blueprint (Karte C, Du-Form, 4 Steps,
  `hallo`-, `intro`- und `routing`-Variable, fester zweiter Satz, `{{accountSignature}}`) zum Anlegen mit `create_campaign`, dazu die
  Variante für Karte A und B.
- `references/fuer-erfahrene.md` — Tests in Mail 1 und „Angebot je Lead“: die Frage beim Anlegen,
  Felder, Vorlage DE und EN, Blueprint, Beispiel, Prüfung.
- `references/routing-baustein.md` — der Abschied mit `{{ai.routing}}`: Body, Prompt, Fälle.
- Skill `outreach-launch` — Versand nach dem Export (Domains, Warm-up, Instantly, KPIs) und wann
  bei schwachen Zahlen Copy, Offer oder Liste geändert werden.
