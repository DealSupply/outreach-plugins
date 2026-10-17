# Datenumfang: was beschafft und hochgeladen wird, was nicht

> Stand 11.10.2026, abgeglichen mit dem Code der Plattform und einem Testlauf (15 Elektriker
> Stuttgart, Google Maps). Grundsatz: **Beschaffe nur, was die Plattform nicht selbst findet.**
> Alles andere kostet doppelt: einmal beim Scrapen, einmal in der Recherche.

## Was die Plattform pro Lead selbst erledigt

| Stufe | Was sie liest und findet |
|---|---|
| Qualifizierung | Startseite, Kontakt- und Angebotsseite, Screenshots mobil und Desktop. Importierte Kategorie, Bewertung, Reichweite und Ort nutzt sie als Hilfsevidenz. |
| Recherche | 3 bis 20 Seiten der Website, je nach Recherche-Tiefe der Kampagne (`quick` 3 bis 5, `standard` 8 bis 12, `deep` 10 bis 20); das Impressum ist Pflicht. Findet den Ansprechpartner mit Rolle und ersetzt eine Rollen-Adresse (info@) durch die persönliche Adresse, wenn sie eine findet. Dazu 2, 3 oder 5 Websuchen (Register, Bewertungen, Presse). |
| Nicht | Google Maps und Google-Bewertungen abrufen, LinkedIn, Instagram, Shop-Technologie, Daten von Verkaufsplattformen. Was davon in die Mail soll, muss mit dem Import kommen. |

Daraus folgt:

- **Nicht beschaffen:** Entscheider-Namen, persönliche E-Mail-Adressen, Handelsregister, USt-Id,
  Firmenbeschreibungen von der Website. Das macht die Recherche, und sie prüft es auch.
- **Immer beschaffen:** die Liste selbst (wer gehört zur Zielgruppe), je Lead eine E-Mail-Adresse
  **oder** die eigene Website (ab ListM8 MCP 3.0.0; ohne Adresse sucht die Recherche sie) und alles,
  was nur auf der Quelle steht und einen Einstieg trägt: Google-Bewertungen und Rezensionen,
  Follower und Bio, Plattform-Bewertung, Shop-Technologie.

## Pflichtfelder je Lead

| Feld | Warum |
|---|---|
| `email` **oder** `website` | Ab ListM8 MCP 3.0.0 reicht eins von beiden. **info@ reicht**, die Recherche sucht die persönliche Adresse selbst. Ohne Adresse sucht sie auf der Website eine; findet sie keine, scheidet der Lead aus (keine Mail). Ein Profil-Link (Instagram, Linktree, Portal) zählt nicht als Website. Ältere Server verlangen weiter eine Adresse je Lead. |
| `website` | Auch mit Adresse fast immer nötig: ohne Website hat die Recherche keinen Startpunkt (Ausnahme: Zielgruppe ohne Website, siehe Maps-Weg). |
| `company` | Anzeige und Anrede. |

## Je Quelle: immer mitnehmen

`build_csv.py` schreibt die Spalten unter genau diesen Namen. Spalten ohne Wert lässt es weg.

