# Your recruiter learning library

Built on **26 October 2026** with the `resource-learning-library` skill, for an absolute beginner in **Lagos, Nigeria** who wants to break into HR through the **Recruiter / Talent Acquisition** path.

You chose: free-first (paid extras listed separately), a balanced blend of video series, official documentation and written courses, a brand-new custom roadmap, and every output format. I assumed about **5 hours a week** and beginner level. If your hours or level change, only the calendar changes - the order of the stages should stay.

## What is here

| File | What it is |
|---|---|
| `out/Recruiter-TA-Library.pdf` | The full library, 15 pages. Best for printing or sharing. |
| `out/Recruiter-TA-Library.docx` | Editable Word version of the same document. |
| `out/Recruiter-TA-Library.html` | Self-contained static web page. No scripts, no external assets. |
| `out/roadmap-app.html` | Single-file interactive tracker: 8 stages, checkboxes, progress, daily streak, export/import. **Styled with the Fieldnotes design system.** Open it in a browser. |
| `src/recruiter-talent-acquisition-library.md` | The editable Markdown source. This is the file to change if you want a revision. |
| `src/roadmap-app.json` | The structured roadmap and resource data behind the tracker. |
| `src/fieldnotes-theme.css` | The ported Fieldnotes design tokens and component overrides. |
| `tools/build_tracker.py` | Builds the themed tracker from the JSON while leaving the vendored skill untouched. |
| `DESIGN-SYSTEM.md` | Provenance, token table, selector mapping, constraints and verification of the port. |
| `out/Recruiter-TA-Library.md` | A byte-identical copy of the source, kept with the other outputs. |
| `check-links.sh` | A repeatable HTTP status check for all 30 cited URLs. **Not run here** - see below. |

The skill that produced everything here is vendored at **`.agents/skills/resource-learning-library/`** in the repository root, so it is version-controlled and persists across sessions. See `.agents/skills/README.md` for provenance and setup.

## Design system

The interactive tracker was restyled on **26 October 2026** with the design system from `MikkoWuyin-dev/Field-Notes_Nature-Photography`: dark navy frame, warm cream paper, bright blue/cyan/pink/yellow accents, monospace chrome, thick borders, hard offset shadows and square corners. The source uses only system fonts and CSS-generated decoration, so the whole look ported into a self-contained file with no external assets.

The theme lives in `src/fieldnotes-theme.css` and is applied by `tools/build_tracker.py` as a second inline style block; the vendored skill's generator is imported but never modified. See `DESIGN-SYSTEM.md` for the full token table and what could not be copied (a tab icon and social preview tags, which the validator forbids). The PDF, DOCX, Markdown and static HTML library are unchanged.

Four refinements were made afterwards: the coloured bars above the hero were removed so the hero fills the top; the footer reads **"Made with love and fried plantain, by Moyinoluwa"** (the three coloured squares above it stay); the hero eyebrow now renders dark ink on yellow rather than the generator's pale blue-white; and each resource card has a foot row with the link at bottom-left and the Done checkbox at bottom-right. These were checked in headless Chromium 153 at 320-1920px. The `web-design-guidelines` skill from the `skill-issue` MCP collection was applied to focus states, tap targets, tabular numerals and form-control semantics.

## The shape of the plan

**8 stages, 26 resource cards, 21 distinct resource URLs, about 94 hours of study - roughly 20 weeks at 5 hours a week.** The source document is 6,829 words.

**24 cards were confirmed free** from provider pages. **2 cards are paid or conditional** and are labelled that way on the card. The paid section of the document discusses a further five paid options, with naira figures from CIPM and clearly marked third-party figures for LinkedIn.

The stages run: orientation -> foundations and fairness -> defining the role -> sourcing -> screening -> structured interviewing -> offers and Nigerian law -> tools, metrics and getting hired. The single most valuable stage is number 6, on structured interviewing. Google's guide there was updated in March 2026 and is free.

Three free credentials are available along the way, and it is worth knowing exactly what they are. Saylor issues a **free course completion certificate** at 70 percent on the final exam. OpenLearn issues a **free statement of participation**. Alison lets you study free and download a **free Learner Record**, while its branded certificate costs extra. None of these is a professional HR qualification. CIPM is the chartered route in Nigeria, and it is paid.

## Honest limits on the research

I read provider course pages, syllabuses, FAQs and policy pages with a page-retrieval tool on 26 October 2026. Search results were treated as leads only. The full verification log, the drop list with reasons, and the per-card verification notes are in the library document itself.

Things I **could not** do:

- **Run the HTTP status-code sweeps.** The sandbox blocks most outbound traffic. A request to `pypi.org` returned 200, while `kaggle.com` and `docs.python.org` failed at the TLS handshake. `check-links.sh` runs those checks on your machine instead; it was not run here, so no status codes are claimed.
- **Create accounts or complete enrolment.** I cannot describe what any provider shows after sign-in. Free claims rest on public provider statements.
- **Read LinkedIn's own help pages.** Both returned HTTP 500. Their prices come from third-party 2026 pricing guides and are labelled unconfirmed.
- **Read past the Jobberman cookie banner.** That card is marked partially verified.
- **Read every individual Google re:Work guide, or the full text of both legal PDFs.** I read the guides index and two guides directly, and the arrangements of articles plus opening provisions of the NDPC directive and the Labour Act. Neither legal document is legal advice.

