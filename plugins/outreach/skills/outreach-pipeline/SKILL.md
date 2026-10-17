---
name: outreach-pipeline
description: Use when user says "outreach:pipeline", "mcp:pipeline", "kompletter mcp durchlauf", "leads komplett verarbeiten", "lead lauf starten", "qualify research generate", "alles in einem lauf mcp", "full pipeline", "abo-lauf", "im abo", "lauf im abo", "server-lauf", "mit subagents", "ohne server", "ohne openrouter", "lokal durchlaufen lassen", or triggers /mcp:pipeline. Gemeinsamer Einstieg für beide Laufarten - Server-Lauf (start_lead_run, schneller, kostet OpenRouter-Guthaben) und Abo-Lauf (Agents im Claude- bzw. ChatGPT-Abo, günstiger, keine Server-Kosten).
---

# Outreach Pipeline — Leads komplett verarbeiten (Server-Lauf oder Abo-Lauf)

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

Dieser Skill verarbeitet die Leads einer Kampagne komplett: qualifizieren → recherchieren → Mail-Variablen
schreiben. Dafür gibt es zwei **gleichwertige Laufarten**. Beide nutzen dieselbe Kampagne, dieselben
Stufen und dieselbe Lead-Auswahl, enden im selben Bericht und führen zum selben nächsten Schritt.

| | Server-Lauf | Abo-Lauf |
|---|---|---|
| Wer arbeitet | ListM8-Server mit den KI-Agents der Kampagne | je Lead ein Agent in deinem KI-Tool |
| Kosten | OpenRouter-Guthaben (echtes Geld, `budget_usd` begrenzt es) | Kontingent deines Claude- bzw. ChatGPT-Abos, keine Server-Kosten |
| Tempo | schneller, läuft im Hintergrund weiter, auch wenn die Sitzung endet | 30 Leads ≈ 5 Minuten, die Sitzung muss offen bleiben |
| Prüfen | Stichprobe danach mit `outreach-verify` | Stichprobe im selben Lauf (Claude Code: ein Workflow) |
| Ausführung | Abschnitt „Server-Lauf“ unten | Skill `outreach-abo-lauf` |

```
gemeinsam: ping + list_campaigns -> export_campaign_blueprint -> list_lead_runs(active_only=true)
           -> Leads und Stufen wählen -> Laufart wählen
Server:    start_lead_run -> get_lead_run_status (poll bis is_terminal)
Abo:       outreach-abo-lauf (Workflow: bauen -> Stichprobe prüfen -> nachbessern)
gemeinsam: Bericht -> Stichprobe prüfen und freigeben (outreach-verify)
```

## Aufruf

| Eingabe | Verhalten |
|---------|-----------|
| `/outreach-pipeline 80` | Kampagne 80, alle 3 Stufen; Laufart erfragen |
| `/outreach-pipeline 80 --bis research` | Nur Qualifizierung und Recherche |
| `/outreach-pipeline 80 --server` (oder „auf dem Server“) | Server-Lauf |
| `/outreach-pipeline 80 --abo` (oder „als Abo-Lauf“, „im Abo“, „ohne Server“) | Abo-Lauf |
| `/outreach-pipeline` | Kampagne via `list_campaigns` wählen |
| Prompt aus dem Startdialog der App („Prompt kopieren“, enthält einen `list_leads`-Aufruf oder Lead-IDs) | Abo-Lauf mit der vorgegebenen Auswahl und den vorgegebenen Stufen (Schritt 2 unten); keine Rückfrage nach Laufart oder Anzahl |

## Gemeinsamer Ablauf (beide Laufarten)

