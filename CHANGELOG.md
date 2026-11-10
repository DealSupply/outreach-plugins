# Changelog

## 2026-11-10 – outreach 0.7.0 (benötigt ListM8 MCP 4.14.0 für „Angebot je Lead“)

Neue Kampagnen starten wie in der App einfach: ein Angebot für alle Leads mit dem festen zweiten Satz der Karte, ohne A/B-Test. Tests und „Angebot je Lead“ gibt es für Erfahrene auf Wunsch (DS-195, Weg A). „Angebot je Lead“ braucht ListM8 MCP 4.14.0 (`ping`); ältere Server bekommen immer ein Angebot für alle, alles andere läuft dort wie bisher.

**outreach**
- `outreach-copy` (SKILL, `references/copy-lehre.md`, `kern/copy-lehre.md`, beide `marketing-offer.md`, `beispiel-blueprint.md`, `kern/beispiele.md`) → Der zweite Satz zum Angebot ist bei Karte A, B und C der feste Satz der App (C „Ich bin gerade noch an den letzten Feinheiten dran.“, A „Darin wäre alles genau auf euch zugeschnitten.“, B „Im Pilot bekommt ihr das kostenlos, dafür bräuchten wir nur ehrliches Feedback.“, je in der Sie-Form und auf Englisch), D und E ohne. `angebot_ausfuehrung` entsteht nicht mehr von selbst. Angebotssatz, zweiter Satz und Schlussfrage stehen immer in drei eigenen Absätzen. Bestehende Kampagnen mit `angebot_ausfuehrung` behalten ihre Variable.
- Neu `outreach-copy/references/fuer-erfahrene.md` → die eine Frage „Für Erfahrene“ beim Anlegen; Tests in Mail 1 wie in der App (Betreff-Test als B mit „Frage zu {{Firma}}“, Intro-Test als nächste Variante, beide A, B und C), Empfehlung „ohne Tests“; „Angebot je Lead“ für Karte A und C mit denselben Feldern wie die Karten der App (Haupt-Angebot plus höchstens drei weitere, je Sache, Wort, Detail und Bedingung aus den sieben Website-Merkmalen), Vorschlägen, der abgenommenen Vorlage (Deutsch Du, Deutsch Sie, Englisch), Blueprint (Station-Antworten `offerPerLead`, `offerCards`, drei Platzhalter in Mail 1, Mail 3 neutral) und Beispiel.
- `outreach-campaign` → fragt einmal „Für Erfahrene“, baut ohne Wahl den Standard, zeigt bei „Angebot je Lead“ Angebote und Anweisung vor dem Anlegen und prüft danach den Station-Block. Keine `offerFocuses`, keine `offerRole`, kein `offerPrompt`. Beim Bearbeiten bleiben Varianten, Schwerpunkte, Station und Variablen, wie sie sind; „Angebot je Lead“ für bestehende Kampagnen in der App.
- `outreach-launch` → der A/B-Test ist ein Punkt der Launch-Checkliste nur bei gewählten Tests.
- `outreach-verify`, `verify-agent` → ein fester zweiter Satz und fehlende Varianten ohne gewählte Tests sind kein Befund; bei „Angebot je Lead“ sind `offer_text` und `offer_cta` Serverwerte, `angebot_ausfuehrung` wird nach den Regeln der Anweisung geprüft, die Wahl des Angebots gegen den `WEBSITE-BEFUND`.
- `outreach-generate`, `lead-agent` → bei „Angebot je Lead“ die Nummer unter `angebot` melden, nur Absatz 2 schreiben, `offer_text` und `offer_cta` leer schicken.
- `kern/check_copy.py` → Step 3 darf mit „Angebot je Lead“ mit dem neutralen Schluss enden.
- `outreach-setup`, README → abgestimmt auf MCP 4.14.0.
- Enthält die Copy-Korrekturen aus DS-180 (Betreff B „Frage zu {{Firma}}“, Auffang-Schwerpunkt, eine Längenregel), die bisher ohne eigene Version waren.

## 2026-11-07 – outreach 0.6.0, datenbeschaffung 0.5.0, fulfillment 0.1.4

Sammelstand auf ListM8 MCP 4.12.0 (Stand develop, nächster Release nach v4.18.4). Er bringt alles, was der Server seit 4.0.0 kann und die Skills bisher nur auf Zweigen kannten, dazu die Copy-Nacharbeit von 0.4.8 bis 0.5.9 (Einträge darunter). Neues nutzen die Skills nur, wenn `ping` die passende Version meldet; ältere Server ab 3.0.0 laufen weiter wie bisher.

**outreach** (neu in diesem Stand, MCP 4.9.0 bis 4.12.0)
- `outreach-campaign` → Blueprint mit A/B-Varianten (`sequence.steps[].variants`, `variantAActive`, `aiVariables[].angle`/`title`/`description`/`role`), Schwerpunkten (`campaign.offerFocuses`, bis 20, Prüffragen mit `fitsWhen`), Angebotsblöcken (`aiVariables[].offerRole`), zwei Personen je Firma (`campaign.recipientsPerCompany`) und Station (`campaign.station`, nur aus dem Export übernehmen). Beim Bearbeiten Varianten mitschicken; `confirm_discard_variants` nur nach Ja mit `discard_variants=true`, `variants_transferred` ist nicht übersteuerbar (MCP 4.11.0).
- `outreach-campaign`, `outreach-pipeline`, `outreach` → Eine in der App eingerichtete Kampagne gibt `release_campaign` frei, nur nach ausdrücklichem Ja; `release_blocked` nennt die Lücken. `start_lead_run` lehnt bis dahin mit `setup_open` ab, im Karten-Test sperrt `model_trial_locked` teure Modelle und Deep (MCP 4.9.0).
- `outreach-generate`, `lead-agent` → Angebotsblöcke: `schwerpunkt` mit Grund, je Block `<name>__stand` `uebernommen` (Vorlage vom Server) oder `angepasst` mit Grund, `proof` und `noun` nie schreiben; `no_offer_focus` überspringt den Lead (`grund=kein-schwerpunkt`), `set_offer_focus` nur auf Wunsch des Nutzers. Person 2 über `second_person` im selben Aufruf, mit eigenem Intro und derselben Anredeform; `second_person_not_open`. Antwortfelder `offer_blocks`, `second_person`, `server_adjusted` (MCP 4.11.0, 4.12.0).
- `outreach-verify`, `verify-agent` → `get_lead_variables` mit `markWritten`, `offerRole`/`templateState` (eine Vorlage ist ein Serverwert und kein Befund zum Wortlaut), `offerFocus` und `secondPerson`; Person 2 wird mitgeprüft, eine Freigabe gilt für beide.
- `outreach-export` → Spalten für Person 2 und `rows_per_person`. `outreach-lists` → `check_leads_exist` trifft Person 2 (`matched_via: second_person`).
- `outreach-setup`, README → Versionsliste von 4.0.0 bis 4.12.0, 46 Tools.
- Power-ups gelten ab MCP 4.6.0 (die Zweige nannten 4.1.0 bzw. 4.4.0, so hat der Server sie nie ausgeliefert).
- Live-Ansicht → die Tests zu Leads ohne E-Mail laufen über die Verbindung `dealsupply` (44 Tests grün).

### Bisher nur auf Zweigen: Intro-Varianten mit Tags und Verbindung `dealsupply` (MCP 4.10.0, PR #19)

Passt zu ListM8 MCP 4.10.0 (Sammelstand des Redesigns, DS-103). Die Verbindung zieht von `outreach.akquise.de` nach `app.dealsupply.ai`.

*outreach* (Verbindung `dealsupply`)
- `.mcp.json`, `mcp.json` → Die mitgelieferte MCP-Verbindung heißt `dealsupply` und zeigt auf `https://app.dealsupply.ai/_mcp/v1`; die Verbindung `akquise` (`outreach.akquise.de`) entfällt. Nach dem Update `dealsupply` einmal anmelden (Claude Code `/mcp`, Claude App unter Connectors, Codex `codex mcp login dealsupply`); eine von Hand angelegte Verbindung `akquise` entfernen.
- `outreach-setup`, README → Einrichtung mit `dealsupply`, Hinweis zum Umstieg von `akquise`, Kunden anderer Outreach-Apps lassen `dealsupply` unverbunden.
- Live-Ansicht → Standard-Server `dealsupply`, Links in die App auf `app.dealsupply.ai`; Server mit anderem Namen (auch ein altes `akquise`) erkennt sie weiter an ihren Tools. Tests umgestellt.

*outreach* (Intro-Varianten mit Tags, MCP 4.10.0)
- `outreach-generate`, `lead-agent` → Intro-Variablen aus `emailGeneration.introVariables` in Rangfolge; Variante A ist das erste Element (meist `intro`, maßgeblich ist die Position, nicht der Name), dann `intro_b` …, jede mit eigenem Anker nach dem Block INTRO-VARIANTEN UND TAGS im `systemPrompt`. `expectedOutput` wörtlich übernehmen, also je Intro-Variable `<name>__anker` und `<name>__schluss` mitschicken. Eine weitere Variante ohne guten eigenen Anker ist ein Rückfall (`"<name>__anker": "rueckfall"`, leerer Wert); der Server speichert sie ohne eigenen Text, gesendet wird der aktuelle Text von Variante A. Eine wörtliche Kopie von A zählt ebenfalls als Rückfall. Zwei selbst geschriebene Varianten enden nie gleich, sonst `validation_failed`. `save_lead_variables`-Referenz mit `tags_written` und `fallbacks`.
- `lead-agent` (Nachbessern) → unveränderte Variablen mit ihren Tags aus `anchorWritten`/`closingWritten` zurückschreiben; Zeilen mit `fallback: true` wieder leer als Rückfall schicken.
- `outreach-verify`, `verify-agent` → `get_lead_variables` mit `anchorWritten`, `closingWritten`, `fallback` und `notStored`: Eine Rückfall-Zeile zeigt den aktuellen Text von Variante A, ist kein fehlender Wert und kein Ablehnungsgrund.
- Ältere Server ohne Tags in `expectedOutput`: Tags werden nicht mitgeschickt, alles bleibt wie bisher.

### Bisher nur auf Zweigen: Close (MCP 4.8.0, PR #18)

Passt zu ListM8 MCP 4.8.0 (Close-Spiegel). Ältere Server kennen `get_close_status` und `set_close_sync` nicht.

*outreach* (Close)
- `outreach` → neuer Abschnitt „Close erklären“: Fragen zum Stand in Close beantwortet `get_close_status` (Verbindung, Leads je Status im Workspace, zuletzt fehlgeschlagene, optional der Schalter einer Kampagne); `set_close_sync` schaltet eine Kampagne an oder aus (`enabled`, optional `transfer_backlog=false`), nur auf Wunsch des Nutzers. Verbinden, Einrichten, Einstiegsstufe und Lead-Status je Stufe gibt es nur in der App, für alle Kampagnen. Leads mit `do_not_contact` kommen nie neu nach Close.
- `outreach-launch` → Zeile „ins CRM Close spiegeln“ in „Wer macht was“.
- `outreach-setup` → Close-Werkzeuge ab MCP 4.8.0.

### Bisher nur auf Zweigen: Power-ups (MCP 4.6.0, aus PR #16 ohne „Leads finden“)

*outreach* (Power-ups, ListM8-MCP 4.6.0, LISTM8-75). Alles Neue gilt erst ab Server-Version 4.6.0 (`ping`); ältere Server kennen die Tools nicht.
- `lead-agent`, `outreach-research` → Eingeschaltete Power-ups aus `get_lead_data.researchGeneration.powerUps` über `run_power_up`: `verify_email` prüft nach dem Lesen der Seiten alle belegten Kandidaten in einem Aufruf (Anbietergebühr ohne Marge, nur Adressen mit Herkunft), `find_person_email` sucht erst nach Impressum, Team- und Kontaktseite und nur für einen Entscheider, dessen persönliche Adresse auf keiner gelesenen Seite steht (Treffer zum Stückpreis, ohne Treffer die Anbietergebühr; höchstens drei Personen). Ein Treffer von `find_person_email` mit Urteil `valid` ist belegt und wird `bestEmail`, auch statt einer allgemeinen Importadresse. Eine nur auf einer Seite gelesene Adresse kennt der Server erst nach dem Speichern: erst `bestEmail` schreiben, dann prüfen. `invalid` und `catch_all_unconfirmed` werden nie `bestEmail`; bei `failed`, `unavailable`, `limit_reached` kein zweiter Aufruf mit derselben Eingabe. Im Server-Lauf prüft der Server am Ende jeder Recherche eine noch ungeprüfte Versandadresse selbst (kostenlos) und wählt bei unzustellbarem Postfach neu.
- `outreach-generate`, `outreach-verify`, `verify-agent` → `undeliverable_address` beim Speichern oder Freigeben: Das Postfach der Versandadresse existiert laut Prüfung nicht. Nicht wiederholen; eine andere Adresse desselben Betriebs mit `switch_primary_email` wählen (nur auf Wunsch des Nutzers) oder den Lead überspringen. Eine Versandadresse mit Urteil `invalid` in `emailVerdicts` ist ein Befund (`art=adresse`, ohne gültige Alternative `art=recht`).
- `outreach-abo-lauf`, `outreach-pipeline` → `list_power_ups` vor dem Lauf, Einschalten mit `set_power_up` nur mit Zustimmung; der Power-up-Block von `quote_lead_run` gehört in die Preisnennung, Treffer und Credits aus `get_lead_run_status.powerUps` in den Bericht. Neuer Grund `invalid_address` in `skipReasons` und `quote_lead_run.without_work`.
- `outreach-campaign` → Power-ups stehen nicht im Blueprint, sie werden nach dem Anlegen mit `set_power_up` geschaltet.

### Bisher nur auf Zweigen: Leads ohne E-Mail (MCP 4.0.0, PR #10)

Leads ohne E-Mail-Adresse (ListM8 MCP 4.0.0). Ein Lead braucht beim Import eine gültige E-Mail oder eine eigene Website; die Recherche sucht die Kontaktadresse dann selbst. Alles Neue gilt erst ab Server-Version 4.0.0 (`ping`); ältere Server behalten den alten Ablauf, jeder Lead braucht dort eine E-Mail.

*outreach*
- `outreach-import` → Prüft zuerst die Server-Version; nur sie entscheidet über den Kontrakt, nicht der Wortlaut einer Fehlermeldung. Ab 4.0.0 reicht E-Mail ODER eigene Website (Baukasten-Unterseiten wie `name.jimdosite.com` zählen, reine Profil- oder Plattform-Links nicht). Ungültige E-Mail mit brauchbarer Website wird ohne Adresse importiert. Teilimport statt Komplett-Ablehnung: `accepted`, `rejected_total`, `rejected_rows` mit Codes (`missing_contact`, `invalid_email`, `platform_only_website` usw.); `validation_failed` nur, wenn nichts importierbar ist; `limit_reached` ist dort ein Fehler für den ganzen Aufruf und nur im Job-Ergebnis ein Zeilencode. Bericht nennt Abgelehnte, Hinweise und Duplikate nach `matchedVia` (E-Mail oder Domain).
- `outreach-research`, `lead-agent` → Ein Lead ohne Adresse bekommt als erstes Ziel die eigene Kontaktadresse (Regeln aus `researchGeneration.contactEmail`): persönliche Adresse von Inhaber oder Geschäftsführung vor info@, nie geraten, nie Plattform-, Verzeichnis-, Agentur- oder Kammeradressen. Fund als `bestEmail` schreiben (der Server macht sie zur Identität; `address_conflict` nicht wiederholen). Kein Fund: Recherche mit Abschnitt „## Kontakt“ und den geprüften Seiten speichern, der Lead scheidet mit `no_contact_email` aus und bekommt keine Mail-Variablen. Antwortzeile mit `adresse=` bzw. `grund=keine-adresse`. Ein Lead mit `not_found` bekommt im Abo-Lauf trotzdem sein Qualifizierungsurteil, sonst bliebe er in der Warteschlange.
- `outreach-generate`, `outreach-verify`, `verify-agent` → `no_contact_email` beim Speichern oder Freigeben ist kein Fehler, nicht wiederholen. Versandadresse ist `sendingEmail`, sonst `email`; ein Lead ohne beide wird nie freigegeben.
- `outreach-pipeline`, `outreach-abo-lauf` → Bericht zählt „ohne Adresse“ aus den `skipReasons` des Laufs bzw. den Antwortzeilen der Agents.
- `outreach-lists`, `outreach-launch` → Leads ohne E-Mail: im Dedup-Index ist `e` leer (nur über `d` bekannt), `check_leads_exist` findet sie nur über die Domain (Abgleich nach ganzen Labels; `match_kind: website_identity` = derselbe Lead, `company_known` = Firma bekannt; ohne `match_kind` eigener Host-Vergleich), `mark_leads_contacted` erreicht sie nur über `lead_ids`; Export und Push nehmen nie Leads ohne Versandadresse mit.
- `outreach-setup` → nennt die Server-Version und was ab 4.0.0 gilt. `outreach-campaign` (Recherche-Referenz) → Hinweis, dass die Regeln zur Kontaktadresse vom Server kommen.
- Live-Ansicht → Import zeigt abgelehnte Zeilen („470 importiert · 3 abgelehnt“); ein Lead, dessen Recherche keine Adresse fand, verlässt im Abo-Lauf die Mail-Phase; Leads ohne E-Mail erscheinen mit ihrer Website bzw. Versandadresse; ein kombinierter Schreibaufruf (Urteil plus Recherche) zählt beide Phasen. 4 neue Tests.

