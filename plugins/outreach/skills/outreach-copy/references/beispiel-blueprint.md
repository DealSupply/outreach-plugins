# Beispiel-Blueprint — vollständig ausformulierte Kampagne

> Referenz zu `outreach-copy`. Ein fiktiver Absender (Jonas Weber, Weber Webdesign) mit
> erfundenen Belegen; Namen und Zahlen stehen hier nur, weil sie in diesem Beispiel die
> „Angaben des Nutzers“ sind. In einer echten Kampagne kommt jede Zahl, jeder Name und jede
> Kapazitätsangabe vom Nutzer. Name, Rolle und Firma des Absenders stehen nicht im Mailtext: Jede
> Mail endet mit `{{accountSignature}}`, die Instantly mit der Signatur des Versandpostfachs füllt.

Schema v1, wie `create_campaign(blueprint=…)` es erwartet (geprüft gegen den
Blueprint-Validator von DealSupply: `schemaVersion` 1, `campaign.name` 3-255 Zeichen, `campaign.language` `de` oder `en` (optional, ab MCP 4.7.0, Standard `de`), Config-Blöcke
als Objekte, `salutation` ∈ `du`/`sie` (der Server nimmt noch `team` an, der Skill setzt es nie), Variablennamen `^[a-zA-Z][a-zA-Z0-9_]*$` und
eindeutig, Prompt ≥ 10 Zeichen, `subject` in Step 1 nicht leer und ab Step 2 leer erlaubt (Thread), `delayDays` ganze Zahl ≥ 0,
`delayUnit` `days` oder `hours`, max. 25 Variablen und 25 Steps).

## Die Entscheidungen in diesem Beispiel

| Punkt | Wahl | Warum |
|---|---|---|
| Offer-Karte | C: Konkretes Deliverable (Reziprozität) | der Entwurf ist je Praxis mit KI in 5 bis 10 Minuten bis morgen lieferbar (Empfehlungsregel der App: dann C, sonst A) |
| Marketing-Offer | fertiger Entwurf der neuen Startseite inklusive Online-Terminbuchungs-Flow | Deliverable, kein Gespräch; vom Nutzer lieferbar |
| Zweiter Satz zum Angebot | der feste Satz der Karte C: „Ich bin gerade noch an den letzten Feinheiten dran.“ | Standard seit 10.11.2026 wie in der App: für alle Leads gleich, als Text im Body, eigener Absatz zwischen Angebotssatz und Schlussfrage; das „morgen“ steht im Schlusssatz. Karte A und B siehe „Variante Karte A und B“ unten |
| Für Erfahrene | keine Tests, ein Angebot für alle | Standard; Tests und „Angebot je Lead“ nur auf Wunsch, siehe „Für Erfahrene“ unten |
| Schlusssatz | „Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“ | Standard bei Karte C, ohne „Link“ |
| Sprache | `language: "de"` | deutschsprachige Praxen; eine englische Kampagne hat eigene Regeln (`outreach-copy`, Abschnitt „Kampagnensprache“) |
| Ansprache | `salutation: "du"`: „Hallo Vorname,“ (Person der Versandadresse, bei info@ o. Ä. der Inhaber aus der Recherche), Fallback „Hallo,“, durchgehend du/dir/dein | Du-Form, eine Person (Inhaberin/Inhaber) |
| Betreffs | Step 1 „kurze Frage“, Step 2, 3 und 4 leer | Entwurfs-Angebot (Karte C): Frage statt Ankündigung; Step 2 bis 4 antworten im Thread von Mail 1 |
| Sequenz | 4 Steps, `delayDays` 0/3/5/7 | Standard; Step 3 ist der neue Winkel mit dem Beleg als Ich-Satz, Step 4 der Abschied der App mit `{{ai.routing}}`; ohne echten Zeit- oder Kapazitätsgrund des Nutzers keine Dringlichkeits-Mail |
| Variablen | `hallo`, `intro`, `routing` | wie die App; der `intro`-Prompt trägt nur Kontext, Sperrliste und Ersatzsatz (die Opener-Regeln gibt der Server), der `routing`-Prompt ist wörtlich die Du-Fassung der App (`routing-baustein.md`, „Die drei Fassungen“; hier als Platzhalter gezeigt, beim Anlegen den echten Text einsetzen) |
| Signatur | „Viele Grüße“, darunter `{{accountSignature}}` | wie die App; keine Unterschrift mit Name, Rolle oder Firma im Mailtext |
| Sperrliste | Angstpatienten, Lachgas, Sedierung/Narkose, Kinderbehandlung, Notdienst, Prophylaxe/Dentalhygiene, digitaler Scan/Abdruck, Implantate allgemein; für Beauty und Dermatologie Botox/Hyaluron, Microneedling, Laser-Haarentfernung | branchenübliche Leistungen tragen keinen Opener (Austauschtest); steht gleichlautend in `researchAgentConfig.additionalPrompt` und im `intro`-Prompt |
| Wörter (fester Text ohne Signatur) | 41 / 23 / 37 / 20 | Step 1 mit Anrede und Bezug (bis 2 Sätze, höchstens 30 Wörter) etwa 70, unter 120; Step 4 mit dem Routing-Absatz (höchstens 35) unter 60 |

