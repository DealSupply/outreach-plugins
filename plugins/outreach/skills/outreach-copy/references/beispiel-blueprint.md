# Beispiel-Blueprint — vollständig ausformulierte Kampagne

> Referenz zu `outreach-copy`. Ein fiktiver Absender (Jonas Weber, Weber Webdesign) mit
> erfundenen Belegen; Namen und Zahlen stehen hier nur, weil sie in diesem Beispiel die
> „Angaben des Nutzers“ sind. In einer echten Kampagne kommt jede Zahl, jeder Name und jede
> Kapazitätsangabe vom Nutzer.

Schema v1, wie `create_campaign(blueprint=…)` es erwartet (geprüft gegen den
Blueprint-Validator von ListM8: `schemaVersion` 1, `campaign.name` 3-255 Zeichen, Config-Blöcke
als Objekte, `salutation` ∈ `du`/`sie` (der Server nimmt noch `team` an, der Skill setzt es nie), Variablennamen `^[a-zA-Z][a-zA-Z0-9_]*$` und
eindeutig, Prompt ≥ 10 Zeichen, `subject` in Step 1 nicht leer und ab Step 2 leer erlaubt (Thread), `delayDays` ganze Zahl ≥ 0,
`delayUnit` `days` oder `hours`, max. 25 Variablen und 25 Steps).

## Die Entscheidungen in diesem Beispiel

| Punkt | Wahl | Warum |
|---|---|---|
| Offer-Karte | C: Konkretes Deliverable (Reziprozität) | kleine Zielgruppe, hohe Reply Rate nötig |
| Marketing-Offer | fertiger Entwurf der neuen Startseite inklusive Online-Terminbuchungs-Flow | Deliverable, kein Gespräch; vom Nutzer lieferbar |
| Feinheiten-Satz | „Ich bin gerade noch an den letzten Feinheiten dran, vor allem daran, die Behandlungsseiten gleich für Google und KI-Suchmaschinen mitzudenken, und werde morgen mit dem Entwurf fertig.“ | Pflicht bei Karte C, eigener Absatz, genau ein On-Top-Detail |
| Ansprache | `salutation: "du"`: „Hallo Vorname,“ (Person der Versandadresse, bei info@ o. Ä. der Inhaber aus der Recherche), Fallback „Hallo,“, durchgehend du/dir/dein | Du-Form, eine Person (Inhaberin/Inhaber) |
| Betreffs | Step 1 „kurze Frage“, Step 3 „kurzes Update“, Step 2 und 4 leer | Entwurfs-Angebot (Karte C): Frage statt Ankündigung; Step 2 antwortet im Thread von Mail 1, Step 3 öffnet einen neuen Thread, Step 4 antwortet darin |
| Sequenz | 4 Steps, `delayDays` 0/3/5/7 | Standard; Step 3 ist der neue Winkel mit Social Proof, Step 4 der Abschied mit Routing-Hinweis; ohne echten Zeit- oder Kapazitätsgrund des Nutzers keine Dringlichkeits-Mail |
| Sperrliste | Angstpatienten, Lachgas, Sedierung/Narkose, Kinderbehandlung, Notdienst, Prophylaxe/Dentalhygiene, digitaler Scan/Abdruck, Implantate allgemein; für Beauty und Dermatologie Botox/Hyaluron, Microneedling, Laser-Haarentfernung | branchenübliche Leistungen tragen keinen Opener (Austauschtest); steht gleichlautend in `researchAgentConfig.additionalPrompt` und im `intro`-Prompt |
| Wörter (fester Text ohne Signatur) | 57 / 23 / 72 / 55 | Step 1 mit Anrede und Bezug (bis 2 Sätze) etwa 85-95, unter 120 |

## Blueprint

