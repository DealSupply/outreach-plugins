---
name: outreach-abo-lauf
description: "Führt einen Abo-Lauf aus – Leads einer Kampagne mit Agents im eigenen Claude- bzw. ChatGPT-Abo verarbeiten statt auf dem Server (keine OpenRouter-Kosten). Wird von outreach-pipeline (Laufart Abo) und outreach-verify (Prüfen im Abo) geladen; direkt verwenden bei „abo-lauf als workflow“, „workflow für leads“, „leads im workflow verarbeiten“, „abo-lauf fortsetzen“. In Claude Code als ein Workflow: Haiku baut, Sonnet prüft eine Stichprobe, Haiku bessert nach, Sonnet prüft gegen."
---

# Abo-Lauf – Leads mit Agents im eigenen Abo verarbeiten

Der Abo-Lauf ist die zweite, gleichwertige Laufart neben dem Server-Lauf (`start_lead_run`). Gleich sind
Kampagne, Stufen, Lead-Auswahl, Bericht und der nächste Schritt (Stichprobe prüfen). Anders ist nur, wer
arbeitet: Statt der Kampagnen-Agents auf dem Server bearbeitet je Lead EIN Agent in deinem KI-Tool alle
Stufen. Das kostet kein OpenRouter-Guthaben, sondern Kontingent deines Abos, und dauert etwas länger
(30 Leads ≈ 5 Minuten). Die Sitzung muss dabei offen bleiben.

Kommst du nicht über `outreach-pipeline`, zuerst dessen gemeinsame Schritte 0–2 erledigen (Umgebung und
Konfiguration, kein aktiver Lauf, Lead-Auswahl und Stufen). Dieser Skill beginnt mit fertiger Lead-Liste.

## Grundregeln

- **Ein Lead pro Agent, immer.** Nie mehrere Leads in einen Agenten geben, Modelle verwechseln sonst Leads.
- **Modelle:** Der `lead-agent` läuft auf **Haiku** (baut und bessert nach), der `verify-agent` auf
  **Sonnet** (prüft). Wer gebaut hat, prüft nie selbst. Nie das Modell der Sitzung erben lassen: Opus
  verbraucht das Kontingent um ein Vielfaches. Nennt der Nutzer ein anderes Modell, nur das Bau-Modell ändern.
- **Die Steuerung kostet mehr als die Agents**, wenn jede Agent-Meldung einzeln in der Sitzung ankommt.
  Darum in Claude Code immer als **Workflow**: Die Sitzung startet ihn einmal und liest am Ende ein
  Ergebnis. Während er läuft, nichts weiter tun und nicht nachfragen; die Meldung kommt von selbst.
- Kein Status wird freigegeben: Der Lauf endet bei `pending_review`; freigeben entscheidet der Nutzer
  (`outreach-verify`).

## Ablauf

1. **Fortschritt anmelden** (wenn `outreach_progress` verfügbar): je einmal
   `outreach_progress(action="start", campaign_id, phase=…, total=<Leads>)` für die gebuchten Stufen
   (`qualification`, `research`, `email`). Das Band zählt die Schreibaufrufe der Agents selbst.
2. **Ausführen**, je nach Client:
   - **Claude Code (Werkzeug `Workflow` vorhanden):** das Skript unten mit `args` starten. Dieser Skill ist
     die ausdrückliche Anweisung dazu, eine weitere Freigabe braucht es nicht.
   - **Ohne Workflow, mit Subagents** (Cowork, ältere Clients): je Lead ein `outreach:lead-agent` mit dem
     Auftrag aus `auftrag()` unten und `model: "haiku"`, `run_in_background: true`, höchstens 10 gleichzeitig,
     eine Welle je Nachrichtenblock. Danach die Stichprobe wie in `outreach-verify`.
   - **Ohne `outreach:lead-agent`:** `general-purpose` mit `model: "sonnet"` (andere Clients: das günstigste Modell mit Web-Zugriff) und den
     Sub-Agent-Vorlagen aus `outreach-qualify`, `outreach-research` und `outreach-generate` nacheinander,
     mit den Abschnitten „Anrede und Ansprache“ und „Intro-Regeln“ aus `outreach-copy` und dem Hinweis, bei
     `not_qualified` aufzuhören.
   - **Ohne Subagents:** die Leads nacheinander in der Sitzung mit denselben Schritten.
