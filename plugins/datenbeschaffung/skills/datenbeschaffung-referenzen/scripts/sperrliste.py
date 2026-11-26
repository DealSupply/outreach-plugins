#!/usr/bin/env python3
"""Sperrliste aus dem eigenen CRM: Bestandskunden, Ex-Kunden, Abmeldungen, Wettbewerber.

    python3 sperrliste.py --crm kunden.csv [--crm abmeldungen.csv] [--zusatz "wettbewerber.de,x@gmail.com"] \
        --blocklist instantly-blocklist.csv [--in leads.csv --out leads-ohne-sperre.csv]

Für den Weg ohne DealSupply (references/ohne-dealsupply.md). Liest einen oder mehrere
CRM-Exporte (CSV mit beliebigen Spalten) und baut daraus:

  --blocklist  die Datei für die Blocklist von Instantly: Spalte `Blocked`, je Zeile eine Domain
               (ohne @) oder eine Adresse. Firmenadressen werden zur Domain (sperrt die ganze
               Firma), private Postfächer (gmail.com, gmx.de, …) bleiben als einzelne Adresse.
  --in/--out   die eigene Lead-Liste ohne gesperrte Zeilen: gesperrt ist eine Zeile, deren Adresse
               gesperrt ist oder deren Website- bzw. Adress-Domain eine gesperrte Domain ist
               (auch als Subdomain: filiale.kunde.de trifft kunde.de).

Spalten erkennt das Skript am Namen (E-Mail: email, e-mail, mail; Website: website, url, domain,
webseite, homepage). --email-spalten/--domain-spalten überschreiben das. Mehrere Adressen in
einer Zelle (Komma, Semikolon, Leerzeichen) werden getrennt.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from urllib.parse import urlparse

# Wie build_csv.py: private Postfächer sperren nie die ganze Domain.
FREEMAIL = {"gmail.com", "googlemail.com", "gmx.de", "gmx.net", "gmx.at", "gmx.ch", "web.de",
            "t-online.de", "yahoo.de", "yahoo.com", "outlook.com", "outlook.de", "hotmail.com",
            "hotmail.de", "live.de", "icloud.com", "me.com", "aol.com", "freenet.de", "posteo.de",
            "mail.de", "online.de", "arcor.de", "bluewin.ch"}
# Profil- und CRM-Links in einer URL-Spalte sind keine Firmen-Domain.
NOT_A_COMPANY = {"linkedin.com", "xing.com", "instagram.com", "facebook.com", "twitter.com", "x.com",
                 "youtube.com", "tiktok.com", "google.com", "close.com", "hubspot.com", "pipedrive.com"}
EMAIL_HEADERS = ("email", "e-mail", "e_mail", "mail")
DOMAIN_HEADERS = ("website", "webseite", "homepage", "url", "domain")
ADDRESS = re.compile(r"[^\s,;<>\"']+@[^\s,;<>\"']+\.[a-z]{2,}", re.I)


def host_key(value: str | None) -> str:
    """Domain ohne Protokoll, Pfad und `www.`; Umlaut-Domains als Punycode."""
    value = (value or "").strip().lower()
    if not value or "@" in value:
        return ""
    try:
        host = urlparse(value if "://" in value else f"http://{value}").hostname or ""
    except ValueError:
        host = ""
    host = host.rstrip(".").removeprefix("www.")
    if "." not in host:
        return ""
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError:
        pass
    return host


def addresses(cell: str | None) -> list[str]:
    return [a.lower().rstrip(".") for a in ADDRESS.findall(cell or "")]


def is_freemail(address: str) -> bool:
    return address.rsplit("@", 1)[-1] in FREEMAIL


def columns(fields: list[str], wanted: str | None, hints: tuple[str, ...]) -> list[str]:
    if wanted is not None:
        names = [w.strip() for w in wanted.split(",") if w.strip()]
        return [f for f in fields if f in names]
    return [f for f in fields if any(h in f.strip().lower() for h in hints)]


def blocked(domain: str, domains: set[str]) -> bool:
    """Gleiche Domain oder Subdomain einer gesperrten Domain."""
    labels = domain.split(".")
    return any(".".join(labels[i:]) in domains for i in range(len(labels) - 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--crm", action="append", default=[], help="CRM-Export als CSV, mehrfach möglich")
    ap.add_argument("--zusatz", default="", help="weitere Domains oder Adressen, kommagetrennt")
    ap.add_argument("--email-spalten", help="Spalten mit Adressen, kommagetrennt (sonst am Namen erkannt)")
    ap.add_argument("--domain-spalten", help="Spalten mit Website oder Domain, kommagetrennt")
    ap.add_argument("--blocklist", help="Datei für die Blocklist von Instantly (Spalte Blocked)")
    ap.add_argument("--in", dest="infile", help="eigene Lead-Liste (CSV mit email und website)")
    ap.add_argument("--out", help="Lead-Liste ohne gesperrte Zeilen")
    args = ap.parse_args()
    if not args.crm and not args.zusatz.strip():
        print("FEHLER: --crm oder --zusatz angeben", file=sys.stderr)
        return 2
    if bool(args.infile) != bool(args.out):
        print("FEHLER: --in und --out nur zusammen", file=sys.stderr)
        return 2

    domains: set[str] = set()
    emails: set[str] = set()

    def take(address: str) -> None:
        if is_freemail(address):
            emails.add(address)
        else:
            dom = host_key(address.split("@", 1)[1])
            if dom:
                domains.add(dom)

    for path in args.crm:
        with open(path, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            fields = list(reader.fieldnames or [])
            mail_cols = columns(fields, args.email_spalten, EMAIL_HEADERS)
            web_cols = [f for f in columns(fields, args.domain_spalten, DOMAIN_HEADERS) if f not in mail_cols]
            if not mail_cols and not web_cols:
                print(f"FEHLER: {path} hat keine Spalte für Adresse oder Website ({', '.join(fields)}). "
                      f"--email-spalten bzw. --domain-spalten setzen.", file=sys.stderr)
                return 2
            for row in reader:
                for col in mail_cols:
                    for a in addresses(row.get(col)):
                        take(a)
                for col in web_cols:
                    dom = host_key(row.get(col))
                    if dom and dom not in FREEMAIL and not blocked(dom, NOT_A_COMPANY):
                        domains.add(dom)
    for entry in (e.strip() for e in args.zusatz.split(",")):
        if "@" in entry:
            for a in addresses(entry):
                take(a)
        elif host_key(entry):
            domains.add(host_key(entry))

    # Eine Adresse unter einer gesperrten Domain ist schon gesperrt.
    emails = {a for a in emails if not blocked(a.rsplit("@", 1)[1], domains)}
    report = f"Sperrliste: {len(domains)} Domains, {len(emails)} einzelne Adressen (private Postfächer)"

    if args.blocklist:
        with open(args.blocklist, "w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Blocked"])
            for entry in [*sorted(domains), *sorted(emails)]:
                writer.writerow([entry])
        report += f" | Blocklist für Instantly: {args.blocklist}"

    if args.infile:
        kept, hits = [], []
        with open(args.infile, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            fields = list(reader.fieldnames or [])
            for row in reader:
                email = (row.get("email") or "").strip().lower()
                mail_dom = host_key(email.split("@", 1)[1]) if "@" in email else ""
                site_dom = host_key(row.get("website"))
                hit = (email and email in emails) \
                    or (site_dom and blocked(site_dom, domains)) \
                    or (mail_dom and not is_freemail(email) and blocked(mail_dom, domains))
                if hit:
                    hits.append(email or site_dom)
                else:
                    kept.append(row)
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(kept)
        report += f" | Leads behalten: {len(kept)} | gesperrt entfernt: {len(hits)}"
        print(report)
        if hits:
            print("Gesperrt (nie anschreiben): " + ", ".join(sorted(set(hits))[:20]))
        return 0

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
