/* Fixed scroll-to-top control for the self-contained FieldNotes tracker. */
(function () {
  'use strict';

  var button = document.getElementById('back-to-top');
  if (!button) return;

  var SHOW_AFTER = 160;
  var IDLE_DELAY = 3000;
  var idleTimer = 0;

  function clearIdleTimer() {
    if (idleTimer) window.clearTimeout(idleTimer);
    idleTimer = 0;
  }

  function hideAfterIdle() {
    idleTimer = 0;
    if (window.scrollY <= SHOW_AFTER && document.activeElement !== button) {
      button.hidden = true;
      return;
    }
    if (document.activeElement === button || button.matches(':hover')) {
      idleTimer = window.setTimeout(hideAfterIdle, IDLE_DELAY);
      return;
    }
    button.hidden = true;
  }

  function updateVisibility() {
    clearIdleTimer();
    if (window.scrollY <= SHOW_AFTER) {
      button.hidden = document.activeElement !== button;
      return;
    }
    button.hidden = false;
    idleTimer = window.setTimeout(hideAfterIdle, IDLE_DELAY);
  }

  button.addEventListener('click', function (event) {
    // Pointer clicks do not need to leave focus on a control that will hide
    // when the page reaches the top. Keep keyboard focus visible until blur.
    if (event.detail > 0) button.blur();
    var reducedMotion = typeof window.matchMedia === 'function'
      && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
  });

  button.addEventListener('focus', clearIdleTimer);
  button.addEventListener('blur', updateVisibility);
  button.addEventListener('mouseenter', clearIdleTimer);
  button.addEventListener('mouseleave', updateVisibility);
  window.addEventListener('scroll', updateVisibility, { passive: true });
  window.addEventListener('pageshow', updateVisibility);
  updateVisibility();
})();
