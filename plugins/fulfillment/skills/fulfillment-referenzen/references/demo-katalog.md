# Demo-Katalog: welche Offers sich mit KI liefern lassen

> Referenz zu `fulfillment`. Ein Offer, das der Nutzer nicht liefern kann, wird nicht geschrieben
> (Regel aus `outreach-copy`). Dieser Katalog sagt, was mit KI realistisch geht.

## Maßstab

Ein Offer taugt als Türöffner, wenn der Nutzer selbst nur **5–10 Minuten** pro Lead braucht
(Prüfen, Abstimmen, Antwort schicken) und die KI den Rest in einem Lauf schafft. Mit Laufzeit der KI
sind das je nach Demo-Art 10–30 Minuten (Spalte „Aufwand“). Die Cold-Mail verspricht „morgen
fertig“; der Aufwand fällt erst an, wenn jemand antwortet.

## Der Katalog

| Deliverable (so steht es im Offer) | Bau-Skill | Aufwand pro Lead | Kosten | Grenzen |
|---|---|---|---|---|
| Entwurf einer neuen Startseite / Website, auch mit Buchungs- oder Anfrage-Bereich | `demo-webseite` | 15–30 Min. | keine (Netlify-Gratisplan, ca. 20 Veröffentlichungen pro Monat) | Buchung und Formulare sind im Entwurf nur Ansicht, keine echte Funktion |
| Landingpage für ein Angebot oder eine Aktion | `demo-webseite` | 15–25 Min. | keine | wie oben |
| Die Suchbegriffe, bei denen die Firma knapp hinter Seite 1 steht, mit je einem Hebel | `demo-seo` | 10–20 Min. | RankM8-Credits (etwa 10–30 je Lead) | braucht RankM8-Verbindung |
| Neue Title-Tags und Meta-Beschreibungen für die wichtigsten Seiten | `demo-seo` | 10 Min. | keine | ohne RankM8 ohne Suchvolumen |
| Lage in der lokalen Google-Suche (Kartenbereich) für 2–3 Suchbegriffe | `demo-seo` | 10 Min. | RankM8-Credits (etwa 5 je Suchbegriff) | braucht RankM8-Verbindung |
| Sichtbarkeit in KI-Suchmaschinen: was ChatGPT & Co. davon abhält, die Firma zu nennen, plus fertige `llms.txt` | `demo-seo` | 10–15 Min. | keine | keine Messung echter KI-Antworten, nur die Voraussetzungen |
| 3 fertige Werbeanzeigen (Meta oder Google) mit Texten und Bildideen | `demo-anzeigen` | 15–20 Min. | keine; Bildgenerierung optional mit Freigabe | keine Schaltung, kein Werbekonto |
| Fertige Stellenanzeige / Recruiting-Anzeige | `demo-anzeigen` | 15 Min. | keine | Gehaltsangaben nur vom Lead |
| Lead-System, das schon 30–50 passende Wunschkunden für den Lead gefunden hat (das System framen, nicht „ich schicke dir Leads“) | `demo-leadliste` | 20–30 Min. | Scraping-Kosten im Konto des Nutzers (harter Deckel 2 $) | nur Firmendaten, keine Privatpersonen |
| Fertige Akquise-Kampagne: Zielgruppe, Offer, Mail-Sequenz, 3 personalisierte Beispiel-Mails | `demo-akquise-kampagne` | 25–30 Min. | keine (optional Leadliste) | nichts wird versendet |
| 30-Tage-Content-Plan (Social Media, Blog) | `demo-anzeigen` (Abschnitt Content-Plan) | 15 Min. | keine | Themen nur aus belegten Leistungen |

## Nicht als Skill lieferbar (ehrlich sagen)

| Offer | Warum nicht | Was stattdessen |
|---|---|---|
| Persönliches Video mit Hebeln (Loom o. Ä.) | Aufnahme macht der Nutzer selbst | Skript mit `demo-seo` oder `demo-webseite` vorbereiten lassen, dann aufnehmen |
| Passende Bewerber oder Lebensläufe (Shortlist) | nur mit eigenem Kandidatenpool des Nutzers (Recruiting), kein KI-Skill; Personendaten | ohne Pool: `demo-anzeigen` (Stellenanzeige oder Recruiting-Kampagne) |
| Eingerichtetes Werbekonto / Tracking | braucht Zugang des Leads | `demo-anzeigen` mit Kampagnen-Struktur |
| Förder-Einschätzung | Fachwissen und Haftung beim Nutzer | nur mit Angaben des Nutzers, nie als Zusage |
| Alles mit „Analyse“, „Audit“, „Potenzial-Check“, „Erstgespräch“, „Beratung“, „Strategiegespräch“ | verboten als Offer | in ein fertiges Ergebnis umformulieren (siehe unten) |

## Vom Prüf-Wort zum fertigen Ergebnis

| Statt … | besser … | Bau-Skill |
|---|---|---|
| kostenlose SEO-Analyse | die 5 Suchbegriffe, bei denen du auf Seite 2 stehst, und was jeweils fehlt | `demo-seo` |
| Website-Check | ein Entwurf, wie die Startseite aussehen könnte | `demo-webseite` |
| Ads-Audit | 3 fertige Anzeigen für dein stärkstes Angebot | `demo-anzeigen` |
| Potenzial-Check Neukunden | ein Lead-System, das schon 40 Firmen in deiner Region gefunden hat, die genau zu dir passen | `demo-leadliste` |
| Beratung zur Kaltakquise | eine fertige Mail-Sequenz mit 3 Beispiel-Mails an echte Wunschkunden | `demo-akquise-kampagne` |

Die endgültige Formulierung (Karte, Überleitung, Feinheiten-Satz) macht `outreach-copy`.

## Unbekanntes Offer: Machbarkeits-Check

Für ein Offer, das in keiner Zeile steht, vier Fragen beantworten:

1. **Ist es ein fertiges Ding?** Kann man es als Datei, Seite oder Liste übergeben? Wenn nein, ist es
   ein Gespräch, kein Offer.
2. **Reichen öffentliche Daten?** Website, Google-Profil, Bewertungen, Social Media, Impressum.
   Braucht es Zugänge oder interne Zahlen des Leads, ist es kein Türöffner.
3. **Schafft die KI den Großteil, so dass dem Nutzer 5–10 Minuten bleiben?** Text, Struktur, HTML, Tabellen, Bildideen: ja.
   Fotos vor Ort, Videos mit Gesicht, Messungen im Konto des Leads: nein.
4. **Führt es zur Dienstleistung des Nutzers?** Das Deliverable ist ein Stück dessen, was er
   später verkauft, nicht ein beliebiges Geschenk.

Drei Ja und Frage 4 ja: machbar, mit dem nächstliegenden Bau-Skill bauen (meist `demo-webseite`
als Hülle für die Darstellung). Sonst dem Nutzer eine Alternative aus dem Katalog vorschlagen.
