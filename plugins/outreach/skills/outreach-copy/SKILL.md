---
name: outreach-copy
description: 'Use when user says "Cold-Mail schreiben", "Cold-Mail prüfen", "Copy prüfen", "Kampagnen-Copy", "Sequenz schreiben", "Betreffzeile", "Opener", "Intro-Prompt", "hallo-Prompt", "Marketing-Offer formulieren", "Offer schärfen", "Feinheiten-Satz", "Follow-ups schreiben", or wants to write, review or fix the copy of an outreach campaign. Verbindliche Cold-Mail-Copy-Regeln (Anatomie der Entry-Mail, Offer-Karten A-E, Feinheiten-Satz, 4er-Sequenz, Wortlimits, Intro- und Anrede-Regeln, Verbote, Selbstprüfung). outreach-campaign, outreach-generate und outreach-verify laden diesen Skill verbindlich.'
---

# Outreach Copy — die Cold-Mail-Regeln für Kampagnen

Dieser Skill ist die eine Copy-Doktrin für alles, was über den Outreach-MCP an Text entsteht:
Sequenz (Betreff und Body jedes Steps), die Prompts der AI-Variablen `hallo` und `intro` und
die pro Lead erzeugten Werte. Er gilt verbindlich für:

| Skill | Wann diesen Skill laden |
|---|---|
| `outreach-campaign` | bevor eine Zeile Sequenz oder Variablen-Prompt entsteht (`create_campaign`, `edit_campaign`) |
| `outreach-generate` | bevor `hallo`/`intro` für einen Lead geschrieben werden (`save_lead_variables`) |
| `outreach-verify` | beim Prüfen der Werte (`get_lead_variables`) vor `approve_lead_variables`/`reject_lead_variables` |

Ausführliche Lehre mit allen Beispielen: `references/copy-lehre.md`. Offer-Lehre:
`references/marketing-offer.md`. Ein vollständig ausformulierter Blueprint:
`references/beispiel-blueprint.md`. Bei einem Widerspruch zwischen diesen Dateien gilt diese
SKILL.md.

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

- Du-Form als Standard: direkt, konkret, kein Beratersprech, keine Floskeln. Deutsch.
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
Variable einer Mail. Immer explizit setzen. Der feste Sequenztext (Überleitung, CTA, Follow-ups)
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
| D: Förder-Hook | Nutzer hat förderfähige Produkte | „Wusstest du, dass der Staat aktuell bis zu [Prozent] der [Kosten] übernimmt?“ |
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
- Bei Karte A und C als bereits erledigte Arbeit formulieren („war so frei und habe … erstellt“),
  nicht als Absicht. Reziprozität wirkt erst, wenn das Geschenk schon existiert.
- Kein „Lass uns mal sprechen“ ohne vorbereiteten Mehrwert.
- Die Überleitung verbindet das Lob mit dem Offer („Genau deshalb …“, „Deswegen war ich so
  frei …“).
- Das Offer steht NUR in Mail 1. Follow-ups wiederholen es nicht.

## Anatomie der Entry-Mail

```
{{ai.hallo}}                     1. Anrede
{{ai.intro}}                     2. Lob / positiver Bezug (Intro-Regeln)
Feste Überleitung + Offer        3. statisch, benennt KEIN lead-spezifisches Problem;
                                    bei A und C als erledigte Arbeit
Feinheiten-Satz                  4. eigener Absatz; Pflicht bei A und C, optional bei B,
                                    entfällt bei D und E
EIN Frage-CTA                    5. niedrige Hürde
Signatur im Klartext             6. Grußformel, Name, „Rolle - Firma“
```

**Feinheiten-Satz (Value Stacking), wörtlich:** „Ich bin gerade noch an den letzten Feinheiten
dran, vor allem […], und werde morgen mit […] fertig.“ In die erste Klammer kommt genau EIN konkretes
On-Top-Detail aus den Angaben des Nutzers, das wirklich lieferbar ist, in die zweite das Deliverable
(„dem Entwurf“, „dem Setup“, „den Anzeigen“). Nichts erfinden. Er steht als eigener Absatz zwischen
Offer und CTA, ist KEIN zweites Offer und KEIN zweiter CTA. Nicht „Feinschliff“, nicht
umformulieren. Den Halbsatz „und werde morgen … fertig“ nur, wenn der Nutzer das Deliverable nach der
Antwort wirklich bis zum nächsten Tag liefern kann; sonst endet der Satz nach dem On-Top-Detail.

