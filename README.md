# FieldNotes-HR

A researched, roadmap-ordered learning library for breaking into HR through the
Recruiter / Talent Acquisition path, plus the tooling that builds and verifies
it. Written for an absolute beginner in Lagos, Nigeria, with a free-first bias.

## Quickstart

```bash
git clone https://github.com/MikkoWuyin-dev/FieldNotes-HR.git
cd FieldNotes-HR
make doctor        # offline diagnosis; missing prerequisites are reported, not repaired
make bootstrap     # validate/recover the pinned project venv
make verify        # full checks, including repository tests, drift and browser
```

Read `AGENTS.md` before agent work. `docs/SETUP.md` owns current recovery and
verification instructions. CI uses the same `verify-core` and `verify-browser`
layers as the full local command. `make check` and legacy `make ci` are subsets,
not full-verification claims. `make repair-env` explicitly recreates only the
recognized project venv with rollback on failure.

## Deployment

Vercel configuration is in `vercel.json`: only `learning-library/out` is
published, with `/` mapped to the tracker and no server/build dependencies.
Keep the Vercel project root at the repository root. See `docs/DEPLOYMENT.md`
for import settings, progress migration and the production smoke-test checklist.

## Repository contents

- **`learning-library/`** — the deliverables: PDF, DOCX, Markdown, static HTML
  and an interactive roadmap tracker styled with the Fieldnotes design system
  and decorated with 10 optional MIT-licensed pixel pals, together with sources
  and a verification log. Start with `learning-library/README.md`; the current
  design contract is `docs/DESIGN-SPEC.md` and the historical port record is
  `learning-library/DESIGN-SYSTEM.md`. See `THIRD-PARTY-NOTICES.md` for the
  Piixpal licence.
- **`.agents/skills/resource-learning-library/`** — the agent skill that
  produced the library, vendored byte-exact so it persists across sessions.
  Includes `SKILL.md`, renderer/validator scripts, requirements and offline
  tests. See `.agents/skills/README.md` for provenance and setup.
- **`.mcp.json`** — project-scoped registration of the `skill-issue` MCP skill
  collection. For each task, search it for relevant skills and use them;
  `.claude/settings.json` pre-approves it for clones.
- **`tools/`** — repo-wide verification (`check.py`, the skill hash inventory,
  and the 13-viewport Chromium harness in `tools/visual/`).
- **`RETROSPECTIVE.md`** — diagnosis of the recurring workflow problems and the
  fixes that addressed them. **`CHANGELOG.md`** — change history.

## Deliverable at a glance

<!-- content-summary:start -->
8 stages, 20 resource cards, 20 distinct card URLs, 94 planned hours.
20 planned weeks; 20 cards have confirmed free-study evidence.
Certificate, account and professional-qualification terms are separate; partial findings are not counted as verified free.
<!-- content-summary:end -->
The manifest covers the current URL evidence; the first
executed HTTP sweep checked its frozen historical URL snapshot. Research caveats and dates
are in `learning-library/src/verification-manifest.json`. The tracker stores
progress per browser origin, has no backend, and makes no autonomous external
resource requests; user-clicked provider links still require internet access.
