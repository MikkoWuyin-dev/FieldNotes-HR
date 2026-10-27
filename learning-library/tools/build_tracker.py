#!/usr/bin/env python3
"""Build the Fieldnotes-themed interactive roadmap tracker.

The vendored skill (`.agents/skills/resource-learning-library/`) is deliberately
left byte-exact. This script calls its generator to produce the functional
single-file app, then layers on:

  * the Fieldnotes design system (a second inline <style> block plus head/hero
    branding edits), and
  * ten optional Piixpal pixel creatures (a third inline <style> block, an inert
    <template> holding the MIT-licensed engine, and a small inline controller).
    They lazy-load on idle, can be paused, and stay off under reduced motion.

Everything stays inline: no external fonts, images, scripts or network calls.

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
PALS_DIR = ROOT / "src" / "pals"
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


def load_pals_sources() -> dict:
    """Read every pals source file. Shared by main(), tools/check.py and CI."""
    return {
        "config": json.loads((PALS_DIR / "pals.json").read_text(encoding="utf-8")),
        "css": (PALS_DIR / "pals.css").read_text(encoding="utf-8"),
        "payload": (PALS_DIR / "piixpal-payload.html").read_text(encoding="utf-8"),
        "controller": (PALS_DIR / "pals-controller.js").read_text(encoding="utf-8"),
    }


def pals_edits(src: dict) -> list[tuple[str, str, str]]:
    """(anchor regex, literal replacement, label) triples for the pals layer.

    Kept separate from `branding_edits` so the original eight-anchor contract
    still describes only the Fieldnotes branding, and `tools/check.py` can break
    each of these three anchors independently too.
    """
    pals = src["config"]["pals"]
    controller = src["controller"].replace(
        "__SITE_PALS_JSON__", json.dumps(pals, separators=(",", ":"))
    )
    if "__SITE_PALS_JSON__" in controller:
        raise RuntimeError("SITE_PALS placeholder was not replaced")

    style = '<style data-pals="fieldnotes">\n' + src["css"].rstrip() + "\n</style>\n"
    controls = (
        '<div class="pals-controls" id="pals-controls" hidden>\n'
        '  <button id="pals-toggle" type="button" aria-pressed="true">Pause tiny pals</button>\n'
        '  <p class="pals-status" id="pals-status" role="status" aria-live="polite"></p>\n'
        '</div>\n'
    )
    script = ('<script data-fieldnotes-pals-controller>\n'
              + controller.rstrip() + "\n</script>\n")
    payload = src["payload"].rstrip()

    return [
        (r"</head>", style + "</head>", "pals style"),
        (r'<main id="roadmap" aria-label="Roadmap stages"></main>',
         controls + '<main id="roadmap" aria-label="Roadmap stages"></main>',
         "pals controls"),
        (r"</body>", payload + "\n" + script + "</body>",
         "pals payload and controller"),
    ]


def inject_pals(html: str, src: dict) -> str:
    """Layer the optional decorative pals onto the already-themed app."""
    for pattern, replacement, label in pals_edits(src):
        # A lambda keeps the replacement literal: no backreference expansion.
        new, count = re.subn(pattern, lambda _m, r=replacement: r, html, count=1)
        if count != 1:
            raise RuntimeError(f"pals anchor not found: {label}")
        html = new
    return html


def branding_edits(data: dict) -> list[tuple[str, str, str]]:
    """The contract between this build layer and the vendored generator's HTML.

    Each triple is (anchor regex, literal replacement, human label). These
    anchors are exact strings emitted by the unmodified `interactive_app.py`.
    `tools/check.py` verifies that every anchor still matches the generator's
    live output and that breaking any single one fails the build loudly, so a
    future generator update cannot silently drop the Fieldnotes branding.
    """
    title = str(data.get("title") or "Learning roadmap")
    chips = "".join(f"<span>{text}</span>" for text in facts(data))
    return [
        (r"<title>Learning roadmap</title>",
         f"<title>{title} | Fieldnotes HR</title>", "title"),

        (r'<meta name="theme-color" content="#0B3D5C">',
         '<meta name="theme-color" content="#11142B">\n'
         '<meta name="color-scheme" content="light">\n'
         '<meta name="description" content="A free-first, roadmap-ordered learning '
         'library for breaking into HR through the Recruiter / Talent Acquisition '
         'path, with browser-local progress tracking.">', "theme-color meta"),

        (r"<body>",
         '<body>\n<a class="skip-link" href="#roadmap">Skip to roadmap</a>', "body"),

        (r'<p class="eyebrow">YOUR LEARNING ROADMAP</p>',
         '<p class="eyebrow">FIELDNOTES / HR</p>', "eyebrow"),

        (r'<footer class="app-footer">A self-contained roadmap tracker\. Your progress is stored locally in this browser\.</footer>',
         '<footer class="app-footer">Made with love and fried plantain, by Moyinoluwa</footer>',
         "footer credit"),

        # Web Interface Guidelines: form controls need a meaningful name and an
        # explicit autocomplete so password managers stay out of non-auth fields.
        (r'<input id="reminder-time" type="time" value="19:00">',
         '<input id="reminder-time" name="reminder-time" type="time" '
         'autocomplete="off" aria-label="Reminder time" '
         'title="Reminder time" value="19:00">', "reminder time input"),

        (r'<input id="import-progress" type="file" accept="application/json,\.json">',
         '<input id="import-progress" name="import-progress" type="file" '
         'accept="application/json,.json">', "import file input"),

        (r'<p id="subtitle"></p>',
         '<p id="subtitle"></p>\n      '
         f'<div class="hero-facts" aria-label="Roadmap overview">{chips}</div>',
         "subtitle"),
    ]


def transform(html: str, data: dict, theme_css: str) -> str:
    for pattern, replacement, label in branding_edits(data):
        # A lambda keeps the replacement literal: no backreference expansion.
        new, count = re.subn(pattern, lambda _m, r=replacement: r, html, count=1)
        if count != 1:
            raise RuntimeError(f"branding anchor not found: {label}")
        html = new

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
    if html.count('data-pals="fieldnotes"') != 1:
        problems.append("pals style block missing or duplicated")
    for marker in ('id="pals-payload"', 'id="pals-controls"',
                   'id="pals-toggle"', "data-fieldnotes-pals-controller"):
        if html.count(marker) != 1:
            problems.append(f"pals marker missing or duplicated: {marker}")
    if "Piixpal v0.4.0" not in html or "MIT" not in html:
        problems.append("Piixpal MIT provenance header missing")
    for pattern, label in (
        (r"<\s*script[^>]*\bsrc\s*=", "external script src"),
        (r"\bfetch\s*\(", "network call in pals layer"),
        (r"XMLHttpRequest", "network call in pals layer"),
        (r"WebSocket", "network call in pals layer"),
    ):
        if re.search(pattern, html, re.I):
            problems.append(label)
    if problems:
        raise RuntimeError("not self-contained: " + ", ".join(problems))


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    theme_css = THEME_PATH.read_text(encoding="utf-8")
    pals_src = load_pals_sources()

    # 1. Functional base from the vendored, hash-verified skill generator.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    interactive_app.build_app(data, OUTPUT_PATH)
    base = OUTPUT_PATH.read_text(encoding="utf-8")

    # 2. Layer the Fieldnotes design system, then the optional pals, on top.
    themed = transform(base, data, theme_css)
    themed = inject_pals(themed, pals_src)
    assert_self_contained(themed)
    OUTPUT_PATH.write_text(themed, encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO)} ({len(themed.encode('utf-8'))} bytes)")
    print("Base generator: vendored skill (unmodified). Theme: Fieldnotes design system.")
    print(f"Pals: {len(pals_src['config']['pals'])} Piixpal creatures (MIT), "
          "lazy-loaded, pausable, off under reduced motion.")
    print("Checks: no external assets, no CSS asset refs, no network calls, "
          "theme + pals blocks present, tokens present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
