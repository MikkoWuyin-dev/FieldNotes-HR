# FieldNotes-HR

A researched, roadmap-ordered learning library for breaking into HR through the
Recruiter / Talent Acquisition path, plus the tooling that builds and verifies
it. Written for an absolute beginner in Lagos, Nigeria, with a free-first bias.

## Quickstart

```bash
git clone https://github.com/MikkoWuyin-dev/FieldNotes-HR.git
cd FieldNotes-HR
make bootstrap     # .venv/ from the pinned requirements.lock
make check         # every fast check
make check-drift   # prove the shipped outputs reproduce from source
```

`docs/SETUP.md` is the canonical setup and verification guide. CI runs the same
commands plus `make check-visual` on every push and pull request.

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

8 stages, 26 resource cards, 21 distinct URLs, about 94 hours of study (roughly
20 weeks at 5 h/week). 24 cards were confirmed free from provider pages; 2 are
paid or conditional. The tracker stores progress in browser localStorage and
makes no network requests. Research caveats — including pages that could not be
read — are recorded in `learning-library/src/verification-manifest.json` and
surfaced by `make check`.
