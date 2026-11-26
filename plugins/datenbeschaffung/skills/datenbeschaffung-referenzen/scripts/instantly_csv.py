#!/usr/bin/env python3
"""Fertige Lead-Liste (csv-spalten.md) -> Datei für den CSV-Import einer Instantly-Kampagne.

    python3 instantly_csv.py --in leads-final.csv --out instantly-<nische>-<datum>.csv \
        [--keine-namen-aus-inhaber]

Für den Weg ohne DealSupply oder den direkten Import in Instantly (references/ohne-dealsupply.md).
Regeln aus der Hilfe von Instantly (Stand 26.11.2026): E-Mail ist Pflicht, die Datei ist UTF-8,
Spaltennamen beginnen mit einem Großbuchstaben, höchstens 20 Zeichen, keine Sonderzeichen, keine
Wahrheitswerte (true/false); eine Zusatzspalte wird zur eigenen Variable `{{Spaltenname}}`.

- Die Kernspalten heißen wie die festen Felder von Instantly (Email, FirstName, LastName,
  CompanyName, Website, Phone, JobTitle, LinkedIn); beim Import ordnet man sie diesen Feldern zu.
- Alle übrigen Spalten mit Einstieg werden eigene Variablen mit deutschem Namen (Firma, Stadt,
  GoogleBewertung, Rezensionstexte, Plattform, Follower …). Interne Spalten (quelle, hinweis,
  place_id, inhaber_rolle, connections, link_typ, gefunden_via_hashtag) fallen weg.
- Fehlen Vor- und Nachname, aber steht ein Inhaber aus dem Impressum da, wird er nur dann zu
  FirstName/LastName, wenn er eindeutig aus Vorname und Nachname besteht (Titel wie Dr. werden
  abgezogen). Mehrere Namen, Firmennamen oder unklare Formen bleiben leer; der Name steht dann nur
  in der Variable Inhaber. --keine-namen-aus-inhaber schaltet das ab.
- Zeilen ohne E-Mail kann Instantly nicht einlesen: Sie fallen weg und werden gezählt.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys

CORE = {"email": "Email", "firstName": "FirstName", "lastName": "LastName", "company": "CompanyName",
        "website": "Website", "phoneNumber": "Phone", "position": "JobTitle", "linkedin_url": "LinkedIn"}
CUSTOM = {"companyClean": "Firma", "city": "Stadt", "kategorie": "Kategorie", "inhaber": "Inhaber",
          "rating": "GoogleBewertung", "reviews_count": "GoogleRezensionen",
          "reviews_tags": "RezensionStichworte", "google_rezensionstexte": "Rezensionstexte",
          "headline": "Headline", "mitarbeiter": "Mitarbeiter", "instagram_url": "Instagram",
          "follower": "Follower", "bio": "Bio", "plattform": "Plattform", "seller_url": "ShopProfil",
          "bewertung": "Bewertung", "bewertungen_anzahl": "BewertungenAnzahl",
          "verkaeufe": "Verkaufszahl", "umsatz_geschaetzt": "Umsatz", "apps": "Apps"}
DROP = {"quelle", "hinweis", "place_id", "inhaber_rolle", "connections", "link_typ",
        "gefunden_via_hashtag"}
# Was Instantly beim Import dafür anbietet (Feldnamen aus der Hilfe von Instantly).
TARGET = {"Email": "Email", "FirstName": "First name", "LastName": "Last name",
          "CompanyName": "Company name", "Website": "Website", "Phone": "Phone",
          "JobTitle": "Job title", "LinkedIn": "LinkedIn"}
TITLE_WORDS = {"dr", "prof", "mag", "ing", "msc", "bsc", "mba", "herr", "frau", "med", "rer", "nat",
               "phil", "jur", "oec", "hc"}
LEGAL = {"gmbh", "ag", "kg", "ug", "ohg", "gbr", "mbh", "co", "ek", "e.k.", "se", "ltd", "inc", "llc"}
NAME = re.compile(r"^[A-ZÄÖÜÀ-Þ][a-zäöüßà-ÿ]+(?:-[A-ZÄÖÜÀ-Þ][a-zäöüßà-ÿ]+)?$")
UMLAUT = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss"})


def is_title(token: str) -> bool:
    key = re.sub(r"[.\-]", "", token.lower())
    return key in TITLE_WORDS or key.startswith("dipl") or token.endswith(".")


def split_owner(owner: str) -> tuple[str, str]:
    """Inhaber -> (Vorname, Nachname), nur bei eindeutiger Form, sonst ("", "")."""
    owner = (owner or "").strip()
    if not owner or re.search(r",|&|/|\bund\b|\band\b|\(", owner, re.I):
        return "", ""
    tokens = [t for t in owner.split() if not is_title(t)]
    if len(tokens) != 2 or any(t.lower().strip(".") in LEGAL for t in tokens):
        return "", ""
    if not all(NAME.match(t) for t in tokens):
        return "", ""
    return tokens[0], tokens[1]


def header_for(column: str, taken: set[str]) -> str:
    """Spaltenname für eine weitere Variable: Großbuchstabe vorn, nur Buchstaben und Ziffern."""
    parts = re.split(r"[^0-9A-Za-z]+", column.translate(UMLAUT))
    name = "".join(p[:1].upper() + p[1:] for p in parts if p)[:20] or "Feld"
    if not name[0].isalpha():
        name = ("F" + name)[:20]
    base, n = name, 2
    while name in taken:
        name = f"{base[:18]}{n}"
        n += 1
    return name


def value(text: str) -> str:
    text = (text or "").strip()
    return {"true": "ja", "false": "nein"}.get(text.lower(), text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--keine-namen-aus-inhaber", action="store_true")
    args = ap.parse_args()

    with open(args.infile, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    if "email" not in fields:
        print("FEHLER: Spalte email fehlt (Format csv-spalten.md)", file=sys.stderr)
        return 2

    mapping: dict[str, str] = {}
    taken: set[str] = set()
    for col in fields:
        if col in DROP:
            continue
        target = CORE.get(col) or CUSTOM.get(col) or header_for(col, taken | set(CORE.values()))
        if target in taken:
            continue
        mapping[col] = target
        taken.add(target)
    for col in ("firstName", "lastName"):  # immer da, damit die Zuordnung gleich bleibt
        if col not in mapping:
            mapping[col] = CORE[col]
    used = [c for c in mapping if c in CORE or any((r.get(c) or "").strip() for r in rows)]
    order = [c for c in CORE if c in used] + [c for c in used if c not in CORE]
    if len(order) > 50:
        print(f"FEHLER: {len(order)} Spalten, Instantly nimmt höchstens 50 Variablen je Import",
              file=sys.stderr)
        return 2

    out, no_email, from_source, from_owner = [], 0, 0, 0
    for row in rows:
        if "@" not in (row.get("email") or ""):
            no_email += 1
            continue
        record = {mapping[c]: value(row.get(c, "")) for c in order}
        if record["FirstName"]:
            from_source += 1
        elif not args.keine_namen_aus_inhaber and not record.get("LastName"):
            first, last = split_owner(row.get("inhaber", ""))
            if first:
                record["FirstName"], record["LastName"] = first, last
                from_owner += 1
        out.append(record)

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=[mapping[c] for c in order])
        writer.writeheader()
        writer.writerows(out)

    print(f"Instantly-Datei: {len(out)} Leads | ohne E-Mail weggelassen: {no_email} | "
          f"mit Vorname: {from_source + from_owner} (aus der Quelle {from_source}, aus dem Inhaber "
          f"{from_owner}) | ohne Vorname: {len(out) - from_source - from_owner}")
    print("Zuordnung beim Import: " + ", ".join(
        f"{mapping[c]} → {TARGET.get(mapping[c], 'Custom variable')}" for c in order))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
