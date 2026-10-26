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
2. The vendored skill stays byte-exact. All appearance changes live in
   `learning-library/src/fieldnotes-theme.css`; the only other build-layer
   edits are HTML branding anchors in
   `learning-library/tools/build_tracker.py`.
3. Never hand-edit `out/roadmap-app.html`. `make build` must reproduce it.

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
| `h1` | `clamp(2.982rem, 8.694vw, 7.644rem)` — 122.304px at 1440px |
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
- At least five distinct tag fills; 26 resource links each with a ↗
  pseudo-element; 8 stages.
- Link and Done on one row, link left of Done, no 2D rectangle overlap.
- All four chips and both progress cards inside the hero; the two progress
  cards never overlap.
- Buttons and stage summaries ≥44px tall; heading outline `h1`×1, `h3`×26;
  skip link present.
- Ticking a card → `1 of 26` / `4%` and a localStorage write; export and
  notification buttons do not throw; reset → `0 of 26`.
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
3. **The 122px h1 wraps to five lines at 1440px**, making the hero roughly
   880px tall. It does not clip or overflow, but it pushes the roadmap far down
   the page. This is the most likely future design change and is currently
   **open** — see `RETROSPECTIVE.md`, issue 3.7.
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

## 7. Making a change

1. Edit `learning-library/src/fieldnotes-theme.css` (or, rarely, the anchors in
   `learning-library/tools/build_tracker.py`).
2. `make build` → `make check` → `make check-drift` → `make check-visual`.
3. Update this document if a token or acceptance criterion changed, and add a
   line to `CHANGELOG.md`. Do not append another dated "refinements" section
   to `learning-library/DESIGN-SYSTEM.md`.
