#!/usr/bin/env node
/**
 * Reproducible headless-browser checks for out/roadmap-app.html.
 *
 * Previously these checks lived in an uncommitted scratch directory and were
 * lost on every sandbox reset. Run with `make check-visual` from the repo root.
 *
 * Uses @sparticuz/chromium's bundled Chromium 153 + puppeteer-core. The AL2023
 * shared libraries are inflated explicitly because the package only does that
 * automatically on Amazon Linux; this makes the harness work on any runner.
 *
 * This is a real browser, but not a real phone: touch momentum, browser chrome
 * and device-specific storage behaviour are out of scope.
 */
import chromium, { inflate, setupLambdaEnvironment } from '@sparticuz/chromium';
import puppeteer from 'puppeteer-core';
import http from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..', '..');
const TARGET = join(REPO, 'learning-library', 'out', 'roadmap-app.html');
const REPORT_DIR = join(HERE, '.cache');
const WIDTHS = [320, 360, 390, 430, 600, 620, 700, 900, 1024, 1200, 1320, 1440, 1920];
const EXPECTED = {
  hero: 'rgb(55, 104, 255)',
  eyebrowInk: 'rgb(17, 20, 43)',
  eyebrowFill: 'rgb(255, 225, 104)',
  footer: 'Made with love and fried plantain, by Moyinoluwa',
  cards: 26,
  stages: 8,
};

if (!existsSync(TARGET)) {
  console.error(`Missing ${TARGET}. Run 'make build' first.`);
  process.exit(2);
}

const html = await readFile(TARGET, 'utf8');
const server = http.createServer((_req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(html);
});
await new Promise((ok) => server.listen(0, '127.0.0.1', ok));
const URL = `http://127.0.0.1:${server.address().port}/`;

const bin = join(HERE, 'node_modules', '@sparticuz', 'chromium', 'bin');
await inflate(join(bin, 'al2023.tar.br'));
setupLambdaEnvironment(join(tmpdir(), 'al2023', 'lib'));
const executablePath = await chromium.executablePath(bin);

