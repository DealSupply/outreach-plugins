#!/usr/bin/env python3
"""Firmensitz und Adresse aus dem Impressum (kostenlos, lokal, ohne Apify).

    python3 sitz_check.py --in kandidaten.json --out geprueft.json [--nur-dach] [--parallel 16]

Liest je Zeile die Website (`website`), lädt Startseite und Impressum und ergänzt:
- `sitz_land` (DE, AT, CH oder leer), `sitz_plz` („20457 Hamburg“), `city` (falls leer)
- `emails`: alle Adressen von Impressum und Startseite (nur, wenn die Zeile keine hat); die
  Versandadresse wählt build_csv.py
- `produkt_signale`: preise, test, login, demo, saas (Hinweise auf ein Software-Produkt)
- `sitz_status`: ok, kein-sitz-erkannt, kein-impressum, nicht-erreichbar, keine-website

Als Anschrift zählt nur eine PLZ mit Straße davor (oder mit Länderkürzel wie CH-8001), das Land
entscheiden die Merkmale im Umfeld der Anschrift (HRB, Firmenbuch, Schweiz …).

--nur-dach behält Zeilen mit Sitz in DE, AT oder CH. Ohne erkannten Sitz bleiben nur Zeilen aus
Quellen mit gesichertem DACH-Sitz (`quellen` enthält linkedin oder startbase); reine
Verzeichnis-Zeilen (OMR) fallen dann heraus. Seiten, die das Impressum erst per JavaScript laden,
sind Kandidaten für impressum-enrichment.

Gedacht für Quellen ohne Sitzangabe (OMR Reviews, Google-Suche, LinkedIn-Standortsuche, die auch
Niederlassungen internationaler Konzerne liefert). Ruft je Domain höchstens zwei Seiten ab.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import html
import json
import re
import ssl
import sys
import time
import urllib.request
from urllib.parse import urljoin, urlparse

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/126 Safari/537.36",
           "Accept-Language": "de-DE,de;q=0.9,en;q=0.5"}
SIGNALS = {
    "preise": r"href=[\"'][^\"']*/(preise|pricing|prices|tarife|plans|pakete)\b|>\s*(Preise|Pricing|Tarife|Pakete)\s*<",
    "test": r"kostenlos testen|gratis testen|free trial|jetzt testen|try (it )?for free|testphase|start for free",
    "login": r">\s*(Login|Anmelden|Einloggen|Sign in|Log in)\s*<|href=[\"']https?://app\.|/login\b",
    "demo": r"demo (buchen|vereinbaren|anfragen|anfordern)|book a demo|request a demo|get a demo",
    "saas": r"\bSaaS\b|Software[- ]as[- ]a[- ]Service|cloudbasiert|cloud-basiert|cloud-based",
}
# Impressum-Links nach Vorrang: erst „impressum/imprint“, dann „legal notice“, zuletzt „legal“
# (das trifft auch /legal/privacy und wird deshalb nur genommen, wenn sonst nichts da ist).
IMPRINT_LINKS = [re.compile(r"href=[\"']([^\"']*(?:%s)[^\"']*)[\"']" % word, re.I)
                 for word in ("impressum|imprint", "legal-notice|legal_notice|legalnotice|rechtliches",
                              "legal")]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
BAD_EMAIL = re.compile(r"\.(png|jpe?g|svg|webp|gif)$|sentry|wixpress|example\.|domain\.", re.I)
# PLZ + Ort; das Länderkürzel davor entscheidet, sonst die Ländermerkmale in der Nähe der Adresse.
PLZ = re.compile(r"\b(D-|DE-|A-|AT-|CH-)?(\d{4,5})\s+([A-ZÄÖÜ][A-Za-zäöüß\-]+(?:\s(?:am|an der|im|bei|ob der|vor der)\s[A-ZÄÖÜ][a-zäöüß]+)?)")
# Eine echte Anschrift hat kurz vor der PLZ eine Straße mit Hausnummer („Eschelsweg 4 (1.OG)“,
# „Steinhöft 9 c/o …“) oder ein Feld „PLZ/Zip code“.
STREET = re.compile(r"[A-Za-zÄÖÜäöüß.\-]{3,}\s+\d{1,4}\s?[a-zA-Z]?\b|\b(zip|zip code|postal code|plz|postleitzahl)\b", re.I)
PHONE = re.compile(r"\b(tel|telefon|fon|phone|fax|mobil|hotline)\b", re.I)
NOT_A_PLACE = {"deutschland", "germany", "österreich", "austria", "schweiz", "switzerland", "kunden", "fax", "tel", "telefon", "geschäftsführer", "geschäftsführung", "united",
               "mitarbeiter", "nutzer", "unternehmen", "euro", "eur", "chf", "stück", "downloads",
               "e-mail", "email", "mail", "ust", "registergericht", "amtsgericht", "hrb", "sitz"}
MARK_DE = re.compile(r"Handelsregister|Amtsgericht|\bHRB\b|\bHRA\b|USt-?Id|Umsatzsteuer-Identifikations|Deutschland|Germany", re.I)
MARK_AT = re.compile(r"Firmenbuch|\bFN\s?\d|Österreich|Austria\b|\bATU\d", re.I)
MARK_ABROAD = re.compile(r"\b(France|Frankreich|United States|USA|United Kingdom|England|Nederland|"
                         r"Netherlands|Niederlande|España|Spain|Italia|Polska|Poland|Sweden|Denmark|Ireland)\b")
MARK_CH = re.compile(r"Schweiz|Switzerland|Suisse|Svizzera|\bCHE-\d|Handelsregisteramt", re.I)


def fetch(url: str, budget: float = 20.0) -> tuple[str, str]:
    """Seite laden; bricht nach `budget` Sekunden ab, auch wenn der Server tröpfelnd sendet."""
    try:
        res = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=12, context=CTX)
        charset = res.headers.get_content_charset() or "utf-8"
        start, chunks, size = time.monotonic(), [], 0
        while size < 800_000 and time.monotonic() - start < budget:
            chunk = res.read(65_536)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        try:
            return res.geturl(), b"".join(chunks).decode(charset, "ignore")
        except LookupError:
            return res.geturl(), b"".join(chunks).decode("utf-8", "ignore")
    except Exception:
        return "", ""


def text_of(page: str) -> str:
    page = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", page)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))


def country_and_place(text: str) -> tuple[str, str, str]:
    """(Land, PLZ, Ort) der ersten Anschrift im Text. Ländermerkmale zählen nur im Umfeld der
    Anschrift, das nächstgelegene entscheidet. So entscheiden weder „Kunden in Deutschland,
    Österreich und der Schweiz“ noch ein Sprachwähler im Footer."""
    for m in PLZ.finditer(text):
        prefix, plz, place = (m.group(1) or "").upper(), m.group(2), m.group(3).rstrip(".-")
        if place.lower() in NOT_A_PLACE:
            continue
        before = text[max(0, m.start() - 60):m.start()]
        if not prefix and (not STREET.search(before) or PHONE.search(before[-25:])):
            continue  # keine Straße davor: Kundenzahl, Telefonnummer, Registernummer
        if not prefix and MARK_ABROAD.search(text[m.end():m.end() + 40]):
            continue  # Anschrift im Ausland („75008 Paris, France“)
        lo = max(0, m.start() - 200)
        near = text[lo:m.end() + 200]
        dist = {}
        for land, rx in (("DE", MARK_DE), ("AT", MARK_AT), ("CH", MARK_CH)):
            spots = [abs(lo + x.start() - m.start()) for x in rx.finditer(near)]
            if spots:
                dist[land] = min(spots)
        if len(plz) == 4:
            if prefix.startswith("CH"):
                return "CH", plz, place
            if prefix.startswith("A"):
                return "AT", plz, place
            alpine = {k: v for k, v in dist.items() if k in ("AT", "CH")}
            if alpine and not (not prefix and 1990 <= int(plz) <= 2039 and min(alpine.values()) > 80):
                return min(alpine, key=alpine.get), plz, place
            continue
        if prefix.startswith("D") or "DE" in dist or not dist:
            # Fünfstellig mit Straße davor, ohne österreichisches oder Schweizer Merkmal in der
            # Nähe und ohne Auslandsangabe dahinter: deutsche Anschrift.
            return "DE", plz, place
    return "", "", ""


def check(row: dict) -> dict:
    site = row.get("website") or ""
    if not site:
        return {**row, "sitz_status": "keine-website"}
    if "://" not in site:
        site = "https://" + site
    final, home = fetch(site)
    if not home and site.startswith("https://"):
        final, home = fetch("http://" + site[8:])
    if not home:
        return {**row, "sitz_status": "nicht-erreichbar"}
    signals = [k for k, p in SIGNALS.items() if re.search(p, home, re.I)]
    imprint = ""
    link = next((m for m in (r.search(home) for r in IMPRINT_LINKS) if m), None)
    if link:
        _, imprint = fetch(urljoin(final or site, html.unescape(link.group(1))))
    land, plz, place = country_and_place(text_of(imprint or home))
    status = "ok" if land else "kein-impressum" if not imprint else "kein-sitz-erkannt"
    out = {**row, "sitz_land": land, "sitz_plz": f"{plz} {place}".strip(), "produkt_signale": ",".join(signals),
           "sitz_status": status}
    if place and not row.get("city"):
        out["city"] = place
    if not row.get("email") and not row.get("emails"):
        # Alle Adressen übergeben; die Versandadresse wählt build_csv.py (eigene Domain vor
        # fremder, persönliche vor Rollen-Adresse, nie bewerbung@ oder datenschutz@ zuerst).
        raw = html.unescape(imprint + " " + home).replace("[at]", "@").replace("(at)", "@")
        found = sorted({e.lower().rstrip(".") for e in EMAIL.findall(raw) if not BAD_EMAIL.search(e)})
        if found:
            out["emails"] = found
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="inp", required=True, help="JSON-Liste mit `website` je Zeile")
    ap.add_argument("--out", required=True)
    ap.add_argument("--nur-dach", action="store_true")
    ap.add_argument("--parallel", type=int, default=16)
    args = ap.parse_args()

    rows = json.load(open(args.inp, encoding="utf-8"))
    done: list[dict] = []
    with cf.ThreadPoolExecutor(args.parallel) as pool:
        for i, r in enumerate(pool.map(check, rows), 1):
            done.append(r)
            if i % 200 == 0:
                print(f"  {i}/{len(rows)} geprüft", file=sys.stderr, flush=True)
    stats: dict[str, int] = {}
    for r in done:
        key = r.get("sitz_land") or ("unbekannt" if r.get("sitz_status") == "ok" else r.get("sitz_status"))
        stats[key] = stats.get(key, 0) + 1
    def dach(r: dict) -> bool:
        # Ohne erkannten Sitz bleiben Firmen aus Quellen mit gesichertem DACH-Sitz erhalten
        # (LinkedIn-Sitzfilter, Startbase); nur reine Verzeichnis-Zeilen (OMR) fliegen raus.
        if r.get("sitz_land") in ("DE", "AT", "CH"):
            return True
        return not r.get("sitz_land") and any(q in (r.get("quellen") or "") for q in ("linkedin", "startbase"))
    keep = [r for r in done if dach(r)] if args.nur_dach else done
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(keep, fh, ensure_ascii=False, indent=1)
    mail = sum(1 for r in keep if r.get("email") or r.get("emails"))
    print(f"Geprüft {len(done)} | Sitz/Status: {stats} | behalten {len(keep)}, davon mit E-Mail {mail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
