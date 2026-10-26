# resource-learning-library

A reconstructed, portable agent skill for building roadmap-ordered learning libraries from verified resources. It supports free, paid, or mixed resources and PDF, DOCX, Markdown, static HTML, or an interactive HTML roadmap tracker.

## Contents

```text
SKILL.md                    Intake, roadmap, research, production, and QA workflow
INSTALL.md                  Installation and smoke-test instructions
requirements.txt             Python dependencies
scripts/docx_render.py      Markdown -> PDF, DOCX, Markdown copy, or static HTML
scripts/validate_build.py   Checks DOCX XML, PDF structure, links, and HTML
scripts/style_audit.py      Checks Markdown mechanics and prose patterns
scripts/interactive_app.py  JSON roadmap/resources -> one-file progress-tracker app
tests/                       Offline smoke tests
example/                     Sample Markdown and demo app data
```

## Install dependencies

Requires Python 3. Install the renderer and validation dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

Research still requires `curl` and a browser/page-retrieval tool; the scripts do not research resources or verify prices on their own.

## Render a resource library

By default, the renderer creates DOCX and static HTML. Select one or more formats explicitly when needed:

```bash
python3 scripts/docx_render.py example/01-getting-started.md -o /tmp/rll-demo --name Demo
python3 scripts/docx_render.py example/01-getting-started.md -o /tmp/rll-demo --name Demo-PDF --format pdf
python3 scripts/docx_render.py example/01-getting-started.md -o /tmp/rll-demo --name Demo-All --format pdf docx md html
python3 scripts/validate_build.py /tmp/rll-demo/Demo-PDF.pdf /tmp/rll-demo/Demo.docx /tmp/rll-demo/Demo.html
python3 scripts/style_audit.py example/01-getting-started.md
```

The first level-one heading is used as the document title and removed from the body by default. See `python3 scripts/docx_render.py --help` for title and output options.

## Build an interactive roadmap app

Prepare roadmap and resource data as JSON, using `example/interactive-demo.json` as a schema example. Then build and validate a single-file app:

```bash
python3 scripts/interactive_app.py --input example/interactive-demo.json --output /tmp/rll-demo/roadmap-app.html
python3 scripts/validate_build.py --interactive-html /tmp/rll-demo/roadmap-app.html
```

The app tracks completed resources, overall progress, and a daily streak by the device's local calendar in the current browser's local storage. It supports manual progress export/import. Browser notifications require permission and a secure context and are checked only while the page is open; the app cannot reliably notify after closing and has no cross-device sync or push backend. The demo data is explicitly illustrative, not a researched or verified resource library.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Reconstruction note

This package is a best-effort reconstruction from the supplied `SKILL.md`, `README.md`, and `INSTALL.md`. The original renderer and audit scripts were not included, so this implementation reproduces the described workflow and interfaces rather than claiming to be the original source code. This revision adds the requested roadmap-first intake, output formats, and interactive tracker while clarifying the browser-notification limits.
