/* FieldNotes-HR decorative pals controller.
 *
 * Source file — injected into out/roadmap-app.html by tools/build_tracker.py.
 * The engine itself lives, inert, in piixpal-payload.html and is only executed
 * on idle. Nothing here talks to a network; the pals are optional decoration.
 *
 * Rules carried over from the reference project:
 *  - PALS_COUNT is derived from the list, never hard-coded.
 *  - Pals default to OFF under prefers-reduced-motion: reduce.
 *  - Targets are prose, never controls (see pals.json); a pal canvas has
 *    pointer-events:auto and would swallow a tap on a button or link.
 *  - The generator rebuilds the stage list on reset/import, so pals are
 *    re-anchored to the new nodes via a childList MutationObserver.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'fieldnotes-hr-pals-v1';
  var reducedMotion = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : { matches: false };

  /* Injected by the build layer from pals.json. */
  var SITE_PALS = __SITE_PALS_JSON__;
  var PALS_COUNT = SITE_PALS.length;

  function byId(id) { return document.getElementById(id); }

  function readPreference() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'on') return true;
      if (saved === 'off') return false;
    } catch (_) { /* storage may be blocked */ }
    return !reducedMotion.matches;
  }

  /* The OS reduced-motion preference wins over any stale saved 'on' value.
   * A visitor can still opt in explicitly with the toggle. */
  var palsEnabled = readPreference() && !reducedMotion.matches;
  var payloadLoaded = false;

  function engineReady() {
    return !!(window.Piixpal && typeof window.Piixpal.add === 'function');
  }

  function loadPayload() {
    if (payloadLoaded) return engineReady();
    payloadLoaded = true;
    var tpl = byId('pals-payload');
    if (!tpl || !tpl.content) return false;
    Array.prototype.forEach.call(tpl.content.querySelectorAll('script'), function (source) {
      var script = document.createElement('script');
      script.textContent = source.textContent;
      document.body.appendChild(script);
    });
    return engineReady();
  }

  function clearPals() {
    document.querySelectorAll('piix-pal[data-fieldnotes-pal]').forEach(function (pal) {
      pal.remove();
    });
  }

  function renderPals() {
    clearPals();
    if (!palsEnabled || !engineReady()) return;
    SITE_PALS.forEach(function (spec) {
      var options = { at: spec.at === undefined ? 0.88 : spec.at };
      if (spec.edge) options.edge = spec.edge;
      if (spec.speed) options.speed = spec.speed;
      if (spec.hue !== undefined) options.hue = spec.hue;
      if (spec.scale) options.scale = spec.scale;
      try {
        var pal = window.Piixpal.add(spec.pal, spec.target, options);
        if (pal) {
          pal.setAttribute('data-fieldnotes-pal', 'site');
          pal.setAttribute('aria-hidden', 'true');
        }
      } catch (_) { /* decoration must never break the tracker */ }
    });
  }

  function showPals() {
    if (!palsEnabled) return;
    if (!loadPayload()) return;
    renderPals();
  }

  function schedulePals() {
    if (typeof window.requestIdleCallback === 'function') {
      window.requestIdleCallback(showPals, { timeout: 2000 });
    } else {
      window.setTimeout(showPals, 1200);
    }
  }

  function updateControl() {
    var toggle = byId('pals-toggle');
    if (!toggle) return;
    toggle.setAttribute('aria-pressed', String(palsEnabled));
    toggle.textContent = palsEnabled ? 'Pause tiny pals' : 'Enable tiny pals';
    var status = byId('pals-status');
    if (status) {
      status.textContent = palsEnabled
        ? PALS_COUNT + ' optional decorative pals are on; the roadmap works without them.'
        : reducedMotion.matches
          ? 'Pals are paused; your reduced-motion preference is respected.'
          : 'Pals are paused. Your roadmap and progress still work normally.';
    }
  }

  function setup() {
    var controls = byId('pals-controls');
    if (controls) controls.hidden = false;

    var toggle = byId('pals-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        palsEnabled = !palsEnabled;
        try { localStorage.setItem(STORAGE_KEY, palsEnabled ? 'on' : 'off'); } catch (_) {}
        if (palsEnabled) showPals(); else clearPals();
        updateControl();
      });
    }

    updateControl();
    if (palsEnabled) schedulePals();

    /* The tracker's generator calls replaceChildren() on #roadmap when progress
     * is reset or imported. Without this, pals keep pointing at detached stage
     * headings and quietly drift away. */
    var roadmap = byId('roadmap');
    if (roadmap && window.MutationObserver) {
      var queued = false;
      new MutationObserver(function () {
        if (!palsEnabled || queued) return;
        queued = true;
        window.requestAnimationFrame(function () {
          queued = false;
          renderPals();
        });
      }).observe(roadmap, { childList: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup, { once: true });
  } else {
    setup();
  }
})();
