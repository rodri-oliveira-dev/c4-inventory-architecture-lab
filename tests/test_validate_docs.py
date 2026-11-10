"""Minimal tests for the deterministic Markdown checker."""

import unittest

from scripts.validate_docs import anchors, slug


class GitHubSlugTests(unittest.TestCase):
    def test_accented_heading(self):
        self.assertEqual(slug("5. Cenário transversal: saída de 10 unidades"), "5-cenário-transversal-saída-de-10-unidades")

    def test_duplicate_headings(self):
        self.assertEqual(anchors("## Resultado\n## Resultado\n"), {"resultado", "resultado-1"})

    def test_inline_code(self):
        self.assertEqual(slug("Contrato de \x60RegistrarSaida\x60"), "contrato-de-registrarsaida")


if __name__ == "__main__":
    unittest.main()
