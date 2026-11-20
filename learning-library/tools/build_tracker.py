#!/usr/bin/env python3
"""Build the Fieldnotes-themed interactive roadmap tracker.

The vendored skill (`.agents/skills/resource-learning-library/`) is deliberately
left byte-exact. This script calls its generator to produce the functional
single-file app, then layers on:

  * the Fieldnotes design system (inline theme CSS and branding edits),
  * a system-aware light/dark toggle with a browser-local override, and
  * ten optional Piixpal pixel creatures plus one hand-built dangling spider
    (an inert <template> holds the MIT-licensed engine and a small inline
    controller). They lazy-load on idle, can be paused, and stay off under
    reduced motion.

Everything stays inline: no external fonts, images, scripts or network calls.

Run from the repository root:
    python3 learning-library/tools/build_tracker.py

Or from learning-library/:
    python3 tools/build_tracker.py
"""
from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # learning-library/
REPO = ROOT.parent                      # FieldNotes-HR/
SKILL_SCRIPTS = REPO / ".agents" / "skills" / "resource-learning-library" / "scripts"

sys.path.insert(0, str(SKILL_SCRIPTS))
import content
import interactive_app  # noqa: E402  (vendored generator, imported not modified)

DATA_PATH = ROOT / "src" / "roadmap-app.json"
THEME_PATH = ROOT / "src" / "fieldnotes-theme.css"
THEME_SCRIPT_PATH = ROOT / "src" / "theme-toggle.js"
SCROLL_TO_TOP_PATH = ROOT / "src" / "scroll-to-top.js"
PALS_DIR = ROOT / "src" / "pals"
OUTPUT_PATH = ROOT / "out" / "roadmap-app.html"


FAVICON_SHA256 = "ab629e3127cc247eb5077d4168f0a612b19d4c7cb05e2a43d5c3dc016449c9dd"


def favicon_tag() -> str:
    """Exact inline SVG favicon copied from Nature Photography's index.html.

    Pin the whole tag, not just the href scheme, so the validation exception
    cannot admit remote links, event handlers or modified active SVG content.
    """
    tag = (ROOT / "src" / "favicon-link.html").read_text(encoding="utf-8").strip()
    if hashlib.sha256(tag.encode()).hexdigest() != FAVICON_SHA256:
        raise RuntimeError("favicon source differs from the pinned reference tag")
    return tag


def without_inline_favicon(html: str) -> str:
    """Require exactly one pinned favicon, then remove only that exact tag.

    Used solely for validation. The delivered HTML retains the inline favicon;
    every other link tag remains subject to the original no-link restriction.
    """
    tag = favicon_tag()
    if html.count(tag) != 1:
        raise RuntimeError("expected exactly one pinned inline favicon")
    return html.replace(tag, "", 1)


def facts(data: dict) -> list[str]:
    stages = data.get("stages", [])
    cards = sum(len(s.get("resources", [])) for s in stages)
    hours = sum(int(s.get("estimated_hours") or 0) for s in stages)
    week_numbers = [int(n) for s in stages for n in re.findall(r"\d+", str(s.get("duration", "")))]
    weeks = max(week_numbers) if week_numbers else 0
    free = data["verified_free_count"]
    return [
        f"{len(stages):02d} STAGES",
        f"{cards} LEARNING CARDS",
        f"{hours} HOURS / {weeks} WEEKS",
        f"{free} VERIFIED FREE",
    ]


def load_pals_sources() -> dict:
    """Read every pals source file. Shared by main(), tools/check.py and CI."""
    return {
        "config": json.loads((PALS_DIR / "pals.json").read_text(encoding="utf-8")),
        "css": (PALS_DIR / "pals.css").read_text(encoding="utf-8"),
        "payload": (PALS_DIR / "piixpal-payload.html").read_text(encoding="utf-8"),
        "controller": (PALS_DIR / "pals-controller.js").read_text(encoding="utf-8"),
    }