*datenbeschaffung*
- `build_csv.py` → `--uebergabe kontakt` (E-Mail oder eigene Website, Standard für ListM8 ab 4.0.0) und `--uebergabe email` (alter Vertrag, `--require-email` bleibt als Alias); verworfene Zeilen mit Grund per `--verworfen` in eine eigene CSV; Hinweis `nur-plattform-url`; CSV als Eingabe, ein zweiter Durchlauf behält Inhaber, Zusatzspalten und frühere Hinweise. Neue Referenz `plattform-hosts.md` (Spiegel der Server-Liste: Profil-Plattformen, Marken mit Länderdomains, Baukästen).
- `dedup.py` → Index-Zeilen ohne Adresse zählen über ihre Domain; Zeilen ohne E-Mail auf bekanntem Host fallen als derselbe Lead weg; Domains nach ganzen Labels wie `check_leads_exist` (ohne `www.`, Umlaut-Domains als Punycode, keine Teilstring-Treffer; derselbe Lead nur bei exakt gleichem Host, Eltern-Domain nur Warnung); `--drop-known-domains-ohne-email`. 9 neue Tests.
- `datenbeschaffung`, `listen-qualitaet`, alle Wege, `impressum-enrichment`, `kontaktseiten-fallback`, `enrichment-waterfall`, `outscraper-bulk` → Die Kontaktlücke: vorab anreichern oder der ListM8-Recherche überlassen (Kosten- und Entscheidungstabelle in `datenumfang.md`); Anreicherung ist ab 4.0.0 optional. Bei ungültiger Adresse aus der Verifizierung bleibt die Zeile mit Website erhalten (Adresse raus, Hinweis `adresse-verworfen`).
- `listm8-mcp.md`, `csv-spalten.md`, `outreach-uebergabe.md`, `listen-und-icp.md`, `erfahrungswerte.md` → neuer Import-Vertrag, Antwortfelder, Dedup über die Website, Platzhalter für die Fundquote der Recherche.

### Bisher nur auf Zweigen: Mails im Review neu schreiben, Sperre je Lead (MCP 2.5.0, PR #9)

*outreach* (ListM8-MCP 2.5.0: E-Mails neu generieren, Sperre je Lead)
- `outreach-pipeline` → `start_lead_run` kennt `regenerate_emails` für Mails im Review (nur mit Stufe `email`, kostet erneut, nur mit Zustimmung); mit `select_by_filter` gilt dann `campaign_status=pending_review`. Während eines Laufs sperren die Variablen-Werkzeuge nur noch den einzelnen Lead.
- `outreach-verify`, `outreach-generate`, Lead-Agent → kennen den Code `email_generation_active` (Mail dieses Leads wird gerade generiert) und überspringen nur diesen Lead; Neugenerierung im Review über `regenerate_emails=true`.

## 2026-11-06 – outreach 0.5.9

Befunde aus dem Nachtest des Endstands (DS-172).

**outreach**
- `outreach-generate` → Den Anker `geschichte` ehrlich melden: ListM8 setzt dahinter die feste Reaktion „das hab ich richtig gern gelesen“ selbst ein, wenn das Intro mit einer anderen bekannten Reaktion endet (nicht bei Kampagnen, deren Intro-Prompt den Schluss selbst regelt), und nennt den Tausch in `server_adjusted`. Ein Intro von Person 2 ist mit keinem Intro von Person 1 wortgleich, gleich welche Variante.
- `verify-agent` → Die getauschte Geschichts-Reaktion und die vom Server gesetzte Sie-Begrüßung sind kein Befund.
- `outreach-copy`, `outreach-generate`, `verify-agent` → Der Betreff von B wird über `emailGeneration.subjectVariables` (Rolle `subject_variant`) erkannt, nicht über den Namen `betreff_b`; der Rückfall-Schlüssel ist `<name>__rueckfall`. Der Rückfall auf den Betreff von A ist in ListM8 keine gespeicherte Kopie: Er bleibt ohne Text und wird beim Versand eingesetzt, auch für Person 2; `get_lead_variables` zeigt ihn mit `fallback: true` (Stand develop, Xeno bccd25e0c).
- `outreach-copy`, `outreach-generate`, `outreach-verify` → Sie-Form: nie „Guten Tag Herr/Frau Nachname,“; mit belegter Anrede „Hallo Herr/Frau Nachname,“ ohne Titel und Vornamen, ohne belegte Anrede „Guten Tag Vorname Nachname,“ (G18). Beide Personen einer Firma grüßen in derselben Form.

## 2026-11-06 – outreach 0.5.8

Entscheidungen vom 06.11.2026 aus dem Credits-Test (DS-170): Betreff B beginnt mit dem Detail, Reaktion nach einem Geschichts-Anker.

**outreach**
- `outreach-copy`, `outreach-generate`, `verify-agent` → Ein echter Betreff B beginnt direkt mit dem Detail („Dachsanierung am Hansmeyerhof“, „Traufblechmontage bei Nitz“), nie mit „Frage zu/zum/zur …“ oder „question about …“; diese Form hat allein der Rückfall „Frage zu <Kurzname>“. ListM8 zählt einen Betreff in dieser Form immer als Rückfall (E53). Beispiele „Frage zu den Samstagskursen“ und „kurze Frage zum Neubau Freising“ ersetzt.
- `check_copy.py` → Hinweis, wenn Betreff B wie der Rückfall beginnt.
- `outreach-copy`, `lead-agent`, `verify-agent` → Hinter Firmengeschichte, Gründung oder Alter heißt die Reaktion immer „das hab ich richtig gern gelesen“ („That was really nice to read.“), nicht „das fand ich richtig sympathisch“ (E54).
- Nach dem Review: Die Form „Frage zu …“ zählt in ListM8 nur in Kampagnen mit dem neuen Betreff-Prompt (Regel ANFANG/START) als Rückfall, ältere Kampagnen behalten ihren Prompt; ein nackter Standard-Betreff zählt immer als Rückfall. `check_copy.py` erkennt dieselben Formen wie ListM8 („Fragen zu“, „eine/kleine/kurze Frage zu“, „Frage wegen/an“, „questions about“, „a quick question about“, nie „Fragebogen“, „Rückfrage“, „questionnaire“).
- `outreach-generate`, `verify-agent` → Die feste Geschichts-Reaktion darf in zwei Intro-Varianten gleich stehen; derselbe Satz in vielen Mails ist dort kein systematischer Befund. Rückfall von Betreff B ohne Kurznamen ist der Betreff von Variante A.
- `outreach-copy`, `lead-agent`, `verify-agent` → „hängen geblieben“ (seit 31.10.2026 verboten) aus allen Reaktionslisten und Beispielen entfernt, steht in den Verbotslisten; `verify-agent` wertet es als Verstoß.

## 2026-11-06 – outreach 0.5.7

Entscheidungen vom 06.11.2026 (DS-167): Wort für die Sache für jede Kampagne, Träger der Förderung.

**outreach**
- `outreach-copy` → Wort für die Sache auch ohne Schwerpunkte: Jede Kampagne hat in ListM8 ein eigenes Wort (Angebots-Seite, vom Assistenten vorgeschlagen). Es steht nur in der Schlussfrage von Mail 3, Mail 1 behält „es“ bzw. „das“; ohne Wort nimmt Mail 3 die Frage aus Mail 1 wörtlich.
- `outreach-copy` → Karte D: Nennt der Nutzer Träger oder Programm der Förderung, steht er statt „der Staat“ („Wusstest du, dass das Land Baden-Württemberg aktuell bis zu …“).
- `outreach-copy` → Das Wort für die Sache der Kampagne gilt in Mail 3, solange dort nicht das Wort des Schwerpunkts steht (`{{ai.offer_noun}}`), auch bei aktiven Schwerpunkten; ListM8 speichert es ohne Satzzeichen und Anführungszeichen, mit kleinem Artikel. Der Träger der Förderung steht mit Artikel („das Land Baden-Württemberg“).
- Person 2 bekommt in ListM8 ein eigenes Intro mit Detail zur Firma, kein Kollegen-Intro mehr; die Regeln kommen aus `get_lead_data` (ZWEITE PERSON), der Anker `kollege` wird abgelehnt.

## 2026-11-06 – outreach 0.5.6

Nacharbeit aus dem Gesamttest, Lauf 5 (DS-166): Schwerpunkte in den Folgemails, Schlussfrage von Mail 3, Betreff B.

**outreach**
- `outreach-copy` → Mail 2 bis 4 nennen mit Schwerpunkten nie einen Schwerpunkt beim Namen; ListM8 streicht einen Satz mit Schwerpunkt-Label. Mail 3 endet immer mit der Frage aus Mail 1, eine eigene Schlussfrage weicht ihr.
- `outreach-copy` → Zweiter Satz und Routing folgen dem gewählten Schwerpunkt, nie dem Haupt-Offer, wenn ein anderer gewählt ist; Pilot-Satz am besten 15 bis 20 Wörter; Prüffragen am besten nach einer Sache mit fester Recherche-Zeile.
- `outreach-copy`, `verify-agent`, `check_copy.py` → Betreff B unter 3 Wörtern ist ein Verstoß, ListM8 setzt den Rückfall.

## 2026-11-06 – outreach 0.5.5

Nacharbeit aus Testlauf 4 (DS-165): Betreff B, Kleinschreibung nach der Anrede, Beleg wörtlich.

**outreach**
- `outreach-copy` → Betreff B: auch kein wertendes Wort zum Detail („Pragmatische Lösungen von Artd“), nur der Gegenstand des Intros ohne Zusatz; Rückfall „Frage zu {{Firma}}“ mit dem Kurznamen aus `firma`, „kurze Frage“ nur ohne sicheren Kurznamen. `save_lead_variables` ersetzt einen gebrochenen oder nackten Standard-Betreff entsprechend.
- `outreach-copy` → Mail 2 bis 4: nach „Hallo …,“ klein weiter, auch in der Sie-Form („da ich bisher nichts gehört habe“); ListM8 setzt das erste Funktionswort selbst klein.
- `outreach-copy` → Mail 3: Beleg wörtlich wie angegeben, kein „bis zu“, das nicht in der Angabe steht (Förderquoten der Karte D bleiben „bis zu“).
- `verify-agent` → Die Marke `gleicher_gegenstand` gilt vorerst nicht als Befund (wie in der Review von ListM8 ausgeblendet, bis die Regel geschärft ist).

## 2026-11-06 – outreach 0.5.4, fulfillment 0.1.4

Stand der Copy-Nacharbeit (Paket 2 und 3) auf Paket 1: zweiter Angebotssatz je Lead für A, B und C, Betreff-Test in Variante B, weitere Intros mit freiem Anker, Schwerpunkt je Lead.

**outreach**
- `outreach-copy` → Karte B: Rahmensatz je Lead, der den Pilot an diesem Lead festmacht (was er konkret bekäme, bezogen auf seine Recherche, und was er dafür gibt), höchstens 25 Wörter; das Detail des gewählten Schwerpunkts ist Grundlage des zweiten Satzes.
- `outreach-copy` → Karte C: Der Feinheiten-Satz kommt je Lead von der KI über `{{ai.angebot_ausfuehrung}}` wie bei A und B; er beginnt wörtlich mit „Ich bin gerade noch an den letzten Feinheiten dran, vor allem“. Ältere Kampagnen behalten den festen Satz im Body.
- `outreach-copy` → Betreff-Test: Variante B von Mail 1 ist Variante A mit dem persönlichen Betreff `{{ai.betreff_b}}` je Lead (Regeln, Rückfall „Frage zu {{Firma}}“ bzw. „kurze Frage“); der Intro-Test läuft als Variante C. `check_copy.py` zeigt „Betreff B: …“ und zählt den Kurznamen der Firma als ein Wort (`--firma` oder Zeile „Kurzname: …“); ein Betreff, der eine harte Regel bricht, wird zum Betreff von Variante A.
- `outreach-copy` → Schwerpunkte: je Lead der, der nach Prüfung und Recherche am besten passt, Rang 1 nur ohne klar besseren; Prüffragen nur nach Sichtbarem auf der Website.
- `outreach-generate`, `verify-agent` → weitere Intro-Varianten nehmen den nächsten freien Eintrag aus „Stärkste Anker“; Marken `rueckfall_trotz_anker` und `gleicher_gegenstand` als weiche Befunde.
- `outreach-campaign`, `outreach-verify`, `beispiel-blueprint.md` → zweiter Satz bei A, B und C, Schlussfragen und Wortzahlen nach dem zusammengeführten Stand.

**fulfillment**
- `fulfillment`, `lead-kontext.md` → Das On-Top-Detail der Karte C steht seit 05.11.2026 je Lead in `angebot_ausfuehrung` (`get_lead_variables`), bei älteren Kampagnen fest im Body.

## 2026-11-05 – outreach 0.5.3

Stand der Copy-Nacharbeit (Paket 1): Mail 3 und die Schlussfragen je Karte folgen der App.

**outreach**
- `outreach-copy` → Mail 3 endet mit genau einer Frage, der Schlussfrage aus Mail 1 (mit dem Wort für die Sache, wo die Karte eins hat); die Beispiele für Step 3 enden nicht mehr mit „melde dich gerne“.
- `outreach-copy` → Schlussfragen je Karte wie in der App, mit Sie-Form: A „Wäre es in Ordnung, wenn ich das auch für dich erstelle? …“, B „Wärst du grundsätzlich offen dafür?“, C unverändert, D „Wäre es in Ordnung, wenn ich dir kurz aufschreibe, welches Programm für dich infrage kommt? …“, E „Wäre das grundsätzlich interessant?“.
- `outreach-copy` → Betreff von Step 1 bei jeder Karte „kurze Frage“; die Karten-Betreffs („Meeting …“, „Anfrage für …“, „Deine Förderung“, „Partnerschaft …?“) entfallen. Nur Step 1 trägt einen Betreff.
- `references/copy-lehre.md` → Aufbau von Step 3 wie in der App: Beleg als erster Absatz, höchstens ein kurzer eigener Satz, Schlussfrage aus Mail 1 als letzter Absatz.
- `beispiel-blueprint.md` → Step 3 mit einem Beleg direkt nach der Anrede und der Schlussfrage aus Mail 1; Varianten A und B mit ihren Schlussfragen.

## 2026-11-05 – outreach 0.5.2, fulfillment 0.1.3

