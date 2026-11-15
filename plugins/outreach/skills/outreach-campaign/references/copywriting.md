# Copywriting — siehe Skill `outreach-copy`

Die Copy-Regeln für Kampagnen stehen ausschließlich im Skill `outreach-copy`
(Skill `outreach-copy`). Er ist vor jeder Zeile Sequenz oder Variablen-Prompt
VERBINDLICH zu laden. Hier steht bewusst keine zweite Fassung.

Dort zu finden:

- Offer-Karten A-E mit den festen Überleitungen, Marketing-Offer-Regeln, verbotene Offer-Begriffe
- Anatomie der Entry-Mail: `{{ai.hallo}}` → `{{ai.intro}}` → Überleitung + Offer →
  zweiter Satz zum Angebot (A/B/C der feste Satz der Karte, D/E keiner)
  → EIN Frage-CTA → „Viele Grüße“ mit `{{accountSignature}}`, jeder Baustein ein eigener Absatz
- 4er-Sequenz (`delayDays` 0/3/5/7, max. 120/50/80/60 Wörter; Step 2 bis 4 ohne Betreff im Thread von Step 1, Step 4 Abschied mit `{{ai.routing}}`), Betreffzeilen
- Anrede je `emailAgentConfig.salutation` (`du` Standard im Singular, `sie` nur gewählt je Kampagne; keine Team-Form), Vornamen über den `hallo`-Prompt
  statt Platzhalter, erlaubte Platzhalter (`{{ai.*}}`, `{{lead.company}}`, `{{lead.website}}`,
  `{{lead.city}}`, `{{custom.*}}`, im Body `{{accountSignature}}`)
- Prompts von `hallo`, `intro` (nur Kampagnenspezifisches) und `routing` (wörtlich aus dem Guide), Intro-Regeln mit Ersatzsatz
- für Erfahrene: Tests in Mail 1 und „Angebot je Lead“ (`references/fuer-erfahrene.md`)
- Verbote, Spam-Wörter, „kostenlos“-Regel, Selbstprüfung und Prüfliste
- `references/copy-lehre.md`, `references/marketing-offer.md`,
  `references/beispiel-blueprint.md` (vollständiger Blueprint), `references/fuer-erfahrene.md`,
  `references/routing-baustein.md`
