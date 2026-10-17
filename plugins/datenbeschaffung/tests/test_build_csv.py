#!/usr/bin/env python3
"""Tests für build_csv.py: python3 plugins/datenbeschaffung/tests/test_build_csv.py

Die Rohdaten sind erfunden, im Aufbau aber wie die echten Datasets der gepinnten Actors
(Google Maps mit Kontaktanreicherung und Rezensionen, Lauf vom 11.10.2026).
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/datenbeschaffung-referenzen/scripts/build_csv.py"

MAPS_ROW = {
    "title": "Elektro Muster GmbH",
    "placeId": "ChIJmuster0001",
    "cid": "1234567890",
    "url": "https://www.google.com/maps/place/?q=place_id:ChIJmuster0001",
    "website": "https://www.elektro-muster.de/",
    "categoryName": "Elektriker",
    "city": "Stuttgart",
    "countryCode": "DE",
    "phone": "+49 711 000000",
    "totalScore": 4.8,
    "reviewsCount": 34,
    "emails": ["bewerbung@elektro-muster.de", "info@elektro-muster.de"],
    "reviewsTags": [{"title": "pv-anlage", "count": 3}, {"title": "termin", "count": 2}],
    "impressum": {
        "people": [{"name": "Petra Prokura", "role": "Prokuristin", "roleType": "authorized_officer"},
                   {"name": "Max Muster", "role": "Inhaber", "roleType": "owner"}],
        "emails": [{"value": "info@elektro-muster.de", "type": "generic"}],
    },
    "reviews": [
        {"name": "Erika Beispiel", "text": None, "publishedAtDate": "2026-09-01T10:00:00.000Z", "stars": 5},
        {"name": "Hans Kunde", "text": "PV-Anlage sauber geplant und montiert.",
         "publishedAtDate": "2025-11-10T07:13:49.780Z", "stars": 5},
        {"name": "Anna Alt", "text": "Schnell da,\nalles erklärt.", "publishedAtDate": "2026-02-03T08:00:00.000Z", "stars": 4},
        {"name": "Ausland", "text": "Ott dolgozom", "textTranslated": "Ich arbeite dort",
         "publishedAtDate": "2020-02-22T09:05:10.185Z", "stars": 5},
    ],
}

MAPS_ROW_NO_WEBSITE = {
    "title": "Elektro Ohne Netz", "placeId": "ChIJmuster0002", "city": "Stuttgart", "countryCode": "DE",
    "url": "https://www.google.com/maps/place/?q=place_id:ChIJmuster0002", "totalScore": None,
    "reviewsCount": None, "emails": [], "reviews": [],
}

INSTAGRAM_ROW = {
    "company": "Coaching Beispiel", "email": "hallo@coaching-beispiel.de",
    "website": "coaching-beispiel.de", "instagram_url": "https://instagram.com/coaching.beispiel",
    "followersCount": 12400, "biography": "Business-Coaching für Handwerksbetriebe", "link_typ": "eigene Website",
}


def run(rows: list[dict], *extra: str) -> tuple[list[dict], list[str], str]:
    with tempfile.TemporaryDirectory() as tmp:
        src, out = Path(tmp) / "in.json", Path(tmp) / "out.csv"
        src.write_text(json.dumps(rows), encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--in", str(src), "--out", str(out),
                                 "--quelle", "apify:test 2026-10-11", *extra],
                                capture_output=True, text=True, check=True)
        with out.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            return list(reader), list(reader.fieldnames or []), result.stdout


class MapsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rows, self.header, self.report = run([MAPS_ROW, MAPS_ROW_NO_WEBSITE])
        self.lead = self.rows[0]

    def test_google_fields_reach_the_csv(self) -> None:
        self.assertEqual(self.lead["rating"], "4.8")
        self.assertEqual(self.lead["reviews_count"], "34")
        self.assertEqual(self.lead["place_id"], "ChIJmuster0001")
        self.assertEqual(self.lead["reviews_tags"], "pv-anlage (3), termin (2)")
        self.assertEqual(self.lead["kategorie"], "Elektriker")

    def test_reviews_newest_first_with_text_only_and_without_names(self) -> None:
        lines = self.lead["google_rezensionstexte"].split("\n")
        self.assertEqual(lines, [
            "2026-02-03 · 4★ · Schnell da, alles erklärt.",
            "2025-11-10 · 5★ · PV-Anlage sauber geplant und montiert.",
            "2020-02-22 · 5★ · Ich arbeite dort",
        ])
        for name in ("Erika", "Hans", "Anna"):
            self.assertNotIn(name, self.lead["google_rezensionstexte"])

    def test_max_reviews_limits_texts(self) -> None:
        rows, _, _ = run([MAPS_ROW], "--max-reviews", "1")
        self.assertEqual(rows[0]["google_rezensionstexte"].count("\n"), 0)

    def test_owner_from_impressum(self) -> None:
        self.assertEqual((self.lead["inhaber"], self.lead["inhaber_rolle"]), ("Max Muster", "Inhaber"))

    def test_application_address_is_not_the_sending_address(self) -> None:
        self.assertEqual(self.lead["email"], "info@elektro-muster.de")
        self.assertIn("rollen-adresse", self.lead["hinweis"])

    def test_maps_link_is_never_the_website(self) -> None:
        other = self.rows[1]
        self.assertEqual(other["website"], "")
        self.assertIn("keine-website", other["hinweis"])
        self.assertIn("keine-rezensionstexte", other["hinweis"])
        self.assertEqual(other["rating"], "")

    def test_report_counts_google_fields(self) -> None:
        self.assertIn("mit Bewertung 1, mit Rezensionstext 1, mit Inhaber 1", self.report)


class ForeignDataTest(unittest.TestCase):
    """Echte Fälle aus dem Lauf vom 11.10.2026: Portal als Website, Agentur im Impressum."""

    def test_portal_website_drops_portal_address_and_person(self) -> None:
        row = {"title": "Elektro Portal-Eintrag", "placeId": "ChIJmuster0004", "countryCode": "DE",
               "website": "https://www.gelbeseiten.de/gsbiz/1234", "emails": ["info@gelbeseiten.de"],
               "impressum": {"people": [{"name": "Petra Portal", "role": "Geschäftsführerin", "roleType": "managing_director"}],
                             "emails": [{"value": "info@gelbeseiten.de"}]}}
        rows, _, report = run([row])
        lead = rows[0]
        self.assertEqual((lead["email"], lead["website"], lead.get("inhaber", "")), ("", "", ""))
        self.assertIn("portal-website", lead["hinweis"])
        self.assertIn("Portal statt eigener Website: 1", report)

    def test_impressum_address_of_other_domain_is_ignored(self) -> None:
        row = {**MAPS_ROW, "emails": [], "impressum": {
            "people": [{"name": "Rita Redaktion", "role": "Redaktionell verantwortlich", "roleType": "content_responsible"}],
            "emails": [{"value": "info@webagentur-beispiel.de"}]}}
        lead = run([row])[0][0]
        self.assertEqual(lead["email"], "")
        self.assertEqual(lead.get("inhaber", ""), "", "redaktionell Verantwortliche sind kein Inhaber")

    def test_own_domain_beats_foreign_scraped_address(self) -> None:
        row = {**MAPS_ROW, "emails": ["kontakt@webagentur-beispiel.de", "info@elektro-muster.de"]}
        self.assertEqual(run([row])[0][0]["email"], "info@elektro-muster.de")


class ProviderShapesTest(unittest.TestCase):
    """Feldnamen echter Läufe vom 11.10.2026 (Daten erfunden)."""

    def test_b2b_database_marks_guessed_and_drops_invalid_addresses(self) -> None:
        base = {"organizationName": "Muster Maschinenbau GmbH", "organizationWebsite": "muster-mb.de",
                "organizationCity": "Ulm", "organizationIndustry": "Machinery", "organizationEmployeeRange": "11 - 50",
                "title": "Geschäftsführer", "firstName": "Max", "lastName": "Muster",
                "linkedinUrl": "https://www.linkedin.com/in/max-muster"}
        rows, _, report = run([
            {**base, "email": "max.muster@muster-mb.de", "emailPatternGuess": "max.muster@muster-mb.de"},
            {**base, "organizationWebsite": "zweite-mb.de", "email": "jörg.muster@zweite-mb.de"},
        ])
        guessed, invalid = rows
        self.assertEqual((guessed["company"], guessed["position"], guessed["city"]), ("Muster Maschinenbau GmbH", "Geschäftsführer", "Ulm"))
        self.assertIn("geratene-adresse", guessed["hinweis"])
        self.assertEqual(invalid["email"], "", "Umlaut vor dem @ ist nie zustellbar")
        self.assertIn("geratene Adressen (vor Import verifizieren): 1", report)

    def test_instagram_profile_uses_external_url_as_website(self) -> None:
        lead = run([{"username": "coach.beispiel", "url": "https://www.instagram.com/coach.beispiel",
                     "followersCount": 1200, "fullName": "Coaching Beispiel", "biography": "Business-Coaching",
                     "externalUrl": "https://coaching-beispiel.de", "businessCategoryName": "Coach"}])[0][0]
        self.assertEqual((lead["website"], lead["instagram_url"], lead["follower"], lead["kategorie"]),
                         ("https://coaching-beispiel.de", "https://www.instagram.com/coach.beispiel", "1200", "Coach"))

    def test_linkedin_person_and_company_shapes(self) -> None:
        person, company = run([
            {"firstName": "Erika", "lastName": "Beispiel", "linkedinUrl": "https://www.linkedin.com/in/erika",
             "currentPositions": [{"title": "Vertriebscoach", "companyName": "Beispiel Coaching"}]},
            {"universalName": "muster-mb", "name": "Muster MB GmbH", "website": "https://muster-mb.de",
             "phone": {"number": "0711000000", "extension": None}, "employeeCount": 21,
             "industries": [{"name": "Machinery Manufacturing"}],
             "locations": [{"city": "Ulm", "headquarter": True}], "linkedinUrl": "https://www.linkedin.com/company/muster-mb"},
        ])[0]
        self.assertEqual((person["position"], person["company"]), ("Vertriebscoach", "Beispiel Coaching"))
        self.assertEqual((company["phoneNumber"], company["city"], company["mitarbeiter"], company["kategorie"]),
                         ("0711000000", "Ulm", "21", "Machinery Manufacturing"))

    def test_impressum_actor_text_addresses_and_managing_director(self) -> None:
        lead = run([{"domain": "muster-mb.de", "companyName": "Muster MB GmbH",
                     "emails": "info@muster-mb.de, vertrieb@muster-mb.de", "managingDirector": "Max Muster"}])[0][0]
        self.assertEqual((lead["email"], lead["inhaber"]), ("vertrieb@muster-mb.de", "Max Muster"))


class OutscraperTest(unittest.TestCase):
    def test_review_count_from_text_is_no_review_text(self) -> None:
        rows, _, _ = run([{"name": "Sanitär Beispiel", "site": "sanitaer-beispiel.de", "email": "info@sanitaer-beispiel.de",
                           "place_id": "ChIJmuster0003", "rating": "4.6", "reviews": "52", "category": "Klempner"}])
        lead = rows[0]
        self.assertEqual((lead["rating"], lead["reviews_count"]), ("4.6", "52"))
        self.assertNotIn("google_rezensionstexte", lead, "leere Spalte fällt weg, die Anzahl ist kein Text")
        self.assertEqual(lead["website"], "https://sanitaer-beispiel.de")
        self.assertIn("keine-rezensionstexte", lead["hinweis"])


class ExtraColumnsTest(unittest.TestCase):
    def test_platform_columns_survive_under_fixed_names(self) -> None:
        rows, header, _ = run([INSTAGRAM_ROW])
        self.assertEqual(rows[0]["follower"], "12400")
        self.assertEqual(rows[0]["bio"], "Business-Coaching für Handwerksbetriebe")
        self.assertEqual(rows[0]["instagram_url"], "https://instagram.com/coaching.beispiel")
        self.assertNotIn("rating", header, "Google-Spalten nur bei Google-Zeilen")

    def test_keep_passes_raw_fields_and_empty_columns_stay_out(self) -> None:
        rows, header, _ = run([{**INSTAGRAM_ROW, "postsCount": 87}], "--keep", "postsCount,gibtsnicht")
        self.assertEqual(rows[0]["postsCount"], "87")
        self.assertNotIn("gibtsnicht", header)
        self.assertNotIn("linkedin_url", header)

    def test_require_email_drops_rows_without_address(self) -> None:
        rows, _, report = run([MAPS_ROW, MAPS_ROW_NO_WEBSITE], "--require-email")
        self.assertEqual(len(rows), 1)
        self.assertIn("verworfen (--uebergabe email): 1 (keine-email 1)", report)


def run_with_rejected(rows: list[dict], *extra: str) -> tuple[list[dict], list[dict], str]:
    with tempfile.TemporaryDirectory() as tmp:
        src, out, rej = Path(tmp) / "in.json", Path(tmp) / "out.csv", Path(tmp) / "verworfen.csv"
        src.write_text(json.dumps(rows), encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--in", str(src), "--out", str(out),
                                 "--quelle", "apify:test 2026-10-16", "--verworfen", str(rej), *extra],
                                capture_output=True, text=True, check=True)
        with out.open(encoding="utf-8", newline="") as fh:
            kept = list(csv.DictReader(fh))
        rejected = []
        if rej.exists():
            with rej.open(encoding="utf-8", newline="") as fh:
                rejected = list(csv.DictReader(fh))
        return kept, rejected, result.stdout


WEBSITE_ONLY = {"title": "Praxis Ohne Mail", "placeId": "ChIJmuster0010", "countryCode": "DE",
                "website": "https://praxis-ohne-mail.de", "emails": [], "city": "Ulm"}


class HandoverTest(unittest.TestCase):
    """Übergabe-CSV ab ListM8 MCP 3.0.0: E-Mail ODER eigene Website (references/plattform-hosts.md)."""

    def test_kontakt_keeps_website_only_row(self) -> None:
        kept, rejected, report = run_with_rejected([WEBSITE_ONLY], "--uebergabe", "kontakt")
        self.assertEqual([r["website"] for r in kept], ["https://praxis-ohne-mail.de"])
        self.assertEqual(rejected, [])
        self.assertIn("ohne E-Mail, mit eigener Website (Recherche sucht die Adresse): 1", report)

    def test_kontakt_rejects_platform_only_with_reason(self) -> None:
        rows = [{**WEBSITE_ONLY, "placeId": f"ChIJp{i}", "website": url} for i, url in enumerate([
            "https://www.instagram.com/praxis", "https://linktr.ee/praxis", "https://www.facebook.com/praxis",
            "https://www.doctolib.fr/praxis"])]
        kept, rejected, report = run_with_rejected(rows, "--uebergabe", "kontakt")
        self.assertEqual(kept, [])
        self.assertEqual({r["grund"] for r in rejected}, {"nur-plattform-url"})
        self.assertIn("verworfen (--uebergabe kontakt): 4 (nur-plattform-url 4)", report)

    def test_kontakt_rejects_without_any_contact(self) -> None:
        kept, rejected, _ = run_with_rejected([MAPS_ROW_NO_WEBSITE], "--uebergabe", "kontakt")
        self.assertEqual(kept, [])
        self.assertEqual(rejected[0]["grund"], "kein-kontaktmerkmal")

    def test_portal_website_without_email_is_platform_only(self) -> None:
        row = {**WEBSITE_ONLY, "website": "https://www.gelbeseiten.de/gsbiz/1234", "emails": ["info@gelbeseiten.de"]}
        kept, rejected, _ = run_with_rejected([row], "--uebergabe", "kontakt")
        self.assertEqual((kept, rejected[0]["grund"]), ([], "nur-plattform-url"))

    def test_builder_subdomain_counts_as_website(self) -> None:
        rows = [{**WEBSITE_ONLY, "placeId": "ChIJb1", "website": "https://praxis.jimdosite.com"},
                {**WEBSITE_ONLY, "placeId": "ChIJb2", "website": "https://salon.wixsite.com/start"},
                {**WEBSITE_ONLY, "placeId": "ChIJb3", "website": "https://www.jimdosite.com"}]
        kept, rejected, _ = run_with_rejected(rows, "--uebergabe", "kontakt")
        self.assertEqual(len(kept), 2, "Kunden-Subdomains eines Baukastens sind eigene Websites")
        self.assertEqual([r["grund"] for r in rejected], ["nur-plattform-url"])

    def test_platform_link_with_email_stays(self) -> None:
        # Instagram & Co. stehen zusätzlich in noise-domains.md: dort gehört die Adresse dem Portal.
        row = {**WEBSITE_ONLY, "website": "https://linktr.ee/praxis", "emails": ["hallo@praxis-beispiel.de"]}
        kept, rejected, _ = run_with_rejected([row], "--uebergabe", "kontakt")
        self.assertEqual((len(kept), rejected), (1, []))

    def test_email_mode_equals_require_email_alias(self) -> None:
        a = run_with_rejected([MAPS_ROW, WEBSITE_ONLY], "--uebergabe", "email")
        b = run_with_rejected([MAPS_ROW, WEBSITE_ONLY], "--require-email")
        self.assertEqual(a, b)
        self.assertEqual(a[1][0]["grund"], "keine-email")

    def test_without_mode_platform_only_is_kept_and_marked(self) -> None:
        row = {**WEBSITE_ONLY, "website": "https://linktr.ee/praxis"}
        kept, rejected, report = run_with_rejected([row])
        self.assertEqual(rejected, [])
        self.assertIn("nur-plattform-url", kept[0]["hinweis"])
        self.assertIn("ohne E-Mail, nur Plattform-Link: 1", report)

    def test_platform_list_loaded_from_reference(self) -> None:
        sys.path.insert(0, str(SCRIPT.parent))
        try:
            import build_csv
        finally:
            sys.path.pop(0)
        self.assertIn("instagram.com", build_csv.PLATFORM_HOSTS)
        self.assertIn("jimdosite.com", build_csv.PLATFORM_BUILDERS)
        self.assertIn("treatwell", build_csv.PLATFORM_BRANDS)
        self.assertTrue(build_csv.is_platform("treatwell.es"))
        self.assertFalse(build_csv.is_platform("praxis.jimdosite.com"))

    def test_second_pass_on_built_csv_keeps_columns_and_hints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "roh.csv", Path(tmp) / "uebergabe.csv"
            src = Path(tmp) / "in.json"
            src.write_text(json.dumps([MAPS_ROW, {**WEBSITE_ONLY, "omr_url": "https://omr.com/x"}]), encoding="utf-8")
            subprocess.run([sys.executable, "-I", str(SCRIPT), "--in", str(src), "--out", str(first),
                            "--quelle", "apify:test 2026-10-16", "--keep", "omr_url"], check=True, capture_output=True)
            text = first.read_text(encoding="utf-8").replace("keine-email", "keine-email;adresse-verworfen")
            first.write_text(text, encoding="utf-8")
            subprocess.run([sys.executable, "-I", str(SCRIPT), "--in", str(first), "--out", str(second),
                            "--quelle", "apify:test 2026-10-16", "--uebergabe", "kontakt"], check=True, capture_output=True)
            with second.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
        lead, website_only = rows
        self.assertEqual((lead["inhaber"], lead["rating"]), ("Max Muster", "4.8"))
        self.assertEqual(website_only["omr_url"], "https://omr.com/x")
        self.assertIn("adresse-verworfen", website_only["hinweis"])
        self.assertEqual(website_only["hinweis"].count("keine-email"), 1)

    def test_csv_input_from_process_serp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "domains.csv", Path(tmp) / "out.csv"
            src.write_text("domain,website,titel,query\nmuster-mb.de,https://muster-mb.de/,Startseite | Muster,"
                           "maschinenbau ulm\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--in", str(src), "--out", str(out),
                                     "--quelle", "serp 2026-10-16", "--uebergabe", "kontakt"],
                                    capture_output=True, text=True, check=True)
            with out.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
        self.assertEqual((rows[0]["website"], rows[0]["company"]), ("https://muster-mb.de/", ""))
        self.assertIn("Leads: 1", result.stdout)


if __name__ == "__main__":
    unittest.main()
