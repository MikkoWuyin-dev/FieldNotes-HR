# Phase 2 — canonical content and progress compatibility

## Delivered scope

Shared stage/resource facts now live in `learning-library/src/catalog.json`.
Document-only narrative has named slots. The Markdown, roadmap JSON, verification
manifest, marked current summaries and five products are generated. Makefile and
drift verification use the same canonical cover metadata. See
`docs/CONTENT-MODEL.md` for authoring and identity rules.

Permanent IDs replace position-based completion identity. The original storage
namespace and frozen legacy alias ledger preserve old local state and backups.
Version 2 exports carry roadmap identity. Import validates versions, completion
types and identity before changing state. Dates/times are normalized; canonical
keys win alias conflicts; unknown boolean keys survive without affecting counts.

All branding, progress and Pals anchors require exactly one match, including
head insertion. The generator normalizes away unknown fields, so a labelled local
identity bridge restores permanent IDs before state loading. Protected generator,
Piixpal payload and favicon source remain unchanged.

## Actual checks and implementation findings

- Bootstrap restored the missing session venv from the unchanged dependency lock.
- Repository tests: 32 methods passed, including six new Phase 2 methods covering
  invalid catalogue inputs, deterministic projections, propagation of edited
  facts, frozen history/aliases, all missing/duplicate extension anchors and
  Node-executed migration/backup/reorder/insertion regressions.
- Vendored tests: five passed; all 12 protected skill hashes matched.
- Fast checks: nine passed, one existing research-freshness warning. No stale
  confirmed evidence; eight unresolved research gaps remain.
- All five outputs reproduced: tracker/Markdown/static HTML bytes, DOCX archive
  parts, and PDF extracted text. This is not universal binary timestamp identity.
- Browser: 13 viewport widths and three collapsed-stage states passed. Legacy
  local state, actual legacy file import, actual version 2 export Blob/import
  round-trip, invalid-import no-write, tick/reset, Pals pause/reduced motion,
  favicon decoding and existing playlist activation/scroll checks passed. No
  console/page runtime errors. Existing bounded Pals overlap remains allowed.
- Compared every original resource modality, cost, duration, teaching rationale,
  action and access/verification field with its canonical counterpart: unchanged.
  The document's false blanket-free claim and stale first-hour instructions were
  intentionally corrected. Cover wording no longer implies uniform verification.
- Compared the extracted historical sweep object and all pre-existing report
  hashes with the pre-Phase-2 snapshot: unchanged. The frozen sweep still records
  30 historical URLs, not the current evidence index's 31 entries.

The first full run failed browser progress tests because the generator stripped
IDs. This was fixed in the local bridge, not by editing the vendor. A subsequent
run caught a documentation link to this not-yet-created note; the note was added
before final verification. Neither failed run is counted as a successful check.

The hero now reports **24 confirmed-free cards**, not the old cost-string-based
25. Partial Jobberman evidence is excluded. Paid CIPM evidence can be confirmed
without being free. Study, certificate, account and professional qualification
remain separate findings; no provider research dates were advanced.

## Boundaries

Catalogue pages for web guidelines and modern JavaScript patterns were consulted;
the latter's GitHub skill instructions were read as a source fallback. This is
not proof of executing its MCP or installing another skill. The repository's
existing vendored skill remains byte-exact.

No fresh provider verification, enrolment, playback/mobile handoff, physical-device
or full accessibility audit was performed. No remote CI, commit, push, PR or
deployment was triggered. Phase 3's complete fresh-agent repository-copy rehearsal
is still separate work. Old backups without an identity cannot have their origin
proven; localStorage still does not cross origins. Export before changing origin.
