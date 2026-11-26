---
name: datenbeschaffung-referenzen
description: Dieses Referenzpaket wird von Datenbeschaffungs-Master und Weg-Skills gelesen. Enthält die DealSupply-MCP-Referenz für Import und Bestand (import_leads, check_leads_exist, export_leads, Listen), den Weg ohne DealSupply bis zur Datei für Instantly, den manuellen Ablauf mit eigenem Apify- oder Outscraper-Konto (Actors, Zugriff, Kosten), CSV-Format, ICP, Ziele außerhalb DACH, Personalisierungs-Hebel und Hilfsskripte. Kein direkter Einstieg.
---

# Datenbeschaffung: Referenz-Paket

Kein eigenständiger Skill, sondern die geteilte Wissensbasis der Datenbeschaffungs-Familie.
Wird zusammen mit den anderen Skills installiert; Master, Weg-Skills und `listen-qualitaet`
lesen von hier (`references/`). In den Wegen dieses Plugins scrapt der Kunde mit eigenem Apify- oder
Outscraper-Konto außerhalb von DealSupply (lokale Betriebe und Entscheider findet DealSupply ab MCP 4.16.0
auch selbst: `outreach-leads-finden`, `outreach-personensuche` im Plugin outreach), bereinigt die Ergebnisse und importiert sie als CSV über die
Oberfläche oder per MCP `import_leads`. Für die DealSupply-Seite zuerst `references/dealsupply-mcp.md` lesen.
Ohne DealSupply-Konto endet der Weg mit einer Datei für Instantly: `references/ohne-dealsupply.md`.

Preise in `kosten.md` und `apify-actors.md` sind Richtwerte mit Prüfdatum; vor jedem Lauf den aktuellen
Preis beim Anbieter prüfen und freigeben lassen.

| Datei | Inhalt |
|---|---|
| `references/dealsupply-mcp.md` | DealSupply-MCP: Import- und Bestands-Tools mit Parametern, Job-Report und Fehlern; Workspace-Regel für Abgleich und Import |
| `references/setup.md` | Apify-Zugang des Kunden verbinden, Token-URL, Selbsttest |
| `references/zugriff.md` | Zugriffsschicht: Actor via MCP / REST / CLI, Kosten-Deckel-Regeln |
| `references/apify-actors.md` | Gepinnte Actors je Kategorie mit Beleg + Prüfdatum |
| `references/kosten.md` | Belegte Actor-Kosten + Daumenregeln + Kostenfallen |
| `references/staedte.md` | DACH-Städtelisten + Pilotstadt-Regeln |
| `references/noise-domains.md` | DIE Ausschlussliste (SERP-Filter, domainBlacklist, -site:) |
| `references/ohne-dealsupply.md` | Der ganze Weg ohne DealSupply-Konto: was entfällt und was es ersetzt, Sperrliste aus dem CRM, Datei und Blocklist für Instantly, Import in Instantly |
| `references/ausserhalb-dach.md` | Ziele außerhalb DACH: was belegt ist, Kontaktweg, Einstellungen je Werkzeug, Grenzen |
| `references/personalisierung.md` | Personalisierungs-Hebel je Weg aus dem Kurshandbuch und die Spalten, die sie tragen |
| `references/datenumfang.md` | Was je Quelle beschafft und hochgeladen wird und was die Plattform selbst übernimmt; Kontaktlücke (vorab anreichern oder der Recherche überlassen), Recherche-Stufe |
| `references/csv-spalten.md` | DAS CSV-Format (deckungsgleich mit dem App-Import) |
| `references/plattform-hosts.md` | Wann eine Website keine eigene Website ist (Profil-Plattformen, Baukästen); Spiegel der Server-Liste für `build_csv.py` |
| `references/icp.md` | ICP-Satz, Anti-ICP, Filter-Dimensionen, Trichter-Prinzip |
| `references/listen-und-icp.md` | Von der Zielgruppe zur versandfähigen Liste: Quellen außerhalb der Weg-Skills, Qualitäts-Check, Datenqualität vor dem Import, Sperrliste, Volumenplanung |
| `references/erfahrungswerte.md` | Belegte Query-Trefferquoten (wächst mit jedem Lauf) |
| `references/outreach-uebergabe.md` | Übergabe in DealSupply: Bestandsabgleich, Liste, Import, CSV-Weg |
| `scripts/build_queries.py` | Suchbegriffe × Städte + -site:-Ausschlüsse |
| `scripts/process_serp.py` | SERP-JSON → eindeutige Firmen-Domains (Noise gefiltert) |
| `scripts/build_csv.py` | Rohdaten (JSON oder CSV) → CSV-Format mit den Zusatzspalten aus `datenumfang.md` (Google-Bewertungen und Rezensionen, Inhaber, Plattformfelder), Wahl der Versandadresse, Firmennamen-Normalisierung, Hinweise; Übergabe-CSV mit `--uebergabe kontakt` (E-Mail oder eigene Website) bzw. `email` (ältere Server), verworfene Zeilen per `--verworfen` |
| `scripts/sperrliste.py` | Ohne DealSupply: Sperrliste aus CRM-Exporten (Domains statt Firmenadressen), Blocklist-Datei für Instantly, gesperrte Zeilen aus der Lead-Liste nehmen |
| `scripts/instantly_csv.py` | Fertige Liste → Datei für den CSV-Import in Instantly (Spaltennamen nach den Regeln von Instantly, Vorname aus dem Inhaber, wo eindeutig) |
| `scripts/dedup.py` | Vorab-Abgleich gegen den Bestandsindex über Adressen und Domains (do_not_contact hart, Leads ohne E-Mail über die Website) |
| `scripts/omr_products.py` | OMR Reviews: alle Software-Produkte über die öffentliche Schnittstelle, kostenlos (Weg F) |
| `scripts/startbase_saas.py` | Startbase: deutsche B2B-SaaS mit Rechtsträger, Ort, Teamgröße, kostenlos (Weg F) |
| `scripts/linkedin_saas.py` | LinkedIn-Firmensuche: Segmente zusammenlegen, Sitzfilter, Tabelle zum Einordnen, Details-Input (Weg F) |
| `scripts/website_suche.py` | Website zu Firmen ohne Domain über die Google-Suche finden (Rechtsträger + Ort) |
| `scripts/quellen_zusammenfuehren.py` | Mehrere Quellen auf die Domain zusammenführen, Herkunft in `quellen` |
| `scripts/sitz_check.py` | Firmensitz, PLZ, Ort, Impressum-Adresse und Produkt-Signale je Website, kostenlos und lokal |
