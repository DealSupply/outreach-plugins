# Research-Fokus formulieren — Anker für die Personalisierung

> Der Research-Agent sammelt, womit der E-Mail-Agent den Opener baut. Ein guter Research-Fokus
> beschreibt ANKER, keine Datenfelder.

## Die Anker-Hierarchie (Server kennt sie — dein Fokus verstärkt sie fürs Angebot)

Maßgeblich ist der Abschnitt „Abhebung und Austauschtest“ in `outreach-copy` →
`references/copy-lehre.md`. Für die Recherche heißt das:

1. **Lob aus Bewertungstexten** (bester Anker, immer zuerst recherchieren): Google-Bewertungen über
   Bewertungsportale und Verzeichnisse, Trusted Shops, Shop-Bewertungen. Konkrete paraphrasierbare
   Aussagen über DIESEN Betrieb (was genau gelobt wird, wie viele Bewertungen dieses Lob tragen).
2. **Abhebendes Detail von der Website**: eigener Name oder eigenes Konzept, ungewöhnliche Zeit oder
   Zahl, eigenes Verfahren, seltene Spezialisierung, Auszeichnung. Auch Stellenanzeigen/Wachstum:
   festhalten, was die Anzeige über den Betrieb verrät (Wachstum, Spezialisierung, Projekt), nicht
   nur dass gesucht wird.
3. **Anzahl und Schnitt der Bewertungen** als eigener Anker, nur bei mindestens 30 Bewertungen und
   einem Schnitt ab 4,5; darunter trägt die Zahl keinen Anker. Werte aus
   dem Import (Google-Profil in den Lead-Attributen) gelten als Quelle; widersprechen sich Quellen,
   den kleineren Wert notieren.
4. **Fallback der Kampagne** (Branche/Region): steht im `intro`-Prompt, nicht in der Recherche.

**Austauschtest:** Ein Fund, der auf zehn andere Betriebe derselben Branche in der Stadt passt, ist
kein Anker, auch nicht mit Nutzen („digital scannen, hilft bei Würgereiz“).

**Sperrliste je Kampagne (Pflicht):** Leite aus Branche und Zielgruppe die branchenüblichen
Leistungen ab, die keinen Opener tragen (meist 6 bis 10 Begriffe: was steht bei fast jedem Betrieb
dieser Branche auf der Leistungsseite?). Sie steht gleichlautend im
`researchAgentConfig.additionalPrompt` UND im `intro`-Prompt. Beispiel Dental: Angstpatienten,
Lachgas, Sedierung/Narkose, Kinderbehandlung, Notdienst, Prophylaxe/Dentalhygiene, digitaler
Scan/Abdruck, Implantate allgemein. Ein gesperrtes Thema zählt nur als Lob aus Bewertungstexten.

Anker sind POSITIV verwendbar (der Opener ist ein Lob). Schmerzpunkte und Lücken sind trotzdem
wertvoll — für die Qualifizierung, für `pain_point`-Variablen und die Kontakt-Empfehlung — aber
sie gehören NIE in den Opener-Anker.

## So formulierst du `researchAgentConfig` / Frage 9 des Guides

Konkret aufs Angebot gemünzt, 3–5 Punkte. Beispiel (Webdesign/SEO an Handwerk):

```
Pro Lead herausfinden:
1. Zuerst die Bewertungen: ein zitierfähiges Kundenlob über DIESEN Betrieb und wie viele Bewertungen
   es tragen (Treffer von Bewertungsportalen öffnen); dazu Anzahl und Schnitt mit Quelle,
   Import-Werte aus den Lead-Attributen gelten. Bester Opener-Anker.
2. Was den Betrieb von anderen seiner Branche abhebt (eigenes Verfahren wie ein 3D-Rundgang vor der
   Badsanierung, ungewöhnliche Zeiten, seltene Spezialisierung, Auszeichnung). Austauschtest: passt
   der Fund auf zehn andere Betriebe der Stadt, ist er kein Anker.
3. Zustand des Web-Auftritts sachlich: Alter/Technik der Website, lokale Auffindbarkeit
   (für Qualifizierung und pain_point - NICHT für den Opener).
4. Entscheider mit Vornamen und Rolle (Impressum/Team-Seite), inkl. Quelle; bei generischen Adressen
   wie info@ ist er die Person für die Anrede.
5. Region/Einzugsgebiet, falls das Offer regional argumentiert.
Sperrliste (nie als Opener-Anker vormerken, außer als Lob aus Bewertungstexten): Badsanierung,
Heizungstausch, Wärmepumpe allgemein, Notdienst, barrierefreies Bad, Meisterbetrieb, Beratung vor Ort.
```

Die eigene Kontaktadresse eines Leads, der ohne E-Mail importiert wurde (ab ListM8 MCP 3.0.0), muss
nicht in den Fokus-Text: Die Regeln dafür bringt der Server selbst mit (`researchGeneration.contactEmail`
in `get_lead_data`). Ein Punkt „Kontaktadresse“ im Fokus-Text ist nur eine Gedächtnisstütze; maßgeblich
bleiben die Regeln des Servers (persönliche Adresse von Inhaber oder Geschäftsführung vor info@, nie
geraten, nie Plattform-, Verzeichnis- oder Agenturadressen).

## Recherche-Stufe (`researchAgentConfig.researchTier`)

Wie viel der Agent im Netz sucht, steht nicht im Fokus-Text, sondern in der Stufe: `basis` (nur Website
und importierte Daten, Bewertungszahlen aus dem Import), `smart` (danach höchstens eine Bewertungssuche,
wenn kein starker Anker belegt ist) oder `deep` (Websuche nach Bedarf, auch Presse, Verzeichnisse,
Register). Der Schlüssel ist optional; ohne ihn gilt die Stufe des Kontos (neue Konten Smart). Nur
setzen, wenn der User es für diese Kampagne will, z. B. `deep` für größere B2B-Unternehmen. „Zuerst die
Bewertungen“ im Fokus wirkt bei Basis und Smart über die Import-Werte und die eine Smart-Suche, nicht
über zusätzliche Suchen.

## Anti-Muster

- „Alles über die Firma herausfinden" — der Agent verbrennt Budget auf Irrelevantem.
- Nur Defizite suchen lassen — dann gibt es keinen Lob-Anker und der Opener wird generisch.
- Fakten verlangen, die Websites fast nie zeigen (Umsatz, Marge) — erzeugt Halluzinationsdruck;
  der Server verbietet Erfundenes, also kommt dann schlicht nichts.
- Mehr als 5 Punkte — Priorität schlägt Vollständigkeit (die Sperrliste zählt nicht mit).
- Standardleistungen als Anker verlangen („Spezialisierung: Angstpatienten, Implantate?“): Dann
  beginnen alle Opener gleich. Was jeder anbietet, gehört auf die Sperrliste.
