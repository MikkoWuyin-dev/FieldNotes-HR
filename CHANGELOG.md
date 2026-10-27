# Changelog

All notable changes to this repository. Dates are in the user's local timezone
(Africa/Lagos). Verification claims below were actually run; see
`docs/SETUP.md` for how to reproduce them.

## 27 October 2026 — mobile hero, playlists and scroll alignment

- Reduced the hero h1 clamp by 25% (35.784px mobile / 91.728px max).
- Added HR Essentials first in Stage 1; replaced the TA channel link with the
  supplied direct playlist. Removed sharing parameters. Read public playlist
  descriptions and lesson listings; playback/app handoff not tested.
- 27 cards / 25 free; preserved the 94-hour budget using selected starter lessons.
- Preserved all existing checkbox keys, localStorage ID and backup compatibility.
- Switched Pals from fixed positioning to a full-document absolute layer so
  scrolling does not depend on animation-frame correction. Engine unchanged.
- Added browser regressions for native scroll alignment and old progress; updated
  card expectations, historical sweep snapshot and regenerated all outputs.
- Real-phone momentum scrolling and YouTube app handoff remain to be tested.
- Investigated non-clickable embedded preview links: all 27 links pass actual
  hit-testing at 13 widths; trusted mouse/touch events reach both playlists,
  and an unsuppressed click requests the correct new-tab URL. Added these
  regressions. Embedded Arena preview restrictions remain unverified; no
  application navigation changes were made based on an unconfirmed cause.

## 27 October 2026 — static Vercel deployment configuration

- Added root `vercel.json`: publish only `learning-library/out`, rewrite `/`
  to the tracker, and skip install/build commands for committed static assets.
- Added `docs/DEPLOYMENT.md` with import settings, localStorage migration,
  reminder limitations and a production smoke-test checklist; linked from README.
- Added two stdlib deployment contract tests and wired them into verify CI.
- No live deployment or Vercel account settings were changed.

## 27 October 2026 — first link sweep results (current branch)

The weekly URL sweep ran for the first time. It was triggered manually from the
GitHub Actions UI (run `40471064309`, `workflow_dispatch` on `main`); the
sandbox's GitHub App token lacks `actions: write`, so `gh workflow run` returns
403 here. All seven job steps passed.

- **Result: 30 URLs — 27 × 200, 3 × 403.** The three non-2xx URLs were the
  OpenLearn course page, the NDPC GAID PDF and the Saylor general FAQ.
- All three 403s were **bot filtering**, not dead links. Each provider page was
  re-read with a browser-like fetch on 27 October 2026: OpenLearn still says
  "Free course" / "Free statement of participation"; Saylor still says no
  tuition or fees and free completion certificates; the NDPC PDF is intact.
  Their `verified_at` dates were advanced to 2026-10-27.
- LinkedIn's two pages returned 200 to curl but 403 (`/learning/`) and 500
  (Recruiter help) to a browser-like recheck, so both remain `unreachable`.
- Added a `link_sweep` block to
  `learning-library/src/verification-manifest.json` recording the run, counts,
  non-2xx findings and the caveat that a 200 does not prove free access. Added
  a `sweep` check to `tools/check.py` that keeps this record consistent with
  `check-links.sh` and the 30 manifest URLs.
- Updated `learning-library/src/recruiter-talent-acquisition-library.md` so the
  library no longer says the sweep was never performed, and rebuilt all five
  outputs. Updated `learning-library/README.md`, `docs/SETUP.md`,
  `RETROSPECTIVE.md` and the workflow/script header comments.