0. **Umgebung und Konfiguration (Pflicht)**: `ping` und `list_campaigns` — Konto und Kampagne müssen zum Auftrag passen. Dann `export_campaign_blueprint(campaign_id)` lesen: Qualifizierungskriterien, Research-Vorgaben, E-Mail-Schritte und AI-Variablen müssen vorhanden und sinnvoll sein (Details: `/outreach-campaign`). Fehlt etwas, NICHT starten, sondern erst ergänzen. Ein Lauf auf unvollständigem Setup kostet Geld bzw. Kontingent, und ein abgeschlossenes Qualifizierungsurteil ist pro Kampagne final: jeder spätere Lauf überspringt es, `write_lead_details` lehnt Änderungen mit `verdict_final` ab.
1. **Vorprüfung (Pflicht)**: `list_lead_runs(campaign_id, active_only=true)`. Ist ein Server-Lauf aktiv: NICHT starten — parallele Läufe über dieselben Leads blockieren sich und können Leads still überspringen. Stattdessen den aktiven Lauf verfolgen oder mit `cancel_lead_run` stoppen.
2. **Leads und Stufen wählen**:
   - Stufen: Default alle 3 (`qualification`, `research`, `email`); Teilmengen und Lücken erlaubt, z. B. nur `email`. Bereits erfüllte Stufen werden je Lead übersprungen.
   - **Vorgegebene Auswahl zuerst:** Gibt der Auftrag einen `list_leads`-Aufruf vor (Listen-Modus mit `run_stages`, etwa aus dem Startdialog der App), ihn einmal genau so ausführen, ohne Argumente zu ändern, wegzulassen oder zu ergänzen. Fehlt in der Antwort `applied_filters`, kennen Server oder Verbindung den Listen-Modus nicht (MCP älter als 2.1.0, oder das Tool-Schema im Client ist veraltet): abbrechen und den Nutzer bitten, die Verbindung neu einzurichten. Sonst die Leads aus `lead_ids` in dieser Reihenfolge nehmen und vor dem ersten Agenten festhalten; nicht mit `offset` blättern, denn bearbeitete Leads fallen aus der Auswahl, und `offset` würde dann Leads überspringen. Kommen weniger Leads als im Auftrag genannt, die gelieferten bearbeiten und die Abweichung nennen; kommen keine, ist nichts zu tun. Gibt der Auftrag Lead-IDs vor: genau diese, in dieser Reihenfolge. Die Stufen kommen dann ebenfalls aus dem Auftrag.
   - Sonst Menge: eine Anzahl, bekannte `lead_ids` oder „alles, was ansteht“. Für einen Lauf ab der Qualifizierung `list_leads(campaign_id, fit_level="", research_status="", campaign_status="processing", qualification_status="pending", limit=<Anzahl>)`. FALLSTRICK: ohne `fit_level=""` und `research_status=""` finden die Defaults frisch hinzugefügte Leads nicht.
   - Urteile gelten **pro Kampagne**: Ein Lead, der nur in einer anderen Kampagne qualifiziert wurde, gilt hier als nie qualifiziert. Bereits kontaktierte Leads blendet der Default-Filter aus (`contact_status`).
3. **Laufart wählen**: Bringt der Auftrag eine Auswahl mit (Schritt 2, etwa aus dem Startdialog der App), ist es ein Abo-Lauf und die Menge steht fest, keine Rückfrage; bei mehr als 50 Leads nur einmal auf den Server-Lauf hinweisen, die Auswahl nicht ändern. Sonst: Nennt der Nutzer keine, mit der Tabelle oben kurz fragen (Server: schneller, kostet OpenRouter-Guthaben; Abo: günstiger, nutzt das eigene Abo). Beim Server-Lauf zusätzlich ein `budget_usd` vorschlagen. Ab etwa 200 Leads eher den Server-Lauf empfehlen, weil er ohne offene Sitzung weiterläuft.
4. **Ausführen**: Server-Lauf nach dem Abschnitt unten; Abo-Lauf: den Skill `outreach-abo-lauf` laden und mit der Lead-Liste aus Schritt 2 ausführen.
5. **Bericht** im gemeinsamen Format (unten), danach der nächste Schritt.

