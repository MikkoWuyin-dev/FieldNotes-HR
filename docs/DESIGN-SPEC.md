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
   only. No `<link>`, `<img>`, `<iframe>`, external scripts, `@import`, web
   fonts or CSS `url(...)` references. Enforced by `make check`.
2. The vendored skill stays byte-exact. Core appearance changes live in
   `learning-library/src/fieldnotes-theme.css`; the optional decorative pals
   live in `learning-library/src/pals/`. The only build-layer edits are HTML
   anchors in `learning-library/tools/build_tracker.py`.
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
| `--fn-pink` | `#FF4E91` | Hard offset shadow |
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

## 3. Structure and composition

- **Hero** fills the top of the sheet with no coloured bar above it. 4px cyan
  border, bottom-only pink `0 10px 0` offset shadow, zero border radius. The
  small side gutter is cancelled so it runs cyan-edge to cyan-edge; this is
  **not** a full `100vw` breakout.
- **Eyebrow** reads `FIELDNOTES / HR` in dark ink (`rgb(17,20,43)`) on yellow
  (`rgb(255,225,104)`). This overrides the generator's pale eyebrow colour.
- **Footer** text is exactly: `Made with love and fried plantain, by
  Moyinoluwa`. The three coloured squares above it stay.
- **Stage headers** use `align-items:baseline` so the number badge, `0%`
  counter and `+`/`−` toggle sit on the title's first line (measured delta
  ~2.3px, down from ~10.3px).
- **Stage intro** has equal 14px top and bottom margins. Outcomes use a filled
  9×9px square marker centred on the first text line.
- **Resource cards** pin the link bottom-left and the Done checkbox
  bottom-right on one card-foot row. Every resource link carries a decorative
  ↗ via `::after` with CSS alt text, so screen readers do not announce it;
  print styles replace it with the full URL.
- **Tags:** every tag gets its own colour, not a default fill. The cycle gives
  cyan / pink / green / orange / lavender; `.tag.cost` stays green (free) and
  `.tag.paid` stays yellow.
- **Toolbar:** the visible "Reminder time" label is removed. The native
  `for`/`id` association is preserved with a visually-hidden label, and the
  input carries `name`, `autocomplete="off"`, `aria-label="Reminder time"` and
  `title="Reminder time"`.

## 4. Type scale and rhythm

| Element | Value |
|---|---|
| `h1` | `clamp(2.2365rem, 6.5205vw, 5.733rem)` — 91.728px at 1440px |
| Subtitle | `clamp(.75rem, 1.5vw, .9525rem)` — 15.24px desktop, 12px mobile |
| Fact chips | 9.12px font, `4.5px 6.75px` padding |
| Progress cards | min-width 105.6px, `7.2px 10.8px` padding, number 1.86rem, label `.864rem` |
| Hero gaps | eyebrow→h1 5px, h1→subtitle 10px, subtitle→chips 12px, chips→cards 12px on mobile |

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
- At least five distinct tag fills; 27 resource links each with a ↗
  pseudo-element; 8 stages.
- Link and Done on one row, link left of Done, no 2D rectangle overlap.
- All four chips and both progress cards inside the hero; the two progress
  cards never overlap.
- Buttons and stage summaries ≥44px tall; heading outline `h1`×1, `h3`×27;
  skip link present.
- Ticking a card → `1 of 27` / `4%` and a localStorage write; export and
  notification buttons do not throw; reset → `0 of 27`.
- No console or page errors.

## 6. Known, deliberate deviations

These are documented rather than silently "fixed", because each was an
explicit user decision or an unresolved trade-off.

1. **Fact chips are 9.12px**, below the 12px readability floor in the
   `ui-ux-pro-max` skill. They are short uppercase metadata chips, not body
   copy. Raising them to a 12px floor is a one-line change if legibility wins
   over the compact look.
2. **The visible "Reminder time" label is hidden**, conflicting with the
   visible-label rule in the same skill. Mitigated with a screen-reader label,
   `aria-label` and `title`. Restoring a visible label is also a one-line
   change.
3. **Hero scale reduced 25% after mobile feedback.** Now 35.784px on narrow
   screens and capped at 91.728px. Verify wrapping on a real phone too.
4. **A tab icon and social preview tags were not ported.** The skill's
   validator forbids `<link>` elements and any CSS `url(...)`, including data
   URIs. All decoration is CSS gradients, borders, shadows and
   pseudo-elements.
