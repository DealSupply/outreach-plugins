# Qualifizierungs-Kriterien formulieren — offen statt restriktiv

> Die Qualifizierung ist ein OFFENER Vorfilter, kein Feinsieb. Falsch aussortierte Leads sind
> endgültig verloren; durchgelassene Grenzfälle kosten nur einen Research-Lauf. Der Server-Agent
> kennt diese Philosophie bereits — deine Kriterien dürfen sie nicht unterlaufen.

## So formulierst du `qualificationSettings`

- **target_customer_profile / fit_criteria: INKLUSIV.** „Passt, wenn …" statt „raus, wenn nicht …".
  Positive Merkmale beschreiben (Branche des KUNDEN, Größenkorridor, Region, erkennbarer Bedarf) —
  nicht eine Checkliste, die jeder Lead vollständig erfüllen muss. Der „Passt, wenn …"-Satz nennt ein
  Merkmal der Zielbranche („Passt, wenn Behandlungen an Haut oder Gesicht angeboten werden"), nie eines,
  das jede Nachbarbranche auch erfüllt („eigenständiger Betrieb mit eigenem Behandlungsangebot"): Das
  lesen Modelle als Eintrittskarte, im Blindtest 23.10. kamen so Massagepraxen, Hotels und eine
  proktologische Praxis in eine Ästhetik-Kampagne.
- **disqualifiers: NUR harte No-Gos, die ein Agent öffentlich prüfen kann.** Falsche Branche,
  Wettbewerber, Konzern, Größenschwelle, kein Geschäftsbetrieb erkennbar, explizite Ausschlüsse
  des Kunden. Jeder Disqualifier muss so konkret sein, dass die Ablehnung einen benennbaren
  Grund hat.
  - **Konzern** heißt: fremde Muttergesellschaft, Franchise oder Börsennotierung. Eine Gruppe
    eigener Betriebe derselben Inhaber ist kein Konzern.
  - **Größe** ist ein eigener Punkt: „Unternehmen oder Unternehmensgruppen mit mehr als N
    Mitarbeitenden, auch familiengeführt“ (N nennt der Kunde; ohne Wunsch keine Schwelle). Nie mit
    „Konzern“ vermischen, sonst urteilt der Agent bei einer Familiengruppe mal so, mal so.
- **NIE als Disqualifier:** Geschmacksurteile (hässliche/dünne Website, wenig Content, kein Blog),
  fehlende Einzelinfos (kein Team auf der Website), Unsicherheit. Das sind Need-Signale oder
  Research-Aufgaben — bei Bedarfs-Offers ist die „schlechte" Website sogar das Verkaufsargument.
  Ebenso nie:
  - was nur das System weiß (Kontaktsperre, Bestandskunde, bereits angeschrieben): Das regelt
    der Kontaktstatus in ListM8, nie der Kampagnentext;
  - der Bedarf, den das Angebot löst: Kein Ausschlussgrund schließt ihn aus („Praxis ohne
    Website“ bei einem Website-Angebot);
  Umgekehrt gehört hinein, wenn der Betrieb schon hat, was das Angebot liefert: Enthält das Angebot
  eine Online-Terminbuchung, ist „eigene Website bindet bereits eine Online-Terminbuchung ein oder
  verlinkt direkt darauf (eigenes Tool oder Anbieter wie Doctolib, OneDoc, Treatwell); ein bloßes
  Verzeichnisprofil zählt nicht“ ein Ausschlussgrund. Nur prüfbare Merkmale: Zusätze wie „bei sonst
  modernem Auftritt“ kann kein Agent entscheiden. Sonst bekommt ein Betrieb mit funktionierender
  Buchung genau diese als Neuheit angeboten.
- **Sprache:** Ist die Mail deutsch und enthält die Liste Schweizer Betriebe, gehört „Website
  ausschließlich französisch- oder italienischsprachig (Romandie, Tessin)“ in die Ausschlussgründe.
  „DACH“ allein schließt die Westschweiz nicht aus.
  - ein Merkmal, dessen Fehlen nur fehlende Information wäre: „Selbstzahlerleistung erkennbar“
    ist ein Fit-Kriterium (erkennbar: höherer Fit, sonst mid), kein Ausschlussgrund.
- **Faustregel für die Erwartung:** In einer halbwegs sauberen Liste sollten grob 60–80 % durch
  die Qualifizierung kommen (überwiegend mid_qualified/qualified). Fallen regelmäßig > 50 %
  durch, sind die Kriterien zu streng ODER die Liste ist falsch — beides beim Nutzer ansprechen,
  nicht stillschweigend hinnehmen.

## Beispiel (Webdesign/SEO an Handwerk)

```json
{
  "target_customer_profile": "Inhabergeführte Handwerksbetriebe (SHK, Elektro, Dach, Bau) in DACH mit 1-50 Mitarbeitern. Passt, wenn ein aktiver Geschäftsbetrieb erkennbar ist - auch mit veralteter oder minimaler Website (das ist unser Ansatzpunkt, kein Ausschluss).",
  "offer_summary": "Kostenlose Vorschau einer neuen, mobilfreundlichen Startseite; danach die komplette Handwerker-Website.",
  "fit_criteria": "Passt, wenn der Betrieb selbst Handwerksleistungen vor Ort erbringt. Starke Signale: Website veraltet oder nicht mobilfreundlich, nur Branchenbuch- oder Google-Profil, gute Bewertungen ohne Sichtbarkeit. Keines davon ist Pflicht.",
  "disqualifiers": "Ketten, Franchise-Zentralen und Konzerne mit fremder Muttergesellschaft oder Börsennotierung, Unternehmen oder Unternehmensgruppen mit mehr als 500 Mitarbeitenden (auch familiengeführt), reine Baumärkte/Handel, Webdesign-/Marketing-Agenturen (Wettbewerber), Innungen, Kammern, Verbände, Bildungsträger, Zeitarbeit, Branchenverzeichnisse, Betriebe in Abwicklung.",
  "additional_prompt": "Im Zweifel mid_qualified mit ehrlicher Begründung - Research und Review filtern weiter. Ablehnung nur mit konkret benanntem Disqualifier."
}
```

Immer diese kanonischen Schlüssel verwenden. Die camelCase-Aliasse (`idealCustomer`,
`additionalInstructions` …) wertet nur die Laufzeit aus; die Oberfläche zeigt die Felder dann leer.
Bei Maps-Listen gehören die typischen Nachbartreffer (Innungen, Verbände, Zeitarbeit, Händler,
Verzeichnisse) in die Disqualifier: Google Maps liefert zu einem Gewerk regelmäßig 30-40 % davon.
Nachbarbetriebe der Branche (Labor, Handel, Zulieferer, Schulen) ausdrücklich nennen, etwa
„Dentallabore, Zahntechnik, Dentalhandel“ bei Zahnarztpraxen: Maps mischt sie unter die Praxen.

„Ablehnung nur mit konkret benanntem Disqualifier" schützt Grenzfälle der Zielbranche; ein Betrieb
aus einer anderen Branche ist kein Grenzfall, der Server lehnt ihn auch ohne Listeneintrag ab. Die
typischen Nachbartreffer trotzdem in die Disqualifier schreiben, das macht das Urteil stabil.

`additional_prompt` ist die Zusatzanweisung der Kampagne („Zusätzliche Hinweise") und wird auch
von der Recherche als Maßstab gelesen. Er gehört deshalb nur Formulierungen, die für beide Stufen gelten
(etwa „im Zweifel mid_qualified"). Keine Adress- oder Pipeline-Anweisungen („primäre E-Mail
nicht ändern“, „Adressen nicht erneut verifizieren“): Die Versandadresse wählt das System.

## Woran du eine zu restriktive Konfiguration erkennst

- Disqualifier-Liste länger als die Fit-Beschreibung.
- Bedingungen mit UND-Ketten („muss X und Y und Z haben").
- Anforderungen an Dinge, die die Website oft nicht zeigt (Umsatz, Mitarbeiterzahl exakt).
- Der Kunde beschreibt seinen TRAUM-Kunden statt seines KAUFENDEN Kunden.
