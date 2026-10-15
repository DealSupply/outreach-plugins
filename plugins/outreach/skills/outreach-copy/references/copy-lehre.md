# Cold-Mail-Copy — Opener, Entry Mail, Follow-Ups, Qualitätsprüfung

> Ausführliche Lehre zu `outreach-copy`. Bei einem Widerspruch gilt die `SKILL.md` des Skills.
>
> **Lesehilfe für die Beispiele:** Die Beispiel-Mails sind aufgelöst dargestellt, wie sie beim
> Empfänger ankommen. In der Sequenz steht die Anrede-Zeile als `{{ai.hallo}}` und der
> individuelle Bezug der Entry Mail als `{{ai.intro}}`; der Rest ist fester Text. Die Beispiele
> sprechen die Person und ihren Betrieb durchgehend im Singular mit „du“ an („dein Team“, „deine
> Praxis“). Die Person wird nie mit ihr/euch angesprochen; Tatsachen über einen Betrieb mit mehreren
> Personen dürfen mit ihr/euer stehen („dass ihr nach ISO 9001 zertifiziert seid“), Details in
> `outreach-copy` unter „Anrede und Ansprache“. In ListM8 legt `emailAgentConfig.salutation`
> die Pronomen für die ganze Mail fest (`du`: nur du/dir/dein, Standard; `sie`: Sie/Ihnen/Ihre, nur
> wenn der Nutzer es für die Kampagne wählt). Den festen Text beim Übernehmen bei `sie` umschreiben.

## Grundhaltung

Eine Cold Mail ist keine kurze Version deiner Website. Sie ist eine Nachricht an einen Menschen, der dich nicht kennt und dessen Tag voll ist. Deshalb gilt: drei Bausteine, ein CTA, und kein Satz über die eigene Firma.

Der häufigste Reflex ist, sich erst vorzustellen. Genau der killt die Mail. Wer sich vorstellt, bevor er einen Grund geliefert hat, weiterzulesen, hat die Mail an die Stelle geschrieben, wo der Empfänger sie löscht.

Und eine Mail reicht nicht. Der größte Teil der Antworten kommt nicht auf die Entry Mail, sondern auf die Nachfass-Mails. Wer nach Mail 1 aufgibt, hat die ganze Arbeit gemacht und die Ernte verschenkt.

## Die Sequenz auf einen Blick

| Mail | Step | Typ | Wörter | `delayDays` | Tag | Betreff / Thread |
|:-----|:-----|:----|:-------|:------------|:----|:-----------------|
| **Entry Mail** | 1 | Komplette Botschaft | max. 120, Ziel 50-90 | 0 | 0 | eigener Betreff, neuer Thread |
| **FUP1** | 2 | Erinnerung | max. 50 | 3 | 3 | leer, Thread von Mail 1 |
| **FUP2** | 3 | Neuer Winkel (Case Study) | max. 80 | 5 | 8 | eigener kurzer Betreff („kurzes Update“), NEUER Thread |
| **FUP3** | 4 | Abschied mit Routing-Hinweis | max. 60 | 7 | 15 | leer, Thread von Mail 3 |

Der Standard sind drei Follow-Ups, zusammen mit der Entry Mail vier Steps. Praxis-Belege: Eric Nowoslawski arbeitet mit zwei bis drei Mails und nie alle im selben Thread, Jay mit vier Steps und Routing, ohne künstliche Knappheit. Deshalb startet Step 3 einen neuen Thread mit eigenem kurzen Betreff, und Step 4 verabschiedet sich mit dem Routing-Hinweis. „Dringlichkeit“ ist kein Standard-Step: Nur wenn der Nutzer einen echten Zeit- oder Kapazitätsgrund nennt, kommt sie als zusätzlicher Step vor dem Abschied (dann fünf Steps, `delayDays` 0/3/5/7/7).

**Alle Zahlen sind Obergrenzen, keine Zielvorgaben.** Die abgenommenen Kampagnen liegen bei der Entry Mail zwischen 55 und 86 Wörtern, die Follow-Up-Bausteine teils deutlich darunter - die kürzeste empfohlene Reminder-Variante hat 14 Wörter. Wer dieselbe Botschaft in weniger Wörtern unterbringt, hat es besser gemacht, nicht schlechter.

Wenn drüber: kürzen. Nicht diskutieren. Aufgefüllt wird nie.

---

# TEIL 1: Der individuelle Bezug (Opener)

Der individuelle Bezug ist der eine Satz, der entscheidet, ob die Mail als persönliche Nachricht oder als Massenmail gelesen wird. Nach unserer Erfahrung hebt gut gemachte AI-Personalisierung die Reply Rate spürbar; ein belegter Faktor ist das nicht, und falsche Personalisierung schadet. Teste deshalb einen Teil der Leads ohne Intro als Kontrollgruppe gegen die Variante mit Intro, bevor du die Personalisierung als gesetzt behandelst.

Aber der Opener ist kein Kompliment-Generator, sondern ein Beweis. Er beweist, dass jemand hingeschaut hat. Deshalb entscheidet nicht die Formulierung, sondern das Detail - und wo es kein Detail gibt, ist eine ehrliche Standardzeile besser als eine erfundene Beobachtung.

**Vorher (ohne AI-Personalisierung):**

„Hallo Max, wir bieten kostenloses Google Ads Setup an..."

**Nachher (mit AI-Personalisierung):**

„Hallo Max, ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, dass deine Lieferung schneller war als bei Amazon. Das ist ein Grund, direkt bei dir statt bei Amazon zu bestellen..."

## Abhebung und Austauschtest

Das ist die zentrale Regel für den Opener. `SKILL.md`, `lead-agent`, `verify-agent`, die Research-Vorgaben und jeder `intro`-Prompt tragen sie in Kurzform; die Gründe, Gegensatzpaare und Beispiele stehen nur hier.

### Abhebung statt Leistungsnennung

Der Opener nennt, was diesen Betrieb von anderen seiner Branche abhebt. Die Abhebungs-Typen:

| Typ | Beispiel für den Fund (nicht für den Satz) |
|:----|:-------------------------------------------|
| Eigenname oder eigenes Konzept | ein Behandlungs- oder Servicekonzept mit eigenem Namen |
| Ungewöhnliche Zeit oder Zahl | Sprechstunde donnerstags bis 20 Uhr, Angebot 48 Stunden nach dem Aufmaß |
| Eigenes Verfahren | jedes Bad vorab als begehbarer 3D-Rundgang |
| Seltene Spezialisierung | nur Holzfenster im Denkmalschutz |
| Auszeichnung | ein Branchenpreis, ein Siegel mit Jahr |
| Lob aus Bewertungen | was Kunden über DIESEN Betrieb schreiben |
| Auffällige Bewertungszahlen | über 200 Rezensionen mit einem Schnitt von 4,8 (eigener Anker, siehe Rangfolge) |

Projekte, Referenzen, Firmengeschichte oder Gründungsjahr (mit seinem Ereignis), Lage und Ausstattung zählen ebenfalls, wenn sie den Austauschtest bestehen. Eine Aufzählung von Leistungen besteht ihn nie.

### Der Austauschtest

Passt der Satz auf zehn andere Betriebe derselben Branche in der Stadt, ist er kein Aufhänger. Dann den nächsten Anker nehmen, zuletzt den Fallback der Kampagne.

- Ein Nutzen rettet keine Standardleistung: „du scannst digital, das hilft bei Würgereiz“ fällt durch, weil der digitale Scan in vielen Praxen Standard ist.
- Dasselbe Thema besteht als Bewertungslob (was Kunden über DIESEN Betrieb schreiben), nicht als Zeile aus der Leistungsliste.

Gegensatzpaare (die Spalte „besteht“ zeigt den Fund, nicht den fertigen Satz):

| Branche | Fällt durch | Besteht | Warum |
|:--------|:------------|:--------|:------|
| Dental | Lachgas für Angstpatienten | „Krone To Go“: die Krone am selben Termin, unter eigenem Namen | Lachgas steht bei vielen Praxen auf der Leistungsseite, ein eigenes Kronen-Konzept am selben Tag nicht |
| Dental | digitaler Scan statt Abdruck, „hilft bei Würgereiz“ | Sprechstunde donnerstags bis 20 Uhr, mit dem Nutzen für Berufstätige | Der Nutzen rettet die Standardleistung nicht; die ungewöhnliche Zeit ist selbst die Abhebung, der Nutzen wird zum positiven Schluss |
| Dental | „du behandelst Angstpatienten“ von der Leistungsseite | mehrere Bewertungen schreiben, dass Patienten trotz Angst ruhig durch die Behandlung kamen | gleiches Thema, aber als Lob über diesen Betrieb |
| Handwerk | du bietest Badsanierung an | jedes Bad vorab als begehbarer 3D-Rundgang | Badsanierung macht jeder Sanitärbetrieb, den Rundgang vor dem ersten Handgriff kaum einer |

### Positiver Schluss

Nach der Beobachtung folgt ein kurzer positiver Halbsatz, in dieser Rangfolge:

1. **Nutzen oder Wirkung**, wenn sie sich aus dem Detail anbietet (wem nützt es, was bewirkt es): „…, so passt ein Termin auch nach der Arbeit.“
2. **Sonst eine kurze persönliche Reaktion** direkt hinter dem benannten Detail, in der Vergangenheit erzählt wie unter Kollegen: „…, das fand ich eine schöne Idee.“, „…, das ist mir gleich ins Auge gefallen.“ Sie sagt nur, dass es aufgefallen ist oder gefallen hat, muss das Detail nicht wiederholen, steht nie allein, und wird je Lead aus dem Detail gebildet, nie als feste Wendung.
3. **Nie ein Prüfer-Urteil über die Qualität ihrer Arbeit.** Es klingt wie die Begutachtung durch einen Fremden: „das wirkt vertrauenswürdig“, „so einen Schnitt hält man nur, wenn die Arbeit stimmt“, „da machst du vieles richtig“, „das schafft man nicht ohne sauberes Arbeiten“, „zeigt, dass die Behandlung ankommt“. (Messrunde 08.10.2026: ein Drittel der neuen Schlüsse waren solche Urteile.)

