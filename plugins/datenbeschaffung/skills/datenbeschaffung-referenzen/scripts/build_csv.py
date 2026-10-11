#!/usr/bin/env python3
"""Rohdaten (Apify-Dataset-JSON) -> DAS eine CSV-Format (references/csv-spalten.md).

    python3 build_csv.py --in maps.json --quelle "apify:compass/crawler-google-places 2026-10-11" \
        --out leads-elektro-stuttgart-20261011.csv [--land de] [--keep spalte1,spalte2]

Versteht die Feldnamen der gepinnten Actors (Maps: title/website/emails/phone/city/categoryName,
totalScore/reviewsCount/placeId/reviewsTags/reviews/impressum; Outscraper: name/site/rating/
reviews/place_id/reviews_data; Impressum: company_name/email/phone_number/...; generisch:
email/company/...). Dedupliziert auf E-Mail (lowercase; ohne E-Mail auf Website bzw. Firma+Stadt),
normalisiert Firmennamen (companyClean), markiert Rollen-Adressen, fehlende Websites und fehlende
E-Mails in `hinweis`.

Zusatzspalten (references/datenumfang.md): Google-Maps-Zeilen bringen Bewertung, Anzahl, place_id,
Rezensions-Stichworte, bis zu fünf Rezensionstexte (ohne Namen der Verfasser) und den Inhaber aus
dem Impressum mit. Die Zusatzspalten der anderen Wege (linkedin_url, follower, bio, plattform, ...)
werden unter festen Namen durchgereicht; weitere Rohfelder nur mit --keep. Eine Zusatzspalte
erscheint nur, wenn mindestens eine Zeile einen Wert hat.

Zeilen OHNE E-Mail bleiben standardmäßig erhalten (`keine-email` in `hinweis`) — sie sind der
Input für die Impressum-/Kontaktseiten-Stufe. Erst die finale Übergabe-CSV läuft mit
--require-email (verwirft E-Mail-lose Zeilen, siehe references/csv-spalten.md).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime

FIELDS = ["email", "firstName", "lastName", "company", "website", "phoneNumber", "city",
          "kategorie", "quelle", "companyClean", "hinweis"]
ROLE_PREFIXES = ("info@", "kontakt@", "office@", "mail@", "hallo@", "hello@", "service@",
                 "kontakt.", "buero@", "zentrale@", "post@")
# Adressen, die nie die Versandadresse sein sollen, solange es eine andere gibt.
UNWANTED_PREFIXES = ("bewerbung", "jobs@", "job@", "karriere@", "career", "ausbildung@",
                     "datenschutz@", "privacy@", "noreply", "no-reply", "rechnung", "buchhaltung@",
                     "invoice", "abuse@", "webmaster@", "presse@", "press@")
# Die Rechtsform muss ein eigenes Wort sein (Trenner oder Whitespace davor) — sonst
# verstümmelt der Suffix-Match Namen wie "Freitag" (ag), "Krug" (ug), "Sonntag" (ag).
LEGAL_SUFFIX = re.compile(
    r"(?:\s*[|–-]\s*|\s+|^)(gmbh\s*&\s*co\.?\s*kg|gmbh|ug\s*\(haftungsbeschränkt\)|ug|ag|kg|ohg|gbr|e\.\s*k\.|e\.k\.|inh\..*)$",
    re.I)

# Google-Maps-Zusatzspalten. Die Namen sind die, die der Outreach-Import von selbst als
# Google-Felder erkennt (Bewertung mit Plattform „Google“, Rezensionsblock der Recherche).
GOOGLE_COLUMNS = ["rating", "reviews_count", "place_id", "reviews_tags", "google_rezensionstexte",
                  "inhaber", "inhaber_rolle"]
GOOGLE_MARKERS = ("placeId", "place_id", "google_place_id", "totalScore", "cid", "reviewsCount")

# Zusatzspalten der übrigen Wege: Zielspalte -> Quellschlüssel (der erste mit Wert gewinnt).
EXTRA_ALIASES: dict[str, tuple[str, ...]] = {
    "position": ("position", "jobTitle", "job_title"),
    "headline": ("headline",),
    "linkedin_url": ("linkedin_url", "linkedinUrl"),
    "connections": ("connections", "connectionsCount"),
    "mitarbeiter": ("mitarbeiter", "employees", "employeeCount", "estimated_num_employees"),
    "instagram_url": ("instagram_url", "instagramUrl"),
    "follower": ("follower", "followers", "followersCount"),
    "bio": ("bio", "biography"),
    "link_typ": ("link_typ",),
    "gefunden_via_hashtag": ("gefunden_via_hashtag",),
    "plattform": ("plattform", "platform"),
    "seller_url": ("seller_url", "sellerUrl"),
    "bewertung": ("bewertung",),
    "bewertungen_anzahl": ("bewertungen_anzahl",),
    "verkaeufe": ("verkaeufe",),
    "umsatz_geschaetzt": ("umsatz_geschaetzt", "estimated_sales"),
    "apps": ("apps",),
}

MAX_REVIEWS = 5  # so viele nimmt der Import je Lead (neueste zuerst)
REVIEW_TEXT_LIMIT = 500
REVIEW_TEXT_KEYS = ("textTranslated", "text", "review_text", "reviewText")
REVIEW_DATE_KEYS = ("publishedAtDate", "review_datetime_utc", "date")
REVIEW_STAR_KEYS = ("stars", "review_rating", "rating")
OWNER_ROLES = ("owner", "managing_director", "ceo", "founder")


def clean_company(name: str) -> str:
    base = name.split("|")[0].split("—")[0].split(" – ")[0].strip()
    prev = None
    while prev != base:
        prev = base
        base = LEGAL_SUFFIX.sub("", base).strip(" ,-")
    return base or name.strip()


def pick(row: dict, *keys: str) -> str:
    for k in keys:
        v = row.get(k)
        if isinstance(v, list):
            v = v[0] if v else None
        if v not in (None, ""):
            return str(v).strip()
    return ""


def scalar(value) -> str:
    """Zellwert: Zahlen ohne Nachkomma-Rauschen, Listen kommagetrennt, Objekte nie roh."""
    if value is None or isinstance(value, dict):
        return ""
    if isinstance(value, bool):
        return "ja" if value else "nein"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else f"{value:g}"
    if isinstance(value, list):
        return ", ".join(s for s in (scalar(v) for v in value) if s)
    return re.sub(r"\s+", " ", str(value)).strip()


def best_email(row: dict) -> str:
    """Versandadresse wählen: persönliche vor Rollen-Adresse, Bewerbungs-/Datenschutz-Adressen
    nur, wenn es keine andere gibt. Das Impressum (Maps-Kontaktanreicherung) ist Ersatzquelle."""
    candidates: list[str] = []
    for key in ("email", "emails"):
        value = row.get(key)
        for v in value if isinstance(value, list) else [value]:
            if isinstance(v, str):
                candidates.append(v)
    impressum = row.get("impressum") if isinstance(row.get("impressum"), dict) else {}
    for entry in impressum.get("emails") or []:
        if isinstance(entry, dict) and isinstance(entry.get("value"), str):
            candidates.append(entry["value"])
    seen: list[str] = []
    for c in candidates:
        c = c.strip().lower()
        if "@" in c and c not in seen:
            seen.append(c)
    if not seen:
        return ""

    def rank(address: str) -> int:
        if address.startswith(UNWANTED_PREFIXES):
            return 2
        return 1 if address.startswith(ROLE_PREFIXES) else 0

    return sorted(seen, key=rank)[0]


def review_date(value) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    for candidate in (text, text[:10]):
        try:
            return datetime.fromisoformat(candidate)
        except ValueError:
            continue
    try:
        return datetime.strptime(text[:10], "%m/%d/%Y")
    except ValueError:
        return None


def review_lines(reviews, limit: int) -> str:
    """Rezensionen ins Importformat „JJJJ-MM-TT · N★ · Text“, neueste zuerst, nur mit Text,
    ohne Namen der Verfasser (die Rohdaten werden nicht weitergereicht)."""
    if isinstance(reviews, str):
        return reviews.strip()
    if not isinstance(reviews, list):
        return ""
    parsed = []
    for review in reviews:
        if not isinstance(review, dict):
            continue
        text = scalar(pick(review, *REVIEW_TEXT_KEYS))
        if not text:
            continue
        if len(text) > REVIEW_TEXT_LIMIT:
            text = text[:REVIEW_TEXT_LIMIT].rstrip() + "…"
        date = review_date(pick(review, *REVIEW_DATE_KEYS))
        stars = pick(review, *REVIEW_STAR_KEYS)
        try:
            stars_int = max(1, min(5, round(float(stars)))) if stars else None
        except ValueError:
            stars_int = None
        parsed.append((date, stars_int, text))
    parsed.sort(key=lambda r: r[0].timestamp() if r[0] else 0, reverse=True)
    lines = []
    for date, stars, text in parsed[:limit]:
        parts = [date.strftime("%Y-%m-%d") if date else None, f"{stars}★" if stars else None, text]
        lines.append(" · ".join(p for p in parts if p))
    return "\n".join(lines)


def review_tags(value) -> str:
    if isinstance(value, list):
        parts = []
        for tag in value:
            if isinstance(tag, dict) and tag.get("title"):
                count = tag.get("count")
                parts.append(f"{tag['title']} ({count})" if isinstance(count, int) else str(tag["title"]))
            elif isinstance(tag, str) and tag.strip():
                parts.append(tag.strip())
        return ", ".join(parts)
    return scalar(value)


def owner(row: dict) -> tuple[str, str]:
    """Inhaber bzw. Geschäftsführer aus dem Impressum, das die Maps-Kontaktanreicherung
    ohnehin mitliest. Nur übernehmen, nie eigens beschaffen (die Recherche prüft ihn)."""
    impressum = row.get("impressum") if isinstance(row.get("impressum"), dict) else {}
    people = [p for p in impressum.get("people") or [] if isinstance(p, dict) and p.get("name")]
    if not people:
        return "", ""
    people.sort(key=lambda p: OWNER_ROLES.index(p.get("roleType")) if p.get("roleType") in OWNER_ROLES else len(OWNER_ROLES))
    return scalar(people[0].get("name")), scalar(people[0].get("role"))


def google_fields(row: dict, max_reviews: int) -> dict[str, str]:
    count = pick(row, "reviewsCount", "reviews_count", "google_reviews_count")
    if not count and not isinstance(row.get("reviews"), list):
        count = pick(row, "reviews")  # Outscraper: "reviews" ist die Anzahl
    # Fertiger Text nur aus google_rezensionstexte; "reviews"/"reviews_data" zählen nur als Liste
    # (bei Outscraper ist "reviews" die Anzahl, aus CSV/XLSX auch als Text).
    reviews = row.get("google_rezensionstexte") if isinstance(row.get("google_rezensionstexte"), (list, str)) \
        and row.get("google_rezensionstexte") else next(
            (row[k] for k in ("reviews", "reviews_data") if isinstance(row.get(k), list) and row[k]), None)
    name, role = owner(row)
    return {
        "rating": scalar(row.get("totalScore") if row.get("totalScore") is not None
                         else row.get("rating") if row.get("rating") is not None
                         else row.get("google_rating")),
        "reviews_count": scalar(int(float(count))) if re.fullmatch(r"\d+(\.0+)?", count or "") else "",
        "place_id": pick(row, "placeId", "place_id", "google_place_id"),
        "reviews_tags": review_tags(row.get("reviewsTags", row.get("reviews_tags"))),
        "google_rezensionstexte": review_lines(reviews, max_reviews) if reviews is not None else "",
        "inhaber": name,
        "inhaber_rolle": role,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quelle", required=True, help='z. B. "apify:compass/crawler-google-places 2026-10-11"')
    ap.add_argument("--land", help="nur Zeilen mit diesem countryCode behalten (de/at/ch)")
    ap.add_argument("--require-email", action="store_true",
                    help="Zeilen ohne E-Mail verwerfen — NUR für die finale Übergabe-CSV")
    ap.add_argument("--keep", default="",
                    help="weitere Rohfelder unverändert als Zusatzspalte mitnehmen (kommagetrennt)")
    ap.add_argument("--max-reviews", type=int, default=MAX_REVIEWS,
                    help=f"Rezensionstexte je Lead (Standard {MAX_REVIEWS}, so viele nutzt der Import)")
    args = ap.parse_args()
    keep = [k.strip() for k in args.keep.split(",") if k.strip()]

    with open(args.infile, encoding="utf-8") as fh:
        data = json.load(fh)

    out: dict[str, dict] = {}
    skipped_no_email = 0
    skipped_unusable = 0
    for row in data if isinstance(data, list) else [data]:
        if not isinstance(row, dict):
            continue
        if args.land and str(row.get("countryCode", "")).lower() not in (args.land.lower(), ""):
            continue
        is_google = any(row.get(k) not in (None, "") for k in GOOGLE_MARKERS)
        email = best_email(row)
        company = pick(row, "company", "title", "company_name", "companyName", "name")
        # Bei Maps ist "url" der Google-Maps-Link, nie die Website des Betriebs.
        website = pick(row, "website", "site", "target_url", "domain") if is_google \
            else pick(row, "website", "site", "url", "target_url", "domain")
        if website and "://" not in website:
            website = "https://" + website
        if not email:
            if args.require_email:
                skipped_no_email += 1
                continue
            if not website and not company:
                # weder anschreibbar noch anreicherbar — nutzlos
                skipped_unusable += 1
                continue
        # Dedup-Schlüssel: E-Mail; ohne E-Mail die Website (gleicher Betrieb doppelt
        # gescrapt), sonst Firma+Stadt.
        city = pick(row, "city") or pick(row.get("company_address") or {}, "city")
        key = email or (
            "site:" + re.sub(r"^https?://(www\.)?", "", website).rstrip("/").lower()
            if website else "co:" + company.lower() + "|" + city.lower()
        )
        if key in out:
            continue
        hints = []
        if email and email.startswith(ROLE_PREFIXES):
            hints.append("rollen-adresse")
        if not email:
            hints.append("keine-email")
        if not website:
            hints.append("keine-website")
        contact = row.get("contact_person") or {}
        record = {
            "email": email,
            "firstName": pick(contact, "first_name") or pick(row, "firstName", "first_name"),
            "lastName": pick(contact, "last_name") or pick(row, "lastName", "last_name"),
            "company": company,
            "website": website,
            "phoneNumber": pick(row, "phoneNumber", "phone", "phone_number", "phones"),
            "city": city,
            "kategorie": pick(row, "kategorie", "categoryName", "category", "type", "branche"),
            "quelle": args.quelle,
            "companyClean": clean_company(company) if company else "",
            "hinweis": "",
        }
        if is_google:
            google = google_fields(row, args.max_reviews)
            if record["firstName"] or record["lastName"]:
                google["inhaber"] = google["inhaber_rolle"] = ""
            if not google["google_rezensionstexte"]:
                hints.append("keine-rezensionstexte")
            record.update(google)
        for column, aliases in EXTRA_ALIASES.items():
            value = next((row[a] for a in aliases if row.get(a) not in (None, "", [])), None)
            if value is not None:
                record[column] = scalar(value)
        for column in keep:
            if column in row and column not in record:
                record[column] = scalar(row[column])
        record["hinweis"] = ";".join(hints)
        out[key] = record

    extras = [c for c in [*GOOGLE_COLUMNS, *EXTRA_ALIASES, *keep]
              if c not in FIELDS and any(r.get(c) for r in out.values())]
    columns = FIELDS + list(dict.fromkeys(extras))
    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(out.values())

    no_web = sum(1 for r in out.values() if "keine-website" in r["hinweis"])
    no_mail = sum(1 for r in out.values() if "keine-email" in r["hinweis"])
    roles = sum(1 for r in out.values() if "rollen-adresse" in r["hinweis"])
    report = (f"Leads: {len(out)} | ohne E-Mail (Impressum-Kandidaten): {no_mail} | "
              f"ohne Website: {no_web} | Rollen-Adressen: {roles}")
    google_rows = [r for r in out.values() if "rating" in r]
    if google_rows:
        report += (f" | Google: mit Bewertung {sum(1 for r in google_rows if r['rating'])}, "
                   f"mit Rezensionstext {sum(1 for r in google_rows if r['google_rezensionstexte'])}, "
                   f"mit Inhaber {sum(1 for r in google_rows if r['inhaber'])}")
    if extras:
        report += f" | Zusatzspalten: {', '.join(dict.fromkeys(extras))}"
    if skipped_no_email:
        report += f" | verworfen (--require-email): {skipped_no_email}"
    if skipped_unusable:
        report += f" | verworfen (weder E-Mail noch Website/Firma): {skipped_unusable}"
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
