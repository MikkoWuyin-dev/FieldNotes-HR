# Setup and verification — the canonical guide

This is the single source of truth for setting up, building and verifying
FieldNotes-HR. If another document disagrees with this one, this one wins and
the other should be corrected. The historical port record is
`learning-library/DESIGN-SYSTEM.md`; the current design contract is
`docs/DESIGN-SPEC.md`; the history of changes is `CHANGELOG.md`.

## Why this document exists

The original work was repeatedly slowed down by an environment that vanished
between sessions, by verification that existed only in prose, and by five
documents describing setup differently. Every step below is now a `make`
target, and every one of them runs in CI via `.github/workflows/verify.yml`.

## Prerequisites

| Tool | Version | Needed for |
|---|---|---|
| Python | 3.11 or newer | All builds and checks |
| `make` | any | Every command below |
| Node.js | 22.17 or newer | Only `make check-visual` |
| Git | any | Cloning; use a full clone (see below) |

No global Python packages are required and no global skill install is needed —
the skill is vendored in `.agents/skills/resource-learning-library/`.

## Quickstart

```bash
git clone https://github.com/MikkoWuyin-dev/FieldNotes-HR.git
cd FieldNotes-HR
make bootstrap     # creates .venv/ from requirements.lock
make check         # all fast checks
make check-drift   # prove the 5 shipped outputs reproduce from src/
make check-visual  # optional: 13-viewport Chromium checks
```

`make bootstrap` is a prerequisite of `make check` and `make check-drift`, so
those targets create the virtualenv automatically on a fresh clone. There is no
need to fight PEP 668 with `--break-system-packages`: everything installs into
`.venv/`, which is gitignored.

If the clone is shallow (the original workspace was), recover full history with
`git fetch --unshallow` before relying on `git log`.

## What each target does

| Target | What it does |
|---|---|
| `make bootstrap` | Creates `.venv/` and installs the exact tree in `requirements.lock`. |
| `make build` | Regenerates all five outputs from the Markdown and JSON sources. |
| `make check` | Runs `tools/check.py`: skill hashes, unit tests, both validators, style audit, builder contract, cross-source consistency, doc lint, research freshness. |
| `make check-drift` | Rebuilds everything into a temp directory and proves the committed outputs still match. |
| `make check-visual` | Installs the pinned npm packages in `tools/visual/` and runs the 13-width Chromium harness. |
| `make ci` | `make check` plus `make check-drift` — exactly what CI runs. |
| `make links` | Sweeps all cited URLs. Needs unrestricted network; also runs weekly in CI. |
| `make pin-skill` | Re-records the vendored skill's SHA-256 inventory. Only after an intentional skill upgrade. |
| `make clean` | Removes untracked build/runtime artefacts, keeping `.venv/`. |

`make check` is deliberately fast and dependency-light. `make check-drift`
renders PDF and DOCX, so it needs the full pinned tree. `make check-visual`
needs npm but no system Chromium: the browser binary is bundled inside the
`@sparticuz/chromium` npm tarball and inflated at runtime.

## Repository layout

- `learning-library/src/` — content and design sources. Both
  `recruiter-talent-acquisition-library.md` and `roadmap-app.json` are inputs;
  `fieldnotes-theme.css` is the appearance layer.
- `learning-library/out/` — the five shipped deliverables. Generated, but
  committed because they are the product.
- `learning-library/tools/build_tracker.py` — the content build layer: it calls
  the vendored generator and injects the theme. Keep it here; documented paths
  point at it.
- `tools/` — repo-wide verification: `check.py`, `skill-hashes.sha256`, and the
  `visual/` browser harness.
- `.agents/skills/resource-learning-library/` — the vendored skill, byte-exact
  and **never edited in place**. Its 12 hashes are recorded in
  `tools/skill-hashes.sha256` and verified by `make check`.
- `docs/` — this file and `docs/DESIGN-SPEC.md`.

There are two `tools/` directories for historical reasons. The one under
`learning-library/` builds content; the root one verifies the whole repo.

## Editing content

1. Edit **both** `learning-library/src/recruiter-talent-acquisition-library.md`
   and `learning-library/src/roadmap-app.json`. They are two representations of
   the same 8 stages / 26 cards / 21 URLs; `make check` fails if they diverge.
2. Run `make build`, then `make check`, then `make check-drift`.
3. PDF and DOCX embed creation timestamps, so their bytes change on every
   build. `make check-drift` compares PDF by extracted text and DOCX by archive
   entries, which is what actually matters. Commit the regenerated binaries.

## Editing appearance

See `docs/DESIGN-SPEC.md`. In short: change
`learning-library/src/fieldnotes-theme.css`, run `make build` (never hand-edit
`out/roadmap-app.html`), then `make check-visual`. The builder's eight HTML
anchors are checked by `make check`; if the vendored generator ever changes,
that check fails loudly instead of silently dropping the branding.

## Verification claims

`make check` prints one line per check and a final `RESULT:` summary. CI runs
the same command, so a green check means the same thing locally and on GitHub.
A freshness warning is **not** a failure: it lists URLs whose provider pages
were never confirmed (LinkedIn, Jobberman, Coursera and the paid extras). Run
`.venv/bin/python tools/check.py all --strict` if you want those gaps to be
fatal.

`.github/workflows/link-check.yml` runs the URL sweep weekly with unrestricted
network and uploads a TSV report as an artifact. A status code never proves a
resource is free — read the provider page and update
`learning-library/src/verification-manifest.json` when anything changes.

## Skill discovery (standing workflow)

`.mcp.json` registers the `skill-issue` MCP catalogue at project scope, and
`.claude/settings.json` pre-approves it for clones. For each task, search that
catalogue for relevant skills and say which were used. The generating sandbox
could not reach the endpoint (allowlisted egress), so earlier work fetched the
same skill sources from the GitHub API instead. If the server is unreachable,
say so plainly and fall back to the vendored skill here — never claim a skill
was used when it was not. The skill's own `INSTALL.md` describes generic agent
locations such as `~/.claude/skills/`; for this repository the authoritative
copy is the vendored one.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `ModuleNotFoundError: No module named 'docx'` | Dependencies were installed globally or not at all. Run `make bootstrap`; use `make check`, not bare `python3`. |
| `branding anchor not found: …` | The vendored generator's HTML changed. Update `learning-library/tools/build_tracker.py` anchors deliberately, then `make check`. |
| `CHANGED: …` in the skill-hashes check | A vendored file was edited. Restore it, or upgrade the skill intentionally and run `make pin-skill`. |
| `libnspr4.so: cannot open shared object file` | The visual harness handles this itself; if you launch Chromium manually, inflate the AL2023 libs first. |
| `make check-drift` says a binary drifted | A source changed without `make build`, or the dependency tree changed. Check `requirements.lock`. |