Leitplanken:

- nichts erfinden, nur was direkt aus dem Detail folgt (nie „deine Patienten lieben das“, nie „alle positiv“);
- keine inhaltsleere Formel und kein Vergleich oder Superlativ („finde ich stark/spannend/bemerkenswert“, „Hammer“, „beeindruckend“, „das sieht man selten“, „das sieht man nicht immer“, „hat man nicht alle Tage“, „das spricht für sich“);
- Abgrenzung: „das fand ich eine schöne Idee“ ist eine Reaktion auf ein benanntes Detail und erlaubt; „finde ich stark“ ist eine Formel, ein gegenwärtiges Urteil ohne Inhalt, und verboten;
- keine feste Wendung: jeden Schluss aus dem konkreten Detail bilden, nie aus Beispielen übernehmen; die Reaktion gibt der Server je Lead aus einer festen Liste vor, Wiederholungen über eine Kampagne sind deshalb erwartet; gleich lautende Nutzen-Schlüsse über mehrere Leads (etwa „Interessierte können sich vorab orientieren“ hinter Bewertungszahlen) sind ein systematischer Befund;
- gilt auch bei Bewertungsankern; insgesamt weiter höchstens 2 Sätze, etwa 30 Wörter, ohne Gedankenstrich (Komma statt Strich);
- der Fallback-Satz der Kampagne bleibt wörtlich, ohne angehängten Schluss.

**Beispiele, nicht wörtlich übernehmen.** Sie zeigen, wie verschieden ein Schluss aus dem jeweiligen Detail entsteht. Wer einen davon in einen Prompt kopiert, macht alle Opener gleich.

| Anker | Opener |
|:------|:-------|
| Eigenes Verfahren (Handwerk) | „ich war gerade auf deiner Website: Du zeigst jedes Bad vorab als begehbaren 3D-Rundgang. So steht der Kunde schon in seinem neuen Bad, bevor die erste Fliese fällt.“ |
| Ungewöhnliche Zeit (Dental) | „mir ist aufgefallen, dass deine Praxis donnerstags bis 20 Uhr Termine hat, da kommt man auch nach einem vollen Arbeitstag noch dran.“ |
| Eigenes Konzept (Dental) | „beim Stöbern auf deiner Website hab ich ‚Krone To Go‘ entdeckt, die Krone am selben Termin. Das erspart deinen Patienten den zweiten Termin und die Zeit mit Provisorium.“ |
| Lob aus Bewertungen (Dental) | „ich hab mir deine Bewertungen angeschaut, und mehrere Patienten schreiben, dass du jeden Schritt vorher erklärst. So weiß man im Stuhl immer, was als Nächstes kommt.“ |
| Eigenname (Café), Reaktion statt Nutzen | „mir ist aufgefallen, dass jede Torte bei dir nach einem Stammgast benannt ist, über die Torte ‚Herr Albers‘ hab ich mich beim Lesen gefreut.“ |

### Bewertungen: Rangfolge der Anker

1. Lob aus Bewertungstexten (Paraphrase; Plural oder „immer wieder“ nur, wenn mindestens 2 Bewertungen es tragen).
2. Abhebendes Detail von der Website, auch Wachstum oder eine Stellenanzeige als Erkenntnis über den Betrieb.
3. Anzahl und Schnitt der Bewertungen als eigener Anker: erst ab mindestens 30 Bewertungen und nur bei gutem Schnitt (ab 4,5). Zahl gerundet („über 200“), Schnitt mit Komma („4,8“). Werte aus dem Import (Google-Profil in den Lead-Attributen) gelten als Quelle; widersprechen sich Quellen, gilt der kleinere Wert. Unter 30 Bewertungen oder unter 4,5 nennt der Opener keine Bewertungszahlen; dann gilt der nächste Anker bzw. der Fallback (Messrunde 08.10.2026: Sterne-Anker mit 9 bis 40 Bewertungen trugen nicht).
4. Fallback der Kampagne.

Die Reihenfolge der Kampagne hat Vorrang, wo eine Kampagne etwas anderes festlegt. Jeder Anker muss den Austauschtest bestehen, sonst gilt der nächste. Bewertungen werden deshalb zuerst recherchiert, nicht erst, wenn die Website wenig hergibt.

### Einstiege abwechseln

Einstiegsrahmen sind erlaubt, keiner ist Standard: „ich hab mir … angeschaut“, „mir ist aufgefallen, dass …“, „beim Stöbern auf deiner Website …“, „ich war gerade auf deiner Website: …“ oder direkt mit dem Detail. Ein Bewertungsanker nennt im Einstieg die Quelle („ich hab mir deine Bewertungen angeschaut, und …“).

Weil jeder Agent nur seinen Lead sieht, wählt er den Einstieg nach der letzten Ziffer der Lead-ID, außer der Anker verlangt einen bestimmten Einstieg (Bewertungen):

| Letzte Ziffer | Einstieg |
|:--------------|:---------|
| 0-2 | „mir ist aufgefallen, dass …“ |
| 3-5 | „ich hab mir … angeschaut“ |
| 6-7 | „beim Stöbern auf deiner Website …“ |
| 8-9 | direkt mit dem Detail |

Prüfung: Beginnt mehr als ein Drittel einer Kampagne gleich, ist das ein systematischer Befund. Dasselbe gilt, wenn mehr als ein Drittel denselben Anker trägt (etwa lauter Angstpatienten): dann den `intro`-Prompt bzw. die Sperrliste nachschärfen, nicht einzeln nachbessern.

### Sperrliste je Kampagne

Jede Kampagne hat im Blueprint eine Sperrliste branchenüblicher Leistungen, die keinen Opener tragen, und zwar an zwei Stellen: in den Research-Vorgaben (`researchAgentConfig.additionalPrompt`) UND im `intro`-Prompt. `outreach-campaign` erzeugt sie beim Kampagnenbau aus Branche und Zielgruppe: Was steht bei fast jedem Betrieb dieser Branche auf der Leistungsseite? Diese Begriffe (meist 6 bis 10) kommen auf die Liste. Ein gesperrtes Thema darf nur als Lob aus Bewertungstexten in den Opener.

Beispiel Dental: Angstpatienten, Lachgas, Sedierung/Narkose, Kinderbehandlung, Notdienst, Prophylaxe/Dentalhygiene, digitaler Scan/Abdruck, Implantate allgemein.

Keine Mustersätze je Branche. Beispiele in Prompts stehen nur strukturell oder als Gegensatzpaar (fällt durch / besteht, ohne fertigen Satz), nie als Vorlage für den positiven Schluss.

## Angle-Hierarchie (in dieser Reihenfolge versuchen)

Die Rangfolge aus „Bewertungen: Rangfolge der Anker“ im Detail. Jeder Angle muss den Austauschtest bestehen, sonst gilt der nächste. Die Vorlagen zeigen den Aufbau, die Beispiele einen fertigen Opener mit positivem Schluss; beides nicht wörtlich übernehmen.

### Angle 1: Lob aus Bewertungstexten (bester Angle)

**Wann:** Google-Bewertungen, Bewertungsportale, Trusted Shops oder Shop-Bewertungen mit Text.
**Warum der beste:** Bewertungen sind spezifisch, emotional und beweisen, dass man wirklich recherchiert hat. Und sie sagen, was Kunden an DIESEM Betrieb schätzen, nicht was auf jeder Leistungsseite steht.
**Anker:** eine konkrete Paraphrase, was genau gelobt wird. Plural oder „immer wieder“ nur, wenn mindestens 2 Bewertungen dieses Lob tragen. Der Einstieg nennt die Quelle.

| Vorlage | Echtes Beispiel |
|:--------|:---------------|
| „ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, [PARAPHRASE]. [Kurzer positiver Schluss aus dem Lob]" | „ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, dass deine Lieferung schneller war als bei Amazon. Das ist ein Grund, direkt bei dir statt bei Amazon zu bestellen." |
| „in deinen Bewertungen schreiben mehrere Kunden, dass [konkretes Lob]. [Kurzer positiver Schluss]" (nur wenn mindestens 2 Bewertungen das Lob tragen) | „in deinen Bewertungen schreiben mehrere Kunden, dass du ehrlich berätst und auch mal von einer Reparatur abrätst, die sich nicht lohnt. Da weiß jeder vorher, woran er ist." |

### Angle 2: Abhebendes Detail von der Website

**Wann:** Die Bewertungen geben kein konkretes Lob her, aber die Website zeigt etwas, das den Betrieb abhebt (Abhebungs-Typen oben).

| Vorlage | Echtes Beispiel |
|:--------|:---------------|
| „ich war gerade auf deiner Website: [abhebendes Detail]. [Kurzer positiver Schluss]" | „ich war gerade auf deiner Website: Bei dir bekommt jeder Kunde nach der Elektroinstallation eine Fotodokumentation aller Leitungen hinter dem Putz. Wer später ein Bild aufhängt, weiß dann, wo er bohren darf." |
| „mir ist aufgefallen, dass [abhebendes Detail]. [Kurzer positiver Schluss]" | „mir ist aufgefallen, dass jedes Objekt bei dir ein festes Reinigungsteam hat, das man vorab mit Foto sieht. So weiß jeder Hausmeister, wer morgens kommt." |

**Auch Stellenanzeige oder Wachstum:** bei Recruiting-Offers oder wenn man über eine Anzeige etwas über den Betrieb erfährt. Anker ist die Erkenntnis, die die Anzeige über das Geschäft verrät (Wachstum, Spezialisierung, ein neues Projekt), nicht die Tatsache, dass gesucht wird. Nie „ich hab gesehen, dass du gerade [Position] suchst“.

| Vorlage | Echtes Beispiel |
|:--------|:---------------|
| „mir ist aufgefallen, dass du [Erkenntnis aus der Anzeige: Wachstum, Spezialisierung, Projekt]. [Kurzer positiver Schluss]" | „mir ist aufgefallen, dass du deinen Einkauf gerade so ausbaust, dass du künftig deutlich mehr Eigenmarken ins Sortiment nimmst. Damit bekommen deine Kunden Produkte, die es nur bei dir gibt." |

