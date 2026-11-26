# Ohne DealSupply: der ganze Weg bis zur Datei für Instantly

> Stand 26.11.2026. Für alle, die das Plugin „datenbeschaffung“ ohne DealSupply-Konto nutzen (zum
> Beispiel aus einem Kurs) oder ihre Liste direkt in Instantly laden wollen. Quellen: Kurshandbuch
> „Datenbeschaffung“ (Stand 19.08.2026), Kapitel 2, 6, 9 und 10 und FAQ; Hilfe von Instantly
> (gelesen am 26.11.2026: CSV-Import, Variablen, Blocklist). Mit DealSupply bleibt der bisherige
> Weg unverändert (`datenumfang.md`, `outreach-uebergabe.md`).

## Welcher Modus gilt

| Lage | Modus | Ende des Laufs |
|---|---|---|
| DealSupply-MCP verbunden (`ping` antwortet) | **mit DealSupply** | Import per `import_leads` |
| DealSupply-Konto, aber keine Verbindung | **mit DealSupply**, Übergabe über die Oberfläche | CSV-Import in der App (`outreach-uebergabe.md`, „CSV-Fallback“) |
| Kein DealSupply-Konto | **ohne DealSupply** | Datei für Instantly (dieses Dokument) |

Ist unklar, ob ein Konto da ist, einmal fragen: „Nutzt du DealSupply, oder soll die Liste direkt
in Instantly (oder ein anderes Versandtool)?“ Auch mit DealSupply-Konto darf der Nutzer die
Instantly-Datei wählen; dann gelten die Regeln hier, und der Bestandsabgleich aus DealSupply läuft
trotzdem vorher, wenn die Verbindung steht.

## Was du ohne DealSupply brauchst

| Was | Warum |
|---|---|
| Einen bezahlten Claude-Tarif (Plugins gibt es nur dort) oder Codex bzw. ChatGPT Desktop | Das Plugin läuft in deiner KI. Für die Skripte braucht die Umgebung Python: Claude Code und Codex haben es, die Claude-App nur mit eingeschalteter Code-Ausführung. Der alte Kurs empfahl Claude Pro, weil der kostenlose Tarif bei langen Läufen abbricht (Kap. 6). |
| Ein eigenes Apify-Konto, **nicht im kostenlosen Plan** | Fast alle Wege laufen dort. Im kostenlosen Plan kostet das Prüfen der Adressen ein Vielfaches (Preisfalle, `kosten.md`). |
| Instantly (oder ein anderes Versandtool) | Dorthin geht die fertige Datei. |
| Einen Export aus deinem CRM | Für die Sperrliste (Bestandskunden, Ex-Kunden, Abmeldungen). |

Das Plugin `outreach` ist dafür nicht nötig; es bringt nur die Verbindung zu DealSupply.

## Was ohne DealSupply wegfällt und was es ersetzt

| Mit DealSupply | Ohne DealSupply |
|---|---|
| Fehlt die Adresse, sucht die Recherche sie auf der Website. | **Jede Zeile braucht vor der Übergabe eine Adresse.** `impressum-enrichment` ist Pflicht für alle Domains ohne Adresse (DACH), `kontaktseiten-fallback` für Seiten ohne Impressum und außerhalb DACH. Unter 20 Domains liest die KI das Impressum selbst, kostenlos. Übergabe immer mit `build_csv.py --uebergabe email`. |
| Die Recherche findet den Ansprechpartner. | Der Geschäftsführer oder Inhaber kommt aus dem Impressum: `impressum-enrichment` übernimmt ihn, die Maps-Kontaktanreicherung liefert ihn als `inhaber`. `instantly_csv.py` macht daraus Vorname und Nachname, wo der Name eindeutig ist. |
| Die Qualifizierung in der App sortiert Beifang aus. | Es gibt keine Qualifizierung. Pilot und 20er-Stichprobe (`listen-qualitaet`, Schritt 4) sind die einzigen Prüfungen, ob ein Lead passt. Deshalb den Anti-ICP schon in Query und Filter streng setzen. |
| Bestandsabgleich mit `export_leads` und `do_not_contact`. | Sperrliste aus dem eigenen CRM (`sperrliste.py`) und die Blocklist in Instantly. |
| Import in die App, die Recherche liefert Stoff für jede Mail. | Datei für Instantly (`instantly_csv.py`). Persönlich wird die Mail nur mit dem, was die Liste mitbringt (`personalisierung.md`). |

Ehrlich sagen, was das kostet: Ohne Recherche bleiben Leads ohne Adresse ohne Adresse. Bei Google
Maps fanden drei Impressum- und Kontakt-Actors für 28 Domains ohne Adresse nur 1 bis 5 Adressen
(`datenumfang.md`); diese Leads fallen dann aus der Liste.

## Ablauf

1. `datenbeschaffung-setup`: Apify verbinden, Preisstufe prüfen (nicht der kostenlose Plan).
2. ICP-Satz und Anti-ICP (`icp.md`).
3. **Sperrliste zuerst** (unten): bekannte Domains kosten sonst beim Anreichern Geld.
4. Weg wählen, Kosten nennen, Freigabe, Pilot, Lauf (Einstieg `datenbeschaffung`).
5. Kontaktlücke schließen: `impressum-enrichment`, danach `kontaktseiten-fallback` für den Rest.
6. `listen-qualitaet`: Format, Sperrliste, Prüfung der Adressen, 20er-Stichprobe, Datei für Instantly.
7. In Instantly: erst die Blocklist importieren, dann die Leads (unten).

