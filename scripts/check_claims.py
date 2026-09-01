#!/usr/bin/env python3
"""Fail CI if required claims files are missing or drafts use forbidden phrases."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = ROOT / "brand" / "claims-allowed.md"
FORBIDDEN = ROOT / "brand" / "claims-forbidden.md"
SCAN_DIRS = ("templates", "drafts", "prompts")
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip"}

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


def iter_scan_files() -> list[Path]:
    files: list[Path] = []
    for name in SCAN_DIRS:
        directory = ROOT / name
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix.lower() not in SKIP_SUFFIXES:
                files.append(path)
    return files


def main() -> int:
    errors: list[str] = []

    if not ALLOWED.is_file():
        errors.append("missing brand/claims-allowed.md")
    else:
        allowed_text = ALLOWED.read_text(encoding="utf-8")
        if "**Status:**" not in allowed_text:
            errors.append("brand/claims-allowed.md is missing a Status header")

    if not FORBIDDEN.is_file():
        errors.append("missing brand/claims-forbidden.md")
        forbidden_phrases: list[str] = []
    else:
        forbidden_phrases = phrases_from_forbidden_table(
            FORBIDDEN.read_text(encoding="utf-8")
        )
        if not forbidden_phrases:
            errors.append("brand/claims-forbidden.md has no parseable phrases")

    for path in iter_scan_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for phrase in forbidden_phrases:
            if re.search(re.escape(phrase), text, flags=re.IGNORECASE):
                errors.append(f"{rel}: forbidden phrase {phrase!r}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: looks like a secret; remove it")

    if errors:
        print("Claims CI failed:")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("Claims CI passed.")
    print(f"  allowed file: {ALLOWED.relative_to(ROOT)}")
    print(f"  forbidden phrases loaded: {len(forbidden_phrases)}")
    print(f"  draft files scanned: {len(iter_scan_files())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
