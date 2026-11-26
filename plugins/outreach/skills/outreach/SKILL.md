---
name: outreach
description: Einstieg für alles rund um Outreach-Kampagnen. Verwenden bei „outreach“, „was kann ich hier machen“, „wo fange ich an“, „Kampagne starten“, „Hilfe zu Outreach“, „woher bekomme ich Leads“, „wie viele Credits habe ich“, „Guthaben“, „freie Plätze“, „Credits nachkaufen“, „Close“, „CRM“, „was ist in Close“ oder wenn unklar ist, welcher Outreach-Skill passt. Fragt kurz nach dem Ziel und leitet an den passenden Skill weiter. Enthält die Workspace-Regel und die Melde-Regel (Fehler und Wünsche an DealSupply melden), die alle Outreach-Skills befolgen.
---

# Outreach – Einstieg

Dieser Skill leitet weiter: Frage den Nutzer, was er erreichen will, und lade dann genau den
passenden Skill. Dazu hält er die Workspace-Regel und die Melde-Regel, auf die alle Outreach-Skills verweisen.

## Erst prüfen

- **Noch nicht eingerichtet?** (kein Outreach-MCP verbunden, erstes Mal, alte Skill-Kopien)
  → `outreach-setup`.
- **Verbunden und welche Version?** Ein Aufruf von `ping` (nur lesend) zeigt, ob die Verbindung steht, und nennt die Version des Servers. Sie gilt für das ganze Gespräch (Versions-Regel unten).
- **Workspace geklärt?** Sonst nach der Workspace-Regel unten, Punkt 1.

## Wohin

