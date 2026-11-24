---
name: outreach-autopilot
description: Use when user says "Autopilot", "Autopilot einrichten", "Autopilot einschalten", "Autopilot pausieren", "Kampagne von allein auffüllen", "automatisch Leads nachkaufen", "Nachschub automatisch", "Agent 24/7", "was hat der Autopilot gemacht", "Autopilot wartet", "Vorschlag des Autopiloten", "Testlauf des Autopiloten", or wants a campaign to keep itself supplied with new leads. Richtet den Autopiloten einer Kampagne ein (set_up_autopilot, suggest_autopilot_search_order), zeigt mit dem Testlauf, was er bringt (start_autopilot_trial), schaltet ihn (switch_autopilot), liest Zustand, Lagebild, Verbrauch und Eingang (get_autopilot) und beantwortet seine Vorschläge (answer_autopilot_proposal).
---

# Autopilot: die Kampagne füllt sich von allein nach

> **Workspace:** Es gilt die Workspace-Regel aus dem Skill `outreach`. Alle Werkzeuge dieses Skills nehmen eine `campaign_id` und laufen von selbst im Workspace der Kampagne.
>
> **Fehler und Wünsche:** Es gilt die Melde-Regel aus dem Skill `outreach`: Nach einem Fehler, den du nicht selbst lösen kannst, fragen, ob du ihn an DealSupply melden sollst, und erst nach einem Ja `report_feedback` mit `attach_last_failure=true` aufrufen. Einen Wunsch, den DealSupply nicht kann, als Wunsch melden anbieten.

Der Autopilot gehört zu genau einer Kampagne. Eingeschaltet schaut er mehrmals am Tag nach, wie lange der Vorrat an fertigen Leads beim heutigen Sendetempo noch reicht. Reicht er nicht, sucht er neue Firmen oder Personen, übergibt sie der Kampagne und lässt Qualifizierung, Recherche und Mails laufen, alles innerhalb eines Tagesbudgets. Er verlässt nie von allein sein maximales Gebiet und ändert nie von allein seine Filter: Braucht er mehr, wartet er und macht einen Vorschlag.

| Teil | Werkzeug | Kosten |
|---|---|---|
| Lesen | `get_autopilot` | nichts |
| Einrichten | `set_up_autopilot` | nichts, es kauft nichts |
| Suchauftrag vorschlagen lassen | `suggest_autopilot_search_order` | nichts oder ein Bruchteil eines Credits (`cost_credits`) |
| Testlauf | `start_autopilot_trial` | Credits, höchstens `trial.max_credits` |
| Schalten | `switch_autopilot` | das Schalten nichts; eingeschaltet gibt er bis zum Tagesbudget aus |
| Vorschlag beantworten | `answer_autopilot_proposal` | nichts; ein angenommener Vorschlag lässt ihn weiterkaufen |

## Die drei Regeln

1. **Einschalten nur auf ausdrückliches Wort.** `switch_autopilot(action="enable")` und `"resume"` geben dem Autopiloten die Erlaubnis, jeden Sendetag von allein Credits auszugeben. Vorher Suchauftrag, maximales Gebiet, Tagesbudget und Art der Freigabe in einem Satz zusammenfassen und auf das Ja zu genau diesem Stand warten. Ein Ja von früher im Gespräch gilt nicht für einen geänderten Stand.
2. **Kein Testlauf ohne Zustimmung zum Höchstbetrag.** `trial.max_credits` aus `get_autopilot` nennen, dann auf das Ja warten.
3. **Zahlen nur aus den Antworten.** Preise, Leads je Tag und Budgets nie schätzen. `get_autopilot` liefert sie unter `budget`, `situation` und `trial`.

Pausieren und Abschalten brauchen keine Rückfrage, wenn der Nutzer es verlangt: Sie stoppen Ausgaben.

## Voraussetzungen