## Blueprint

```json
{
  "schemaVersion": 1,
  "campaign": {
    "name": "Praxis-Relaunch: Startseiten-Entwurf für ästhetische Praxen",
    "language": "de",
    "intelligence": {
      "version": 1,
      "campaign_brief": {
        "business": {
          "value": "Weber Webdesign, Ein-Mann-Studio von Jonas Weber, baut Websites für ästhetische Praxen: Praxis-Relaunch in sechs Wochen nach einem eigenen Conversion-Framework mit Vorher-Nachher-Strecken, Behandlerprofilen, Social Proof und Online-Terminbuchung als einzigem Call-to-Action. Verkauft wird kein Webdesign, sondern planbare Beratungstermine über die Website.",
          "source": "answer",
          "status": "confirmed"
        },
        "target_audience": {
          "value": "Inhabergeführte ästhetische Praxen im DACH-Raum: Zahnärzte mit Ästhetik-Fokus, Beauty- und Ästhetik-Studios, dermatologische Privatpraxen mit 5 bis 25 Mitarbeitenden und einer Website, die älter als vier Jahre ist. Termine laufen fast nur übers Telefon, die Rezeption verliert Anfragen in der Sprechstunde. Klinikketten und Franchise-Gruppen sind ausgeschlossen.",
          "source": "answer",
          "status": "confirmed"
        },
        "usp": {
          "value": [
            "Fünf Jahre Healthcare-Agenturerfahrung und über 40 Projekte, darunter Zahnarztpraxen und Beauty-Studios",
            "Conversion-Framework statt Template: Vertrauensbeweise nach vorn, Online-Terminbuchung als einziger Call-to-Action",
            "Sicherheit bei DSGVO und Heilmittelwerbegesetz, DSGVO-sicheres Hosting",
            "Harte Zahlen als Beleg: verdreifachte Online-Terminanfragen bei Praxis Dr. Sommer in vier Monaten, 60 Prozent höhere Buchungsquote beim Beauty-Studio Glow",
            "Nachbesserungs-Versprechen: messbar mehr Beratungsanfragen innerhalb von 90 Tagen nach Go-Live, sonst kostenlose Nacharbeit"
          ],
          "source": "answer",
          "status": "confirmed"
        },
        "tone": {
          "value": "direct_personal",
          "source": "answer",
          "status": "confirmed"
        }
      },
      "offer_contract": {
        "title": {
          "value": "Fertiger Entwurf der neuen Startseite inklusive Online-Terminbuchungs-Flow",
          "source": "answer",
          "status": "confirmed"
        },
        "cta": {
          "value": "Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.",
          "source": "answer",
          "status": "confirmed"
        }
      }
    },
    "qualificationSettings": {
      "target_customer_profile": "Inhabergeführte ästhetische Praxis im DACH-Raum: Zahnarztpraxis mit Ästhetik-Fokus, Beauty- oder Ästhetik-Studio, dermatologische Privatpraxis. 5 bis 25 Mitarbeitende, ein oder zwei Standorte, Inhaber entscheidet selbst.",
      "offer_summary": "Praxis-Relaunch in sechs Wochen nach einem Conversion-Framework mit Online-Terminbuchung als einzigem Call-to-Action. Türöffner ist ein fertiger Entwurf der neuen Startseite inklusive Online-Terminbuchungs-Flow.",
      "fit_criteria": "Passt, wenn die Website sichtbar älter als vier Jahre ist, keine Online-Terminbuchung eingebunden ist und Termine über Telefon oder ein einfaches Kontaktformular laufen. Nachfrage ist da, sichtbar an Google-Bewertungen ab etwa 20 Rezensionen oder einem aktiven Instagram-Profil. Selbstzahler- oder Ästhetikleistungen sind erkennbar: dann höherer Fit, sonst mittlerer Fit.",
      "disqualifiers": "Klinikketten, Krankenhäuser, MVZ in Konzern- oder Investorenträgerschaft, Franchise-Gruppen und Praxisverbünde mit zentralem Marketing. Hersteller und Händler von Praxisbedarf, Ausbildungsinstitute. Praxen, deren eigene Website bereits ein Buchungstool wie Doctolib einbindet oder direkt darauf verlinkt. Praxen mit ausschließlich französisch- oder italienischsprachiger Website. Praxen, die eine Agentur als laufenden Betreuer im Impressum nennen. Einzelbehandler ohne Personal und Praxen mit über 25 Mitarbeitenden. Wettbewerber: Webdesign-Agenturen, Freelancer, Marketingagenturen, Praxis-Software-Anbieter. Firmen außerhalb Deutschland, Österreich, Schweiz.",
      "additional_prompt": "Ziel ist ein Beleg, dass die Praxis inhabergeführt ist und die Website älter als vier Jahre wirkt."
    },
    "researchAgentConfig": {
      "additionalPrompt": "Finde pro Praxis genau einen Anker für den Mail-Opener: etwas, das diese Praxis von anderen ihrer Branche abhebt und positiv verwendbar ist. Beginne immer mit den Bewertungen und prüfe in dieser Reihenfolge: 1) Bewertungstexte (Treffer von Bewertungsportalen und Verzeichnissen öffnen): was Patienten konkret über DIESE Praxis schreiben und wie viele Bewertungen dieses Lob tragen, 2) Website: EIN abhebendes Detail (eigenes Konzept oder eigener Name, ungewöhnliche Sprechzeiten, eigenes Verfahren, seltene Spezialisierung, Auszeichnung), auch Wachstum, ein neuer Behandler oder Standort aus einer Stellenanzeige (was die Anzeige über die Praxis verrät, nicht dass gesucht wird), 3) Anzahl und Schnitt der Bewertungen mit Quelle; Werte aus den Lead-Attributen des Imports (Google-Profil) gelten als Quelle, widersprechen sich Quellen, notiere den kleineren Wert. Austauschtest: Ein Fund, der auf zehn andere Praxen derselben Branche in der Stadt passt, ist kein Anker. Sperrliste (branchenübliche Leistungen, nie als Anker vormerken, außer als Lob aus Bewertungstexten): Angstpatienten, Lachgas, Sedierung oder Narkose, Kinderbehandlung, Notdienst, Prophylaxe und Dentalhygiene, digitaler Scan oder Abdruck, Implantate allgemein; bei Beauty-Studios und dermatologischen Praxen zusätzlich Faltenbehandlung mit Botox oder Hyaluron, Microneedling, Laser-Haarentfernung. Erfasse zusätzlich: Vorname der Inhaberin oder des Inhabers (bei einer generischen Praxisadresse wie info@ ist das die Person, an die die Mail gehen soll), ob eine Online-Terminbuchung eingebunden ist, wie alt die Website wirkt, Stadt. Notiere nur, was du wirklich auf der Website, in Bewertungsportalen, in Verzeichnissen oder in den Lead-Attributen siehst. Keine Vermutungen, keine erfundenen Zahlen.",
      "researchDepth": "quick",
      "researchPriorities": "Anzahl und Schnitt mit belegtem Lob (ab 30 Bewertungen und 4,5) > Lob aus Bewertungstexten > abhebendes Website-Detail (auch Wachstum/Stellenanzeige) > Anzahl und Schnitt allein > Ersatzsatz"
    },
    "emailAgentConfig": {
      "emailLanguage": "Deutsch (DACH)",
      "emailTone": "Direkt, knapp und menschlich in Du-Form, wie eine kurz getippte Nachricht von einem Selbstständigen an einen Praxisinhaber: kurze Sätze, kein Beratersprech, kein Werbeton, echtes Lob statt Kritik, ein klarer CTA.",
      "salutation": "du"
    }
  },
  "aiVariables": [
    {
      "name": "hallo",
      "prompt": "Erzeuge ausschließlich die Begrüßungszeile einer Cold-Mail an eine inhabergeführte ästhetische Praxis (Zahnarztpraxis mit Ästhetik-Fokus, Beauty-Studio, dermatologische Privatpraxis) im DACH-Raum. Absender ist Jonas Weber, Webdesigner für Praxis-Websites. Die Kampagne spricht die Person in Du-Form an.\n\nAufgabe: Gib genau eine Zeile aus, nichts weiter. Kein zweiter Satz, keine Einleitung, keine Erklärung.\n\nRegeln:\n- Angesprochen wird die Person, der die Versandadresse gehört: Geht aus dem Research oder aus einem Custom-Attribut mit dem Vornamen ihr Vorname klar hervor, schreibe \"Hallo <Vorname>,\".\n- Ist die Versandadresse generisch (zum Beispiel info@, kontakt@, praxis@), nimm den Vornamen der Inhaberin, des Inhabers oder der verantwortlichen Person, die der Research als Entscheider nennt, damit die Mail dort ankommt. Bei Personenmarken immer den Vornamen.\n- Wenn keine Person klar erkennbar ist, schreibe genau \"Hallo,\".\n- Niemals \"Hallo zusammen,\", \"Hallo <Praxisname> Team,\", \"Hallo Herr <Nachname>,\" oder \"Hallo Frau <Nachname>,\", keine Titel wie \"Dr.\": Die Mail ist in Du-Form geschrieben.\n- Die Zeile endet immer mit einem Komma.\n- Keine erfundenen Namen, keine Rollen erfinden, keine Platzhalter in eckigen oder geschweiften Klammern, keine Gedankenstriche, keine Emojis.\n- Deutsche Rechtschreibung mit echten Umlauten und ß.",
      "sortOrder": 1
    },
    {
      "name": "intro",
      "prompt": "# Opener\n\nDie allgemeinen Opener-Regeln (Abhebung, Austauschtest, Anker-Reihenfolge, positiver Schluss, Einstieg, Anrede) bekommst du zur Laufzeit. Hier steht nur, was für diese Kampagne gilt.\n\n## Kontext\n\nDu schreibst den Opener einer Cold-E-Mail.\n\n- Absender: Weber Webdesign (Jonas Weber), Websites für inhabergeführte ästhetische Praxen\n- Angebot: ein fertiger Entwurf der neuen Startseite inklusive Online-Terminbuchung\n- Zielgruppe: inhabergeführte ästhetische Praxen im DACH-Raum (Zahnarztpraxen mit Ästhetik-Fokus, Beauty- und Ästhetik-Studios, dermatologische Privatpraxen)\n- Ansprache: du, die Person im Singular\n\nDein Text steht direkt unter der Anrede und wird im festen Mailtext mit dem Satz „Deswegen war ich so frei und habe dir einen kompletten Entwurf für eine neue Startseite erstellt, inklusive eingebautem Online-Terminbuchungs-Flow.“ fortgesetzt. Das Angebot, die Überleitung und der Stand der Arbeit stehen also im festen Text. Du nennst sie nicht und nimmst sie nicht vorweg.\n\nDies ist Email 1 von 4 der Sequenz.\n\n## Sperrliste\n\nAngstpatienten, Lachgas, Sedierung oder Narkose, Kinderbehandlung, Notdienst, Prophylaxe und Dentalhygiene, digitaler Scan oder Abdruck, Implantate allgemein; bei Beauty-Studios und dermatologischen Praxen zusätzlich Faltenbehandlung mit Botox oder Hyaluron, Microneedling, Laser-Haarentfernung. Diese Themen tragen keinen Opener, außer als Lob aus Bewertungstexten.\n\n## Ersatzsatz\n\nGibt die Recherche keinen Anker her, der den Austauschtest besteht, schreibe genau diesen Satz, ohne Einstieg und ohne Schluss (Branche und Region pro Lead aus den Lead-Daten einsetzen, nie als Klammer stehen lassen): \"als [Branche] in [Ort oder Region] bist du genau die Art Praxis, die ich suche.\"\n\n**Schreibe jetzt nur den Opener. Nichts danach.**",
      "sortOrder": 2
    },
    {
      "name": "routing",
      "prompt": "<Routing-Prompt der App, Du-Fassung aus routing-baustein.md, wörtlich>",
      "sortOrder": 3
    }
  ],
  "sequence": {
    "steps": [
      {
        "stepNumber": 1,
        "subject": "kurze Frage",
        "body": "{{ai.hallo}}\n\n{{ai.intro}}\n\nDeswegen war ich so frei und habe dir einen kompletten Entwurf für eine neue Startseite erstellt, inklusive eingebautem Online-Terminbuchungs-Flow.\n\nIch bin gerade noch an den letzten Feinheiten dran.\n\nWäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.\n\n\nViele Grüße\n{{accountSignature}}\n\nFalls das gerade kein Thema für dich ist, gib mir kurz Bescheid.",
        "delayDays": 0,
        "delayUnit": "days"
      },
      {
        "stepNumber": 2,
        "subject": "",
        "body": "{{ai.hallo}}\n\ndu hast sicher viel um die Ohren, ich wollte nur sichergehen, dass meine Mail bei dir angekommen ist.\n\nEin kurzes Ja reicht mir.\n\n\nViele Grüße\n{{accountSignature}}",
        "delayDays": 3,
        "delayUnit": "days"
      },
      {
        "stepNumber": 3,
        "subject": "",
        "body": "{{ai.hallo}}\n\nich habe die Website der Praxis Dr. Sommer neu aufgesetzt, danach haben sich ihre Online-Terminanfragen in vier Monaten verdreifacht.\n\nWäre es in Ordnung, wenn ich dir morgen den Entwurf für deine neue Startseite zusende? Völlig unverbindlich natürlich.\n\n\nViele Grüße\n{{accountSignature}}\n\nFalls das gerade kein Thema für dich ist, gib mir kurz Bescheid.",
        "delayDays": 5,
        "delayUnit": "days"
      },
      {
        "stepNumber": 4,
        "subject": "",
        "body": "{{ai.hallo}}\n\nda ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung.\n\n{{ai.routing}}\n\n\nViele Grüße\n{{accountSignature}}",
        "delayDays": 7,
        "delayUnit": "days"
      }
    ]
  }
}
```

