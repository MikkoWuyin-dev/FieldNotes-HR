# Setup and verification — current guide

Start with `AGENTS.md` for approval, branch, evidence and protected-file rules.
This file owns current commands. `docs/DESIGN-SPEC.md` owns current visual rules;
`CHANGELOG.md` and the retrospective/reports record history, not current setup.

## Prerequisites

| Tool | Supported baseline |
|---|---|
| Python + venv support | >=3.11; CI uses Python 3.11 |
| Node + npm | Node >=22.12.0; CI uses 22.22.3 |
| Git, Bash, make | Required for the documented workflow |
| Platform | Linux browser harness; other OS/browser combinations are not certified |

No global Python packages or personal skill install are required. Dependencies
are pinned in `requirements.lock` and `tools/visual/package-lock.json`.

## Start a session

```sh
git status -sb
make doctor
make bootstrap
make verify
```

Doctor may exit nonzero on a fresh session because tools are absent. Read its
specific next steps. A dirty working tree is a warning: preserve it. If history
is shallow, fetch full history before claiming a complete history audit; do not
change branches to recover it.

## Commands and scope

| Command | Scope and effects |
|---|---|
| `make doctor` | Read-only offline diagnosis: Git/branch/history, Python, Node/npm, dependencies/imports, protected hashes, output presence. No repair or product tests. |
| `make bootstrap` | Checks the current lock, installed versions, required imports and pip dependency consistency every time. Recreates missing/unhealthy venv transactionally. May need package-registry access. |
| `make repair-env` | Explicit recreation of only the recognized `.venv`; rollback if replacement fails. Does not edit source, output or lock. |
| `make verify` | Full: environment, repository tests, fast checks, output drift and browser. Each layer gets a status; missing required coverage exits nonzero. |
| `make verify-core` | Core subset used by CI; explicitly not full verification. |
| `make verify-browser` | Browser subset used by CI; explicitly not full verification. |
| `make check` | Fast checks, including five borrowed smoke tests, validators, contracts, sources, selected docs, Pals, historical sweep and freshness. |
| `make check-drift` | Rebuild in a temporary directory; compare five outputs without replacing delivered files. |
| `make check-visual` | npm clean install and the 13-width Chromium harness; no source/output rebuild. |
| `make ci` | Legacy fast + drift subset only. Use `make verify` for the complete local command. |
| `make build` | Regenerate all five delivered files intentionally. |
| `make preview` | Stdlib tracker rebuild + durable server, default `0.0.0.0:8000`. |
| `make links` | Outside-link HTTP report; needs suitable egress; does not establish free access. |
| `make pin-skill` | Change approved fingerprints only after a reviewed, intentional skill upgrade. |
| `make clean` | Remove selected disposable caches/reports, not source or delivered files; keeps venv. |

CI runs `make verify-core` and `make verify-browser` in separate jobs using the
same runner/layer definitions as the full local command. Both jobs must succeed.
Warnings remain visible. A missing/failed required layer makes its scope fail;
other independent layers still run where possible. A core-only success is not
a browser success. Verification never rebuilds delivered outputs in place.

## Environment maintenance and interrupted repair

Bootstrap examines the live package versions rather than trusting a stamp or
only the existence of `.venv/bin/python`. A changed package pin, missing import
or failed pip check triggers replacement. A healthy environment is left alone;
a comment-only lock change does not force a pointless reinstall.

Replacement renames the old recognized venv to `.venv.repair-backup`, creates
`.venv` at its final path, installs the lock and checks it. On success the old
copy is removed; on handled failure or interruption the old copy is restored.
No system-pip override or automatic lock rewriting is used.

For safety, maintenance refuses a symlink `.venv`, an unrecognized directory or
an existing backup. `.venv-maintenance.lock` prevents concurrent maintenance.
An abrupt machine termination cannot execute rollback: inspect the two venv
paths and any running process before manually recovering. Do not blindly remove
backups or another operation's lock. Source and generated deliverables are never
repair targets. Installation failures remain failures; registry restrictions
are not a reason to weaken TLS or install unpinned packages.

## Sources and generated outputs

<!-- content-summary:start -->
8 stages, 21 resource cards, 21 distinct card URLs, 94 planned hours.
20 planned weeks; 20 cards have confirmed free-study evidence.
Certificate, account and professional-qualification terms are separate; partial findings are not counted as verified free.
<!-- content-summary:end -->

Edit shared facts in `learning-library/src/catalog.json`, and document-only
prose in `learning-library/src/library-narrative.md`. Markdown, tracker JSON,
manifest and marked summary blocks are generated projections. Verification
checks complete projections, not only counts/URLs. See `docs/CONTENT-MODEL.md`
for access classifications, permanent IDs and backup migration. Never change a
historical sweep to imply it checked newly added URLs.