1. `ping`: Die Werkzeuge gibt es ab MCP 4.48.0. Fehlen sie in der Tool-Liste, obwohl der Server neu genug ist, ist der Autopilot für dieses Konto noch nicht freigeschaltet. Das dem Nutzer so sagen und nichts nachbauen (keine eigene Schleife aus Leads finden und Läufen).
2. Die Kampagne braucht eine fertige Einrichtung mit Sequenz und eine Verknüpfung mit Instantly. Ohne Instantly gibt es den Autopiloten noch nicht. Fehlt etwas, nennt `get_autopilot` es unter `readiness.blockers`.
3. `get_credit_balance`: `available` merken. Bei `account.subscription_required` zuerst einen Plan wählen lassen.

## Ablauf: einrichten

### 1. Stand lesen

`get_autopilot(campaign_id)`. Bei `autopilot: null` gibt es noch keinen (`readiness.blockers` nennt dann `autopilot_missing` und dahinter, was der Kampagne selbst noch fehlt). Sonst steht unter `autopilot.state`, wo er ist:

| `state` | Bedeutung |
|---|---|
| `setup` | angelegt, noch nicht eingeschaltet |
| `working` | eingeschaltet, arbeitet |
| `waiting` | eingeschaltet, wartet auf etwas (`waiting_reason`) |
| `paused` | vom Nutzer angehalten |
| `off` | abgeschaltet, Einstellungen bleiben |

### 2. Suchauftrag klären

Fragen, wen der Autopilot suchen soll: **Firmen** (Google Maps, `search_kind="maps"`) oder **Personen** (`search_kind="people"`).

Den Auftrag nicht raten. Zwei Wege:

- **Vorschlag der App:** `suggest_autopilot_search_order(campaign_id, kind)`. Die App liest Angebot, Zielgruppe, Region und die Leads, die die Kampagne schon als passend beurteilt hat. `source` sagt, woher der Vorschlag kommt:
  - `linked_search`: übernommen aus der Suche, aus der die Leads der Kampagne stammen, kostenlos.
  - `ai`: von der KI, kostet einen Bruchteil eines Credits (`cost_credits`).
  - `insufficient`: Die Kampagne sagt zu wenig. `missing` nennt, was fehlt (`audience`, `region`, `offer`). Den Nutzer danach fragen.
  - `unavailable`: gerade kein Vorschlag möglich, dann den Auftrag mit dem Nutzer von Hand klären.
  
  Für Firmen kommen `categories` (gesetzt), `further_categories` (könnten auch passen, als Angebot an den Nutzer), `start_areas`, `max_areas`, `filters`, `unresolved_trades` (hat der Katalog nicht) und `note` (Begründung). Für Personen kommen `people_filter`, `people_labels` und `unresolved`. Der Vorschlag speichert nichts.
- **Von Hand:** Branchen über `search_prospect_categories`, Gebiete über `search_prospect_areas`, Werte der Personenfilter über `search_people_filter_values` (Skills `outreach-leads-finden` und `outreach-personensuche`).

Dem Nutzer den Auftrag zeigen und sein Ja abwarten, dann speichern.

### 3. Speichern

`set_up_autopilot(campaign_id, …)` legt den Autopiloten an, falls es keinen gibt, und speichert, was du übergibst. Alles Weggelassene bleibt, wie es gespeichert ist. Ein Aufruf darf also einen einzelnen Teil setzen.

**Firmen:**

```
set_up_autopilot(
  campaign_id=…,
  search_kind="maps",
  category_keys=["gcid:electrician"],
  start_areas=[{"area_key": "de:city:saarland:saarbruecken", "radius_km": 10}],
  exclude_chains=true,
  max_areas=[{"area_key": "de:state:saarland"}],
  daily_budget_credits=30,
  approval_mode="manual",
  start_send_rate_per_day=20
)
```

- `start_areas`: wo die Suche beginnt. Von dort geht der Autopilot Schritt für Schritt weiter.
- `max_areas`: das größte Gebiet, in dem er je suchen darf. Pflicht bei Firmen.
- `min_rating`, `min_reviews`: optional, `0` löscht den Wert wieder.
- Listen (`category_keys`, `start_areas`, `max_areas`) ersetzen die gespeicherte Liste, sie hängen nichts an.

**Personen:**

