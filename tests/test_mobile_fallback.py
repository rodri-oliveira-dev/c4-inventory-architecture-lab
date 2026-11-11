"""Unit tests for the lightweight iOS companion bootstrap."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_mobile_fallback import (REDIRECT_MARKER, VIEWS, create_mobile_site,
                                   inject_fallback, mobile_html)


class MobileFallbackTests(unittest.TestCase):
    def test_injection_is_first_and_idempotent(self):
        html = '<!doctype html><html><head><script type="module" src="/assets/app.js"></script></head></html>'
        result = inject_fallback(html)
        self.assertLess(result.index(REDIRECT_MARKER), result.index('type="module"'))
        self.assertEqual(inject_fallback(result), result)
        self.assertIn("full", result)
        self.assertIn("max-width: 820px", result)

    def test_missing_head_rejected(self):
        with self.assertRaises(ValueError):
            inject_fallback("<html><body></body></html>")

    def test_generated_mobile_html_has_six_svg_views_without_scripts(self):
        html = mobile_html()
        self.assertEqual(html.count('loading="lazy"'), len(VIEWS))
        self.assertEqual(len(VIEWS), 6)
        self.assertIn("Visão leve", html)
        self.assertNotIn("<script", html)
        for name, _, file, _ in VIEWS:
            self.assertIn(f'id="{name}"', html)
            self.assertIn(file, html)

    def test_build_requires_all_svg_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "index.html").write_text("<html><head></head></html>", encoding="utf-8")
            (site / "mobile" / "diagrams").mkdir(parents=True)
            with self.assertRaises(FileNotFoundError):
                create_mobile_site(site)
            for _, _, name, _ in VIEWS:
                (site / "mobile" / "diagrams" / name).write_text("<svg/>", encoding="utf-8")
            create_mobile_site(site)
            self.assertTrue((site / "mobile" / "index.html").is_file())
            self.assertIn(REDIRECT_MARKER, (site / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
