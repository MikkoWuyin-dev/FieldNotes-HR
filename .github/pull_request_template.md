## What changed

<!-- One or two sentences. Link the retrospective issue if this addresses one. -->

## Content or design change?

- [ ] Content edit in `learning-library/src/` — did you update **both**
      `recruiter-talent-acquisition-library.md` **and** `roadmap-app.json`?
- [ ] Appearance edit in `learning-library/src/fieldnotes-theme.css` — did you
      run `make build` so `out/roadmap-app.html` is regenerated, not hand-edited?
- [ ] Pal placement edit in `learning-library/src/pals/pals.json` — did you
      re-run `make check-visual` and confirm zero control overlap at every width?
- [ ] Neither (tooling / docs / CI only).

## Verification

Run locally and paste the summary line from each:

```bash
make bootstrap
make check
```

- [ ] `make check` passed (unit tests, validators, style audit, contract test,
      source consistency, doc lint)
- [ ] `make check-drift` passed — committed outputs still match their sources
- [ ] If appearance changed: `make check-visual` passed at all 13 widths
- [ ] `check-links.sh` / freshness concerns noted, or N/A

## Honest reporting

If a check could not be run in this environment, say so here. Do not claim a
check passed unless it was actually executed. Note any research claims whose
provider pages could not be reached.
