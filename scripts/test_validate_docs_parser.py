#!/usr/bin/env python3
"""Focused regression tests for Markdown tables consumed by validate_docs."""

import shutil
import tempfile
import unittest
from pathlib import Path

from validate_docs import PRD_ROW_PATTERN, ROOT, table_rows, validate


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

    def test_candidate_without_lf_policy_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate = Path(temp_dir) / "candidate"
            shutil.copytree(
                ROOT,
                candidate,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            (candidate / ".gitattributes").unlink()

            errors = validate(candidate)

        self.assertIn("missing LF line-ending policy", errors)


if __name__ == "__main__":
    unittest.main()