3. **Bericht** wie in `outreach-pipeline` (gleiches Format für beide Laufarten). Dazu die
   `aufhänger=`-Angaben der `bau`-Zeilen mit `mail=gespeichert` auszählen: Zeigt mehr als ein Drittel
   dasselbe Anker-Thema (z. B. lauter Angstpatienten), im Bericht als systematischen Befund melden und
   vorschlagen, Sperrliste und `intro`-Prompt über `outreach-campaign` nachzuschärfen (bei
   `nur_pruefen` fehlt die Angabe, dann entfällt die Zählung). Zeilen mit `grund=keine-adresse`
   (ab MCP 3.0.0: Lead ohne E-Mail importiert, Recherche fand keine eigene Adresse, keine Mail)
   zählen als „ohne Adresse“ und sind kein Fehler. Danach alle angemeldeten
   Phasen mit `outreach_progress(action="end", campaign_id, phase=…)` schließen, auch wenn alles gezählt
   scheint: Leads ohne Schreibaufruf (Recherche vorhanden, aussortiert, Fehler) hält das Band sonst offen.
4. **Rennschutz:** Meldet ein Agent `lead_run_active`, läuft parallel ein Server-Lauf über dieselben Leads.
   Abwarten (`get_lead_run_status`), dann diese Leads erneut starten.
5. **Ohne Adresse:** `no_contact_email` (Lead ohne Versandadresse) beendet einen Lead ohne Fehler; nicht
   erneut starten.

## Workflow-Skript (Claude Code)

`args`:

| Feld | Bedeutung | Standard |
|---|---|---|
| `campaign_id` | Kampagne | – |
| `leads` | `[{ id, company }]` aus `list_leads` | – |
| `server` | Name des Outreach-Servers, wenn mehrere verbunden sind (z. B. `listm8`) | leer |
| `stufen` | Einschränkung wie „nur Qualifizierung und Recherche“; leer = alle Stufen | leer |
| `pruefen` | Größe der Stichprobe (0 = keine, Anzahl der Leads = alle) | 10 |
| `nur_pruefen` | `true`: Leads haben schon Mail-Variablen, nur prüfen und nachbessern (aus `outreach-verify`); `pruefen` dann = Anzahl der Leads | `false` |
| `bauen`, `pruefer` | Modelle | `haiku`, `sonnet` |

```js
export const meta = {
  name: 'outreach-abo-lauf',
  description: 'Abo-Lauf: je Lead bauen, Stichprobe prüfen, Befunde nachbessern und gegenprüfen',
  phases: [{ title: 'Bauen' }, { title: 'Prüfen' }, { title: 'Nachbessern' }],
}
const { campaign_id, leads, server = '', stufen = '', nur_pruefen = false, bauen = 'haiku', pruefer = 'sonnet' } = args
const pruefen = args.pruefen ?? (nur_pruefen ? leads.length : 10)
const srv = server ? ` Server: ${server}.` : ''
const kopf = l => `Kampagne ${campaign_id}, Lead ${l.id} (${l.company}).${srv}`
const auftrag = l => `${kopf(l)}${stufen ? ` ${stufen}.` : ''} Ohne Rückfragen bis zur Antwortzeile arbeiten.`
const zeile = (r, re) => String(r ?? '').split('\n').map(s => s.trim()).find(s => re.test(s))
// Stichprobe gleichmäßig über die Liste streuen
const abstand = pruefen > 0 ? Math.max(1, Math.floor(leads.length / pruefen)) : 0
const stichprobe = new Set(abstand ? leads.filter((_, i) => i % abstand === 0).slice(0, pruefen).map(l => l.id) : [])
const lead = (label, phase) => ({ agentType: 'outreach:lead-agent', model: bauen, label, phase })
const pruef = (label, phase) => ({ agentType: 'outreach:verify-agent', model: pruefer, label, phase })

const ergebnis = await pipeline(leads,
  l => nur_pruefen ? `OK lead=${l.id} mail=gespeichert (vorhanden)` : agent(auftrag(l), lead(`Bauen ${l.id}`, 'Bauen'))
    .then(r => zeile(r, /^(OK|FEHLER) lead=/) ?? `FEHLER lead=${l.id} stufe=agent: ${String(r).slice(0, 150)}`),
  async (bau, l) => {
    if (!stichprobe.has(l.id) || !/mail=gespeichert/.test(bau)) return { bau }
    const urteil = zeile(await agent(`${kopf(l)} Modus: nur Urteil`, pruef(`Prüfen ${l.id}`, 'Prüfen')), /^(URTEIL|FEHLER) lead=/)
    return { bau, urteil }
  },
  async (r, l) => {
    const m = /ergebnis=(ablehnen|hinweis) art=(text|recherche|adresse) .*?grund=(.*)$/.exec(r.urteil ?? '')
    if (!m) return r
    const nach = zeile(await agent(`${kopf(l)} Nachbessern: art=${m[2]}, Befund: ${m[3]}`,
      lead(`Nachbessern ${l.id}`, 'Nachbessern')), /^(NACHGEBESSERT|UNVERÄNDERT|FEHLER) lead=/)
    if (!/^NACHGEBESSERT/.test(nach ?? '')) return { ...r, nach }
    const gegen = zeile(await agent(`${kopf(l)} Modus: nur Urteil`, pruef(`Gegenprüfen ${l.id}`, 'Nachbessern')), /^(URTEIL|FEHLER) lead=/)
    return { ...r, nach, gegen }
  })
return ergebnis.map((r, i) => r ?? { bau: `FEHLER lead=${leads[i].id} stufe=workflow: abgebrochen` })
```

