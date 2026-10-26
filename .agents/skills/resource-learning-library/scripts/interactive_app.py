#!/usr/bin/env python3
"""Build a single-file interactive roadmap tracker from structured JSON."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


APP_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0B3D5C">
<title>Learning roadmap</title>
<style>
:root{color-scheme:light;--navy:#0B3D5C;--blue:#12628F;--pale:#F6FAFD;--ink:#183243;--muted:#536B7B;--border:#D4E0E7;--green:#15805D;--amber:#B56A12;--red:#A63B4B}
*{box-sizing:border-box}body{margin:0;background:#F3F7F9;color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}button,input{font:inherit}button{cursor:pointer}
.app{max-width:1120px;margin:0 auto;padding:24px 18px 52px}.hero{display:flex;justify-content:space-between;gap:24px;align-items:center;padding:30px clamp(20px,5vw,46px);background:var(--navy);color:white;border-radius:18px;box-shadow:0 14px 32px rgba(11,61,92,.14)}.eyebrow{margin:0 0 8px;color:#B8D2E0;letter-spacing:.12em;font-size:.75rem;font-weight:800}.hero h1{font-size:clamp(1.7rem,4vw,2.7rem);line-height:1.14;margin:0}.hero p{color:#DCEAF1;margin:10px 0 0;max-width:60ch}.hero-stats{display:flex;gap:18px;flex-wrap:wrap}.hero-stat{min-width:88px;text-align:center;padding:12px;border:1px solid rgba(255,255,255,.2);border-radius:12px;background:rgba(255,255,255,.08)}.hero-stat strong{display:block;font-size:1.55rem}.hero-stat span{font-size:.78rem;color:#DCEAF1}
.progress-track{height:10px;background:#DCE7ED;border-radius:99px;overflow:hidden}.progress-fill{height:100%;width:0;background:linear-gradient(90deg,#168078,#49B98C);transition:width .25s ease}.dashboard{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:18px 0}.panel{background:white;border:1px solid var(--border);border-radius:14px;padding:16px 18px}.panel-head{display:flex;justify-content:space-between;gap:12px;align-items:baseline;margin-bottom:10px}.panel h2{font-size:1rem;margin:0;color:var(--navy)}.panel strong{color:var(--blue)}.panel p{margin:8px 0 0;color:var(--muted);font-size:.9rem}
.toolbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:18px 0;padding:14px;background:white;border:1px solid var(--border);border-radius:14px}.toolbar button,.file-button{border:1px solid var(--border);border-radius:9px;background:white;color:var(--navy);padding:9px 12px;font-weight:700}.toolbar button.primary{background:var(--blue);border-color:var(--blue);color:white}.toolbar button:hover,.file-button:hover{filter:brightness(.97)}.toolbar label{font-size:.85rem;color:var(--muted);font-weight:650}.toolbar input[type=time]{padding:7px;border:1px solid var(--border);border-radius:8px;color:var(--ink)}.file-button input{position:absolute;width:1px;height:1px;opacity:0}.status{flex:1 1 260px;min-width:220px;color:var(--muted);font-size:.84rem}.notice{padding:13px 16px;background:#EAF5F7;border-left:4px solid #168078;border-radius:8px;color:#214B4D;font-size:.9rem;margin:16px 0 22px}.notice strong{color:#0C5B55}
.stage{background:white;border:1px solid var(--border);border-radius:15px;margin:14px 0;overflow:hidden;box-shadow:0 3px 12px rgba(11,61,92,.035)}.stage summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px;padding:17px 20px}.stage summary::-webkit-details-marker{display:none}.stage summary:after{content:"＋";margin-left:auto;color:var(--blue);font-weight:800}.stage[open] summary:after{content:"−"}.stage-num{flex:0 0 36px;width:36px;height:36px;display:grid;place-items:center;border-radius:50%;background:#E8F1F6;color:var(--navy);font-weight:800}.stage-heading{min-width:0;flex:1}.stage-heading strong{display:block;color:var(--navy);font-size:1.04rem}.stage-heading small{display:block;color:var(--muted);margin-top:2px}.stage-meter{min-width:70px;text-align:right;color:var(--blue);font-weight:750;font-size:.84rem}.stage-body{padding:0 20px 20px}.stage-description{margin:0 0 10px;color:#354E5C}.outcomes{margin:8px 0 16px;padding-left:22px;color:var(--muted);font-size:.91rem}.resource-list{display:grid;gap:10px}.resource{padding:14px 15px;border:1px solid var(--border);border-radius:11px;background:#FCFDFE}.resource.done{border-color:#A8D8C7;background:#F4FBF7}.resource-top{display:flex;justify-content:space-between;align-items:flex-start;gap:14px}.resource h3{margin:0;color:var(--navy);font-size:1rem}.resource-meta{display:flex;gap:6px;flex-wrap:wrap;margin:7px 0}.tag{display:inline-block;border-radius:999px;background:#EAF1F5;color:#3B5968;padding:3px 8px;font-size:.74rem;font-weight:700}.tag.cost{background:#E8F5EE;color:#176644}.tag.paid{background:#FFF2DF;color:#86500D}.resource p{margin:6px 0;color:#425B69;font-size:.91rem}.resource a{color:var(--blue);font-weight:700;overflow-wrap:anywhere}.completion{display:flex;gap:8px;align-items:center;white-space:nowrap;color:#23674D;font-weight:700;font-size:.85rem}.completion input{width:18px;height:18px;accent-color:var(--green)}.stage-empty{padding:12px;background:var(--pale);border-radius:9px}.app-footer{text-align:center;color:var(--muted);font-size:.82rem;padding:26px 0 0}
@media(max-width:720px){.hero{align-items:flex-start;flex-direction:column}.hero-stats{width:100%}.hero-stat{flex:1}.dashboard{grid-template-columns:1fr}.stage summary{padding:14px}.stage-body{padding:0 14px 15px}.stage-meter{display:none}.toolbar{align-items:flex-start}.status{flex-basis:100%}.resource-top{flex-direction:column}.completion{white-space:normal}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition:none!important}}
</style>
</head>
<body>
<div class="app">
<header class="hero">
  <div><p class="eyebrow">YOUR LEARNING ROADMAP</p><h1 id="title"></h1><p id="subtitle"></p></div>
  <div class="hero-stats" aria-label="Learning stats"><div class="hero-stat"><strong id="overall-percent">0%</strong><span>complete</span></div><div class="hero-stat"><strong id="streak-count">0</strong><span>day streak</span></div></div>
</header>
<section class="dashboard" aria-label="Progress overview">
  <div class="panel"><div class="panel-head"><h2>Overall roadmap</h2><strong id="progress-label">0 of 0 complete</strong></div><div class="progress-track" role="progressbar" aria-label="Overall roadmap progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-fill" id="progress-fill"></div></div><p id="next-step">Start with the first item in the roadmap.</p></div>
  <div class="panel"><div class="panel-head"><h2>Today's check-in</h2><strong id="today-status">Not logged yet</strong></div><p id="reminder-summary">Complete one learning task today to record activity toward your streak.</p></div>
</section>
<div class="toolbar" aria-label="Reminder and progress controls">
  <button class="primary" id="enable-notifications" type="button">Enable browser reminders</button>
  <label for="reminder-time">Reminder time</label><input id="reminder-time" type="time" value="19:00">
  <span class="status" id="notification-status" role="status" aria-live="polite">Browser reminders require permission and this page to remain open.</span>
  <button id="export-progress" type="button">Export progress</button>
  <label class="file-button" for="import-progress">Import progress<input id="import-progress" type="file" accept="application/json,.json"></label>
  <button id="reset-progress" type="button">Reset</button>
</div>
<div class="notice"><strong>Saved on this device.</strong> Progress stays in this browser's local storage, follows this device's local calendar for streaks, and does not sync across devices. Browser notifications are checked while this page is open; they cannot reliably alert you after it is closed. If notifications are unavailable or permission is denied, the in-app check-in still works.</div>
<main id="roadmap" aria-label="Roadmap stages"></main>
<footer class="app-footer">A self-contained roadmap tracker. Your progress is stored locally in this browser.</footer>
</div>
<script>
'use strict';
const DATA = __DATA_JSON__;
const STORAGE_KEY = 'rll-roadmap-progress-v1:' + (DATA.storage_id || DATA.title || 'roadmap').toLowerCase().replace(/[^a-z0-9]+/g,'-');
const RESOURCE_ITEMS = [];
let state = loadState();

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
}
function safeUrl(value) {
  try { const u = new URL(value); return (u.protocol === 'https:' || u.protocol === 'http:') ? u.href : ''; }
  catch (_) { return ''; }
}
function localDateKey(date = new Date()) {
  const y = date.getFullYear(); const m = String(date.getMonth()+1).padStart(2,'0'); const d = String(date.getDate()).padStart(2,'0');
  return `${y}-${m}-${d}`;
}
function dateFromKey(key) { const [y,m,d] = key.split('-').map(Number); return new Date(y,m-1,d,12,0,0,0); }
function previousDay(key) { const d = dateFromKey(key); d.setDate(d.getDate()-1); return localDateKey(d); }
function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    return { done: saved.done && typeof saved.done === 'object' ? saved.done : {}, activityDates: Array.isArray(saved.activityDates) ? saved.activityDates.filter(x => /^\d{4}-\d{2}-\d{2}$/.test(x)) : [], reminderTime: /^\d\d:\d\d$/.test(saved.reminderTime || '') ? saved.reminderTime : (DATA.reminder_time || '19:00'), notificationsEnabled: saved.notificationsEnabled === true, lastNotificationDate: saved.lastNotificationDate || '' };
  } catch (_) { return {done:{},activityDates:[],reminderTime:DATA.reminder_time||'19:00',notificationsEnabled:false,lastNotificationDate:''}; }
}
function saveState() { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) { setNotice('Could not save to browser storage. Export progress or try another browser.'); } }
function setNotice(message) { document.getElementById('notification-status').textContent = message; }
function markActivity() { const today = localDateKey(); if (!state.activityDates.includes(today)) state.activityDates.push(today); }
function streakLength() {
  const dates = new Set(state.activityDates); const today = localDateKey();
  let cursor = dates.has(today) ? today : previousDay(today); let length = 0;
  while (dates.has(cursor)) { length++; cursor = previousDay(cursor); }
  return length;
}
function resourceKey(stageIndex, resourceIndex) { return `s${stageIndex}-r${resourceIndex}`; }
function stageKey(stageIndex) { return `s${stageIndex}-complete`; }
function buildRoadmap() {
  const root = document.getElementById('roadmap');
  root.replaceChildren();
  RESOURCE_ITEMS.length = 0;
  const stages = Array.isArray(DATA.stages) ? DATA.stages : [];
  stages.forEach((stage, stageIndex) => {
    const details = el('details', 'stage'); if (stageIndex === 0) details.open = true;
    details.dataset.stage = String(stageIndex);
    const summary = el('summary');
    summary.append(el('span','stage-num',String(stageIndex+1)));
    const heading = el('span','stage-heading');
    const stageTitle = el('strong','',stage.title || `Stage ${stageIndex+1}`); heading.append(stageTitle);
    const sub = [stage.duration, stage.estimated_hours ? `${stage.estimated_hours} hours` : ''].filter(Boolean).join(' · ');
    if (sub) heading.append(el('small','',sub));
    summary.append(heading);
    const meter = el('span','stage-meter','0%'); meter.dataset.meter = String(stageIndex); summary.append(meter);
    details.append(summary);
    const body = el('div','stage-body');
    if (stage.description) body.append(el('p','stage-description',stage.description));
    if (Array.isArray(stage.outcomes) && stage.outcomes.length) {
      const list = el('ul','outcomes'); stage.outcomes.forEach(item => list.append(el('li','',item))); body.append(list);
    }
    const resources = Array.isArray(stage.resources) ? stage.resources : [];
    if (!resources.length) {
      const label = el('label','completion stage-empty');
      const checkbox = el('input'); checkbox.type = 'checkbox'; checkbox.checked = !!state.done[stageKey(stageIndex)];
      checkbox.addEventListener('change', () => { if (checkbox.checked) { state.done[stageKey(stageIndex)] = true; markActivity(); } else delete state.done[stageKey(stageIndex)]; saveState(); updateDashboard(); updateStageMeters(); });
      label.append(checkbox, document.createTextNode(' Mark this stage complete'));
      body.append(label);
    } else {
      const list = el('div','resource-list');
      resources.forEach((resource, resourceIndex) => {
        const key = resourceKey(stageIndex,resourceIndex); RESOURCE_ITEMS.push({key, title:resource.title || 'Learning resource', stageIndex, resourceIndex});
        const card = el('article','resource' + (state.done[key] ? ' done' : ''));
        const top = el('div','resource-top');
        const content = el('div'); content.append(el('h3','',resource.title || 'Learning resource'));
        const tags = el('div','resource-meta');
        if (resource.provider) tags.append(el('span','tag',resource.provider));
        if (resource.modality || resource.type) tags.append(el('span','tag',resource.modality || resource.type));
        if (resource.cost) tags.append(el('span','tag ' + (/paid|\$|£|€|₦|NGN/i.test(resource.cost) ? 'paid' : 'cost'),resource.cost));
        if (resource.duration || resource.time) tags.append(el('span','tag',resource.duration || resource.time));
        if (resource.verification_date) tags.append(el('span','tag',`Checked ${resource.verification_date}`));
        content.append(tags);
        if (resource.why) content.append(el('p','',resource.why));
        if (resource.action) content.append(el('p','',`Next action: ${resource.action}`));
        if (resource.access_note || resource.verification_note) content.append(el('p','',resource.access_note || resource.verification_note));
        const url = safeUrl(resource.url || resource.link || '');
        if (url) { const link = el('a','',resource.link_label || 'Open resource'); link.href = url; link.target = '_blank'; link.rel = 'noopener noreferrer'; content.append(link); }
        top.append(content);
        const label = el('label','completion'); const checkbox = el('input'); checkbox.type = 'checkbox'; checkbox.checked = !!state.done[key]; checkbox.setAttribute('aria-label',`Mark ${resource.title || 'resource'} complete`);
        checkbox.addEventListener('change', () => { if (checkbox.checked) { state.done[key] = true; markActivity(); } else delete state.done[key]; saveState(); card.classList.toggle('done',checkbox.checked); updateDashboard(); updateStageMeters(); });
        label.append(checkbox,document.createTextNode('Done')); top.append(label); card.append(top); list.append(card);
      });
      body.append(list);
    }
    details.append(body); root.append(details);
  });
  updateDashboard(); updateStageMeters();
}
function allTrackableItems() {
  const items=[]; (DATA.stages||[]).forEach((stage,si)=>{ const resources=Array.isArray(stage.resources)?stage.resources:[]; if(resources.length) resources.forEach((_,ri)=>items.push(resourceKey(si,ri))); else items.push(stageKey(si)); }); return items;
}
function updateDashboard() {
  const items=allTrackableItems(); const done=items.filter(key=>!!state.done[key]).length; const pct=items.length?Math.round(done/items.length*100):0;
  document.getElementById('overall-percent').textContent=`${pct}%`; document.getElementById('progress-label').textContent=`${done} of ${items.length} complete`;
  const fill=document.getElementById('progress-fill'); fill.style.width=`${pct}%`; const bar=fill.parentElement; bar.setAttribute('aria-valuenow',String(pct));
  document.getElementById('streak-count').textContent=String(streakLength());
  const todayDone=state.activityDates.includes(localDateKey()); document.getElementById('today-status').textContent=todayDone?'Logged today':'Not logged yet';
  document.getElementById('reminder-summary').textContent=todayDone?'Nice work — today’s learning activity is recorded.':`Complete a resource before or after ${state.reminderTime} to record today’s activity.`;
  const next=RESOURCE_ITEMS.find(item=>!state.done[item.key]); document.getElementById('next-step').textContent=next?`Next up: ${next.title}`:(items.length?'You completed every roadmap item. Keep revisiting or add another goal.':'Add roadmap resources to start tracking.');
}
function updateStageMeters() {
  (DATA.stages||[]).forEach((stage,si)=>{ const resources=Array.isArray(stage.resources)?stage.resources:[]; const keys=resources.length?resources.map((_,ri)=>resourceKey(si,ri)):[stageKey(si)]; const done=keys.filter(key=>!!state.done[key]).length; const meter=document.querySelector(`[data-meter="${si}"]`); if(meter) meter.textContent=`${keys.length?Math.round(done/keys.length*100):0}%`; });
}
function setupReminderControls() {
  const time=document.getElementById('reminder-time'); time.value=state.reminderTime;
  time.addEventListener('change',()=>{state.reminderTime=time.value||'19:00';saveState();updateDashboard();setNotice(`Reminder time saved as ${state.reminderTime}. Keep the page open for browser alerts.`);});
  document.getElementById('enable-notifications').addEventListener('click',async()=>{
    if (!('Notification' in window)) { setNotice('This browser does not support system notifications. The in-app reminder remains available.'); return; }
    if (!window.isSecureContext) { setNotice('Browser notifications need a secure HTTPS page or localhost. The in-app reminder remains available.'); return; }
    try { const permission=await Notification.requestPermission(); state.notificationsEnabled=permission==='granted'; saveState();
      if(permission==='granted') { setNotice('Browser reminders are enabled while this page stays open. They will not run after the app is closed.'); checkReminder(); }
      else setNotice(`Notification permission ${permission}. The in-app reminder remains available.`);
    } catch (_) { setNotice('Could not request notification permission. The in-app reminder remains available.'); }
  });
  document.getElementById('export-progress').addEventListener('click',()=>{
    const blob=new Blob([JSON.stringify({version:1,title:DATA.title,done:state.done,activityDates:state.activityDates,reminderTime:state.reminderTime},null,2)],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='learning-roadmap-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
  });
  document.getElementById('import-progress').addEventListener('change',async(event)=>{
    const file=event.target.files && event.target.files[0]; if(!file) return;
    try { const incoming=JSON.parse(await file.text()); if(!incoming || typeof incoming.done!=='object' || !Array.isArray(incoming.activityDates)) throw new Error('format');
      state.done=incoming.done;state.activityDates=incoming.activityDates.filter(x=>/^\d{4}-\d{2}-\d{2}$/.test(x));if(/^\d\d:\d\d$/.test(incoming.reminderTime||''))state.reminderTime=incoming.reminderTime;saveState();buildRoadmap();time.value=state.reminderTime;setNotice('Progress imported.');
    } catch (_) { setNotice('That file could not be read as roadmap progress JSON.'); } event.target.value='';
  });
  document.getElementById('reset-progress').addEventListener('click',()=>{ if(!window.confirm('Clear progress and streak history saved in this browser?')) return; state={done:{},activityDates:[],reminderTime:DATA.reminder_time||'19:00',notificationsEnabled:false,lastNotificationDate:''};saveState();buildRoadmap();time.value=state.reminderTime;setNotice('Progress reset on this device.'); });
}
function checkReminder() {
  if (!state.notificationsEnabled || !('Notification' in window) || Notification.permission!=='granted') return;
  const now=new Date(); const current=`${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`; const today=localDateKey();
  if(current>=state.reminderTime && state.lastNotificationDate!==today && !state.activityDates.includes(today)) {
    try { const notification=new Notification(DATA.title||'Learning roadmap',{body:'Take a few minutes to continue your learning roadmap and protect your daily streak.'}); notification.onclick=()=>{window.focus();notification.close();}; state.lastNotificationDate=today; saveState(); }
    catch (_) { setNotice('A browser reminder could not be shown. The in-app check-in remains available.'); }
  }
}
document.getElementById('title').textContent=DATA.title||'Learning roadmap';
document.getElementById('subtitle').textContent=DATA.subtitle||'Work through the roadmap in order, one step at a time.';
buildRoadmap(); setupReminderControls();
if (state.notificationsEnabled && 'Notification' in window && Notification.permission==='granted') setNotice('Browser reminders are enabled while this page stays open.');
checkReminder(); setInterval(checkReminder,60000); document.addEventListener('visibilitychange',()=>{if(!document.hidden)checkReminder();});
</script>
</body>
</html>
'''


def _normalise(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    title = str(data.get("title") or data.get("topic") or "Learning roadmap").strip()
    raw_stages = data.get("stages", data.get("roadmap", []))
    if not isinstance(raw_stages, list):
        raise ValueError("'stages' (or 'roadmap') must be a list")
    stages: list[dict[str, Any]] = []
    for index, raw_stage in enumerate(raw_stages, start=1):
        if not isinstance(raw_stage, dict):
            raise ValueError(f"stage {index} must be a JSON object")
        stage = {
            "title": str(raw_stage.get("title") or raw_stage.get("name") or f"Stage {index}"),
            "description": str(raw_stage.get("description") or ""),
            "duration": str(raw_stage.get("duration") or ""),
            "estimated_hours": raw_stage.get("estimated_hours", ""),
            "outcomes": raw_stage.get("outcomes") if isinstance(raw_stage.get("outcomes"), list) else [],
            "resources": [],
        }
        raw_resources = raw_stage.get("resources", [])
        if not isinstance(raw_resources, list):
            raise ValueError(f"stage {index} 'resources' must be a list")
        for r_index, raw_resource in enumerate(raw_resources, start=1):
            if not isinstance(raw_resource, dict):
                raise ValueError(f"resource {r_index} in stage {index} must be a JSON object")
            resource = {
                "title": str(raw_resource.get("title") or f"Resource {r_index}"),
                "provider": str(raw_resource.get("provider") or ""),
                "url": str(raw_resource.get("url") or raw_resource.get("link") or ""),
                "modality": str(raw_resource.get("modality") or raw_resource.get("type") or ""),
                "cost": str(raw_resource.get("cost") or ""),
                "duration": str(raw_resource.get("duration") or raw_resource.get("time") or ""),
                "why": str(raw_resource.get("why") or ""),
                "action": str(raw_resource.get("action") or ""),
                "access_note": str(raw_resource.get("access_note") or raw_resource.get("verification_note") or ""),
                "verification_date": str(raw_resource.get("verification_date") or ""),
                "link_label": str(raw_resource.get("link_label") or "Open resource"),
            }
            if resource["url"]:
                parts = urlsplit(resource["url"])
                if parts.scheme not in {"http", "https"} or not parts.netloc:
                    raise ValueError(f"resource URL must be http(s): {resource['url']}")
            stage["resources"].append(resource)
        stages.append(stage)
    reminder_time = str(data.get("reminder_time") or "19:00")
    if not re.fullmatch(r"\d{2}:\d{2}", reminder_time):
        raise ValueError("'reminder_time' must use 24-hour HH:MM format")
    hours, minutes = map(int, reminder_time.split(":"))
    if hours > 23 or minutes > 59:
        raise ValueError("'reminder_time' is not a valid clock time")
    return {
        "title": title,
        "subtitle": str(data.get("subtitle") or "Work through the roadmap in order, one step at a time."),
        "reminder_time": reminder_time,
        "storage_id": str(data.get("storage_id") or title),
        "stages": stages,
    }


def build_app(data: dict[str, Any], output_path: str | Path) -> Path:
    normalized = _normalise(data)
    serialized = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))
    # Prevent user-provided text from terminating the inline script element.
    serialized = serialized.replace("<", r"\u003c").replace(">", r"\u003e").replace("&", r"\u0026")
    serialized = serialized.replace("\u2028", r"\u2028").replace("\u2029", r"\u2029")
    document = APP_TEMPLATE.replace("__DATA_JSON__", serialized)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON roadmap/resource data")
    parser.add_argument("--output", required=True, help="path for the generated single-file HTML app")
    args = parser.parse_args(argv)
    source = Path(args.input)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
        output = build_app(data, args.output)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {output}")
    print("Note: progress is stored in this browser; notifications require permission and the page to remain open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