def pals_edits(src: dict) -> list[tuple[str, str, str]]:
    """(anchor regex, literal replacement, label) triples for the pals layer.

    Kept separate from `branding_edits` so the branding-anchor contract
    still describes only the Fieldnotes branding, and `tools/check.py` can break
    each of these three anchors independently too.
    """
    pals = src["config"]["pals"]
    controller = src["controller"].replace(
        "__SITE_PALS_JSON__", json.dumps(pals, separators=(",", ":"))
    )
    if "__SITE_PALS_JSON__" in controller:
        raise RuntimeError("SITE_PALS placeholder was not replaced")

    style = '<style data-pals="fieldnotes">\n' + src["css"].rstrip() + "\n</style>\n"
    controls = (
        '<div class="pals-controls" id="pals-controls" hidden>\n'
        '  <button id="pals-toggle" type="button" aria-pressed="true">Pause tiny pals</button>\n'
        '  <p class="pals-status" id="pals-status" role="status" aria-live="polite"></p>\n'
        '</div>\n'
    )
    spider = (
        '<div class="fieldnotes-dangling-spider" id="fieldnotes-spider" hidden aria-hidden="true">\n'
        '  <svg viewBox="0 0 64 108" focusable="false">\n'
        '    <path class="spider-thread" d="M52 0V70"></path>\n'
        '    <g class="spider-dangle">\n'
        '      <path class="spider-legs" d="M48 78L43 73L39 74L36 70 M47 81L41 80L37 83L34 81 M47 84L42 87L39 92L35 94 M49 87L45 93L44 99L40 102 M56 78L60 73L62 74L63 70 M57 81L61 80L63 83 M57 84L61 87L62 92 M55 87L59 93L60 99L63 102"></path>\n'
        '      <ellipse class="spider-body" cx="52" cy="81" rx="4.8" ry="5.4"></ellipse>\n'
        '      <ellipse class="spider-body" cx="52" cy="88" rx="5.4" ry="6.2"></ellipse>\n'
        '      <circle class="spider-eyes" cx="50" cy="78" r="1"></circle>\n'
        '      <circle class="spider-eyes" cx="54" cy="78" r="1"></circle>\n'
        '    </g>\n'
        '  </svg>\n'
        '</div>\n'
    )
    script = ('<script data-fieldnotes-pals-controller>\n'
              + controller.rstrip() + "\n</script>\n")
    payload = src["payload"].rstrip()

    return [
        (r"</head>", style + "</head>", "pals style"),
        (r'<main id="roadmap" aria-label="Roadmap stages"></main>',
         controls + '<main id="roadmap" aria-label="Roadmap stages"></main>',
         "pals controls"),
        (r"</body>", spider + payload + "\n" + script + "</body>",
         "dangling spider, pals payload and controller"),
    ]


def inject_pals(html: str, src: dict) -> str:
    """Layer the optional decorative pals onto the already-themed app."""
    for pattern, replacement, label in pals_edits(src):
        # A lambda keeps the replacement literal: no backreference expansion.
        new, count = re.subn(pattern, lambda _m, r=replacement: r, html)
        if count != 1:
            raise RuntimeError(f"pals anchor not found: {label}")
        html = new
    return html


