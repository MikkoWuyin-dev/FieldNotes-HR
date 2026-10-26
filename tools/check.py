#!/usr/bin/env python3
"""One-command verification for FieldNotes-HR.

Every claim this repository makes about its own output is checked here, so a
reviewer (or CI) can reproduce the verification instead of trusting prose in a
README. Run via `make check` / `make check-drift`, or directly:

    .venv/bin/python tools/check.py                 # all fast checks
    .venv/bin/python tools/check.py drift          # full output reproduction
    .venv/bin/python tools/check.py contract       # just one check
    .venv/bin/python tools/check.py all --strict   # freshness warnings are fatal
    .venv/bin/python tools/check.py pin-hashes     # refresh the skill inventory

Only the Python standard library plus the pinned requirements.lock packages are
needed. Nothing here modifies tracked files except the explicit `pin-hashes`
command.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html as html_mod
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / ".agents" / "skills" / "resource-learning-library"
SCRIPTS = SKILL / "scripts"
LIB = REPO / "learning-library"
SRC = LIB / "src"
OUT = LIB / "out"
BUILD_TOOLS = LIB / "tools"
DOCS = REPO / "docs"
MD = SRC / "recruiter-talent-acquisition-library.md"
DATA = SRC / "roadmap-app.json"
MANIFEST = SRC / "verification-manifest.json"
TRACKER = OUT / "roadmap-app.html"
LINKS_SH = LIB / "check-links.sh"
HASH_FILE = REPO / "tools" / "skill-hashes.sha256"
MAKEFILE = REPO / "Makefile"

TITLE = "From zero to first recruiter role"
SUBTITLE = "A roadmap-ordered learning library for an absolute beginner"
HERO_META = "Lagos, Nigeria - verified 26 October 2026 - about 94 hours over 20 weeks"
BASE_NAME = "Recruiter-TA-Library"

CHECKS: dict[str, object] = {}

# Backticked filenames that are legitimately NOT files in this repository:
# parts of the upstream design repo, a DOCX archive part, an out-of-repo
# session upload, a generated report, and a file deliberately removed. Anything
# not on this list that looks like a repo path must resolve, or the docs lint
# fails. Keep this list small and explicit.
EXTERNAL_PATH_TOKENS = {
    "word/document.xml",                      # a part inside the DOCX zip
    "index.html",                             # upstream Nature Photography repo
    "AUDIT-PLAIN.md",                         # upstream Nature Photography repo
    "docs/headless-chromium.md",              # upstream Nature Photography repo
    "resource-learning-library-transfer.md",  # session upload, never committed
    "link-status.tsv",                        # generated report, gitignored
    "tools/visual/.cache/last-run.json",      # generated browser report, gitignored
    ".claude/settings.local.json",            # removed per-developer file
    "settings.local.json",                    # removed per-developer file
}


class Warn(Exception):
    """A check that succeeded but has something a human should look at."""


def check(name: str):
    def decorate(fn):
        CHECKS[name] = fn
        return fn
    return decorate


def run(argv: list[str], cwd: Path = REPO) -> str:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [str(a) for a in argv], cwd=cwd, env=env,
        capture_output=True, text=True,
    )
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        tail = "\n".join(output.splitlines()[-12:])
        raise AssertionError(
            f"exit {proc.returncode}: {' '.join(str(a) for a in argv)}\n{tail}"
        )
    return output


def load_data() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def import_builder():
    """Import the repo-local build layer and the vendored generator."""
    if str(BUILD_TOOLS) not in sys.path:
        sys.path.insert(0, str(BUILD_TOOLS))
    import build_tracker  # noqa: F401  (registers SKILL_SCRIPTS on sys.path)
    import interactive_app
    return build_tracker, interactive_app


# --------------------------------------------------------------------------
# 1. The vendored skill really is byte-exact.
# --------------------------------------------------------------------------
@check("skill-hashes")
def check_skill_hashes() -> str:
    if not HASH_FILE.is_file():
        raise AssertionError(f"missing inventory: {HASH_FILE}")
    expected: dict[str, str] = {}
    for line in HASH_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, sep, rel = line.partition("  ")
        if not sep:
            raise AssertionError(f"malformed inventory line: {line}")
        expected[rel.strip()] = digest.strip()

    actual = {
        p.relative_to(REPO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(SKILL.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc")
    }
    problems = []
    for rel, digest in expected.items():
        if rel not in actual:
            problems.append(f"missing: {rel}")
        elif actual[rel] != digest:
            problems.append(f"CHANGED: {rel}")
    for rel in actual:
        if rel not in expected:
            problems.append(f"unexpected file in vendored skill: {rel}")
    if problems:
        raise AssertionError("; ".join(problems))
    return f"{len(expected)} vendored files byte-exact (SHA-256)"


# --------------------------------------------------------------------------
# 2. The skill's own test suite still passes in this environment.
# --------------------------------------------------------------------------
@check("unit")
def check_unit() -> str:
    out = run([sys.executable, "-m", "unittest", "discover",
               "-s", str(SKILL / "tests"), "-v"], cwd=SKILL)
    m = re.search(r"Ran (\d+) tests?", out)
    n = m.group(1) if m else "?"
    if re.search(r"FAILED|ERROR", out):
        raise AssertionError("unittest reported a failure:\n" + "\n".join(out.splitlines()[-12:]))
    return f"{n} vendored skill tests OK"


# --------------------------------------------------------------------------
# 3. The shipped files pass the skill's validators.
# --------------------------------------------------------------------------
@check("validators")
def check_validators() -> str:
    run([sys.executable, SCRIPTS / "validate_build.py",
         OUT / f"{BASE_NAME}.pdf", OUT / f"{BASE_NAME}.docx",
         OUT / f"{BASE_NAME}.html"])
    run([sys.executable, SCRIPTS / "validate_build.py",
         "--interactive-html", TRACKER])
    return "PDF, DOCX, static HTML and interactive HTML validated"


# --------------------------------------------------------------------------
# 4. Prose style audit.
# --------------------------------------------------------------------------
@check("style")
def check_style() -> str:
    out = run([sys.executable, SCRIPTS / "style_audit.py", MD])
    last = out.splitlines()[-1] if out.splitlines() else "clean"
    return f"style_audit: {last.strip()[:100]}"


# --------------------------------------------------------------------------
# 5. Contract between the build layer and the frozen generator.
# --------------------------------------------------------------------------
@check("contract")
def check_contract() -> str:
    bt, interactive_app = import_builder()
    data = load_data()
    theme = (SRC / "fieldnotes-theme.css").read_text(encoding="utf-8")
    edits = bt.branding_edits(data)

    with tempfile.TemporaryDirectory() as td:
        base_path = Path(td) / "base.html"
        interactive_app.build_app(data, base_path)
        base = base_path.read_text(encoding="utf-8")

        # A clean build reproduces the committed tracker exactly.
        themed = bt.transform(base, data, theme)
        bt.assert_self_contained(themed)
        if themed != TRACKER.read_text(encoding="utf-8"):
            raise AssertionError("a fresh build no longer matches out/roadmap-app.html")

        # Every anchor still matches the live generator output, and breaking
        # any one of them fails loudly with its own label.
        for pattern, _replacement, label in edits:
            m = re.search(pattern, base)
            if not m:
                raise AssertionError(f"anchor no longer matches generator output: {label}")
            broken = base[:m.start()] + "__BROKEN_ANCHOR__" + base[m.end():]
            try:
                bt.transform(broken, data, theme)
            except RuntimeError as exc:
                if label not in str(exc):
                    raise AssertionError(
                        f"anchor {label!r} failed with the wrong message: {exc}"
                    ) from exc
            else:
                raise AssertionError(f"breaking anchor {label!r} did not fail the build")

        # The </head> injection point is part of the contract too.
        try:
            bt.transform(base.replace("</head>", "", 1), data, theme)
        except RuntimeError as exc:
            if "</head>" not in str(exc):
                raise AssertionError(f"unexpected </head> failure: {exc}") from exc
        else:
            raise AssertionError("removing </head> did not fail the build")

        # Self-containment is enforced, not just asserted in a doc.
        try:
            bt.assert_self_contained(themed.replace("<body>", '<img src="x"><body>', 1))
        except RuntimeError:
            pass
        else:
            raise AssertionError("assert_self_contained accepted an <img> element")

    return (f"{len(edits)} branding anchors + </head> verified; "
            "each fails loudly when broken; tracker bit-exact")


# --------------------------------------------------------------------------
# 6. The two content sources and the shipped tracker agree.
# --------------------------------------------------------------------------
@check("sources")
def check_sources() -> str:
    data = load_data()
    md = MD.read_text(encoding="utf-8")
    stages = data["stages"]
    resources = [r for s in stages for r in s["resources"]]
    json_urls = {r["url"] for r in resources}
    md_urls = {u.rstrip(".,;)") for u in
               re.findall(r"https?://[^\s\"<>)\]]+", md)}
    if json_urls != md_urls:
        only_json = sorted(json_urls - md_urls)
        only_md = sorted(md_urls - json_urls)
        raise AssertionError(f"URL mismatch; only in JSON: {only_json}; only in Markdown: {only_md}")

    md_stage_titles = re.findall(r"^## (Stage \d+:[^\n]*)", md, re.M)
    json_stage_titles = [s["title"] for s in stages]
    if md_stage_titles != json_stage_titles:
        raise AssertionError("stage headings in Markdown differ from roadmap-app.json")

    n_h3 = len(re.findall(r"^### ", md, re.M))
    if n_h3 != len(resources):
        raise AssertionError(f"Markdown has {n_h3} resource headings, JSON has {len(resources)}")

    hours = sum(int(s.get("estimated_hours") or 0) for s in stages)
    if (OUT / f"{BASE_NAME}.md").read_bytes() != MD.read_bytes():
        raise AssertionError("out/Recruiter-TA-Library.md has drifted from src/")

    tracker = html_mod.unescape(TRACKER.read_text(encoding="utf-8"))
    missing = sorted(u for u in json_urls if u not in tracker)
    if missing:
        raise AssertionError(f"URLs missing from the tracker: {missing}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_urls = {e["url"] for e in manifest["urls"]}
    link_urls = set(re.findall(r'^\s*"(https?://[^"]+)"',
                               LINKS_SH.read_text(encoding="utf-8"), re.M))
    if not json_urls <= manifest_urls:
        raise AssertionError("verification manifest does not cover every resource URL")
    if link_urls != manifest_urls:
        raise AssertionError("check-links.sh and verification-manifest.json URL sets differ")

    return (f"{len(stages)} stages / {len(resources)} cards / {hours} h / "
            f"{len(json_urls)} URLs agree across JSON, Markdown, tracker, manifest")


# --------------------------------------------------------------------------
# 7. Documentation lint: stale claims, broken paths, phantom make targets.
# --------------------------------------------------------------------------
@check("docs")
def check_docs() -> str:
    problems: list[str] = []
    doc_paths = [
        REPO / "README.md", LIB / "README.md", LIB / "DESIGN-SYSTEM.md",
        REPO / ".agents" / "skills" / "README.md", DOCS / "SETUP.md",
        DOCS / "DESIGN-SPEC.md", REPO / "RETROSPECTIVE.md",
        REPO / "CHANGELOG.md",
    ]
    for p in doc_paths:
        if not p.is_file():
            problems.append(f"missing canonical document: {p.relative_to(REPO)}")

    design_system = LIB / "DESIGN-SYSTEM.md"
    if design_system.is_file():
        text = design_system.read_text(encoding="utf-8")
        for phrase in (
            "only the first (provider) chip and the cost chip",
            "the long metadata chips stay quiet cream",
        ):
            if phrase in text:
                problems.append(f"stale tag-colour claim in DESIGN-SYSTEM.md: {phrase!r}")

    if LINKS_SH.is_file() and "NOT RUN" in LINKS_SH.read_text(encoding="utf-8"):
        problems.append("check-links.sh still claims the sweep was never run")

    extensions = (".py", ".md", ".json", ".css", ".html", ".sh", ".yml",
                  ".yaml", ".lock", ".txt", ".sha256", ".pdf", ".docx",
                  ".tsv", ".xml")
    token_re = re.compile(r"`([^`\n]+)`")
    for doc in doc_paths:
        if not doc.is_file():
            continue
        for raw in token_re.findall(doc.read_text(encoding="utf-8")):
            token = raw.strip()
            if not token.endswith(extensions):
                continue
            if token in EXTERNAL_PATH_TOKENS:
                continue
            if any(c in token for c in ("$", " ", "*", "://", "...", "<", ">")):
                continue
            candidates = [
                REPO / token, LIB / token, LIB / "src" / token,
                LIB / "out" / token, LIB / "tools" / token,
                REPO / "tools" / token, SKILL / token,
                SKILL / "scripts" / Path(token).name, DOCS / token,
            ]
            if not any(c.exists() for c in candidates):
                problems.append(f"{doc.relative_to(REPO)}: referenced path missing: {token}")

    if MAKEFILE.is_file():
        targets = set(re.findall(r"^([a-zA-Z][a-zA-Z0-9_-]*):", MAKEFILE.read_text(), re.M))
        for doc in doc_paths:
            if not doc.is_file():
                continue
            # Only code-formatted `make <target>` mentions are linted. Matching
            # bare prose would flag ordinary sentences such as "make the change".
            for code_span in token_re.findall(doc.read_text(encoding="utf-8")):
                for target in re.findall(r"\bmake\s+([a-zA-Z][a-zA-Z0-9_-]*)",
                                         code_span):
                    if target not in targets:
                        problems.append(
                            f"{doc.name}: 'make {target}' has no Makefile target"
                        )
    else:
        problems.append("Makefile missing")

    if problems:
        raise AssertionError("; ".join(problems[:8]) + (
            f" … and {len(problems) - 8} more" if len(problems) > 8 else ""
        ))
    return "no stale claims; referenced paths and make targets exist"


# --------------------------------------------------------------------------
# 8. Research freshness (warning by default, fatal under --strict).
# --------------------------------------------------------------------------
@check("freshness")
def check_freshness(today: dt.date | None = None, strict: bool = False) -> str:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    today = today or dt.date.today()
    max_age = int(manifest.get("max_age_days", 90))
    stale: list[str] = []
    gaps: list[str] = []
    for entry in manifest["urls"]:
        when = entry.get("verified_at")
        if not when or entry.get("status") != "confirmed":
            gaps.append(f"{entry['status']}: {entry['url']}")
            continue
        age = (today - dt.date.fromisoformat(when)).days
        if age > max_age:
            stale.append(f"{entry['url']} ({age} days old)")
    if not stale and not gaps:
        return f"all {len(manifest['urls'])} URLs verified within {max_age} days"

    lines = [f"{len(stale)} stale (> {max_age} days), {len(gaps)} open verification gaps"]
    lines += [f"  STALE {s}" for s in stale[:5]]
    lines += [f"  GAP   {g}" for g in gaps[:5]]
    message = "\n".join(lines)
    if strict:
        raise AssertionError(message)
    raise Warn(message)


# --------------------------------------------------------------------------
# 9. Full rebuild: every shipped output still reproduces from source.
# --------------------------------------------------------------------------
@check("drift")
def check_drift() -> str:
    bt, interactive_app = import_builder()
    data = load_data()
    theme = (SRC / "fieldnotes-theme.css").read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        built = tmp / "roadmap-app.html"
        interactive_app.build_app(data, built)
        themed = bt.transform(built.read_text(encoding="utf-8"), data, theme)
        if themed != TRACKER.read_text(encoding="utf-8"):
            raise AssertionError("out/roadmap-app.html has drifted from src/")

        run([sys.executable, SCRIPTS / "docx_render.py", MD,
             "-o", str(tmp), "--name", BASE_NAME,
             "--title", TITLE, "--subtitle", SUBTITLE,
             "--hero-meta", HERO_META,
             "--format", "md", "html", "pdf", "docx"], cwd=LIB)

        for name in (f"{BASE_NAME}.md", f"{BASE_NAME}.html"):
            if (tmp / name).read_bytes() != (OUT / name).read_bytes():
                raise AssertionError(f"out/{name} has drifted from src/")

        # DOCX bytes differ only in ZIP metadata; compare archive contents.
        with (zipfile.ZipFile(OUT / f"{BASE_NAME}.docx") as committed,
              zipfile.ZipFile(tmp / f"{BASE_NAME}.docx") as fresh):
            if committed.namelist() != fresh.namelist():
                raise AssertionError("DOCX archive parts differ")
            for part in committed.namelist():
                if committed.read(part) != fresh.read(part):
                    raise AssertionError(f"DOCX part has drifted: {part}")

        # PDF embeds a creation timestamp; compare extracted text instead.
        from pypdf import PdfReader
        def pdf_text(path: Path) -> str:
            return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
        if pdf_text(OUT / f"{BASE_NAME}.pdf") != pdf_text(tmp / f"{BASE_NAME}.pdf"):
            raise AssertionError("PDF text has drifted from src/")

    return ("all 5 outputs reproduce (PDF by extracted text, DOCX by archive "
            "entries; binary timestamps ignored)")


# --------------------------------------------------------------------------

def pin_hashes() -> None:
    lines = [
        "# SHA-256 inventory of the vendored resource-learning-library skill.",
        "# Recorded 27 October 2026. These 12 files are the transfer bundle,",
        "# reconstructed byte-exactly. They must never be edited in place.",
        "#",
        "# Verify:  python3 tools/check.py skill-hashes",
        "# Refresh (only after an intentional skill upgrade): make pin-skill",
        "#",
    ]
    for p in sorted(SKILL.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc"):
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f"{digest}  {p.relative_to(REPO).as_posix()}")
    HASH_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines) - 6} hashes to {HASH_FILE.relative_to(REPO)}")


FAST = ("skill-hashes", "unit", "validators", "style", "contract",
        "sources", "docs", "freshness")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("checks", nargs="*",
                        help=f"checks to run (default: {' '.join(FAST)}); "
                             "'all' = fast checks, 'drift' = full reproduction, "
                             "'pin-hashes' rewrites the skill inventory")
    parser.add_argument("--strict", action="store_true",
                        help="make freshness warnings fatal")
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    args = parser.parse_args(argv)

    if args.checks == ["pin-hashes"]:
        pin_hashes()
        return 0

    selected: list[str] = []
    for name in args.checks or list(FAST):
        if name in ("all", "fast"):
            selected.extend(FAST)
        elif name == "everything":
            selected.extend(FAST)
            selected.append("drift")
        elif name in CHECKS:
            selected.append(name)
        else:
            parser.error(f"unknown check {name!r}; choose from: "
                         f"{', '.join(CHECKS)}")
    # Preserve order, drop duplicates.
    selected = list(dict.fromkeys(selected))

    today = dt.date.fromisoformat(args.today) if args.today else None
    results: list[tuple[str, str, str]] = []
    for name in selected:
        fn = CHECKS[name]
        try:
            if name == "freshness":
                message = fn(today=today, strict=args.strict)
            else:
                message = fn()
        except Warn as exc:
            results.append(("WARN", name, str(exc)))
        except Exception as exc:  # noqa: BLE001 - report every failure, don't stop
            results.append(("FAIL", name, str(exc)))
        else:
            results.append((" OK ", name, message))

    width = max(len(n) for _, n, _ in results) if results else 1
    print(f"\nFieldNotes-HR verification — {len(selected)} check(s)")
    print("-" * 72)
    for status, name, message in results:
        print(f"[{status}] {name:<{width}}  {message}")
    print("-" * 72)
    failed = sum(1 for s, _, _ in results if s == "FAIL")
    warned = sum(1 for s, _, _ in results if s == "WARN")
    print(f"RESULT: {len(results) - failed - warned} passed, {warned} warned, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
