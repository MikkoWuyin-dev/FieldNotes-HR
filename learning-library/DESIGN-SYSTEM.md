# Fieldnotes design system (ported)

> **This is the historical port record (26 October 2026).** For the current
> design contract — tokens, type scale, acceptance criteria and known
> deviations — see `docs/DESIGN-SPEC.md`. Setup and verification are in
> `docs/SETUP.md`. The four "refinements" sections below are a chronological
> log, not a description of the final state; `CHANGELOG.md` summarises them.
> The ten decorative pixel pals were added later and are **not** documented
> here; see `docs/DESIGN-SPEC.md` §7 and `THIRD-PARTY-NOTICES.md`.

The interactive roadmap tracker in this repo uses the visual design system from
**`MikkoWuyin-dev/Field-Notes_Nature-Photography`**, a single-file nature
photography learning app. Extracted on **2026-10-26** from its `index.html`
(`:root` token block, component CSS, hero decoration), `README.md`,
`AUDIT-PLAIN.md` and `assets/og-image.png`.

The design language is deliberately portable: the source uses **only system font
stacks and CSS-generated decoration**. There are no web fonts, no image assets in
the page, and no runtime network requests. Nothing had to be substituted.

## 1. Primitive tokens

These are copied verbatim from the source `:root`:

| Token | Value | Role |
|---|---|---|
| `--fn-ink` | `#11142B` | Dark navy: page frame, text, borders |
| `--fn-paper` | `#FFF8E7` | Warm cream page background |
| `--fn-cream` | `#FFFDF6` | Card and panel surface |
| `--fn-line` | `#1E2553` | Structural border colour |
| `--fn-muted` | `#565C73` | Secondary text |
| `--fn-shade` | `#D8D9EA` | Soft lavender accent |
| `--fn-blue` | `#3768FF` | Hero background, primary fills |
| `--fn-blue-ink` | `#2C55DA` | Links, small labels |
| `--fn-cyan` | `#65E8FF` | Frame rule, hero border, accent |
| `--fn-pink` | `#FF4E91` | Hard offset shadow, stage numbers |
| `--fn-yellow` | `#FFE168` | Eyebrow chip, primary buttons |
| `--fn-green` | `#5EE780` | Free / success accent |
| `--fn-orange` | `#FF9958` | Warm accent |
| `--fn-tag-default` / `playful` / `pixel` / `action` / `mobile` | `#65E8FF` / `#FFC3DE` / `#FFE168` / `#5EE780` / `#DCD0FF` | Tag fills |
| `--fn-status-live-*` | `#E9FFEF` / `#164D2D` | Completed state |
| `--fn-status-caveat-*` | `#FFF1BD` / `#6E4A00` | Notice panel |
| `--fn-stack-gap` | `52px` | One vertical rhythm for every stacked section |
| `--fn-mono` | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` | Chrome, labels, metadata |
| `--fn-prose` | `system-ui, sans-serif` | Body copy |

Dark-navy frame + warm paper, thick 3-4px borders, hard offset shadows
(`6px 6px 0 var(--fn-line)`, `10px 10px 0 var(--fn-pink)`), and **zero border
radius** are the defining moves. Focus is a 3px blue outline at 3px offset.

## 2. How it was applied

`src/fieldnotes-theme.css` holds the tokens and all component overrides.
`tools/build_tracker.py` calls the **vendored, unmodified** skill generator
`interactive_app.build_app()` to produce the functional single-file app, then
injects the theme as a **second inline `<style>` block** plus a few head/hero
branding edits (title, theme colour, eyebrow, hero fact chips, skip link).

This keeps `.agents/skills/resource-learning-library/` byte-exact against its
SHA-256 inventory while making a rebuild reproduce the new look:

```bash
# from the repository root
python3 learning-library/tools/build_tracker.py
```

The generator's own CSS variables (`--navy`, `--blue`, `--border`, …) are aliased
to the Fieldnotes tokens in `:root`, so its rules that already use `var()` pick up
the new palette automatically; the remaining hard-coded colours are overridden
explicitly.

### Selector mapping

| Source component | Target class in this app |
|---|---|
| `.hero`, `.hero-eyebrow`, `.hero-meta span`, `.hero::after` | `.hero`, `.eyebrow`, `.hero-facts span` / `.hero-stat`, `.hero::after` |
| `.panel`, `.progress-track`, `.progress-fill` | `.panel`, same names |
| `.button`, `.filter-button`, `.search` | `.toolbar button`, `.file-button`, `input[type=time]` |
| `.tag`, `.tag.i`, `.tag.px` | `.tag`, `.tag.cost`, `.tag.paid` |
| `.stage`, `.stage-summary`, `.number`, `.stage-chevron` | `.stage`, `.stage summary`, `.stage-num`, `summary::after` |
| `.resource-card`, `.done-control`, `.outcomes li` | `.resource`, `.completion`, `.outcomes li` |
| `.card-foot` (link left, Done right) | `.resource a` + `.completion`, pinned into a reserved bottom band |
| `.tour-invite` (caveat styling) | `.notice` |
| `.app-footer::before` decoration | three coloured squares (echoes the source's 3x3 accent grid) |

**Adaptation (final state):** the generator emits five metadata chips per
resource (provider, modality, cost, time, verification date). An early version
of this port gave only the first chip and the cost chip accent colours, leaving
the long metadata chips quiet cream. **That was changed in the second
refinement:** every tag now receives its own coloured fill through the
`--fn-tag-cycle-*` component tokens (cyan, pink, green, orange, lavender),
while `.tag.cost` stays green for free and `.tag.paid` stays yellow. All six
fills pass WCAG AA against `--fn-ink`. See `docs/DESIGN-SPEC.md` §2–3.

### Requested refinements (2026-10-26) — historical

The four dated subsections below record each round in the order it happened;
later rounds override earlier ones (for example the 1.15× h1 was subsequently
replaced by a 1.4× clamp, not multiplied again). For the resulting values read
`docs/DESIGN-SPEC.md`.

Four changes were made after the first port. All live in `src/fieldnotes-theme.css`
or `tools/build_tracker.py`, so a rebuild reproduces them.

1. **Top bars removed.** The `.app::before` strip (cyan rule + three coloured
   bars) was deleted and `.app` top padding set to zero, so the hero now starts
   at the very top of the sheet and fills the space. The three coloured squares
   above the footer were kept.
2. **Footer credit.** `build_tracker.py` replaces the generator's footer line
   with `Made with love and fried plantain, by Moyinoluwa`.
3. **Eyebrow contrast.** The generator ships `.hero p{color:#DCEAF1}`, whose
   specificity (0,1,1) beat the theme's plain `.eyebrow` rule (0,1,0) and made
   `FIELDNOTES / HR` render pale blue-white on yellow. A `.hero .eyebrow` rule
   (0,2,0) now forces the dark `--fn-ink` colour. This was verified by computed
   style, not just by reading the CSS.
4. **Card foot.** The generator nests the resource link inside an unclassed div
   and puts the completion label beside it. Without editing the vendored
   generator, `.resource` reserves a 56px bottom band and both the link and the
   Done control are absolutely pinned into it — link bottom-left, Done
   bottom-right, on the same row. Cards stretched to equal height in the 2-up
   grid therefore keep their foot rows aligned. Print styles return both to
   normal flow.

**Skill used:** `web-design-guidelines` from the `skill-issue` MCP collection.
Its live rule set was applied where it fits a static single-file app:
`:focus-within` on the compound checkbox label, `font-variant-numeric:
tabular-nums` on compared numbers, `text-wrap: balance` on short headings,
`touch-action: manipulation` and an intentional tap highlight, `min-width:0` on
flex children, and `name` / `autocomplete="off"` on the two inputs. Rules that
need a framework, routing, images, virtualisation or a server do not apply here.
The generator's `window.confirm` on Reset already satisfies the destructive-
action rule, and `prefers-reduced-motion` was already handled.

### Second refinements (2026-10-26)

Five more adjustments, again made only in `src/fieldnotes-theme.css` so the
vendored generator stays byte-exact.

1. **Every tag has a colour.** The source design gives each tag a bright fill
   (`--tag-default` cyan plus `.p`/`.px`/`.i`/`.m` modifiers); this port had
   reset the base tag to cream, leaving three of five chips on the card
   background. A five-colour component-token cycle now colours every chip:
   cyan → pink → green → orange → lavender, with `.tag.cost` (green) and
   `.tag.paid` (yellow) overriding position 3 semantically. Position 4 uses
   `--fn-orange` instead of green/yellow so all five chips stay visually
   distinct. Verified as 5 distinct computed background colours.
2. **Stage intro margins.** `.stage-description` was `margin:0 0 14px`; the top
   is now 14px to match the bottom.
3. **Outcomes markers.** The `/` glyph is replaced by a 9×9px filled ink
   square, centred on the first text line via `top:calc(8px + .7em)` plus
   `translateY(-50%)`. Computed top and bottom padding were already equal at
   8px, so the perceived imbalance came from the slash being pinned at
   `top:8px` while multi-line items wrapped; centring the marker fixes it.
4. **External-link arrow.** Each of the 26 resource links gets a small ↗ via
   `::after{content:"\2197" / ""}`. The `/ ""` is CSS alt text, so the decorative
   glyph is not announced as "north east arrow". In print the pseudo-element
   switches to `" (" attr(href) ")"` so URLs are still spelled out.
5. **Hero.** Negative side margins equal to `--fn-app-pad` cancel the sheet's
   gutter, so the hero runs cyan-edge to cyan-edge while the centred 1320px
   sheet is preserved (no `100vw` breakout). The right-offset pink shadow became
   bottom-only to avoid a horizontal scrollbar. The `h1` clamp grew 1.15× from
   `clamp(1.85rem,5.4vw,4.75rem)` to `clamp(2.13rem,6.21vw,5.46rem)`, and the
   eyebrow gained 5px of bottom margin. The chip's bottom margin had been
   collapsed to zero by the generator's `.hero p{margin:10px 0 0}`, so the
   override was raised to `.hero .eyebrow` (0,2,0) to make the gap take effect.

**Skills consulted this round:** `design-system-patterns` (token hierarchy —
primitive → semantic → component tokens, which drove the `--fn-tag-cycle-*`
component tokens), `accessibility-compliance` (WCAG AA contrast and text
alternatives), and `web-design-guidelines` (decorative-icon alt text and focus
styles). The MCP server's POST tools remain unreachable from this sandbox, so
each skill's own `SKILL.md` was fetched from the allowlisted GitHub API. All six
tag fills were tested against the dark ink text: contrast ratios 8.59:1 to
14.00:1, all passing WCAG AA.

### Third refinements (2026-10-26): hero type scale

Three proportional changes, again only in `src/fieldnotes-theme.css`. The four
fact chips and the two progress cards had shared a single rule
(`.hero-facts span,.hero-stat`), so that rule was split into shared chrome
(border, background, colour, overflow) plus two independent sizing rules —
otherwise shrinking the chips would have shrunk the progress cards too.

1. **Hero subtitle 0.75×.** `clamp(1rem,2vw,1.27rem)` →
   `clamp(.75rem,1.5vw,.9525rem)`. Measured 20.32px → 15.24px at 1440px, and
   16px → 12px at 390px (the clamp floor). Line-height stays 1.55.
2. **Four fact chips 0.75×.** Type `.76rem` → `.57rem` (12.16px → 9.12px) and
   padding `6px 9px` → `4.5px 6.75px`. Chip count stays 4.
3. **Two progress cards 1.2×.** min-width `88px` → `105.6px`, padding
   `6px 9px` → `7.2px 10.8px`, number `1.55rem` → `1.86rem` (24.8px →
   29.76px), label `.72rem` → `.864rem`. Card count stays 2. Scaled via the
   underlying properties, not `transform: scale()`, to avoid blurring and
   overlap.

**Skill consulted:** `ui-ux-pro-max` (the collection's top-ranked design skill,
via its `SKILL.md` and `typography.csv` on the allowlisted GitHub API). Its
priority rules informed the check for no horizontal scroll, 44px tap targets and
type legibility. It also flags text below 12px as an anti-pattern, and the
shrunken fact chips now compute to 9.12px. That is below the guideline, but
these are short uppercase metadata chips rather than body copy, and white on
`rgba(17,20,43,.62)` over the blue hero remains high contrast. The 0.75× scale
was an explicit request; it can be raised to a 12px floor if legibility on a
real device is a concern.

### Fourth refinements (2026-10-26): hero rhythm and stage headers

Four more adjustments, in `src/fieldnotes-theme.css` plus one build-layer
attribute edit in `tools/build_tracker.py`.

1. **h1 ×1.4.** `clamp(2.13rem,6.21vw,5.46rem)` →
   `clamp(2.982rem,8.694vw,7.644rem)` (87.36px → 122.3px at 1440px). The
   `18ch` measure and `.98` line-height were kept after measuring that the h1
   does not clip inside the hero's `overflow:hidden` at any width. Consequence:
   the headline wraps to five lines on desktop and the hero grows to ~880px.
2. **Stage header baseline.** `.stage summary` used `align-items:center`, which
   aligned the number badge, `0%` counter and `+`/`−` toggle to the centre of
   the **two-line** heading block — ~10px below the title text. Changed to
   `align-items:baseline` so all three share the title's first baseline.
   Measured delta dropped from ~10.3px to ~2.2px at every width from 320 to
   1920px. (The pseudo-element is a flex item and joins the same baseline
   group.)
3. **"Reminder time" label removed from view.** The visible uppercase label was
   crowding the toolbar's flex row. The native `<label for="reminder-time">` is
   retained but visually hidden with the standard `.sr-only` pattern
   (`position:absolute`, 1px, clipped), and absolutely positioned so it leaves
   the flex flow entirely. The time input now carries `aria-label="Reminder
   time"` and `title="Reminder time"` (added in the build layer) so it announces
   itself to assistive tech and gives a mouse hover cue. The adjacent "Enable
   browser reminders" button supplies context.
4. **Tighter hero vertical rhythm**, excluding eyebrow→h1 as requested:
   h1→subtitle `18px` → `10px`; subtitle→chips `.hero-facts` margin-top `22px`
   → `12px`; chips→progress cards on mobile (where the hero stacks) `gap:24px`
   → `12px`. On desktop those two groups sit side by side, so only the mobile
   rule changed. Eyebrow→h1 stays at 5px.

**Skills consulted this round:** `taste-skill` (`design-taste-frontend`, on
art direction, type set larger and removing unneeded labels), `ui-ux-pro-max`
and `accessibility-compliance`. Two of their rules pull in opposite directions
here: `ui-ux-pro-max` has `input-labels` ("visible label per input"), while the
requested removal needs the label gone from view. The compromise keeps the
**programmatic** label association intact via `.sr-only` and adds an explicit
`aria-label` plus `title`, so the control still has an accessible name and a
mouse cue. This is the one place the design deliberately departs from the
skill's visible-label rule — an unreadable 3px label would have been worse.
`ui-ux-pro-max`'s `spacing-scale` (4/8px increments) informed the 10/12px gap
values. The MCP's POST tools remain unreachable from this sandbox, so skill
sources came from the allowlisted GitHub API.

## 3. Constraints that shaped the port

The skill's `validate_build.py --interactive-html` requires a self-contained
file. It rejects `<link>`, `<img>`, `<iframe>`, external `script src`, and **any
CSS `url(...)` reference** (including data URIs). So:

- The source's inline SVG favicon (`<link rel="icon" href="data:image/svg+xml…">`)
  was **not** copied. A tab icon would fail validation.
- The source's `assets/og-image.png` and social preview tags were **not** copied;
  they are external assets. The banner look is recreated in CSS instead.
- All decoration is CSS gradients, borders, shadows and pseudo-elements. The
  hero's banded grid uses two crossed `linear-gradient`s with a
  `mask-image` fade, exactly as the source does.
- The source's three coloured banner bars were initially reproduced with layered
  gradients on `.app::before`, then **removed on request**; the footer squares
  remain. All decoration is CSS gradients, borders, shadows and pseudo-elements.
- Print styles collapse the palette to black on white and spell out link URLs,
  following the source's print rules.

Typography needed no substitution: `--fn-mono` and `--fn-prose` are both system
stacks, so there are no `@font-face` or `@import` rules.

## 4. Verification

> All of these checks are now reproducible with `make check`,
> `make check-drift` and `make check-visual`, and run in CI via
> `.github/workflows/verify.yml`. This section records the original manual run.

Measured in **headless Chromium 153** (installed via the npm allowlist recipe in
the source repo's `docs/headless-chromium.md`), driving the actual built file:

- Computed styles match the tokens: hero `rgb(55,104,255)`, cyan 4px border,
  bottom-only pink `0 10px 0` shadow, 0px radius, cream app background,
  monospace body font, yellow eyebrow. After the refinements: eyebrow computes to
  `rgb(17,20,43)` on `rgb(255,225,104)`, hero top = app top = 0 with the bar
  pseudo-element's `content: none`, and the footer credit is the requested text.
- No console errors or page errors.
- **Zero horizontal overflow** at 320, 360, 390, 430, 600, 620, 700, 900,
  1024, 1200, 1320, 1440 and 1920 px. At every width: five distinct tag
  colours, `.stage-description` 14px/14px margins, a 9×9px filled square
  marker, an ↗ on all 26 links, and link/Done on one row with no overlap. A
  proper 2D overlap test confirms the two progress cards never overlap (they
  stack vertically at ≥900px and sit side by side below that), and both cards
  plus all four chips stay inside the hero at every width.
- After the fourth refinements, at all 13 widths: h1 `scrollWidth` equals
  `clientWidth` (no clipping), and the number badge / `0%` counter sit within
  ~2.3px of the stage title's first baseline (was ~10.3px). The hidden reminder
  label is `position:absolute` with 1×1px clip, and the input reports
  `aria-label`, `title`, `name` and `autocomplete` correctly.
- Functionality intact: 8 stages, 26 resources; ticking a resource moves the
  counter from `0 of 26` to `1 of 26`, sets `4%`, updates the stage meter to
  `33%`, advances "Next up", marks `.resource.done` and writes to localStorage;
  export and notification buttons do not throw; reset returns to zero.
- Heading outline is `h1` × 1, `h2` × 2, `h3` × 26; a skip link is present;
  primary buttons, import label, done control and stage summary all measure
  **≥44px** tall. The resource link also has a 44px tap target now.
- Print emulation replaces the ↗ with `" (https://…)"`; reduced-motion keeps
  the filled square and its centring transform.
- `validate_build.py --interactive-html` passes: no external assets, one inline
  script, one theme style block.

Headless Chromium is not a real phone: touch momentum, browser chrome and
device-specific storage behaviour were not tested.
