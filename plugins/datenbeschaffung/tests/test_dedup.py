#!/usr/bin/env python3
"""Tests für dedup.py: python3 -I plugins/datenbeschaffung/tests/test_dedup.py

Bestandsindex im Format von export_leads(format="index") ab ListM8 MCP 3.0.0
(`e` = E-Mail des Leads, leer bei Leads ohne E-Mail; auch null möglich).
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/datenbeschaffung-referenzen/scripts/dedup.py"

INDEX = {"index": [
    {"e": "anna@praxis-a.de", "d": "praxis-a.de", "s": "not_contacted", "se": ["info@praxis-a.de"]},
    {"e": "", "d": "praxis-ohne-mail.de", "s": "not_contacted"},
    {"e": None, "d": "altserver.de", "s": "not_contacted"},
    {"e": "info@gesperrt.de", "d": "gesperrt.de", "s": "do_not_contact"},
    {"e": "kontakt@firma-b.de", "d": "firma-b.de", "s": "contacted"},
    {"e": "", "d": "mueller.de", "s": "not_contacted"},
    {"e": "", "d": "bäckerei-müller.de", "s": "not_contacted"},
    {"e": "", "d": "filiale.kette.de", "s": "not_contacted"},
]}

FIELDS = ["email", "company", "website", "hinweis"]


def run(rows: list[dict], *extra: str) -> tuple[list[dict], str]:
    with tempfile.TemporaryDirectory() as tmp:
        index, src, out = Path(tmp) / "index.json", Path(tmp) / "in.csv", Path(tmp) / "out.csv"
        index.write_text(json.dumps(INDEX), encoding="utf-8")
        with src.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--index", str(index), "--in", str(src),
                                 "--out", str(out), *extra], capture_output=True, text=True, check=True)
        with out.open(encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh)), result.stdout


class DedupTest(unittest.TestCase):
    def test_null_and_empty_index_address_do_not_crash(self) -> None:
        kept, report = run([{"email": "neu@neu.de", "company": "Neu", "website": "https://neu.de"}])
        self.assertEqual(len(kept), 1)
        self.assertIn("Behalten: 1", report)

    def test_sending_and_secondary_addresses_are_known(self) -> None:
        kept, report = run([{"email": "ANNA@praxis-a.de", "website": "https://praxis-a.de"},
                            {"email": "info@praxis-a.de", "website": "https://praxis-a.de"}])
        self.assertEqual(kept, [])
        self.assertIn("Schon im Bestand entfernt: 2", report)

    def test_row_without_email_on_known_addressless_website_is_the_same_lead(self) -> None:
        kept, _ = run([{"company": "Praxis", "website": "https://www.praxis-ohne-mail.de/kontakt"},
                       {"company": "Alt", "website": "altserver.de"}])
        self.assertEqual(kept, [])

    def test_row_without_email_on_company_with_address_is_only_marked(self) -> None:
        kept, report = run([{"company": "B", "website": "https://firma-b.de"}])
        self.assertIn("firma-schon-im-bestand", kept[0]["hinweis"])
        self.assertIn("ohne E-Mail behalten", report)

    def test_drop_known_domains_without_email_only_hits_rows_without_email(self) -> None:
        kept, _ = run([{"company": "B", "website": "https://firma-b.de"},
                       {"email": "neu@firma-b.de", "website": "https://firma-b.de"}],
                      "--drop-known-domains-ohne-email")
        self.assertEqual([r["email"] for r in kept], ["neu@firma-b.de"])

    def test_do_not_contact_domain_drops_rows_without_email(self) -> None:
        kept, report = run([{"company": "G", "website": "https://gesperrt.de"}])
        self.assertEqual(kept, [])
        self.assertIn("do_not_contact entfernt: 1", report)

    def test_similar_or_sub_hosts_are_not_the_same_lead(self) -> None:
        kept, report = run([{"company": "Bäckerei Müller", "website": "https://baeckerei-mueller.de"},
                            {"company": "Shop", "website": "https://shop.mueller.de"}])
        self.assertEqual(len(kept), 2)
        self.assertEqual([r["hinweis"] for r in kept], ["", ""])
        self.assertIn("Domain-Warnungen: 0", report)

    def test_parent_domain_of_a_known_host_is_only_a_warning(self) -> None:
        kept, report = run([{"company": "Kette", "website": "https://kette.de"}])
        self.assertEqual(len(kept), 1)
        self.assertIn("firma-schon-im-bestand", kept[0]["hinweis"])
        self.assertIn("Domain-Warnungen: 1", report)

    def test_umlaut_and_punycode_hosts_match(self) -> None:
        kept, _ = run([{"company": "Müller", "website": "https://www.xn--bckerei-mller-bfb28a.de/impressum"}])
        self.assertEqual(kept, [])


if __name__ == "__main__":
    unittest.main()
