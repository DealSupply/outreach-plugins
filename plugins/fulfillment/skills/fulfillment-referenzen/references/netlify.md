# Veröffentlichen mit Netlify

> Referenz zu `demo-ausliefern`. Stand der Angaben: 12.10.2026 (Netlify-Doku). Vor dem ersten Einsatz
> beim Nutzer kurz prüfen, ob sich Abläufe geändert haben.

## Voraussetzung: Netlify-Konto

Ohne Konto veröffentlichte Seiten sind passwortgeschützt und werden **nach einer Stunde entfernt**,
wenn niemand sie übernimmt. Für Demos, die der Lead in Ruhe ansehen soll, braucht der Nutzer ein
Konto (netlify.com, Anmeldung mit E-Mail oder GitHub). Einmal einrichten, dann für alle Demos nutzen.

**Gratisplan reicht für etwa 20 Veröffentlichungen im Monat** (300 Credits, 15 je Veröffentlichung
inkl. jeder Aktualisierung; Stand 10/2026). Sind die Credits aufgebraucht, pausieren die Projekte bis
zum nächsten Monat. Wer mehr Demos verschickt: Personal-Plan (rund 9 $ im Monat, etwa 66
Veröffentlichungen) oder Demos nach 30 Tagen konsequent löschen. Änderungen am Entwurf möglichst
gesammelt veröffentlichen statt nach jeder Kleinigkeit.

## Drei Wege, vom einfachsten zum schnellsten

### 1. Netlify Drop (No-Code, jede Umgebung)

1. Bei Netlify einloggen.
2. Einen Ordner anlegen, z. B. `entwurf-mueller-dach`, darin `index.html` (optional `_headers`, siehe unten).
3. Den Ordner auf **https://app.netlify.com/drop** ziehen.
4. Netlify zeigt die Adresse (`zufallsname.netlify.app`). Unter Project configuration → Change
   project name einen schwer erratbaren Namen setzen (Schema unten).
5. **Aktualisieren:** im Projekt unter „Deploys“ den geänderten Ordner erneut hineinziehen.

### 2. Netlify-Connector (claude.ai, Claude App, Claude Code)

Netlify hat einen offiziellen Connector (MCP-Server `https://netlify-mcp.netlify.app/mcp`).
- **claude.ai / App:** Customize → Connectors → Netlify hinzufügen → im Browser bei Netlify anmelden.
- **Claude Code:** `claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp`,
  danach `/mcp` zum Anmelden.

Damit kann die KI ein Projekt anlegen und die Dateien direkt veröffentlichen. Vor dem Veröffentlichen
den Projektnamen nach dem Schema unten setzen und dem Nutzer zeigen, was veröffentlicht wird.
Ob der Connector in claude.ai Dateien ohne lokalen Ordner hochladen kann, beim ersten Mal prüfen;
klappt es nicht, Netlify Drop nehmen.

### 3. Netlify CLI (Claude Code, Codex)

```bash
npx netlify-cli login                                   # einmalig, öffnet den Browser
npx netlify-cli deploy --create-site <projektname> --dir <ordner> --prod
# Aktualisieren:
npx netlify-cli deploy --dir <ordner> --prod --site <projektname>
```

Die Befehle vor dem Ausführen nennen. Melden die Optionen einen Fehler (Versionen ändern sich),
`npx netlify-cli deploy --help` lesen und anpassen, nicht raten.

## Pflicht in jeder Demo

**Nicht indexierbar:**

- **Pflicht** im `<head>` jeder HTML-Seite: `<meta name="robots" content="noindex, nofollow">`
- **Zusätzlich**, wenn die KI die Dateien selbst schreibt (Claude Code, Codex, Cowork): Datei
  `_headers` im selben Ordner. Sie schützt auch Dateien ohne HTML (z. B. Bilder):

```
/*
  X-Robots-Tag: noindex, nofollow
```

Legt der Nutzer `_headers` von Hand an: Die Datei heißt genau `_headers`, ohne Endung. TextEdit
(Mac) und Editor (Windows) hängen gern `.txt` an; dann ignoriert Netlify sie still. Im Zweifel
weglassen, das Meta-Tag reicht für eine HTML-Demo. Listen (CSV) nie über Netlify veröffentlichen.

**Schwer erratbare Adresse:** `entwurf-<firma-kurz>-<6 zufällige Zeichen>`, z. B.
`entwurf-mueller-dach-k7q2xm`. Nur Kleinbuchstaben, Ziffern, Bindestriche; Umlaute umschreiben
(ü → ue), weil Adressen keine Umlaute tragen.

**Kein Tracking**, keine Analyse-Skripte, keine Cookies in Demos.

## Aufräumen

Demos ohne Auftrag nach spätestens 30 Tagen löschen (Netlify: Project configuration → Delete
project). Der Nutzer führt eine kurze Liste (Lead, Adresse, Datum); `demo-ausliefern` erinnert daran.
Bei Auftrag die Demo nicht weiterverwenden, sondern das echte Projekt neu aufsetzen.
