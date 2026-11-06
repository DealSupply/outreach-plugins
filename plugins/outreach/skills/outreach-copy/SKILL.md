---
name: outreach-copy
description: 'Use when user says "Cold-Mail schreiben", "Cold-Mail prüfen", "Copy prüfen", "Kampagnen-Copy", "Sequenz schreiben", "Betreffzeile", "Opener", "Intro-Prompt", "hallo-Prompt", "Marketing-Offer formulieren", "Offer schärfen", "Feinheiten-Satz", "zweiter Angebotssatz", "angebot_ausfuehrung", "Follow-ups schreiben", or wants to write, review or fix the copy of an outreach campaign. Verbindliche Cold-Mail-Copy-Regeln (Anatomie der Entry-Mail, Offer-Karten A-E, zweiter Satz zum Angebot je Karte, 4er-Sequenz, Wortlimits, Intro- und Anrede-Regeln, Verbote, Selbstprüfung). outreach-campaign, outreach-generate und outreach-verify laden diesen Skill verbindlich.'
---

# Outreach Copy — die Cold-Mail-Regeln für Kampagnen

Dieser Skill ist die eine Copy-Doktrin für alles, was über den Outreach-MCP an Text entsteht:
Sequenz (Betreff und Body jedes Steps), die Prompts der AI-Variablen `hallo` und `intro` (bei
Karte A und B dazu `angebot_ausfuehrung`) und die pro Lead erzeugten Werte. Er gilt verbindlich für:

| Skill | Wann diesen Skill laden |
|---|---|
| `outreach-campaign` | bevor eine Zeile Sequenz oder Variablen-Prompt entsteht (`create_campaign`, `edit_campaign`) |
| `outreach-generate` | bevor `hallo`/`intro` für einen Lead geschrieben werden (`save_lead_variables`) |
| `outreach-verify` | beim Prüfen der Werte (`get_lead_variables`) vor `approve_lead_variables`/`reject_lead_variables` |

Ausführliche Lehre mit allen Beispielen: `references/copy-lehre.md`. Offer-Lehre:
`references/marketing-offer.md`. Ein vollständig ausformulierter Blueprint:
`references/beispiel-blueprint.md`. Bei einem Widerspruch zwischen diesen Dateien gilt diese
SKILL.md.

## Kampagnensprache

Jede Kampagne hat eine Sprache (`campaign.language`, ab ListM8-MCP 4.7.0): `de` (Standard) oder
`en`. Bei der Generierung steht sie in `get_lead_data` → `emailGeneration.language`. Fehlt das
Feld (älterer Server), ist die Kampagne deutsch.

- **`de`:** Dieser Skill gilt vollständig, mit allen deutschen Sprachregeln.
- **`en`:** Englische Kampagnen haben eigene Regeln, natürliches US-Englisch, nie aus dem
  Deutschen übersetzen. Die deutschen Sprachregeln dieses Skills (du/Sie, Anführungszeichen „…“,
  Umlaute, deutsche Beispielsätze und Reaktionsformen) gelten dort nicht. Stattdessen:
  - Anrede `Hi {first name},` (nur Vorname, ohne du/Sie); ohne benennbare Person `Hi there,`.
  - Grußformel `Best,` über der Signatur.
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
| `sie` (Ausnahme) | Sie/Ihnen/Ihre | „Hallo Frau Nachname,“ / „Hallo Herr Nachname,“ | „Guten Tag,“ |

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
  „Guten Tag,“.
- NIE „Hallo Herr/Frau Nachname,“ zusammen mit Du-Text (`du`), nie „Hallo <Firma> Team,“ oder
  „Hallo zusammen,“, nie „Hey …“, nie Sie und du gemischt.
- Die Anrede kommt immer aus `{{ai.hallo}}`. Kein `{{firstName}}`, kein `{{companyName}}`, kein
  `{{custom.vorname}}` direkt in Betreff oder Body: Es gibt kein Vornamen-Feld, und ein leeres
  Attribut ergibt „Hallo ,“. Liegt der Vorname als Custom-Attribut aus dem Import vor (Schlüssel
  zeigt `get_lead_data` unter `customAttributes`), nennt der `hallo`-Prompt ihn als Quelle.
- Titel („Dr.“) nur in der Sie-Form und nur, wenn er belegt ist.

## Schritt 1: Offer-Typ wählen

Der Marketing-Offer ist nicht die Dienstleistung des Nutzers, sondern der Türöffner: das
konkrete, greifbare Ding, das den Erstkontakt trägt. Wähle GENAU EINE Karte und begründe die
Wahl dem Nutzer in einem Satz.

