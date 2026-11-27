#!/usr/bin/env python3
"""Focused regression tests for Markdown tables consumed by validate_docs."""

import unittest

from validate_docs import PRD_ROW_PATTERN, table_rows


class PrdTableParserTests(unittest.TestCase):
    def test_acceptance_ids_allow_markdown_alignment_padding(self):
        markdown = (
            "| Critério | Regras | Aceite |\n"
            "| --- | --- | --- |\n"
            "| A01      | H01      | Bootstrap reproduzível |\n"
            "| X16 | F05 → F06 | integrated | R05 | Canais compartilham ledger |\n"
            "| P06 | Entrega em clone limpo |\n"
        )

        self.assertEqual(
            table_rows(markdown, PRD_ROW_PATTERN),
            [
                ("A01", "H01", "Bootstrap reproduzível"),
                ("X16", "F05 → F06", "integrated", "R05", "Canais compartilham ledger"),
                ("P06", "Entrega em clone limpo"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
