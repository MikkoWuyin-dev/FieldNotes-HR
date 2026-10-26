# Retrospective — FieldNotes-HR

**Written:** 27 October 2026, on branch `arena/bd812372-fieldnotes-hr`.
**Scope:** the work that produced the recruiter learning library, the Fieldnotes
design-system port, PR #1 and PR #2 (merged as `fd7c568`).

This is an engineering retrospective, not a review of the learning content. Its
purpose is to name the friction that repeatedly slowed the work down, so that the
next change to this repository does not pay the same tax again.

---

## 1. Summary

The repository is small — 28 tracked files, roughly 594 KB — but it absorbed a
disproportionate amount of process overhead. The delivered artifact is healthy:
the interactive tracker rebuilds **byte-for-byte** from source, the
self-containment validator passes, and there are no external assets or network
calls in the shipped HTML.

Almost all of the lost time went into four activities that had nothing to do with
the product:

1. Re-establishing the working environment at the start of every session.
2. Re-running verification by hand because it was not encoded in the repository.
3. Working around an outbound-network allowlist that blocked research,
   link checking and the MCP skill catalogue.
4. Chasing small design changes through a build layer and an append-only
   documentation trail, each time re-verifying at 13 viewport widths.

The unifying cause: **verification and environment setup were things an agent
did, not things the repository enforced.** The fixes in this repository turn
them into commands and CI jobs.

---

## 2. Evidence gathered

Read-only diagnosis run against the merged `main` state. Commands were re-run,
not recalled.

| Check | Result |
|---|---|
| Rebuild `out/roadmap-app.html` from source in a temp directory | **Pass** — bit-exact, 72,721 bytes, SHA-256 `85113a35…` |
| `validate_build.py --interactive-html` | **Pass** — `external_assets=none`, `inline_scripts=1` |
| `python3 -m unittest discover -s tests -v` | **5 run, 1 ERROR** — `ModuleNotFoundError: No module named 'docx'`. Environmental, not a code regression: dependencies were absent from the fresh session. |
| Headless Chromium tooling | **Absent** — `/tmp/chromium` gone |
| `curl https://openstax.org/` | `000` — OpenSSL `SSL_ERROR_SYSCALL` |
| `gh workflow list` | **empty** — no CI |
| Root `.gitignore` | **absent** — `node_modules`, `__pycache__`, `.DS_Store`, `link-status.tsv` all unignored |
| Local git history | shallow (`grafted`); required `git fetch --unshallow` |

Additional measurements: 21 URLs duplicated between `src/roadmap-app.json` and
`src/recruiter-talent-acquisition-library.md`; `out/Recruiter-TA-Library.md` is a
byte-identical copy of its source; the verification date appears 153 times across
9 files; `tools/build_tracker.py` depends on 8 exact-string regex anchors plus a
`</head>` anchor; `src/fieldnotes-theme.css` overrides about 30 generator class
names across 459 lines.

**Caveat on evidence.** Some findings — repeated dependency reinstalls, the four
design rounds, the branch-pointer desync — come from session history that is not
recorded in git. The environment fragility is independently confirmed by the
missing `python-docx` and vanished Chromium in the diagnosis session itself.
Everything about structure, duplication counts, stale docs and missing CI was
verified against the files.

---

## 3. Recurring issues

### 3.1 Environment amnesia — chronic, highest cost

Python dependencies, npm browser tooling, the global skill copy and, on one
occasion, the built HTML itself were repeatedly lost between sessions. Each
recovery required reinstalling with `--break-system-packages`, re-extracting a
Chromium build, and re-running every validator. The local clone was shallow, and
at one point the local branch pointer was behind its remote counterpart,
requiring `git reset --mixed FETCH_HEAD` to avoid a non-fast-forward push.

**Root cause:** no hermetic bootstrap. Nothing in the repository reconstructs a
working environment; tooling lived outside the repo in `/home/user/browser-check`
and `/tmp/chromium`.

**Cost:** 10–20 minutes at the start of every session, plus a standing risk of
reporting "all checks passed" against an environment that did not produce the
files under test.

### 3.2 Verification was a manual ritual, not a repo asset — chronic

No CI workflow, no Makefile, no `pyproject.toml`, no lock file. The README
documents five separate commands for a rebuild. The "13 viewport widths" checks
were driven by scripts that were never committed and no longer exist. The only
tests in the repo are the vendored skill's five unit tests, which test the skill
— not `build_tracker.py`, the theme, or the branding anchors. PR #2 had zero
checks.

**Cost:** a reviewer could not reproduce any of the verification claims; every
small change required a full manual re-run; a regression in the theme layer
would be invisible until somebody opened the HTML.

### 3.3 Outbound-network wall — chronic