def branding_edits(data: dict) -> list[tuple[str, str, str]]:
    """The contract between this build layer and the vendored generator's HTML.

    Each triple is (anchor regex, literal replacement, human label). These
    anchors are exact strings emitted by the unmodified `interactive_app.py`.
    `tools/check.py` verifies that every anchor still matches the generator's
    live output and that breaking any single one fails the build loudly, so a
    future generator update cannot silently drop the Fieldnotes branding.
    """
    title = str(data.get("title") or "Learning roadmap")
    chips = "".join(f"<span>{text}</span>" for text in facts(data))
    theme_toggle = (
        '<button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle color theme" '
        'data-theme-icon="sun" aria-pressed="false" '
        'title="Follows your system setting by default; your choice is saved in this browser.">'
        '<svg class="theme-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<g class="theme-icon-sun"><circle cx="12" cy="12" r="3.75"></circle>'
        '<path d="M12 1.75v2.1m0 16.3v2.1M4.76 4.76l1.49 1.49m11.5 11.5 1.49 1.49M1.75 12h2.1m16.3 0h2.1M4.76 19.24l1.49-1.49m11.5-11.5 1.49-1.49"></path></g>'
        '<path class="theme-icon-moon" d="M20.4 15.1A8.55 8.55 0 0 1 8.9 3.6 8.6 8.6 0 1 0 20.4 15.1Z"></path>'
        '</svg></button>'
    )
    return [
        (r"<title>Learning roadmap</title>",
         f"<title>{title} | Fieldnotes HR</title>", "title"),

        (r'<meta name="theme-color" content="#0B3D5C">',
         '<meta name="theme-color" content="#11142B">\n'
         '<meta name="color-scheme" content="light dark">\n'
         '<meta name="description" content="A free-first, roadmap-ordered learning '
         'library for breaking into HR through the Recruiter / Talent Acquisition '
         'path, with browser-local progress tracking.">', "theme-color meta"),

        (r"<body>",
         '<body>\n<a class="skip-link" href="#roadmap">Skip to roadmap</a>', "body"),

        (r'<p class="eyebrow">YOUR LEARNING ROADMAP</p>',
         '<div class="hero-eyebrow-row"><p class="eyebrow">FIELDNOTES / HR</p>'
         + theme_toggle + '</div>', "hero eyebrow and theme toggle"),

        (r'<footer class="app-footer">A self-contained roadmap tracker\. Your progress is stored locally in this browser\.</footer>',
         '<footer class="app-footer">Made with love and fried plantain, by Moyinoluwa</footer>',
         "footer credit"),

        (r'<div class="toolbar" aria-label="Reminder and progress controls">',
         '<div class="toolbar" aria-label="Tracker controls">', "toolbar"),

        # Web Interface Guidelines: form controls need a meaningful name and an
        # explicit autocomplete so password managers stay out of non-auth fields.
        (r'<input id="reminder-time" type="time" value="19:00">',
         '<input id="reminder-time" name="reminder-time" type="time" '
         'autocomplete="off" aria-label="Reminder time" '
         'title="Reminder time" value="19:00">', "reminder time input"),

        (r'<input id="import-progress" type="file" accept="application/json,\.json">',
         '<input id="import-progress" name="import-progress" type="file" '
         'accept="application/json,.json">', "import file input"),

        (r'<p id="subtitle"></p>',
         '<p id="subtitle"></p>\n      '
         f'<div class="hero-facts" aria-label="Roadmap overview">{chips}</div>',
         "subtitle"),
    ]


def replace_once(html: str, old: str, new: str, label: str) -> str:
    if html.count(old) != 1:
        raise RuntimeError(f"extension anchor missing or duplicated: {label}")
    return html.replace(old, new, 1)


