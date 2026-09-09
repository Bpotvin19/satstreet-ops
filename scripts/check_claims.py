#!/usr/bin/env python3
"""Fail CI if required claims files are missing or drafts use forbidden phrases."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = ("templates", "drafts", "prompts")
UNSCANNABLE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip"}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xai-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"),
]


def phrases_from_forbidden_table(text: str) -> list[str]:
    phrases: list[str] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        phrase = cells[0]
        if phrase.lower() in {"phrase", ""} or set(phrase) <= {"-", "\u2014"}:
            continue
        phrases.append(phrase)
    return phrases


def iter_scan_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in SCAN_DIRS:
        directory = root / name
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                files.append(path)
    return files


def check(root: Path) -> tuple[list[str], int, int]:
    errors: list[str] = []
    allowed = root / "brand" / "claims-allowed.md"
    forbidden = root / "brand" / "claims-forbidden.md"

    if not allowed.is_file():
        errors.append("missing brand/claims-allowed.md")
    else:
        allowed_text = allowed.read_text(encoding="utf-8")
        if "**Status:**" not in allowed_text:
            errors.append("brand/claims-allowed.md is missing a Status header")

    if not forbidden.is_file():
        errors.append("missing brand/claims-forbidden.md")
        forbidden_phrases: list[str] = []
    else:
        forbidden_phrases = phrases_from_forbidden_table(
            forbidden.read_text(encoding="utf-8")
        )
        if not forbidden_phrases:
            errors.append("brand/claims-forbidden.md has no parseable phrases")

    scan_files = iter_scan_files(root)
    for path in scan_files:
        rel = path.relative_to(root)
        if path.suffix.lower() in UNSCANNABLE_SUFFIXES:
            errors.append(
                f"{rel}: unsupported binary format in claims-scanned directory"
            )
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for phrase in forbidden_phrases:
            if re.search(re.escape(phrase), text, flags=re.IGNORECASE):
                errors.append(f"{rel}: forbidden phrase {phrase!r}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: looks like a secret; remove it")

    return errors, len(forbidden_phrases), len(scan_files)


def main() -> int:
    errors, forbidden_count, scanned_count = check(ROOT)

    if errors:
        print("Claims CI failed:")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("Claims CI passed.")
    print("  allowed file: brand/claims-allowed.md")
    print(f"  forbidden phrases loaded: {forbidden_count}")
    print(f"  draft files scanned: {scanned_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
