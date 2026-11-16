# FieldNotes-HR: the whole project explained in plain English

**Written:** 1 November 2026, using the Lagos time zone.  
**Who this is for:** anyone who wants the full story, even if they have never built a website.  
**Project:** <https://github.com/MikkoWuyin-dev/FieldNotes-HR>  
**Website address supplied by the owner:** <https://fieldnotes-hr.vercel.app/>  
**Detailed technical version:** [ENGINEERING-REPORT.md](ENGINEERING-REPORT.md)

This is a separate, easier-to-read version of the engineering report. It is **not a short summary**. It explains what we built, how we built it, what went wrong, what we checked, and what still needs work. It also keeps the detailed lists at the end.

We are describing the same version of the project as the first report: the version after change request number 8 was accepted. Its full identifying code is:

```text
765f2e2b672e7ae04a0137133c2028d48cb70357
```

You do not need to remember that code. It is like a label on a particular edition of a book. It tells a future developer exactly which edition this report describes.

**Important:** writing this explanation does not change the website. It does not make old research new. It does not mean we have tested the live website again. The successful tests described below were run while preparing the original engineering report. We are explaining those results here, not pretending we ran them again for this rewrite.

## How to use this report

Read the main chapters for the story. Use the appendices—the extra sections at the end—when you want an exact link, date, file name or saved record.

Some exact computer instructions and names remain unchanged. Changing `make check` into friendlier words would stop it being the actual instruction a developer needs. Instead, we explain what it does beside it.

The course names and official file names also stay unchanged. A long official name is a label, not a word you must already understand.

## Contents

