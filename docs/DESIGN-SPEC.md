# Fieldnotes tracker — current design contract

**Status:** current as of 27 October 2026. This document describes **what the
tracker is now**, with measurable acceptance criteria. It replaces the four
dated "refinements" sections in `learning-library/DESIGN-SYSTEM.md`, which
remain as a historical record of the port. `CHANGELOG.md` holds the change
history. Setup and verification are in `docs/SETUP.md`.

The visual source of truth is `MikkoWuyin-dev/Field-Notes_Nature-Photography`.
Tokens were copied from that repository's `:root` block on 26 October 2026.

---

## 1. Non-negotiable constraints

1. `out/roadmap-app.html` is **one self-contained file**: inline CSS and JS
   only. The sole link-tag exception is the exact pinned inline SVG favicon
   described below; no other link tags are allowed. No `<img>`, `<iframe>`,
   external scripts, `@import`, web
   fonts or CSS `url(...)` references. Enforced by `make check`.
2. The vendored skill stays byte-exact. Core appearance changes live in
   `learning-library/src/fieldnotes-theme.css`; local behavior lives in
   `learning-library/src/theme-toggle.js` and
   `learning-library/src/scroll-to-top.js`; decorative pals live in
   `learning-library/src/pals/`. The build layer injects these sources at
   validated anchors in `learning-library/tools/build_tracker.py`.
3. Never hand-edit `out/roadmap-app.html`. `make build` must reproduce it.
4. The pals engine is a vendored **MIT-licensed** third-party payload. It is
   never edited in place; its SHA-256 is pinned in
   `learning-library/src/pals/pals.json` and checked by `make check`. See
   `THIRD-PARTY-NOTICES.md`.

## 2. Primitive tokens

| Token | Value | Use |
|---|---|---|
| `--fn-ink` | `#11142B` | Text, page frame |
| `--fn-paper` | `#FFF8E7` | Warm sheet behind content |
| `--fn-cream` | `#FFFDF6` | Card surfaces |
| `--fn-line` | `#1E2553` | Borders and rules |
| `--fn-muted` | `#565C73` | Secondary text |
| `--fn-blue` | `#3768FF` | Hero fill, focus ring |
| `--fn-blue-ink` | `#2C55DA` | Link and accent text |
| `--fn-cyan` | `#65E8FF` | Hero border | 
| `--fn-pink` | `#FF4E91` | Decorative accent blocks |
| `--fn-shadow` | `#E63E7A` light / `#FF4E91` dark | Offset shadows; ≥3:1 against measured neighboring surfaces |
| `--fn-yellow` | `#FFE168` | Eyebrow, paid tags |
| `--fn-green` | `#5EE780` | Free tags |
| `--fn-orange` | `#FF9958` | Duration tags |
| `--fn-tag-default/playful/pixel/action/mobile` | cyan / `#FFC3DE` / yellow / green / `#DCD0FF` | Tag palette |
| `--fn-mono` / `--fn-prose` | system mono / system sans | Chrome / prose |

Component tokens `--fn-tag-cycle-1` … `--fn-tag-cycle-5` map the tag palette to
positions in `.resource-meta`. All six tag fills pass WCAG AA against
`--fn-ink` (measured range 8.59:1 to 14.00:1).

The generator's own variables (`--navy`, `--blue`, `--border`, `--pale`, …) are
aliased to these tokens in `:root`, so its existing `var()` rules inherit the
Fieldnotes palette; remaining hard-coded colours are overridden explicitly.

The light tokens are the default. `:root[data-theme="dark"]` remaps semantic
surface, text, border, control and status tokens while keeping the Fieldnotes
accent colours. `learning-library/src/theme-toggle.js` reads the system
`prefers-color-scheme` before first paint, follows system changes until the
visitor chooses a theme, and saves that override under
`fieldnotes-hr-theme-v1`. This appearance preference is separate from roadmap
progress and is not part of progress backups.

## 3. Structure and composition

- **Hero** fills the top of the sheet with no coloured bar above it. 4px cyan
  border, bottom-only `0 10px 0 var(--fn-shadow)` offset shadow, zero border
  radius. The small side gutter is cancelled so it runs cyan-edge to cyan-edge;
  this is **not** a full `100vw` breakout. The circular sun/moon toggle is
  anchored to the hero's far-right content edge and top-aligned with the eyebrow
  on desktop; on mobile it remains aligned with the full-width eyebrow row. The
  row is top-aligned 20–28px below the hero's outside edge, with no leftover
  top lane from the toggle's former position. The visible circle matches the
  eyebrow's computed height (~26px); a transparent 44×44 pointer target keeps
  it practical to tap. Its yellow surface keeps dark ink in both modes, and its
  accessible name and `aria-pressed` expose the toggle state.
