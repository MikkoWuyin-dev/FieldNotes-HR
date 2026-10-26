# Fieldnotes design system (ported)

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

**Adaptation:** the generator emits five metadata chips per resource (provider,
modality, cost, time, verification date). The source uses bright tags only for
short one-word keys, so here only the first (provider) chip and the cost chip
carry the accent palette; the long metadata chips stay quiet cream with a 2px
border. This keeps the visual language without turning every card into a wall of
neon.

### Requested refinements (2026-10-26)

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

Measured in **headless Chromium 153** (installed via the npm allowlist recipe in
the source repo's `docs/headless-chromium.md`), driving the actual built file:

- Computed styles match the tokens: hero `rgb(55,104,255)`, cyan 4px border,
  pink `10px 10px 0` shadow, 0px radius, cream app background, monospace body
  font, yellow eyebrow. After the refinements: eyebrow computes to
  `rgb(17,20,43)` on `rgb(255,225,104)`, hero top = app top = 0 with the bar
  pseudo-element's `content: none`, and the footer credit is the requested text.
- No console errors or page errors.
- **Zero horizontal overflow** at widths 320, 390, 430, 600, 620, 700, 900,
  1024, 1440 and 1920 px. At every width the link and Done control are on the
  same row with no overlap.
- Functionality intact: 8 stages, 26 resources; ticking a resource moves the
  counter from `0 of 26` to `1 of 26`, sets `4%`, updates the stage meter to
  `33%`, advances "Next up", marks `.resource.done` and writes to localStorage;
  export and notification buttons do not throw; reset returns to zero.
- Heading outline is `h1` × 1, `h2` × 2, `h3` × 26; a skip link is present;
  primary buttons, import label, done control and stage summary all measure
  **≥44px** tall. The resource link also has a 44px tap target now.
- `validate_build.py --interactive-html` passes: no external assets, one inline
  script, one theme style block.

Headless Chromium is not a real phone: touch momentum, browser chrome and
device-specific storage behaviour were not tested.
