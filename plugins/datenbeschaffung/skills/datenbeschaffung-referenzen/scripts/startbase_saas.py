#!/usr/bin/env python3
"""Startbase.de -> deutsche B2B-SaaS-Firmen als JSON (kostenlos, ohne Konto, ohne Apify).

    python3 startbase_saas.py --out startbase.json [--max 500] [--bundesland Hamburg,Bayern]

Startbase (Startup-Datenbank, nur Deutschland) pflegt je Profil die Felder Geschäftsmodell
(Wert „SaaS“), Zielgruppe (B2B/B2C/B2B2C), Sektor, Gründungsjahr, Teamgröße, Hauptquartier,
Bundesland und juristische Person. Die Sitemap listet alle Profile (14.10.2026: 9.665); rund
23 % sind aktive B2B-SaaS (Stichprobe 500 Profile, hochgerechnet etwa 2.200).

Die Website steht nur hinter dem Login. Ausgabe deshalb ohne `website`; die Domain kommt aus dem
Abgleich mit den anderen Quellen oder über website_suche.py (Google-Suche nach Rechtsträger + Ort).

Höflich abrufen: 4 parallele Abrufe, 0,3 s Pause je Abruf, alle 9.665 Profile in etwa 25 Minuten.
--max nimmt eine Zufallsstichprobe (Pilot).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import html
import json
import random
import re
import sys
import time
import urllib.request

SITEMAP = "https://www.startbase.de/sitemaps/companies.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) datenbeschaffung/startbase"}


def get(url: str) -> str:
    for attempt in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS),
                                          timeout=25).read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(3 * (attempt + 1))
    return ""


def field(text: str, label: str) -> str:
    m = re.search(re.escape(label) + r":\s*\|[\s|]*([^|]+?)\s*\|", text)
    value = m.group(1).strip() if m else ""
    return "" if value in ("-", "n/a") else value


def parse(url: str) -> dict:
    page = get(url)
    time.sleep(0.3)
    if not page:
        return {"startbase_url": url, "fehler": "nicht-erreichbar"}
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", re.sub(
        r"(?is)<(script|style)[^>]*>.*?</\1>", " ", page))))
    title = re.search(r"<title>([^<]+)</title>", page)
    name = html.unescape(title.group(1).split("|")[0].strip()) if title else ""
    hq = field(text, "Hauptquartier")
    return {
        "company": field(text, "Juristische Person") or re.sub(r"\s*\(.*\)$", "", name),
        "produkt": re.sub(r"\s*\(.*\)$", "", name),
        "city": hq.split(",")[0].strip(),
        "land": hq.split(",")[-1].strip() if "," in hq else "",
        "bundesland": field(text, "Bundesland"),
        "geschaeftsmodell": field(text, "Geschäftsmodell"),
        "zielgruppe": field(text, "Zielgruppe"),
        "kategorie": field(text, "Sektor"),
        "mitarbeiter": field(text, "Größe des Teams").replace(" Mitarbeiter", ""),
        "gruendung": field(text, "Gründungsjahr"),
        "historisch": "historischer eintrag" in text.lower(),
        "startbase_url": url,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=0, help="Zufallsstichprobe (0 = alle)")
    ap.add_argument("--bundesland", default="", help="kommagetrennt, z. B. Hamburg,Bayern")
    ap.add_argument("--alle-modelle", action="store_true", help="nicht auf SaaS + B2B filtern")
    args = ap.parse_args()

    urls = re.findall(r"<loc>([^<]+/organization/[^<]+)</loc>", get(SITEMAP))
    if not urls:
        print("Sitemap nicht erreichbar oder leer.", file=sys.stderr)
        return 1
    if args.max:
        random.seed(7)
        urls = random.sample(urls, min(args.max, len(urls)))
    print(f"{len(urls)} Profile werden gelesen …", file=sys.stderr)
    rows: list[dict] = []
    with cf.ThreadPoolExecutor(4) as pool:
        for i, r in enumerate(pool.map(parse, urls), 1):
            rows.append(r)
            if i % 500 == 0:
                print(f"  {i}/{len(urls)}", file=sys.stderr)

    lands = {b.strip().lower() for b in args.bundesland.split(",") if b.strip()}
    keep = [r for r in rows if "fehler" not in r and not r["historisch"]
            and (args.alle_modelle or ("SaaS" in r["geschaeftsmodell"] and "B2B" in r["zielgruppe"]))
            and (not lands or r["bundesland"].lower() in lands)]
    for r in keep:
        r.pop("historisch", None)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(keep, fh, ensure_ascii=False, indent=1)
    failed = sum(1 for r in rows if "fehler" in r)
    print(f"Profile {len(rows)} (nicht erreichbar {failed}) -> aktive B2B-SaaS {len(keep)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