- **Eyebrow** reads `FIELDNOTES / HR` in dark ink (`rgb(17,20,43)`) on yellow
  (`rgb(255,225,104)`). This overrides the generator's pale eyebrow colour.
- **Footer** text is exactly: `Made with love and fried plantain, by
  Moyinoluwa`. The three coloured squares above it stay.
- **Stage headers** use an explicit four-column grid: number badge and title
  share a top edge; the percentage and one plus/minus indicator share the first
  row and are vertically centered together. The duration sits below the title
  in its own aligned column. The generator's default summary pseudo-icon is
  suppressed so it cannot create a duplicate under the number. The remaining
  1.25rem indicator is larger than the percentage counter. The visual harness
  measures number/title top-edge drift and percentage/icon center drift at all
  13 widths, requiring ≤1.1px for each pair.
- **Stage bodies** omit the introductory description and repeated outcome/
  learning-objective list from tracker accordions; the stage title and duration
  remain in the header. Full stage copy remains in the generated library document.
- **Resource cards** pin the link bottom-left and the Done checkbox
  bottom-right on one card-foot row. Every resource link carries a decorative
  ↗ via `::after` with CSS alt text, so screen readers do not announce it;
  print styles replace it with the full URL.
- **Tags:** every tag gets its own colour, not a default fill. The cycle gives
  cyan / pink / green / orange / lavender; `.tag.cost` stays green (free) and
  `.tag.paid` stays yellow.
- **Toolbar:** browser-reminder controls and copy are removed. Export, import and
  reset retain a polite live status for progress actions. The compact circular
  sun/moon theme toggle sits in the eyebrow row, starts from the system setting,
  and saves a browser-local override. The disabled "Checked in today" button
  uses light ink on the dark surface in dark mode; the active yellow button
  continues to use dark ink.
- **Back to top:** a 48px fixed arrow button sits at the bottom right after the
  visitor scrolls. It hides at the top or after three seconds without scrolling;
  keyboard focus keeps it available, and smooth scrolling respects reduced
  motion.

## 4. Type scale and rhythm

| Element | Value |
|---|---|
| `h1` | `clamp(2.2365rem, 6.5205vw, 5.733rem)` — 91.728px at 1440px |
| Subtitle | `clamp(.75rem, 1.5vw, .9525rem)` — 15.24px desktop, 12px mobile |
| Fact chips | 9.12px font, `4.5px 6.75px` padding |
| Progress cards | min-width 105.6px, `7.2px 10.8px` padding, number 1.86rem, label `.864rem` |
| Hero rhythm | top inset `clamp(16px,2vw,24px)` (eyebrow 20–28px below outer edge); eyebrow→h1 5px, h1→subtitle 10px, subtitle→chips 12px, chips→cards 12px on mobile |

The 40% h1 increase was requested twice and is applied **once**. Any future
size change should be an explicit replacement of the clamp, not another
multiplier on top.

## 5. Acceptance criteria (machine-checked)

`make check-visual` runs these in Chromium 153 at 320, 360, 390, 430, 600,
620, 700, 900, 1024, 1200, 1320, 1440 and 1920 px. `make check` covers the
non-visual invariants.

- Zero horizontal overflow; `h1` never clips (`scrollWidth <= clientWidth`).
- Hero background `rgb(55,104,255)`; eyebrow dark ink on yellow; footer credit
  exact — at every width.
- At least five distinct tag fills; 21 resource links each with a ↗
  pseudo-element; 8 stages.
- Link and Done on one row, link left of Done, no 2D rectangle overlap.
- All four chips and both progress cards inside the hero; the two progress
  cards never overlap.
- Buttons and stage summaries ≥44px tall; heading outline `h1`×1, `h3`×21;
  skip link present. The compact theme icon matches the eyebrow's height and
  alignment while retaining a transparent 44×44 pointer target.
- Ticking a task → `1 of 21` / `4%` and a localStorage write; export/import/reset
  remain usable; no reminder controls, permission prompts or reminder scheduler
  are present; reset → `0 of 21`.
