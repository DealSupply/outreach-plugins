# Qualitätsprüfung vor dem Veröffentlichen

> Referenz für alle `demo-*`-Skills. Erst wenn alle harten Punkte erfüllt sind, geht die Demo an
> `demo-ausliefern`. Ergebnis der Prüfung dem Nutzer kurz als Liste zeigen.

## Harte Punkte (alle Demo-Arten)

| Prüfung | Woran erkennbar |
|---|---|
| Keine Platzhalter | kein `[`, `{{`, „Lorem“, „Beispiel GmbH“, „XXX“, „TODO“ im sichtbaren Text (Ausnahmen: die ausdrücklich markierten Beispiel-Platzhalter und Variablen in `demo-akquise-kampagne` und Markdown-Links in einer `llms.txt`) |
| Firma, Ort, Telefon, E-Mail stimmen | Abgleich mit der Website des Leads, Zeichen für Zeichen |
| Nichts erfunden | jede Zahl, jede Bewertung, jeder Preis, jede Auszeichnung hat eine Quelle (Website, Google-Profil, Recherche) |
| Echte Umlaute | „ä ö ü ß“ statt „ae oe ue ss“ (Ausnahme: Web-Adressen) |
| Keine Gedankenstriche als Satzzeichen | kein „ – “, „ — “ und kein „ - “ (Bindestrich mit Leerzeichen) im Fließtext |
| Versprechen erfüllt | Offer aus der Kampagne und On-Top-Detail aus dem Feinheiten-Satz sind sichtbar umgesetzt |
| Entwurfs-Hinweis vorhanden | Demo ist als Entwurf von [Absender] erkennbar (siehe `recht-und-grenzen.md`) |
| `noindex` gesetzt | Meta-Tag in jeder HTML-Seite, `_headers` wenn die KI die Dateien schreibt (siehe `netlify.md`) |
| Keine Namen aus Rezensionen | Lob nur sinngemäß, ohne Verfasser |

## Zusätzlich bei Webseiten

| Prüfung | Woran erkennbar |
|---|---|
| Handy-tauglich | bei 375 px Breite kein seitliches Scrollen, Text ab 16 px, Knöpfe mindestens 44 px hoch |
| Kontrast | heller Text nur auf dunklem Grund und umgekehrt; kein grauer Text auf Bild ohne Abdunklung |
| Ein Ziel | ein Haupt-Knopf (anrufen, anfragen, buchen), überall derselbe Text |
| Ladezeit | keine Bilder über 400 KB, keine externen Frameworks |
| Links funktionieren | Telefon als `tel:`, E-Mail als `mailto:`, Anker-Links springen an die richtige Stelle |
| Schriften datenschutzfreundlich | keine Google-Fonts-Einbindung von Google-Servern (Systemschriften oder lokal eingebunden) |

In Claude Code mit Browser-Werkzeug: Seite einmal bei 375 px und bei 1280 px Breite ansehen
(Screenshot) und prüfen. Ohne Browser: Code-Prüfung der Punkte und den Nutzer bitten, die Seite
einmal auf dem Handy zu öffnen.

## KI-typische Fehler vermeiden

- Überschriften wie „Willkommen bei …“, „Ihr Partner für …“, „Qualität, die überzeugt“
- Drei gleich gebaute Kacheln mit Symbol, Überschrift, Floskel
- Superlative ohne Beleg („die besten“, „einzigartig“, „erstklassig“)
- Erfundene Statistiken („über 1.000 zufriedene Kunden“) und erfundene Kundenstimmen
- Englische Füllwörter in deutschen Texten („Excellence“, „Experience“)

Lieber konkret aus dem Lead: echte Leistung, echter Ort, echtes Lob aus Bewertungen, echte Zahl.
