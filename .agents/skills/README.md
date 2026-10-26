# Vendored agent skills

Skills in this directory are committed to the repository so they survive session and sandbox resets. Keep this copy as the authoritative one.

## `resource-learning-library/`

A portable agent skill for building roadmap-ordered learning libraries from verified resources. It supports free, paid or mixed resources and PDF, DOCX, Markdown, static HTML and an interactive HTML roadmap tracker.

**Provenance.** Reconstructed on 2026-10-26 from `resource-learning-library-transfer.md`, a portable transfer bundle attached to the session. All 12 files were copied from the bundle's fenced blocks and verified against its SHA-256 inventory table; every file matched its declared byte count and digest. No file was modified during vendoring.

Contents: `SKILL.md` (workflow), `INSTALL.md`, `README.md`, `requirements.txt`, four scripts in `scripts/`, an offline smoke test in `tests/`, and two examples in `example/`. See the skill's own `README.md` and `INSTALL.md` for details.

**Dependencies are not vendored.** On a fresh machine, from the repository root:

```bash
python3 -m pip install -r .agents/skills/resource-learning-library/requirements.txt
```

On PEP 668 externally-managed systems, use a virtualenv or add `--break-system-packages`. The requirements are `python-docx`, `reportlab` and `pypdf`.

**Smoke test:**

```bash
cd .agents/skills/resource-learning-library
python3 -m unittest discover -s tests -v
```

Deliverables produced with this skill live in `learning-library/` at the repository root; see `learning-library/README.md`. A global copy may also be placed at `$HOME/.agents/skills/resource-learning-library/` for agents that scan a personal skills root, but that copy is not the source of truth.

## Skill discovery for each task (standing workflow)

The project is registered with the **`skill-issue` MCP server** in [`.mcp.json`](../../.mcp.json) at the repository root (project scope, so it is shared and survives resets). It is a ranked library of agent skills.

**For every request or task, search that collection for skills relevant to the task and use them where they fit.** A typical sequence:

1. Query the server for recommendations (`recommend_skills`) or search by keyword (`search_skills`), optionally narrowing with `list_domains` / `list_domain_skills`.
2. Read the chosen skill with `get_skill` and follow its instructions.
3. Say which skills were used and what they changed. If the server is unreachable, say so plainly and fall back to the vendored skills here — never claim a skill was used when it was not.

The endpoint is `https://skill-issue.in/api/mcp` (streamable HTTP, JSON-RPC over **POST**). It cannot be reached from this sandbox's allowlisted egress; a normal machine can. On 2026-10-26 the `web-design-guidelines` skill was selected for the tracker restyling and its live rule set was applied — see `learning-library/DESIGN-SYSTEM.md`. Since its tools were not callable from the sandbox, the skill's own `SKILL.md` and its linked rule set were fetched from the allowlisted GitHub API instead.
