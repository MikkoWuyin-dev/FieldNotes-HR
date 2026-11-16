# From zero to first recruiter role: a roadmap-ordered learning library

> [!NOTE] Read this first
> Built on 26 October 2026 for an absolute beginner in Lagos, Nigeria, who wants to enter HR through the recruiter and talent acquisition path, with about five study hours a week. Work through the stages in order. Research began on that date, with selected later checks noted on the cards. Some access findings remain partial, conditional or unconfirmed; dates are not promises of current terms. Terms change; re-check before you pay or enrol. This is a learning plan. It cannot promise a job, a professional credential or mastery.

## Start here

{{overview}}

The most useful idea in the whole plan sits in Stage 6: ask every candidate the same well-designed questions and score the answers against a rubric you wrote before you met them. Stages 1 to 5 exist so that you can do that well. Stage 7 keeps you on the right side of Nigerian law. Stage 8 turns the practice into evidence you can show an employer.

Prioritise the confirmed-free study materials and skip optional paid paths. Confirm the partial listing terms before relying on that practice channel. The paid options are gathered at the end, with real prices where a provider published them and a clear warning where a price came from a third party. None of the free certificates here is a professional HR qualification.

## How this library was checked

I used a web-search tool and a page-retrieval tool to read provider pages on 26 October 2026. Search results were treated as leads. A resource only entered the confirmed-free list when the provider's own course page, syllabus, FAQ or policy page described the learning material as available without payment.

No account was created on any provider site, so I could not see anything behind a login. That means free claims rest on public provider statements rather than on a completed enrolment. Where a provider's own FAQ contradicted a marketing button, I followed the FAQ and said so on the card.

Three distinctions matter throughout:

- **Free to study** means the lessons, readings and assessments are available without payment. It says nothing about a certificate.
- **Free certificate** means the provider issues a completion document at no cost. Saylor does this. OpenLearn issues a free statement of participation instead. Alison charges for its branded certificate but gives a free Learner Record.
- **Professional qualification** is a different category again. In Nigeria the chartered body is CIPM, and its route is paid. A free course certificate is evidence of study, not a licence to practise.

Prices are quoted in the currency the provider publishes. CIPM publishes in naira. The LinkedIn figures come from third-party 2026 pricing guides and are marked as unconfirmed, because LinkedIn's own help pages failed when I tried to read them. I did not convert currencies or add taxes, bank charges or data costs.

One check in this skill's normal workflow could not run in the generating sandbox. It blocks most outbound traffic: a request to pypi.org returned 200, while requests to kaggle.com and docs.python.org failed at the TLS handshake. So no HTTP status codes were obtained there. The batch sweep over the then-current 30 cited URLs has since run in GitHub Actions (workflow run 40471064309, 27 October 2026): 27 returned 200 and 3 returned 403. Those three 403s were bot filtering, not broken links — the OpenLearn course page, the NDPC GAID PDF and the Saylor FAQ were each re-read and their free claims still hold. A 200 never proves a resource is free: LinkedIn's pages answer 200 to a plain curl but still return 403 and 500 to a browser, and remain unverified. A ready-to-run script, `check-links.sh`, sits next to these files so you can repeat the sweep; `src/verification-manifest.json` records the result. Where a specific provider page could not be read, the card says so.

## Roadmap at a glance

{{roadmap-table}}

Estimates are mine, based on the provider's stated course lengths plus practice time. They are planning figures, not promises. If you can only manage three hours in a week, stretch the stage rather than skipping the practice task.

---

## The stages and their resources

{{stage:orientation}}

{{stage:foundations}}

{{stage:define-role}}

{{stage:sourcing}}

{{stage:screening}}

{{stage:interviewing}}

{{stage:nigerian-law}}

{{stage:career-tools}}

## Paid extras, kept separate

These are real options, listed so you can decide later with your eyes open. Two of them appear as labelled cards inside the roadmap; the rest are here only.

**University of Minnesota, Recruiting, Hiring, and Onboarding Employees (Coursera).** The Stage 2 card explains the access ambiguity in full: the page shows an "Enroll for free" button while the same page's FAQ says full access needs a paid Certificate experience, a free trial, or a "Full Course, No Certificate" option where available. Coursera Plus was advertised on the page in US dollars, but the exact price depends on region and promotion. Financial aid is mentioned in the FAQ. The course asks for about ten hours a week, which is twice your budget, so treat it as an optional deepening rather than a core stage.

**CIPM Nigeria membership by examination.** The generated Stage 8 card carries the provider-published naira fee table and entry requirements, with the original verification date and subject-to-review warning. This is a paid professional route to consider after gaining experience, not a free course certificate.

**LinkedIn Learning, bundled with LinkedIn Premium Career.** Third-party 2026 pricing guides put individual access around USD 39.99 a month or USD 239.88 a year, with a one-month trial that requires a card. LinkedIn's own help page returned HTTP 500 when I tried to read it on 26 October 2026, so those figures are not provider-confirmed. Recruiter and talent sourcing learning paths live here. Some public libraries, universities and employers provide free access; check locally before paying.

**LinkedIn Recruiter Lite.** A sourcing product rather than a course. Third-party 2026 guides quote about USD 170 a month or USD 1,680 a year, with a one-month trial needing a card; the LinkedIn help page for the trial also failed to load during my check. As a beginner you can learn the method free in Stage 4. Buy a seat when an employer gives you one or when you have a pipeline big enough to justify it.

