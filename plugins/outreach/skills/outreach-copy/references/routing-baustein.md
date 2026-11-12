# Routing im Abschied – „bei dir richtig oder eher bei X oder Y?“

Der letzte Step jeder Sequenz (der Abschied) fragt den Empfänger je Lead, ob eine andere, namentlich
genannte Person der bessere Ansprechpartner ist. Wirkt, weil es eine leichte Antwort erlaubt („schreib
Anna“) und zeigt, dass recherchiert wurde. Seit 31.10.2026 ist das in der App der Standard jeder neuen
Sequenz; das Plugin baut den Abschied genauso.

## Wo in der Sequenz

Als **Step 4** (Abschied, `delayDays` 7, leerer Betreff, Thread von Step 1). Hat der Nutzer einen
echten Zeit- oder Kapazitätsgrund, steht eine Dringlichkeits-Mail davor, der Abschied wird Step 5.
Der Body ist der Abschied der App: Anrede, fester Abschiedssatz, `{{ai.routing}}` als eigener Absatz,
Grußformel und Signatur. Nie ein fester Routing-Satz an dieser Stelle.

Deutsch (Du- und Sie-Form gleich):

```text
{{ai.hallo}}\n\nda ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung.\n\n{{ai.routing}}\n\n\nViele Grüße\n{{accountSignature}}
```

Englisch:

```text
{{ai.hallo}}\n\nSince I haven't heard back, I'll assume the timing isn't right, and that's completely fine.\n\n{{ai.routing}}\n\n\nBest,\n{{accountSignature}}
```

## Die Variable `routing`

- Name `routing`, in jeder neuen Kampagne, nach den übrigen Variablen.
- Prompt: wörtlich der Prompt der App, nicht selbst formulieren, nicht kürzen, keine angebotsbezogenen
  Stellen einsetzen: Das Angebot der ersten Mail kennt der Prompt aus der Kampagne. Deutsche Kampagnen
  nehmen die Fassung zur `salutation` (Du oder Sie): den ROUTING-PROMPT aus dem MCP-Prompt
  `campaign_blueprint_guide`, der den Stand des verbundenen Servers trägt; ist er nicht greifbar, die
  Fassung unten. Englische Kampagnen nehmen immer die englische Fassung unten: Der Guide liefert nur
  die beiden deutschen, und der Server tauscht den Prompt beim Anlegen nicht aus. Ein deutscher Prompt
  in einer englischen Kampagne schreibt deutsche Sätze.
- Der Prompt schreibt höchstens 35 Wörter, beginnt groß, ohne Anrede, Abschiedssatz und Gruß, in vier
  Fällen:
  - **A**, die Recherche belegt andere, aktuell beschäftigte Personen mit passender Rolle: „Ich bin
    mir nicht sicher, ob ich damit bei dir richtig bin oder eher bei <Vorname 1> oder <Vorname 2>.
    Gib mir gern kurz Bescheid.“
  - **B**, keine belegten Alternativen und die Zuständigkeit ist unklar: genau „Sag mir gern kurz
    Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte.“
  - **C**, Einzelbetrieb, eindeutig zuständiger Empfänger oder der Vermerk „Routing nicht sinnvoll“:
    eine weiche Nachfrage zum Angebot der ersten Mail („Falls du dir <das Angebot der ersten Mail>
    später doch ansehen möchtest, gib mir einfach kurz Bescheid.“), kein neues Angebot.
  - **D**, die Kampagne schreibt auch eine zweite Person der Firma an: „Ich hab mich auch bei
    <Vorname> gemeldet …“ und die Frage, wer von beiden zuständig ist.
- Namen nur aus belegter aktueller Firmenzugehörigkeit mit passender Rolle, nie die begrüßte Person,
  nie aus E-Mail-Adressen geraten.

## Die drei Fassungen des Prompts

Wörtlich aus der App (`api/config/campaign-templates/`, Stand v4.19.0). Im Blueprint steht der Text
als `prompt` der Variable `routing`, mit Zeilenumbrüchen als `\n` und `"` als `\"`.

### Deutsch, `salutation: "du"` (`prompts/shared/routing.md`)

