# Umgebungen: was wo geht

> Referenz zu `fulfillment`. Die Skills sind für alle KI-Werkzeuge geschrieben. Claude Code kann am
> meisten; mit claude.ai und einem No-Code-Weg kommt man trotzdem ans Ziel.

## Umgebung erkennen

- **Claude Code / Codex CLI:** Shell und Dateisystem vorhanden (Dateien schreiben, Befehle ausführen).
- **Claude App / claude.ai / Cowork:** keine Shell; Dateien entstehen als Download bzw. im
  Arbeitsordner (Cowork); Websites lesen über die Websuche/Abruf-Funktion; Connectors (MCP).
- **ChatGPT Desktop / Codex App:** ähnlich wie claude.ai, Plugins über den Marketplace.
- **Andere KI-Werkzeuge (Cursor, Gemini, …):** Skills per `npx skills add`; Verbindung zur
  Outreach-App separat.

In einem Satz nennen, welche Umgebung erkannt wurde, und den passenden Weg wählen.

## Was je Umgebung geht

| Aufgabe | Claude Code | claude.ai / App / Cowork | andere KI ohne Werkzeuge |
|---|---|---|---|
| Website des Leads lesen | Abruf-Werkzeug oder `curl` | Websuche/Abruf | Nutzer kopiert Inhalte hinein |
| Demo-Datei erzeugen | Datei im Projektordner | Datei zum Herunterladen (Cowork: im Ordner) | Code-Block, Nutzer speichert als `index.html` |
| Veröffentlichen | Netlify CLI oder Netlify-Connector | Netlify-Connector (beim ersten Mal testen) oder Netlify Drop | Netlify Drop |
| Link am Lead speichern | Outreach-MCP | Outreach-Connector | in der App von Hand |
| Bilder generieren | nur mit Bild-Werkzeug und Freigabe | je nach Plan | extern |

## Wenn etwas fehlt

- **Kein Website-Abruf möglich:** Nutzer bitten, die Startseite und die Leistungsseite zu öffnen
  und den Text hineinzukopieren; den Recherche-Bericht aus der App kann er ebenso hineinkopieren.
- **Keine Datei möglich:** die komplette Seite als ein HTML-Code-Block ausgeben, mit der Anweisung:
  „In eine leere Datei kopieren, als `index.html` speichern (Endung prüfen, nicht `.html.txt`), in
  einen eigenen Ordner legen und den Ordner auf app.netlify.com/drop ziehen.“
- **Keine Outreach-Verbindung:** alles geht, nur der Link wird in der App von Hand am Lead
  eingetragen (Feld `demo-url`).
