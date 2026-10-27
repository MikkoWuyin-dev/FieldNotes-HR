# Your recruiter learning library

> **Setup and verification:** `docs/SETUP.md` is canonical. Run `make bootstrap`
> then `make check`; CI runs the same checks. The current design contract is
> `docs/DESIGN-SPEC.md`; `learning-library/DESIGN-SYSTEM.md` is the historical
> port record and `CHANGELOG.md` the change history.

Built on **26 October 2026** with the `resource-learning-library` skill, for an absolute beginner in **Lagos, Nigeria** who wants to break into HR through the **Recruiter / Talent Acquisition** path.

You chose: free-first (paid extras listed separately), a balanced blend of video series, official documentation and written courses, a brand-new custom roadmap, and every output format. I assumed about **5 hours a week** and beginner level. If your hours or level change, only the calendar changes - the order of the stages should stay.

## What is here

| File | What it is |
|---|---|
| `out/Recruiter-TA-Library.pdf` | The full library, 15 pages. Best for printing or sharing. |
| `out/Recruiter-TA-Library.docx` | Editable Word version of the same document. |
| `out/Recruiter-TA-Library.html` | Self-contained static web page. No scripts, no external assets. |
| `out/roadmap-app.html` | Single-file interactive tracker: 8 stages, checkboxes, progress, daily streak, export/import. **Styled with the Fieldnotes design system and decorated with 10 optional pixel pals.** Open it in a browser. |
| `src/recruiter-talent-acquisition-library.md` | The editable Markdown source. This is the file to change if you want a revision. |
| `src/roadmap-app.json` | The structured roadmap and resource data behind the tracker. |
| `src/fieldnotes-theme.css` | The ported Fieldnotes design tokens and component overrides. |
| `src/pals/` | The 10 decorative pals: `src/pals/pals.json` (placements), `src/pals/pals-controller.js`, `src/pals/pals.css`, the vendored MIT-licensed Piixpal engine and its licence. |
| `tools/build_tracker.py` | Builds the themed tracker from the JSON while leaving the vendored skill untouched, then injects the pals. |
| `DESIGN-SYSTEM.md` | Provenance, token table, selector mapping, constraints and verification of the port. |
| `out/Recruiter-TA-Library.md` | A byte-identical copy of the source, kept with the other outputs. |
| `src/verification-manifest.json` | Per-URL verification status and date for all 30 checked URLs, plus the first CI link-sweep record; read by `make check`. |
| `check-links.sh` | A repeatable HTTP status check for all 30 cited URLs. It could not run in the generating sandbox; it now runs weekly in CI and was first dispatched on 27 October 2026. |
| `../tools/check.py` | The single verification runner behind `make check` and `make check-drift`. |
| `../tools/visual/` | The committed 13-viewport Chromium harness behind `make check-visual`. |

The skill that produced everything here is vendored at **`.agents/skills/resource-learning-library/`** in the repository root, so it is version-controlled and persists across sessions. See `.agents/skills/README.md` for provenance and setup.

## Design system

The interactive tracker was restyled on **26 October 2026** with the design system from `MikkoWuyin-dev/Field-Notes_Nature-Photography`: dark navy frame, warm cream paper, bright blue/cyan/pink/yellow accents, monospace chrome, thick borders, hard offset shadows and square corners. The source uses only system fonts and CSS-generated decoration, so the whole look ported into a self-contained file with no external assets.

The theme lives in `src/fieldnotes-theme.css` and is applied by `tools/build_tracker.py` as a second inline style block; the vendored skill's generator is imported but never modified. See `DESIGN-SYSTEM.md` for the full token table and what could not be copied (a tab icon and social preview tags, which the validator forbids). The PDF, DOCX, Markdown and static HTML library are unchanged.

Four rounds of refinements followed the initial port: hero/footer/eyebrow/card-foot changes, coloured tags and stage markers, a rebalanced hero type scale, and finally a larger h1 with baseline-aligned stage headers and tighter spacing. Each round is recorded in `CHANGELOG.md` and in the historical `DESIGN-SYSTEM.md`. **The current values live in `docs/DESIGN-SPEC.md`** — read that rather than the chronological log, because later rounds replace earlier ones (the 40% h1 increase was requested twice and applied once).

All changes live in `src/fieldnotes-theme.css` (plus one input-attribute edit in `tools/build_tracker.py`). They are now checked reproducibly in Chromium 153 at 13 widths from 320 to 1920px by `make check-visual`, not by a throwaway script.

The `web-design-guidelines`, `design-system-patterns` and `accessibility-compliance` skills from the `skill-issue` MCP collection were applied to focus states, tap targets, tabular numerals, form-control semantics, component tokens and WCAG AA contrast.

