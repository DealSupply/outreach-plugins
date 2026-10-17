# Plattform-Hosts: wann eine Website keine eigene Website ist

> Stand: ListM8 MCP 3.0.0, abgeglichen am 16.10.2026 mit der Server-Liste (`Model/Web/SharedHosts`).
> **Maßgeblich ist der Server.** Die aktuelle Liste liefert die App unter
> `GET /api/leads/import-rules` (`platformHosts`, `platformBrands`, `builderHosts`). Weicht sie ab,
> kostet das nur eine Ablehnung mit Grund `platform_only_website`, keine Daten. Dann hier nachziehen.

Ab ListM8 3.0.0 darf ein Lead ohne E-Mail importiert werden, wenn er eine **eigene** Website hat;
die Recherche sucht dort die Kontaktadresse. Ein Link auf ein Profil bei einer Plattform ist keine
eigene Website: Ohne E-Mail lehnt der Import solche Zeilen ab. Mit E-Mail bleibt der Link erhalten
(er hilft der Recherche).

`build_csv.py` liest die drei Listen unten (Zeilen, die mit `- ` beginnen, je Abschnitt).

## Profil-Plattformen (die ganze Host-Familie zählt nicht als Website)

- facebook.com
- instagram.com
- linkedin.com
- xing.com
- google.com
- google.de
- linktr.ee
- tiktok.com
- youtube.com
- x.com
- twitter.com
- g.page
- goo.gl
- beacons.ai
- about.me
- booksy.com
- doctolib.de
- jameda.de
- treatwell.de
- yelp.com
- tripadvisor.com
- gelbeseiten.de
- dasoertliche.de
- 11880.com
- golocal.de
- cylex.de
- meinestadt.de
- wlw.de
- kosmetikstudios-24.de
- widimedia.com
- speisekartenweb.de

## Marken mit Länderdomains (treatwell.es, doctolib.fr …)

- treatwell
- doctolib
- pinterest

## Baukästen (nur die Plattform-Domain selbst zählt nicht, Kunden-Subdomains sind eigene Websites)

`praxis.jimdosite.com` ist die Website eines Betriebs und damit ein gültiger Lead ohne E-Mail;
`jimdosite.com` selbst nicht. Genau diese Betriebe sind für viele ICPs (Webdesign) die Zielgruppe.

- business.site
- wixsite.com
- wix.com
- jimdofree.com
- jimdosite.com
- jimdo.com
- weebly.com
- squarespace.com
- strikingly.com
- carrd.co
- site123.me
- webnode.de
- webnode.com
- webnode.at

## Pflege

Meldet der Import `platform_only_website` für einen Host, der hier fehlt (oder die Liste aus
`import-rules` enthält einen neuen Eintrag), den Host im passenden Abschnitt ergänzen und das
Datum oben setzen. Die Noise-Liste (`noise-domains.md`) bleibt davon getrennt: Sie filtert
Suchtreffer und Portale vor dem Import, diese Liste beantwortet nur „ist das eine eigene Website?“.