| Karte | Wann | Überleitung (statisch, für alle Leads gleich) |
|---|---|---|
| A: Kostenlose Teildienstleistung | Standard, funktioniert in 80 % der Fälle. Im Zweifel diese. | „Genau deshalb bieten wir aktuell für [Anzahl] Unternehmen in [Region] ein kostenloses [Deliverable] an.“ |
| B: Tester/Pilotprojekt | Neues Produkt, wenig Referenzen, Exklusivität als Narrativ | „Genau solche Unternehmen suchen wir gerade. Wir starten [Projekt] mit [Anzahl] Betrieben in [Region].“ |
| C: Konkretes Deliverable (Reziprozität) | Kleine Zielgruppe, hohe Reply Rate nötig. Höchste Reply Rate, mehr Aufwand pro Lead. | „Deswegen war ich so frei und habe [Deliverable] für dich erstellt.“ |
| D: Förder-Hook | Nutzer hat förderfähige Produkte | „Wusstest du, dass der Staat aktuell bis zu [Prozent] der [Kosten] übernimmt?“ (nennt der Nutzer Träger oder Programm, steht er statt „der Staat“: „das Land Baden-Württemberg“) |
| E: Partner gesucht | Nischen-Anbieter, Kooperation auf Augenhöhe | „Genau solche [Branche] suchen wir als Partner. Wir haben regelmäßig [Anfragen], die zu dir passen würden.“ |

Die Klammern füllst du beim Schreiben der Sequenz aus den Angaben des Nutzers; im fertigen Text
steht keine Klammer mehr. Pronomen an die `salutation` anpassen (Standard `du`: dir/dich/dein).

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
3. Sonst einen Vorschlag nach Karte A machen und vom Nutzer bestätigen lassen.

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
Zweiter Satz zum Angebot         4. eigener Absatz, je Karte: A, B und C
                                    {{ai.angebot_ausfuehrung}} (je Lead), D und E keiner