```json
{
  "schemaVersion": 1,
  "campaign": {
    "name": "Praxis-Relaunch: Startseiten-Entwurf für ästhetische Praxen",
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
          "value": "Wäre es in Ordnung, wenn ich dir das zusende? Völlig unverbindlich natürlich.",
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
      "researchPriorities": "Lob aus Bewertungstexten > abhebendes Website-Detail (auch Wachstum/Stellenanzeige) > Anzahl und Schnitt der Bewertungen (ab 30 Bewertungen und 4,5) > Fallback"
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
      "prompt": "Du schreibst den Opener einer Cold-Mail. Absender ist Jonas Weber, selbstständiger Webdesigner, der Websites für inhabergeführte ästhetische Praxen baut (Zahnärzte mit Ästhetik-Fokus, Beauty-Studios, dermatologische Privatpraxen im DACH-Raum). Angeboten wird im weiteren Verlauf der Mail ein fertig vorbereiteter Entwurf einer neuen Startseite inklusive Online-Terminbuchung. Dein Text steht direkt unter der Anrede \"Hallo ...,\" und wird danach mit einem festen Satz fortgesetzt, der mit \"Deswegen war ich so frei ...\" beginnt.\n\nZiel: eine Beobachtung, die diese Praxis von anderen ihrer Branche abhebt und als Lob endet, damit der feste Satz danach einen Grund hat. Das kann nur jemand schreiben, der wirklich auf Website, Google-Profil oder Bewertungen war. Der Empfänger soll merken: hier hat sich jemand Mühe gemacht.\n\nAufgabe: Schreibe maximal 2 kurze Sätze, insgesamt etwa 30 Wörter. Beginne mit einem Kleinbuchstaben, weil dein Text direkt auf die Anrede mit Komma folgt; nur der erste Buchstabe ist klein, ein zweiter Satz beginnt groß. Schreibe inhaltlich über den Empfänger, nie über den Absender; Einstiegsrahmen wie \"ich hab mir ... angeschaut\" oder \"mir ist aufgefallen\" sind erlaubt und keine Selbstvorstellung. Ton: locker, authentisch, Du-Form im Singular (du, dein, dir, nie ihr, euch, Sie), wie eine kurze Nachricht an einen Bekannten. Der letzte Satz muss so enden, dass ein Satz mit \"Deswegen war ich so frei ...\" nahtlos anschließt, ohne dass du ein Problem, eine Lücke oder einen Bedarf benannt hast.\n\nWas abhebt: ein Eigenname oder eigenes Konzept, eine ungewöhnliche Sprechzeit oder Zahl, ein eigenes Verfahren, eine seltene Spezialisierung, eine Auszeichnung, ein Lob aus Bewertungen, auffällige Bewertungszahlen.\n\nAustauschtest: Passt dein Satz auf zehn andere Praxen derselben Branche in der Stadt, ist er kein Aufhänger. Dann nimm den nächsten Anker, zuletzt den Fallback. Ein Nutzen rettet keine Standardleistung. Dasselbe Thema besteht als Lob aus Bewertungstexten (was Patienten über DIESE Praxis schreiben), nicht als Zeile aus der Leistungsliste. Fällt durch: Lachgas für Angstpatienten. Besteht: ein eigenes Kronen-Konzept mit der Krone am selben Termin.\n\nSperrliste (branchenübliche Leistungen, die keinen Opener tragen, außer als Lob aus Bewertungstexten): Angstpatienten, Lachgas, Sedierung oder Narkose, Kinderbehandlung, Notdienst, Prophylaxe und Dentalhygiene, digitaler Scan oder Abdruck, Implantate allgemein; bei Beauty-Studios und dermatologischen Praxen zusätzlich Faltenbehandlung mit Botox oder Hyaluron, Microneedling, Laser-Haarentfernung.\n\nAnker-Reihenfolge, nimm den ersten, der den Austauschtest besteht:\n1. Lob aus Bewertungstexten: eine konkrete Paraphrase dessen, was Patienten an dieser Praxis loben. Plural oder \"immer wieder\" nur, wenn mindestens 2 Bewertungen dieses Lob tragen.\n2. Abhebendes Detail von der Website, auch Wachstum oder eine Stellenanzeige als Erkenntnis über die Praxis (Wachstum, Spezialisierung, neues Projekt), ohne zu sagen, dass die Praxis sucht oder einstellt.\n3. Anzahl und Schnitt der Bewertungen als eigener Anker, nur bei mindestens 30 Bewertungen und einem Schnitt ab 4,5: Zahl gerundet (\"über 200\"), Schnitt mit Komma (\"4,8\"). Werte aus dem Import (Google-Profil) gelten als Quelle; widersprechen sich Quellen, nimm den kleineren Wert. Unter 30 Bewertungen oder unter 4,5 keine Bewertungszahlen.\n4. Fallback.\n\nPositiver Schluss: Ein Lob aus Bewertungstexten trägt das Intro allein, hänge dann keinen Schluss an, der es nur wiederholt. Nach einem neutralen Faktum oder einer Bewertungszahl folgt ein kurzer Halbsatz. Zuerst eine Würdigung am Detail: was genau dieses Detail über die Praxis zeigt, als Folgerung (\"das zeigt, dass dir deine Patientinnen auch nach dem Termin wichtig sind\"), Anerkennung, Seltenheit mit dem Detail (\"so eine Nachsorge erlebt man nicht oft\"), Kundensicht oder lobender Nutzen, der sagt, was das Detail wert ist; hinter einer Bewertungszahl gleich die Reaktion. Sonst eine kurze persönliche Reaktion, die am Detail hängt und es benennt, in der Vergangenheit erzählt (Muster: \"das fand ich eine schöne Idee\", \"hat mir gut gefallen\"; nie allein, nie als feste Wendung). Ein Superlativ nur, wenn der Anker wirklich beeindruckt, und immer am Detail. Nie ein Mechanik-Nutzen, der erklärt, was man dank des Details tun kann (\"so können sich Interessierte vorab ein Bild machen\", \"so kann man unverbindlich nachfragen\"). Nie ein leeres Prüfer-Urteil über die Qualität der Arbeit, das aus dem Detail nicht folgt (\"das wirkt vertrauenswürdig\", \"so einen Schnitt hält man nur, wenn die Arbeit stimmt\", \"da machst du vieles richtig\", \"zeigt, dass die Behandlung ankommt\"). Nichts erfinden, nur was direkt aus dem Detail folgt (nie \"deine Patienten lieben das\", nie \"alle positiv\"). Keine feste Wendung: bilde jeden Schluss aus dem konkreten Detail. Nie zweimal loben. Nicht beim Fallback.\n\nEinstieg: Kein Einstieg ist Standard. Wähle ihn nach der letzten Ziffer der Lead-ID: 0-2 \"mir ist aufgefallen, dass ...\", 3-5 \"ich hab mir ... angeschaut\", 6-7 \"beim Stöbern auf deiner Website ...\", 8-9 direkt mit dem Detail. Ein Bewertungsanker nennt immer die Quelle im Einstieg (\"ich hab mir deine Bewertungen angeschaut, und ...\"). Steht keine Lead-ID im Kontext, wähle den Einstieg passend zum Anker und nicht immer denselben.\n\nStreng verboten:\n- Jede Form von Kritik, Defizit oder Verbesserungsvorschlag. Keine Wörter wie Problem, Lücke, Hürde, fehlt, veraltet, ausbaufähig, begrenzt, noch nicht, leider, schade, verschenkt Potenzial.\n- Konjunktiv-Wünsche wie \"wäre schön, wenn ...\" oder \"wäre sinnvoll, wenn ...\".\n- Auditartige Formulierungen, Ratschläge, Bevormundung.\n- Selbstvorstellung oder Pitch: kein \"Wir sind\", \"Mein Name ist\", \"Wir helfen\", \"Ich bin auf deine Webseite gestoßen\".\n- Floskeln, Superlative und Lobadjektive ohne Inhalt wie \"tolle Webseite\", \"ich war beeindruckt von deinem Auftritt\", \"finde ich spannend\", \"finde ich stark\", \"Hammer\", \"beeindruckend\" ohne Detail, \"das sieht man selten\", \"das sieht man nicht immer\", \"hat man nicht alle Tage\", \"das spricht für sich\".\n- Ein zweiter Satz ist konkret und wiederholt oder nimmt nicht vorweg, was der feste Text danach sagt.\n- Der angesprochenen Person nichts zuschreiben, was einer anderen Person gehört (zum Beispiel den Podcast des Inhabers in einer Mail an eine Mitarbeiterin); nenne die Person dann beim Namen.\n- Erfundene Fakten, Namen, Rollen oder Zahlen. Nenne Bewertungszahlen nur, wenn sie im Research oder in den Lead-Attributen belegt sind.\n- Sichtbare Platzhalter in Klammern, M-Striche, Gedankenstriche als Trenner, Emojis, Bold, Aufzählungen.\n- Mehr als 2 Sätze.\n\nFallback: Wenn kein Anker den Austauschtest besteht, schreibe genau diesen Satz: \"eine inhabergeführte Praxis zu leiten, bedeutet viel Verantwortung, und das sehe ich mit Respekt.\" Der Fallback behauptet nichts Unbelegtes über die Praxis. Er bleibt wörtlich, ohne angehängten Schluss. Nutze diesen Fallback lieber, als eine Beobachtung zu erfinden oder eine generische Floskel zu schreiben.\n\nDeutsche Rechtschreibung mit echten Umlauten und ß.",
      "sortOrder": 2
    }
  ],
  "sequence": {
    "steps": [
      {
        "stepNumber": 1,
        "subject": "kurze Frage",
        "body": "{{ai.hallo}}\n\n{{ai.intro}}\n\nDeswegen war ich so frei und habe dir einen kompletten Entwurf für eine neue Startseite erstellt, inklusive eingebautem Online-Terminbuchungs-Flow.\n\nIch bin gerade noch an den letzten Feinheiten dran, vor allem daran, die Behandlungsseiten gleich für Google und KI-Suchmaschinen mitzudenken, und werde morgen mit dem Entwurf fertig.\n\nWäre es in Ordnung, wenn ich dir das zusende? Völlig unverbindlich natürlich.\n\nViele Grüße\nJonas Weber\nInhaber - Weber Webdesign",
        "delayDays": 0,
        "delayUnit": "days"
      },
      {
        "stepNumber": 2,
        "subject": "",
        "body": "{{ai.hallo}}\n\ndu hast sicher viel um die Ohren, ich wollte nur sichergehen, dass meine Mail bei dir angekommen ist.\n\nEin kurzes Ja reicht mir.\n\nViele Grüße\nJonas Weber\nInhaber - Weber Webdesign",
        "delayDays": 3,
        "delayUnit": "days"
      },
      {
        "stepNumber": 3,
        "subject": "kurzes Update",
        "body": "{{ai.hallo}}\n\nzu dem Entwurf für deine neue Startseite ein Beispiel, was so etwas bringen kann. Bei der Praxis Dr. Sommer in Stuttgart haben sich die Online-Terminanfragen nach dem Relaunch in vier Monaten verdreifacht. Der größte Hebel war, dass Terminwünsche nicht mehr nur mitten in der Sprechstunde am Telefon landen. Beim Beauty-Studio Glow in München stieg die Buchungsquote der Behandlungsseiten um 60 Prozent.\n\nWenn du magst, schicke ich dir die Case Study als PDF.\n\nViele Grüße\nJonas Weber\nInhaber - Weber Webdesign",
        "delayDays": 5,
        "delayUnit": "days"
      },
      {
        "stepNumber": 4,
        "subject": "",
        "body": "{{ai.hallo}}\n\nda ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung. Sag mir gern kurz Bescheid, falls ich mich damit besser bei jemand anderem im Team melden sollte. Der Entwurf bleibt bei mir liegen, falls das Thema irgendwann wieder aktuell wird.\n\nAlles Gute für die Praxis.\n\nViele Grüße\nJonas Weber\nInhaber - Weber Webdesign",
        "delayDays": 7,
        "delayUnit": "days"
      }
    ]
  }
}
```