```text
# AI Routing - Frage nach der richtigen Person

Du schreibst den Routing-Absatz der letzten Mail einer Cold-Mail-Sequenz (Abschied). Er steht als eigener Absatz nach dem festen Abschiedssatz und vor dem Gruß. Ansprache: Du-Form, du/dich/dein für die Person, nie Sie und nie ihr/euch als Anrede.

## Aufgabe

Erzeuge ausschließlich diesen Absatz, ohne Anrede, ohne Abschiedssatz und ohne Gruß, höchstens 35 Wörter. Beginne mit einem Großbuchstaben. Ton: locker wie eine kurze Rückfrage („not sure if I should be speaking to you or X or Y, let me know“), keine förmliche Zuständigkeitsabfrage.

Nutze hallo aus demselben Ergebnis (die begrüßte Person ist der Empfänger) und die Personen der Recherche unter „Team & Kontaktinformationen“, vor allem „Weitere Ansprechpartner“.

## Vier Fälle

Fall A, die Recherche belegt andere, aktuell beschäftigte Personen mit einer Rolle, die zum Angebot der Kampagne passt: „Ich bin mir nicht sicher, ob ich damit bei dir richtig bin oder eher bei <Vorname 1> oder <Vorname 2>. Gib mir gern kurz Bescheid.“ Bei nur einer passenden Person die zweite Alternative weglassen.

Fall B, keine belegten Alternativen und die Zuständigkeit ist unklar: exakt „Sag mir gern kurz Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte.“

Fall C, Einzelbetrieb, eindeutig zuständiger Empfänger oder der Recherche-Vermerk „Routing nicht sinnvoll“: keine künstliche Unsicherheit, stattdessen eine weiche Nachfrage zum Angebot der ersten Mail, etwa „Falls du dir <das Angebot der ersten Mail> später doch ansehen möchtest, gib mir einfach kurz Bescheid.“ Nur das, was die erste Mail schon anbietet: kein neues Angebot, kein neuer Aspekt. Hat die Kampagne Schwerpunkte, ist das Angebot der ersten Mail der für diesen Lead gewählte Schwerpunkt (wie ihn offer_text dieses Leads nennt), nie das Haupt-Offer, wenn ein anderer gewählt ist.

Fall D, die Kampagne schreibt auch eine zweite Person der Firma an (Block ZWEITE PERSON im Systemprompt): Nenne die jeweils andere angeschriebene Person nie als Alternative, sondern schreibe „Ich hab mich auch bei <Vorname> gemeldet …“ und frag, wer von euch beiden zuständig ist.

## Regeln

- Namen nur aus belegter aktueller Firmenzugehörigkeit mit passender Rolle, so geschrieben wie in der Recherche; nie die begrüßte Person selbst.
- Namen nie aus E-Mail-Adressen raten; eine Adresse wie anna@ belegt keine Person.
- Kein leerer Wert, keine Platzhalter, kein erneuter Pitch, keine Frist, keine Gedankenstriche.

**Schreibe jetzt nur den Routing-Absatz. Nichts danach.**
```

### Deutsch, `salutation: "sie"` (`prompts/shared/routing-sie.md`)

```text
# AI Routing - Frage nach der richtigen Person

Du schreibst den Routing-Absatz der letzten Mail einer Cold-Mail-Sequenz (Abschied). Er steht als eigener Absatz nach dem festen Abschiedssatz und vor dem Gruß. Ansprache: Sie-Form, Sie/Ihnen/Ihre, nie du/ihr.

## Aufgabe

Erzeuge ausschließlich diesen Absatz, ohne Anrede, ohne Abschiedssatz und ohne Gruß, höchstens 35 Wörter. Beginne mit einem Großbuchstaben. Ton: freundlich und kurz wie eine Rückfrage, keine förmliche Zuständigkeitsabfrage.

Nutze hallo aus demselben Ergebnis (die begrüßte Person ist der Empfänger) und die Personen der Recherche unter „Team & Kontaktinformationen“, vor allem „Weitere Ansprechpartner“.

## Vier Fälle

Fall A, die Recherche belegt andere, aktuell beschäftigte Personen mit einer Rolle, die zum Angebot der Kampagne passt: „Ich bin mir nicht sicher, ob ich damit bei Ihnen richtig bin oder eher bei <Vorname Nachname 1> oder <Vorname Nachname 2>. Geben Sie mir gern kurz Bescheid.“ Bei nur einer passenden Person die zweite Alternative weglassen. „Frau“ oder „Herr“ nur, wenn die Recherche die Person so nennt.

Fall B, keine belegten Alternativen und die Zuständigkeit ist unklar: exakt „Sagen Sie mir gern kurz Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte.“

Fall C, Einzelbetrieb, eindeutig zuständiger Empfänger oder der Recherche-Vermerk „Routing nicht sinnvoll“: keine künstliche Unsicherheit, stattdessen eine weiche Nachfrage zum Angebot der ersten Mail, etwa „Falls Sie sich <das Angebot der ersten Mail> später doch ansehen möchten, geben Sie mir einfach kurz Bescheid.“ Nur das, was die erste Mail schon anbietet: kein neues Angebot, kein neuer Aspekt. Hat die Kampagne Schwerpunkte, ist das Angebot der ersten Mail der für diesen Lead gewählte Schwerpunkt (wie ihn offer_text dieses Leads nennt), nie das Haupt-Offer, wenn ein anderer gewählt ist.

Fall D, die Kampagne schreibt auch eine zweite Person der Firma an (Block ZWEITE PERSON im Systemprompt): Nenne die jeweils andere angeschriebene Person nie als Alternative, sondern schreibe „Ich habe mich auch bei <Vorname Nachname> gemeldet …“ und frag, wer von Ihnen beiden zuständig ist. „Frau“ oder „Herr“ nur, wenn die Recherche die Person so nennt.

## Regeln

- Namen nur aus belegter aktueller Firmenzugehörigkeit mit passender Rolle, so geschrieben wie in der Recherche; nie die begrüßte Person selbst.
- Namen nie aus E-Mail-Adressen raten; eine Adresse wie anna@ belegt keine Person.
- Kein leerer Wert, keine Platzhalter, kein erneuter Pitch, keine Frist, keine Gedankenstriche.

**Schreibe jetzt nur den Routing-Absatz. Nichts danach.**
```

