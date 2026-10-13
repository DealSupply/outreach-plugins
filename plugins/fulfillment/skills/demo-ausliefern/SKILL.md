---
name: demo-ausliefern
description: Veröffentlicht eine fertige Demo (Webseiten-Entwurf, SEO-Ergebnis, Anzeigen, Muster-Kampagne) nicht auffindbar bei Netlify, speichert den Link als demo-url am Lead in der Outreach-App und schreibt die Antwort an den Lead. Verwenden bei „Demo veröffentlichen“, „Entwurf online stellen“, „Link für den Lead“, „Demo ausliefern“, „Netlify“, „Antwort mit Link schreiben“ oder nach jedem demo-Skill.
---

# Demo ausliefern

Die fertige Demo online stellen, so dass Suchmaschinen sie nicht finden und nur hat, wer den Link
bekommt, den Link am Lead speichern und die Antwort-Mail vorbereiten. Wissen (alle unter
`../fulfillment-referenzen/references/`): `netlify.md`, `demo-link.md`, `qualitaet.md`.

## Vorher prüfen

- Qualitätsprüfung (`qualitaet.md`) ist bestanden. Wenn nicht: zurück zum Bau-Skill.
- Jede HTML-Seite enthält `<meta name="robots" content="noindex, nofollow">`. Kann die KI Dateien
  schreiben, liegt zusätzlich `_headers` im Ordner. Fehlt etwas, jetzt ergänzen.
- Entwurfs-Hinweis ist sichtbar.

## 1. Weg wählen

| Lage | Weg |
|---|---|
| Netlify-Connector verbunden (Netlify-Tools vorhanden) | Connector |
| Claude Code oder Codex mit Shell | Netlify CLI (bei erstem Mal `login`) |
| sonst (claude.ai ohne Connector, andere KI, No-Code) | Netlify Drop |

Hat der Nutzer noch kein Netlify-Konto: kurz erklären, warum es nötig ist (ohne Konto wird die Seite
nach einer Stunde entfernt) und wie es geht (netlify.com). Der Gratisplan reicht für etwa 20
Veröffentlichungen im Monat (`netlify.md`). Einmalig.

## 2. Veröffentlichen

1. Projektname nach Schema `entwurf-<firma-kurz>-<6 zufällige Zeichen>` bilden und nennen.
2. Dem Nutzer sagen, was veröffentlicht wird (Ordner, Anzahl Dateien), und bestätigen lassen.
3. Veröffentlichen nach dem gewählten Weg (`netlify.md`).
4. Adresse öffnen bzw. abrufen und prüfen: Seite lädt, Bilder sind da, `noindex` ist aktiv. In
   Claude Code: `curl -sI <adresse> | grep -i x-robots-tag` und `curl -s <adresse> | grep -i noindex`.
   Sonst: den Nutzer die Seite öffnen lassen, Rechtsklick → Seitenquelltext anzeigen, nach
   `noindex` suchen.

## 3. Link am Lead speichern

Mit Outreach-Verbindung:

```
bulk_set_lead_attributes(lead_ids=[<lead_id>], attributes={"demo-url": "<adresse>", "demo-datum": "<JJJJ-MM-TT>"}, create_missing=true)
```

Schlüssel mit Bindestrich, nie mit Unterstrich (Grund in `demo-link.md`); `attributes_created` in
der Antwort prüfen. Ohne Verbindung oder ohne Schreibrecht: Link dem Nutzer nennen, er trägt ihn in
der App am Lead ein.

## 4. Antwort an den Lead

Antwort nach `demo-link.md` schreiben: Anrede wie in der Kampagne, Link, ein Satz zum versprochenen
Detail, eine Frage. Dem Nutzer zum Kopieren geben. **Nie selbst versenden**; der Versand läuft im
Postfach des Nutzers bzw. in Instantly.

## 5. Merken und aufräumen

Dem Nutzer eine Zeile für seine Demo-Liste geben: `Firma | Adresse | Datum | Lead in der App`.
Hinweis: Demos ohne Auftrag nach 30 Tagen löschen (`netlify.md`, Abschnitt Aufräumen), dazu das
Löschdatum nennen. Fragt der Nutzer „welche Demos sind alt“, seine Demo-Liste durchgehen; in der App
stehen `demo-url` und `demo-datum` am Lead.

## Abschluss

Kurz: Adresse, `noindex` geprüft ja/nein, Link am Lead gespeichert ja/nein, Antwort-Text bereit,
Löschdatum.
