# FieldNotes-HR — recurring issues that hindered or slowed the work

**Prepared:** 1 November 2026, Africa/Lagos.  
**Scope:** repeated work barriers and repeated sources of rework, from the original library through PR #8 and the subsequent report audits.  
**Product version inspected:** `765f2e2b672e7ae04a0137133c2028d48cb70357`.  
**Working branch:** `arena/8c02879a-fieldnotes-hr`.  
**Companion documents:** [engineering report](ENGINEERING-REPORT.md), [plain-English report](ENGINEERING-REPORT-PLAIN-ENGLISH.md), [earlier retrospective](../RETROSPECTIVE.md).

> **Recurring issues only.** This is not another complete project history, bug list or speculative risk register. An incident is included as evidence only when it helps establish a repeated problem. One-off errors, untested possibilities and intentional project constraints are not promoted into recurring failures.

## Contents

1. [Scope and rules for inclusion](#1-scope-and-rules-for-inclusion)
2. [Main findings](#2-main-findings)
3. [Recurring issue register](#3-recurring-issue-register)
4. [R01 — working environments and temporary state kept disappearing](#r01--working-environments-and-temporary-state-kept-disappearing)
5. [R02 — restricted outbound access repeatedly blocked the next step](#r02--restricted-outbound-access-repeatedly-blocked-the-next-step)
6. [R03 — workflow-start permission failures caused a repeated retry loop](#r03--workflow-start-permission-failures-caused-a-repeated-retry-loop)
7. [R04 — verification repeatedly required avoidable manual reconstruction](#r04--verification-repeatedly-required-avoidable-manual-reconstruction)
8. [R05 — each extension had to work around a frozen generator](#r05--each-extension-had-to-work-around-a-frozen-generator)
9. [R06 — one change repeatedly had to be synchronized across many files](#r06--one-change-repeatedly-had-to-be-synchronized-across-many-files)
10. [R07 — documentation repeatedly fell behind implementation](#r07--documentation-repeatedly-fell-behind-implementation)
11. [R08 — visual work repeatedly cycled through interpretation and revision](#r08--visual-work-repeatedly-cycled-through-interpretation-and-revision)
12. [R09 — faulty test assumptions repeatedly created extra debugging](#r09--faulty-test-assumptions-repeatedly-created-extra-debugging)
13. [R10 — browser checks repeatedly needed another context or state](#r10--browser-checks-repeatedly-needed-another-context-or-state)
14. [R11 — provider signals repeatedly failed to settle access claims](#r11--provider-signals-repeatedly-failed-to-settle-access-claims)
15. [How the recurring issues reinforced one another](#4-how-the-recurring-issues-reinforced-one-another)
16. [What changed after the fixes](#5-what-changed-after-the-fixes)
17. [Priority actions and proof that they work](#6-priority-actions-and-proof-that-they-work)
18. [One-off incidents and risks deliberately excluded](#7-one-off-incidents-and-risks-deliberately-excluded)
19. [Crosswalk to the earlier retrospective](#8-crosswalk-to-the-earlier-retrospective)
20. [Evidence index and limits](#9-evidence-index-and-limits)
21. [Final conclusions](#10-final-conclusions)

## 1. Scope and rules for inclusion

### 1.1 What counts as recurring

A problem qualifies here when the available record shows **at least two distinguishable manifestations of the same underlying barrier**, and those manifestations required extra recovery, investigation, synchronization, repeated interpretation or waiting.

There are three forms of recurrence:

- **Across stages or sessions:** for example, dependencies missing during the retrospective and preview tools disappearing later.
- **Repeated cost on separate changes:** for example, updating both content sources and rebuilding outputs for more than one content revision. This is a repeated workflow burden even if it never produced a shipped defect.
- **Clustered retries within one episode:** for example, several workflow-start attempts failing under the same inadequate effective permission. This is repeated obstruction, but not proof that the same failure happened across multiple releases.

The register labels these differences. It does not turn one prolonged episode into several unrelated outages.

For a structural constraint, the report requires repeated **actual accommodations**, not merely a prediction that the structure might cause trouble someday. The unchanged generator qualifies because the design port, creature integration and favicon work each needed a separate local adaptation. An unexercised security recommendation does not qualify merely because it sounds important.

### 1.2 What does not count

The following are not sufficient on their own:

- The same event being mentioned in three documents.
- Several error messages from one command being presented as independent incidents.
- A repeated word or a long-standing limitation with no evidence it repeatedly hindered work.
- A valid owner requirement that required engineering effort.
- An intentional approval gate or fixed session branch.
- An isolated bug, typo, library-install obstacle or mistaken command.
- A future risk discovered in the code but not yet observed causing repeated delay.

A problem can be an example within a qualifying family without becoming its own recurring issue. The single favicon-size mistake, for example, belongs to a repeated pattern of wrong test assumptions; it is not labelled a recurring favicon defect.

### 1.3 What “slowed work” means here

The record supports several types of cost:

1. **Recovery cost:** reinstalling tools, rebuilding files and restarting previews.
2. **Blocked-path cost:** switching tools or waiting for a person with the right permissions.
3. **Investigation cost:** separating product faults from environment, test or container faults.
4. **Propagation cost:** synchronizing content, outputs, documentation and tests.
5. **Review cost:** checking whether a claim or historical record is still applicable.
6. **Rework cost:** repeating a build or browser sweep after a correction.

Not all repeated work was avoidable. Validation, careful research and responding to legitimate feedback are part of doing the job. This report identifies the friction that multiplied that work; it does not declare every review cycle wasted time.

### 1.4 Evidence and honesty about time

Evidence is drawn from the repository, the first retrospective, the chronological engineering report and the recorded conversation summarized there. The plain-English report is a translation of the same history, not a second independent source proving an event happened twice.

Current source files were inspected for this report. Existing product tests and provider research were **not rerun**. Results quoted from the earlier audit retain that attribution. No failed dispatch or download was repeated just to recreate a known limitation.

There is no complete time-tracking log. The old retrospective estimates **10–20 minutes at the start of each session** for environment recovery. That is its historical estimate, not a newly measured average or a reliable basis for multiplying out a project-wide hour total. No total hours, financial loss or percentage of wasted effort is invented here.

### 1.5 Status labels

- **Substantially addressed:** a concrete mitigation exists and the record contains useful confirmation. This does not mean the underlying environment can never fail again.
- **Partly addressed:** some cost is removed, but part of the repeated burden remains.
- **Workaround, not removal:** a different route completed the task while the original restriction persisted.
- **Still present:** current source or the latest historical observation shows the mechanism remains.
- **Not rechecked here:** we have not reattempted the restricted operation or rerun its product test for this report.

## 2. Main findings

### 2.1 The central pattern

The project repeatedly paid for knowledge, tooling and assumptions that had not yet been made durable or executable.

At first, the right environment was something the assistant had to recreate. Verification was something the assistant remembered to do. Visual requirements were partly negotiated through successive screenshots. Research confidence lived in prose spread across files. Later, the project encoded much of that work into source files, commands, manifests and CI.

That improved reliability, but it did not remove every recurring burden. Outside access remained restricted. Provider terms remained ambiguous. The generator stayed intentionally immutable. Documentation still developed old claims alongside newer ones.

### 2.2 Eleven families, not eleven unrelated root causes

This report groups the recurring friction into **11 families**. They overlap causally. In particular:

- R01 makes R04 worse by erasing verification tools.
- R02 and R03 both block operations, but need different remedies: connectivity versus authorization.
- R05 and R06 increase the number of places touched by a change.
- R06 feeds R07 by giving documentation more facts to synchronize.
- R08 makes R04 more expensive because every additional visual round needs checking.
- R09 concerns incorrect assertions; R10 concerns missing states or execution contexts. They are not the same failure.
- R11 concerns what evidence actually establishes, even when access works. It is not just another network problem.

The same recovery or test run may appear in more than one explanation. **Do not add the issue counts or qualitative impact labels to calculate a total loss.**

### 2.3 The strongest repeated problems

The clearest cross-stage recurrence is:

1. Loss of temporary execution state and setup work.
2. Blocked external access across research, skill discovery and artifact retrieval.
3. Source/output/document synchronization.
4. Documentation drift, including drift returning after an explicit cleanup.
5. Repeated visual and testing refinement before a result could be accepted confidently.

The narrowest qualifying issue is R03: repeated permission failures clustered around dispatching the first link sweep. It is included because repeated attempts demonstrably failed and slowed that task. It is not described as a GitHub outage or a problem on every PR.

### 2.4 Fixes helped; they did not rewrite history

PR #3 substantially improved setup and verification. PR #4 made preview recovery durable. PR #5 let the owner complete a network-dependent task outside the sandbox. PR #7 added stronger state and interaction regressions. PR #8 added a narrow, tested favicon adapter.

The previous comprehensive audit recorded successful local checks and successful GitHub checks. Those results support the mitigations at that baseline. They do not prove that every stale sentence disappeared, that blocked integrations acquired new permissions, or that every phone was tested.

## 3. Recurring issue register

Impact priority is qualitative: how broadly the issue blocked or multiplied work. It is not a measured number of hours.

| ID | Repeated issue | Recurrence type | Strongest evidence anchors | Impact priority | Latest supported status |
|---|---|---|---|---|---|
| R01 | Environment/tools/temporary state disappearing | Across sessions and stages | Missing `docx`/Chromium; vanished reference copy; preview/cache/output reset | Highest recovery priority | Recovery substantially improved; resets still possible |
| R02 | Restricted outbound access | Across tasks and destinations | Provider curl; MCP POST; redirected log/artifact download | High blocking priority | Workarounds, restriction not removed |
| R03 | Actions dispatch permission retries | Clustered repeats in one episode | Reconnect and alternate-token attempts still returned 403 | High within the sweep task | Owner dispatch worked; original permission path not fixed |
| R04 | Manual recreation/orchestration of verification | Across early changes and recovery cycles | Scratch browser tools; multi-command rebuilds; repeated full sweeps | High multiplier | Substantially improved; full local coverage still needs several commands |
| R05 | Local workarounds around the frozen generator | Separate extension tasks | Branding/CSS port; Pals injection; favicon validation adapter | Medium/high integration burden | Guarded, not eliminated |
| R06 | Multi-file content/output synchronization | Separate content and artifact revisions | Original dual sources; sweep refresh; playlist/card change | High propagation burden | Drift/count checks help; duplicated prose remains |
| R07 | Current instructions/claims becoming stale | Before and after doc cleanup | Tag-color/setup drift; later card/layer/favicon prose | High review/trust burden | Still present in inspected documents |
| R08 | Visual interpretation/refinement loops | Four original rounds and later feedback | Hero/gutters/type/chips; Pals size; mobile h1 revision | Medium/high rework multiplier | Current spec and measured checks help |
| R09 | Tests encoding the wrong assumption | Distinct feature stages | Repeat-hue rule; synchronous-scroll timing; SVG natural size | Medium debugging burden | Known mistakes corrected; test-review discipline still needed |
| R10 | One browser setup/state not answering the user question | Different layouts and contexts | Expanded-only state; live mobile scroll feedback; embedded-link investigation | Medium/high investigation burden | Coverage expanded; real-device/context limits remain |
| R11 | Weak/ambiguous provider signals requiring repeated interpretation | Across providers and research rounds | Coursera/Alison distinctions; Jobberman partial; status/content mismatch | High research burden | Manifest/caveats help; gaps remain |

---

## R01 — working environments and temporary state kept disappearing

### The repeated pattern

Useful setup existed in temporary locations or installed state rather than in a fully reconstructible project. A new session or reset repeatedly removed pieces needed to continue the previous task.

The visible failures differed—missing import, missing browser, dead preview, missing reference clone, absent Pals—but the recurring dependency was the same: work relied on state that was not durable.

### Distinguishable manifestations

1. **Early development sessions:** the retrospective records repeated dependency reinstalls and Chromium extraction. The exact command-by-command sequence is not all preserved.
2. **Post-design diagnosis:** the five-test smoke suite encountered `ModuleNotFoundError: No module named 'docx'`, and `/tmp/chromium` was absent. This independently confirmed that earlier working installations were not present in the later session.
3. **Pals inspection:** the temporary Nature Photography clone was gone and had to be cloned again to inspect the actual engine/configuration.
4. **Preview recovery:** a reset removed `.venv`, `node_modules`, browser binaries, the process and a server script located in `tools/visual/.cache/`.
5. **Output identity:** the same reset behavior restored the committed older tracker from before Pals. Restarting a server was not sufficient; it could serve a valid but stale product.
6. **Later report audit:** a shallow checkout again needed full history fetched, and the audit recreated dependencies through bootstrap. These are reconstructive steps recorded in the first report, not additional product defects.

The initial PEP 668 install refusal was one incident. It is not counted as a recurring Python-policy failure. It matters here because repeated setup amplified the inconvenience of getting dependency installation right.

### Why it slowed work

- Work began with repair rather than the requested feature.
- A missing package could look like a code regression until diagnosed.
- A missing test harness required rebuilding the means of checking work.
- A live server could create false confidence while serving an older output.
- Temporary reference inspection had to be repeated instead of resumed.
- Session reconstruction made it harder to establish exactly which environment produced an artifact.

The historical 10–20-minute estimate belongs to the earlier retrospective. It should not be treated as a measured cost for every later recovery.

### Underlying mechanism

The sandbox has ephemeral process/runtime state and excludes common generated/cache directories from snapshots. Git's tracked-file rules and the sandbox's persistence rules are separate systems.

That distinction was particularly damaging for `learning-library/out/`: generated outputs are valid committed products, but uncommitted output changes were not a dependable snapshot store. A reset could bring back the committed old version.

### Fixes and their limits

**Implemented:** a project-vendored skill, fixed dependency list, private `.venv`, `make bootstrap`, committed browser harness and lock, durable standard-library preview server, rebuild-on-preview-start and a Pals marker warning.

**Observed improvement:** the history records a subsequent reset in which the durable preview path rebuilt the correct Pals output without another code repair. The first report's bootstrap and checks also completed successfully.

**Still true:** processes, venvs, npm installations, browser binaries and scratch copies can disappear. Bootstrap also currently keys on the venv executable existing, so it does not automatically repair every half-broken environment or react to every lock change.

**Next prevention:** treat installed state as disposable, keep recovery commands in tracked files, and verify served artifact identity—not merely that the port responds. Add an explicit environment-refresh mechanism before claiming bootstrap handles partial environments.

**Evidence:** E01, E03, E04, E05, E11.

## R02 — restricted outbound access repeatedly blocked the next step

### The repeated pattern

The sandbox could reach selected development hosts but not every host needed for the work. A normal-looking step—visit a provider, call a tool endpoint, fetch a browser, download an artifact—could fail because it crossed an access boundary.

This is a network capability issue. It is distinct from R03, where GitHub could be reached but the caller could not authorize a particular operation.

### Distinguishable manifestations

1. **Provider verification:** original shell curl attempts to course/provider sites failed, including the independently recorded OpenStax `000`/TLS error. The original broad sweep could not be completed locally.
2. **Skill discovery:** project MCP registration existed, but the endpoint's POST tools were inaccessible from the sandbox. Reading public catalog/source material became a separate fallback path.
3. **Browser tooling:** ordinary browser-download routes were not a dependable option. The lasting harness uses Chromium shipped through an allowed npm package, avoiding a separate download host.
4. **GitHub evidence retrieval:** reading run metadata worked, but logs and the link-sweep artifact redirected to hosts outside the outbound allowance. A successful GitHub upload did not mean the sandbox could download the uploaded file.

Provider-side rejection is not always caused by the sandbox. For example, a provider can filter bots independently. R11 covers the repeated work required to interpret those results. We do not attribute every 403, 500 or cookie wall to one firewall.

### Why it slowed work

- The intended tool had to be replaced with a different tool or environment.
- Normal shell checks could not establish results that a browser-like fetch might establish.
- A registered tool could not be treated as an executed tool.
- The report could confirm a run but not inspect all its raw evidence.
- The owner had to participate in obtaining results that normally could have been retrieved programmatically.
- More explanations and caveats were needed to prevent the workaround from becoming an inflated verification claim.

### Fixes and their limits

**Implemented/worked around:** fetched provider pages with a separate page-fetch service where possible; read skill instructions through allowed sources; ran the broad sweep in GitHub Actions; packaged Chromium through npm; used owner-pasted summaries and independent metadata when artifact download failed.

**Not fixed:** the sandbox's general egress policy was not removed. A public fetch succeeding does not prove shell or MCP POST access. An npm-based browser does not grant arbitrary browser-download or provider access.

**Current evidence limit:** no fresh attempt was made here to download the old TSV. The original raw-artifact limitation remains the appropriate description.

### Better handling

Before repeating a blocked step, identify whether the needed host, redirect target and HTTP method are supported. Keep a task-specific capability map: shell provider access, fetch-service access, MCP execution, GitHub metadata and GitHub artifact retrieval are separate capabilities.

Use a fallback after a justified diagnosis. Do not disable TLS verification or claim success from a different tool without stating the change of environment.

**Evidence:** E01, E04, E06, E12, E14.

## R03 — workflow-start permission failures caused a repeated retry loop

### The repeated pattern

The first link-sweep task encountered several failed attempts to start a GitHub Actions workflow. Reconnection and alternate token routes did not change the effective authorization.

**Recurrence boundary:** this is a documented cluster of retries within one task, not evidence of repeated Actions failures on every feature or a GitHub service outage. Successful push/PR checks elsewhere show that some Actions paths worked.

### Distinguishable attempts and observations

- The manual workflow-start path returned HTTP 403.
- The integration was reconnected and the operation tried again without a successful permission change.
- Both available `GH_TOKEN` and `GITHUB_TOKEN` routes were tried; the requested dispatch still failed.
- A diagnostic `repository_dispatch` was accepted, but no configured workflow listened for that event. It did not start the intended check and cannot be counted as successful dispatch.
- The owner eventually started the intended workflow from the GitHub interface. Run `40471064309` completed successfully.

The exact number and timings of every retry are not available. “Several failed routes/attempts” is supported; a made-up retry count is not.

### Why it slowed work

The same permission barrier was revisited without evidence that the relevant permission had changed. That delayed selecting the route that actually had the needed authority: the owner's manual workflow start.

The successful diagnostic event also needed interpretation. It proved that one event could be sent, not that the intended workflow had executed. Checking that difference required another round of investigation.

### Root cause and limits

The historical record identifies missing effective Actions-write authorization for the dispatch operation. Repository read access, git push capability and access to some GitHub APIs are not the same as the permission to start this workflow.

A reconnect might repair a broken connection, but it does not necessarily grant a new permission. Changing which environment variable supplies a token does not establish that the token has a different effective capability.

### What worked

The owner manually dispatched the intended workflow, and its metadata confirmed success. The owner pasted the result summary when artifact retrieval was separately blocked by R02.

That completed the task. It did not repair the original integration permission path, and this report has not retested that path.

### Better handling

Use an explicit retry stop rule:

1. Confirm the operation and non-sensitive error.
2. Check whether authorization or configuration has actually changed.
3. Retry only when there is a reason the outcome may differ.
4. Otherwise move to the authorized fallback and record who triggered it.
5. Verify an actual workflow run exists; never equate event acceptance with execution.

Do not request private tokens or authentication secrets in chat. The user's normal approval and account-control boundaries are safeguards, not the recurring issue.

**Evidence:** E06, E12; first sweep run linked in E15.

## R04 — verification repeatedly required avoidable manual reconstruction

### The repeated pattern

Early checks depended on personal command sequences and scratch tools rather than a complete, version-controlled verification entry point. Each change or recovery could require reconstructing how to prove the result.

The issue is **not that tests were run repeatedly**. Running tests after changes is necessary. The issue is repeated manual preparation, orchestration and interpretation that the repository could have supplied.

### Distinguishable manifestations

1. **Initial generation/design:** build and validation involved several separately documented commands; the early browser sweeps were run from a scratch setup outside the repository.
2. **Successive design rounds:** each small style change needed another build, relevant validators and a 13-width check, with the operator managing the sequence.
3. **Fresh-session diagnosis:** the scratch browser setup was absent. Prior “checked at 13 widths” claims did not come with a durable reproduction path in the repo.
4. **Early PR review:** PR #2 had no repository CI checks, so a reviewer could not use PR check status to reproduce the project's custom extension coverage.
5. **Later recovery:** even after command automation improved, resets still required recreating the executable environment before the durable checks could run; R01 increased the cost until preview and browser paths were hardened.

The last point is shared cost with R01, not another independent outage.

### Why it slowed work

- More opportunities to omit one part of the sequence.
- Repeated command reconstruction and dependency diagnosis.
- Verification claims tied to an earlier operator/session rather than a reproducible artifact.
- Reviewers having to trust prose instead of inspecting durable assertions.
- Unclear distinctions between the supplied skill's tests and the project's own theme/adapter behavior.

### What changed

PR #3 added `Makefile`, `tools/check.py`, output drift, contract checks, source checks, the committed browser harness and `verify.yml`. Later changes added Pals, deployment, click, scroll, legacy-state and favicon checks.

The first report recorded 9 fast passes, 1 known research warning, drift success, five repository tests, five borrowed tests and 13 successful browser widths. These are **earlier audit results**, not newly run results for this report.

### Remaining friction

`make ci` runs fast checks and drift. It does not run every step in GitHub's workflow: repository test discovery and `make check-visual` are separate. Even the Makefile comment describing `ci` broadly needs to be read with the actual workflow.

That is a remaining orchestration inconsistency, not evidence a particular later release skipped those tests. The earlier audit explicitly ran the separate commands.

### Better handling

Provide one accurately named full-verification command, or publish an unmistakable command sequence with separate fast/full scopes. Keep browser tools, expectations and reports reproducible. Record what ran for the current change, rather than carrying forward a generic “all tests passed” sentence.

Measure setup/recovery time separately from necessary test runtime before trying to optimize either.

**Evidence:** E01, E03, E05, E11, E13, E14.

## R05 — each extension had to work around a frozen generator

### The repeated pattern

The supplied skill had to remain byte-exact. That was an explicit and valid requirement. However, it had no project-specific extension interface for every requested change. New work repeatedly needed local post-processing, overrides or adapters around unchanged generated output.

This is repeated **integration friction**, not a claim the vendor repeatedly broke or that preserving it was a mistake.

### Distinguishable manifestations

1. **Design port:** the local builder replaced known pieces of generated HTML while a second stylesheet overrode the generator's visual rules.
2. **CSS behavior:** the generator's `.hero p` rule beat a plain `.eyebrow` rule for both color/margin-related behavior. Reading the intended local declaration was not enough; computed styles and stronger selectors were needed.
3. **Card-footer layout:** the generator's link nesting and sibling completion label meant the requested left/right bottom alignment had to be achieved with local layout rules rather than a direct template edit.
4. **Pals:** adding a real engine required three additional injection anchors, an inert template, a local controller and re-anchoring after the generator rebuilt stage nodes.
5. **Saved progress insertion:** the new first card required a guarded rewrite of the generator's positional-key function to preserve old meaning. This is one compatibility incident within the repeated adapter workload, not evidence of repeated saved-data loss.
6. **Favicon:** the unchanged validator rejected all link tags. A local exact-tag exception and temporary validation copy were needed to satisfy both the icon request and the original boundary.

### Why it slowed work

Each feature had two questions: how should the feature behave, and how can it be added without changing protected code?

The integration also had to be tested at the seam. A theme declaration could exist but lose in the cascade. An HTML anchor could disappear after an intentional vendor update. A stage rebuild could leave a creature pointing at an old node. A safe favicon could still violate a broad validation rule.

These are concrete reasons for the extra contracts, count checks, payload pins and browser assertions. They are not proof every hypothetical vendor upgrade has already failed.

### Implemented protection

The project now has eight branding anchors, three Pals anchors, a required head insertion point, a guarded key-function shim, exact vendor hashes, a pinned Pals payload and a pinned favicon tag.

Contract tests deliberately break expected anchors. Browser tests inspect actual styles and interactions. The favicon exception is narrow: it removes only the one exact approved tag from a temporary checking copy and leaves the delivered file intact.

### Remaining mechanism

The wrapper still depends on generator internals. General substitutions use `count=1`; not every duplicate-anchor condition is rejected uniformly. CSS still overlays a second styling system. Future work can require another adapter.

Current tests make those dependencies more visible; they do not turn the generator into a general plugin system.

### Better handling

Document the extension seams as a versioned local interface. Route changes through the wrapper and theme. Where possible, normalize a small piece of generated structure once rather than adding unrelated overrides indefinitely. On an intentional vendor upgrade, review each seam deliberately.

Do not edit the protected skill, weaken self-containment or repin unknown bytes merely to make a check green. The owner's immutable-vendor requirement remains part of the solution boundary.

**Evidence:** E02, E03, E04, E07, E08, E10.

## R06 — one change repeatedly had to be synchronized across many files

### The repeated pattern

Learning facts lived in both long-form Markdown and tracker JSON. Finished outputs were committed. Verification metadata, link scripts, hero facts, browser expectations and current documentation also depended on those facts.

As a result, one conceptual change repeatedly had a larger edit-and-check footprint than its visible size suggested.

### Distinguishable manifestations

1. **Original library:** stage/card/URL information was entered in two source representations, then delivered in five formats. The retrospective measured 21 card URLs duplicated across the sources at that time.
2. **Verification maintenance:** the original date was measured as appearing 153 times across nine files. That is a historical snapshot showing propagation load, not a current file-count claim.
3. **First sweep refresh, PR #5:** provider findings changed, requiring manifest and prose updates, output regeneration and documentation/comment updates.
4. **Playlist/card update, PR #7:** adding one starter card required coordinated JSON/Markdown changes, rebuilt outputs, changed card expectations and safe progress labels. It also required preserving the old sweep's URL set rather than changing history to match the present.
5. **Artifact review across builds:** PDF/DOCX timestamps and packaging details made ordinary binary comparisons less useful, so rebuild comparisons needed meaningful, format-specific methods.

### Why it slowed work

The difficult part was not always editing the card. It was identifying everything that represented the same fact, making the changes consistently and proving the finished files were not stale.

Counts were especially easy to confuse: the current product has 27 cards, 22 distinct card URLs and 31 verification entries; the old executed sweep has 30 URLs. Treating those as one universal “number of links” would make the record wrong.

This family is about repeated synchronization effort. It does not assert that progress was actually corrupted, the old sweep was falsified, or every content edit shipped stale output. Some of the work prevented those defects.

### What improved

- Cross-source checks compare stages, card counts, hours and URL relationships.
- Computed hero facts reduce some manual counting.
- Drift rebuilds all five outputs in a temporary directory.
- Text/HTML comparisons are exact; PDFs are compared by extracted text and DOCX by internal archive entries.
- The old HTTP sweep has its own frozen URL snapshot, separate from the current set.
- The new Stage 1 card has a dedicated key while existing Stage 1 keys keep their meaning.

### What remains

The two content sources are still authored separately. Count and URL agreement does not prove agreement of every explanation, cost qualification or next action. PDF text equality does not prove identical layout.

The persistent synchronization burden is visible in R07: even after checks were added, some current instructions still repeated old counts or behavior.

### Better handling

Use one structured content model to derive repeated representations where practical. Until then, compare more than counts: titles, providers, price/access classifications, study budgets, actions and caveats need deliberate checks.

Keep present-day content distinct from historical evidence. A new playlist belongs in a new sweep, not in a rewritten old result. Review binaries through rendered or extracted content without calling timestamp-only changes new learning content.

**Evidence:** E01, E03, E06, E07, E09, E13.

## R07 — documentation repeatedly fell behind implementation

### The repeated pattern

Documentation was often expanded by adding a newer paragraph or dated subsection while older current-looking statements remained. Readers then had to reconstruct which statement still applied.

This pattern is particularly well supported because it was diagnosed and partially corrected in PR #3, then reappeared in later current instructions.

### Earlier manifestations

- The historical design document said only provider and cost tags were accented after the stylesheet had changed to color all tags.
- Generic skill installation instructions referred to personal/global locations, while this repository used a vendored project copy.
- Setup commands were spread across several documents and working directories, with inconsistent package-install caveats.
- Dated refinement sections served partly as a changing specification, making later overrides easy to miss.

These findings motivated the canonical setup guide, current design specification, historical labels and doc lint.

### Later manifestations visible in inspected files

- `docs/SETUP.md` still describes the content as 26 cards/21 URLs instead of the current 27/22.
- The same guide still describes `pals.css` as a fixed unclipped layer after the layer became document-positioned absolute.
- `learning-library/README.md` still contains earlier design prose saying a tab icon could not be copied because of validation, despite the later exact favicon exception.
- The design specification's opening blanket no-link rule requires reconciliation with its later favicon exception.
- The long-form “first hour” guidance remained out of step with the HR Essentials-first card order.
- The doc checker returned “no stale claims” while its actual implementation only checked selected phrases, paths and Make targets.

### What is not documentation drift

A changelog entry correctly saying the layer was fixed when PR #4 landed is historical evidence, not an error to erase. Likewise, the retrospective's 28-file/roughly-594KB snapshot and original 26-card count are legitimate when read with their original scope/date.

The problem is a statement presented as current, or an unqualified success message, disagreeing with current behavior. Confusing old but correctly dated history with stale instructions would create unnecessary rewriting and damage the audit trail.

### Why it slowed work

- Repeated source inspection was needed to settle apparently simple questions.
- New sessions could follow a valid-looking but obsolete instruction.
- Every change required finding and updating scattered prose.
- Reviewers had to interpret whether contradictory numbers were a mistake or a different historical scope.
- A green docs check could not be used as the broad assurance its wording implied.

### What worked and what did not

Separating `DESIGN-SPEC.md`, `CHANGELOG.md`, `SETUP.md` and historical records helped. The lint caught known patterns and broken references. Those improvements did not ensure all current prose changed with code.

The first report identified the contradictions rather than silently repairing them. This report also leaves those original files unchanged.

### Better handling

Treat current claims as owned data: designate a small canonical location, derive repeated counters/examples where possible and require an affected-document review for behavior changes.

Change checker output to describe its actual scope. Add explicit checks for current examples, but do not promise that regexes can prove every sentence is up to date. Retain properly labelled history.

**Evidence:** E01, E03, E09, E11, E13.

## R08 — visual work repeatedly cycled through interpretation and revision

### The repeated pattern

Appearance requirements often arrived as small visible changes. Their exact meaning or interaction with other rules had to be resolved through implementation, measured rendering and feedback.

The owner was entitled to refine the design. The recurring friction was the amplification of each change through coupled styles, unclear boundaries and the full build/check/document cycle—not the existence of feedback itself.

### Distinguishable cycles

1. **Initial refinements:** top bars, exact footer credit, dark eyebrow and card-footer link/checkbox alignment.
2. **Second round:** all tag colors, balanced stage margins, square markers, arrows and hero edge alignment.
3. **Third round:** smaller subtitle/fact chips, larger progress cards and separation of a shared rule so one component's scaling did not leak into another.
4. **Fourth round:** a larger h1, baseline-aligned stage headers, hidden visible reminder label and adjusted hero gaps.
5. **Pals review:** heading creatures that technically rendered at scale 2 were visually enlarged to scale 3 and retested.
6. **Production feedback:** the previously enlarged h1 was later reduced by 25% because it wrapped too much on mobile.

The repeated 40% instruction was applied once. The hero-gutter clarification meant cancelling a small sheet gap, not a viewport-wide breakout. These are examples of interpretation inside the recurring workflow, not separate recurring specification defects.

### Why it slowed work

A small visual delta could change layout at multiple widths, interaction space, creature placement and print behavior. Its cost included rebuilding, measuring actual styles, checking the 13-width matrix and updating records.

A shared CSS rule could multiply the effect beyond the intended component. The third round's split between chip and card rules is concrete evidence that component coupling mattered.

The later mobile title feedback also showed that “fits without overflow” was not identical to “reads well on a phone.” A technically passing geometry test did not settle all design preferences.

### What improved

Named tokens, a current design specification and computed-style/geometry checks made acceptance more explicit. The record now distinguishes one 40% increase from compounded increases and a later independent 25% reduction. The latest clamp and viewport results can be checked directly.

The Pals intake also improved requirement collection: tracker-only scope, real engine, ten placements from eight species and distributed placement were agreed before implementation.

### What remains

Visual evaluation still requires human judgment. The small chip text and visible-label choice are documented user-approved tradeoffs, not recurring mistakes that this report is authorized to reverse.

There is no basis to label all four rounds unnecessary or calculate a “wasted design percentage.” Some were new preference requests rather than failed execution.

### Better handling

Before implementation, translate visual requests into explicit acceptance examples: narrow/default-open layout, desktop layout, exact scope of “edge-to-edge,” preserved gaps and named components affected by scaling.

Batch related choices where the user prefers it, without bypassing their approval process. Keep tokens/component rules separate so an approved change to one element does not silently change another.

**Evidence:** E01, E02, E03, E04, E07.

## R09 — faulty test assumptions repeatedly created extra debugging

### The repeated pattern

At several feature stages, the product or proposed configuration was reasonable but a test encoded the wrong assumption. The failure then required testing the test, not immediately changing the delivered feature.

Three different examples establish recurrence. They do not mean the same test repeatedly failed after being fixed.

### Case 1: the repeated-sprite hue rule

The initial Pals check required a hue on the first appearance of a sprite that would later repeat. The intended rule was that additional appearances should be visually differentiated. The checker was narrowed to require hue only on subsequent occurrences.

**Extra work:** inspect whether config or assertion was wrong, correct the check and rerun it. The response was not to tint every first appearance merely to satisfy a mistaken rule.

### Case 2: synchronous scroll timing

The native-scroll regression initially observed zero movement because smooth scrolling had not happened synchronously. A no-movement result could not test the positioning hypothesis.

The test switched to instant scrolling, froze frame correction and added the fixed-layer control. That made the experiment answer the intended question: whether actors move natively with a 240px scroll.

**Extra work:** separate a timing problem in the experiment from the actual mobile-scroll problem, then rerun the regression with a meaningful control.

### Case 3: SVG natural dimensions

The favicon test initially assumed the reference SVG's 32-by-32 viewBox implied 32-by-32 natural dimensions. Chromium reported 150-by-150 because explicit dimensions were absent.

The artwork matched the requested exact reference. The test was corrected to draw it to a 32px canvas and inspect four colors.

**Extra work:** inspect SVG semantics, distinguish internal drawing coordinates from intrinsic image size, change the assertion and rerun browser checks. The exact requested tag was not altered to appease the test.

### Why the pattern matters

A red test can indicate:

- a product defect;
- an environment failure;
- a valid test of the wrong scenario;
- or an incorrect assertion.

Assuming the first answer every time can create product changes that satisfy the test while violating the requirement. The recorded fixes avoided that trap, but only after investigation.

### Mitigation and remaining need

The three known assumptions were corrected and the corresponding tests passed in the recorded work. The scroll control experiment and actual favicon decoding are particularly useful because they test observable mechanisms rather than convenient proxies.

For future tests, state the requirement, the mechanism being measured, allowed variation and why failure would mean the product is wrong. For timing-sensitive behavior, establish that the action happened before interpreting a measurement. For exact-copy assets, separate source fidelity from browser rendering assumptions.

This is a recurring testing-process issue, not a current claim that the suite remains broken.

**Evidence:** E04, E07, E08; recorded validation E13.

## R10 — browser checks repeatedly needed another context or state

### The repeated pattern

A result in one browser arrangement repeatedly failed to answer the whole user-facing question. The work then needed another state, input method, scroll experiment, container check or owner test.

Unlike R09, the problem here is often **scope**, not a mathematically wrong assertion. A check can be valid and still cover the wrong starting layout or a different execution context.

### Distinguishable manifestations

1. **Expanded-only visual checks:** the initial Pals visual setup opened all stages. Normal visitors start with only Stage 1 open. Separate default-state checks at 320/900/1440px were added.
2. **Mobile title usability:** earlier geometry checks passed, yet the owner later found excessive title wrapping on phones. No overflow is a narrower criterion than comfortable reading.
3. **Mobile scroll behavior:** a fixed decorative layer could render and pass static placement checks while lagging compositor-driven scrolling. A synchronous native-coupling regression and fixed-layer control were needed.
4. **Embedded-preview links:** the owner reported unclickable links, but all 27 links passed hit tests across 13 widths; mouse, touch and normal new-tab requests worked in the harness. The surrounding preview could differ from a standalone browser, but the actual cause remained unproven.
5. **YouTube destination versus playback:** readable playlist metadata and successful event activation did not establish video playback or phone-app handoff. Those were explicitly left outside the test claim.

Some examples overlap R08 or R09. They are shared evidence of why new tests were needed, not additional unrelated incident counts.

### Why it slowed work

The investigation repeatedly had to ask: are we testing the same state and environment in which the user sees the problem?

A static screenshot cannot settle scrolling. A click event reaching an anchor cannot settle external app handling. A direct top-level page does not prove an embedded container permits the same navigation. An all-expanded page does not represent the first view.

This required expanding coverage rather than simply rerunning an unchanged pass and dismissing feedback.

### What improved

The harness gained default-state measurements, all-link hit tests, trusted mouse/touch activation, an unsuppressed new-tab request, native scroll coupling and the old-state compatibility fixture. The owner later accepted the live PR #7 fixes.

No speculative navigation change was shipped for the preview problem. That restraint is part of the improvement: failure to reproduce did not justify inventing a cause or ignoring the report.

### Remaining boundary

The evidence does not include a complete physical-device/browser matrix, comprehensive assistive-technology testing, all mobile OS notification behavior or confirmed YouTube app playback. Owner acceptance is useful but does not specify every device and browser used.

These missing checks are residual scope limits. They are not themselves claimed as repeated observed failures.

### Better handling

Record the reproduction context early: live versus embedded preview, browser/device, open/collapsed state, input type and whether failure occurs before navigation, during navigation or inside an external app.

Build the smallest test that answers that specific question, then retain broad geometry coverage. Keep “event activated,” “new tab requested,” “destination loaded” and “video played” as separate outcomes.

**Evidence:** E03, E04, E07, E13, E14.

## R11 — provider signals repeatedly failed to settle access claims

### The repeated pattern

Research repeatedly reached a page, status or marketing statement that was too weak or ambiguous to settle the actual question: can this learner study the material free, what evidence of completion is free, and what remains paid or conditional?

This is different from R02. Even with successful connectivity, a 200 or “free” headline can leave the important question unanswered.

### Distinguishable manifestations

- **Coursera:** “Enroll for free” coexisted with FAQ conditions involving purchase, trial or a no-certificate route where available. Reading more, not just finding the button, was necessary.
- **Alison:** free study and a free Learner Record did not make the branded certificate free. The inspected policy did not establish an exact checkout price.
- **Jobberman:** only a cookie banner was readable; provider search-listing language could support a lead but not complete access terms. The partial status had to survive later checking.
- **LinkedIn:** the original help-page failure led to clearly unconfirmed secondary-source prices. Later curl 200 results did not resolve browser-like 403/500 failures or provide readable provider content.
- **OpenLearn/Saylor/NDPC sweep results:** three 403 replies required content rereads instead of declaring the pages dead. The fetch/curl discrepancy supported continued findings without revealing each provider's internal firewall behavior.
- **YouTube playlists:** titles and descriptions were readable while an error banner also appeared. Metadata access did not prove playback or app handoff.

The same provider uncertainty repeated in more than one research round in some cases, especially LinkedIn. Across the collection, different providers repeatedly required the same careful separation of weak signals from stronger claims.

### Why it slowed work

Each resource needed more than a working link. The work could include reading a FAQ, comparing policy wording, checking certificate conditions, preserving caveats and reopening an item after an HTTP discrepancy.

The honest outcome could remain “unclear.” Repeating a query does not guarantee an answer, and a broad “verified” label cannot replace missing evidence.

Some of this effort was unavoidable research quality, not wasted activity. The avoidable part was relying on coarse wording or duplicated notes that made qualifications harder to track consistently.

### What improved

The verification manifest separates content status and date from mechanical HTTP results. Paid/conditional items are marked. The sweep's older URL snapshot is preserved. Research freshness exposes unresolved gaps rather than silently hiding them.

The previous audit recorded 23 confirmed entries and eight open gaps across the remaining statuses, with zero confirmed entries older than 90 days. Those are the earlier audit's findings, not new reads for this report.

### Remaining weakness

The hero's `VERIFIED FREE` count is still based on cost strings not starting with `paid`, not on manifest confidence. This is a current model/wording weakness identified in the audit. It is **not counted as another historical incident or a separately proven recurring delay**.

The eight gaps are eight records, not eight repeated outages. “Bot filtering” and “login wall” in old notes must also be treated at the strength the available response evidence supports.

### Better handling

Separate study cost, certificate cost, trial conditions, account needs, region and evidence strength in structured fields. Record the exact page and date that support each claim. Stop once available tools cannot improve confidence; retain uncertainty and schedule a useful recheck rather than generating endless identical attempts.

**Evidence:** E01, E06, E07, E12, E16.

---

## 4. How the recurring issues reinforced one another

### 4.1 Recovery loop: R01 → R04 → R01

```text
Temporary environment disappears
    -> recreate dependencies/browser/preview
    -> reconstruct how to verify the current output
    -> rely on scratch state again if recovery is not saved
    -> next reset repeats the work
```

The durable bootstrap, harness and preview script break much of this loop. They do not stop resets; they stop a reset from requiring the same manual invention again.

The preview incident added a second condition: recovery must identify the output being served. Port reachability alone did not prove Pals were present.

### 4.2 Access loop: R02 + R03 → R11

```text
Research or automation path is blocked
    -> try another permitted tool or authorized operator
    -> receive metadata, summary, partial content or a different response
    -> interpret what that evidence actually proves
    -> retain uncertainty and schedule a useful follow-up
```

Connectivity, authorization and content confidence are separate gates:

| Gate | Question | Example |
|---|---|---|
| Connectivity | Can this environment reach the required destination/method? | MCP POST or artifact redirect blocked. |
| Authorization | Is this caller allowed to perform the reachable operation? | Workflow dispatch denied. |
| Relevance | Did the requested job/page actually run or load? | Accepted diagnostic event with no workflow listener. |
| Sufficiency | Does the result establish the intended claim? | 200 does not prove free course access. |

Confusing the gates encourages retries at the wrong layer. Reconnecting an account will not necessarily allow an outside redirect host. Reaching a provider will not necessarily clarify its certificate price.

### 4.3 Change-amplification loop: R05 + R06 + R08 → R04 + R07

```text
Visible or content change
    -> adapt generator output or CSS
    -> synchronize repeated source facts and outputs
    -> rerun contracts/format/browser checks
    -> update current instructions and dated history
    -> an overlooked old paragraph creates later reconstruction work
```

This explains why a small visible request had a larger work footprint. It does not prove the original requirement was unreasonable.

The best target for improvement is reducing unnecessary propagation and making acceptance explicit—not skipping tests or bypassing the owner's approvals.

### 4.4 Confidence loop: R09 + R10 + R11

A convenient proxy repeatedly looked close to the real question but was not identical to it:

| Proxy or partial observation | Actual question still needing an answer |
|---|---|
| Natural SVG dimensions | Does the exact requested artwork render correctly? |
| No synchronous scroll delta | Did the test actually scroll before measuring? |
| A page with all stages open | Does the normal first view work? |
| Click event reaches a link | Does the surrounding container allow the intended navigation? |
| Playlist names are readable | Does video playback/app handoff work on the device? |
| HTTP 200 | Is the intended content readable, and on what terms? |
| Cost text does not begin with “paid” | Is free study confirmed at the desired evidence strength? |
| Doc lint passes | Are all current claims actually current? |

Some rows are corrected historical assumptions; others are current evidence limits or a model weakness. They are not eight additional recurring issues. Together they explain why careful interpretation remained a repeated task.

### 4.5 Attribution without double-counting

A single preview recovery can demonstrate R01 and increase R04's work. A single content revision can demonstrate R06 and create R07 risk. Neither makes the recovery or revision happen twice.

Therefore this report provides a causal map and repeated manifestations, not an additive incident score. The underlying record is not detailed enough for a reliable project-wide cost accounting model.

## 5. What changed after the fixes

### 5.1 Change in operating conditions

| Stage | Before/trigger | Mitigation that landed | What the record actually supports |
|---|---|---|---|
| Initial library and design, PRs #1–#2 | Scratch environment, manual checks, duplicated sources, refinement loops | Vendored skill and local wrapper/theme | Working outputs, but recovery and repeatability still costly |
| Reproducibility, PR #3 | Diagnosis of eight early recurring issues | Lock/venv, Makefile, runner, contracts, source/drift checks, docs split, CI, committed browser harness | Recorded local and GitHub success; not proof all structural burdens vanished |
| Pals/preview, PR #4 | New adapter work, test-rule correction and repeated preview reset | Local Pals integration, added checks, durable preview and rebuild on start | Later reset recovery improved; old temp-only preview path replaced |
| Sweep, PR #5 | Dispatch permission failures and unavailable raw artifact | Owner dispatch, preserved result summary/metadata, content rereads and sweep record | Actual successful run; original dispatch permission and egress limits not removed |
| Mobile/playlists, PR #7 | New content propagation, mobile feedback, context investigations | Smaller title, direct playlists, protected keys, document-space Pals, expanded regressions | Tests plus owner live acceptance for the fixes; not a universal device matrix |
| Favicon, PR #8 | Immutable validator conflict and wrong natural-size test assumption | Exact-tag adapter, rejection tests, canvas-color test | Corrected checks passed; no later owner live-icon confirmation |
| Report audits | Historical/current prose conflicts and evidence reconstruction | Documented contradictions and limits | Better diagnosis, not implementation of the recommendations in these reports |

PR #6's hosting configuration is not separately listed as a recurring failure phase. It was a successful feature task. Its tests contribute to the verification system without establishing another repeated obstruction.

### 5.2 Status by mechanism

**Substantially reduced:** manual reconstruction of core checks; dependence on a cache-only preview script; reliance on a lost global skill copy; silent stale-output risk under normal drift checks.

**Still external or environment-bound:** sandbox egress restrictions and the recorded workflow-dispatch permission path. Workarounds completed tasks; they did not remove those restrictions.

**Still structural:** two authoring representations, generated-output review, immutable-generator seams and browser-context limits.

**Demonstrably returned after earlier cleanup:** current documentation drift. This is the strongest example of a mitigation that helped but was not sufficient to prevent recurrence.

**Known instances corrected:** Pals hue assertion, scroll timing experiment and favicon natural-size assertion. A need for better test reasoning remains, but the report does not imply these three exact bugs are still active.

### 5.3 Why green checks are compatible with this report

The prior audit's successful checks show that the measured contracts held. They do not imply no work was slowed earlier, nor do they guarantee every narrative claim is current.

A project can have correct current output and an expensive development workflow. Conversely, a smooth workflow would not prove provider prices are true. This report is about the repeated work barriers, not a claim that the entire product is broken.

## 6. Priority actions and proof that they work

These are proposed improvements to recurring mechanisms. **They were not implemented or tested as part of writing this report.** The role column suggests who should own the work; it does not assign obligations to a named person.

### 6.1 First priority: do not pay recovery costs twice

| Action | Recurring families | Suggested owner | Evidence needed before calling it complete |
|---|---|---|---|
| Keep a recovery path that works without disposable runtime state | R01/R04 | Build/tooling maintainer | Fresh supported environment can bootstrap and preview from tracked sources without hidden scratch dependencies |
| Make dependency refresh detect lock changes or incomplete installs | R01 | Build/tooling maintainer | Existing-but-incomplete venv and changed-lock scenarios repair intentionally; ordinary bootstrap output is not mistaken for a refresh |
| Verify artifact identity at preview start | R01/R06 | Preview/build maintainer | Expected version/markers are visible, and a deliberately old output is rebuilt or clearly rejected |
| Offer one accurately scoped full verification entry point | R04 | Tooling maintainer | Command includes repository tests, fast checks, drift and browser checks, or explicitly reports any omitted layer |

The existing `make preview` and committed harness already address much of the first and third rows. Improvements should build on them rather than replace working mechanisms gratuitously.

### 6.2 Second priority: reduce change propagation and stale claims

| Action | Recurring families | Suggested owner | Evidence needed before calling it complete |
|---|---|---|---|
| Establish a canonical structured learning model or stronger field comparisons | R06/R11 | Content/build maintainer | Deliberate divergence in title, cost/access caveat, action or provider is caught—not only changed counts/URLs |
| Keep historical evidence immutable and current data separately derived | R06/R07/R11 | Content/research maintainer | New URLs do not alter old sweep membership; a new result has its own date/snapshot |
| Consolidate current instructions and remove known contradictory current claims | R07 | Documentation maintainer | Setup counts/layer/icon wording agree with source, without rewriting correctly labelled history |
| Narrow doc-check success wording to its actual coverage | R07 | Verification maintainer | A deliberately stale current example is caught where covered; output does not promise universal absence of stale prose |
| Separate cost category from verification confidence | R06/R11 | Content/model maintainer | Partial/unconfirmed free-labelled entries cannot automatically inflate a “verified free” claim |

Stable resource IDs are useful when reducing model duplication, but do not claim this report proves repeated real progress corruption. The recorded Stage 1 compatibility risk was addressed before release.

### 6.3 Third priority: handle blocked operations deliberately

| Action | Recurring families | Suggested owner | Evidence needed before calling it complete |
|---|---|---|---|
| Record capabilities by tool, method and redirect path | R02 | Environment/tooling maintainer | The operator can distinguish allowed metadata reads from blocked artifact downloads and blocked MCP execution |
| Adopt a permission-retry stop rule | R03 | Workflow operator | After an unchanged denial, subsequent action is diagnosis or authorized fallback, not unexplained token swapping |
| Define a safe owner-assisted sweep procedure | R02/R03/R11 | Research/workflow maintainer | A result includes actual run ID, exact URL set, provenance and a clear statement if raw output is unavailable |
| Schedule meaningful provider rechecks instead of repeating low-value fetches | R11 | Research maintainer | A retry seeks new evidence or marks uncertainty; a status code alone cannot silently change a content claim |

There is no need to request secrets or weaken platform restrictions. A properly documented manual fallback can be the correct solution.

### 6.4 Fourth priority: reduce visual and test rework

| Action | Recurring families | Suggested owner | Evidence needed before calling it complete |
|---|---|---|---|
| Specify default-state and narrow-width acceptance before a visual round | R08/R10 | UI maintainer with owner input | Scope of gutters, component scaling and preserved spacing is written clearly enough to test |
| Review test assumptions separately from test implementation | R09 | Test author/reviewer | Each new assertion identifies the real requirement, measurement timing and permitted variation |
| Match reproduction context before changing code | R10 | UI/test maintainer | Device/browser/container/input and failure stage are recorded; event dispatch is not mistaken for destination success |
| Preserve extension-seam contracts during upgrades | R05 | Builder maintainer | Missing/changed seams fail clearly; protected sources stay unchanged unless the upgrade is deliberate |

A new design request is not itself a process failure. The goal is fewer preventable interpretation and cross-component side effects, not fewer opportunities for the owner to improve the product.

### 6.5 Measurements worth recording next time

No reliable baseline exists for total time loss. Future tracking could distinguish:

- Time to reach a ready environment after a reset.
- Number of recovery actions requiring a source change versus ordinary reinstall/rebuild.
- Time spent diagnosing environment/test/context versus actual product defects.
- Number of denied dispatch retries after the last meaningful permission change.
- Number of manually maintained representations touched by one content change.
- Stale current claims found after a release, distinct from valid historical statements.
- Verification setup time versus execution time.
- Visual revisions due to new preferences versus misinterpreted requirements.

These are proposed measurements, not numbers this report has already collected. They should not become a simplistic score that punishes necessary research or user feedback.

## 7. One-off incidents and risks deliberately excluded

All 32 rows of the engineering report's failure register and all eight early retrospective categories were reviewed. The 32 rows are categories in a historical register, not a proven count of distinct outages.

The following exclusions keep this report focused. This section records screening decisions, not additional recurring issue diagnoses.

| Candidate | Why it is not a standalone recurring issue here | Treatment |
|---|---|---|
| Initial transfer-bundle reconstruction | A one-time intake task; no evidence of repeated extraction failure | Background to R01, not a new issue |
| PEP 668 refusal | One recorded policy obstacle; repeated setup is the broader pattern | Example within R01 only |
| One branch-pointer mismatch | No evidence the same mismatch repeatedly disrupted work | Excluded as its own category |
| `gh pr edit` Projects Classic error | One recorded CLI/API compatibility incident | Excluded |
| Harness `EPIPE` from piping to `head` | One command-output mistake | Excluded |
| Preview HEAD mapping difference | One corrected route inconsistency, not repeated routing failure | Not elevated into a recurring server bug |
| One shadow mistake, one gutter clarification, repeated h1 wording | Individually isolated examples within several visual rounds | R08 pattern only; no three additional issues |
| The single new-card key migration | A prevented compatibility risk, not repeated user data loss | Relevant adapter/synchronization work under R05/R06 |
| Hue, scroll-timing and favicon-size mistakes | Each happened separately; the repeat is wrong test assumptions across tasks | Grouped as R09, not three recurring product bugs |
| Favicon validator rejection | One feature conflict within several immutable-generator extensions | R05, not “favicons keep breaking” |
| `repository_dispatch` with no listener | One diagnostic dead end inside repeated dispatch attempts | R03 context, not a separately recurring integration failure |
| Missing shared libraries | Environmental/tool packaging work; not evidence the app repeatedly crashed | R01/R04/R02 context only |
| Fixed-layer scroll and preview-link complaint | Different user-context investigations; no proof either was repeatedly broken after correction | R10 pattern; preview cause remains unknown |
| HTTP status/content discrepancy | Repeated across providers and rounds, not all one environment failure | R02/R11 distinction retained |
| Timestamp-only document differences | A repeated review/comparison burden, not recurring corrupted documents | R06/R04, with the comparison fix acknowledged |
| Missing accounts/cloud sync/closed-tab reminders | Intentional static-product scope, not observed recurring work failures | Excluded |
| Backup hardening, multi-tab races, CPU teardown, security scans, action SHA pinning | Important possible improvements without evidence of repeated historical delay from each | Not promoted into recurring issues |
| Small chips/hidden visible reminder label | Documented tradeoffs, not evidence of repeated unauthorized mistakes | No separate issue |
| Owner approval gates and the fixed session branch | Explicit operating rules | Not labelled hindrances to remove |
| Many historical session branches | Different sessions used their assigned branches | Not proof of recurring branch misuse |
| Correctly dated old counts or behavior in historical records | Legitimate history is not stale current guidance | Kept separate from R07 |

The earlier retrospective called repository hygiene a **latent** problem. This report does not treat that word as proof of recurrence. Concrete repeated effects—lost dependencies, external config dependence, ignored scratch tooling and reconstruction—are covered by R01/R04. Merely lacking an ignore file or seeing several branch names is not another independently repeated work barrier.

## 8. Crosswalk to the earlier retrospective

The earlier retrospective described the PR #1/#2 period. Its eight labels were useful for that point in the project, but later work provides more evidence and requires more precise status labels.

| Early category | Where the actual repeated mechanism appears here | Important update |
|---|---|---|
| Environment amnesia | R01, with verification effects in R04 | Durable bootstrap/harness helped; later preview reset exposed output-identity risk and prompted another fix |
| Verification as a manual ritual | R04 | Checks and CI now exist; do not repeat the old “no CI” statement as current |
| Outbound-network wall | R02; separate permission loop R03; evidence interpretation R11 | A real sweep ran outside the sandbox; raw artifact and MCP-execution limits were not erased |
| Brittle extension of frozen generator | R05 | Additional Pals/key/favicon seams demonstrate repeated accommodation, with explicit tests now guarding them |
| Multiple sources of truth and generated outputs | R06 | Drift/count checks exist, but dual authorship and prose synchronization remain |
| Append-only documentation drift | R07 | Current-looking stale claims reappeared after the cleanup; dated history must still remain intact |
| Design-by-screenshot churn | R08, with distinct testing/context lessons in R09/R10 | Current spec and explicit Pals intake help; feedback itself is not the defect |
| Repo hygiene/configuration, labelled latent | Concrete repeated consequences in R01/R04; otherwise excluded | No artificial recurring category for one-off branch desync or mere absence of config |

R09 and R10 are separated because later Pals, scroll, click and favicon work supplies distinct evidence that was not all available to the early retrospective. R11 separates content uncertainty from network access. R03 separates effective permission from connectivity.

This expansion changes the grouping, not the number of historical events. It is not valid to subtract eight from eleven and conclude there were exactly three newly recurring defects.

## 9. Evidence index and limits

### 9.1 Source index

Evidence identifiers refer to the records below. Local file links allow an engineer to inspect the code or prose behind the diagnosis.

| ID | Source | What it establishes | Limits |
|---|---|---|---|
| E01 | [Retrospective](../RETROSPECTIVE.md), §§2–3 and §6 | Independent early missing-dependency/browser diagnosis; early structural measurements; recorded recurring setup/design costs | Written for an older snapshot; estimates and conversation-derived events are not full time logs |
| E02 | [Historical design record](../learning-library/DESIGN-SYSTEM.md), requested/second/third/fourth refinements | Actual style-cascade issues, multiple refinement rounds, shared-rule separation and interpreted scope | Historical subsections must not be mistaken for final current values |
| E03 | [Changelog](../CHANGELOG.md), reproducibility and design sections; [engineering report §4.4](ENGINEERING-REPORT.md#44-retrospective-and-reproducibility-remediation) | What repeatability tooling landed and why; CI moved from unobserved to observed | Summaries of earlier work, not independent duplicate incidents |
| E04 | [Engineering report §§4.5–4.6](ENGINEERING-REPORT.md#45-pals-request-and-implementation); changelog Pals section | Vanished reference copy, hue-rule correction, size adjustment, repeated preview recovery and later improved recovery | Some actions survive as recorded conversation rather than raw command logs |
| E05 | [Makefile](../Makefile); [preview server](../tools/serve_preview.py) | Durable build/preview paths, venv target behavior, rebuild-before-serve, Pals warning | Source inspection establishes behavior; no fresh reset simulation for this report |
| E06 | [Engineering report §4.7](ENGINEERING-REPORT.md#47-url-sweep-dispatch-failures-and-first-real-result); changelog sweep section | Repeated permission attempts, owner dispatch, artifact-download limit and rereads | No exact retry-count log or downloaded raw TSV |
| E07 | [Engineering report §§4.9–4.10](ENGINEERING-REPORT.md#49-production-mobile-feedback), [§11.5](ENGINEERING-REPORT.md#115-scroll-regression-and-control-experiment); changelog mobile section | Mobile feedback, synchronization burden, scroll-test correction and click-context investigation | Headless events and owner acceptance are not a full real-device matrix |
| E08 | [Engineering report §15](ENGINEERING-REPORT.md#15-favicon-port-and-validation-exception), especially §15.4; [favicon tests](../tools/test_favicon.py) | Exact icon adapter and natural-dimension assumption corrected to rendered-color test | Historical successful browser execution, not a fresh live-icon check |
| E09 | [Setup guide](SETUP.md), editing/Pals sections; [library README](../learning-library/README.md), design section; [design specification](DESIGN-SPEC.md), opening and favicon sections; [content source](../learning-library/src/recruiter-talent-acquisition-library.md), “Your first hour” | Concrete current-looking claims requiring reconciliation with later implementation | Dated historical tables/entries are not automatically errors |
| E10 | [Tracker builder](../learning-library/tools/build_tracker.py); [theme](../learning-library/src/fieldnotes-theme.css); [Pals controller](../learning-library/src/pals/pals-controller.js) | Exact seams, local overrides, positional-key adapter and re-anchoring mechanism | Not evidence that every possible seam failure has already happened |
| E11 | [Check runner](../tools/check.py), especially `check_docs` and contract/source/drift checks; [verify workflow](../.github/workflows/verify.yml) | What is actually checked; limited doc-lint scope; separate workflow steps | A check's existence is not proof it ran for this reporting task |
| E12 | [Manifest](../learning-library/src/verification-manifest.json); [sweep script](../learning-library/check-links.sh); [link workflow](../.github/workflows/link-check.yml) | Current versus historical URL sets, content versus HTTP findings, schedule/report design | A schedule does not prove a later run occurred; content dates are historical |
| E13 | [Engineering report §16](ENGINEERING-REPORT.md#16-tests-ci-and-fresh-verification-results) | Earlier audit's actual successful checks and explicit limits, including manual stale-prose findings | Those tests were not rerun to write this recurring-issues report |
| E14 | [Browser harness](../tools/visual/visual_check.mjs) and [package settings](../tools/visual/package.json) | npm browser route, AL2023 extraction, default/expanded states, click/scroll/icon assertions | Linux/headless scope does not become full physical-device coverage |
| E15 | [Sweep run 40471064309](https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40471064309), as recorded in the manifest and prior audit | Successful owner-started workflow, 30-address summary and run provenance | Not re-queried here; raw rows unavailable locally in that audit |
| E16 | [Card JSON](../learning-library/src/roadmap-app.json), [long-form research](../learning-library/src/recruiter-talent-acquisition-library.md), [manifest](../learning-library/src/verification-manifest.json) | Provider-specific access distinctions, partial findings and caveats | Public-page findings are not logged-in enrolment or price revalidation today |

### 9.2 What was done for this report

- Read the earlier retrospective and both comprehensive reports where relevant.
- Inspect current Makefile, builder, preview server, checker, workflow, browser harness, content/manifest and affected documentation.
- Compare historical diagnoses with actual remaining mechanisms.
- Review the 32-row incident register to avoid promoting isolated problems into recurring issues.
- Separate recurrence across stages from clustered dispatch retries and continuous synchronization burden.
- Preserve uncertainty about elapsed time, raw sweep evidence, provider filtering and the embedded preview's behavior.
- Save this new report separately; leave application files and both prior reports unchanged.

The skill catalog was consulted for this task as requested in the standing workflow. No clearly applicable retrospective-specific skill was selected or executed. Catalog access is not a claim of successful MCP tool execution.

### 9.3 What was not done

No product implementation was changed, no provider research was refreshed, no blocked operation was retried, no live site or hosting account was inspected, no application test suite was rerun, and no commit/push/PR was authorized or performed.

Document checks—links, expected sections and unchanged-input fingerprints—are not product regression tests. If those document checks pass, that says nothing new about provider access or runtime browser behavior.

### 9.4 Confidence by type of statement

- **Strongest:** current file contents; the source of a stale instruction; actual adapter structure; test coverage visible in code; previously recorded concrete command results.
- **Supported historical account:** repeated early reinstallations, branch recovery context, order of preview retries, individual dispatch attempts whose raw transcripts are not all preserved.
- **Qualified interpretation:** bot filtering, login-wall explanations, relative time impact and suspected embedded-container restrictions.
- **Recommendations only:** proposed one-command full verification, improved content schema, stronger doc rules, retry stop policy and future measurements.

No confidence label converts one incident repeated in several reports into several incidents. Evidence strength and recurrence count are different questions.

## 10. Final conclusions

The most consequential recurring burden was **reconstructing a trustworthy working context**: tools, generated files, instructions and the meaning of test/research results.

The practical progress was to move that context into durable sources and checks. The project now retains the skill, dependency versions, preview script, browser harness, extension contracts, output comparisons and research-status records. Those changes meaningfully reduced repeated recovery and review work.

Three limits remain central:

1. **External limits:** network access, effective integration permissions and provider access conditions cannot be solved merely by repeating the same request.
2. **Structural limits:** an immutable generator plus duplicated content and committed outputs continues to require careful adapters and synchronization.
3. **Evidence limits:** passing one test, reading one page or receiving one status code does not automatically answer a broader user-facing question.

Documentation drift is the clearest recurring issue that returned after an explicit mitigation. It deserves ongoing ownership rather than another one-time cleanup.

The lesson is not “avoid tests,” “avoid feedback” or “remove approvals.” It is: **make recovery repeatable, make scope explicit, reduce duplicated facts, stop unproductive retries and state exactly what each piece of evidence proves.**

**End of report.**