5. **Headless Chromium is not a real phone.** Touch momentum, browser chrome
   and device-specific storage behaviour were not tested.

Skills consulted for the port: `web-design-guidelines`,
`design-system-patterns`, `accessibility-compliance`, `taste-skill` and
`ui-ux-pro-max` from the `skill-issue` catalogue. Deviations 1 and 2 above are
where their advice was consciously overridden.

## 7. Decorative pals

Ten optional pixel creatures were ported from the reference project's
**Piixpal v0.4.0** engine (MIT, https://github.com/diiviikk5/Piixpal). They are
decoration only: the tracker is fully usable with them paused.

- **Source of truth:** `learning-library/src/pals/pals.json` — 10 entries, each
  `{pal, target, at, hue?, scale?, edge?}`. `PALS_COUNT` in the controller is
  derived from that array, never hard-coded. The build layer injects the array
  into `learning-library/src/pals/pals-controller.js`.
- **Sprites:** all eight available (`bitbug`, `lurk`, `moss`, `pip`, `capy`,
  `bumble`, `shel`, `frog`) appear once; `moss` and `bumble` each repeat with a
  hue rotation (320° and 205°) so no two identical creatures sit together.
- **Placement:** spread down the whole page against **visible prose** targets —
  hero title and subtitle, both dashboard panels, stage headings for stages 1,
  3, 5 and 7, and the footer. A pal's canvas has `pointer-events:auto`, so pals
  are never anchored to a button, link, input or `<summary>`.
- **Engine:** the core plus eight sprite scripts are vendored byte-exact as an
  inert `<template>` in `learning-library/src/pals/piixpal-payload.html` (9
  inline scripts, ~83 KB). The controller clones them into the document on
  `requestIdleCallback`, so content renders first. The layer is
  a full-body `position:absolute` layer, clipped only at the complete document
  boundary. This avoids frame-delayed scroll corrections on mobile. Never
  clip a zero-size or viewport-height layer: that hides lower-page pals. A `MutationObserver` re-anchors pals when the
  generator rebuilds the stage list on reset/import.
- **Control:** a "Pause tiny pals" toggle with an `aria-live` status line sits
  between the caveat notice and the roadmap. Preference is stored under
  `fieldnotes-hr-pals-v1`. Pals are **off by default** under
  `prefers-reduced-motion: reduce`; a visitor can still opt in explicitly.
- **Styling:** `learning-library/src/pals/pals.css` (document-positioned layer, control
  panel, print and reduced-motion rules). No CSS `url()` references.

### Pals acceptance criteria

`make check` verifies the static invariants; `make check-visual` verifies the
rendered behaviour:

- Exactly 10 pals, all 8 sprites used, every repeat hue-rotated, 10 unique
  prose targets, no target that is a control.
- Payload SHA-256 matches the pin; MIT headers, licence text and
  `THIRD-PARTY-NOTICES.md` present; payload has no external script, image,
  link, CSS `url()`, `fetch`, XHR, WebSocket or `javascript:` URL.
- Tracker contains exactly one pals style block, payload template, control
  panel, toggle and controller script.
- At all 13 widths, both with the stage list expanded **and** in the default
  collapsed state: no horizontal overflow, **zero** control-centre hits, and no
  pal overlapping a control by more than **1100px²** (the reference project's
  rule).
- Pausing removes all `piix-pal` elements and sets `aria-pressed="false"`;
  enabling restores 10. Under `prefers-reduced-motion: reduce`, **zero** pals
  are created.
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
There are 27 cards and 25 free cards. The total remains 94 hours: HR Essentials
uses a one-hour starter budget within Stage 1's existing eight hours, not an
additional full-course requirement. Playlist runtimes/playback are not verified.

The build layer preserves the old Stage 1 checkbox keys: the new card uses
`hr-essentials-v1`; existing cards keep `s0-r0`, `s0-r1`, `s0-r2`. Storage ID
and import/export format stay unchanged, so existing progress needs no migration.
Browser regression checks restore a legacy saved-state fixture and verify the
correct cards are checked. The skill and Piixpal payload remain byte-exact.

The scroll regression compares document positioning against the old fixed layer
in the same JS task, before an animation frame can compensate for scrolling.
Physical iOS/Android momentum scrolling and YouTube app handoff remain untested.
