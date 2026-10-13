---
name: demo-akquise-kampagne
description: "Baut eine fertige, hochpersonalisierte Muster-Akquise-Kampagne für einen Lead, der selbst Kunden gewinnen will (Agenturen, Coaches, Berater, Webdesigner, Dienstleister): Zielgruppe, Marketing-Offer, 4er-Mail-Sequenz und drei Beispiel-Mails an echte Wunschkunden des Leads. Verwenden bei „Demo-Akquise-Kampagne“, „KI-Akquise-System als Demo“, „Muster-Kampagne für den Lead“, „Outreach-Kampagne für … entwerfen“, „Kaltakquise-Demo“ oder wenn das Offer der Kampagne ein Akquise-System ist. Nichts wird versendet."
---

# Demo-Akquise-Kampagne

Dem Lead zeigen, wie seine eigene Kaltakquise aussehen würde: fertig durchdacht, mit echten
Beispiel-Mails an echte Firmen aus seiner Zielgruppe. Das ist der stärkste Beweis für ein
KI-Akquise-System, weil der Lead die Personalisierung an Firmen sieht, die er kennt.

**Verbindlich:** `outreach-copy` (Plugin outreach) für alle Mail-Texte: Offer-Karten, Anatomie der
Entry-Mail, Feinheiten-Satz, Sequenz, Verbote, Selbstprüfung. Ist das Plugin outreach nicht
installiert, auf `fulfillment-setup` verweisen; ohne `outreach-copy` keine Mail-Texte.

Wissen (alle unter `../fulfillment-referenzen/references/`): `qualitaet.md`, `recht-und-grenzen.md`, `webseiten-bauplan.md`.

## Abgrenzung

- **Nichts wird versendet**, keine Kampagne im Konto des Nutzers angelegt, keine Leads importiert.
  Alles ist ein Dokument für den Lead.
- Beispiel-Mails sind deutlich als Beispiele markiert und gehen an niemanden.

## Ablauf

### 1. Den Lead verstehen (5 Min.)

Website des Leads lesen: Was verkauft er, an wen, mit welchen Belegen (Referenzen, Zahlen,
Fallstudien)? Daraus ein Kurz-Briefing wie in `outreach-campaign`: Angebot, Zielgruppe, USPs,
Tonalität. Nur Belegtes; Lücken markieren.

### 2. Zielgruppe und Offer (5 Min.)

- ICP-Satz für die Kunden des Leads: „[Branche] mit [Größe] in [Region], erkennbar an [Merkmal].
  Nicht: [Ausschluss].“
- Marketing-Offer für den Lead nach `outreach-copy` (Karte wählen und in einem Satz begründen,
  Deliverable statt Gespräch). Das Offer muss etwas sein, das der Lead selbst liefern kann.
- Lieferbarkeit mit `../fulfillment-referenzen/references/demo-katalog.md` prüfen und zeigen, wie
  er es liefern würde. Das zeigt dem Lead das ganze System: Akquise **und** Lieferung.

### 3. Sequenz (10 Min.)

Vier Mails nach `outreach-copy` (Entry-Mail mit Variablen `{{ai.hallo}}`, `{{ai.intro}}`, drei
Follow-ups). Anrede nach `outreach-copy`: Standard `du`; `sie` nur, wenn der Nutzer oder der Lead
es ausdrücklich wählt (die Branche allein ist kein Grund). Die Selbstprüfung aus `outreach-copy`
vollständig durchlaufen.

### 4. Drei Beispiel-Mails an echte Wunschkunden (10 Min.)

1. Drei echte Firmen aus der Zielgruppe des Leads finden (Websuche; oder aus `demo-leadliste`).
2. Je Firma nach den Recherche-Regeln einen Anker finden (Bewertungslob, abhebendes Website-Detail),
   Austauschtest bestehen.
3. Je Firma die fertige Mail 1 ausformulieren (Anrede, Intro, Offer, Feinheiten-Satz, CTA,
   Signatur des Leads).
4. Firmennamen dürfen stehen (öffentliche Firmen), **keine Namen von Ansprechpartnern**: Anrede
   „Hallo [Vorname],“ als sichtbarer Platzhalter mit Hinweis, dass die Recherche ihn findet.
   (Einzige erlaubte Klammer, ausdrücklich als Beispiel-Platzhalter markiert.)

### 5. Darstellen

Eine Seite (HTML, schlicht, `webseiten-bauplan.md` als Grundlage):

1. „So könnte die Kaltakquise von [Lead] aussehen“, Entwurfs-Hinweis von [Absender]
2. Zielgruppe (ICP-Satz) und warum
3. Das Offer und wie es geliefert wird
4. Die Sequenz (4 Mails, Abstände in Tagen)
5. Drei Beispiel-Mails, je mit Kasten „Woher der Bezug kommt“ (die Quelle des Ankers)
6. Was das System pro Woche leisten kann: nur Angaben des Nutzers (z. B. „100 recherchierte
   Mails pro Woche“), keine erfundenen Antwortquoten

### 6. Prüfen und ausliefern

`qualitaet.md` (harte Punkte), Selbstprüfung aus `outreach-copy` für alle Mails, dann
`demo-ausliefern`.