Führt zwei getrennt gewachsene Stände zusammen: die Linie 0.5.x auf GitHub (Workspaces, Export, Kampagnensprache, Start-Satz aus der App mit `{{accountSignature}}`) und die lokale Linie 0.4.2 bis 0.4.8 (Copy-Kern, Chance-Winkel, Abmeldezeile, Import, Verbindung `dealsupply`, Versand-Setup, zweiter Satz zum Angebot, Schlussfrage ohne „Link“). Beide Einträge unten bleiben gültig; die Versionsnummern 0.4.x und fulfillment 0.1.1/0.1.2 der lokalen Linie wurden nie veröffentlicht.

**outreach**
- `outreach-copy` → Signatur aus dem Konto (`{{accountSignature}}`) und feste Abmeldezeile stehen nebeneinander; die Abmeldezeile folgt unter `{{accountSignature}}`.
- `outreach-campaign` → Setup-Check prüft `campaign.language`, `salutation` nur bei `de` und `angebot_ausfuehrung` bei Karte A und B.
- `outreach-verify` → Copy-Prüfung mit zweitem Satz je Karte, Schlusssatz ohne „Link“ und den Regeln für englische Kampagnen.
- `verify-agent` → liest `angleWritten` und die Kampagnensprache.
- `beispiel-blueprint.md` → zweiter Satz, Schlusssatz und Sprache in der Übersicht.
- `outreach-launch` → Sperren gelten im ganzen Workspace (Regel 5 nach der neuen Tracking-Regel).

**fulfillment**
- `lead-kontext.md` → Antworter mit `opportunity` und `replied`, Suche außerhalb des Standard-Workspaces mit `workspace`.

## 2026-11-05 – outreach 0.4.8

**outreach**
- `outreach-copy` → Mail 1 bekommt nach dem Angebotssatz immer einen zweiten Satz zum Angebot, passend zur Karte: bei C der Feinheiten-Satz (Fortschritt, „Ich bin gerade noch an den letzten Feinheiten dran, vor allem …“), bei A ein Inhaltssatz (was für diesen Lead konkret drin wäre, im Konjunktiv, nie als erledigte Arbeit), bei B ein Rahmensatz (was der Empfänger im Pilot bekommt und was er dafür gibt), bei D und E keiner. Ersetzt „Feinheiten-Satz Pflicht bei A und C, optional bei B“. Bei A und B schreibt die KI den Satz je Lead über die neue Variable `{{ai.angebot_ausfuehrung}}` (eigener Absatz direkt nach dem Angebotssatz); Pflichtinhalt des Prompts, Selbstprüfung und Prüfliste nachgezogen, Beispiele für A und B neu.
- `outreach-copy` → Schlusssatz ohne „Link“: Standard „Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.“ (Sie-Form „… wenn ich es Ihnen morgen zusende? …“), mit Wort für die Sache „… wenn ich dir morgen den Entwurf zusende? …“. Das „morgen“ steht damit im Schlusssatz, der Halbsatz „und werde morgen mit … fertig“ im Feinheiten-Satz entfällt.
- `beispiel-blueprint.md` → Variante für Karte A und B mit Step-1-Body und ausformuliertem `angebot_ausfuehrung`-Prompt je Karte.
- `outreach-campaign` → `angebot_ausfuehrung` bei Karte A und B anlegen; `outreach-verify` prüft den zweiten Satz je Karte und den Schlusssatz ohne „Link“.
- Copy-Kern (`skills/outreach-copy/kern/`) → dieselben Regeln, Beispiele für Karte A und B.

## 2026-11-01 – outreach 0.5.1

Passt zu ListM8 v4.18 mit dem Weg „Mit deiner KI“ (LISTM8-86, MCP 4.7.0, `list_campaigns` mit `setup_state`/`setup_path`). Ältere Server ohne diese Felder: Der Ablauf erkennt die leere Kampagne an fehlenden Schritten und Variablen.