## Variante Karte A und B: fester zweiter Satz

Wählt der Nutzer Karte A (kostenlose Teildienstleistung) oder B (Pilotprojekt), gibt es keinen
Feinheiten-Satz: Er behauptet Arbeit, die es vor der Antwort nicht gibt. Der zweite Satz ist der
feste Satz der Karte, als eigener Absatz direkt nach dem Angebotssatz, ohne KI-Variable. Gegenüber
dem Blueprint oben ändern sich drei Stellen gemeinsam:

1. Step 1 `body`: Angebotssatz der Karte, darunter der feste Satz der Karte, darunter der CTA der
   Karte, jeder als eigener Absatz.
2. `intro`-Prompt: Der feste Folgesatz unter „Kontext“ heißt „Genau deshalb bieten wir aktuell …“ (A)
   bzw. „Genau solche Praxen suchen wir gerade …“ (B) statt „Deswegen war ich so frei …“, und das
   Angebot ist kein fertig vorbereiteter Entwurf.
3. `offer_contract`: Titel und CTA der Karte; der Betreff von Step 1 bleibt „kurze Frage“. Step 3
   endet mit der Schlussfrage der Karte aus Step 1 (A: „Wäre es in Ordnung, wenn ich das auch für dich
   erstelle? Völlig unverbindlich natürlich.“, B: „Wärst du grundsätzlich offen dafür?“).