Je Lead kommt `{ bau, urteil?, nach?, gegen? }` zurück:

- `bau`: `OK lead=… fit=… recherche=… mail=…` bzw. `FEHLER …`. `fit=not_qualified` heißt aussortiert.
- `urteil` (nur Stichprobe): `URTEIL lead=… ergebnis=<freigeben|ablehnen|hinweis> art=…`.
- `nach` und `gegen`: eine Runde Nachbessern für `art=text|recherche|adresse` und die Gegenprüfung.
  Besteht die Gegenprüfung nicht oder lautet `nach` `UNVERÄNDERT`, geht der Lead mit Grund an den Nutzer,
  ebenso jedes Urteil mit `art=fit` oder `art=recht`.
- Derselbe Befund bei drei oder mehr Leads ist systematisch: nicht einzeln nachbessern, sondern die
  Ursache beheben (Variablen-Prompt über `outreach-campaign`) und die betroffenen Leads neu generieren.

Der Workflow fährt so viele Agents gleichzeitig, wie der Rechner zulässt (meist 6–14). Mehr als etwa
200 Leads in einem Lauf: lieber den Server-Lauf vorschlagen, der ohne offene Sitzung weiterläuft.

## Abgebrochen? Fortsetzen

Endet die Sitzung mitten im Lauf, ist nichts verloren. Ein erneuter Start ist harmlos: Abgeschlossene
Qualifizierungsurteile sind final und werden übersprungen, eine vorhandene Recherche wird nur genutzt.

- Gleiche Sitzung: `Workflow({ scriptPath, resumeFromRunId })`. Fertige Agents kommen aus dem Cache.
  Ein Agent, der zurückgefragt statt gearbeitet hat, gilt dort als fertig: diesen Lead neu starten.
- Nie einen `lead-agent` ohne Stufenangabe auf Leads mit gespeicherten Mail-Variablen ansetzen: Er
  schreibt sie neu. Zum Prüfen vorhandener Mails `nur_pruefen: true`.
- Neue Sitzung: offene Leads mit `list_leads` wie beim Start ermitteln (für die Mail-Stufe
  `campaign_status="processing"`) und nur diese in einem neuen Workflow laufen lassen. Nie Leads mit
  gespeicherten Mail-Variablen erneut bauen lassen, das überschreibt sie.

## Verwandt

- Einstieg und Wahl der Laufart: `outreach-pipeline`
- Prüfen und Freigeben (auch im Abo): `outreach-verify`
- Einzelne Stufen: `outreach-qualify`, `outreach-research`, `outreach-generate`
