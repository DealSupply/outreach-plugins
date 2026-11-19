---
name: outreach-lists
description: Use when user says "outreach:lists", "Listen anzeigen", "Liste anlegen", "Liste löschen", "was habe ich schon gescrapt", "Bestand prüfen", "Bestand exportieren", "Bestandsindex", "Liste in Kampagne", "bulk taggen", "wie viele Leads habe ich in …", "Leads filtern", "Ansicht speichern", "gespeicherte Ansichten", or wants to manage lead lists, lead filters and saved views in the Outreach app via MCP.
---

# Outreach Lists — Listen verwalten über den MCP

> **Live-Ansicht (Claude Code mit Plugin `outreach`):** Ergebnisse von `list_leads`, `import_leads`/`get_job_status` und Lead-Runs erscheinen dort als Karte bzw. im Band über dem Prompt. Dann die Liste **nicht noch einmal als Tabelle** wiederholen – nur kurz zusammenfassen, was der Nutzer wissen oder entscheiden muss. In anderen Umgebungen (Claude-Chat, ChatGPT, Codex) wie gewohnt als kurze Liste ausgeben.

> **Workspace:** Es gilt die Workspace-Regel aus dem Skill `outreach`: Workspace kennen, `workspace` nur bei Aufrufen ohne Objekt-ID mitgeben, vor jedem Schreiben oder Lauf den Workspace nennen.
>
> **Fehler und Wünsche:** Es gilt die Melde-Regel aus dem Skill `outreach`: Nach einem Fehler, den du nicht selbst lösen kannst, fragen, ob du ihn an DealSupply melden sollst, und erst nach einem Ja `report_feedback` mit `attach_last_failure=true` aufrufen. Einen Wunsch, den DealSupply nicht kann, als Wunsch melden anbieten.

Verwaltet Lead-Listen: die benannten Gruppierungen zwischen Beschaffung und Kampagne. Eine Liste entsteht aus einem eigenen Import (`outreach-import`), aus einer Suche über Leads finden (`outreach-leads-finden`) oder aus einer Übernahme der Personensuche (`outreach-personensuche`); neue Leads sucht dieser Skill nicht selbst.
Leads bleiben dabei immer normale Leads im Bestand ihres Workspaces — eine Liste ist eine Klammer mit
Herkunft, kein zweiter Datentopf. Bestand, Listen und Abgleich gelten je Workspace: Ein Index oder eine
Prüfung aus einem anderen Workspace zählt nicht, und Liste und Kampagne müssen im selben liegen.

Ab MCP 4.32.0 filtert und zählt der Skill den Bestand mit dem Filter der App und verwaltet gespeicherte
Ansichten (Abschnitt „Filter und Ansichten“).

Scope: `leads:read` fürs Lesen/Exportieren/Zählen, `leads:write` für Anlegen/Löschen/Verlinken und für Ansichten.

## Die Werkzeuge und wann welches