**outreach**
- `outreach-campaign` → neuer Ablauf „Genannte leere Kampagne füllen“: Der Start-Satz aus der App („Richte mit outreach die Kampagne #123 ein.“, auch mit Workspace oder englisch) füllt genau diese Kampagne per `edit_campaign`, nie per `create_campaign`. Prüft vorher mit `export_campaign_blueprint` und `list_campaigns`, ob sie leer ist und im genannten Workspace liegt; nicht leer oder im Assistenten angefangen heißt nachfragen. Mails und Team in einem Aufruf, danach Prüfen und Freigeben in der App; Lead-Läufe warten bis zur Freigabe.
- Signatur aus dem Konto auf diesem Weg: keine Frage nach Name, Rolle und Firma, jede Mail endet mit der Grußformel und `{{accountSignature}}` (`outreach-campaign`, `outreach-copy`, `copy-lehre.md`).
- `outreach`, `outreach-setup` → leiten den Start-Satz an diesen Ablauf weiter.
- `outreach-launch` → Checkliste: Bei `{{accountSignature}}` braucht jedes Versandpostfach in Instantly eine schlanke Signatur.

## 2026-11-01 – outreach 0.5.0, datenbeschaffung 0.4.2, fulfillment 0.1.1

Passt zu ListM8 v4.18.0 (MCP 4.7.0). Fasst die bisher getrennten Stände Workspaces (#11), Export (#14) und Kampagnensprache (#15) in einer Version zusammen.

### Workspaces (MCP über alle Workspaces einer Person)

**outreach** (ListM8 #95, neues Tool `list_workspaces`)
- `outreach` → neuer Abschnitt „Workspace-Regel“, auf den alle Outreach-Skills verweisen: Workspace kennen (`list_workspaces`, bei mehreren fragen), `workspace=<uuid>` nur bei Aufrufen ohne Objekt-ID (`list_campaigns`, `search_leads`, `list_lists`, `list_lead_runs`, `export_leads`, `check_leads_exist`, `import_leads`, `create_campaign`, `create_list`, `get_credit_balance`, `mark_leads_contacted` mit E-Mails), nie bei `campaign_id`, `lead_id(s)`, `list_id`, `lead_run_id`, `job_id`; vor jedem Schreiben oder Lauf den Workspace nennen; `workspace` in den Antworten lesen; Betrachter (`viewer`) nur lesend; Fehlercodes `workspace_not_found`, `workspace_mismatch`, `workspace_read_only`.
- `outreach-setup` → neuer Schritt 2b: `list_workspaces` nach der Verbindungsprüfung. Ein Workspace wird nur genannt, bei mehreren fragt der Skill, in welchem gearbeitet wird; Betrachter erfahren, dass dort nur Lesen geht; offene Einladungen werden nur genannt.
- `outreach-campaign`, `outreach-generate`, `outreach-import`, `outreach-launch`, `outreach-lists`, `outreach-pipeline`, `outreach-qualify`, `outreach-research`, `outreach-verify` → Verweis auf die Workspace-Regel. Dazu: `create_campaign` im gewählten Workspace, Import und Dubletten-Abgleich im selben Workspace, Liste und Kampagne nur aus einem Workspace, `list_campaigns` nimmt optional `workspace`, Sperren per `mark_leads_contacted(lead_ids=…)` statt E-Mail-Liste, Sperren gelten im ganzen Workspace.
- `outreach-abo-lauf`, `lead-agent`, `verify-agent` → Aufrufe mit `campaign_id`/`lead_id` laufen im Workspace der Kampagne, nie `workspace` mitgeben; `workspace_read_only` beendet die Arbeit am Lead.
- Live-Ansicht → Das Band fragt `list_lead_runs` im Workspace, den die Antworten eines Laufs nennen; Läufe ohne Workspace-Angabe wie bisher. Zwei Tests.
- Ältere Server ohne `list_workspaces`: Die Skills fallen still auf den Standard-Workspace zurück und geben `workspace` nie mit.
- `outreach-setup` → nach dem Wechsel in einen anderen Workspace Guthaben und Plätze mit `get_credit_balance(workspace=<uuid>)` neu lesen; Credits gehören zum Workspace.

**datenbeschaffung**
- `listm8-mcp.md` → Abschnitt „Workspace“: Abgleich, Liste und Import immer im selben, gewählten Workspace; ein Bestandsindex aus einem anderen Workspace zählt nicht. Signaturen mit `workspace` und `list_workspaces`.
- `outreach-uebergabe.md`, `setup.md`, `listen-qualitaet`, `datenbeschaffung` → Index, Prüfung, Liste und Import im selben Workspace; Kampagne und Liste aus demselben Workspace.
- `datenbeschaffung-setup` → nennt den Workspace bei der Prüfung der Outreach-Verbindung, fragt bei mehreren, in welchen importiert wird.

**fulfillment**
- `fulfillment`, `fulfillment-setup`, `lead-kontext.md`, `demo-link.md` → bei mehreren Workspaces nach dem Workspace der Kampagne fragen, `list_campaigns` und `search_leads` dort aufrufen; der Demo-Link (`bulk_set_lead_attributes` mit `lead_ids`) braucht keine Angabe und scheitert für Betrachter mit `workspace_read_only`.

### Export (MCP 4.4.0)

Passt zu ListM8 MCP 4.4.0 (Kampagnen-Export als Datei). Ältere Server kennen `export_campaign_leads` nicht; dann verweist der Skill auf den Export in der App.

**outreach**
- Neu `outreach-export` → Leads einer Kampagne als Excel oder CSV, wie der Export-Dialog der App: Zweck (`sending`, `overview`, `crm`), Umfang, erst `dry_run` mit Zahlen und Ausschlussgründen, dann Datei im Hintergrund, `get_lead_export` bis `ready`, Download per `curl` oder Link (24 Stunden, ohne Anmeldung). Markieren als exportiert nur auf Wunsch, beim ersten Download.
- `outreach` → leitet „als Excel/CSV exportieren“ an `outreach-export`.
- `outreach-lists` → Kampagnen-Export verweist auf `outreach-export`; `export_leads` bleibt für Bestand, Listen und Abgleichsindex.
- `outreach-launch` → Übergabe ohne Instantly-Integration per `outreach-export` (Zweck `sending`, noch nicht exportierte Freigaben, markieren).

### Kampagnensprache (MCP 4.7.0)

Passt zu ListM8 MCP 4.7.0 (Kampagnensprache). Ältere Server kennen `campaign.language` nicht; dann ist jede Kampagne deutsch und alles bleibt wie bisher.

**outreach** (Kampagnensprache `de`/`en`)
- `outreach-campaign` → Sprache im Briefing erfragen (Vorschlag Deutsch) und als `campaign.language` setzen (`de` Standard, `en`). Fehlt das Feld, nimmt `create_campaign` Deutsch (außer `emailLanguage` nennt eindeutig Englisch), `edit_campaign` behält die bisherige Sprache. Setup-Check und Bestätigung nennen die Sprache.
- `outreach-copy` → neuer Abschnitt „Kampagnensprache“: Die Copy-Regeln gelten für deutsche Kampagnen. Englische haben eigene Regeln (Anrede `Hi {first name},`, ohne Person `Hi there,`, kein du/Sie, Gruß `Best,`, Betreff klein mit 2–5 Wörtern wie `quick question`/`quick update`, Opener beginnt groß, Reaktion als eigener Satz oder „which“-Nebensatz, kein „free“, keine Floskel-Einstiege, Mail 1 höchstens 100 Wörter, P.S.-Abmeldezeile in Mail 1 und 3, Anführungszeichen “…”, natürliches US-Englisch, nicht übersetzen); maßgeblich sind die Server-Regeln aus `get_lead_data`. Die Regeln sind geprüft; eine ausführliche englische Copy-Lehre (Beispiele, Offer-Karten A–E) kann später folgen. `beispiel-blueprint` trägt `language: "de"`, `copy-lehre` und `marketing-offer` verweisen auf den Abschnitt.
- `outreach-generate`, `lead-agent` → Mail-Variablen in der Sprache aus `emailGeneration.language`; bei `en` gelten `salutationRule` und `systemPrompt`, die deutschen Prüfpunkte (Umlaute, „…“, du/Sie, deutsche Einstiege und Reaktionen) entfallen. `save_lead_variables` prüft das offene „ nur in deutschen Kampagnen.
- `outreach-qualify`, `lead-agent` → `qualificationSummary` in der Sprache aus `qualificationGeneration.writeBack.summaryLanguage`.
- `outreach-research` → Der Recherchebericht bleibt deutsch, auch in englischen Kampagnen.
- `outreach-verify`, `verify-agent` → Sprache der Kampagne prüfen; bei `en` sind `systemPrompt` und `salutationRule` die Grundlage, die deutschen Prüfpunkte entfallen.
- `outreach-setup` → englische Kampagnen ab MCP 4.7.0.

**fulfillment**
- `lead-kontext`, `demo-link` → Die Antwort an den Lead in der Sprache der Kampagne (`campaign.language`), in englischen Kampagnen mit `Hi Vorname,` und `Best,`.

## 2026-11-01 – outreach 0.4.7

**outreach**
- `outreach-launch` → Versand-Setup auf DealSupplys Stand: Domains beim Domain-Anbieter kaufen (Endungen wie .de, .at, .com, .info, .org; Zapmail selbst verkauft kein .de) und in Zapmail über „Connect Existing Domains“ verbinden, bei Cloudflare über die Verbindung des Cloudflare-Kontos statt Nameservern; Namen nah an der Hauptdomain. Postfächer bei Google oder Microsoft (beides in Zapmail), eine echte Person in Schreibweisen, Profilbild. Warm-up mit Instantlys Voreinstellungen, Start erst bei Health Score über 90 %, am besten 98 bis 100 %. Daily campaign limit 30 und „Campaign slow ramp“ am Postfach statt Wochenplan 100, 200, 300; die Kampagne bekommt gleich Postfächer mal 30. Sendefenster Mo bis Fr 09:00 bis 17:00 wie in der App. Open- und Link-Tracking standardmäßig aus, nur für sofortiges Anrufen nach dem Öffnen an.
- `outreach-copy` → Tracking-Absatz auf dieselbe Regel gebracht.

## 2026-11-01 – fulfillment 0.1.2

**fulfillment**
- `fulfillment` (Modus B) und `lead-kontext.md` → Antworter in zwei Abrufen: erst `contact_status="opportunity"` (interessierte Antwort, auch aus dem Instantly-Abgleich), dann `"replied"`. Bisher fand der Skill nur `replied` und bot interessierte Leads nie an. Der Filter nimmt genau einen Wert, deshalb zwei Aufrufe.

## 2026-11-01 – outreach 0.4.6, fulfillment 0.1.1

**outreach**
- Die mitgelieferte MCP-Verbindung heißt jetzt `dealsupply` und zeigt auf `https://app.dealsupply.ai/_mcp/v1` (vorher `akquise`, `outreach.akquise.de`). Wer das Plugin bisher über die Verbindung `akquise` genutzt hat, meldet sich einmal neu an; eine von Hand angelegte DealSupply-Verbindung kann danach weg.
- Live-Ansicht in Claude Code: Standard-Server `dealsupply`, Links ohne eigene Adresse vom Server führen auf `app.dealsupply.ai`.
- `outreach-copy` → keine Verweise mehr auf fremde Regelwerke anderer Marken; die Regeln selbst bleiben gleich.
- `outreach-setup` → Anmeldeweg für DealSupply-Kunden mit den heutigen Menünamen der Claude App („Connectors“ → „Connect“); ChatGPT im Browser als eigene Umgebung (nur Verbindung, keine Skills).

**fulfillment**
- `demo-akquise-kampagne` heißt jetzt `demo-kampagne` (Aufruf `/demo-kampagne`, in Claude Code `/fulfillment:demo-kampagne`); Inhalt unverändert. `fulfillment`, `fulfillment-setup` und die Referenzen nennen den neuen Namen.

## 2026-11-01 – outreach 0.4.5

**outreach**
- `outreach-import` → auf den Stand des Import-Werkzeugs gebracht: Leads brauchen eine Mail **oder** eine eigene Website, Leads ohne Mail werden normal recherchiert; ungültige Zeilen meldet der Server einzeln in `rejected_rows`, statt den ganzen Aufruf abzuweisen; Person der Zeile über `firstName`, `lastName`, `academicTitle`, `salutation` oder `fullName`; Platzprüfung und Report zählen neue Leads statt neuer Mail-Adressen.

## 2026-11-01 – outreach 0.4.4

**outreach**
- `outreach-import` → Google-Maps-Listen: die Place ID immer als `place_id` mitgeben. Der Skill erkennt sie an Spaltennamen, am Wertformat (`ChIJ…`) und in Maps-Links, trennt sie von `cid` und `google_id` und fragt nach, wenn sie in einer Maps-Liste fehlt. Dazu die Liste der Google-Maps-Schlüssel, die der Import ohne `attribute_mappings` behält.

## 2026-10-27 – outreach 0.4.2

Fasst die Arbeitsstände 0.3.43 bis 0.3.45 auf der Linie 0.4.x zusammen.

**outreach**
- `outreach-copy` → software-freier Copy-Kern unter `skills/outreach-copy/kern/` (Copy-Lehre, Offer-Lehre, Beispiele, Prüfskript). Er ist die Quelle für den Heartbeat-Skill `cold-mail-copy`; `scripts/export-copy-kern.sh` überträgt ihn, `--check` meldet Abweichungen.
- `outreach-copy`, `lead-agent`, `verify-agent` → Chance-Winkel für KI-Variablen in Instantly-Varianten (A/B-Test der Intros: Lob gegen Chance, ohne Beleg Rückfall auf Lob).
- `outreach-copy`, `verify-agent`, Copy-Kern → feste, menschliche Abmeldezeile unter der Signatur („Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid, dann melde ich mich nicht mehr.“). „STOPP“, „Abmelden“, „unsubscribe“ und ähnliche Opt-out-Fachsprache sind verboten; der technische Abmeldeweg im Versandtool bleibt.

## 2026-10-27 – Umzug nach DealSupply (ohne neue Plugin-Version)

**outreach**, **datenbeschaffung**, **fulfillment**
- Das Repo zieht von `RankM8/outreach-plugins` nach `DealSupply/outreach-plugins`. README, Manifeste (`repository`, `author`, `developerName`), Marketplace-Owner und die Update-Skills nennen die neue Adresse. Der Marketplace heißt weiter `outreach-plugins`, die Befehle zum Aktualisieren bleiben gleich; GitHub leitet die alte Adresse weiter. Das SEO-Werkzeug RankM8 in `fulfillment` bleibt unverändert.

## 2026-10-26 – outreach 0.4.1, datenbeschaffung 0.4.1

Passt zu ListM8 MCP 4.3.0 (Richtpreis mit Abrechnung nach Aufwand). Ältere Server kennen `charging` nicht; dann gilt der feste Preis wie bisher.

**outreach** (Richtpreise)
- `outreach-pipeline` → das Angebot nennt in `charging` die Abrechnungsart: `fixed` bucht den Preis genau, `guide` ist ein Richtpreis (jede Stufe bucht ihren Aufwand, mindestens den Richtpreis, höchstens das Doppelte). Bei `guide` alle Preise als ca.-Angabe nennen; `estimated_credits` ist die Summe zu diesen Preisen (Untergrenze), `max_credits` die echte Obergrenze (das Doppelte). Den Teil über dem Richtpreis bucht der Server nur bis zum freien Guthaben und zum Lauf-Budget. `effort_not_priced` gibt es nur noch bei Festpreisen. Abbruch und Statusbericht: bei Richtpreisen kann `spent_credits` über Preis mal Leads liegen, höchstens beim Doppelten und nie über `budget_credits`.
- `outreach-research`, `outreach-qualify`, `outreach-generate`, `outreach-launch` → „Credits je Lead“ statt „Credits zum festen Preis je Lead“.

**datenbeschaffung**
- `listm8-mcp.md` → „Credits je Lead“ statt „Credits zum festen Preis“.

## 2026-10-26 – outreach 0.3.42

**outreach**
- `outreach-launch` (`technisches-setup`) → Zapmail-Preis korrigiert: Der Starter-Plan kostet 39 USD im Monat für 10 Postfächer (rund 3,90 USD je Postfach, jedes weitere 3,50 USD), nicht 3,90 USD für alle zehn. Geprüft auf zapmail.ai am 26.10.2026. Die Gesamtkosten des Setups steigen dadurch auf rund 125 EUR im Monat (Hypergrowth) bzw. rund 80 EUR (Growth).

## 2026-10-23 – outreach 0.3.41

**outreach** (gleichauf mit dem ListM8-Server)
- `outreach-research`, `lead-agent` → Quelle im Bericht ist die Seite oder Plattform (URL, Impressum, Google-Profil, Import), nie ein Arbeitsschritt wie „Vorqualifizierung“ oder „Recherche“. Grund: Im Gegencheck vom 23.10. nannte ein Modell in 10 von 15 Berichten „Vorqualifizierung“ als Quelle.

## 2026-10-23 – outreach 0.3.40

**outreach** (gleichauf mit dem ListM8-Server: Reaktion als Richtung, Mittelweg)
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent` → Die fünf erprobten Reaktionen sind Richtung und Tonlage, keine Pflicht. Der Server schlägt je Lead eine vor; passt eine eigene kurze Reaktion besser zum Detail, wird sie im selben Ton formuliert (etwa „da musste ich direkt schmunzeln“ bei einer historischen Kegelbahn), höchstens etwa sechs Wörter, keine Floskel. Passt der Vorschlag nicht, eine eigene statt einer festen Ausweichform. Nie derselbe Satz in allen Mails.
- `verify-agent` → Eine eigene, passende Reaktion ist kein Befund; Gutachten-Ton, Übertreibung und Floskeln bleiben Befunde, eine deutlich zu lange freie Reaktion ist ein Hinweis.

## 2026-10-23 – outreach 0.3.39

**outreach** (gleichauf mit dem ListM8-Server: Reaktionsliste nach Antwortdaten)
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent`, `verify-agent` → Die Reaktion im Intro-Schluss nutzt die fünf Formen mit den besten Antwortquoten im Prod-Dump vom 23.10.2026 (725 kontaktierte Intros): „das fand ich richtig schön“ (13,0 %), „das ist mir direkt hängen geblieben“ (9,6 %), „das hat mir gut gefallen“ (8,9 %), „das fand ich richtig sympathisch“ (8,2 %), „das hat mich angesprochen“ (6,1 %). „schöne Idee“ und „schöner Ansatz“ sind raus, ebenso die ungetesteten Formen. „richtig“ in einer Reaktion ist erlaubt, Übertreibung und Floskeln nicht.
- `verify-agent` → Hinweis bei übertriebener Reaktion oder „sympathisch“/„schön“ hinter einer Bewertungszahl, nicht mehr bei „richtig“.

## 2026-10-23 – outreach 0.3.38

**outreach** (gleichauf mit dem ListM8-Server: Reaktion vor Würdigung)
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent`, `verify-agent`, `outreach-generate`, `outreach-verify` → Neue Rangfolge im Intro-Schluss: 1) kein Schluss, wenn das Detail selbst ein Lob ist (Kundenstimme, Auszeichnung, Bewertungslob) oder der feste Folgesatz lobt; 2) sonst eine kurze, schlichte Reaktion in der Vergangenheit am Detail („das ist mir direkt aufgefallen“, „das fand ich direkt spannend“), je Lead wechselnd; 3) eine Würdigung nur ausnahmsweise mit etwas Neuem und Konkretem, nie im Gutachten-Ton und nie als „das zeigt, wie …“. Grund: In den Blindtests vom 23.10. geriet die Würdigung in 18 von 77 Mails zum Gutachten oder wiederholte das Detail, Reaktionen wurden kaum bemängelt.
- `verify-agent` → Ein fehlender Schluss ist kein Befund mehr; Folgerung im Gutachten-Ton ist einer, eine gesteigerte Reaktion ein Hinweis. Derselbe Reaktionssatz in fast allen Mails einer Kampagne ist ein systematischer Befund.
- `copy-lehre` → Beispiele ohne Schluss oder mit Reaktion, Würdigung und Superlativ nur als Ausnahme, Gegenbeispiel mit dem Herrenstudio.

## 2026-10-23 – outreach 0.3.37

**outreach** (gleichauf mit dem ListM8-Server: Kern-Passung vor dem offenen Vorfilter)
- `lead-agent` → Ein Kerngeschäft außerhalb des Zielkunden ist `not_qualified`, auch ohne Disqualifier der Liste; eine einzelne Zusatzleistung oder thematische Nähe ist keine Überschneidung.
- `outreach-campaign` (Referenz Qualifizierung) → Der „Passt, wenn …"-Satz nennt ein Merkmal der Zielbranche, nie eines, das jede Nachbarbranche erfüllt; „Ablehnung nur mit konkret benanntem Disqualifier" schützt nur Grenzfälle der Zielbranche. Grund: Im Blindtest vom 23.10. gingen 18 von 77 Mails an unpassende Leads (Massagepraxen, Hotels, Tantra-Massage, proktologische Praxis).

## 2026-10-23 – outreach 0.3.36

**outreach** (gleichauf mit dem ListM8-Server: Recherche-Bericht in Kundensprache)
- `outreach-research`, `lead-agent` → Der Bericht enthält nur Ergebnisse über die Firma in Alltagssprache. Regeln aus `anchorRules`, `campaignFrame` und `researchTier` stehen weder mit Namen noch mit Inhalt darin: keine Schwellen, keine Abwägung, ob ein Anker trägt, keine Abhakliste der Ausschlussgründe (stattdessen die Tatsache über den Betrieb), kein Seitenbudget, keine Recherche-Stufe, keine Herkunft „aus der Vorqualifizierung“, kein Prüfstatus von Adressen, keine Suchvorlagen. Grund: Im Blindtest mit fünf Modellen stand Arbeitssprache in 49 von 80 Berichten.

## 2026-10-23 – outreach 0.3.35

**outreach** (gleichauf mit dem ListM8-Server, Beispiele folgen den eigenen Schluss-Regeln)
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent`, `verify-agent` → Seltenheit als eigene Erfahrung („so eine Nachsorge ist mir noch nicht begegnet“), nie im allgemeinen „man“; Anerkennung nur mit Inhalt („da steckt richtig viel Handarbeit drin“) statt „das spricht für eure Arbeit“; ein Schluss, der ausmalt, was Kunden dank des Details tun können oder sich sparen, ist in jeder Satzform Mechanik-Nutzen. Beispiele entsprechend ersetzt (Badumbau, Krone To Go).
- `outreach-copy` → Der Schluss hängt mit Komma am Detail, ein zweiter Satz nur, wenn er als eigener Satz besser klingt.
- `outreach-research`, `lead-agent` → Was einen Anker abhebt, steht im Bericht am Detail, nicht als „ungewöhnlich“ oder Branchenurteil.

## 2026-10-23 – outreach 0.3.34

**outreach** (gleichauf mit dem ListM8-Server, Blindvergleich vom 23.10.2026)
- `outreach-research`, `lead-agent` → Recherche-Bericht in Alltagssprache: keine Arbeitsbegriffe aus den Anker-Regeln (MINDESTSTÄRKE, Bedingung (a) bis (d), Austauschtest, Sperrliste, Ersatzsatz, PFLICHT-WEBSUCHE) und keine Feldnamen, denn der Bericht erscheint für Kunden in der Lead-Ansicht. Superlative und Vergleiche mit anderen Betrieben nur mit Beleg aus der Quelle.
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent`, `verify-agent`, `outreach-generate` → Intro zusammen höchstens 30 Wörter, EIN Detail statt gestapelter Lobpunkte; die Würdigung sagt etwas Neues statt das Detail umzuformulieren, Seltenheit nur als eigene Erfahrung am Detail, nie als Vergleich mit anderen Betrieben; im Zweifel Reaktion oder kein Schluss, nie zwei Schlussformen hintereinander.
- `verify-agent` → umformuliertes Detail, Gutachten-Urteil, Vergleich ohne Beleg, zwei Schlussformen und gestapelte Lobpunkte sind Verstöße.

## 2026-10-23 – outreach 0.3.33

**outreach** (gleichauf mit dem ListM8-Server: Abschluss-Stufen statt Nutzen zuerst)
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent`, `verify-agent`, `outreach-verify`, `outreach-generate` → Intro = Einstieg + Anker + Abschluss, der Abschluss bleibt keine Pflicht. Stufen: 1) Würdigung am Detail (Folgerung, Anerkennung, Seltenheit mit dem Detail, Kundensicht, lobender Nutzen), 2) Reaktion in der Vergangenheit am Detail, lieber schlicht als gesteigert, 3) Superlativ nur bei wirklich beeindruckendem Anker und am Detail. Hinter einer Bewertungszahl bleibt die Reaktion.
- Verboten: Mechanik-Nutzen (ein Schluss, der erklärt, was man dank des Details tun kann, etwa „so können sich Interessierte vorab ein Bild machen“), Lob ohne Detail, doppeltes Lob. Das Prüfer-Verbot gilt nur noch für leere Urteile, die aus dem Detail nicht folgen. Grund: In etwa einem Drittel der Intros stand ein Mechanik-Nutzen.
- `copy-lehre` → Beispieltabelle nach Stufen, Kundenlob ohne Schluss, Gegenbeispiel Mechanik-Nutzen. `verify-agent` → Mechanik-Nutzen ist ein Befund, eine Reaktion statt möglicher Würdigung nicht.

## 2026-10-17 – outreach 0.3.32

**outreach** (gleichauf mit dem ListM8-Server: der Schluss im Intro ist keine Pflicht mehr)
- `outreach-copy`, `copy-lehre`, `beispiel-blueprint`, `lead-agent`, `verify-agent`, `outreach-verify`, `outreach-generate` → Ein Lob aus Bewertungstexten trägt das Intro allein; ein Schluss, der das Lob nur wiederholt, fällt weg, und neben einem lobenden festen Folgesatz wird nie zweimal gelobt. Ein neutrales Faktum und eine Bewertungszahl bekommen weiter einen kurzen Schluss. Grund: Bei der einzigen Kampagne mit Antwortdaten kamen alle Interessenten aus Intros ohne Schluss.
- Die Reaktion aus dem Block `SCHLUSS DES OPENERS` ist ein Vorschlag, keine Vorgabe. `verify-agent`: fehlender Schluss hinter Kundenlob ist kein Befund, doppeltes Lob ein Hinweis.
- `copy-lehre` → Beispiel zur Bewertungszahl schließt mit einer Reaktion statt mit einem Nutzen (Widerspruch zur Server-Regel behoben).

## 2026-10-15 – outreach 0.3.32

**outreach** (Kundenfall 15.10.2026: Claude lehnte eine Prompt-Änderung über den MCP ab)
- `outreach-campaign` → Einen Variablen-Prompt ändert `update_ai_variable` (ListM8-MCP 2.4.0) ohne Export und Voll-Blueprint. Die Warnung, `edit_campaign` lösche alle erzeugten Werte, ist ersetzt: Der Server gleicht Variablen seit August 2026 per Name ab, Werte bleiben. Rückfrage bleibt Pflicht, bevor schon erzeugte Leads neu generiert werden.
- `outreach-launch`, `outreach-generate`, `outreach-verify`, `outreach-copy` (Copy-Lehre) → nennen `update_ai_variable` für Prompt-Änderungen und korrigieren dieselbe Löschwarnung.

## 2026-10-14 – outreach 0.4.0, datenbeschaffung 0.3.1

Setzt ListM8 MCP 3.0.0 voraus (Credits zum festen Preis je Lead). Meldet `ping` eine ältere Version, kennt der Server noch keine Credits; dafür steht in `outreach-pipeline` genau ein Satz.

