#!/usr/bin/env python3
"""Website zu Firmen ohne Domain finden (Startbase, Verbandslisten) über eine Google-Suche.

    # 1. Suchanfragen bauen (eine je Firma) -> Input für den SERP-Actor (apify-actors.md)
    python3 website_suche.py anfragen --in startbase.json --out serp-input.json
    # 2. Actor laufen lassen (limit "10", country "DE"), Ergebnis als serp.json speichern
    # 3. Treffer übernehmen
    python3 website_suche.py zuordnen --in startbase.json --serp serp.json --out mit-website.json

Die Anfrage lautet `"<Rechtsträger>" <Ort>` bzw. `"<Produkt>" <Ort>`. Übernommen wird der erste
Treffer, dessen Domain zum Firmen- oder Produktnamen passt und kein Portal ist
(noise-domains.md). Ohne passenden Treffer bleibt `website` leer und `hinweis` nennt den Grund.
Kosten: 1.000 Firmen = 1.000 Suchseiten, mit dem primären SERP-Actor etwa 0,50 $ (kosten.md).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import unicodedata
from urllib.parse import urlparse

LEGAL = re.compile(r"\b(gmbh|ag|ug|se|kg|co|ohg|gbr|mbh|haftungsbeschränkt|haftungsbeschraenkt|"
                   r"gesellschaft|holding|deutschland|germany|software|technologies|solutions|group)\b")


def noise() -> set[str]:
    path = pathlib.Path(__file__).resolve().parent.parent / "references/noise-domains.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    extra = {"startbase.de", "northdata.de", "northdata.com", "firmenwissen.de", "unternehmensregister.de",
             "handelsregister.de", "dealroom.co", "crunchbase.com", "linkedin.com", "xing.com",
             "kununu.com", "omr.com", "capterra.com.de", "capterra.com", "g2.com", "wikipedia.org",
             "bundesanzeiger.de", "companyhouse.de", "online-handelsregister.de", "firmen.wiwo.de",
             "moneyhouse.ch", "firmenabc.at", "wko.at", "gruenderszene.de", "deutsche-startups.de",
             "facebook.com", "instagram.com", "youtube.com", "stepstone.de", "indeed.com"}
    return set(re.findall(r"\b([a-z0-9][a-z0-9.-]+\.[a-z]{2,})\b", text)) | extra


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", (text or "").lower()).encode("ascii", "ignore").decode()
    text = re.sub(r"\(.*?\)", " ", text)
    return re.sub(r"[^a-z0-9]", "", LEGAL.sub(" ", text))


def root(url: str) -> str:
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    parts = host.split(".")
    return ".".join(parts[-3:]) if len(parts) > 2 and parts[-2] in ("co", "com") else ".".join(parts[-2:])


def fits(domain: str, names: list[str]) -> bool:
    label = re.sub(r"[^a-z0-9]", "", domain.split(".")[0])
    for n in names:
        if len(n) >= 4 and (n in label or (len(label) >= 4 and label in n)):
            return True
    return False


def query_of(row: dict) -> str:
    name = row.get("company") or row.get("produkt") or ""
    return f'"{name}" {row.get("city") or ""}'.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("modus", choices=["anfragen", "zuordnen"])
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--serp")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rows = json.load(open(args.inp, encoding="utf-8"))
    todo = [r for r in rows if not r.get("website")]

    if args.modus == "anfragen":
        queries = sorted({query_of(r) for r in todo})
        json.dump({"keyword": "\n".join(queries), "limit": "10", "country": "DE", "hl": "de",
                   "include_merged": False}, open(args.out, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"{len(queries)} Suchanfragen für {len(todo)} Firmen ohne Website -> {args.out}")
        return 0

    if not args.serp:
        ap.error("zuordnen braucht --serp")
    results: dict[str, list[str]] = {}
    for page in json.load(open(args.serp, encoding="utf-8")):
        term = page.get("search_term") or (page.get("searchQuery") or {}).get("term", "")
        urls = [r.get("url", "") for r in page.get("results") or page.get("organicResults") or []]
        results.setdefault(term, []).extend(urls)
    bad = noise()
    found = 0
    for r in todo:
        names = [norm(r.get("company", "")), norm(r.get("produkt", ""))]
        hit = next((d for d in (root(u) for u in results.get(query_of(r), []))
                    if d and d not in bad and fits(d, names)), "")
        if hit:
            r["website"] = "https://" + hit
            found += 1
        else:
            r["hinweis"] = "keine-website-gefunden" if query_of(r) in results else "nicht-gesucht"
    json.dump(rows, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Ohne Website {len(todo)} -> gefunden {found} ({round(100 * found / max(len(todo), 1))} %)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