| Aufgabe | Tool | Hinweise |
|---|---|---|
| „Was habe ich schon (gescrapt)?" | `list_lists` | Zähler je Liste: total, in Kampagnen, kontaktiert; Herkunft (`source`) zeigt, was der Nutzer dort hinterlegt hat (z. B. Tool/Actor/Query/Datum/Kosten) |
| Liste durchsehen | `get_list(list_id, limit, offset)` | Neutraler Browse (`limit` 1–200, Standard 25) mit Kampagnen-Mitgliedschaften — OHNE die Pipeline-Filterlogik von `list_leads` |
| Liste anlegen | `create_list(name, description, source)` | `source` IMMER füllen (frei, z. B. {tool, actor, query, runAt, costUsd}) — sie ersetzt jedes manuelle Scrape-Log |
| Leads hineinbekommen | `import_leads(leads, list_id, attribute_mappings)` | Dedupliziert selbst: Bestands-Leads werden nur verlinkt; läuft async (`job_id`, per `get_job_status` abwarten), das Job-Result nennt `linked_to_list` + `do_not_contact_hits` |
| Bestand prüfen (Bulk) | `check_leads_exist(emails, domains)` | Bis 1.000 kombiniert je Call; E-Mail-Match inkl. Zweitadressen; Domain-Treffer nach ganzen Labels mit `match_kind`: `website_identity` = für eine Zeile ohne E-Mail derselbe Lead, `company_known` = „Firma bekannt" (Warnung, kein Ausschluss); ohne `match_kind` (älterer Server) derselbe Lead nur bei gleichem Host der `website`; Zeilen ohne E-Mail nur über `domains` prüfbar; Treffer gekappt (`summary.truncated`): alle Eingaben teilen sich einen Deckel von 10 mal Anzahl der Eingaben je Trefferliste, und bei `truncated` zählt die Zusammenfassung zu wenig (meist eine zu breite Domain wie „e.de“: Eingabe enger fassen); ab MCP 4.11.0 trifft eine E-Mail auch Person 2 einer Firma (`matched_via: second_person`); ab MCP 4.16.0 nennt ein Domain-Treffer `person_key`, wenn der Lead eine Person aus der Personensuche ist: ein solcher Treffer ist immer `company_known`, nie derselbe Lead, weitere Personen der Firma sind eigene Leads |
| Bestand exportieren (Leads einer Kampagne als Datei: `outreach-export`) | `export_leads(format, list_id, contact_status, limit, offset, filter, view_id)` | `json`/`csv` für Menschen und Tools (Seiten bis 10.000 Zeilen, `limit`/`offset`; `email` kann null sein); **`index`** ist der kompakte Abgleichsindex ({e, d, s} je Lead, `e` leer bei Leads ohne E-Mail, dann nur über `d` bekannt) für den Vorab-Dedup vor externen Scrape-Läufen. Ab MCP 4.16.0 tragen `json` und `csv` je Lead `googlePlaceId` und `googleCid` (im CSV die letzten Spalten). Ab MCP 4.32.0 engen `filter` und `view_id` (Ort `global`) den Export zusätzlich ein |
| Liste → Kampagne | `add_leads_to_campaign(campaign_id, list_id \| lead_ids \| filter/view_id)` | Überspringt `do_not_contact` IMMER und meldet es; verlinkte Leads starten als „processing", KI-Läufe startet erst `start_lead_run`. HARTES LIMIT 1000: Bei Listen > 1000 Leads wirft `list_id` `limit_reached`, dann IDs via `get_list` (limit max. 200, offset) paginiert holen oder per `export_leads(list_id=…, limit/offset)` und in Chunks bis 1000 über `lead_ids` verlinken. Ab MCP 4.32.0 auch die Leads eines Filters oder einer Ansicht der Lead-Datenbank (`filter`, `view_id`, genau eines von `list_id`, `lead_ids` oder Filter): mehr als 1000 Treffer lehnt der Server mit `limit_reached` ab, er schneidet nie ab |
| Batch taggen | `bulk_set_lead_attributes(lead_ids \| filter/view_id, attributes, create_missing)` | Gleiche Attributwerte auf bis zu 1.000 Leads in EINEM Call; für je-Lead-verschiedene Werte `write_lead_details`. Ab MCP 4.32.0 statt `lead_ids` auch `filter`/`view_id` (dann `workspace` nach der Workspace-Regel, der Filter hat keine Objekt-ID) |
| Global suchen/filtern | `search_leads(query, attribute_key/attribute_value, in_campaign, filter, view_id)` | Strukturfilter erlauben leere Text-Query; `in_campaign="none"` = noch unverplantes Rohmaterial. Ab MCP 4.32.0 engen `filter` und `view_id` zusätzlich ein, `query` darf dann leer sein |
| Wonach lässt sich filtern? | `describe_lead_filters(place, campaign_id)` | Ab MCP 4.32.0, nur lesend: Kategorien, Felder, Operatoren und feste Werte des Filters der App, dazu die Ansichten des Orts. Vor jedem Filter-Ausdruck lesen, Feldnamen nie raten |
| Wie viele Leads trifft ein Filter? Welche Städte, Kategorien, Tags gibt es? | `count_leads(place, campaign_id, filter, view_id, facets, value_search)` | Ab MCP 4.32.0, nur lesend: zählt, ohne Leads zu laden. Mit `facets` (bis 20 Auswahlfelder) die Zahl je Wert, wie die Filterspalte der App |
| Ansichten ansehen | `list_lead_views(place, campaign_id, with_counts)` | Ab MCP 4.32.0, nur lesend: Systemansichten und gespeicherte Ansichten mit Filter und Sortierung, mit `with_counts=true` samt Zahl |
| Filter als Ansicht speichern oder ersetzen | `save_lead_view(name, filter, place, campaign_id, visibility, sort_by, sort_direction, view_id)` | Ab MCP 4.32.0, schreibt: nur auf Wunsch des Nutzers, siehe „Filter und Ansichten“ |
| Ansicht löschen | `delete_lead_view(view_id)` | Ab MCP 4.32.0: nur nach Bestätigung; die Leads bleiben |
| Liste löschen | `delete_list(list_id, delete_leads, confirm_delete)` | s. Löschregeln |

