# FieldNotes-HR — comprehensive engineering history, architecture and handover

**Prepared:** 1 November 2026 (Africa/Lagos).  
**Audience:** engineers maintaining the content pipeline, browser application, verification tooling and deployment.  
**Audited product baseline:** `765f2e2b672e7ae04a0137133c2028d48cb70357` (merge of PR #8).  
**Report workspace:** `arena/8c02879a-fieldnotes-hr`.  
**Repository:** <https://github.com/MikkoWuyin-dev/FieldNotes-HR>.  
**Production address supplied by the owner:** <https://fieldnotes-hr.vercel.app/>.

> This is a retrospective and technical handover, not a new release. No product implementation, production setting or research finding was changed to prepare it. The application and generated artifacts discussed here are the PR #8 baseline. Read the limitations and evidence distinctions before interpreting any “verified” statement.

## Contents

1. [Scope, evidence and dates](#1-scope-evidence-and-dates)
2. [Executive engineering summary](#2-executive-engineering-summary)
3. [Original brief and operating constraints](#3-original-brief-and-operating-constraints)
4. [Chronological reconstruction](#4-chronological-reconstruction)
5. [Repository architecture and ownership boundaries](#5-repository-architecture-and-ownership-boundaries)
6. [Learning content, research and access claims](#6-learning-content-research-and-access-claims)
7. [Skill provenance and discovery](#7-skill-provenance-and-discovery)
8. [Generation and reproducibility](#8-generation-and-reproducibility)
9. [Browser runtime and persistence](#9-browser-runtime-and-persistence)
10. [Design-system port and visual evolution](#10-design-system-port-and-visual-evolution)
11. [Piixpal integration and scroll repair](#11-piixpal-integration-and-scroll-repair)
12. [Link-sweep execution and evidence limits](#12-link-sweep-execution-and-evidence-limits)
13. [Preview infrastructure and sandbox recovery](#13-preview-infrastructure-and-sandbox-recovery)
14. [Deployment architecture and production feedback](#14-deployment-architecture-and-production-feedback)
15. [Favicon port and validation exception](#15-favicon-port-and-validation-exception)
16. [Tests, CI and fresh verification results](#16-tests-ci-and-fresh-verification-results)
17. [Security, privacy, accessibility and performance](#17-security-privacy-accessibility-and-performance)
18. [Failure register and abandoned approaches](#18-failure-register-and-abandoned-approaches)
19. [Known debt and prioritized recommendations](#19-known-debt-and-prioritized-recommendations)
20. [Maintenance, release and incident runbooks](#20-maintenance-release-and-incident-runbooks)
21. [Work deliberately not done](#21-work-deliberately-not-done)
22. [Evidence and source index](#22-evidence-and-source-index)
23. [Appendix A — PR and commit ledger](#appendix-a--pr-and-commit-ledger)
24. [Appendix B — complete current roadmap catalog](#appendix-b--complete-current-roadmap-catalog)
25. [Appendix C — all URL verification records](#appendix-c--all-url-verification-records)
26. [Appendix D — artifact measurements and file inventory](#appendix-d--artifact-measurements-and-file-inventory)
27. [Appendix E — acceptance and decision ledger](#appendix-e--acceptance-and-decision-ledger)

---

## 1. Scope, evidence and dates

### 1.1 What “everything” means in this report

This report covers the available conversation history, the complete reachable Git history, all eight merged pull requests, the source files, the generated outputs, historical verification records, the manually dispatched URL-sweep result, owner feedback from the live deployment, and fresh checks run during this audit. It includes unsuccessful attempts and operational friction, not just the final successful architecture.

No finite audit can establish unrecorded activity. Some early actions survive only in the conversation's session summary and repository retrospective rather than individual command transcripts or commits. Such actions are described as historical records, not freshly repeated experiments. Temporary screenshots, original upload bundles and external scratch directories are not assumed to survive.

### 1.2 Evidence classes

| Class | Meaning | Examples |
|---|---|---|
| **Current source inspection** | Directly observable at the audited commit | JSON fields, CSS clamp, key mapping, reminder implementation, workflow configuration |
| **Fresh local verification** | Executed while preparing this report | `make ci`, five repository tests, Chromium harness, artifact hashes |
| **Git/GitHub evidence** | Queried from history or API during the audit | Commit graph, PR merge status, check-run conclusions, sweep run metadata |
| **Historical execution evidence** | Recorded earlier in the conversation, retrospective or changelog | PEP 668 failure, scratch-tool loss, original design measurements, failed dispatch attempts |
| **Owner production confirmation** | Owner tested the actual deployed site | “I've verified the fixes. All work as intended” after the mobile/playlist/Pals release |
| **Inference or recommendation** | Reasoned interpretation, not an established observation | Embedded-preview popup restrictions as a suspected cause; future browser compatibility risks |

A successful CI job does not prove every claim in its documentation. A successful URL request does not prove the returned page is the requested content, freely accessible, or correctly priced. A headless test is not a substitute for a physical phone.

### 1.3 Time discipline

Implementation commits and PR merges are dated **26–27 October 2026**. This report is prepared **1 November 2026**. PR dates in Appendix A use GitHub's UTC `mergedAt`; local time in Lagos is UTC+1. Git commit metadata contains mixed offsets, so raw timestamps are not silently treated as the same timezone. A one-second difference between a Git merge commit timestamp and GitHub's recorded merge time is not a separate event.

The resource research dates remain historical dates, primarily 26 October, with selected re-reads and playlist additions on 27 October. This report does **not** refresh provider research to 1 November. Likewise, an old generated “verified” banner is not a claim of continuous verification.

### 1.4 Audit boundaries

The working tree started clean on the report branch. The shallow checkout was expanded with `git fetch --unshallow origin` to recover actual history. Dependencies were recreated using the repository bootstrap. Only this report is intended as the new deliverable; no commit, push, deployment or PR is authorized by the reporting request.

No tokens, passwords, authorization headers, signed artifact download URLs or personal authentication material are reproduced. The production URL is the owner's supplied address; this audit does not constitute a fresh production browsing, deployment-account or DNS inspection.

## 2. Executive engineering summary

FieldNotes-HR is two products delivered from one repository:

1. A researched HR/Recruiter/Talent Acquisition learning library in Markdown, PDF, DOCX and static HTML.
2. A single-file, browser-local interactive roadmap tracker with the same stage/resource structure, a ported Fieldnotes visual system, optional pixel creatures and an inline favicon.

The first version contained **8 stages, 26 cards, 21 distinct card URLs and 94 estimated hours**. Production feedback added an HR Essentials playlist and replaced a channel destination with the actual Talent Acquisition playlist. The current version has **8 stages, 27 cards, 22 distinct card URLs and the same 94-hour study budget**. There are **31 current URL-check entries**, because the verification universe also contains supporting policy pages and optional extras. The first executed HTTP sweep checked an older **30-URL** snapshot.

The deployed runtime has no project backend, accounts, database, synchronization service, analytics implementation, external font dependency or required runtime package installation. The tracker is **166,050 bytes** at the audited commit, including all CSS, JavaScript, Piixpal scripts and the SVG favicon. A normal resource click deliberately navigates out to a provider; “no network calls” refers to autonomous application dependencies, not to user-requested external navigation or the host's own delivery infrastructure.

The dominant engineering work was not writing a frontend framework application. It was preserving an immutable, user-supplied generator while extending its output, making those extensions reproducible, encoding verification into the repository, and distinguishing environmental failures from product defects.

The project progressed through eight merged PRs:

- #1: learning library and vendored skill.
- #2: Nature Photography design-system port and iterative refinements.
- #3: retrospective, pinned environment, verification runner, CI and browser harness.
- #4: ten Piixpal creatures and durable preview setup.
- #5: first URL-sweep findings and regenerated library.
- #6: static deployment configuration.
- #7: mobile typography, correct playlists, progress compatibility and Pals scroll repair.
- #8: matching favicon with a narrowly pinned validation exception.

Fresh audit results: **9 fast checks passed, 1 research-freshness warning, 0 failures**; five outputs reproduce under their defined comparison methods; five repository unit-test methods pass; the five vendored renderer tests pass; Chromium passes 13 widths and three default-state checks, including native scroll coupling, legacy saved progress, playlist input activation and favicon colour rendering.

The main remaining risks are content/model duplication, string-anchor coupling to a frozen generator, misleading aggregate “verified free” wording, incomplete browser/device coverage, stale historical prose, permissive backup input validation, and a development environment whose network/permission constraints prevent some otherwise normal operations.

## 3. Original brief and operating constraints

### 3.1 Learner and deliverables

The learner was an absolute beginner in Lagos, Nigeria, entering HR through recruitment and talent acquisition. Intake selected:

- A **free-first** plan rather than a paid-only or indiscriminately mixed catalog.
- A balanced combination of video, official documentation and written courses.
- A new custom roadmap, not a resource dump organized by provider or media type.
- Approximately five study hours per week.
- All supported outputs: Markdown, PDF, DOCX, static HTML and interactive HTML.

The organizing principle was roadmap-first: develop HR orientation, fair-process foundations, role definition, sourcing, screening, structured interviewing, Nigerian legal/offer awareness, then tools, metrics and portfolio evidence. The plan must not imply guaranteed employment, professional licensing or mastery.

### 3.2 Research truthfulness

The user repeatedly required honest reporting of checks not run. Provider pages, not search-result summaries, were the basis for confirming access claims. Free learning, free completion evidence, paid branded certificates, and professional qualifications had to remain distinct. Prices could not be invented or silently converted into local currency. Provider ambiguity had to be retained rather than resolved optimistically.

### 3.3 Immutable skill and source-driven output

The supplied `resource-learning-library` skill had to persist in the repository and remain byte-exact. Appearance changes had to live in source/build files, with outputs regenerated. Editing only the output HTML was explicitly rejected as a maintenance strategy.

This constraint explains both the architecture and its compromises: repository-local Python wraps the unmodified generator; CSS overrides are appended; exact generated anchors are transformed; compatibility code is injected locally rather than editing the vendored JavaScript template.

### 3.4 Approval and Git workflow

The user introduced a standing instruction: acknowledge understanding and wait for a go-ahead before executing changes, unless the request itself authorizes them. The conversation consequently includes separate understanding, inspection, implementation and commit/merge authorizations.

An earlier “do not commit/push yet” was later explicitly reversed. Commits, pushes, PR creation and merges occurred on explicit instructions. Each development session used its assigned `arena/...` branch; it was not legitimate to silently switch work to `main`. Merge operations preserved history using `gh pr merge <number> --merge`. PRs were checked for state, expected refs and CI before merging, and the result was confirmed against GitHub and remote `main`.

### 3.5 Design authority and deliberate choices

The owner selected `MikkoWuyin-dev/Field-Notes_Nature-Photography` as the visual source of truth. The HR app was not meant to become a wholly new aesthetic. It inherited the navy frame, cream paper, vivid accents, monospace interface chrome, hard shadows and square corners, then followed owner-specific adjustments described in Section 10.

Later decisions explicitly selected tracker-only Pals, the actual Piixpal engine, ten placements rather than ten newly invented species, and distribution down the page rather than a single decorative strip.

## 4. Chronological reconstruction

### 4.1 Initial skill intake and reconstruction

The starting artifact was a portable Markdown transfer bundle, historically located at `/tmp/arena-coding-uploads/resource-learning-library-transfer.md`. An extraction script reconstructed 12 files from fenced blocks. Declared byte counts and SHA-256 digests were checked before execution. A personal/global skill copy initially supported discovery; the lasting fix was to vendor the bundle into `.agents/skills/resource-learning-library/`.

The generator dependencies were `python-docx`, `reportlab` and `pypdf`. A plain system `pip install` encountered PEP 668's externally-managed-environment restriction. Early sessions used virtual environments and, historically, a system-wide `--break-system-packages` workaround. That workaround is **not** the current setup procedure.

The supplied renderer was smoke-tested. Research and learner intake then produced Markdown content and structured JSON; all five output formats were generated and validated. PR #1 committed the skill and library, then merged into `main`.

### 4.2 Research and initial outputs

Provider exploration used web search as lead generation and page fetching for actual findings. The original resource library was approximately 6,829 words, with a 15-page PDF. It distinguished free Saylor completion certificates, OpenLearn participation statements, Alison's paid branded certificate and free Learner Record, and CIPM's paid professional route.

Coursera's marketing “Enroll for free” did not override a contradictory access FAQ. Jobberman remained partial because only a cookie banner could be read. LinkedIn pricing remained explicitly third-party/unconfirmed when help pages failed. The initial HTTP sweep could not run against provider domains from the sandbox, and that limitation was disclosed rather than hidden.

### 4.3 Design-system port

The reference repository was cloned and inspected. Its CSS custom properties and component language were ported into `fieldnotes-theme.css`; `build_tracker.py` became the repository-local wrapper. The original tracker functionality remained in the vendored generator.

Project-scoped MCP discovery was configured for `skill-issue`. The HTTP endpoint's POST tools were inaccessible from the sandbox, so relevant skill sources and linked guidelines were obtained through available web fetching and the GitHub API. The record includes installation of Claude Code for MCP registration work; the CLI itself is not a committed application dependency.

A scratch Puppeteer/Chromium harness outside the repository measured styles and geometry at 13 widths. Four rounds of refinements followed. A local/remote branch-pointer mismatch was resolved by fetching and using a mixed reset to the fetched remote while preserving working changes. The final design work landed in PR #2.

### 4.4 Retrospective and reproducibility remediation

After PR #2, a read-only diagnosis found a shallow clone, absent dependencies, missing Chromium, no CI, no root ignore policy, duplicated sources, fragile anchors and stale documentation. A missing `docx` import reproduced the environment problem independently.

`RETROSPECTIVE.md` named eight recurring causes. In its original order these were **environment amnesia; verification as a manual ritual rather than a repo asset; the outbound-network wall; brittle extension of a frozen generator; multiple sources of truth with committed generated artifacts; append-only documentation drift; design-by-screenshot churn; and repository hygiene/configuration**. The user requested implementing the fixes sequentially. The resulting work added the lock, Makefile, single check runner, hash inventory, source consistency checks, research manifest/freshness warning, output drift comparisons, current design specification, setup guide, CI, PR checklist, durable browser harness, ignore policy and binary attributes.

The builder exposed `branding_edits()` for contract tests without changing the tracker bytes. Clean bootstrap and fresh-clone simulations were recorded historically. CI then passed on push and PR; a follow-up commit corrected documentation from “unobserved CI” to observed success. PR #3 merged both commits.

### 4.5 Pals request and implementation

The owner requested ten decorative “Pals,” as in the reference. The reference clone had vanished, so it was cloned again outside the product repository. Inspection established eight sprite species and a then-current reference configuration of 14 placements. The reference's older audit text mentioned eight creatures, demonstrating why source inspection mattered more than one historical prose paragraph.

Four intake decisions chose:

1. Interactive tracker only.
2. The real Piixpal engine, not CSS/SVG lookalikes.
3. Ten placements using eight species, with repeats differentiated by hue.
4. Distribution throughout the page.

The engine's inert template, core and eight sprite scripts were copied, and the upstream MIT license was fetched. New placement/configuration, CSS and controller files were created. Static checks and browser checks were extended. The first `make check` exposed an overly strict repeated-sprite rule requiring a hue even on the first appearance; it was corrected so only subsequent occurrences require a hue.

Stage-heading creatures were initially tested at scale 2, then increased to scale 3 after visual review and another successful suite. Screenshots were scratch artifacts, not committed product assets.

### 4.6 Repeated preview recovery

The tracker was opened via a temporary Python server at port 8000. A root GET mapped to `roadmap-app.html`; HEAD initially still returned the directory listing and was subsequently aligned with GET.

Sandbox resets then killed the process, removed `.venv`, `node_modules`, browser binaries and the `.cache` server script. More importantly, snapshot-excluded `out/` restored the **committed old tracker**, so simply restarting could serve a healthy-looking application without Pals.

The fix moved the server into durable `tools/serve_preview.py` and added stdlib-only `make preview`, which regenerates the tracker before serving. A warning detects a missing Pals payload. A subsequent reset demonstrated that the durable tooling survived and restored the exact Pals build without new code repairs. The user then authorized commit/push/PR; PR #4 included Pals and preview recovery.

### 4.7 URL-sweep dispatch failures and first real result

Manual workflow dispatch repeatedly failed with HTTP 403 under the integration tokens. Reconnecting the GitHub integration and trying both `GH_TOKEN` and `GITHUB_TOKEN` did not change the result. A diagnostic `repository_dispatch` event succeeded but no workflow listened for that event, so it was not a sweep. Push-trigger/check-output workarounds were offered but not authorized.

Reading workflow metadata worked. Reading logs/artifacts did not: redirected hosts were outside sandbox egress permissions, and public run pages required sign-in for logs. The owner selected manual dispatch in GitHub and pasted the summary. Run `40471064309` was independently confirmed as successful, with artifact upload success, while the actual TSV was unavailable locally.

The summary reported 27 HTTP 200 responses and three 403s. The three affected provider pages were read again using the page-fetch tool, supporting continued access findings. LinkedIn still failed under that tool. The manifest, documentation and library outputs were updated, a sweep consistency check was added, and PR #5 merged the record.

### 4.8 Deployment preparation and owner deployment

The owner proposed Vercel hosting. Advice focused on static output publishing, homepage routing, avoiding the development server as a build command, localStorage origin migration, and the fact that HTTPS does not create background notifications.

With approval, `vercel.json`, deployment documentation and static contract tests were added. PR #6 merged the configuration after CI. The owner deployed the site and supplied its production URL. No claim was made that the assistant had performed the production deployment or inspected all account settings.

### 4.9 Production mobile feedback

The owner identified:

- Excessive h1 wrapping on mobile and requested about a 25% reduction.
- The HR Learning Lab link opening YouTube incorrectly, with a “Couldn't Load Link” error in the app.
- A correct direct Talent Acquisition playlist URL.
- A foundational HR Essentials playlist that should precede it.
- Pals bobbing/jittering rapidly while scrolling on mobile.

The title clamp was scaled down exactly 25%. Both direct playlist URLs were canonicalized without `si` sharing parameters. Public playlist metadata identified 16 HR Essentials videos and 43 Talent Acquisition videos, but fetching also exposed a YouTube error banner; playback and app handoff were not asserted from those fetches.

Adding the first card exposed positional-key compatibility risk. A new dedicated key preserved all previous Stage 1 keys. The study budget stayed 94 hours by treating HR Essentials as a selected one-hour starter allocation within Stage 1, not a new full-course requirement. The historic HTTP sweep was frozen to its original URL snapshot rather than pretending the new destinations had been swept.

The Pals layer moved from fixed to full-document absolute positioning. A synchronous scroll regression measured zero native-positioning error and 240px lag in the fixed-layer control before engine correction. PR #7 merged the changes and regenerated outputs.

### 4.10 Embedded-preview click investigation

The owner could not click links in the embedded preview. Investigation first suspected a full-page decorative overlay. Direct hit-testing of all 27 resource links at all 13 widths ruled out interception in the tested browser. Real mouse input and emulated touch reached both playlist anchors; an unprevented click requested the correct new-tab URL.

The suspected remaining cause was preview-container external-tab handling, but it was never independently established. No speculative navigation rewrite was shipped. The investigation added regression coverage and clearly separated event activation from successful external page playback.

After merging PR #7, the owner reported: **“I've verified the fixes. All work as intended.”** This is the available production acceptance evidence for the mobile, playlist and scroll changes. It is not a recorded device/browser matrix or a timing trace.

### 4.11 Favicon parity

The owner requested the same favicon as Nature Photography. The exact inline SVG tag was fetched from the reference's `index.html`. The existing immutable validator prohibited every link tag, including a safe inline favicon. Rather than modifying the skill or disabling validation, a hash-pinned exact-tag exception was implemented locally.

Three favicon tests were added alongside the two deployment tests. Browser QA initially assumed the SVG had an intrinsic 32px size, but Chromium reported 150px because the reference declares a viewBox without explicit dimensions. The test was corrected to render the unchanged SVG onto a 32px canvas and inspect its four colours.

PR #8 merged after build, browser and hosting-preview checks passed. There is no later owner statement confirming the production tab icon or favicon-cache refresh. This report stops at that product baseline.

## 5. Repository architecture and ownership boundaries

### 5.1 Component diagram

```text
Authoring inputs                           Build / validation boundary
----------------                           ---------------------------
recruiter-talent-acquisition-library.md --> vendored docx_render.py
                                             |--> PDF
                                             |--> DOCX
                                             |--> static HTML (no JS)
                                             `--> Markdown copy

roadmap-app.json -------------------------> vendored interactive_app.build_app()
fieldnotes-theme.css --------------------> repository build_tracker.transform()
favicon-link.html -----------------------> exact pinned inline favicon insertion
pals/{config,CSS,payload,controller} ------> repository inject_pals()
                                             `--> roadmap-app.html

check.py + hash inventories + tests ------> structural, semantic and drift checks
visual_check.mjs + Chromium --------------> actual built tracker behaviour
vercel.json -----------------------------> publish only committed out/ files
```

### 5.2 Authoritative inputs

- **Markdown content source:** the long-form instructional artifact, research explanation, resource cards, paid extras, exclusions and verification log.
- **Roadmap JSON:** the interactive app's structured content; it is not currently generated from Markdown.
- **Theme CSS:** visual tokens and overrides for the generated tracker.
- **Pals directory:** configuration/controller/style code plus immutable engine payload and license.
- **Favicon link source:** exact upstream inline tag.
- **Build wrapper:** all permitted transformations of the immutable interactive generator's output.
- **Manifest:** source-level verification classifications and the historical HTTP-sweep record.

### 5.3 Generated outputs

`learning-library/out/` contains exactly five files. They are generated **and committed** because downloadable/deployable files are part of the product. The deployment consumes those committed files directly, without regeneration. Therefore source correctness alone is insufficient: stale output is a deployable defect.

The Markdown output is a deliberate byte-identical copy of the Markdown source. The static HTML and interactive HTML serve different use cases. The static library is readable without JavaScript and includes the full narrative; the tracker builds its resource DOM in JavaScript and exposes local interactions. The HR tracker does not inherit every feature from the reference site: guided tours and search/filter UI are not present simply because they existed upstream.

### 5.4 Two tools directories

`learning-library/tools/` owns the content-specific build wrapper. Root `tools/` owns repository verification, the preview server and browser QA. This split is historical but now documented. Neither directory should be moved casually: imports, Make targets, tests and documentation reference these paths.

### 5.5 Configuration and documentation hierarchy

- `docs/SETUP.md`: intended canonical environment and verification guide.
- `docs/DESIGN-SPEC.md`: current design contract, with later sections recording compatibility/favicons.
- `learning-library/DESIGN-SYSTEM.md`: historical port/refinement record, not the final CSS specification.
- `CHANGELOG.md`: chronological work log; historical rows remain historical.
- `RETROSPECTIVE.md`: root-cause diagnosis and remediation log, scoped originally to PRs #1–#3 and later annotated.
- `docs/DEPLOYMENT.md`: publishing and production smoke-test procedures.
- `THIRD-PARTY-NOTICES.md`: Piixpal provenance/license pointer.

Some of these documents contain stale statements identified in Section 19. This report does not silently repair them. Current code plus fresh evidence takes precedence over outdated narrative.

## 6. Learning content, research and access claims

### 6.1 Eight-stage curriculum

| Stage | Calendar | Hours | Current cards | Intended engineering/product rationale |
|---|---|---:|---:|---|
| 1. Orientation | Weeks 1–2 | 8 | 4 | Establish HR context before recruitment vocabulary and lifecycle mapping |
| 2. Foundations | Weeks 3–5 | 14 | 4 | Fair process, job/person requirements and relevant legal framing |
| 3. Define the role | Weeks 6–7 | 10 | 3 | Define success before sourcing or evaluating candidates |
| 4. Find people | Weeks 8–10 | 14 | 4 | Boolean sourcing, recruitment channels and candidate experience |
| 5. Screen | Weeks 11–12 | 10 | 3 | Evidence-based shortlisting against explicit criteria |
| 6. Interview | Weeks 13–15 | 16 | 3 | Structured questions, rubrics and consistent decision-making |
| 7. Law and offers | Weeks 16–17 | 10 | 3 | Nigeria-specific candidate-data, recruiting and offer/onboarding awareness |
| 8. Work the process | Weeks 18–20 | 12 | 3 | Pipeline metrics, a practice portfolio and entry-level applications |
| **Total** | **20 calendar weeks** | **94** | **27** | Study budgets, not promises or mandatory full-provider-course runtimes |

The sum is 94 hours; at exactly five hours/week this is 18.8 weeks. The published approximately 20-week schedule has planning flexibility and staged allocation. Several resource cards link full courses while assigning selected units; adding provider full runtimes would overstate the core requirement.

Stage practice progresses from a lifecycle diagram to job analysis, advert and scoring criteria, sourcing strings, shortlist, interview kit, legal questions, pipeline metrics and a portfolio. Stage 8 asks learners to apply to five junior recruiter/HR assistant roles with evidence rather than certificates alone. No real candidate personal data was gathered by the project.

### 6.2 Research protocol

Search results were candidate discovery, not confirmation. The resource cards record provider, format, cost, estimated study time, why it belongs in the stage, next action and an access/verification note. A free badge was supposed to be supported by public provider language, with explicit caveats for incomplete access.

No accounts were created, subscriptions purchased or enrolments completed during the research. Account-required resources therefore rest on provider statements, not a tested signed-in journey. The library's legal sources were not read cover to cover; arrangements of articles and opening provisions were inspected. Google re:Work's index and two guides were read directly, but not every guide named by the curriculum.

### 6.3 Provider-specific decisions

- **Saylor:** free tuition/materials and completion certificate, with a 70% final-exam threshold. Free accounts are needed for assessments. Proctored college-credit arrangements are a separate category and not required for the completion certificate.
- **OpenLearn:** free course and free statement of participation, with an account for tracking/claiming evidence and some activities. The course is older and UK-framed; its employment-law examples do not substitute for Nigerian law.
- **Alison:** free study/completion; optional branded certificates are paid; a free Learner Record is distinct from that certificate. No exact certificate checkout price was established.
- **Coursera, University of Minnesota:** “Enroll for free” conflicts with access conditions in the FAQ. Full access may mean a paid Certificate experience, a trial, or a no-certificate option where offered. That option was not confirmed for this course; the card remains paid/conditional and not confirmed free. Its ten-hours/week pace exceeds the learner's budget, reinforcing its optional status.
- **OpenStax:** free, openly licensed textbook; US examples and legal references are context rather than Nigerian instruction.
- **O*NET:** a free occupational database useful for analyzing roles, with US classifications requiring local interpretation.
- **Workable and Greenhouse:** public templates, worksheets and articles are learning resources, not an assertion that their commercial recruiting software is free.
- **Google re:Work:** practical hiring/interviewing guides are reused at several stages; a shared URL intentionally supports different stage-specific actions.
- **HubSpot Academy:** a short CRM lesson is relevant as a practice pipeline tool. Its inclusion does not turn the route into a marketing-certification plan or imply all HubSpot software tiers are free.
- **Jobberman:** free-listing claim is partial because only cookie-banner content was available to the research tool. Paid tiers exist. This is a persistent qualification, not erased by a later HTTP 200.
- **NDPC:** primary regulator GAID PDF supplies local privacy principles, lawful bases, consent and breach-duty context. A student plan is not legal advice or an exhaustive compliance opinion.
- **PLAC Labour Act reproduction:** a free statutory text, not a fresh legal opinion or a guarantee of consolidated current amendments. The library calls out the age of the Act and need for current local advice.
- **CIPM:** paid professional membership-by-examination is the local professional-route reference, not a free course credential.
- **HR Learning Lab:** public introductory playlists disclose AI-supported video production. They are primers whose consequential legal or professional claims should be cross-checked against primary sources.
- **LinkedIn:** prices remained secondary-source estimates because provider help content could not be reliably read. Neither a successful HTTP code nor a login page removes that gap.

### 6.4 Prices and credential distinctions

Historical provider-published CIPM amounts recorded in the library were application **NGN 10,000**, acceptance **NGN 12,000**, Foundation **NGN 55,440**, Intermediate I **NGN 57,190**, Intermediate II **NGN 58,200**, Professional I **NGN 64,050**, Professional II **NGN 70,050**, and exemption fees **NGN 20,250–24,300**. They were explicitly subject to provider review. Entry requirements were recorded as degree/HND plus five SSCE credits including English and Mathematics; undergraduates could enrol but induction followed graduation. These are historical content findings, not revalidated current quotes.

Secondary 2026 guides supplied roughly **USD 39.99/month or USD 239.88/year** for LinkedIn Learning/Premium Career and **USD 170/month or USD 1,680/year** for Recruiter Lite, with trial/card caveats. They were deliberately labelled unconfirmed. No currency conversion, taxes, payment-card charges or data costs were added.

HRCI's Coursera course, AIHR sourcing/recruitment certification and Udemy recruiter training were kept outside the confirmed-free set; free-trial language is not permanent free access. Optional paid extras were separated from the core route rather than hidden in a free-only narrative.

### 6.5 Exclusions and localization

Roundup-only free-certificate claims from Simplilearn SkillUp, LearnTube.ai, LearnCafe and similar listings were not promoted to verified resources. SHRM/CIPD/HRCI member toolkits or exam products were not presented as free. Long unverified channel directories were rejected as padding. Broad marketing/sales certifications were excluded despite some genuinely free providers because they did not serve the learner's recruiter path.

Two structural gaps were named: current free Nigeria-specific recruiter courses are scarce, and useful US/UK methods arrive with nonlocal titles and legal assumptions. The legal/regulator stage is a conscious corrective, not a claim that every imported example transfers unchanged.

### 6.6 Counts are different concepts

At this baseline:

- 27 resource **cards**.
- 22 distinct **card URLs**.
- 31 distinct **current verification/check-script URLs**.
- 30 URLs in the **historical sweep snapshot**.
- 23 confirmed, 1 ambiguous, 1 partial, 2 unreachable and 4 not-confirmed **manifest entries**.
- 25 non-paid-labelled cards, but **one of those is the partially verified Jobberman listing**.

The hero's `VERIFIED FREE` fact is computed from cost strings that do not start with `paid`, not from manifest status. Therefore its displayed 25 must not be treated as a proof that 25 card-level free-access claims have equally strong verification. This is a current reporting/model weakness found by source inspection; Section 19 recommends fixing it. The two paid/conditional cards are Coursera and CIPM; paid CIPM can still have a `confirmed` manifest status because “confirmed” means the access finding is documented, not “free.”

### 6.7 Verification freshness

`verified_at` dates describe content inspection, not curl availability. Entries without a date or not marked confirmed are gaps. Confirmed entries older than `max_age_days=90` become stale. Default mode warns; `--strict` makes the warning fatal. Eight gaps remain at this baseline. The current check prints only the first five gap details even though its summary reports all eight; Appendix C lists all entries.

This mechanism is review scheduling, not automated ongoing provider validation. It does not detect changed prices within the 90-day window. The broad opening statement that every cost/access claim was checked on the original date is too strong when read without the later exception notes; the report's per-entry distinctions are more accurate.

## 7. Skill provenance and discovery

### 7.1 Vendored execution skill

The 12-file `resource-learning-library` bundle is both a functional dependency and a provenance boundary. It includes `SKILL.md`, installation/readme material, requirements, four scripts, two examples, tests and its own ignore file. Root `tools/skill-hashes.sha256` records SHA-256 for every vendored file. Verification rejects missing, changed **and unexpected** files, excluding interpreter cache files.

That is stronger than merely checking whether the four Python scripts exist. An accidental README edit inside the skill violates the same boundary as a generator edit. Intentional upgrades require re-extracting/reviewing the skill, rerunning its tests and project contracts, and deliberately regenerating the inventory with `make pin-skill`.

The bundle's own test suite has five methods covering parsed block kinds, PDF/DOCX/static HTML generation and validators, interactive-app inline structure, protection against JSON closing a script, and style/output-name guards. It is not an exhaustive security audit or format conformance suite.

Piixpal's license does **not** confer a license on the entire repository or the learning-resource content. The skill's file integrity is proven by hashes; a comprehensive project-wide licensing review was not performed.

### 7.2 Discovery service registration

The user trusted `skill-issue.in` and requested durable project registration and task-by-task skill discovery. `.mcp.json` and `.claude/settings.json` commit the project-scoped registration and permissions; a global `/root/.claude.json` registration was also recorded historically but is not a portable repository dependency.

Historical discovery touched:

- `frontend-design` and responsive-design guidance for the initial port.
- `design-web-design-guidelines` for web-design review.
- `design-design-system-patterns` for tokens/component consistency.
- `design-accessibility-compliance` for contrast, focus, keyboard, targets and reduced motion.
- `design-taste` for visual restraint and typography review.
- `design-ui-ux-pro-max` for design-system/UX guidance.

The endpoint's available catalog was fetched, but sandbox HTTP POST restrictions prevented normal MCP execution. GitHub sources and externally linked guidance were inspected as fallbacks. Thus **“registered and source reviewed” is accurate; “MCP tools successfully ran for every task” is not**.

During this report task, the design-guidelines catalog page was fetched again. No clearly applicable report-specific skill was selected, installed or executed. This report was assembled from repository/history evidence and normal engineering analysis, not represented as output of an unavailable audit skill.

## 8. Generation and reproducibility

### 8.1 Environment lock

`requirements.lock` freezes seven direct/transitive Python packages:

| Package | Version |
|---|---|
| charset-normalizer | 3.5.2 |
| lxml | 6.1.3 |
| pillow | 13.0.0 |
| pypdf | 6.21.2 |
| python-docx | 1.2.0 |
| reportlab | 4.5.1 |
| typing_extensions | 4.16.0 |

Python 3.11 is the supported baseline; the fresh local run reported 3.11.2. The upstream skill only specifies broad ranges. Freezing the resolved tree avoids changes caused by unconstrained dependency releases, but the lock is not a hashed wheel lock and does not freeze OS libraries or pip itself. Bootstrap upgrades pip and installs from the lock when `.venv/bin/python` is absent.

**Important operational caveat:** `make bootstrap` uses the venv Python executable as its file target. If the executable exists but packages are missing or the lock changed, Make does not automatically re-install the environment. Recreate `.venv` or explicitly install the lock in that case; do not claim an existing venv was refreshed just because `make bootstrap` printed a Python version.

### 8.2 Document generation

`make build` invokes the vendored `docx_render.py` with the Markdown source, output directory, `Recruiter-TA-Library` basename, title, subtitle and hero metadata, requesting PDF/DOCX/MD/HTML. It then invokes `build_tracker.py`.

The long-form formats share the parsed Markdown block model. The skill supports headings, paragraphs, callouts, tables, lists and code in the scope tested by its sample. Output links are validated by the format-specific checks. A detailed manual proofread of every page and every screen-reader rendering was not recorded.

The Makefile's hero metadata still identifies the original 26 October verification date. Later source updates do not automatically turn that into a new date. This is a deliberate audit warning about static metadata, not a proposed date falsification.

### 8.3 Tracker transformation pipeline

The wrapper imports `interactive_app` from the immutable skill, builds the functional base HTML, and applies the local transformation. The current contract comprises:

- Eight branding anchors.
- Three Pals anchors.
- A required closing head tag for the pinned favicon insertion.
- A guarded exact resource-key function rewrite.
- Source-level prohibition checks against external dependencies.

The eight branding edits cover the browser title, theme/description metadata, skip link, hero eyebrow, footer credit, reminder input semantics, import input name and computed hero facts. The inline theme stylesheet is inserted separately before the closing head tag. Pals add their stylesheet, control panel, inert engine template and controller. The generator's own script is not edited in the vendored tree.

Each regex substitution is limited to one match and fails when no match exists, rather than silently applying global substitutions over unknown HTML. The contract test checks the original anchors, deliberately breaks each one and expects failure, and proves the transformed tracker reproduces byte-for-byte. Do not infer uniform duplicate-anchor rejection: the key shim and favicon have explicit exact-count guards, while the general branding substitutions use `count=1`. This turns vendor-template drift into a build failure rather than an unnoticed partial theme.

The coupling is nevertheless fragile: these are string/regex anchors into an upstream template, not a formal plugin interface. A legitimate upstream markup change can break many local tests simultaneously. The appropriate response is an intentional adapter review, not broadening the regex until it passes arbitrary content.

### 8.4 Self-containment

The product tracker contains no required external script, stylesheet, image, frame, font or CSS asset URL. Its favicon is an approved `data:image/svg+xml` link. Piixpal sprites are script data, not downloaded image files. The builder enforces self-containment and the immutable validator is run on a temporary copy with only the exact approved favicon removed.

The application can load as a local file and retain core interactions, subject to browser storage/security rules. HTTPS is required for ordinary hosted notification permission. The linked courses themselves still require connectivity, accounts where stated, provider availability and sometimes paid access.

### 8.5 What reproducible means here

The output-drift check builds all five artifacts in a temporary directory and compares:

- Markdown: exact text/bytes.
- Static HTML: exact text/bytes.
- Tracker: exact text/bytes.
- PDF: page text extracted with `pypdf`.
- DOCX: ZIP archive entry contents, ignoring timestamp/container metadata.

PDF/DOCX binary hashes can change from metadata even when content is semantically identical. The PDF comparison also does not establish pixel-identical pagination or typography; extracted text can remain equal while layout changes. Current binary hashes in Appendix D are an audited snapshot, not a promise of universal byte reproducibility on every OS.

### 8.6 Committed generated artifacts and cache policy

Root `.gitignore` excludes venvs, Python/Node caches, logs, screenshots and local sweep TSV output. `.gitattributes` protects format handling, including PDF/DOCX binary treatment. The output directory is a special case: artifacts are committed despite the sandbox's generic snapshot exclusion for directories called `out`. This difference caused a real preview regression and is why the preview rebuilds the tracker every start.

`make clean` removes selected untracked test/cache artifacts and Python caches while preserving `.venv`; it is not a full dependency reset or a deletion of delivered outputs.

## 9. Browser runtime and persistence

### 9.1 State and render model

The tracker is plain inline JavaScript and browser APIs, not React/Vue/Svelte. `DATA` is serialized JSON. `buildRoadmap()` constructs stage `<details>` elements, summaries, resource `<article>` cards, metadata, links and completion labels using `textContent`/DOM creation. The first stage is open by default; no resources are hard-coded in the output independently of `DATA`.

Completing an item updates state, records today's activity, saves localStorage, updates card presentation, updates overall metrics and recalculates stage percentages. Unchecking removes the completion flag, but it does **not** erase the day's activity record. Empty-resource stages are supported via a separate stage-complete key even though this particular plan has cards in all eight stages.

Dashboard progress is count-based, not time-weighted. A one-hour card and a multi-hour course each count as one item. The next action is the first incomplete resource in roadmap order. At 27 cards one completion rounds to 4%.

### 9.2 Storage namespace and schema

The progress key is:

```text
rll-roadmap-progress-v1:
  + normalize(DATA.storage_id || DATA.title || 'roadmap')
```

Normalization lowercases and replaces runs of nonalphanumeric characters with hyphens. The current JSON supplies stable `storage_id: rll-recruiter-ta-2026-10-26`, yielding `rll-roadmap-progress-v1:rll-recruiter-ta-2026-10-26`, so ordinary title changes need not destroy progress. The exact data value is preserved in the source and has not been renamed during the design/mobile releases.

Persisted state includes:

```json
{
  "done": { "s0-r0": true },
  "activityDates": ["2026-10-27"],
  "reminderTime": "19:00",
  "notificationsEnabled": false,
  "lastNotificationDate": ""
}
```

The sample is schematic, not an actual user's export. `done` is a map, not a list of index positions. Only recognized current item keys contribute to displayed progress; old/unknown keys can remain stored. A storage read failure falls back to defaults. A write failure displays a notice advising export or another browser. In-memory progress can still work for that session.

### 9.3 Stage 1 insertion compatibility

Original Stage 1 had three cards with keys `s0-r0`, `s0-r1`, `s0-r2`. A naïve prepend would reuse `s0-r0` for HR Essentials and shift every old completion to the wrong card.

The local build adapter replaces the generator's exact `resourceKey()` function so that:

| Current Stage 1 index | Current card | Saved key |
|---:|---|---|
| 0 | New HR Essentials playlist | `hr-essentials-v1` |
| 1 | Existing TA card, now direct playlist | `s0-r0` |
| 2 | Existing Saylor PRDV226 | `s0-r1` |
| 3 | Existing OpenStax chapter | `s0-r2` |

Other stages retain their original positional keys. Neither the localStorage namespace nor export envelope changed. The regression fixture restores old keys and expects new Stage 1 checkbox states `[false, true, false, true]`.

This is backward-compatible for **this insertion**, not a general migration framework. Reordering later cards/stages is still dangerous. Stable resource IDs throughout the model are a recommended future change, with an explicit migration from all old keys.

### 9.4 Streaks and local calendar

Activity dates use the device's local year/month/day, not UTC. The previous-day helper constructs a local date at noon before subtracting a day, reducing midnight/DST edge complications. A streak includes today when logged; otherwise it can remain active through yesterday. The plan's Lagos context does not force all users into Africa/Lagos—travel and timezone changes follow the browser/device.

Only completing an item logs activity; merely opening a resource or leaving the tab open does not. Repeated completion actions on the same local day add no duplicate date. Reset clears both progress and streak history after confirmation.

### 9.5 Export/import

Export downloads `learning-roadmap-progress.json` with `version: 1`, title, `done`, `activityDates` and `reminderTime`. It uses a Blob/object URL, then revokes the URL. Notification permission state, last notification date and Pals preferences are not exported.

Import parses a user-selected local JSON file, requires an object-like `done` field and array of activity dates, filters date-shaped strings, optionally accepts a time-shaped string, saves, rebuilds cards and reports success. No file is uploaded.

The import validator is deliberately simple, but that leaves debt: it does not enforce the exported version/title, validate real calendar dates or time ranges, filter done keys/values strictly, cap file size, or reject every object-shape anomaly. The report does not claim schema-level validation. Prefer trusted exports until this is hardened.

### 9.6 Reset and DOM rebuild interaction

Reset asks for confirmation and replaces state with defaults. Import and reset both call `buildRoadmap()`, which replaces the roadmap's child nodes. That destroys old stage-heading DOM anchors. The Pals controller observes direct child-list replacement and reattaches decorations after the next animation frame. Without that observer, decorations could target detached elements after otherwise successful data operations.

### 9.7 Reminders and notifications

The native time input defaults to 19:00. The owner-approved interface removes the visible “Reminder time” label; an accessible name/title remains.

Notification permission is requested only after a user action. Unsupported APIs, insecure contexts, denied/default permissions and exceptions all receive in-app explanatory messages. Enabling notifications stores a boolean, but a stored boolean alone cannot grant browser permission.

While the document is running, `checkReminder()` executes immediately, every 60 seconds, and when visibility returns. It requires:

1. App notification setting enabled.
2. A supported Notification API with permission `granted`.
3. Local current time at or after the stored reminder time.
4. No notification already recorded for today.
5. No learning activity already recorded for today.

The notification body invites a short return to the roadmap; clicking focuses the window and closes the alert. Failures fall back to the in-app check-in.

There is no service worker, scheduled push service, server cron for a learner, or reliable closed-tab delivery. Browser throttling, suspended tabs and mobile OS notification support can prevent timely alerts. Hosting on HTTPS improves permission eligibility; it does not change this architectural limit.

### 9.8 Browser-origin migration

localStorage belongs to origin and browser profile. A local file, sandbox preview domain, temporary deployment URL, production domain and future custom domain are separate storage contexts. Nothing automatically transfers between them. The deployment guide tells users to export before changing origin and import afterward.

The Pals preference is separately stored as `fieldnotes-hr-pals-v1`; it is not part of the progress export. Moving domains can reset decoration preferences without losing a separately imported progress file. Private browsing, storage eviction, profile resets and manual site-data deletion can still remove state.

## 10. Design-system port and visual evolution

### 10.1 Reference vocabulary

The port adopted the reference's editorial “field notes” identity:

| Token | Value | Role |
|---|---|---|
| Ink | `#11142B` | Main text/page frame |
| Paper | `#FFF8E7` | Sheet background |
| Cream | `#FFFDF6` | Card surfaces |
| Rule | `#1E2553` | Borders |
| Muted | `#565C73` | Secondary text |
| Blue | `#3768FF` | Hero and focus |
| Blue ink | `#2C55DA` | Links |
| Cyan | `#65E8FF` | Hero rule/accent |
| Pink | `#FF4E91` | Hard offset shadow |
| Yellow | `#FFE168` | Eyebrows/paid-cost tags |
| Green | `#5EE780` | Free-cost tags |
| Orange | `#FF9958` | Duration accents |

System monospace fonts form interface chrome; system sans-serif carries prose. No remote font fetch is needed. Square corners, thick rules and discrete shadow offsets replace a generic rounded-dashboard aesthetic. Generator variables are aliased to Fieldnotes tokens, and remaining hard-coded styles are explicitly overridden in the appended stylesheet.

### 10.2 Hero refinements

The owner requested removing coloured bars above the hero while preserving the three coloured squares above the footer. The hero reaches the sheet's inner cyan edges, not a `100vw` full-browser breakout. The small-gutter clarification matters: a viewport-wide interpretation would break the framed composition and risk overflow.

The eyebrow now uses dark ink, not a pale inherited colour. Its next interval into the h1 was intentionally preserved while other hero spacing tightened. The repeated “h1 +40%” instruction was treated as one 40% increase, not two compounded increases. A mistaken left-only shadow result was corrected to the bottom-only pink shadow. These corrections are part of the implementation history, not final defects.

Before mobile feedback, the enlarged clamp reached approximately 122.3px at its maximum. The later requested 25% reduction produced:

```css
font-size: clamp(2.2365rem, 6.5205vw, 5.733rem);
```

At a 16px root font this is a 35.784px minimum and 91.728px maximum. It is exactly 75% of the previous `2.982rem / 8.694vw / 7.644rem` clamp. Fresh Chromium results measured 35.8px at 320–430px and 91.7px at 1440–1920px.

The hero facts are computed from JSON rather than manually updated counts, with the semantic caveat about `VERIFIED FREE` described earlier. The reference favicon was initially omitted and only added in PR #8.

### 10.3 Resource-card composition

The four historical refinement rounds were not a single undifferentiated redesign:

1. **Initial port:** tokens, borders, hard shadows, square corners, CSS decoration/print rules; removal of top hero bars, footer credit, dark eyebrow, bottom link/Done placement.
2. **Second round:** all metadata tags coloured; stage-intro margins equalized; square outcome markers; arrows on the then-26 links; hero inner-edge alignment and larger title.
3. **Third round:** subtitle and fact chips reduced 25%; progress cards enlarged 20%; previously shared chip/card styling separated so changes would not leak between components.
4. **Fourth round:** title enlarged 40% once; stage heading components baseline-aligned; visible reminder label hidden with an accessible name retained; hero gaps tightened except the protected eyebrow-to-title interval.

The later 25% title reduction belongs to production-feedback PR #7, not to those original four rounds.

The final owner-directed resource layout places the provider link bottom-left and the completion checkbox bottom-right. Stage-intro text has equal margins, and outcomes use a filled square marker. Each outbound resource link receives a small northeast arrow.

The footer text is exactly:

> Made with love and fried plantain, by Moyinoluwa

The footer's three coloured squares remain. The toolbar/footer left edges and document frame are measured in browser QA rather than assumed from CSS.

### 10.4 Metadata colours

Every metadata role was meant to have a differentiated fill; generic provider/modality/date/time tags cycle through the reference palette while free and paid cost tags retain semantic green/yellow. Six rendered fills are checked. Historical contrast measurements ranged approximately **8.59:1–14.00:1** against the ink colour.

“Every tag gets its own colour” was implemented as distinct role/cycle colours, not a globally unique colour for every card instance. The ordinal cycle means many cards intentionally repeat the same palette.

The skill chooses a paid-style cost tag when the text contains `paid`, a currency sign or `NGN`. Cost classification is therefore string-based. Future content changes should not assume a richly typed pricing model exists.

### 10.5 Responsive decisions

The app was tested at 320, 360, 390, 430, 600, 620, 700, 900, 1024, 1200, 1320, 1440 and 1920 CSS pixels. QA measures horizontal overflow, title size, tags, borders/shadows, dashboard collisions, card controls, focus-oriented structure, footer alignment and creature interference.

Default first-stage-open states were separately checked at 320/900/1440 after an initial test had only exercised all stages expanded. This test correction is important: expanded-only checks missed the exact state normal visitors first see.

The “Done” control and link retain their left/right alignment at narrow widths. Toolbar buttons and stage summaries meet the harness's 44px minimum-height rule. This is not a claim that every clickable element has a 44×44px target.

### 10.6 Explicitly accepted accessibility tradeoffs

The design retained small chip text, historically around 9.12px, and removed the reminder's visible label at the owner's direction while keeping an accessible name. Contrast and control geometry were checked, but these choices can still reduce readability/cognitive clarity. Formal WCAG conformance, browser zoom stress testing, long translated strings and assistive-technology usability were not certified.

## 11. Piixpal integration and scroll repair

### 11.1 Provenance, payload and license

The engine is **Piixpal v0.4.0**, upstream <https://github.com/diiviikk5/Piixpal>, obtained from the reference site's inert `template#pals-payload`. The project keeps the payload byte-exact and records SHA-256:

```text
298776d7bbe408cd3146f61fbb38ec8fddaa2facb1db99c3f013638f5d20ea75
```

The upstream MIT text is in `learning-library/src/pals/LICENSE-MIT.txt`; `THIRD-PARTY-NOTICES.md` points to provenance. The engine's own sprite/core code is not edited to fit the application. Project-local controller/CSS perform the integration.

### 11.2 All ten placements

| # | Sprite | Anchor | Special configuration |
|---:|---|---|---|
| 1 | bitbug | Hero `#title` | Text edge, `at: 0.9` |
| 2 | lurk | Hero `#subtitle` | `at: 0.88` |
| 3 | moss | First dashboard panel h2 | `at: 0.9` |
| 4 | pip | `#next-step` | `at: 0.85` |
| 5 | capy | `#reminder-summary` | `at: 0.5` |
| 6 | bumble | Stage 1 heading | Scale 3, `at: 0.9` |
| 7 | shel | Stage 3 heading | Scale 3, `at: 0.9` |
| 8 | frog | Stage 5 heading | Scale 3, `at: 0.9` |
| 9 | moss | Stage 7 heading | Hue 320, scale 3, `at: 0.88` |
| 10 | bumble | Footer | Hue 205, scale 3, `at: 0.5` |

The sprite list contains eight species: bitbug, lurk, moss, pip, capy, bumble, shel and frog. Ten placements are not ten unique sprites. Targets are prose, never links, buttons, checkboxes or time inputs. The engine's actual canvas can accept pointer events, so “decorative” alone is not evidence of harmless hit-testing.

### 11.3 Lifecycle and controls

The inert engine template is copied inline but executed only when the controller chooses to load it. `requestIdleCallback` with a two-second timeout is preferred; a 1.2-second timer is the fallback. Payload execution happens once. Each render removes the app's old `piix-pal` elements and creates current placements, marking them `aria-hidden`.

A toggle persists `on`/`off` under the separate Pals storage key. `aria-pressed`, visible button text and a live status message explain the current state. Reduced-motion preference overrides a stale saved `on` on initial load, so no actors are created by default under `prefers-reduced-motion: reduce`. A visitor can explicitly opt in. Print CSS hides decoration and its controls.

Exceptions are swallowed at the decoration boundary so a creature cannot prevent learning interactions. That is a resilience choice but also means not all failed individual placements become console errors; explicit count/anchor tests remain necessary.

The controller reads the media query during initialization rather than registering a live change listener. The CSS reduced-motion rule also cannot be assumed to penetrate arbitrary Shadow DOM internals. The observed initial reduced-motion result is strong; a comprehensive live OS-toggle and engine-loop teardown test is not established.

### 11.4 Original scroll problem

The engine creates an overlay using Shadow DOM and updates actor coordinates with animation frames. A fixed overlay must track page-scroll movement in JavaScript. Mobile compositor-driven scrolling can advance the page before main-thread frame corrections run, producing visible lag/jitter.

The repair retains the engine and payload but overrides the host layer:

```css
body { position: relative; }
div[data-piixpal] {
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
  overflow: clip !important;
}
```

The overlay now spans document space and moves natively with targets. Full dimensions prevent a zero-sized/viewport-sized clipping regression. This is distinct from simply hiding offscreen creatures or changing animation speeds.

### 11.5 Scroll regression and control experiment

The test freezes the engine's requestAnimationFrame loop, scrolls synchronously by 240px and measures actor rectangles. With the absolute layer the native movement error is **0px**. It then temporarily sets the layer to fixed as a control and measures **240px** error before correction. That establishes the positioning mechanism directly, without waiting for a new frame to conceal the lag.

An initial zero-delta measurement was a test bug: inherited smooth-scroll CSS meant the scroll had not occurred synchronously. The test now requests instant scrolling. It does not change the production smooth-scroll preference merely to satisfy QA.

Fresh browser output repeats `delta=240, maxError=0, fixedError=240`. The owner's later live acceptance supports the practical mobile improvement; neither source constitutes universal GPU/compositor performance certification.

### 11.6 Interaction bounds and accepted overlap

The visual suite checks counts, anchor visibility, absence of control-centre coverage and a bounded rectangular intersection area, with a configured maximum of **1,100px²** per control intersection. **Zero interference does not mean zero geometric overlap.** Fresh runs showed roughly 555–560px² worst overlap with stage summaries at intermediate desktop widths, within the configured tolerance, while all control-centre hit counts were zero.

Pals can therefore intentionally sit on the upper/outer edge of prose-related components. The test does not assert a pristine exclusion zone around every control at every animation phase. A separate resource-link hit test probes all 27 links across the viewport matrix, and collapsed states are checked separately.

### 11.7 Pause is not yet a measured full CPU shutdown

Pausing removes the app's creature elements, and the tests observe zero visible placements. Once loaded, the upstream engine and its shared overlay/loop may remain. There was no full power/CPU teardown measurement proving all animation infrastructure is stopped. If battery impact matters, profile and add an upstream-compatible teardown lifecycle rather than claiming the current control guarantees zero processing.

## 12. Link-sweep execution and evidence limits

### 12.1 Why the local sweep originally failed

The sandbox permits selected development hosts but not arbitrary provider domains. Historical provider curl attempts produced certificate/TLS failures and `000` response codes. A page-fetch service could read some pages even when shell curl could not. Those are different execution environments and cannot be conflated.

`check-links.sh` was committed so a machine with suitable outbound access could execute it. It uses `curl -sS -o /dev/null -w "%{http_code}" -L --max-time 25`, retains default TLS checking, suppresses stderr and writes a TSV status/URL report. It does not set a custom user agent. Removing TLS verification was not adopted as a verification strategy.

### 12.2 Workflow policy

`.github/workflows/link-check.yml` runs on manual dispatch and Mondays at **06:17 UTC** (`17 6 * * 1`). It checks out full history, runs the script, writes a GitHub step summary, reports non-2xx results and uploads `link-status.tsv` as `link-status`. Freshness is nonblocking.

The workflow is a report, not a universal access gate. Providers can block bots, return login pages with 200, redirect to a homepage or show regional offers. A human/provider-page review is required before changing a free-access claim.

The schedule configuration is not evidence a scheduled run occurred. The audit found the manual run below, not a subsequent weekly result. Given the implementation date and this report date, the next Monday is 2 November; no outcome for that future run is implied.

### 12.3 The one observed sweep

| Field | Recorded value |
|---|---|
| Run | <https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40471064309> |
| Event | Manual `workflow_dispatch`, performed by owner |
| Created | 27 October 2026, 08:04:47 UTC |
| Head | `0a3f440` (PR #4 baseline) |
| Conclusion | Success |
| URL count | 30 |
| Results | 27 × HTTP 200; 3 × HTTP 403 |
| Artifact | Upload step succeeded; raw TSV not retrieved in the sandbox |
| Evidence channel | Owner-pasted summary plus independently queried run metadata |

The three 403 pages were OpenLearn's recruitment course, Saylor's FAQ and NDPC's GAID PDF. They were re-read with the fetch tool; the content supported the existing findings. “Bot filtering” is the recorded interpretation of the curl/fetch discrepancy, not a demonstrated internal diagnosis of each provider's firewall.

LinkedIn returned 200 to curl in the summary but remained unreadable or errored under page fetching. The manifest retained `unreachable` and unconfirmed price notes. This is a useful concrete example of why code-only status classification would have been wrong.

### 12.4 Historical snapshot preservation

After playlist changes, the current URL set grew to 31. The old snapshot contains the previous HR Learning Lab channel URL and does not magically gain evidence for both new playlists. The manifest freezes `link_sweep.urls` for the actual run. The `sweep` check validates count and breakdown against that snapshot, while `sources` validates the current 31-entry list against the current script.

The sweep cannot be replayed byte-for-byte from the available raw evidence because the TSV was not retrieved. It must be cited as a historical owner-provided summary with independently corroborated run status, not a locally parsed artifact.

## 13. Preview infrastructure and sandbox recovery

### 13.1 Durable local server

`tools/serve_preview.py` is a standard-library HTTP server. It binds `0.0.0.0`, serves only `learning-library/out`, and maps `/` and `/index.html` to the interactive tracker for both GET and HEAD. It performs a startup warning check for Pals markers.

Start the durable entry point with:

```sh
make preview                 # port 8000
make preview PORT=8001       # alternate port
```

It rebuilds **only** the tracker, not timestamp-bearing PDF/DOCX files, and needs plain Python rather than the document venv. In the agent environment it should run under the long-lived process tool, not a timed one-shot shell command. The server does not need a framework's host/origin allowlist and sends no embedding-blocking configuration in this setup.

Preview hosts are proxied external URLs; a user's browser is not the sandbox. The application uses no browser-side localhost API calls, so no backend proxying is necessary. If a backend is introduced later, that architectural assumption must be revisited.

### 13.2 Reset sequence that caused missing Pals

1. Implementation generated a new uncommitted tracker in `out/`.
2. The preview process and runtime caches were lost during reset.
3. The snapshot omitted runtime/cache directories and restored Git's committed pre-Pals tracker.
4. A basic HTTP server could start successfully and serve the old HTML.
5. The owner saw a working preview with no Pals.

This was not fixed by a new sprite implementation. It was fixed by moving the script out of a cache directory and rebuilding from durable sources at startup.

### 13.3 What survives and what does not

Durable: tracked sources, config, scripts, lockfiles and committed outputs.  
Ephemeral: process state, `.venv`, `node_modules`, browser binaries, test reports, screenshots, `/tmp` uploads, global installations and cloned reference scratch copies.

A runtime reset is not proof the code was deleted; equally, a successful process restart is not proof the correct artifact was served. Recovery must check both process reachability and output identity/markers.

### 13.4 Browser installation workaround

The original scratch browser was lost with the environment. The committed harness uses `puppeteer-core` plus npm-distributed `@sparticuz/chromium`, avoiding a separate blocked browser-download host. The harness inflates the bundled AL2023 shared libraries and configures the library path. Early missing shared-library launch errors were environmental, not CSS failures.

The harness dependency set is locked in `tools/visual/package-lock.json`. It is Linux-oriented and uses Node >=22.12, with CI pinned to 22.22.3. It is not a portable claim that the same binary works on every workstation architecture.

## 14. Deployment architecture and production feedback

### 14.1 Static hosting contract

`vercel.json` specifies no application framework, no install command, no build command, `learning-library/out` as the output directory and one root rewrite to `/roadmap-app.html`. The hosting platform serves committed outputs; Node and Python are development/verification tools, not production servers.

There is intentionally **no catch-all rewrite**. A broad `/(.*)` → tracker rule would hijack PDF, DOCX and library HTML downloads and return tracker HTML for their paths. The two deployment tests protect the root mapping and the output-only publishing boundary. They do not query the owner's account dashboard or production deployment.

The two empty commands are intentional, not forgotten setup. CI proves artifacts before merge, and the hosting platform publishes them. If a future contributor decides to build on the host instead, they must provide a compatible Python environment, ensure all generated outputs are rebuilt, preserve drift checking and review the changed trust boundary.

### 14.2 Supported product routes

- `/` → interactive tracker.
- `/roadmap-app.html` → direct tracker file.
- `/Recruiter-TA-Library.html` → full static library.
- `/Recruiter-TA-Library.md` → Markdown artifact.
- `/Recruiter-TA-Library.pdf` → PDF artifact.
- `/Recruiter-TA-Library.docx` → DOCX artifact.

No API routes or custom application 404 handler exist in the repository. Resource links go to provider sites, not application routes. Root-directory exposure is limited to generated outputs by the host configuration rather than exposing `.agents`, content sources or tooling.

### 14.3 CI versus hosting checks

PR #8's checks included the repository build/verification job, browser job and a Vercel deployment check; the recorded PR build/browser durations were approximately 17s/19s. These are reported historical results, not performance service-level objectives. Merge-commit GitHub checks were independently inspected during this audit and both repository jobs succeeded on run:

<https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40485000208>

A hosting-preview success is not proof the owner's production tab has refreshed its favicon cache or that every linked course works on every phone. No connector/account audit was performed for this report.

### 14.4 Production verification boundary

The owner supplied `https://fieldnotes-hr.vercel.app/` and later confirmed the PR #7 fixes. The assistant did not independently browse production during this audit. Production deployment of the exact PR #8 hash, response headers, CDN caching, account ownership, environment settings and custom-domain behavior were not independently checked.

The report therefore distinguishes:

- Repository and CI state: directly verified.
- Successful hosting check: observed via GitHub check metadata.
- PR #7 functional live acceptance: owner confirmation.
- PR #8 live favicon: no subsequent owner confirmation.
- Current production infrastructure/security posture: outside the audited evidence.

## 15. Favicon port and validation exception

### 15.1 Exact artwork, not an approximation

The source was fetched from the reference repository through GitHub's contents API. `learning-library/src/favicon-link.html` stores the exact stripped link tag. The SVG has `viewBox="0 0 32 32"`, a dark square background and three horizontal yellow/cyan/pink bars. It is URL-encoded in a data URI, not stored as a separate remote asset.

The whole stripped tag is pinned to:

```text
ab629e3127cc247eb5077d4168f0a612b19d4c7cb05e2a43d5c3dc016449c9dd
```

Pinning only an allowed URI scheme would be weaker: another SVG, an event handler or additional link attributes could then pass. The implementation deliberately pins the full tag.

### 15.2 Local exception algorithm

1. Read/strip the favicon source and hash it.
2. Fail if it differs from the pinned reference.
3. Insert it once before the closing `</head>` in the generated app.
4. Require exactly one occurrence in the delivered HTML.
5. For immutable-validator invocation only, remove that **exact** occurrence from a temporary HTML copy.
6. Run the original validator on that copy, leaving every other link or external dependency subject to rejection.
7. Deliver the original HTML with its favicon still present.

The hash inventory proves the vendored validator was not altered. This is not a general relaxation to allow arbitrary `<link>` tags or active SVG content.

### 15.3 Unit-test coverage

The three favicon methods verify:

- Data URI, XML structure, four rectangles, viewBox and all reference colours.
- One approved favicon in the actual delivered tracker, with none remaining after adapter removal.
- Rejection of six variants: missing approved favicon, duplicate approved favicon, remote icon replacement, added event attribute, extra remote stylesheet and an extra unapproved inline icon.

These complement, rather than replace, the overall self-containment checks and output drift proof.

### 15.4 Browser decoding and corrected assumption

An SVG viewBox is an internal coordinate system, not necessarily the image's intrinsic CSS dimensions. With no explicit width/height, Chromium reported 150×150 natural dimensions. The first test's 32px assumption failed even though the artwork exactly matched the requested reference.

The corrected test decodes the link URI in the browser, draws it to a 32px canvas and samples four positions:

| Coordinate | RGBA | Meaning |
|---|---|---|
| (1, 1) | `[17,20,43,255]` | `#11142B` background |
| (5, 8) | `[255,225,104,255]` | `#FFE168` upper bar |
| (5, 15) | `[101,232,255,255]` | `#65E8FF` middle bar |
| (5, 22) | `[255,78,145,255]` | `#FF4E91` lower bar |

This passed locally and in browser CI. The requested source was not “fixed” by adding width/height, which would have violated exact-copy acceptance.

## 16. Tests, CI and fresh verification results

### 16.1 Verification layers

| Layer | Invocation | What it establishes | What it does not establish |
|---|---|---|---|
| Skill integrity | `tools/check.py skill-hashes` | All 12 vendor files match inventory | Upstream trust/security of those bytes |
| Vendor unit tests | `tools/check.py unit` | Five smoke methods succeed | Every parser corner case or real-world document |
| Format validators | `tools/check.py validators` | Current PDF/DOCX/static/tracker satisfy project rules | Pixel perfection or formal standards compliance |
| Prose audit | `tools/check.py style` | No configured mechanical/style findings | Pedagogical truth or perfect human prose |
| Transform contract | `tools/check.py contract` | Expected anchors, failure-on-break and bit-exact tracker | Robustness to arbitrary upstream templates |
| Content consistency | `tools/check.py sources` | Stage/card/hour/URL agreement across selected representations | Equality of every prose field or meaning |
| Documentation sanity | `tools/check.py docs` | Listed stale-pattern/path/Make checks | Absence of every stale sentence |
| Pals | `tools/check.py pals` | Config count/sprites/targets/hash/license/required markers | Browser geometry or measured CPU cost |
| Sweep record | `tools/check.py sweep` | Historical record internally consistent | A new network sweep or raw TSV reconstruction |
| Freshness | `tools/check.py freshness` | Dates and statuses produce expected warnings | Automatic provider revalidation |
| Drift | `tools/check.py drift` | Five outputs reproduce using defined comparisons | Universal binary/platform reproducibility |
| Repository unit tests | `python3 -m unittest discover -s tools -p 'test_*.py' -v` | Two deployment + three favicon methods | Actual hosting account configuration |
| Browser geometry/behavior | `make check-visual` | Built tracker passes headless Chromium assertions | All browsers, devices, accessibility tools or provider playback |

### 16.2 CI workflow

`verify.yml` runs on push to any branch, PR and manual dispatch, with read-only repository contents permission. Both jobs use full checkout (`fetch-depth: 0`). The build job uses Python 3.11, pip cache keyed by `requirements.lock`, bootstrap, repository unit-test discovery, fast checks, drift and a nonblocking freshness report.

The browser job uses Node 22.22.3, npm cache keyed by the browser lock and `make check-visual`. Dependencies are `@sparticuz/chromium` 153.0.0 and `puppeteer-core` 25.16.0. The observed browser identifies as HeadlessChrome/153.0.8010.0.

Actions are referenced by major tags (`checkout@v4`, setup-python@v5, setup-node@v4, upload-artifact@v4), not pinned commit SHAs. That is a supply-chain hardening opportunity, not a test failure.

`make ci` is deliberately the non-browser pair `check` + `check-drift`. Despite its name, it is **not the complete GitHub workflow**: repository test discovery and browser checks must also be run for equivalent local coverage.

### 16.3 Fresh audit execution

During this report task, the following sequence completed successfully:

```sh
make bootstrap
make ci
python3 -m unittest discover -s tools -p 'test_*.py' -v
make check-visual
```

Results observed on 1 November 2026:

- Skill hashes: 12 byte-exact files.
- Vendored smoke tests: five methods pass.
- PDF, DOCX, static HTML and tracker validation pass with the pinned favicon exception.
- Prose: zero mechanical errors, zero configured style findings.
- Transform: eight branding anchors, three Pals anchors and closing head verified; break tests and bit-exact output pass.
- Sources: eight stages, 27 cards, 94 hours and 22 distinct card URLs agree.
- Pals: ten placements, eight sprites, ten prose targets, payload hash and MIT checks pass.
- Sweep: original 30-URL/27×200/3×403 record passes internal checks.
- Freshness: zero entries stale beyond 90 days; **eight open gaps**, warning only.
- Aggregate fast suite: **9 passed, 1 warned, 0 failed**.
- Drift: **1 passed, 0 warned, 0 failed**; all five outputs reproduce.
- Repository unittest discovery: **5 tests, OK**.
- Browser: **13/13 widths**, **0 failures**, **no runtime errors** in tested paths.

The `docs` check printed “no stale claims,” but manual inspection found stale prose outside its limited pattern set. This report explicitly does not repeat that phrase as a repository-wide guarantee.

### 16.4 Fresh viewport measurements

| Width (CSS px) | Document width | h1 px | Tag fills observed | Footer delta px | Pals | Control-centre hits | Worst overlap px² | Result |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 320 | 320 | 35.8 | 6 | 0 | 10 | 0 | 0 | Pass |
| 360 | 360 | 35.8 | 6 | 0 | 10 | 0 | 0 | Pass |
| 390 | 390 | 35.8 | 6 | 0 | 10 | 0 | 0 | Pass |
| 430 | 430 | 35.8 | 6 | 0 | 10 | 0 | 0 | Pass |
| 600 | 600 | 39.1 | 6 | 0 | 10 | 0 | 0 | Pass |
| 620 | 620 | 40.4 | 6 | 0 | 10 | 0 | 0 | Pass |
| 700 | 700 | 45.6 | 6 | 0 | 10 | 0 | 0 | Pass |
| 900 | 900 | 58.7 | 6 | 0 | 10 | 0 | 556 | Pass |
| 1024 | 1024 | 66.8 | 6 | 0 | 10 | 0 | 555 | Pass |
| 1200 | 1200 | 78.2 | 6 | 0 | 10 | 0 | 560 | Pass |
| 1320 | 1320 | 86.1 | 6 | 0 | 10 | 0 | 557 | Pass |
| 1440 | 1440 | 91.7 | 6 | 0 | 10 | 0 | 0 | Pass |
| 1920 | 1920 | 91.7 | 6 | 0 | 10 | 0 | 0 | Pass |

Default/collapsed checks: one stage open at 320, 900 and 1440px; zero control-centre hits; worst observed overlap 0, 556 and 0px² respectively; all pass. Nonzero overlap is intentionally bounded, not hidden as a zero-overlap claim.

### 16.5 Behavioral coverage

The current harness covers:

- Source-derived card count and all outbound anchors.
- First-stage HR Essentials/TA ordering and old-state compatibility fixture.
- Link hit-testing across the 13-width matrix.
- Trusted mouse and touch-emulated activation of both playlist links at 390/1440px.
- A default, unprevented new-tab request to the HR Essentials playlist.
- A checkbox change from `0 of 27 / 0%` to `1 of 27 / 4%` and back.
- Native scroll coupling with a deliberately failing fixed-layer control.
- Ten enabled creatures, zero visible creatures when paused and zero on reduced-motion initial load.
- Decoded inline favicon colour samples.
- Basic control geometry, heading counts and skip-link presence.

Some event-activation tests prevent navigation so they can measure dispatch safely; the separate default-new-tab test preserves normal behavior. Neither establishes YouTube playback, sign-in state, mobile app handling, provider availability or success inside an embedded preview.

The suite is not a full automated export→reset→import persistence test, comprehensive notification test, multi-tab synchronization test, assistive-technology test or Safari/Firefox matrix. Do not infer those from the headline pass count.

## 17. Security, privacy, accessibility and performance

### 17.1 Trust model

The browser consumes trusted, repository-authored content and locally selected progress files. Resource text is generally created with `textContent`, and URLs are restricted to `http:`/`https:`. Outbound links use `_blank` plus `noopener noreferrer`, avoiding direct opener control and suppressing the normal referrer.

The generator escapes `<` in embedded JSON, with a vendored test proving a malicious `</script>` title cannot break out of the JSON script. This is an important narrow guarantee. It is **not** proof every HTML substitution or every authored field is safe for arbitrary untrusted content. The wrapper and generator are not a public multi-tenant publishing service.

Inline scripts and styles are a deliberate portability tradeoff. A strict host CSP that forbids inline execution would break the app unless hashes/nonces and the dynamically activated Pals scripts were carefully supported. No repository-defined hardened production header set was audited. The favicon exception is exact and does not authorize arbitrary data-URI SVG additions.

### 17.2 Privacy

There is no project-owned backend or telemetry call in the app. Progress remains browser-local and export is user-initiated. That avoids server-side storage of learner progress but also means no account recovery, cross-device sync, shared-device isolation beyond browser profiles or central backup.

The export file can disclose study behavior, dates and reminder time. It should be treated as personal local data. Clicking a provider link exposes the visit to that external site under its policies. The hosting provider necessarily processes delivery requests; “no application analytics” is not a statement about all hosting access logs.

The practice curriculum explicitly recommends fake/anonymized data rather than collecting real candidates' personal information. The app is not an ATS and should not be repurposed as one without a separate privacy and security design.

### 17.3 Dependency and code integrity

Three separate boundaries exist:

1. Skill inventory pins the entire 12-file bundle.
2. Pals config pins the engine payload, with MIT/provenance checks.
3. Builder pins the complete favicon tag.

Python and npm versions are pinned, but dependencies were not vulnerability-scanned in this audit and lock entries are not a proof of absence of vulnerabilities. The project has no recorded SBOM, signed build attestation or license inventory covering every transitive component.

`pin-skill` must remain a deliberate upgrade operation. Running it to quiet an unexpected mismatch would destroy the evidence boundary rather than fix the problem.

### 17.4 Accessibility evidence and limits

Implemented/tested features include semantic headings, native stage disclosure elements, a skip link, keyboard-operable native controls, accessible completion labels, progress ARIA values, a reminder name/title, status notices, visible focus styling, contrast-oriented colours, optional decoration and initial reduced-motion handling.

The decorative engine's Shadow DOM requires special care: ordinary outer-document selectors do not automatically reach its internal actors. Decorative custom elements are marked hidden from accessibility APIs, but a real screen-reader traversal was not recorded. The project has no automated axe report or formal WCAG certification in the available evidence.

Small chips, removal of the visible reminder label, animation, long resource titles and localised text remain usability risks. Multi-directional text, high contrast/forced-colors, text-only zoom, 200–400% zoom, portrait/landscape rotation and keyboard-only full task journeys are appropriate future manual checks.

### 17.5 Performance evidence and limits

The tracker is a compact single HTML document with no runtime framework install. Idle activation delays optional animation so core UI construction is not intentionally blocked by creature setup. All 27 cards are rendered locally; no pagination or data-fetch state exists.

No Lighthouse/Core Web Vitals, low-end-device battery test, long-session memory profile, network-throttling benchmark or production latency measurement was performed. The browser harness measures geometry and selected behavior, not load performance. A 166KB file and passing headless tests are not performance guarantees.

Absolute Pals positioning reduces the need for scroll correction, but the engine still has animation/lifecycle overhead. Long-term pause/teardown and live preference changes should be profiled, not assumed efficient.

## 18. Failure register and abandoned approaches

| Event | Observable symptom | Diagnosis/evidence | Resolution or current boundary |
|---|---|---|---|
| Portable skill intake | Executable skill absent until reconstructed | Supplied fenced transfer bundle | Extracted, validated, later vendored with inventory |
| PEP 668 | System pip refused install | Externally managed Python | Current venv/lock bootstrap; old override is historical only |
| Reset dependency loss | `docx` import and browser launch fail | Venv/npm/browser files absent | Durable bootstrap and npm harness, not repeated manual installs |
| Shallow checkout | Incomplete history made reconstruction unreliable | Shallow clone diagnosis | Full-history CI and audit unshallow fetch |
| Branch pointer mismatch | Working source and branch history diverged | Historical remote/local inspection | Fetch + mixed reset preserving work; no destructive hard reset reported |
| Skill MCP | HTTP POST access blocked | Endpoint/tool calls unavailable in sandbox | Durable registration plus catalog/GitHub-source fallback; not claimed execution |
| Provider curl | TLS/network errors, `000` | Restricted sandbox domains | Read pages through fetch tool; run sweep on GitHub |
| Dispatch attempts | HTTP 403 | Integration lacked effective Actions-write access | Owner manual dispatch; no unsafe credential request |
| `repository_dispatch` | API accepted but no run appeared | No workflow event listener | Not counted as a successful sweep; abandoned |
| Logs/artifacts | Redirected downloads blocked | Egress host restrictions; UI sign-in | Owner pasted summary; raw evidence limitation retained |
| `gh pr edit` | Projects Classic API error | Historical CLI behavior | REST PATCH workaround; no product workaround required |
| CSS cascade | Pale eyebrow/unchanged styles despite source intent | Computed styles and specificities | Explicit local overrides and computed-style tests |
| Hero shadow | Refinement produced wrong shadow edge | Visual feedback | Bottom-only pink shadow restored |
| Repeated title request | Potential double 40% scaling | Repeated wording in same requested change | Applied once, explicitly documented |
| Hero breakout ambiguity | “Remove gutter” could mean full viewport | Owner clarification | Cancel small sheet gutter only |
| Pals reuse check | First occurrence wrongly required a hue | New config checker failed | Require hue only on subsequent occurrences |
| Pals scale | Heading sprites visually too small | Scratch screenshots | Stage/footer placements increased to scale 3 and retested |
| Preview HEAD | HEAD differed from root GET mapping | Header check/directory response | Shared mapping for both methods |
| Vanished preview script | Process restart command referenced deleted cache file | Snapshot exclusions | Commit stdlib server in `tools/`, add `make preview` |
| Missing Pals after reset | Running preview served pre-Pals output | `out/` restored committed old artifact | Rebuild tracker before every preview start; marker warning |
| Browser shared libraries | Chromium failed before page load | Missing bundled runtime-library extraction | Inflate npm-provided libraries and set library path |
| Harness `EPIPE` | Piping a verbose Node run to `head` broke output | Consumer closed stdout early | Rerun complete command without truncating pipe |
| Expanded-only visual test | Missed normal first-stage-open state | Review of test setup | Added collapsed/default checks at three widths |
| Positional keys | Prepending card would misassign saved completions | Source inspection before release | Dedicated new key plus legacy mapping and fixture |
| Fixed-overlay scroll | Mobile Pals jittered/lagged | Geometry mechanism and fixed-layer control | Full-document absolute layer, not engine mutation |
| Scroll test zero delta | Test falsely showed no movement | Smooth-scroll timing | Explicit instant scroll in regression only |
| Embedded preview links | Owner couldn't activate external navigation in preview | All-link hit tests and real mouse/touch/new-tab request passed | No speculative navigation patch; external-container cause remains unproven |
| YouTube metadata error | Page payload contained error banner despite readable lessons | Fetch response ambiguity | Direct canonical playlists, explicit playback/app-handoff caveat |
| Favicon validator | Original no-link rule rejects inline favicon | Immutable validator inspection | Exact-tag temporary-copy adapter; vendor unchanged |
| Favicon dimension assertion | Expected natural size 32; Chromium gave 150 | ViewBox differs from intrinsic dimensions | Test canvas-rendered colours; exact source preserved |
| Drift false alarms | PDF/DOCX hashes change on rebuild | Container timestamps/metadata | Semantic PDF and archive-entry DOCX comparison |
| Documentation “no stale claims” | Runner passes despite outdated prose | Manual audit outside regex scope | Record contradictions; recommend stronger checks |

The common pattern is that environmental, evidence and test-design failures were not all product defects. Fixing the wrong layer—disabling TLS, editing the vendor, weakening link restrictions broadly, or shipping an unproven navigation workaround—would have made the final system less trustworthy.

## 19. Known debt and prioritized recommendations

These are recommendations, not changes implemented by the report.

### 19.1 Correctness and user-data priorities

1. **Introduce stable IDs for every stage/resource.** Preserve existing storage namespace and migrate all legacy keys with explicit fixtures. The current prepend adapter solves only one insertion; later reordering can still corrupt meaning.
2. **Harden backup validation.** Enforce version, a valid map of recognized keys and booleans, valid dates/times, a bounded file size and a deliberate unknown-key policy. Test malformed JSON, null/arrays, future versions and cross-roadmap imports.
3. **Add persistence end-to-end tests.** Complete resources, reload, export, reset, import and verify exact state including streak/time. Test blocked localStorage and save exceptions. Current tests do not cover the full journey.
4. **Replace string-derived free counts.** Model cost/access/verification separately. Distinguish free-to-study, certificate cost, trial/conditional access and partial/unconfirmed status. Rename or qualify the current `VERIFIED FREE` hero until its semantics match.
5. **Perform a production smoke test for the PR #8 favicon.** Confirm actual deployed commit, root/download routes, tab icon/cache refresh and origin-specific import/export. Owner confirmed PR #7, not a later full PR #8 matrix.

### 19.2 Content and documentation priorities

6. **Resolve the eight manifest gaps where possible.** Preserve ambiguity if pages remain inaccessible. Do not replace a failed read with a search-result price.
7. **Keep current and historical URL universes separate.** The next sweep should cover the current 31 entries and store its own timestamp/snapshot; the 30-URL first sweep must remain immutable historical evidence.
8. **Reduce duplicated content models.** Either generate JSON from an explicit structured source or compare titles, providers, cost, duration, notes and actions in addition to counts/URLs. Current checks can miss prose divergence.
9. **Fix known stale prose with a separate authorized change:**
   - `learning-library/README.md` still contains the earlier statement that the reference favicon was not copied.
   - `docs/SETUP.md` has an older editing example saying 26 cards/21 URLs and an old fixed-layer description.
   - The introductory `docs/DESIGN-SPEC.md` no-link rule predates the narrow favicon exception documented later; consolidate the final contract.
   - The long-form “first hour” still points learners toward the TA channel despite the newer HR Essentials-first card order.
   - Broad original-date access-verification wording should explicitly defer to per-entry caveats/dates.
   - Old 122px hero, 28-file/~594KB snapshot and early script-count descriptions belong to historical snapshots, not current-state summaries.
10. **Strengthen documentation checks.** Check current file examples and structured metadata, and make “no stale claims” output less absolute. Hand-maintained narrative cannot be exhaustively verified by a few regexes.

### 19.3 Runtime and UX priorities

11. Test real iOS Safari, Android Chrome and desktop Firefox/Safari, especially YouTube app handoff, notifications, localStorage, downloads and touch/scroll behavior.
12. Review the small chip typography and hidden visible reminder label with actual users. Accessible names are necessary but not a complete readability solution.
13. Add screen-reader/keyboard audits, zoom/reflow/forced-colors checks and a live reduced-motion preference test.
14. Profile creature CPU/battery use, pause teardown and long sessions. If needed, add a public lifecycle adapter rather than modifying the pinned engine casually.
15. Consider multi-tab state coordination only if required. There is no `storage`-event reconciliation; concurrent tabs can overwrite each other's latest state. Do not promise sync.

### 19.4 Build and supply-chain priorities

16. Make bootstrap sensitive to lock changes or add an explicit environment-refresh target. The current file-target approach can leave an existing venv stale.
17. Pin GitHub actions to commit SHAs if the project's risk policy requires it; add dependency/vulnerability and licensing review.
18. Consider hash-enforced Python installation and documented OS/browser environment constraints. Pinned versions alone do not freeze package-host supply chains.
19. If the skill is upgraded, review all eight branding anchors, three Pals anchors, key shim and favicon adapter. Never run `pin-skill` merely to bless an unexplained mutation.
20. Add a visual PDF snapshot/manual review step if exact pagination matters. Extracted text equality does not prove visual layout equality.
21. Normalize curl transport failures in `check-links.sh`. The current command captures curl’s own `000` plus fallback `echo 000`, so some failures can become `000000` instead of one normalized code. Keep reporting nonblocking, but distinguish transport failure from an HTTP status explicitly.

### 19.5 Scope control

Accounts, a backend, cloud synchronization, push notifications, an ATS, payment flow and a CMS were not user requirements. Do not add them merely to remove the limitations of a deliberately local static product. Each would substantially change cost, privacy, hosting, operational and security responsibilities.

## 20. Maintenance, release and incident runbooks

### 20.1 Clean development setup

```sh
# Repository root; Python 3.11 + venv support, make, Bash and Node 22.22.3
make bootstrap
make ci
python3 -m unittest discover -s tools -p 'test_*.py' -v
make check-visual
```

If `.venv` exists but dependencies are stale, intentionally recreate it or run `.venv/bin/python -m pip install -r requirements.lock` before retrying. Avoid system-pip overrides. npm/browser caches can be discarded and recreated; do not commit them.

### 20.2 Content update

1. Read the relevant provider page and record what was actually verified.
2. Update long-form Markdown and corresponding JSON, including actions and caveats.
3. Update current URL script/manifest if destinations change.
4. Do not rewrite previous sweep snapshots as if they included new URLs.
5. Preserve keys for existing resources, or design/test a migration before inserting/reordering.
6. Regenerate with `make build`.
7. Run fast, drift, repository and browser tests.
8. Read the affected output sections and PDF/DOCX pages.
9. Review `git diff --check`, changed generated files and research claims.
10. Record outstanding uncertainty; do not bump verified dates without a read.

### 20.3 Theme or Pals update

Edit `fieldnotes-theme.css`, `pals.css`, `pals-controller.js` or `pals.json` as appropriate, never output-only HTML or engine payload. Rebuild tracker; run contracts, drift and browser checks. Check all default and expanded states. Pay special attention to links, time input, checkbox labels, stage summaries and control centres near creature canvases.

A theme change can inadvertently shift anchor geometry without changing Pals config. A content title change can do the same. Treat visual QA as relevant to both.

### 20.4 Vendor upgrade

Save the old inventory/payload reference, review upstream provenance and license, update intentionally, regenerate inventories only after review, and inspect every failed contract. Run vendor smoke tests and project tests. Update documentation if upstream markup assumptions change. Preserve backward-compatible saved progress.

### 20.5 Preview recovery after reset

- Confirm current branch and source files before rebuilding.
- Use `make preview` in a long-lived process.
- Verify root maps to tracker, GET and HEAD agree, and the served file includes Pals/favicons expected for the baseline.
- If the port is stale, stop the known process rather than repeatedly launching duplicates.
- A missing venv is not a blocker for tracker-only preview; document generation still needs bootstrap.

### 20.6 Research sweep

Prefer GitHub Actions if provider egress is blocked locally. Manually dispatch `link-check` through an authorized account or wait for the schedule. Inspect the TSV and provider pages, not only the conclusion. Record exact URL snapshot, statuses, timestamp and run link. Non-2xx needs explanation; 2xx needs content/access review before claims change.

If logs/artifacts are unavailable, ask the owner for the summary without credentials or signed URLs and clearly annotate the reduced evidence. Never report a dispatch attempt or a diagnostic event as a completed run.

### 20.7 Release process

1. Follow the user's approval boundary before commands/changes and before Git operations.
2. Stay on the assigned session branch; verify `git status` and diff.
3. Run equivalent CI coverage, not only `make ci`.
4. Commit/push only when authorized, create a PR from the session branch and review checks.
5. Merge the explicit PR number with the selected merge strategy; do not obscure the merge exit status.
6. Confirm PR `MERGED`, remote main hash and merge checks.
7. Verify production routes, downloads, progress compatibility, new-tab behavior, mobile scrolling and favicon separately.
8. Preserve exported test data if changing domains; do not erase owner progress during a smoke test.

### 20.8 Rollback

Because production publishes committed outputs, the rollback unit is the known-good repository/artifact revision, not a live application server restart. Use a deliberate revert PR or hosting rollback after approval. Consider persistence semantics: reverting a resource insertion can leave unknown keys in local state; they should not be reassigned to unrelated resources.

No rollback was exercised during this audit. This is a proposed operating procedure based on the current static architecture.

## 21. Work deliberately not done

For completeness, the available evidence does **not** establish:

- Paid enrolment, logged-in course completion or purchase verification.
- A free certificate from every “free” learning provider.
- A professional qualification earned by following the plan.
- Independent confirmation of LinkedIn prices.
- A legal opinion on all Nigerian recruitment/privacy requirements.
- A full reading of every long guide or every legal PDF page.
- A raw artifact-backed reconstruction of the first HTTP sweep.
- Successful MCP execution merely because MCP registration exists.
- Original screenshot preservation or exact visual replay of every interim design.
- A complete physical-device/browser compatibility matrix.
- Confirmed root cause of embedded-preview new-tab failure.
- Background/closed-tab notifications or a service worker.
- Account-based persistence, multi-device sync or recovery after browser data deletion.
- Full schema validation of arbitrary progress files.
- Complete CPU teardown when decorative Pals are paused.
- Formal WCAG, security, privacy, licensing or performance certification.
- Independent production browsing or hosting-account audit during this report.
- Owner verification of the final live favicon after PR #8.
- A report commit, push, PR or merge; those require a separate instruction.

These exclusions are part of the engineering result. They prevent a future maintainer from interpreting historical confidence or a passing suite as coverage the project never had.

## 22. Evidence and source index

### Primary internal sources

- [Root README](../README.md): project entry point and checks.
- [Library README](../learning-library/README.md): outputs and content orientation; contains historical prose caveats noted above.
- [Changelog](../CHANGELOG.md): incremental decisions and actual checks recorded during work.
- [Retrospective](../RETROSPECTIVE.md): early diagnosis, failed approaches and remediation.
- [Setup](SETUP.md): developer commands and architecture notes.
- [Current design spec](DESIGN-SPEC.md): intended current visual contract, with later compatibility/favicon sections.
- [Historical design record](../learning-library/DESIGN-SYSTEM.md): original reference port and four refinements.
- [Deployment guide](DEPLOYMENT.md): static hosting and smoke procedures.
- [Long-form content](../learning-library/src/recruiter-talent-acquisition-library.md).
- [Tracker content JSON](../learning-library/src/roadmap-app.json).
- [Verification manifest](../learning-library/src/verification-manifest.json).
- [Tracker builder](../learning-library/tools/build_tracker.py).
- [Fast/drift verification runner](../tools/check.py).
- [Browser harness](../tools/visual/visual_check.mjs).
- [Third-party notices](../THIRD-PARTY-NOTICES.md).

### External project/provenance evidence

- Product repository and PRs: <https://github.com/MikkoWuyin-dev/FieldNotes-HR> (each PR linked in Appendix A).
- Visual source: <https://github.com/MikkoWuyin-dev/Field-Notes_Nature-Photography>.
- Engine source: <https://github.com/diiviikk5/Piixpal>.
- Discovery catalog reviewed during report: <https://skill-issue.in/?skill=design-web-design-guidelines>.
- First sweep: <https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40471064309>.
- Latest merge verification: <https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40485000208>.
- Production address supplied by owner: <https://fieldnotes-hr.vercel.app/>.

Provider URLs and exact per-entry findings are reproduced in Appendices B/C. The report does not use bare successful requests as access citations; it retains the original verification dates and caveats. External source descriptions here reflect the historical reads or repository metadata identified above, not a newly completed provider review.

---

## Appendix A — PR and commit ledger

### A.1 All eight pull requests

All are merged into `main`. File/addition/deletion counts are GitHub PR totals, not unique repository-wide totals; generated artifacts and files touched by several PRs contribute repeatedly.

| PR | GitHub title | Source branch | Merge time (UTC) | Merge hash | Files | Additions | Deletions |
|---|---|---|---|---|---:|---:|---:|
| [#1](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/1) | Vendor resource-learning-library skill and add recruiter learning library | `arena/19ef6871-fieldnotes-hr` | 2026-10-26T17:30:04Z | `6b33fb5` | 23 | 4188 | 0 |
| [#2](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/2) | Restyle roadmap tracker with Fieldnotes design system | `arena/788290da-fieldnotes-hr` | 2026-10-26T22:58:25Z | `fd7c568` | 9 | 1427 | 13 |
| [#3](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/3) | Make builds reproducible: retrospective, pinned environment, CI and verification | `arena/bd812372-fieldnotes-hr` | 2026-10-26T23:50:29Z | `e2c6dce` | 24 | 2651 | 87 |
| [#4](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/4) | Add ten decorative Pals to the tracker and make previews reproducible | `arena/833b18a5-fieldnotes-hr` | 2026-10-27T07:20:03Z | `0a3f440` | 19 | 1388 | 45 |
| [#5](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/5) | Record first link sweep results and refresh library verification notes | `arena/46f91e1e-fieldnotes-hr` | 2026-10-27T08:36:39Z | `8f18a91` | 13 | 167 | 34 |
| [#6](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/6) | Configure static Vercel deployment | `arena/f5ea4032-fieldnotes-hr` | 2026-10-27T08:42:50Z | `c035742` | 6 | 115 | 0 |
| [#7](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/7) | Fix mobile layout, playlist destinations and Pals scrolling | `arena/3f0257c3-fieldnotes-hr` | 2026-10-27T09:44:46Z | `d469e5d` | 17 | 324 | 80 |
| [#8](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/8) | Match Nature Photography favicon | `arena/ca8cd9c8-fieldnotes-hr` | 2026-10-27T09:59:30Z | `765f2e2` | 10 | 146 | 10 |

### A.2 All reachable commits at the audited baseline

This is the chronological reachable history ending at the audited commit: **19 commits**, including the initial commit and eight merge commits. Times below normalize the Git **committer** timestamp to UTC; PR merge times above come from GitHub and can differ by one second. The current report is not part of this history.

| Commit | Committer time (UTC) | Subject |
|---|---|---|
| [`c4d1470`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/c4d1470a9da2489f68cdaf225f5b7f1adeaba869) | 2026-10-26T09:24:35Z | Initial commit |
| [`600c9bf`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/600c9bff8b6e1bd5da941f094ac18690498a79b9) | 2026-10-26T17:22:25Z | Vendor resource-learning-library skill and add recruiter learning library |
| [`6b33fb5`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/6b33fb5d6137831304f230a5e98a0f709dad3c3a) | 2026-10-26T17:30:04Z | Merge pull request #1 from MikkoWuyin-dev/arena/19ef6871-fieldnotes-hr |
| [`e18975b`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/e18975b9515fe4a84998d3b6047faea8e8dda228) | 2026-10-26T19:49:13Z | Restyle roadmap tracker with Fieldnotes design system and register skill MCP |
| [`72cd11c`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/72cd11c200c64360137e76b1f3dd9794802409c9) | 2026-10-26T22:53:59Z | Refine Fieldnotes tracker: tags, stage headers, hero scale and rhythm |
| [`fd7c568`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/fd7c568e2112518ed013a01d05ee74aa7f02b04b) | 2026-10-26T22:58:25Z | Merge pull request #2 from MikkoWuyin-dev/arena/788290da-fieldnotes-hr |
| [`28043e6`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/28043e6d4fc9d6c4068a593dad4790d10701f620) | 2026-10-26T23:43:14Z | Make builds reproducible: retrospective, pinned env, CI and verification |
| [`0defd24`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/0defd246b5a13049886aedee2b2eaa88d0571afe) | 2026-10-26T23:46:07Z | Update retrospective and changelog: CI verification now observed |
| [`e2c6dce`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/e2c6dce25359715ca525589bd76b1b9e953939df) | 2026-10-26T23:50:29Z | Merge pull request #3 from MikkoWuyin-dev/arena/bd812372-fieldnotes-hr |
| [`a51c6b9`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/a51c6b99d391c45544dd8dbb18880c8f22580317) | 2026-10-27T07:10:55Z | Add ten Piixpal decorative pals and make previews reproducible |
| [`0a3f440`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/0a3f4406259b9210bb413a08ca20792a2d3eadb1) | 2026-10-27T07:20:02Z | Merge pull request #4 from MikkoWuyin-dev/arena/833b18a5-fieldnotes-hr |
| [`53111de`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/53111dee367667bd2cce85086bca54aa9b2980cd) | 2026-10-27T08:32:01Z | Record first link sweep results and refresh library verification notes |
| [`8f18a91`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/8f18a912c561ef0f99915dca26f7db9e42e624ea) | 2026-10-27T08:36:38Z | Merge pull request #5 from MikkoWuyin-dev/arena/46f91e1e-fieldnotes-hr |
| [`103673d`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/103673d633e5c368da2261664c70481e7f437d19) | 2026-10-27T08:42:14Z | Configure static Vercel deployment and test publishing contract |
| [`c035742`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/c03574243a3110573f74d6a03681268f86e4bd5c) | 2026-10-27T08:42:50Z | Merge pull request #6 from MikkoWuyin-dev/arena/f5ea4032-fieldnotes-hr |
| [`f003cb0`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/f003cb00f24f75cf851ac16c7c5c533c2746df06) | 2026-10-27T09:44:07Z | Fix mobile hero and Pals scroll alignment; add direct HR playlists |
| [`d469e5d`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/d469e5d41b09c308cac34388b718dc38e4fed3f9) | 2026-10-27T09:44:45Z | Merge pull request #7 from MikkoWuyin-dev/arena/3f0257c3-fieldnotes-hr |
| [`f332ef9`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/f332ef9c44dd67c4d5916d561900a20b8efb5996) | 2026-10-27T09:58:26Z | Match Nature Photography favicon with pinned inline SVG validation |
| [`765f2e2`](https://github.com/MikkoWuyin-dev/FieldNotes-HR/commit/765f2e2b672e7ae04a0137133c2028d48cb70357) | 2026-10-27T09:59:30Z | Merge pull request #8 from MikkoWuyin-dev/arena/ca8cd9c8-fieldnotes-hr |

### A.3 Reporting branch

The current reporting branch is `arena/8c02879a-fieldnotes-hr`, based on the PR #8 merge. Historical branches in the table identify earlier sessions; they are not instructions to switch branches. No additional product commit or unmerged implementation PR existed in the inspected baseline.

## Appendix B — complete current roadmap catalog

The following is a field-level transcription of the structured roadmap at the audited baseline, not a fresh provider verification. It preserves all 27 cards, stage descriptions/outcomes, costs, study allocations, rationale, next actions and access notes so that content decisions can be reviewed without guessing from counts. The long-form source contains additional teaching narrative, practice assignments, paid extras and exclusions discussed in Section 6.

**Tracker title:** Zero to Recruiter: a Talent Acquisition roadmap  
**Subtitle:** An 8-stage path for an absolute beginner in Lagos, Nigeria. About 5 hours a week. Free resources first; paid options are marked and listed separately in the library document.  
**Reminder default:** `19:00`  
**Stable storage ID:** `rll-recruiter-ta-2026-10-26`

### B.1 Stage 1: Orientation - what a recruiter actually does

**Schedule:** Weeks 1-2; **stage budget:** 8 hours; **cards:** 4.

Learn the hiring lifecycle end to end, the vocabulary of talent acquisition, and where the recruiter fits alongside hiring managers. No prior HR knowledge assumed.

**Outcomes:**

- Describe the stages from workforce planning to onboarding
- Name the common recruiter roles and the difference between agency and in-house recruiting
- Explain why hiring decisions should be based on defined criteria rather than gut feel

#### B.1.1 The HR Learning Lab: HR Essentials (video playlist)

- **Provider:** HR Learning Lab (YouTube)
- **Destination:** <https://www.youtube.com/playlist?list=PLeDNHX61_qlQeRK1_i5flRpz2T0wjQXN2>
- **Format:** Free video series
- **Cost/access label:** Free
- **Card study allocation:** 1 hour for starter lessons and notes (study budget)
- **Content-check date shown on card:** 2026-10-27
- **Manifest status:** `confirmed`
- **Persisted completion key:** `hr-essentials-v1`
- **Link label:** Open the playlist
- **Why included:** Start with what HR does, the employee life cycle and the wider HR profession before specialising in talent acquisition.
- **Next action:** Watch lessons 1-4, then sketch the employee life cycle and explain where recruitment fits. Use remaining study time for notes and review.
- **Access/verification note:** Checked 2026-10-27: public HR Essentials playlist, 16 listed videos; description and initial lesson titles readable without sign-in. The fetch also exposed a YouTube error banner, so playback and mobile app handoff remain untested. Content developed by Dr. Heather Staples; videos produced using AI-supported tools. This is introductory study, not a professional qualification.

#### B.1.2 The HR Learning Lab: Talent Acquisition (video playlist)

- **Provider:** HR Learning Lab (YouTube)
- **Destination:** <https://www.youtube.com/playlist?list=PLeDNHX61_qlQWYcxZNB19TDOKbl625W2c>
- **Format:** Free video series
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours of selected lessons and notes (study budget)
- **Content-check date shown on card:** 2026-10-27
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s0-r0`
- **Link label:** Open the playlist
- **Why included:** Short, beginner-oriented lessons on job analysis, workforce planning, recruiting, selection and hiring practice. The fastest way to hear the vocabulary before reading heavier material.
- **Next action:** Watch the first five lessons and write a one-page diagram of the hiring lifecycle in your own words.
- **Access/verification note:** Checked 2026-10-27: public Talent Acquisition playlist, 43 listed videos, description and lesson titles readable without sign-in; playback and mobile app handoff not tested. Creator discloses AI-supported production; confirm consequential claims against primary sources.

#### B.1.3 PRDV226: Introduction to Human Resource Management

- **Provider:** Saylor University
- **Destination:** <https://learn.saylor.org/course/view.php?id=1292>
- **Format:** Written course with lectures and videos
- **Cost/access label:** Free, with a free completion certificate
- **Card study allocation:** About 14 hours for the whole course
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s0-r1`
- **Link label:** Open the course
- **Why included:** Units 1 and 2 cover where the right people are and how to recruit and keep quality employees. It gives the structured foundation the shorter videos skip.
- **Next action:** Work through Units 1 and 2 this fortnight; come back for Units 3 and 4 in Stage 2.
- **Access/verification note:** Verified 2026-10-26 on the course syllabus and the Saylor FAQ: no tuition or fees, all materials free, free course completion certificate at 70 percent on the final exam. A free account is needed for assessments and the exam. Only the proctored college-credit route carries a fee; you do not need it for the free certificate.

#### B.1.4 Principles of Management, Chapter 11: Human Resource Management

- **Provider:** OpenStax (Rice University)
- **Destination:** <https://openstax.org/books/principles-management/pages/11-introduction>
- **Format:** Free peer-reviewed textbook
- **Cost/access label:** Free
- **Card study allocation:** About 1 hour for the introduction and section 11.1
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s0-r2`
- **Link label:** Read Chapter 11
- **Why included:** A university-level explanation of how HR became a strategic function and what talent acquisition is for. Useful when you need the reasoning, not just the steps.
- **Next action:** Read the chapter introduction and 11.1; note three ways HR creates value that you can repeat in an interview.
- **Access/verification note:** Verified 2026-10-26: free openly licensed textbook, readable in web view. US-oriented examples; treat the legal sections as context, not Nigerian law.

### B.2 Stage 2: Foundations - fair process, job roles and the law

**Schedule:** Weeks 3-5; **stage budget:** 14 hours; **cards:** 4.

Build the ground rules: equal opportunity, job and person requirements, the recruitment and selection sequence, and the legal duties that apply when handling candidate information in Nigeria.

**Outcomes:**

- Run a full and fair recruitment and selection process step by step
- Separate job requirements from person specifications
- Recognise the basic compliance duties that apply to candidate data in Nigeria

#### B.2.1 Human resources: recruitment and selection

- **Provider:** The Open University (OpenLearn)
- **Destination:** <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0>
- **Format:** Free written course with activities
- **Cost/access label:** Free, with a free statement of participation
- **Card study allocation:** 12 hours
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s1-r0`
- **Link label:** Open the free course
- **Why included:** The single best free beginner course for the actual sequence: job analysis, job description, person specification, attracting applicants, advertising, shortlisting and references. It is the spine of this stage.
- **Next action:** Complete sections 4.2 to 4.5 and draft a job analysis for one real Lagos vacancy you find online.
- **Access/verification note:** Verified 2026-10-26 on the provider course page: free course, free statement of participation; a free account is needed to track progress, claim the statement and open all quizzes and activities. Course content was last updated in 2018 and uses UK equality-law framing - pair it with the Nigerian sources in Stage 7.

#### B.2.2 Diploma in Human Resources (HR)

- **Provider:** Alison
- **Destination:** <https://alison.com/course/diploma-in-human-resources-hr>
- **Format:** Free video diploma course
- **Cost/access label:** Free to study; the optional certificate costs extra
- **Card study allocation:** 10-15 hours
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s1-r1`
- **Link label:** Open the course
- **Why included:** A video-led alternative to the text-heavy OpenLearn course. It covers the key skills and responsibilities of HR, recruitment and selection, and employee separation.
- **Next action:** Use it for revision: watch the recruitment and selection modules and compare the sequence with OpenLearn section 4.
- **Access/verification note:** Verified 2026-10-26 on Alison's help centre and certification page: all courses are free to study and complete; a paid digital or printed certificate is optional and a free Learner Record is available instead. The provider page did not show an exact certificate price, so I am not quoting one. Alison lists 15 free recruitment courses on its recruitment tag page.

#### B.2.3 BUS301: Human Resource Management

- **Provider:** Saylor University
- **Destination:** <https://learn.saylor.org/course/BUS301>
- **Format:** Written course with lectures and videos
- **Cost/access label:** Free, with a free completion certificate
- **Card study allocation:** About 24 hours for the full course
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s1-r2`
- **Link label:** Open the course
- **Why included:** A deeper follow-on to PRDV226 with strategic HR planning, staffing, compliance and labour relations. Use selected units rather than the whole course if you are short on time.
- **Next action:** Read the staffing and recruitment/selection units only; skip performance and compensation units until you are job hunting.
- **Access/verification note:** Verified 2026-10-26 via the Saylor FAQ and course syllabus: no tuition or fees, free final exam and free completion certificate. The US employment-law material is not Nigerian law.

#### B.2.4 Recruiting, Hiring, and Onboarding Employees (audit option)

- **Provider:** University of Minnesota on Coursera
- **Destination:** <https://www.coursera.org/learn/recruiting-hiring-onboarding-employees>
- **Format:** University video course
- **Cost/access label:** Paid or conditional - not counted as confirmed free
- **Card study allocation:** About 2 weeks at 10 hours a week (about 20 hours)
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `ambiguous`
- **Persisted completion key:** `s1-r3`
- **Link label:** Check the enrolment options
- **Why included:** The syllabus is a strong match for this roadmap: workforce planning, job analysis, legal selection, sourcing, hiring analytics and onboarding. Four modules with 14 videos in module 1 alone.
- **Next action:** Only consider it after the free stages. Try to select the Full Course, No Certificate option if it is offered to you, then decide whether the certificate is worth paying for.
- **Access/verification note:** NOT counted as confirmed free. Verified 2026-10-26: the course page shows an 'Enroll for free' button and 'Included with Coursera Plus', but the same page's FAQ says that to access course materials you need to purchase the Certificate experience, start a Free Trial, or use a Full Course, No Certificate option where available. I could not confirm that the no-certificate option is offered for this course. Financial aid is mentioned in the FAQ. Prices vary by region and promotion; check the page before enrolling.

### B.3 Stage 3: Define the role - job analysis, descriptions and success criteria

**Schedule:** Weeks 6-7; **stage budget:** 10 hours; **cards:** 3.

Before sourcing anyone, learn to work out what the job actually requires and what good evidence of it looks like. Most bad hiring starts here.

**Outcomes:**

- Turn a vague request into a written job description and person specification
- Define measurable hiring attributes before speaking to candidates
- Build a simple scorecard that every interviewer can use

#### B.3.1 ONET OnLine (Occupational Information Network)

- **Provider:** US Department of Labor
- **Destination:** <https://www.onetonline.org/>
- **Format:** Free official occupational database
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours to explore one occupation properly
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s2-r0`
- **Link label:** Search occupations
- **Why included:** Over 1,000 occupation profiles with tasks, skills, knowledge and work activities. It teaches you how to derive requirements from the work itself instead of copying a competitor's advert.
- **Next action:** Look up one role you want to recruit for, export the task list, and highlight the five tasks a new hire must do in month one.
- **Access/verification note:** Verified 2026-10-26: free public database, 1,016 occupation titles listed on the site, no login seen. It is US data, so use it to learn the method of job analysis, then validate duties against Nigerian job adverts.

#### B.3.2 HR templates: job descriptions, interview kits and email templates

- **Provider:** Workable
- **Destination:** <https://resources.workable.com/hr-templates/>
- **Format:** Free official templates and guides
- **Cost/access label:** Free
- **Card study allocation:** 1-2 hours to adapt a template
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s2-r1`
- **Link label:** Browse the free templates
- **Why included:** More than 1,000 free job descriptions, 390-plus interview kits, 50-plus recruiting email templates, onboarding checklists and Boolean cheatsheets. Good raw material once you understand the structure.
- **Next action:** Rewrite one downloaded job description so that every requirement maps to a task you identified in ONET. Delete anything you cannot defend.
- **Access/verification note:** Verified 2026-10-26 on the provider templates index: templates are described as free to download. The page also advertises a separate 15-day free trial of the paid Workable software; you do not need the trial to use the templates. Templates are generic and US/UK flavoured - localise pay, notice and leave wording.

#### B.3.3 Structured hiring: Introduction (with free worksheets)

- **Provider:** Greenhouse Support
- **Destination:** <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction>
- **Format:** Free official process documentation
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours including the worksheets
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s2-r2`
- **Link label:** Read and download
- **Why included:** Sets out the six-step structured hiring process: role kick-off, scorecard definition, interview planning, interview kit, sourcing and interviewing, and candidate round-up. It makes you define success before you search.
- **Next action:** Download the linked worksheet and build a scorecard for your practice role with no more than six attributes.
- **Access/verification note:** Verified 2026-10-26 on the provider support article: the article and its two downloadable PDFs (a structured interview worksheet about 4 MB and an interactive eBook about 9 MB) are available without a login. The document is product documentation but the method transfers to any hiring process.

### B.4 Stage 4: Find people - sourcing, Boolean search and candidate experience

**Schedule:** Weeks 8-10; **stage budget:** 14 hours; **cards:** 4.

Learn where candidates are, how to search for them, how to write outreach that gets replies, and how to treat people well while doing it.

**Outcomes:**

- Build Boolean search strings for a real role
- Compare job boards, referrals, pipelines and direct search
- Write a short outreach message and a simple candidate experience plan

#### B.4.1 Boolean search cheatsheets for sourcing

- **Provider:** Workable
- **Destination:** <https://resources.workable.com/boolean-search-cheatsheets/>
- **Format:** Free written cheat sheets
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours to practise
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s3-r0`
- **Link label:** Open the cheatsheets
- **Why included:** Role-specific Boolean strings show you how brackets, quotes, AND, OR and NOT actually work when searching for people. This is the core craft skill of sourcing.
- **Next action:** Take one cheatsheet, rebuild its string for a Lagos-based role, and run it in a free search engine. Save ten plausible profiles and note why each matched.
- **Access/verification note:** Verified 2026-10-26 on the provider page: the cheatsheets are free with no account or payment shown. Most examples target technical and sales roles; adapt the keywords for Nigerian job titles.

#### B.4.2 Talent Sourcing Strategies (video 16)

- **Provider:** HR Learning Lab (YouTube)
- **Destination:** <https://www.youtube.com/watch?v=yMnw_2VNOVE>
- **Format:** Free video lesson
- **Cost/access label:** Free
- **Card study allocation:** 7 minutes
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s3-r1`
- **Link label:** Watch the lesson
- **Why included:** A quick tour of employer branding, referrals, job boards, pipelines, CV mining and job fairs, plus the growth-mindset argument for looking past job titles.
- **Next action:** After watching, pick two sourcing channels that fit a small Lagos employer and explain why you skipped the others.
- **Access/verification note:** Verified 2026-10-26: public video, no payment shown. Content developed by Heather Staples, PhD, SPHR, SHRM-SCP; the description states the videos are produced using AI-supported tools. Useful as an overview, not as a primary authority.

#### B.4.3 Google re:Work guides (hiring set)

- **Provider:** Google re:Work
- **Destination:** <https://rework.withgoogle.com/intl/en/guides/>
- **Format:** Free official practice guides
- **Cost/access label:** Free
- **Card study allocation:** About 3 hours across the relevant guides
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s3-r2`
- **Link label:** Open the guides index
- **Why included:** The index lists 23 free guides. The hiring ones cover creating a job description, reviewing resumes, shaping candidate experience, structured interviewing, interviewer training, hiring committees and onboarding. They are the closest thing to an open playbook from a major employer.
- **Next action:** From the index, open Shape the candidate experience and note three changes you would make to a typical Nigerian recruitment process.
- **Access/verification note:** Verified 2026-10-26 on the provider guides index: 23 guides listed with step and tool counts, no login or payment shown. Individual guides were not all opened; the structured interviewing and interviewer training guides were read directly. Google's data is from its own workforce, not Nigerian employers.

#### B.4.4 Jobberman free employer listing (practice channel)

- **Provider:** Jobberman Nigeria
- **Destination:** <https://www.jobberman.com/employer/free-listing>
- **Format:** Free job board and applicant tracking tool
- **Cost/access label:** Free listing; paid tiers exist
- **Card study allocation:** 1-2 hours to set up a practice advert
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `partial`
- **Persisted completion key:** `s3-r3`
- **Link label:** Check the free listing
- **Why included:** A Nigeria-specific channel where you can see how local employers write adverts and how applicants are sorted. Useful for practising without spending money.
- **Next action:** Draft and save a practice advert for your Stage 3 role. Do not publish a real vacancy without authorisation.
- **Access/verification note:** Partially verified on 2026-10-26: the provider page returned only a cookie banner when I retrieved it, so I could not read the full terms. The free-listing claim comes from Jobberman's own search listing, which describes free job posting, CV sorting and an ATS. Confirm current terms, eligibility and any limits before relying on it.

### B.5 Stage 5: Screen and shortlist - reading CVs against criteria

**Schedule:** Weeks 11-12; **stage budget:** 10 hours; **cards:** 3.

Turn a pile of applications into a defensible shortlist. Practice consistent screening before you ever speak to a candidate.

**Outcomes:**

- Screen a CV against the scorecard instead of against your impressions
- Write a short phone-screen script with the same questions for everyone
- Record evidence for rejections in a way you can defend

#### B.5.1 Google re:Work guide: Review resumes

- **Provider:** Google re:Work
- **Destination:** <https://rework.withgoogle.com/intl/en/guides/>
- **Format:** Free official practice guide
- **Cost/access label:** Free
- **Card study allocation:** About 1 hour
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s4-r0`
- **Link label:** Open the guides index
- **Why included:** A five-step guide to screening for qualifications, consistency and impact. It gives you an explicit standard, which is what most beginner screeners lack.
- **Next action:** From the guides index, open Review resumes. Then screen ten practice CVs and write one line of evidence for each decision.
- **Access/verification note:** Verified 2026-10-26 on the provider guides index, where Review resumes is listed as a five-step guide. I did not open the individual guide page, so the exact steps were not read. No login or payment shown on the index.

#### B.5.2 Greenhouse guidance library (screening and interviewing)

- **Provider:** Greenhouse
- **Destination:** <https://www.greenhouse.com/guidance>
- **Format:** Free official articles, eBooks and worksheets
- **Cost/access label:** Free
- **Card study allocation:** 2-3 hours browsing and reading
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s4-r1`
- **Link label:** Open the guidance hub
- **Why included:** Filterable by topic, including interviewing, candidate experience, DE and I, and recruiter tips. It shows how a hiring-software company explains screening problems to recruiters.
- **Next action:** Read one interviewing article and one bias-related article, then add two bias checks to your Stage 3 scorecard.
- **Access/verification note:** Verified 2026-10-26 on the provider guidance hub: articles, eBooks, webinars and worksheets listed as free resources. Some gated items such as the 2026 hiring benchmarks report may require a form; treat those as unverified for free access. Content is vendor marketing as well as guidance.

#### B.5.3 OpenLearn section 4.10: Shortlisting (revisit)

- **Provider:** The Open University (OpenLearn)
- **Destination:** <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0>
- **Format:** Free written course section
- **Cost/access label:** Free
- **Card study allocation:** About 1 hour
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s4-r2`
- **Link label:** Return to the course
- **Why included:** Rather than a new course, return to the shortlisting section of the Stage 2 course now that you have a real scorecard. It connects fair selection criteria to paperwork and references.
- **Next action:** Re-read 4.10 to 4.12 and compare its shortlisting method with your Stage 3 scorecard. Note one conflict and how you would resolve it.
- **Access/verification note:** Same free course as Stage 2; no separate card or extra cost. Verification details are in the Stage 2 card.

### B.6 Stage 6: Interview and decide - structured interviewing in practice

**Schedule:** Weeks 13-15; **stage budget:** 16 hours; **cards:** 3.

Learn the highest-value skill in this roadmap: asking the same well-designed questions and scoring answers against a written rubric.

**Outcomes:**

- Write behavioural and hypothetical questions tied to defined attributes
- Build a rubric that distinguishes poor, borderline, solid and outstanding answers
- Run a mock interview and score it independently of a partner

#### B.6.1 A guide to structured interviewing for better hiring practices

- **Provider:** Google re:Work
- **Destination:** <https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices>
- **Format:** Free official practice guide
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s5-r0`
- **Link label:** Read the guide
- **Why included:** The most important single document in this library. Updated in March 2026, it explains the four parts of structured interviewing, how to define hiring attributes, how to draft questions and follow-ups, and how to score with a shared rubric.
- **Next action:** Write eight questions for your practice role: four behavioural and four hypothetical, each mapped to a scorecard attribute. Add what a poor and an outstanding answer would sound like.
- **Access/verification note:** Verified 2026-10-26 by reading the provider page: marked Updated March 2026, free, no login or payment shown. Google reports these results from its own hiring data; the method is widely supported by research, but the specific numbers are not a promise for your context.

#### B.6.2 Effective interviewer training for better candidate experiences

- **Provider:** Google re:Work
- **Destination:** <https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences>
- **Format:** Free official practice guide
- **Cost/access label:** Free
- **Card study allocation:** About 1 hour
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s5-r1`
- **Link label:** Read the guide
- **Why included:** Shows how to write useful interview feedback, avoid vague comments and personality judgements, and leave time for candidate questions. This is what makes a rubric work in a real panel.
- **Next action:** After your mock interview, rewrite your feedback using the guide's rules and check whether a stranger could reconstruct the evidence.
- **Access/verification note:** Verified via the provider's own page content returned in search results on 2026-10-26; the guide is part of the same free re:Work set. The page itself was not opened directly, so individual steps were not fully read.

#### B.6.3 Reuse: Greenhouse structured hiring introduction and Workable interview kits

- **Provider:** Greenhouse and Workable
- **Destination:** <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction>
- **Format:** Free official templates and process docs
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s5-r2`
- **Link label:** Reopen the worksheets
- **Why included:** You already have these from Stage 3. The Greenhouse worksheet turns your questions into an interview plan; the Workable kits show how commercial teams package questions by stage.
- **Next action:** Assemble a one-page interview kit: purpose, attributes, questions, scoring anchors and a recommendation field.
- **Access/verification note:** No new resource or cost. Verification details are in the Stage 3 cards.

### B.7 Stage 7: Offer, onboarding and the law in Nigeria

**Schedule:** Weeks 16-17; **stage budget:** 10 hours; **cards:** 3.

Close the loop: references, offers, onboarding, and the two legal areas that a Lagos-based recruiter will meet immediately - data protection and employment law.

**Outcomes:**

- Explain the lawful bases for processing candidate data under Nigerian law
- Draft a short candidate privacy notice
- Read the recruiting provisions of the Labour Act and know when to escalate to a lawyer

#### B.7.1 Nigeria Data Protection Act 2023: General Application and Implementation Directive (GAID) 2025

- **Provider:** Nigeria Data Protection Commission (NDPC)
- **Destination:** <https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf>
- **Format:** Free primary legal guidance (official PDF)
- **Cost/access label:** Free
- **Card study allocation:** About 3 hours for the relevant articles
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s6-r0`
- **Link label:** Open the official PDF
- **Why included:** A recruiter handles CVs, references and background checks, which are personal data. The GAID sets out the principles, lawful bases, consent rules, information duties for data subjects, breach notification and data processing agreements.
- **Next action:** Read Articles 15, 16, 17, 18, 27, 33 and 34, then draft a six-line privacy notice you could put on a job application form.
- **Access/verification note:** Verified 2026-10-26 by reading the official NDPC PDF (reference NDPC/NDP ACT-GAID/01/2025). I read the arrangement of articles and the opening articles, not the entire document. This is a regulator's implementation directive, not the Act itself, and it is not legal advice. Confirm the current text and any later amendments with a Nigerian lawyer.

#### B.7.2 Labour Act, Chapter L1 Laws of the Federation of Nigeria 2004

- **Provider:** PLAC Laws of Nigeria (statute copy); ILO NATLEX listing
- **Destination:** <https://lawsofnigeria.placng.org/laws/L1.pdf>
- **Format:** Free primary legislation (official-style PDF)
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours for Parts I and II
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s6-r1`
- **Link label:** Open the statute PDF
- **Why included:** Part II is specifically about recruiting, including prohibitions on recruiting without a permit or licence, employer permits, recruiter licences and restrictions. Section 7 covers written particulars of employment terms, which matters when you prepare an offer.
- **Next action:** Read sections 7, 23, 24, 25, 26 and 71. Write down three questions you would ask an employer before running a search on their behalf.
- **Access/verification note:** Verified 2026-10-26 by reading the free statute PDF. The Act dates from 1971 and is reproduced as Cap. L1 LFN 2004; the ILO NATLEX entry records the 1990 revised edition. It may have been amended or partly superseded, so check current law and get local legal advice before acting on it. This is an official-style reproduction, not a government gazette download.

#### B.7.3 Google re:Work: onboarding and candidate experience guides

- **Provider:** Google re:Work
- **Destination:** <https://rework.withgoogle.com/intl/en/guides/>
- **Format:** Free official practice guides
- **Cost/access label:** Free
- **Card study allocation:** About 2 hours
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s6-r2`
- **Link label:** Open the guides index
- **Why included:** Closes the loop from Stage 4. The data-driven onboarding guide and the candidate experience guide show what happens after the offer is signed, which is where a recruiter's responsibility often quietly ends.
- **Next action:** From the guides index, open the onboarding guide and sketch a 30-day onboarding checklist for your practice role.
- **Access/verification note:** Verified 2026-10-26 on the provider guides index; those two guides are listed among the 23 free results. I did not open the individual guide pages. No login or payment shown on the index.

### B.8 Stage 8: Work the process - tools, metrics and getting hired

**Schedule:** Weeks 18-20; **stage budget:** 12 hours; **cards:** 3.

Pull the pieces into a portfolio, learn the numbers recruiters are judged on, and start applying for junior recruiter and HR assistant roles in Lagos.

**Outcomes:**

- Track a practice pipeline in a free tool and report simple funnel numbers
- Present one finished hiring project as a portfolio piece
- Apply for entry-level roles with evidence rather than certificates alone

#### B.8.1 Managing Your Contacts With the HubSpot CRM

- **Provider:** HubSpot Academy
- **Destination:** <https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm>
- **Format:** Free short video lesson
- **Cost/access label:** Free
- **Card study allocation:** 20 minutes
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s7-r0`
- **Link label:** Open the lesson
- **Why included:** A free CRM is a practical stand-in for an applicant tracking system while you practise. The Academy's course catalogue is explicitly free and online.
- **Next action:** Create a free account, add your ten practice candidates, and label each with a stage so you can produce a funnel count.
- **Access/verification note:** Verified 2026-10-26 on the HubSpot Academy courses page: the catalogue is described as completely free and online, with a free account required; this lesson is listed at 20 minutes. The CRM is a commercial product with paid tiers; the free tier is enough for the practice task.

#### B.8.2 Greenhouse guidance: recruiting metrics and benchmarks

- **Provider:** Greenhouse
- **Destination:** <https://www.greenhouse.com/guidance>
- **Format:** Free official articles and reports
- **Cost/access label:** Free
- **Card study allocation:** 2-3 hours
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s7-r1`
- **Link label:** Open the guidance hub
- **Why included:** Recruiters are judged on time to hire, source of hire, pass-through rates and quality of hire. Learning the vocabulary lets you discuss your practice project in an interview.
- **Next action:** Calculate four funnel rates from your practice pipeline and write a short paragraph explaining the bottleneck.
- **Access/verification note:** Verified 2026-10-26 on the provider guidance hub: free articles and resources listed. The 2026 hiring benchmarks report is advertised on the same page and may require a form; I did not verify its access terms, so do not assume the underlying dataset is freely downloadable.

#### B.8.3 CIPM Nigeria: professional membership by examination

- **Provider:** Chartered Institute of Personnel Management of Nigeria
- **Destination:** <https://cipmnigeria.org/membership/membership-routes/>
- **Format:** Paid professional qualification
- **Cost/access label:** Paid - NGN fees shown on the provider site
- **Card study allocation:** Five exam stages, four exam diets a year
- **Content-check date shown on card:** 2026-10-26
- **Manifest status:** `confirmed`
- **Persisted completion key:** `s7-r2`
- **Link label:** Check current fees
- **Why included:** CIPM is the body chartered to regulate HR practice in Nigeria. Its syllabus shows the local body of knowledge, including Nigerian Labour Law, workforce planning and HR metrics, and its qualification is recognised locally.
- **Next action:** Do not enrol yet. Read the syllabus and exam FAQ, then decide after you have six months of experience whether the qualification is right for your path.
- **Access/verification note:** Verified 2026-10-26 on the provider membership routes page and exam FAQ. Published fees: application NGN 10,000; acceptance NGN 12,000; Foundation NGN 55,440; Intermediate I NGN 57,190; Intermediate II NGN 58,200; Professional I NGN 64,050; Professional II NGN 70,050, with exemption fees from NGN 20,250 to NGN 24,300. The provider states fees are subject to review. Minimum entry is a degree or HND with five SSCE credits including English and Mathematics; undergraduates may enrol but are inducted only after graduating. Prices are in naira because the provider publishes in naira; no USD conversion is implied.

## Appendix C — all URL verification records

### C.1 Status definitions and aggregate

- **`confirmed`:** Provider page was read and the free/paid finding is documented.
- **`ambiguous`:** Page was read but the free claim could not be confirmed; not counted as free.
- **`partial`:** Only a cookie banner or partial content was visible.
- **`unreachable`:** Provider page failed (HTTP 500); figures come from third parties.
- **`not_confirmed`:** Lead/paid extra only; no provider confirmation of free access.

Original research date: `2026-10-26`. Age threshold: `90` days. **23 confirmed / 1 ambiguous / 1 partial / 2 unreachable / 4 not-confirmed = 31 entries.** The latter eight constitute open gaps. A confirmed finding may document a paid item; confirmed does not mean free.

### C.2 Per-URL content findings

| # | URL | Content status | Content verification date | Recorded finding |
|---:|---|---|---|---|
| 1 | <https://www.youtube.com/playlist?list=PLeDNHX61_qlQWYcxZNB19TDOKbl625W2c> | `confirmed` | 2026-10-27 | Checked 2026-10-27: public Talent Acquisition playlist, 43 listed videos, description and lesson titles readable without sign-in; playback and mobile app handoff not tested. Creator discloses AI-supported production; confirm consequential claims against primary sources. |
| 2 | <https://www.youtube.com/playlist?list=PLeDNHX61_qlQeRK1_i5flRpz2T0wjQXN2> | `confirmed` | 2026-10-27 | Checked 2026-10-27: public HR Essentials playlist, 16 listed videos; description and initial lesson titles readable without sign-in. The fetch also exposed a YouTube error banner, so playback and mobile app handoff remain untested. Content developed by Dr. Heather Staples; videos produced using AI-supported tools. This is introductory study, not a professional qualification. |
| 3 | <https://learn.saylor.org/course/view.php?id=1292> | `confirmed` | 2026-10-26 | PRDV226 syllabus: no tuition, free materials, free completion certificate at 70%. |
| 4 | <https://openstax.org/books/principles-management/pages/11-introduction> | `confirmed` | 2026-10-26 | Openly licensed textbook, free web view. |
| 5 | <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0> | `confirmed` | 2026-10-27 | OpenLearn course page: free course, free statement of participation. CI sweep 2026-10-27 got 403 (bot filtering); page re-read the same day and the claim still holds. |
| 6 | <https://alison.com/course/diploma-in-human-resources-hr> | `confirmed` | 2026-10-26 | Free to study; branded certificate paid; free Learner Record. |
| 7 | <https://learn.saylor.org/course/BUS301> | `confirmed` | 2026-10-26 | Saylor BUS301 course page read. |
| 8 | <https://www.coursera.org/learn/recruiting-hiring-onboarding-employees> | `ambiguous` | 2026-10-26 | Page read, but FAQ ties full access to purchase/trial/no-certificate option. NOT counted as free. |
| 9 | <https://www.onetonline.org/> | `confirmed` | 2026-10-26 | Free public occupational database. |
| 10 | <https://resources.workable.com/hr-templates/> | `confirmed` | 2026-10-26 | Templates free to download; no software trial required. |
| 11 | <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction> | `confirmed` | 2026-10-26 | Free structured-hiring article and worksheets. |
| 12 | <https://resources.workable.com/boolean-search-cheatsheets/> | `confirmed` | 2026-10-26 | Free cheatsheets confirmed. |
| 13 | <https://www.youtube.com/watch?v=yMnw_2VNOVE> | `confirmed` | 2026-10-26 | Public free video checked directly. |
| 14 | <https://rework.withgoogle.com/intl/en/guides/> | `confirmed` | 2026-10-26 | Guides index plus two guides read; other guides cited by name from the index. |
| 15 | <https://www.jobberman.com/employer/free-listing> | `partial` | Not confirmed | Returned only a cookie banner. Free-listing claim from provider search listing; card marked partially verified. |
| 16 | <https://www.greenhouse.com/guidance> | `confirmed` | 2026-10-26 | Free guidance hub read. |
| 17 | <https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices> | `confirmed` | 2026-10-26 | Guides index plus two guides read; other guides cited by name from the index. |
| 18 | <https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences> | `confirmed` | 2026-10-26 | Guides index plus two guides read; other guides cited by name from the index. |
| 19 | <https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf> | `confirmed` | 2026-10-27 | Regulator PDF; arrangements of articles and opening provisions read, not cover to cover. CI sweep 2026-10-27 got 403 (bot filtering); PDF re-read the same day and is intact. |
| 20 | <https://lawsofnigeria.placng.org/laws/L1.pdf> | `confirmed` | 2026-10-26 | Statute copy; arrangements and opening provisions read, not cover to cover. Not legal advice. |
| 21 | <https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm> | `confirmed` | 2026-10-26 | Academy catalogue described as free with a free account. |
| 22 | <https://cipmnigeria.org/membership/membership-routes/> | `confirmed` | 2026-10-26 | Paid route; naira fee table published. Prices subject to review. |
| 23 | <https://www.linkedin.com/learning/> | `unreachable` | Not confirmed | LinkedIn help pages returned HTTP 500 on 2026-10-26. Prices come from third-party 2026 guides and are unconfirmed. CI sweep 2026-10-27 got 200 (a login wall); a browser-like recheck the same day got 403, so the content has still not been read. |
| 24 | <https://www.linkedin.com/help/recruiter/answer/a6807901> | `unreachable` | Not confirmed | HTTP 500 on 2026-10-26. Recruiter Lite figures are third-party and unconfirmed. CI sweep 2026-10-27 got 200 (a login wall); a browser-like recheck the same day got 500, so the content has still not been read. |
| 25 | <https://www.coursera.org/learn/aphri-talent-acquisition-and-onboarding> | `not_confirmed` | Not confirmed | Paid extra; free status not confirmed from a provider page. |
| 26 | <https://www.aihr.com/courses/sourcing-recruitment-certification/> | `not_confirmed` | Not confirmed | Paid/subscription product; free status not confirmed from a provider page. |
| 27 | <https://www.udemy.com/course/recruiter-training-hire-top-employees-in-30-days/> | `not_confirmed` | Not confirmed | Paid product; prices change frequently. |
| 28 | <https://helpcenter.alison.com/en/articles/8206417-is-alison-really-free> | `confirmed` | 2026-10-26 | Alison help centre FAQ read. |
| 29 | <https://support.saylor.org/hc/en-us/articles/23586212781844-FAQ-General> | `confirmed` | 2026-10-27 | Saylor general FAQ: no tuition or fees, completion certificates free. CI sweep 2026-10-27 got 403 (bot filtering); FAQ re-read the same day and the claim still holds. |
| 30 | <https://learn.saylor.org/mod/page/view.php?id=94644> | `confirmed` | 2026-10-26 | Saylor course material page read. |
| 31 | <https://www.jobberman.com/job-seeker> | `not_confirmed` | Not confirmed | Lead page only; no access claim verified. |

### C.3 Exact first-sweep URL snapshot

This list has **30 URLs**, not the current 31. The 27 statuses marked 200 are inferred from the owner-pasted complete summary/count and non-2xx list; they are not independently parsed TSV rows. HTTP codes below apply to the historical 27 October run only.

| # | Historical URL | HTTP result | Follow-up for non-2xx |
|---:|---|---:|---|
| 1 | <https://www.youtube.com/@HRLearningLab> | 200 | — |
| 2 | <https://learn.saylor.org/course/view.php?id=1292> | 200 | — |
| 3 | <https://openstax.org/books/principles-management/pages/11-introduction> | 200 | — |
| 4 | <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0> | 403 | Bot filtering, not a dead link. Page re-read 2026-10-27 via a browser-like fetch: 'Free course' and 'Free statement of participation on completion' are still displayed. Claim holds. |
| 5 | <https://alison.com/course/diploma-in-human-resources-hr> | 200 | — |
| 6 | <https://learn.saylor.org/course/BUS301> | 200 | — |
| 7 | <https://www.coursera.org/learn/recruiting-hiring-onboarding-employees> | 200 | — |
| 8 | <https://www.onetonline.org/> | 200 | — |
| 9 | <https://resources.workable.com/hr-templates/> | 200 | — |
| 10 | <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction> | 200 | — |
| 11 | <https://resources.workable.com/boolean-search-cheatsheets/> | 200 | — |
| 12 | <https://www.youtube.com/watch?v=yMnw_2VNOVE> | 200 | — |
| 13 | <https://rework.withgoogle.com/intl/en/guides/> | 200 | — |
| 14 | <https://www.jobberman.com/employer/free-listing> | 200 | — |
| 15 | <https://www.greenhouse.com/guidance> | 200 | — |
| 16 | <https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices> | 200 | — |
| 17 | <https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences> | 200 | — |
| 18 | <https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf> | 403 | Bot filtering. PDF re-read 2026-10-27: Nigeria Data Protection Act GAID 2025, arrangement of articles and opening provisions still present. Claim holds. |
| 19 | <https://lawsofnigeria.placng.org/laws/L1.pdf> | 200 | — |
| 20 | <https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm> | 200 | — |
| 21 | <https://cipmnigeria.org/membership/membership-routes/> | 200 | — |
| 22 | <https://www.linkedin.com/learning/> | 200 | — |
| 23 | <https://www.linkedin.com/help/recruiter/answer/a6807901> | 200 | — |
| 24 | <https://www.coursera.org/learn/aphri-talent-acquisition-and-onboarding> | 200 | — |
| 25 | <https://www.aihr.com/courses/sourcing-recruitment-certification/> | 200 | — |
| 26 | <https://www.udemy.com/course/recruiter-training-hire-top-employees-in-30-days/> | 200 | — |
| 27 | <https://helpcenter.alison.com/en/articles/8206417-is-alison-really-free> | 200 | — |
| 28 | <https://support.saylor.org/hc/en-us/articles/23586212781844-FAQ-General> | 403 | Bot filtering. FAQ re-read 2026-10-27: 'We do not charge tuition or fees' and 'Yes, our course completion certificates are free of cost' are still published. Claim holds. |
| 29 | <https://learn.saylor.org/mod/page/view.php?id=94644> | 200 | — |
| 30 | <https://www.jobberman.com/job-seeker> | 200 | — |

**Recorded sweep notes (retained verbatim):**

- The other 27 URLs returned 200 to curl. This is inferred from the job summary's counts (200 x 27, 403 x 3) plus its complete non-2xx list; the raw link-status.tsv artifact could not be downloaded from this sandbox because its Azure Blob redirect is outside the egress allowlist.
- A 200 does not resolve an ambiguous, partial or not_confirmed status. Coursera, Jobberman, LinkedIn and the paid extras were not re-read, so their research statuses are unchanged.
- LinkedIn re-checked 2026-10-27 with a browser-like fetch: /learning/ returned 403 and the Recruiter help article returned 500. The sweep's 200 is a login wall, not readable content; both remain 'unreachable'.
- Historical 30-URL snapshot: predates the two direct playlist URLs added on 2026-10-27; no CI HTTP codes are claimed for those new URLs.

The manifest’s statement that a LinkedIn 200 is a login wall is the historical interpretation; the raw response body was not available in this audit. The defensible conclusion is that the 200 did not establish readable provider content or validate prices.

## Appendix D — artifact measurements and file inventory

### D.1 Delivered artifacts

Measured from the audited committed files during report preparation. The Markdown source contains **7,344 whitespace-separated tokens** by Python `str.split()`; this is a mechanical word-count approximation. The current PDF contains **15 pages**, with **7,295 extracted text tokens**. Those counts differ because rendered metadata, parsing and extraction differ. The approximately 6,829-word figure in the early record refers to the original version, not this baseline.

| File in `learning-library/out/` | Bytes | SHA-256 |
|---|---:|---|
| `Recruiter-TA-Library.docx` | 57,938 | `7035af4ef964e507484be227eb8ef7da8ef86e12d4b326218e493002bfddce16` |
| `Recruiter-TA-Library.html` | 57,233 | `fd51c44e83766849de8e1dedaeb78be82e595f677516004846e26d604ef90604` |
| `Recruiter-TA-Library.md` | 47,473 | `9fa8ea0ad01c920943cc72ce1f1ab39977bd1f064fa989cf7f6449d77e511af5` |
| `Recruiter-TA-Library.pdf` | 52,610 | `76e6977c4c85f47bb12630f4496867b49fec731f24fda1599579d8e65750edca` |
| `roadmap-app.html` | 166,050 | `80f10411b75e8dd592657c4331af95d1608065f3681764a73154fc05d870cc19` |

These hashes identify this snapshot. PDF/DOCX future rebuilds can have different outer-file hashes while passing the defined drift comparison. Do not use them as an excuse to ignore a content drift failure.

### D.2 Complete tracked baseline inventory

There were **57 tracked files before adding this report**. Every file is listed below with size and digest. Cache/venv/npm/browser/screenshot artifacts are excluded. This inventory is baseline evidence, not a request to commit new hash maintenance for every normal edit. `docs/ENGINEERING-REPORT.md` is the new report and is intentionally outside the baseline inventory.

| Baseline path | Bytes | SHA-256 |
|---|---:|---|
| `.agents/skills/README.md` | 3,898 | `7d82073789b2f2a777de5a59f28ccb1f93a2a3833567c0ad5ff16f1827404ee2` |
| `.agents/skills/resource-learning-library/.gitignore` | 55 | `c5f1191fec77b67a23d58cf6c759919972e6ae9f4cf26f7436dc31152ce321a9` |
| `.agents/skills/resource-learning-library/INSTALL.md` | 2,982 | `cae23217cabd2b917a6dac6dc7a701f519dc6c3bb9629acf8686436af86c729a` |
| `.agents/skills/resource-learning-library/README.md` | 3,406 | `dc9d6571c395267af144dd14a1dd05e6dea26cf41ec580b6a7c3b1f3276f14bc` |
| `.agents/skills/resource-learning-library/SKILL.md` | 16,297 | `4b4eefce609469073f3ec20d76b64032080cec5e543b4e6a742dba92fe784fdd` |
| `.agents/skills/resource-learning-library/example/01-getting-started.md` | 974 | `7a19b9a280368894b80b83cc1a1235af51abc34351ebf3b634a607fbbc4dddd0` |
| `.agents/skills/resource-learning-library/example/interactive-demo.json` | 1,266 | `7a7e7253381ddca8fcf981779b350a8990b7618f06581ec77b93838f8e444793` |
| `.agents/skills/resource-learning-library/requirements.txt` | 48 | `9c690c94974c01bc2d2e83c2fb9a756bb848314fedcf5efab3da791601ac7c37` |
| `.agents/skills/resource-learning-library/scripts/docx_render.py` | 45,325 | `9b04901c3332d2fc8a1075ac344fd4f7d100ea53ca79746e9d086bf34b1e56dd` |
| `.agents/skills/resource-learning-library/scripts/interactive_app.py` | 26,179 | `684529f10150fe0b49e07b99bcc839ada0a02dcebdc68f4ad4c0fa9e0174b1d0` |
| `.agents/skills/resource-learning-library/scripts/style_audit.py` | 6,342 | `d7923bbf33ea95f7063422ed87b084d882fe2eacdf6cfaab4714675f9fefe7dc` |
| `.agents/skills/resource-learning-library/scripts/validate_build.py` | 9,325 | `d4b2beaf202c691f70a9f3db7ac6b36069f3be038f89f09bd6923febdce2ca30` |
| `.agents/skills/resource-learning-library/tests/test_renderer.py` | 4,502 | `f28f4bd6487bd939776324213f5e7bf5f0603d3e01b410af347dfe2b95318c8a` |
| `.claude/settings.json` | 55 | `e7872a9769b87ee6522f1b580d0b2742847612265256c3b1bfcc1e21c2adb189` |
| `.gitattributes` | 216 | `ea5f7c9c7a2004776aca9e08034727b9dfb9daa28da193714aed90072342416a` |
| `.github/pull_request_template.md` | 1,293 | `6a255bd0a3bd9608523abe340c545b6df5dfbd5283812f586d8beb352deccc3e` |
| `.github/workflows/link-check.yml` | 2,451 | `6397b59e77402527fbd964ec6648431dc8062218b0a29763ac4a6b9886010e05` |
| `.github/workflows/verify.yml` | 1,772 | `f09004bc907522a6dcdc6390cd02950a8b6f2da4a9d31da390779d28f565f683` |
| `.gitignore` | 507 | `571f77aacf78cb811f25dc7ff8d3674a304b7e28d2b78cdc7959e485e931868e` |
| `.mcp.json` | 120 | `f6016a482aeac902cc678488918bbb912bc948dbce251061ffc4ee296b55a727` |
| `CHANGELOG.md` | 11,850 | `a9b4f61d5cd25f2b5580ccf6d6900e8e16125d3c4a95517a6edfe4546b4c73f8` |
| `Makefile` | 3,261 | `5066ae9e897978fc0583e383e50f6c1c72e12e360fb2a05a6996d2f4838b201c` |
| `README.md` | 2,762 | `b7ba4538beb6a19c8d44faf58bdf2a09725c2140e24f906c2d52be7f2cba6077` |
| `RETROSPECTIVE.md` | 15,459 | `59b43a553f2459d5d8450085490d99ac3b360ead1c0bf158aedddc5589f17247` |
| `THIRD-PARTY-NOTICES.md` | 1,553 | `cff6bb4c1c644079267964f94946728750ba37e53e2a34b964b762e925d5fada` |
| `docs/DEPLOYMENT.md` | 2,793 | `615e1601b19005e2c2f6c059df54821bbe2b1781b2f96e90df8963aaa3a6f6f7` |
| `docs/DESIGN-SPEC.md` | 13,418 | `fe02fc4faadaa8ad074afbe17dd3406d925c7bf30ed9599a7194f62103901441` |
| `docs/SETUP.md` | 11,699 | `a75349e6f337a78d1a29d69e24fe25e6bdd1934ae4f193520450f0c43bf6072f` |
| `learning-library/DESIGN-SYSTEM.md` | 18,701 | `238e949b8635202442a658544a979dbd0043eee26a15dd9a767c32f902ee76f9` |
| `learning-library/README.md` | 15,866 | `31dd9ad5305b37e03c3127c232016197703cacbad31db912c63bbde558e546c6` |
| `learning-library/check-links.sh` | 2,916 | `f34d53f671bf00fea6512d25d2141d4827fe52fa57b129bea08ebeba53637be4` |
| `learning-library/out/Recruiter-TA-Library.docx` | 57,938 | `7035af4ef964e507484be227eb8ef7da8ef86e12d4b326218e493002bfddce16` |
| `learning-library/out/Recruiter-TA-Library.html` | 57,233 | `fd51c44e83766849de8e1dedaeb78be82e595f677516004846e26d604ef90604` |
| `learning-library/out/Recruiter-TA-Library.md` | 47,473 | `9fa8ea0ad01c920943cc72ce1f1ab39977bd1f064fa989cf7f6449d77e511af5` |
| `learning-library/out/Recruiter-TA-Library.pdf` | 52,610 | `76e6977c4c85f47bb12630f4496867b49fec731f24fda1599579d8e65750edca` |
| `learning-library/out/roadmap-app.html` | 166,050 | `80f10411b75e8dd592657c4331af95d1608065f3681764a73154fc05d870cc19` |
| `learning-library/src/favicon-link.html` | 358 | `cd09f700b5450855f33f492eb0fc97dcddd9f4e3c9148bfb3b35622f820cc2e7` |
| `learning-library/src/fieldnotes-theme.css` | 21,080 | `e2df5f73aba89856db8abb4e10a59d7bfd26e19dafd139a49bfc53cde6568ce4` |
| `learning-library/src/pals/LICENSE-MIT.txt` | 1,077 | `f053fb9421ba2fe0f728523dd2ca28213867340014615370dbe787f40d9973b6` |
| `learning-library/src/pals/pals-controller.js` | 5,239 | `f158645b25535380af663f34a1712b79cdeed5053e691790ebe6d4fbb74193d1` |
| `learning-library/src/pals/pals.css` | 2,334 | `3ce58832ea81055a2427c7d462ab51df7cb2165913d995d80641a957a919cf5e` |
| `learning-library/src/pals/pals.json` | 1,620 | `4a68521364940341a496d1b43ea8489e1939a56d00e46e61b5dc2b4b1e36dd21` |
| `learning-library/src/pals/piixpal-payload.html` | 83,164 | `298776d7bbe408cd3146f61fbb38ec8fddaa2facb1db99c3f013638f5d20ea75` |
| `learning-library/src/recruiter-talent-acquisition-library.md` | 47,473 | `9fa8ea0ad01c920943cc72ce1f1ab39977bd1f064fa989cf7f6449d77e511af5` |
| `learning-library/src/roadmap-app.json` | 35,971 | `0209577e326b622d65aec548afed73b77e824f3fc1f805a8fcfec6fb905401a2` |
| `learning-library/src/verification-manifest.json` | 13,876 | `a86692ecfe715ecc0fe1de309586b7e749c95abbc2097f40b40f9949a4c81450` |
| `learning-library/tools/build_tracker.py` | 12,703 | `d01b4a4d88325eb34b056aee14458bc8918994f27c2a7a5e8cff88ed05917f97` |
| `requirements.lock` | 1,054 | `add41cdb4910c0eb625da03dabd391e76252f4d60bcb037cb0d643fed6feb4d6` |
| `tools/check.py` | 31,734 | `0d890e33d663ef91878c2dde17c392f6f7700d5a521891e3a439c089ebd455ee` |
| `tools/serve_preview.py` | 2,917 | `4cf197a2b227efda92fa9c7ea0bcc52d192a77ed11a8b5d4aabf533df09a2419` |
| `tools/skill-hashes.sha256` | 1,846 | `819e7d6be648a6dec6aada40215bd467b847ee9e34b58c000df8c5ea8c0f4f5b` |
| `tools/test_deployment.py` | 1,463 | `eab935c2beacb1bedce556cefa1bd3038d47358adb01b5487f8123b4785db2ca` |
| `tools/test_favicon.py` | 1,901 | `36ea87a6f77d2eb110ffd81e1d0dc4fa9315dfba666c8bbfa9f39b71a3b1ad76` |
| `tools/visual/package-lock.json` | 19,227 | `a60905d4919e604c5aae67a9fb1b02210edc21c38461e89609abd8497dd23a31` |
| `tools/visual/package.json` | 397 | `efd6a4984165fe325ecd5cf2af800f0c83ba6c1f0959d7db16ea3dd75bc90229` |
| `tools/visual/visual_check.mjs` | 27,844 | `f9ee8e3f76259338b2688a718c7452bb6482b45005eed464bef9064e787acd83` |
| `vercel.json` | 248 | `b5ca0d97184d023400f93e9d2b04444ec0878993f49dc298941fcf1e8aeb914d` |

### D.3 Artifact-change policy

A source-only edit to Markdown, JSON, theme, Pals or favicon is incomplete if its generated output is stale. A generated-output-only edit is incomplete if `make build` would erase it. Review both source and output, run drift without overwriting evidence first, and regenerate intentionally. Keep runtime/download/test caches outside Git.


## Appendix E — acceptance and decision ledger

This ledger ties the major explicit requests and subsequent corrections to the delivered implementation or an openly retained limitation. “Implemented” describes repository state; live acceptance is stated separately where available.

| Request/decision | Result and engineering consequence | Evidence boundary |
|---|---|---|
| Absolute beginner entering HR through recruiter/TA | Eight-stage capability sequence with introductory context and practical outputs | Intake and source content |
| Lagos/Nigeria, about five hours/week | Approximately 20-week, 94-hour plan; naira CIPM fees; local privacy/labour stage | Source content, not personal career advice |
| Free first; mixed media | Video, textbooks, provider guides, courses, templates and primary legal material | Card fields and exclusions |
| All output formats | MD/PDF/DOCX/static HTML/interactive HTML committed | Five artifacts and drift test |
| Free study versus free certificate | Explicit OpenLearn/Saylor/Alison/Coursera/CIPM distinctions | Historical public-page reads; no enrolment |
| Check facts, do not pretend checks ran | Original sandbox sweep failure disclosed; later manual run recorded with evidence limits | Manifest/history/Section 12 |
| Keep supplied skill in repo byte-exact | 12-file vendor tree plus SHA inventory | Fresh hash check |
| Register trusted skill discovery durably | Project MCP config/permissions persisted | Registration exists; sandbox MCP POST execution blocked |
| Search relevant skills per task | Task-specific design/accessibility guidance reviewed; report catalog fetched | Not represented as successful MCP execution |
| Acknowledge instructions before execution | Conversation used staged understanding/go-ahead gates | Historical conversation; report request itself authorized audit |
| Do not commit yet, later commit/push/PR | Git mutations occurred only after later explicit authorization | Eight merged PRs; report remains uncommitted |
| Use Nature Photography as visual authority | Reference tokens, rules, fonts, border/shadow language ported | Theme/spec/history |
| Do not hand-edit output only | Local CSS/build wrapper source; regenerated committed tracker | Transform and drift checks |
| Remove bars above hero, preserve footer squares | Top starts with hero; footer accent squares remain | CSS and visual QA |
| Dark hero eyebrow | Ink-on-yellow computed styles | Browser assertions |
| Done bottom-right, link bottom-left | Card layout and mobile behavior preserved | Geometry checks |
| Every tag coloured; free/paid semantic | Six visible fills with semantic cost styles | Fresh computed styles, string-based cost classification caveat |
| Equal stage-intro margins, square outcome marker | Theme selectors implement both | Source/visual history |
| Small outward arrow on each link | Northeast arrow decoration on resource links | All-link visual assertion |
| Footer exact credit | “Made with love and fried plantain, by Moyinoluwa” | Built tracker/browser assertion |
| Increase h1 by 40% (repeated wording) | Applied once; later separately reduced by 25% | Historical design record and current clamp |
| Remove small hero gutter, not full-width breakout | Hero fills framed sheet's inner edges | Owner clarification and overflow checks |
| Tighter hero rhythm except eyebrow-to-title | Spacing adjusted without collapsing that interval | Historical refinements/theme |
| Remove visible Reminder time label | Accessible name/title retained on native input | Build anchor and current HTML |
| Ten Pals like the reference | Real engine, eight species, ten placements, tracker only | Explicit four-way intake and config |
| Distribute Pals down page | Hero/dashboard/alternating-stage/footer anchors | Full placement table |
| Keep decoration optional and accessible | Idle activation, pause, live status, initial reduced-motion off, print hiding | Source + browser tests, teardown/live-preference gaps noted |
| Preview should work after reset | Durable stdlib server and rebuild-on-start Make target | Historical recovery and tracked tooling |
| Run the actual link sweep | Owner-dispatched Actions run succeeded after API permission failures | Summary + metadata; no local raw TSV |
| Host publicly | Static root rewrite, publish only `out`, download paths not caught | Config/tests; owner deployment |
| Mobile h1 too large | Exactly 25% reduced clamp | Current CSS and 13 measured widths |
| Open correct TA playlist | Direct playlist URL replaces channel destination | Metadata/readable titles + activation tests; playback caveat |
| Add HR Essentials first | New first card, 27 total, same 94-hour budget | JSON/Markdown/generated outputs |
| Do not lose existing progress | Dedicated key for new card, legacy Stage 1 mapping unchanged | Saved-state fixture |
| Pals jitter while scrolling | Document-space absolute overlay | 0px native error versus 240px fixed control; owner acceptance |
| Preview links unclickable | Investigated all anchors and real inputs; no reproduced interception | No unproven navigation fix shipped |
| Fixes should work live | Owner confirmed after PR #7 | Owner acceptance, not independent device matrix |
| Exact reference favicon | Exact inline tag/hash, validator adapter, colour test | PR #8 + CI; production icon not later confirmed |
| Comprehensive engineer report | This document: architecture, chronology, inventory, research, failures, checks and limits | New Markdown deliverable only |

### Closing handover

The project is maintainable because its constraints are now explicit: immutable vendor boundaries, source-owned customizations, committed outputs, runnable checks, separate current and historical evidence, and honest browser/network limits. The next engineer should preserve those boundaries while simplifying the duplicated content and persistence model. A passing test is meaningful only when its scope is understood; a historical assertion should never become a current guarantee through repetition.

**End of report.**
