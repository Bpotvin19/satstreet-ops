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
            shutil.copy2(
                check_claims.ROOT / "brand" / name,
                self.root / "brand" / name,
            )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_prompt(self, text: str, name: str = "fixture.md") -> Path:
        path = self.root / "prompts" / name
        path.write_text(text, encoding="utf-8")
        return path

    def write_prompt_bytes(self, content: bytes, name: str) -> Path:
        path = self.root / "prompts" / name
        path.write_bytes(content)
        return path

    def errors(self) -> list[str]:
        errors, _, _ = check_claims.check(self.root)
        return errors

    def assert_has_error(self, expected: str) -> None:
        errors = self.errors()
        self.assertTrue(
            any(expected in error for error in errors),
            f"expected error containing {expected!r}; got {errors!r}",
        )

    def test_legitimate_self_contained_guardrail_text_passes(self) -> None:
        self.write_prompt(
            "No company fact is approved by default. "
            "For missing facts, write UNKNOWN or ASK LEGAL."
        )
        self.assertEqual(self.errors(), [])

    def test_every_supported_text_format_is_inspected(self) -> None:
        for suffix in sorted(check_claims.SUPPORTED_TEXT_SUFFIXES):
            with self.subTest(suffix=suffix):
                path = self.write_prompt("Internal draft.", "fixture" + suffix)
                self.assertEqual(self.errors(), [])
                path.unlink()

    def test_gitkeep_policy_text_is_inspected(self) -> None:
        self.write_prompt("Marketing copy promising zero slippage.", ".gitkeep")
        self.assert_has_error("forbidden phrase 'zero slippage'")

    def test_forbidden_claim_in_supported_file_fails(self) -> None:
        self.write_prompt("Marketing copy promising zero slippage.", "fixture.txt")
        self.assert_has_error("forbidden phrase 'zero slippage'")

    def test_retired_exemption_marker_does_not_bypass_enforcement(self) -> None:
        self.write_prompt(
            "<!-- claims-check: allow-forbidden-phrases -->\n"
            "Marketing copy promising zero slippage."
        )
        self.assert_has_error("forbidden phrase 'zero slippage'")

    def test_office_documents_fail_closed(self) -> None:
        for suffix in (".docx", ".xlsx", ".pptx", ".odt"):
            with self.subTest(suffix=suffix):
                path = self.write_prompt("uninspectable", "fixture" + suffix)
                self.assert_has_error("unsupported file type")
                path.unlink()

    def test_archives_fail_closed(self) -> None:
        for suffix in (".gz", ".zip", ".7z", ".tar", ".rar"):
            with self.subTest(suffix=suffix):
                path = self.write_prompt("uninspectable", "fixture" + suffix)
                self.assert_has_error("unsupported file type")
                path.unlink()

    def test_unknown_extension_fails_closed(self) -> None:
        self.write_prompt("uninspectable", "fixture.unknown")
        self.assert_has_error("unsupported file type")

    def test_invalid_utf8_in_supported_file_fails_closed(self) -> None:
        self.write_prompt_bytes(b"\xff\xfe\x80", "fixture.md")
        self.assert_has_error("is not valid UTF-8 text")

    def test_secret_scanning_runs_on_every_supported_text_format(self) -> None:
        fake_secret = "sk-" + "A" * 24
        for suffix in sorted(check_claims.SUPPORTED_TEXT_SUFFIXES):
            with self.subTest(suffix=suffix):
                path = self.write_prompt(fake_secret, "fixture" + suffix)
                self.assert_has_error("looks like a secret")
                path.unlink()

    def test_unicode_and_whitespace_evasions_fail(self) -> None:
        evasions = (
            "zero\u200b slippage",
            "zero\u00a0slippage",
            "zero\n\t slippage",
            "\uff5a\uff45\uff52\uff4f slippage",
        )
        for text in evasions:
            with self.subTest(text=repr(text)):
                path = self.write_prompt(text)
                self.assert_has_error("forbidden phrase 'zero slippage'")
                path.unlink()


if __name__ == "__main__":
    unittest.main()