## Filter und Ansichten (ab MCP 4.32.0)

Version nach der Versions-Regel im Skill `outreach`: Stehen die fünf Werkzeuge in der Tool-Liste, kennt
der Server sie; ob ein altes Werkzeug `filter` und `view_id` annimmt, sagt die Version aus `ping` (einmal
je Gespräch).

Die fünf Werkzeuge `describe_lead_filters`, `count_leads`, `list_lead_views`, `save_lead_view` und
`delete_lead_view` arbeiten mit demselben Filter wie die Filterspalte der App: Ein Ausdruck wählt
genau die Leads, die die App mit diesem Filter zeigt. Das ist der richtige Weg, sobald eine Frage
oder Auswahl mehr braucht als Suchtext, ein Attribut und `in_campaign`, und immer, wenn nur eine
Zahl gefragt ist („wie viele …?“): zählen statt Seiten laden.

**Orte (`place`):** `global` ist die Lead-Datenbank des Workspaces (Standard), `campaign` der
Leads-Reiter einer Kampagne, `review` der Review einer Kampagne; die beiden letzten brauchen
`campaign_id`. Ein Filter gilt für seinen Ort: `search_leads`, `export_leads`,
`add_leads_to_campaign`, `mark_leads_contacted` und `bulk_set_lead_attributes` nehmen Filter und
Ansichten des Orts `global`, `list_leads`, `quote_lead_run` und `start_lead_run` die des Orts
`campaign` (`outreach-pipeline`). Am Ort `global` haben die Aufrufe keine Objekt-ID: `workspace`
nach der Workspace-Regel mitgeben. **Welcher Ort:** Fragt der Nutzer nach dem Bestand („wie viele
Leads habe ich in Wien?“), ist es `global`. Nennt er eine Kampagne („wie viele in Kampagne 80?“),
ist es `place="campaign"` mit `campaign_id`: Nur dort gibt es die Felder der Kampagne (Urteil,
Stand der Mail, offene Arbeit), und die Zahl zählt nur Leads dieser Kampagne. Geht es um die
Reiter des Reviews, `place="review"`. Der Katalog unterscheidet sich je Ort: `describe_lead_filters`
immer mit demselben `place` und derselben `campaign_id` lesen wie die Zählung danach.

**Ablauf:**

1. `describe_lead_filters(place, campaign_id)` lesen: Felder (etwa `location.city`, `list.id`,
   `lead.score`, `lead.created_at`, `contact.status`), die Operatoren je Feld und die festen Werte.
   Feldnamen, Operatoren und Werte kommen aus dieser Antwort, nie aus dem Gedächtnis.
