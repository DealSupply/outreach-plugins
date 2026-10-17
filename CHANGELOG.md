# Changelog

## 2026-10-16 – outreach 0.4.0, datenbeschaffung 0.5.0

Leads ohne E-Mail-Adresse (ListM8 MCP 3.0.0). Ein Lead braucht beim Import eine gültige E-Mail oder eine eigene Website; die Recherche sucht die Kontaktadresse dann selbst. Alles Neue gilt erst ab Server-Version 3.0.0 (`ping`); ältere Server behalten den alten Ablauf, jeder Lead braucht dort eine E-Mail.

**outreach**
- `outreach-import` → Prüft zuerst die Server-Version; nur sie entscheidet über den Kontrakt, nicht der Wortlaut einer Fehlermeldung. Ab 3.0.0 reicht E-Mail ODER eigene Website (Baukasten-Unterseiten wie `name.jimdosite.com` zählen, reine Profil- oder Plattform-Links nicht). Ungültige E-Mail mit brauchbarer Website wird ohne Adresse importiert. Teilimport statt Komplett-Ablehnung: `accepted`, `rejected_total`, `rejected_rows` mit Codes (`missing_contact`, `invalid_email`, `platform_only_website` usw.); `validation_failed` nur, wenn nichts importierbar ist; `limit_reached` ist dort ein Fehler für den ganzen Aufruf und nur im Job-Ergebnis ein Zeilencode. Bericht nennt Abgelehnte, Hinweise und Duplikate nach `matchedVia` (E-Mail oder Domain).
- `outreach-research`, `lead-agent` → Ein Lead ohne Adresse bekommt als erstes Ziel die eigene Kontaktadresse (Regeln aus `researchGeneration.contactEmail`): persönliche Adresse von Inhaber oder Geschäftsführung vor info@, nie geraten, nie Plattform-, Verzeichnis-, Agentur- oder Kammeradressen. Fund als `bestEmail` schreiben (der Server macht sie zur Identität; `address_conflict` nicht wiederholen). Kein Fund: Recherche mit Abschnitt „## Kontakt“ und den geprüften Seiten speichern, der Lead scheidet mit `no_contact_email` aus und bekommt keine Mail-Variablen. Antwortzeile mit `adresse=` bzw. `grund=keine-adresse`. Ein Lead mit `not_found` bekommt im Abo-Lauf trotzdem sein Qualifizierungsurteil, sonst bliebe er in der Warteschlange.
- `outreach-generate`, `outreach-verify`, `verify-agent` → `no_contact_email` beim Speichern oder Freigeben ist kein Fehler, nicht wiederholen. Versandadresse ist `sendingEmail`, sonst `email`; ein Lead ohne beide wird nie freigegeben.
- `outreach-pipeline`, `outreach-abo-lauf` → Bericht zählt „ohne Adresse“ aus den `skipReasons` des Laufs bzw. den Antwortzeilen der Agents.
- `outreach-lists`, `outreach-launch` → Leads ohne E-Mail: im Dedup-Index ist `e` leer (nur über `d` bekannt), `check_leads_exist` findet sie nur über die Domain (Abgleich nach ganzen Labels; `match_kind: website_identity` = derselbe Lead, `company_known` = Firma bekannt; ohne `match_kind` eigener Host-Vergleich), `mark_leads_contacted` erreicht sie nur über `lead_ids`; Export und Push nehmen nie Leads ohne Versandadresse mit.
- `outreach-setup` → nennt die Server-Version und was ab 3.0.0 gilt. `outreach-campaign` (Recherche-Referenz) → Hinweis, dass die Regeln zur Kontaktadresse vom Server kommen.
- Live-Ansicht → Import zeigt abgelehnte Zeilen („470 importiert · 3 abgelehnt“); ein Lead, dessen Recherche keine Adresse fand, verlässt im Abo-Lauf die Mail-Phase; Leads ohne E-Mail erscheinen mit ihrer Website bzw. Versandadresse; ein kombinierter Schreibaufruf (Urteil plus Recherche) zählt beide Phasen. 4 neue Tests.

**datenbeschaffung**
- `build_csv.py` → `--uebergabe kontakt` (E-Mail oder eigene Website, Standard für ListM8 ab 3.0.0) und `--uebergabe email` (alter Vertrag, `--require-email` bleibt als Alias); verworfene Zeilen mit Grund per `--verworfen` in eine eigene CSV; Hinweis `nur-plattform-url`; CSV als Eingabe, ein zweiter Durchlauf behält Inhaber, Zusatzspalten und frühere Hinweise. Neue Referenz `plattform-hosts.md` (Spiegel der Server-Liste: Profil-Plattformen, Marken mit Länderdomains, Baukästen).
- `dedup.py` → Index-Zeilen ohne Adresse zählen über ihre Domain; Zeilen ohne E-Mail auf bekanntem Host fallen als derselbe Lead weg; Domains nach ganzen Labels wie `check_leads_exist` (ohne `www.`, Umlaut-Domains als Punycode, keine Teilstring-Treffer; derselbe Lead nur bei exakt gleichem Host, Eltern-Domain nur Warnung); `--drop-known-domains-ohne-email`. 9 neue Tests.
- `datenbeschaffung`, `listen-qualitaet`, alle Wege, `impressum-enrichment`, `kontaktseiten-fallback`, `enrichment-waterfall`, `outscraper-bulk` → Die Kontaktlücke: vorab anreichern oder der ListM8-Recherche überlassen (Kosten- und Entscheidungstabelle in `datenumfang.md`); Anreicherung ist ab 3.0.0 optional. Bei ungültiger Adresse aus der Verifizierung bleibt die Zeile mit Website erhalten (Adresse raus, Hinweis `adresse-verworfen`).
- `listm8-mcp.md`, `csv-spalten.md`, `outreach-uebergabe.md`, `listen-und-icp.md`, `erfahrungswerte.md` → neuer Import-Vertrag, Antwortfelder, Dedup über die Website, Platzhalter für die Fundquote der Recherche.

## 2026-10-15 – outreach 0.3.32

**outreach** (Kundenfall 15.10.2026: Claude lehnte eine Prompt-Änderung über den MCP ab)
- `outreach-campaign` → Einen Variablen-Prompt ändert `update_ai_variable` (ListM8-MCP 2.4.0) ohne Export und Voll-Blueprint. Die Warnung, `edit_campaign` lösche alle erzeugten Werte, ist ersetzt: Der Server gleicht Variablen seit August 2026 per Name ab, Werte bleiben. Rückfrage bleibt Pflicht, bevor schon erzeugte Leads neu generiert werden.
- `outreach-launch`, `outreach-generate`, `outreach-verify`, `outreach-copy` (Copy-Lehre) → nennen `update_ai_variable` für Prompt-Änderungen und korrigieren dieselbe Löschwarnung.

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
