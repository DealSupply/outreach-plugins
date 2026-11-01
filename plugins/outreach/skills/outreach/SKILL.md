---
name: outreach
description: Einstieg für alles rund um Outreach-Kampagnen. Verwenden bei „outreach“, „was kann ich hier machen“, „wo fange ich an“, „Kampagne starten“, „Hilfe zu Outreach“, „wie viele Credits habe ich“, „Guthaben“, „freie Plätze“, „Credits nachkaufen“ oder wenn unklar ist, welcher Outreach-Skill passt. Fragt kurz nach dem Ziel und leitet an den passenden Skill weiter. Enthält die Workspace-Regel, die alle Outreach-Skills befolgen.
---

# Outreach – Einstieg

Dieser Skill leitet weiter: Frage den Nutzer, was er erreichen will, und lade dann genau den
passenden Skill. Dazu hält er die Workspace-Regel, auf die alle Outreach-Skills verweisen.

## Erst prüfen

- **Noch nicht eingerichtet?** (kein Outreach-MCP verbunden, erstes Mal, alte Skill-Kopien)
  → `outreach-setup`.
- **Verbunden?** Ein Aufruf von `list_campaigns` (nur lesend) zeigt, ob die Verbindung steht.
- **Workspace geklärt?** Sonst nach der Workspace-Regel unten, Punkt 1.

## Wohin

