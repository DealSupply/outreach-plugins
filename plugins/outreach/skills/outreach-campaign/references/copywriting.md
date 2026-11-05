# Copywriting — siehe Skill `outreach-copy`

Die Copy-Regeln für Kampagnen stehen ausschließlich im Skill `outreach-copy`
(Skill `outreach-copy`). Er ist vor jeder Zeile Sequenz oder Variablen-Prompt
VERBINDLICH zu laden. Hier steht bewusst keine zweite Fassung.

Dort zu finden:

- Offer-Karten A-E mit den festen Überleitungen, Marketing-Offer-Regeln, verbotene Offer-Begriffe
- Anatomie der Entry-Mail: `{{ai.hallo}}` → `{{ai.intro}}` → Überleitung + Offer →
  zweiter Satz zum Angebot (C Feinheiten-Satz, A/B `{{ai.angebot_ausfuehrung}}` je Lead, D/E keiner)
  → EIN Frage-CTA → Klartext-Signatur
- 4er-Sequenz (`delayDays` 0/3/5/7, max. 120/50/80/60 Wörter; Step 2 bis 4 ohne Betreff im Thread von Step 1, Step 4 Abschied mit Routing-Hinweis), Betreffzeilen
- Anrede je `emailAgentConfig.salutation` (`du` Standard im Singular, `sie` nur gewählt je Kampagne; keine Team-Form), Vornamen über den `hallo`-Prompt
  statt Platzhalter, erlaubte Platzhalter (`{{ai.*}}`, `{{lead.company}}`, `{{lead.website}}`,
  `{{lead.city}}`, `{{custom.*}}`)
- Pflichtinhalt der Prompts von `hallo`, `intro` und `angebot_ausfuehrung`, Intro-Regeln mit Fallback-Satz
- Verbote, Spam-Wörter, „kostenlos“-Regel, Selbstprüfung und Prüfliste
- `references/copy-lehre.md`, `references/marketing-offer.md`,
  `references/beispiel-blueprint.md` (vollständiger Blueprint)
