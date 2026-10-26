#!/usr/bin/env python3
"""Build the Fieldnotes-themed interactive roadmap tracker.

The vendored skill (`.agents/skills/resource-learning-library/`) is deliberately
left byte-exact. This script calls its generator to produce the functional
single-file app, then layers the Fieldnotes design system on top as a second
inline <style> block plus a few head/hero branding edits.

Run from the repository root:
    python3 learning-library/tools/build_tracker.py

Or from learning-library/:
    python3 tools/build_tracker.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # learning-library/
REPO = ROOT.parent                      # FieldNotes-HR/
SKILL_SCRIPTS = REPO / ".agents" / "skills" / "resource-learning-library" / "scripts"

sys.path.insert(0, str(SKILL_SCRIPTS))
import interactive_app  # noqa: E402  (vendored generator, imported not modified)

DATA_PATH = ROOT / "src" / "roadmap-app.json"
THEME_PATH = ROOT / "src" / "fieldnotes-theme.css"
OUTPUT_PATH = ROOT / "out" / "roadmap-app.html"


def facts(data: dict) -> list[str]:
    stages = data.get("stages", [])
    cards = sum(len(s.get("resources", [])) for s in stages)
    hours = sum(int(s.get("estimated_hours") or 0) for s in stages)
    week_numbers = [int(n) for s in stages for n in re.findall(r"\d+", str(s.get("duration", "")))]
    weeks = max(week_numbers) if week_numbers else 0
    free = sum(
        1 for s in stages for r in s.get("resources", [])
        if not str(r.get("cost", "")).lower().startswith("paid")
    )
    return [
        f"{len(stages):02d} STAGES",
        f"{cards} LEARNING CARDS",
        f"{hours} HOURS / {weeks} WEEKS",
        f"{free} VERIFIED FREE",
    ]


def transform(html: str, data: dict, theme_css: str) -> str:
    def sub(pattern: str, replacement: str, label: str) -> None:
        nonlocal html
        new, count = re.subn(pattern, lambda m: replacement, html, count=1)
        if count != 1:
            raise RuntimeError(f"branding anchor not found: {label}")
        html = new

    title = str(data.get("title") or "Learning roadmap")
    sub(r"<title>Learning roadmap</title>",
        f"<title>{title} | Fieldnotes HR</title>", "title")

    sub(r'<meta name="theme-color" content="#0B3D5C">',
        '<meta name="theme-color" content="#11142B">\n'
        '<meta name="color-scheme" content="light">\n'
        '<meta name="description" content="A free-first, roadmap-ordered learning '
        'library for breaking into HR through the Recruiter / Talent Acquisition '
        'path, with browser-local progress tracking.">', "theme-color meta")

    sub(r"<body>",
        '<body>\n<a class="skip-link" href="#roadmap">Skip to roadmap</a>', "body")

    sub(r'<p class="eyebrow">YOUR LEARNING ROADMAP</p>',
        '<p class="eyebrow">FIELDNOTES / HR</p>', "eyebrow")

    sub(r'<footer class="app-footer">A self-contained roadmap tracker\. Your progress is stored locally in this browser\.</footer>',
        '<footer class="app-footer">Made with love and fried plantain, by Moyinoluwa</footer>',
        "footer credit")

    # Web Interface Guidelines: form controls need a meaningful name and an
    # explicit autocomplete so password managers stay out of non-auth fields.
    sub(r'<input id="reminder-time" type="time" value="19:00">',
        '<input id="reminder-time" name="reminder-time" type="time" '
        'autocomplete="off" aria-label="Reminder time" '
        'title="Reminder time" value="19:00">', "reminder time input")
    sub(r'<input id="import-progress" type="file" accept="application/json,\.json">',
        '<input id="import-progress" name="import-progress" type="file" '
        'accept="application/json,.json">', "import file input")

    chips = "".join(f"<span>{text}</span>" for text in facts(data))
    sub(r'<p id="subtitle"></p>',
        '<p id="subtitle"></p>\n      '
        f'<div class="hero-facts" aria-label="Roadmap overview">{chips}</div>',
        "subtitle")

    style = '<style data-theme="fieldnotes">\n' + theme_css.rstrip() + "\n</style>\n"
    if "</head>" not in html:
        raise RuntimeError("branding anchor not found: </head>")
    html = html.replace("</head>", style + "</head>", 1)
    return html


def assert_self_contained(html: str) -> None:
    problems = []
    for pattern, label in (
        (r"<\s*link\b", "link element"),
        (r"<\s*img\b", "image element"),
        (r"<\s*iframe\b", "iframe element"),
    ):
        if re.search(pattern, html, re.I):
            problems.append(label)
    css_blocks = re.findall(r"<\s*style\b[^>]*>(.*?)<\s*/\s*style\s*>", html, re.I | re.S)
    if any(re.search(r"url\s*\(", css, re.I) for css in css_blocks):
        problems.append("CSS asset reference")
    for tag in re.finditer(r"<\s*script\b([^>]*)>", html, re.I):
        if re.search(r"\bsrc\s*=", tag.group(1), re.I):
            problems.append("external script")
    if html.count('data-theme="fieldnotes"') != 1:
        problems.append("theme block missing or duplicated")
    for token in ("--fn-ink:#11142B", "--fn-paper:#FFF8E7", "--fn-blue:#3768FF"):
        if token not in html:
            problems.append(f"missing token {token}")
    if problems:
        raise RuntimeError("not self-contained: " + ", ".join(problems))


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    theme_css = THEME_PATH.read_text(encoding="utf-8")

    # 1. Functional base from the vendored, hash-verified skill generator.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    interactive_app.build_app(data, OUTPUT_PATH)
    base = OUTPUT_PATH.read_text(encoding="utf-8")

    # 2. Layer the Fieldnotes design system on top.
    themed = transform(base, data, theme_css)
    assert_self_contained(themed)
    OUTPUT_PATH.write_text(themed, encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO)} ({len(themed.encode('utf-8'))} bytes)")
    print("Base generator: vendored skill (unmodified). Theme: Fieldnotes design system.")
    print("Checks: no external assets, no CSS asset refs, one theme block, tokens present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
