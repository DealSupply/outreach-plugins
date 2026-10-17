#!/usr/bin/env python3
"""Vorab-Abgleich gegen den Outreach-Bestand — VOR der kostenpflichtigen Anreicherung.

    python3 dedup.py --index bestand-index.json --in roh.csv --out neu.csv
        [--drop-known-domains | --drop-known-domains-ohne-email]

--index: Antwort von export_leads(format="index") — {"index": [{"e","d","s","se"?}, ...]}
         (auch als reines Array akzeptiert). Älter als 24 h → Warnung.
         `e` ist die Versandadresse (ab ListM8 MCP 3.0.0; leer bei Leads ohne Adresse, ältere
         Server: auch null), `se` alle übrigen Adressen des Leads, `d` die Website-Domain.
Entfernt: exakte E-Mail-Treffer (Versand-, Identitäts- und Zweitadressen), do_not_contact-Treffer
(hart: auch Zeilen ohne E-Mail, deren Domain gesperrt ist), und Zeilen ohne E-Mail, deren
Website schon ein Lead ohne E-Mail im Bestand trägt (der Import würde sie nur verknüpfen).
Markiert: übrige Domain-Treffer ("Firma schon im Bestand") in der Spalte `hinweis`: kein
Ausschluss, es sei denn --drop-known-domains (alle) bzw. --drop-known-domains-ohne-email
(nur Zeilen ohne E-Mail) ist gesetzt.
Zeilen OHNE E-Mail bleiben sonst erhalten: ab ListM8 3.0.0 sucht die Recherche die Adresse auf
der Website, auf älteren Servern sind sie Anreicherungs-Kandidaten.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse


def root_domain(value: str | None) -> str | None:
    if not value or not value.strip():
        return None
    value = value.strip().lower()
    host = urlparse(value if "://" in value else f"http://{value}").hostname or value.split("/")[0]
    return host[4:] if host.startswith("www.") else host or None


def address(value) -> str:
    return value.strip().lower() if isinstance(value, str) else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--drop-known-domains", action="store_true",
                    help="Domain-Treffer ebenfalls entfernen statt nur markieren")
    ap.add_argument("--drop-known-domains-ohne-email", action="store_true",
                    help="Domain-Treffer nur bei Zeilen ohne E-Mail entfernen")
    args = ap.parse_args()

    with open(args.index, encoding="utf-8") as fh:
        payload = json.load(fh)
    rows = payload.get("index", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or (rows and not isinstance(rows[0], dict)) or (rows and "e" not in rows[0]):
        print("FEHLER: --index ist kein gültiger Bestandsindex (erwartet die Antwort von "
              "export_leads format=index). Datei prüfen — enthält sie eine Fehlermeldung?", file=sys.stderr)
        return 2
    generated = payload.get("generated_at") if isinstance(payload, dict) else None
    if generated:
        age = datetime.now(timezone.utc) - datetime.fromisoformat(generated)
        if age > timedelta(hours=24):
            print(f"WARNUNG: Bestandsindex ist {age.days}d {age.seconds // 3600}h alt — "
                  f"frisch ziehen (export_leads format=index).", file=sys.stderr)

    known_emails: dict[str, str] = {}
    known_domains: dict[str, str] = {}
    # Domains, unter denen ein Lead OHNE E-Mail bekannt ist: dieselbe Website ist derselbe Lead.
    addressless_domains: set[str] = set()
    for r in rows:
        status = r.get("s", "not_contacted")
        addresses = [address(r.get("e")), *(address(se) for se in r.get("se") or [])]
        for a in addresses:
            if a:
                known_emails[a] = status
        if r.get("d"):
            # do_not_contact gewinnt, wenn eine Domain mehrfach vorkommt
            if r["d"] not in known_domains or status == "do_not_contact":
                known_domains[r["d"]] = status
            if not any(addresses):
                addressless_domains.add(r["d"])

    kept, dropped_known, dropped_dnc, domain_hits, no_email_kept = [], [], [], 0, 0
    with open(args.infile, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        if "hinweis" not in fields:
            fields.append("hinweis")
        for row in reader:
            email = address(row.get("email"))
            if email:
                status = known_emails.get(email)
                if status == "do_not_contact":
                    dropped_dnc.append(email)
                    continue
                if status is not None:
                    dropped_known.append(email)
                    continue
            dom = root_domain(row.get("website")) or (email.split("@", 1)[1] if "@" in email else None)
            dom_status = known_domains.get(dom) if dom else None
            if dom_status == "do_not_contact":
                dropped_dnc.append(email or f"(ohne E-Mail: {dom})")
                continue
            if dom_status is not None:
                domain_hits += 1
                same_lead = not email and dom in addressless_domains
                if same_lead or args.drop_known_domains or (args.drop_known_domains_ohne_email and not email):
                    dropped_known.append(email or f"(ohne E-Mail: {dom})")
                    continue
                hinweis = (row.get("hinweis") or "").strip()
                row["hinweis"] = (hinweis + ";" if hinweis else "") + "firma-schon-im-bestand"
            if not email:
                no_email_kept += 1
            kept.append(row)

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept)

    print(f"Behalten: {len(kept)} | Schon im Bestand entfernt: {len(dropped_known)} | "
          f"do_not_contact entfernt: {len(dropped_dnc)} | Domain-Warnungen: {domain_hits}"
          + (f" | ohne E-Mail behalten (Recherche bzw. Anreicherung sucht die Adresse): {no_email_kept}"
             if no_email_kept else ""))
    if dropped_dnc:
        print("do_not_contact (NIE anschreiben): " + ", ".join(sorted(set(dropped_dnc))[:20]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