**CTA:** Genau einer, nie zwei Optionen. Standard bei Karte A und C ist der CTA der Master-Formel
(Kurs Outbound 3.0, Lektion 2.4): „Wäre es in Ordnung, wenn ich dir das zusende? Völlig
unverbindlich natürlich.“ Der Zusatz „Völlig unverbindlich natürlich.“ senkt die Hürde und ist kein
zweiter CTA. Weitere Beispiele: „Darf ich es dir zusenden?“, „Antworte mir einfach kurz.“, „Wäre das
grundsätzlich interessant?“. Kein Terminvorschlag und kein Link in Mail 1.

Die Master-Formel in fünf Bausteinen: Lob → „Deswegen …“ → konkretes Offer → Fertigstellung
(„… und werde morgen mit dem Entwurf fertig.“, hier im Feinheiten-Satz) → CTA mit wenig Verpflichtung.
„Werde morgen fertig“ wirkt stärker als „bin fertig“: Der Lead sieht, dass gerade noch für ihn
gearbeitet wird.

**Kein Pitch, keine Selbstvorstellung im Body.** Authority und Proof gehören in die Signatur bzw.
in Step 3. Über den Empfänger schreiben, nie über den Absender („Du bekommst …“, nicht „Wir
bieten …“).

Muster für Karte C, direkt nach dem Lob-Intro, jeder Baustein ein eigener Absatz:

```
Deswegen war ich so frei und habe dir einen kompletten Webseitenentwurf inklusive
Buchungssystem erstellt.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an der Optimierung für Google
und KI-Suchmaschinen, und werde morgen mit dem Entwurf fertig.

Wäre es in Ordnung, wenn ich dir das zusende? Völlig unverbindlich natürlich.
```

**Signatur:** Name, Rolle und Firma des ABSENDERS als Klartext aus den Angaben des Nutzers, z. B.
„Viele Grüße\nAngela Selbert\nGeschäftsführerin - njoy online marketing GmbH“. Nie
`{{sender.firstName}}`, `{{sender.company}}` o. Ä. (gibt es nicht). Ohne bekannten Absendernamen
nur „Viele Grüße“. Schlank: keine Auszeichnungen, Links, Telefonnummern oder Social-Leisten.

## Intro-Regeln (`{{ai.intro}}`)

