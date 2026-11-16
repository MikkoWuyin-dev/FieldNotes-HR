# Content and identity contract (Phase 2)

## Edit here

- `learning-library/src/catalog.json`: stage/resource facts, document metadata,
  explicit access classifications and per-URL research evidence. A resource ID
  identifies a learning task, not a URL: revisits of one URL can be separate tasks.
- `learning-library/src/library-narrative.md`: document-only teaching/context.
  Named slots insert canonical stages, resource cards, totals and first action.
- `learning-library/src/history/first-link-sweep.json`: frozen executed sweep.
  Do not append current URLs to an old result. A new sweep needs its own evidence.
- `learning-library/src/progress-compatibility.json`: frozen legacy aliases;
  retain existing mappings, even when retiring a card. New IDs must never reuse
  an existing ID or alias. New tasks get new descriptive IDs, not positions.

`make build` validates these inputs, generates the Markdown, roadmap JSON,
verification manifest and marked current-summary blocks, then renders all five
products. `python3 learning-library/tools/content.py --check` is a read-only
projection check. `make verify` includes it. Generated projections remain in Git
for consumers, diffs and compatibility, not as independent authoring inputs.
Makefile and drift checking read the same document metadata as the builder.
Historical reports and dated test tables retain their original snapshot counts.

## Access and evidence

Study, certificate and account classifications are distinct enumerated fields.
`not_verified` is intentionally not a negative claim. Account requirements can
vary between reading, assessment and certification; the evidence prose states
that distinction. A checked date records an existing research event, not fresh
verification performed by a build. Evidence URLs must be in the research index.

The hero free count requires BOTH explicit free study and confirmed URL evidence.
A paid professional route may have confirmed evidence without being free.
A partial listing page is not confirmed free. Certificates, optional fees,
professional exam prices, provider caveats and dates remain on the same generated
resource card in both the document and tracker. Document-only historical
verification narrative is not a replacement for the structured research index.
No new provider, enrolment, playback or external-link check is implied.

## Saved progress and backups

Storage namespace is unchanged. Keys are `resource:<permanent-id>` and
`stage:<permanent-id>`. Reordering/inserting cards no longer changes identity.
The local adapter normalizes old stored state in memory; subsequent actions save
canonical keys. Import uses the same normalizer. Original version 1 and unversioned
backups remain accepted. Version 2 exports carry the storage ID; a mismatching
identity or unsupported version is rejected without changing saved state.

Only boolean completion values are accepted on import. Known aliases map to
permanent IDs; explicit canonical values (including false) win over aliases.
Unknown boolean keys are retained but do not affect counts, allowing retired IDs
to return later. Invalid dates are discarded, duplicates removed and invalid
reminder times fall back to the configured default. Import replaces progress,
just as before; it does not enable notification permission. Old backups have no
reliable roadmap identity, so their origin cannot be proven automatically.
Export a backup before migrating origins: localStorage does not cross origins.

The protected generator is not patched. `build_tracker.py` applies labelled,
exactly-one extension anchors for branding, progress and Pals. Missing AND
duplicate anchors fail the build. Tests mutate each anchor, exercise legacy and
new backups, reject invalid payloads, and reorder/insert cards with saved ticks.
All behavior changes belong in these source adapters, not output-only edits.
