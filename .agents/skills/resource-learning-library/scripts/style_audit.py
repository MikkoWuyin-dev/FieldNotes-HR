#!/usr/bin/env python3
"""Audit a Markdown source for mechanical issues and prose patterns to review."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
THROAT_CLEARING = (
    "in today's fast-paced world",
    "in today’s fast-paced world",
    "in this guide, we will",
    "in this article, we will",
    "it is important to note",
    "it should be noted that",
    "let's dive in",
    "let’s dive in",
    "without further ado",
    "at the end of the day",
)
PUFFED_ADJECTIVES = (
    "comprehensive", "robust", "powerful", "seamless", "transformative",
    "innovative", "cutting-edge", "game-changing", "world-class", "unparalleled",
)
CONSULTANT_SPEAK = (
    "leverage", "synergy", "holistic", "stakeholder alignment", "end-to-end",
    "best-in-class", "unlock", "empower", "optimize", "optimization",
)
NOT_X_Y_RE = re.compile(
    r"\b(?:it['’]s|it is) not\b.{0,120}\b(?:it['’]s|it is|but rather|but instead)\b|"
    r"\bnot\b.{1,80}\bbut\b",
    re.I,
)
ADJECTIVE_TRIPLET_RE = re.compile(
    r"\b[\w-]+(?:ive|ous|ful|able|ible|al|ic|less),\s+"
    r"[\w-]+(?:ive|ous|ful|able|ible|al|ic|less)\s+(?:and|&)\s+"
    r"[\w-]+(?:ive|ous|ful|able|ible|al|ic|less)\b",
    re.I,
)


def _split_fences(text: str) -> tuple[str, int, bool]:
    """Return non-code prose, number of fence lines, and whether a fence remains open."""
    prose: list[str] = []
    fence_count = 0
    in_code = False
    for line in text.splitlines():
        if re.match(r"^\s*```", line):
            fence_count += 1
            in_code = not in_code
            continue
        if not in_code:
            prose.append(line)
    return "\n".join(prose), fence_count, in_code


def _line_no(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def audit_text(text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    findings: list[str] = []
    prose, fence_count, fence_open = _split_fences(text)

    if fence_count % 2:
        errors.append(f"odd number of fenced-code markers ({fence_count})")
    if fence_open:
        errors.append("unclosed fenced code block")

    bold_count = prose.count("**")
    if bold_count % 2:
        errors.append(f"unbalanced ** markers ({bold_count} occurrences outside fenced code)")

    for line_number, line in enumerate(prose.splitlines(), start=1):
        # Inline-code spans should open and close on the same line. Count isolated
        # backticks, but exclude escaped ones and the triple-fence syntax (already removed).
        inline_ticks = len(re.findall(r"(?<!\\)`", line))
        if inline_ticks % 2:
            errors.append(f"line {line_number}: odd number of inline backticks ({inline_ticks})")

    for match in LINK_RE.finditer(prose):
        label, raw_target = match.groups()
        target = raw_target.strip()
        line_number = _line_no(prose, match.start())
        if not label.strip():
            errors.append(f"line {line_number}: Markdown link has an empty label")
        if not target or any(char.isspace() for char in target):
            errors.append(f"line {line_number}: malformed link target {raw_target!r}")
            continue
        parts = urlsplit(target)
        if parts.scheme in {"http", "https"}:
            if not parts.netloc:
                errors.append(f"line {line_number}: URL has no host: {target}")
        elif parts.scheme == "mailto":
            if not parts.path:
                errors.append(f"line {line_number}: mailto link has no address")
        elif parts.scheme:
            errors.append(f"line {line_number}: unsafe or unsupported link scheme {parts.scheme!r}")
        elif not target.startswith(("#", "/", "./", "../")):
            # Bare relative paths are allowed, but call out unusual targets.
            if "://" in target:
                errors.append(f"line {line_number}: malformed link target {target!r}")

    lower = prose.lower()
    seen_findings: set[tuple[int, str]] = set()
    for phrase in THROAT_CLEARING:
        start = 0
        while True:
            offset = lower.find(phrase, start)
            if offset < 0:
                break
            key = (_line_no(prose, offset), f"throat-clearing phrase: {phrase}")
            seen_findings.add(key)
            start = offset + len(phrase)

    for phrase in PUFFED_ADJECTIVES:
        for match in re.finditer(rf"\b{re.escape(phrase)}\b", lower):
            seen_findings.add((_line_no(prose, match.start()), f"inflated adjective to review: {phrase}"))

    for phrase in CONSULTANT_SPEAK:
        for match in re.finditer(rf"\b{re.escape(phrase)}\b", lower):
            seen_findings.add((_line_no(prose, match.start()), f"consultant-speak to review: {phrase}"))

    for match in NOT_X_Y_RE.finditer(prose):
        seen_findings.add((_line_no(prose, match.start()), "possible ‘not X, but Y’ rhetorical turn"))

    for match in ADJECTIVE_TRIPLET_RE.finditer(prose):
        seen_findings.add((_line_no(prose, match.start()), f"possible three-adjective tic: {match.group(0)}"))

    findings.extend(f"line {line}: {message}" for line, message in sorted(seen_findings))
    return errors, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", help="Markdown source to audit")
    args = parser.parse_args(argv)
    path = Path(args.markdown)
    if not path.is_file():
        print(f"ERROR: source file not found: {path}", file=sys.stderr)
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: could not read {path}: {exc}", file=sys.stderr)
        return 2

    errors, findings = audit_text(text)
    for error in errors:
        print(f"ERROR: {error}")
    for finding in findings:
        print(f"REVIEW: {finding}")
    if not findings:
        print("REVIEW: no prose-pattern flags")
    print(f"SUMMARY: {len(errors)} mechanical error(s); {len(findings)} style finding(s) to review")
    # Style findings invite human judgment. Only mechanical breakage fails the audit.
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
