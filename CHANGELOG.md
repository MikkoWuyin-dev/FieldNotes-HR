# Changelog

All notable changes to this repository. Dates are in the user's local timezone
(Africa/Lagos). Verification claims below were actually run; see
`docs/SETUP.md` for how to reproduce them.

## 27 October 2026 — reproducibility and CI (current branch)

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
  tick/reset works, no console or page errors.
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
