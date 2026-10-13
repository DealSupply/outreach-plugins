# Demo-Link am Lead und Antwort-Vorlagen

> Referenz zu `demo-ausliefern`.

## Link am Lead speichern

Der Link wird als Custom-Attribut am Lead gespeichert. So sieht der Nutzer in der App, welcher Lead
schon eine Demo hat und wann sie entstand.

```
bulk_set_lead_attributes(
  lead_ids=[<lead_id>],
  attributes={"demo-url": "https://entwurf-mueller-dach-k7q2xm.netlify.app", "demo-datum": "2026-10-12"},
  create_missing=true
)
```

- **Schlüssel mit Bindestrich** (`demo-url`, `demo-datum`): Die App bildet Feldnamen als
  Kleinbuchstaben mit Bindestrich. Ein Schlüssel mit Unterstrich würde beim ersten Mal als
  `demo-url` angelegt, beim nächsten Aufruf nicht gefunden und erneut angelegt (`demo-url_1` …).
- `create_missing=true` legt die Felder beim ersten Mal an; danach sind sie für alle Leads da.
- Die Antwort nennt neu angelegte Felder (`attributes_created`). Steht dort ein anderer Schlüssel
  als `demo-url` bzw. `demo-datum`, gab es schon ein gleichnamiges Feld: dem Nutzer melden und
  künftig den Schlüssel aus der Antwort verwenden.
- Datum als `JJJJ-MM-TT`, damit es sich sortieren lässt.
- Braucht die Berechtigung `leads:write`. Fehlt sie, den Link dem Nutzer nennen; er trägt ihn in der
  App am Lead ein.

## Antwort an den Lead

Der Lead hat auf die Cold-Mail geantwortet („ja, gern“). Die Antwort ist kurz, hält das Versprechen
und stellt genau eine Frage. Anrede wie in der Kampagne (`salutation`). Keine Gedankenstriche,
kein Werbeton, Signatur wie in der Kampagne.

**Webseiten-Entwurf (du):**

```
Hallo [Vorname],

wie versprochen hier der Entwurf: [Link]

Ich habe vor allem [On-Top-Detail aus dem Feinheiten-Satz] umgesetzt. Schau ihn dir in Ruhe an,
am besten auch einmal auf dem Handy.

Was ist dein erster Eindruck?

Viele Grüße
[Name]
```

**SEO-Ergebnis (du):**

```
Hallo [Vorname],

hier wie versprochen die Übersicht: [Link]

Am meisten bringt aus meiner Sicht [der eine Hebel mit dem größten Effekt]. Das ließe sich ohne
großen Aufwand umsetzen.

Soll ich dir kurz zeigen, wie das konkret aussehen würde?

Viele Grüße
[Name]
```

**Allgemein:** Link, ein Satz zum wichtigsten Punkt, eine Frage. Nie einen Preis, nie ein Paket,
nie drei Fragen auf einmal. Das Gespräch über den Auftrag kommt nach seiner Reaktion.

**Sie-Form:** „Guten Tag Frau [Nachname],“ bzw. „Guten Tag Herr [Nachname],“; ist die Person nicht
klar, „Guten Tag,“. Alle Pronomen umstellen (Ihnen, Ihr, Sie), Gruß „Viele Grüße“ bleibt.

Die Klammern füllt der Skill aus; im fertigen Text steht keine Klammer mehr.

## Wann der Link verschickt wird

Der Demo-Link geht **in der Antwort** an den Lead, nachdem er auf die Cold-Mail reagiert hat. In
die Sequenz gehört er nicht: `outreach-copy` erlaubt in Mail 1 keinen Link und ab Mail 3 nur einen
Kalender- oder Website-Link, und Follow-ups bringen kein neues Offer.
