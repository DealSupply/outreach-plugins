# CSV-Spalten — DAS eine Format

> Jede Stufe der Datenbeschaffung schreibt und liest exakt dieses Format (`build_csv.py`). Welche
> Zusatzspalten je Quelle hineingehören und warum, steht in `datenumfang.md`.
> `import_leads` (Outreach-MCP) übernimmt die Kernfelder `email`, `company`, `website`,
> `phoneNumber`, `city` direkt und erkennt die Google-Spalten (`rating`, `reviews_count`,
> `place_id`, `reviews_tags`, `google_rezensionstexte`) von selbst. ALLE anderen Spalten (auch
> `firstName`/`lastName`!) brauchen beim Import eine Deklaration in `attribute_mappings`, sonst
> werden sie stillschweigend verworfen (Details: `outreach-uebergabe.md`, Schritt 3). Der
> App-Import bietet die Zusatzspalten interaktiv als Attribute an.

## Kernspalten (immer vorhanden, exakt diese Header)

| Spalte | Pflicht | Regeln |
|---|---|---|
| `email` | nein* | lowercase, getrimmt. *Ab ListM8 MCP 3.0.0 braucht jede Zeile der ÜBERGABE-CSV eine E-Mail **oder** eine eigene Website (`build_csv.py --uebergabe kontakt`); ohne E-Mail sucht die Recherche der Plattform die Adresse. Auf älteren Servern ist die E-Mail in der Übergabe-CSV Pflicht (`--uebergabe email`). Während der Anreicherung darf sie leer sein (build_csv.py behält die Zeile und markiert `keine-email` in `hinweis`). Bei mehreren Adressen wählt build_csv.py die der eigenen Domain vor Freemail vor fremden Domains, die persönliche vor der Rollen-Adresse, Bewerbungs- und Datenschutz-Adressen nur ohne Alternative. Platzhalter (`info@mysite.com`) und Adressen mit Umlaut vor dem @ verwirft es. |
| `firstName` | nein | leer lassen statt raten — eine kaputte Anrede killt die Mail. Nur übernehmen, wenn die Quelle ihn ohnehin liefert (LinkedIn, Apollo); nie eigens beschaffen. |
| `lastName` | nein | dito |
| `company` | nein | Anzeigename; Normalisierung (GmbH-Zusätze) macht build_csv.py in `companyClean` |
| `website` | ja* | mit Protokoll (https://…). *Pflicht, wenn die E-Mail fehlt, und praktisch immer: ohne Website kein Startpunkt für die Recherche (Leads ohne Website markiert build_csv.py in `hinweis`). Ein Profil-Link (Instagram, Linktree, Branchenportal …, Liste `plattform-hosts.md`) zählt nicht als Website; Baukasten-Subdomains (`praxis.jimdosite.com`) schon. Bei Google Maps ist `url` der Maps-Link und wird nie als Website übernommen. |
| `phoneNumber` | nein | E.164 bevorzugt (+49 …) |
| `city` | nein | Stadtname ohne PLZ |
| `kategorie` | nein | Branche/Kategorie aus der Quelle (z. B. Google-Maps-categoryName) |
| `quelle` | ja | Herkunftsvermerk: `apify:<actor> <datum>` — macht Läufe rückverfolgbar |
| `companyClean` | nein | normalisierter Firmenname für die Ansprache („Müller Bau" statt „Müller Bau GmbH & Co. KG") |
| `hinweis` | nein | maschinelle Anmerkungen: `rollen-adresse`, `keine-email`, `keine-website`, `keine-rezensionstexte`, `portal-website` (Maps-Eintrag mit Branchenportal statt eigener Website; Adresse verworfen), `fremde-domain` (Adresse einer anderen Firmen-Domain; Freemail zählt nicht), `geratene-adresse` (aus dem Namensmuster einer Datenbank geraten; nur verifiziert übernehmen), `nur-plattform-url` (keine E-Mail und nur ein Profil-Link als Website; die Übergabe mit `--uebergabe kontakt` verwirft solche Zeilen), `adresse-verworfen` (der Verifier hat die Adresse aussortiert, die Zeile bleibt über ihre Website im Rennen) |

## Zusatzspalten (werden beim Import zu Attributen)

Erscheinen nur, wenn mindestens eine Zeile einen Wert hat.

| Spalte | Quelle | Inhalt |
|---|---|---|
| `rating` | Google Maps | Google-Bewertung, z. B. `4.8` |
| `reviews_count` | Google Maps | Anzahl der Google-Rezensionen |
| `place_id` | Google Maps | Google Place ID (Quellenlink der Rezensionen, Abgleich) |
| `reviews_tags` | Google Maps | Stichworte aus den Rezensionen: `pv-anlage (3), termin (2)` |
| `google_rezensionstexte` | Google Maps | bis zu 5 Rezensionen mit Text, neueste zuerst, eine je Zeile: `2026-02-03 · 4★ · Text`. Ohne Namen der Verfasser. |
| `inhaber`, `inhaber_rolle` | Google Maps (Impressum der Kontaktanreicherung) | Inhaber bzw. Geschäftsführer; nur gefüllt, wenn `firstName`/`lastName` leer sind |
| `position`, `headline`, `linkedin_url`, `connections` | LinkedIn, Apollo | Rolle und Profil der Person |
| `mitarbeiter` | Apollo | Mitarbeiterzahl |
| `instagram_url`, `follower`, `bio`, `link_typ`, `gefunden_via_hashtag` | Instagram | Profil, Reichweite, Bio, Art des Bio-Links, Fund-Hashtag |
| `plattform`, `seller_url`, `bewertung`, `bewertungen_anzahl`, `verkaeufe` | Verkaufsplattformen | Plattform-Profil und -Bewertung (nicht Google) |
| `umsatz_geschaetzt`, `apps` | StoreLeads | Shop-Kennzahlen |

Die Rohfelder der Actors werden unter diese Namen übersetzt (z. B. `followersCount` → `follower`,
`biography` → `bio`, `totalScore` → `rating`). Weitere Rohfelder nur mit `--keep feld1,feld2` und nur,
wenn sie einen Einstieg tragen (`datenumfang.md`).

## Regeln

1. **UTF-8 mit korrekten Umlauten.** Niemals ae/oe/ue-Ersatz.
2. **Eine Zeile = ein Lead = eine eindeutige E-Mail, ohne E-Mail eine eindeutige Website.** Dedup
   passiert VOR dem Schreiben (dedup.py); der Import gleicht Zeilen ohne E-Mail ebenfalls über die
   Website ab.
7. **Verworfene Zeilen** der Übergabe schreibt `build_csv.py --verworfen <datei>` mit Spalte `grund`
   (`nur-plattform-url`, `kein-kontaktmerkmal`, `keine-email`) in eine eigene CSV; die Zahl gehört
   in den Bericht.
3. **Länder-Split:** je Land eine Datei (`leads-de.csv`, `leads-at.csv`, `leads-ch.csv`).
4. **Rollen-Adressen** (info@, kontakt@, office@) sind erlaubt und werden in `hinweis` markiert —
   die Recherche sucht die persönliche Adresse, die Qualifizierung entscheidet (Trichter-Prinzip).
5. **Mehrzeilige Zellen** (`google_rezensionstexte`) stehen in Anführungszeichen; App-Import und
   `import_leads` lesen sie zeilenweise.
6. Dateinamen: `leads-<nische>-<region>-<jjjjmmtt>.csv` — z. B. `leads-shk-koeln-20260819.csv`.
