from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import check_claims


class ClaimsCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "brand").mkdir()
        (self.root / "prompts").mkdir()
        for name in ("claims-allowed.md", "claims-forbidden.md"):
            shutil.copy2(check_claims.ROOT / "brand" / name, self.root / "brand" / name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_prompt(self, text: str, name: str = "fixture.md") -> None:
        (self.root / "prompts" / name).write_text(text, encoding="utf-8")

    def errors(self) -> list[str]:
        errors, _, _ = check_claims.check(self.root)
        return errors

    def test_legitimate_guardrail_text_passes(self) -> None:
        self.write_prompt(
            "Apply every restriction in brand/claims-forbidden.md. "
            "Do not reproduce its prohibited phrases."
        )
        self.assertEqual(self.errors(), [])

    def test_prohibited_claim_in_ordinary_prompt_fails(self) -> None:
        self.write_prompt("Marketing copy promising zero slippage.")
        self.assertTrue(any("forbidden phrase 'zero slippage'" in e for e in self.errors()))

    def test_retired_exemption_marker_does_not_bypass_enforcement(self) -> None:
        self.write_prompt(
            "<!-- claims-check: allow-forbidden-phrases -->\n"
            "Marketing copy promising zero slippage."
        )
        self.assertTrue(any("forbidden phrase 'zero slippage'" in e for e in self.errors()))

    def test_secret_scanning_remains_active(self) -> None:
        fake_secret = "sk-" + "A" * 24
        self.write_prompt(
            "<!-- claims-check: allow-forbidden-phrases -->\n" + fake_secret
        )
        self.assertTrue(any("looks like a secret" in e for e in self.errors()))

    def test_prompt_cannot_evade_scanning_with_binary_suffix(self) -> None:
        self.write_prompt("Marketing copy promising zero slippage.", "fixture.pdf")
        self.assertTrue(
            any("unsupported binary format" in error for error in self.errors())
        )


if __name__ == "__main__":
    unittest.main()