| Der Nutzer will … | Skill |
|---|---|
| eine Kampagne anlegen oder ändern | `outreach-campaign` |
| mit dem Start-Satz aus der App eine Kampagne einrichten („Richte mit outreach die Kampagne #123 ein.“) | `outreach-campaign`, Ablauf „Genannte leere Kampagne füllen“: genau diese Kampagne füllen, nie eine neue anlegen |
| Cold-Mail-Copy schreiben oder prüfen, ein Marketing-Offer formulieren | `outreach-copy` |
| Leads importieren (CSV, Liste) | `outreach-import` |
| Listen ansehen, anlegen, in eine Kampagne übernehmen | `outreach-lists` |
| Leads qualifizieren | `outreach-qualify` |
| Leads recherchieren | `outreach-research` |
| Mail-Variablen generieren | `outreach-generate` |
| generierte Mails prüfen und freigeben | `outreach-verify` |
| alles in einem Lauf (qualifizieren → recherchieren → generieren), auf dem Server oder im eigenen Abo | `outreach-pipeline` (fragt nach der Laufart) |
| einen Abo-Lauf direkt ausführen oder fortsetzen („Abo-Lauf“, „im Abo“, „ohne Server“, „als Workflow“) | `outreach-abo-lauf` |
| Leads einer Kampagne als Excel oder CSV herunterladen (Freigaben, für Instantly, fürs CRM) | `outreach-export` |
| Versand vorbereiten: Domains, Postfächer, Warm-up, Instantly, Auswertung | `outreach-launch` |
| neue Leads beschaffen (Apify, Outscraper) | `datenbeschaffung` – gehört zum Plugin **datenbeschaffung**; ist es nicht installiert, auf `outreach-setup` verweisen |
| prüfen, welches Offer sich mit KI liefern lässt, oder für einen Lead, der geantwortet hat, die versprochene Demo bauen (Webseiten-Entwurf, SEO, Anzeigen, Leadliste, Muster-Kampagne) | `fulfillment` – gehört zum Plugin **fulfillment**; ist es nicht installiert: `/plugin install fulfillment@outreach-plugins` (Claude Code) bzw. im Marketplace installieren |
| Guthaben, Credits, Preise, Limits, freie Plätze im Account, Nachkauf | kein eigener Skill: direkt `get_credit_balance` (nur lesend) aufrufen und erklären, siehe unten |
| Plugin aktualisieren | `outreach-update` |

## Guthaben und Limits erklären

`get_credit_balance` liefert alles in einem Aufruf:

- `billing_mode`: `credits` (Plattform-Credits) oder `byok` (das Konto zahlt die KI mit dem eigenen
  OpenRouter-Key; dann gibt es keine Credits, keine Preise und keinen Nachkauf, alle Credit-Felder sind `null`).
- Bei `credits`: `available` (verfügbar), `reserved` (gebunden in laufenden Server-Läufen), `by_origin`
  (Credits aus dem Abo verfallen, `next_expiry` nennt die nächsten; nachgekaufte Credits verfallen nie;
  `debt` ist eine offene Schuld). Beträge sind Credits mit bis zu drei Nachkommastellen, keine Währung.
- `account` (beide Modi): `leads_in_account` von `lead_limit` (`-1` = unbegrenzt), `free_slots` (so
  viele neue Leads passen noch; `null` = unbegrenzt), `over_limit` (mehr Leads als der Plan erlaubt:
  keine neuen, Läufe auf bestehenden Leads gehen weiter), `campaigns` von `campaign_limit`,
  `subscription_required` (kein aktives Abo: Es lässt sich nichts anlegen, zuerst einen Plan wählen).
  Nur neue E-Mail-Adressen belegen einen Platz. Gelöschte Leads geben ihren Platz sofort frei, schon
  gebuchte Credits werden dafür nicht erstattet.
- `purchase` (beide Modi): `allowed` sagt, ob der Nutzer jetzt Credits kaufen kann, `app_url` führt zur
  Credits-Seite der App. Einen Nachkauf nur bei `allowed: true` vorschlagen; kaufen kann nur der Nutzer
  selbst in der App. Sonst bleiben ein Planwechsel, ein günstigeres KI-Modell oder eine günstigere
  Recherche-Stufe, oder der Abo-Lauf, der keine Credits kostet.

Preise je Lead nie aus dem Gedächtnis nennen: Den verbindlichen Preis zeigt `quote_lead_run` vor einem
Server-Lauf (`outreach-pipeline`). Wer ein Jahresabo hat, wechselt erst nach Ende der Laufzeit auf ein
Monatsabo; mehr nicht zusagen.

## Regeln

- Nichts Kostenpflichtiges starten, ohne dass der Nutzer genau diesen Umfang freigibt.
- Kennt der Nutzer sein Ziel nicht, zuerst eine Frage: „Willst du eine neue Kampagne aufsetzen,
  Leads verarbeiten oder neue Leads beschaffen?“

## Workspace-Regel

Gilt für jeden Outreach-Skill, auch wenn er direkt aufgerufen wird. Eine Verbindung reicht für alle
Workspaces des Nutzers. Kampagnen, Leads, Listen, Läufe und Guthaben gehören zu genau einem
Workspace, auch der Bestand für den Dubletten-Abgleich.

1. **Workspace kennen.** Ist er im Gespräch noch nicht geklärt, `list_workspaces` aufrufen (nur
   lesend). Ein Workspace: weiter, ohne zu fragen. Mehrere: Name, Rolle und Plan zeigen, fragen, in
   welchem gearbeitet wird, und die Wahl für das Gespräch merken.
2. **Aufrufe ohne Objekt-ID** bekommen `workspace=<uuid>`, wenn der gewählte Workspace nicht der
   Standard ist (`default: true`). Das betrifft die Werkzeuge zum Auflisten, Suchen, Prüfen,
   Importieren und Anlegen, etwa `list_campaigns`, `search_leads`, `list_lists`, `list_lead_runs`,
   `export_leads`, `check_leads_exist`, `import_leads`, `create_campaign`, `create_list`,
   `get_credit_balance` und `mark_leads_contacted` mit E-Mail-Adressen. Ohne Angabe laufen sie im
   Standard-Workspace. Eine unbekannte uuid lehnt der Server mit `workspace_not_found` ab.
3. **Aufrufe mit Objekt-ID** (`campaign_id`, `lead_id`, `lead_ids`, `list_id`, `lead_run_id`,
   `job_id`) nie mit `workspace`, auch nicht `import_leads` oder `export_leads` mit `list_id`: Sie
   laufen von selbst im Workspace des Objekts. Passen Angabe und Objekt nicht zusammen, lehnt der
   Server mit `workspace_mismatch` ab. Liste und Kampagne eines Aufrufs müssen im selben Workspace
   liegen.
4. **Vor jedem Schreiben und jedem Lauf den Workspace nennen**, etwa „Ich importiere 120 Leads in
   Agentur Nord.“ Ein Server-Lauf rechnet über das Guthaben des Workspaces der Kampagne ab.
5. **Antworten lesen.** Jede nennt ihren Workspace (`workspace` mit `name` und `role`). Wechselt er,
   das dem Nutzer in einem Satz sagen. Fehlt eine bekannte Kampagne in `list_campaigns`, liegt sie
   vielleicht in einem anderen Workspace.
6. **Rolle `viewer`:** Dort geht nur Lesen. Schreib-Werkzeuge lehnt der Server mit
   `workspace_read_only` ab. Nichts importieren, anlegen, starten oder freigeben, sondern dem Nutzer
   sagen, dass er dafür Mitglied oder Admin des Workspaces sein muss.
7. **Älterer Server** (kein `list_workspaces` in der Tool-Liste): Alles läuft im Standard-Workspace.
   `workspace` nie mitgeben und Workspaces nicht erwähnen.