### Angle 3: Anzahl und Schnitt der Bewertungen

**Wann:** Kein Lob aus Bewertungstexten und kein abhebendes Website-Detail, aber mindestens 30 Bewertungen mit einem Schnitt ab 4,5. Unter 30 Bewertungen oder unter 4,5 keine Bewertungszahlen.
**Anker:** Zahl gerundet, Schnitt mit Komma, Quelle im Einstieg. Werte aus dem Import (Google-Profil) gelten als Quelle; widersprechen sich Quellen, gilt der kleinere Wert.

| Vorlage | Echtes Beispiel |
|:--------|:---------------|
| „ich hab mir deine Bewertungen angeschaut: [über N] Rezensionen mit einem Schnitt von [X,Y]. [Kurzer positiver Schluss]" | „ich hab mir deine Bewertungen angeschaut: über 200 Rezensionen mit einem Schnitt von 4,8. Wer neu einen Zahnarzt sucht, sieht daran, dass viele vor ihm gute Erfahrungen gemacht haben." |

### Angle 4: Fallback der Kampagne (Branchen-/Regional-Bezug)

**Wann:** Kein Anker besteht den Austauschtest. Schwächster Angle, aber besser als eine Floskel. Der Satz bleibt wörtlich, ohne angehängten Schluss, und behauptet nichts Unbelegtes über den Lead.

| Vorlage |
|:--------|
| „als [Branche]-Unternehmen in [Region] bist du genau die Art Firma, die wir suchen" |

### Angle 5: Storytelling / Bier-Masche (Sonderfall)

**Wann:** NUR bei regionaler Zielgruppe + Dialekt-Tonalität. Nicht als Standard-Angle verwenden. Funktioniert nur, wenn der Absender selbst aus der Region kommt und Dialekt authentisch rüberkommt. Die Dialekt-Anrede schreibt dann der `hallo`-Prompt, nicht ein Platzhalter.

| Echtes Beispiel |
|:----------------|
| „Servus Max, i hab mi' vor kurzem mit einem Unternehmer aus unserer Region über Marketing unterhalten. Er hat mir erzählt, dass es immer schwieriger wird, online aufzufallen. I dad mi' interessieren, wie läuft die Neukundengewinnung bei dir?" |

## Der Opener ist Lob oder eine anerkennende Beobachtung

Das Intro ist Lob oder eine anerkennende Beobachtung: ein positiver Bezug auf den Lead, der beweist, dass jemand hingeschaut hat, getragen von einem konkreten Detail. Es ist KEINE Kritik und KEIN Verbesserungsvorschlag. Das Problem sind leere Lobadjektive ohne Inhalt, nicht das Lob selbst.

Einstiege: keiner ist Standard. Die letzte Ziffer der Lead-ID entscheidet, ein Bewertungsanker nennt die Quelle (siehe „Einstiege abwechseln“).

**MUSS:**

