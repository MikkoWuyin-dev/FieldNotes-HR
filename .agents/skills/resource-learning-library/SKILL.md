---
name: resource-learning-library
description: Use when someone wants a researched, roadmap-ordered learning resource library for a topic, with free, paid, or mixed resources in PDF, DOCX, Markdown, static HTML, or an interactive HTML roadmap tracker.
requirements:
  - python3
  - python-docx
  - reportlab (PDF output)
  - pypdf (PDF validation)
  - curl
  - web page retrieval (fetch_page or an equivalent browser tool)
---

# Resource-learning library

Build a useful, detailed resource library around the learner's topic and roadmap. First establish the topic, acceptable cost, preferred resource formats, whether a roadmap already exists, and the desired output. If there is no roadmap, create one before researching resources. Map each resource to a roadmap stage and present the library in that sequence.

Treat cost, access, and progress claims carefully. Never promise that a library guarantees mastery, employment, or a credential. Be explicit about what was checked, what remains uncertain, and which assumptions were used.

## 1. Intake: ask before researching

Ask the following questions in a short, easy-to-answer intake. Use the ask-user tool when available; otherwise ask conversationally. Let people choose more than one resource modality or output format when that makes sense.

1. **What topic or subject do you want to learn?** Invite a specific outcome or subtopic if they know it.
2. **What cost range should resources follow?** Free only, paid only, or both/free and paid?
3. **What resource formats do you prefer?** Offer videos, books, written courses, interactive courses, mobile-app courses, and “something different.” Allow multiple selections.
4. **Do you already have a learning roadmap?** Yes or no.
5. **What format should the finished library use?** PDF, DOCX, Markdown, or HTML; allow multiple formats if requested.

If the user already has a roadmap, ask them to **upload it as a file or paste it as plain text**. If upload is unavailable or inconvenient, accept pasted text. Read the roadmap before researching; preserve its stages, ordering, and constraints unless the user asks for changes. Normalize unclear headings or timing only transparently, and ask about ambiguities that materially affect the work.

If the user has no roadmap, create a detailed roadmap for their topic before sourcing the library. Work from the perspective of a seasoned domain expert without claiming personal credentials. Ground the sequence in credible references, professional expectations, or established curricula where applicable. Include:

- the intended starting level and end capability;
- prerequisites and foundations;
- ordered stages or modules, with learning outcomes;
- key concepts and skills for each stage;
- practice tasks, projects, and checks for understanding;
- estimated effort and milestones, with assumptions stated;
- a capstone or other way to demonstrate progress where appropriate.

Use the resulting or user-supplied roadmap as the **organizing spine** of the research. Search for resources that teach the roadmap's actual concepts and skills, stage by stage. Do not collect a generic pile of popular links and try to fit a roadmap around it afterward.

If the user is unsure or cannot answer any question, offer a topic-specific recommendation and explain why. Do not silently make a consequential choice. For example, recommend free-first when budget is unknown, a mix of written and video formats when modality is unknown, or creating a roadmap when the user is unsure whether theirs is usable. For the topic itself, help them choose from their stated goal or interests rather than inventing an unrelated subject.

Keep useful context from the earlier workflow, but ask only when it changes the result: target level or career outcome, country/region, hours per week, accessibility needs, and relevant jurisdiction. If the user does not know, recommend a reasonable default and state it.

### HTML follow-up

If the user selects HTML, ask whether they want:

- a **static resource page** that presents the roadmap and resource cards; or
- an **interactive roadmap app** that helps them follow the sequence and track progress.

Explain the difference and recommend one if they are unsure. Static is appropriate for a reference document; interactive is useful for self-paced study and progress tracking.

## 2. Build or normalize the roadmap

For a user-supplied roadmap, identify its stages, prerequisites, outcomes, and ordering before searching. Preserve its logic and mark any optional improvements separately. If the roadmap has gaps, point them out and propose additions; do not silently rewrite the user's plan.

For a new roadmap, make it detailed enough to guide resource discovery. Tailor the depth to the topic and starting level. Use primary references for regulated, technical, or high-stakes subjects. For a career goal, consider real role requirements and distinguish foundational learning from job-specific practice. Explain time estimates as estimates, not guarantees.

Create an internal map from every stage to the skills, concepts, and search terms it covers. Use that map to plan and track research. If reliable resources are scarce for a stage, report the gap rather than padding it with unrelated links.

## 3. Find resources and verify cost/access honestly

Search results are leads, not evidence. Read provider pages and verify each candidate against the user's cost and modality preferences.

