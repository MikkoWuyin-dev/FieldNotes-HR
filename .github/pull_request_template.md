## What changed

<!-- One or two sentences. Link the retrospective issue if this addresses one. -->

## Content or design change?

- [ ] Content edit: update `learning-library/src/catalog.json` and/or
      `learning-library/src/library-narrative.md`, then run `make build`.
      Review generated Markdown, roadmap JSON, manifest and current summaries;
      do not edit generated projections as independent sources.
- [ ] Appearance edit in `learning-library/src/fieldnotes-theme.css` — did you
      run `make build` so `out/roadmap-app.html` is regenerated, not hand-edited?
- [ ] Pal placement edit in `learning-library/src/pals/pals.json` — did you
      re-run `make check-visual` and confirm zero control-centre hits and bounded overlap at every width?
- [ ] Neither (tooling / docs / CI only).

## Verification

Run locally and paste the summary line from each:

```bash
make doctor
make verify
```

- [ ] Full `make verify` completed; attach each layer status (including warnings).
- [ ] Any FAILED or NOT RUN required layer is disclosed, not called a full pass.
- [ ] Output/source changes and protected-file boundaries reviewed.
- [ ] `check-links.sh` / freshness concerns noted, or N/A

## Honest reporting

If a check could not be run in this environment, say so here. Do not claim a
check passed unless it was actually executed. Note any research claims whose
provider pages could not be reached.
