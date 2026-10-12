# Lead-Kontext aus der Outreach-App

> Referenz zu `fulfillment`. Welche Daten die Outreach-App liefert und wofür eine Demo sie nutzt.
> Alle Tools hier sind lesend, außer `bulk_set_lead_attributes` (siehe `demo-link.md`).

## Kampagne: `export_campaign_blueprint(campaign_id)`

Die Antwort steckt unter `blueprint`.

| Feld | Bedeutung für die Demo |
|---|---|
| `blueprint.campaign.intelligence.offer_contract.title.value` | **Das Offer.** Genau das wird geliefert. |
| `blueprint.sequence.steps[0].body` | Mail 1 mit dem **Feinheiten-Satz** („vor allem …“): dieses On-Top-Detail wurde versprochen und muss in der Demo sichtbar sein |
| `blueprint.campaign.intelligence.campaign_brief.business.value` | Was der Nutzer verkauft; die Demo führt dorthin |
| `blueprint.campaign.intelligence.campaign_brief.usp.value` | Belege und Stärken des Nutzers (nie erfinden) |
| `blueprint.campaign.intelligence.campaign_brief.target_audience.value` | Zielgruppe; hilft bei Branche und Tonalität |
| `blueprint.campaign.emailAgentConfig.salutation` | `du` oder `sie`: dieselbe Anrede in der Antwort an den Lead |

Fehlt `offer_contract`, das Offer **beim Nutzer erfragen**. `qualificationSettings.offer_summary`
beschreibt oft die bezahlte Leistung, nicht den Türöffner, und taugt deshalb nicht als Ersatz.

## Wer hat geantwortet: `list_leads`

```
list_leads(campaign_id, contact_status="replied", fit_level="", research_status="", campaign_status="")
```

- Die drei leeren Filter sind Pflicht: Ohne sie zeigt `list_leads` nur Leads, die noch bearbeitet
  werden, und ein angeschriebener Lead taucht nicht auf.
- `replied` steht nur am Lead, wenn die App den Status aus Instantly abgeglichen hat. Fehlt der
  Abgleich, nennt der Nutzer den Lead (Firma oder E-Mail); dann `search_leads(query="<Firma oder Domain>")`.
- Weitere Werte: `opportunity` (vom Nutzer als Chance markiert), `contacted`, `all`.
- Den Lead immer mit dem Nutzer bestätigen; eine Antwort kann auch eine Absage sein.

Jede Zeile liefert `id`, `company`, `website`, `city`, `phoneNumber`, `email`, `contactStatus`
und `appUrl`. Das sind die Grunddaten der Demo.

## Grenze: `get_lead_data` sperrt angeschriebene Leads

`get_lead_data` ist für die Mail-Erzeugung gebaut und lehnt jeden Lead ab, der schon kontaktiert
wurde (Fehler `contact_gate`). Für Antworter heißt das: **Recherche-Bericht und Import-Attribute
kommen nicht über die Verbindung.** Deshalb:

1. Die **Website des Leads live lesen**; sie ist ohnehin die beste Quelle.
2. Braucht es den Recherche-Bericht (z. B. für das Lob aus Bewertungen), den Nutzer bitten, den Lead
   in der App zu öffnen (`appUrl`) und den Bericht hineinzukopieren.
3. Google-Bewertungen (Schnitt, Anzahl, Lob) sonst direkt im Google-Profil des Leads ansehen.

`get_lead_data(campaign_id, lead_id)` funktioniert nur für Leads, die noch nicht angeschrieben
wurden, also wenn eine Demo **vor** dem Versand entsteht. Dann liefert es zusätzlich
`lead.research.text`, `lead.research.decisionMaker` und `lead.customAttributes` (z. B. `rating`,
`reviews_count`, `google_rezensionstexte`, `inhaber`).

**Vorrang der Quellen:** Website des Leads (live) > Recherche-Bericht > Import-Attribute.
Widersprechen sich Quellen (z. B. Telefonnummer), die Website nehmen und den Widerspruch melden.

## Was nie in eine Demo gehört

- Interne Felder der App (Score, Qualifizierungsurteil, Kategorie, `appUrl`)
- Namen aus Rezensionen (Datenschutz); Rezensionstexte nur sinngemäß und ohne Namen
- Persönliche E-Mail-Adressen; im Kontaktbereich nur, was auf der Website des Leads steht