2. Ausdruck bauen: `{"v":1,"where":[…],"search":"Text"}`. Eine Bedingung ist
   `{"field","op","values"}` für `in` und `not_in`, `{"field","op","value"}` für `eq`, `contains`,
   `starts_with`, `gte`, `lte`, `before`, `after`, `last_days`, dazu `"to"` bei `between`, und nur
   `{"field","op"}` für `is_set` und `is_empty`. Alle Bedingungen in `where` gelten zusammen;
   `{"any":[…]}` gilt, wenn eine davon gilt. Der Wert `"__none__"` heißt „nicht gesetzt“. Mehrere
   positive Bedingungen auf Kampagnenfeldern gelten für dieselbe Kampagne; `not_in` und `is_empty`
   auf ihnen schließen einen Lead aus, sobald irgendeine Kampagne im Bereich passt.
3. Werte dynamischer Felder (im Katalog `dynamic: true`: Städte, Kategorien, Tags, Attribute) stehen
   nicht im Katalog, sondern an den Leads: `count_leads(…, facets=["location.city"])` listet sie mit
   Zahlen. Die Zahl je Wert zählt die Leads, die mit diesem Wert unter allen ANDEREN Bedingungen
   passen würden, genau wie die Spalte der App.
   - **Der Wert für den Filter ist der `key` der Facette, nicht das `label`.** Bei Städten ist der
     `key` klein geschrieben (`"baar"`), das `label` ist die Schreibweise für den Nutzer („Baar“).
     In `values` gehört immer der `key`; dem Nutzer zeigst du das `label`.
   - **Höchstens 50 Werte je dynamischem Feld.** Die Liste endet still nach den 50 Werten mit den
     meisten Leads (absteigend nach Zahl), die Antwort kennzeichnet das nicht. Kommen genau 50
     Werte, ist die Liste fast sicher unvollständig: nie als „alle Städte“ ausgeben und nie die
     Zahlen zu einer Gesamtzahl addieren (die Gesamtzahl ist `total`). Dem Nutzer sagen, dass es die
     50 häufigsten sind. Für „gibt es den Wert X?“ und für seltene Werte mit `value_search`
     nachfassen: Es sucht über die 50 hinaus nach Werten, die den Text enthalten (auch dort
     höchstens 50 Treffer). Felder mit festen Werten sind nicht begrenzt.
   - **Gleichstand bei „die meisten“:** Liegen zwei Werte vorn gleichauf, beide mit ihrer Zahl
     nennen und den Nutzer wählen lassen, nicht selbst einen nehmen. Dazu sagen, was gezählt ist:
     `count_leads` zählt alle Leads des Orts, die der Filter trifft, nicht nur die mit offener
     Arbeit. Ist „die meisten, für die noch etwas zu tun ist“ gemeint, die Bedingung `run.open_work`
     (Ort `campaign`) in den Filter nehmen und neu zählen; im Zweifel nachfragen.
   - **`"__none__"` bei dynamischen Feldern:** Der Katalog führt den Wert dort nicht als Option, er
     gilt trotzdem: `{"field":"location.city","op":"in","values":["__none__"]}` trifft die Leads
     ohne Ort. `total: 0` heißt dann, jeder Lead hat einen Ort, nicht, dass der Wert ungültig wäre.
   - **„Leads ohne E-Mail“ sind je nach Frage ein anderes Feld:**

     | Der Nutzer meint … | Bedingung |
     |---|---|
     | ohne E-Mail importiert (die Adresse des Leads selbst ist leer, auch wenn die Recherche später eine gefunden hat) | `lead.email` mit `is_empty` |
     | hat gerade keine Adresse, an die eine Mail gehen könnte (weder importiert noch gefunden) | `contact.sending_address` mit `is_empty` (mit `is_set`: hat eine) |
     | die Suche läuft noch bzw. steht noch aus (keine Adresse, Recherche nicht abgeschlossen) | `contact.email_state` `in` `["searching"]` |
     | nicht gefunden (keine Adresse, Recherche abgeschlossen; diese Leads bekommen nie eine Mail) | `contact.email_state` `in` `["not_found"]` |
     | nicht anschreibbar, mit Grund | `contact.send_block` `in` `["no_address"]` (keine Adresse), `["foreign_address"]` (die Adresse ist als fremd gesperrt, derselbe Grund wie `foreign_address` im Lauf), `["invalid_address"]` (das Postfach existiert laut Prüfung nicht); `["__none__"]` heißt: darf eine Mail bekommen |

     `contact.email_state` `present` ist dasselbe wie `contact.sending_address` `is_set`. Ob ein
     Feld am gewählten Ort vorkommt und welche Werte es dort hat, sagt `describe_lead_filters`.