## The ten decorative pals

The tracker now carries **10 optional animated pixel creatures** ported from the
reference project's Piixpal v0.4.0 engine. They are MIT-licensed; the full
notice is in `THIRD-PARTY-NOTICES.md` and the licence text in
`src/pals/LICENSE-MIT.txt`.

All eight sprites (`bitbug`, `lurk`, `moss`, `pip`, `capy`, `bumble`, `shel`,
`frog`) appear once, with `moss` and `bumble` repeating under hue rotations.
They are spread from the hero to the footer against **visible prose** targets —
never a button or link, because a pal's canvas would swallow the tap. The
engine is an inert `<template>` loaded on idle, so it never blocks the roadmap;
there is a **Pause tiny pals** toggle with a live status line, and pals are off
by default for visitors who prefer reduced motion.

Placement is edited in `src/pals/pals.json`. Current-state rules and acceptance
criteria are in `docs/DESIGN-SPEC.md` §7. The engine adds about 92 KB, taking
the self-contained tracker from ~72 KB to ~165 KB. Pals do not appear in the
PDF, DOCX, Markdown or static HTML.

## The shape of the plan

**8 stages, 26 resource cards, 21 distinct resource URLs, about 94 hours of study - roughly 20 weeks at 5 hours a week.** The source document is 6,829 words.

**24 cards were confirmed free** from provider pages. **2 cards are paid or conditional** and are labelled that way on the card. The paid section of the document discusses a further five paid options, with naira figures from CIPM and clearly marked third-party figures for LinkedIn.

The stages run: orientation -> foundations and fairness -> defining the role -> sourcing -> screening -> structured interviewing -> offers and Nigerian law -> tools, metrics and getting hired. The single most valuable stage is number 6, on structured interviewing. Google's guide there was updated in March 2026 and is free.

Three free credentials are available along the way, and it is worth knowing exactly what they are. Saylor issues a **free course completion certificate** at 70 percent on the final exam. OpenLearn issues a **free statement of participation**. Alison lets you study free and download a **free Learner Record**, while its branded certificate costs extra. None of these is a professional HR qualification. CIPM is the chartered route in Nigeria, and it is paid.

## Honest limits on the research

I read provider course pages, syllabuses, FAQs and policy pages with a page-retrieval tool on 26 October 2026. Search results were treated as leads only. The full verification log, the drop list with reasons, and the per-card verification notes are in the library document itself.

Things I **could not** do:

- **Run the HTTP status-code sweeps in the generating environment.** The sandbox blocks most outbound traffic: a request to `pypi.org` returned 200, while `kaggle.com` and `docs.python.org` failed at the TLS handshake. The original sweep was therefore **not run there and no status codes are claimed from it**. `.github/workflows/link-check.yml` runs `check-links.sh` weekly with unrestricted network; `make links` runs the same sweep locally.
  **First result (manual dispatch, 27 October 2026, run `40471064309`):** 30 URLs checked — **27 × 200, 3 × 403**. The three 403s (OpenLearn course, NDPC GAID PDF, Saylor FAQ) were all **bot filtering**: each page was re-read via a browser-like fetch and its free claim still holds. LinkedIn's pages returned 200 to curl but 403/500 to a browser, so they remain unverified. A status code still never proves a resource is free; the record is in `src/verification-manifest.json`.
- **Create accounts or complete enrolment.** I cannot describe what any provider shows after sign-in. Free claims rest on public provider statements.
- **Read LinkedIn's own help pages.** Both returned HTTP 500. Their prices come from third-party 2026 pricing guides and are labelled unconfirmed.
- **Read past the Jobberman cookie banner.** That card is marked partially verified.
- **Read every individual Google re:Work guide, or the full text of both legal PDFs.** I read the guides index and two guides directly, and the arrangements of articles plus opening provisions of the NDPC directive and the Labour Act. Neither legal document is legal advice.

Coursera's course is the one to be careful with. Its page shows an "Enroll for free" button, but the same page's FAQ says full access needs a paid Certificate experience, a free trial, or a "Full Course, No Certificate" option where available. I could not confirm that the no-certificate option is offered for this course, so it is **not counted as free**.

Provider terms change. Re-check any paid item and any free-certificate claim before you spend time or money.

## Checks actually run on the finished files

Every row below is now reproducible: `make check` runs the validators, unit tests, style audit, builder contract, source consistency and doc lint; `make check-drift` proves all five outputs rebuild from source; `make check-visual` runs the browser checks. CI runs all three.

