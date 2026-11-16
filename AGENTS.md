# FieldNotes-HR: start here

## Before touching the project

1. Read the current conversation/session branch instructions and `git status -sb`.
   Preserve existing work, including untracked reports. Never reset, clean, stash,
   rename branches or overwrite changes merely to obtain a clean tree.
2. Acknowledge the requested change and wait for the owner's go-ahead before
   commands/changes, unless the message already authorizes the work. A request
   to implement is not permission to commit, push, open/merge a PR or deploy.
3. Stay on the session's assigned branch. Do not assume a branch name from an
   older report is current. Inspect history only as deeply as the task needs;
   fetch full history explicitly before claiming a complete chronology.
4. Run `make doctor`. It is read-only and offline by default. A dirty-tree
   warning is information, not permission to delete another person's work.
5. Search the registered skill-issue catalogue for a relevant skill per task.
   If execution is blocked, disclose it and read suitable available sources.
   Catalog access or registration is not successful MCP execution.

## Sources and protected boundaries

- `docs/SETUP.md`: current commands, recovery and capabilities.
- `docs/DESIGN-SPEC.md`: intended current appearance/behavior.
- `CHANGELOG.md`: dated history, not instructions overriding current source.
- `RETROSPECTIVE.md`, engineering/plain-English/recurring-issue reports and
  `learning-library/DESIGN-SYSTEM.md`: historical evidence. Do not rewrite them
  to make today's implementation appear to have existed earlier.
- `learning-library/src/catalog.json` is the shared learning-fact authority;
  `learning-library/src/library-narrative.md` supplies document-only prose.
  Markdown, roadmap JSON and verification manifest are generated projections.
  See `docs/CONTENT-MODEL.md`. Run `make build` after edits, never patch generated
  projections alone. Frozen history and legacy identity aliases are not new evidence.
- Theme changes belong in `learning-library/src/fieldnotes-theme.css`; local
  extensions belong in `learning-library/tools/build_tracker.py` and Pals
  source files. Regenerate output, never hand-edit output only.
- Never edit `.agents/skills/resource-learning-library/`, the pinned Piixpal
  payload or favicon source casually. Intentional upgrades require review and
  explicit pin changes; never repin merely to silence an unexpected mismatch.
- Keep existing localStorage IDs, saved-resource keys and backup compatibility.
  Do not reorder cards without a migration. Keep historical sweep URLs frozen;
  a new URL is not evidence that an older sweep checked it.

## Working commands

- `make doctor`: diagnose; does not install, repair, regenerate or call outside
  services. Nonzero means a local prerequisite/integrity problem was found.
- `make bootstrap`: validate/recreate the project venv if missing or unhealthy.
- `make repair-env`: explicitly recreate only the recognized `.venv`, keeping
  the old copy until replacement passes; rollback on failure. Never system pip.
- `make verify`: **full** local checks (environment, repository tests, fast
  checks, drift, browser). Failure or an unrun required layer exits nonzero.
- `make check`: fast subset; `make ci`: legacy fast + drift subset, **not full**.
- `make verify-core` / `make verify-browser`: CI uses these same verification
  layers in parallel; neither alone is a full-verification claim.
- `make build`: regenerate five products, then review changed artifacts.
- `make preview`: rebuild only tracker, serve on `0.0.0.0:8000` (or PORT).
  Use a managed long-running process. To identify a running local preview:
  `python3 -B tools/doctor.py --preview-port 8000`.

## Disposable state and safe recovery

Processes, `.venv`, node_modules, browsers, caches, screenshots and `/tmp`
reference clones may disappear. `out/` is snapshot-excluded in the agent
workspace: serving an existing file does not prove it is the newest build.
The preview prints a tracker fingerprint and returns it in a response header.
Doctor can match served bytes to the local file; `make verify` separately checks
that the local file reproduces from source.

Bootstrap/repair never edits source or the lock. It refuses symlink/unrecognized
`.venv` paths and existing repair backups. After an interrupted repair, inspect
`.venv.repair-backup` and the maintenance lock before any manual recovery. Do
not delete a lock while another operation is running. See setup for details.

## Capability and retry rules

Connectivity, authorization, job execution and content truth are separate checks.
Historically provider curl/MCP POST/artifact redirects were restricted. GitHub
metadata could be read while workflow dispatch lacked effective Actions-write
permission. Do not retry an unchanged denial without a meaningful capability,
configuration or authorization change. Use the documented owner-assisted sweep
fallback. Never request tokens, passwords or signed download links in chat.

A 200 is not proof of free access. “Free trial”, free study, free certificate
and professional qualification are different. Do not update verification dates
without reading relevant evidence. HTTPS does not enable closed-tab reminders.

## Before handing off

Report the exact checks run, PASSED/FAILED/WARNING/NOT RUN, and scope. Do not say
“all checks passed” if a required layer was absent. Browser events do not prove
external playback or mobile-app handoff; headless Chrome is not every phone.
Review `git diff --check` and status. Summarize changes, warnings, limitations and
remaining work. Do not commit/push/deploy without the owner's separate authority.
Record durable decisions in the appropriate current guide/changelog, never rely
on a temporary cache or the conversation as the only setup instruction.