### Karte A

Step 1 `body`:

```json
"{{ai.hallo}}\n\n{{ai.intro}}\n\nGenau deshalb bieten wir aktuell für eine Handvoll Praxen im DACH-Raum einen kostenlosen Entwurf für eine neue Startseite mit Online-Terminbuchung an.\n\nDarin wäre alles genau auf euch zugeschnitten.\n\nWäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich natürlich.\n\n\nViele Grüße\n{{accountSignature}}\n\nFalls das gerade kein Thema für dich ist, gib mir kurz Bescheid."
```

### Karte B

Step 1 `body`:

```json
"{{ai.hallo}}\n\n{{ai.intro}}\n\nGenau solche Praxen suchen wir gerade. Wir starten ein Pilotprojekt für buchbare Praxis-Startseiten mit einer Handvoll Praxen im DACH-Raum.\n\nIm Pilot bekommt ihr das kostenlos, dafür bräuchten wir nur ehrliches Feedback.\n\nWärst du grundsätzlich offen dafür?\n\n\nViele Grüße\n{{accountSignature}}\n\nFalls das gerade kein Thema für dich ist, gib mir kurz Bescheid."
```

Die festen Sätze der Karten gelten wörtlich, auch in der Sie-Form („Darin wäre alles genau auf Sie
zugeschnitten.“, „Im Pilot bekommen Sie das kostenlos, dafür bräuchten wir nur ehrliches
Feedback.“; bei C gleich) und auf Englisch (`outreach-copy`, „Zweiter Satz zum Angebot“).

