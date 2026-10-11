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
        self.assertIn("verworfen (--require-email): 1", report)


if __name__ == "__main__":
    unittest.main()