```
set_up_autopilot(
  campaign_id=…,
  search_kind="people",
  people_filters={"lists": {"job_titles": {"include": ["Geschäftsführer"]}}},
  daily_budget_credits=30,
  approval_mode="manual"
)
```

- `people_filters` hat die Form von `create_people_search`. Mindestens ein Filter ist Pflicht.
- Personen haben kein Gebiet, `max_areas` entfällt.
- Personen kommen ohne E-Mail-Adresse. Die Kampagne braucht dafür das E-Mail-Power-up, sonst nennt `readiness.blockers` `email_finder_off` (`set_power_up`, Skill `outreach-campaign`).

**Grenzen:**

| Parameter | Bedeutung |
|---|---|
| `daily_budget_credits` | das Höchste, was er an einem Tag für Suche, Recherche und Mails zusammen ausgibt |
| `approval_mode` | `manual`: Der Nutzer gibt jede Mail frei. `direct`: Mails der eigenen Leads des Autopiloten werden freigegeben, wie sie geschrieben sind |
| `start_send_rate_per_day` | neue Leads, die Instantly am Tag anschreibt, als Startwert, bis der Autopilot das echte Tempo gemessen hat |
| `refill_below_workdays` | nachfüllen, sobald der Vorrat unter so viele Sendetage fällt (Standard 3) |
| `target_workdays` | auffüllen bis auf so viele Sendetage (Standard 7), muss über `refill_below_workdays` liegen |
| `backlog_limit` | bei `manual`: nichts mehr kaufen, sobald so viele Mails auf Freigabe warten (Standard 150) |

**Das Tagesbudget begründen.** Nach dem Speichern eines Suchauftrags `get_autopilot` lesen: `budget.full_supply` nennt, was den Versand voll versorgt (`daily_credits`, `leads_per_day`), `budget.plan_spread` verteilt die verfallenden Credits des Plans bis zum Verfall, `budget.credits_per_lead` den Preis je Lead. `situation.instantly.suggested_new_leads_per_day` ist, was die Instantly-Kampagne am Tag an neuen Leads zulässt, und der passende Startwert für `start_send_rate_per_day`. Dem Nutzer die Varianten nennen und ihn wählen lassen. `budget.minimum_daily_credits` ist die Untergrenze: Ein Durchgang holt mindestens zehn Leads, ein Tagesbudget darunter kauft nie etwas. Liegt der Wunsch des Nutzers darunter, das sagen, statt es still zu speichern.

**Art der Freigabe.** `direct` verschickt ohne menschlichen Blick. Nur setzen, wenn der Nutzer das ausdrücklich will, und es ihm so sagen.

### 4. Testlauf

`start_autopilot_trial(campaign_id)` sucht rund zehn Firmen oder Personen mit dem gespeicherten Auftrag und lässt die Kampagne sie beurteilen. Er ist die letzte Bedingung vor dem Einschalten.

1. `get_autopilot` → `trial.max_credits` nennen, auf das Ja warten.
2. `start_autopilot_trial(campaign_id)` → `status: "running"`.
3. Alle 20 bis 30 Sekunden `get_autopilot` lesen, bis `trial.status` `finished` ist. Das dauert ein paar Minuten. Nicht schneller abfragen.
4. Ergebnis zeigen: `trial.companies` mit Firma oder Person, Ort, `fit_level` und Begründung (`summary`), dazu `trial.total`, `trial.judged`, `trial.fit_count`.

Passen die Treffer nicht, den Suchauftrag mit dem Nutzer ändern (`set_up_autopilot`) und den Testlauf wiederholen. Ein Wechsel zwischen Firmen und Personen verwirft einen bestandenen Testlauf.