Das Intro ist Lob oder eine anerkennende Beobachtung: ein positiver Bezug auf den Lead, der
beweist, dass jemand hingeschaut hat, getragen von einem konkreten Detail. Es ist KEINE Kritik
und KEIN Verbesserungsvorschlag. Das Problem sind leere Lobadjektive ohne Inhalt, nicht das Lob.
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
  Pflicht, gibt dem festen Folgesatz („Deshalb …“) aber einen Grund, wo das Detail noch kein Lob ist.
  Ist das Detail schon selbst ein Lob (was Kunden in Bewertungen schreiben), trägt es das Intro allein; ein Schluss ist frei, und einer, der das Lob nur wiederholt, fällt weg.
  Ein neutrales Faktum (Öffnungszeit, Verfahren, Spezialisierung, Projekt, Auszeichnung) und eine
  Bewertungszahl bekommen einen kurzen Halbsatz, in diesen Stufen (hinter einer Bewertungszahl gleich
  Stufe 2):
  1) Würdigung am Detail: was genau dieses Detail über den Betrieb zeigt, als Folgerung („das zeigt,
  dass euch eure Kundinnen auch nach dem Termin wichtig sind“), Anerkennung mit Inhalt, die sagt, wofür
  („da steckt richtig viel Handarbeit drin“), Seltenheit als eigene Erfahrung, die das Detail selbst
  nennt („so eine Nachsorge ist mir noch nicht begegnet“),
  Kundensicht („da weiß man als Kunde, dass man richtig ist“) oder lobender Nutzen, der kurz würdigt,
  was das Detail über den Betrieb sagt („das spart Zeit bei der Behandlung“);
  2) sonst eine kurze persönliche Reaktion direkt hinter dem benannten Detail, in der Vergangenheit
  erzählt wie unter Kollegen; sie sagt nur, dass es aufgefallen ist oder gefallen hat („…, das ist mir
  direkt aufgefallen“, lieber schlicht als „richtig gut gefallen“), muss das Detail nicht wiederholen und steht nie ohne das Detail; eine passende Reaktion schlägt der Block `SCHLUSS DES OPENERS`
  im System-Prompt (`emailGeneration.systemPrompt`) vor; fehlt er (älterer Server), die
  Reaktion je Lead selbst variieren und die zwei bekannten Muster („das fand ich eine schöne Idee“,
  „hat mir gut gefallen“) nicht wörtlich übernehmen;
  3) ein Superlativ („wirklich beeindruckend“) nur, wenn der Anker wirklich beeindruckt und weder
  Stufe 1 noch Stufe 2 gut klingt, immer direkt am Detail.
  Die Würdigung sagt etwas Neues über den Betrieb (was das Detail über seine Haltung zeigt oder was
  es Kunden bringt), statt das Detail umzuformulieren: „seit 2004 in der Branche, das spricht für
  viel Branchenerfahrung“ sagt dasselbe zweimal, „macht das Angebot schön konkret“ urteilt wie ein
  Gutachten. Seltenheit steht als eigene Erfahrung am Detail, nie im allgemeinen „man“
  („erlebt man nicht oft“) und nie als Vergleich mit anderen Betrieben („hebt dich von jeder anderen Agentur ab“, „bietet sonst kaum ein Studio an“): Solche
  Vergleiche belegt keine Quelle. Im Zweifel die Reaktion; klingt auch sie nicht, bleibt das Faktum
  ohne Schluss. Genau eine Schlussform, nie Würdigung und Reaktion hintereinander.
  Verboten: der Mechanik-Nutzen, also ein Schluss, der erklärt, was man dank des Details tun kann
  („so können sich Interessierte vorab ein Bild machen“, „so kann man unverbindlich nachfragen“,
  „so bekommen Kunden schneller einen Termin“), in jeder Satzform: ein Schluss, der ausmalt, was
  Kunden dank des Details tun können oder sich sparen (wer, wann, wofür), auch „das spart
  Berufstätigen den Urlaubstag für den Reifenwechsel“; Lob ohne Detail („finde ich stark“, „Hammer“);
  doppeltes Lob; das leere Prüfer-Urteil über die Qualität ihrer Arbeit, das aus dem Detail nicht
  folgt und auf jeden Betrieb passt („das wirkt vertrauenswürdig“, „so einen Schnitt hält man nur,
  wenn die Arbeit stimmt“, „da machst du vieles richtig“, „das schafft man nicht ohne sauberes
  Arbeiten“, „zeigt, dass die Behandlung ankommt“). Eine Würdigung ist erlaubt, weil sie am konkreten
  Detail hängt. Nichts erfinden, nur was direkt aus dem Detail folgt. Keine feste Wendung aus
  Beispielen: jede Würdigung aus dem konkreten Detail bilden, die Reaktion nie aus Beispielen. Lobt
  schon der erste Satz des festen Mailtexts selbst, entfällt der Schluss: nie zweimal loben. Der
  Fallback-Satz bleibt ohne Schluss.
- Ausschließlich positiv, getragen vom konkreten Detail selbst. Verboten sind austauschbare
  Bewertungsfloskeln und Superlative wie „das spricht für sich“, „das sieht man selten“, „das sieht
  man nicht immer“, „hat man nicht alle Tage“, „finde ich stark“, „finde ich spannend“, „finde ich
  bemerkenswert“, „Hammer“, „beeindruckend“. Abgrenzung: „finde ich stark“ ist eine Formel, ein
  gegenwärtiges Urteil ohne Inhalt; eine Würdigung oder Reaktion am benannten Detail ist erlaubt,
  Seltenheit und Superlativ nur mit dem Detail („so eine Nachsorge ist mir noch nicht begegnet“), nie allein
  („das sieht man selten“, „beeindruckend“) (siehe Positiver Schluss). Die Formeln machen alle Opener gleich (ListM8-Regel, gilt
  zusätzlich zu den Akquise-Regeln). Auch in Beispielen und Prompts nie als Muster stehen lassen:
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

