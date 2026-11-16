# Phase 1 — implementation and verification

## Scope

Implemented on `arena/8c02879a-fieldnotes-hr`, based on the PR #8 product.
This is a working-tree change, not a published release. No commit, push, PR,
hosting change or deployment was performed. Existing historical reports were
preserved, even where their descriptions of then-current tooling are now old.

## Delivered

- `AGENTS.md`: durable agent entry point, approval/branch constraints, source
  authority, protected boundaries, recovery, retry policy and handoff rules.
- `tools/doctor.py` / `make doctor`: offline diagnosis without automatic repair.
  Optional local preview probe refuses redirects/proxies and checks served bytes
  against both the response fingerprint and the local tracker.
- `tools/environment.py`: live lock-version, import and pip-consistency checks;
  bootstrap recovers a missing/unhealthy venv. Explicit repair recreates only
  the recognized project venv, retains a backup until health passes, and rolls
  back on handled failure. Unsafe paths, existing backups and concurrent
  maintenance are refused. Abrupt termination still requires manual inspection.
- `tools/verify.py` / `make verify`: all required layers have explicit statuses.
  Failure or NOT RUN required coverage exits nonzero. Independent later checks
  continue where possible. Research warnings remain visible rather than hidden.
- Shared core/browser scopes wired into the existing two CI jobs. Each subset
  says that it is not a full-verification claim.
- Preview startup/GET/HEAD tracker identity via SHA-256 and response header.
- Current setup/count/layer/favicon instructions corrected; current-summary
  assertions added and doc-check wording limited to its actual coverage.
- Safety/coverage tests in `tools/test_workflow.py` and an updated PR checklist.

## Actual checks run

| Check | Observed result |
|---|---|
| Initial offline doctor in this reset environment | Correctly failed the missing-venv prerequisite; reported shallow history and existing work without changing it |
| Final `make doctor` after recovery | Local prerequisites/protected files/output presence passed; dirty-tree and shallow-history warnings; preview/external checks explicitly NOT RUN |
| Full `make verify` | All required layers executed; completed with the existing research warning |
| Repository tests | 26 methods passed, including the original deployment/favicon methods |
| Borrowed smoke tests | 5 passed inside the fast suite |
| Fast suite | 9 passed, 1 warning, 0 failures; warning: 0 stale dates, 8 open research gaps |
| Drift | All five outputs reproduce using the existing PDF-text/DOCX-entry comparisons |
| Browser | 13/13 widths plus three default-state checks passed; no runtime errors in tested paths |
| `make verify-core` | Required core layers completed; browser explicitly outside partial scope |
| `make verify-browser` | Browser layer passed; core explicitly outside partial scope |
| Preview identity test | Real temporary HTTP server: GET/HEAD fingerprints and matching-body probe passed; mismatched body/header refused |

Unit coverage includes missing environment, lock reread, healthy no-op, unsafe
path/backup refusal, failed-repair rollback, unchanged source sentinel, offline
read-only diagnosis, obsolete-node refusal, selected-doc drift, required-layer
NOT RUN failure, later-layer execution after failure and shared CI scope wiring.

## Real isolated environment-recovery exercises

A temporary root with a copy of the actual lock and an unrelated source sentinel
was used, not the working repository's venv/source as a destructive fixture:

1. Cold bootstrap created and checked the pinned environment.
2. Repeating healthy bootstrap did not reinstall.
3. Removing pypdf made health inspection fail; bootstrap restored health.
4. Changing the typing_extensions pin from 4.16.0 to 4.15.0 was detected; the
   replacement matched the modified temporary lock.
5. Explicit repair succeeded; no backup or maintenance lock remained.
6. The unrelated source sentinel remained unchanged.

Rollback on a simulated creation failure was separately verified by unit tests.
The old fixture environment was restored. This is not a claim that forced
machine termination or every filesystem/network failure was exercised.

## Problems found during implementation

The first full-command attempt found a missing default root argument in the new
bootstrap CLI; it was fixed and a regression test added. The runner correctly
marked dependent checks NOT RUN and still ran its independent browser layer.
A later docs check flagged a transient lock-directory name and a preview route
as if they were source files; these two exact non-file references were added to
the explicit exception list. Final full and scoped runs completed as above.

## Deliberate boundaries / follow-up

- No delivered learning artifact, content source, protected skill, engine,
  favicon artwork, progress key or dependency lock was changed.
- The legacy teaching “Your first hour” paragraph remains a disclosed content
  mismatch. Aligning it and regenerating its documents belongs to content work.
- Canonical content modelling/permanent-ID migration is Phase 2, not done here.
- A complete fresh-agent repository rehearsal is Phase 3. The isolated venv
  exercises above are narrower and do not claim that milestone.
- CI configuration was tested locally through the shared scopes; remote GitHub
  execution was not triggered or observed for these unpushed changes.
- Doctor intentionally leaves preview/network checks NOT RUN unless requested;
  its successful local diagnosis is not full product verification.
- The shallow-history warning was not suppressed or repaired unnecessarily;
  no new complete-history claim was made.