- With no saved theme choice, light/dark follows `prefers-color-scheme` and
  responds to system changes. A manual choice updates `aria-pressed`, persists
  after reload, and remains separate from progress reset and backup data.
- The eyebrow row stays with the hero text column; the circular theme toggle's
  right edge matches the hero's content edge within 1px at every tested width.
  The eyebrow begins 20–28px below the hero's outside top edge, eliminating the
  old reserved lane. The toggle remains in the same row; its visible width and
  height match the eyebrow within 1px, its top edge aligns within 1px, and a
  transparent 44×44 pseudo-element preserves the pointer target. It shows a
  sun in light mode and a moon in dark mode while preserving system defaults
  and saved overrides. The disabled "Checked in today" control has light ink
  on its dark surface. Yellow text stays dark at ≥4.5:1; visible box-shadow
  colors are checked at ≥3:1 in both themes.
- Every stage summary puts its number, title, percentage and exactly one
  disclosure icon in the first grid row with no overlap at all 13 tested widths.
  The number/title top edges and the percentage/icon centers are each within
  1.1px; the duration sits below the title. The default summary pseudo-icon is
  hidden, and the remaining icon is at least 1.5× the percentage counter's font
  size.
- The bottom-right back-to-top button appears after scrolling, returns the page
  to the top, hides at the top or after three idle seconds, and respects reduced
  motion. It is keyboard accessible and at least 44×44px.
- No console or page errors.

## 6. Known, deliberate deviations

These are documented rather than silently "fixed", because each was an
explicit user decision or an unresolved trade-off.

1. **Fact chips are 9.12px**, below the 12px readability floor in the
   `ui-ux-pro-max` skill. They are short uppercase metadata chips, not body
   copy. Raising them to a 12px floor is a one-line change if legibility wins
   over the compact look.
2. **Hero scale reduced 25% after mobile feedback.** Now 35.784px on narrow
   screens and capped at 91.728px. Verify wrapping on a real phone too.
3. **The tab icon now matches Nature Photography.** The exact inline SVG
   favicon is stored in `learning-library/src/favicon-link.html` and injected
   by the builder. One hash-pinned exception permits this data-URI link tag;
   all other link elements remain forbidden. Social preview tags remain unported.
4. **Headless Chromium is not a real phone.** Touch momentum, browser chrome
   and device-specific storage behaviour were not tested.

Skills consulted for the port: `web-design-guidelines`,
`design-system-patterns`, `accessibility-compliance`, `taste-skill` and
`ui-ux-pro-max` from the `skill-issue` catalogue. Deviation 1 above is where
that advice was consciously overridden.

## 7. Decorative pals

Eleven optional decorative Pals are available: ten pixel creatures from the
reference project's **Piixpal v0.4.0** engine (MIT,
https://github.com/diiviikk5/Piixpal) plus one locally authored dangling spider.
They are decoration only: the tracker is fully usable with them paused.

- **Source of truth:** `learning-library/src/pals/pals.json` — 11 entries: ten
  Piixpal placements `{pal, target, at, hue?, scale?, edge?}` plus the spider
  record `{pal, kind, position}`. `PALS_COUNT` is derived from the full array.
  The build layer injects the array into
  `learning-library/src/pals/pals-controller.js`.
- **Sprites:** all eight available Piixpal sprites (`bitbug`, `lurk`, `moss`,
  `pip`, `capy`, `bumble`, `shel`, `frog`) appear among the ten engine pals;
  `moss` and `bumble` repeat with hue rotations (320° and 205°).
- **Placement:** ten Piixpal creatures are spread down the page against
  **visible prose** targets — hero title and subtitle, both dashboard panels,
  stage headings for stages 1, 3, 5 and 7, and the footer. Their canvases have
  `pointer-events:auto`, so none targets a button, link, input or `<summary>`.
  The separate inline spider hangs at the viewport's top-right, is
  `pointer-events:none`, and stays fixed there while the user scrolls.
- **Engine:** the core plus eight sprite scripts are vendored byte-exact as an
  inert `<template>` in `learning-library/src/pals/piixpal-payload.html` (9
  inline scripts, ~83 KB). The controller clones them into the document on
  `requestIdleCallback`, so content renders first. The layer is
  a full-body `position:absolute` layer, clipped only at the complete document
  boundary. This avoids frame-delayed scroll corrections on mobile. Never
  clip a zero-size or viewport-height layer: that hides lower-page pals. A `MutationObserver` re-anchors pals when the
  generator rebuilds the stage list on reset/import.