## Für Erfahrene: Tests und „Angebot je Lead“

Beides nur, wenn der Nutzer es auf die Frage „Für Erfahrene“ ausdrücklich wählt; Bau und Wortlaut
in `fuer-erfahrene.md`. Gegenüber dem Blueprint oben ändert sich:

- **Betreff-Test:** neue Variable `betreff_b` mit `"role": "subject_variant"` und dem Prompt des
  Servers, dazu in Step 1 `"variants": [{"subject": "{{ai.betreff_b}}", "body": <Body von Step 1 wörtlich>, "active": true}]`.
- **Intro-Test:** neue Variable `intro_b` (mit Betreff-Test `intro_c`) mit `"role": "intro_variant"`
  und dem Prompt von `intro`, dazu eine Variante mit Betreff „kurze Frage“ und dem Body von Step 1,
  in dem `{{ai.intro_b}}` bzw. `{{ai.intro_c}}` statt `{{ai.intro}}` steht.
- **„Angebot je Lead“ (Karte A und C):** `campaign.station` mit den Antworten der Karten, in Step 1
  `{{ai.offer_text}}\n\n{{ai.angebot_ausfuehrung}}\n\n{{ai.offer_cta}}` statt Angebotssatz, festem
  Satz und Schlussfrage, die drei Variablen `offer_text`, `angebot_ausfuehrung` (die Anweisung nach
  der Vorlage, DealSupply baut sie beim Import selbst) und `offer_cta`, und Step 3 endet mit „Melde dich gerne, wenn das Thema für dich relevant
  ist.“ statt mit der Schlussfrage. Vollständiges Beispiel mit diesem Absender:
  `fuer-erfahrene.md`, Teil 2.