**outreach** (Credits zum festen Preis, Angebot vor dem Lauf, Account-Limit)
- `outreach-pipeline` → Server-Lauf mit Credits zum festen Preis je Lead statt OpenRouter-Guthaben: einmal je Lauf `get_credit_balance` (`billing_mode`, `available`, `purchase`), dann Pflicht-Angebot `quote_lead_run` (Preis je Lead, aussortierter Lead, `max_credits`, Leads ohne Arbeit, Kappung) und Start mit `quote_hash` nach Zustimmung. Lauf-Budget nur noch `budget_percent` (Anteil am verfügbaren Guthaben); `budget_usd` ist veraltet und wird vom Server ignoriert. BYOK-Konten (eigener OpenRouter-Key): keine Preise, kein Lauf-Budget, kein Nachkauf. Preise nur als Beispiel im Standardmodell (Basis 0,75, Smart 1, Deep 2, aussortiert 0,25), verbindlich ist das Angebot.
- `outreach-pipeline` → neue Startfehler als Tabelle: `price_changed`, `model_not_priced`, `effort_not_priced`, `model_missing`, `credits_exhausted`, `limit_reached` (auch ohne aktives Abo), `run_not_startable`. Neuer Endzustand `credits_exhausted`: Nachkauf nur bei `purchase.allowed` (Link `purchase.app_url`), danach `resume_lead_run` für denselben Lauf; `billing_mode_changed` heißt neuer Lauf. `budget_exhausted` meint nur noch das Lauf-Budget aus `budget_percent`. Abbruch: laufende Stufen buchen ihren eingefrorenen Festpreis. Bericht nennt gebuchte Credits und das Guthaben danach, bei BYOK das eigene OpenRouter-Konto, im Abo „keine Credits“.
- `outreach` → Fragen zu Guthaben, Credits, Limits, freien Plätzen und Nachkauf beantwortet ein Aufruf von `get_credit_balance` (`account`, `by_origin`, `purchase`); kein Nachkauf, wenn `purchase.allowed` false ist; Jahresabo wechselt erst nach Laufzeitende auf monatlich.
- `outreach-setup` → nach der Verbindung `ping` (Version) und `get_credit_balance` (Abrechnungsmodus, verfügbare Credits, Leads im Account, fehlendes Abo); ein eigener OpenRouter-Key nur bei BYOK.
- `outreach-import` → Platzprüfung vor dem Import gegen `account.free_slots`: nur neue E-Mail-Adressen belegen einen Platz. Passt es nicht, lehnt der Server den ganzen Aufruf mit `limit_reached` ab; Teilimport mit `allow_partial=true` nur nach Rückfrage. Neue Antwortfelder (`new_leads`, `known_leads`, `free_slots`) und Job-Felder (`skipped_over_limit`).
- `outreach-lists` → Löschen mit `delete_leads=true` gibt Plätze sofort frei; schon gebuchte Credits werden nicht erstattet.
- `outreach-campaign` → `limit_reached` bei Kampagnen nur ohne aktives Abo bzw. hinter der Paywall; `references/research.md`: die Recherche-Stufe bestimmt den Credit-Preis je Lead, `deep` nur mit Zustimmung.
- `outreach-abo-lauf`, `outreach-qualify`, `outreach-research`, `outreach-generate`, `outreach-verify`, `lead-agent` → Abo-Lauf und Manuell-Modus kosten keine Credits und kein OpenRouter-Guthaben, nur Abo-Kontingent.
- Live-Ansicht → Kosten in Credits mit deutschem Zahlformat (bis drei Nachkommastellen, „12,25 Credits“, Budget als „12,25/50 Credits“), bei BYOK ohne Betrag; `credits_exhausted` ist ein Endzustand („Credits aufgebraucht“), `budget_exhausted` heißt „Lauf-Budget erreicht“; `resume_lead_run` holt denselben Lauf zurück ins Band und zeigt „Lead-Run fortgesetzt“.

**datenbeschaffung** (Platzprüfung vor dem Import)
- `datenbeschaffung` → Phase 3 liest mit MCP `get_credit_balance.account.free_slots`: Die geplanten neuen Leads müssen vor dem bezahlten Scrape in die freien Plätze passen (sonst kleinere Menge, Leads löschen oder Plan wechseln); ohne aktives Abo lässt sich nichts importieren. Der KI-Lauf danach hat einen eigenen Preis in Credits (`quote_lead_run`) oder läuft im Abo ohne Credits.
- `listen-qualitaet` → Platzprüfung vor `import_leads` wiederholen, wenn die bereinigte Liste mehr neue Adressen hat als geplant.
- `listm8-mcp.md` → Vertragsstand MCP 3.0.0: Import und Listen kosten keine Credits; neue Zeile `get_credit_balance`; Lead-Limit beim Import (`limit_reached`, `allow_partial`, neue Antwort- und Job-Felder); Löschen gibt Plätze sofort frei, gebuchte Credits werden nicht erstattet; der KI-Lauf kostet Credits zum festen Preis je Lead.
- `outreach-uebergabe.md` → Platzprüfung beim Import, `start_lead_run` nach Preis-Angebot oder Abo-Lauf, Löschen gibt Plätze sofort frei.
- `datenumfang.md` → die Recherche-Tiefe steuert nur das Seitenbudget; den Credit-Preis bestimmt die Recherche-Stufe.

## 2026-10-14 – datenbeschaffung 0.4.0

**datenbeschaffung** (neuer Weg F: SaaS- und Software-Firmen in DACH, Testreihe vom 14.10.2026)
- `weg-f-saas` → neuer Weg für „alle SaaS in DACH“: OMR Reviews und Startbase kostenlos, dazu die LinkedIn-Firmensuche segmentiert nach Region und Größe, Einordnung SaaS gegen Agentur durch Claude, Details nur für SaaS, die noch keine Quelle kennt, Zusammenführen auf die Domain und Sitzprüfung im Impressum. Kernbefund aus der Vollerhebung Hamburg: LinkedIn 387, OMR 246, nur 62 in beiden; keine Quelle allein findet mehr als etwa ein Viertel (Startbase dazu: 135, mit LinkedIn nur 27 gemeinsam; geschätzt 1.500 bis 2.000 SaaS in Hamburg).
- `datenbeschaffung` → Routing: Software- und SaaS-Firmen gehen an `weg-f-saas`, nicht mehr an `weg-a-b2b-google`.
- Neue Skripte: `omr_products.py` (OMR-Schnittstelle, 14.023 Produkte in einer Minute), `startbase_saas.py` (Geschäftsmodell SaaS, Zielgruppe B2B), `linkedin_saas.py` (Segmente zusammenlegen, Sitzfilter, Tabelle zum Einordnen, Details-Input), `website_suche.py` (Website über Rechtsträger und Ort, 52 bis 58 % Treffer), `quellen_zusammenfuehren.py` (Domain-Abgleich, Herkunft in `quellen`), `sitz_check.py` (Sitz, PLZ, Impressum-Adresse und Produkt-Signale, kostenlos). 8 Tests.
- `apify-actors.md` → LinkedIn-Firmendetails (`harvestapi/linkedin-company`), Trefferzahl je Segment über `totalResultCount`; Capterra-Actors ausgeschlossen bzw. nicht empfohlen; Impressum-Actor an JavaScript-Lücken schwach und langsam.
- `kosten.md`, `erfahrungswerte.md`, `datenumfang.md` → belegte Kosten und Trefferquoten der SaaS-Quellen, Spalten für OMR- und LinkedIn-Daten.

## 2026-10-13 – outreach 0.3.31

**outreach** (gleichauf mit dem ListM8-Server, A/B-Vergleich App gegen MCP vom 13.10.2026)
- `outreach-copy`, `verify-agent`, `lead-agent`, `outreach-verify` → Positiver Schluss: Eine kurze Reaktion direkt hinter dem benannten Detail („…, das ist mir gleich ins Auge gefallen“) muss das Detail nicht wiederholen und ist kein Befund. Wiederholte Reaktionen über eine Kampagne sind erwartet (der Server gibt sie je Lead aus einer festen Liste vor); gleich lautende Nutzen-Schlüsse wie „Interessierte können sich vorab orientieren“ hinter Bewertungszahlen bleiben ein systematischer Befund.
- `outreach-copy` → Bewertungszahlen erst, wenn weder Bewertungslob noch ein abhebendes Website-Detail besteht, Schluss dann mit der Reaktion; Wachstum oder Auszeichnungen eines Franchisegebers gehören nicht dem angeschriebenen Standort. Was der Standort selbst anbietet, bleibt ein Anker.
- `verify-agent` → Eine Reaktion, die nicht zum Anker passt („Idee“ hinter einer Bewertungszahl) oder den Einstieg doppelt, ist ein Hinweis.


## 2026-10-12 – fulfillment 0.1.0, outreach 0.3.30

**fulfillment** (neues Plugin: das Marketing-Offer liefern)
- `fulfillment` → Einstieg mit zwei Modi: „Offer finden“ (welches Offer lässt sich mit KI so liefern, dass dem Nutzer 5-10 Minuten bleiben; Übergabe an `outreach-copy`) und „Demo liefern“ (Offer aus `blueprint.campaign.intelligence.offer_contract`, Antworter über `list_leads(contact_status="replied")` mit leeren Queue-Filtern, Weiterleitung an den Bau-Skill). `get_lead_data` sperrt angeschriebene Leads (`contact_gate`); die Demo-Skills lesen deshalb die Website des Leads live.
- `demo-webseite` → Webseiten-Entwurf aus der bestehenden Website des Leads: Steckbrief, Struktur, eine `index.html` (überall machbar, auch ohne Dateisystem), Qualitätsprüfung, Abstimmung.
- `demo-seo` → SEO-Ergebnis statt „Analyse“: Suchbegriffe auf Platz 11–20 (`domain_keywords`), lokale Suche (`serp_search`), neue Title-Tags, KI-Suchmaschinen mit fertiger `llms.txt`. RankM8 optional; ohne Verbindung die Bausteine ohne Messdaten. Mit dem RankM8-Tool `quick_check` misst ein Aufruf Seite-2-Begriffe, lokale Suche, KI-Crawler und `llms.txt`; `share_quick_check` liefert eine fertige, nicht auffindbare Report-Seite als Alternative zur eigenen Netlify-Seite.
- `demo-anzeigen` → 3 Meta-Anzeigen, Google-Suchanzeige, Stellenanzeige oder 30-Tage-Content-Plan; nichts wird geschaltet.
- `demo-leadliste` → Lead-System als Demo, das schon 30–50 passende Wunschkunden gefunden hat; `datenbeschaffung` im Geschenk-Modus (ICP, Pilot, harter Deckel 2 $; kein Bestandsabgleich, kein Import, keine Kampagne), nur Firmendaten.
- `demo-akquise-kampagne` → Muster-Kampagne für Leads, die selbst Kunden gewinnen wollen: Zielgruppe, Offer, Sequenz und 3 Beispiel-Mails nach `outreach-copy`; nichts wird versendet.
- `demo-ausliefern` → nicht auffindbar veröffentlichen bei Netlify (Connector, CLI oder Drop; Gratisplan etwa 20 Veröffentlichungen im Monat), `noindex` per Meta-Tag (plus `_headers`, wenn die KI Dateien schreibt), schwer erratbare Adresse, Link als `demo-url` und `demo-datum` per `bulk_set_lead_attributes` am Lead (Bindestrich-Schlüssel, sonst legt die App das Feld doppelt an), Antwort-Text zum Kopieren, Löschen nach 30 Tagen.
- `fulfillment-setup`, `fulfillment-update` → Einrichtung (Outreach-Verbindung, Plugins, Netlify, optional RankM8) und Aktualisierung.
- `fulfillment-referenzen` → Demo-Katalog, Lead-Kontext, Umgebungen, Netlify, Demo-Link und Antwort-Vorlagen, Qualitätsprüfung, Recht und Grenzen, Webseiten-Bauplan (Erfahrungswerte aus über 60 Demo-Seiten).

**outreach**
- `outreach` → Weiterleitung an `fulfillment` (Offer-Lieferbarkeit prüfen, Demo für einen Antworter bauen).
- `outreach-copy` → `references/marketing-offer.md`: Verweis auf den Demo-Katalog des Plugins fulfillment bei der Frage, ob ein Offer lieferbar ist.
- `outreach-update` → nennt das Plugin fulfillment.
- `outreach-abo-lauf` → Beschreibung in Anführungszeichen: Der Doppelpunkt brach das YAML, `npx skills add` übersprang den Skill bisher.

## 2026-10-11 – outreach 0.3.29

**outreach** (ListM8 MCP 2.3.0: Recherche-Stufen Basis, Smart, Deep Research)
- `lead-agent`, `outreach-research` → Abo-Recherche hält sich an `get_lead_data.researchGeneration.researchTier.rules`: Basis nur Website und importierte Daten (eine Suche nach Firma und Ort nur, wenn die Website gar nichts liefert), Smart höchstens eine Bewertungssuche ohne starken Anker, Deep wie bisher mit Bewertungen zuerst. „Bewertungen zuerst“ gilt damit nur noch für Deep. Fehlt das Feld (älterer Server), gilt Deep. Gilt auch für „Nachbessern“ mit `art=recherche`.
- `outreach-pipeline` → Server-Lauf: `research_tier` für einen einzelnen Lauf, nur auf Nennung des Users.
- `outreach-campaign` → `references/research.md`: optionaler Blueprint-Schlüssel `researchAgentConfig.researchTier`, Wirkung der Stufen auf „Bewertungen zuerst“.

## 2026-10-11 – datenbeschaffung 0.3.0

**datenbeschaffung** (Testreihe mit echten Läufen: Maps, B2B-Datenbanken, LinkedIn, Instagram, Impressum, Verifier)
- `erfahrungswerte.md` → Messwerte vom 11.10.2026: Maps-Treffer, E-Mail-Quote und Rezensionen je Branche (Elektro, SHK, Agenturen, Dachdecker, Maschinenbau), B2B-Quellen im Vergleich, E-Mail-Lücke nach Maps, Coaches über LinkedIn und Instagram.
- `weg-c-local-maps` → `reviewsStartDate: "18 months"` im Standard-Input (halb so viele bezahlte Rezensionen); Kategorie im Pilot prüfen statt der Übersetzung zu trauen (`roofing contractor` 12 % Treffer, `Dachdecker` 57 %, mit `categoryFilterWords` 86 %); Suchwörter für Agenturen und Maschinenbau.
- `datenbeschaffung` → Industrie und Maschinenbau zuerst über Maps (85 % passend, 95 % mit Adresse), dann LinkedIn-Firmensuche plus Impressum, dann Datenbank.
- `build_csv.py` → erkennt Branchenportale als Website und verwirft deren Adressen; Adresse der eigenen Domain vor Freemail vor fremder Domain (Umlaut-Domains und andere Endungen zählen als eigene); Impressum-Adressen nur von der eigenen Domain oder Freemail; Inhaber nur bei Inhaber, Geschäftsführung, Gründer; Platzhalter- und Umlaut-Adressen verworfen; versteht die Formen von B2B-Datenbanken, LinkedIn-Personen und -Firmen, Instagram-Profilen und Impressum-Actors; markiert geratene Adressen. 18 Tests.
- `listen-qualitaet` → Entscheidungstabelle für das Verifier-Ergebnis; geratene Adressen nur „gut“; Preisfalle im kostenlosen Apify-Plan (0,10 $ je Adresse).
- `apify-actors.md`, `zugriff.md` → Actors mit Vollzugriff auf das Apify-Konto ausgeschlossen (`code_crafter/leads-finder`); neue Abschnitte B2B-Datenbanken und LinkedIn-Firmen; Verifier-Preise je Stufe.
- `kosten.md`, `datenumfang.md`, `impressum-enrichment`, `weg-a-apollo`, `weg-d-coaches-linkedin`, `weg-d-instagram-hashtag` → belegte Kosten je Quelle; Rezensions-Stichworte nur mit Ortsdetails; zweiter Impressum-Lauf nach Maps lohnt selten, bei LinkedIn-Firmen ist er der Normalfall; Angestellte bei LinkedIn-Coaches aussortieren; deutsche Hashtags.
- `noise-domains.md` → drei Branchenportale aus den Maps-Läufen.

## 2026-10-11 – datenbeschaffung 0.2.0