| Quelle | Spalten | Was es kostet | Warum |
|---|---|---|---|
| **Google Maps** (Weg C, Outscraper) | `rating`, `reviews_count`, `place_id`, `reviews_tags`, `kategorie`, `google_rezensionstexte` (5 neueste mit Text), `inhaber` und `inhaber_rolle` aus dem Impressum | Bewertung und Anzahl sind im Grundpreis. Stichworte und Rezensionstexte kommen mit den Ortsdetails: rund 0,2 bis 0,3 Cent je Lead (0,00105 $ Ortsdetails plus 0,00026 $ je Rezension, Stufe GOLD); mit `reviewsStartDate: "18 months"` nur für Rezensionen, die die Plattform nutzt, etwa halb so viele. Der Inhaber steckt in der Kontaktanreicherung, die ohnehin läuft. | Die Recherche sucht nicht mehr selbst nach Bewertungen, wenn Rezensionstexte importiert sind (eine Websuche weniger, rund 0,7 Cent plus Tokens). Ohne Import fand sie im Praxistest bei 43 % der Leads keinen Rezensionstext. Bewertung ab 30 Rezensionen und 4,5 Sternen ist ein bewährter Einstieg. |
| **LinkedIn** (Weg D) | `firstName`, `lastName`, `position`, `headline`, `linkedin_url`, `connections` | im Profilpreis | Die Plattform liest LinkedIn nicht. |
| **Instagram** (Weg D) | `instagram_url`, `follower`, `bio`, `link_typ`, `gefunden_via_hashtag` | im Profilpreis | Die Plattform liest Instagram nicht; Follower und Bio sind der Einstieg. |
| **Verkaufsplattformen** (Weg E) | `plattform`, `seller_url`, `bewertung`, `bewertungen_anzahl`, `verkaeufe`, `kategorie` | im Actor-Preis | Plattform-Bewertung und Verkäufe stehen nicht auf der eigenen Website. |
| **StoreLeads** (Weg B) | `plattform`, `umsatz_geschaetzt`, `apps` | im Export | Technologie und Umsatz findet keine Recherche. |
| **Apollo** (Weg A) | `firstName`, `lastName`, `position`, `linkedin_url`, `mitarbeiter` | im Export | Kommt ohnehin mit; den Entscheider muss die Recherche dann nur bestätigen. |
| **SaaS-Verzeichnisse und LinkedIn-Firmen** (Weg F) | `kategorie`, `plattform`, `bewertung`, `bewertungen_anzahl` (OMR), `linkedin_url`, `mitarbeiter`, `follower`; per `--keep` `omr_url`, `kostenlos_testen`, `quellen`, `gruendung` | OMR und Startbase kostenlos, LinkedIn im Firmenpreis | Die OMR-Bewertung und die Kategorie sind öffentlich und nachprüfbar, die Plattform liest OMR nicht. `quellen` zeigt, in wie vielen Verzeichnissen die Firma steht. |
| **Google-Suche** (Wege A, B, D) | nur die Pflichtfelder und `kategorie` (die Nische der Query) | – | Der Suchtreffer selbst trägt keinen Einstieg. Für Zielgruppen mit Maps-Eintrag den Maps-Weg vorziehen, weil Bewertungen dabei sind. |

Weitere Rohfelder nur mit `--keep` und nur, wenn sie einen Einstieg tragen, den die Website nicht hat.

## Nie hochladen

- Namen, Fotos oder Profile von Rezensenten und anderen Dritten.
- Koordinaten, Öffnungszeiten, Bilder, Maps-Links (die `place_id` reicht), Rohdaten-JSON.
- Register- und USt-Nummern: kein Einstieg für eine Mail, die Recherche findet sie bei Bedarf.

## Kostenpflichtige Zusätze, die beim Maps-Actor aus bleiben

| Zusatz | Preis (GOLD) | Warum aus |
|---|---|---|
| Business-Leads-Anreicherung (Entscheider, Arbeits-E-Mail) | 0,004 $ je Lead | Macht die Recherche. |
| E-Mail-Verifizierung im Actor | 0,002 $ je Adresse | Der eigene Verifier kostet 0,0006 $ (`listen-qualitaet`). |
| Social-Profile, Bilder, Wettbewerber-Analyse | ab 0,00026 $ je Stück | Kein Einstieg für die Mail. |

## Die Kontaktlücke: vorab anreichern oder der Recherche überlassen

Treffer ohne Adresse (bei Maps 20 bis 50 %) dürfen ab ListM8 MCP 3.0.0 mit ihrer eigenen Website
importiert werden: Die Recherche sucht dann die Kontaktadresse (Impressum, Kontaktseite, Footer).
Findet sie keine, scheidet der Lead aus und bekommt keine Mail. Auf älteren Servern braucht jede
Zeile weiter eine Adresse; dann gilt die Reihenfolge unten als Pflicht.