## Sperrliste aus dem eigenen CRM (Kurshandbuch Kap. 9)

Gegen drei Quellen wird jede Liste abgeglichen: Kunden und kürzlich beendete Kundenbeziehungen aus
dem CRM, die eigene Blacklist (Ex-Kunden, Beschwerden, Abmeldungen) und, je nach Geschäft,
Wettbewerber.

**Handarbeit:** Den Export zieht der Nutzer selbst, die KI kommt nicht in sein CRM. Beispiel Close
(Kap. 9): Leads → Filter „is any of“ Kunde, Ex-Kunde, Blacklist → oben rechts die drei Punkte →
Export als CSV. Jedes andere CRM geht genauso, solange die Datei eine Spalte mit Website oder
E-Mail hat.

```
python3 ../datenbeschaffung-referenzen/scripts/sperrliste.py --crm kunden.csv [--crm abmeldungen.csv] \
  [--zusatz "wettbewerber.de,wettbewerber2.de"] --blocklist instantly-blocklist.csv \
  --in leads.csv --out leads-ohne-sperre.csv
```

- Firmenadressen werden zur **Domain** (sperrt die ganze Firma), private Postfächer (gmail.com,
  gmx.de …) bleiben einzelne Adressen (Kap. 9: „Domain immer, wenn eine Firmenadresse da ist“).
- `--in/--out` nimmt gesperrte Zeilen aus der eigenen Liste, auch Subdomains der gesperrten Firma.
- Vor dem bezahlten Anreichern laufen lassen, die Domains zusätzlich in die Query-Ausschlüsse geben.
- Die Abmeldungen und Beschwerden aus Instantly beim nächsten Lauf als weiteren Export mitgeben.

## Die Datei für Instantly

```
python3 ../datenbeschaffung-referenzen/scripts/instantly_csv.py --in leads-final.csv \
  --out instantly-<nische>-<datum>.csv
```

Das Skript hält die Regeln von Instantly ein (UTF-8, E-Mail Pflicht, Spaltennamen mit
Großbuchstaben vorn, höchstens 20 Zeichen, keine Sonderzeichen, keine Wahrheitswerte) und nennt
die Zuordnung für den Import. Die Kernspalten heißen wie die festen Felder von Instantly (`Email`,
`FirstName`, `LastName`, `CompanyName`, `Website`, `Phone`, `JobTitle`, `LinkedIn`); alles andere mit
Einstieg wird eine eigene Variable (`Firma`, `Stadt`, `Inhaber`, `GoogleBewertung`,
`Rezensionstexte`, `Plattform`, `Follower` …). Interne Spalten (`quelle`, `hinweis`, `place_id`)
bleiben in der eigenen CSV.

**Leere Vornamen:** Das Skript nennt die Zahl. Eine Mail, die mit dem Vornamen beginnt, braucht für
diese Leads eine Anrede ohne Namen; welche, regelt die Copy, nicht die Liste. Sind es viele, die
Leads ohne Vorname als eigene Datei in eine eigene Kampagne geben.

### So lädst du sie in Instantly (dem Nutzer so weitergeben)

1. **Blocklist zuerst:** Settings → Blocklist → „+ Import“ → CSV-Datei `instantly-blocklist.csv`
   hochladen und als Spalte `Blocked` wählen. Höchstens 5 MB je Datei, sonst teilen.
   **Importieren, nicht nur verlinken:** Nur so gilt die Blocklist auch für Leads, die schon in
   Kampagnen stehen (Kap. 9; ein verlinktes Google Sheet prüft Instantly nur beim Hochladen).
2. **Leads:** Kampagne öffnen → Leads hinzufügen → CSV hochladen. Instantly schlägt die
   Zuordnung vor; mit der Zeile „Zuordnung beim Import“ des Skripts vergleichen: Kernspalten auf die
   festen Felder, alle anderen als „Custom variable“. In der Mail heißen sie dann `{{Firma}}`,
   `{{Stadt}}` usw., Groß- und Kleinschreibung genau wie die Spalte.
3. **„Check for duplicates across all campaigns/lists“** angehakt lassen (Standard): Leads, die schon
   in einer anderen Kampagne stehen, kommen nicht doppelt hinein.
4. **„Verify leads“:** kostet laut Instantly 0,25 Credits je Lead. Nur eine Prüfung wählen: Sind die
   Adressen in `listen-qualitaet`, Schritt 3, schon geprüft, abwählen; sonst anhaken. Der alte Kurs
   empfahl die Prüfung in Instantly wegen der Catch-all-Erkennung (Kap. 9).

## Regeln, die ohne DealSupply genauso gelten

- Keine Liste älter als sechs Monate; bei jedem neuen Kampagnenstart frisch beschaffen oder die
  alte Liste mindestens neu prüfen (Kap. 2 und FAQ).
- Dieselben Leute erst nach 6 bis 12 Monaten wieder anschreiben (FAQ).
- Bounce unter 3 %, über 5 % gilt bei Gmail und Outlook als Spam-Signal (Kap. 2).
- Aus der Rohliste bleibt nach Sperrliste, Prüfung der Adressen und Stichprobe gut die Hälfte
  versandbereit (Kap. 9, Kaskade unten in `listen-qualitaet`). Rohmenge danach planen.