Review und Freigabe gehören bewusst NICHT in den Lauf: Er endet bei `pending_review`, freigeben entscheidet der Nutzer (Vier-Augen-Prinzip, `outreach-verify`). Die Stichprobe im Abo-Lauf urteilt nur, sie gibt nichts frei.

## Server-Lauf (start_lead_run)

Das MCP-Tool `start_lead_run` verkettet Qualifizierung, Research und E-Mail-Variablen pro Lead mit den kampagneneigenen AI-Agents — abgerechnet über den OpenRouter-Account des Users. Dein Client startet, pollt und berichtet. Vorbedingungen des Servers: OpenRouter-Key + AI-Modell konfiguriert; die email-Stufe braucht eine E-Mail-Sequenz an der Kampagne.

1. **Lead-Auswahl**: `lead_ids` (1-2000) für bekannte Mengen ODER `select_by_filter=true` für „alles, was ansteht" (Filter wie `list_leads`, gleicher Fallstrick wie in Schritt 2). Bei `matched_total > selected` sind nur die Top-2000 nach Score im Lauf — Folgelauf für den Rest. `select_by_filter` kennt nur die Basisfilter. Eine Auswahl mit den Filtern der Lead-Liste (Suche, Score, Städte, Sortierung, `run_stages`) holt `list_leads` im Listen-Modus (MCP ab 2.1.0); deren `lead_ids` dann als `lead_ids` übergeben.
2. **Optionen**: `budget_usd` (0.01-10000; erreicht => Lauf endet als `budget_exhausted`, laufende Jobs laufen aus). `agent_key` nur auf explizite User-Nennung — ein unbekannter Schlüssel überspringt die Qualifizierungs- und Research-Stufe still pro Lead. `research_tier` (`basis`, `smart`, `deep`) nur auf User-Nennung: gilt nur für diesen Lauf; ohne Angabe gilt die Stufe der Kampagne, sonst die des Kontos. Basis liest nur die Website, Smart sucht danach höchstens einmal nach Bewertungen, Deep sucht im Recherche-Loop (teuerste Stufe).
3. **Fehler beim Start** (Text `<code>: <Meldung>`): `run_not_startable` = fehlende Vorbedingung (OpenRouter-Key, AI-Modell, E-Mail-Sequenz, gesperrter KI-Anbieter) — an den User zurückgeben, keine Retry-Schleife; als Ausweg den Abo-Lauf anbieten. `no_leads_matched` = der Filter trifft nichts — Filter anpassen oder mit `list_leads` und denselben Parametern gegenprüfen. `validation_failed` = ungültige Parameter (Stufen, Budget, `lead_ids` UND `select_by_filter` zugleich). `limit_reached` = mehr als 2000 `lead_ids` (in mehrere Läufe splitten) ODER Plan-Limit/Paywall (HTTP 402, der Text nennt den Grund) — dann an den User, kein Retry. `campaign_not_found` = falsche Kampagne. Ein erschöpftes Plan-Kontingent kann sich auch erst nach dem Start zeigen: Der Lauf endet dann als `limit_exhausted` (nur im Status sichtbar).
4. **Polling**: `get_lead_run_status(lead_run_id)` alle 30-60 s. Fortschritt am completed-Zähler der LETZTEN Stufe in `stageProgress[]` gegen `leadTotal` messen (Fehler = Summe aller `stageProgress[].failed`) — NICHT an den Stufen-Totals, die wachsen während des Laufs. Stoppen bei `is_terminal: true`. CAVEAT: ein `completed` jünger als ~30 Minuten kann der Server wieder auf `running` zurückholen — vor dem Abschlussbericht nachprüfen.
5. **Abbruch**: `cancel_lead_run(lead_run_id)` — storniert noch nicht gestartete Jobs und Folgestufen, bereits laufende Jobs laufen aus (`running_jobs`; leichtes Überschießen möglich); idempotent (`already_terminal`). Endzustand via `get_lead_run_status` verifizieren.
6. **Während des Laufs**: `save_lead_variables`, `approve_lead_variables` und `reject_lead_variables` (E-Mail-Stufe) sowie `write_lead_details` (Qualifizierung/Research) sind mit `lead_run_active` gesperrt, ebenso `switch_primary_email` bei aktiver Research-Stufe (Rennschutz, kein Fehler).

