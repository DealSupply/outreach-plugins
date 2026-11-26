# Ziele außerhalb von Deutschland, Österreich und der Schweiz

> Stand 26.11.2026. Ehrlich vorweg: Alle Messwerte dieses Plugins (`erfahrungswerte.md`,
> `kosten.md`, Trefferquoten in den Weg-Skills) stammen aus Läufen in DACH. Für andere Länder gibt
> es keine eigenen Messungen. Was hier steht, ist der Stand des Kurshandbuchs „Datenbeschaffung“
> (19.08.2026) und das, was die Werkzeuge technisch hergeben. Das dem Nutzer vor dem ersten Lauf
> so sagen.

## Was belegt ist

| Aussage | Quelle |
|---|---|
| Die Impressumspflicht ist eine Besonderheit von Deutschland, Österreich und der Schweiz. Anderswo fehlt das Impressum oft, die Kontaktdaten stehen auf einer Kontaktseite oder gar nicht. | Kurshandbuch Kap. 6 |
| Impressum-Scraper bei internationalen Seiten: E-Mail 50 bis 70 %, Telefon 40 bis 60 %, Geschäftsführer 30 bis 50 %, Adresse 40 bis 60 % (bei deutschen Agenturen und Beratern 85 bis 95 % E-Mail). | Kurshandbuch Kap. 10 |
| Der Kontaktseiten-Fallback bringt typischerweise 5 bis 15 % zusätzliche Treffer. | Kurshandbuch Kap. 10 |
| Auf den EU-Marktplätzen von Amazon (DE, AT, FR, IT, ES) stehen E-Mail, Telefon, Adresse und USt-IdNr. im Verkäuferprofil; auf amazon.com fehlen sie oft ganz. | Kurshandbuch Kap. 8 |

Daraus folgt für die Erwartung: Von 100 Websites haben eher 50 bis 70 eine Adresse statt 75 bis 95
wie in DACH, und der Vorname fehlt öfter. Die Rohmenge entsprechend größer planen. Die
Qualitätsschwelle aus `impressum-enrichment` („unter 50 % heißt: falsche oder ausländische Seiten“)
ist hier kein Fehlerzeichen, sondern die Erwartung.

## Kontaktweg

- `kontaktseiten-fallback` statt `impressum-enrichment`: Der gepinnte Impressum-Actor ist auf
  deutsche Impressumsseiten gebaut (`languageCode: "de"`). Für englischsprachige Seiten die Pfade
  `/contact`, `/contact-us` und `/about` nehmen.
- Mit DealSupply sucht die Recherche die Adresse auch auf fremdsprachigen Seiten; gemessen ist das
  für andere Länder ebenfalls nicht.
- Ohne DealSupply bleiben Leads ohne gefundene Adresse draußen (`ohne-dealsupply.md`).

## Was je Werkzeug für das Zielland zu ändern ist

| Werkzeug | Für das Zielland | Grenze |
|---|---|---|
| Google-Suche (`build_queries.py`, SERP-Actor) | Suchbegriffe in der Landessprache; Städte des Ziellands mit `--region custom --cities "…"`; Ländercode des Actors (`gl`/`country`, großgeschrieben, z. B. `GB`, `FR`) | Das Plugin hat keine Städteliste außerhalb DACH: Die KI schlägt die größten Städte des Landes vor, der Nutzer bestätigt sie, Pilotstadt zuerst wie in `staedte.md`. `noise-domains.md` kennt vor allem deutschsprachige Portale: Was im Piloten durchrutscht, dort nachtragen, bevor skaliert wird. |
| Google Maps (`weg-c-local-maps`) | `locationQuery` im Zielland, `language` der Landessprache, in `build_csv.py` `--land <ländercode>` | Die Maps-Kategorien sind ohnehin englisch; Trefferquoten außerhalb DACH nicht gemessen. |
| LinkedIn (`weg-d-coaches-linkedin`) | Zielland im Standortfilter | Keine. |
| Instagram-Hashtags | Tags in der Landessprache | Keine. |
| Plattform-Verkäufer (`weg-e-plattform`) | EU-Marktplätze vor amazon.com | Auf amazon.com fehlen die Kontaktdaten oft. |
| SaaS (`weg-f-saas`), `sitz_check.py`, `omr_products.py --dach`, `linkedin_saas.py --dach` | nichts |  Nur für DACH gebaut (OMR Reviews und Startbase sind deutschsprachige Verzeichnisse). Für andere Länder nicht nutzbar; dort LinkedIn-Firmensuche plus `kontaktseiten-fallback`. |
| Prüfung der Adressen (Verifier, Instantly) | nichts | Länderunabhängig. |

## Pilot

Der Pilot ist hier doppelt wichtig: gleiche Actor-Preise, aber weniger Adressen, also höhere
Kosten je versandfähigem Lead. Eine Stadt, Kosten vorher nennen, Deckel setzen. Das Ergebnis mit
Land und Datum in `erfahrungswerte.md` eintragen: Es ist dann der erste echte Messwert für das Land.
