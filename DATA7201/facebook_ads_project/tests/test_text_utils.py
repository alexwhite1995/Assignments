from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from data7201_project.text_utils import contains_keyword, extract_domains, normalise_domain


class TextUtilsTest(unittest.TestCase):
    def test_normalise_domain_removes_scheme_www_port_and_case(self) -> None:
        self.assertEqual(normalise_domain("HTTPS://WWW.Example.ORG:443/path"), "example.org")

    def test_extract_domains_preserves_first_seen_unique_domains(self) -> None:
        text = "Visit https://example.org/a and www.news.com.au/story then example.org/b."
        self.assertEqual(extract_domains(text), ["example.org", "news.com.au"])

    def test_contains_keyword_matches_phrases_case_insensitively(self) -> None:
        self.assertTrue(contains_keyword("A national Voice referendum ad", ["voice referendum"]))
        self.assertFalse(contains_keyword("Invoice processing", ["voice"]))


if __name__ == "__main__":
    unittest.main()