### Terminal-Status deuten

| Status | Bedeutung | Nächster Schritt |
|--------|-----------|-------------------|
| `completed` | Alle Leads durch | Stichprobe mit /outreach-verify |
| `completed_with_failures` | Mind. ein Job endgültig gescheitert | Fehl-Leads berichten, Folgelauf anbieten |
| `budget_exhausted` | Budget erreicht, Rest storniert | Restmenge beziffern, höheres Budget oder Abo-Lauf für den Rest anbieten |
| `limit_exhausted` | Plan-Limit mitten im Lauf | An den User (Plan/Limit) — kein Auto-Retry |
| `provider_exhausted` | KI-Anbieter (OpenRouter) lehnt das Konto ab | An den User — kein Retry; Abo-Lauf als Ausweg anbieten |
| `cancelled` | Vom User gestoppt | Stand berichten |
| `failed` | Vorbereitung gescheitert, nichts verarbeitet | `statusReason` ausgeben, Vorbedingungen prüfen |

Hinweis zu den Kosten: `spentUsd` ist der Betrag, an dem `budgetUsd` stoppt. Laufende Jobs können nach dem Stopp noch Kosten nachbuchen.

Hinweis zu den Zahlen: `not_qualified`-Leads und Leads mit blockierendem Kontaktstatus verlassen die Kette OHNE Job: sie erscheinen in keinem Stufen-Zähler; `completed` kann deshalb legitim unter `leadTotal` bleiben. Ab MCP 3.0.0 gilt das auch für Leads ohne Kontaktadresse: Hat ein ohne E-Mail importierter Lead nach der Recherche keine eigene Adresse, verlässt er die Kette vor der E-Mail-Stufe (Grund `no_contact_email`, kein Job, keine Kosten). `get_lead_run_status` zählt die Gründe in `skipReasons` (u. a. `no_contact_email`, `foreign_address`, `contacted`, `not_qualified`).

## Bericht (beide Laufarten)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lead-Lauf abgeschlossen — Kampagne {campaign.name} · {Server-Lauf | Abo-Lauf} ({status})
Stufen: {stages} | Leads: {fertig}/{gesamt} | aussortiert: {not_qualified} | ohne Adresse: {no_contact_email} | Fehler: {failed}
Kosten: {spentUsd} USD{von budgetUsd USD}  bzw.  im Abo, keine Server-Kosten
Stichprobe: {geprüft} geprüft · {frei} ohne Befund · {nachgebessert} nachgebessert · {offen} offen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Beim Server-Lauf entfällt die Zeile „Stichprobe“, bis sie mit `outreach-verify` gelaufen ist. Offene Leads (Urteil `fit` oder `recht`, nach einer Runde Nachbessern nicht bestanden) einzeln mit Grund und Empfehlung nennen.

Danach: „Nächster Schritt: Stichprobe prüfen (beim Server-Lauf mit /outreach-verify, 10 Leads) bei neuer Kampagne, nach Änderungen oder vor dem ersten Export; danach freigeben.“

## Verwandt

- Abo-Lauf ausführen: `outreach-abo-lauf` · Review und Freigabe: `/outreach-verify`
- Einzelne Stufen: `/outreach-qualify`, `/outreach-research`, `/outreach-generate`
- Vorbereitung: `/outreach-campaign`, `/outreach-import`, `/outreach-lists`
- Copy-Fragen (Sequenz, Betreffzeilen, Offer, Prompts von `hallo`/`intro`, Prüfung der Mails) laufen über den Skill `outreach-copy`.