- Use provider pages for enrolment, pricing, syllabus, access, and terms. Prefer primary sources over blogs and roundup lists.
- Batch `curl` checks over candidate URLs (roughly 20–50 per sweep), keeping a URL-to-status mapping and the script so checks can be repeated. Example: `curl -sS -o /dev/null -w "%{http_code}\n" -L --max-time 25 "$url"`.
- A `403` may be access control or bot filtering; try the available page-retrieval/browser tool before dropping the resource. A `526` commonly signals an origin TLS/certificate error, not proof of bot blocking; confirm through another route and record what happened. `000` means curl received no HTTP response; drop the URL or label it unverified.
- Check each resource's modality against the user's preferences. If a suitable resource does not exist in a preferred format, say so and offer a useful alternative rather than disguising the format.
- Keep a drop list for meaningful exclusions and give reasons.

### When the user wants free resources

Treat “free” as a claim to verify, not a label copied from a search result. For **every resource presented as free**:

1. Inspect the provider's current course/resource page and its pricing, FAQ, enrolment, or access terms.
2. Check that the actual learning material needed for the roadmap stage is accessible without payment, a paid subscription, a credit card, or a trial that converts to paid. A free preview of a paid course is not a free course.
3. Check whether a free account is required, whether only some modules are free, whether access expires, whether a certificate or assessment costs extra, and whether terms vary by country or cohort.
4. Distinguish “free to study” from “free certificate.” A paid credential is not a reason to call the learning content paid if the user accepts that distinction, but disclose it clearly.
5. Do not bypass a paywall or infer access from a marketing headline. If the syllabus, required lessons, or access conditions cannot be confirmed, exclude it from the confirmed-free list or label it **unverified—not counted as free**.
6. Record the provider page checked, date checked, relevant location/currency, and the exact access/cost finding. Note access gates such as approval, waitlists, financial-aid awards, essays, or vouchers.

The verification is a point-in-time check, not a lifetime guarantee; tell the reader that provider terms can change. If the user wants paid resources or both, record actual price, currency, billing basis, region, date checked, taxes/fees if shown, and certificate/assessment costs. Separate free and paid choices visibly.

Record every resource as a detailed card with: **roadmap stage/order · link · provider · modality · actual cost/access conditions · time estimate · level/prerequisites · what it teaches · why it fits this stage · a concrete next action · verification date and note**. Distinguish provider-stated facts from your own time estimates or recommendations.

## 4. Organize the library in roadmap order

Present the roadmap first, then arrange resource cards under the matching stages in the exact learning sequence. For each stage, explain its outcomes, prerequisites, estimated effort, practice task, and how the selected resources work together. Keep beginner prerequisites before advanced material. Avoid repeating a complete resource card in several sections; use a short key or “see resource” reference when a resource supports more than one stage.

If the best available resource only partially covers a roadmap objective, state the gap and add a practice task or another verified source to cover it. Do not pad stages with loosely related content. If the user asks for a learning plan over a number of weeks, translate workload into a calendar using their weekly hours and make assumptions explicit.

## 5. Produce the selected output

Use one Markdown source per document and a shared renderer where possible. Do not hand-edit generated DOCX/PDF/HTML outputs after rendering.

- **Markdown:** deliver the editable `.md` source itself.
- **DOCX:** render the Markdown with `scripts/docx_render.py`.
- **PDF:** render with the same script's PDF output. PDF generation uses ReportLab; validate the resulting file before delivery.
- **Static HTML:** use the shared renderer. Keep it self-contained with inline CSS and no JavaScript, external stylesheets, images, iframes, or CSS `url(...)` assets. Clickable resource links are allowed.
- **Interactive HTML app:** convert the roadmap and researched resources to the JSON shape used by `example/interactive-demo.json`, then run `scripts/interactive_app.py`. Deliver a single-file app with the ordered stages, resource cards, completion controls, overall progress, and a daily learning streak.

The interactive app stores progress in the current browser's local storage, calculates streaks by the device's local calendar, and includes progress export/import. It asks permission before using browser notifications and checks reminders **only while the app page is open**. It cannot reliably notify when closed, does not sync progress across devices, and does not use a backend or push service. Browser notifications require a supported browser, user permission, and a secure context such as HTTPS or localhost; if unavailable or denied, the in-app check-in still works. State these limits clearly. Do not claim background push reminders.

