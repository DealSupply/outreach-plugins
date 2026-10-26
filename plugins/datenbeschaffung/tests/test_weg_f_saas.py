#!/usr/bin/env python3
"""Tests für die Skripte von Weg F: python3 plugins/datenbeschaffung/tests/test_weg_f_saas.py

Ohne Netz: geprüft werden die reinen Funktionen (Sitz aus dem Impressum-Text, Domain-Zuordnung
der Website-Suche) und die Datei-Abläufe (Zusammenführen, LinkedIn-Sitzfilter und Details-Input).
Die Rohdaten sind erfunden, im Aufbau aber wie die echten Antworten vom 14.10.2026.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/datenbeschaffung-referenzen/scripts"
sys.path.insert(0, str(SCRIPTS))

import sitz_check  # noqa: E402
import website_suche  # noqa: E402

LINKEDIN_SHORT = [
    {"universalName": "kundenwolke", "name": "Kundenwolke GmbH", "linkedinUrl": "https://www.linkedin.com/company/kundenwolke/",
     "location": {"linkedinText": "Hamburg, Hamburg"}, "summary": "Die CRM-Software für Handwerker", "followers": "1K followers"},
    {"universalName": "megacorp", "name": "MegaCorp", "linkedinUrl": "https://www.linkedin.com/company/megacorp/",
     "location": {"linkedinText": "Mountain View, CA"}, "summary": "Search", "followers": "30M followers"},
    {"universalName": "pixelwerk", "name": "Pixelwerk Agentur", "linkedinUrl": "https://www.linkedin.com/company/pixelwerk/",
     "location": {"linkedinText": "Hamburg"}, "summary": "Webdesign und Apps im Auftrag", "followers": "300 followers"},
    {"universalName": "zeitkonto", "name": "Zeitkonto", "linkedinUrl": "https://www.linkedin.com/company/zeitkonto/",
     "location": {"linkedinText": "Hamburg, HH"}, "summary": "Zeiterfassung in der Cloud", "followers": "2K followers"},
]
LINKEDIN_DETAIL = {
    "universalName": "kundenwolke", "name": "Kundenwolke GmbH", "website": "https://www.kundenwolke.de/",
    "linkedinUrl": "https://www.linkedin.com/company/kundenwolke/", "employeeCount": 34, "followerCount": 1200,
    "foundedOn": {"year": 2017}, "tagline": "Die CRM-Software für Handwerker",
    "locations": [{"city": "Hamburg", "headquarter": True}, {"city": "Berlin", "headquarter": False}],
    "email": "info@kundenwolke.de", "sitz_land": "DE", "sitz_plz": "20457 Hamburg",
}
OMR_ROWS = [
    {"produkt": "Kundenwolke CRM", "website": "https://kundenwolke.de", "kategorie": "CRM", "plattform": "OMR Reviews",
     "bewertung": 4.6, "bewertungen_anzahl": 41, "omr_url": "https://omr.com/de/reviews/product/kundenwolke-crm"},
    {"produkt": "Zeitkonto", "website": "https://zeitkonto.io", "kategorie": "Zeiterfassung", "plattform": "OMR Reviews",
     "bewertung": None, "bewertungen_anzahl": 0, "linkedin_url": "https://www.linkedin.com/company/zeitkonto/"},
]


def run(script: str, *args: str) -> str:
    res = subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True, check=True)
    return res.stdout + res.stderr


class SitzTest(unittest.TestCase):
    def test_deutsches_impressum(self):
        text = "Impressum Kundenwolke GmbH Großer Burstah 1 20457 Hamburg Amtsgericht Hamburg HRB 12345"
        self.assertEqual(sitz_check.country_and_place(text), ("DE", "20457", "Hamburg"))

    def test_jahreszahl_ist_keine_plz(self):
        text = "© 2026 Muster AG Firmenbuch FN 123456a Mariahilfer Straße 1 1060 Wien Österreich"
        self.assertEqual(sitz_check.country_and_place(text), ("AT", "1060", "Wien"))

    def test_schweiz_mit_praefix(self):
        text = "Muster AG, Bahnhofstrasse 1, CH-8001 Zürich, Schweiz, CHE-123.456.789"
        self.assertEqual(sitz_check.country_and_place(text)[:2], ("CH", "8001"))

    def test_zahlen_ohne_anschrift_sind_keine_plz(self):
        for text in ("Über 10000 Kunden in Deutschland vertrauen uns",
                     "Registergericht Hamburg HRB 12345 Geschäftsführer Max Muster",
                     "Tel 040 12345 Fax 040 12346 Deutschland"):
            self.assertEqual(sitz_check.country_and_place(text), ("", "", ""), text)

    def test_ausland_mit_deutschem_sprachwaehler(self):
        text = "Acme SAS, 12 Rue de Rivoli, 75008 Paris, France. Sprache: Deutschland | English"
        self.assertEqual(sitz_check.country_and_place(text)[0], "")

    def test_schweiz_ohne_praefix_mit_dach_satz(self):
        text = "Kunden in Deutschland, Österreich und der Schweiz. Muster AG, Bahnhofstrasse 1, 8001 Zürich. Schweiz"
        self.assertEqual(sitz_check.country_and_place(text), ("CH", "8001", "Zürich"))

    def test_ohne_dach_merkmal(self):
        self.assertEqual(sitz_check.country_and_place("Acme Inc., 1 Market St, San Francisco, CA 94105")[0], "")


class WebsiteSucheTest(unittest.TestCase):
    def test_domain_passt_zum_namen(self):
        names = [website_suche.norm("Kundenwolke GmbH"), website_suche.norm("Kundenwolke")]
        self.assertTrue(website_suche.fits("kundenwolke.de", names))
        self.assertFalse(website_suche.fits("northdata.de", names))

    def test_portale_sind_ausgeschlossen(self):
        self.assertIn("northdata.de", website_suche.noise())
        self.assertEqual(website_suche.root("https://www.app.kundenwolke.de/login"), "kundenwolke.de")


class AblaufTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def write(self, name: str, data) -> str:
        path = self.tmp / name
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return str(path)

    def test_linkedin_sitzfilter_und_details(self):
        short = self.write("short.json", LINKEDIN_SHORT)
        out = str(self.tmp / "li")
        run("linkedin_saas.py", "vorbereiten", "--orte", "Hamburg", "--out", out, short)
        kept = json.loads(Path(out + ".json").read_text(encoding="utf-8"))
        self.assertEqual({r["universalName"] for r in kept}, {"kundenwolke", "pixelwerk", "zeitkonto"})
        self.assertEqual(len(Path(out + ".tsv").read_text(encoding="utf-8").splitlines()), 3)

        klassen = self.tmp / "klassen.tsv"
        klassen.write_text("kundenwolke\tsaas_b2b\npixelwerk\tdienstleister\nzeitkonto\tsaas_b2b\n", encoding="utf-8")
        omr = self.write("omr.json", OMR_ROWS)
        det = str(self.tmp / "det.json")
        log = run("linkedin_saas.py", "details", "--in", out + ".json", "--klassen", str(klassen),
                  "--bekannt", omr, "--out", det)
        # Zeitkonto kennt OMR schon über die LinkedIn-URL, die Agentur ist kein SaaS.
        self.assertEqual(json.loads(Path(det).read_text())["companies"],
                         ["https://www.linkedin.com/company/kundenwolke/"])
        self.assertIn("schon bekannt 1", log)
        known = json.loads(Path(str(self.tmp / "det-bekannt.json")).read_text(encoding="utf-8"))
        self.assertEqual([k["linkedin_url"] for k in known], ["https://www.linkedin.com/company/zeitkonto/"])

    def test_klassen_mit_windows_zeilenenden(self):
        short = self.write("short.json", LINKEDIN_SHORT)
        out = str(self.tmp / "li")
        run("linkedin_saas.py", "vorbereiten", "--orte", "Hamburg", "--out", out, short)
        klassen = self.tmp / "klassen.tsv"
        klassen.write_text("kundenwolke\tsaas_b2b \r\nzeitkonto\tsaas_b2b\r\n", encoding="utf-8")
        log = run("linkedin_saas.py", "details", "--in", out + ".json", "--klassen", str(klassen),
                  "--out", str(self.tmp / "det.json"))
        self.assertIn("Details nötig für 2", log)
        self.assertIn("1 Firmen ohne Klasse", log)

    def test_zusammenfuehren_auf_domain(self):
        omr = self.write("omr.json", OMR_ROWS)
        li = self.write("li.json", [LINKEDIN_DETAIL])
        sb = self.write("sb.json", [{"company": "Zeitkonto GmbH", "produkt": "Zeitkonto", "city": "Hamburg",
                                     "gruendung": "2019"}])
        out = self.tmp / "merged.json"
        run("quellen_zusammenfuehren.py", "--out", str(out), f"linkedin:{li}", f"startbase:{sb}", f"omr:{omr}")
        merged = json.loads(out.read_text(encoding="utf-8"))
        rows = {"https://" + website_suche.root(r["website"]): r for r in merged}
        self.assertEqual(len(merged), 2)
        wolke = rows["https://kundenwolke.de"]
        self.assertEqual(wolke["quellen"], "linkedin,omr")
        self.assertEqual(wolke["company"], "Kundenwolke GmbH")  # Firma aus LinkedIn, nicht der Produktname
        self.assertEqual(wolke["produkt"], "Kundenwolke CRM")
        self.assertEqual(wolke["mitarbeiter"], 34)
        self.assertEqual(wolke["email"], "info@kundenwolke.de")  # Feld aus sitz_check bleibt erhalten
        self.assertEqual(wolke["bewertung"], 4.6)
        # Startbase-Zeile ohne Website landet im zweiten Durchgang über den Namen bei der OMR-Domain.
        self.assertEqual(rows["https://zeitkonto.io"]["quellen"], "omr,startbase")
        self.assertEqual(rows["https://zeitkonto.io"]["gruendung"], "2019")


if __name__ == "__main__":
    unittest.main()