| Antwort | Bedeutung | Was tun |
|---|---|---|
| `trial.outcome` `failed`, `trial.failure` gesetzt | abgebrochen, der Text nennt den Grund | Grund weitersagen, beheben, neu starten |
| `trial.outcome` `no_verdict` | gefunden, aber keine Firma oder Person wurde beurteilt; der Testlauf gilt nicht als bestanden | Qualifizierung der Kampagne prüfen (Skill `outreach-campaign`), dann neu starten; der neue Testlauf kostet erneut |
| `trial.outcome` `nothing_found` | der Auftrag findet nichts | Auftrag weiter fassen |
| `autopilot_cycle_running` | es läuft schon ein Durchgang | warten und `get_autopilot` lesen |
| `autopilot_not_in_setup` | der Autopilot ist nicht mehr in der Einrichtung | den Testlauf gibt es nur vor dem Einschalten, nicht wiederholen |
| `usage_limit_exceeded` | das Lead-Limit des Kontos lässt keine zehn neuen Leads zu | Platz schaffen oder Plan wechseln, Credits helfen nicht |
| `autopilot_not_ready` | es fehlt noch etwas, die Punkte stehen im Text | Punkte abarbeiten |

### 5. Einschalten

Zusammenfassen: wen er sucht, wo höchstens, wie viel am Tag, wie freigegeben wird. Auf das Ja warten. Dann `switch_autopilot(campaign_id, action="enable")`.

Bei `autopilot_not_ready` stehen die offenen Punkte im Text und unter `readiness.blockers`:

| Blocker | Bedeutung |
|---|---|
| `search_order_missing`, `max_area_missing`, `budget_missing` | in der Einrichtung fehlt dieser Teil |
| `trial_missing` | noch kein bestandener Testlauf |
| `setup_open`, `sequence_missing` | die Kampagne selbst ist nicht fertig (Skill `outreach-campaign`) |
| `no_instantly_link`, `no_instantly_connection` | die Kampagne ist nicht mit Instantly verknüpft oder Instantly nicht verbunden; das geht nur in der App |
| `agent_unavailable` | die Kampagne nennt einen Agenten, den das Konto nicht hat |
| `email_finder_off` | Personen-Auftrag ohne E-Mail-Power-up |
| `prospect_unavailable` | Leads finden steht dem Konto gerade nicht zur Verfügung |

## Ablauf: begleiten

### Was hat er getan?

`get_autopilot(campaign_id, events=20)`:

- `situation`: Vorrat in Sendetagen (`days_of_supply`) gegen das Ziel (`target_workdays`), Sendetempo (`pace`), was fehlt (`shortfall_leads`), Engpass (`bottleneck`).
- `budget.today`: Tagesbudget, heute ausgegeben, heute noch frei.
- `events`: die neuesten Einträge seines Eingangs, neueste zuerst. `kind` und `message_key` sagen, was geschah, `params` tragen die Zahlen, `reasoning` seine Begründung, `cost_credits` die Kosten. Dem Nutzer in eigenen Worten berichten, die Schlüssel nicht vorlesen.
- `autopilot.next_beat_at`: wann er das nächste Mal nachschaut.

### Er wartet

Bei `state: "waiting"` sagt `waiting_reason`, worauf:

| `waiting_reason` | Bedeutung | Was hilft |
|---|---|---|
| `area_exhausted` | im maximalen Gebiet findet er nichts Neues mehr, oder die Personenfilter sind ausgeschöpft | einen Vorschlag annehmen oder Gebiet bzw. Filter mit `set_up_autopilot` erweitern |
| `review_backlog` | zu viele Mails warten auf Freigabe | Mails freigeben (Skill `outreach-verify`) |
| `credits_exhausted` | das Guthaben ist leer | Credits kaufen lassen |
| `lead_limit` | das Lead-Limit des Kontos ist erreicht | Platz schaffen oder Plan wechseln, Credits helfen nicht |
| `pace_unknown` | er kennt das Sendetempo nicht | `start_send_rate_per_day` setzen |
| `setup_open` | die Einrichtung der Kampagne ist wieder offen | Kampagne fertigstellen |
| `instantly_error` | Instantly antwortet nicht wie erwartet oder die Verknüpfung fehlt | in der App prüfen |
| `prospect_unavailable` | Leads finden ist gerade nicht verfügbar | später wieder lesen |
| `run_blocked` | der Lead-Lauf kann nicht starten | `events` lesen, der letzte Eintrag nennt den Grund |

Er arbeitet von allein weiter, sobald der Grund weg ist.