| Der Nutzer will … | Skill |
|---|---|
| eine Kampagne anlegen oder ändern | `outreach-campaign` |
| an einer bestehenden Kampagne eine Mail (Betreff, Text, Wartezeit), eine Einstellung (Name, Sprache, Anrede, Recherche-Stufe, Kriterien) oder einen Variablen-Prompt ändern, oder nur einen Teil ansehen | `outreach-campaign`, Phase 3, „Gezielt ändern“ (ab MCP 4.27.0: `get_campaign_part`, `update_campaign_mail`, `update_campaign_setting`; die Kampagne wird dafür nicht ersetzt) |
| mit dem Start-Satz aus der App eine Kampagne einrichten („Richte mit outreach die Kampagne #123 ein.“) | `outreach-campaign`, Ablauf „Genannte leere Kampagne füllen“: genau diese Kampagne füllen, nie eine neue anlegen |
| Cold-Mail-Copy schreiben oder prüfen, ein Marketing-Offer formulieren | `outreach-copy` (ab MCP 4.45.0 mit den Copy-Regeln der App aus `get_copy_rules`) |
| neue lokale Betriebe als Leads finden, nach Branche und Gebiet über Google Maps („Leads finden“, „Friseure in Freiburg“) | `outreach-leads-finden` (ab MCP 4.16.0): Angebot zeigen, nach Zustimmung starten, Stand abfragen, an eine Kampagne übergeben |
| Entscheider in Firmen finden, nach Rolle, Branche, Größe und Ort („Personensuche“, „Geschäftsführer finden“), und ihre E-Mail-Adressen suchen | `outreach-personensuche` (ab MCP 4.16.0): blättern kostet in der Regel nichts, Übernahme und E-Mail-Suche je nach Zustimmung zum Angebot |
| mehr Firmen wie die guten Leads einer Kampagne, wie ein einzelner Lead oder wie Beispiel-Websites („ähnliche Firmen“, „mehr Firmen wie diese“) | `outreach-aehnliche-firmen` (ab MCP 4.16.0): ansehen kostet nichts, übernommen wird nach Zustimmung zum Angebot. Nicht jedes Konto hat die Funktion schon; das zeigt erst der erste Aufruf (`feature_disabled`) |
| Stand einer laufenden Suche nach neuen Leads, weitersuchen, abbrechen | `outreach-leads-finden` bzw. `outreach-personensuche` |
| Leads importieren (CSV, Liste) | `outreach-import` |
| Listen ansehen, anlegen, in eine Kampagne übernehmen | `outreach-lists` |
| Leads zählen oder filtern wie in der Filterspalte der App, im ganzen Bestand („wie viele Leads aus Wien habe ich?“, „welche Städte sind im Bestand?“) oder in einer Kampagne („wie viele Leads der Kampagne 80 sind aus Wien?“, „wie viele warten dort auf die Freigabe?“), Ansichten ansehen, speichern oder löschen | `outreach-lists`, Abschnitt „Filter und Ansichten“ (ab MCP 4.32.0: `describe_lead_filters`, `count_leads`, `list_lead_views`, `save_lead_view`, `delete_lead_view`). Bestand: `place="global"`; Frage zu einer Kampagne: `place="campaign"` mit `campaign_id`. Für die Auswahl eines Laufs `outreach-pipeline` |
| Leads qualifizieren | `outreach-qualify` |
| Leads recherchieren | `outreach-research` |
| Mail-Variablen generieren | `outreach-generate` |
| generierte Mails prüfen und freigeben | `outreach-verify` |
| alles in einem Lauf (qualifizieren → recherchieren → generieren), auf dem Server oder im eigenen Abo | `outreach-pipeline` (fragt nach der Laufart) |
| einen Abo-Lauf direkt ausführen oder fortsetzen („Abo-Lauf“, „im Abo“, „ohne Server“, „als Workflow“) | `outreach-abo-lauf` |
| Leads einer Kampagne als Excel oder CSV herunterladen (Freigaben, für Instantly, fürs CRM) | `outreach-export` |
| Versand vorbereiten: Domains, Postfächer, Warm-up, Instantly, Auswertung | `outreach-launch` |
| neue Leads mit eigenem Konto bei Apify oder Outscraper beschaffen | `datenbeschaffung` – gehört zum Plugin **datenbeschaffung**; ist es nicht installiert, auf `outreach-setup` verweisen |
| prüfen, welches Offer sich mit KI liefern lässt, oder für einen Lead, der geantwortet hat, die versprochene Demo bauen (Webseiten-Entwurf, SEO, Anzeigen, Leadliste, Muster-Kampagne) | `fulfillment` – gehört zum Plugin **fulfillment**; ist es nicht installiert: `/plugin install fulfillment@outreach-plugins` (Claude Code) bzw. im Marketplace installieren |
| Guthaben, Credits, Preise, Limits, freie Plätze im Account, Nachkauf | kein eigener Skill: direkt `get_credit_balance` (nur lesend) aufrufen und erklären, siehe unten |
| eine in der App eingerichtete Kampagne freigeben (`setup_state: open`, `start_lead_run` meldet `setup_open`) | `outreach-campaign`, Schritt „Freigeben“: `release_campaign` nur nach ausdrücklichem Ja (ab MCP 4.9.0) |
| Power-ups einer Kampagne ansehen oder schalten (E-Mail prüfen, Person finden) | kein eigener Skill: `list_power_ups(campaign_id)` (nur lesend); `set_power_up` nur auf ausdrücklichen Wunsch, Treffer kosten Credits (ab MCP 4.6.0) |
| für einen Lead den Schwerpunkt des Angebots von Hand setzen („trotzdem mit Haupt-Offer schreiben“) | kein eigener Skill: `set_offer_focus(campaign_id, lead_id, rank)` nur auf ausdrücklichen Wunsch (ab MCP 4.11.0); überstimmt die Schwerpunkt-Prüfung, danach neu generieren |
| Stand der Übertragung ins CRM Close, eine Kampagne nach Close an- oder ausschalten | kein eigener Skill: `get_close_status` (nur lesend) bzw. `set_close_sync`, siehe unten |
| einen Fehler oder Wunsch an DealSupply melden („melde das“, „das sollte gehen“, „kann DealSupply das nicht?“), sehen, was aus einer Meldung wurde | kein eigener Skill: Melde-Regel unten |
| Plugin aktualisieren | `outreach-update` |

## Guthaben und Limits erklären

`get_credit_balance` liefert alles in einem Aufruf:

- `billing_mode`: `credits` (Plattform-Credits) oder `byok` (das Konto zahlt die KI mit dem eigenen
  OpenRouter-Key; dann gibt es keine Credits, keine Preise und keinen Nachkauf, alle Credit-Felder sind `null`).
- `own_ai_key` (ab MCP 4.37.0): `true` heißt, ein Credit-Konto lässt seine KI über den eigenen
  OpenRouter-Schlüssel laufen (Option im Tarif, einschalten in den Workspace-Einstellungen, Reiter KI).
  `billing_mode` bleibt `credits`, und das Guthaben gilt weiter, zahlt aber nur Power-ups und Daten
  (Leads finden, Personensuche); die KI im Server-Lauf kostet keine Credits, dafür zählt die Lauf-Quote des
  Plans (`outreach-pipeline`). Das ist nicht `byok`: Credits, Nachkauf und Power-ups bleiben.
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
  selbst in der App. Sonst bleiben ein Planwechsel, eine geringere Denktiefe der Agents oder eine günstigere
  Recherche-Stufe (das KI-Modell wählt ab MCP 4.31.0 die App, nicht mehr der Nutzer), oder der Abo-Lauf, der
  keine Credits kostet.

Preise je Lead nie aus dem Gedächtnis nennen: Den verbindlichen Preis zeigt `quote_lead_run` vor einem
Server-Lauf (`outreach-pipeline`). Wer ein Jahresabo hat, wechselt erst nach Ende der Laufzeit auf ein
Monatsabo; mehr nicht zusagen.

## Close erklären (ab MCP 4.8.0)

Mit verbundenem und eingerichtetem Close überträgt die App jeden Lead, an den Instantly verschickt
hat, in die Close-Org des Kunden: mit Stufe (`sent`, `opened`, `clicked`, `neutral_reply`,
`interested`, `not_interested`, `do_not_contact`), Antwort und Briefing-Notiz. Verbinden und
Einrichten gehen nur in der App (Integrationen → Close), ebenso Einstiegsstufe und Lead-Status je
Stufe; beides gilt für alle Kampagnen.

- `get_close_status` (nur lesend): Verbindung, Leads je Status (`waiting`, `pushed`, `failed`) im
  Workspace und die zuletzt fehlgeschlagenen mit Grund; mit `campaign_id` auch, ob die Kampagne
  nach Close geht. Fehlen `counts`, ist Close nicht verbunden, gestört oder abgeschaltet.
- `set_close_sync`: `campaign_id`, `enabled` (an oder aus), optional `transfer_backlog=false` (nur
  Outreach ab jetzt). Nur auf ausdrücklichen Wunsch des Nutzers ändern.
- Ein Lead mit `do_not_contact` (Abmeldung, Bounce, Sperre) kommt nie neu nach Close; steht er schon
  dort, bekommt er nur diese Stufe. Gelöscht wird in Close nie etwas.

## Regeln

- Nichts Kostenpflichtiges starten, ohne dass der Nutzer genau diesen Umfang freigibt.
- Für alles, was Credits kostet, gilt dieselbe Reihenfolge: erst das Angebot holen (`quote_…`), es dem
  Nutzer zeigen, auf sein Ja zu genau diesem Angebot warten, erst dann starten. Das gilt für Server-Läufe
  (`quote_lead_run`), Leads finden (`quote_prospect_search`), die Übernahme von Personen
  (`quote_people_import`), die E-Mail-Suche (`quote_people_email_search`) und die Übernahme ähnlicher
  Firmen (`quote_similar_companies_import`).
- Kennt der Nutzer sein Ziel nicht, zuerst eine Frage: „Willst du eine neue Kampagne aufsetzen,
  Leads verarbeiten oder neue Leads beschaffen?“

## Versions-Regel

Gilt für jeden Outreach-Skill. Viele Stellen sagen „ab MCP x“. So wird das geprüft, ohne doppelte Aufrufe:

1. **Die Version kommt aus `ping`, einmal je Gespräch.** Ist sie im Gespräch schon bekannt (dieser Einstieg, `outreach-setup`, Schritt 0 eines anderen Skills), nicht noch einmal aufrufen. Ein Skill, der direkt aufgerufen wird und die Version braucht, ruft `ping` als Erstes auf.
2. **Ein neues Werkzeug:** Steht es in der Tool-Liste deiner Umgebung, kennt der Server es; dafür braucht es kein `ping`. Fehlt es, gilt der Weg für ältere Server, den der Skill nennt.
3. **Ein neuer Parameter oder ein neues Feld an einem alten Werkzeug** (etwa `filter` und `view_id`, `budget_credits`, `confirm_pushed_sequence_change`): Das zeigt die Tool-Liste nicht verlässlich. Hier entscheidet die Version aus `ping`. Einen Parameter, den die Version nicht kennt, nie mitschicken: Ältere Server übergehen ihn ohne Fehler.
4. `list_campaigns` prüft nicht die Version, sondern nur, ob Kampagne und Workspace zum Auftrag passen.

## Workspace-Regel

Gilt für jeden Outreach-Skill, auch wenn er direkt aufgerufen wird. Eine Verbindung reicht für alle
Workspaces des Nutzers. Kampagnen, Leads, Listen, Läufe und Guthaben gehören zu genau einem
Workspace, auch der Bestand für den Dubletten-Abgleich.

1. **Workspace kennen.** Ist er im Gespräch noch nicht geklärt, `list_workspaces` aufrufen (nur
   lesend). Hat `ping` schon `workspace_count: 1` gemeldet, gibt es nur einen: Dann genügt der
   Name aus `ping` (`default_workspace`) bzw. aus der ersten Antwort, `list_workspaces` ist nur
   nötig, wenn die Rolle gebraucht wird. Ein Workspace: weiter, ohne zu fragen. Mehrere: Name, Rolle und Plan zeigen, fragen, in
   welchem gearbeitet wird, und die Wahl für das Gespräch merken.
2. **Aufrufe ohne Objekt-ID** bekommen `workspace=<uuid>`, wenn der gewählte Workspace nicht der
   Standard ist (`default: true`). Das betrifft die Werkzeuge zum Auflisten, Suchen, Prüfen,
   Importieren und Anlegen, etwa `list_campaigns`, `search_leads`, `list_lists`, `list_lead_runs`,
   `export_leads`, `check_leads_exist`, `import_leads`, `create_campaign`, `create_list`,
   `get_credit_balance` und `mark_leads_contacted` mit E-Mail-Adressen. Ohne Angabe laufen sie im
   Standard-Workspace. Ab MCP 4.32.0 gehören dazu auch `describe_lead_filters`, `count_leads`,
   `list_lead_views` und `save_lead_view` am Ort `global` sowie jedes Werkzeug, das seine Leads über
   `filter` oder `view_id` der Lead-Datenbank statt über IDs wählt; mit `campaign_id` (Ort `campaign`
   oder `review`) entscheidet die Kampagne. Dasselbe gilt für `quote_prospect_search`, `start_prospect_search` ohne
   `search_id`, `list_prospect_searches` (auch mit `kind="people"`), `list_prospect_area_postal_codes`,
   `create_people_search`, `find_similar_companies` und für `quote_similar_companies_import` und
   `import_similar_companies` mit `example_domains`; Werkzeuge mit `search_id` laufen im Workspace der
   Suche, die ähnlichen Firmen eines Leads oder einer Kampagne im Workspace des Objekts. Eine unbekannte uuid lehnt der Server mit `workspace_not_found` ab.
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

## Melde-Regel: Fehler und Wünsche an DealSupply (ab MCP 4.33.0)

Gilt für jeden Outreach-Skill, auch wenn er direkt aufgerufen wird. Nur wenn der Server
`report_feedback` in seiner Tool-Liste führt (ab MCP 4.33.0, und nur, wenn DealSupply das Melden für den
Server eingerichtet hat). Fehlt das Werkzeug, auf „Melden“ in der App verweisen und nichts weiter tun.

1. **Fehler des Produkts.** Schlägt ein Aufruf fehl und du kannst es nicht selbst lösen, oder schildert
   der Nutzer etwas, das nicht funktioniert: in ein, zwei Sätzen sagen, was schiefging, dann fragen:
   „Soll ich das als Fehler an DealSupply melden? Ich hänge an, was der Server zu dem Aufruf
   aufgezeichnet hat. Du musst nichts erklären.“ Dann auf die Antwort warten.
2. **Selbst lösbar ist kein Fehler.** Falsche oder fremde ID, fehlendes Argument, `validation_failed`,
   `insufficient_scope`, `workspace_read_only`, `workspace_mismatch`, `setup_open`, `rate_limited`,
   erschöpfte Credits oder Limits: beheben oder dem Nutzer erklären, keine Meldung anbieten. Punkt 1
   gilt erst, wenn es danach weiter scheitert oder der Fehler unerklärlich ist (`internal_error`, ein
   Abbruch ohne Grund, ein Ergebnis, das nicht stimmen kann).
3. **Wunsch.** Will der Nutzer etwas, das DealSupply nicht kann (kein Werkzeug, keine Einstellung dafür):
   klar sagen, dass es heute nicht geht, und anbieten: „Soll ich das als Wunsch an DealSupply melden?“
   Dazu in einem Satz, was du schreiben würdest.
4. **Nur nach einem Ja melden**, mit `report_feedback`:
   - `kind`: `bug` (Fehler), `wish` (Wunsch) oder `question` (Frage).
   - `text`: erste Zeile ein kurzer Titel, dann was der Nutzer versucht und was er erwartet hat, in seinen
     Worten und seiner Sprache.
   - Bei einem Fehler `attach_last_failure=true`: Dann geht die Aufzeichnung des Servers mit (Werkzeug,
     Argumente ohne Geheimnisse, Fehler, Zeit). Fehlertexte und Argumente nicht selbst abschreiben.
     Ist nicht der letzte fehlgeschlagene Aufruf gemeint, `failed_call_id` aus `recent_failed_calls`
     eines früheren Ergebnisses.
   - Optional `campaign_id` und `area` (`Kampagnen`, `Leads`, `Mails`, `Versand`, `Integrationen`,
     `Konto und Abrechnung`).
5. **Nichts Geheimes, keine Daten Dritter.** In `text` nie API-Schlüssel, Passwörter oder Tokens und nie
   Namen, E-Mail-Adressen oder Telefonnummern von Leads. Die Kampagne nennen statt der Personen.
6. **Danach** bestätigen, den Titel nennen und sagen, wo der Nutzer den Stand sieht: „Den Stand findest
   du in DealSupply unter Roadmap, Reiter Meine Meldungen.“ (`app_url` der Antwort). Bei einem Fehler
   anbieten, den Schritt später noch einmal zu versuchen; bei einem Wunsch sagen, dass er auf der Roadmap
   mit „Will ich auch“ dafür stimmen kann, sobald er dort steht. Ändert sich der Stand, zeigt die App einen
   Punkt an „Roadmap“.
   - `rate_limited`: Höchstens 10 Meldungen je Stunde und Person, zusammen mit der App. Dem Nutzer sagen,
     wann es wieder geht (steht in der Meldung), und nicht gleich wiederholen.
   - `feedback_failed`: Die Meldung ist nicht angekommen. Das sagen und auf „Melden“ in der App verweisen,
     dort geht auch ein Bildschirmfoto mit.
7. **Sagt der Nutzer nein:** nichts melden, weitermachen und für dasselbe nicht noch einmal fragen.
   Dasselbe nie zweimal melden.
8. **Agents und Workflows** (`lead-agent`, `verify-agent`, Abo-Lauf) melden nie und fragen nicht. Sie
   nennen einen Fehler, den sie nicht lösen können, mit Werkzeug und Fehlercode in ihrer Antwort. Die
   Sitzung, die den Lauf gestartet hat, fragt den Nutzer nach dem Bericht einmal für alle zusammen.