- Abhebung statt Leistungsnennung: Der Opener besteht den Austauschtest und nennt kein Thema von der Sperrliste der Kampagne (außer als Lob aus Bewertungstexten). Ein Nutzen rettet keine Standardleistung
- Nach der Beobachtung ein kurzer positiver Schluss aus dem konkreten Detail: Nutzen oder Wirkung, sonst eine kurze Reaktion am benannten Detail, nie ein Prüfer-Urteil über die Qualität der Arbeit (Rangfolge und Leitplanken unter „Positiver Schluss“); der Fallback-Satz bleibt ohne Schluss
- Ausschließlich positiv: echtes Lob oder anerkennende Beobachtung, getragen vom konkreten Detail. Austauschbare Bewertungsfloskeln und Superlative („das spricht für sich", „das sieht man selten", „das sieht man nicht immer", „hat man nicht alle Tage", „finde ich stark", „finde ich spannend", „Hammer", „beeindruckend", auch umgestellt wie „ich finde spannend, dass …") sind verboten (ListM8-Regel), und zwar auch als Beispielsatz: Modelle kopieren Beispiele
- Anker in der Rangfolge: Lob aus Bewertungstexten (Paraphrase; Plural oder „immer wieder" nur, wenn mindestens 2 Bewertungen dieses Lob tragen), dann abhebendes Website-Detail, dann Anzahl und Schnitt als eigener Anker (nur ab 30 Bewertungen und 4,5, Zahl gerundet, Schnitt mit Komma, bei widersprüchlichen Quellen der kleinere Wert), dann der Fallback
- Stellenanzeige: die Erkenntnis über den Betrieb nutzen (Wachstum, Spezialisierung, Projekt), ohne anzukündigen, dass der Betrieb sucht oder einstellt
- Ein zweiter Satz ist konkret und wiederholt oder nimmt nicht vorweg, was der feste Text danach sagt. Beginnt der feste Text mit „Das hat mich neugierig gemacht.", darf kein Intro-Satz mit dieser Aussage davor stehen
- Zuschreibung stimmt: Der angeschriebenen Person nie etwas zuschreiben, das einer anderen gehört (etwa den Podcast der Inhaberin in einer Mail an eine Mitarbeiterin). Die Person beim Namen nennen oder einen Anker wählen, der zur angeschriebenen Person gehört
- Konkreter, verifizierbarer Bezug, den man nur kennt, wenn man wirklich auf Website/Shop/Bewertungen war
- Maximal 2 Sätze, etwa 30 Wörter
- Beginnt mit Kleinbuchstaben (folgt direkt auf „Hallo …,"); nur der erste Buchstabe ist klein, jeder weitere Satz beginnt groß. Substantive und Namen bleiben auch am Anfang groß („Kunden loben …“, nie „kunden loben …“)
- Inhaltlich über den EMPFÄNGER schreiben, nie über den Absender; Einstiegsrahmen wie „ich hab mir … angeschaut“ oder „mir ist aufgefallen“ sind erlaubt und keine Selbstvorstellung
- Locker und authentisch, Ton wie eine kurze Nachricht an einen Bekannten
- Muss nahtlos in die feste Überleitung übergehen, ohne ein Problem zu benennen

**NIEMALS:**

- Kritik, Defizit, Mangel, „Lücke", „Hürde", „Problem", „leider", „schade"
- Konjunktiv-Wunsch: „wäre (doch) schön/besser/sinnvoll, wenn ..."
- „noch nicht", „fehlt", „begrenzt", „veraltet", „ausbaufähig", „verschenkt Potenzial", auditartige Formulierungen
- Bevormundende Verbesserungsvorschläge oder Ratschläge
- Selbstvorstellung oder Pitch („Wir sind ...", „Mein Name ist ...", „Wir helfen ...")
- Floskeln („Ich bin auf Ihre Webseite gestoßen", „Tolle Webseite")
- Erfundene Fakten, Personen, Rollen oder Zahlen
- Sichtbare Platzhalter wie [Branche] oder [Name] oder M-Striche (—)

Warum kein Kritik-Opener: Wer mit einem Mangel einsteigt, macht den Empfänger klein und muss ihn danach überzeugen. Wer mit Lob einsteigt, hat ihn auf seiner Seite und muss nur noch das Offer nennen.

## Prompt-Vorlage: Standard-Opener (funktioniert für 80 % der Fälle)

Diese Vorlage geht als Prompt der AI-Variable `intro` in die Kampagne (`aiVariables`). Die Lead-Daten (Firma, Website, Stadt, Recherche, Custom-Attribute) bekommt das Modell beim Generieren automatisch dazu; sie müssen nicht als Platzhalter im Prompt stehen. Die Klammern füllst du beim Anlegen aus den Angaben des Nutzers.

```
Du schreibst einen individuellen Eröffnungssatz für eine Cold-E-Mail.
Der Absender ist [FIRMENNAME], [KURZBESCHREIBUNG DER DIENSTLEISTUNG].
Dein Text steht direkt unter der Anrede "Hallo ...," und wird mit einem
festen Satz fortgesetzt, der mit "[FESTER FOLGESATZ, z. B. Deswegen war
ich so frei ...]" beginnt.

Aufgabe:
Schreibe 1-2 Sätze, insgesamt etwa 30 Wörter: eine Beobachtung, die diesen
Betrieb von anderen seiner Branche abhebt, und danach einen kurzen
positiven Halbsatz: Nutzen oder Wirkung, sonst eine kurze Reaktion am
Detail. Der Opener muss
natürlich in das Marketing Offer überleiten.

Was abhebt: ein Eigenname oder eigenes Konzept, eine ungewöhnliche Zeit
oder Zahl, ein eigenes Verfahren, eine seltene Spezialisierung, eine
Auszeichnung, ein Lob aus Bewertungen, auffällige Bewertungszahlen.

AUSTAUSCHTEST: Passt dein Satz auf zehn andere Betriebe derselben Branche
in der Stadt, ist er kein Aufhänger. Dann nimm den nächsten Anker,
zuletzt den FALLBACK.
- Ein Nutzen rettet keine Standardleistung.
- Dasselbe Thema besteht als Lob aus Bewertungstexten (was Kunden über
  DIESEN Betrieb schreiben), nicht als Zeile aus der Leistungsliste.
- Fällt durch: [STANDARDLEISTUNG DER BRANCHE]. Besteht: [ABHEBENDER FUND
  AUS DERSELBEN BRANCHE].

SPERRLISTE (branchenübliche Leistungen, die keinen Opener tragen; erlaubt
nur als Lob aus Bewertungstexten):
[SPERRLISTE DER KAMPAGNE, meist 6-10 Begriffe aus Branche und Zielgruppe]

ANKER-REIHENFOLGE (nimm den ersten, der den Austauschtest besteht):
1. Lob aus Bewertungstexten: eine konkrete Paraphrase, was genau gelobt
   wird. Plural oder "immer wieder" nur, wenn mindestens 2 Bewertungen
   dieses Lob tragen.
2. Abhebendes Detail von der Website, auch Wachstum oder eine
   Stellenanzeige als Erkenntnis über den Betrieb (Wachstum,
   Spezialisierung, Projekt). Kündige nie an, dass der Betrieb sucht oder
   einstellt.
3. Anzahl und Schnitt der Bewertungen als eigener Anker, nur bei
   mindestens 30 Bewertungen und einem Schnitt ab 4,5: Zahl gerundet
   ("über 200"), Schnitt mit Komma ("4,8"). Werte aus dem Import
   (Google-Profil) gelten als Quelle; widersprechen sich Quellen, nimm den
   kleineren Wert. Unter 30 Bewertungen oder unter 4,5 keine
   Bewertungszahlen.
4. FALLBACK.

POSITIVER SCHLUSS: Nach der Beobachtung folgt ein kurzer Halbsatz. Zuerst
Nutzen oder Wirkung, wenn sie sich aus dem Detail anbietet (wem nützt es,
was bewirkt es). Sonst eine kurze persönliche Reaktion direkt hinter dem
benannten Detail (muss es nicht wiederholen), in der Vergangenheit erzählt (Muster: "das fand ich eine
schöne Idee", "hat mir gut gefallen"; nie allein und nie als feste
Wendung). Nie ein Prüfer-Urteil über die Qualität der Arbeit ("das wirkt
vertrauenswürdig", "so einen Schnitt hält man nur, wenn die Arbeit
stimmt", "da machst du vieles richtig", "das schafft man nicht ohne
sauberes Arbeiten", "zeigt, dass die Behandlung ankommt"). Nichts
erfinden, nur was direkt aus dem Detail folgt (nie "deine Kunden lieben
das", nie "alle positiv"). Keine inhaltsleere Formel und kein Superlativ
("finde ich stark", "Hammer", "das sieht man selten", "das sieht man nicht
immer", "hat man nicht alle Tage", "beeindruckend", "das spricht für
sich"). Bilde jeden Schluss aus dem konkreten Detail. Gilt auch bei
Bewertungsankern, nicht beim FALLBACK.

EINSTIEG: Kein Einstieg ist Standard. Wähle ihn nach der letzten Ziffer
der Lead-ID: 0-2 "mir ist aufgefallen, dass ...", 3-5 "ich hab mir ...
angeschaut", 6-7 "beim Stöbern auf deiner Website ...", 8-9 direkt mit
dem Detail. Ein Bewertungsanker nennt immer die Quelle im Einstieg ("ich
hab mir deine Bewertungen angeschaut, und ..."). Steht keine Lead-ID im
Kontext, wähle den Einstieg passend zum Anker und nicht immer denselben.

REGELN:
- Deutsch mit korrekten Umlauten (ä, ö, ü, ß)
- KEINE M-Striche und keine Gedankenstriche als Trenner, auch kein
  Bindestrich mit Leerzeichen; Bindestriche nur innerhalb von Wörtern;
  Komma statt Strich
- Max. 2 Sätze, etwa 30 Wörter
- Locker und authentisch, NICHT werblich
- Beginne mit Kleinbuchstabe (wird nach "Hallo ...," eingefügt); nur der
  erste Buchstabe ist klein, jeder weitere Satz beginnt groß; Substantive
  und Namen bleiben auch am Anfang groß ("Kunden loben ...")
- Beziehe dich auf etwas Konkretes, das man nur sehen kann wenn man
  wirklich auf der Website war
- Ausschließlich positiv: kein Mangel, keine Kritik, kein Verbesserungsvorschlag
- Verboten: "Lücke", "Hürde", "Problem", "leider", "schade", "noch nicht",
  "fehlt", "begrenzt", "veraltet", "ausbaufähig", "verschenkt Potenzial",
  Konjunktiv-Wünsche ("wäre schön, wenn ..."), Ratschläge, Selbstvorstellung
  ("Wir sind", "Mein Name ist", "Wir helfen"), Floskeln ("Ich bin auf deine
  Webseite gestoßen", "Tolle Webseite"), sichtbare Platzhalter in Klammern
- Keine Frage, kein Link, keine erfundene Zahl, kein erfundener Name; keine Kunden-, Projekt-,
  Ergebnis- oder Bewertungszahlen aus Selbstangaben der Website (Gründungsjahr mit
  seinem Ereignis und Teamgröße sind Tatsachen und erlaubt)
- Verboten sind auch "finde ich spannend", "finde ich stark" und andere
  Lobadjektive ohne Inhalt: das Detail trägt das Lob
- Ein zweiter Satz ist konkret und wiederholt oder nimmt nicht vorweg, was
  der feste Text danach sagt
- Schreibe der angesprochenen Person nichts zu, das einer anderen Person
  gehört (z. B. den Podcast des Inhabers in einer Mail an eine Mitarbeiterin);
  nenne die Person dann beim Namen
- Auch ein Projekt, eine Referenz, Firmengeschichte oder Gründungsjahr
  (mit seinem Ereignis), Auszeichnungen und Siegel (ohne Altersgrenze),
  Lage und Ausstattung können tragen, jeweils mit EINEM konkreten Detail
  und nur, wenn sie den Austauschtest bestehen. Eine Aufzählung von
  Leistungen ist nie ein Aufhänger.
- Wenn kein Anker den Austauschtest besteht: gib den Fallback-Satz zurück,
  erfinde nichts, schreibe keine Floskel und keine Leistungsliste

FALLBACK (wenn kein Anker den Austauschtest besteht; wörtlich, ohne
angehängten Schluss; er behauptet nichts Unbelegtes über den Lead, z. B.
nicht "so gut bewertet"):
"als [BRANCHE]-Unternehmen in [REGION] bist du genau die Art Firma,
die wir suchen"
```

Die Vorlage steht im Singular (du/dein); bei `sie` auf Sie/Ihnen/Ihre umschreiben. Sperrliste und Gegensatzpaar füllst du aus Branche und Zielgruppe (siehe „Sperrliste je Kampagne“); das Gegensatzpaar nennt nur Funde, nie einen fertigen Satz oder Schluss. Ein vollständig ausformulierter `intro`-Prompt steht in `beispiel-blueprint.md`.

## Ein schwacher Opener ist schlechter als der Fallback

Der wichtigste Punkt beim Prüfen: Ein generischer Opener („deine Website macht einen professionellen Eindruck") schadet mehr als ein ehrlicher Branchen-Fallback. Er verbrennt die einzige Stelle, an der die Mail persönlich wirken könnte, und der Empfänger merkt sofort, dass da eine Maschine geraten hat.

Deshalb gilt: **Lieber Fallback als Floskel.** Der Prompt muss das ausdrücklich erlauben, sonst erfindet das Modell etwas.

## Prüftabelle für die Stichprobe

Vor dem Export immer mindestens 10 Leads im Review (`outreach-verify`, `get_lead_variables`) von Hand lesen. Verwerfen (`reject_lead_variables`) und neu generieren, wenn einer dieser Punkte zutrifft:

| Prüfung | Verwerfen wenn |
|:--------|:---------------|
| Länge | Mehr als 2 Sätze oder deutlich über 30 Wörter |
| Groß-/Kleinschreibung | Beginnt mit Großbuchstaben (passt dann nicht hinter die Anrede) |
| Tonalität | Enthält Kritik, Mangel, Konjunktiv-Wunsch oder einen Ratschlag |
| Austauschtest | Würde genauso auf zehn andere Betriebe derselben Branche in der Stadt passen, nennt eine Standardleistung (auch mit Nutzen), oder das Lob besteht nur aus einem Adjektiv ohne Inhalt |
| Sperrliste | Der Anker steht auf der Sperrliste der Kampagne und ist kein Lob aus Bewertungstexten |
| Positiver Schluss | Fehlt, ist eine Floskel oder ein Superlativ, ist ein Prüfer-Urteil über die Qualität der Arbeit („das wirkt vertrauenswürdig“, „da machst du vieles richtig“), ist eine Reaktion, vor der kein Detail steht, behauptet etwas, das nicht direkt aus dem Detail folgt, oder hängt am Fallback-Satz. Gleich lautende Nutzen-Schlüsse über mehrere Leads sind ein systematischer Befund; wiederholte Reaktionen aus der Server-Liste sind es nicht |
| Bewertungsanker | Zahlen bei weniger als 30 Bewertungen oder einem Schnitt unter 4,5, ungerundete Zahl, Schnitt mit Punkt, der größere von zwei widersprüchlichen Werten, nur Zahlen, obwohl ein Lob aus Bewertungstexten belegt ist; „mehrere“/„immer wieder“ ohne mindestens 2 Bewertungen; Einstieg ohne Quelle |
| Zuschreibung | Schreibt der angesprochenen Person etwas zu, das einer anderen gehört |
| Wahrheit | Enthält Zahl, Name oder Fakt, der nicht aus dem Research kommt |
| Form | Enthält Fragezeichen, Ausrufezeichen, Link oder M-Strich |
| Platzhalter | Enthält sichtbares [Klammer-Feld] oder ein nicht aufgelöstes Merge-Tag |
| Übergang | Der feste Folgesatz („Genau deshalb ...", „Deswegen war ich so frei ...") schließt sich nicht flüssig an |
| Absender | Schreibt über uns statt über den Empfänger |

Wenn mehr als 2 von 10 Openern durchfallen, ist der Prompt das Problem, nicht der Lead. Dasselbe gilt, wenn mehr als ein Drittel gleich beginnt oder denselben Anker trägt. Dann Prompt nachschärfen (`update_ai_variable`) und die betroffenen Leads neu generieren, mit Zustimmung des Nutzers, weil die Neugenerierung erneut kostet.

## Wo der Opener steht - und wo nicht

Der personalisierte Opener steht ausschließlich in der Entry Mail. Follow-Ups nutzen nur die Anrede plus festen Text. Ein zweiter personalisierter Bezug in Mail 3 wirkt wie ein Skript, das sich wiederholt.

Damit der Opener überhaupt entstehen kann, braucht jeder Lead ein gefülltes Website-Feld - ohne Website hat die Recherche keine Grundlage und es bleibt zwangsläufig beim schwächsten Angle.

---

# TEIL 2: Die Entry Mail

## Die Goldene Formel

Jede Cold Mail besteht aus genau 3 Teilen nach der Ansprache. Kein Pitch, kein Proof, keine Firmenvorstellung.

```
ANSPRACHE  →  INDIVIDUELLER BEZUG  →  ÜBERLEITUNG + OFFER  →  CTA
(2-3 Wörter)   (1-2 Sätze)           (1-2 Sätze)             (1 Satz)
{{ai.hallo}}   {{ai.intro}}          fester Text             fester Text
```

Bei Karte A und C kommt zwischen Offer und CTA der Feinheiten-Satz als eigener Absatz (siehe unten).

| Baustein | Was er macht | Beispiel |
|:---------|:-------------|:---------|
| **Ansprache** | Tür aufmachen | „Hallo Max," |
| **Individueller Bezug** | Zeigen: ich hab mich mit dir beschäftigt | „ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, dass deine Lieferung schneller war als bei Amazon. Das ist ein Grund, direkt bei dir statt bei Amazon zu bestellen." |
| **Überleitung + Offer** | Nahtloser Brücken-Satz zum Angebot. KEIN Pitch. | „Deswegen war ich so frei und habe ein kurzes Video mit drei konkreten Hebeln für dich aufgenommen." |
| **CTA** | EINE Handlung. Nicht zwei | „Wäre es in Ordnung, wenn ich es dir zusende? Völlig unverbindlich natürlich." |

**Die Mail soll klingen wie eine WhatsApp von einem Freund, nicht wie eine Agentur-Website.**

## Was RAUS ist

**Proof-Block:** „Nach über 200 Kampagnen...", „Wir sind seit 10 Jahren...", „Als Google Premium Partner..." - das alles hat KEINEN Platz in der Entry Mail. Es schreckt Leute ab und wirkt wie ein Pitch.

**Wo Proof hingehört:**

- **FUP2** (Step 3, neuer Winkel) - dort gehören Case Studies und Social Proof hin
- **Signatur** - kurz und dezent (siehe Signatur-Regeln unten)

**VERBOTEN im Body:**

- „Wir helfen [Zielgruppe] dabei, [Dienstleistung]..." - PITCH
- „Das machen wir seit X Jahren..." - PITCH
- „Als [Zertifizierung/Partner]..." - PITCH
- Jeder Satz der die eigene Firma beschreibt - PITCH

Authority (Jahre, Kunden, Zertifizierungen) gehört in die **Signatur**, nicht in den Body.

## Die universelle Überleitung

Der wichtigste Baustein. Die Überleitung ist der statische Satz NACH dem individuellen Bezug. Er verbindet den Bezug nahtlos mit dem Offer - ohne Pitch. Er ist für alle Leads gleich, deshalb muss er zu JEDEM möglichen Bezug passen.

**Anforderungen:**

- Muss sich an JEDEN möglichen individuellen Bezug anschließen
- Muss direkt zum Offer überleiten
- Benennt KEIN lead-spezifisches Problem
- KEIN „Wir sind...", „Wir machen...", „Seit X Jahren..."
- 1-2 Sätze, nicht mehr

### Überleitungs-Bausteine nach Offer-Typ

| Offer-Typ | Überleitung |
|:----------|:------------|
| **A: Kostenlose Teildienstleistung** | „Genau deshalb bieten wir aktuell für [Anzahl] Unternehmen in [Region] ein kostenloses [Deliverable] an." |
| **B: Tester/Pilotprojekt** | „Genau solche Unternehmen suchen wir gerade. Wir starten [Projekt] mit [Anzahl] Betrieben in [Region]." |
| **C: Konkretes Deliverable (Reziprozität)** | „Deswegen war ich so frei und habe [Deliverable] für dich erstellt." |
| **D: Förder-Hook** | „Wusstest du, dass der Staat aktuell bis zu [Prozent] der [Kosten] übernimmt?" |
| **E: Partner gesucht** | „Genau solche [Branche] suchen wir als Partner. Wir haben regelmäßig [Anfragen] die zu dir passen würden." |

Bei Karte A und C steht das Deliverable als bereits erledigte bzw. laufende Arbeit da, nie als Absicht („würde gerne erstellen").

### Warum das funktioniert

„Genau deshalb...", „Deswegen war ich so frei...", „Genau solche Unternehmen..." - diese Formulierungen schließen sich an JEDEN individuellen Bezug an, egal ob der über Bewertungen, die Website oder die Branche spricht. Sie leiten direkt zum Offer über, ohne einen Pitch-Block dazwischen.

## Value Stacking: der Feinheiten-Satz

Bei den Offer-Typen Teildienstleistung (A) und Reziprozität (C) folgt nach dem Marketing-Offer ein zweiter Satz, der den Wert stapelt, ohne ein zweites Offer zu werden: Die Arbeit ist schon (fast) erledigt, und es kommt noch etwas on top. Bei B ist er optional, bei D und E entfällt er.

Wortlaut: „Ich bin gerade noch an den letzten Feinheiten dran, vor allem […], und werde morgen mit […] fertig." Er steht als eigener Absatz zwischen Offer und CTA.

```
Deswegen war ich so frei und habe dir einen kompletten Webseitenentwurf inklusive Buchungssystem erstellt.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an der Optimierung für Google und KI-Suchmaschinen, und werde morgen mit dem Entwurf fertig.

Wäre es in Ordnung, wenn ich dir das zusende? Völlig unverbindlich natürlich.
```

Die Regeln:

- **Erledigte Arbeit statt Absicht:** „war so frei und habe ... erstellt", nicht „würde gerne erstellen". Reziprozität wirkt erst, wenn das Geschenk schon existiert.
- **Genau EIN On-Top-Detail** („vor allem ..."), aus den Angaben des Nutzers, und es muss wirklich lieferbar sein. Nichts erfinden.
- **Kein zweiter CTA, kein zweites Offer.** Der Satz beschreibt dasselbe Deliverable, nur eine Schicht tiefer.

## Der CTA

Genau EIN CTA pro Mail. Nie zwei Optionen.

| Gut | Warum |
|:----|:------|
| „Antworte mir einfach kurz." | Niedrigste Hürde, die es gibt |
| „Darf ich es dir zusenden?" | Ja/Nein-Frage, eine Sekunde Aufwand |
| „Wäre es in Ordnung, wenn ich es dir zusende? Völlig unverbindlich natürlich." (nach „werde morgen … fertig“) | Reziprozität plus Ja/Nein |
| „Wäre das grundsätzlich interessant?" | Verpflichtet zu nichts |

Kein „Lass uns mal sprechen" ohne vorbereiteten Mehrwert. Kein Terminvorschlag in Mail 1. Kein Link in Mail 1 - der CTA ist die Antwort, nicht der Klick.

## Betreffzeilen

Die Betreffzeile entscheidet, ob die Mail geöffnet wird. Nur Step 1 trägt einen Betreff: 2-5 Wörter, keine Werbung. Er klingt wie eine harmlose Frage eines Menschen, keine Ankündigung und keine Ergebnisansage („Website für …“, „Entwurf für …“, „Idee für …“, „Website ist fertig“). Einen Firmennamen trägt er nur über `{{ai.firma}}` (bereinigter Kurzname), nie über das rohe `{{lead.company}}`: Importnamen sind oft Google-Titel oder Domains. Ohne Variable `firma` steht kein Name im Betreff, dann „kurze Frage“. Nie `{{firstName}}` (gibt es nicht) oder ein Custom-Attribut, das leer sein kann.

### Was funktioniert

| Stil | Beispiele | Warum |
|:-----|:---------|:------|
| **Neugier** | „kurze Frage" | Niedrige Hürde, macht neugierig; Standard für Karte C und jedes Entwurfs-Angebot |
| **Neugier** | „Frage zur Terminbuchung" | Wenn das Buchungssystem den Kern des Offers bildet |
| **Neugier** | „Zugang freigeschaltet" | Was für ein Zugang? Muss ich aufmachen (nur mit echtem Zugang, siehe unten) |
| **Persönlich** | „Meeting {{ai.firma}} & Julia" | Klingt nach echtem Termin (Karte A, nur mit `firma`) |
| **Persönlich** | „Gespräch {{ai.firma}} & Arne" | Impliziert bestehende Beziehung (nur mit `firma`) |
| **Direkt** | „Anfrage für {{ai.firma}}" | Business-like, ernst (Karte A/B, nur mit `firma`) |
| **Förderung** | „Deine Förderung" | Geld = Aufmerksamkeit (nur Karte D) |
| **Partner** | „Partnerschaft {{ai.firma}}?" | Augenhöhe (nur Karte E, nur mit `firma`) |

### Was nicht funktioniert

| Beispiel | Problem |
|:---------|:--------|
| „Website für {{ai.firma}}", „Anzeigen-Ideen für …" | Kündigt das Ergebnis an, klingt nach Werbung |
| „Anfrage für {{lead.company}}" | Roher Importname (Titel, Domain) im Betreff |
| „Kostenlose Beratung für {{ai.firma}}" | Zu lang, klingt nach Spam |
| „Exklusives Angebot - jetzt zugreifen!" | Spam-Trigger |
| „Re: Ihre Anfrage" | Fake-Reply, zerstört Vertrauen |

Zusätzlich: keine Großschreibung ganzer Wörter, keine Ausrufezeichen, keine Zahlen mit Prozentzeichen. Und niemals ein Spam-Wort im Betreff, auch wenn es im Body vorkommt - die vollständige Wortliste steht in Teil 4.

### Betreffzeilen für Follow-Ups

Step 2 und Step 4 haben keinen Betreff: das Feld bleibt leer, die Mails laufen im Thread der vorigen Betreff-Mail (Step 2 in Step 1, Step 4 in Step 3). Kein „Re:“.

Step 3 startet einen neuen Thread und bekommt deshalb einen eigenen kurzen Betreff, z. B. „kurzes Update“. Er wiederholt den Betreff von Step 1 nicht, kündigt kein Ergebnis an und folgt denselben Regeln wie der Betreff von Step 1 (2-5 Wörter, kein Spam-Wort, Firmenname nur über `{{ai.firma}}`).

### Test von Hand: Betreff-Variante B

Der Standard für Step 1 bleibt „kurze Frage“. Als Testmöglichkeit legt man beim echten Versand in Instantly von Hand eine Variante B „Frage zu {{firma}}“ an, in ein bis zwei Kampagnen mit Variable `firma`. Das ist ein Hinweis, keine Pflicht; ListM8 kennt keine Betreff-Varianten.

## Signatur-Regeln

Die Signatur darf NICHT wie eine Vertriebler-Signatur aussehen. Minimalistisch - Name, Titel, Firma. Fertig. Sie steht als Klartext aus den Angaben des Nutzers im festen Text, nie als `{{sender.*}}`-Variable. Ohne bekannten Absendernamen nur die Grußformel.

**So:**

```
Viele Grüße
Angela Selbert
Geschäftsführerin - njoy online marketing GmbH
```

**Auch ok (wenn wirklich beeindruckend):**

```
Viele Grüße
Michael Rohrböck
Geschäftsführer - Tiles Media GmbH
M.Sc. Informatik, TU Wien
```

**NICHT so:**

```
Viele Grüße
Angela Selbert
Geschäftsführerin - njoy online marketing GmbH
Google Premium Partner | 2.200+ Seminarteilnehmer
Ausgezeichnet als Top SEO Agentur 2025
www.njoy-online-marketing.de | Tel: 0221 298 012 63
Folge uns auf LinkedIn | Twitter | Instagram
```

**Warum:** Eine aufgeblähte Signatur macht den gleichen Fehler wie ein Pitch-Block im Body - sie schreit „Ich will dir was verkaufen". Je mehr Zeilen, desto mehr wirkt es wie eine Agentur-Mail statt wie eine persönliche Nachricht.

## Vollständige Beispiele

**Karte A, kostenlose Teildienstleistung (79 Wörter):**

```
Betreff: Meeting {{ai.firma}} & Julia

Hallo Max,

mir ist aufgefallen, dass jedes Objekt bei dir ein festes
Reinigungsteam hat, das man vorab mit Foto sieht. So weiß jeder
Hausmeister, wer morgens kommt.

Genau deshalb bereiten wir aktuell für zwei Unternehmen in der Region
München ein kostenloses Google Ads Setup vor.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an den
Suchbegriffen für dein Gewerk, und werde morgen mit dem Setup fertig.

Wenn das für dich spannend klingt, antworte mir einfach kurz.

Viele Grüße
Julia Weinmann
Co-Founder - Weinmann Media
```

**Karte C, Reziprozität (86 Wörter):**

```
Betreff: kurze Frage

Hallo Max,

ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, dass
deine Lieferung schneller war als bei Amazon. Das ist ein Grund, direkt
bei dir statt bei Amazon zu bestellen.

Deswegen war ich so frei und habe ein kurzes Video mit drei konkreten
Hebeln für deinen Shop aufgenommen.

Ich bin gerade noch an den letzten Feinheiten dran, vor allem an den
Beispielen aus deinem Sortiment, und werde morgen mit dem Video fertig.

Wäre es in Ordnung, wenn ich es dir zusende? Völlig unverbindlich natürlich.

Viele Grüße
Angela Selbert
Geschäftsführerin - njoy online marketing GmbH
```

**Karte E, Partner gesucht (64 Wörter):**

```
Betreff: Partnerschaft {{ai.firma}}?

Hallo Max,

mir ist aufgefallen, dass du Holzfenster im Denkmalschutz nachbaust,
Profil für Profil nach dem Original. Damit behält ein Altbau sein
Gesicht, auch wenn die Fenster neu sind.

Genau solche Handwerksbetriebe suchen wir als Partner. Wir haben
regelmäßig Anfragen von Bauherren in der Region, die genau solche
Projekte umsetzen wollen und einen zuverlässigen Betrieb suchen.
Wäre das grundsätzlich interessant? Antworte mir einfach kurz.

Viele Grüße
Max Huber
Geschäftsführer - Huber Architekten
```

Alle drei liegen zwischen 64 und 86 Wörtern, also im Korridor, in dem die abgenommenen Kampagnen arbeiten (55 bis 86). Gezählt ist der Body ohne Betreff und Signatur, Anrede und Bezug eingerechnet.

---

# TEIL 3: Die Follow-Ups

Follow-Ups sind keine Wiederholungen. Jede hat eine eigene Aufgabe, ein eigenes Wortlimit und maximal EINEN neuen Aspekt. Die Sequenz ist kein Trichter aus immer dringlicheren Aufforderungen, sondern eine Reihe kurzer, menschlicher Nachrichten - jede mit genau einem neuen Gedanken.

**Die Wortzahlen sind Obergrenzen.** Kürzer ist bei Follow-Ups fast immer besser: Die Ultra-kurz-Variante von FUP1 hat 14 Wörter und funktioniert genau deshalb - sie sieht aus wie eine echte Nachricht zwischen zwei Terminen, nicht wie ein Textbaustein.

**Kein Doppelpunkt-Opener.** Ein Einstieg wie „kurz nachgehakt:", „kurzes Update:" oder „zur Erinnerung:" direkt nach der Anrede wirkt sofort wie Werbung. Jedes Follow-Up beginnt mit einem ganzen, weichen Satz in der Ansprache der Kampagne - so, wie man einem Bekannten schreibt.

In der Sequenz beginnt jedes Follow-Up mit `{{ai.hallo}}`; die Texte unten stehen aufgelöst mit „Hallo Max,". Kein `{{ai.intro}}` in Follow-Ups.

## FUP1: Erinnerung (Step 2, 30-50 Wörter, `delayDays` 3)

**Aufgabe:** Nur nachhaken. Kein neuer Pitch, kein Offer wiederholen. Betreff leer, die Mail läuft im Thread von Mail 1.

| Variante | Text |
|:---------|:-----|
| **Locker** | „Hallo Max, wollte nur kurz nachhaken. Hast du meine Mail von letzter Woche gesehen? Vielleicht ist sie im Trubel untergegangen. Gib mir hier gerne kurz Bescheid." |
| **Ultra-kurz** | „Hallo Max, ist meine Mail von letzter Woche angekommen? Gib mir gerne kurz Bescheid." |
| **Weich** | „Hallo Max, du hast sicher viel um die Ohren. Ich wollte nur sichergehen, dass meine Mail von letzter Woche angekommen ist. Gib mir gerne kurz Bescheid." |

Das ist alles. FUP1 ist die kürzeste Mail der Sequenz und darf sich anfühlen wie eine Nachricht, die in 10 Sekunden getippt wurde. „Letzte Woche" nur schreiben, wenn der Abstand das hergibt; bei 3 Tagen „neulich" oder „vor ein paar Tagen".

## FUP2: Neuer Winkel mit Social Proof (Step 3, 50-80 Wörter, `delayDays` 5)

**Aufgabe:** EIN neuer Aspekt. **HIER gehört der Social Proof hin - nicht in die Entry Mail.**

**Neuer Thread:** Diese Mail bekommt einen eigenen kurzen Betreff (z. B. „kurzes Update“) und steht ohne den Verlauf von Mail 1. Sie muss für sich verständlich sein: höchstens ein Halbsatz Bezug auf das Angebot, kein neues Offer, kein Pitch. Wer Mail 1 nie geöffnet hat, sieht so eine frische Nachricht statt einer dritten Erinnerung im selben Faden.

Das ist der Slot, den die meisten verschenken. In der Entry Mail wirkt Proof wie ein Pitch. Hier, nach zwei Kontakten ohne Verkaufsdruck, wirkt er wie ein Beleg.

| Variante | Text |
|:---------|:-----|
| **Case Study** | „Hallo Max, letzte Woche hatte ich einen Händler im Gespräch, der zwei Jahre lang gekämpft hat, seinen Amazon-Account wieder freizuschalten. Am Ende hat ihn eine falsche Handynummer endgültig rausgeworfen. Alles weg. Genau solche Geschichten zeigen, warum ein starker eigener Shop so wichtig ist. Falls das Thema für dich relevant ist, melde dich gerne." |
| **Konkretes Ergebnis** | „Hallo Max, wir haben gerade ein Pilotprojekt im [Branche]-Bereich abgeschlossen. Der Betrieb spart jetzt über 15 Stunden pro Woche, weil die komplette Auftragsabwicklung automatisiert läuft. Vorher war das ein Vollzeitjob, jetzt klickt der Inhaber morgens einmal drauf und der Rest läuft. Falls das auch für dich spannend klingt, melde dich gerne." |
| **Relevanter Fakt** | „Hallo Max, bei Unternehmen mit bis zu 49 Mitarbeitern liegt die Förderquote aktuell bei bis zu 100 % der Weiterbildungskosten plus Lohnkostenzuschuss. Das heißt konkret: Dein Team lernt neue Skills und der Staat zahlt den größten Teil. Falls das auch für dich relevant ist, melde dich gerne. Ich kann dir in zwei Minuten sagen, was für dich drin wäre." |

**Regel für die Case Study:** eine Geschichte, eine Zahl, ein Ergebnis. Keine Aufzählung von Kunden, keine Logo-Parade. Nur Belege, die der Nutzer angegeben hat.

**Regel für Zahlen:** immer als Spanne („bis zu"), nie als Zusage. Förderquoten und Ergebnisse hängen von Größe, Branche und Programm ab - eine pauschale Behauptung stimmt für einen Teil der Empfänger nicht und macht die ganze Mail unglaubwürdig.

## FUP3: Abschied mit Routing-Hinweis (Step 4, 40-60 Wörter, `delayDays` 7)

**Aufgabe:** Tür offen lassen, ohne Druck, und mit einem Satz klären, ob jemand anderes der bessere Ansprechpartner ist. Betreff leer, die Mail läuft im Thread von Mail 3.

| Variante | Text |
|:---------|:-----|
| **Verständnisvoll mit Routing** | „Hallo Max, da ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung. Sag mir gern kurz Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte. Alles Gute!" |
| **Mit belegten Namen** (Variable `routing`) | „Hallo Max, ich bin mir nicht sicher, ob ich damit bei dir richtig bin oder eher bei Anna oder Tom. Gib mir gern kurz Bescheid." |

Kein Vorwurf, keine letzte Chance, keine Schuldzuweisung, keine künstliche Knappheit. Der Abschied bringt erfahrungsgemäß mehr Antworten als eine Dringlichkeits-Mail, genau weil er nichts will und eine leichte Antwort erlaubt („schreib Anna“). Die zweite Variante braucht ein Recherche-Ziel und die AI-Variable `routing`, siehe `routing-baustein.md`.

## Optional: Dringlichkeit als zusätzlicher Step

„Dringlichkeit“ gehört nicht zum Standard. Nur wenn der Nutzer einen echten Zeit- oder Kapazitätsgrund nennt, kommt sie als zusätzlicher Step zwischen Step 3 und den Abschied (dann fünf Steps, `delayDays` 0/3/5/7/7, max. 60 Wörter, Betreff leer, Thread von Mail 3).

| Variante | Text |
|:---------|:-----|
| **Kapazität** | „Hallo Max, wir haben aktuell nur noch einen freien Platz für unser Pilotprojekt in [Region]. Wollte kurz abklären, ob das Thema für dich relevant ist, bevor der Platz weg ist. Gib mir einfach kurz Bescheid." |
| **Zeitfenster** | „Hallo Max, die Fördertöpfe werden jährlich neu vergeben und sind ab Q3 erfahrungsgemäß knapper. Falls du dieses Jahr noch profitieren willst, solltest du zeitnah starten." |

Wenn die Dringlichkeit erfunden ist, merkt der Empfänger das - und dann ist auch die Entry Mail rückwirkend unglaubwürdig. Nur echte Kapazitäts- oder Zeitgrenzen nennen, die der Nutzer angegeben hat; ohne echten Grund entfällt der Step.

## Der CTA wird von Mail zu Mail weicher

| Mail | CTA-Charakter | Beispiel |
|:-----|:--------------|:---------|
| Entry | Erlaubnis erbitten | „Darf ich es dir zusenden?" |
| FUP1 | Nur anstoßen | „Ist meine Mail angekommen?" |
| FUP2 | Offen anbieten | „Falls das für dich relevant ist, melde dich gerne." |
| FUP3 | Tür offen lassen, Routing | „Sag mir gern kurz Bescheid, falls ich mich besser bei jemand anderem melden sollte." |

Je später die Mail, desto niedriger die Hürde. Wer im Abschied plötzlich einen Termin verlangt, dreht die Logik um.

## Der Fehler, der jede Sequenz killt

Das Offer steht NUR in der Entry Mail. Follow-Ups wiederholen es NICHT.

```
SCHLECHT (FUP1):
"Hallo Max, ich hatte dir letzte Woche geschrieben wegen unserem
kostenlosen Google Ads Setup wo wir dir 3 Kampagnen einrichten..."

GUT (FUP1):
"Hallo Max, wollte nur kurz nachhaken. Hast du meine Mail
von letzter Woche gesehen?"
```

Warum: Wer das Offer wiederholt, sagt dem Empfänger „du hast meine Mail nicht verstanden". Wer nur nachhakt, sagt „ich weiß, dass dein Tag voll ist". Das Zweite bekommt Antworten.

Weitere Regeln:

- Kein personalisierter Opener in den Follow-Ups. Der individuelle Bezug ist in Mail 1 passiert und wirkt in Mail 3 wie ein Skript.
- Jeder FUP hat max. EINEN neuen Aspekt. Nicht zwei, nicht drei.
- Step 2 läuft im Thread der Entry Mail und Step 4 im Thread von Step 3, damit der Kontext sichtbar bleibt; ihr Betreff bleibt leer. Step 3 öffnet einen neuen Thread mit eigenem kurzem Betreff.

## Wenn Antworten kommen, aber keine Termine

Dann ist nicht die Sequenz das Problem. Dann wurde nicht nachtelefoniert - der Schritt, den Kunden am häufigsten überspringen und der die Terminquote am stärksten verändert.

---

# TEIL 4: Qualität, Verbote und Freigabe

Die meisten Cold Mails scheitern nicht an einem fehlenden Trick, sondern an einem zu viel: ein Satz über die eigene Firma, ein zweiter CTA, ein Link, zwanzig Wörter mehr. Prüfen heißt hier fast immer streichen.

Und: Prüfen ist kein Geschmacksurteil. Fast alles, was eine Mail killt, ist messbar - Wortzahl, Anzahl der CTAs, verbotene Formulierungen, Sonderzeichen. Wer nach Gefühl freigibt, gibt irgendwann alles frei.

## Die 12 Gebote

1. **Immer über den EMPFÄNGER schreiben, nie über den Absender.** „Du bekommst..." statt „Wir bieten..."
2. **KEIN Firmen-Pitch im Body.** Keine Selbstvorstellung, kein „Wir machen X seit Y Jahren". Die Mail soll klingen wie eine WhatsApp, nicht wie eine Agentur-Website
3. **Nahtlose Überleitung nach dem Opener.** Der nächste Satz MUSS an den Empfänger anschließen, KEIN Wechsel zum Absender
4. **Offer steht NUR in der Entry Mail.** Follow-Ups wiederholen es NICHT
5. **EIN CTA pro Mail.** Nie zwei Optionen
6. **Kein Bold im Fließtext.** Soll aussehen wie eine echte Mail
7. **Keine Bulletpoints** in der Mail selbst
8. **Keine Emojis**
9. **Keine Gedankenstriche als Trenner** - kein M-Strich (—) und auch kein Bindestrich mit Leerzeichen ( - ). Bindestriche nur innerhalb von Wörtern (E-Mail, Smart-Home); Ausnahme ist die Signaturzeile „Rolle - Firma"
10. **Wortlimits sind hart.** Wenn drüber: kürzen
11. **Betreffzeile ultra kurz** (2-5 Wörter, ohne Spam-Wort, persönlich über `{{ai.firma}}` oder Neugier)
12. **Jeder FUP hat max. EINEN neuen Aspekt.** Nicht zwei, nicht drei

## Anti-Patterns: Was sofort killt

### Anti-Pattern 1: Der Pitch-Block nach dem Bezug

```
SCHLECHT:
"ich war gerade auf deinem Shop und habe mir die Bewertungen angeschaut.
Einer deiner Kunden schreibt, dass deine Lieferung schneller war als bei
Amazon.

Wir helfen E-Commerce Unternehmen dabei, ihre Umsätze
unabhängiger von Amazon aufzubauen - vor allem über Google
Shopping. Das machen wir seit über 10 Jahren als Google
Premium Partner für Shops in ganz DACH.

Bei deinem Shop sehe ich da echtes Potenzial..."

WARUM SCHLECHT:
- Der zweite Absatz ist ein kompletter Firmen-Pitch
- "Wir helfen X dabei Y" = Agentur-Website
- "Seit 10 Jahren" + "Premium Partner" = niemand hat gefragt
- Der Leser schaltet ab bevor er zum Offer kommt
```

**So geht's besser:**

„ich hab mir deine Bewertungen angeschaut, und ein Kunde schreibt, dass deine Lieferung schneller war als bei Amazon. Das ist ein Grund, direkt bei dir statt bei Amazon zu bestellen. Deswegen war ich so frei und habe ein kurzes Video mit drei konkreten Hebeln zu deinem Online-Auftritt aufgenommen. / Ich bin gerade noch an den letzten Feinheiten dran, vor allem an den Beispielen für deine Startseite, und werde morgen mit dem Video fertig. / Wäre es in Ordnung, wenn ich es dir zusende? Völlig unverbindlich natürlich." (/ = neuer Absatz)

Kein Pitch. Vom Bezug direkt zum Offer. Fertig.

### Anti-Pattern 2: Die Über-uns-Mail

```
SCHLECHT:
"Guten Tag, wir sind ein führender Anbieter im Bereich
Marketing und möchten Ihnen unsere Dienste vorstellen..."

WARUM SCHLECHT:
Schreibt über sich selbst, kein Bezug, kein Offer.
```

### Anti-Pattern 3: „Analyse" als Offer

„Analyse ist der kleine Freund von Sales Call und jeder checkt, dass das ein Verkaufs-Call ist."

Nie: „Kostenlose Website-Analyse", „Unverbindliches Audit", „Potenzial-Check", „Erstgespräch", „Beratung", „Strategiegespräch"

Stattdessen ein konkretes Deliverable: „Kostenloses Google Ads Setup", „Ein kurzes Video mit 3 Hebeln"

### Anti-Pattern 4: Offer in Follow-Ups wiederholen

Der Reminder darf nur nachhaken, nicht das Angebot erklären. Wer es wiederholt, sagt dem Empfänger „du hast meine Mail nicht verstanden". Die Vorher-Nachher-Beispiele stehen in Teil 3.

### Anti-Pattern 5: Zwei CTAs

```
SCHLECHT:
"Antworte mir kurz oder buche dir hier einen Termin: [Link]"

GUT:
"Antworte mir einfach kurz."
```

### Anti-Pattern 6: KI-Sprache

| KI-Signal | Besser |
|:----------|:-------|
| „In der heutigen schnelllebigen Geschäftswelt..." | Weglassen |
| M-Striche überall | Satz teilen oder Komma; Bindestriche nur innerhalb von Wörtern |
| „Lass mich wissen, wenn du Interesse hast" | „Antworte mir kurz" |
| Perfekte Grammatik in lockerem Kontext | Schreib wie du sprichst |
| „Gerne möchte ich Ihnen aufzeigen..." | „Ich zeig dir kurz..." |

Weitere Formulierungen, die eine Mail sofort nach Maschine klingen lassen:

| Verdächtig | Besser |
|:-----------|:-------|
| „Ich hoffe, diese Nachricht erreicht Sie gut" | Weglassen, direkt zum Bezug |
| „Ich wollte mich einmal bei Ihnen melden" | Weglassen |
| „Darüber hinaus", „Nicht zuletzt", „Zusammenfassend" | In einer 100-Wort-Mail hat nichts davon Platz |
| „Es ist wichtig zu verstehen, dass..." | Den Punkt einfach sagen |
| „Wir sind bestrebt", „Synergien", „ganzheitlich", „nachhaltig skalieren" | Konkret sagen, was passiert |
| „Ich freue mich auf Ihre Rückmeldung" | „Antworte mir einfach kurz" |
| Drei Adjektive in einer Reihe | Eines reicht, meistens keines |

## Formale Anforderungen

Diese Punkte haben nichts mit Geschmack zu tun - sie entscheiden, ob die Mail im Postfach oder im Spam landet.

| Regel | Warum |
|:------|:------|
| **Plain Text, kein HTML-Layout** | Aufwendig gestaltete Mails sehen für Spam-Filter aus wie Newsletter |
| **Kein Link in der Entry Mail** | Der CTA ist die Antwort, nicht der Klick. Ein Link im Erstkontakt ist zusätzlich ein Automations-Signal |
| **Max. 1 Link ab FUP2 (Step 3)** | Und nur zu Kalender oder Website |
| **Keine Anhänge** | Sofort verdächtig. Erst nach Reply senden |
| **Keine Bilder, keine Logos im Body** | Gleicher Effekt wie HTML-Layout |
| **Keine Großschreibung ganzer Wörter** | Klassisches Spam-Merkmal, besonders im Betreff |
| **Abmeldehinweis am Ende** | Eine schlichte Zeile, kein bunter Button. Wer keinen Abmeldeweg findet, klickt stattdessen auf Spam - und die Beschwerdequote ist der Wert, an dem die Zustellung hängt |

Open- und Link-Tracking sind Standard und ausdrücklich erlaubt - die KPI-Steuerung und das Nachtelefonieren nach Öffnern hängen daran. Eingerichtet wird beides im Versandtool, nicht in der Kampagne.

## Spam-Trigger im Deutschen

Diese Wörter erhöhen die Spam-Wahrscheinlichkeit messbar. Im **Betreff sind sie komplett verboten**, im Body werden sie vermieden:

„gratis", „100 %", „garantiert", „Garantie", „jetzt zugreifen", „jetzt handeln", „begrenztes Angebot", „nur heute", „exklusives Angebot", „hier klicken", „Rabatt", „Sonderpreis", „Gewinner", „Sie haben gewonnen", „dringend", „risikofrei", „ohne Risiko", „Geld verdienen"

## Wenn die abgenommene Copy und das Zustellrisiko kollidieren

Der Copywriting-Baukasten ist an echten Kampagnen erprobt und gilt. An drei Stellen empfiehlt er trotzdem etwas, das aus Zustellsicht ein Risiko trägt. Hier stehen die Entscheidungen dazu - die Copy-Regeln oben bleiben unangetastet.

### „kostenlos" im Offer

Der Baukasten baut mehrere Offer-Typen darauf auf („Kostenloses Google Ads Setup"), und das bleibt so - ein konkretes Deliverable trägt das Wort.

- **Im Betreff: nie.** Auch nicht als „kostenfrei" oder „gratis"
- **Im Body: höchstens einmal**, und nur direkt am konkreten Deliverable, nie als Eigenschaft der Zusammenarbeit („ein kostenloses Erstgespräch")
- **Nie in Kombination** mit einem zweiten Trigger („jetzt kostenlos zugreifen")

Ein vages Angebot wird von dem Wort nur verdächtig, ein konkretes nicht.

### „100 %" im Förder-Follow-Up

Das Förder-Beispiel im Follow-Up nennt „100 % der Weiterbildungskosten". Zwei Anpassungen beim Einsatz:

- **Als Spanne formulieren:** „bis zu 100 %" statt „100 %". Förderquoten hängen von Größe, Branche und Programm ab - eine pauschale Zusage stimmt für einen Teil der Empfänger nicht
- Die Zahl darf im Body stehen, weil sie hier eine Sachinformation ist und kein Werbeversprechen. Im **Betreff** hat sie nichts zu suchen

### „Zugang freigeschaltet"

Steht in der Betreffzeilen-Bibliothek und funktioniert - sie macht neugierig. Aber sie verspricht einen Zugang, den es beim Öffnen nicht gibt, und enttäuschte Neugier ist der kürzeste Weg zu einer Spam-Beschwerde.

- **Nur verwenden, wenn es den Zugang wirklich gibt** - etwa den Platz im Pilotprojekt aus Offer-Karte B
- Sonst eine der anderen Neugier-Betreffzeilen wählen („kurze Frage")

## Die Zahl, an der die Zustellung hängt

Neben Bounce und Reply gibt es einen dritten Wert, der über die Zustellbarkeit entscheidet: die **Spam-Beschwerdequote**. Sie muss unter **0,3 %** bleiben - das ist der Schwellenwert der großen Anbieter, kein Erfahrungswert.

Was die Quote treibt, ist fast immer Copy: irreführende Betreffzeilen, ein Offer, das die Mail nicht hält, kein erkennbarer Abmeldeweg, oder eine Zielgruppe, für die die Mail keinen Sinn ergibt. Deshalb ist sie hier und nicht nur in der Kampagnensteuerung ein Thema.

## Proof-Reading-Checkliste

Vor dem Anlegen bzw. vor dem Export jede Mail mit dieser Liste prüfen.

**Struktur:**

- [ ] Folgt der Goldenen Formel (Bezug - Überleitung + Offer - [Feinheiten-Satz bei A/C] - CTA)?
- [ ] Wortlimit eingehalten?
- [ ] Nur EIN CTA?
- [ ] KEIN Pitch-Block? (keine Firmenvorstellung, kein „Wir sind seit X Jahren...")
- [ ] Kein Bold, keine Bullets, keine Emojis?

**Inhalt:**

- [ ] Schreibe ich über den EMPFÄNGER oder über uns?
- [ ] Besteht der individuelle Bezug den Austauschtest (passt nicht auf zehn andere Betriebe der Branche, nichts von der Sperrliste außer als Bewertungslob), mit kurzem positivem Schluss aus dem Detail (Nutzen oder Reaktion am Detail, kein Prüfer-Urteil) und ohne Lobadjektiv ohne Inhalt? Bewertungszahlen nur ab 30 Bewertungen und einem Schnitt von 4,5?
- [ ] Stimmt die Anrede (Du-Form: Vorname der Person, der die Adresse gehört, bei generischen Adressen der Entscheider; sonst „Hallo,“)?
- [ ] Ist das Offer konkret genug? (Würde ICH antworten?)
- [ ] Kommt Social Proof erst im FUP2 (Step 3, neuer Thread), NICHT in der Entry Mail?
- [ ] Klingt die Signatur schlank und nicht wie ein Pitch?

**Follow-Ups:**

- [ ] Wird das Offer in den FUPs NICHT wiederholt?
- [ ] Hat jeder FUP max. EINEN neuen Aspekt?
- [ ] Ist der Social Proof/Case Study im FUP2 (nicht vorher)?

**Formatierung:**

- [ ] Keine M-Striche und keine Gedankenstriche als Trenner?
- [ ] Betreff von Step 1: 2-5 Wörter, ohne Spam-Wort, ohne Ankündigung, ohne `{{firstName}}`/`{{companyName}}`, Firmenname nur als `{{ai.firma}}`? Step 3 mit eigenem kurzem Betreff (nicht gleich Step 1), Step 2 und 4 ohne Betreff?
- [ ] Anrede über `{{ai.hallo}}`, Pronomen passend zur `salutation`?
- [ ] Klingt die Mail wie von einem Menschen, nicht wie ChatGPT?

**Zustellung:**

- [ ] Kein Link in der Entry Mail?
- [ ] Kein Spam-Wort im Betreff?
- [ ] „kostenlos" höchstens einmal im Body, nie im Betreff?
- [ ] Keine sichtbaren Platzhalter oder nicht aufgelösten Variablen?
- [ ] Abmeldehinweis vorhanden?

## Der Prüfdurchlauf in acht Schritten

Wenn du eine fertige Mail prüfst (oder eine gerade geschriebene selbst kontrollierst), geh in dieser Reihenfolge vor. Jeder Schritt hat genau eine Frage:

1. **Als Empfänger lesen.** Würdest du antworten? Wenn nein: warum nicht? Das ist der einzige Test, der zählt.
2. **Absender-Check.** Jeden Satz durchgehen: geht er über den Empfänger oder über uns? Jeder Satz über uns fliegt raus, außer der Signatur.
3. **Pitch-Scan.** Suche nach „wir helfen", „wir sind", „wir machen", „seit ... Jahren", „als ... Partner". Jeder Treffer ist ein Anti-Pattern 1.
4. **CTA zählen.** Mehr als eine Handlungsaufforderung? Streichen bis eine übrig ist.
5. **Wörter zählen.** Über dem Limit? Kürzen, nicht umformulieren.
6. **Zeichen-Scan.** Gedankenstriche (— oder Bindestrich mit Leerzeichen als Trenner), Emojis, Bold, Bullets, Links - Zeichen für Zeichen durchgehen, nicht überfliegen. Gedankenstriche sind das häufigste KI-Signal und rutschen am leichtesten durch.
7. **Spam-Scan.** Betreff und Body gegen die Trigger-Liste prüfen, „kostenlos" und „100 %" gegen die Regeln oben.
8. **Austauschtest.** Würde der Opener genauso auf zehn andere Betriebe derselben Branche in der Stadt passen? Dann ist er zu schwach: nächster Anker, zuletzt der Fallback.

Bei jedem Fehler: korrigieren und den Durchlauf **von vorne** starten. Korrekturen erzeugen neue Fehler - besonders beim Kürzen.

## Das Wichtigste

Ohne Detail kein Beweis - eine echte Bewertung, ein echtes Feature, eine echte Stellenanzeige ist der Unterschied zwischen einer Mail, die persönlich wirkt, und einer, die es nur behauptet.

Schreib über den Empfänger, nie über den Absender. Vier kurze Mails mit je einem Gedanken schlagen zwei lange mit je fünf. Und beim Prüfen gilt: zwei Drittel sind Streichungen, ein Drittel ist Zeichen zählen. Nur der erste Schritt - „würde ich antworten?" - ist Ermessen, und der entscheidet am Ende trotzdem alles.