Was eine Lücke kostet:

| Weg | Kosten je Lead |
|---|---|
| Impressum-Actor vorab (`impressum-enrichment`) | rund 0,2 Cent je Domain plus Startgebühr, Batches ab etwa 50 Domains (`kosten.md`) |
| ListM8-Server-Lauf | Qualifizierung plus Recherche, rund 2 bis 3 Cent je Lead, auch wenn am Ende keine Adresse kommt; dazu ein Platz im Lead-Kontingent |
| Abo-Lauf | kein Geld, aber Abo-Kontingent je Lead |

Entscheidung, jeweils mit dem Nutzer:

| Lage | Empfehlung |
|---|---|
| Quelle ohne Kontaktdaten (Google-Suche, LinkedIn-Firmen, Instagram-Websites, Händlerdomains) **und** ab etwa 50 Domains | Vorab `impressum-enrichment`: rund 10-mal billiger als die Recherche, und es läuft vor der Qualifizierung (29 von 40 LinkedIn-Firmen bekamen so eine Adresse). |
| Maps-Lauf (Kontaktanreicherung ist schon im Preis) | Kein Zusatzlauf: Im Test vom 11.10.2026 fanden drei Impressum- und Kontakt-Actors für 28 Domains ohne Adresse nur 1 bis 5 Adressen. Leads mit eigener Website importieren (die Recherche sucht) oder abspalten; die niedrige Erwartung nennen. |
| Liste unter 50 Leads oder Pilot | Nicht anreichern, die Recherche erledigt es. |
| `max_leads` knapp | Vorab anreichern oder Leads ohne Adresse weglassen: jeder importierte Lead belegt einen Platz, auch wenn er später ausscheidet. |
| Abo-Lauf mit knappem Kontingent und großer Liste | Vorab anreichern. |
| Verifizierte Adressen vor dem Import gewünscht (Bounce unter 3 %) | Vorab anreichern: Adressen aus der Recherche laufen nicht durch den Verifier (`listen-qualitaet`). |
| Nicht-DACH-Domains | Optional `kontaktseiten-fallback`, sonst die Recherche. |

Immer zuerst: die Adresse aus dem Impressum der Maps-Kontaktanreicherung nehmen (macht
`build_csv.py` selbst, nur mit eigener Domain oder Freemail; fremde Firmen-Domains im Impressum sind
meist die Webagentur). Leads ganz ohne eigene Website (nur Profil-Link oder gar nichts) kann
niemand recherchieren: Sie fliegen bei der Übergabe raus und werden berichtet.

**Geratene Adressen** aus B2B-Datenbanken (`emailPatternGuess`, Hinweis `geratene-adresse`) nie
ungeprüft importieren: Im Test waren 23 von 51 unzustellbar. Nur verifiziert „gut“ übernehmen.

Persönliche Adressen eines Entscheiders nie vorab kaufen. `enrichment-waterfall` nur für wenige
wertvolle Leads, bei denen die Recherche einen Namen, aber keine persönliche Adresse gefunden hat.

## Recherche-Tiefe empfehlen

Die Stufe ist eine Einstellung der Kampagne (`researchAgentConfig.researchTier`: `basis`, `smart`,
`deep`, gesetzt über den Outreach-Workflow `outreach-campaign`). Bei der Übergabe eine Empfehlung
aussprechen:

| Liste | Empfehlung |
|---|---|
| Lokale Betriebe mit Website und Rezensionstexten | `basis`: Impressum, Startseite und Rezensionen reichen für Anrede und Einstieg. |
| Kleine Firmen ohne Rezensionen, oder viele Leads ohne Adresse | `smart`: Fehlt die Adresse auf der Website, sucht die Recherche einmal gezielt nach dem Impressum. |
| Größere Firmen, die Informationen von Drittquellen brauchen | `deep` |

Die Empfehlung ändert nichts von selbst; der Nutzer entscheidet in der Kampagne.