`check-links.sh` still carried the header "NOT RUN in the generating sandbox".
The `skill-issue` MCP endpoint was registered in `.mcp.json` but its POST tools
were unreachable, so skill guidance had to be fetched from the allowlisted
GitHub API instead. Research caveats remain permanent: LinkedIn help pages
returned HTTP 500 (prices from third-party guides, unconfirmed), Jobberman
showed only a cookie banner, and Coursera's free access could not be confirmed.

**Cost:** no HTTP status codes could ever be claimed; free/paid claims could not
be re-checked; the "verified 26 October 2026" stamp had no expiry or re-check
mechanism.

### 3.4 Brittle extension of a frozen generator — structural

The requirement that the vendored skill remain byte-exact is correct, but it
forced the design system into a post-processing layer. `tools/build_tracker.py`
rewrites generated HTML using eight exact-string regex anchors tied to the
generator's internal markup. `src/fieldnotes-theme.css` overrides roughly 30
generator class names. The README must warn readers not to run the underlying
generator directly.

**Cost:** any change to the vendored generator breaks the build with
`branding anchor not found`, or silently orphans a style override. Two styling
systems coexist in one output file.

### 3.5 Multiple sources of truth and committed generated artifacts — chronic

The Markdown source and the JSON data both contain the same 21 URLs, 8 stages
and 26 cards. Five generated outputs are committed, including binary PDF and
DOCX whose diffs are unreviewable. The Markdown output is a byte-identical
duplicate of its source. Nothing detected drift if only one output was
regenerated.

**Cost:** a content edit needs two source edits plus five regenerations; binary
diffs are unreviewable; drift is silent.

### 3.6 Append-only documentation drift — episodic, recurring

`DESIGN-SYSTEM.md` §2 still claimed that only the provider chip and cost chip
carry accent colours, long after the CSS was changed to colour every tag. The
document has four separately dated "refinements" sections — a changelog
standing in for a current-state spec. Setup instructions are spread across five
files and disagree: the skill's `INSTALL.md` installs to `~/.claude/skills/`
while the repo uses `.agents/skills/`; its plain `pip install` lacks the PEP 668
caveat that the other docs carry; build commands are given from two different
working directories.

**Cost:** readers cannot tell what is current; each design round meant editing
several docs; onboarding requires reconciling five files.

### 3.7 Design-by-screenshot churn — episodic, likely to recur

Four sequential refinement rounds, each requiring a full rebuild plus a
13-viewport sweep plus documentation updates. Requirements arrived as
pixel-level deltas rather than a token sheet with acceptance criteria. Known
debt remains: the 122 px h1 wraps to five lines, making the hero about 880 px
tall; the 9.12 px fact chips sit below the 12 px readability guideline; the
hidden "Reminder time" label conflicts with the UI-guidelines skill.

**Cost:** a high verification multiplier for each tiny visual change, with
ambiguous specifications causing rework.

### 3.8 Repo hygiene and configuration — latent

No root `.gitignore`; loose dependency ranges (`>=1.1,<2` and similar) with no
lock; `.claude/settings.local.json` committed even though "settings.local" is by
convention a per-developer file; the MCP config unusable in the sandbox with no
automated fallback; three different session branches used across the project.

---

## 4. What is *not* broken

The build is deterministic and bit-exact; the self-containment assertions work;
the validator passes on the interactive tracker; the vendored skill is intact;
there are no external assets, fonts or network calls in the shipped HTML; the
merge into `main` was clean; and the documented 13-width overflow checks passed
when they were actually run.

**The product is fine. The workflow around it was expensive.**

---

## 5. Remediation plan, in implementation order

| # | Fix | Addresses |
|---|---|---|
| 0 | Repo hygiene: `.gitignore`, `.gitattributes`, pinned `requirements.lock`, MCP settings moved to project scope, PR template | 3.8 |
| 1 | `make bootstrap` + `make check`: one pinned virtualenv, one command that runs every validator | 3.1, 3.2 |
| 2 | GitHub Actions CI running `make check`, plus a scheduled link-check workflow | 3.2, 3.3 |
| 3 | Builder contract test + recorded generator hash: anchors cannot silently rot | 3.4 |
| 4 | `make check-drift` + cross-source consistency check | 3.5 |
| 5 | `verified_at` manifest + freshness check so research staleness is visible | 3.3 |
| 6 | `docs/DESIGN-SPEC.md` (current state), `CHANGELOG.md` (history), canonical `docs/SETUP.md`, doc lint | 3.6, 3.7 |
| 7 | Committed visual-check harness with an optional browser install target | 3.7 |

Dependencies between the fixes meant they were implemented in a slightly
different order; §6 records what actually landed, with its own numbering.

---

## 6. Implementation log — what actually landed

