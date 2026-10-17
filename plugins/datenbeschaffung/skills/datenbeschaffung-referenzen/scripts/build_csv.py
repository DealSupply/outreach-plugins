#!/usr/bin/env python3
"""Rohdaten (Apify-Dataset-JSON) -> DAS eine CSV-Format (references/csv-spalten.md).

    python3 build_csv.py --in maps.json --quelle "apify:compass/crawler-google-places 2026-10-11" \
        --out leads-elektro-stuttgart-20261011.csv [--land de] [--keep spalte1,spalte2]
        [--uebergabe kontakt|email] [--verworfen verworfen.csv]

--in nimmt ein Apify-Dataset (JSON) oder eine CSV (z. B. domains.csv aus process_serp.py).

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

Zeilen OHNE E-Mail bleiben standardmäßig erhalten (`keine-email` in `hinweis`): Sie sind der
Input für die optionale Impressum-/Kontaktseiten-Stufe. Die finale Übergabe-CSV läuft mit
--uebergabe (references/csv-spalten.md, references/plattform-hosts.md):
  kontakt  ab ListM8 MCP 3.0.0: E-Mail ODER eigene Website. Zeilen nur mit Plattform-Link
           (Instagram, Linktree, Branchenportal …) oder ganz ohne Kontaktmerkmal fliegen raus.
  email    ältere Server: nur Zeilen mit E-Mail (gleich dem früheren --require-email).
Verworfene Zeilen schreibt --verworfen mit Spalte `grund` in eine eigene CSV.
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import pathlib
import re
from datetime import datetime
from urllib.parse import urlparse

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
FREEMAIL = {"gmail.com", "googlemail.com", "gmx.de", "gmx.net", "gmx.at", "gmx.ch", "web.de",
            "t-online.de", "yahoo.de", "yahoo.com", "outlook.com", "outlook.de", "hotmail.com",
            "hotmail.de", "live.de", "icloud.com", "me.com", "aol.com", "freenet.de", "posteo.de",
            "mail.de", "online.de", "arcor.de", "bluewin.ch", "gmx.ch"}
JUNK_DOMAINS = {"mysite.com", "example.com", "example.de", "example.org", "domain.com", "domain.de",
                "beispiel.de", "musterfirma.de", "ihre-domain.de", "email.com", "sentry.io",
                "wixpress.com", "sentry-next.wixpress.com"}
UMLAUTS = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
# Website-Baukästen: Kunden-Websites auf Subdomains sind echte Betriebe (wie process_serp.py).
BUILDER_PLATFORMS = {"jimdo.com", "jimdosite.com", "wordpress.com", "wix.com", "wixsite.com",
                     "weebly.com", "webnode.com", "webador.de", "shopify.com", "myshopify.com"}
REJECTED_FIELDS = ["grund", "email", "company", "website", "city", "quelle"]
# Hinweise, die build_csv.py bei jedem Lauf selbst neu berechnet.
COMPUTED_HINTS = {"portal-website", "rollen-adresse", "fremde-domain", "keine-email",
                  "nur-plattform-url", "keine-website", "keine-rezensionstexte"}


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
        if isinstance(v, dict):  # z. B. LinkedIn: {"number": …}
            v = v.get("number") or v.get("value")
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


def load_noise() -> tuple[set[str], list[str]]:
    """Portale aus references/noise-domains.md (dieselbe Liste wie process_serp.py)."""
    path = pathlib.Path(__file__).resolve().parent.parent / "references/noise-domains.md"
    if not path.exists():
        return set(), []
    text = path.read_text(encoding="utf-8")
    domains = set(re.findall(r"\b([a-z0-9][a-z0-9.-]+\.[a-z]{2,})\b", text))
    patterns = re.findall(r"\b([a-z0-9][a-z0-9*.-]*\*[a-z0-9*.-]*\.[a-z]{2,})\b", text)
    return domains, patterns


NOISE, NOISE_PATTERNS = load_noise()


def load_platforms() -> tuple[set[str], set[str], list[str]]:
    """Profil-Plattformen, Baukästen und Marken aus references/plattform-hosts.md (Spiegel der
    Server-Liste; maßgeblich bleibt der Server)."""
    path = pathlib.Path(__file__).resolve().parent.parent / "references/plattform-hosts.md"
    hosts: set[str] = set()
    builders: set[str] = set()
    brands: list[str] = []
    if not path.exists():
        return hosts, builders, brands
    section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line.lower()
        elif line.startswith("- "):
            value = line[2:].strip().lower()
            if "profil" in section:
                hosts.add(value)
            elif "marken" in section:
                brands.append(value)
            elif "baukäst" in section:
                builders.add(value)
    return hosts, builders, brands


PLATFORM_HOSTS, PLATFORM_BUILDERS, PLATFORM_BRANDS = load_platforms()


def host_of(website: str) -> str:
    host = (urlparse(website if "://" in website else "https://" + website).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def is_portal(host: str) -> bool:
    if not host:
        return False
    if host in NOISE or any(fnmatch.fnmatch(host, p) for p in NOISE_PATTERNS):
        return True
    return any(host.endswith("." + n) for n in NOISE if n not in BUILDER_PLATFORMS)


def is_platform(host: str) -> bool:
    """Ein Profil-Link statt eigener Website: Profil-Plattform (samt Subdomains), Markendomain
    oder die Baukasten-Domain selbst. Baukasten-Subdomains (praxis.jimdosite.com) zählen als
    eigene Website."""
    if not host:
        return False
    if any(host == p or host.endswith("." + p) for p in PLATFORM_HOSTS):
        return True
    if host in PLATFORM_BUILDERS:
        return True
    return any(re.search(r"(?:^|\.)" + re.escape(b) + r"\.(?:[a-z]{2,3}\.)?[a-z]{2,}$", host)
               for b in PLATFORM_BRANDS)


def base_label(domain: str) -> str:
    """Name der Domain ohne Endung, Umlaute ausgeschrieben: xn--schtze-...de und schuetze-...de,
    touch5.net und touch5.de gelten als dieselbe Firma."""
    labels = domain.split(".")
    label = labels[-2] if len(labels) >= 2 else labels[0]
    if label.startswith("xn--"):
        try:
            label = label.encode("ascii").decode("idna")
        except UnicodeError:
            pass
    return label.translate(UMLAUTS)


def same_domain(address: str, host: str) -> bool:
    domain = address.rsplit("@", 1)[-1]
    if not host:
        return False
    return (domain == host or domain.endswith("." + host) or host.endswith("." + domain)
            or base_label(domain) == base_label(host))


def is_freemail(address: str) -> bool:
    return address.rsplit("@", 1)[-1] in FREEMAIL


def is_junk(address: str) -> bool:
    """Platzhalter aus Website-Vorlagen, technische Absender und ungültige Adressen (Umlaute vor
    dem @ kommen aus geratenen Namensmustern und sind nie zustellbar)."""
    domain = address.rsplit("@", 1)[-1]
    if not address.isascii() or not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,24}", address):
        return True
    return domain in JUNK_DOMAINS or any(domain.endswith("." + j) for j in JUNK_DOMAINS)


def normalize(row: dict) -> dict:
    """Rohformen der Anbieter auf die generischen Schlüssel bringen (Feldnamen aus echten
    Läufen vom 11.10.2026). Nur ergänzen, nie Vorhandenes überschreiben."""
    r = dict(row)

    def put(key: str, value) -> None:
        if value not in (None, "", []) and r.get(key) in (None, "", []):
            r[key] = value

    if isinstance(r.get("emails"), str):  # Impressum-Actors liefern Adressen als Text
        r["emails"] = [e for e in re.split(r"[,;\s]+", r["emails"]) if e]
    if "username" in r and "followersCount" in r:  # Instagram-Profil
        put("instagram_url", r.get("url") or f"https://www.instagram.com/{r['username']}/")
        r.pop("url", None)
        put("website", r.get("externalUrl"))
        put("company", r.get("fullName") or r["username"])
        put("kategorie", r.get("businessCategoryName"))
    positions = r.get("currentPositions")
    if isinstance(positions, list) and positions and isinstance(positions[0], dict):  # LinkedIn-Person
        put("position", positions[0].get("title"))
        put("company", positions[0].get("companyName"))
        r.pop("url", None)
    if "organizationName" in r:  # B2B-Datenbank in Apollo-Form
        put("company", r.get("organizationName"))
        put("position", r.get("title"))
        put("website", r.get("organizationWebsite"))
        put("city", r.get("organizationCity"))
        put("kategorie", r.get("organizationIndustry"))
        put("mitarbeiter", r.get("organizationEmployeeRange"))
        guess = str(r.get("emailPatternGuess") or "").strip().lower()
        if guess and guess == str(r.get("email") or "").strip().lower():
            r["_geraten"] = True
    if "universalName" in r and isinstance(r.get("locations"), list):  # LinkedIn-Firma
        put("company", r.get("name"))
        industries = r.get("industries") or []
        if industries and isinstance(industries[0], dict):
            put("kategorie", industries[0].get("name"))
        put("mitarbeiter", r.get("employeeCount"))
        hq = next((x for x in r["locations"] if isinstance(x, dict) and x.get("headquarter")), {})
        put("city", hq.get("city"))
    put("inhaber", r.get("managingDirector"))  # Impressum-Actor
    return r


def best_email(row: dict, host: str) -> str:
    """Versandadresse wählen: Adresse der eigenen Domain vor fremder (Webagentur, Portal),
    persönliche vor Rollen-Adresse, Bewerbungs-/Datenschutz-Adressen nur ohne Alternative.
    Das Impressum (Maps-Kontaktanreicherung) ist Ersatzquelle, aber nur mit eigener Domain oder
    Freemail (eine fremde Firmen-Domain im Impressum ist meist die Webagentur)."""
    candidates: list[str] = []
    for key in ("email", "emails"):
        value = row.get(key)
        for v in value if isinstance(value, list) else [value]:
            if isinstance(v, str):
                candidates.append(v.strip().lower())
    impressum = row.get("impressum") if isinstance(row.get("impressum"), dict) else {}
    for entry in impressum.get("emails") or []:
        if isinstance(entry, dict) and isinstance(entry.get("value"), str):
            address = entry["value"].strip().lower()
            if same_domain(address, host) or is_freemail(address):
                candidates.append(address)
    seen: list[str] = []
    for c in candidates:
        if "@" in c and c not in seen and not is_junk(c):
            seen.append(c)
    if not seen:
        return ""

    def rank(address: str) -> tuple[int, int]:
        # Eigene Domain zuerst, dann Freemail (im Handwerk üblich), zuletzt fremde Firmen-Domains.
        foreign = 0 if not host or same_domain(address, host) else 1 if is_freemail(address) else 2
        if address.startswith(UNWANTED_PREFIXES):
            return foreign, 2
        return foreign, 1 if address.startswith(ROLE_PREFIXES) else 0

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
    # Nur Inhaber, Geschäftsführung, Gründer: „redaktionell verantwortlich“ o. Ä. ist oft
    # eine Agentur oder ein Portal, nie der Ansprechpartner.
    people = [p for p in impressum.get("people") or []
              if isinstance(p, dict) and p.get("name") and p.get("roleType") in OWNER_ROLES]
    if not people:
        # Eine schon gebaute CSV (zweiter Durchlauf zur Übergabe) trägt den Inhaber als Spalte.
        return scalar(row.get("inhaber")), scalar(row.get("inhaber_rolle"))
    people.sort(key=lambda p: OWNER_ROLES.index(p["roleType"]))
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


def rejection(mode: str | None, website: str, platform_only: bool) -> str:
    """Grund, warum eine Zeile ohne E-Mail nicht in die Übergabe-CSV darf ("" = behalten)."""
    if mode == "email":
        return "keine-email"
    if mode == "kontakt" and (not website or platform_only):
        return "nur-plattform-url" if platform_only else "kein-kontaktmerkmal"
    return ""


SERP_ONLY_COLUMNS = ("titel", "query", "domain")


def load_rows(path: str) -> tuple[list, list[str]]:
    """Apify-Dataset (JSON) oder CSV, dazu die Zusatzspalten einer CSV (die bleiben erhalten, auch
    wenn eine schon gebaute CSV für die Übergabe noch einmal durchläuft). Bei SERP-Domains
    (process_serp.py) zählen domain/website; der Suchtitel wird nie Firmenname (zu unzuverlässig)."""
    if path.lower().endswith(".csv"):
        with open(path, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = [dict(r) for r in reader]
            header = list(reader.fieldnames or [])
        for r in rows:
            r.pop("titel", None)
            r.pop("query", None)
        extra = [c for c in header if c not in FIELDS and c not in GOOGLE_COLUMNS
                 and c not in EXTRA_ALIASES and c not in SERP_ONLY_COLUMNS]
        return rows, extra
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return (data if isinstance(data, list) else [data]), []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quelle", required=True, help='z. B. "apify:compass/crawler-google-places 2026-10-11"')
    ap.add_argument("--land", help="nur Zeilen mit diesem countryCode behalten (de/at/ch)")
    ap.add_argument("--uebergabe", choices=["kontakt", "email"],
                    help="finale Übergabe-CSV: kontakt = E-Mail oder eigene Website (ListM8 >= 3.0.0), "
                         "email = nur Zeilen mit E-Mail (ältere Server)")
    ap.add_argument("--require-email", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--verworfen", help="verworfene Zeilen mit Spalte grund in diese CSV schreiben")
    ap.add_argument("--keep", default="",
                    help="weitere Rohfelder unverändert als Zusatzspalte mitnehmen (kommagetrennt)")
    ap.add_argument("--max-reviews", type=int, default=MAX_REVIEWS,
                    help=f"Rezensionstexte je Lead (Standard {MAX_REVIEWS}, so viele nutzt der Import)")
    args = ap.parse_args()
    keep = [k.strip() for k in args.keep.split(",") if k.strip()]
    mode = "email" if args.require_email else args.uebergabe

    data, csv_extra = load_rows(args.infile)
    keep = list(dict.fromkeys([*keep, *csv_extra]))

    out: dict[str, dict] = {}
    rejected: list[dict] = []
    skipped_unusable = 0
    for row in data:
        if not isinstance(row, dict):
            continue
        row = normalize(row)
        if args.land and str(row.get("countryCode", "")).lower() not in (args.land.lower(), ""):
            continue
        is_google = any(row.get(k) not in (None, "") for k in GOOGLE_MARKERS)
        company = pick(row, "company", "title", "company_name", "companyName", "name", "produkt")
        # Bei Maps ist "url" der Google-Maps-Link, nie die Website des Betriebs.
        website = pick(row, "website", "site", "target_url", "domain") if is_google \
            else pick(row, "website", "site", "url", "target_url", "domain")
        if website and "://" not in website:
            website = "https://" + website
        host = host_of(website) if website else ""
        portal = is_portal(host)
        platform_only = portal or is_platform(host)
        raw_website = website
        if portal:
            # Eintrag auf einem Branchenportal: Adresse und Impressum gehören dem Portal.
            website, host, email = "", "", ""
        else:
            email = best_email(row, host)
        city = pick(row, "city") or pick(row.get("company_address") or {}, "city")
        if not email:
            grund = rejection(mode, website, platform_only)
            if grund:
                rejected.append({"grund": grund, "email": "", "company": company, "website": raw_website,
                                 "city": city, "quelle": args.quelle})
                continue
            if not website and not company:
                # weder anschreibbar noch anreicherbar — nutzlos
                skipped_unusable += 1
                continue
        # Dedup-Schlüssel: E-Mail; ohne E-Mail die Website (gleicher Betrieb doppelt
        # gescrapt), sonst Firma+Stadt.
        key = email or (
            "site:" + re.sub(r"^https?://(www\.)?", "", website).rstrip("/").lower()
            if website else "co:" + company.lower() + "|" + city.lower()
        )
        if key in out:
            continue
        hints = ["portal-website"] if portal else []
        if email and email.startswith(ROLE_PREFIXES):
            hints.append("rollen-adresse")
        if email and host and not same_domain(email, host) and not is_freemail(email):
            hints.append("fremde-domain")
        if email and row.get("_geraten"):
            hints.append("geratene-adresse")
        if not email:
            hints.append("keine-email")
            if platform_only and not portal:
                hints.append("nur-plattform-url")
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
            if portal or record["firstName"] or record["lastName"]:
                google["inhaber"] = google["inhaber_rolle"] = ""
            if not google["google_rezensionstexte"]:
                hints.append("keine-rezensionstexte")
            record.update(google)
        elif row.get("inhaber") and not (record["firstName"] or record["lastName"]):
            record["inhaber"] = scalar(row["inhaber"])
        for column, aliases in EXTRA_ALIASES.items():
            value = next((row[a] for a in aliases if row.get(a) not in (None, "", [])), None)
            if value is not None:
                record[column] = scalar(value)
        for column in keep:
            if column in row and column not in record:
                record[column] = scalar(row[column])
        # Fremde Hinweise einer schon gebauten CSV (z. B. adresse-verworfen) bleiben erhalten.
        earlier = [h for h in str(row.get("hinweis") or "").split(";") if h and h not in COMPUTED_HINTS]
        record["hinweis"] = ";".join(dict.fromkeys([*earlier, *hints]))
        out[key] = record

    extras = [c for c in [*GOOGLE_COLUMNS, *EXTRA_ALIASES, *keep]
              if c not in FIELDS and any(r.get(c) for r in out.values())]
    columns = FIELDS + list(dict.fromkeys(extras))
    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(out.values())

    if args.verworfen and rejected:
        with open(args.verworfen, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=REJECTED_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rejected)

    no_web = sum(1 for r in out.values() if "keine-website" in r["hinweis"])
    no_mail = sum(1 for r in out.values() if "keine-email" in r["hinweis"])
    only_platform = sum(1 for r in out.values() if "nur-plattform-url" in r["hinweis"])
    roles = sum(1 for r in out.values() if "rollen-adresse" in r["hinweis"])
    portals = sum(1 for r in out.values() if "portal-website" in r["hinweis"])
    foreign = sum(1 for r in out.values() if "fremde-domain" in r["hinweis"])
    guessed = sum(1 for r in out.values() if "geratene-adresse" in r["hinweis"])
    no_mail_label = ("ohne E-Mail, mit eigener Website (Recherche sucht die Adresse)" if mode == "kontakt"
                     else "ohne E-Mail (Impressum-Kandidaten)")
    report = (f"Leads: {len(out)} | {no_mail_label}: {no_mail} | "
              f"ohne Website: {no_web} (davon Portal statt eigener Website: {portals}) | "
              f"Rollen-Adressen: {roles} | Adresse fremder Domain: {foreign}")
    if guessed:
        report += f" | geratene Adressen (vor Import verifizieren): {guessed}"
    google_rows = [r for r in out.values() if "rating" in r]
    if google_rows:
        report += (f" | Google: mit Bewertung {sum(1 for r in google_rows if r['rating'])}, "
                   f"mit Rezensionstext {sum(1 for r in google_rows if r['google_rezensionstexte'])}, "
                   f"mit Inhaber {sum(1 for r in google_rows if r['inhaber'])}")
    if extras:
        report += f" | Zusatzspalten: {', '.join(dict.fromkeys(extras))}"
    if only_platform:
        report += f" | ohne E-Mail, nur Plattform-Link: {only_platform}"
    if rejected:
        counts: dict[str, int] = {}
        for r in rejected:
            counts[r["grund"]] = counts.get(r["grund"], 0) + 1
        report += f" | verworfen (--uebergabe {mode}): {len(rejected)} (" + ", ".join(
            f"{g} {n}" for g, n in sorted(counts.items())) + ")"
    if skipped_unusable:
        report += f" | verworfen (weder E-Mail noch Website/Firma): {skipped_unusable}"
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