def progress_edits(data: dict) -> list[tuple[str, str, str]]:
    ledger = json.loads((ROOT / 'src/progress-compatibility.json').read_text())
    aliases = {old: prefix+identity for kind,prefix in [('resources','resource:'),('stages','stage:')]
               for identity,old_keys in ledger[kind].items() for old in old_keys}
    adapter = (ROOT / 'src/progress-adapter.js').read_text() + '\n' + (ROOT / 'src/milestones.js').read_text()
    if adapter.count('__PROGRESS_ALIASES__') != 1:
        raise RuntimeError('progress aliases slot missing or duplicated')
    adapter = adapter.replace('__PROGRESS_ALIASES__',json.dumps(aliases,sort_keys=True))
    identities = [{'id': stage['id'], 'resources': [{k:r[k] for k in ('id','milestones','milestone_note','optional','learning_notes','references','access_note','access_summary')} for r in stage['resources']]}
                  for stage in data['stages']]
    bridge = ('const RESOURCE_ITEMS = [];\nconst PROGRESS_IDENTITIES = '
              + json.dumps(identities, separators=(',', ':')).replace('<', '\u003c')
              + ';\nDATA.retired_resources = ' + json.dumps(data.get('retired_resources',[])).replace('<', '\u003c') + ';\nDATA.stages.forEach((stage,si) => { stage.id=PROGRESS_IDENTITIES[si].id; '
              'stage.resources.forEach((resource,ri) => { Object.assign(resource,PROGRESS_IDENTITIES[si].resources[ri]); }); });')
    return [
        ('const RESOURCE_ITEMS = [];', bridge, 'identity bridge'),
        ('localStorage.setItem(STORAGE_KEY, JSON.stringify(state));', 'preserveProgressUpgradeSnapshot(); localStorage.setItem(STORAGE_KEY, JSON.stringify(state));', 'progress recovery'),
        ("const heading = el('span','stage-heading');\n    const stageTitle = el('strong','',stage.title || `Stage ${stageIndex+1}`); heading.append(stageTitle);\n    const sub = [stage.duration, stage.estimated_hours ? `${stage.estimated_hours} hours` : ''].filter(Boolean).join(' · ');\n    if (sub) heading.append(el('small','',sub));\n    summary.append(heading);\n    const meter = el('span','stage-meter','0%'); meter.dataset.meter = String(stageIndex); summary.append(meter);",
         "const stageTitle = el('strong','stage-heading',stage.title || `Stage ${stageIndex+1}`); summary.append(stageTitle);\n    const sub = [stage.duration, stage.estimated_hours ? `${stage.estimated_hours} hours` : ''].filter(Boolean).join(' · ');\n    if (sub) summary.append(el('small','stage-subheading',sub));\n    const meter = el('span','stage-meter','0%'); meter.dataset.meter = String(stageIndex); summary.append(meter);\n    const indicator = el('span','stage-toggle-indicator'); indicator.setAttribute('aria-hidden','true'); summary.append(indicator);",
         'aligned stage summary'),
        ('function buildRoadmap() {', 'function buildLegacyRoadmap() {', 'milestone renderer'),
        ('function updateDashboard() {', 'function updateLegacyDashboard() {', 'balanced dashboard'),
        ('function updateStageMeters() {', 'function updateLegacyStageMeters() {', 'balanced stage meters'),
        ('function loadState() {', adapter+'\nfunction loadLegacyState() {', 'progress loader'),
        ('function resourceKey(stageIndex, resourceIndex) { return `s${stageIndex}-r${resourceIndex}`; }',
         'function resourceKey(stageIndex, resourceIndex) { return "resource:" + DATA.stages[stageIndex].resources[resourceIndex].id; }', 'progress-key'),
        ('function stageKey(stageIndex) { return `s${stageIndex}-complete`; }',
         'function stageKey(stageIndex) { return "stage:" + DATA.stages[stageIndex].id; }', 'stage-key'),
        ("{version:1,title:DATA.title,done:state.done,activityDates:state.activityDates,reminderTime:state.reminderTime}",
         "{version:3,storage_id:DATA.storage_id,title:DATA.title,done:state.done,activityDates:state.activityDates,manualCheckinDates:state.manualCheckinDates,legacyActivityDates:state.legacyActivityDates,milestones:state.milestones,detailed:state.detailed,reminderTime:state.reminderTime}", 'backup export'),
        ("const incoming=JSON.parse(await file.text()); if(!incoming || typeof incoming.done!=='object' || !Array.isArray(incoming.activityDates)) throw new Error('format');",
         "const incoming=normalizeProgress(JSON.parse(await file.text()),true);", 'backup import'),
        ("function markActivity() { const today = localDateKey(); if (!state.activityDates.includes(today)) state.activityDates.push(today); }",
         "function markActivity() { /* Completion is independent of attendance. */ }", 'independent attendance'),
        ("buildRoadmap(); setupReminderControls();", "buildRoadmap(); setupReminderControls(); setupDailyCheckin();", 'daily check-in setup'),
        ("const todayDone=state.activityDates.includes(localDateKey()); document.getElementById('today-status').textContent=todayDone?'Logged today':'Not logged yet';",
         "renderDailyCheckin(); const todayDone=state.activityDates.includes(localDateKey());", 'daily status'),
        ("document.getElementById('reminder-summary').textContent=todayDone?'Nice work — today’s learning activity is recorded.':`Complete a resource before or after ${state.reminderTime} to record today’s activity.`;",
         "renderDailyCheckin();", 'daily explanatory text'),
        ("state.done=incoming.done;state.activityDates=incoming.activityDates.filter(x=>/^\\d{4}-\\d{2}-\\d{2}$/.test(x));if(/^\\d\\d:\\d\\d$/.test(incoming.reminderTime||''))state.reminderTime=incoming.reminderTime;saveState();buildRoadmap();time.value=state.reminderTime;setNotice('Progress imported.');",
         "const candidate={...incoming,notificationsEnabled:state.notificationsEnabled}; preserveProgressUpgradeSnapshot(); const before=localStorage.getItem(STORAGE_KEY); if(before && !localStorage.getItem(STORAGE_KEY+':before-checkins-v3')) localStorage.setItem(STORAGE_KEY+':before-checkins-v3',before); localStorage.setItem(STORAGE_KEY,JSON.stringify(candidate)); state=candidate;buildRoadmap();time.value=state.reminderTime;setNotice('Backup restored. No new study day was added.');", 'check-in backup import'),
        ("state={done:{},activityDates:[],reminderTime:DATA.reminder_time||'19:00',notificationsEnabled:false,lastNotificationDate:''};",
         "state=normalizeProgress({});", 'check-in reset'),
        ("<div class=\"notice\"><strong>Saved on this device.</strong> Progress stays in this browser's local storage, follows this device's local calendar for streaks, and does not sync across devices. Browser notifications are checked while this page is open; they cannot reliably alert you after it is closed. If notifications are unavailable or permission is denied, the in-app check-in still works.</div>",
         "<div class=\"notice\"><strong>Saved in this browser.</strong> Progress stays here and won't move to other devices. Streaks use your local date. Check off tasks when done; progress is self-reported.</div>", 'plain-language progress note'),
        ('<button class="primary" id="enable-notifications" type="button">Enable browser reminders</button>',
         '<button class="primary" id="enable-notifications" type="button">Turn on reminders</button>', 'reminder button copy'),
        ('<label for="reminder-time">Reminder time</label>',
         '<label for="reminder-time">Remind me at</label>', 'reminder label copy'),
        ('Browser reminders require permission and this page to remain open.',
         'Reminders need permission and this page to stay open.', 'reminder help copy'),
        ('<button id="export-progress" type="button">Export progress</button>',
         '<button id="export-progress" type="button">Download backup</button>', 'backup export label'),
        ('>Import progress<input id="import-progress"',
         '>Import backup<input id="import-progress"', 'backup import label'),
        ('<button id="reset-progress" type="button">Reset</button>',
         '<button id="reset-progress" type="button">Clear progress</button>', 'reset button label'),
        ('Could not save to browser storage. Export progress or try another browser.',
         'Could not save progress. Download a backup or try another browser.', 'storage error copy'),
        ('This browser does not support system notifications. The in-app reminder remains available.',
         'Notifications are not supported here. You can still check in here.', 'unsupported notifications copy'),
        ('Browser notifications need a secure HTTPS page or localhost. The in-app reminder remains available.',
         'Notifications need HTTPS or localhost. You can still check in here.', 'secure context copy'),
        ('Browser reminders are enabled while this page stays open. They will not run after the app is closed.',
         'Reminders are on while this page is open. They stop when you close it.', 'notification enabled copy'),
        ('Notification permission ${permission}. The in-app reminder remains available.',
         'Notifications ${permission}. You can still check in here.', 'notification permission copy'),
        ('Could not request notification permission. The in-app reminder remains available.',
         'Could not turn on notifications. You can still check in here.', 'notification error copy'),
        ('Reminder time saved as ${state.reminderTime}. Keep the page open for browser alerts.',
         'Reminder set for ${state.reminderTime}. Keep this page open for alerts.', 'reminder saved copy'),
        ('That file could not be read as roadmap progress JSON.',
         'Cannot read this backup. Choose a valid progress file.', 'backup error copy'),
        ('Clear progress and streak history saved in this browser?',
         'Clear all progress and study days from this browser?', 'reset confirmation copy'),
        ('Progress reset on this device.',
         'Progress cleared from this browser.', 'reset result copy'),
        ('Take a few minutes to continue your learning roadmap and protect your daily streak.',
         'Take a few minutes to study and keep your streak.', 'reminder notification copy'),
        ('A browser reminder could not be shown. The in-app check-in remains available.',
         'Could not show the reminder. You can still check in here.', 'reminder failure copy'),
        ("setNotice('Browser reminders are enabled while this page stays open.');",
         "setNotice('Reminders are on while this page is open.');", 'loaded reminder copy'),
        ('Work through the roadmap in order, one step at a time.',
         'Learn recruiting, one step at a time.', 'subtitle fallback copy'),
    ]


