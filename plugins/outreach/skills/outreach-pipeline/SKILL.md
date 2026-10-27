---
name: outreach-pipeline
description: Use when user says "outreach:pipeline", "mcp:pipeline", "kompletter mcp durchlauf", "leads komplett verarbeiten", "lead lauf starten", "qualify research generate", "alles in einem lauf mcp", "full pipeline", "abo-lauf", "im abo", "lauf im abo", "server-lauf", "mit subagents", "ohne server", "ohne openrouter", "lokal durchlaufen lassen", or triggers /mcp:pipeline. Gemeinsamer Einstieg für beide Laufarten - Server-Lauf (start_lead_run, schneller, kostet Credits je Lead, bei BYOK-Konten das eigene OpenRouter-Konto) und Abo-Lauf (Agents im Claude- bzw. ChatGPT-Abo, keine Credits und kein OpenRouter, nur Abo-Kontingent).
---

# Outreach Pipeline — Leads komplett verarbeiten (Server-Lauf oder Abo-Lauf)

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

Dieser Skill verarbeitet die Leads einer Kampagne komplett: qualifizieren → recherchieren → Mail-Variablen
schreiben. Dafür gibt es zwei **gleichwertige Laufarten**. Beide nutzen dieselbe Kampagne, dieselben
Stufen und dieselbe Lead-Auswahl, enden im selben Bericht und führen zum selben nächsten Schritt.

| | Server-Lauf | Abo-Lauf |
|---|---|---|
| Wer arbeitet | ListM8-Server mit den KI-Agents der Kampagne | je Lead ein Agent in deinem KI-Tool |
| Kosten | Credits je Lead nach KI-Modell und Recherche-Stufe, vorher per `quote_lead_run` sichtbar (bei Richtpreisen als ca.-Angabe); `budget_percent` deckelt den Lauf. BYOK-Konto: eigenes OpenRouter-Konto, keine Credits | keine Credits, kein OpenRouter, nur Kontingent deines Claude- bzw. ChatGPT-Abos |
| Tempo | schneller, läuft im Hintergrund weiter, auch wenn die Sitzung endet | 30 Leads ≈ 5 Minuten, die Sitzung muss offen bleiben |
| Prüfen | Stichprobe danach mit `outreach-verify` | Stichprobe im selben Lauf (Claude Code: ein Workflow) |
| Ausführung | Abschnitt „Server-Lauf“ unten | Skill `outreach-abo-lauf` |

