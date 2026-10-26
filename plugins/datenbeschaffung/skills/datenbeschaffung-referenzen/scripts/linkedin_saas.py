#!/usr/bin/env python3
"""LinkedIn-Firmensuche (Short) -> SaaS-Kandidaten mit Sitz in der Region.

    # 1. Short-Ergebnisse aller Segmente zusammenlegen, auf Sitz filtern, Tabelle zum Einordnen
    python3 linkedin_saas.py vorbereiten --orte "Hamburg" --out li-hamburg seg1.json seg2.json ...
       -> li-hamburg.json (Firmen mit Sitz in der Region) + li-hamburg.tsv (slug, Name, Tagline, Follower)
    # 2. Claude ordnet jede Zeile der TSV einer Klasse zu (weg-f-saas, Schritt 4) -> klassen.tsv
    # 3. Details nur für SaaS, die noch keine andere Quelle kennt
    python3 linkedin_saas.py details --in li-hamburg.json --klassen klassen.tsv \
        --bekannt omr.json --out details-input.json
       -> Input für den Details-Actor ({"companies": [...]})

Die Standortsuche liefert jede Firma mit irgendeinem Büro in der Region, sortiert nach Größe,
also zuerst internationale Konzerne. Der Sitz steht im Short-Ergebnis unter
location.linkedinText, meist englisch ("Hamburg, Hamburg", "Munich, Bavaria", "Cologne"). --orte
nimmt Städte oder Bundesländer kommagetrennt, beide Schreibweisen angeben ("München,Munich");
--dach erkennt alle DACH-Länder, Bundesländer, Kantone und Großstädte.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

DACH = ("germany|deutschland|austria|österreich|switzerland|schweiz|suisse|"
        "baden-w|bavaria|bayern|berlin|brandenburg|bremen|hamburg|hesse|hessen|"
        "mecklenburg|lower saxony|niedersachsen|north rhine|nordrhein|rhineland|rheinland|saarland|"
        "saxony|sachsen|schleswig|thuringia|thüringen|"
        "vienna|wien|styria|steiermark|tyrol|tirol|salzburg|carinthia|kärnten|vorarlberg|"
        "upper austria|oberösterreich|lower austria|niederösterreich|burgenland|"
        "zurich|zürich|bern|basel|geneva|genf|lucerne|luzern|zug|st. gallen|aargau|vaud|waadt|ticino|"
        "munich|münchen|cologne|köln|frankfurt|stuttgart|düsseldorf|dusseldorf|leipzig|dresden|"
        "hannover|hanover|nuremberg|nürnberg|karlsruhe|mannheim|bonn|münster|aachen|freiburg|"
        "graz|linz|innsbruck|lausanne|winterthur")


def load(paths: list[str]) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for path in paths:
        for r in json.load(open(path, encoding="utf-8")):
            slug = r.get("universalName")
            if slug:
                rows.setdefault(slug, r)
    return rows


def hq_text(r: dict) -> str:
    return ((r.get("location") or {}).get("linkedinText") or "").lower()


def prepare(args) -> int:
    rows = load(args.dateien)
    if args.dach:
        pattern = re.compile(DACH, re.I)
    else:
        places = [re.escape(p.strip().lower()) for p in args.orte.split(",") if p.strip()]
        if not places:
            print("--orte oder --dach angeben", file=sys.stderr)
            return 1
        pattern = re.compile("|".join(places), re.I)
    keep = [r for r in rows.values() if pattern.search(hq_text(r))]
    json.dump(keep, open(args.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(args.out + ".tsv", "w", encoding="utf-8") as fh:
        for r in keep:
            tagline = re.sub(r"\s+", " ", r.get("summary") or "")[:220]
            fh.write("\t".join([r["universalName"], (r.get("name") or "").replace("\t", " "),
                                tagline.replace("\t", " "), str(r.get("followers") or "")]) + "\n")
    print(f"Firmen {len(rows)} -> Sitz in der Region {len(keep)} ({args.out}.json, {args.out}.tsv)")
    return 0


def details(args) -> int:
    rows = {r["universalName"]: r for r in json.load(open(args.inp, encoding="utf-8"))}
    classes = {}
    for line in open(args.klassen, encoding="utf-8"):
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) >= 2 and parts[0]:
            classes[parts[0]] = parts[1]
    missing = [slug for slug in rows if slug not in classes]
    wanted = {c.strip() for c in args.klassen_behalten.split(",")}
    # Bekannt ist nur, wessen LinkedIn-Seite eine andere Quelle schon nennt (Namensgleichheit
    # wie „Connect“ gegen „Connect GmbH“ ist zu unsicher). Die bekannten Firmen kommen ohne
    # Details mit (bekannt.json), damit `linkedin` im Abgleich als Quelle zählt.
    known_slugs = set()
    for path in args.bekannt:
        for k in json.load(open(path, encoding="utf-8")):
            m = re.search(r"linkedin\.com/company/([^/?#]+)", k.get("linkedin_url") or "")
            if m:
                known_slugs.add(m.group(1).lower().rstrip("/"))
    pick = [r for slug, r in rows.items() if classes.get(slug) in wanted]
    new = [r for r in pick if r["universalName"].lower() not in known_slugs]
    known = [{"company": r.get("name"), "linkedin_url": r.get("linkedinUrl")} for r in pick if r not in new]
    json.dump({"companies": [r["linkedinUrl"] for r in new]}, open(args.out, "w", encoding="utf-8"))
    known_path = re.sub(r"\.json$", "", args.out) + "-bekannt.json"
    json.dump(known, open(known_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Klassen {sorted(wanted)}: {len(pick)} Firmen, davon schon bekannt {len(known)} "
          f"({known_path}), Details nötig für {len(new)} (Kosten siehe kosten.md)")
    if missing:
        print(f"Achtung: {len(missing)} Firmen ohne Klasse in {args.klassen}, z. B. {missing[:3]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="modus", required=True)
    p = sub.add_parser("vorbereiten")
    p.add_argument("dateien", nargs="+")
    p.add_argument("--orte", default="")
    p.add_argument("--dach", action="store_true")
    p.add_argument("--out", required=True, help="Dateiname ohne Endung")
    d = sub.add_parser("details")
    d.add_argument("--in", dest="inp", required=True)
    d.add_argument("--klassen", required=True)
    d.add_argument("--klassen-behalten", default="saas_b2b")
    d.add_argument("--bekannt", nargs="*", default=[])
    d.add_argument("--out", required=True)
    args = ap.parse_args()
    return prepare(args) if args.modus == "vorbereiten" else details(args)


if __name__ == "__main__":
    sys.exit(main())