**datenbeschaffung** (Nur beschaffen, was die Plattform nicht selbst findet)
- `datenbeschaffung-referenzen` → neue Referenz `datenumfang.md`: was die Plattform je Lead selbst erledigt (Website, Impressum, Ansprechpartner, persönliche Adresse), was je Quelle mitkommen muss (Google-Bewertung und Rezensionen, LinkedIn-, Instagram-, Plattform- und Shopdaten), was nie hochgeladen wird, die E-Mail-Lücke und eine Empfehlung zur Recherche-Tiefe.
- `build_csv.py` → reicht die Zusatzspalten jetzt durch. Bisher schrieb es nur elf feste Spalten; Google-Bewertung, Anzahl, Rezensionen und alle Plattformspalten der Wege (Follower, Bio, Headline, LinkedIn, Plattform, Umsatz) gingen vor dem Import verloren. Neu: `rating`, `reviews_count`, `place_id`, `reviews_tags`, `google_rezensionstexte` (5 neueste mit Text, ohne Namen der Verfasser), `inhaber`/`inhaber_rolle` aus dem Impressum des Maps-Scrapes, feste Namen für die Plattformspalten, `--keep` für weitere Rohfelder. Versandadresse: persönliche vor info@, nie bewerbung@ o. Ä., solange es eine andere gibt; Adresse aus dem Impressum, wenn der Scrape keine hat. Der Google-Maps-Link wird nie mehr als Website übernommen. Tests unter `plugins/datenbeschaffung/tests/`.
- `weg-c-local-maps` → Rezensionen im Standard-Input (`maxReviews: 10`, neueste, ohne Personendaten), Kosten aus dem Testlauf vom 11.10.2026 (0,0036 $ je Place ohne, 0,0061 $ mit Rezensionen), E-Mail-Lücke nur noch für die Adresse.
- `datenbeschaffung` → neuer Leitsatz und Phase 2b „Datenumfang festlegen“; Apify-Zugang erst nach der Wahl des Wegs prüfen; Maps-Weg auch für Agenturen und Kanzleien mit Maps-Eintrag; Empfehlung der Recherche-Tiefe bei der Übergabe.
- `impressum-enrichment`, `enrichment-waterfall`, `weg-a-apollo`, `weg-b-storeleads`, `weg-d-coaches-google`, `weg-a-b2b-google` → keine Entscheider-, Register- oder Mobilnummern-Beschaffung vorab; Impressum nur für die Adresse mit dem günstigsten passenden Actor; Waterfall erst nach der Recherche; Apollo für schwer auffindbare Firmen, nicht wegen der Kontaktdaten.
- `outreach-uebergabe.md`, `listm8-mcp.md`, `csv-spalten.md`, `listen-qualitaet` → Google-Spalten erkennt der Import selbst; empfohlene Attributnamen für alle übrigen Spalten; Prüfung vor dem Import, ob die Einstiegsdaten in der CSV stehen.
- `kosten.md`, `apify-actors.md`, `zugriff.md` → Preise des Maps-Actors je Preisstufe, Mindestdeckel je Actor (Google Maps 0,50 $).

## 2026-10-10 – outreach 0.3.28

**outreach** (Zusammenführung zweier paralleler Stände)
- Enthält die veröffentlichten Stände 0.3.21–0.3.23 (Startdialog-Auswahl im Abo-Lauf, Grenzen des Zurücksetzens, Anführungszeichen) und die bisher unveröffentlichten Arbeitsstände 0.3.21–0.3.27 vom 07. und 08.10. (Abo-Lauf als Workflow, Opener-Regeln vom Server, Anrede, Sterne-Anker, positiver Schluss). Beide sind unten einzeln beschrieben.
- `outreach-pipeline`: Startdialog-Auswahl und Abo-Lauf als Workflow (`outreach-abo-lauf`) zusammengeführt.
- `lead-agent`: Anführungszeichen-Regel und `validation_failed`-Behandlung neben der Intro-Gegenprobe nach den Server-Regeln.

## 2026-10-10 – outreach 0.3.23

**outreach** (Prod: Intro an einem geraden Anführungszeichen abgeschnitten)
- `outreach-copy` → Anführungszeichen nur als deutsches Paar „…“, geschlossen immer mit “, nie mit dem geraden Zeichen ("); neue harte Zeile in der Prüftabelle. Ein gerades Zeichen hinter „ beendet im JSON den String, das Objekt bleibt gültig und der Wert kommt abgeschnitten an.
- `lead-agent` → dieselbe Regel beim Schreiben; meldet `save_lead_variables` `validation_failed: Unclosed quotation mark`, das Zitat schließen und den vollständigen Text neu speichern. Der Server lehnt solche Werte seit ListM8 vom 10.10.2026 ab.

## 2026-10-08 – outreach 0.3.22

**outreach** (Abo-Prompt aus dem Startdialog der App, MCP 2.1.0)
- `outreach-pipeline` → Abo-Lauf übernimmt eine vorgegebene Auswahl: Enthält der Auftrag einen `list_leads`-Aufruf (Listen-Modus mit `run_stages`, so kopiert ihn der Startdialog „KI-Verarbeitung starten“) oder Lead-IDs, gilt genau diese Auswahl mit den genannten Stufen. Der Aufruf läuft einmal unverändert, die Leads kommen aus `lead_ids` und werden vor dem ersten Agenten festgehalten (kein Blättern mit `offset`: bearbeitete Leads fallen aus der Auswahl). Fehlt `applied_filters`, sind Server oder Verbindung zu alt: abbrechen statt mit der Standardauswahl weiterzumachen. Keine Rückfrage nach Laufart oder Anzahl mehr, wenn die Auswahl feststeht; Fortschritt nur für die Stufen des Laufs; der Agent bekommt die Stufen im Auftrag.
- `outreach-pipeline` → Server-Lauf: `select_by_filter` kennt nur die Basisfilter, eine Auswahl mit den Listenfiltern geht über `list_leads` und `lead_ids`.
- `outreach-qualify`, `outreach-research`, `outreach-generate` → eine vorgegebene Auswahl gilt statt der Warteschlange der Phase; `outreach-generate` erwähnt den Listen-Modus bei den Parametern von `list_leads`.

## 2026-10-07 – outreach 0.3.21, datenbeschaffung 0.1.3

**outreach**, **datenbeschaffung** (ListM8: versendete Leads ohne Reaktion können erneut durch die Pipeline)
- `datenbeschaffung-referenzen` → `listm8-mcp.md`: `mark_leads_contacted` setzt mit `status="not_contacted"` nur noch kontaktierte Leads ohne Reaktion und mit beendeter Instantly-Sequenz zurück. Die übrigen bleiben unverändert und stehen je Grund in `reset_blocked`. Ein zurückgesetzter Lead bekommt beim nächsten Lauf neue Recherche und neue E-Mail und geht nur in eine andere Instantly-Kampagne.
- `outreach-launch` → Phase 6: Weg für die neue Ansprache versendeter Leads (Pop-up im KI-Lauf, per MCP Reset plus `start_lead_run`) und die Grenzen des Resets.

## 2026-10-08 – outreach Arbeitsstand 0.3.27 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Messrunde: die Reaktion im positiven Schluss wurde wörtlich aus den zwei Mustern kopiert, 7 von 17 Schlüssen „das hat mir gut gefallen“ / „das fand ich eine schöne Idee“)
- Die Reaktion kommt jetzt wörtlich aus dem Block `SCHLUSS DES OPENERS` im System-Prompt; der Server wählt je Lead eine von acht Formen über die Lead-ID (wie den Einstieg im Block `EINSTIEG DES OPENERS`). Bietet sich ein Nutzen an, bleibt der Nutzen vorn.
- Fehlt der Block (älterer Server), variiert der Agent die Reaktion selbst und übernimmt die zwei bekannten Muster nicht wörtlich.
- Angeglichen in `lead-agent` und `outreach-copy`.

## 2026-10-08 – outreach Arbeitsstand 0.3.26 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Messrunde 30 Leads Dental: ein Drittel der neuen Schlüsse urteilte über die Qualität der Arbeit und klang wie die Begutachtung durch einen Fremden)
- Positiver Schluss mit Rangfolge: 1) Nutzen oder Wirkung, wenn sie sich aus dem Detail anbietet; 2) sonst eine kurze persönliche Reaktion, die am Detail hängt und es benennt, in der Vergangenheit erzählt („das fand ich eine schöne Idee“, „hat mir gut gefallen“), nie allein und nie als feste Wendung; 3) nie ein Prüfer-Urteil über die Qualität der Arbeit („das wirkt vertrauenswürdig“, „so einen Schnitt hält man nur, wenn die Arbeit stimmt“, „da machst du vieles richtig“ u. a.).
- Inhaltsleere Formeln bleiben verboten, ergänzt um „hat man nicht alle Tage“. Abgrenzung: „finde ich stark“ ist eine Formel, die Reaktion am benannten Detail ist erlaubt.
- Angeglichen in `copy-lehre.md` (Abschnitt „Positiver Schluss“, Beispiel mit Reaktion, Prompt-Vorlage, Prüftabelle, Checkliste), `outreach-copy`, `lead-agent`, `verify-agent`, `outreach-verify`, `outreach-generate` und `beispiel-blueprint.md`. `verify-agent` nennt eine Reaktion wörtlich in `grund`, damit der Bericht dieselbe Reaktion bei mehreren Leads als systematischen Befund meldet. Gleichstand mit den Server-Regeln.

## 2026-10-08 – outreach Arbeitsstand 0.3.25 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Messrunde 30 Leads Dental: Sterne-Anker mit 9 bis 40 Bewertungen trugen nicht, sie bekamen nur Note 2 bis 3)
- Anzahl und Schnitt der Bewertungen sind als eigener Anker erst ab mindestens 30 Bewertungen UND einem Schnitt ab 4,5 erlaubt (vorher ohne Mindestanzahl, ab 4,5). Darunter gilt der nächste Anker bzw. der Fallback der Kampagne.
- Angeglichen in `copy-lehre.md` (Rangfolge, Angle 3, Prompt-Vorlage, Prüftabelle, Checkliste), `outreach-copy`, `lead-agent` (Intro-Gegenprobe und Nachbesserung), `verify-agent` (Prüfblock Opener), `outreach-verify`, `outreach-generate`, `research.md` und `beispiel-blueprint.md`. Gleichstand mit den Server-Regeln.

## 2026-10-08 – outreach Arbeitsstand 0.3.24 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Gleichstand mit den Server-Regeln zu Anrede und Zuschreibung)
- `outreach-copy`, `copy-lehre`, `outreach-verify`, `verify-agent`: Die Person wird nie mit ihr/euch angesprochen, Tatsachen über einen Betrieb mit mehreren Personen dürfen aber mit ihr/euer stehen („dass ihr nach ISO 9001 zertifiziert seid“). Firmenleistungen gehören dem Betrieb, „du hast …“ nur bei eigener Leistung, Ein-Personen-Betrieb oder Personenmarke; kein du/ihr-Wechsel im selben Satz. Verify wertet „dass ihr … habt“ nicht mehr als Fehler.
- `outreach-copy`: Anrede bei Adressen nur mit Nachnamen (instagram.leitner@) und bei weiteren allgemeinen Adressen (hello@, partnership@, business@, kooperation@ u. a.); Personenmarken und Ein-Personen-Betriebe immer mit Vornamen, auch hinter einer allgemeinen Adresse.

## 2026-10-08 – outreach Arbeitsstand 0.3.23 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Server ist die eine Quelle der Opener-Regeln)
- `lead-agent` nimmt die Regeln aus `get_lead_data` als maßgeblich: `researchGeneration.anchorRules` und `campaignFrame` für die Recherche, `emailGeneration.systemPrompt` mit dem Block `EINSTIEG DES OPENERS` für die Mail. Die Regeltexte im Plugin gelten nur noch, wenn ein älterer Server diese Felder nicht liefert.

## 2026-10-08 – outreach Arbeitsstand 0.3.22 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Copy-Beratung zu Opener und Angle-Bibliothek nach den Haiku-Läufen Dental: viele Opener nannten Standardleistungen wie Angstpatienten oder Lachgas, Anzahl und Schnitt der Bewertungen blieben ungenutzt)
- `copy-lehre.md` → neuer Abschnitt „Abhebung und Austauschtest“ als zentrale Opener-Regel: Abhebungs-Typen, Austauschtest (passt der Satz auf zehn andere Betriebe derselben Branche in der Stadt, ist er kein Aufhänger; ein Nutzen rettet keine Standardleistung), Gegensatzpaare aus Dental und Handwerk, positiver Schluss mit Leitplanken, Rangfolge der Anker (Lob aus Bewertungstexten > abhebendes Website-Detail > Anzahl und Schnitt als eigener Anker ab 4,5 > Fallback), Einstiege nach der letzten Ziffer der Lead-ID und eine Sperrliste branchenüblicher Leistungen je Kampagne. „Anzahl und Sterne nie allein“ entfällt. Angle-Hierarchie, Prompt-Vorlage, Prüftabelle und Beispiele angeglichen; die Beispiele bestehen den Austauschtest und tragen bewusst verschiedene Schlüsse.
- `outreach-copy` → Intro-Regeln und Pflichtinhalt des `intro`-Prompts auf Austauschtest, Sperrliste, positiven Schluss, Sterne-Regel und Einstiegswechsel umgestellt; „bewährte Einstiege dürfen gleich bleiben“ entfällt. Keine ausformulierten Schlüsse als Beispiel, weil schreibende Modelle sie kopieren.
- `beispiel-blueprint.md` → Beispiel „Umgang mit Angstpatienten“ gestrichen, Sperrliste Dental in Research-Vorgaben und `intro`-Prompt, `intro`-Prompt nach der neuen Regel.
- `outreach-campaign` → Pflicht, je Kampagne eine Sperrliste aus Branche und Zielgruppe zu erzeugen und in Research-Vorgaben und `intro`-Prompt einzutragen; `research.md` mit neuer Anker-Rangfolge und Austauschtest.
- `lead-agent` → recherchiert Bewertungen zuerst über Bewertungsportale (Google Maps ist per WebFetch nicht lesbar, Import-Werte gelten als Quelle), beachtet die Sperrliste und prüft das Intro gegen Austauschtest, Sperrliste, Sterne-Regel, positiven Schluss und Einstieg; meldet `aufhänger=` als Thema des Ankers.
- `verify-agent`, `outreach-verify`, `outreach-generate`, `outreach-research` → prüfen bzw. recherchieren nach denselben Regeln; Verstoß ist `ablehnen` mit `art=text`.
- `outreach-abo-lauf` → Der Bericht meldet einen systematischen Befund, wenn mehr als ein Drittel der Leads dasselbe Anker-Thema trägt.

## 2026-10-07 – outreach Arbeitsstand 0.3.21 (unveröffentlicht, ausgeliefert mit 0.3.28)

**outreach** (Messung 07.10.: 30 Leads im Abo-Lauf, Einzel-Agents gegen Workflow)
- Neuer Skill `outreach-abo-lauf`: Der Abo-Lauf läuft in Claude Code als ein Workflow. Je Lead baut der `lead-agent` (Haiku), eine Stichprobe prüft der `verify-agent` (Sonnet), Befunde zu Text, Recherche und Adresse werden in derselben Kette nachgebessert und gegengeprüft. Die Sitzung liest nur noch das Ergebnis statt jeder Agent-Meldung; die Steuerung kostete dadurch rund 90 % weniger. Dazu Fortsetzen nach Abbruch, `nur_pruefen` für bereits generierte Leads und Ausweichwege ohne Workflow bzw. ohne Subagents.
- `outreach-pipeline` ist der gemeinsame Einstieg für Server-Lauf und Abo-Lauf: gleiche Vorprüfung, Lead- und Stufenwahl, gleicher Bericht und gleicher nächster Schritt; die Laufarten unterscheiden sich nur in Tempo (Server) und Kosten (Abo). Bei `run_not_startable`, `budget_exhausted` und `provider_exhausted` wird der Abo-Lauf als Ausweg angeboten.
- `lead-agent` läuft standardmäßig auf Haiku (vorher Sonnet) und fragt nie zurück; ein Agent hatte im Workflow statt zu arbeiten nachgefragt.
- `outreach-verify`, `outreach-qualify`, `outreach-research`, `outreach-generate` und der Einstieg `outreach` verweisen für größere Mengen auf den Workflow aus `outreach-abo-lauf`.

