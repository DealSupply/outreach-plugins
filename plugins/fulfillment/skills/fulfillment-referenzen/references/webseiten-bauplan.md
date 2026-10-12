# Webseiten-Bauplan für Demos

> Referenz zu `demo-webseite` (auch genutzt von `demo-seo` und `demo-anzeigen` als Hülle für die
> Darstellung). Erfahrungswerte aus über 60 gebauten Demo-Seiten: was Interessenten überzeugt und
> welche Korrekturen am häufigsten nötig waren.

## 1. Steckbrief: erst sammeln, dann bauen

Vor der ersten Zeile Code einen Steckbrief schreiben (dem Nutzer zeigen, Lücken markieren):

| Feld | Quelle |
|---|---|
| Firmenname (exakt wie im Impressum), Inhaber | Impressum, Über-uns |
| Telefon, E-Mail, Adresse, Öffnungszeiten | Kontakt, Footer, Google-Profil |
| Leistungen einzeln mit Kurzbeschreibung (und Preis, falls öffentlich) | Leistungsseiten |
| Das, was diese Firma abhebt (eigenes Konzept, Spezialisierung, Auszeichnung) | Website, Recherche-Bericht aus der App (per Kopie) |
| Lob aus Bewertungen, sinngemäß, mit Anzahl und Schnitt | Google-Profil, Import-Attribute |
| Farben (Logo-Hauptfarbe, Knopf-Farbe der alten Seite) | Logo, Website |
| Logo-Datei (höchste Auflösung, SVG oder PNG) | Header der Website |
| Bilder der Website mit Thema (Team, Räume, Arbeit, Produkte) | alle Unterseiten |
| Social-Media-Profile | Footer, Header |

**Regel:** Was nicht im Steckbrief steht, kommt nicht auf die Seite. Fehlt etwas Wichtiges (z. B.
Öffnungszeiten), lieber den Abschnitt weglassen als etwas erfinden.

Seiten, die nur mit JavaScript laden (Wix, Jimdo, manche Baukästen), liefern beim einfachen Abruf
oft wenig Text. Dann einen Browser nutzen, falls vorhanden, oder den Nutzer um die Inhalte bitten.

## 2. Aufbau der Startseite

Reihenfolge für Dienstleister (anpassen, nicht stur abarbeiten):

1. **Entwurfs-Leiste** (schmal, oben): „Entwurf von [Absender] für [Firma]. Nicht die offizielle Website.“
2. **Kopfzeile:** Logo, 3–5 Menüpunkte (Anker-Links), Haupt-Knopf (anrufen, anfragen oder buchen)
3. **Hero:** echtes Foto als Hintergrund mit Abdunklung (35–60 %), Überschrift mit Leistung und Ort,
   ein Satz Nutzen, Haupt-Knopf, darunter ein Vertrauens-Anker (z. B. „4,9 aus 180 Google-Bewertungen“)
4. **Leistungen:** 3–6 Leistungen mit konkretem Satz statt Floskel
5. **Das Besondere:** der Anker, der diese Firma abhebt (aus Recherche oder Bewertungen)
6. **Stimmen:** 2–3 sinngemäße Aussagen aus Bewertungen ohne Namen, mit Quelle „aus Google-Bewertungen“
7. **Ablauf:** 3 Schritte bis zum Ergebnis (Anfrage, Termin, Ergebnis)
8. **Das On-Top-Detail aus dem Offer** (z. B. Buchungsbereich, FAQ für KI-Suchmaschinen), sichtbar
9. **Kontakt:** Adresse, Öffnungszeiten, Telefon, E-Mail, Link „Route in Google Maps“
10. **Fußzeile:** Entwurfs-Hinweis und Link zum **Impressum des Absenders** (die Demo betreibt der
    Absender, nicht der Lead); keine Impressums- oder Datenschutzangaben des Leads als eigene ausgeben

**Buchungs- oder Anfrage-Bereich** als reine Ansicht: Auswahl von Leistung, Tag und Uhrzeit sichtbar,
Knopf ohne Funktion mit Hinweis „Im Entwurf ohne Funktion“. Kein Formular, das Daten sendet.

## 3. Gestaltung

