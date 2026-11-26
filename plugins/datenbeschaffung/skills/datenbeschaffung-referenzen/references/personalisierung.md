# Personalisierungs-Hebel je Weg

> Stand 26.11.2026. Quelle der Hebel: Kurshandbuch „Datenbeschaffung“ (19.08.2026), Kapitel 2, 4
> (Weg A), 5 (Weg B) und 6 (Weg C); für die Wege D, E und F die Felder, die die Quelle liefert
> (`datenumfang.md`).

Ein Hebel ist ein Fakt über den Lead, an dem die Mail zeigt, dass es um ihn geht. Der alte Kurs
verlangt je Lead mindestens Firma, Website, Position und Branchen-Kontext (Kap. 2). Beschafft wird
nur, was die Quelle ohnehin mitliefert; kein Hebel wird eigens gekauft.

- **Mit DealSupply** liest die Recherche Website und Impressum, aber nicht LinkedIn, Instagram,
  Shop-Technologie und Plattformdaten (`datenumfang.md`). Genau diese Hebel müssen mit der Liste
  kommen, sonst fehlen sie der Mail.
- **Ohne DealSupply** kommt jeder Hebel nur über die Liste (als Variable in Instantly,
  `ohne-dealsupply.md`) oder über das, was der Nutzer sich beim Ansehen der Leads notiert.

Vor dem Lauf dem Nutzer in einem Satz sagen, welcher Hebel mitkommt und welchen er selbst
notieren muss.

## Übersicht

| Weg | Hebel laut Kurs | Spalte, wenn die Quelle ihn liefert | Sonst |
|---|---|---|---|
| A, B2B (`weg-a-apollo`, `weg-a-b2b-google`) | Funding-Runde, letzter LinkedIn-Post der Person, Tech-Stack, neue Einstellungen (Kap. 4) | Apollo: `position`, `linkedin_url`, `mitarbeiter`; Funding oder Technologien nur per `--keep`, wenn sie im Export stehen | Je Lead von Hand oder mit der KI aus LinkedIn und Website (Kap. 4). Der Google-Weg bringt keinen Hebel mit. |
| B, Shops (`weg-b-storeleads`, `weg-b-ecom-google`) | Sortiment, Plattform („ihr seid auf Shopify“), fehlende Technologie („Google Ads, aber keine TikTok Ads“), eine Kundenbewertung zitieren, Saisonalität (Black Friday, Weihnachtsgeschäft, Sommersaison) (Kap. 5) | StoreLeads: `plattform`, `apps`, per `--keep` `technologien` und `plattform_wechsel`; Google-Weg: `kategorie` (die Nische der Suche) | Das Sortiment steht auf der Website. Saisonalität ist ein Zeitpunkt, keine Spalte: den Versand danach planen. |
| C, lokal (`weg-c-local-maps`, `outscraper-bulk`) | Google-Bewertung und eine Rezension zitieren, regionaler Bezug (Stadtteil), Aktualität („seit 2022 zertifiziert“) (Kap. 6) | `rating`, `reviews_count`, `google_rezensionstexte`, `reviews_tags`, `city` | Die Aktualität steht auf der Website. |
| D, Coaches (`weg-d-*`) | Positionierung und Angebot in eigenen Worten | `bio`, `follower`, `headline`, Caption per `--keep` (Hashtag-Weg) | nichts weiter |
| E, Plattform-Händler (`weg-e-plattform`) | Bewertung und Verkäufe auf der Plattform, Kategorie | `bewertung`, `bewertungen_anzahl`, `verkaeufe`, `kategorie`, `seller_url` | nichts weiter |
| F, SaaS (`weg-f-saas`) | Bewertung und Kategorie auf OMR, kostenloser Test | `bewertung`, `bewertungen_anzahl`, `kategorie`, per `--keep` `kostenlos_testen` | nichts weiter |

## Grenzen

- **Trigger filtern, nicht erwähnen** (`icp.md`): Neue Einstellungen oder ein neuer
  Geschäftsführer gehören in den Filter, nicht in die Mail. Ausnahme ist ein Recruiting-Angebot.
- **Schätzwerte** (Umsatz, Traffic aus StoreLeads) taugen zum Sortieren, nie als Tatsache in der
  Mail (`weg-b-storeleads`).
- **Keine Namen von Rezensenten** oder anderen Dritten (`datenumfang.md`).
- Was in der Mail steht, entscheidet die Copy, nicht die Datenbeschaffung.