4. **Zählen, bevor etwas geschieht:** `count_leads(place, campaign_id, filter, view_id)` gibt
   `total` und den angewandten Ausdruck zurück. Die Zahl dem Nutzer nennen, bevor ein Filter in ein
   Werkzeug geht, das schreibt, exportiert oder einen Lauf anbietet.
5. Den Ausdruck als `filter` an das Werkzeug geben, oder eine Ansicht als `view_id`; beides
   zusammen heißt, der Filter engt die Ansicht weiter ein. Trägt die Ansicht eine Suche und der
   Filter eine andere, lehnt der Server ab (`validation_failed`): `filter.search` weglassen oder
   ohne `view_id` aufrufen.

**Ansichten:** `list_lead_views` nennt je Ansicht `id`, `name`, `system`, `workQueue`, Filter und
Sortierung; dieselbe Liste steht unter `views` in `describe_lead_filters`. Systemansichten haben
einen Schlüssel als `id`: am Ort `global` `all`, `not_contacted`, `research_failed`,
`interest_shown`; am Ort `campaign` dazu `mail_queue` (wartet auf die Mail), `awaiting_approval`
und `qualified_unresearched`; am Ort `review` die Reiter `review_open`, `review_approved`,
`review_exported`, `review_rejected`. Welche davon die App als Arbeitsvorrat führt, sagt
`workQueue: true` (`research_failed`, `awaiting_approval`, `interest_shown`,
`qualified_unresearched`); `all`, `not_contacted` und `mail_queue` sind Ansichten, kein
Arbeitsvorrat. Die Liste nicht aus dem Gedächtnis nennen, sondern aus der Antwort. Gespeicherte
Ansichten haben eine Nummer als Zeichenkette (eine Zahl geht auch). `createdBy` nennt, wer sie gespeichert hat; es ist `null`, wenn
diese Person ihr Konto gelöscht hat, die Ansicht bleibt dann beim Workspace. Mit `with_counts=true`
trägt jede Ansicht `count`; eine Ansicht, die ein gelöschtes Feld oder eine gelöschte Liste nennt,
meldet stattdessen `count_error`, die übrigen zählen trotzdem. Am Ort `review` ist eine
Systemansicht ein Reiter wie in der App: Die Zahlen je Wert zählen dann innerhalb des Reiters.

**Speichern und Löschen (schreibt, `leads:write`):** Eine Ansicht nur speichern, wenn der Nutzer
das will, etwa weil er dieselbe Auswahl in der App oder in späteren Gesprächen wieder braucht; für
eine einmalige Frage reicht der Ausdruck. Vorher mit `count_leads` zählen und dem Nutzer Zahl, Name,
Ort und Sichtbarkeit nennen, dann auf sein Ja warten, wie vor jedem Schreiben; hat er Name und
Sichtbarkeit selbst so genannt und die Zahl stimmt mit seiner Erwartung überein, gilt sein Auftrag
als Ja. Trifft der Filter 0 Leads, das vor dem Speichern sagen und fragen, ob er die leere Ansicht
trotzdem will: Der Server legt sie ohne Hinweis an. Die Antwort trägt nur `id`, `name` und
`workspace`, keinen Filter und keine Zahl: nach dem Speichern mit
`list_lead_views(place, campaign_id, with_counts=true)` bestätigen, dass die Ansicht mit dem
erwarteten Filter und der erwarteten Zahl dasteht, und dem Nutzer die `id` nennen. Sichtbarkeit: `visibility` `personal` (Standard, nur der Nutzer) oder `workspace` (alle im
Workspace sehen sie; nur auf ausdrücklichen Wunsch). `sort_by` und `sort_direction` sind optional;
eine Kampagnen-Ansicht wird in jeder Kampagne angeboten. Mit `view_id` ersetzt `save_lead_view`
eine gespeicherte Ansicht statt eine neue anzulegen: vorher zeigen, was ersetzt wird. Ändern und
löschen darf nur, wer sie angelegt hat, oder ein Admin des Workspaces (`forbidden`).
`delete_lead_view(view_id)` nur nach Bestätigung; die Leads bleiben unberührt, die Ansicht ist weg,
auch für alle anderen, wenn sie für den Workspace galt.