Coursera's course is the one to be careful with. Its page shows an "Enroll for free" button, but the same page's FAQ says full access needs a paid Certificate experience, a free trial, or a "Full Course, No Certificate" option where available. I could not confirm that the no-certificate option is offered for this course, so it is **not counted as free**.

Provider terms change. Re-check any paid item and any free-certificate claim before you spend time or money.

## Checks actually run on the finished files

| Check | Result |
|---|---|
| `validate_build.py` on PDF, DOCX, static HTML | All 3 passed. PDF header valid, 15 pages. DOCX: 17 XML parts, 43 headings, 2 tables, 26 hyperlink elements, 21 external hyperlink relationships, no Markdown residue. Static HTML: no external assets, no scripts. |
| `validate_build.py --interactive-html` on the tracker | Passed after the redesign. Two inline style blocks (generator + theme), one inline script, no external scripts, no external assets, no CSS asset references. |
| `style_audit.py` on the Markdown source | 0 mechanical errors, 0 prose-pattern flags. |
| `python3 -m unittest discover -s tests -v` | 5 tests, all OK. |
| Re-reading the built files, not just the builder's exit code | DOCX `word/document.xml` contains the expected stage, price and date text plus theme fills `0B3D5C` and `F6FAFD`. PDF has 42,785 characters of extractable text. Static HTML has 26 clickable resource links. Tracker contains all 8 stages, localStorage, streak dates and the permission request. |
| Headless Chromium 153 on the redesigned tracker | Computed colours match the ported tokens; no console or page errors; **zero horizontal overflow at 320/390/430/600/620/700/900/1024/1440/1920 px**; ticking a card updates the counter, percent, stage meter and localStorage; export and reminder buttons do not throw; reset returns to zero; headings `h1`×1 / `h2`×2 / `h3`×26; all tested controls ≥44px tall. After the four refinements: eyebrow `rgb(17,20,43)` on yellow, hero starts at y=0, top bar pseudo-element has `content:none`, footer credit exact, and link/Done sit on one row bottom-left/bottom-right with no overlap at every width. |

The `url()` strings you may spot in the tracker are JavaScript identifiers (`new URL`, `createObjectURL`, `safeUrl`), not CSS asset references. There are no `fetch`, `XMLHttpRequest`, WebSocket, external script tags, images or `@import` calls in that file.

## About the tracker

Progress lives in **this browser's local storage**. The streak uses the device's local calendar. Reminders are checked **only while the app page is open** - it cannot notify you in the background, does not sync between devices, and has no backend or push service. Browser notifications need a supported browser, your permission and a secure context such as HTTPS or localhost; if they are unavailable or denied, in-app check-ins still work. Use the export button now and then to keep a manual backup.

## If you want a revision

The Markdown source and the JSON are the two files to edit for content; `src/fieldnotes-theme.css` is the file to edit for appearance. Run these from the `learning-library/` directory. `SKILL` points at the vendored copy in the repo, so no global skill install is needed:

```bash
SKILL=../.agents/skills/resource-learning-library
python3 "$SKILL/scripts/docx_render.py" src/recruiter-talent-acquisition-library.md \
  -o out --name Recruiter-TA-Library \
  --title "From zero to first recruiter role" \
  --subtitle "A roadmap-ordered learning library for an absolute beginner" \
  --hero-meta "Lagos, Nigeria - verified 26 October 2026 - about 94 hours over 20 weeks" \
  --format pdf docx md html
python3 tools/build_tracker.py
python3 "$SKILL/scripts/validate_build.py" out/Recruiter-TA-Library.pdf out/Recruiter-TA-Library.docx out/Recruiter-TA-Library.html
python3 "$SKILL/scripts/validate_build.py" --interactive-html out/roadmap-app.html
python3 "$SKILL/scripts/style_audit.py" src/recruiter-talent-acquisition-library.md
```

**Do not** run `scripts/interactive_app.py` directly on `src/roadmap-app.json` to build the delivered tracker - that produces the old unthemed look. `tools/build_tracker.py` calls that same generator internally and then layers the theme, so the vendored skill stays byte-exact.

The skill is now vendored in this repository at `.agents/skills/resource-learning-library/`, so it is committed and survives session resets. Its 12 files were reconstructed from the transfer bundle and hash-verified against the bundle's SHA-256 inventory. Python dependencies are not vendored: on a fresh machine run `python3 -m pip install -r ../.agents/skills/resource-learning-library/requirements.txt` (use a venv or `--break-system-packages` on PEP 668 systems) before the commands above. A personal copy may also exist at `$HOME/.agents/skills/resource-learning-library/` for agents that scan a global skills root; treat the repo copy as authoritative.

## Your first hour

Open the HR Learning Lab channel, watch the first three Talent Acquisition lessons, and draw the hiring lifecycle on one sheet of paper. Then open the Stage 1 Saylor course, create your free account, and tick the first item in the tracker.
