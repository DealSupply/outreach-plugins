#!/usr/bin/env python3
"""Tests für sperrliste.py und instantly_csv.py (Weg ohne DealSupply):
python3 -I plugins/datenbeschaffung/tests/test_instantly.py

Die Daten sind erfunden; die Spalten der Lead-Liste folgen csv-spalten.md, der CRM-Export ist wie
ein Export aus Close aufgebaut (Firmenname, URL, Adressen des Hauptkontakts).
"""
from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/datenbeschaffung-referenzen/scripts"

LEADS = ["email", "firstName", "lastName", "company", "website", "phoneNumber", "city", "kategorie",
         "quelle", "companyClean", "hinweis", "rating", "reviews_count", "place_id",
         "google_rezensionstexte", "inhaber", "inhaber_rolle"]


def write(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def run(script: str, *args: str) -> str:
    result = subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *args],
                            capture_output=True, text=True, check=True)
    return result.stdout


class SperrlisteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        write(self.dir / "crm.csv", ["display_name", "url", "primary_contact_primary_email", "linkedin_url"], [
            {"display_name": "Kunde A", "url": "https://www.kunde-a.de/", "primary_contact_primary_email": "",
             "linkedin_url": "https://www.linkedin.com/company/kunde-a"},
            {"display_name": "Ex-Kunde B", "url": "", "primary_contact_primary_email": "Chef@Exkunde-B.de"},
            {"display_name": "Privat C", "url": "",
             "primary_contact_primary_email": "privat.c@gmail.com; zweit@gmx.de"},
        ])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_blocklist_has_header_domains_and_private_addresses(self) -> None:
        report = run("sperrliste.py", "--crm", str(self.dir / "crm.csv"), "--zusatz", "wettbewerber.de",
                     "--blocklist", str(self.dir / "block.csv"))
        with (self.dir / "block.csv").open(encoding="utf-8") as fh:
            lines = fh.read().split()
        self.assertEqual(lines[0], "Blocked")
        self.assertEqual(sorted(lines[1:]), sorted(["exkunde-b.de", "kunde-a.de", "wettbewerber.de",
                                                    "privat.c@gmail.com", "zweit@gmx.de"]))
        self.assertNotIn("linkedin.com", lines)  # Profil-Link ist keine Firmen-Domain
        self.assertNotIn("gmail.com", lines)  # privates Postfach sperrt nie die ganze Domain
        self.assertIn("3 Domains, 2 einzelne Adressen", report)

    def test_lead_list_loses_blocked_rows(self) -> None:
        write(self.dir / "leads.csv", LEADS, [
            {"email": "info@kunde-a.de", "website": "https://kunde-a.de"},
            {"email": "info@neu.de", "website": "https://filiale.exkunde-b.de"},
            {"email": "privat.c@gmail.com", "website": "https://privat-c.de"},
            {"email": "andere@gmail.com", "website": "https://neu-zwei.de"},
            {"email": "info@neu-drei.de", "website": "https://neu-drei.de"},
        ])
        report = run("sperrliste.py", "--crm", str(self.dir / "crm.csv"), "--in", str(self.dir / "leads.csv"),
                     "--out", str(self.dir / "frei.csv"))
        kept = [r["email"] for r in read(self.dir / "frei.csv")]
        self.assertEqual(kept, ["andere@gmail.com", "info@neu-drei.de"])
        self.assertIn("gesperrt entfernt: 3", report)

    def test_missing_columns_fail_loudly(self) -> None:
        write(self.dir / "leer.csv", ["name"], [{"name": "X"}])
        result = subprocess.run([sys.executable, "-I", str(SCRIPTS / "sperrliste.py"), "--crm",
                                 str(self.dir / "leer.csv"), "--blocklist", str(self.dir / "b.csv")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--email-spalten", result.stderr)


class InstantlyCsvTest(unittest.TestCase):
    def convert(self, rows: list[dict], *extra: str) -> tuple[list[dict], list[str], str]:
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "in.csv", Path(tmp) / "out.csv"
            write(src, LEADS + ["kostenlos_testen"], rows)
            report = run("instantly_csv.py", "--in", str(src), "--out", str(out), *extra)
            with out.open(encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                return list(reader), list(reader.fieldnames or []), report

    def test_headers_follow_instantly_rules(self) -> None:
        rows, header, report = self.convert([{
            "email": "info@elektro-muster.de", "company": "Elektro Muster GmbH", "website": "https://elektro-muster.de",
            "city": "Stuttgart", "companyClean": "Elektro Muster", "quelle": "apify:x 2026-11-26",
            "hinweis": "rollen-adresse", "rating": "4.8", "place_id": "ChIJ1", "inhaber": "Max Muster",
            "inhaber_rolle": "Inhaber", "google_rezensionstexte": "2026-02-03 · 5★ · Sauber\n2026-01-01 · 4★ · Gut",
            "kostenlos_testen": "True"}])
        self.assertEqual(header[:3], ["Email", "FirstName", "LastName"])
        for name in header:
            self.assertRegex(name, r"^[A-Z][A-Za-z0-9]{0,19}$")
        for internal in ("Quelle", "Hinweis", "PlaceId", "InhaberRolle"):
            self.assertNotIn(internal, header)
        self.assertEqual(rows[0]["Firma"], "Elektro Muster")
        self.assertEqual(rows[0]["Stadt"], "Stuttgart")
        self.assertEqual(rows[0]["KostenlosTesten"], "ja")  # keine Wahrheitswerte
        self.assertIn("\n", rows[0]["Rezensionstexte"])
        self.assertIn("Firma → Custom variable", report)
        self.assertIn("CompanyName → Company name", report)

    def test_owner_becomes_first_name_only_when_unambiguous(self) -> None:
        owners = {"a@a.de": "Dr. Hans-Peter Müller", "b@b.de": "Anna Beispiel und Paul Beispiel",
                  "c@c.de": "Muster GmbH", "d@d.de": "Karl von Stein", "e@e.de": "Dipl.-Ing. Eva Lang",
                  "f@f.de": "Max M."}
        rows, _, report = self.convert([{"email": k, "inhaber": v} for k, v in owners.items()])
        names = {r["Email"]: (r["FirstName"], r["LastName"]) for r in rows}
        self.assertEqual(names["a@a.de"], ("Hans-Peter", "Müller"))
        self.assertEqual(names["e@e.de"], ("Eva", "Lang"))
        for unclear in ("b@b.de", "c@c.de", "d@d.de", "f@f.de"):
            self.assertEqual(names[unclear], ("", ""), unclear)
        self.assertEqual({r["Email"]: r["Inhaber"] for r in rows}["b@b.de"], owners["b@b.de"])
        self.assertIn("aus dem Inhaber 2", report)

    def test_source_names_win_and_switch_off_works(self) -> None:
        rows, _, _ = self.convert([{"email": "x@x.de", "firstName": "Lena", "lastName": "Quelle",
                                    "inhaber": "Max Muster"}])
        self.assertEqual((rows[0]["FirstName"], rows[0]["LastName"]), ("Lena", "Quelle"))
        rows, _, _ = self.convert([{"email": "y@y.de", "inhaber": "Max Muster"}], "--keine-namen-aus-inhaber")
        self.assertEqual(rows[0]["FirstName"], "")

    def test_rows_without_email_are_dropped_and_counted(self) -> None:
        rows, _, report = self.convert([{"email": "", "website": "https://ohne.de"},
                                        {"email": "mit@mit.de", "website": "https://mit.de"}])
        self.assertEqual([r["Email"] for r in rows], ["mit@mit.de"])
        self.assertIn("ohne E-Mail weggelassen: 1", report)


if __name__ == "__main__":
    unittest.main()