**Alison branded certificate.** The courses are free to study and the free Learner Record is a legitimate record of completion. If you want the branded digital or printed certificate, Alison's policy pages confirm it costs extra but the page I read did not show a current price. Check at checkout and decide whether a free Learner Record plus your Stage 8 portfolio says more to an employer.

**HRCI Talent Acquisition and Onboarding (Coursera), AIHR Sourcing and Recruitment Certificate, and the Udemy recruiter training courses.** All three are paid or subscription products whose free status I could not confirm from a provider page. Coursera's own results page labels the HRCI course "Free trial". Prices for Udemy change frequently. I have deliberately left them out of the confirmed-free list rather than guess.

## What was excluded, and why

- **Simplilearn SkillUp, LearnTube.ai, LearnCafe and similar "free HR certificate" listings.** Their free-certificate claims came from roundup articles rather than provider pages. One provider page stated that the course was available to subscribers. I could not confirm that the full learning material opens without payment, so they do not count as free here.
- **SHRM, CIPD and HRCI member toolkits.** Their public articles are useful, but the templates and exam preparation sit behind membership or a paid assessment. Excluded from the free list; no judgement on their quality.
- **The long directories of "best recruiter YouTube channels".** Only HR Learning Lab was verified directly. I did not add the other channels, because a list of unverified links would pad the library without teaching anything.
- **Free marketing and sales certifications.** HubSpot Academy is genuinely free, but a full marketing certification would pull you away from the recruiter path. Only its short CRM lesson appears, in Stage 8, where a candidate tracker is actually needed.
- **Anything behind a login I could not open.** Where a page showed only a cookie banner, I kept the resource and marked its verification as partial rather than dropping it silently.

There are also two gaps worth naming. Free, current, Nigeria-specific recruiter training is scarce; the local legal material here is primary legislation and regulator guidance, which is harder to read than a course but more reliable. And several core guides come from US employers or US government data. They teach a method that transfers, but their examples, job titles and legal assumptions do not. Stage 7 exists to correct that.

## Verification log

Primary provider pages read on 26 October 2026:

| Provider | Page read | Access finding |
|---|---|---|
| The Open University | OpenLearn course page | Free course; free statement of participation with a free account. |
| Saylor University | PRDV226 syllabus and general FAQ | No tuition; free materials; free completion certificate at 70 percent. |
| Alison | Help centre FAQ and certification page | All courses free to study; branded certificate optional and paid; free Learner Record. |
| Alison | Recruitment tag page | 15 free recruitment courses listed, including the HR diploma. |
| Coursera | Course page and its FAQ | "Enroll for free" button, but FAQ ties full access to purchase, trial or a no-certificate option. Not counted as free. |
| Google re:Work | Guides index and structured interviewing guide | 23 free guides; no login shown; interviewing guide updated March 2026. |
| Workable | HR templates index and Boolean cheatsheets | Templates free to download; separate software trial is not required. |
| Greenhouse | Guidance hub and structured hiring support article | Free articles, eBooks and worksheets; two PDF downloads available. |
| OpenStax | Principles of Management chapter 11 | Free openly licensed textbook in web view. |
| ONET OnLine | Site home | Free public occupational database; 1,016 occupation titles listed. |
| HubSpot Academy | Courses catalogue | Catalogue described as completely free and online with a free account. |
| NDPC | NDP Act GAID 2025 official PDF | Free regulator directive; articles on principles, lawful bases, consent and breach duties. |
| PLAC Laws of Nigeria | Labour Act Cap L1 PDF | Free statute copy; Part II covers recruiting permits and recruiter licences. |
| CIPM Nigeria | Membership routes page and exam FAQ | Paid; naira fee table published; exams four times a year online. |
| HR Learning Lab | YouTube channel video and description | Public free playlist; AI-assisted production disclosed by the creator. |

Checks I could not run, stated plainly:

- **HTTP status-code sweeps in the generating sandbox.** Blocked by the egress allowlist, so no status codes came from there. The sweep has since run in GitHub Actions (27 October 2026): 30 URLs, 27 with 200 and 3 with 403. `check-links.sh` in this folder repeats it. A status code never proves a resource is free — the provider page still has to be read. Page retrieval succeeded for every URL I opened except two, noted next.
- **LinkedIn help pages.** Both returned HTTP 500 on 26 October 2026. The CI sweep recorded 200 for them, but that is a login wall: a browser-like recheck on 27 October 2026 returned 403 for the learning index and 500 for the Recruiter help article. Neither has been read. Their prices in this document come from third-party 2026 pricing guides and are labelled unconfirmed.
- **The Jobberman free-listing page.** Returned only a cookie banner. Its free-listing claim comes from the provider's own search listing, so that card is marked partially verified.
- **Creating accounts and completing enrolment.** Not done. I cannot describe what any provider shows after sign-in.
- **Every individual Google re:Work guide.** I read the guides index in full and two guides directly. The rest are cited by name from the index.
- **Full text of both legal PDFs.** I read the arrangements of articles and the opening provisions. Neither document was read cover to cover, and neither is legal advice.

Provider terms change. A free course can move behind a subscription and a price can rise between one exam diet and the next. Re-check any paid item and any free-certificate claim before you commit time or money.

## About the interactive tracker

The single-file app stores your progress in this browser's local storage and counts a streak using the device's local calendar. It checks reminders only while the app page is open. It cannot send background notifications, does not sync between devices, and has no backend or push service. Browser notifications need a supported browser, your permission and a secure context such as HTTPS or localhost; if they are unavailable or denied, the in-app check-in still works. Use the export button now and then to keep a manual backup, and import that file if you change devices.

## Your first hour

{{first-hour}}