| Check | Result |
|---|---|
| `make check` / `make check-drift` (27 October 2026) | Passed. Vendored skill 12/12 SHA-256 hashes exact; 8 branding anchors each fail loudly when broken; 8 stages / 26 cards / 94 h / 21 URLs agree across JSON, Markdown, tracker and manifest; all five outputs reproduce (PDF by extracted text, DOCX by archive entries). |
| `make check-visual` (27 October 2026, after the pals) | Headless Chromium 153: 13/13 widths passed plus 3 collapsed-state checks; 10 pals mounted on a fixed layer, **zero control-centre hits and zero control overlap**, pause removes all 10, reduced motion creates none; no console or page errors; tick → `1 of 26` / `4%` / localStorage, reset → `0 of 26`. Harness committed in `tools/visual/`. |
| `make check` (after the pals) | 8 passed, 1 known freshness warning, 0 failed. New `pals` check verifies 10 placements, all 8 sprites, hue-rotated repeats, prose-only targets, pinned payload SHA-256, MIT notice and tracker markers. |
| `validate_build.py` on PDF, DOCX, static HTML | All 3 passed. PDF header valid, 15 pages. DOCX: 17 XML parts, 43 headings, 2 tables, 26 hyperlink elements, 21 external hyperlink relationships, no Markdown residue. Static HTML: no external assets, no scripts. |
| `validate_build.py --interactive-html` on the tracker | Passed after the redesign. Two inline style blocks (generator + theme), one inline script, no external scripts, no external assets, no CSS asset references. |
| `style_audit.py` on the Markdown source | 0 mechanical errors, 0 prose-pattern flags. |
| `python3 -m unittest discover -s tests -v` | 5 tests, all OK. |
| Re-reading the built files, not just the builder's exit code | DOCX `word/document.xml` contains the expected stage, price and date text plus theme fills `0B3D5C` and `F6FAFD`. PDF has 42,785 characters of extractable text. Static HTML has 26 clickable resource links. Tracker contains all 8 stages, localStorage, streak dates and the permission request. |
| Headless Chromium 153 on the redesigned tracker | Computed colours match the ported tokens; no console or page errors; **zero horizontal overflow at 320/360/390/430/600/620/700/900/1024/1200/1320/1440/1920 px**; ticking a card updates the counter, percent, stage meter and localStorage; export and reminder buttons do not throw; reset returns to zero; headings `h1`×1 / `h2`×2 / `h3`×26; all tested controls ≥44px tall. After the refinements: eyebrow `rgb(17,20,43)` on yellow, hero starts at y=0, top bar pseudo-element has `content:none`, footer credit exact, link/Done on one row with no overlap at every width, all four chips plus both progress cards stay inside the hero with no 2D overlap, the 122px h1 never clips, and stage-header badge/counter sit within ~2.3px of the title's first baseline. |

The `url()` strings you may spot in the tracker are JavaScript identifiers (`new URL`, `createObjectURL`, `safeUrl`), not CSS asset references. There are no `fetch`, `XMLHttpRequest`, WebSocket, external script tags, images or `@import` calls in that file.

## About the tracker

Progress lives in **this browser's local storage**. The streak uses the device's local calendar. Reminders are checked **only while the app page is open** - it cannot notify you in the background, does not sync between devices, and has no backend or push service. Browser notifications need a supported browser, your permission and a secure context such as HTTPS or localhost; if they are unavailable or denied, in-app check-ins still work. Use the export button now and then to keep a manual backup.

## If you want a revision

The Markdown source and the JSON are the two files to edit for content; `src/fieldnotes-theme.css` is the file to edit for appearance. Run everything **from the repository root** — `docs/SETUP.md` is the canonical guide:

```bash
make bootstrap     # .venv/ from the pinned requirements.lock
make build         # regenerate all 5 outputs
make check         # validators, tests, contract, consistency, doc lint
make check-drift   # prove committed outputs reproduce
make check-visual  # if appearance changed
```

**Do not** run `scripts/interactive_app.py` directly on `src/roadmap-app.json` to build the delivered tracker - that produces the old unthemed look. `tools/build_tracker.py` calls that same generator internally and then layers the theme, so the vendored skill stays byte-exact.

The skill is vendored at `.agents/skills/resource-learning-library/`, so it is committed and survives session resets. Its 12 SHA-256 hashes are recorded in `tools/skill-hashes.sha256` and checked by `make check`; never edit those files in place. Python dependencies are not vendored, but `make bootstrap` installs the exact tree from `requirements.lock` into `.venv/` - no global install, no PEP 668 workaround. A personal copy may also exist at `$HOME/.agents/skills/resource-learning-library/` for agents that scan a global skills root; treat the repo copy as authoritative.

## Your first hour

Open the HR Learning Lab channel, watch the first three Talent Acquisition lessons, and draw the hiring lifecycle on one sheet of paper. Then open the Stage 1 Saylor course, create your free account, and tick the first item in the tracker.