For the app, keep CSS and JavaScript inline, avoid external/CDN dependencies and network requests, use safe DOM text insertion for user/resource text, validate resource URLs as HTTP(S), and make the layout usable on mobile and with keyboard/screen-reader navigation. Never embed secrets or credentials. The app should let learners export/import progress so they can back it up manually.

DOCX formatting details that are easy to get wrong:

| Effect | Implementation note |
|---|---|
| Cell / paragraph shading | Use `<w:shd w:val="clear" w:color="auto" w:fill="0B3D5C">` in `w:tcPr` or `w:pPr`; the fill attribute is `w:fill`, not `w:color`. |
| Hero band and callouts | Use real paragraph shading and borders with padding/indents; set namespaced Word attributes with `qn()`. |
| Zebra tables | Shade each even-row cell, not just the row; add `w:tblBorders` including `insideH` and `insideV`. |
| Callouts | Use `w:pBdr` and a tinted `w:shd`; vary border, fill, and ink for note, tip, and warning. |
| Clickable links | Create external hyperlink relationships and a `w:hyperlink` element with its own run properties. Plain blue text is not a real link. |
| Monospace code | Use one paragraph per code line, a monospace font, compact spacing, a shared panel fill, and boundary borders. |
| Page number | Add a Word page-number field to the footer; a typed numeral is not a page-number field. |

## 6. Debloat and split deliberately

When the user says the result is bloated, apply their criteria as deletions, not hedges.

- **Membership rule:** remove platforms that fail the user's checklist. Preserve the useful technique or competency in the relevant roadmap stage, and state how the plan now covers it.
- **Access friction:** if the user wants immediately usable free resources, remove resources gated behind applications, essays, approvals, waitlists, uncertain awards, or vouchers they cannot use.
- **Canonical resource cards:** keep each complete resource card in one canonical library document. Companion documents should refer to it by name or short key rather than copying the card and URL again.
- **Split by reader task:** put the tracker with the plan, legal/reference tables with the law document, and templates with the job-hunt document. Add a small cross-document map at the top of each file.
- Report before/after word counts and duplicate-resource counts so the reader can see what changed.

## 7. Validate outputs and prose

Never report “done” solely because a script exited cleanly. Run the checks for the selected output types and report actual results:

```bash
python3 scripts/validate_build.py out/*.docx out/*.pdf out/static.html
python3 scripts/validate_build.py --interactive-html out/roadmap-app.html
python3 scripts/style_audit.py src/overview.md
python3 -m unittest discover -s tests -v
```

`validate_build.py` parses DOCX XML parts, counts headings/tables/hyperlink relationships, reports theme fills in `word/document.xml`, checks for common Markdown residue, validates a PDF signature/page structure (using `pypdf` when installed), and checks that static or interactive HTML does not load external assets. The `--interactive-html` flag allows inline JavaScript for the roadmap app but still rejects external script sources, external assets, and CSS `url(...)` references.

`style_audit.py` checks mechanical Markdown issues (unbalanced `**`, malformed or unsafe Markdown link targets, odd fenced-code counts) and flags prose patterns for human review: throat-clearing, inflated adjectives, “it's not X, it's Y” turns, consultant-speak, and possible three-adjective tics. Style findings are prompts to inspect, not proof that every match is wrong; a list of three resources is fine.

Name the checks and their results. Example: “DOCX XML parsed; 4 tables; 12 external hyperlink relationships; no Markdown residue. PDF: 3 pages with extractable text. Static HTML: no external assets. Interactive app: one inline script, no external assets. Four unit tests passed.” Do not invent counts or claim checks that were not run. Link status checks do not prove a resource is free; access/pricing verification requires reading provider pages.

## 8. Protect existing files and avoid false claims

- **Frozen artefacts:** if the user says “leave file X as is,” set a write guard or build to a separate output directory before generating anything else. Do not call a shared entry point that rebuilds every output from edited sources.
- **Verify the right file:** inspect `word/document.xml` inside the DOCX ZIP when checking rendered text and fills; theme colours in `word/styles.xml` do not prove that document content uses them. Re-read the built file instead of trusting only the builder's return value.
- **Free-access claims:** exclude or mark unverified anything whose current access terms could not be checked. Never describe browser reminders as background notifications; the included app requires the page to stay open.

## 9. Write the friendly overview last

Write the reader-facing overview after the roadmap and files exist, so every sentence can be checked against the actual results: word counts, stage/resource counts, verification dates, tracker rows, and questions. Use plain, warm, specific language. Avoid jargon, throat-clearing, invented praise, and repetitive three-adjective phrasing. End with one useful first action that fits in about an hour.
