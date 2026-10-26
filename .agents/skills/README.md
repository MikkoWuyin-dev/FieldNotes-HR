# Vendored agent skills

Skills in this directory are committed to the repository so they survive session and sandbox resets. Keep this copy as the authoritative one.

> **Canonical setup:** `docs/SETUP.md`. The skill's own `INSTALL.md` describes
> generic agent locations such as `~/.claude/skills/`; those are conventions,
> not instructions for this repo. Here the authoritative copy is the vendored
> one, and dependencies come from `make bootstrap` using `requirements.lock` —
> do not install globally or use `--break-system-packages`.

## `resource-learning-library/`

A portable agent skill for building roadmap-ordered learning libraries from verified resources. It supports free, paid or mixed resources and PDF, DOCX, Markdown, static HTML and an interactive HTML roadmap tracker.

**Provenance.** Reconstructed on 2026-10-26 from `resource-learning-library-transfer.md`, a portable transfer bundle attached to the session. All 12 files were copied from the bundle's fenced blocks and verified against its SHA-256 inventory table; every file matched its declared byte count and digest. No file was modified during vendoring. That inventory is now committed as `tools/skill-hashes.sha256` and checked by `make check`, so the byte-exact claim no longer depends on a bundle that lives outside the repo. To upgrade the skill deliberately: replace the files, then run `make pin-skill`.

Contents: `SKILL.md` (workflow), `INSTALL.md`, `README.md`, `requirements.txt`, four scripts in `scripts/`, an offline smoke test in `tests/`, and two examples in `example/`. See the skill's own `README.md` and `INSTALL.md` for details.

**Dependencies are not vendored.** From the repository root, `make bootstrap`
installs the exact pinned tree from `requirements.lock` into `.venv/`. There is
no global install and no PEP 668 workaround. The three top-level requirements
are `python-docx`, `reportlab` and `pypdf`; the lock also pins their transitive
dependencies, because unpinned installs changed PDF/DOCX bytes between runs.

**Smoke test:** `make check` from the repository root runs the vendored unit
tests alongside every other check. To run only that suite:

```bash
.venv/bin/python -m unittest discover -s .agents/skills/resource-learning-library/tests -v
```

Deliverables produced with this skill live in `learning-library/` at the repository root; see `learning-library/README.md`. A global copy may also be placed at `$HOME/.agents/skills/resource-learning-library/` for agents that scan a personal skills root, but that copy is not the source of truth.

## Skill discovery for each task (standing workflow)

The project is registered with the **`skill-issue` MCP server** in [`.mcp.json`](../../.mcp.json) at the repository root (project scope, so it is shared and survives resets). It is a ranked library of agent skills.

**For every request or task, search that collection for skills relevant to the task and use them where they fit.** A typical sequence:

1. Query the server for recommendations (`recommend_skills`) or search by keyword (`search_skills`), optionally narrowing with `list_domains` / `list_domain_skills`.
2. Read the chosen skill with `get_skill` and follow its instructions.
3. Say which skills were used and what they changed. If the server is unreachable, say so plainly and fall back to the vendored skills here — never claim a skill was used when it was not.

The endpoint is `https://skill-issue.in/api/mcp` (streamable HTTP, JSON-RPC over **POST**). It cannot be reached from this sandbox's allowlisted egress; a normal machine can. On 2026-10-26 the `web-design-guidelines` skill was selected for the tracker restyling and its live rule set was applied — see `learning-library/DESIGN-SYSTEM.md`. Since its tools were not callable from the sandbox, the skill's own `SKILL.md` and its linked rule set were fetched from the allowlisted GitHub API instead.