- **Farben:** Logo-Hauptfarbe als Primärfarbe. Daraus ableiten (HSL): dunklere Variante
  (Sättigung +10, Helligkeit −15) für Hover, sehr helle Variante (gleicher Farbton, Sättigung 5–10 %,
  Helligkeit 95–97 %) für Hintergründe von Abschnitten. Text fast schwarz (#1a1a1a), nie reines Grau
  auf Weiß unter Kontrast 4,5:1.
- **Schriften:** Systemschriften (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`) oder eine
  lokal eingebundene Schrift. Keine Einbindung von Google-Servern.
- **Abwechslung:** nicht jeder Abschnitt als Kachel-Raster. Wechsel aus Bild-Text-Split, Liste,
  Zitat, Zahlenreihe.
- **Hero:** immer echtes, passendes Foto (vom Lead), nie nur ein Farbverlauf; bei fehlenden Fotos
  eine ruhige Farbfläche mit großer Typografie statt eines unpassenden Stockbilds.
- **Kopfzeile beim Scrollen:** fest oben, mit Hintergrundfarbe ab dem ersten Scrollen; Text muss in
  jedem Zustand lesbar sein.

## 4. Technik

**Standard: eine einzige `index.html`** mit eingebettetem CSS und höchstens wenig JavaScript.
Läuft in jeder Umgebung, lässt sich per Drag & Drop veröffentlichen und braucht keinen Build.

- Bilder: Adressen der Website des Leads nicht direkt verlinken (Hotlinking bricht oft). In
  Umgebungen mit Dateisystem die Bilder herunterladen, verkleinern (max. 1600 px Breite, unter
  400 KB) und in einen Ordner `bilder/` legen. Ohne Dateisystem: wenige Bilder, die der Nutzer selbst
  in den Ordner legt, oder Farbflächen.
- Logo als Datei neben `index.html`; fehlt es, Firmenname als Schriftzug.
- Mobile zuerst bauen (375 px), dann für breite Bildschirme erweitern.
- Kein Framework, keine externen Skripte, keine Cookies.

**Mehrseitig (optional, Claude Code):** Für Entwürfe mit mehreren Unterseiten kann ein Astro-Projekt
sinnvoll sein (`npm create astro@latest`, statische Ausgabe, `npm run build`, Ordner `dist/`
veröffentlichen). Nur, wenn das Offer mehrere Seiten verspricht.

## 5. Google und KI-Suchmaschinen (oft das On-Top-Detail)

Wenn das Offer „Optimierung für Google und KI-Suchmaschinen“ verspricht, sichtbar umsetzen:

- `<title>` mit Leistung und Ort (50–60 Zeichen), `<meta name="description">` (140–160 Zeichen)
- genau eine `<h1>`, sinnvolle `<h2>`-Gliederung
- strukturierte Daten als JSON-LD (`LocalBusiness` bzw. passender Untertyp) mit echten Daten:
  Name, Adresse, Telefon, Öffnungszeiten, Website. **Keine** Bewertungen (`aggregateRating`) aus
  Google-Bewertungen in die strukturierten Daten: Google erlaubt das nicht für Bewertungen über das
  eigene Unternehmen. Bewertungen gehören sichtbar in den Text.
- FAQ-Abschnitt mit 4–6 echten Fragen, sichtbar auf der Seite. Er hilft Besuchern und
  KI-Suchmaschinen; besondere Darstellung in Google (FAQ-Rich-Results) nicht versprechen, die zeigt
  Google seit 2023 kaum noch.
- Alt-Texte für alle Bilder
- Abschnitte, die eine Frage direkt in 2–3 Sätzen beantworten (zitierbar für KI-Antworten)

Den Nutzer darauf hinweisen: In der Demo steht `noindex`; die Optimierung wirkt erst auf der echten Seite.

## 6. Häufigste Korrekturen (vorher vermeiden)

| Korrektur | Vermeidung |
|---|---|
| Reste eines anderen Kunden (Namen, Texte) | jede Seite neu aus dem Steckbrief schreiben, nie eine fremde Demo umbauen; am Ende nach fremden Firmennamen suchen |
| „Der Hero gefällt mir nicht“ | echtes, passendes Foto, Abdunklung, kurze Überschrift |
| „Die Bilder passen nicht“ | jedes Bild auf Passung prüfen; lieber weniger, aber passende |
| Text auf Kopfzeile unlesbar | Kopfzeile in allen Zuständen prüfen (oben, beim Scrollen) |
| Leistungen wirken gleichförmig | wechselnde Darstellung, konkrete Sätze |
| Bei Korrekturen wird nebenbei anderes geändert | **genau das ändern, was der Nutzer sagt, sonst nichts**; danach Ergebnis zeigen |