**Schreiben mit Filter:** `add_leads_to_campaign`, `mark_leads_contacted` und
`bulk_set_lead_attributes` nehmen `filter`/`view_id` statt `lead_ids` (nie beides). Der Server
schneidet dabei nie ab: Mehr als 1000 Treffer lehnt er mit `limit_reached` ab, einen Filter ohne
Bedingung mit `validation_failed`, null Treffer mit `no_leads_matched`. Bei mehr als 1000 den
Filter enger fassen (etwa nach `list.id` oder `lead.created_at`) und in mehreren Aufrufen arbeiten.

**Wann der alte Weg bleibt:** Eine ganze Liste in eine Kampagne schieben geht weiter mit `list_id`.
Ein Lead nach Name, Adresse oder Domain finden: `search_leads` mit `query`. Dubletten vor einem
Import prüfen: `check_leads_exist`. Der Abgleichsindex vor einem Scrape: `export_leads(format="index")`.

**Fehler:** `validation_failed: <Grund> at filter.<Pfad>` (bei einer Ansicht `at view_id.<Pfad>`)
nennt die Stelle im Ausdruck: mit `describe_lead_filters` korrigieren. `not_found`: unbekannte,
gelöschte oder fremde Ansicht, oder eine Systemansicht, wo eine gespeicherte verlangt ist.
`campaign_not_found`: unbekannte oder fremde Kampagne. `forbidden`: die Ansicht gehört jemand
anderem.

**Ältere Server:** Fehlt `describe_lead_filters` in der Tool-Liste (`ping` unter 4.32.0), gibt es
weder Filter-Ausdruck noch Ansichten, und die Werkzeuge kennen `filter` und `view_id` nicht: nie
mitschicken, ein älterer Server würde sie ohne Fehler übergehen und ohne Filter arbeiten. Dort
gelten die Wege aus der Tabelle oben: `search_leads` mit seinen eigenen Filtern, für Kampagnen
`list_leads` im Listen-Modus, zählen über `total` der Antwort.

## Löschregeln (dem Nutzer VOR dem Löschen erklären)

- Ohne `delete_leads`: nur die Klammer verschwindet, jeder Lead bleibt.
- Mit `delete_leads=true` (verlangt `confirm_delete=true`): gelöscht werden NUR Leads, die nie
  kontaktiert wurden, in keiner Kampagne und in keiner anderen Liste sind — alles andere wird
  entkoppelt. Der Report nennt beide Zahlen. Das ist das Undo für Test-Importe und gibt die Plätze
  im Lead-Limit des Accounts sofort frei (`get_credit_balance.account.free_slots`); schon gebuchte
  Credits für gelöschte Leads werden nicht erstattet.
- Löschen ist endgültig — immer erst `get_list` zeigen, dann die ausdrückliche Bestätigung des
  Nutzers einholen, dann löschen.
- Fehler `lead_mutation_busy` (bei `delete_list` ab MCP 4.16.0, bei `add_leads_to_campaign` schon
  früher): Eine andere Änderung an den Leads läuft gerade (z. B. ein Import). Es wurde nichts gelöscht
  bzw. verlinkt; einmal kurz warten und denselben Aufruf wiederholen.