## Variante der Ansprache: Sie

Standard ist `du` im Singular. Ohne benennbaren Ansprechpartner lautet der Gruß „Hallo,“ und der
Text bleibt im Singular („dein Team“, „deine Praxis“); eine Ihr- oder Team-Form gibt es nicht. Nur
wenn der Nutzer die Kampagne siezen will (Kampagnen an sehr große Unternehmen), ändert man drei
Stellen gemeinsam: `emailAgentConfig.salutation`, die Format-Regeln im `hallo`-Prompt und die
Pronomen im festen Sequenztext (inklusive `offer_contract.cta` und der Pronomen-Vorgabe im
`intro`-Prompt).

| `salutation` | `hallo`-Regel im Prompt | fester Text, Beispiel Step 1 |
|---|---|---|
| `sie` | „Hallo Frau <Nachname>,“ / „Hallo Herr <Nachname>,“, Titel nur wenn belegt; Fallback „Guten Tag,“ | „Deswegen war ich so frei und habe Ihnen einen kompletten Entwurf … erstellt …“ / „Wäre es in Ordnung, wenn ich Ihnen das zusende? Völlig unverbindlich natürlich.“ |

Nie „Hallo Herr/Frau …“ zusammen mit Du-Text.

## Optional: Kurzname `firma`

Führt die Kampagne nach `outreach-campaign` den Kurznamen als AI-Variable `firma`, kommt sie
als dritte Variable dazu (Reihenfolge `hallo`, `firma`, `intro`, `sortOrder` 1-3). Der Betreff
von Step 1 bleibt „kurze Frage“; nur Karte A, B und E tragen den Namen im Betreff, und dann
ausschließlich als `{{ai.firma}}`, nie als rohes `{{lead.company}}`. Am Copy-Regelwerk ändert
das nichts.
