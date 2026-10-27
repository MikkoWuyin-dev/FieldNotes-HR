# Deploying to Vercel

This is a static site. The root `vercel.json` publishes only
`learning-library/out` and rewrites `/` to `/roadmap-app.html`. The four library
files remain available at their original filenames. There is deliberately no
catch-all rewrite: a missing file should return 404, not the tracker.

## Import settings

1. Import the GitHub repository into Vercel.
2. Keep **Root Directory** at the repository root (not `learning-library/out`),
   so Vercel reads `vercel.json`.
3. Use framework preset **Other** and production branch **main**.
4. Allow the repository configuration to supply the output directory and empty
   install/build commands. Remove conflicting dashboard overrides. No environment
   variables, Python server, Node dependencies or runtime functions are required.
5. Deploy after this configuration has been merged into main. A branch preview
   can test it beforehand.

The committed outputs are the deployable artifacts. This deployment deliberately
skips regeneration: existing GitHub Actions checks verify that outputs reproduce
from source. Before committing content changes, run `make build`, `make ci`, and
`make check-visual`, then commit the regenerated outputs. Never run `make preview`
as a Vercel build command: it starts a persistent local server.

Only put publicly shareable files in `learning-library/out`; everything there is
published. Source files, skill bundles and tooling outside it are not web assets.

## Configuration check

Run `python3 -m unittest discover -s tools -p 'test_deployment.py'` to check the
published file set, homepage rewrite and disabled install/build steps. This is a
local contract test, not a substitute for a real Vercel deployment test.

## Production smoke test

- `/` opens the tracker; `/roadmap-app.html` opens the same app.
- Download `/Recruiter-TA-Library.pdf`, `/Recruiter-TA-Library.docx`, and
  `/Recruiter-TA-Library.md`; `/Recruiter-TA-Library.html` opens the static library.
- A nonexistent route returns 404. `/README.md` and `/tools/check.py` should not
  expose repository files.
- Tick a resource, refresh, and check progress persists. Export and import a
  backup; check reset works.
- Check mobile layouts, Pals pause/resume, and reduced-motion behaviour.
- Test reminders only after explicitly granting notification permission; they
  still require the page to remain open. HTTPS does not enable background push.

Progress is stored in localStorage, scoped to a browser and origin. Export from
Arena before moving to the deployed domain, then import there. Preview domains,
production domains and custom domains do not share progress automatically. Choose
a stable custom domain early if you plan to use one.

No live deployment has been created or verified merely by adding this config.