Appearance belongs in `learning-library/src/fieldnotes-theme.css` and the local
builder; theme behavior lives in `learning-library/src/theme-toggle.js`, and
the fixed back-to-top control is sourced from
`learning-library/src/scroll-to-top.js`. The light/dark control sits at the
hero's top right, follows the system setting until changed and stores its
separate browser-local preference without changing progress or backups. The
back-to-top button appears after scrolling, hides at the top or after three
seconds without scrolling, and respects reduced-motion preferences. Pals
sources are under `learning-library/src/pals/`: the layer uses
full-document **absolute** positioning, with ten placements and eight species.
The MIT engine is pinned and unchanged; the local controller handles idle
activation, pause, initial reduced-motion defaults and re-anchoring.

After content/design edits, run `make build`, inspect source and outputs, then
`make verify`. PDF/DOCX metadata may change; drift compares PDF extracted text
and DOCX archive entries, not universal binary hashes. Read affected pages when
layout matters. Never edit only the finished HTML.

The legacy “Your first hour” teaching paragraph is still awaiting alignment with
the HR Essentials-first card order; correcting teaching content and regenerating
its documents is deferred to content work, not silently done by environment repair.

## Preview identity and browser origins

```sh
make preview
# optional different port: make preview PORT=8080
# separate shell, opt-in local HTTP read:
python3 -B tools/doctor.py --preview-port 8000
```

Preview rebuilds tracker only, so it works with stdlib Python after venv/npm
loss. Use a managed long-running process rather than a timed shell call. It
maps both GET and HEAD `/` and `/index.html` to the tracker, sends no-store
headers and exposes `X-FieldNotes-Artifact-SHA256`. The server also prints the
tracker fingerprint at startup. Doctor compares served bytes, header and local
tracker; source drift is checked separately by verification.

Without `--preview-port`, doctor makes no network requests and does not assert
that a preview exists. This flag contacts sandbox loopback, not the user's
browser. Do not put localhost backend URLs into browser-facing code.

The agent snapshot excludes runtime/cache folders and `out/`; old committed
output can return after a reset. Rebuild rather than merely restarting a server.
localStorage is per browser origin/profile. Export/import when moving between
local files, preview and production; these do not automatically share progress.

## Validation, warnings and exact favicon exception

The supplied skill stays byte-exact. Its validator rejects all link tags. Our
local policy permits exactly one hash-pinned inline favicon: remove only that
exact tag from a temporary validation copy, validate the rest, deliver the
original with the icon. Use repository checks, not a blanket validator override.
No external fonts, scripts or images are permitted.

Research freshness warnings identify old confirmed dates or unresolved access
gaps, not automatic provider rereads. For a deliberately strict run use
`.venv/bin/python tools/check.py all --strict`. Doc lint checks selected current
summaries, known patterns, references and Make targets. It does not prove every
sentence is current, and a green browser run does not certify all real devices.

## Restricted access and retry policy

Historically shell provider access, MCP POST and artifact redirect hosts were
restricted. Metadata access and workflow-start authority are separate. Doctor
is offline; it cannot grant permissions or prove these external paths work.
After an unchanged refusal, stop retrying unless configuration, route or
permission actually changed. Never ask for credentials or signed artifact URLs.

The owner-assisted fallback is to start `link-check` in GitHub's Actions UI (or
wait for Monday 06:17 UTC), then provide the actual run link, exact URL snapshot,
status totals and non-success list. If raw output is unavailable, record that
limit and its provenance. A configured schedule is not proof a run occurred.
A 200 never proves free access; read relevant provider pages before changing
claims/dates. The first run was 40471064309: 30 URLs, 27x200/3x403. Browser-like
rereads supported the three content findings; bot filtering was the interpretation,
not a direct inspection of provider firewalls. Do not change that old snapshot.

## Skills, handoff and boundaries

`.mcp.json` registers the catalogue and `.claude/settings.json` holds project
approval. Search for useful skills per task; disclose execution restrictions and
use suitable readable sources where available. Registration/catalog access does
not establish MCP execution. The vendored skill's generic INSTALL instructions
are not this repository's setup policy.

At handoff state exact commands/results, warnings and NOT RUN layers, plus dirty
files needing preservation. Get explicit authorization before Git publication
or deployment. Historical reports remain historical; do not rewrite them to hide
previous limitations. No closed-tab notifications, cloud progress sync, full
accessibility certification or complete physical-device coverage is promised.