## 2026-10-05 – outreach 0.3.20

**outreach** (Abgleich mit dem Kurs Outbound 3.0, Lektionen 2.4 und 2.5)
- `outreach-copy` → Entry-Mail nach der Master-Formel: Lob → „Deswegen …“ → Offer → Feinheiten-Satz als eigener Absatz mit Fertigstellung („Ich bin gerade noch an den letzten Feinheiten dran, vor allem […], und werde morgen mit […] fertig.“) → CTA „Wäre es in Ordnung, wenn ich dir das zusende? Völlig unverbindlich natürlich.“ Vorher stand der Feinheiten-Satz im selben Absatz wie das Offer, die Fertigstellung fehlte und der CTA trug das „morgen“.
- `marketing-offer.md` → neue Offer-Bibliothek mit den bewährten Formulierungen je Leistung (Website, Meta Ads, CRM, Voice Agent, Automatisierung, Software-Testzugang, Lead-System, Recruiting, Chatbot, Rechnungswesen) und den Detailregeln (KI bei skeptischen Zielgruppen nicht erwähnen, System framen statt Leads schicken).
- `copy-lehre.md`, `beispiel-blueprint.md`: Beispiele und CTA an den Aufbau angeglichen.

## 2026-10-05 – outreach 0.3.19

**outreach** (freigegebener Staging-Lead mit „die Preise sind fair“ im Opener)
- `outreach-copy` → Heikles ist nie Aufhänger, auch nicht als Teil eines Bewertungslobs: Preis, „günstig“, persönliche Merkmale oder Familie von Rezensierenden, Gesundheitsdetails, negative Zitatwörter. Die Regel stand schon im Server, fehlte aber im Plugin.
- `outreach-copy` → Ein Bewertungsanker beginnt mit einem Einstieg, der die Quelle nennt („ich hab mir deine Bewertungen angeschaut, und …“), nicht mit einem nackten „jemand schreibt …“.
- `verify-agent` → prüft beides und lehnt mit `art=text` ab.

## 2026-10-05 – outreach 0.3.18

**outreach** (Agent-Reviews Runde 2; lag auf `fix/sprache-buchung-routing` und war als 0.3.11 vorgesehen, jetzt in `main`)
- `outreach-campaign` → Qualifizierung: Der Ausschlussgrund „Online-Terminbuchung schon vorhanden“ ist jetzt prüfbar formuliert (eigene Website bindet ein oder verlinkt direkt; Verzeichnisprofil allein zählt nicht). Unprüfbare Zusätze wie „bei sonst modernem Auftritt“ entfallen; im Testfeld wurde der Grund dadurch je Lead gegensätzlich ausgelegt.
- `outreach-campaign` → Qualifizierung: Neue Regel zur Sprache. Bei deutscher Mail und Schweizer Leads gehört „Website ausschließlich französisch- oder italienischsprachig“ in die Ausschlussgründe; „DACH“ allein schließt die Westschweiz nicht aus.
- `routing-baustein.md`: Vermerkt die Recherche „Routing nicht sinnvoll“, gilt Fall C.
- `beispiel-blueprint.md` an beide Regeln angeglichen.

## 2026-10-05 – outreach 0.3.17

**outreach** (Gegenprüfung nach dem Nachbessern auf drei Staging-Kampagnen)
- `outreach-copy`, `verify-agent` → Zuschreibung einheitlich mit den Server-Regeln: Lob für eine andere Person ist erlaubt, wenn das Intro sie beim Namen nennt. Ein Fehler ist es, wenn es der angeschriebenen Person gilt oder eine Bewertung jemanden ohne Namen meint („die Zahnärztin“), obwohl der Betrieb mehrere hat; dann gilt das Lob dem Betrieb („in deiner Praxis“). Der `verify-agent` hatte vorher auch namentlich genanntes Lob abgelehnt.
- `lead-agent` → Nachbessern bei schwacher Recherche: Meldet die Recherche „kein starker Anker“, liest er erst die Bewertungsquellen selbst und sucht ein konkretes Lob (zwei Bewertungen oder eine aktuelle), bevor er den Fallback nimmt. Im Lauf hatten drei nachgebesserte Intros einen schwachen Fund zum Lob gemacht und die Gegenprüfung nicht bestanden; die Nachrecherche in den Bewertungen fand dann wärmere, belegte Anker.

## 2026-10-05 – outreach 0.3.16

**outreach** (Verify über 26 Leads auf drei Staging-Kampagnen: 18 frei, 7 Hinweise, 1 Ablehnung; sechs der acht Befunde waren ohne Nutzer behebbar)
- `outreach-verify` → neue Phase „Nachbessern“: Ablehnungen und Hinweise der Art `text`, `recherche` oder `adresse` gehen nicht mehr an den Nutzer, sondern an je einen `lead-agent` im Abo. Er schreibt eine neue Version, recherchiert die offene Frage gezielt nach oder stellt die Versandadresse auf die belegte um. Danach prüft ein neuer `verify-agent` gegen; wer schreibt, gibt nie selbst frei. Eine Runde je Lead, systematische Befunde (ab drei Leads) werden weiter an der Ursache behoben. An den Nutzer gehen nur `fit` und `recht` und was nach einer Runde offen bleibt.
- `verify-agent` → jedes Urteil nennt die Art des Befunds (`art=text|recherche|adresse|fit|recht`), bei `recherche` die offene Frage, bei `adresse` die belegte bessere Adresse.
- `lead-agent` → Auftrag „Nachbessern: art=…, Befund: …“ ändert nur die betroffenen Variablen, ergänzt die Recherche um einen Abschnitt „Nachrecherche“, ohne etwas zu streichen, und stellt die Versandadresse per `switch_primary_email` um. Neue Antwortzeilen `NACHGEBESSERT` und `UNVERÄNDERT`.

## 2026-10-04 – outreach 0.3.15

**outreach** (Verify-Lauf über 49 Leads auf 1081)
- `outreach-verify` → Standard ist eine Stichprobe von 10 Leads (neue Kampagne, nach Änderungen, vor dem ersten Export) statt einer Vollprüfung. Systematische Funde werden an der Ursache behoben und die betroffenen Leads neu generiert; Vollprüfung nur auf ausdrücklichen Wunsch. Der Rest wird nach bestandener Stichprobe nur auf Bestätigung freigegeben (App oder `approve_lead_variables` ohne Prüf-Agenten). Im Lauf kamen rund 80 % der Funde aus zwei systematischen Ursachen.
- `outreach-pipeline`, `outreach-generate`: empfehlen nach dem Generieren die Stichprobe statt einer Vollprüfung.
- `verify-agent`: Routing-Abwägungen (Fall B oder C, eine Alternative weniger) sind kein Hinweis mehr, solange der Text zum gewählten Fall passt.

## 2026-10-04 – outreach 0.3.14

**outreach**
- Band → neue Phase „Prüfung“ (`verify`): `outreach_progress(action="start", phase="verify")` meldet einen Verify-Lauf an; jeder `verify-agent` meldet sein Urteil mit `action="verdict"` (auch im Modus „nur Urteil“, der nichts schreibt), approve/reject zählen ebenfalls. Die Zeile zeigt „N geprüft · x frei · y abgelehnt · z Hinweis“.
- `verify-agent` → Versandadresse: maßgeblich ist `lead.sendingEmail` aus `get_lead_variables` (persönliche Adresse aus der Recherche), nicht die Importadresse `lead.email`. Braucht den ListM8-Server mit `sendingEmail` in `get_lead_variables`; ohne das Feld gilt weiter `lead.email`.
- `outreach-verify`: meldet die Phase „Prüfung“ an und schließt sie nach dem Bericht.

## 2026-10-04 – outreach 0.3.13

**outreach**
- Befehl `/outreach-runs` heißt jetzt `/outreach-status` (zeigt Server-Läufe, Abo-Läufe und Imports über dem Prompt; `zu`/`auf` wie bisher). Der alte Name funktioniert als Alias weiter.

## 2026-10-04 – outreach 0.3.12

**outreach** (Verify-Test auf Kampagne 1081, 19 Urteile)
- `lead-agent` → Anrede: Der `hallo`-Prompt der Kampagne entscheidet auch, wer bei einer Sammeladresse angesprochen wird. Verlangt er dort eine Team-Anrede, gilt sie, selbst wenn der Entscheider bekannt ist; die eingebaute Regel „bei info@ der Entscheider“ greift nur, wenn der Prompt nichts dazu sagt. Im Test hatten sechs Mails einen Vornamen an einer Sammeladresse, obwohl die Kampagne Team-Anrede vorgibt.
- `verify-agent`: hält die gespeicherte `bestEmail` gegen die Adress-Hinweise der Recherche (ungültig markierte Adresse → `hinweis`); bei einer offenen Abwägung nie `freigeben`, sondern `hinweis`, gleiche Fälle bekommen das gleiche Urteil.

## 2026-10-04 – outreach 0.3.11

**outreach**
- Neuer Agent `verify-agent` (Sonnet, ein Agent pro Lead): prüft die gespeicherten Variablen gegen Recherche (Faktenprüfung), Person, Kampagnenregeln, Copy und Versandhinweise und urteilt `freigeben`, `ablehnen` oder `hinweis`. Standard ist „Modus: nur Urteil“ (schreibt nichts); „Modus: entscheiden“ setzt approved bzw. rejected, `hinweis` bleibt beim Nutzer. Mit derselben ID-Prüfung wie der `lead-agent`.
- `outreach-verify`: Ablauf mit dem `verify-agent` (Kampagnenprüfung einmal vorab, erste Läufe nur Urteil); die `hallo`-Prüfung richtet sich nach dem Variablen-Prompt der Kampagne, wenn dieser eine eigene Form vorgibt.

## 2026-10-04 – outreach 0.3.10

**outreach**
- `lead-agent` → Datenprüfung: Nach `get_lead_data` prüft der Agent, dass `lead.id` und `campaign.id` seinem Auftrag entsprechen. Claude Code legt große Antworten als Datei mit Millisekunden-Zeitstempel im gemeinsamen Sitzungsordner ab; zwei parallele Agents können sich diese Datei überschreiben (im 50er-Lauf auf 1081 einmal passiert, der Agent hat es bemerkt und nichts geschrieben). Bei falscher ID ruft er erneut ab und schreibt im Zweifel nichts.
- `lead-agent` → Stufen: Ohne ausdrückliche Stufennennung laufen immer alle Stufen. Ein Hinweis zur Anrede („speichere alle drei Variablen“) hatte drei Agents dazu gebracht, die Qualifizierung zu überspringen.

## 2026-10-04 – outreach 0.3.9

**outreach** (Agent-Reviews Runde 1)
- `outreach-campaign` → Qualifizierung: Hat der Betrieb schon, was das Angebot liefert, gehört das in die Ausschlussgründe. Bei einem Angebot mit Online-Terminbuchung schließt „bereits eingebundene Online-Terminbuchung bei sonst modernem Auftritt“ aus; im Testfeld bekamen sonst fünf Betriebe mit funktionierender Buchung genau diese als Neuheit angeboten.

## 2026-10-04 – outreach 0.3.8

**outreach**
- `outreach-pipeline`, `outreach-qualify`, `outreach-research`, `outreach-generate` → Abo-Lauf: Nach dem Bericht werden die angemeldeten Phasen immer mit `outreach_progress(action="end")` geschlossen. Leads ohne Schreibaufruf (Recherche schon vorhanden und Mail wegen Fremdadresse übersprungen) hielten das Band sonst als laufend.
- `lead-agent` → Recherche: Vor Schritt 3 prüft der Agent `research.text` in `get_lead_data` (auch wenn die Antwort als Datei kommt). Steht dort schon ein Text, schreibt er weder Recherche noch `bestEmail`, `decisionMaker` oder `contactRecommendation`. Im 50er-Lauf auf Kampagne 2274 hatten zwei Agents eine vorhandene Recherche übersehen und überschrieben.

## 2026-10-04 – outreach 0.3.7

**outreach**
- Band → Abo-Lauf: Die Zeile zeigt nur noch, wie viel dieser Lauf vom 5-Stunden- und Wochenfenster verbraucht hat („verbraucht 5 h 3 % · Woche < 1 %“), nicht mehr den Stand des Kontos. Die Werte kommen in ganzen Prozent, ein Anstieg unter einem Punkt erscheint als „< 1 %“.
- `lead-agent` → Intro-Gegenprobe: Eine bloße Feststellung ohne das Besondere daran ist kein Aufhänger (dann gilt der Fallback der Kampagne), Erfolgsaussagen der Praxis über sich selbst werden nicht als Ergebnis wiedergegeben, das Intro bleibt bei etwa 30 Wörtern.

## 2026-10-04 – outreach 0.3.6

**outreach** (Kontrolllauf über 12 Testkampagnen)
- `marketing-offer.md` → Karte B: Begrenzte Plätze erzeugen Dringlichkeit nur, wenn die Plätze wirklich begrenzt sind; keine künstliche Knappheit.
- `outreach-copy` → Anrede: Der feste Text nennt den Empfänger nur mit einer Bezeichnung, die auf jeden Lead der Liste passt. Mischt die Zielgruppe Firmen und Einzelpersonen (Agenturen und Freelancer), heißt es „dein Business“ oder „für dich“ statt „deine Agentur“.
- `outreach-research`, `lead-agent`: Eine öffentlich belegte persönliche Adresse der empfohlenen Entscheidungsperson, auch Freemail, ersetzt eine allgemeine Importadresse (info@, kontakt@); die Importadresse bleibt Zweitadresse. Eine persönliche Importadresse bleibt Versandadresse.

## 2026-10-04 – outreach 0.3.5

**outreach** (Sequenz, Anrede und Adressregel nach den Entscheidungen des Inhabers)
- `outreach-copy` → Sequenz: Standard sind 4 Steps statt 5: Step 1 Entry (eigener Betreff, neuer Thread), Step 2 Erinnerung (Betreff leer, Thread von Mail 1), Step 3 neuer Winkel mit Social Proof (NEUER Thread mit eigenem kurzem Betreff, z. B. „kurzes Update“), Step 4 Abschied mit Routing-Hinweis (Betreff leer, Thread von Mail 3). `delayDays` 0/3/5/7, Wortlimits 120/50/80/60. „Dringlichkeit“ ist kein Standard-Step mehr, sondern nur ein zusätzlicher Step, wenn der Nutzer einen echten Zeit- oder Kapazitätsgrund nennt. Das ersetzt die Regel „alle Follow-up-Betreffs leer“ aus 0.3.4 und die 5-Step-Struktur. Begründung aus der Praxis: Eric Nowoslawski arbeitet mit 2 bis 3 Mails und nie alle im selben Thread, Jay mit 4 Steps und Routing, ohne künstliche Knappheit. Der Routing-Hinweis steht jetzt als fester Satz im Abschied; die Variable `routing` mit belegten Namen bleibt die Ausbaustufe (`routing-baustein.md`).
- `outreach-copy` → Anrede: Standard ist du im Singular. Ohne benennbaren Ansprechpartner lautet der Gruß „Hallo,“ und der Text bleibt im Singular („dein Team“, „dein Betrieb“). Der Team-Modus (ihr/euch, „Hallo <Firma> Team,“, „Hallo zusammen,“) entfällt in `outreach-copy`, `outreach-campaign`, `outreach-generate`, `outreach-verify`, `lead-agent` und den Beispielen. Die Sie-Form gilt nur als Wahl je Kampagne für sehr große Unternehmen, nie automatisch je Lead. Alle Beispiele in `copy-lehre.md` von „ihr/euch“ auf du umgestellt.
- `outreach-copy` → Betreff: „kurze Frage“ bleibt Standard für Step 1. Als Testmöglichkeit beim echten Versand in Instantly von Hand eine Variante B „Frage zu {{firma}}“ (braucht die Variable `firma`), nur als Hinweis, keine Pflicht.
- `outreach-research`, `lead-agent`: Gehört die Importadresse laut Recherche belegt einem Dritten (Kammer, Verband, Portal, Agentur, andere Firma) und gibt es keine eigene belegte Adresse, entsteht keine Mail; `bestEmail` bleibt leer, die Recherche vermerkt es. Eine eigene DNS- oder MX-Prüfung gibt es nicht. Der ListM8-Server setzt die Regel in der E-Mail-Stufe um.
- Gleichstand: `outreach-campaign`, `outreach-generate`, `outreach-verify`, `outreach-launch`, `marketing-offer.md`, `routing-baustein.md` und `beispiel-blueprint.md` (jetzt 4 Steps, Step 3 „kurzes Update“, Abschied mit Routing) auf Sequenz und Anrede angeglichen.
- Hinweis: Betreff in Step 3 und leere Betreffs in Step 2 und 4 setzen voraus, dass der ListM8-Server sie beim Blueprint-Import annimmt (Betreff ab Step 2 darf leer sein, Step 3 darf einen eigenen tragen).