def apply_progress(html: str, data: dict) -> str:
    for old,new,label in progress_edits(data):
        html = replace_once(html,old,new,label)
    return html


def remove_reminder_option(html: str) -> str:
    """Remove reminder UI and scheduling while retaining progress backup compatibility."""
    controls = (
        '  <button class="primary" id="enable-notifications" type="button">Turn on reminders</button>\n'
        '  <label for="reminder-time">Remind me at</label><input id="reminder-time" '
        'name="reminder-time" type="time" autocomplete="off" aria-label="Reminder time" '
        'title="Reminder time" value="19:00">\n'
    )
    html = replace_once(html, controls, "", "reminder controls")

    old_status = ('<span class="status" id="notification-status" role="status" '
                  'aria-live="polite">Reminders need permission and this page to stay open.</span>')
    new_status = ('<span class="status" id="progress-status" role="status" '
                  'aria-live="polite">Progress updates will appear here.</span>')
    html = replace_once(html, old_status, new_status, "progress status copy")
    html = replace_once(html, "document.getElementById('notification-status')",
                        "document.getElementById('progress-status')", "progress status target")

    # The generator combines reminder listeners and backup controls in one
    # function. Drop only the reminder-specific prefix; export/import/reset
    # continue to use the same visible progress status.
    setup_pattern = (
        r"function setupReminderControls\(\) \{\n.*?"
        r"(?=  document\.getElementById\('export-progress'\)\.addEventListener)"
    )
    html, count = re.subn(setup_pattern, "function setupProgressControls() {\n", html, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("reminder setup anchor missing or duplicated")

    # Import/reset handlers used to restore the reminder-time input. The
    # preference field itself remains in saved state so older backups still
    # round-trip, but there is no longer an input to synchronize.
    resync = "time.value=state.reminderTime;"
    if html.count(resync) != 2:
        raise RuntimeError("expected two reminder-time input syncs in progress handlers")
    html = html.replace(resync, "")

    check_pattern = r"function checkReminder\(\) \{.*?\n\}\n"
    html, count = re.subn(check_pattern, "", html, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("reminder scheduler anchor missing or duplicated")

    html = replace_once(
        html,
        "buildRoadmap(); setupReminderControls(); setupDailyCheckin();",
        "buildRoadmap(); setupProgressControls(); setupDailyCheckin();",
        "progress controls setup",
    )
    scheduler = (
        "if (state.notificationsEnabled && 'Notification' in window && Notification.permission==="
        "'granted') setNotice('Reminders are on while this page is open.');\n"
        "checkReminder(); setInterval(checkReminder,60000); "
        "document.addEventListener('visibilitychange',()=>{if(!document.hidden)checkReminder();});"
    )
    html = replace_once(html, scheduler, "", "reminder scheduler startup")

    for marker in ('id="enable-notifications"', 'id="reminder-time"',
                   'function setupReminderControls(', 'function checkReminder(',
                   'Notification.requestPermission', 'setInterval(checkReminder'):
        if marker in html:
            raise RuntimeError(f"reminder option remains in generated app: {marker}")
    return html


def transform(html: str, data: dict, theme_css: str) -> str:
    for pattern, replacement, label in branding_edits(data):
        # A lambda keeps the replacement literal: no backreference expansion.
        new, count = re.subn(pattern, lambda _m, r=replacement: r, html)
        if count != 1:
            raise RuntimeError(f"branding anchor not found: {label}")
        html = new

    html = apply_progress(html, data)
    html = remove_reminder_option(html)

    style = '<style data-theme="fieldnotes">\n' + theme_css.rstrip() + "\n</style>\n"
    theme_script = THEME_SCRIPT_PATH.read_text(encoding="utf-8").strip()
    if not theme_script:
        raise RuntimeError("theme controller source is empty")
    theme_script_tag = '<script data-theme-controller>\n' + theme_script + "\n</script>\n"
    if html.count("</head>") != 1:
        raise RuntimeError("branding anchor not found: </head>")
    html = html.replace("</head>", favicon_tag() + "\n" + theme_script_tag + style + "</head>", 1)

    scroll_script = SCROLL_TO_TOP_PATH.read_text(encoding="utf-8").strip()
    if not scroll_script:
        raise RuntimeError("scroll-to-top controller source is empty")
    scroll_button = (
        '<button id="back-to-top" class="back-to-top" type="button" hidden '
        'aria-label="Back to top" title="Back to top">'
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M12 19V5M6 11l6-6 6 6"></path></svg></button>\n'
    )
    scroll_script_tag = ('<script data-scroll-to-top-controller>\n'
                         + scroll_script + "\n</script>\n")
    html = replace_once(html, "</body>", scroll_button + scroll_script_tag + "</body>",
                        "back-to-top control")
    return html


def assert_self_contained(html: str) -> None:
    html = without_inline_favicon(html)
    problems = []
    for pattern, label in (
        (r"<\s*link\b", "link element"),
        (r"<\s*img\b", "image element"),
        (r"<\s*iframe\b", "iframe element"),
    ):
        if re.search(pattern, html, re.I):
            problems.append(label)
    css_blocks = re.findall(r"<\s*style\b[^>]*>(.*?)<\s*/\s*style\s*>", html, re.I | re.S)
    if any(re.search(r"url\s*\(", css, re.I) for css in css_blocks):
        problems.append("CSS asset reference")
    for tag in re.finditer(r"<\s*script\b([^>]*)>", html, re.I):
        if re.search(r"\bsrc\s*=", tag.group(1), re.I):
            problems.append("external script")
    if html.count('data-theme="fieldnotes"') != 1:
        problems.append("theme block missing or duplicated")
    for token in ("--fn-ink:#11142B", "--fn-paper:#FFF8E7", "--fn-blue:#3768FF",
                  "--fn-shadow:#E63E7A"):
        if token not in html:
            problems.append(f"missing token {token}")
    if html.count('data-pals="fieldnotes"') != 1:
        problems.append("pals style block missing or duplicated")
    if html.count("data-theme-controller") != 1:
        problems.append("theme controller missing or duplicated")
    if html.count('name="color-scheme" content="light dark"') != 1:
        problems.append("light/dark color-scheme hint missing or duplicated")
    eyebrow_control = ('<div class="hero-eyebrow-row"><p class="eyebrow">FIELDNOTES / HR</p>'
                       '<button id="theme-toggle"')
    if html.count(eyebrow_control) != 1:
        problems.append("theme toggle must share the hero eyebrow row")
    if html.count("'stage-toggle-indicator'") != 1:
        problems.append("aligned stage toggle indicator missing or duplicated")
    for marker in ('id="theme-toggle"', 'aria-label="Toggle color theme"',
                   'data-theme-icon="sun"', 'id="back-to-top"', 'data-scroll-to-top-controller',
                   'id="fieldnotes-spider"', 'id="pals-payload"', 'id="pals-controls"',
                   'id="pals-toggle"', 'id="progress-status"',
                   "data-fieldnotes-pals-controller"):
        if html.count(marker) != 1:
            problems.append(f"build marker missing or duplicated: {marker}")
    for marker in ('id="enable-notifications"', 'id="reminder-time"',
                   'function setupReminderControls(', 'function checkReminder(',
                   'Notification.requestPermission', 'setInterval(checkReminder'):
        if marker in html:
            problems.append(f"removed reminder feature remains: {marker}")
    if "Piixpal v0.4.0" not in html or "MIT" not in html:
        problems.append("Piixpal MIT provenance header missing")
    for pattern, label in (
        (r"<\s*script[^>]*\bsrc\s*=", "external script src"),
        (r"\bfetch\s*\(", "network call in pals layer"),
        (r"XMLHttpRequest", "network call in pals layer"),
        (r"WebSocket", "network call in pals layer"),
    ):
        if re.search(pattern, html, re.I):
            problems.append(label)
    if problems:
        raise RuntimeError("not self-contained: " + ", ".join(problems))


def main() -> int:
    content.generate()
    data = content.app_data(content.load())
    theme_css = THEME_PATH.read_text(encoding="utf-8")
    pals_src = load_pals_sources()

    # 1. Functional base from the vendored, hash-verified skill generator.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    interactive_app.build_app(data, OUTPUT_PATH)
    base = OUTPUT_PATH.read_text(encoding="utf-8")

    # 2. Layer the Fieldnotes design system, then the optional pals, on top.
    themed = transform(base, data, theme_css)
    themed = inject_pals(themed, pals_src)
    assert_self_contained(themed)
    OUTPUT_PATH.write_text(themed, encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO)} ({len(themed.encode('utf-8'))} bytes)")
    print("Base generator: vendored skill (unmodified). Theme: Fieldnotes design system.")
    pals = pals_src['config']['pals']
    fixed_spiders = sum(1 for pal in pals if pal.get('kind') == 'fixed-spider')
    print(f"Pals: {len(pals)} total ({len(pals) - fixed_spiders} Piixpal creatures + "
          f"{fixed_spiders} fixed viewport spider), lazy-loaded, pausable, off under reduced motion.")
    print("Checks: no external assets, no CSS asset refs, no network calls, "
          "theme + pals blocks present, tokens present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