Implemented on 27 October 2026 on branch `arena/bd812372-fieldnotes-hr`. No
tracker appearance or library content changed: `out/roadmap-app.html` is still
byte-identical at SHA-256
`85113a35c675824aaa5c63b09d0450eaafdb77c33b103657a625d26a45fa4a6`.

| # | Fix delivered | Addresses |
|---|---|---|
| 0 | Root `.gitignore`, `.gitattributes`, `requirements.lock` (full frozen tree), `.claude/settings.json` replacing the per-developer `settings.local.json`, PR template | 3.8 |
| 1 | `Makefile` with `make bootstrap`, `build`, `check`, `check-drift`, `check-visual`, `ci`, `links`, `pin-skill`, `clean`; one pinned `.venv/` | 3.1, 3.2 |
| 2 | `tools/check.py` single runner: 9 checks, per-check `[ OK ]`/`[WARN]`/`[FAIL]` lines and a `RESULT:` summary | 3.2 |
| 3 | `.github/workflows/verify.yml` (checks + drift + visual) and `.github/workflows/link-check.yml` (weekly URL sweep with real network) | 3.2, 3.3 |
| 4 | `branding_edits()` refactor in `learning-library/tools/build_tracker.py` plus a contract check that breaks each of the 8 anchors, the `</head>` anchor and the self-containment guard | 3.4 |
| 5 | `tools/skill-hashes.sha256` — the 12-file SHA-256 inventory is now in the repo and machine-checked, with `make pin-skill` for intentional upgrades | 3.4 |
| 6 | `make check-drift`: rebuilds all 5 outputs and compares the tracker and static MD/HTML byte-for-byte, the PDF by extracted text and the DOCX by archive entries | 3.5 |
| 7 | Cross-source consistency check (URLs, stage titles, card and hour counts across JSON / Markdown / tracker / manifest) and `src/verification-manifest.json` with a freshness check | 3.3, 3.5 |
| 8 | `docs/SETUP.md` (canonical), `docs/DESIGN-SPEC.md` (current state), `CHANGELOG.md` (history), doc lint for stale claims / broken paths / phantom `make` targets, and corrections to the four older docs | 3.6, 3.7 |
| 9 | `tools/visual/` — committed 13-viewport Chromium 153 harness with a pinned npm lock file, replacing scratch scripts outside the repo | 3.7 |

### Verification actually run

- `make check` — **7 passed, 1 warned, 0 failed.** The warning is the intended
  one: 8 URLs have open verification gaps (Coursera, Jobberman, LinkedIn and
  the paid extras). Nothing is hidden behind a green tick.
- `make check-drift` — **all 5 outputs reproduce.** Investigation showed PDF
  bytes change only because of embedded creation timestamps, and the committed
  DOCX differs from a fresh render only in ZIP metadata: every archive entry is
  byte-identical. The drift check therefore compares semantics, not timestamps.
- `make check-visual` — **13/13 widths passed** in Chromium 153, no console or
  page errors; tick → `1 of 26` / `4%` / localStorage, reset → `0 of 26`.
  Report written to `tools/visual/.cache/last-run.json` (gitignored).
- `make build` output remains bit-exact; the 12 vendored skill files remain
  byte-exact against the committed inventory.

### What this does **not** fix

- **CI verification is now confirmed.** The `verify` workflow ran on both the
  push (`40421681523`) and the pull request (`40421748294`); in each run both
  `build + verify` and `13-viewport browser checks` passed in GitHub Actions.
  The local results above are therefore reproducible on a clean runner. The
  scheduled `link-check` workflow only fires weekly or on manual dispatch, so
  **its results are still unobserved** and no HTTP status codes are claimed.
- **The URL sweep still has not been run from this sandbox.** `curl` here still
  returns `000` with an SSL error. GitHub Actions can now run it weekly and
  publishes a TSV report as an artifact. A status code never proves a resource
  is free — a human still has to read the provider page.
- **The `skill-issue` MCP endpoint is still unreachable from this sandbox.**
  The registration is durable and documented, but skill discovery here still
  relies on the allowlisted GitHub API fallback.
- **Research claims still expire.** `verification-manifest.json` makes staleness
  visible after 90 days, but nothing automatically re-reads provider pages and
  rewrites free/paid claims. That still needs a human.
- **Design debt is documented, not resolved.** The 122px five-line h1, the
  9.12px chips and the hidden visible label are recorded as deliberate
  deviations in `docs/DESIGN-SPEC.md` §6. The h1 is flagged as the most likely
  future change.
- **Headless Chromium is still not a real phone.** Touch momentum, browser
  chrome and device-specific storage behaviour remain untested.
- **The two content sources were not merged.** They are now checked for
  disagreement rather than generated from one another — a pragmatic safety net,
  not full single-sourcing. Generating one from the other would add a third
  format and risk the byte-exact deliverables; it remains an open option.