- **Control:** a "Pause tiny pals" toggle with an `aria-live` status line sits
  between the caveat notice and the roadmap. It controls all 11 Pals, including
  the fixed spider. Preference is stored under `fieldnotes-hr-pals-v1`. Pals
  are **off by default** under `prefers-reduced-motion: reduce`; a visitor can
  still opt in explicitly, with the spider's sway animation disabled.
- **Styling:** `learning-library/src/pals/pals.css` (document-positioned
  Piixpal layer, fixed spider, control panel, print and reduced-motion rules).
  No CSS `url()` references.

### Pals acceptance criteria

`make check` verifies the static invariants; `make check-visual` verifies the
rendered behaviour:

- Exactly 11 total Pals: 10 Piixpal creatures plus one local fixed spider. All
  8 sprites are used, repeated sprites are hue-rotated, and all 10 Piixpal
  placements use unique prose targets rather than controls.
- The spider is visible at the fixed viewport top-right and stays there across
  scrolling at all 13 tested widths. Its layer is pointer-transparent and its
  sway stops under reduced motion.
- Payload SHA-256 matches the pin; MIT headers, licence text and
  `THIRD-PARTY-NOTICES.md` present; payload has no external script, image,
  link, CSS `url()`, `fetch`, XHR, WebSocket or `javascript:` URL.
- Tracker contains exactly one pals style block, payload template, fixed-spider
  element, control panel, toggle and controller script.
- At all 13 widths, both with the stage list expanded **and** in the default
  collapsed state: no horizontal overflow, **zero** control-centre hits, and no
  pal overlapping a control by more than **1100px²** (the reference project's
  rule).
- Pausing removes all 10 `piix-pal` elements, hides the fixed spider and sets
  `aria-pressed="false"`; enabling restores all 11 Pals. Under
  `prefers-reduced-motion: reduce`, none are created/shown by default, and the
  spider sway is disabled even if a visitor explicitly enables decoration.
- No console or page errors.

### Pals limitations

- The pals preference is **not** included in the tracker's export/import JSON:
  the vendored generator cannot be modified, so progress export is unchanged.
- The engine adds ~92 KB: `out/roadmap-app.html` grows from ~72 KB to ~165 KB.
  It is lazy-loaded on idle, so content is not blocked.
- Pals can be poked and dragged (that is the engine's charm), but the
  hit-testing above guarantees they never swallow a tap on a control.

## 8. Making a change

1. Edit `learning-library/src/fieldnotes-theme.css` for core appearance,
   `learning-library/src/theme-toggle.js` for theme behavior,
   `learning-library/src/pals/pals.json` for pal placement, or (rarely) the
   anchors in `learning-library/tools/build_tracker.py`.
2. `make build` → `make check` → `make check-drift` → `make check-visual`.
3. If you changed a pal target, re-check the no-overlap measurements at every
   width before merging.
4. Update this document if a token or acceptance criterion changed, and add a
   line to `CHANGELOG.md`. Do not append another dated "refinements" section
   to this document.

## 9. Playlist and progress compatibility update

Stage 1 now starts with HR Essentials, followed by the direct Talent Acquisition
playlist. Both use canonical YouTube playlist URLs without sharing parameters.
Current totals are generated in the root and library READMEs. HR Essentials
uses a starter budget within the orientation stage, not an additional
full-course requirement. Playlist runtimes/playback are not verified.

Resource and stage keys now use permanent IDs. The unchanged storage namespace
and frozen compatibility ledger migrate original positional keys on load and
on legacy backup import. Version 2 exports include the storage identity. See
`docs/CONTENT-MODEL.md` for conflict, validation and retained-key behavior.
The skill and Piixpal payload remain byte-exact.

## 10. Favicon validation exception

`learning-library/src/favicon-link.html` is copied byte-exactly (apart from its
trailing newline) from the reference project's icon link in `index.html`.
The builder pins the complete tag by SHA-256 and requires exactly one occurrence.
It removes only that tag from a temporary validation copy before the unchanged
vendored HTML validator runs. This is a repository policy exception, not a claim
that the original skill accepts favicon links. The delivered app retains it.

`tools/test_favicon.py` covers SVG contents and rejection of missing, duplicate,
modified, remote or extra link tags. Browser QA decodes the actual inline image, renders it at
32×32 and checks the four colours. Browser tab display/cache behaviour still needs a live-device check.