### Englisch (`en/prompts/shared/routing.md`)

```text
# AI Routing - Asking for the right person

You write the routing paragraph of the last email of a cold email sequence (the goodbye). It stands as a paragraph of its own after the fixed goodbye sentence and before the sign-off.

## Your task

Write only this paragraph, without greeting, goodbye sentence or sign-off, at most 35 words. Start with a capital letter. Tone: casual like a quick question ("not sure if I should be speaking to you or X or Y, let me know"), never a formal question about responsibilities.

Use hallo from the same result (the greeted person is the recipient) and the people the research lists under "Team & Kontaktinformationen", above all "Weitere Ansprechpartner".

## Four cases

Case A, the research shows other people currently working at the company in a role that fits the campaign's offer: "Not sure if you're the right person for this or if I should be talking to <first name 1> or <first name 2>. Just let me know." With only one fitting person, leave out the second option.

Case B, no documented alternatives and it is unclear who handles this: exactly "If someone else on your team handles this, just let me know and I'll reach out to them instead."

Case C, a one-person business, a recipient who clearly handles this, or the research note "Routing nicht sinnvoll": no artificial doubt; instead a soft question about the offer of the first email, such as "If you'd still like to see <the offer of the first email> later, just let me know." Only what the first email already offers: no new offer, no new angle. If the campaign has focuses, the offer of the first email is the focus chosen for this lead (as offer_text of this lead names it), never the main offer when another one is chosen.

Case D, the campaign also writes to a second person of the company (block SECOND PERSON in the system prompt): never name the other person who is written to as an alternative; write "I also reached out to <first name> …" and ask which of the two handles this.

## Rules

- Names only of people with documented current employment and a fitting role, written as in the research; never the greeted person.
- Never guess names from email addresses; an address like anna@ does not document a person.
- No empty value, no placeholders, no new pitch, no deadline, no dashes.

**Now write only the routing paragraph. Nothing after it.**
```

## Woher die Namen kommen

Die Recherche der App sucht die Personen selbst: Der Bericht trägt unter „Team &
Kontaktinformationen“ den Abschnitt „Weitere Ansprechpartner“ mit höchstens zwei Personen außer der
empfohlenen Kontaktperson (Name, Rolle, Quelle), sonst „Routing nicht sinnvoll“. Ein eigenes
Recherche-Ziel im `researchAgentConfig.additionalPrompt` ist dafür nicht nötig.

## Bestehende Kampagnen

Kampagnen, die noch einen festen Routing-Satz im Abschied tragen (angelegt bis outreach 0.8.0),
behalten ihn beim Bearbeiten, außer der Nutzer will umstellen. Dann Step 4 wie oben, die Variable
`routing` dazu, Vollersatz nach `outreach-campaign`, Phase 3.

## Erfahrungswerte

In einer Agentur-Kampagne mit über 400 generierten Leads verteilten sich die Werte auf etwa 20 % mit
Namen (Fall A), 20 % Team-Satz (Fall B) und 60 % Einzelbetrieb oder eindeutig zuständig (Fall C). Die
Quote von Fall A ist eine gute Kennzahl für die Recherche-Qualität.