0. [A small dictionary before we begin](#0-a-small-dictionary-before-we-begin)
1. [What we know and how we know it](#1-what-we-know-and-how-we-know-it)
2. [What we made](#2-what-we-made)
3. [The original request and the rules](#3-the-original-request-and-the-rules)
4. [The complete story in time order](#4-the-complete-story-in-time-order)
5. [Where everything lives](#5-where-everything-lives)
6. [The learning plan and the research](#6-the-learning-plan-and-the-research)
7. [The borrowed building tools and skill search](#7-the-borrowed-building-tools-and-skill-search)
8. [How the five finished files are made](#8-how-the-five-finished-files-are-made)
9. [How the tracker remembers your work](#9-how-the-tracker-remembers-your-work)
10. [How we changed the look](#10-how-we-changed-the-look)
11. [The ten tiny creatures](#11-the-ten-tiny-creatures)
12. [Checking the outside links](#12-checking-the-outside-links)
13. [Keeping the preview working](#13-keeping-the-preview-working)
14. [Putting the project on the internet](#14-putting-the-project-on-the-internet)
15. [The little picture on the browser tab](#15-the-little-picture-on-the-browser-tab)
16. [The checks and their actual results](#16-the-checks-and-their-actual-results)
17. [Safety, privacy, usability and speed](#17-safety-privacy-usability-and-speed)
18. [Every recorded problem and what happened next](#18-every-recorded-problem-and-what-happened-next)
19. [What should improve next](#19-what-should-improve-next)
20. [Instructions for the next person](#20-instructions-for-the-next-person)
21. [What we did not do](#21-what-we-did-not-do)
22. [Where to find the evidence](#22-where-to-find-the-evidence)
23. [Appendix A: every accepted change and saved step](#appendix-a-every-accepted-change-and-saved-step)
24. [Appendix B: every learning card](#appendix-b-every-learning-card)
25. [Appendix C: every link-research record](#appendix-c-every-link-research-record)
26. [Appendix D: every finished file and project file](#appendix-d-every-finished-file-and-project-file)
27. [Appendix E: every main request and its result](#appendix-e-every-main-request-and-its-result)
28. [Appendix F: a completeness guide](#appendix-f-a-completeness-guide)

## 0. A small dictionary before we begin

You can return to this list whenever you meet an unfamiliar word.

| Word | Plain meaning in this project |
|---|---|
| HR | Human resources: the work of helping an organization manage its people and employment processes. |
| Recruiter | A person who helps find and choose people for jobs. |
| Talent acquisition, or TA | The broader work of attracting and hiring people, often with future needs in mind. |
| Roadmap | A learning plan that puts steps in a useful order. |
| Resource | Something used for learning: a course, video, guide, template or document. |
| Card | One box in the tracker that describes a learning resource and has a Done checkbox. |
| Source file | A file we edit to tell the project what to build. Think of it as a recipe. |
| Output or artifact | A finished file made from the recipe, such as a PDF or webpage. |
| Repository, or repo | The project folder together with its saved change history. |
| Git | The tool that saves and compares versions of the project. |
| GitHub | The online place holding the project and its shared change requests. |
| Commit | A named saved step in Git. It has an identifying code. |
| Branch | A separate line of work, so proposed changes do not immediately change the main version. |
| Pull request, or PR | A request to review and accept work from a branch. It is not a request to download a file. |
| Merge | Accepting the branch's work into another branch, usually `main`. |
| Push | Sending local saved Git work to the online repository. |
| Build | Run tools that turn the source files into the finished files. |
| Generator | A program that makes finished files from input data. |
| Dependency | A software tool or library that another tool needs. |
| Lockfile | A list fixing the versions of tools we want to use. |
| Browser | The app used to view websites, such as Chrome or Safari. |
| HTML | The instructions describing a webpage's parts and content. |
| CSS | The instructions controlling a webpage's appearance and layout. |
| JavaScript | The code that makes things happen inside the webpage. |
| JSON | A text format for labelled data, such as a title and a list of resources. |
| Markdown | Plain text with simple marks for headings, lists and links. This report uses it. |
| PDF | A document format commonly used for reading and printing. |
| DOCX | A word-processing document format, commonly opened in Microsoft Word. |
| Static hosting | Sending prepared files to visitors, rather than running our own application server for every action. |
| Backend | A separate service running on a server, often for accounts or stored data. This project has no project-owned backend. |
| localStorage | A small browser storage cupboard used to remember this site's progress on that browser. |
| Origin | A website's combination of address type, host name and port. Browsers separate storage by origin. |
| API | A set of agreed instructions that one program can use to ask another program to do something. |
| CI | Automatic checks run when project changes are sent to GitHub. |
| Test | A program or human check of a particular expected result. One passing test does not check everything. |
| Validator | A checker that looks for a particular set of mistakes or broken rules. |
| Headless browser | A real browser controlled by code without a normal visible browser window. |
| Viewport | The area available for a webpage in a browser window. |
| Pixel, or px | A small unit used to measure things on the screen. CSS pixels are not always individual physical screen dots. |
| Favicon | The little picture beside a page's title on the browser tab. |
| SVG | A picture described with shapes and drawing instructions instead of a normal photo grid. |
| Hash or fingerprint | A long code calculated from a file. It helps us notice if the file's contents change. |
| SHA-256 | The particular fingerprint method used here. It is not a password. |
| Byte | A tiny unit of stored information. File sizes are often counted in bytes. |
| Sandbox | The controlled computer environment where the assistant works. It has access limits and can lose temporary files. |
| Cache | Temporary saved material that makes repeated work faster. It should be safe to recreate. |
| Regression | Something that used to work stops working after a change. |
| Accessibility | Making something usable by people with different abilities and ways of using a device. |
| Reduced motion | A device setting asking websites to avoid unnecessary movement. |
| Evidence | A record, observation or test result supporting a claim. |

A useful comparison is a school notebook project. The source files are the notes and instructions. The finished website and documents are the neat copies. Git remembers changes. A PR asks someone to approve a new edition. Tests check particular things before the edition is accepted.

That comparison has limits. Tests are not all-knowing teachers, and a file fingerprint does not prove that a document tells the truth. We will keep explaining those limits.

## 1. What we know and how we know it

### 1.1 What this report includes

The story comes from the available conversation, the project's files, its complete available Git history, all eight accepted PRs, the older written work records, GitHub's test records and the owner's feedback.

It includes the work that failed. For example, we could not always reach outside websites, temporary tools disappeared, and one picture test made the wrong assumption. Those details matter because the next developer needs to understand the causes, not just see a happy ending.

We cannot honestly include events that left no record. Some early details survive in the conversation summary and the earlier retrospective—a document looking back at problems—rather than in a full command-by-command recording. We identify them as older records, not as experiments we have just repeated.

Temporary screenshots, uploads and scratch folders may no longer exist. A report should not suggest that someone can open evidence we no longer have.

### 1.2 Six different kinds of evidence

| Kind | What it means | Example |
|---|---|---|
| Reading the current files | We can point to what the code currently says. | The saved-progress key and the title's size rule. |
| Running a check during the first report | We actually ran a program and recorded its result then. | The 13-width browser check. |
| Git or GitHub records | The version system or online service recorded the event. | A PR's accepted time and a check's success. |
| Older work records | The conversation or project notes say it happened earlier. | The first Python install failure. |
| Owner's live-site check | The owner tried the real website and told us the result. | “I've verified the fixes. All work as intended.” |
| Explanation or suggestion | A possible cause or future improvement, not a proven event. | The idea that the preview container blocked new tabs. |

These are not interchangeable. “The owner says it works on the live site” is useful evidence. It does not tell us every phone and browser they used. “An automatic check passed” is useful too. It does not prove every sentence in the documentation is current.

A link can return an “OK” reply while showing a login page. That does not prove a course is free. A browser controlled by code can pass a touch test without proving the same thing on a real phone with a moving browser toolbar.

### 1.3 Dates need labels too

The main building work happened on **26 and 27 October 2026**. The engineering report and this explanation are dated **1 November 2026**.

Most course research was done on 26 October. Some pages were reread and the playlist changes were checked on 27 October. We have not reread every provider page for this new report.

The saved history uses times with different time-zone labels. The appendices show standardized **UTC** times. Lagos is one hour ahead of UTC. A one-second difference between a Git record and GitHub's accepted time does not mean we merged the same work twice.

“Verified on 26 October” means “checked on that date,” not “guaranteed unchanged forever.” This distinction is especially important for prices and free-access offers.

### 1.4 What happened during the first report

The reporting branch is `arena/8c02879a-fieldnotes-hr`. We expanded a shallow copy of the history so it included the earlier saved work. A shallow copy is like receiving only the last few pages of a diary. We needed the older pages to tell the story properly.

The instruction used was `git fetch --unshallow origin`. The needed software tools were recreated. The main checks were run again, and the original engineering report was written.

For this plain-English task, we are rewriting that report. We are not changing application code, publishing a release, accepting a new PR or sending a commit online.

Private sign-in information, tokens and temporary signed download addresses are not included. The public website address came from the owner; neither report is a fresh inspection of the owner's hosting account or internet address settings.

## 2. What we made

### 2.1 Two connected things

FieldNotes-HR gives a beginner two main things:

1. **A learning library.** It explains what to learn and why, with courses, videos, guides and practical work. It comes as Markdown, PDF, Word-compatible DOCX and a normal webpage.
2. **A learning tracker.** It shows the plan in a webpage, lets the learner mark cards Done, shows progress and keeps a learning streak. It also has reminder controls, backup controls, ten optional tiny creatures and the matching tab picture.

There are five finished files because the tracker is a separate fifth format.

The library is for someone starting from zero in HR and aiming towards recruitment or talent acquisition. It is not a promise of a job. It is not a university degree or a professional licence.

### 2.2 The important numbers

| What we counted | First version | Version described here |
|---|---:|---:|
| Stages | 8 | 8 |
| Learning cards | 26 | 27 |
| Different web addresses used by cards | 21 | 22 |
| Planned study hours | 94 | 94 |
| Entries in the current link-research list | 30 originally | 31 |
| Addresses in the first actually completed link sweep | 30 | Still that same historical group of 30 |

The new first card is an HR Essentials playlist. The old talent-acquisition card now opens the correct direct playlist rather than a general channel.

The study plan did not grow beyond 94 hours. We used a selected one-hour starter allocation for the added playlist. “One hour” is a study budget for selected lessons and notes. It is not a claim that an entire 16-video playlist lasts exactly one hour.

### 2.3 A small website that does not need our own server program

The tracker is one prepared HTML file containing its styles, working code, picture and creature code. Its measured size is **166,050 bytes**—about 166KB if you count a kilobyte as 1,000 bytes.

There is no project-owned account system, database, progress-sync service or analytics code. We do not run a separate backend for the tracker. It uses the browser's storage.

That simplicity has benefits: fewer moving parts and no project server holding everyone's progress. It also has costs: changing browsers or website addresses does not automatically move your saved work.

“No automatic outside downloads” does not mean the whole internet disappears. Opening a course link still visits its provider. The hosting company still receives requests when someone loads the website.

### 2.4 Eight accepted batches of work

We accepted eight PRs:

1. The skill and the original learning library.
2. The borrowed Fieldnotes design and later appearance adjustments.
3. Reliable setup, recorded checks, automatic checks and better instructions.
4. Ten Pals and a preview that recovers properly.
5. Results of the first completed outside-link sweep.
6. Static website publishing settings.
7. Smaller mobile title, correct playlists, safe old progress and smoother creature scrolling.
8. The exact reference tab picture with a carefully limited checking exception.

The appendices list every PR and every saved Git step, not just these short descriptions.

### 2.5 The main lesson

The hardest work was not choosing a fashionable website framework. It was protecting the unchanged borrowed generator while adding project-specific behavior, making the finished files rebuild correctly, saving useful test tools inside the project, and being honest about what blocked checks or incomplete evidence could tell us.

## 3. The original request and the rules

### 3.1 Who the learning plan was for

The learner was an absolute beginner in Lagos, Nigeria. They could study for about five hours each week and wanted to move into HR through recruiter or talent-acquisition work.

They chose a **free-first** plan. That means prefer free learning, but explain useful paid options separately and honestly. They wanted a mix of videos, official documents and written courses—not 27 almost-identical links.

The plan needed to be made specially for this goal. It should begin with basics, build skills in order and produce practical examples a learner could show when applying for jobs.

All five supported output formats were requested. We did not decide that a PDF alone was enough.

### 3.2 What “free” was allowed to mean

These are different claims:

- You can read or watch the lesson without paying.
- You can finish assessments without paying.
- You can get a basic completion record without paying.
- You can get a branded certificate without paying.
- You can earn a recognized professional qualification.

A course might satisfy the first claim and not the others. We had to keep those differences visible.

Search results and roundup articles could suggest leads, but the actual provider's page was needed to support a price or access claim. If the page could not be read, we had to say so. We were not allowed to invent missing prices, exchange rates, enrolment results or test successes.

### 3.3 The borrowed skill must stay unchanged

The user supplied a tool bundle called `resource-learning-library`. It was like receiving a working printing machine with instructions: use it, keep a permanent copy, but do not alter its original parts.

We therefore kept its 12 files unchanged. Local project files handle the extra colors, layout, creatures, saved-progress adjustment and favicon.

That rule matters. If someone secretly changes the borrowed generator, future developers cannot easily tell which behavior came from the original tool and which behavior came from us.

### 3.4 Edit the recipe, not just the finished cake

The owner said appearance changes must live in source or build files. We could not simply open the finished tracker and edit it by hand.

Why? Imagine correcting a printed poster but leaving the computer file wrong. The next print would bring the mistake back. Editing only `out/roadmap-app.html` would have the same problem.

The proper approach is to change the theme or builder and then regenerate the finished page.

### 3.5 Permission before action

The owner added a standing rule: explain that we understand a request and wait for the go-ahead before acting, unless the message already gives permission.

“Write the file” does not automatically mean “publish the change.” At different points the owner first said not to commit or push, then later explicitly allowed committing, pushing, creating a PR and merging it. The later permission replaced the earlier temporary restriction for that work.

This new report has permission to be written. It does not have separate permission to be committed or pushed.

### 3.6 Keep work on the correct branch

Each session had its assigned `arena/...` branch. A branch is a separate line of work. We had to stay on the assigned one rather than quietly switching to `main` or inventing another branch.

The history contains several older session branches. Their names explain where earlier work came from; they are not instructions for us to switch to them now.

### 3.7 The chosen visual reference

The owner chose the project `Field-Notes_Nature-Photography` as the reference for the look. It supplied the dark navy, warm paper colors, bright accents, thick edges, square corners and hard shadows.

We were copying a design language, not copying every feature. For example, the HR tracker did not gain a search system or guided tour just because a reference site had one.

## 4. The complete story in time order

### 4.1 We reconstructed the supplied tool bundle

The original transfer arrived as a Markdown file containing labelled blocks of code. A script pulled those blocks out and recreated 12 real files.

We checked each file's stated size and fingerprint before using it. A fingerprint is a code calculated from the bytes in a file. Matching fingerprints helped show the reconstructed copy was exact.

The temporary upload was historically at `/tmp/arena-coding-uploads/resource-learning-library-transfer.md`. That is a past location, not a promise that the upload is still there.

A personal tool copy helped at first. Later, the important copy was placed inside `.agents/skills/resource-learning-library/`, where the project could keep it through resets.

### 4.2 Python installation hit a safety rule

The generator needed `python-docx`, `reportlab` and `pypdf`. These tools make Word files, make PDFs and read PDFs.

A normal system-wide Python package installation was refused by a protection called **PEP 668**. Its purpose is to stop casual package changes from damaging a Python environment managed by the operating system.

Early work used separate virtual environments, and the older record also mentions a `--break-system-packages` override. That override is history, **not the current recommendation**. The final setup uses a project-only `.venv` folder and a fixed package list.

### 4.3 We built the first library

We collected the learner's choices, researched provider pages and wrote the plan in two forms: a long readable Markdown document and structured JSON for the tracker.

The first library had eight stages, 26 cards, 21 different card addresses and 94 hours. The source had about 6,829 words, and the PDF had 15 pages.

The research kept important limits visible. Coursera's “Enroll for free” did not necessarily mean full free access. Alison's free lessons did not make its branded certificate free. Jobberman's page was only partly readable. LinkedIn prices were not confirmed from a readable provider page.

All five formats were generated and checked. PR #1 stored the tool bundle and the library in the project and was accepted.

### 4.4 We borrowed the reference design

We downloaded a working copy of the Nature Photography reference and inspected its style settings. Those settings became the HR tracker's theme.

The borrowed generator stayed unchanged. We added a local theme stylesheet and a local builder around it.

The owner also asked for durable skill discovery through `skill-issue.in`. We saved project settings for it. The sandbox could not run its usual POST-based tool requests, so we read the catalog and available linked source material instead. Setting it up did not mean every tool call worked.

A temporary browser-check program tested the page at 13 widths. Four rounds of visual requests followed. At one point the local branch history and online branch history did not line up. The older record says a fetch and **mixed reset** fixed the branch pointer while keeping the working changes. That is different from throwing changes away with a hard reset.

PR #2 accepted the design work and its refinements.

### 4.5 We stopped relying on memory and temporary tools

After the design work, a review found repeated weaknesses:

1. The environment forgot tools between sessions.
2. Checks were a manual habit rather than saved project tools.
3. The sandbox could not reach many outside sites.
4. Our additions relied on exact pieces of the frozen generator's output.
5. Content was repeated in several places and finished files could drift out of date.
6. Documents kept adding history without clearly separating old and current instructions.
7. Tiny appearance requests caused repeated screenshot, rebuild and check work.
8. Basic folder, version and configuration housekeeping needed improvement.

An actual missing `docx` import helped confirm the lost-dependency problem. It was not just a theory.

We wrote `RETROSPECTIVE.md` to explain the causes. Then we added a package lock, Makefile, single check runner, saved fingerprints, source comparisons, research-age warnings, rebuild checks, clearer setup/design documents, automatic GitHub checks, a PR checklist and a permanent browser-check program.

We also taught the builder to expose its branding edits for testing without changing the finished tracker. The older record includes clean-setup and fresh-copy trials.

PR #3 included the fixes. A second saved step updated the notes once GitHub checks had actually succeeded. We did not leave “not yet observed” in the notes after observing success.

### 4.6 The owner asked for ten tiny Pals

The reference site's copy had disappeared from temporary storage, so we downloaded it again. Inspection found eight creature types and 14 placements in that reference version. An older note said something different, which is why we looked at the actual source.

The owner chose four things:

- Put creatures only in the interactive tracker.
- Use the real Piixpal engine, not lookalike drawings.
- Make ten placements from eight species, with tinted repeats.
- Spread them down the page instead of putting them all in one strip.

We copied the unchanged engine and sprite scripts, fetched the MIT permission text and wrote local placement, styling and control files.

Our first new check had its own mistake: it demanded a color shift even for the first appearance of a repeated creature. We corrected the rule so only later repeats needed the shift.

Some heading creatures looked too small at scale 2. After visual review they became scale 3, and checks were repeated. The temporary screenshots were not kept as product files.

### 4.7 The preview kept disappearing or returning the wrong page

The preview first used a temporary Python web server on port 8000. Opening `/` returned the tracker. But a HEAD request—a request for headers without the page body—still behaved like a folder listing. We corrected both to use the same route.

Then resets erased the running server, the virtual environment, Node tools, browser files and the server script kept in a cache folder.

There was a worse surprise. The generic snapshot system excluded folders named `out`, so the tracker could return to an older committed version without Pals. A server could run perfectly while serving the wrong old page.

The fix was to save a real server script under `tools/serve_preview.py` and make `make preview` rebuild the tracker before serving it. The server needs only standard Python. A missing-Pals warning adds another clue.

A later reset showed the lasting script survived and could rebuild the correct preview. PR #4 accepted the creatures and preview repairs.

### 4.8 We could not start the link sweep ourselves

The shell environment could not reach arbitrary course-provider websites. A sweep—a program visiting every listed address—needed another environment.

GitHub Actions could do it, but our attempts to start its workflow returned HTTP 403, meaning the request was refused. Reconnecting and trying the available token routes did not grant the missing permission.

We tried a diagnostic `repository_dispatch` event. GitHub accepted that event, but no workflow was listening for it. No sweep started. An accepted message is not the same thing as completed work.

Reading run information worked. Downloading redirected logs and artifacts did not, because the destination hosts were outside the sandbox's allowed connections. Public log pages also needed sign-in.

The owner manually started the workflow in GitHub and pasted the results. We separately confirmed the run was successful. It checked 30 addresses: 27 returned 200 and three returned 403.

We reread the three blocked provider pages using the page-fetch service. Their content supported the previous findings. LinkedIn still could not be read reliably, so its uncertainty stayed.

PR #5 recorded the sweep, findings and rebuilt library files. We did not claim to possess the raw downloaded TSV file when we did not.

### 4.9 We prepared public hosting

The owner proposed Vercel. We explained that this was a static website: publish the finished files, map the homepage to the tracker and do not run the development preview server as a production build.

We also explained that HTTPS does not create reminders that work after the tab closes. Export/import is needed when moving progress to a different website address.

With approval, we added `vercel.json`, a publishing guide and two tests. PR #6 accepted them. The owner deployed the site and supplied the public address.

We did not claim to have performed the owner's deployment or inspected all settings in their hosting account.

### 4.10 The owner found mobile problems

The owner reported these related needs:

1. The main title wrapped too much on phones; reduce it by about a quarter.
2. The HR Learning Lab link did not open the right thing in the YouTube app.
3. Use the direct Talent Acquisition playlist supplied by the owner.
4. Add the foundational HR Essentials playlist before it.
5. Fix the creatures' rapid bobbing or jitter while scrolling.

The title's entire size rule was reduced by exactly 25%. We used clean direct playlist addresses without the extra `si` share-tracking part.

The fetched public playlist information showed 16 HR Essentials videos and 43 Talent Acquisition videos. However, it also included a YouTube error banner. We could read names and descriptions but could not claim that playback or handoff into the phone app had been tested through that fetch.

Adding a new first card could have moved old Done ticks onto the wrong lessons. We spotted that risk before release and gave the new card its own saved label while preserving old labels.

The plan stayed 94 hours. The old sweep stayed a historical 30-address record; it was not rewritten to pretend it had checked the new links.

For creature scrolling, we changed the overlay from staying attached to the screen to moving with the whole document. The later chapter explains why that worked.

PR #7 accepted these changes and rebuilt outputs.

### 4.11 The preview-link mystery

The owner then found that links did not seem clickable inside the embedded preview. A decorative layer covering the links was a reasonable first suspect.

We checked the actual topmost element at all 27 resource links across all 13 widths. The tested browser did not find creatures blocking them. Real mouse input and touch-like input activated the correct playlist links. A normal click also requested the correct new tab.

One possible explanation was the surrounding preview container's rules for opening outside pages. That remained a possibility, not a proven cause.

We added useful tests but did not ship a guessed navigation “fix.” After PR #7, the owner tested the live site and said: **“I've verified the fixes. All work as intended.”**

That is the live acceptance record we have. It is not a list of every phone, browser and network tested.

### 4.12 We matched the tab picture

The owner asked for the exact favicon from Nature Photography. We fetched its actual inline SVG link from `index.html` through GitHub.

The unchanged checker rejected all `<link>` tags, including this harmless approved picture. Rather than weakening the whole rule or editing the borrowed checker, we made a tiny local exception for one exact fingerprinted tag.

Three tests were added. The first browser picture test failed because it assumed the picture's natural size was 32 pixels. Its drawing area was 32 by 32, but Chromium treated its unspecified natural size as 150 by 150.

The picture was correct. Our test assumption was wrong. We changed the test to draw it at 32 by 32 and check the four expected colors, leaving the requested source unchanged.

PR #8 passed the recorded checks and was accepted. We have no later owner message confirming the icon on the live browser tab. Browser icon caching can also hide a fresh change, so we keep that limit visible.

## 5. Where everything lives

### 5.1 The project is a workshop with recipes and finished products

Here is the basic flow:

```text
Long learning document
    -> unchanged document-making tool
    -> Markdown, PDF, Word-compatible file, normal webpage

Structured learning-card list
    -> unchanged tracker-making tool
    -> local theme and progress-label changes
    -> local creatures and tab picture
    -> one finished tracker webpage

Checks compare the recipes, finished products and recorded rules.
The host publishes the finished files, not the whole workshop.
```

The main files have different jobs. Mixing those jobs up is a common cause of mistakes.

### 5.2 The things we are supposed to edit

- `learning-library/src/recruiter-talent-acquisition-library.md`: the long explanation, learning steps, research notes, paid extras and exclusions.
- `learning-library/src/roadmap-app.json`: the labelled data used to build tracker stages and cards.
- `learning-library/src/fieldnotes-theme.css`: the colors, sizes, spacing and other visual rules.
- `learning-library/src/pals/`: creature positions, controls and styles, plus the unchanged engine and its permission text.
- `learning-library/src/favicon-link.html`: the exact approved tab-picture tag.
- `learning-library/tools/build_tracker.py`: the local wrapper that adds our changes to the borrowed generator's result.
- `learning-library/src/verification-manifest.json`: the research-status list and the historical link-sweep record. A manifest is simply an organized list of records.

### 5.3 The things the tools make

`learning-library/out/` contains the five finished files. They are generated, but they are also saved in Git because they are the product people download and the host serves.

This makes old output dangerous. If we change a recipe but forget to rebuild, the public website can still serve the old finished file. Having the right source is not enough.

The finished Markdown intentionally duplicates the source Markdown exactly. That gives people a convenient downloadable copy.

The static library webpage and tracker webpage are not the same thing. The library includes the longer explanations and can be read without JavaScript. The tracker uses JavaScript to build its cards and interactions.

### 5.4 Why there are two tools folders

`learning-library/tools/` makes this specific content. The root `tools/` checks the whole project and runs the preview and browser tests.

This split grew out of the project's history. It is not worth casually moving things just to make the folders look tidier. Commands, imports, tests and documentation already rely on those paths.

### 5.5 Which documents do which jobs

| Document | What to use it for |
|---|---|
| `docs/SETUP.md` | Setting up the working tools and understanding commands. |
| `docs/DESIGN-SPEC.md` | The intended current visual rules, including later additions. |
| `learning-library/DESIGN-SYSTEM.md` | The story of the original design transfer and refinements. |
| `CHANGELOG.md` | A dated list of changes. |
| `RETROSPECTIVE.md` | Earlier causes of trouble and the repairs. |
| `docs/DEPLOYMENT.md` | Publishing and live-site checks. |
| `THIRD-PARTY-NOTICES.md` | Where the creature engine came from and where its licence is. |

Some older sentences are out of date. For example, one setup paragraph still says 26 cards, and an older description still calls the creature layer fixed. We point those out rather than repeating them as current facts.

When an old paragraph disagrees with the actual current files and a clearly scoped test, we should investigate and update the paragraph—not assume the paragraph wins because it is in a guide.

## 6. The learning plan and the research

### 6.1 The eight stages

| Stage | Weeks | Planned hours | Cards now | What the learner is trying to do |
|---|---|---:|---:|---|
| 1. Orientation | 1–2 | 8 | 4 | Understand HR and what recruiters do. |
| 2. Foundations | 3–5 | 14 | 4 | Learn fair hiring, job requirements and basic process. |
| 3. Define the role | 6–7 | 10 | 3 | Explain the job and decide what good performance means. |
| 4. Find people | 8–10 | 14 | 4 | Search for suitable people and communicate well. |
| 5. Screen | 11–12 | 10 | 3 | Compare CV evidence against clear requirements. |
| 6. Interview | 13–15 | 16 | 3 | Ask fair, planned questions and use scoring rules. |
| 7. Offers and Nigerian law | 16–17 | 10 | 3 | Understand local privacy, recruiting and joining-work concerns. |
| 8. Run the process | 18–20 | 12 | 3 | Track work, measure results, prepare examples and apply for jobs. |
| **Total** | **About 20 weeks** | **94** | **27** | A planned route, not a job guarantee. |

At exactly five hours every week, 94 hours is 18.8 weeks. The published schedule uses about 20 weeks to allow breathing room and sensible stages.

The plan does not require completing every linked course from beginning to end. Some cards select particular lessons. Adding the full running time of every provider course would give the wrong total.

### 6.2 The practice work matters

The learner gradually makes a hiring-process diagram, a job description, job requirements, search strings, a shortlist, an interview kit, questions about local law, a simple pipeline and useful measures.

A shortlist is a smaller list of applicants worth considering further. A pipeline is a record of people moving through steps such as contacted, screened and interviewed.

By the final stage the learner should have examples of work, not only certificates. The plan asks them to apply to five junior recruiter or HR assistant roles with that evidence.

Practice should use fake or anonymized candidate details. This project did not gather a real list of candidates' private information.

### 6.3 How research was done

Search helped us find possibilities. The provider's own public page helped establish what was offered.

Each card records a title, provider, web address, format, cost wording, study allocation, reason for inclusion, next action, access notes and a check date where available.

We did not create learning accounts, buy subscriptions or finish enrolments. If a provider said an account would give access, we could record that statement, but we could not honestly claim to have tested the whole signed-in experience.

We did not read every page of every legal PDF. We inspected the arrangement and relevant opening material. We read the Google re:Work index and two guides directly, not every guide the curriculum might refer to.

### 6.4 What each provider contributed and what to watch for

**Saylor.** It says there is no tuition charge, materials are free and a completion certificate is free after reaching the stated 70% final-exam threshold. Assessments need a free account. A proctored college-credit route is a separate matter; the plan does not require it.

**OpenLearn.** The recruitment course is free, with a free statement of participation. An account is needed for tracking, claiming the record and some activities. Its material is older and uses UK examples. It does not replace Nigerian employment law.

**Alison.** Study is free. A branded certificate costs extra. A free Learner Record is different from that paid certificate. We did not establish a current exact checkout price for the certificate.

**University of Minnesota on Coursera.** A button saying “Enroll for free” was not enough. The FAQ said full access could involve paying for the Certificate experience, starting a trial, or choosing a no-certificate route where available. We could not confirm that last route for this course. The card is therefore paid or conditional, not confirmed free. Its suggested ten hours per week also exceeds the learner's five-hour budget, making it an optional deeper course rather than a required pace.

**OpenStax.** The textbook is free and openly licensed. Its US examples and law are useful background, not Nigerian rules.

**O*NET.** This is a free public database of job information. It helps explain tasks and skills. Its job classifications come from the US and need local interpretation.

**Workable.** Public job descriptions, emails and Boolean-search guides are useful. Boolean search means combining words with rules such as AND, OR and NOT to improve a search. Free guides do not mean Workable's commercial recruiting software is free.

**Greenhouse.** Public structured-hiring explanations, worksheets and other guides help with clear evaluation. Again, free learning material does not make the paid software free.

**Google re:Work.** Practical guides support hiring, screening, interviews and related process thinking. The same address is deliberately reused in more than one stage with a different task.

**HubSpot Academy.** A short lesson on managing contacts helps learners practice a simple candidate tracker. It does not turn the plan into a marketing course. It also does not mean every HubSpot product tier is free.

**Jobberman.** The free employer-listing claim remains only partly checked because our reading tool could see a cookie banner rather than enough page content. Paid tiers also exist. A later “OK” web reply did not remove that gap.

**NDPC.** Nigeria's data-protection regulator supplies the GAID document used for local privacy principles and duties. The plan is an introduction, not a complete legal opinion.

**PLAC's Labour Act copy.** This is a free reproduction of statutory text. It is not a guarantee that we have a fully updated legal interpretation or every amendment. Current local advice still matters.

**CIPM Nigeria.** Its examination route is a paid professional membership path. It is not another free beginner course or a qualification someone earns just by checking all the tracker boxes.

**HR Learning Lab.** The public playlists help beginners. Their creator discloses AI-supported production. Important legal or professional claims should be checked against stronger primary sources. Introductory videos are not a professional qualification.

**LinkedIn.** The provider's own help pages could not be read reliably. The recorded prices came from other guides and remained unconfirmed. A successful status code could not fix unreadable content or prove a price.

### 6.5 The exact price claims we recorded

These were the historical provider-published CIPM figures recorded in the library. They were **not reread for this report** and the provider said they could change.

| Item | Historical amount |
|---|---:|
| Application | NGN 10,000 |
| Acceptance | NGN 12,000 |
| Foundation | NGN 55,440 |
| Intermediate I | NGN 57,190 |
| Intermediate II | NGN 58,200 |
| Professional I | NGN 64,050 |
| Professional II | NGN 70,050 |
| Exemptions, depending on case | NGN 20,250–24,300 |

The recorded entry condition was a degree or HND plus five SSCE credits, including English and Mathematics. Undergraduates could enrol, but induction followed graduation. These are recorded requirements, not a new guarantee about today's rules.

Other 2026 guides suggested roughly **USD 39.99 per month or USD 239.88 per year** for LinkedIn Learning/Premium Career, and **USD 170 per month or USD 1,680 per year** for Recruiter Lite. Trial and payment-card conditions were noted. Because readable provider confirmation was missing, these stayed secondary-source estimates.

No exchange-rate conversion, tax, payment-card charge or mobile-data cost was invented. Alison's branded-certificate cost stayed unspecified because the inspected policy did not establish an exact current checkout price.

HRCI on Coursera, AIHR's sourcing/recruitment certificate and Udemy recruiter training were kept out of the confirmed-free set. “Free trial” is not the same as “free whenever you study.”

### 6.6 Things left out on purpose

We did not add Simplilearn SkillUp, LearnTube.ai, LearnCafe and similar “free HR certificate” leads just because an outside roundup said they were free. Some claims were not backed by readable provider pages; one page referred to subscribers.

SHRM, CIPD and HRCI membership toolkits or exam products were not presented as free. Long lists of unverified YouTube channels were rejected as padding. Broad marketing and sales certificates were left out even where the provider genuinely had free learning, because they would pull attention away from the recruiter goal.

We did retain short relevant material, such as the contact-management lesson, when it directly supported a recruiter task.

### 6.7 Why Nigeria needed its own stage

Many accessible free guides come from US or UK organizations. Their methods can be useful, but their job titles, assumptions and laws do not automatically fit Nigeria.

Free, current, Nigeria-specific recruiter courses were hard to find. Primary legislation and regulator guidance are harder for beginners than friendly video lessons, but they provide a stronger local basis. Stage 7 helps correct that imbalance. It does not magically make every imported example locally correct.

### 6.8 Why the different totals are not a contradiction

There are 27 cards, but some reuse the same site. That leaves 22 different card addresses.

The checking list also includes provider policy pages and paid extras, so it has 31 entries. The older sweep happened before the playlist change and still has its own 30-address snapshot.

Current research statuses are:

- 23 entries with a documented, confirmed finding.
- 1 whose free access is unclear.
- 1 that we could only partly read.
- 2 whose provider content we could not reliably reach/read.
- 4 leads or extras without confirmed free access.

“Confirmed” means the recorded access or price finding is supported. It can confirm that something is **paid**.

### 6.9 A current wording problem: “VERIFIED FREE”

The hero says 25 cards are verified free. The code gets that number by counting cost labels that do not start with “paid.” It does **not** look at the research status list.

That means Jobberman's only-partly-checked card is included. So it is safer to say **25 cards are not labelled as paid**, rather than claiming all 25 have equally strong free-access proof.

The two paid/conditional cards are Coursera and CIPM. CIPM can have a confirmed status because its paid nature is documented.

This is a weakness found in the report, not something secretly fixed while writing it. A future change should separate cost, certificate cost and strength of evidence in the data itself.

### 6.10 How we notice research getting old

The list records when a finding was checked. Confirmed findings older than 90 days become stale. Unconfirmed, unclear, partial or unreachable findings are open gaps.

The normal check warns rather than stopping the whole build. A stricter option, `--strict`, turns the warning into a failure.

At the first report's check there were zero findings older than the limit and eight open gaps. Only the first five gap details were printed, though the total correctly said eight. Appendix C includes them all.

A 90-day warning is a reminder to review. It cannot detect a provider changing prices tomorrow. Likewise, a broad old sentence saying all claims were checked must be read alongside the actual dated exceptions, not used to erase them.

## 7. The borrowed building tools and skill search

### 7.1 What a skill is here

In this project, a skill is a bundle of instructions and helper programs for the assistant. It is not the learner's HR skill. The supplied `resource-learning-library` bundle teaches the assistant how to create the library and includes working generator programs.

Its 12 files include workflow instructions, installation/readme documents, a requirements list, four scripts, two examples, tests and an ignore file.

We saved it inside the project rather than relying on a personal installation that could disappear. This is sometimes called **vendoring**: keeping the needed third-party source as part of your own project folder.

### 7.2 How we protect the original copy

`tools/skill-hashes.sha256` lists a fingerprint for every one of the 12 files. The checker complains if a file is missing, changed or unexpectedly added. Ordinary Python cache files are excluded from that comparison.

Even an innocent wording change inside the borrowed skill would break the exact-copy rule. That is intentional. Local explanations belong outside its protected folder.

A fingerprint does not prove the borrowed tool is safe or correct. It proves our copy matches the version we agreed to keep. You can faithfully copy a mistaken recipe; it is still a mistaken recipe.

### 7.3 The skill's five tests

The borrowed tests check five groups of behavior:

1. The Markdown reader recognizes headings, paragraphs, callouts, tables, lists and code.
2. A sample can become Word, PDF and static HTML and pass the supplied checks.
3. The tracker is self-contained and has expected browser features.
4. Tricky text containing `</script>` cannot escape from the embedded JSON and become a new script.
5. The style checker and safe output-file naming behave as expected.

These are useful basic tests, often called smoke tests. They are not a complete check of every document or every security risk.

### 7.4 Updating it must be a deliberate act

`make pin-skill` writes a new fingerprint list. It is for a reviewed, intended upgrade—not a way to silence an unexplained warning.

A careful upgrade means checking where the replacement came from, its licence, all changed behavior, our local wrapper assumptions and saved-progress compatibility. Then run both the borrowed tests and project tests.

Piixpal's MIT licence covers that engine. It does not automatically license the whole HR project, the supplied skill or every linked course. A complete licence review of every project part was not performed.

### 7.5 The skill-discovery service

The owner asked us to use `skill-issue.in` to look for relevant skills for each task. We saved the project connection in `.mcp.json` and `.claude/settings.json`.

**MCP** is a way an assistant can connect to tools. The project files record the connection and permissions. An older global registration in `/root/.claude.json` and installation of Claude Code were part of earlier setup work, but they are not portable website dependencies.

The service's normal tool requests use HTTP POST. Our sandbox could not make those calls successfully. We therefore read the public catalog and fetched available skill instructions and linked rules, including through GitHub.

The design work drew on frontend design, responsive layout, web interface rules, design-system patterns, accessibility, visual-taste guidance and UI/UX guidance. Those helped with colors, spacing, focus indicators, form names, touch targets and consistent components.

For this plain-English task, the catalog was checked again. The available design-guidelines material was not a suitable writing-specific skill, so it was not presented as a writing tool we had executed. No specialist writing skill was newly installed or run. The rewrite uses the first report as its main source.

The honest distinction remains: **the connection was saved and useful material was read; the blocked MCP tools did not suddenly become working tools.**

## 8. How the five finished files are made

### 8.1 A separate toolbox for Python

A virtual environment is a project-only toolbox. It avoids changing the operating system's own Python tools.

The toolbox lives in `.venv`. The fixed package list is `requirements.lock`:

| Tool | Version kept for this project | Its place in the toolbox |
|---|---|---|
| charset-normalizer | 3.5.2 | Helps software handle text encodings. |
| lxml | 6.1.3 | Works with structured document markup. |
| pillow | 13.0.0 | Works with images. |
| pypdf | 6.21.2 | Reads PDFs, including text used for comparisons. |
| python-docx | 1.2.0 | Makes/reads Word-compatible documents. |
| reportlab | 4.5.1 | Makes PDFs. |
| typing_extensions | 4.16.0 | Supplies Python typing helpers needed by software. |

Python 3.11 is the supported baseline. The earlier fresh local check used 3.11.2. Freezing versions reduces surprises from new package releases. It does not freeze the operating system, every shared library or the package installer itself.

The original skill allows wider version ranges. Our project lock keeps the chosen resolved versions instead.

### 8.2 A small setup weakness worth knowing

`make bootstrap` creates the environment when `.venv/bin/python` is missing. If that executable already exists, Make treats the target as present.

So if someone changes the lockfile or deletes some packages but leaves that Python executable, `make bootstrap` may only print a version rather than repair the toolbox.

The next person must recreate the environment or explicitly install from the lock in that case. Do not assume a printed Python version proves every package was refreshed.

### 8.3 One command makes the finished files

`make build` first runs the unchanged document generator, `docx_render.py`, on the long Markdown source. It supplies a title, subtitle, output name and short front-page description.

The generated base name is `Recruiter-TA-Library`. The title used for the long documents is “From zero to first recruiter role,” with its beginner-roadmap subtitle. The front-page metadata still mentions Lagos, 26 October 2026 and about 94 hours over 20 weeks.

That old date is not automatically updated by a later edit. We should not bump it without real research, but the static date also should not mislead readers about later changed cards.

The tool makes PDF, DOCX, Markdown and static HTML. Then our local `build_tracker.py` makes the tracker.

### 8.4 The tracker gets a safe local wrapper

Imagine an unchanged printing machine produces a basic poster. We add a project-controlled finishing station afterward, rather than opening the machine and changing its parts.

The tracker wrapper:

- Calls the unchanged generator with the JSON card data.
- Applies eight known branding edits.
- Adds the theme stylesheet.
- Replaces one exact saved-resource-label function to protect old progress.
- Adds the pinned favicon.
- Uses three known places to insert Pals styles, controls and scripts.
- Checks the finished result for forbidden outside dependencies.

The eight branding edits cover the browser title, page metadata, skip link, eyebrow label, footer credit, reminder input information, import-file input name and hero fact chips.

“Metadata” means information about the page, such as a description and theme color. A skip link lets a keyboard user jump to the roadmap instead of passing repeated content.

### 8.5 What an anchor means in the builder

Here, an anchor is a known piece of the generator's text that the wrapper looks for. For example, it expects a particular title tag before replacing it.

If that piece disappears, the build should fail loudly instead of silently producing a half-themed page. Tests deliberately break the expected pieces and confirm the wrapper complains.

General replacements are limited to one match. That is **not** the same as proving there were never duplicates: some replacements stop after the first match. The saved-key replacement and favicon have stricter exact-count guards.

This is more reliable than editing random text, but it is still a fragile connection. If the borrowed generator changes its HTML, the finishing station may no longer recognize its output. An upgrade requires review, not simply wider and weaker search patterns.

### 8.6 What “self-contained” means

The tracker does not need to fetch an external font, image, stylesheet, frame or script to start working. CSS and JavaScript are inside the HTML. Creature drawings are inside the code. The tab picture is an approved inline SVG data link.

This makes the file portable. It can be opened as a local file for many basic actions, though browser storage and security behavior may differ. Hosted browser notifications normally need HTTPS.

The courses themselves are not packed inside the file. Clicking a course still needs the provider's website and any account, payment or connection that provider requires.

### 8.7 The exact-build comparison

`make check-drift` makes temporary fresh outputs and compares them with the saved finished files.

| File type | How it is compared | Why |
|---|---|---|
| Markdown | Exact bytes/text | It should reproduce exactly. |
| Static HTML | Exact bytes/text | The same inputs should make the same page code. |
| Tracker HTML | Exact bytes/text | Our complete wrapped tracker should match. |
| PDF | Extracted page text | Date/metadata bytes can change even when readable content is the same. |
| DOCX | Contents of archive entries | A DOCX is a package of internal files; outer timestamp details can vary. |

This is what “reproduce” means in the report. It does not mean every binary byte must always be identical everywhere.

There is an important limit for PDFs: matching extracted text does not prove exactly matching visual layout. The same words could wrap differently. Page design needs visual review when it matters.

### 8.8 What we save and what we throw away

The five finished files stay in Git. Environment folders, downloaded Node packages, browser caches, logs, screenshots and local link reports normally do not.

`.gitignore` lists things Git should leave out. `.gitattributes` tells Git how to handle file types and line endings, including binary document files.

`make clean` removes selected disposable reports and caches while keeping `.venv`. It is not a complete reinstall command and does not delete the delivered documents.

The sandbox has its own snapshot rules on top of Git's rules. That extra layer is why an `out` folder could return to the older committed version after a reset, even though generated files are legitimate project products.

## 9. How the tracker remembers your work

### 9.1 How the cards appear

This is plain JavaScript, not a React, Vue or Svelte application. It reads the JSON data and creates the webpage parts.

Each stage uses a native expandable `<details>` section. The first one starts open. Each learning resource becomes an article with its title, small labels, explanation, action, link and Done checkbox.

Most text is added as text, rather than treated as new HTML. That helps prevent ordinary content from turning into unexpected webpage instructions.

When a checkbox changes, the app updates the saved state, today's activity if appropriate, the card's appearance, the overall progress and the stage's percentage.

### 9.2 Cards count equally, not by hours

Overall progress counts completed cards. A one-hour starter card and a longer course both count as one item.

With 27 cards, one Done card rounds to 4%. It does not mean 4% of the planned study hours are complete.

“Next up” is the first incomplete card in the plan's order. It is not a personalized recommendation system.

The borrowed generator can also track a stage with no cards through a stage-complete label. This plan does not currently need that feature because every stage has resources.

### 9.3 The browser cupboard

The app keeps a small JSON record in localStorage. Its storage name is:

```text
rll-roadmap-progress-v1:rll-recruiter-ta-2026-10-26
```

That name combines the generator's prefix with the fixed `storage_id` in our JSON. Keeping a separate fixed ID means a normal display-title change does not have to lose saved progress.

If the ID were absent, the generator could fall back to the title. It turns the chosen name lowercase and changes groups of other characters into hyphens.

A simplified example of the saved record is:

```json
{
  "done": { "s0-r0": true },
  "activityDates": ["2026-10-27"],
  "reminderTime": "19:00",
  "notificationsEnabled": false,
  "lastNotificationDate": ""
}
```

This is an example, not a real person's private file. `true` means that saved label is marked complete. `19:00` means 7 p.m.

Only labels belonging to current cards affect the displayed card count. Unknown old labels may remain in the record without counting as current work.

### 9.4 What happens if storage fails

If saved data cannot be read, the app uses defaults. If saving fails, it tells the user it could not save and suggests exporting progress or using another browser.

The current page can still remember work in its running memory for a while. That is not the same as safely saving it for later. Closing or reloading can lose unsaved changes.

There is no account to recover the record from a server.

### 9.5 Why the new first card needed special care

Originally, the first stage's three cards had position-based labels:

```text
s0-r0
s0-r1
s0-r2
```

Think of them as shelf labels. If you put a new book on the first shelf and slide the old books along without changing the records, a tick for the old first book could suddenly mean the new book.

We did not allow that. The new HR Essentials card has `hr-essentials-v1`. The old cards keep their old labels:

| Current Stage 1 position | Card | Saved label |
|---:|---|---|
| 1 | HR Essentials | `hr-essentials-v1` |
| 2 | Talent Acquisition | `s0-r0` |
| 3 | Saylor PRDV226 | `s0-r1` |
| 4 | OpenStax chapter | `s0-r2` |

Computer indexes begin at zero, which is why the code uses indexes 0–3 for those human positions 1–4.

The storage name and backup format stayed the same. Other stages kept their existing position-based labels.

A browser test loads old saved flags and expects Stage 1 to show `[false, true, false, true]`: the new card not done, the old first done, old second not done, old third done.

This solves **this insertion**. It is not a general solution for every future reorder. Giving every stage and resource a permanent ID is recommended later.

### 9.6 How streaks work

A streak counts consecutive local calendar days with recorded learning activity. The app uses the device's date, not a forced Lagos clock and not a UTC date.

Completing a card logs today. Just opening the page or opening a resource does not. Completing more than one card on a day does not add duplicate dates.

If you uncheck a card, its Done flag goes away, but the activity record for that day does not. That is reasonable: undoing a tick does not prove you did no learning.

If today has no activity yet, a streak can still continue through yesterday. The helper that finds previous days uses local noon, which helps avoid some midnight and daylight-saving-time problems.

Changing device time zones or travel still follows device dates. This is not a central attendance system with a fixed world clock.

### 9.7 Export: make your own backup

Export creates a local download named `learning-roadmap-progress.json`.

It contains the format version, title, Done map, activity dates and reminder time. It does not contain browser notification permission, the last notification date or the Pals on/off setting.

The code creates a temporary browser download address for the file, clicks it and releases that address shortly afterward. It does not upload the file to our server.

The file can reveal study dates and reminder habits. It is personal data even though it is not a candidate database.

### 9.8 Import: bring the backup back

Import reads a selected local file. It checks that it looks roughly like the expected progress data, filters date-shaped strings, optionally accepts a time-shaped string, saves it and rebuilds the cards.

The checks are simple, not a complete format police force. They do not fully enforce:

- The backup version or matching roadmap title.
- Real dates rather than just `YYYY-MM-DD` shapes.
- Real time ranges rather than just `HH:MM` shapes.
- Only known Done labels with true/false values.
- A maximum file size.
- Rejection of every odd object, array or null shape.

Use your own trusted exports. Better validation and full backup-cycle tests are recommended, not claimed as already implemented.

### 9.9 Reset and rebuilding the page

Reset asks for confirmation. If accepted, it clears progress and streak history and restores defaults, including notifications off.

Reset and import replace the roadmap's current HTML nodes with freshly built ones. A node is a particular webpage element in the browser's memory.

This matters for Pals. A creature attached to an old heading would otherwise still point at an element that no longer belongs to the page. A watcher notices the replacement and reattaches creatures to the new headings.

### 9.10 Reminder controls

The default reminder time is 19:00. The owner agreed to hide the visible “Reminder time” label. The input still has an accessible name and a title so its purpose can be announced or identified.

The app asks the browser for notification permission only after the user presses the button. It handles missing support, an insecure page, denied permission and other errors with an explanation on the page.

A saved setting saying “notifications enabled” cannot itself grant permission. The browser must still say permission is granted.

### 9.11 When a notification can appear

The app checks immediately, every 60 seconds and when the tab becomes visible again. All these conditions must be true:

1. Notifications are enabled in the app.
2. The browser supports them and permission is granted.
3. Local time has reached or passed the chosen time.
4. No notification has already been recorded today.
5. No learning activity has been recorded today.

The notification asks the learner to return to learning. Clicking it focuses the window and closes the notification. If displaying it fails, the app keeps its on-page message.

There is no service worker, push server or server-side reminder schedule. A service worker would be a special browser background program; we did not add one.

Tabs can be slowed, suspended or closed. Phone operating systems have their own restrictions. Therefore reminders are checked **while this page can run**, not promised after the browser closes.

HTTPS helps with permission. It does not give a static page magical background alarm powers.

### 9.12 Moving between addresses or devices

A browser keeps separate storage for separate origins. A local file, sandbox preview, temporary deployment, live Vercel address and a future custom domain do not share one storage cupboard.

Different browsers and profiles are also separate. Private browsing, site-data deletion or browser storage cleanup can erase progress.

Before moving, export. On the new address or browser, import. That is the current transfer method.

Pals use another name, `fieldnotes-hr-pals-v1`, for their preference. That setting is not in the progress backup. You may have to turn Pals off again after moving even when progress imports correctly.

Two tabs also do not coordinate through a storage-change listener. Each can save its own current idea of progress and overwrite the other. There is no multi-tab synchronization promise.

## 10. How we changed the look

### 10.1 A shared set of colors

A design system is a reusable set of visual decisions. A token is a named value in that system, like “ink color” instead of scattering the same color code everywhere.

| Name | Exact color | Job |
|---|---|---|
| Ink | `#11142B` | Main text and dark page frame. |
| Paper | `#FFF8E7` | Warm main sheet. |
| Cream | `#FFFDF6` | Card surfaces. |
| Rule | `#1E2553` | Borders and dividing lines. |
| Muted | `#565C73` | Less important text. |
| Blue | `#3768FF` | Main hero color and focus accents. |
| Blue ink | `#2C55DA` | Links. |
| Cyan | `#65E8FF` | Bright hero border/accent. |
| Pink | `#FF4E91` | Hard shadow. |
| Yellow | `#FFE168` | Eyebrow and paid-cost labels. |
| Green | `#5EE780` | Free-cost labels. |
| Orange | `#FF9958` | Time-related accents. |

The page uses fonts already available on the device: a monospace style for interface details and a normal system sans-serif for reading text. Monospace letters take equal-width spaces, like typewriter text. Sans-serif letters lack the small decorative strokes found in some print fonts.

No outside web-font download is needed. Thick edges, square corners and solid-offset shadows match the reference, rather than a soft rounded generic dashboard.

Some generator color names are redirected to the new tokens. Other fixed styles are overridden later in the stylesheet.

### 10.2 The hero and its boundaries

The hero is the big introductory block at the top of the page. Its eyebrow is the small heading above the main title.

The owner asked us to remove the colored bars above it but keep the three squares above the footer. The hero should fill the top of the framed sheet.

“Remove the gutter” meant remove the small inner gap, **not** stretch the hero across the whole browser width. That clarification protected the framed design and avoided unwanted overflow.

The eyebrow had to be dark ink, not a pale inherited color. The pink shadow had to sit below the hero; a mistaken side-only result was corrected.

The owner wanted tighter spacing but asked us not to shrink the eyebrow-to-title gap. We kept that distinction.

### 10.3 Four earlier appearance rounds

The first design work was refined in four rounds:

1. Transfer colors, edges, shadows, square corners, decoration and print rules. Remove top bars, add exact footer credit, darken eyebrow, put links and Done controls at the bottom of cards.
2. Give metadata labels distinct colors, equalize stage-introduction margins, use square outcome bullets, add link arrows, align hero edges and enlarge the title.
3. Make subtitle and fact chips 25% smaller, make progress cards 20% larger and split a shared rule so card changes did not accidentally change chips.
4. Increase the title 40% once, line stage-header parts up on a common text baseline, hide the visible reminder label while keeping its accessible name, and tighten hero spacing.

The “increase 40%” wording appeared twice. We treated it as one requested increase, not two increases multiplied together.

### 10.4 The later mobile title reduction

The larger title later wrapped too much on phones. The owner then asked for a 25% reduction. This was a separate later request, not a reversal hidden inside the four rounds.

The current rule is:

```css
font-size: clamp(2.2365rem, 6.5205vw, 5.733rem);
```

In plain terms: let the title grow with the browser width, but do not go below the minimum or above the maximum.

At the usual 16px base font size, the minimum is 35.784px and maximum 91.728px. The earlier three values were `2.982rem`, `8.694vw` and `7.644rem`. Multiplying each by 0.75 gives the new rule.

Earlier the maximum was about 122.3px. The fresh recorded browser check saw about 35.8px at phone widths and 91.7px at wide desktop widths.

### 10.5 Card layout and exact credit

Resource links sit at the bottom-left; Done checkboxes sit at the bottom-right. Stage-introduction margins are balanced. Outcomes use filled square bullets. Every resource link has a small northeast arrow, ↗.

The footer says exactly:

> Made with love and fried plantain, by Moyinoluwa

The three colored squares remain above it. Checks measure footer alignment instead of guessing it from the stylesheet.

### 10.6 The small colored labels

Provider, format, study-time and check-date tags use a repeating palette. Cost tags keep useful meaning: green for free-style labels and yellow for paid-style labels.

“Every tag gets its own color” means the roles/cycle have differentiated fills. It does not mean all tags across all 27 cards have globally unique colors.

Historical color-contrast measurements against the ink color were about 8.59:1 to 14.00:1. Higher contrast generally makes text easier to distinguish from its background, but it does not solve tiny text.

The code decides some paid styling by finding words or currency marks, including `paid` and `NGN`, in a text label. It is not using a complete structured pricing system.

### 10.7 The screen-size checks

We used these CSS-pixel widths:

```text
320, 360, 390, 430, 600, 620, 700,
900, 1024, 1200, 1320, 1440, 1920
```

The tests check side overflow, heading size, tag colors, dashboard collisions, card controls, basic heading structure, footer alignment and creature interference.

Initially the visual tests opened all stages. That did not fully represent the normal first view. We added separate checks at 320, 900 and 1440 with only the first stage open.

Toolbar buttons and stage summaries meet the test's 44px minimum-height rule. This does not mean every clickable thing has a 44-by-44px area.

### 10.8 Choices still worth reviewing

Small chips were historically about 9.12px. The visible reminder label was removed by agreement. Those choices can still be difficult for some people, even with good contrast and accessible names.

We did not earn a formal accessibility certificate. We did not fully test translated long labels, every screen reader, large zoom, right-to-left text or every high-contrast setting.

## 11. The ten tiny creatures

### 11.1 Where they came from

The engine is **Piixpal v0.4.0**, from <https://github.com/diiviikk5/Piixpal>. We copied its inert template from the Nature Photography reference.

An inert template is stored webpage content that does not run just because it is present. Our controller decides when to activate it.

The permission text is `learning-library/src/pals/LICENSE-MIT.txt`. The project also points to it from `THIRD-PARTY-NOTICES.md`.

The engine payload stays unchanged and has this fingerprint:

```text
298776d7bbe408cd3146f61fbb38ec8fddaa2facb1db99c3f013638f5d20ea75
```

You do not need to read that aloud. A developer can compare it to detect an unintended engine change.

### 11.2 Every placement

| # | Creature type | Where it sits | Extra setting |
|---:|---|---|---|
| 1 | bitbug | Main title | Text edge; position value 0.9. |
| 2 | lurk | Subtitle | Position 0.88. |
| 3 | moss | First dashboard panel heading | Position 0.9. |
| 4 | pip | Next-up sentence | Position 0.85. |
| 5 | capy | Reminder summary | Position 0.5. |
| 6 | bumble | Stage 1 heading | Scale 3; position 0.9. |
| 7 | shel | Stage 3 heading | Scale 3; position 0.9. |
| 8 | frog | Stage 5 heading | Scale 3; position 0.9. |
| 9 | moss | Stage 7 heading | Color shift 320; scale 3; position 0.88. |
| 10 | bumble | Footer | Color shift 205; scale 3; position 0.5. |

The position values tell the engine where along the target to place the creature. Scale changes its size. Hue changes its color family.

There are eight species and ten placements. The repeated moss and bumble are tinted differently. We did not invent ten new species.

Targets are words or prose-related elements, not links, buttons, checkboxes or time controls. This matters because the creature canvas can receive pointer input and could steal a tap if placed badly.

### 11.3 How they start

The engine code is inside the page but waits until the browser has an idle chance to load it. We use `requestIdleCallback` with a two-second timeout where supported, or a 1.2-second timer otherwise.

It loads once. Rendering removes the old project-owned creature elements and creates the current set. Their custom elements are marked `aria-hidden` so decoration is not supposed to become meaningful reading content for assistive tools.

We catch decoration errors so a failed creature does not stop learning progress. The tradeoff is that some creature failures may be quiet. Explicit count and placement tests are therefore important.

### 11.4 On, off and reduced motion

The control says “Pause tiny pals” when they are on and “Enable tiny pals” when off. Its pressed state and a live status message describe the state.

The preference is saved separately. If the device requests reduced motion, Pals start off even if an older saved setting says on. A visitor can explicitly opt in.

Print rules hide the creatures and their controls. They do not belong on paper.

We do not have complete evidence for every possible live change of the operating system's motion setting. The controller reads it at startup rather than listening for every later change. Also, ordinary CSS outside a Shadow DOM does not necessarily reach its inner animation parts.

### 11.5 Why scrolling was shaky

Originally the creature overlay stayed attached to the screen. The main page moved underneath it, and JavaScript had to keep correcting creature positions.

On a phone, scrolling can be moved by the browser's graphics system before the main JavaScript thread catches up. A creature can briefly lag behind its word, then jump back. Repeating that can look like rapid bobbing.

The fix made the overlay belong to the whole document instead. When the browser scrolls the document, the creatures move naturally with it.

The exact local rule is:

```css
body { position: relative; }
div[data-piixpal] {
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
  overflow: clip !important;
}
```

The full width and height matter. A wrongly sized layer could cut off creatures. Clipping should happen at the whole document boundary, not at a tiny or screen-only box.

We did not change creature speed or rewrite the borrowed engine to hide the problem.

### 11.6 How we checked the explanation

The test freezes the engine's animation loop, scrolls by 240px and measures where actors move before JavaScript can correct them.

- With the document-positioned layer, native movement error is **0px**.
- When the test temporarily returns the layer to fixed positioning, error is **240px**.

This second case is a control experiment: deliberately restore the old condition to see whether the expected problem returns.

The first attempt measured no scroll movement because smooth scrolling had not completed immediately. That was a test timing mistake. The test now asks for instant scrolling. We did not change the user's normal page just to satisfy the experiment.

The recorded fresh result was `delta=240, maxError=0, fixedError=240`. The owner's live acceptance supports the practical improvement, but we still did not test every mobile graphics system.

### 11.7 “No blocked controls” is not “no overlap anywhere”

The browser tests count ten actors, inspect the real layer and check whether any creature covers the center of a control. They also limit the largest rectangular overlap to **1,100 square pixels**.

The fresh run found some edge overlap of roughly 555–560 square pixels at intermediate widths, often near a stage summary. That is below the allowed limit, and control-center hits were zero.

So we should not claim absolutely zero overlap. The intended effect lets creatures sit near words without blocking important interaction areas. Tests also check every resource link across the width list and check the normal collapsed layout.

### 11.8 Pause does not yet prove zero power use

Pausing removes the visible project creatures, and tests see zero placements. The already loaded shared engine or animation loop may still exist.

We did not measure complete CPU shutdown, battery use or a long paused session. If that matters later, profile it and add a reviewed stop/cleanup method rather than promising the current button uses no processing at all.

## 12. Checking the outside links

### 12.1 Why the sandbox could not do everything

The sandbox allows selected internet hosts, not arbitrary provider websites. Shell requests to providers could fail with TLS/certificate or connection errors and produce `000`, meaning no proper HTTP reply was obtained.

The page-fetch service is a different tool running through a different route. It could read some pages that shell curl could not. We must not pretend both tools have the same network access.

Disabling certificate checking was not adopted as a way to make results look successful.

### 12.2 What the sweep script does

`learning-library/check-links.sh` visits the listed addresses and prints a small table. A TSV is a text table whose columns are separated by tab characters.

Its curl command follows redirects, allows up to 25 seconds, records the HTTP code, keeps normal TLS checks and suppresses error text. It does not set a special user-agent name.

HTTP status meanings here include:

- **200:** the server returned an OK response. The body could still be a login wall or wrong content.
- **403:** the request was refused. It could be bot filtering rather than a dead page.
- **500:** the server reported an internal error.
- **000:** no normal HTTP response was obtained.

There is a small current script weakness: curl can print its own `000` and the fallback can add another `000`, making `000000`. A future cleanup should normalize that transport error. The report does not pretend this has already been fixed.

### 12.3 The automatic schedule

The `link-check` workflow can be started manually and is scheduled for Mondays at **06:17 UTC**. Its cron setting is `17 6 * * 1`.

It checks out the full project history, runs the script, writes a result summary, lists non-2xx results, produces a freshness warning and uploads `link-status.tsv` under the artifact name `link-status`.

It is a **report**, not a rule that every non-200 must break the entire project. Providers can reject bots while serving real people. An OK response can also be misleading. Human reading is still needed before changing a free-access claim.

A schedule written in a file is not proof that every scheduled run has happened. The audit saw the manual run below. As of the report date, the next Monday was 2 November; we do not claim a future result.

### 12.4 The one completed sweep we have evidence for

| Detail | Recorded value |
|---|---|
| Run number | `40471064309` |
| Address | <https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40471064309> |
| How it started | Owner manually selected `workflow_dispatch` in GitHub. |
| Created | 27 October 2026 at 08:04:47 UTC. |
| Code version | `0a3f440`, after PR #4. |
| Result | Success. |
| Addresses | 30. |
| HTTP results | 27 × 200 and 3 × 403. |
| Raw file | Upload succeeded, but the sandbox could not download it. |
| Evidence we had | Owner-pasted summary plus independently checked run information. |

The three 403 pages were the OpenLearn recruitment course, Saylor's FAQ and NDPC's GAID PDF. Rereading them through the page-fetch service supported the earlier content findings.

The difference between a curl refusal and a readable page suggested bot filtering. We did not inspect those providers' internal firewall rules, so that is an interpretation, not a behind-the-scenes diagnosis.

### 12.5 Why LinkedIn stayed uncertain

The pasted summary implied LinkedIn returned 200 to curl. Our reading tool still got a refusal or error and could not establish the actual provider information.

So we did not promote the recorded third-party prices into confirmed provider prices. The historical notes call the 200 a login wall; without the raw response body, the safest conclusion is simply that it did not prove readable content or pricing.

### 12.6 Keep the old checklist frozen

The current address list has 31 entries. The first sweep's `link_sweep.urls` list still has the exact older 30, including the old channel link rather than both new playlists.

The project has separate checks for the current list and for the old sweep's internal totals. That prevents a later editor from silently giving the first sweep credit for links it never visited.

Because we could not get the raw TSV, we cannot claim to have rebuilt the 27 successful rows directly from it. Their codes come from the summary totals and complete non-success list. Appendix C explains that again beside the full snapshot.

## 13. Keeping the preview working

### 13.1 What a preview is

A preview is a temporary way to try the project before publishing it. A small server sends the finished page to a browser. It is not the same thing as the public production website.

The lasting server script is `tools/serve_preview.py`. It uses Python's standard library, so it does not need the document-building packages just to serve a page.

The normal command is:

```sh
make preview
```

That rebuilds the tracker and serves it on port 8000. A port is a numbered doorway to a computer service. An alternative is:

```sh
make preview PORT=8001
```

The server listens on `0.0.0.0`, meaning it can receive connections through the sandbox's preview system. Binding only to `127.0.0.1` would mean listening only inside the machine, which is wrong for this user-facing preview arrangement.

### 13.2 Routes and warning signs

The preview serves only `learning-library/out`. Visiting `/` or `/index.html` maps to the tracker for both GET and HEAD requests.

GET asks for the page; HEAD asks for the response headers without its body. Treating them differently made an earlier check confusing, so the mapping was shared.

The server warns if expected Pals signs are missing. That does not replace all tests, but it helps catch a preview accidentally serving the old pre-Pals tracker.

The tracker is rebuilt at preview start. PDF and Word files are not rebuilt then, avoiding unnecessary timestamp changes to those binaries.

### 13.3 Why a browser's localhost is not our localhost

The owner's browser runs on their device. The preview server runs in the sandbox. `localhost` in the browser means the owner's own device, not our sandbox server.

This project avoids the problem because it has no browser-side calls to a local backend. It does not need a proxy for a second service. If a backend is added later, the browser should use properly routed addresses rather than hard-coded sandbox localhost URLs.

A long-running preview should be started with the environment's process manager, not a one-shot command that stops being managed after a timeout.

### 13.4 The exact reset trap

The troublesome sequence was:

1. Sources were edited and a new tracker with Pals was built.
2. The preview and caches disappeared during a reset.
3. The snapshot rules skipped `out`, restoring the older committed tracker.
4. Restarting a generic server worked.
5. The browser received a healthy-looking but old page with no Pals.

The error was not “the creatures need new artwork.” It was “we served the wrong finished file.” The durable rebuild-on-start command fixes the right layer.

### 13.5 What lasts and what must be recreated

**Expected to last:** saved source files, settings, scripts, locks and committed outputs.

**Not safe to rely on:** running processes, `.venv`, `node_modules`, downloaded browser binaries, screenshots, test caches, `/tmp` uploads, global installs and temporary reference-project copies.

A reset does not automatically mean the code is lost. A restarted process does not automatically mean the right code is being served. Recovery needs both checks.

### 13.6 Keeping browser testing available

The original scratch browser tools disappeared. The permanent harness uses `puppeteer-core` and a Chromium package distributed through npm.

That avoids needing a separate blocked browser-download host. The harness unpacks the required AL2023 shared libraries and points Chromium to them. A shared library is another piece of native software the browser needs to start.

Earlier launch failures from missing libraries were environment failures, not bad page layout.

The packages are fixed by `tools/visual/package-lock.json`. The setup is Linux-oriented and uses Node 22 or newer within the specified supported range, with GitHub checks fixed at Node 22.22.3. It is not a promise that the same browser binary runs on every computer type.

## 14. Putting the project on the internet

### 14.1 Publishing finished files

`vercel.json` says:

- There is no chosen application framework.
- There is no install command on the host.
- There is no build command on the host.
- Publish `learning-library/out`.
- Rewrite the homepage `/` to `/roadmap-app.html`.

Those empty commands are intentional. The project checks and saves the finished files before hosting them. The public host does not need to run our Python document workshop for each release.

If someone later wants the host to build the files, they must deliberately set up the needed environment and rebuild checks. That is a changed publishing process, not a harmless one-line adjustment.

### 14.2 Why we did not redirect everything to the tracker

Only the homepage is rewritten. A catch-all rule would send every unknown path to the tracker.

That can break downloads. A browser asking for a PDF might receive HTML for the tracker instead. The URL could look right while the content was wrong.

The two publishing tests protect the limited homepage rewrite and output-only directory. They do not inspect the actual owner's hosting dashboard.

### 14.3 The expected public paths

| Path | What it should open |
|---|---|
| `/` | Tracker. |
| `/roadmap-app.html` | Tracker directly. |
| `/Recruiter-TA-Library.html` | Long normal webpage. |
| `/Recruiter-TA-Library.md` | Markdown document. |
| `/Recruiter-TA-Library.pdf` | PDF document. |
| `/Recruiter-TA-Library.docx` | Word-compatible document. |

There are no project API routes and no custom application-wide missing-page handler. Course links point outside the project.

Publishing just `out` also avoids intentionally exposing the workshop's source and helper folders as normal site files.

### 14.4 What the online checks showed

PR #8 had successful repository checks and a successful Vercel deployment check. Its recorded build and browser job durations were about 17 and 19 seconds. Those are historical timings, not promised future speeds.

During the first report, the checks for the accepted merge were also inspected. Both repository jobs succeeded on run:

<https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40485000208>

A hosting check succeeding is not the same thing as someone seeing the new icon on a real tab. The browser may cache the old picture. Nor does hosting success prove every outside lesson plays.

### 14.5 What we can say about the live site

The owner supplied the public address and confirmed the PR #7 fixes worked. That is real user feedback.

We did not independently browse production for these reports. We did not inspect DNS, CDN cache settings, account ownership, response-security headers or every hosting environment option.

We also did not establish a later owner confirmation of the PR #8 live favicon. We know the repository and check results; we do not expand them into a claim about every production detail.

## 15. The little picture on the browser tab

### 15.1 Exact match, not a similar drawing

The requested picture is the Nature Photography favicon. It has a dark square background and three horizontal bars: yellow, cyan and pink.

The source is an SVG inside a data URI. That means the small picture's drawing instructions live in the link itself rather than in a separately downloaded image.

Its internal drawing area is `0 0 32 32`. The exact stripped tag is saved in `learning-library/src/favicon-link.html` and pinned to this fingerprint:

```text
ab629e3127cc247eb5077d4168f0a612b19d4c7cb05e2a43d5c3dc016449c9dd
```

The whole tag is pinned, not just the beginning of the address. Otherwise a different SVG, extra event-handling instruction or unexpected attribute could sneak through the exception.

### 15.2 A checker exception like a named guest pass

The borrowed HTML checker rejects every `<link>` tag. That is useful for preventing outside dependencies, but it also rejects this approved inline favicon.

We did not rewrite the borrowed checker. Instead:

1. Read and fingerprint the approved source.
2. Refuse it if its fingerprint changed.
3. Put it before the closing head tag in the built tracker.
4. Require one and only one exact approved tag in the result.
5. Make a temporary checking copy with only that exact tag removed.
6. Run the original checker on the temporary copy.
7. Deliver the real page with its favicon still inside.

It is like allowing one named guest through a rule, not unlocking the door for everyone. Any other link tag still faces the original restriction.

### 15.3 What the three picture tests cover

The first checks the data-link type, SVG structure, drawing area, four rectangles and all four colors.

The second checks the actual delivered tracker has the one approved favicon and that removing it for checking leaves no other link tag.

The third tries six bad variations and expects refusal:

- Approved picture missing.
- Approved picture duplicated.
- Remote image substituted.
- An extra `onload` instruction added.
- A remote stylesheet added elsewhere.
- An unapproved extra inline picture added.

These are focused tests. They work alongside the full self-contained-page and rebuild checks.

### 15.4 When the test, not the picture, was wrong

The SVG says its drawing coordinates run across 32 by 32 units. It does not declare explicit natural width and height.

The first browser test assumed its natural size would therefore be 32 by 32. Chromium reported 150 by 150. That did not mean the wrong picture had been copied.

The corrected test draws the exact image onto a 32-by-32 canvas and samples four pixels. A canvas is a browser drawing surface. RGBA numbers describe red, green, blue and opacity, each on a 0–255 scale here.

| Sample spot | RGBA numbers | Expected part |
|---|---|---|
| (1, 1) | `[17,20,43,255]` | Dark background. |
| (5, 8) | `[255,225,104,255]` | Yellow top bar. |
| (5, 15) | `[101,232,255,255]` | Cyan middle bar. |
| (5, 22) | `[255,78,145,255]` | Pink bottom bar. |

The corrected test passed. We did not add width and height to the requested original picture merely to make our mistaken assumption pass.

## 16. The checks and their actual results

### 16.1 Think of tests as different questions

A spelling check does not prove a story is true. A door-lock test does not prove the roof is strong. Software checks also have separate jobs.

| Check | The question it asks | What success does not prove |
|---|---|---|
| Skill fingerprints | Do all 12 protected files still match? | That the original tool has no bugs. |
| Borrowed unit tests | Do five sample behavior groups work? | Every possible input works. |
| Format validators | Do current documents meet the programmed rules? | Perfect page appearance or formal standards approval. |
| Style audit | Does the prose trigger listed mechanical/style problems? | Every sentence is excellent or factually true. |
| Builder contract | Do known insertion points still work, and do broken ones cause failure? | Any future generator change will be painless. |
| Source consistency | Do the selected counts, stage details and URLs agree? | Every repeated explanation has identical meaning. |
| Documentation check | Do listed paths, Make targets and known stale patterns look right? | No outdated sentence exists anywhere. |
| Pals check | Are count, species, targets, fingerprints and licence markers right? | Actual screen placement or low CPU use. |
| Sweep-record check | Do the old result totals fit their old snapshot? | A new network sweep was performed. |
| Research-age check | Are entries old or still uncertain? | Providers have not changed anything. |
| Output-drift check | Do fresh outputs match by the agreed methods? | Every platform produces identical binary bytes. |
| Publishing/favicon tests | Do five focused project test methods pass? | The owner's live hosting account is configured exactly as expected. |
| Browser harness | Do selected real browser actions and measurements work? | Every phone, browser and accessibility tool works. |

### 16.2 What GitHub runs automatically

`.github/workflows/verify.yml` runs after pushes, PRs and manual starts. It asks only for repository-content read permission and checks out full history rather than a shallow copy.

One job uses Python 3.11 and a cached package download setup keyed by the lockfile. It creates the environment, discovers the repository tests, runs the fast checks, checks rebuild drift and reports research freshness without making that warning block everything.

The other uses Node 22.22.3 and runs the browser harness. The fixed browser packages are `@sparticuz/chromium` 153.0.0 and `puppeteer-core` 25.16.0. The observed browser called itself HeadlessChrome/153.0.8010.0.

A job is a group of automated steps. A cache here speeds downloads; it does not replace source files or test evidence.

The workflow actions are fixed to major release names such as `checkout@v4`, not exact commit fingerprints. Fixing them more tightly is a future supply-chain safety option.

### 16.3 Do not overread the command name `make ci`

Locally, `make ci` runs fast checks plus drift. It does **not** include every online step.

To match the important workflow coverage, also run repository unit-test discovery and `make check-visual`. The name is convenient but can mislead someone who assumes it means everything GitHub does.

### 16.4 Commands actually run for the first report

The following completed successfully during the original report's audit on 1 November:

```sh
make bootstrap
make ci
python3 -m unittest discover -s tools -p 'test_*.py' -v
make check-visual
```

They were not rerun just to translate the report. This section preserves the original execution evidence.

### 16.5 Actual totals

- Twelve protected skill files matched their fingerprints.
- Five borrowed smoke-test methods passed.
- PDF, DOCX, static HTML and tracker checks passed, with the exact favicon exception.
- The prose audit found zero configured mechanical errors and zero style findings.
- The eight branding anchors, three Pals anchors and closing head point passed their break-and-fail checks; the tracker matched exactly.
- Counts and URLs agreed: eight stages, 27 cards, 94 hours and 22 different card addresses.
- Ten creatures, eight species, ten prose targets and licence/payload checks passed.
- The old sweep's 30/27/3 figures passed their internal check.
- Research freshness reported zero stale entries beyond 90 days and eight open gaps.
- The fast result was **9 passed, 1 warning, 0 failed**.
- The drift check was **1 passed, 0 warnings, 0 failed**, covering five outputs.
- Repository discovery ran **5 tests, all OK**: two publishing tests and three favicon tests.
- Browser checks passed **13 of 13 widths**, with **zero failures** and **no runtime errors in the tested paths**.

The borrowed five and repository five are different groups. The ten fast checks also are not simply ten more independent unit-test methods. Do not add unlike counts and call the sum “everything tested.”

### 16.6 The exact screen measurements

“Document width” matching the viewport means the tested page did not spill sideways. “Footer difference” measures the alignment the harness expects. “Overlap” is square pixels of rectangular creature/control intersection, not blocked taps.

| Browser width | Document width | Title size px | Label colors | Footer difference px | Pals | Control-center hits | Largest overlap px² | Result |
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

The normal first-stage-open checks at 320, 900 and 1440 also passed. Their largest overlaps were 0, 556 and 0 square pixels, and their center-hit counts were zero.

### 16.7 What actions were exercised

The browser tests checked:

- Current card count and resource links.
- HR Essentials before Talent Acquisition.
- Old saved Stage 1 progress still matching the correct cards.
- The topmost clickable element at every resource link across the widths.
- Trusted mouse and touch-like activation of both playlists at 390 and 1440.
- A normal click requesting the correct new-tab HR Essentials address.
- Ticking and unticking a card: `0 of 27` to `1 of 27 / 4%` and back.
- The 240px scroll experiment and fixed-layer control.
- Ten visible Pals when enabled, zero when paused and zero on reduced-motion startup.
- Actual favicon decoding and colors.
- Basic heading numbers, skip-link presence and selected control sizes.

Some activation tests deliberately prevent the outside navigation so the harness can measure which link was activated safely. A separate default-new-tab test allows the normal request.

Those tests do not play a YouTube video, authenticate a course account or prove a phone's app handoff succeeds.

### 16.8 The documentation checker was too confident in its wording

It printed “no stale claims.” Yet manual reading found older wrong sentences the pattern checks did not cover.

Its real result is narrower: the particular files, paths, targets and known stale phrases it checks passed. We should improve both its checks and its message. A reassuring sentence from a checker should not override contrary evidence.

## 17. Safety, privacy, usability and speed

### 17.1 What content the app trusts

The tracker uses project-authored data and a locally selected progress file. It is not a public publishing system where strangers upload arbitrary course pages.

Resource text is generally added with `textContent`. Links are allowed only for `http:` or `https:` addresses. They open in a new tab with `noopener noreferrer`, which helps stop the opened page controlling the original tab and avoids sending the normal referrer information.

The generator protects embedded JSON from a `</script>` escape, with a test for it. That is a specific safety result, not proof that every string substitution in every file is safe for hostile input.

### 17.2 Inline code is a deliberate tradeoff

The single-file design uses inline CSS and JavaScript. That helps portability but can conflict with strict website security policies that block inline code.

A Content Security Policy, or CSP, is a browser rule set about what code and resources may load. A strict one would need careful approved hashes or other allowances, including consideration of Pals scripts activated later.

We did not audit a complete production security-header setup. The exact favicon exception does not permit arbitrary active SVG code elsewhere.

### 17.3 Where personal information goes

The app itself has no project-owned analytics or server storing progress. It does not upload a selected backup file. That is a privacy benefit, but it also means no server copy can rescue lost progress.

A shared device still needs separate browser profiles if people want separation. An exported backup contains study dates and reminder time, so keep it sensibly.

Clicking an outside resource visits another company's website, under its own policies. The host also sees requests needed to deliver the page. “No app analytics” does not mean no hosting access logs exist.

The tracker is not an applicant-tracking system. Do not start putting real candidates' personal records into a practice workflow without a separate privacy and safety plan.

### 17.4 Different kinds of file protection

We protect three particular boundaries:

1. Every borrowed skill file has a saved fingerprint.
2. The Piixpal engine has a pinned fingerprint and recorded licence.
3. The entire approved favicon tag has a pinned fingerprint.

Python and Node tool versions are also fixed. However, we did not perform a complete dependency-vulnerability scan, prepare a full software bill of materials, sign a build proof or review every library licence.

A software bill of materials is an ingredient list for software. Version locks and fingerprints help, but they are not a universal “safe” badge.

### 17.5 Things that help different users

The project includes native controls, useful headings, a skip link, named checkboxes, progress-bar values for assistive tools, status messages, focus styling, high-contrast colors, optional decoration and reduced-motion startup behavior.

A focus indicator shows which control a keyboard user will activate. ARIA information gives assistive tools extra meaning, such as a progress percentage.

We did not run a full screen-reader journey or produce a formal WCAG report. WCAG is a set of accessibility guidelines. Mentioning it is not the same as being certified against it.

The creature engine uses Shadow DOM, a more separate inner part of the page. Ordinary outside selectors do not automatically inspect every inner behavior. A real assistive-technology review would still help.

Small chip text, the hidden reminder label, movement, long titles, large zoom, forced colors, translations, right-to-left writing and device rotation all deserve further attention.

### 17.6 What we know about speed

The tracker is one reasonably small file without a big runtime framework. Pals wait until idle time. All 27 cards are made locally, so there is no loading spinner waiting for a card-data server.

That does not give us measured Core Web Vitals, a Lighthouse score, low-end phone battery use, long-session memory behavior or real production loading times. Those measurements were not performed.

Moving creatures into document space reduces the scroll-correction problem. It does not prove the whole animation system is free to run. Pause cleanup and live reduced-motion changes need more testing if power use matters.

## 18. Every recorded problem and what happened next

This table preserves the failure list from the engineering report in simpler words. Some items are older recorded events, not freshly reproduced problems.

| Problem | What happened | What we did or what remains true |
|---|---|---|
| Supplied skill was a transfer document | The working files did not exist until extracted. | Recreated 12 files and checked their sizes/fingerprints; saved them in the repo. |
| System Python refused installation | PEP 668 protected the managed environment. | Final setup uses a private venv and version lock; old override is not current advice. |
| Tools vanished after resets | Imports or browser startup failed because installed files were gone. | Added repeatable setup and durable test tools. |
| History was shallow | Only part of the earlier work was visible. | Fetched full history; automatic checks also use full checkout. |
| Branch histories did not align | Local and online branch pointers differed. | Older record says fetch plus mixed reset kept working changes while aligning history. |
| MCP calls were blocked | Normal skill-service POST requests could not run. | Saved registration, read catalog/source alternatives and disclosed the limit. |
| Provider curl failed | TLS/network errors and no useful response. | Used readable-page tools where possible; moved sweep to GitHub. |
| Workflow start was refused | HTTP 403 continued after reconnect attempts. | Owner manually started it; no request for private credentials. |
| A diagnostic event did nothing | `repository_dispatch` was accepted but no workflow listened. | Did not count it as a sweep or keep retrying the same non-solution. |
| Log/artifact download was blocked | Redirect hosts were outside allowed access; UI needed sign-in. | Used owner summary plus run metadata; did not invent raw evidence. |
| PR editing hit an old API problem | `gh pr edit` encountered a Projects Classic error. | Used a REST PATCH workaround historically; no website code fix needed. |
| Styles inherited wrong colors | A pale eyebrow or an older rule still won. | Checked actual computed styles and added explicit local overrides. |
| Hero shadow went to the wrong edge | A refinement produced an unwanted side result. | Restored the intended bottom-only pink shadow. |
| Duplicate title-size wording | Applying 40% twice could overgrow the title. | Applied the repeated instruction once and recorded that choice. |
| Gutter request could be misunderstood | Removing a small gap might be mistaken for full-browser width. | Followed the owner's clarified framed-sheet meaning. |
| Repeated-creature test was wrong | It demanded tinting even on the first copy. | Required a tint only on later repeated appearances. |
| Creatures looked too small | Heading placements at scale 2 lacked presence. | Increased selected stage/footer placements to scale 3 and rechecked. |
| HEAD and GET disagreed | Homepage headers could look like a folder response. | Used matching tracker routes. |
| Preview script vanished | It lived inside a disposable cache folder. | Saved it under root `tools/` and added `make preview`. |
| Pals disappeared after reset | A server served the older committed tracker. | Rebuild tracker before preview start; warn on missing markers. |
| Chromium could not launch | Required shared libraries were not unpacked. | Unpacked bundled libraries and set the environment correctly. |
| Output pipe caused EPIPE | A verbose Node command was piped to `head`, which closed early. | Reran the full command without that truncating pipe. |
| Visual checks only opened all stages | They missed the normal visitor starting layout. | Added first-stage-only checks at three widths. |
| New card could steal old ticks | Position labels would move meaning after a prepend. | Added a new fixed label and retained old mappings. |
| Pals jittered while scrolling | A fixed layer depended on delayed JavaScript correction. | Used a full-document absolute layer and a control experiment. |
| Scroll experiment initially measured zero | Smooth scroll had not happened immediately. | Used instant scrolling in the test, not an unrequested production change. |
| Preview links seemed dead | The owner reported it, but tested links were not blocked. | Added mouse/touch/hit tests; no guessed navigation patch; outside-container cause unproven. |
| YouTube fetch included an error | Lesson information was readable, but an error banner also appeared. | Used direct playlists and kept playback/app-handoff caveats. |
| Favicon broke no-link validation | An approved inline icon still used a forbidden tag. | Exact-tag temporary checking exception, borrowed validator unchanged. |
| Picture test expected the wrong size | 32-unit viewBox was mistaken for natural 32px dimensions. | Rendered at 32px and sampled colors; left exact artwork unchanged. |
| Document bytes changed on rebuild | PDF/DOCX metadata and timestamps can differ. | Used meaningful text/internal-file comparisons, not misleading raw hash equality. |
| Docs checker overstated success | Pattern checks passed while manual reading found stale prose. | Recorded the contradiction and recommended a narrower message and better checks. |

The point is not to make every failure sound like a disaster. It is to put the repair in the right place. Weakening security, editing protected files or shipping a guess could have made the project less reliable.

## 19. What should improve next

These are suggestions. We did **not** silently implement them while writing either report.

### 19.1 Protect saved work first

**1. Give every resource a permanent ID.** The current special case handles one new first card. Future rearrangement still risks old ticks changing meaning. Migrate old labels deliberately and test it.

**2. Strengthen backup checking.** Require the expected version and shape, valid dates/times, known keys and sensible values. Limit file size and decide how to treat unknown or future-version data.

**3. Test a complete backup journey.** Tick cards, reload, export, reset, import and check everything again, including streak and reminder time. Also test storage failures. Current evidence is not that complete.

**4. Fix the meaning of “verified free.”** Store study cost, certificate cost, conditional access and research confidence as separate facts. Do not derive a strong claim just from a sentence that does not begin with “paid.”

**5. Check the final live icon and routes.** Confirm the deployed revision, download paths, browser-tab picture and progress transfer on the live address. PR #7 has owner acceptance; a later PR #8 full live test is not recorded.

### 19.2 Keep content and explanations honest

**6. Revisit the eight research gaps.** Try stronger provider evidence, but keep uncertainty if access still fails.

**7. Run a new sweep on the current 31 addresses.** Save its own timestamp and snapshot. Do not rewrite the old 30-address history.

**8. Reduce repeated content.** Markdown and JSON contain overlapping facts. Ideally use one structured source or compare more fields, including cost, notes, titles, providers, time and actions. Matching totals alone is not enough.

**9. Repair known old sentences in a separately approved change.** Current examples include:

- Library README wording saying the reference favicon was not copied.
- Setup examples saying 26 cards and 21 URLs.
- Setup's old “fixed” creature-layer description.
- The early design rule saying no link tags without immediately stating the exact favicon exception.
- A long-form first-hour instruction still pointing towards the TA channel rather than the new HR Essentials-first order.
- Broad original-date verification wording that can hide later caveats.
- Old 122px-title, 28-file/about-594KB and early script-count descriptions that belong to older snapshots.

**10. Make documentation checks less absolute.** Check more current examples and change “no stale claims” into wording that matches what was actually tested.

### 19.3 Check more real users and devices

**11. Try actual iOS Safari, Android Chrome, desktop Firefox and Safari.** Focus on links, YouTube app handoff, notifications, storage, downloads and scrolling.

**12. Revisit tiny text and the missing visible reminder label.** A useful computer-readable name does not solve every human readability problem.

**13. Add keyboard and screen-reader journeys.** Also test zoom/reflow, forced colors and changing reduced-motion preferences while the page is open.

**14. Measure Pals power and cleanup.** Profile long sessions, pause behavior and battery/CPU effects before promising complete shutdown.

**15. Decide whether tabs need coordination.** Add it only if needed, but do not currently claim several tabs stay synchronized.

### 19.4 Improve the toolbox carefully

**16. Refresh the environment when the lock changes.** The existing Python executable should not hide missing or outdated packages.

**17. Consider fixing GitHub actions to exact commit IDs.** Add package-security and licensing reviews if the project needs stronger supply-chain protection.

**18. Consider stricter package download verification.** Document the supported operating system and browser setup. Version numbers alone are not a full guarantee.

**19. Review every wrapper assumption during a skill upgrade.** Keep the eight branding anchors, three creature anchors, key shim and icon exception in mind. Do not just rewrite fingerprints to quiet warnings.

**20. Check PDFs visually when layout matters.** Equal extracted words can still wrap or paginate differently.

**21. Normalize curl failures.** Ensure a failed connection yields a clear one-part code rather than possible `000000`. Keep it a useful report rather than a misleading pass/fail gate.

### 19.5 Do not add a huge system just because you can

Accounts, cloud sync, payment, a content-management system, a real applicant tracker and push notifications were not part of this brief.

They would create new hosting, privacy, safety, cost and maintenance duties. A deliberately simple local tracker should not accidentally become an unplanned online service.

## 20. Instructions for the next person

These are practical steps, with actual commands kept exact. A 12-year-old reader does not need to run them to understand the project.

### 20.1 Start from a clean toolbox

Use Python 3.11 with venv support, Make, Bash and the supported Node version, preferably the same 22.22.3 used in CI.

```sh
make bootstrap
make ci
python3 -m unittest discover -s tools -p 'test_*.py' -v
make check-visual
```

If `.venv` exists but is incomplete, recreate it deliberately or install the lock using its Python. Do not go back to overriding system package protections.

Downloaded Node tools and browser caches can be recreated. They should not be committed as product content.

### 20.2 Change a resource or lesson

1. Read the actual provider page and write down what it really proves.
2. Update the long Markdown source and matching JSON card.
3. Update the current script/manifest if an address changes.
4. Keep old sweep snapshots unchanged.
5. Preserve existing saved labels, or design and test a migration before moving cards.
6. Run `make build`.
7. Run fast, drift, repository and browser tests.
8. Read affected webpage, PDF and DOCX sections.
9. Check the diff for unintended changes and whitespace problems.
10. Record uncertainty. Do not change a check date without doing the check.

A diff is a view showing what changed between versions. `git diff --check` catches certain whitespace mistakes; it does not judge the truth of the content.

### 20.3 Change appearance or Pals

Edit the local theme, controller, Pals styles or placement JSON. Do not hand-edit only the final HTML or casually change the protected engine.

Rebuild and check both all-expanded and normal first-stage-open layouts. Look carefully around links, time input, Done labels, stage headings and creature canvases.

A longer title can move a creature even when the creature settings did not change. Content edits can therefore need visual checks too.

### 20.4 Upgrade the borrowed skill

Keep the old fingerprint record. Review the replacement and licence. Update intentionally. Expect local anchors to need review.

Run the borrowed tests, project tests and saved-progress checks. Only then record new approved fingerprints. A failed integrity check is an investigation request, not permission to bless unknown bytes.

### 20.5 Recover a broken preview

- Confirm the current branch and source files.
- Start `make preview` as a managed long-running process.
- Confirm the homepage really serves the tracker, not a folder or old file.
- Check GET/HEAD behavior and expected Pals/favicon signs.
- Stop a known stale process before starting duplicates.
- Remember tracker preview needs ordinary Python, while document building needs the full environment.

### 20.6 Refresh outside-link research

Run the workflow where outside access works. Read its results and relevant provider pages.

Record the exact address snapshot, run link, date and status totals. Investigate non-successes, but do not assume every 200 proves a valid free course.

If artifact access is blocked, ask for a safe pasted summary, not a token or signed secret address. Clearly say the raw file was not inspected.

### 20.7 Release a change

1. Follow the user's understanding/go-ahead rule.
2. Stay on the assigned session branch.
3. Review status and changed files.
4. Run full relevant checks, not only `make ci`.
5. Commit/push/create the PR only with permission.
6. Review the checks and merge the explicit PR number when authorized.
7. Confirm it is actually merged and identify the new main version.
8. Check the live homepage, downloads, old progress, links, mobile scroll and icon separately.
9. Do not erase the owner's progress during a test; use sensible test data and backup first.

A merge command should report its actual failure if it fails. Do not hide that result behind shell tricks and then claim success.

### 20.8 Going back safely

A rollback means returning to a known-good release. Here the release unit is the saved version and finished artifacts, not restarting a complicated app server.

After approval, a revert PR or hosting rollback could return the site to an earlier version. Saved progress still needs thought: old or unknown labels should never be recycled for unrelated resources.

No rollback was actually rehearsed in the first report. This is a proposed procedure based on the static design.

## 21. What we did not do

The full story includes limits. We do not have evidence for the following claims, so we do not make them:

- We bought or completed the linked courses.
- Every free lesson comes with a free certificate.
- The plan itself awards a professional qualification.
- LinkedIn's prices were confirmed by readable provider pages.
- The library is a complete legal opinion about recruitment in Nigeria.
- Every long guide and every legal PDF page was fully read.
- We downloaded and inspected the first sweep's raw TSV.
- MCP tools worked just because registration files exist.
- Every original screenshot and temporary upload is preserved.
- All physical phones, browsers and assistive tools passed.
- We proved the cause of the embedded-preview link problem.
- Notifications reliably arrive after the tab is closed.
- Progress automatically synchronizes across devices or tabs.
- Lost local progress can be recovered without a backup.
- Arbitrary imported files receive full schema validation.
- Pausing Pals guarantees all CPU work stops.
- The project has formal accessibility, safety, privacy, licence or speed certification.
- Either report independently checked the live production account and all settings.
- The owner confirmed the final live favicon after PR #8.
- This plain-English rewrite reran the original tests or updated provider research.
- This report has permission to be committed, pushed or merged.

Saying “not checked” is not failure. Pretending something was checked when it was not would be the failure.

## 22. Where to find the evidence

### 22.1 Files inside the project

| Link | What it helps you check |
|---|---|
| [Original engineering report](ENGINEERING-REPORT.md) | The technical version this explanation follows. |
| [Root README](../README.md) | Starting point for the project. |
| [Library README](../learning-library/README.md) | Output files and learning-library introduction; some old prose is noted above. |
| [Changelog](../CHANGELOG.md) | Dated work record. |
| [Retrospective](../RETROSPECTIVE.md) | Early recurring problems and repairs. |
| [Setup guide](SETUP.md) | Commands and environment information, with stale examples flagged in this report. |
| [Design specification](DESIGN-SPEC.md) | Intended current look and later special cases. |
| [Older design record](../learning-library/DESIGN-SYSTEM.md) | Original style transfer and refinements. |
| [Deployment guide](DEPLOYMENT.md) | Publishing and live checks. |
| [Long-form library](../learning-library/src/recruiter-talent-acquisition-library.md) | The learning narrative and research reasoning. |
| [Tracker data](../learning-library/src/roadmap-app.json) | Exact current stage and card fields. |
| [Research manifest](../learning-library/src/verification-manifest.json) | Check dates, uncertainty and historical sweep. |
| [Tracker builder](../learning-library/tools/build_tracker.py) | Local changes around the unchanged generator. |
| [Project checker](../tools/check.py) | What the fast and drift checks actually do. |
| [Browser checker](../tools/visual/visual_check.mjs) | Actual geometry and behavior assertions. |
| [Third-party notices](../THIRD-PARTY-NOTICES.md) | Creature-engine origin and licence pointer. |

### 22.2 Public project records

- Project: <https://github.com/MikkoWuyin-dev/FieldNotes-HR>.
- Visual reference: <https://github.com/MikkoWuyin-dev/Field-Notes_Nature-Photography>.
- Creature engine: <https://github.com/diiviikk5/Piixpal>.
- Skill catalog page checked: <https://skill-issue.in/?skill=design-web-design-guidelines>.
- First sweep: <https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40471064309>.
- Latest merge checks inspected for the original report: <https://github.com/MikkoWuyin-dev/FieldNotes-HR/actions/runs/40485000208>.
- Live address supplied by the owner: <https://fieldnotes-hr.vercel.app/>.

The following appendices keep the detailed records. Exact codes and official titles remain exact. Surrounding explanations tell you what they mean. Their presence does not turn historical research into a new check.

---

## Appendix A: every accepted change and saved step

### A.1 The eight pull requests

A PR is a proposed batch of work. All eight below were accepted into `main`. A branch is the line of work it came from. The merge code identifies the accepted version. Dates use UTC; add one hour for Lagos. `Z` at the end means UTC.

“Files” counts files touched in that PR. “Additions” and “deletions” are GitHub’s change counts. They are not a count of unique ideas or a useful measure of effort. The same file can appear in several PRs, and generated text contributes to the totals.

| PR | Exact saved title | Work branch | Accepted at (UTC) | Version code | Files | Additions | Deletions |
|---|---|---|---|---|---:|---:|---:|
| [#1](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/1) | Vendor resource-learning-library skill and add recruiter learning library | `arena/19ef6871-fieldnotes-hr` | 2026-10-26T17:30:04Z | `6b33fb5` | 23 | 4188 | 0 |
| [#2](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/2) | Restyle roadmap tracker with Fieldnotes design system | `arena/788290da-fieldnotes-hr` | 2026-10-26T22:58:25Z | `fd7c568` | 9 | 1427 | 13 |
| [#3](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/3) | Make builds reproducible: retrospective, pinned environment, CI and verification | `arena/bd812372-fieldnotes-hr` | 2026-10-26T23:50:29Z | `e2c6dce` | 24 | 2651 | 87 |
| [#4](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/4) | Add ten decorative Pals to the tracker and make previews reproducible | `arena/833b18a5-fieldnotes-hr` | 2026-10-27T07:20:03Z | `0a3f440` | 19 | 1388 | 45 |
| [#5](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/5) | Record first link sweep results and refresh library verification notes | `arena/46f91e1e-fieldnotes-hr` | 2026-10-27T08:36:39Z | `8f18a91` | 13 | 167 | 34 |
| [#6](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/6) | Configure static Vercel deployment | `arena/f5ea4032-fieldnotes-hr` | 2026-10-27T08:42:50Z | `c035742` | 6 | 115 | 0 |
| [#7](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/7) | Fix mobile layout, playlist destinations and Pals scrolling | `arena/3f0257c3-fieldnotes-hr` | 2026-10-27T09:44:46Z | `d469e5d` | 17 | 324 | 80 |
| [#8](https://github.com/MikkoWuyin-dev/FieldNotes-HR/pull/8) | Match Nature Photography favicon | `arena/ca8cd9c8-fieldnotes-hr` | 2026-10-27T09:59:30Z | `765f2e2` | 10 | 146 | 10 |

**What those titles mean:**

- **PR #1:** Keep the supplied 12-file tool inside the project and add the first learning plan and finished formats.
- **PR #2:** Make the tracker look like the selected Fieldnotes reference, then adjust it through owner feedback.
- **PR #3:** Make setup and rebuilding repeatable, record what went wrong, and save automatic check tools.
- **PR #4:** Add ten optional creatures and stop preview recovery from depending on vanished temporary files.
- **PR #5:** Record the first completed outside-link sweep and explain its three refused requests.
- **PR #6:** Tell the host to serve only finished files and send the homepage to the tracker.
- **PR #7:** Fix the oversized phone title, use actual playlists, preserve old ticks and make creatures move with the page.
- **PR #8:** Copy the exact little tab picture, with a tightly limited exception to the no-link checker.

### A.2 Every saved Git step

There are **19 commits** in the product history described here. A merge is also a saved step, so it appears alongside the work it accepted. The initial project save and eight merge saves are included. Neither report was part of that product history.

The middle column uses the Git save/committer time converted to UTC. GitHub’s PR acceptance time can be a second different. Exact subjects below are historical labels, not unexplained instructions to run.

| Commit | Saved time (UTC) | Exact saved label |
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

**Reading the smaller work steps:** the design work had one main style save and a later refinement save; the repeatable-build work had one implementation save and a later note update after CI success was actually observed. The remaining main feature saves correspond to their PR descriptions above. “Merge pull request” means the related proposed work was accepted, not that the entire project was rewritten.

### A.3 The reporting line of work

These reports are being written on `arena/8c02879a-fieldnotes-hr`, starting from the PR #8 version. Older branch names in the table identify earlier sessions. We do not switch to them. The inspected product version had no extra unmerged implementation PR to include.

## Appendix B: every learning card

This appendix keeps all **27 cards**, not just a few examples. Titles, providers, addresses, dates, cost labels and storage codes stay exact where they identify the real records. The explanations and activities are rewritten in simpler English. No provider has been freshly checked for this translation.

**Tracker title:** Zero to Recruiter: a Talent Acquisition roadmap.

**Who it is for:** a complete beginner in Lagos, studying about five hours weekly, starting with free learning and clearly labelled paid options.

**Reminder default:** `19:00`, or 7 p.m. **Storage ID:** `rll-recruiter-ta-2026-10-26`. A card’s saved label tells the browser which Done tick belongs to it. It is not a certificate code.

### B.1 Stage 1: Orientation - what a recruiter actually does

**When:** Weeks 1-2. **Stage budget:** 8 hours. **Cards:** 4.

Learn what happens from planning a job through helping a new employee settle in. Understand recruitment words and how a recruiter works with a hiring manager. No earlier HR knowledge is expected.

**By the end, aim to:**

- Explain the steps from deciding what staff are needed to helping a new worker start.
- Name common recruiter jobs and explain recruiting for your own employer versus recruiting for client employers.
- Explain why written requirements are fairer than choosing mainly by a feeling.

#### B.1.1 The HR Learning Lab: HR Essentials (video playlist)

- **Provider:** HR Learning Lab (YouTube)
- **Actual address:** <https://www.youtube.com/playlist?list=PLeDNHX61_qlQeRK1_i5flRpz2T0wjQXN2>
- **Type shown on the card:** Free video series
- **Exact cost label:** Free
- **Time wording on the card:** 1 hour for starter lessons and notes (study budget)
- **Date printed on the card:** 2026-10-27. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `hr-essentials-v1`
- **Link button wording:** Open the playlist

**Why it belongs here:** Learn the wider job of HR and the employee life cycle before concentrating on recruiting.

**What to do:** Watch lessons 1–4. Draw the stages of an employee’s time with an organization and show where recruitment fits. Use the rest of the selected hour for notes and review.

**What we checked and what to be careful about:** The public playlist was checked on 27 October. It listed 16 videos, and the description and early lesson titles could be read without signing in. The fetch also showed a YouTube error banner. That means video playback and opening the phone app were not tested by this read. Dr. Heather Staples developed the content, using AI-supported production tools. This is beginner learning, not a professional qualification.

#### B.1.2 The HR Learning Lab: Talent Acquisition (video playlist)

- **Provider:** HR Learning Lab (YouTube)
- **Actual address:** <https://www.youtube.com/playlist?list=PLeDNHX61_qlQWYcxZNB19TDOKbl625W2c>
- **Type shown on the card:** Free video series
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours of selected lessons and notes (study budget)
- **Date printed on the card:** 2026-10-27. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s0-r0`
- **Link button wording:** Open the playlist

**Why it belongs here:** Short lessons introduce job analysis, planning staff needs, recruiting, choosing people and hiring practice. They introduce vocabulary before the heavier reading.

**What to do:** Watch the first five lessons. Make a one-page diagram explaining the whole hiring process in your own words.

**What we checked and what to be careful about:** The public playlist was checked on 27 October. It listed 43 videos with readable lesson titles and description without sign-in. Playback and mobile-app handoff were not tested. The creator discloses AI-supported production, so check important legal or professional claims against primary sources.

#### B.1.3 PRDV226: Introduction to Human Resource Management

- **Provider:** Saylor University
- **Actual address:** <https://learn.saylor.org/course/view.php?id=1292>
- **Type shown on the card:** Written course with lectures and videos
- **Exact cost label:** Free, with a free completion certificate
- **Time wording on the card:** About 14 hours for the whole course
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s0-r1`
- **Link button wording:** Open the course

**Why it belongs here:** Units 1 and 2 explain finding, recruiting and keeping suitable employees. They give a more organized foundation than brief videos alone.

**What to do:** Study Units 1 and 2 during these two weeks. Return to Units 3 and 4 in Stage 2.

**What we checked and what to be careful about:** The syllabus and Saylor FAQ were read on 26 October. They say no tuition or fees, free material and a free completion certificate at 70% on the final exam. A free account is needed for assessments and the exam. Only the separately proctored college-credit route carries a fee; it is not needed for that free completion certificate. The roughly 14-hour length is for the whole course, not an extra 14-hour Stage 1 requirement.

#### B.1.4 Principles of Management, Chapter 11: Human Resource Management

- **Provider:** OpenStax (Rice University)
- **Actual address:** <https://openstax.org/books/principles-management/pages/11-introduction>
- **Type shown on the card:** Free peer-reviewed textbook
- **Exact cost label:** Free
- **Time wording on the card:** About 1 hour for the introduction and section 11.1
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s0-r2`
- **Link button wording:** Read Chapter 11

**Why it belongs here:** This chapter explains why HR supports an organization’s goals, not just paperwork. It helps you understand the reasons behind recruitment steps.

**What to do:** Read the chapter introduction and section 11.1. Note three ways HR creates value that you could explain in a job interview.

**What we checked and what to be careful about:** The free openly licensed web textbook was checked on 26 October. Its examples are US-based. Read its legal discussion as background, not as Nigerian law. The selected introduction and section are allocated about one hour.

### B.2 Stage 2: Foundations - fair process, job roles and the law

**When:** Weeks 3-5. **Stage budget:** 14 hours. **Cards:** 4.

Learn fair hiring rules, the difference between what a job requires and what a person must bring, the hiring sequence and responsibilities for candidate information in Nigeria.

**By the end, aim to:**

- Describe a complete, fair hiring process in order.
- Tell job duties apart from the abilities and qualities a person needs.
- Recognize basic responsibilities when collecting and using candidate data in Nigeria.

#### B.2.1 Human resources: recruitment and selection

- **Provider:** The Open University (OpenLearn)
- **Actual address:** <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0>
- **Type shown on the card:** Free written course with activities
- **Exact cost label:** Free, with a free statement of participation
- **Time wording on the card:** 12 hours
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s1-r0`
- **Link button wording:** Open the free course

**Why it belongs here:** This is the main beginner course for job analysis, job descriptions, suitable-person requirements, attracting applicants, adverts, shortlisting and references.

**What to do:** Complete sections 4.2–4.5. Choose a real Lagos vacancy online and draft an explanation of the work it requires.

**What we checked and what to be careful about:** The provider page was read on 26 October. It offers a free course and free statement of participation. A free account is needed for tracking, claiming the statement and all quizzes/activities. Content was last updated in 2018 and uses UK equality-law ideas, so use the Nigerian sources in Stage 7 too. The manifest separately records a successful 27 October reread after the sweep got 403.

#### B.2.2 Diploma in Human Resources (HR)

- **Provider:** Alison
- **Actual address:** <https://alison.com/course/diploma-in-human-resources-hr>
- **Type shown on the card:** Free video diploma course
- **Exact cost label:** Free to study; the optional certificate costs extra
- **Time wording on the card:** 10-15 hours
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s1-r1`
- **Link button wording:** Open the course

**Why it belongs here:** A video-led alternative to the more text-heavy OpenLearn course. It covers HR responsibilities, recruitment, selection and employees leaving an organization.

**What to do:** Use the recruitment and selection modules for revision. Compare their process with OpenLearn section 4.

**What we checked and what to be careful about:** Alison’s help and certificate pages were read on 26 October. Studying and completing courses is free; a digital or printed branded certificate is optional and paid. A free Learner Record is available instead. We did not establish an exact certificate price. The recruitment tag page listed 15 free recruitment courses. The 10–15 hours is the listed course length, not a demand to add all of it to the selected plan.

#### B.2.3 BUS301: Human Resource Management

- **Provider:** Saylor University
- **Actual address:** <https://learn.saylor.org/course/BUS301>
- **Type shown on the card:** Written course with lectures and videos
- **Exact cost label:** Free, with a free completion certificate
- **Time wording on the card:** About 24 hours for the full course
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s1-r2`
- **Link button wording:** Open the course

**Why it belongs here:** A deeper course after PRDV226, covering HR planning, staffing, compliance and workplace relations. Selected parts fit the plan better than completing everything immediately.

**What to do:** Read only the staffing and recruitment/selection units for now. Leave performance and compensation units until job hunting.

**What we checked and what to be careful about:** Saylor’s FAQ and syllabus were checked on 26 October: no tuition or fees, with a free final exam and completion certificate. The full course is about 24 hours. Its US employment-law material must not be mistaken for Nigerian law.

#### B.2.4 Recruiting, Hiring, and Onboarding Employees (audit option)

- **Provider:** University of Minnesota on Coursera
- **Actual address:** <https://www.coursera.org/learn/recruiting-hiring-onboarding-employees>
- **Type shown on the card:** University video course
- **Exact cost label:** Paid or conditional - not counted as confirmed free
- **Time wording on the card:** About 2 weeks at 10 hours a week (about 20 hours)
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `ambiguous`. Free full access is unclear. This is an open gap, not confirmed free.
- **Saved Done label:** `s1-r3`
- **Link button wording:** Check the enrolment options

**Why it belongs here:** The topics fit well: planning staff, analyzing jobs, lawful selection, finding applicants, hiring measures and helping new staff start. There are four modules, with 14 videos in the first alone.

**What to do:** Consider it after the free stages. If a “Full Course, No Certificate” choice is actually offered to you, review it. Then decide separately whether paying for a certificate is worthwhile.

**What we checked and what to be careful about:** This card is NOT counted as confirmed free. On 26 October the page showed “Enroll for free” and Coursera Plus inclusion, but its FAQ tied material access to buying the Certificate experience, a trial, or a no-certificate choice where available. We could not confirm that last choice for this course. Financial aid is mentioned. Regional prices and promotions vary. Its roughly two weeks at ten hours weekly is about 20 hours and exceeds this learner’s usual weekly pace.

### B.3 Stage 3: Define the role - job analysis, descriptions and success criteria

**When:** Weeks 6-7. **Stage budget:** 10 hours. **Cards:** 3.

Before looking for people, find out what the job really needs. Decide what evidence would show someone can do it. A vague beginning can spoil the rest of hiring.

**By the end, aim to:**

- Turn a vague hiring request into a job description and a list of suitable-person requirements.
- Choose clear things to measure before speaking to applicants.
- Make a simple scoring sheet every interviewer can use.

#### B.3.1 ONET OnLine (Occupational Information Network)

- **Provider:** US Department of Labor
- **Actual address:** <https://www.onetonline.org/>
- **Type shown on the card:** Free official occupational database
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours to explore one occupation properly
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s2-r0`
- **Link button wording:** Search occupations

**Why it belongs here:** Look at real tasks, skills and knowledge before writing a job advert. This helps avoid copying someone else’s list without understanding it.

**What to do:** Choose an occupation, export its tasks and highlight five things a new hire must do in the first month.

**What we checked and what to be careful about:** The public site was checked on 26 October, with 1,016 occupation titles and no login seen. The card describes more than 1,000 profiles. It is US data: learn the analysis method, then compare duties with Nigerian adverts. Allow about two hours to explore one role properly.

#### B.3.2 HR templates: job descriptions, interview kits and email templates

- **Provider:** Workable
- **Actual address:** <https://resources.workable.com/hr-templates/>
- **Type shown on the card:** Free official templates and guides
- **Exact cost label:** Free
- **Time wording on the card:** 1-2 hours to adapt a template
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s2-r1`
- **Link button wording:** Browse the free templates

**Why it belongs here:** The collection includes more than 1,000 job descriptions, 390-plus interview kits, 50-plus recruiting email templates, onboarding checklists and search guides. They are starting material, not instructions to copy blindly.

**What to do:** Adapt one description so every requirement links to a task you found in O*NET. Delete requirements you cannot justify.

**What we checked and what to be careful about:** The provider index said the templates were free to download on 26 October. A separate 15-day software trial was advertised, but it is not required for the templates. Localize pay, notice and leave wording because examples are generic and US/UK-flavored. Allow one to two hours for adaptation.

#### B.3.3 Structured hiring: Introduction (with free worksheets)

- **Provider:** Greenhouse Support
- **Actual address:** <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction>
- **Type shown on the card:** Free official process documentation
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours including the worksheets
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s2-r2`
- **Link button wording:** Read and download

**Why it belongs here:** Learn six planned hiring steps: discuss the role, define a scorecard, plan interviews, build an interview kit, source/interview and discuss the candidates. Decide what success looks like before searching.

**What to do:** Download the worksheet and make a scorecard with no more than six abilities or qualities for your practice role.

**What we checked and what to be careful about:** The support article was read on 26 October. The article and two PDFs could be accessed without login: an approximately 4MB structured-interview worksheet and 9MB interactive eBook. It is product documentation, but the method can be used without that product. The card allows about two hours including the worksheets.

### B.4 Stage 4: Find people - sourcing, Boolean search and candidate experience

**When:** Weeks 8-10. **Stage budget:** 14 hours. **Cards:** 4.

Find places to look for suitable people, learn to search effectively, write useful messages and treat applicants respectfully.

**By the end, aim to:**

- Build a search using Boolean word rules for a real job.
- Compare job boards, recommendations from others, saved candidate lists and direct searching.
- Write a brief first message and plan how candidates will be treated through the process.

#### B.4.1 Boolean search cheatsheets for sourcing

- **Provider:** Workable
- **Actual address:** <https://resources.workable.com/boolean-search-cheatsheets/>
- **Type shown on the card:** Free written cheat sheets
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours to practise
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s3-r0`
- **Link button wording:** Open the cheatsheets

**Why it belongs here:** Practice search rules using brackets, quotes, AND, OR and NOT. These help a recruiter find more suitable people instead of searching only one vague job title.

**What to do:** Adapt one example for a Lagos role, run it in a free search engine and save ten plausible practice profiles with a reason for each match.

**What we checked and what to be careful about:** The provider page was checked on 26 October. The sheets were free, with no account or payment shown. Many examples concern technical and sales jobs, so adapt the words to Nigerian roles. About two hours is for practice; use anonymized or fake data in the project rather than building a real candidate-data system.

#### B.4.2 Talent Sourcing Strategies (video 16)

- **Provider:** HR Learning Lab (YouTube)
- **Actual address:** <https://www.youtube.com/watch?v=yMnw_2VNOVE>
- **Type shown on the card:** Free video lesson
- **Exact cost label:** Free
- **Time wording on the card:** 7 minutes
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s3-r1`
- **Link button wording:** Watch the lesson

**Why it belongs here:** A seven-minute overview of employer reputation, referrals, job boards, candidate lists, searching CVs and job fairs. It also encourages looking beyond exact job titles.

**What to do:** Choose two candidate-finding channels suitable for a small Lagos employer and explain why you left the others out.

**What we checked and what to be careful about:** The public video was checked on 26 October with no payment shown. Its description credits Heather Staples and lists PhD, SPHR and SHRM-SCP qualifications. It says the videos use AI-supported production. Treat it as an introductory overview, not a primary authority for important claims.

#### B.4.3 Google re:Work guides (hiring set)

- **Provider:** Google re:Work
- **Actual address:** <https://rework.withgoogle.com/intl/en/guides/>
- **Type shown on the card:** Free official practice guides
- **Exact cost label:** Free
- **Time wording on the card:** About 3 hours across the relevant guides
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s3-r2`
- **Link button wording:** Open the guides index

**Why it belongs here:** The index lists 23 guides, including job descriptions, CV review, candidate experience, interviews, interviewer training, hiring committees and onboarding. It is an open practical guide collection from a large employer.

**What to do:** Open “Shape the candidate experience” from the index and list three ways you would improve a typical Nigerian recruitment process.

**What we checked and what to be careful about:** The index was read on 26 October, with guide/tool counts and no login or payment shown. Not every individual guide was opened. The wider records say two guides were read, while the training card more specifically says its content came via search results rather than a direct page open. Keep that narrower detail; do not claim every guide was directly read. Google’s results come from its own workforce, not Nigerian employers. About three hours is spread over selected guides.

#### B.4.4 Jobberman free employer listing (practice channel)

- **Provider:** Jobberman Nigeria
- **Actual address:** <https://www.jobberman.com/employer/free-listing>
- **Type shown on the card:** Free job board and applicant tracking tool
- **Exact cost label:** Free listing; paid tiers exist
- **Time wording on the card:** 1-2 hours to set up a practice advert
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `partial`. Only part of the page was readable. This is an open gap.
- **Saved Done label:** `s3-r3`
- **Link button wording:** Check the free listing

**Why it belongs here:** A Nigeria-specific place to understand local job adverts and applicant sorting. It may help practice without buying recruiting software, but the access terms need confirmation.

**What to do:** Draft and save a practice advert for your Stage 3 role. Do not publish a real vacancy without the right authorization.

**What we checked and what to be careful about:** Only a cookie banner was readable on 26 October. The free-posting, CV-sorting and applicant-tracking claims came from Jobberman’s own search listing, not a full terms page. Paid tiers exist. Confirm eligibility, limits and current terms before relying on it. The card has a 26 October check label; the manifest leaves the confirmed date empty because the finding is only partial. One to two hours is a practice allocation.

### B.5 Stage 5: Screen and shortlist - reading CVs against criteria

**When:** Weeks 11-12. **Stage budget:** 10 hours. **Cards:** 3.

Reduce a pile of applications to a smaller list you can explain and defend. Apply the same rules before interviewing people.

**By the end, aim to:**

- Compare a CV with the scoring sheet rather than a first impression.
- Prepare the same short phone-screen questions for everyone.
- Write down evidence for rejection decisions so the reasoning can be explained.

#### B.5.1 Google re:Work guide: Review resumes

- **Provider:** Google re:Work
- **Actual address:** <https://rework.withgoogle.com/intl/en/guides/>
- **Type shown on the card:** Free official practice guide
- **Exact cost label:** Free
- **Time wording on the card:** About 1 hour
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s4-r0`
- **Link button wording:** Open the guides index

**Why it belongs here:** The index describes a five-step guide for checking qualifications, consistency and impact. A written standard helps avoid judging mainly by impressions.

**What to do:** Open “Review resumes” from the index. Screen ten practice CVs and write one line of evidence supporting each decision.

**What we checked and what to be careful about:** On 26 October the provider index listed the guide as five steps and showed no payment or login. The individual guide page was not opened, so the exact steps were not read. That limit stays even though the general index has a confirmed finding. The card allocates about one hour.

#### B.5.2 Greenhouse guidance library (screening and interviewing)

- **Provider:** Greenhouse
- **Actual address:** <https://www.greenhouse.com/guidance>
- **Type shown on the card:** Free official articles, eBooks and worksheets
- **Exact cost label:** Free
- **Time wording on the card:** 2-3 hours browsing and reading
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s4-r1`
- **Link button wording:** Open the guidance hub

**Why it belongs here:** The hub has topics including interviews, candidate experience, recruiter advice and DE&I—diversity, equity and inclusion, meaning fair treatment across different backgrounds.

**What to do:** Read one interview article and one bias-related article. Add two checks against unfair assumptions to your Stage 3 scorecard.

**What we checked and what to be careful about:** The guidance hub was read on 26 October. It lists free articles, eBooks, webinars and worksheets, but some items such as the 2026 benchmark report may require a form. Their free-download access was not established. Remember it also markets a commercial product. Allow two to three hours for selected reading.

#### B.5.3 OpenLearn section 4.10: Shortlisting (revisit)

- **Provider:** The Open University (OpenLearn)
- **Actual address:** <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0>
- **Type shown on the card:** Free written course section
- **Exact cost label:** Free
- **Time wording on the card:** About 1 hour
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s4-r2`
- **Link button wording:** Return to the course

**Why it belongs here:** Reuse a course you already met instead of collecting another unnecessary link. With a real scorecard, the shortlisting advice becomes more useful.

**What to do:** Reread sections 4.10–4.12 and compare them with your scorecard. Find one disagreement and explain how you would resolve it.

**What we checked and what to be careful about:** This revisits the same free OpenLearn course from Stage 2. The card is another task using the same resource, not a new paid course or another distinct destination. Its access evidence is the Stage 2 evidence. Allow about one hour.

### B.6 Stage 6: Interview and decide - structured interviewing in practice

**When:** Weeks 13-15. **Stage budget:** 16 hours. **Cards:** 3.

Practice asking planned questions and judging answers against the same written scoring rules. A rubric is simply a guide explaining what different scores mean.

**By the end, aim to:**

- Write questions about past actions and imagined situations, each tied to a required ability.
- Describe weak, borderline, solid and outstanding answers in a scoring guide.
- Run a practice interview and score it separately from a partner before comparing.

#### B.6.1 A guide to structured interviewing for better hiring practices

- **Provider:** Google re:Work
- **Actual address:** <https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices>
- **Type shown on the card:** Free official practice guide
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s5-r0`
- **Link button wording:** Read the guide

**Why it belongs here:** This key guide explains structured interviewing: define what you are testing, prepare questions and follow-ups, and use a shared scoring guide. Its page was marked updated March 2026.

**What to do:** Write eight questions for the practice role: four about past behavior and four about imagined situations. Link each to a scorecard item and describe weak versus outstanding answers.

**What we checked and what to be careful about:** The provider page was read on 26 October and showed free access without login or payment. Google’s reported numbers come from its own hiring data. They are not a promised result for your workplace. The selected work is about two hours.

#### B.6.2 Effective interviewer training for better candidate experiences

- **Provider:** Google re:Work
- **Actual address:** <https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences>
- **Type shown on the card:** Free official practice guide
- **Exact cost label:** Free
- **Time wording on the card:** About 1 hour
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s5-r1`
- **Link button wording:** Read the guide

**Why it belongs here:** Good interview feedback needs evidence, not comments like “I just liked them.” The guide also covers useful feedback and leaving time for the candidate’s questions.

**What to do:** After a mock interview, rewrite feedback using the guide’s advice. Ask whether someone who was not there could understand the evidence.

**What we checked and what to be careful about:** The specific card says provider-authored content was returned in search results on 26 October. It was not a direct full-page read, and individual steps were not fully read. The general manifest groups it with the free re:Work guides. Keep the detailed caution rather than overstating it. Allow about one hour.

#### B.6.3 Reuse: Greenhouse structured hiring introduction and Workable interview kits

- **Provider:** Greenhouse and Workable
- **Actual address:** <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction>
- **Type shown on the card:** Free official templates and process docs
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s5-r2`
- **Link button wording:** Reopen the worksheets

**Why it belongs here:** Reuse the Greenhouse worksheet and Workable interview-kit examples from Stage 3. A kit makes the questions and scoring usable by real interviewers.

**What to do:** Build a one-page kit with the interview’s purpose, what is being tested, the questions, score descriptions and a recommendation space.

**What we checked and what to be careful about:** There is no new course cost. The earlier Stage 3 cards explain access. The tracker’s actual destination is the Greenhouse introduction; the title also reminds learners to reuse Workable materials. Reuse does not create a new unique URL for each named item. About two hours is allocated.

### B.7 Stage 7: Offer, onboarding and the law in Nigeria

**When:** Weeks 16-17. **Stage budget:** 10 hours. **Cards:** 3.

Finish the hiring journey with references, offers and helping a new person start. Learn the local privacy and employment-law questions that arise quickly for a Lagos recruiter.

**By the end, aim to:**

- Explain the legal reasons that can allow use of a candidate’s personal information.
- Write a short notice explaining what happens to candidate data.
- Read the recruiting rules in the Labour Act and recognize when to ask a lawyer.

#### B.7.1 Nigeria Data Protection Act 2023: General Application and Implementation Directive (GAID) 2025

- **Provider:** Nigeria Data Protection Commission (NDPC)
- **Actual address:** <https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf>
- **Type shown on the card:** Free primary legal guidance (official PDF)
- **Exact cost label:** Free
- **Time wording on the card:** About 3 hours for the relevant articles
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s6-r0`
- **Link button wording:** Open the official PDF

**Why it belongs here:** CVs, references and background checks involve personal data. The directive explains principles, lawful reasons for use, consent, information duties, breach reporting and agreements for handling data.

**What to do:** Read Articles 15, 16, 17, 18, 27, 33 and 34. Draft a six-line notice for a job-application form explaining use of candidate information.

**What we checked and what to be careful about:** The official NDPC PDF, reference NDPC/NDP ACT-GAID/01/2025, was inspected on 26 October and reread on 27 October after a sweep refusal. We read the article arrangement and opening articles, not the whole document. It is the implementation directive, not the Act itself. This is not legal advice: check the current text and amendments with a Nigerian lawyer. About three hours is for selected articles.

#### B.7.2 Labour Act, Chapter L1 Laws of the Federation of Nigeria 2004

- **Provider:** PLAC Laws of Nigeria (statute copy); ILO NATLEX listing
- **Actual address:** <https://lawsofnigeria.placng.org/laws/L1.pdf>
- **Type shown on the card:** Free primary legislation (official-style PDF)
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours for Parts I and II
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s6-r1`
- **Link button wording:** Open the statute PDF

**Why it belongs here:** Part II concerns recruiting permits, employer permits, recruiter licences and restrictions. Section 7 concerns written employment terms relevant to an offer.

**What to do:** Read sections 7, 23, 24, 25, 26 and 71. Write three questions to ask an employer before recruiting on its behalf.

**What we checked and what to be careful about:** The free statute copy was checked on 26 October. The Act dates from 1971 and is reproduced as Cap. L1 LFN 2004; the ILO NATLEX record mentions a 1990 revised edition. It may have later changes or parts replaced by other law. This is an official-style reproduction, not a government gazette download. Get current local legal advice before acting. The card allows about two hours for Parts I and II.

#### B.7.3 Google re:Work: onboarding and candidate experience guides

- **Provider:** Google re:Work
- **Actual address:** <https://rework.withgoogle.com/intl/en/guides/>
- **Type shown on the card:** Free official practice guides
- **Exact cost label:** Free
- **Time wording on the card:** About 2 hours
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s6-r2`
- **Link button wording:** Open the guides index

**Why it belongs here:** Hiring is not finished the moment someone accepts an offer. Candidate experience and helping someone join the organization complete the process.

**What to do:** From the index, open the onboarding guide and sketch a checklist for the new worker’s first 30 days.

**What we checked and what to be careful about:** The onboarding and candidate-experience guides were listed among the 23 results on the provider index on 26 October, with no payment or login shown. Those individual pages were not opened. This is index-level evidence, not a full read. Allow about two hours.

### B.8 Stage 8: Work the process - tools, metrics and getting hired

**When:** Weeks 18-20. **Stage budget:** 12 hours. **Cards:** 3.

Combine your work into a portfolio: a collection of examples showing what you can do. Learn basic recruiting measures and start applying for beginner roles.

**By the end, aim to:**

- Track a practice candidate list in a free tool and count movement through each hiring step.
- Present one finished hiring project as an example of your ability.
- Apply for beginner jobs using work evidence, not only certificates.

#### B.8.1 Managing Your Contacts With the HubSpot CRM

- **Provider:** HubSpot Academy
- **Actual address:** <https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm>
- **Type shown on the card:** Free short video lesson
- **Exact cost label:** Free
- **Time wording on the card:** 20 minutes
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s7-r0`
- **Link button wording:** Open the lesson

**Why it belongs here:** A contact-management tool can stand in for an applicant tracker while learning. CRM means customer relationship management; here it is only a practice record of contacts and stages.

**What to do:** Create a free account, add ten fake or anonymized practice candidates and label their hiring stages. Count how many are at each stage.

**What we checked and what to be careful about:** The Academy catalog was checked on 26 October. It describes courses as free and online with a free account; the lesson is listed as 20 minutes. The CRM has paid tiers, but the plan treats its free tier as sufficient for this practice. No account was actually created during our research.

#### B.8.2 Greenhouse guidance: recruiting metrics and benchmarks

- **Provider:** Greenhouse
- **Actual address:** <https://www.greenhouse.com/guidance>
- **Type shown on the card:** Free official articles and reports
- **Exact cost label:** Free
- **Time wording on the card:** 2-3 hours
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s7-r1`
- **Link button wording:** Open the guidance hub

**Why it belongs here:** Learn terms such as time to hire, source of hire, pass-through rates and quality of hire. They help explain where a process slows down or loses candidates.

**What to do:** Calculate four rates from your practice pipeline and write a paragraph explaining the main bottleneck—the point slowing progress.

**What we checked and what to be careful about:** The free guidance hub was checked on 26 October. The advertised 2026 benchmark report may require a form; we did not establish its download terms or assume the underlying dataset is free. Two to three hours is selected reading, not a promise of access to every report.

#### B.8.3 CIPM Nigeria: professional membership by examination

- **Provider:** Chartered Institute of Personnel Management of Nigeria
- **Actual address:** <https://cipmnigeria.org/membership/membership-routes/>
- **Type shown on the card:** Paid professional qualification
- **Exact cost label:** Paid - NGN fees shown on the provider site
- **Time wording on the card:** Five exam stages, four exam diets a year
- **Date printed on the card:** 2026-10-26. This is a historical check label.
- **Research-list status:** `confirmed`. A documented provider finding exists. It may say the item is paid; it does not automatically mean free.
- **Saved Done label:** `s7-r2`
- **Link button wording:** Check current fees

**Why it belongs here:** The local professional route helps show the Nigerian body of HR knowledge, including labour law, staff planning and HR measures. It is distinct from beginner completion certificates.

**What to do:** Do not enrol yet. Read the syllabus and exam FAQ, then reconsider after about six months of work experience.

**What we checked and what to be careful about:** The provider membership and exam FAQ were read on 26 October. There are five exam stages and four exam diets a year; “diet” here means an examination sitting, not food. Fees: application NGN 10,000; acceptance NGN 12,000; Foundation NGN 55,440; Intermediate I NGN 57,190; Intermediate II NGN 58,200; Professional I NGN 64,050; Professional II NGN 70,050; exemptions NGN 20,250–24,300. They can change. Recorded entry requirements are degree/HND plus five SSCE credits including English and Mathematics. Undergraduates can enrol but induction follows graduation. Amounts stay in provider-published naira, with no invented dollar conversion. This is a paid professional path, not part of the free-certificate claim.

### B.9 Why a few card notes seem to disagree

The source records were written at different times and levels of detail. A card can print a 26 October check date while the manifest records a 27 October reread. Jobberman can print a check-attempt date while the manifest leaves its confirmed date empty. Some broad re:Work notes say two guides were read, while the interviewer-training card specifically says its material came through search results, not a direct page open. We preserve these differences and explain them rather than quietly inventing a stronger, perfectly tidy history.

The original long-form document also contains practice projects, paid extras, exclusions and teaching explanations outside these card fields. The main chapters explain that wider material; these cards are not claimed to be the entire library by themselves.


## Appendix C: every link-research record

### C.1 How to read the labels

The original research date is **26 October 2026**. Some specific records were updated on 27 October. The review-age limit is **90 days**. These are records carried over into this explanation, not new provider visits.

| Exact stored label | Simple meaning |
|---|---|
| `confirmed` | The recorded provider finding is supported. It may confirm that an item is paid, not that it is free. |
| `ambiguous` | The page was read, but full free access is still unclear. |
| `partial` | Only part of the content was readable, such as a cookie banner. |
| `unreachable` | Readable provider content was not obtained; older notes may include server errors and unconfirmed outside-source prices. |
| `not_confirmed` | A lead or optional extra did not get confirmed provider evidence for free access. |

The totals are **23 confirmed, 1 unclear, 1 partial, 2 unreadable and 4 not confirmed: 31 entries altogether**. The last four groups make the eight open gaps. “No confirmed date” is not the same as “we never tried.” It means the record does not have a successful confirmation date.

### C.2 All 31 current records

#### C.2.1 Record 1: `confirmed`

**Address:** <https://www.youtube.com/playlist?list=PLeDNHX61_qlQWYcxZNB19TDOKbl625W2c>  
**Recorded confirmation date:** 2026-10-27.

The public TA playlist was checked on 27 October: 43 videos, with names and description readable without sign-in. Playback and phone-app handoff were not checked. AI-supported production is disclosed; check important claims against primary sources.

#### C.2.2 Record 2: `confirmed`

**Address:** <https://www.youtube.com/playlist?list=PLeDNHX61_qlQeRK1_i5flRpz2T0wjQXN2>  
**Recorded confirmation date:** 2026-10-27.

The public HR Essentials playlist was checked on 27 October: 16 videos and readable early titles/description. A YouTube error banner also appeared. Playback and phone-app handoff were not checked. Dr. Heather Staples developed it using AI-supported production; it is not a professional qualification.

#### C.2.3 Record 3: `confirmed`

**Address:** <https://learn.saylor.org/course/view.php?id=1292>  
**Recorded confirmation date:** 2026-10-26.

The PRDV226 syllabus says no tuition, free materials and a free completion certificate after 70% on the final exam.

#### C.2.4 Record 4: `confirmed`

**Address:** <https://openstax.org/books/principles-management/pages/11-introduction>  
**Recorded confirmation date:** 2026-10-26.

The textbook is openly licensed and readable free on the web.

#### C.2.5 Record 5: `confirmed`

**Address:** <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0>  
**Recorded confirmation date:** 2026-10-27.

The course page says the course and statement of participation are free. The 27 October sweep got 403; a same-day page reread still supported that claim. Bot filtering was the recorded explanation, not an inspected firewall fact.

#### C.2.6 Record 6: `confirmed`

**Address:** <https://alison.com/course/diploma-in-human-resources-hr>  
**Recorded confirmation date:** 2026-10-26.

Learning is free. The branded certificate is paid, but a Learner Record is free.

#### C.2.7 Record 7: `confirmed`

**Address:** <https://learn.saylor.org/course/BUS301>  
**Recorded confirmation date:** 2026-10-26.

The Saylor BUS301 course page was read. The wider Saylor access notes explain the free course and completion certificate.

#### C.2.8 Record 8: `ambiguous`

**Address:** <https://www.coursera.org/learn/recruiting-hiring-onboarding-employees>  
**Recorded confirmation date:** 2026-10-26.

The page was read, but the FAQ says access depends on purchase, trial or an available no-certificate choice. Full free access was not established, so it is not counted as free.

#### C.2.9 Record 9: `confirmed`

**Address:** <https://www.onetonline.org/>  
**Recorded confirmation date:** 2026-10-26.

This is a free public database about occupations and their tasks.

#### C.2.10 Record 10: `confirmed`

**Address:** <https://resources.workable.com/hr-templates/>  
**Recorded confirmation date:** 2026-10-26.

Templates are free to download. Starting a software trial is not required.

#### C.2.11 Record 11: `confirmed`

**Address:** <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction>  
**Recorded confirmation date:** 2026-10-26.

The structured-hiring article and worksheets were available free.

#### C.2.12 Record 12: `confirmed`

**Address:** <https://resources.workable.com/boolean-search-cheatsheets/>  
**Recorded confirmation date:** 2026-10-26.

The search cheat sheets were confirmed free.

#### C.2.13 Record 13: `confirmed`

**Address:** <https://www.youtube.com/watch?v=yMnw_2VNOVE>  
**Recorded confirmation date:** 2026-10-26.

The public free video was checked directly.

#### C.2.14 Record 14: `confirmed`

**Address:** <https://rework.withgoogle.com/intl/en/guides/>  
**Recorded confirmation date:** 2026-10-26.

The index and material from two guides were reviewed; other guide names came from the index. The training card gives the more cautious detail that it used returned search content rather than opening that page directly. Not every guide was read.

#### C.2.15 Record 15: `partial`

**Address:** <https://www.jobberman.com/employer/free-listing>  
**Recorded confirmation date:** No confirmed date.

Only a cookie banner could be read. The free-listing claim came from the provider’s search listing, so the card remains only partly checked. Its card check-attempt date does not supply a confirmed manifest date.

#### C.2.16 Record 16: `confirmed`

**Address:** <https://www.greenhouse.com/guidance>  
**Recorded confirmation date:** 2026-10-26.

The free guidance collection was read. Some linked reports may have extra forms and were not all independently checked.

#### C.2.17 Record 17: `confirmed`

**Address:** <https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices>  
**Recorded confirmation date:** 2026-10-26.

The structured-interviewing guide belongs to the reviewed re:Work set; its specific card records a direct page read and a March 2026 update. Other guides named from the index should not inherit that full-read claim.

#### C.2.18 Record 18: `confirmed`

**Address:** <https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences>  
**Recorded confirmation date:** 2026-10-26.

The manifest groups this with the reviewed re:Work material. Its specific card says provider content came back in search results, not a direct full-page open; individual steps were not fully read.

#### C.2.19 Record 19: `confirmed`

**Address:** <https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf>  
**Recorded confirmation date:** 2026-10-27.

The regulator PDF’s article list and opening provisions were read, not every page. The 27 October sweep got 403; a same-day reread found the PDF intact. The note interprets that refusal as bot filtering.

#### C.2.20 Record 20: `confirmed`

**Address:** <https://lawsofnigeria.placng.org/laws/L1.pdf>  
**Recorded confirmation date:** 2026-10-26.

The statute copy’s arrangement and opening provisions were read, not every page. It is not legal advice or proof that every later amendment is included.

#### C.2.21 Record 21: `confirmed`

**Address:** <https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm>  
**Recorded confirmation date:** 2026-10-26.

The Academy catalog described learning as free with a free account. The lesson is listed there; no research account was created.

#### C.2.22 Record 22: `confirmed`

**Address:** <https://cipmnigeria.org/membership/membership-routes/>  
**Recorded confirmation date:** 2026-10-26.

This is a paid professional route with a published naira fee table. The provider can review/change prices.

#### C.2.23 Record 23: `unreachable`

**Address:** <https://www.linkedin.com/learning/>  
**Recorded confirmation date:** No confirmed date.

The 26 October LinkedIn help research failed with server errors. Prices came from other 2026 guides and are unconfirmed. The 27 October summary implied 200, but the reading-tool retry got 403. Readable provider content was still not established; “login wall” is the older interpretation.

#### C.2.24 Record 24: `unreachable`

**Address:** <https://www.linkedin.com/help/recruiter/answer/a6807901>  
**Recorded confirmation date:** No confirmed date.

The help page returned 500 on 26 October. Recruiter Lite prices stayed outside-source estimates. The 27 October summary implied 200, but the reading-tool retry still got 500. The older note calls it a login wall; no raw body was available to prove that.

#### C.2.25 Record 25: `not_confirmed`

**Address:** <https://www.coursera.org/learn/aphri-talent-acquisition-and-onboarding>  
**Recorded confirmation date:** No confirmed date.

This is an optional paid extra. A provider page did not establish free access.

#### C.2.26 Record 26: `not_confirmed`

**Address:** <https://www.aihr.com/courses/sourcing-recruitment-certification/>  
**Recorded confirmation date:** No confirmed date.

This is a paid/subscription product. A provider page did not establish free access.

#### C.2.27 Record 27: `not_confirmed`

**Address:** <https://www.udemy.com/course/recruiter-training-hire-top-employees-in-30-days/>  
**Recorded confirmation date:** No confirmed date.

This is a paid product with frequently changing prices.

#### C.2.28 Record 28: `confirmed`

**Address:** <https://helpcenter.alison.com/en/articles/8206417-is-alison-really-free>  
**Recorded confirmation date:** 2026-10-26.

Alison’s help FAQ was read; it supports the distinction between free learning and a paid branded certificate.

#### C.2.29 Record 29: `confirmed`

**Address:** <https://support.saylor.org/hc/en-us/articles/23586212781844-FAQ-General>  
**Recorded confirmation date:** 2026-10-27.

Saylor’s FAQ says no tuition or fees and free completion certificates. The 27 October sweep got 403, but a same-day reread still supported the finding.

#### C.2.30 Record 30: `confirmed`

**Address:** <https://learn.saylor.org/mod/page/view.php?id=94644>  
**Recorded confirmation date:** 2026-10-26.

The Saylor course-material page was read. This is an extra evidence address, not another tracker card.

#### C.2.31 Record 31: `not_confirmed`

**Address:** <https://www.jobberman.com/job-seeker>  
**Recorded confirmation date:** No confirmed date.

This was only a lead page. No access claim was confirmed.

### C.3 The exact older 30-address sweep

Do not confuse this with the current 31-entry list above. These are the addresses in the actual first run, before the two direct-playlist addresses replaced the general channel destination. The three 403 entries are individually identified in the summary. The 27 entries shown as 200 are inferred from the owner’s total and complete non-success list, not parsed from a raw TSV we downloaded.

| # | Address at the time | Reply code | What happened after a refusal |
|---:|---|---:|---|
| 1 | <https://www.youtube.com/@HRLearningLab> | 200 | No separate non-success follow-up in this summary. |
| 2 | <https://learn.saylor.org/course/view.php?id=1292> | 200 | No separate non-success follow-up in this summary. |
| 3 | <https://openstax.org/books/principles-management/pages/11-introduction> | 200 | No separate non-success follow-up in this summary. |
| 4 | <https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0> | 403 | Reread on 27 October: the free course and free participation statement were still shown. |
| 5 | <https://alison.com/course/diploma-in-human-resources-hr> | 200 | No separate non-success follow-up in this summary. |
| 6 | <https://learn.saylor.org/course/BUS301> | 200 | No separate non-success follow-up in this summary. |
| 7 | <https://www.coursera.org/learn/recruiting-hiring-onboarding-employees> | 200 | No separate non-success follow-up in this summary. |
| 8 | <https://www.onetonline.org/> | 200 | No separate non-success follow-up in this summary. |
| 9 | <https://resources.workable.com/hr-templates/> | 200 | No separate non-success follow-up in this summary. |
| 10 | <https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction> | 200 | No separate non-success follow-up in this summary. |
| 11 | <https://resources.workable.com/boolean-search-cheatsheets/> | 200 | No separate non-success follow-up in this summary. |
| 12 | <https://www.youtube.com/watch?v=yMnw_2VNOVE> | 200 | No separate non-success follow-up in this summary. |
| 13 | <https://rework.withgoogle.com/intl/en/guides/> | 200 | No separate non-success follow-up in this summary. |
| 14 | <https://www.jobberman.com/employer/free-listing> | 200 | No separate non-success follow-up in this summary. |
| 15 | <https://www.greenhouse.com/guidance> | 200 | No separate non-success follow-up in this summary. |
| 16 | <https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices> | 200 | No separate non-success follow-up in this summary. |
| 17 | <https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences> | 200 | No separate non-success follow-up in this summary. |
| 18 | <https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf> | 403 | Reread the PDF on 27 October: article list and opening provisions were still present. |
| 19 | <https://lawsofnigeria.placng.org/laws/L1.pdf> | 200 | No separate non-success follow-up in this summary. |
| 20 | <https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm> | 200 | No separate non-success follow-up in this summary. |
| 21 | <https://cipmnigeria.org/membership/membership-routes/> | 200 | No separate non-success follow-up in this summary. |
| 22 | <https://www.linkedin.com/learning/> | 200 | No separate non-success follow-up in this summary. |
| 23 | <https://www.linkedin.com/help/recruiter/answer/a6807901> | 200 | No separate non-success follow-up in this summary. |
| 24 | <https://www.coursera.org/learn/aphri-talent-acquisition-and-onboarding> | 200 | No separate non-success follow-up in this summary. |
| 25 | <https://www.aihr.com/courses/sourcing-recruitment-certification/> | 200 | No separate non-success follow-up in this summary. |
| 26 | <https://www.udemy.com/course/recruiter-training-hire-top-employees-in-30-days/> | 200 | No separate non-success follow-up in this summary. |
| 27 | <https://helpcenter.alison.com/en/articles/8206417-is-alison-really-free> | 200 | No separate non-success follow-up in this summary. |
| 28 | <https://support.saylor.org/hc/en-us/articles/23586212781844-FAQ-General> | 403 | Reread on 27 October: the FAQ still said no tuition/fees and free completion certificates. |
| 29 | <https://learn.saylor.org/mod/page/view.php?id=94644> | 200 | No separate non-success follow-up in this summary. |
| 30 | <https://www.jobberman.com/job-seeker> | 200 | No separate non-success follow-up in this summary. |

**Everything the old sweep notes were trying to say:**

- The other 27 responses are inferred from 27 × 200 plus a complete three-item non-success list. The raw TSV could not be downloaded because its Azure Blob redirect was outside the sandbox’s allowed hosts. Azure Blob is an outside file-storage service; it is not part of our tracker.
- A 200 reply does not remove a research gap. Coursera, Jobberman, LinkedIn and paid extras did not gain new confirmed content findings simply from the sweep. Later LinkedIn retries still failed to provide readable content.
- LinkedIn Learning’s browser-like retry got 403; the Recruiter help retry got 500. The older record describes the sweep’s 200 as a login wall. Without the raw body, treat that as an interpretation, not something we independently saw in that response.
- This is a historical snapshot of 30 addresses. It gives no sweep HTTP code for either newly added direct playlist URL. A future sweep needs its own current list and date.

## Appendix D: every finished file and project file

### D.1 How to read the numbers and fingerprints

A byte is a unit of stored information. The long SHA-256 codes below are file fingerprints. They identify the specific saved content from the first report’s inspected product version. They are not passwords, links to secret accounts or things a learner needs to memorize.

These are copied historical measurements from the first report, not newly claimed production measurements. The Markdown source had **7,344 chunks separated by spaces/whitespace** when counted with Python. That is an approximate word count. The PDF had **15 pages** and **7,295 extracted text chunks**. Formatting, front-page text and text extraction explain why those counts differ. The early approximately 6,829-word count belonged to the first library version.

| Finished file in `learning-library/out/` | Bytes | Exact file fingerprint (SHA-256) |
|---|---:|---|
| `Recruiter-TA-Library.docx` | 57,938 | `7035af4ef964e507484be227eb8ef7da8ef86e12d4b326218e493002bfddce16` |
| `Recruiter-TA-Library.html` | 57,233 | `fd51c44e83766849de8e1dedaeb78be82e595f677516004846e26d604ef90604` |
| `Recruiter-TA-Library.md` | 47,473 | `9fa8ea0ad01c920943cc72ce1f1ab39977bd1f064fa989cf7f6449d77e511af5` |
| `Recruiter-TA-Library.pdf` | 52,610 | `76e6977c4c85f47bb12630f4496867b49fec731f24fda1599579d8e65750edca` |
| `roadmap-app.html` | 166,050 | `80f10411b75e8dd592657c4331af95d1608065f3681764a73154fc05d870cc19` |

Word and PDF outer-file fingerprints can change after a rebuild because of timestamps or other packaging details, even if the agreed drift comparison passes. That does not excuse actual content changes or a failing drift check.

### D.2 What all the file groups do

| File or group | Plain job description |
|---|---|
| `.agents/skills/README.md` | Explains where the protected skill is and how discovery works. |
| The 12 files inside `.agents/skills/resource-learning-library/` | The supplied instructions, examples, requirements, four programs and tests. Keep their approved contents unchanged. |
| `.claude/settings.json` and `.mcp.json` | Save project-level tool-connection/permission settings. They do not prove blocked external tools successfully ran. |
| `.gitignore` | Tells Git which disposable local files not to save. |
| `.gitattributes` | Helps Git handle document types and line endings consistently. |
| `.github/pull_request_template.md` | Prompts reviewers and authors to check important things before accepting work. |
| `.github/workflows/verify.yml` | Runs automatic project and browser checks. |
| `.github/workflows/link-check.yml` | Runs the separate outside-link report on its schedule or by manual request. |
| `Makefile` | Gives short names such as `make build` to longer sets of instructions. |
| `requirements.lock` | Fixes the Python package versions for repeatable document building. |
| `README.md` and `learning-library/README.md` | Introduce the project and its learning outputs. |
| `CHANGELOG.md` and `RETROSPECTIVE.md` | Explain dated changes, recurring problems and earlier repairs. |
| `THIRD-PARTY-NOTICES.md` | Points to the creature engine’s origin and permission text. |
| `docs/SETUP.md`, `docs/DESIGN-SPEC.md`, `docs/DEPLOYMENT.md` | Explain setup, intended current appearance and publishing. |
| `learning-library/DESIGN-SYSTEM.md` | Keeps the older style-transfer/refinement story, not a replacement for current source. |
| `learning-library/check-links.sh` | Requests each listed outside address and prints response codes. |
| The five files under `learning-library/out/` | The finished documents and tracker visitors receive. |
| `learning-library/src/recruiter-talent-acquisition-library.md` | The long editable learning document and research explanation. |
| `learning-library/src/roadmap-app.json` | The editable stage and card data for the tracker. |
| `learning-library/src/verification-manifest.json` | Stores research findings, dates, uncertainties and the old sweep snapshot. |
| `learning-library/src/fieldnotes-theme.css` | Controls the project’s appearance on top of the generator’s default look. |
| `learning-library/src/favicon-link.html` | Stores the exact approved tab-picture tag. |
| `learning-library/src/pals/pals.json` | Lists the ten creature positions and the protected payload fingerprint. |
| `learning-library/src/pals/pals-controller.js` | Handles starting, pausing, preferences and reconnecting creatures after the cards rebuild. |
| `learning-library/src/pals/pals.css` | Places the creature layer in document space and styles its controls. |
| `learning-library/src/pals/piixpal-payload.html` | The unchanged engine and eight species scripts. |
| `learning-library/src/pals/LICENSE-MIT.txt` | The upstream permission text for that engine. |
| `learning-library/tools/build_tracker.py` | Wraps the unchanged tracker generator with our theme, old-progress mapping, creatures and icon. |
| `tools/check.py` | Runs the project’s fast and drift checks. |
| `tools/serve_preview.py` | Serves the local preview from the output folder. |
| `tools/skill-hashes.sha256` | Lists the approved fingerprints for every supplied skill file. |
| `tools/test_deployment.py` and `tools/test_favicon.py` | Test the publishing settings and exact favicon exception. |
| `tools/visual/visual_check.mjs` | Controls Chromium and measures the actual built tracker. |
| `tools/visual/package.json` and `package-lock.json` | Describe and fix the Node/browser-test dependencies. |
| `vercel.json` | Tells the public host which finished folder and homepage rewrite to use. |

### D.3 The complete 57-file product inventory

The product version had **57 tracked files before either report**. The next table preserves all original paths, byte sizes and fingerprints. The reports are extra documents, not part of this older 57-file inventory. Local tool installations, cache files, screenshots and reports were not part of that list.

Do not worry if the codes look unreadable. The plain descriptions above explain the groups; the codes are kept so a maintainer has the same exact evidence as in the engineering report.

| Exact path in that product version | Bytes | File fingerprint (SHA-256) |
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

### D.4 The two new report files

- `docs/ENGINEERING-REPORT.md` is the technical explanation written first.
- `docs/ENGINEERING-REPORT-PLAIN-ENGLISH.md` is this separate explanation.

Neither changes the five finished learning files. We have not given these living reports a fixed fingerprint table here, which would become stale whenever the report changes. The 57-file historical list remains clearly separate.

### D.5 Do not edit only half of the job

Changing a source recipe without rebuilding leaves old finished files. Editing only the finished files means the next build can erase the change. Review both sides, compare before overwriting evidence, rebuild intentionally and keep disposable tool folders out of Git.

## Appendix E: every main request and its result

“Present in the files” and “checked by the owner on the live website” are different claims. The last column keeps that difference visible. This table follows all 39 decisions in the original report and adds this separate plain-English request.

| Request in simple words | What resulted | What the evidence does and does not say |
|---|---|---|
| Help a complete beginner enter HR through recruiting | Made an eight-stage plan with explanations and practical work. | The learner choices and source content show it. |
| Fit Lagos and about five study hours weekly | Kept about 20 weeks/94 hours, local legal sources and naira professional-route fees. | A learning plan, not a promise of a career result. |
| Free-first learning in different formats | Used videos, textbooks, guides, courses, templates and legal documents; marked paid extras. | See the card records and exclusions. |
| Provide every requested output format | Saved Markdown, PDF, DOCX, normal HTML and tracker HTML. | Five outputs were checked for rebuild drift. |
| Do not confuse free study with free certificates | Explained Saylor, OpenLearn, Alison, Coursera and CIPM differences. | Public-page findings, not completed enrolments. |
| Check facts and admit blocked checks | Disclosed the early blocked sweep and later recorded the owner-started result carefully. | Raw TSV remained unavailable. |
| Keep the supplied skill exact and permanent | Saved 12 original files and an approved fingerprint list. | The first report’s fingerprint check passed. |
| Save the trusted skill-discovery connection | Kept project connection/permission files. | Normal MCP POST calls were still blocked. |
| Look for useful skills per task | Read design/accessibility guidance and revisited the catalog for reporting. | Not a claim that unavailable MCP tools ran. |
| Explain understanding before acting | Used explicit go-ahead stages in the conversation. | This rewrite began after “Go ahead.” |
| Wait to commit, then publish changes only when approved | Earlier work was committed/pushed/PR’d after later explicit permission. | Eight product PRs accepted; reporting permission is not publishing permission. |
| Use Nature Photography as design authority | Transferred its palette, rules, font approach, borders and shadows. | Theme and design records document it. |
| Never make output-only appearance edits | Kept local CSS and builder changes, then regenerated. | Builder and drift checks support this. |
| Remove top bars but keep footer squares | Hero begins the framed content; footer accents remain. | Styles and browser checks. |
| Make the small hero eyebrow dark | Used dark ink on yellow. | Measured browser styles. |
| Put Done bottom-right and link bottom-left | Aligned card controls that way, including narrow layouts. | Geometry checks. |
| Give tags colors but preserve free/paid meaning | Rendered six fills; cost colors remain meaningful. | The paid/free classification is still text-based. |
| Balance stage margins and use square bullets | Applied the theme rules for both. | Source and visual history. |
| Put an outward arrow on each resource link | Added the small northeast arrow. | All-link browser assertion. |
| Use the exact footer credit | “Made with love and fried plantain, by Moyinoluwa”. | Built page and browser assertion. |
| Increase title 40%, despite repeated wording | Applied the increase once; a later request reduced it 25%. | Historical record and current size rule. |
| Remove only the small hero side gap | Aligned to the sheet, not full browser width. | Owner clarification and overflow checks. |
| Tighten hero spacing except eyebrow-to-title | Changed other gaps while protecting that interval. | Theme/refinement record. |
| Hide visible Reminder time label | Kept the input’s accessible name and title. | Current input markup. |
| Add ten real Pals | Used actual Piixpal, eight species and ten placements, tracker only. | Four owner choices and saved configuration. |
| Spread creatures down the page | Placed them on hero, dashboard, selected stage headings and footer. | All ten placements listed in Chapter 11. |
| Keep decoration optional and considerate | Idle startup, pause, status, reduced-motion startup off and print hiding. | Full teardown and live preference-change coverage remain limited. |
| Make preview survive resets | Saved the server script and rebuild-on-start command. | The historical recovery test and durable files. |
| Run a real outside-link sweep | Owner manually started a successful Actions run after our permission failures. | Summary plus run metadata, not downloaded raw rows. |
| Make the project publicly hostable | Published only output and rewrote only the homepage. | Config/tests plus owner deployment. |
| Make the phone title smaller | Reduced every part of its size rule by exactly 25%. | Current CSS and measured widths. |
| Open the actual TA playlist | Replaced the channel destination with a direct playlist. | Metadata and link input tests; playback caveat remains. |
| Put HR Essentials first | Added first card: 27 total, still 94 planned hours. | Sources and rebuilt files. |
| Do not move old Done ticks to new cards | Used a dedicated new label and retained old first-stage labels. | Old-state test fixture. |
| Stop Pals jitter during scrolling | Put the overlay in document space. | 0px native movement error versus 240px fixed control; owner acceptance. |
| Investigate unclickable preview links | Checked all links and mouse/touch behavior; no interception reproduced. | No guessed navigation patch was shipped. |
| Have fixes work on the live site | Owner confirmed after PR #7. | Not a full device/browser report. |
| Match the exact reference favicon | Copied/pinned it and added a tiny validation adapter plus color test. | PR #8/checks passed; later live icon not owner-confirmed. |
| Write a comprehensive engineering report | Created the first detailed file covering history, code, research, failures, evidence and limits. | A separate uncommitted document, not a product release. |
| Explain the same whole story in plain English | Created this separate file with definitions, examples and complete detailed lists. | No product edits, fresh provider research or new claimed test run. |

## Appendix F: a completeness guide

This table helps a reader move between the original engineering report and this explanation. It is a guide to coverage, not a claim that software can prove every sentence is equally understandable to every 12-year-old. We keep factual records exact and simplify their explanations.

| Original topic | Where the simpler explanation is |
|---|---|
| 1. Scope, evidence and dates | Chapter 1; opening notes distinguish the original checks from this rewrite. |
| 2. Executive engineering summary | Chapter 2: products, counts, eight PRs and the main lesson. |
| 3. Original brief and operating constraints | Chapter 3: learner, truthfulness, immutable tools, permissions and branch/design rules. |
| 4. Chronological reconstruction | Chapter 4: every phase from transfer bundle through favicon, including setbacks. |
| 5. Repository architecture and ownership boundaries | Chapter 5 and Appendix D: recipes, outputs, tool folders and document roles. |
| 6. Content/research/access findings | Chapter 6 and Appendices B/C: all providers, prices, exclusions, counts and gaps. |
| 7. Skill provenance and discovery | Chapter 7: origins, fingerprints, five tests, discovery setup and blocked execution. |
| 8. Generation and reproducibility | Chapter 8: pinned tools, build steps, anchors, self-containment and exact/meaningful comparisons. |
| 9. Browser runtime and persistence | Chapter 9: rendering, storage shape, fixed labels, streaks, backup, reset and reminders. |
| 10. Design-system port and evolution | Chapter 10: palette, all four rounds, title math, layout, tags and accepted tradeoffs. |
| 11. Piixpal and scroll repair | Chapter 11: licence, ten placements, lifecycle, motion, scroll control and overlap/CPU limits. |
| 12. Link sweep and evidence limits | Chapter 12 and Appendix C: network restrictions, schedule, manual result and frozen snapshot. |
| 13. Preview/reset infrastructure | Chapter 13: server, routes, browser-machine difference, resets and browser-library setup. |
| 14. Deployment and live feedback | Chapter 14: hosting config, all routes, no catch-all, CI evidence and live-check boundary. |
| 15. Favicon and validation exception | Chapter 15: exact fingerprint, exception steps, all six rejection variants and four color samples. |
| 16. Tests/CI/results | Chapter 16: every check layer, exact results, viewport table, exercised actions and missing coverage. |
| 17. Security/privacy/accessibility/performance | Chapter 17: trust boundaries, inline code, storage privacy and unperformed audits. |
| 18. Failure register | Chapter 18: all 32 recorded problem rows, with plain explanations and outcomes. |
| 19. Known debt/recommendations | Chapter 19: all 21 numbered suggestions and the warning against unrequested large systems. |
| 20. Maintenance/release/incident runbooks | Chapter 20: setup, edits, upgrades, preview recovery, research, releases and rollback. |
| 21. Work not done | Chapter 21: explicit limits, including no fresh test or research claims for this rewrite. |
| 22. Evidence/source index | Chapter 22: internal files and public records with their jobs explained. |
| Appendix A | Appendix A: eight PRs and 19 commits, with exact codes/dates/labels retained. |
| Appendix B | Appendix B: all eight stages, all 24 stage outcomes and all 27 cards, including actions/access caveats. |
| Appendix C | Appendix C: five statuses, all 31 current records and the exact 30-address historical sweep. |
| Appendix D | Appendix D: five output sizes/fingerprints, all 57 product files, group descriptions and report-file separation. |
| Appendix E | Appendix E: all 39 earlier decision rows plus the new plain-English report request. |

### Final explanation

We made more than a list of links. We made a researched learning route, five useful finished files, a local progress tracker, a borrowed visual style and a set of tools that help keep future changes honest.

We also learned not to confuse the workshop with the product. A missing browser package is not a broken design. An OK link reply is not proof of a free course. A wrong test assumption is not a wrong picture. A successfully started server can still serve an old page. A passing test is useful only when we understand its question.

The next person should keep the protected tools unchanged unless deliberately upgrading them, edit sources before rebuilding outputs, protect old progress, preserve old evidence and make new claims only after checking them.

That is what makes the project easier to trust—not pretending nothing ever went wrong, but leaving clear instructions and honest evidence about what happened.

**End of the plain-English report.**
