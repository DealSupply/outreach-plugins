---
name: demo-leadliste
description: Baut für einen Lead, der Neukunden braucht (Agentur, Berater, Dienstleister, Handwerk), ein kleines Lead-System, das schon 30–50 passende Wunschkunden gefunden hat, als Türöffner „habe dir ein System eingerichtet, das schon … passende Kunden gefunden hat“. Verwenden bei „Demo-Leadliste“, „Lead-System als Demo“, „passende Kunden für … finden“, „Leadliste für den Lead“ oder wenn das Offer der Kampagne ein Outreach- oder Lead-System ist. Nutzt das Plugin datenbeschaffung im Geschenk-Modus.
---

# Demo-Leadliste

Dem Lead zeigen, dass ein System für ihn passende Kunden findet, mit einer kleinen, sauberen
Liste als Beweis und einem Satz je Firma, warum sie passt. Gerahmt wird **das System**, nicht
„ich schicke dir Leads“ (Regel aus `outreach-copy`, `references/marketing-offer.md`).

Wissen: `../fulfillment-referenzen/references/recht-und-grenzen.md` (nur Firmendaten),
`../fulfillment-referenzen/references/qualitaet.md`. Beschaffung: Plugin **datenbeschaffung**
(Einstieg `datenbeschaffung`).

## Geschenk-Modus der Datenbeschaffung

Die Liste ist ein Geschenk an den Lead, kein Bestand des Nutzers. Gegenüber dem normalen Ablauf
von `datenbeschaffung` gilt:

| Schritt in `datenbeschaffung` | Im Geschenk-Modus |
|---|---|
| Phase 1: ICP mit Rolle, Branche, Größe, Region, Trigger, Anti-ICP | **gilt**, für die Kunden des Leads |
| Phase 2: Weg wählen | **gilt** |
| Phase 2b: Datenumfang | **gilt**, nur Firmendaten (siehe unten) |
| Phase 3: Abgleich mit dem eigenen Bestand | **entfällt** (es sind nicht die Leads des Nutzers) |
| Phase 4: Kosten nennen, **harter Deckel**, Freigabe | **gilt**: Pilot mit höchstens 50 Treffern, Deckel 2 $ |
| Phase 5: `listen-qualitaet`, Verifizierung, Import | **entfällt**: kein Import in die App des Nutzers, keine Kampagne, keine E-Mail-Verifizierung |

Die Datenbeschaffung endet hier ausnahmsweise bei der bereinigten CSV. **Nie** per `import_leads`
in das Konto des Nutzers laden und **nie** einer Kampagne zuordnen.

## Ablauf

### 1. Wunschkunde des Leads bestimmen (5 Min.)

Aus der Website des Leads: Wem verkauft er? Referenzen, Branchenseiten, Fallstudien, Leistungen.
ICP-Satz nach dem Muster aus `datenbeschaffung` bestätigen lassen:
„[Rolle] in [Branche] mit [Größe] in [Region], erkennbar an [Trigger]. Nicht: [Anti-ICP].“

### 2. Beschaffen (15 Min., kleiner Pilot)

`datenbeschaffung` im Geschenk-Modus (Tabelle oben) fahren. Kosten nennen, Deckel 2 $ setzen,
ausdrückliche Freigabe abwarten; die Kosten fallen im Apify-Konto des Nutzers an. Ist das Plugin
nicht installiert: auf `fulfillment-setup` verweisen oder nach Rücksprache 20–30 Firmen per Websuche
von Hand zusammenstellen.

### 3. Bereinigen und begründen (10 Min.)

- Nur Firmendaten: Firma, Website, Ort, allgemeine Kontaktadresse (info@, kontakt@) bzw. Telefon aus
  dem Impressum, Google-Bewertung falls vorhanden. **Keine Namen von Privatpersonen, keine
  persönlichen Adressen, keine Mobilnummern.**
- Je Firma eine Spalte „Warum passend“ mit einem belegten Merkmal (z. B. „Website von 2016, keine
  Online-Buchung“, „wächst: 3 offene Stellen“). Positiv und sachlich formulieren.
- Dubletten und unpassende Firmen entfernen. Lieber 30 gute als 50 gemischte.
- Den Lead selbst und seine bekannten Kunden (Referenzseite) aus der Liste nehmen.

### 4. Darstellen

Eine Seite (HTML, schlicht, Grundlage `../fulfillment-referenzen/references/webseiten-bauplan.md`):

1. „So findet ein Lead-System passende Kunden für [Lead]“, Entwurfs-Hinweis von [Absender]
2. Der Wunschkunde (ICP-Satz) und woran das System ihn erkennt
3. Ergebnis des ersten Laufs: Anzahl gefunden, Region, Datum
4. Die ersten 10 Einträge als Vorschau mit „Warum passend“
5. Was als Nächstes möglich wäre (mehr Regionen, laufende Suche), nur nach Angaben des Nutzers

Die vollständige Liste (CSV) **nicht** öffentlich mitveröffentlichen; sie geht nach der Antwort per
Mail an den Lead. Hinweis zur Nutzung: „nur Firmen, öffentlich erreichbare Kontakte; Ansprache nach
den geltenden Regeln für Werbung“.

### 5. Prüfen und ausliefern

`qualitaet.md` (harte Punkte) und Stichprobe von 5 Einträgen gegen die Websites, dann
`demo-ausliefern`.