let browser;
const runtimeErrors = [];
try {
  browser = await puppeteer.launch({
    args: [...chromium.args, '--no-sandbox'],
    executablePath,
    headless: 'shell',
  });
  const page = await browser.newPage();
  page.on('pageerror', (err) => runtimeErrors.push(`pageerror: ${err.message}`));
  page.on('console', (msg) => {
    if (msg.type() === 'error') runtimeErrors.push(`console.error: ${msg.text()}`);
  });
  page.on('dialog', (dialog) => dialog.accept());
  await page.goto(URL, { waitUntil: 'load' });

  const results = [];
  for (const width of WIDTHS) {
    await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
    const measured = await page.evaluate((expected) => {
      document.querySelectorAll('details.stage').forEach((d) => { d.open = true; });
      const failures = [];
      const rect = (el) => el.getBoundingClientRect();
      const overlaps = (a, b) => !(
        a.right <= b.left + 0.5 || b.right <= a.left + 0.5 ||
        a.bottom <= b.top + 0.5 || b.bottom <= a.top + 0.5
      );
      const px = (n) => Math.round(n * 10) / 10;

      // 1. No horizontal overflow, no clipped h1.
      const scrollW = document.documentElement.scrollWidth;
      if (scrollW > window.innerWidth + 1) {
        failures.push(`horizontal overflow: scrollWidth ${scrollW} > ${window.innerWidth}`);
      }
      const h1 = document.querySelector('.hero h1');
      if (!h1) failures.push('missing .hero h1');
      else if (h1.scrollWidth > h1.clientWidth + 1) {
        failures.push(`h1 clipped: scrollWidth ${h1.scrollWidth} > clientWidth ${h1.clientWidth}`);
      }

      // 2. Ported design tokens are actually applied.
      const hero = document.querySelector('.hero');
      if (!hero) failures.push('missing .hero');
      else if (getComputedStyle(hero).backgroundColor !== expected.hero) {
        failures.push(`hero background is ${getComputedStyle(hero).backgroundColor}`);
      }
      const eyebrow = document.querySelector('.eyebrow');
      if (eyebrow) {
        const cs = getComputedStyle(eyebrow);
        if (cs.color !== expected.eyebrowInk) failures.push(`eyebrow ink is ${cs.color}`);
        if (cs.backgroundColor !== expected.eyebrowFill) failures.push(`eyebrow fill is ${cs.backgroundColor}`);
      } else failures.push('missing .eyebrow');
      const footer = document.querySelector('.app-footer');
      if (!footer || !footer.textContent.includes(expected.footer)) {
        failures.push('footer credit text is wrong');
      }

      // 3. Every tag has its own fill; cost/paid keep their semantic colours.
      const tags = [...document.querySelectorAll('.resource-meta .tag')];
      const fills = new Set(tags.map((t) => getComputedStyle(t).backgroundColor));
      if (fills.size < 5) failures.push(`only ${fills.size} distinct tag fills`);

      // 4. All resources present, each link carries the decorative arrow.
      const links = [...document.querySelectorAll('.resource a')];
      if (links.length !== expected.cards) failures.push(`${links.length} resource links, expected ${expected.cards}`);
      const noArrow = links.filter((a) => getComputedStyle(a, '::after').content === 'none').length;
      if (noArrow) failures.push(`${noArrow} links missing the ↗ pseudo-element`);
      const stages = document.querySelectorAll('details.stage').length;
      if (stages !== expected.stages) failures.push(`${stages} stages, expected ${expected.stages}`);

      // 5. Link bottom-left, Done bottom-right, same row, no 2D overlap.
      let worstBottomDelta = 0;
      for (const card of document.querySelectorAll('.resource')) {
        const a = card.querySelector('a');
        const done = card.querySelector('.completion');
        if (!a || !done) { failures.push('resource card missing link or Done control'); continue; }
        const ra = rect(a);
        const rd = rect(done);
        worstBottomDelta = Math.max(worstBottomDelta, Math.abs(ra.bottom - rd.bottom));
        if (Math.abs(ra.bottom - rd.bottom) > 8) failures.push('link/Done not on one row');
        if (overlaps(ra, rd)) failures.push('link/Done rectangles overlap');
        if (ra.left > rd.left) failures.push('link is not left of Done');
      }

      // 6. Chips and both progress cards stay inside the hero and never overlap.
      const hr = rect(hero);
      const chips = [...document.querySelectorAll('.hero-facts span')];
      const stats = [...document.querySelectorAll('.hero-stat')];
      for (const el of [...chips, ...stats]) {
        const r = rect(el);
        if (r.left < hr.left - 1 || r.right > hr.right + 1 ||
            r.top < hr.top - 1 || r.bottom > hr.bottom + 1) {
          failures.push('a chip or progress card falls outside the hero');
        }
      }
      if (stats.length === 2 && overlaps(rect(stats[0]), rect(stats[1]))) {
        failures.push('the two progress cards overlap');
      }

      // 7. Tap targets and heading outline.
      const small = [...document.querySelectorAll('.toolbar button, .stage summary')]
        .filter((el) => rect(el).height < 44).length;
      if (small) failures.push(`${small} controls are under 44px tall`);
      const outline = ['h1', 'h2', 'h3'].map((s) => document.querySelectorAll(s).length);
      if (outline[0] !== 1 || outline[2] !== expected.cards) {
        failures.push(`heading outline h1/h2/h3 = ${outline.join('/')}`);
      }
      if (!document.querySelector('.skip-link')) failures.push('skip link missing');

      return {
        failures: [...new Set(failures)],
        scrollW,
        h1FontPx: h1 ? px(parseFloat(getComputedStyle(h1).fontSize)) : 0,
        tagFills: fills.size,
        worstBottomDelta: px(worstBottomDelta),
      };
    }, EXPECTED);
    results.push({ width, ...measured });
  }

  // 8. Functional checks at desktop width, on a clean localStorage.
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'load' });
  const before = await page.$eval('#progress-label', (el) => el.textContent.trim());
  await page.evaluate(() => {
    document.querySelector('.resource .completion input[type="checkbox"]').click();
  });
  const after = await page.evaluate(() => ({
    label: document.getElementById('progress-label').textContent.trim(),
    pct: document.getElementById('overall-percent').textContent.trim(),
    stored: Object.keys(localStorage).length > 0,
  }));
  const functional = [];
  if (!before.includes('0 of 26')) functional.push(`initial label unexpected: ${before}`);
  if (!after.label.includes('1 of 26')) functional.push(`after tick: ${after.label}`);
  if (after.pct !== '4%') functional.push(`after tick percent: ${after.pct}`);
  if (!after.stored) functional.push('progress was not written to localStorage');

  // Buttons should not throw. Dispatch in-page to avoid download/permission UI.
  await page.evaluate(() => {
    document.getElementById('export-progress').click();
    document.getElementById('enable-notifications').click();
  });
  await new Promise((r) => setTimeout(r, 250));

  await page.evaluate(() => document.getElementById('reset-progress').click());
  await new Promise((r) => setTimeout(r, 150));
  const reset = await page.$eval('#progress-label', (el) => el.textContent.trim());
  if (!reset.includes('0 of 26')) functional.push(`after reset: ${reset}`);

  // ---- report ------------------------------------------------------------
  console.log(`\nFieldNotes-HR visual check — Chromium ${await browser.version()}`);
  console.log('-'.repeat(78));
  console.log('width  overflow  h1(px)  tag fills  foot-row Δ(px)  result');
  for (const r of results) {
    const ok = r.failures.length === 0;
    console.log(
      `${String(r.width).padEnd(6)} ${String(r.scrollW).padEnd(9)} ` +
      `${String(r.h1FontPx).padEnd(7)} ${String(r.tagFills).padEnd(10)} ` +
      `${String(r.worstBottomDelta).padEnd(15)} ${ok ? 'PASS' : 'FAIL'}`
    );
    for (const f of r.failures) console.log(`         - ${f}`);
  }
  console.log('-'.repeat(78));
  const failedWidths = results.filter((r) => r.failures.length);
  console.log(`functional: ${functional.length ? 'FAIL' : 'PASS'}` +
              (functional.length ? ` — ${functional.join('; ')}` : ` (${before} → ${after.label} / ${after.pct} → ${reset})`));
  console.log(`runtime errors: ${runtimeErrors.length ? runtimeErrors.join('; ') : 'none'}`);
  const failures = failedWidths.length + functional.length + runtimeErrors.length;
  console.log(`RESULT: ${WIDTHS.length - failedWidths.length}/${WIDTHS.length} widths passed, ${failures} failure(s)`);

  await mkdir(REPORT_DIR, { recursive: true });
  await writeFile(join(REPORT_DIR, 'last-run.json'), JSON.stringify({
    generatedAt: new Date().toISOString(),
    chromium: await browser.version(),
    widths: results,
    functional,
    runtimeErrors,
  }, null, 2) + '\n');
  console.log(`Report: ${join(REPORT_DIR, 'last-run.json')}`);
  process.exitCode = failures ? 1 : 0;
} catch (err) {
  console.error('Visual check crashed:', err);
  process.exitCode = 2;
} finally {
  if (browser) await browser.close();
  await new Promise((ok) => server.close(ok));
}