### Vorschläge

Unter `autopilot.proposals` stehen offene Vorschläge mit `id`, `kind`, `change` und `reasoning`:

- `new_area`: ein weiteres Gebiet zum maximalen Gebiet.
- `new_categories`: weitere Branchen zum Suchauftrag.

Dem Nutzer den Vorschlag mit der Begründung zeigen. Auf sein Wort `answer_autopilot_proposal(campaign_id, proposal_id, decision="accept" | "reject")`. Angenommen wird die Änderung übernommen und der Autopilot arbeitet sofort weiter, also kauft er wieder innerhalb des Tagesbudgets. Abgelehnt bleibt alles, wie es ist, und er wartet weiter.

| Antwort | Bedeutung |
|---|---|
| `autopilot_proposal_decided` | über den Vorschlag wurde schon entschieden |
| `autopilot_proposal_outdated` | der Vorschlag gehört zur Firmensuche, der Autopilot sucht inzwischen Personen |
| `autopilot_proposal_not_found` | den Vorschlag gibt es nicht (mehr) |

### Pausieren, fortsetzen, abschalten

`switch_autopilot(campaign_id, action=…)`:

- `pause`: Er beginnt sofort nichts Neues mehr. Was schon bezahlt ist (eine laufende Suche, ein laufender Lead-Lauf), läuft zu Ende. Das dem Nutzer sagen.
- `resume`: setzt fort und prüft die Bedingungen erneut. Braucht das Wort des Nutzers wie das Einschalten.
- `disable`: schaltet ab. Die Einstellungen bleiben, er lässt sich wieder einschalten.

`autopilot_state_changed` heißt, dass er nicht in dem Zustand ist, den die Aktion braucht: `get_autopilot` lesen und neu entscheiden.

### Einstellungen ändern

`set_up_autopilot` mit nur dem Teil, der sich ändert, geht auch bei eingeschaltetem Autopiloten. Zwei Grenzen:

- Der Wechsel zwischen Firmen und Personen geht nicht, während ein Durchgang läuft (`autopilot_cycle_running`). Später noch einmal versuchen oder vorher pausieren und warten, bis der Durchgang durch ist.
- `autopilot_search_order_changed` oder `autopilot_settings_changed`: Jemand hat den Teil inzwischen geändert (auch ein angenommener Vorschlag). `get_autopilot` lesen, dem Nutzer den neuen Stand zeigen und die Änderung darauf neu aufsetzen.

## Fehler

| Code | Bedeutung | Was tun |
|---|---|---|
| `campaign_not_found`, `not_found` | Kampagne unbekannt oder der Autopilot ist für das Konto nicht freigeschaltet | `list_campaigns` prüfen, sonst dem Nutzer sagen, dass es den Autopiloten für sein Konto noch nicht gibt |
| `autopilot_not_found` | die Kampagne hat noch keinen Autopiloten | `set_up_autopilot` |
| `validation_failed` | eine Angabe passt nicht, der Text nennt das Feld | Angabe korrigieren |
| `insufficient_credits` | das Guthaben reicht nicht für den Testlauf | Credits kaufen lassen (nur wenn `get_credit_balance.purchase.allowed`) |
| `autopilot_trial_not_priced`, `autopilot_not_priced` | für diese Kampagne gibt es gerade keinen Preis | später erneut versuchen, sonst melden |
| `workspace_read_only` | Betrachter im Workspace | nur `get_autopilot` geht |
| `insufficient_scope` | der Verbindung fehlt die Berechtigung | Verbindung neu einrichten (Skill `outreach-setup`) |

## Verwandte Skills

- `outreach-leads-finden`: Branchen und Gebiete für einen Firmen-Auftrag, einmalige Suchen von Hand.
- `outreach-personensuche`: Filter für einen Personen-Auftrag.
- `outreach-campaign`: Kampagne, Sequenz und Power-ups.
- `outreach-verify`: Mails prüfen und freigeben, wenn der Autopilot wegen wartender Freigaben steht.
- `outreach-pipeline`: einzelne Läufe von Hand.
