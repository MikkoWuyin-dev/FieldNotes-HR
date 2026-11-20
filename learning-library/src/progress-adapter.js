// Preserve the existing payload before the first version-3 write.
// Resource identities, aliases and the storage ID stay unchanged.
function preserveProgressUpgradeSnapshot() {
  const before=localStorage.getItem(STORAGE_KEY);
  if(!before) return;
  if(!localStorage.getItem(STORAGE_KEY+':before-progress-v3'))
    localStorage.setItem(STORAGE_KEY+':before-progress-v3',before);
}
// Local extension: resource identities and backup validation, independent of order.
function progressAliases() { return __PROGRESS_ALIASES__; }
function progressDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(value + 'T12:00:00Z');
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0,10) === value;
}
function progressTime(value) { return typeof value === 'string' && /^(?:[01]\d|2[0-3]):[0-5]\d$/.test(value); }
function normalizeProgress(value, imported = false) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('format');
  if (imported && value.version !== undefined && ![1,2,3].includes(value.version)) throw new Error('version');
  if (value.storage_id !== undefined && value.storage_id !== DATA.storage_id) throw new Error('roadmap');
  if (imported && (!value.done || typeof value.done !== 'object' || Array.isArray(value.done) || !Array.isArray(value.activityDates))) throw new Error('format');
  const input = value.done && typeof value.done === 'object' && !Array.isArray(value.done) ? value.done : {};
  const aliases = progressAliases(); const done = Object.create(null);
  for (const [key, checked] of Object.entries(input)) {
    if (typeof checked !== 'boolean') { if (imported) throw new Error('completion type'); else continue; }
    if (['__proto__','constructor','prototype'].includes(key)) continue;
    // Canonical entries, including explicit false, take precedence over aliases.
    const target = Object.prototype.hasOwnProperty.call(aliases,key) ? aliases[key] : key;
    if (target !== key && Object.prototype.hasOwnProperty.call(input,target)) continue;
    done[target] = checked;
  }
  const booleanMap = key => {
    const input=value[key]; const result=Object.create(null);
    if(input === undefined) return result; // earlier check-in-only version 3 files
    if(!input || typeof input!=='object' || Array.isArray(input)) throw new Error('milestone format');
    for(const [id,checked] of Object.entries(input)) {
      if(['__proto__','constructor','prototype'].includes(id)) continue;
      if(typeof checked!=='boolean') throw new Error('milestone type');
      result[id]=checked;
    }
    return result;
  };
  const milestones=booleanMap('milestones'), detailed=booleanMap('detailed');
  const dates = key => [...new Set((Array.isArray(value[key])?value[key]:[]).filter(progressDate))];
  if (imported && value.version === 3) {
    if (value.storage_id !== DATA.storage_id || !Array.isArray(value.manualCheckinDates) || !Array.isArray(value.legacyActivityDates)) throw new Error('check-in format');
    if (![...value.manualCheckinDates,...value.legacyActivityDates].every(progressDate)) throw new Error('check-in date');
  }
  // A version 3 file must supply provenance. Older dates remain legacy activity.
  const manualCheckinDates = value.version === 3 ? dates('manualCheckinDates') : [];
  const legacyActivityDates = value.version === 3 ? dates('legacyActivityDates') : dates('activityDates');
  return {version:3, storage_id:DATA.storage_id, done, milestones, detailed,
    manualCheckinDates, legacyActivityDates,
    activityDates:[...new Set([...legacyActivityDates,...manualCheckinDates])],
    reminderTime:progressTime(value.reminderTime)?value.reminderTime:(DATA.reminder_time||'19:00'),
    notificationsEnabled:!imported && value.notificationsEnabled===true,
    lastNotificationDate:progressDate(value.lastNotificationDate)?value.lastNotificationDate:''};
}
function loadState() {
  try { return normalizeProgress(JSON.parse(localStorage.getItem(STORAGE_KEY)||'{}')); }
  catch (_) { return normalizeProgress({}); }
}

// Explicit attendance is separate from resource completion. No timers award credit.
function renderDailyCheckin() {
  const today = localDateKey();
  const manual = state.manualCheckinDates.includes(today);
  const logged = state.activityDates.includes(today);
  document.getElementById('today-status').textContent = logged ? 'Checked in today' : 'Not checked in yet';
  document.getElementById('reminder-summary').textContent = logged
    ? 'Today’s study is recorded. Your roadmap progress is separate.'
    : 'A little learning counts. You do not need to finish a lesson.';
  const button = document.getElementById('daily-checkin');
  if (button) { button.disabled = logged; button.textContent = logged ? 'Checked in today' : 'I studied today'; }
  const undo = document.getElementById('undo-checkin');
  if (undo) undo.hidden = !manual;
}
function changeDailyCheckin(undo = false) {
  const today = localDateKey();
  const candidate = normalizeProgress({...state,
    manualCheckinDates: undo ? state.manualCheckinDates.filter(date => date !== today)
      : [...new Set([...state.manualCheckinDates,today])]
  });
  // Write before replacing in-memory state: storage failures must not claim success.
  try {
    preserveProgressUpgradeSnapshot();
    const old = localStorage.getItem(STORAGE_KEY);
    if (old && !localStorage.getItem(STORAGE_KEY + ':before-checkins-v3')) {
      localStorage.setItem(STORAGE_KEY + ':before-checkins-v3',old);
    }
    localStorage.setItem(STORAGE_KEY,JSON.stringify(candidate));
  } catch (_) { setNotice('Could not save your check-in. Existing progress was not replaced. Export a backup and retry.'); return false; }
  state = candidate;
  updateDashboard();
  setNotice(undo ? 'Today’s manual check-in removed. Previous activity is preserved.' : 'Checked in for today. Roadmap progress is unchanged.');
  return true;
}
function setupDailyCheckin() {
  const panel = document.getElementById('today-status').closest('.panel');
  const controls = el('div','daily-checkin-controls');
  const button = el('button','','I studied today'); button.type='button'; button.id='daily-checkin';
  const undo = el('button','','Undo today’s check-in'); undo.type='button'; undo.id='undo-checkin'; undo.hidden=true;
  controls.append(button,undo); panel.append(controls);
  button.addEventListener('click',()=>changeDailyCheckin());
  undo.addEventListener('click',()=>changeDailyCheckin(true));
  const refresh = () => { if (document.visibilityState !== 'hidden') updateDashboard(); };
  window.addEventListener('focus',refresh);
  document.addEventListener('visibilitychange',refresh);
  setInterval(refresh,30000);
  renderDailyCheckin();
}