EIN Frage-CTA                    5. niedrige Hürde
Signatur im Klartext             6. Grußformel, Name, „Rolle - Firma“
Abmeldezeile                     7. nach einer Leerzeile unter der Signatur (Step 1 und 3)
```

**Zweiter Satz zum Angebot (Stand 05.11.2026):** Nach dem Angebotssatz folgt in Mail 1 immer ein
zweiter Satz zum Angebot, als eigener Absatz zwischen Offer und CTA. Er ist KEIN zweites Offer und
KEIN zweiter CTA, sondern beschreibt dasselbe Deliverable eine Schicht tiefer. Was er sagt, hängt
von der Karte ab:

| Karte | Inhalt des Satzes | Wer schreibt ihn |
|---|---|---|
| C: Konkretes Deliverable | Fortschritt: der Feinheiten-Satz, genau ein Detail je Lead | KI je Lead, `{{ai.angebot_ausfuehrung}}` |
| A: Kostenlose Teildienstleistung | Inhalt: was für diesen Lead konkret drin wäre | KI je Lead, `{{ai.angebot_ausfuehrung}}` |
| B: Tester/Pilotprojekt | Rahmen, an diesem Lead festgemacht: was er im Pilot bekäme und was er dafür gibt | KI je Lead, `{{ai.angebot_ausfuehrung}}` |
| D: Förder-Hook, E: Partner gesucht | kein weiterer Satz, die Überleitung hat schon zwei Sätze | entfällt |

**Ein Satz je Lead bei A, B und C (`{{ai.angebot_ausfuehrung}}`, Stand 05.11.2026):** Die KI
schreibt den zweiten Satz je Lead neu, passend zu Recherche und Website des Leads. Auch bei C ist
der Feinheiten-Satz kein fester Text mit Lücke mehr: Ein Detail für die ganze Liste las sich in
jeder Mail gleich und oft grammatisch schief („vor allem die Platzierung der Anfrageoption“).

- **C, Feinheiten-Satz (Wortlaut der Regel vom 05.11.2026):** Ein Satz, der genau so beginnt:
  „Ich bin gerade noch an den letzten Feinheiten dran, vor allem“ und dann genau ein Detail des
  schon erstellten Ergebnisses nennt, an dem noch gefeilt wird, passend zu diesem Lead (aus seiner
  Recherche oder dem Detail des Schwerpunkts), grammatisch vollständig (z. B. „an der …“). Kein
  „morgen“, kein „fertig werden“, keine neue Leistung. Englisch: „I'm just finishing up the last
  few details, mainly …“. Das „morgen“ steht im Schlusssatz („… wenn ich es dir morgen
  zusende?“). Beispiel: „Ich bin gerade noch an den letzten Feinheiten dran, vor allem an den
  Vorher-nachher-Bildern deiner Implantat-Fälle.“

- **A, Inhaltssatz:** was für diesen Lead konkret im Deliverable drin wäre, im Konjunktiv.
  Beispiel: „Darin wären deine drei meistgebuchten Behandlungen mit Preis, Ablauf und
  Buchungsknopf, gebaut aus den Texten und Fotos, die du schon online hast.“
- **B, Rahmensatz (Wortlaut der Regel vom 05.11.2026):** Ein Satz, der den Rahmen des Pilots an
  diesem Lead festmacht: was er im Pilot konkret bekäme, bezogen auf etwas aus seiner Recherche
  (seine Leistung, seine Zielkunden, seine Region), und was er dafür gibt (ehrliches Feedback).
  Nicht bei jedem Lead derselbe Satz. Beispiel: „Im Pilot schreibe ich dir die erste Mail an
  einen deiner Wunschkunden aus dem Maschinenbau, du sagst mir dafür ehrlich, was du davon
  hältst.“
- **A und B nie mit dem Feinheiten-Wortlaut:** Er behauptet Arbeit, die es dort vor der Antwort
  nicht gibt.
- **Mit Schwerpunkten:** Grundlage des Satzes ist das Detail des Schwerpunkts, den die KI für den
  Lead wählt, zugeschnitten auf die Recherche. Bei Pilot und Partner steht der Schwerpunkt selbst
  nicht im Angebotssatz. Gewählt wird je Lead der Schwerpunkt, der nach Schwerpunkt-Prüfung und
  Recherche am besten passt; das Haupt-Offer (Rang 1) nur, wenn keiner klar besser passt (seit
  06.11.2026). Prüffragen fragen nur nach Sichtbarem auf der Website (Seite, Formular, Buchung,
  Bilder, Karriereseite, Bewertungen, Vertriebsrollen), nie nach Absichten, internen Abläufen oder
  Werkzeugen; am besten nach einer Sache, die eine feste Zeile der Recherche beantwortet (Fragen
  nach Preisen oder Gutscheinen bleiben meist „unbekannt“). Ist nicht Rang 1 gewählt, nennen der
  zweite Satz und das Routing nichts vom Haupt-Offer (seit 06.11.2026).
- **Grenzen für alle drei:** bei A und B nie als erledigte Arbeit (kein „erstellt“,
  „vorbereitet“, „liegt bereit“, kein Feinheiten-Wortlaut), bei C nur das schon Erstellte; nur
  Inhalte, die die Lieferzusage des Nutzers deckt; keine Zahl, die weder Lieferzusage noch Recherche belegt; keine Frist; kein Gespräch, Termin oder
  Call; keine Frage, der CTA folgt fest; ein Satz mit höchstens 25 Wörtern, am besten 15 bis 20
  (nachzählen, ein Strichpunkt zählt mit, ein längerer Satz wird gekürzt); Pronomen gemäß `salutation`. Kein zweiter Prüf- oder
  Korrekturlauf: Der Prompt muss den Satz beim ersten Schreiben richtig machen.
- Im Body steht die Variable als eigener Absatz direkt nach dem Angebotssatz. Sie wird je Lead
  einmal erzeugt und steht deshalb, wie `{{ai.intro}}`, nur in Step 1. Ihren Prompt regelt
  „Prompts der AI-Variablen“ unten, ausformulierte Prompts für A, B und C stehen in
  `references/beispiel-blueprint.md`.

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
„das“. Jede Kampagne hat außerdem ein eigenes Wort für die Sache (in ListM8 auf der Angebots-Seite unter der Schlussfrage, vom Assistenten vorgeschlagen): Es steht nur in der Frage von Mail 3 und gilt dort, solange Mail 3 nicht das Wort des Schwerpunkts trägt (Variable `{{ai.offer_noun}}`); Mail 1 behält „es“ bzw. „das“; ohne Wort nimmt Mail 3 die Frage aus Mail 1 wörtlich (06.11.2026). Kein „Link“ im Schlusssatz (nicht „… wenn ich dir morgen den Link dazu schicke?“), die Sache
wird zugesendet. „morgen“ und „zusenden“ nur bei C, und nur, wenn der Nutzer das Deliverable nach der
Antwort wirklich bis zum nächsten Tag liefern kann, sonst „… wenn ich es dir zusende?“. Der Zusatz
„Völlig unverbindlich natürlich.“ senkt die Hürde und ist kein zweiter CTA. Eine Schlussfrage, die
der Nutzer selbst bestätigt hat, gilt wörtlich. Der Betreff von Step 1 ist bei jeder Karte „kurze
Frage“. Kein Terminvorschlag und kein Link in Mail 1.

Die Master-Formel (Kurs Outbound 3.0, Lektion 2.4) in fünf Bausteinen: Lob → „Deswegen …“ →
konkretes Offer → Fertigstellung → CTA mit wenig Verpflichtung. Im Kurs trägt der Halbsatz „… und
werde morgen mit dem Entwurf fertig.“ die Fertigstellung, bei uns trägt sie das „morgen“ im
Schlusssatz. „Morgen“ wirkt stärker als „schon fertig“: Der Lead sieht, dass gerade noch für ihn
gearbeitet wird.

**Kein Pitch, keine Selbstvorstellung im Body.** Authority und Proof gehören in die Signatur bzw.
in Step 3. Über den Empfänger schreiben, nie über den Absender („Du bekommst …“, nicht „Wir
bieten …“).

Muster je Karte, direkt nach dem Lob-Intro, jeder Baustein ein eigener Absatz. Karte C (der
Feinheiten-Satz kommt je Lead aus `{{ai.angebot_ausfuehrung}}`, hier eine mögliche Fassung):

```
Deswegen war ich so frei und habe dir einen kompletten Webseitenentwurf inklusive
Buchungssystem erstellt.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an der Optimierung für Google
und KI-Suchmaschinen.

Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.
```

Karte A (der Satz nach dem Angebot kommt je Lead aus `{{ai.angebot_ausfuehrung}}`):

```
Genau deshalb bieten wir aktuell für [Anzahl] Praxen in [Region] einen kostenlosen Entwurf
für eine neue Startseite mit Online-Terminbuchung an.