```
gemeinsam: ping + list_campaigns -> export_campaign_blueprint -> list_lead_runs(active_only=true)
           -> Leads und Stufen wählen -> Laufart wählen
Server:    get_credit_balance -> quote_lead_run -> Zustimmung -> start_lead_run(quote_hash)
           -> get_lead_run_status (poll bis is_terminal); bei credits_exhausted resume_lead_run
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

0. **Umgebung und Konfiguration (Pflicht)**: `ping` und `list_campaigns` — Konto und Kampagne müssen zum Auftrag passen. Diese Anleitung setzt MCP 3.0.0 voraus; meldet `ping` eine Version unter 3.0.0, kennt der Server keine Credits (kein `quote_lead_run`, kein `get_credit_balance`), der Server-Lauf läuft dann ohne Angebot mit `budget_usd` als Deckel in US-Dollar, und die Kosten trägt das eigene OpenRouter-Konto. Dann `export_campaign_blueprint(campaign_id)` lesen: Qualifizierungskriterien, Research-Vorgaben, E-Mail-Schritte und AI-Variablen müssen vorhanden und sinnvoll sein (Details: `/outreach-campaign`). Fehlt etwas, NICHT starten, sondern erst ergänzen. Ein Lauf auf unvollständigem Setup kostet Credits bzw. Kontingent, und ein abgeschlossenes Qualifizierungsurteil ist pro Kampagne final: jeder spätere Lauf überspringt es, `write_lead_details` lehnt Änderungen mit `verdict_final` ab.
1. **Vorprüfung (Pflicht)**: `list_lead_runs(campaign_id, active_only=true)`. Ist ein Server-Lauf aktiv: NICHT starten — parallele Läufe über dieselben Leads blockieren sich und können Leads still überspringen. Stattdessen den aktiven Lauf verfolgen oder mit `cancel_lead_run` stoppen.
2. **Leads und Stufen wählen**:
   - Stufen: Default alle 3 (`qualification`, `research`, `email`); Teilmengen und Lücken erlaubt, z. B. nur `email`. Bereits erfüllte Stufen werden je Lead übersprungen.
   - **Vorgegebene Auswahl zuerst:** Gibt der Auftrag einen `list_leads`-Aufruf vor (Listen-Modus mit `run_stages`, etwa aus dem Startdialog der App), ihn einmal genau so ausführen, ohne Argumente zu ändern, wegzulassen oder zu ergänzen. Fehlt in der Antwort `applied_filters`, kennen Server oder Verbindung den Listen-Modus nicht (MCP älter als 2.1.0, oder das Tool-Schema im Client ist veraltet): abbrechen und den Nutzer bitten, die Verbindung neu einzurichten. Sonst die Leads aus `lead_ids` in dieser Reihenfolge nehmen und vor dem ersten Agenten festhalten; nicht mit `offset` blättern, denn bearbeitete Leads fallen aus der Auswahl, und `offset` würde dann Leads überspringen. Kommen weniger Leads als im Auftrag genannt, die gelieferten bearbeiten und die Abweichung nennen; kommen keine, ist nichts zu tun. Gibt der Auftrag Lead-IDs vor: genau diese, in dieser Reihenfolge. Die Stufen kommen dann ebenfalls aus dem Auftrag.
   - Sonst Menge: eine Anzahl, bekannte `lead_ids` oder „alles, was ansteht“. Für einen Lauf ab der Qualifizierung `list_leads(campaign_id, fit_level="", research_status="", campaign_status="processing", qualification_status="pending", limit=<Anzahl>)`. FALLSTRICK: ohne `fit_level=""` und `research_status=""` finden die Defaults frisch hinzugefügte Leads nicht.
   - Urteile gelten **pro Kampagne**: Ein Lead, der nur in einer anderen Kampagne qualifiziert wurde, gilt hier als nie qualifiziert. Bereits kontaktierte Leads blendet der Default-Filter aus (`contact_status`).
3. **Laufart wählen**: Bringt der Auftrag eine Auswahl mit (Schritt 2, etwa aus dem Startdialog der App), ist es ein Abo-Lauf und die Menge steht fest, keine Rückfrage; bei mehr als 50 Leads nur einmal auf den Server-Lauf hinweisen, die Auswahl nicht ändern. Sonst: Nennt der Nutzer keine, mit der Tabelle oben kurz fragen (Server: schneller, kostet Credits je Lead; Abo: keine Credits, nutzt das eigene Abo). Für die Frage darf der Preis schon dastehen: `get_credit_balance` und `quote_lead_run` sind nur lesend und kosten nichts (Server-Lauf, Schritte 0 und 2). Preise nur aus dem Angebot nennen, nie aus dem Gedächtnis. Ab etwa 200 Leads eher den Server-Lauf empfehlen, weil er ohne offene Sitzung weiterläuft.
4. **Ausführen**: Server-Lauf nach dem Abschnitt unten; Abo-Lauf: den Skill `outreach-abo-lauf` laden und mit der Lead-Liste aus Schritt 2 ausführen.
5. **Bericht** im gemeinsamen Format (unten), danach der nächste Schritt.

Review und Freigabe gehören bewusst NICHT in den Lauf: Er endet bei `pending_review`, freigeben entscheidet der Nutzer (Vier-Augen-Prinzip, `outreach-verify`). Die Stichprobe im Abo-Lauf urteilt nur, sie gibt nichts frei.

## Server-Lauf (start_lead_run)

Das MCP-Tool `start_lead_run` verkettet Qualifizierung, Research und E-Mail-Variablen pro Lead mit den kampagneneigenen AI-Agents. Abgerechnet wird mit Plattform-Credits je Lead, der Preis ist beim Start eingefroren. Das Angebot nennt in `charging` die Abrechnungsart: bei `fixed` gilt der Preis genau, bei `guide` ist er ein Richtpreis, jede Stufe bucht ihren Aufwand, mindestens den Richtpreis und höchstens das Doppelte; eine höhere Denktiefe kann den Preis bis zum Doppelten erhöhen. Den Teil über dem Richtpreis bucht der Server nur bis zum freien Guthaben und zum Lauf-Budget, das Guthaben wird dadurch nie negativ. Grundsätzlich gilt: Ein voll durchlaufener Lead kostet `credits_per_lead`, ein bei der Qualifizierung aussortierter nur `credits_disqualified`; technische Fehler einer Stufe und Leads ohne offene Arbeit (kontaktiert, aussortiert, erledigt) kosten nichts. Der Preis hängt an den KI-Modellen der Kampagne und an der Recherche-Stufe, als Beispiel im Standardmodell: Basis 0,75, Smart 1, Deep 2 Credits je Lead, aussortiert 0,25. Maßgeblich ist immer das Angebot von `quote_lead_run`. Dein Client holt das Angebot, startet, pollt und berichtet. Vorbedingungen des Servers: ein KI-Modell mit Credit-Preis; die email-Stufe braucht eine E-Mail-Sequenz an der Kampagne. Einen eigenen OpenRouter-Key braucht nur ein BYOK-Konto.

0. **Guthaben und Abrechnungsmodus**: `get_credit_balance` einmal je Lauf lesen. `billing_mode` entscheidet an genau drei Stellen: beim Preis-Angebot, bei den Kosten im Bericht und beim Hinweis auf einen Nachkauf.
   - `credits`: `available` ist das verfügbare Guthaben (Bilanz minus Reservierungen aktiver Läufe), `by_origin` zeigt, was aus dem Abo stammt (verfällt, `next_expiry`) und was nachgekauft ist (verfällt nie). Alle Beträge sind Credits als Dezimalzahl mit höchstens drei Nachkommastellen, nie eine Währung.
   - `byok`: Das Konto zahlt die KI mit dem eigenen OpenRouter-Key. Keine Preise nennen, kein Lauf-Budget, kein `credits_exhausted` erwarten, nie einen Credit-Kauf vorschlagen; die Credit-Felder sind `null`.
   - `purchase` (beide Modi): `allowed` sagt, ob der Nutzer gerade Credits kaufen kann, `app_url` führt zur Credits-Seite der App. Nur bei `allowed: true` einen Nachkauf vorschlagen; kaufen kann nur der Nutzer selbst in der App.
1. **Lead-Auswahl**: `lead_ids` (1-2000) für bekannte Mengen ODER `select_by_filter=true` für „alles, was ansteht" (Filter wie `list_leads`, gleicher Fallstrick wie in Schritt 2). Bei `matched_total > selected` sind nur die Top-2000 nach Score im Lauf — Folgelauf für den Rest. `select_by_filter` kennt nur die Basisfilter. Eine Auswahl mit den Filtern der Lead-Liste (Suche, Score, Städte, Sortierung, `run_stages`) holt `list_leads` im Listen-Modus (MCP ab 2.1.0); deren `lead_ids` dann als `lead_ids` übergeben.
2. **Preis-Angebot (Pflicht bei `billing_mode: credits`)**: `quote_lead_run` mit genau den Parametern des geplanten Starts (Stufen, Auswahl, `research_tier`, `budget_percent`, `agent_key`). Es reserviert und startet nichts. Dem Nutzer nennen: `credits_per_lead` (voll durchlaufener Lead), `credits_disqualified` (aussortierter Lead), `max_credits` (Summe für die Leads mit Arbeit; bei `charging: guide` stattdessen `estimated_credits` als ca.-Angabe nennen und `max_credits` als Obergrenze, das Doppelte), `with_work_count` und `without_work` (kosten nichts), `research_tier` und `available_credits`. Bei `capped: true` passen nur `affordable_count` Leads ins Guthaben bzw. ins Lauf-Budget; das ausdrücklich sagen. Erst nach Zustimmung starten und den `quote_hash` an `start_lead_run` übergeben. Bei `billing_mode: byok` ist das Angebot nur eine Mengenprüfung (`with_work_count`, `without_work`), ohne Preis und ohne `quote_hash`.
3. **Optionen**:
   - `budget_percent` (1-100): Lauf-Budget als Anteil am beim Start verfügbaren Guthaben (Budget in Credits = `available` × Prozent / 100); bei größeren Läufen vorschlagen. Erreicht der Lauf es, endet er als `budget_exhausted`. Bei `byok` wirkungslos, dann weglassen.
   - `budget_usd` nie verwenden: seit MCP 3.0.0 veraltet und in beiden Modi ignoriert (die Antwort trägt dann eine `note`). Ein Lauf-Budget in US-Dollar gibt es nicht mehr.
   - `research_tier` (`basis`, `smart`, `deep`) nur auf User-Nennung: gilt nur für diesen Lauf; ohne Angabe gilt die Stufe der Kampagne, sonst die des Kontos. Basis liest nur die Website, Smart sucht danach höchstens einmal nach Bewertungen, Deep sucht im Recherche-Loop. Die Stufe ändert den Preis je Lead (Beispiel oben); nach einem Wechsel das Angebot neu holen.
   - `agent_key` nur auf explizite User-Nennung: Ein unbekannter Schlüssel überspringt die Qualifizierungs- und Research-Stufe still pro Lead.
4. **Starten**: `start_lead_run` mit denselben Parametern und dem `quote_hash` (bei `byok` ohne). Die Antwort lesen: `selected_count` unter `requested_count` heißt, das Guthaben hat die Auswahl gekappt; die reduzierte Menge und jede `note` dem Nutzer nennen. Den Rest erst nach Abschluss in einen Folgelauf nehmen.
5. **Fehler beim Start** (Text `<code>: <Meldung>`, nie in eine Retry-Schleife):

   | Code | Bedeutung | Handlung |
   |---|---|---|
   | `price_changed` | Modell, Denktiefe, Recherche-Stufe oder Preisversion haben sich seit dem Angebot geändert; kein Lauf angelegt | `quote_lead_run` erneut, neuen Preis nennen, nach Zustimmung mit dem neuen `quote_hash` starten |
   | `model_not_priced` | ein Slot nutzt ein Modell ohne Credit-Preis | Nutzer wählt in den KI-Modell-Einstellungen ein bepreistes Modell |
   | `effort_not_priced` | Denktiefe `xhigh` oder `max` ist bei Festpreisen (`charging: fixed`) gesperrt | Nutzer wählt eine niedrigere Denktiefe |
   | `model_missing` | für einen Slot ist gar kein KI-Modell gewählt | Nutzer wählt zuerst ein Modell |
   | `credits_exhausted` | das Guthaben reicht nicht einmal für einen Lead; nichts gestartet | benötigte und verfügbare Credits aus dem Text nennen; `get_credit_balance.purchase` lesen: nur bei `allowed` einen Nachkauf vorschlagen (Link `purchase.app_url`), sonst Plan wechseln oder ein günstigeres Modell bzw. eine günstigere Recherche-Stufe wählen (`quote_lead_run` zeigt den Preis). Der Abo-Lauf kostet keine Credits und bleibt immer ein Ausweg |
   | `limit_reached` | mehr als 2000 `lead_ids`, Plan-Limit oder kein aktives Abo (`get_credit_balance.account.subscription_required`) | zu viele IDs: in mehrere Läufe splitten; sonst an den Nutzer (Plan wählen bzw. wechseln) |
   | `run_not_startable` | andere Vorbedingung fehlt (E-Mail-Sequenz, gesperrter KI-Anbieter, Stufe gesperrt; bei `byok` der eigene OpenRouter-Key) | an den Nutzer; als Ausweg den Abo-Lauf anbieten |
   | `no_leads_matched` | der Filter trifft nichts | Filter anpassen oder mit `list_leads` und denselben Parametern gegenprüfen |
   | `validation_failed` | ungültige Parameter (Stufen, `budget_percent`, `quote_hash`, `lead_ids` UND `select_by_filter` zugleich) | Parameter korrigieren |
   | `campaign_not_found` | falsche Kampagne | Kampagne prüfen |

   Ein erschöpftes Plan-Limit kann sich auch erst nach dem Start zeigen: Der Lauf endet dann als `limit_exhausted` (nur im Status sichtbar).
6. **Polling**: `get_lead_run_status(lead_run_id)` alle 30-60 s. Fortschritt am completed-Zähler der LETZTEN Stufe in `stageProgress[]` gegen `leadTotal` messen (Fehler = Summe aller `stageProgress[].failed`) — NICHT an den Stufen-Totals, die wachsen während des Laufs. Stoppen bei `is_terminal: true`. CAVEAT: ein `completed` jünger als ~30 Minuten kann der Server wieder auf `running` zurückholen — vor dem Abschlussbericht nachprüfen.
7. **Abbruch**: `cancel_lead_run(lead_run_id)` storniert noch nicht gestartete Jobs und Folgestufen; bereits laufende Jobs laufen aus (`running_jobs`) und buchen ihren beim Start eingefrorenen Stufenpreis (bei Richtpreisen nach Aufwand, höchstens das Doppelte), stornierte Stufen kosten nichts; idempotent (`already_terminal`). Endzustand via `get_lead_run_status` verifizieren.
8. **Während des Laufs**: `save_lead_variables`, `approve_lead_variables` und `reject_lead_variables` (E-Mail-Stufe) sowie `write_lead_details` (Qualifizierung/Research) sind mit `lead_run_active` gesperrt, ebenso `switch_primary_email` bei aktiver Research-Stufe (Rennschutz, kein Fehler).

### Terminal-Status deuten

| Status | Bedeutung | Nächster Schritt |
|--------|-----------|-------------------|
| `completed` | Alle Leads durch | Stichprobe mit /outreach-verify |
| `completed_with_failures` | Mind. ein Job endgültig gescheitert | Fehl-Leads berichten, Folgelauf anbieten |
| `credits_exhausted` | Guthaben aufgebraucht, Rest storniert; als einziger Endzustand fortsetzbar | Nachkauf nur bei `get_credit_balance.purchase.allowed` vorschlagen (Link `purchase.app_url`), sonst Plan wechseln. Danach mit `get_credit_balance` prüfen, dass `available` über null liegt, und `resume_lead_run(lead_run_id)` für DENSELBEN Lauf aufrufen, keinen neuen starten; der Lauf behält seinen Preis. Antwortet `resume_lead_run` wieder mit `credits_exhausted`, reicht das Guthaben weiter nicht: zurück an den Nutzer, keine Schleife. `billing_mode_changed` heißt, der Abrechnungsmodus wurde seit dem Start umgestellt: neuen Lauf anbieten. Ist kein Kauf möglich, den Rest als Abo-Lauf anbieten |
| `budget_exhausted` | Lauf-Budget aus `budget_percent` erreicht, Rest storniert | Restmenge beziffern, Folgelauf mit neuem Angebot oder Abo-Lauf für den Rest anbieten; kein `resume_lead_run` |
| `limit_exhausted` | Plan-Limit mitten im Lauf | An den User (Plan/Limit) — kein Auto-Retry |
| `provider_exhausted` | Störung beim KI-Anbieter bzw. beim Plattform-Key; bei `byok` lehnt OpenRouter das eigene Konto ab (Guthaben leer oder Key abgelehnt) | An den User, kein Retry; Abo-Lauf als Ausweg anbieten |
| `cancelled` | Vom User gestoppt (oder beim Umstellen des Abrechnungsmodus abgebrochen, siehe `statusReason`) | Stand berichten |
| `failed` | Vorbereitung gescheitert, nichts verarbeitet | `statusReason` ausgeben, Vorbedingungen prüfen |

Hinweis zu den Credits: `spent_credits` ist, was der Lauf gebucht hat, `reserved_credits` die noch offene Reservierung, `budget_credits` der Deckel aus `budget_percent` (sonst `null`). Laufende Jobs buchen nach einem Stopp noch ihren Stufenpreis. Bei Richtpreisen (`price.charging: guide`) kann `spent_credits` über Preis mal Leads liegen, höchstens beim Doppelten und nie über `budget_credits`. `price` ist der beim Start eingefrorene Preis je Lead; er bleibt gleich, auch wenn der Nutzer während des Laufs das Modell wechselt. Bei `byok` sind alle Credit-Felder `null`.

Hinweis zu den Zahlen: `not_qualified`-Leads und Leads mit blockierendem Kontaktstatus verlassen die Kette OHNE Job — sie erscheinen in keinem Stufen-Zähler; `completed` kann deshalb legitim unter `leadTotal` bleiben.

## Bericht (beide Laufarten)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lead-Lauf abgeschlossen — Kampagne {campaign.name} · {Server-Lauf | Abo-Lauf} ({status})
Stufen: {stages} | Leads: {fertig}/{gesamt} | aussortiert: {not_qualified} | Fehler: {failed}
Kosten: {spent_credits} Credits gebucht{ von budget_credits} · Guthaben danach {available}  bzw.  BYOK: eigenes OpenRouter-Konto  bzw.  im Abo, keine Credits
Stichprobe: {geprüft} geprüft · {frei} ohne Befund · {nachgebessert} nachgebessert · {offen} offen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Die Kosten-Zeile richtet sich nach `billing_mode`: bei `credits` `spent_credits` aus dem letzten `get_lead_run_status` und `available` aus einem frischen `get_credit_balance`, Zahlen mit Dezimalkomma (etwa 12,25 Credits). Beim Server-Lauf entfällt die Zeile „Stichprobe“, bis sie mit `outreach-verify` gelaufen ist. Offene Leads (Urteil `fit` oder `recht`, nach einer Runde Nachbessern nicht bestanden) einzeln mit Grund und Empfehlung nennen.

Danach: „Nächster Schritt: Stichprobe prüfen (beim Server-Lauf mit /outreach-verify, 10 Leads) bei neuer Kampagne, nach Änderungen oder vor dem ersten Export; danach freigeben.“

## Verwandt

- Abo-Lauf ausführen: `outreach-abo-lauf` · Review und Freigabe: `/outreach-verify`
- Einzelne Stufen: `/outreach-qualify`, `/outreach-research`, `/outreach-generate`
- Vorbereitung: `/outreach-campaign`, `/outreach-import`, `/outreach-lists`
- Copy-Fragen (Sequenz, Betreffzeilen, Offer, Prompts von `hallo`/`intro`, Prüfung der Mails) laufen über den Skill `outreach-copy`.
