---
name: fulfillment
description: Einstieg für alles rund ums Liefern des Marketing-Offers. Verwenden bei „Fulfillment“, „Demo bauen“, „Demo für den Lead“, „Lead hat geantwortet, was jetzt“, „Offer liefern“, „Entwurf erstellen“, „welches Offer kann ich liefern“, „was kann ich als Türöffner anbieten“ oder wenn unklar ist, welcher Demo-Skill passt. Liest das Offer der Kampagne, prüft die Machbarkeit mit KI und leitet an den passenden demo-Skill weiter.
---

# Fulfillment – Einstieg

Fulfillment heißt: das Marketing-Offer aus der Cold-Mail wirklich liefern. Die Mail sagt „war so
frei und habe … erstellt“; dieser Skill sorgt dafür, dass es danach in Minuten fertig ist.

Dieser Skill baut selbst nichts. Er klärt, **was** geliefert wird und **für wen**, und lädt dann
genau einen Bau-Skill. Wissen, das alle Skills teilen, steht in
`../fulfillment-referenzen/references/`.

## Leitsätze

1. **Nur liefern, was das Offer verspricht.** Das Deliverable steht im Offer der Kampagne. Nichts
   Größeres bauen, nichts anderes nachschieben.
2. **Fertiges Ergebnis statt Gespräch.** Jede Demo ist ein greifbares Ding (Entwurf, Liste, Texte),
   nie eine „Analyse“, ein „Audit“ oder ein „Potenzial-Check“ (Regel aus `outreach-copy`).
3. **Nur belegte Fakten.** Alles über den Lead stammt aus seiner Website, öffentlichen Quellen oder
   der Recherche in der App. Keine erfundenen Zahlen, Bewertungen, Preise oder Referenzen.
4. **Nichts Kostenpflichtiges ohne Freigabe.** Credits (z. B. RankM8), Scraping-Kosten oder
   Bildgenerierung vorher beziffern und freigeben lassen.
5. **Demos sind nicht auffindbar.** Veröffentlichte Demos tragen `noindex`, einen Entwurfs-Hinweis
   und eine schwer erratbare Adresse (`demo-ausliefern`). Wer den Link hat, kann sie öffnen.
6. **Deutsch mit echten Umlauten.** Keine Gedankenstriche in Texten, die der Lead liest.

## Schritt 1: Verbindung prüfen

`list_campaigns` aufrufen (nur lesend).

- **Antwort kommt:** weiter mit Schritt 2.
- **Kein Outreach-Tool vorhanden:** Fulfillment geht trotzdem. Dann das Offer und die Website des
  Leads beim Nutzer erfragen und mit Schritt 2 weitermachen. Für die Verbindung auf
  `fulfillment-setup` verweisen.

## Schritt 2: Modus klären

Eine Frage, wenn es nicht aus dem Auftrag hervorgeht:
„Willst du ein Offer für eine Kampagne finden, oder eine Demo für einen Lead bauen, der geantwortet hat?“

### Modus A: Offer finden (vor oder beim Kampagnen-Aufbau)

1. Angebot des Nutzers kennen: aus dem Gespräch oder `export_campaign_blueprint(campaign_id)`
   (`intelligence.campaign_brief.business`, `usp`).
2. In `../fulfillment-referenzen/references/demo-katalog.md` die zwei bis drei passenden
   Demo-Arten heraussuchen, die zu seiner Dienstleistung führen und nach der Antwort schnell
   lieferbar sind (Maßstab im Katalog).
3. Je Vorschlag in einem Satz: Deliverable, Bau-Skill, Aufwand pro Lead, was es kostet.
4. Die Formulierung des Offers gehört `outreach-copy` (Karte, Überleitung, Feinheiten-Satz). Den
   gewählten Vorschlag dorthin übergeben, nicht selbst Mail-Text schreiben.

### Modus B: Demo liefern (Lead hat geantwortet)

1. **Kampagne:** `export_campaign_blueprint(campaign_id)` lesen. Das Offer steht in
   `blueprint.campaign.intelligence.offer_contract.title.value`; fehlt es, beim Nutzer erfragen.
   Das On-Top-Detail aus dem Feinheiten-Satz steht in Mail 1 (`blueprint.sequence.steps[0].body`);
   es MUSS in der Demo sichtbar umgesetzt sein, denn es wurde versprochen.
2. **Lead:** Wer hat geantwortet?
   `list_leads(campaign_id, contact_status="replied", fit_level="", research_status="", campaign_status="")`.
   Den Lead mit dem Nutzer bestätigen. Die Zeile liefert Firma, Website, Ort und Telefon.
   **`get_lead_data` lehnt angeschriebene Leads ab** (`contact_gate`); Recherche-Bericht und
   Bewertungen kommen deshalb von der Website, dem Google-Profil oder per Kopie aus der App.
   Details: `../fulfillment-referenzen/references/lead-kontext.md`.
3. **Demo-Art zuordnen** über `demo-katalog.md` und den Bau-Skill laden:

| Offer handelt von … | Bau-Skill |
|---|---|
| Webseite, Startseite, Landingpage, Relaunch, Buchungssystem auf der Website | `demo-webseite` |
| Google-Sichtbarkeit, Suchbegriffe, Title-Tags, lokale Suche, KI-Suchmaschinen | `demo-seo` |
| Werbeanzeigen (Meta, Google), Anzeigen-Konzepte, Stellenanzeigen, Recruiting-Anzeige | `demo-anzeigen` |
| fertige Liste mit passenden Kunden, Leads, Kontakten | `demo-leadliste` |
| Kaltakquise-/Outreach-System, Akquise-Kampagne, Sequenz für den Lead | `demo-akquise-kampagne` |

4. Nach dem Bau immer `demo-ausliefern`: veröffentlichen, Link am Lead speichern, Antwort-Text.

Passt das Offer in keine Zeile: Machbarkeits-Check aus `demo-katalog.md` (Abschnitt „Unbekanntes
Offer“) durchgehen und dem Nutzer ehrlich sagen, was mit KI geht und was er selbst machen muss.

## Schritt 3: Umgebung beachten

Die Skills funktionieren in claude.ai, der Claude App, Claude Code, ChatGPT/Codex und anderen
KI-Werkzeugen. Was je Umgebung geht (Datei erzeugen, Website lesen, veröffentlichen):
`../fulfillment-referenzen/references/umgebungen.md`. Ohne Dateisystem erzeugt der Bau-Skill die
Datei zum Herunterladen; der Nutzer veröffentlicht per Drag & Drop.

## Abschluss

Kurz berichten: Kampagne, Lead, Offer, gebaute Demo-Art, Link, ob der Link am Lead gespeichert ist,
was der Nutzer noch selbst tun muss (z. B. Antwort abschicken).