## Prompts der AI-Variablen `hallo` und `intro`

Pflicht sind genau diese zwei Variablen (`sortOrder` 1 und 2). Weitere sind optional (z. B.
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
- den positiven Schluss (Kundenlob trägt sich selbst, ein neutrales Faktum und eine Bewertungszahl
  bekommen einen) mit den Stufen (Würdigung am Detail, sonst kurze Reaktion direkt hinter dem
  benannten Detail, Superlativ nur bei wirklich beeindruckendem Anker und am Detail; nie ein
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

Ein vollständig ausformuliertes Paar steht in `references/beispiel-blueprint.md`.

## Platzhalter in ListM8

Aufgelöst werden nur diese Platzhalter (abschließende Liste für Betreff und Body):

- `{{ai.hallo}}`, `{{ai.intro}}`, `{{ai.<name>}}` (die Variablen der Kampagne)
- `{{lead.company}}`, `{{lead.website}}`, `{{lead.city}}` (der Server löst zusätzlich
  `lead.email` und `lead.phoneNumber` auf; in Copy nicht verwenden)
- `{{custom.<schlüssel>}}` (Custom-Attribute aus dem Import; leer, wenn der Lead keinen Wert hat)

Alles andere (`{{firstName}}`, `{{companyName}}`, `{{sender.*}}`, If-Blöcke, Default-Syntax)
landet als Rohtext beim Empfänger. Ein nicht erzeugter AI-Wert erscheint als „[NOT GENERATED]“.
Firmenname des Empfängers im Body: `{{lead.company}}` (bzw. `{{ai.firma}}`, wenn die Kampagne den
Kurznamen führt), nie `{{companyName}}`. Im Betreff nie das rohe `{{lead.company}}`, siehe
Betreffzeilen.

## Sequenz

Standard sind 4 Steps mit festen Rollen (Praxis-Belege: Eric Nowoslawski mit 2 bis 3 Mails, nie
alle im selben Thread; Jay mit 4 Steps und Routing, ohne künstliche Knappheit). `delayDays` ist die
Wartezeit VOR dem Step (kumuliert Tag 0, 3, 8, 15), eine ganze Zahl; `delayUnit` immer `"days"`.
Threads: Step 1 öffnet einen Thread, Step 2 antwortet darin, Step 3 öffnet einen NEUEN Thread, Step 4
antwortet im Thread von Step 3. Der Betreff steht deshalb nur in Step 1 und Step 3, in Step 2 und 4
bleibt er leer.

| Step | Rolle | `delayDays` | Wörter max. | Betreff | Inhalt |
|---|---|---|---|---|---|
| 1 | Entry Mail | 0 | 120 (Ziel 50-90) | eigener, neuer Thread | `{{ai.hallo}}` + `{{ai.intro}}` + feste Überleitung mit Offer + Feinheiten-Satz als eigener Absatz (A/C) + EIN CTA + Signatur |
| 2 | Erinnerung | 3 | 50 | leer, Thread von Mail 1 | `{{ai.hallo}}` + nur nachhaken, weich wie eine schnell getippte Nachricht („du hast sicher viel um die Ohren, ich wollte nur sichergehen, dass meine Mail angekommen ist“). Kein Doppelpunkt-Opener, kein Offer, kein neuer Aspekt, kein `{{ai.intro}}` |
| 3 | Neuer Winkel (Mehrwert + Social Proof) | 5 | 80 | eigener kurzer Betreff, NEUER Thread (z. B. „kurzes Update“) | `{{ai.hallo}}` + EIN Beleg: eine Case Story, eine Zahl, ein Ergebnis. HIER steht der Social Proof. Die Mail muss ohne den Verlauf von Mail 1 verständlich sein: höchstens ein Halbsatz Bezug auf das Angebot, kein neues Offer, kein `{{ai.intro}}` |
| 4 | Abschied mit Routing-Hinweis | 7 | 60 | leer, Thread von Mail 3 | `{{ai.hallo}}` + Tür offen lassen, ohne Druck und ohne Vorwurf + Routing-Hinweis („sag mir gern kurz Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte“). Kein Offer |

- Gezählt wird der Body ohne Betreff und ohne Signatur, den Bezug aus `{{ai.intro}}` (bis zu
  2 Sätzen) eingerechnet. Die Limits sind Obergrenzen: kürzer ist erlaubt und meist besser.
  Bewährte Entry-Mails liegen bei 55 bis 86 Wörtern. Nie auffüllen.
- Der CTA wird von Step zu Step weicher: Erlaubnis erbitten → nur anstoßen → offen anbieten →
  Tür offen lassen.
- Jedes Follow-up hat max. EINEN neuen Aspekt und beginnt mit einem ganzen, weichen Satz in der
  gewählten Ansprache. Das erste Wort nach `{{ai.hallo}}` (in jedem Step) schreibt man klein, weil
  es auf „Hallo …,“ folgt: „du hast sicher …“, nicht „Du hast sicher …“; Substantive bleiben groß.
- **Dringlichkeit** ist kein Standard-Step. Nur wenn der Nutzer einen echten Zeit- oder
  Kapazitätsgrund nennt, kommt sie als zusätzlicher Step zwischen Step 3 und den Abschied
  (dann 5 Steps, `delayDays` 0/3/5/7/7; Wortlimit 60; leerer Betreff, Thread von Mail 3). Ohne
  echten Grund entfällt sie, nichts Erfundenes und keine künstliche Knappheit.
- Fehlt dem Nutzer ein echter Beleg für Step 3: nachfragen, nicht erfinden.
- Der Routing-Hinweis in Step 4 steht als fester Satz im Body. Hat die Kampagne ein
  Recherche-Ziel für Ansprechpartner, ersetzt die AI-Variable `routing` ihn durch eine Version mit
  belegten Namen („bin ich bei dir richtig oder eher bei Anna oder Tom?“); Vorlage und Regeln in
  `references/routing-baustein.md`.

## Betreffzeilen

Nur Step 1 und Step 3 tragen einen Betreff (jeweils ein neuer Thread): 2-5 Wörter, keine Werbung, kein Spam-Wort, keine Großschreibung
ganzer Wörter, kein Ausrufezeichen, kein Prozentzeichen. Er klingt wie eine harmlose Frage eines
Menschen. Keine Ankündigung und keine Ergebnisansage („Website für …“, „Entwurf für …“, „Idee
für …“, „Website ist fertig“).

Firmenname im Betreff nur über `{{ai.firma}}` (bereinigter Kurzname, siehe `outreach-campaign`),
nie über das rohe `{{lead.company}}`: Importnamen sind oft Google-Titel oder Domains. Führt die
Kampagne keine Variable `firma`, steht im Betreff kein Firmenname, dann „kurze Frage“.

Bewährte Muster (an den Offer-Typ anpassen):

- „kurze Frage“ (Standard: Neugier, niedrige Hürde; Karte C und jedes Entwurfs-Angebot wie
  Website, Anzeigen, Stellenanzeigen, Testzugang)
- „Frage zur Terminbuchung“ (wenn das Buchungssystem den Kern des Offers bildet)
- „Meeting {{ai.firma}} & <Absender-Vorname>“ (Karte A; persönlich, wirkt wie ein Termin; nur mit `firma`)
- „Anfrage für {{ai.firma}}“ (Karte A/B; direkt, business-like; nur mit `firma`)
- „Deine Förderung“ (nur bei Karte D)
- „Partnerschaft {{ai.firma}}?“ (nur bei Karte E, nur mit `firma`)

Step 2 und Step 4 (und eine optionale Dringlichkeits-Mail): Betreff LEER, die Mails laufen im Thread
der vorigen Betreff-Mail (Step 2 in Step 1, Step 4 in Step 3). Kein neuer Betreff-Text, kein „Re:“.

Step 3 startet einen neuen Thread mit eigenem kurzem Betreff, z. B. „kurzes Update“. Er wiederholt
den Betreff von Step 1 nicht, kündigt kein Ergebnis an und hält dieselben Regeln (2-5 Wörter, kein
Spam-Wort, Firmenname nur über `{{ai.firma}}`).

**Test von Hand (Hinweis, keine Pflicht):** Der Standard für Step 1 bleibt „kurze Frage“. Wer
Betreffs testen will, legt beim echten Versand in Instantly von Hand eine Variante B „Frage zu
{{firma}}“ an (braucht die Variable `firma` in der Kampagne, am besten in 1 bis 2 Kampagnen). ListM8
kennt keine Betreff-Varianten.

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

**Spam-Wörter** — im Betreff komplett verboten, im Body vermeiden: „gratis“, „100 %“,
„garantiert“, „Garantie“, „jetzt zugreifen“, „jetzt handeln“, „begrenztes Angebot“, „nur heute“,
„exklusives Angebot“, „hier klicken“, „Rabatt“, „Sonderpreis“, „Gewinner“, „Sie haben gewonnen“,
„dringend“, „risikofrei“, „ohne Risiko“, „Geld verdienen“.
„unverbindlich“ ist kein Spam-Wort (abweichend von akquise-ai); der Standard-CTA endet mit
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
4. Steht das Offer nur in Step 1 (in Step 3 höchstens ein Halbsatz Bezug)?
5. Steht `{{ai.intro}}` nur in Step 1?
6. Steht der Social Proof in Step 3 und nicht früher?
7. Zeichen-Scan: M-Striche, Emojis, Bold, Bulletpoints, Links in Step 1?
8. Spam-Scan: Betreff und Body gegen die Wortliste. „kostenlos“ höchstens einmal im Body?
9. Platzhalter-Scan: kein [Klammer-Feld]? Jede `{{…}}`-Variable gegen die abschließende Liste
   prüfen. Signatur als Klartext, keine `{{sender.*}}`-Variablen?
10. Betreff von Step 1 und Step 3: 2-5 Wörter, kein Spam-Wort, keine Großschreibung, keine
    Ankündigung, Firmenname nur über `{{ai.firma}}`, Step 3 nicht gleich Step 1? Step 2 und Step 4
    ohne Betreff?
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
| Betreff-Länge | max. 5 Wörter (Step 1 und 3) | weich |
| Betreff-Platzhalter | kein `{{lead.company}}` im Betreff; Firmenname nur als `{{ai.firma}}` | hart |
| Follow-up-Betreff | `subject` in Step 1 und 3 nicht leer, in Step 2 und 4 (sowie in einem Dringlichkeits-Step) leer | hart |
| Betreff ohne Schreien | kein Wort mit 4+ Großbuchstaben, kein „!“ | weich |
| Ein CTA | kein „oder/alternativ … buchen/klicken/vereinbaren/reservieren/anrufen/Termin sichern“ neben der Antwort-Bitte | hart |
| Kein Link in Mail 1 | kein „http(s)://“, „www.“, „calendly.com“, „hier buchen“ in Step 1 | hart |
| Offer ist kein Gespräch | Step 1 enthält keinen verbotenen Offer-Begriff (außer verneint: „statt …“, „kein …“) | hart |
| Intro nur in Step 1 | `{{ai.intro}}` in keinem Step ab 2 | hart |
| Anrede überall | jeder Step enthält `{{ai.hallo}}` | weich |
| Umlaute | keine Transliteration (fuer, ueber, gruess, koennen, moechte, groess, persoenlich, moeglich, waere, haette …) in Sequenz, Prompts und Konfiguration | hart |

## Verwandt

- `references/copy-lehre.md` — Abhebung und Austauschtest (zentrale Opener-Regel mit
  Gegensatzpaaren, Sperrliste, Einstiegswechsel), Goldene Formel, Angle-Hierarchie, Überleitungsbausteine,
  Feinheiten-Satz, Beispiele A/C/E, Follow-ups mit Varianten, 12 Gebote, Anti-Patterns,
  Zustellregeln, Prüfdurchlauf.
- `references/marketing-offer.md` — Karten A-E im Detail, Werttest, Offer-Killer,
  Reziprozität, was kein Offer ist.
- `references/beispiel-blueprint.md` — vollständiger Blueprint (Karte C, Du-Form, 4 Steps,
  `hallo`- und `intro`-Prompt) zum Anlegen mit `create_campaign`.
- Skill `outreach-launch` — Versand nach dem Export (Domains, Warm-up, Instantly, KPIs) und wann
  bei schwachen Zahlen Copy, Offer oder Liste geändert werden.
