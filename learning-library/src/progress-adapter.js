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
  if (imported && value.version !== undefined && ![1,2].includes(value.version)) throw new Error('version');
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
  return {version:2, storage_id:DATA.storage_id, done,
    activityDates:[...new Set((Array.isArray(value.activityDates)?value.activityDates:[]).filter(progressDate))],
    reminderTime:progressTime(value.reminderTime)?value.reminderTime:(DATA.reminder_time||'19:00'),
    notificationsEnabled:!imported && value.notificationsEnabled===true,
    lastNotificationDate:progressDate(value.lastNotificationDate)?value.lastNotificationDate:''};
}
function loadState() {
  try { return normalizeProgress(JSON.parse(localStorage.getItem(STORAGE_KEY)||'{}')); }
  catch (_) { return normalizeProgress({}); }
}