## Variante der Ansprache: Sie

Standard ist `du` im Singular. Ohne benennbaren Ansprechpartner lautet der Gruß „Hallo,“ und der
Text bleibt im Singular („dein Team“, „deine Praxis“); eine Ihr- oder Team-Form gibt es nicht. Nur
wenn der Nutzer die Kampagne siezen will (Kampagnen an sehr große Unternehmen), ändert man drei
Stellen gemeinsam: `emailAgentConfig.salutation`, die Format-Regeln im `hallo`-Prompt und die
Pronomen im festen Sequenztext (inklusive `offer_contract.cta` und der Zeile „Ansprache“ im
`intro`-Prompt) und die Fassung des `routing`-Prompts (Sie-Fassung, `routing-baustein.md`).

| `salutation` | `hallo`-Regel im Prompt | fester Text, Beispiel Step 1 |
|---|---|---|
| `sie` | „Hallo Frau <Nachname>,“ / „Hallo Herr <Nachname>,“ (Frau/Herr nur, wenn belegt, sonst „Guten Tag <Vorname> <Nachname>,“), keine Titel; Fallback „Guten Tag,“ | „Deswegen war ich so frei und habe Ihnen einen kompletten Entwurf … erstellt …“ / „Wäre es in Ordnung, wenn ich es Ihnen morgen zusende? Völlig unverbindlich natürlich.“ |

Nie „Hallo Herr/Frau …“ zusammen mit Du-Text.

## Optional: Kurzname `firma`

Führt die Kampagne nach `outreach-campaign` den Kurznamen als AI-Variable `firma`, kommt sie
dazu (Reihenfolge `hallo`, `firma`, `intro`, `sortOrder` 1-3; mit „Angebot je Lead“ danach `offer_text`, `angebot_ausfuehrung`, `offer_cta`; `routing` zuletzt). Der Betreff
von Step 1 bleibt bei jeder Karte „kurze Frage“; einen Firmennamen im Betreff gibt es nur über den
Betreff-Test (Variante B mit `betreff_b`, `fuer-erfahrene.md`), nie als rohes `{{lead.company}}`. Im
Text steht `{{ai.firma}}` statt `{{lead.company}}`. Am Copy-Regelwerk ändert das nichts.