## Typische Abläufe

**„Zeig mir meine Listen"** → `list_lists` → kompakte Tabelle (Name, total/in Kampagnen/kontaktiert,
Herkunft, Datum).

**„Sind die schon im Bestand?" (vor einem Import)** → E-Mails sammeln, für Zeilen ohne E-Mail die
Domains → `check_leads_exist` → Zusammenfassung: X neu, Y bekannt (E-Mail-Treffer und
für Zeilen ohne E-Mail die Domain-Treffer mit `match_kind: website_identity`, der Import verlinkt sie nur), Z do_not_contact (namentlich: die werden NIE
importiert oder angeschrieben), W „Firma bekannt“ (Warnung).

**„Gib mir den Abgleichsindex"** → `export_leads(format="index")` → als Datei speichern —
damit gleicht der Nutzer die extern gescrapten Ergebnisse lokal ab, bevor Anreicherung oder Verifizierung Geld kostet.

**„Wie viele Leads aus Wien sind noch in keiner Kampagne?“** (ab MCP 4.32.0, Bestand) →
`describe_lead_filters(place="global")` → Ausdruck bauen (Stadt als `key`, also `"wien"`) →
`count_leads(place="global", filter=…)` → die Zahl nennen. Erst wenn
der Nutzer die Leads sehen oder nutzen will, `search_leads(filter=…)`, `export_leads(filter=…)` oder
`add_leads_to_campaign(campaign_id, filter=…)` mit demselben Ausdruck.

**„Welche Städte habe ich im Bestand?“** (ab MCP 4.32.0) →
`count_leads(place="global", facets=["location.city"])` → die Werte (`label`) mit Zahlen als kurze
Liste. Kommen 50 Werte, sind es nur die 50 häufigsten: das sagen und für einen bestimmten Ort mit
`value_search` nachfassen.

**„Wie viele Leads der Kampagne 80 sind aus Wien und warten auf die Freigabe?“** (ab MCP 4.32.0,
Kampagne) → `describe_lead_filters(place="campaign", campaign_id=80)` →
`count_leads(place="campaign", campaign_id=80, view_id="awaiting_approval", filter={"v":1,"where":[{"field":"location.city","op":"in","values":["wien"]}]})`
→ die Zahl nennen. Ohne `place="campaign"` zählte der Aufruf den ganzen Bestand.

**„Aus welcher Stadt hat Kampagne 80 die meisten Leads?“** →
`count_leads(place="campaign", campaign_id=80, facets=["location.city"])` → der erste Wert; bei
Gleichstand beide nennen. Gezählt sind alle Leads der Kampagne, nicht nur die mit offener Arbeit.

**„Schieb Liste X in Kampagne Y"** → erst `get_list` (Zahlen + kontaktiert-Anteil zeigen) →
Bestätigung → `add_leads_to_campaign(campaign_id, list_id)` → Report (added / already / dnc-skipped).
Bei > 1000 Leads in der Liste: IDs paginiert holen (`get_list` mit limit max. 200 oder `export_leads(format="json", list_id=…, limit=1000, offset hochzählen)`), je 1000 als
`lead_ids`-Chunk verlinken, Reports aufsummieren — `list_id` direkt würde `limit_reached` werfen.
Danach startet `start_lead_run` die Verarbeitung (vorher `list_lead_runs(active_only=true)` prüfen).

## Grenzen (ehrlich benennen)

Kein Bulk-Löschen einzelner Leads außerhalb von Listen, kein Listen-Merge. Eine Liste ist eine
feste Klammer; eine Auswahl nach Regeln, die sich mit dem Bestand ändert, ist ab MCP 4.32.0 eine
gespeicherte Ansicht (`save_lead_view`), auf älteren Servern gibt es sie nicht. Wer eine feste
Liste aus einer Auswahl braucht: neu zusammenstellen (`search_leads` + `import_leads` mit `list_id`
verlinkt Bestands-Leads ohne Duplikate).
