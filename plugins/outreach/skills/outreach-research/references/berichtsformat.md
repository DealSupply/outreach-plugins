# Berichtsformat der Recherche (wie der Server)

Wortlaut aus `LeadResearchPromptBuilder::reportFormat()` von DealSupply (MCP 4.16.0). Der Server-Lauf schreibt
jeden Recherchebericht genau so. Der Bericht gilt kampagnenübergreifend, also auch für spätere Server-Läufe und
andere Kampagnen. Darum schreiben Abo-Lauf und Manuell-Modus dasselbe Format, mit allen Abschnitten in dieser
Reihenfolge und den Überschriften wörtlich.

Diese Abschnitte liest der Server später maschinell, sie sind Pflicht:

- `# Recherche-Bericht` (Titel) und die Zeile `**Bester Anker:**`: ohne beide gilt der Bericht als unvollständig.
- `## WEBSITE-BEFUND` mit allen acht Zeilen und nur den vorgegebenen Werten (`ja (…)`, `nein (…)`,
  `nur Anfrageformular (…)`, `nur Telefon oder Mail (…)`, `nur Sammelseite (…)`, `unklar (…)`). Daraus wählen
  „Angebot je Lead“ und die Schwerpunkt-Prüfung das Angebot und der Chance-Winkel seine Beobachtung.
- `## BEWERTUNGEN EXTERN`
- `## Stärkste Anker für einen Opener` mit drei nummerierten Einträgen und `**Bester Anker:**`: Daraus nehmen
  Intro-Varianten ihren Anker (`rueckfall_trotz_anker` misst daran).
- `### Weitere Ansprechpartner` (höchstens zwei Personen oder genau eine Zeile „Routing nicht sinnvoll“):
  Daraus schreibt die Variable `routing` ihre Fälle.

„Anker-Regeln oben“ und „RANGFOLGE DER ANKER“ meinen `researchGeneration.anchorRules` aus `get_lead_data`.
Die eckigen Klammern sind Platzhalter: durch belegte Inhalte ersetzen, nie stehen lassen. Fehlt ein Wert,
steht dort, was die Vorlage dafür vorsieht („nicht festgestellt“, „keine Hinweise gefunden“, „unklar (Grund)“,
„keine“).

