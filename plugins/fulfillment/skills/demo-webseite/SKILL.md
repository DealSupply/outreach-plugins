---
name: demo-webseite
description: Baut einen Webseiten-Entwurf für einen Lead aus seiner bestehenden Website. Verwenden bei „Demo-Webseite“, „Webseitenentwurf für den Lead“, „Startseite für … bauen“, „Website-Vorschau“, „Landingpage-Entwurf“, „Entwurf wie versprochen“ oder wenn das Offer der Kampagne ein Website-Entwurf ist. Ergebnis ist eine fertige index.html (überall machbar, auch ohne Programmierkenntnisse), danach geht es an demo-ausliefern.
---

# Demo-Webseite

Aus der Website eines Leads einen modernen Entwurf bauen, der genau das zeigt, was die Cold-Mail
versprochen hat. Ziel: Der Lead sieht seine eigene Firma, besser dargestellt, in unter einer Minute.

Wissen dazu (alle unter `../fulfillment-referenzen/references/`): `webseiten-bauplan.md` (Aufbau, Gestaltung,
Technik), `qualitaet.md`, `recht-und-grenzen.md`, `umgebungen.md`, `netlify.md`.

## Eingaben

- **Offer und On-Top-Detail** aus der Kampagne (über `fulfillment` oder `export_campaign_blueprint`)
- **Lead:** Firma, Website, Ort, Telefon aus `list_leads` (siehe `lead-kontext.md`) oder Website-Adresse
  vom Nutzer. Für angeschriebene Leads liefert `get_lead_data` nichts (`contact_gate`).
- **Absender:** Firma und Name des Nutzers (für die Entwurfs-Leiste)

Fehlt das Offer, fragen: „Was genau hast du versprochen? Ganze Website, Startseite oder Landingpage,
und mit welchem Extra?“

## Ablauf

### 1. Steckbrief (5 Min.)

Website des Leads lesen: Startseite, Leistungen, Über-uns, Kontakt, Impressum. Dazu das
Google-Profil (Bewertungen) und, falls der Nutzer ihn hineinkopiert, den Recherche-Bericht aus der App. Steckbrief nach Abschnitt 1 des Bauplans schreiben und dem
Nutzer zeigen, Lücken markieren. Bilder und Logo mit Thema auflisten.

### 2. Struktur festlegen (2 Min.)

Abschnitte nach Abschnitt 2 des Bauplans wählen, passend zur Branche. Das On-Top-Detail aus dem
Feinheiten-Satz bekommt einen eigenen, sichtbaren Abschnitt. Dem Nutzer in einer Zeile nennen:
„Startseite mit Hero, Leistungen, Bewertungen, Buchungsbereich, FAQ, Kontakt.“

### 3. Bauen (10–15 Min.)

Eine `index.html` nach Abschnitt 3 und 4 des Bauplans:

- Entwurfs-Leiste oben, `noindex` im `<head>`
- Texte neu formuliert aus dem Steckbrief. Die Website spricht die **Kunden des Leads** an, also
  die Anrede, die der Lead auf seiner eigenen Seite nutzt (nicht die Anrede der Kampagne)
- Farben aus dem Logo abgeleitet, Systemschriften
- Bilder: in Umgebungen mit Dateisystem herunterladen und verkleinern (`bilder/`); sonst wenige,
  die der Nutzer ablegt, oder Farbflächen
- Bei „Google und KI-Suchmaschinen“ im Offer: Abschnitt 5 des Bauplans vollständig umsetzen

Ablage: Ordner `entwurf-<firma-kurz>/` mit `index.html`, `_headers` (wenn die KI Dateien schreiben
kann, siehe `netlify.md`), `bilder/` und Logo. Ohne Dateisystem: Datei zum Herunterladen bzw. HTML-Code-Block mit Speicher-Anleitung
(`umgebungen.md`).

### 4. Prüfen (3 Min.)

Alle Punkte aus `../fulfillment-referenzen/references/qualitaet.md` (harte Punkte und Webseiten-Punkte). In Claude Code mit
Browser-Werkzeug Screenshots bei 375 px und 1280 px ansehen. Ergebnis als kurze Liste zeigen.

### 5. Abstimmen

Den Entwurf dem Nutzer zeigen (Screenshot oder lokale Datei öffnen lassen). Korrekturen: **genau
das ändern, was gesagt wird, sonst nichts**, danach erneut zeigen. Erst nach seinem Okay weiter.

### 6. Übergabe

`demo-ausliefern` laden: veröffentlichen, Link am Lead speichern, Antwort-Text.

## Grenzen

- Keine Funktionen (Formulare, Buchung, Shop); alles Interaktive ist als Ansicht gekennzeichnet.
- Kein Klon der alten Seite mit neuen Farben: Struktur und Texte werden neu gedacht.
- Keine Inhalte, die der Lead nicht hat (Team-Mitglieder, Leistungen, Preise, Auszeichnungen).
- Mehrseitige Entwürfe nur, wenn das Offer sie verspricht (Bauplan, Abschnitt 4).
