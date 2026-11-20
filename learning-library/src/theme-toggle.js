/* Theme preference for the self-contained FieldNotes tracker. */
(function () {
  'use strict';

  var STORAGE_KEY = 'fieldnotes-hr-theme-v1';
  var root = document.documentElement;
  var media = typeof window.matchMedia === 'function'
    ? window.matchMedia('(prefers-color-scheme: dark)')
    : null;

  function readPreference() {
    try {
      var saved = window.localStorage.getItem(STORAGE_KEY);
      return saved === 'light' || saved === 'dark' ? saved : null;
    } catch (_) {
      return null;
    }
  }

  var preference = readPreference();
  var effectiveTheme = preference || (media && media.matches ? 'dark' : 'light');
  var preferenceSaved = preference !== null;

  function updateButton() {
    var button = document.getElementById('theme-toggle');
    if (!button) return;
    button.setAttribute('aria-pressed', String(effectiveTheme === 'dark'));
    button.setAttribute('aria-label', 'Toggle color theme');
    button.setAttribute('data-theme-icon', effectiveTheme === 'dark' ? 'moon' : 'sun');
    button.title = preference
      ? preferenceSaved
        ? 'Saved as ' + preference + ' theme in this browser.'
        : 'Theme choice applies until this page closes; browser storage is unavailable.'
      : 'Following your system setting (' + effectiveTheme + '). Click to save a choice.';
  }

  function applyTheme(theme) {
    effectiveTheme = theme;
    root.setAttribute('data-theme', theme);
    root.setAttribute('data-theme-source', preference ? 'user' : 'system');
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#0B0D16' : '#11142B');
    updateButton();
  }

  function setupToggle() {
    var button = document.getElementById('theme-toggle');
    if (!button) return;
    updateButton();
    button.addEventListener('click', function () {
      preference = effectiveTheme === 'dark' ? 'light' : 'dark';
      try {
        window.localStorage.setItem(STORAGE_KEY, preference);
        preferenceSaved = true;
      } catch (_) {
        preferenceSaved = false;
      }
      applyTheme(preference);
    });
  }

  function followSystem(event) {
    if (preference) return;
    applyTheme(event.matches ? 'dark' : 'light');
  }

  // Apply the stored choice or system default before the page's theme CSS loads.
  applyTheme(effectiveTheme);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupToggle, { once: true });
  } else {
    setupToggle();
  }

  if (media) {
    if (typeof media.addEventListener === 'function') media.addEventListener('change', followSystem);
    else if (typeof media.addListener === 'function') media.addListener(followSystem);
  }
})();
