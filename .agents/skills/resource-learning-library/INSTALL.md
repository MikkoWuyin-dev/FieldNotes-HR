# Installing this skill on another agent

A skill is a folder containing `SKILL.md` and its supporting files. There is no package-manager installer: copy or unpack the folder into a location your agent scans, then restart the agent session if it reads skills only at startup.

## 1. Get the folder onto the machine

Use the ZIP distributed with this reconstruction, or copy the `resource-learning-library/` folder directly. The ZIP contains that folder at its root.

```bash
unzip resource-learning-library.zip -d ~/.claude/skills/
```

## 2. Place it where your agent looks

| Agent | Common location |
|---|---|
| Claude Code | `~/.claude/skills/resource-learning-library/` (personal) or `.claude/skills/resource-learning-library/` (repository) |
| OpenAI Codex CLI | `~/.codex/skills/resource-learning-library/` (personal) or `.codex/skills/resource-learning-library/` (repository) |
| Other CLI agents | Follow that agent's current documentation; point its custom instructions at this `SKILL.md` if it does not scan skill folders. |
| Arena | The skill loader may use a managed skills root. If it is not writable or does not scan the workspace, run the workflow and scripts by their full workspace path. |

These are common conventions, not a guarantee for every agent version. Trust the agent's current documentation. Restart the agent after installing if needed.

## 3. Install rendering and validation dependencies

```bash
python3 -m pip install -r requirements.txt
```

This installs `python-docx` (DOCX), `reportlab` (PDF), and `pypdf` (PDF validation). `curl` is used for link-status checks. A page-retrieval/browser tool is needed to read provider pages and verify pricing/access. The document scripts do not perform web research.

## 4. Smoke test

From the skill directory, run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/docx_render.py example/01-getting-started.md -o /tmp/rll-test --name Demo --format pdf docx md html
python3 scripts/validate_build.py /tmp/rll-test/Demo.pdf /tmp/rll-test/Demo.docx /tmp/rll-test/Demo.html
python3 scripts/interactive_app.py --input example/interactive-demo.json --output /tmp/rll-test/roadmap-app.html
python3 scripts/validate_build.py --interactive-html /tmp/rll-test/roadmap-app.html
python3 scripts/style_audit.py example/01-getting-started.md
```

The validator should report valid DOCX XML, a valid PDF with pages, no external assets in static HTML, and only inline script(s) in the interactive app. Exact counts depend on source content.

## 5. If the agent has no file access

Paste `SKILL.md` into the agent's task instructions. Tell it to establish the topic, cost preference, preferred modalities, roadmap, and output format before research; verify provider pages; and report checks it could not actually run. Without filesystem access, the included scripts cannot run; perform those checks manually or use an environment that can execute them. Do not claim a smoke test passed unless it was run.