- Not claimed: the raw `link-status.tsv` artifact (its Azure Blob redirect is
  outside this sandbox's egress allowlist). The 27 × 200 figure comes from the
  job summary's counts plus its complete non-2xx list. A status code never
  proves a resource is free.

## 27 October 2026 — ten decorative pals

Added the reference project's animated pixel creatures to the interactive
tracker only. No library content changed; PDF, DOCX, Markdown and static HTML
are untouched.

- Vendored the MIT-licensed **Piixpal v0.4.0** engine (core + 8 sprite scripts)
  byte-exactly as an inert `<template>` at
  `learning-library/src/pals/piixpal-payload.html`. Added the full licence text
  and `THIRD-PARTY-NOTICES.md`; pinned the payload SHA-256.
- Added `learning-library/src/pals/pals.json` (10 placements against visible
  prose), `learning-library/src/pals/pals-controller.js` (idle load, pause,
  reduced motion, re-anchoring) and `learning-library/src/pals/pals.css`
  (fixed unclipped layer, control panel, print rules).
- `learning-library/tools/build_tracker.py` now injects the pals as three more
  anchors, separate from the eight Fieldnotes branding anchors. Both sets are
  covered by the contract check.
- All 8 sprites used once; `moss` and `bumble` repeat with hue rotations.
- Tracker grows from 72,721 to 164,554 bytes. Still a single self-contained
  file: 11 inline scripts, no external assets, no network calls.
- `make check` gained a `pals` check; `make check-visual` now waits for the
  10 pals and asserts count, fixed layer, zero control-centre hits, ≤1100px²
  overlap, pause, and reduced motion — at 13 widths plus the default
  collapsed state.
- Added `make preview` and `tools/serve_preview.py`. A sandbox reset had wiped
  the previous preview script (it lived in the gitignored, snapshot-excluded
  `tools/visual/.cache/`) and silently restored the committed no-Pals tracker,
  because `learning-library/out/` is snapshot-excluded too. `make preview` now
  rebuilds the tracker from source before serving on `0.0.0.0:8000`, warns if
  the Pals payload is absent, and needs only stdlib Python — no `.venv` or
  `node_modules`. Documented in `docs/SETUP.md`.

Verified: `make check` 8 passed / 1 known freshness warning / 0 failed;
`make check-drift` passed; `make check-visual` 13/13 widths plus 3 collapsed
checks passed, no console errors. Skills consulted from the `skill-issue`
catalogue: `web-design-guidelines`, `accessibility-compliance`,
`frontend-design`, `taste-skill`, `ui-ux-pro-max-skill`, `responsive-design`.

Known limitation: the pals pause preference is stored separately from the
tracker's export/import JSON, because the vendored generator cannot be modified.

## 27 October 2026 — reproducibility and CI

Fixes the recurring friction documented in `RETROSPECTIVE.md`. No content or
appearance change: `out/roadmap-app.html` remains byte-identical at SHA-256
`85113a35c675824aaa5c63b09d0450eaafdb77c33b103657a625d26a45fa4a6c`.

- Added `RETROSPECTIVE.md` with the diagnosis of eight recurring issues.
- Added root `.gitignore` (venv, node_modules, caches, OS files, generated
  reports), `.gitattributes` (binary PDF/DOCX), and a PR template.
- Replaced the loose dependency ranges with a fully frozen
  `requirements.lock`; added `make bootstrap` creating `.venv/`, and `make
  check` / `make check-drift` / `make check-visual` / `make build` / `make
  links` / `make pin-skill` / `make clean`.
- Added `tools/check.py`: one runner for skill hashes, unit tests, both
  validators, style audit, the builder's eight-anchor contract, cross-source
  consistency, doc lint, research freshness and full output reproduction.
- Committed the vendored skill's SHA-256 inventory as
  `tools/skill-hashes.sha256`, so "byte-exact" is machine-checkable.
- Refactored `learning-library/tools/build_tracker.py` to expose
  `branding_edits()` without changing a single byte of generated output, and
  added a contract test that breaks each anchor in turn.
- Added `learning-library/src/verification-manifest.json` recording the
  status and date of all 30 checked URLs, plus a freshness check.
- Added CI: `.github/workflows/verify.yml` (checks, drift, visual) and
  `.github/workflows/link-check.yml` (weekly URL sweep with unrestricted
  network). `learning-library/check-links.sh` now runs in CI.
- Added a reproducible 13-viewport Chromium harness in `tools/visual/` with a
  committed lock file. Verified locally: 13/13 widths pass, functional
  tick/reset works, no console or page errors. Both `verify` CI jobs
  (`build + verify` and `13-viewport browser checks`) subsequently passed on
  the push and pull-request runs; the weekly `link-check` sweep has not yet
  fired.
- Added `docs/SETUP.md` (canonical setup) and `docs/DESIGN-SPEC.md` (current
  design contract with measurable acceptance criteria).
- Corrected the stale tag-colour claim in
  `learning-library/DESIGN-SYSTEM.md` and marked its four refinement sections
  as historical.
- Moved the MCP approval from the per-developer
  `.claude/settings.local.json` to project-scoped `.claude/settings.json`.

## 26 October 2026 — design system port and refinements (PR #2, merged `fd7c568`)

Ported the design system from
`MikkoWuyin-dev/Field-Notes_Nature-Photography` into the interactive tracker
without modifying the vendored skill.

- Initial port: Fieldnotes tokens, thick borders, hard offset shadows, square
  corners, CSS-only decoration, print rules. Hero bar removal, footer credit,
  dark-ink eyebrow, and card-foot link/Done placement.
- Second round: every tag given its own colour; stage intro margins
  equalised; outcomes square marker; ↗ on all 26 links; hero edge-to-edge
  with a larger h1.
- Third round: subtitle and fact chips scaled down 25%; progress cards scaled
  up 20%; shared chip/card rule split.
- Fourth round: h1 grown 40% (applied once), stage headers switched to
  baseline alignment, visible "Reminder time" label hidden behind an
  accessible name, hero gaps tightened.
- Registered the `skill-issue` MCP at project scope in `.mcp.json` and
  documented per-task skill discovery.
- Verified in headless Chromium 153 at 13 widths: no overflow, no clipping, no
  overlap, no console errors; validators, style audit and 5 unit tests passed;
  vendored skill 12/12 hashes exact.

## 26 October 2026 — initial library (PR #1, merged `6b33fb5`)

- Produced a researched, roadmap-ordered HR / Recruiter / Talent Acquisition
  learning library: 8 stages, 26 resource cards, 21 distinct URLs, 94
  estimated hours (~20 weeks at 5 h/week), 6,829-word Markdown source.
- Output formats: PDF (15 pages), DOCX, Markdown, static HTML and a
  self-contained interactive tracker.
- 24 cards confirmed free from provider pages; 2 paid or conditional; paid
  extras documented separately with the free-to-study / free-certificate /
  professional-qualification distinction preserved.
- Vendored the 12-file `resource-learning-library` skill into the repository
  so it survives session resets.
- Added `learning-library/check-links.sh` for the 30 cited URLs. It was
  **not run** in the generating sandbox because outbound traffic was
  allowlisted; that limitation is now addressed by CI.

## Known research limitations (unchanged)

LinkedIn help pages returned HTTP 500, so its prices come from third-party
2026 guides and are unconfirmed. Jobberman showed only a cookie banner and is
marked partially verified. Coursera's no-certificate free access could not be
confirmed, so that course is not counted as free. No accounts were created and
no enrolment was completed. These gaps are recorded per URL in
`learning-library/src/verification-manifest.json` and surfaced by `make check`.