{{ai.angebot_ausfuehrung}}

Wäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich natürlich.
```

Karte B:

```
Genau solche Agenturen suchen wir gerade. Wir starten ein Pilotprojekt für persönliche
Erstmails mit [Anzahl] Agenturen in [Region].

{{ai.angebot_ausfuehrung}}

Wärst du grundsätzlich offen dafür?
```

**Signatur:** Name, Rolle und Firma des ABSENDERS als Klartext aus den Angaben des Nutzers, z. B.
„Viele Grüße\nAngela Selbert\nGeschäftsführerin - njoy online marketing GmbH“. Nie
`{{sender.firstName}}`, `{{sender.company}}` o. Ä. (gibt es nicht). Ohne bekannten Absendernamen
nur „Viele Grüße“. Schlank: keine Auszeichnungen, Links, Telefonnummern oder Social-Leisten.

**Signatur aus dem Konto:** Füllt `outreach-campaign` eine Kampagne, die die App angelegt hat
(Start-Satz „Richte mit outreach die Kampagne #… ein“, Ablauf „Genannte leere Kampagne füllen“),
steht statt der Klartext-Signatur direkt unter der Grußformel `{{accountSignature}}`:
„…?\n\n\nViele Grüße\n{{accountSignature}}“ (englisch „…?\n\n\nBest,\n{{accountSignature}}“). Instantly setzt dort
die Signatur des Versandpostfachs ein. Dann nicht nach Name, Rolle und Firma fragen und keine
Unterschrift in den Mailtext schreiben; was unter der Signatur steht, folgt unter `{{accountSignature}}`.

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
  Vergangenheit erzählt wie unter Kollegen, im Ton der fünf Formen mit den besten Antwortquoten
  (Prod-Dump 23.10.2026): „das fand ich richtig schön“, „das ist mir direkt hängen geblieben“, „das hat mir gut gefallen“, „das fand ich richtig sympathisch“, „das hat mich angesprochen“; „richtig“ ist erlaubt, Übertreibung („total begeistert“)
  und Floskeln nicht; am Detail und nie ohne es. Sie wechselt von Lead zu Lead, nie steht in allen Mails
  derselbe Satz: Der Block `SCHLUSS DES OPENERS` im System-Prompt (`emailGeneration.systemPrompt`)
  schlägt je Lead eine Form vor, als Richtung und Tonlage, nicht als Pflicht. Passt eine eigene kurze Reaktion besser zum Detail, im selben Ton formulieren (bei einer historischen Kegelbahn etwa „da musste ich direkt schmunzeln“), höchstens etwa sechs Wörter, keine Floskel; passt der
  Vorschlag nicht („schön“ oder „sympathisch“ hinter einer Bewertungszahl oder einem technischen
  Detail), eine eigene bilden. Fehlt der Block (älterer Server), die Reaktion je Lead selbst variieren. Hinter einer Bewertungszahl steht immer die Reaktion.
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
  bemerkenswert“, „Hammer“, „beeindruckend“. Abgrenzung: „finde ich stark“ ist eine Formel, ein
  gegenwärtiges Urteil ohne Inhalt; eine Würdigung oder Reaktion am benannten Detail ist erlaubt,
  Seltenheit und Superlativ nur mit dem Detail („so eine Nachsorge ist mir noch nicht begegnet“), nie allein
  („das sieht man selten“, „beeindruckend“) (siehe Positiver Schluss). Die Formeln machen alle Opener gleich (gilt zusätzlich
  zu den übrigen Opener-Regeln). Auch in Beispielen und Prompts nie als Muster stehen lassen:
  Modelle kopieren Beispiele.
- Anker-Rangfolge: 1) Lob aus Bewertungstexten (Paraphrase; Plural oder „immer wieder“ nur, wenn
  mindestens 2 Bewertungen es tragen) 2) abhebendes Detail von der Website, auch Wachstum oder
  Stellenanzeige als Erkenntnis 3) Anzahl und Schnitt der Bewertungen als eigener Anker, nur bei
  mindestens 30 Bewertungen und einem Schnitt ab 4,5; Zahl gerundet („über 200“), Schnitt mit Komma
  („4,8“); Werte aus dem Import (Google-Profil) gelten als Quelle, bei widersprüchlichen Quellen
  der kleinere Wert; unter 30 Bewertungen oder unter 4,5 keine Bewertungszahlen; die Zahl kommt erst,
  wenn weder Bewertungslob noch ein abhebendes Website-Detail besteht (eine hohe Zahl überholt keine
  eigene Akademie und kein eigenes Verfahren), und schließt mit der Reaktion, nie mit „so können sich
  Interessierte vorab orientieren“ 4) Fallback der Kampagne. Die Reihenfolge
  der Kampagne hat Vorrang, wo sie etwas anderes festlegt.
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

Hinweis: Der ListM8-Server legt beim Generieren zusätzlich eigene Intro-Regeln in den Prompt
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
der Chance-Variable und geht in Variante B hinaus; Instantly wertet nach Variante aus, ListM8 zeigt
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

## Prompts der AI-Variablen `hallo`, `intro` und `angebot_ausfuehrung`

Pflicht sind genau diese zwei Variablen (`sortOrder` 1 und 2), bei Karte A und B zusätzlich
`angebot_ausfuehrung` direkt nach `intro`. Weitere sind optional (z. B.
`proof`, `research_hook`, oder `firma` als Kurzname, wie `outreach-campaign` ihn vorsieht).
Namen: nur `a-zA-Z0-9_`, mit Buchstaben beginnend, eindeutig. Jede Variable wird pro Lead EINMAL
erzeugt: `{{ai.intro}}` steht deshalb NUR in Step 1; Follow-ups nutzen `{{ai.hallo}}` plus festen
Text.

Jeder Prompt ist eigenständig (Server-Minimum 10 Zeichen, besser ausführlich): Bei der
Generierung sieht das Modell NUR diesen Prompt, die Lead-Daten, die Recherche und den
Kampagnenkontext, nicht diesen Skill. Er enthält Kontext (wer schreibt, was angeboten wird, für
wen), Ziel, Aufgabe, verbotene Formulierungen und Tonfall.

Der `hallo`-Prompt MUSS enthalten:

- dass NUR die Begrüßungszeile ausgegeben wird, kein weiterer Satz, endet mit Komma;
- das Format passend zur `salutation` (Tabelle oben) samt Fallback („Hallo,“ in der Du-Form,
  „Guten Tag,“ in der Sie-Form);
- die Namensquelle: die Person, der die Versandadresse gehört; bei generischen Adressen
  (info@, kontakt@ …) der Entscheider/Inhaber aus der Recherche; ggf. Custom-Attribut mit dem
  Vornamen. Dazu das Verbot, Namen, Titel oder Rollen zu erfinden;
- das Verbot von Platzhaltern in Klammern, Gedankenstrichen und Emojis; echte Umlaute.

Der `intro`-Prompt MUSS enthalten:

- Kontext: Absender, Angebot und den festen Folgesatz, an den das Intro anschließt (z. B.
  „Deswegen war ich so frei …“);
- die Abhebungs-Typen und den Austauschtest (zehn andere Betriebe derselben Branche in der Stadt;
  ein Nutzen rettet keine Standardleistung), höchstens ein Gegensatzpaar aus der Branche als
  Fund, nie als fertiger Satz;
- die Sperrliste der Kampagne (dieselbe wie in `researchAgentConfig.additionalPrompt`);
- die Anker-Rangfolge (Lob aus Bewertungstexten > abhebendes Website-Detail, auch Stellenanzeige
  als Erkenntnis statt „du suchst“ > Anzahl und Schnitt > Fallback) samt Sterne-Regel: Zahlen
  nur bei mindestens 30 Bewertungen und einem Schnitt ab 4,5, gerundet, mit Komma, Import-Werte
  als Quelle, bei Widerspruch der kleinere Wert;
- den positiven Schluss mit der Rangfolge (kein Schluss, wenn das Detail selbst ein Lob ist,
  Kundenstimme oder Auszeichnung; sonst eine kurze Reaktion am Detail, je Lead wechselnd;
  eine Würdigung nur ausnahmsweise mit etwas Neuem und Konkretem, nie „das zeigt, wie …“; nie ein
  Mechanik-Nutzen, nie ein leeres Prüfer-Urteil) und Leitplanken (nichts erfinden, keine Floskel,
  keine feste Wendung), ohne ausformulierte Beispiel-Schlüsse;
- den Einstiegswechsel nach der letzten Ziffer der Lead-ID, mit Quelle im Einstieg bei
  Bewertungsankern;
- die Verbotsliste aus den Intro-Regeln, einschließlich der Floskeln „finde ich spannend/stark“;
- Form: max. 2 Sätze, erster Buchstabe klein, weitere Sätze groß, über den Empfänger,
  Pronomen gemäß `salutation`;
- einen ausformulierten FALLBACK-Satz für den Fall, dass kein belastbares Detail gefunden wird,
  plus die Anweisung, diesen Fallback zu nutzen statt eine Floskel zu erfinden. Der Fallback
  behauptet nichts Unbelegtes über den Lead („so gut bewertet“, „seit Jahren“, „viele
  zufriedene Kunden“).

Der `angebot_ausfuehrung`-Prompt (nur Karte A, B und C) MUSS enthalten:

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

Ein vollständig ausformuliertes Paar `hallo`/`intro` steht in `references/beispiel-blueprint.md`,
dazu je ein `angebot_ausfuehrung`-Prompt für Karte A und B.

## Platzhalter in ListM8

Aufgelöst werden nur diese Platzhalter (abschließende Liste für Betreff und Body):

- `{{ai.hallo}}`, `{{ai.intro}}`, `{{ai.<name>}}` (die Variablen der Kampagne)
- `{{lead.company}}`, `{{lead.website}}`, `{{lead.city}}` (der Server löst zusätzlich
  `lead.email` und `lead.phoneNumber` auf; in Copy nicht verwenden)
- `{{custom.<schlüssel>}}` (Custom-Attribute aus dem Import; leer, wenn der Lead keinen Wert hat)
- `{{accountSignature}}` nur im Body und nur bei der Signatur aus dem Konto (siehe Signatur)

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
| 1 | Entry Mail | 0 | 120 (Ziel 50-90) | eigener, öffnet den Thread | `{{ai.hallo}}` + `{{ai.intro}}` + feste Überleitung mit Offer + zweiter Satz zum Angebot als eigener Absatz (A/B/C `{{ai.angebot_ausfuehrung}}`, D/E keiner) + EIN CTA + Signatur |
| 2 | Erinnerung | 3 | 50 | leer, Thread von Mail 1 | `{{ai.hallo}}` + nur nachhaken, weich wie eine schnell getippte Nachricht („du hast sicher viel um die Ohren, ich wollte nur sichergehen, dass meine Mail angekommen ist“). Kein Doppelpunkt-Opener, kein Offer, kein neuer Aspekt, kein `{{ai.intro}}` |
| 3 | Neuer Winkel (Mehrwert + Social Proof) | 5 | 80 | leer, Thread von Mail 1 | `{{ai.hallo}}` + EIN Beleg als erster Absatz, nach der Anrede klein weiter wie Mail 1: eine Case Story, eine Zahl, ein Ergebnis. HIER steht der Social Proof. Höchstens ein kurzer eigener Satz, dann dieselbe Schlussfrage wie Mail 1 mit dem Wort für die Sache statt „es“ (Karte C: „Wäre es in Ordnung, wenn ich dir morgen den Entwurf zusende? Völlig unverbindlich natürlich.“), damit die Mail ohne Mail 1 verständlich ist. Karten ohne Wort für die Sache (B, D, E, eigene Frage) nehmen die Frage aus Mail 1 wörtlich; Mail 3 endet immer mit einer Frage, nie mit einer bloßen Aufforderung („sag einfach kurz Bescheid“). Kein eigener Satz um das Angebot („Falls du … sehen möchtest, melde dich“), kein neues Offer, kein `{{ai.intro}}`. Eine eigene Schlussfrage weicht in ListM8 der Frage aus Mail 1 (seit 06.11.2026). Mit Schwerpunkten nennen Mail 2 bis 4 nie einen Schwerpunkt beim Namen (sie gelten für alle Leads, der Schwerpunkt ist je Lead verschieden); ListM8 streicht einen Satz, der ein Schwerpunkt-Label enthält |
| 4 | Abschied mit Routing-Hinweis | 7 | 60 | leer, Thread von Mail 1 | `{{ai.hallo}}` + Tür offen lassen, ohne Druck und ohne Vorwurf + Routing-Hinweis („sag mir gern kurz Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte“). Kein Offer |

- Gezählt wird der Body ohne Betreff und ohne Signatur, den Bezug aus `{{ai.intro}}` (bis zu
  2 Sätzen) eingerechnet. Die Limits sind Obergrenzen: kürzer ist erlaubt und meist besser.
  Bewährte Entry-Mails liegen bei 55 bis 86 Wörtern. Nie auffüllen.
- Der CTA wird von Step zu Step weicher: Erlaubnis erbitten → nur anstoßen → in Step 3 dieselbe
  Frage wie Step 1 mit dem Wort für die Sache → Tür offen lassen.
- Jedes Follow-up hat max. EINEN neuen Aspekt und beginnt mit einem ganzen, weichen Satz in der
  gewählten Ansprache. Das erste Wort nach `{{ai.hallo}}` (in jedem Step) schreibt man klein, weil
  es auf „Hallo …,“ folgt: „du hast sicher …“, nicht „Du hast sicher …“, auch in der Sie-Form („da ich
  bisher nichts gehört habe“, „ich wollte kurz nachfragen“, „bei rund 80 Gründungen …“); „Sie“, Namen
  und Substantive bleiben groß. ListM8 setzt ein solches Wort am Anfang des ersten Absatzes auch selbst
  klein (seit 06.11.2026).
- **Dringlichkeit** ist kein Standard-Step. Nur wenn der Nutzer einen echten Zeit- oder
  Kapazitätsgrund nennt, kommt sie als zusätzlicher Step zwischen Step 3 und den Abschied
  (dann 5 Steps, `delayDays` 0/3/5/7/7; Wortlimit 60; leerer Betreff, Thread von Mail 1). Ohne
  echten Grund entfällt sie, nichts Erfundenes und keine künstliche Knappheit.
- Fehlt dem Nutzer ein echter Beleg für Step 3: nachfragen, nicht erfinden.
- Der Routing-Hinweis in Step 4 steht als fester Satz im Body. Hat die Kampagne ein
  Recherche-Ziel für Ansprechpartner, ersetzt die AI-Variable `routing` ihn durch eine Version mit
  belegten Namen („bin ich bei dir richtig oder eher bei Anna oder Tom?“); Vorlage und Regeln in
  `references/routing-baustein.md`.

## Betreffzeilen

Nur Step 1 trägt einen Betreff (er öffnet den Thread): 2-5 Wörter, keine Werbung, kein Spam-Wort, keine Großschreibung
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

**Betreff-Test (seit 05.11.2026):** Der Assistent von ListM8 legt einen Betreff-Test an (ab Werk an): Variante B von
Mail 1 ist wörtlich Variante A, nur mit dem Betreff `{{ai.betreff_b}}`, den die KI je Lead schreibt.
Variante A behält „kurze Frage“. Ist der Intro-Test zusätzlich an, läuft er als Variante C mit
„kurze Frage“ und `{{ai.intro_c}}`. Der Prompt der Variable kommt vom Server (`get_lead_data`,
`emailGeneration.subjectVariables`); Regeln für den persönlichen Betreff (SOP vom 05.11.2026):

- 3 bis 6 Wörter, Ziel 4 bis 5; der Firmenname zählt als ein Wort, kein ganzer Satz; zwei Wörter
  lesen sich wie ein Etikett („euer Ausstattungsatelier“), ListM8 ersetzt sie seit 06.11.2026 durch
  den Rückfall
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
   prüfen. Signatur als Klartext (bei Signatur aus dem Konto `{{accountSignature}}` unter der Grußformel), keine `{{sender.*}}`-Variablen?
10. Betreff von Step 1: 2-5 Wörter, kein Spam-Wort, keine Großschreibung, keine Ankündigung,
    Firmenname nur über `{{ai.firma}}`? Step 2, Step 3 und Step 4 ohne Betreff?
11. Enthält der `intro`-Prompt Austauschtest, Sperrliste der Kampagne, Anker-Rangfolge mit
    Sterne-Regel, positiven Schluss, Einstiegswechsel, die Verbote UND einen Fallback-Satz, der
    keine unbelegte Tatsache behauptet? Steht dieselbe Sperrliste in den Research-Vorgaben?
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
16. Zweiter Satz zum Angebot in Step 1 passend zur Karte: bei A, B und C
    `{{ai.angebot_ausfuehrung}}` als eigener Absatz mit einem Prompt nach den Regeln oben (bei C
    beginnt der Satz mit dem Feinheiten-Wortlaut, ohne „morgen“), bei D und E keiner? Schlusssatz
    ohne „Link“?

## Prüfliste nach Code-Regeln

Diese Regeln lassen sich mechanisch prüfen. ListM8 prüft sie beim Anlegen nicht, also prüfst du
sie: vor dem Anlegen der Sequenz und beim Review der Werte abhaken. „Hart“ = Fehler, „weich“ =
Hinweis, der begründet werden muss.

| Regel | Prüfung | Stufe |
|---|---|---|
| Wortlimit | Step 1-4 max. 120/50/80/60 Wörter, ein zusätzlicher Dringlichkeits-Step max. 60 (Platzhalter zählen nicht mit, den Intro-Umfang einrechnen) | hart |
| Zielkorridor | Entry-Mail unter 50 Wörtern: trägt der Bezug? | weich |
| Kein Gedankenstrich | kein „—“ und kein „–“ im Text | hart |
| Anführungszeichen geschlossen | jedes „ schließt mit “, nie mit " | hart |
| Kein Pitch | kein „wir helfen“, „wir sind ein/eine/der/die/seit“, „wir bieten“, „seit (über) N Jahren“, „als zertifizierter/offizieller/Google/Meta … Partner“, „mein Name ist“, „unser Unternehmen“ | hart |
| Kein Platzhalter | kein sichtbares `[Feld]` | hart |
| Bekannte Variablen | nur `{{ai.*}}`, `{{lead.company}}`, `{{lead.website}}`, `{{lead.city}}`, `{{custom.*}}` | hart |
| Kein Emoji | keine Emojis/Symbole | hart |
| Keine Formatierung | kein `**fett**`, keine Zeile, die mit „-“, „*“ oder „•“ beginnt | weich |
| „kostenlos“ | höchstens einmal pro Mail | weich |
| Betreff ohne Spam | kein Spam-Wort, kein „kostenlos“, „kostenlose“, „kostenloses“, „kostenfrei“ | hart |
| Betreff-Länge | max. 5 Wörter (Step 1) | weich |
| Betreff-Platzhalter | kein `{{lead.company}}` im Betreff; Firmenname nur als `{{ai.firma}}` | hart |
| Follow-up-Betreff | `subject` in Step 1 nicht leer, in Step 2, 3 und 4 (sowie in einem Dringlichkeits-Step) leer | hart |
| Schlussfrage in Step 3 | Step 3 endet mit einer Frage (dieselbe wie Step 1, mit dem Wort für die Sache, wo die Karte eins hat) | hart |
| Betreff ohne Schreien | kein Wort mit 4+ Großbuchstaben, kein „!“ | weich |
| Ein CTA | kein „oder/alternativ … buchen/klicken/vereinbaren/reservieren/anrufen/Termin sichern“ neben der Antwort-Bitte | hart |
| Kein Link in Mail 1 | kein „http(s)://“, „www.“, „calendly.com“, „hier buchen“ in Step 1 | hart |
| Zweiter Angebotssatz | Step 1 bei Karte A/B/C mit `{{ai.angebot_ausfuehrung}}`, bei D/E ohne; kein Feinheiten-Wortlaut im Prompt von A/B | hart |
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
  `hallo`- und `intro`-Prompt) zum Anlegen mit `create_campaign`, dazu die Variante für Karte A
  und B mit `angebot_ausfuehrung`-Prompt.
- Skill `outreach-launch` — Versand nach dem Export (Domains, Warm-up, Instantly, KPIs) und wann
  bei schwachen Zahlen Copy, Offer oder Liste geändert werden.
