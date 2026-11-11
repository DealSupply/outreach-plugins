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
- Prompt: wörtlich der ROUTING-PROMPT aus dem MCP-Prompt `campaign_blueprint_guide`. Deutsche
  Kampagnen nehmen die Fassung zur `salutation` (Du oder Sie), englische die eine englische Fassung.
  Nicht selbst formulieren, nicht kürzen, keine angebotsbezogenen Stellen einsetzen: Das Angebot der
  ersten Mail kennt der Prompt aus der Kampagne. Ist der Guide nicht greifbar, `routing` mit dem
  Prompt einer bestehenden Kampagne aus `export_campaign_blueprint` übernehmen, nie aus dem
  Gedächtnis.
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