```markdown
# Recherche-Bericht

**Firma:** [Name] · **Website:** [URL] · **Stadt:** [Stadt] · **Analysiert:** [Heute]

## Unternehmen im Überblick

**Geschäftsmodell:** [B2B/B2C/SaaS/Agentur/etc.] · **Unternehmensgröße:** [Einzelunternehmen/Klein/Mittel/Groß + Details] · **Positionierung:** [Budget/Standard/Premium]
**Hauptleistungen:** [Liste] · **Zielgruppe:** [Wer sind deren Kunden?]
**Besonderheiten:** [was sie laut Quelle besonders macht, als Tatsache, ohne Vergleich mit anderen Betrieben]

## Eigentümer & Zugehörigkeit

**Inhaber/Träger:** [wer betreibt das Unternehmen, mit Quelle — oder "nicht festgestellt"]
**Gruppen-, Konzern- oder Franchise-Zugehörigkeit:** [belegte Fakten mit Quelle — oder "keine Hinweise gefunden"]
**Standorte:** [Anzahl und wer sie betreibt]
**Art und Größe des Betriebs:** [Tatsachen mit Quelle, z. B. "Einzelpraxis mit drei Behandlerinnen", "GmbH mit rund 40 Mitarbeitenden", "eigene Behandlungen vor Ort, kein Onlineshop"; als Aussage über die Firma, nie als Liste der Kriterien einer Kampagne]

## WEBSITE-BEFUND

- Gelesene Seiten: [URLs der gelesenen Seiten der eigenen Website]
- Bewertungen oder Kundenstimmen auf der Website: [ja (Seite, wörtliches Zitat) | nein (geprüfte Seiten) | unklar (Grund)]
- Online-Buchung oder Terminbuchung: [ja (Buchungsmaschine) (Anbieter oder Link) | nur Anfrageformular (Seite) | nur Telefon oder Mail (Seite) | unklar (Grund)]
- Kontakt- oder Anfrageformular: [ja (Seite) | nein (geprüfte Seiten) | unklar (Grund)]
- Eigene Seiten zu einzelnen Projekten oder Referenzen: [ja (URL einer Projektseite) | nur Sammelseite (URL) | nein (geprüfte Seiten) | unklar (Grund)]
- Karriere- oder Stellenseite: [ja (Seite) | nein (geprüfte Seiten) | unklar (Grund)]
- Galerie oder Vorher-Nachher-Bilder: [ja (Seite, Galerie oder Vorher-Nachher) | nein (geprüfte Seiten) | unklar (Grund)]
- Vertriebsrollen im Team genannt: [ja (Seite, Rolle) | nein (geprüfte Seiten) | unklar (Grund)]

## BEWERTUNGEN EXTERN

- [Plattform]: [Anzahl] Bewertungen, Schnitt [Wert] [Quellentyp-Tag]; [bis zu 3 Inhalte: „Zitat oder Paraphrase“ (Monat/Jahr, URL)]
- [oder genau eine Zeile: keine gefunden (gesucht: Plattformen bzw. Suchanfrage); ohne Websuche: keine gefunden (nicht gesucht)]

## Stärkste Anker für einen Opener

1. [Stärkster positiver Anker als schlichte Tatsache wie in den Anker-Regeln oben, mit Inhalt (was gelobt/ausgezeichnet wird), Quelle und Quellentyp-Tag; Zahlen nur als Stütze; bei Kundenlob je Thema die Zählung der Rezensionen; keine Abwägung, ob er trägt]
2. [Zweiter Anker zu einem anderen Gegenstand als 1 (anderes Projekt, andere Behandlung, andere Kundenstimme), gleiche Regeln]
3. [Dritter Anker zu einem dritten Gegenstand, gleiche Regeln; gibt es keinen: "Kein weiterer belegter Anker"]

**Bester Anker:** [Nummer] ([wenige Worte, was die Firma an dieser Stelle auszeichnet, z. B. "eigenes Kronen-Konzept mit Namen"; gewählt nach den Regeln oben, ohne sie zu nennen]) — oder "kein starker Anker gefunden" ohne Begründung

## Team & Kontaktinformationen

### Geschäftsführung & Entscheidungsträger
**[Name wie auf der Quelle, mit Titel; Herr/Frau nur, wenn die Quelle es schreibt, nie aus dem Vornamen ergänzt]** — Position: [Position] · E-Mail: [Email oder "Nicht persönlich gefunden"] · Gefunden: [Impressum/Team-Seite/etc.]
[Weitere Entscheider falls gefunden]

### Weitere Ansprechpartner
**[Name wie auf der Quelle]** · Rolle: [Rolle oder Zuständigkeit wie auf der Quelle] · Quelle: [URL]
[höchstens zwei Personen außer der empfohlenen Kontaktperson, je eine Zeile; sonst genau eine Zeile "Routing nicht sinnvoll" mit kurzem Grund, z. B. "(Einzelbetrieb)"]

### Allgemeine Kontakte
**Allgemeine E-Mail:** [email] · **Telefon:** [nummer falls gefunden] · **Kontaktformular:** [Ja/Nein] · **Terminbuchung:** [Link, auch auf fremdem Host oder Anbieter-Subdomain; sonst "Nein"] · **Social Media:** [LinkedIn, etc. falls gefunden]

### Empfohlener Kontakt
**Empfohlene Kontaktperson:** [Name] · **Empfohlene E-Mail:** [email] · **Begründung:** [Warum diese Person/Email?]

## Konkrete Funde

Bis zu 5 Funde in dieser Form, nach dem Rang der RANGFOLGE DER ANKER geordnet (Fund 1 ist der stärkste):
### Fund [N]: [Aussagekräftiger Titel]
**Wo gefunden:** [URL oder Seitenname] · **Details:** [Was genau, mit konkretem Kontext]
**Anker:** [Anker-Satz als schlichte Tatsache wie in den Anker-Regeln oben, mit Quellentyp-Tag bei Zahlen]

## Aktivitäts-Signale

**Content-Aktivität:** [Sehr aktiv/Aktiv/Mäßig/Inaktiv + Details, z. B. "Blog bis März 2025"] · **Wachstum:** [Expansion, neue Mitarbeiter, Services]
**Aktualität:** [Website-Stand, Copyright-Jahr] · **Engagement:** [Google Rating, Social Media]

## Kommunikations-Empfehlung

**Ton auf Website:** [Formal/Locker/Technisch/Freundlich/etc.]
**Zu vermeiden:** [was in einer Nachricht an diese Firma unpassend wäre, aus ihrer Sicht: falsche Branchenbegriffe, sensible Themen; keine Regeln der Kampagne]

## Recherche-Details

**Besuchte URLs:**
- [URL 1, exakt wie abgerufen, ohne Zusatz]
- [...]
**Nicht erreichbar (Abruf gescheitert oder blockiert):** [URLs — oder "keine"]
**Websuchen:** [die tatsächlich verwendeten Suchwörter, sonst "keine"]
**Offene Fragen:** [was über die Firma offen bleibt, als Frage über die Firma]
```
