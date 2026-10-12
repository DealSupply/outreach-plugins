---
name: fulfillment-referenzen
description: Referenzpaket des Fulfillment-Plugins, gelesen vom Einstieg fulfillment und den demo-Skills. Enthält den Demo-Katalog (Offer → Demo-Art, Machbarkeit, Aufwand), den Lead-Kontext aus der Outreach-App, Umgebungen (claude.ai, Claude Code, Codex, No-Code), Veröffentlichen mit Netlify, Demo-Link und Antwort-Vorlagen, Qualitätsprüfung, Recht und Grenzen sowie den Webseiten-Bauplan. Kein direkter Einstieg.
---

# Fulfillment: Referenz-Paket

Kein eigenständiger Skill, sondern die geteilte Wissensbasis der Fulfillment-Familie. Der Einstieg
`fulfillment` und alle `demo-*`-Skills lesen von hier (`references/`).

| Datei | Inhalt |
|---|---|
| `references/demo-katalog.md` | Welche Offers sich mit KI liefern lassen: Demo-Art, Bau-Skill, Aufwand, Kosten, Grenzen; Check für unbekannte Offers |
| `references/lead-kontext.md` | Was aus der Outreach-App kommt (Blueprint, Antworter über `list_leads`, Grenze von `get_lead_data`) und wofür es taugt |
| `references/umgebungen.md` | Was in claude.ai, Claude App, Claude Code, ChatGPT/Codex und anderen KI-Werkzeugen geht |
| `references/netlify.md` | Veröffentlichen: Netlify-Connector, Netlify Drop, Netlify CLI, `noindex`, Adressen, Aufräumen |
| `references/demo-link.md` | Link am Lead speichern (`demo-url`, `demo-datum`), Antwort-Vorlagen, wann der Link verschickt wird |
| `references/qualitaet.md` | Qualitätsprüfung vor dem Veröffentlichen (für alle Demo-Arten) |
| `references/recht-und-grenzen.md` | Bilder, Logos, Texte des Leads, Datenschutz, Kennzeichnung, Branchen mit Werberegeln |
| `references/webseiten-bauplan.md` | Aufbau, Gestaltung und Technik einer Demo-Webseite (genutzt von `demo-webseite`; als Hülle für die Darstellung auch von `demo-seo`, `demo-anzeigen`, `demo-leadliste`, `demo-akquise-kampagne`) |