## 2026-10-04 – outreach 0.3.4

**outreach** (Copy-SOPs nach dem Testfeld korrigiert)
- `outreach-copy`: Betreff nur in Step 1, keine Ankündigung oder Ergebnisansage („Website für …“), Standard „kurze Frage“ (Buchungssystem als Kern: „Frage zur Terminbuchung“). Firmenname im Betreff nur über `{{ai.firma}}`, nie über das rohe `{{lead.company}}`; ohne `firma` „kurze Frage“. Follow-ups (Step 2-5) haben keinen Betreff und laufen im Thread. Betreff-Beispiele in `SKILL.md`, `copy-lehre.md`, `marketing-offer.md` und `beispiel-blueprint.md` angeglichen (Karte C hatte zwei verschiedene Betreffs).
- `outreach-copy`: Opener. Einstiegsrahmen wie „ich hab mir … angeschaut“ sind erlaubt (Widerspruch zu „nie über den Absender“ aufgelöst); eine bloße Feststellung („du bietest X an“) ist kein Aufhänger, dann gilt der Fallback; Gründungsjahr mit Ereignis und Teamgröße sind keine verbotenen Selbstangaben-Zahlen.
- `outreach-campaign`: Variable `firma` kürzt die Rechtsform ohne Wortrest, macht aus einer Domain die Marke, übernimmt einen neueren Namen aus Impressum oder Recherche, nimmt bei langen Namen den Markenkern und schreibt Versalien normal (Abkürzungen bis 4 Buchstaben bleiben). Neu: abgeleitete oder geklonte Kampagnen gegen das neue Offer prüfen (kein Offer-Rest im Prompt).
- `outreach-campaign` → Qualifizierung: Ausschlussgründe nur, was ein Agent öffentlich prüfen kann (nie Kontaktsperre oder Bestandskunde); Konzern (fremde Muttergesellschaft, Franchise, Börse) und Größenschwelle als getrennte Punkte; Nachbarbetriebe der Branche ausdrücklich ausschließen; kein Ausschlussgrund schließt den Bedarf aus, den das Angebot löst; „Selbstzahlerleistung erkennbar“ ist ein Fit-Kriterium; keine Adress- oder Pipeline-Anweisungen im `additional_prompt`.
- Hinweis: Leere Betreffs in Step 2-5 setzen voraus, dass der ListM8-Server sie beim Blueprint-Import annimmt.

## 2026-10-04 – outreach 0.3.3

**outreach** (Live-Ansicht in Claude Code)
- Abo-Lauf im Band zeigt den Stand beider Abo-Fenster („5 h 12 % · Woche 43 %“) und die Zunahme seit Laufbeginn, sobald sie messbar ist (ab 0,1 Punkten). Vorher stand dort nur die Zunahme der Woche, die bei kleinen Läufen immer „+0,0 %“ zeigte. Die Fenster zählen das ganze Konto, parallel laufende Sitzungen erscheinen mit.

## 2026-10-04 – outreach 0.3.2

**outreach** (Live-Ansicht in Claude Code)
- Band fragt laufende Server-Läufe mit EINEM `list_lead_runs` je Server und Runde ab statt einem `get_lead_run_status` je Lauf; einzeln nur, wer in der Liste fehlt. Abfrage alle 20 statt 10 Sekunden.
- Antwortet ein ausgelasteter Server nur noch über eine Hintergrundaufgabe (der Mod sieht dann keinen Status), hört das Band nach drei Runden ohne verwertbare Antwort auf, den Lauf abzufragen, und zeigt „Stand unbekannt“; `/outreach-runs` lädt neu. Vorher fragte es fertige Läufe endlos weiter ab, und jede Antwort landete als Meldung im Chat.

## 2026-10-04 – outreach 0.3.1

**outreach** (Live-Ansicht in Claude Code)
- `/outreach-runs zu` klappt das Band auf eine Zeile ein („Outreach · 13 Läufe · 4 laufen · eingeklappt“), `/outreach-runs auf` bzw. `/outreach-runs` klappt es wieder auf und lädt die laufenden Läufe neu. Das Abfragen läuft im eingeklappten Zustand weiter. Daneben bleibt das Einklappen von Claude Code selbst (`[−]`, Strg+X Strg+A).

## 2026-10-04 – outreach 0.3.0

**outreach** (Abo-Lauf vereinfacht: ein Agent je Lead für alle Stufen)
- Neuer Plugin-Agent `outreach:lead-agent` (Sonnet, alle Werkzeuge): qualifiziert, hört bei `not_qualified` auf, recherchiert (vorhandene Recherche wird genutzt) und schreibt die Mail-Variablen – `get_lead_data` wird je Lead nur einmal gelesen, die Mail entsteht mit dem, was der Agent selbst über den Lead gelernt hat. Lädt den Copy-Skill selbst; nennt der Auftrag einen Server, nutzt er nur dessen Werkzeuge.
- Entfernt: die Agenten `qualifier`, `researcher`, `writer` und die schlanken Mod-Agenten (`*-schlank`). Ihre Werkzeug-Einschränkung führte zu Abbrüchen (große `get_lead_data`-Antwort als Datei ohne Read, Werkzeugnamen je nach Servername).
- `outreach-pipeline`: Abschnitt „Abo-Lauf“ – Leads wählen, Fortschritt anmelden, je Lead ein `lead-agent` (höchstens 10 gleichzeitig), Bericht aus den Antwortzeilen statt erneuter Lead-Liste. `outreach`: leitet „Abo-Lauf“, „im Abo“, „ohne Server“ an `outreach-pipeline --abo` weiter.
- `outreach-qualify`, `outreach-research`, `outreach-generate`: einzelne Stufe im Abo über `lead-agent` mit „nur <Stufe>“.
- Band: ein Abo-Lauf ist EINE Zeile („5 Leads · 3 fertig · 1 aussortiert · Qual 5/5 · Rech 4/4 · Mail 3/4 · im Abo“); eine schon vorhandene Recherche zählt als erledigt, sobald die Mail des Leads gespeichert ist.

## 2026-10-04 – outreach 0.2.1

**outreach**
- `outreach-pipeline`: Abo-Lauf ist direkt aufrufbar (`/outreach-pipeline 80 --abo`, „im Abo“, „ohne Server“) und steht in der Aufruf-Tabelle; ohne Angabe fragt der Skill, ob Server- oder Abo-Lauf.

## 2026-10-04 – outreach 0.2.0

**outreach** (Abo-Läufe: Leads im Claude- bzw. ChatGPT-Abo statt auf dem Server verarbeiten)
- Neue Plugin-Agenten `qualifier`, `researcher`, `writer` (Sonnet, ein Lead pro Agent) – laufen überall, auch in Cowork.
- In Claude Code meldet der Mod zusätzlich schlanke Varianten `qualifier-schlank`, `researcher-schlank`, `writer-schlank` an: nur die Outreach-Werkzeuge des verbundenen Servers (unter dem Namen, den der Kunde vergeben hat), Sonnet. Gemessen: weniger als halb so viel Kontext je Lead wie ein allgemeiner Agent.
- `outreach-qualify`, `outreach-research`, `outreach-generate`: Abschnitt „Abo-Lauf“ – ein Lead pro Agent (keine Sammel-Agenten, sonst Verwechslungen), Agent-Wahl schlank → Plugin-Agent → `general-purpose` mit Sonnet, höchstens 10 gleichzeitig, Anmeldung im Band über `outreach_progress`. Generate: der Orchestrator hängt die Copy-Regeln an, Subagents laden den Skill nicht selbst.
- `outreach-pipeline` (Manuell-Modus): Kette je Lead (Qualifizierung → Recherche → Mail) als Workflow in Claude Code, sonst Phasen nacheinander.
- Band: Abo-Phasen heißen „im Abo“; als nicht qualifiziert beurteilte Leads gelten in Recherche und Mail als aussortiert („4 fertig · 1 aussortiert“, grün); alle drei Phasen eines Laufs bleiben sichtbar; „Öffnen“ führt in die App des Servers, der geschrieben hat (vorher teils falsche Domain); Verbrauch am Wochen-Kontingent des Abos seit Phasenstart („+2,4 % Woche“).

## 2026-10-04 – outreach 0.1.9

**outreach**
- `outreach-copy`: Musterbeispiele in Skill und `marketing-offer.md` auf die Du-Form umgestellt (vorher „für euch erstellt“, „euch das morgen zusende“ – Agenten übernahmen daraus die Ihr-Form).
- `outreach-copy`: Das erste Wort nach `{{ai.hallo}}` schreibt man in jedem Step klein („du hast sicher …“).

## 2026-10-04 – outreach 0.1.8

**outreach**
- `outreach-copy` (Ansprache): `du` an den Ansprechpartner ist ausdrücklich der Standard, auch für Praxen, Finanz und generische Adressen. `team` und `sie` nur auf ausdrücklichen Wunsch – nicht, weil eine alte Vorlage oder Bestandskampagne so schreibt. Mischform „Hallo Max,“ vor „euch“ als Fehler benannt.

## 2026-10-04 – outreach 0.1.7

**outreach**
- Neuer Baustein Routing-Follow-up („bin ich bei dir richtig oder eher bei Anna oder Tom?“): `outreach-copy/references/routing-baustein.md` mit Einsatzfällen, Platz in der Sequenz (Step 4 statt „Dringlichkeit“), Recherche-Ziel, Prompt-Vorlage der Variable `routing` (Fälle mit Namen, Team, Solo) und Erfahrungswerten. `outreach-copy` und `outreach-campaign` verweisen darauf und bieten ihn bei Zielgruppen mit Teams an.

## 2026-10-04 – outreach 0.1.6, datenbeschaffung 0.1.2

**outreach**
- `outreach-import`: Job-Ergebnis richtig beschrieben – `duplicates`, `internalDuplicates`, `do_not_contact_hits` und `errors` sind Listen, berichtet wird ihre Anzahl; `consolidated` erklärt. Import meldet keinen Prozentwert, nur den Status.
- `outreach-import`: realistische Paketgröße im Chat (etwa 100–300 Leads je Aufruf, jeder Lead kostet Kontext); bei mehreren Tausend Zeilen den CSV-Import der App empfehlen und hier nur vorbereiten.

**datenbeschaffung**
- Übergabe an Outreach (`outreach-uebergabe.md`, `listm8-mcp.md`, `listen-qualitaet`): dieselbe Korrektur der Job-Ergebnis-Felder.

## 2026-10-04 – outreach 0.1.5

**outreach** (Live-Ansicht in Claude Code)
- Import-Ergebnis zählt Duplikate wieder: Der Server liefert sie als Liste der betroffenen Zeilen, nicht als Zahl; vorher fiel die Angabe weg.

## 2026-10-04 – outreach 0.1.4

**outreach** (Live-Ansicht in Claude Code)
- Import im Chat als eine Zeile ohne Fortschrittsbalken („Import gestartet · 500 Leads · Fortschritt über dem Prompt“); mehrere auf einmal gestartete Importe werden zu einer Zeile zusammengefasst. Der alte Balken blieb bei 0 %, weil der Import keinen Prozentwert meldet.
- Der Fortschritt steht jetzt im Band über dem Prompt: Status „wartet“/„läuft“ (Prozent nur, wenn der Server einen meldet), danach Ergebnis mit importierten Leads und Duplikaten oder der Fehlergrund; bei Abschluss ein Hinweis. Das Band fragt `get_job_status` alle 10 s, nur solange ein Import läuft.
- `get_job_status` zu anderen Job-Arten (z. B. Recherche) wird nicht als Import gezeigt.

## 2026-10-04 – outreach 0.1.3

**outreach**
- `outreach-copy` (Anrede): Du-Form grüßt mit „Hallo Vorname,“ der Person, der die Versandadresse gehört; bei generischen Adressen (info@, kontakt@ …) mit dem Vornamen des Entscheiders aus der Recherche; ohne klar erkennbare Person nur „Hallo,“ (nie „Hallo zusammen,“ vor du-Text). Sie-Form analog, Fallback „Guten Tag,“.
- `outreach-copy` (Opener): Lob oder anerkennende Beobachtung, getragen von einem konkreten Detail. Bewertungsanker ist eine Paraphrase des Lobs, Anzahl und Sterne nie allein und nie als erste Worte; Stellenanzeige als Erkenntnis über den Betrieb statt „ihr sucht“; zweiter Satz konkret und ohne Vorwegnahme des festen Texts; Fallback ohne unbelegte Behauptung; keine Zuschreibung fremder Leistungen an die angeschriebene Person.
- Beispiele ohne „finde ich spannend“ und Zahl-zuerst-Bewertungsopener; die Aussage „AI-Personalisierung verdoppelt bis verdreifacht die Reply Rate“ ist als Erfahrungswert mit Empfehlung zur Kontrollgruppe formuliert.
- `outreach-copy` (Anrede): Bei mehreren gleichrangigen Inhabern oder Geschäftsführern gilt der empfohlene Ansprechpartner, sonst die erstgenannte Person im Impressum.
- `outreach-copy` (Opener): Ohne Kundenlob sind Projekt/Referenz/Spezialisierung mit einem Detail, Firmengeschichte, Auszeichnungen (ohne Altersgrenze) sowie Lage und Ausstattung erlaubt; ohne konkreten Aufhänger steht der Fallback-Satz statt einer Leistungsliste; Substantive bleiben am Anfang groß.
- `outreach-campaign` (Research-Fokus), `outreach-generate` und `outreach-verify` an die neuen Regeln angepasst.

## 2026-10-04 – datenbeschaffung 0.1.1, outreach 0.1.2

**datenbeschaffung**
- Neu: `datenbeschaffung-setup` (Outreach-Verbindung, Apify-Zugang mit kostenlosem Selbsttest, optional Outscraper, alte Kopien aufräumen) und `datenbeschaffung-update`.

**outreach**
- `outreach-setup` verweist nach der Installation der Datenbeschaffung auf `datenbeschaffung-setup`.

## 0.1.1 – 2026-10-04

**outreach**
- Skills wiederholen Lead-Listen nicht mehr als Tabelle, wenn die Live-Ansicht in Claude Code sie schon als Karte zeigt.

## 0.1.0 – 2026-10-03

Erste Fassung als Marketplace `outreach-plugins` (vorher Skills-Repo `listm8-skills`).

**outreach**
- Plugin mit allen Outreach-Skills, MCP-Verbindung `akquise` (`outreach.akquise.de`) und
  Live-Ansicht für Claude Code (Lead-Vorschau, Band mit laufenden Lead-Runs, `/outreach-runs`).
- Neu: `outreach` (Einstieg), `outreach-setup` (Einrichtung, Aufräumen alter Kopien),
  `outreach-update`.
- `outreach-copy`: Cold-Mail-Copy-Regeln aus der Cold-Mailing-SOP; `outreach-launch`:
  Versand-Vorbereitung und Optimierung.
- Skills passen zum MCP mit 32 Tools; kein Scraping über den MCP, kein Probelauf.

**datenbeschaffung**
- Plugin mit dem Einstieg `datenbeschaffung`, allen Beschaffungswegen (Apify/Outscraper im
  eigenen Konto), Anreicherung, Listen-Qualität und den geteilten Referenzen.
