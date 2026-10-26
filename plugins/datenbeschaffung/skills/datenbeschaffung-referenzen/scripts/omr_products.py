#!/usr/bin/env python3
"""OMR Reviews -> Software-Anbieter als JSON (kostenlos, ohne Konto, ohne Apify).

    python3 omr_products.py --out omr.json [--kategorie crm,time-tracking] [--min-reviews 1] [--dach]

OMR Reviews (omr.com/de/reviews) beantwortet öffentliche GraphQL-Abfragen ohne Anmeldung
(api.reviews.omr.com/graphql, geprüft 14.10.2026: 14.023 Produkte, 500 je Seite, 29 Abrufe für
alles). Je Produkt kommen Anbieter-Website, Kategorie, OMR-Bewertung, Anzahl der Bewertungen,
LinkedIn-Seite, Testzugang und Kurzbeschreibung. Die Felder heißen so, wie build_csv.py sie
versteht (produkt, website, kategorie, plattform, bewertung, bewertungen_anzahl, linkedin_url).

Kein Feld nennt den Firmensitz. `germanLocation` ist der Serverstandort, nicht der Sitz.
--dach behält nur Produkte, deren Domain auf .de/.at/.ch endet oder deren Firmen-Slug eine
deutsche Rechtsform trägt (Vorfilter, keine Prüfung). Den Sitz prüft danach sitz_check.py.
Mehrere Produkte eines Anbieters werden auf die Domain zusammengelegt (es zählt das Produkt mit
den meisten Bewertungen).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from urllib.parse import urlparse

API = "https://api.reviews.omr.com/graphql"
FIELDS = """id slug title url companySlug linkedin shortDescription
mainCategory { slug title } reviewCount averageRecommendationRating
freeTrial freePlanAvailable cloud germanLocation"""
LEGAL = re.compile(r"(^|-)(gmbh|ag|ug|kg|gesmbh|gmbh-co-kg|se|ohg|gbr|sarl|sa)(-|$)")
DACH_TLD = (".de", ".at", ".ch")


def query(page: int, per_page: int, category: str | None) -> dict:
    cat = f', categorySlug: "{category}"' if category else ""
    body = {"query": "{ products(page: %d, perPage: %d%s) { pagination { totalCount totalPages } "
                     "products { %s } } }" % (page, per_page, cat, FIELDS)}
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "datenbeschaffung/omr_products"})
    for attempt in range(4):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=90))
            if data.get("errors"):
                raise RuntimeError(data["errors"][0].get("message"))
            return data["data"]["products"]
        except Exception as exc:  # Netz, Zeitüberschreitung, Rate-Limit
            if attempt == 3:
                raise
            print(f"  Seite {page}: {exc} – neuer Versuch", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return {}


def host(url: str) -> str:
    h = (urlparse(url if "://" in url else "https://" + url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def row(p: dict) -> dict | None:
    domain = host(p.get("url") or "")
    if not domain or domain == "omr.com" or domain.endswith(".omr.com"):
        return None
    rating = p.get("averageRecommendationRating")
    return {
        # Der Titel ist der Produktname („Kundenwolke CRM“), nicht die Firma. `company` füllen
        # andere Quellen oder die Recherche; build_csv.py nimmt sonst `produkt` als Anzeigenamen.
        "produkt": p.get("title"),
        "website": "https://" + domain,
        "kategorie": (p.get("mainCategory") or {}).get("title"),
        "plattform": "OMR Reviews",
        "bewertung": round(rating, 1) if rating and p.get("reviewCount") else None,
        "bewertungen_anzahl": p.get("reviewCount") or 0,
        "linkedin_url": p.get("linkedin"),
        "omr_url": f"https://omr.com/de/reviews/product/{p['slug']}",
        "omr_firma": p.get("companySlug"),
        "kostenlos_testen": "ja" if p.get("freeTrial") or p.get("freePlanAvailable") else "",
        "beschreibung": (p.get("shortDescription") or "").strip(),
        "_domain": domain,
    }


def is_dach(r: dict) -> bool:
    return r["_domain"].endswith(DACH_TLD) or bool(LEGAL.search(r.get("omr_firma") or ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--kategorie", default="", help="OMR-Kategorie-Slugs, kommagetrennt (leer = alle)")
    ap.add_argument("--min-reviews", type=int, default=0)
    ap.add_argument("--dach", action="store_true", help="Vorfilter auf .de/.at/.ch oder Rechtsform")
    ap.add_argument("--per-page", type=int, default=500)
    args = ap.parse_args()

    cats = [c.strip() for c in args.kategorie.split(",") if c.strip()] or [None]
    raw: list[dict] = []
    for cat in cats:
        page, pages = 1, 1
        while page <= pages:
            res = query(page, args.per_page, cat)
            pages = res["pagination"]["totalPages"]
            raw += res["products"]
            print(f"{cat or 'alle'}: Seite {page}/{pages} ({len(raw)} Produkte)", file=sys.stderr)
            page += 1
            time.sleep(0.5)

    by_domain: dict[str, dict] = {}
    for p in raw:
        r = row(p)
        if not r or r["bewertungen_anzahl"] < args.min_reviews or (args.dach and not is_dach(r)):
            continue
        best = by_domain.get(r["_domain"])
        if not best or r["bewertungen_anzahl"] > best["bewertungen_anzahl"]:
            by_domain[r["_domain"]] = r
    rows = list(by_domain.values())
    for r in rows:
        r.pop("_domain")
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    rated = sum(1 for r in rows if r["bewertungen_anzahl"])
    print(f"Produkte {len(raw)} -> Anbieter (Domains) {len(rows)}, davon mit Bewertung {rated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
