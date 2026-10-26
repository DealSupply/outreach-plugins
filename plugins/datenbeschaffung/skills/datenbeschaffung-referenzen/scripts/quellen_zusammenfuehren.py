#!/usr/bin/env python3
"""Mehrere Quellen auf die Domain zusammenführen (weg-f-saas und jede Mehrquellen-Liste).

    python3 quellen_zusammenfuehren.py --out kandidaten.json \
        omr:omr.json linkedin:linkedin-details.json startbase:startbase-web.json

Jedes Argument ist `<quelle>:<datei.json>`. Versteht die generischen Felder (company, website,
city, email, kategorie, mitarbeiter, ...) und die Rohform der LinkedIn-Firmendetails
(name, website, employeeCount, linkedinUrl, locations). Zusammengeführt wird auf die Domain der
Website; ein Feld, das schon gefüllt ist, wird nicht überschrieben (die erste Quelle gewinnt).
Reihenfolge: linkedin vor startbase vor omr, denn LinkedIn und Startbase nennen die Firma, OMR
nur das Produkt. `quellen` hält fest, wo die Firma überall auftaucht. Das ist
ein Qualitätssignal: Wer in zwei Quellen steht, verkauft fast sicher ein Produkt.

Zeilen ohne Website werden über den bereinigten Firmennamen zugeordnet; bleibt kein Treffer,
landen sie am Ende ohne Website (Kandidaten für website_suche.py).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from urllib.parse import urlparse

LEGAL = re.compile(r"\b(gmbh|ag|ug|se|kg|co|ohg|gbr|mbh|haftungsbeschränkt|haftungsbeschraenkt|"
                   r"holding|deutschland|germany|software|technologies|solutions|group)\b")


def domain(url: str | None) -> str:
    if not url:
        return ""
    host = (urlparse(url if "://" in url else "https://" + url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def name_key(name: str | None) -> str:
    text = unicodedata.normalize("NFKD", (name or "").lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", LEGAL.sub(" ", re.sub(r"\(.*?\)|\|.*", " ", text)))


def slug_of(url: str | None) -> str:
    m = re.search(r"linkedin\.com/company/([^/?#]+)", url or "")
    return m.group(1).lower() if m else ""


def generic(row: dict) -> dict:
    """LinkedIn-Firmendetails in die generischen Felder übersetzen, alles andere unverändert."""
    if "universalName" not in row:
        return dict(row)
    locs = row.get("locations") or []
    hq = next((l for l in locs if l.get("headquarter")), locs[0] if locs else {})
    count = row.get("employeeCount")
    # Felder, die spätere Schritte (sitz_check.py) an die Rohzeile gehängt haben, bleiben erhalten.
    added = {k: row[k] for k in ("email", "emails", "sitz_land", "sitz_plz", "sitz_status", "produkt_signale")
             if row.get(k)}
    return {
        **added,
        "company": row.get("name"),
        "website": row.get("website") or row.get("callToActionUrl"),
        "city": row.get("city") or hq.get("city"),
        "mitarbeiter": count,
        "linkedin_url": row.get("linkedinUrl"),
        "follower": row.get("followerCount"),
        "gruendung": (row.get("foundedOn") or {}).get("year"),
        "beschreibung": row.get("tagline") or (row.get("description") or "")[:200],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("quellen", nargs="+", help="quelle:datei.json")
    args = ap.parse_args()

    merged: dict[str, dict] = {}
    by_name: dict[str, str] = {}
    by_slug: dict[str, str] = {}  # LinkedIn-Seite -> Domain (OMR nennt sie bei vielen Produkten)
    loose: list[dict] = []
    counts: dict[str, int] = {}
    for spec in args.quellen:
        label, _, path = spec.partition(":")
        if not label or not path:
            ap.error(f"„{spec}“: erwartet quelle:datei.json")
        rows = json.load(open(path, encoding="utf-8"))
        counts[label] = len(rows)
        for raw in rows:
            row = generic(raw)
            if row.get("website") and "://" not in str(row["website"]):
                row["website"] = "https://" + str(row["website"])
            key = domain(row.get("website")) or by_slug.get(slug_of(row.get("linkedin_url"))) \
                or by_name.get(name_key(row.get("company"))) or by_name.get(name_key(row.get("produkt")))
            if not key:
                loose.append({**row, "quellen": label})
                continue
            target = merged.setdefault(key, {"quellen": ""})
            for field, value in row.items():
                if value not in (None, "", [], 0) and target.get(field) in (None, "", [], 0):
                    target[field] = value
            if label not in target["quellen"].split(","):
                target["quellen"] = ",".join(q for q in (target["quellen"], label) if q)
            for name in (row.get("company"), row.get("produkt")):
                if name_key(name) and len(name_key(name)) >= 4:
                    by_name.setdefault(name_key(name), key)
            if slug_of(row.get("linkedin_url")):
                by_slug.setdefault(slug_of(row.get("linkedin_url")), key)

    # Zweiter Durchgang: Zeilen ohne Website, deren Name erst eine spätere Quelle mitbrachte.
    still_loose = []
    for row in loose:
        key = by_slug.get(slug_of(row.get("linkedin_url"))) or by_name.get(name_key(row.get("company"))) \
            or by_name.get(name_key(row.get("produkt")))
        if not key:
            still_loose.append(row)
            continue
        target = merged[key]
        for field, value in row.items():
            if field != "quellen" and value not in (None, "", [], 0) and target.get(field) in (None, "", [], 0):
                target[field] = value
        if row["quellen"] not in target["quellen"].split(","):
            target["quellen"] += "," + row["quellen"]
    loose = still_loose
    out = list(merged.values()) + loose
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    multi = sum(1 for r in merged.values() if "," in r["quellen"])
    print(f"Eingang {counts} -> {len(merged)} Firmen mit Website (in mehreren Quellen: {multi}), "
          f"{len(loose)} ohne Website")
    return 0


if __name__ == "__main__":
    sys.exit(main())
