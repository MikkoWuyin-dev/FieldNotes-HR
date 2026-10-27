# Third-party notices

FieldNotes-HR ships one vendored third-party component. Its full licence text is in
`learning-library/src/pals/LICENSE-MIT.txt`.

## Piixpal v0.4.0 — tiny pixel creatures that live on your website

- **Upstream:** https://github.com/diiviikk5/Piixpal
- **Licence:** MIT — `Copyright (c) 2026 Piixpal contributors`
- **Vendored from:** `MikkoWuyin-dev/Field-Notes_Nature-Photography`, where it is
  embedded as an inert `<template id="pals-payload">` in `index.html`.
- **Copied into this repository as:** `learning-library/src/pals/piixpal-payload.html`
  (the template block, byte-exact apart from two provenance comments above it).
- **Used for:** the 10 optional decorative "pals" in
  `learning-library/out/roadmap-app.html`. The engine is lazy-loaded on idle,
  can be paused by the visitor, and is off by default under
  `prefers-reduced-motion: reduce`.
- **Integrity:** the payload's SHA-256 is pinned in
  `learning-library/src/pals/pals.json` and checked by `make check`.

The payload comprises the Piixpal core plus eight sprite definitions
(`bitbug`, `lurk`, `moss`, `pip`, `capy`, `bumble`, `shel`, `frog`). Each script
carries its own MIT header. It uses canvas and shadow DOM, makes no network
requests, and contains no external assets. Our own controller, configuration and
styling live in `learning-library/src/pals/`.

The other vendored component, `.agents/skills/resource-learning-library/`, is a
skill bundle supplied by the user in this session; its provenance is recorded in
`.agents/skills/README.md`.
