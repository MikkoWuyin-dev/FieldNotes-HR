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
 * Pal rules come from the reference project's browser suite: a pal canvas has
 * pointer-events:auto, so no pal may cover a control's centre and no pal may
 * overlap a control by more than 1100px². Pals are also expected to disappear
 * when paused and under prefers-reduced-motion: reduce.
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
const PAL_COUNT = 10;
const TOTAL_PAL_COUNT = 11;
const MAX_CONTROL_OVERLAP = 1100; // px², per the reference project's rule
const EXPECTED = {
  hero: 'rgb(55, 104, 255)',
  eyebrowInk: 'rgb(17, 20, 43)',
  eyebrowFill: 'rgb(255, 225, 104)',
  footer: 'Made with love and fried plantain, by Moyinoluwa',
  cards: 20,
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

function waitForPals(page, timeout = 15000) {
  return page.waitForFunction((count) => {
    const els = document.querySelectorAll('piix-pal[data-fieldnotes-pal]').length;
    const layer = document.querySelector('div[data-piixpal]');
    const actors = layer && layer.shadowRoot
      ? layer.shadowRoot.querySelectorAll('.a').length : 0;
    const spider = document.getElementById('fieldnotes-spider');
    return els === count && actors >= count && !!spider && !spider.hidden;
  }, { timeout }, PAL_COUNT);
}

function auditThemeContrast(page) {
  return page.evaluate(async () => {
    const stages=[...document.querySelectorAll('details.stage')];
    const openStates=stages.map(stage=>stage.open);
    stages.forEach(stage=>{stage.open=true;});
    await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(resolve,500))));
    const parseColor = (value) => {
      const match = String(value).match(/rgba?\(([^)]+)\)/i);
      if (!match) return null;
      const parts = match[1].trim().split(/[\s,\/]+/).filter(Boolean).map(Number);
      return {r:parts[0],g:parts[1],b:parts[2],a:parts.length>3?parts[3]:1};
    };
    const luminance = (color) => {
      const channel = (value) => {
        const c = value / 255;
        return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4;
      };
      return .2126*channel(color.r) + .7152*channel(color.g) + .0722*channel(color.b);
    };
    const contrast = (a,b) => {
      const light = Math.max(luminance(a),luminance(b));
      const dark = Math.min(luminance(a),luminance(b));
      return (light+.05)/(dark+.05);
    };
    const nearestOpaqueBackground = (element) => {
      for(let node=element;node && node.nodeType===1;node=node.parentElement) {
        const color=parseColor(getComputedStyle(node).backgroundColor);
        if(color && color.a>=.99) return color;
      }
      return null;
    };
    const isYellow = (color) => color && color.r>=190 && color.g>=140 &&
      color.r>=color.g && color.r-color.g<=55 && color.g-color.b>=30;
    const label = (element) => element.id ? '#'+element.id :
      '.'+String(element.className||element.tagName).toString().trim().replace(/\s+/g,'.');
    const yellowText = [...document.querySelectorAll('body *')]
      .filter(element=>element.textContent.trim() || element.getAttribute('aria-label'))
      .map(element=>{
        const bg=nearestOpaqueBackground(element);
        const fg=parseColor(getComputedStyle(element).color);
        return {element:label(element),background:bg,foreground:fg,
                ratio:bg&&fg?contrast(fg,bg):0};
      })
      .filter(item=>isYellow(item.background));
    const shadowElements=[...document.querySelectorAll(
      '.hero,.panel,.toolbar,.notice,.stage,.resource,.pals-controls,#theme-toggle,#back-to-top'
    )];
    const shadows=shadowElements.map(element=>{
      const value=getComputedStyle(element).boxShadow;
      const match=value.match(/rgba?\([^)]+\)/i);
      const color=match?parseColor(match[0]):null;
      const surface=nearestOpaqueBackground(element.parentElement);
      return {element:label(element),shadow:color,raw:value,
              elementShadowToken:getComputedStyle(element).getPropertyValue('--fn-shadow').trim(),
              hovered:element.matches(':hover'),surface,
              ratio:color&&surface?contrast(color,surface):0};
    }).filter(item=>item.shadow);
    const result={
      theme:document.documentElement.dataset.theme,
      shadowToken:getComputedStyle(document.documentElement).getPropertyValue('--fn-shadow').trim(),
      yellowText,
      yellowFailures:yellowText.filter(item=>item.ratio<4.5),
      shadows,
      shadowFailures:shadows.filter(item=>item.ratio<3),
      minYellowRatio:yellowText.length?Math.min(...yellowText.map(item=>item.ratio)):0,
      minShadowRatio:shadows.length?Math.min(...shadows.map(item=>item.ratio)):0,
    };
    stages.forEach((stage,index)=>{stage.open=openStates[index];});
    return result;
  });
}

let browser;
const runtimeErrors = [];
const themeFailures = [];
const contrastFailures = [];
const contrastAudits = [];
const scrollFailures = [];
const spiderFailures = [];
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
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await page.goto(URL, { waitUntil: 'load' });

  // Decode the actual favicon in Chromium, not just its source XML.
  const faviconResult = await page.evaluate(async () => {
    const icons = [...document.querySelectorAll('link[rel="icon"]')];
    if (icons.length !== 1) return {ok:false, count:icons.length};
    const image = new Image();
    const loaded = await new Promise(resolve => {
      image.onload = () => resolve(true);
      image.onerror = () => resolve(false);
      image.src = icons[0].href;
    });
    if (!loaded) return {ok:false,inline:true};
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 32;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(image,0,0,32,32);
    const pixels = [[1,1],[5,8],[5,15],[5,22]].map(([x,y]) =>
      Array.from(ctx.getImageData(x,y,1,1).data));
    const expected = [[17,20,43,255],[255,225,104,255],[101,232,255,255],[255,78,145,255]];
    return {ok:JSON.stringify(pixels) === JSON.stringify(expected), pixels,
            inline:icons[0].href.startsWith('data:image/svg+xml,')};
  });
  console.log('Inline favicon decode:',JSON.stringify(faviconResult));
  if (!faviconResult.ok || !faviconResult.inline) runtimeErrors.push('favicon did not render expected colours at 32px');

  // The engine is lazy-loaded on idle; wait for the pal elements AND their
  // actors (some behaviours spawn a small companion, so actors >= pals).
  let palsMounted = true;
  try {
    await waitForPals(page);
  } catch (_) {
    palsMounted = false;
  }

  // Scroll coupling regression: with RAF paused, compositor/native scrolling
  // must move every actor by exactly the same amount as its document target.
  await page.setViewport({width:390,height:900,deviceScaleFactor:1});
  const scrollRegression = await page.evaluate(() => {
    const layer = document.querySelector('div[data-piixpal]');
    const actors = [...layer.shadowRoot.querySelectorAll('.a')];
    cancelAnimationFrame(window.Piixpal._k.raf);
    // Measure in a single JS task, before the next engine frame can compensate.
    const before = actors.map(a => a.getBoundingClientRect().top);
    const y = scrollY;
    window.scrollTo({top:y + 240, behavior:'instant'});
    const delta = scrollY - y;
    const errors = actors.map((a,i) => Math.abs(a.getBoundingClientRect().top - before[i] + delta));
    window.scrollTo({top:y, behavior:'instant'});
    // Control experiment: the former fixed layer lags by the full scroll delta
    // until its engine frame updates the origin.
    layer.style.setProperty('position','fixed','important');
    const fixedBefore = actors.map(a => a.getBoundingClientRect().top);
    window.scrollTo({top:y+240,behavior:'instant'});
    const fixedError = Math.max(...actors.map((a,i) => Math.abs(a.getBoundingClientRect().top-fixedBefore[i]+240)));
    window.scrollTo({top:y,behavior:'instant'});
    layer.style.removeProperty('position');
    return {delta, maxError:Math.max(...errors), fixedError};
  });
  if (scrollRegression.delta === 0 || scrollRegression.maxError > 1 || scrollRegression.fixedError < 200) {
    runtimeErrors.push('scroll coupling failed: '+JSON.stringify(scrollRegression));
  }
  console.log('Native scroll coupling:', JSON.stringify(scrollRegression));
  await page.reload({waitUntil:'load'});
  await waitForPals(page);
  const spiderScroll=await page.evaluate(()=>{
    const spider=document.getElementById('fieldnotes-spider');
    const before=spider.getBoundingClientRect();
    const start=scrollY;
    const target=Math.min(600,document.documentElement.scrollHeight-innerHeight);
    window.scrollTo({top:target,behavior:'instant'});
    const after=spider.getBoundingClientRect();
    const data={visible:!spider.hidden,position:getComputedStyle(spider).position,
      pointerEvents:getComputedStyle(spider).pointerEvents,top:before.top,
      scrolledTop:after.top,rightGap:innerWidth-after.right,scrollY};
    window.scrollTo({top:start,behavior:'instant'});
    return data;
  });
  if(!spiderScroll.visible || spiderScroll.position!=='fixed' || spiderScroll.pointerEvents!=='none' ||
     Math.abs(spiderScroll.top)>1 || Math.abs(spiderScroll.top-spiderScroll.scrolledTop)>1 ||
     spiderScroll.rightGap<0 || spiderScroll.rightGap>10 || spiderScroll.scrollY<100) {
    spiderFailures.push('dangling spider is not visible at the fixed viewport top-right while scrolling: '+JSON.stringify(spiderScroll));
  }

  // The theme follows system changes until a visitor saves an override.
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'dark'}]);
  await page.reload({waitUntil:'load'});
  await waitForPals(page);
  const systemDark=await page.evaluate(()=>{
    const button=document.getElementById('theme-toggle');
    return {
      theme:document.documentElement.dataset.theme,
      source:document.documentElement.dataset.themeSource,
      pressed:button.getAttribute('aria-pressed'),
      icon:button.getAttribute('data-theme-icon'),
      ariaLabel:button.getAttribute('aria-label'),
      sunVisible:getComputedStyle(button.querySelector('.theme-icon-sun')).display!=='none',
      moonVisible:getComputedStyle(button.querySelector('.theme-icon-moon')).display!=='none',
      scheme:getComputedStyle(document.documentElement).colorScheme,
      surface:getComputedStyle(document.querySelector('.app')).backgroundColor,
      text:getComputedStyle(document.body).color,
      meta:document.querySelector('meta[name="theme-color"]').content,
    };
  });
  if(systemDark.theme!=='dark' || systemDark.source!=='system' || systemDark.pressed!=='true' ||
     systemDark.icon!=='moon' || systemDark.ariaLabel!=='Toggle color theme' ||
     systemDark.sunVisible || !systemDark.moonVisible || systemDark.scheme!=='dark' ||
     systemDark.surface!=='rgb(20, 24, 39)' || systemDark.text!=='rgb(244, 243, 238)' || systemDark.meta!=='#0B0D16') {
    themeFailures.push('dark system default or moon icon failed: '+JSON.stringify(systemDark));
  }
  const darkCheckin=await page.evaluate(()=>{
    const button=document.getElementById('daily-checkin');
    const wasDisabled=button.disabled,wasText=button.textContent;
    button.disabled=true;button.textContent='Checked in today';
    const style=getComputedStyle(button);
    const measured={text:button.textContent,color:style.color,background:style.backgroundColor};
    button.disabled=wasDisabled;button.textContent=wasText;
    return measured;
  });
  if(darkCheckin.text!=='Checked in today' || darkCheckin.color!=='rgb(244, 243, 238)' || darkCheckin.background!=='rgb(20, 24, 39)') {
    themeFailures.push('checked-in button does not use light ink on the dark surface: '+JSON.stringify(darkCheckin));
  }
  const themePlacement=await page.evaluate(()=>{
    const button=document.getElementById('theme-toggle');
    const row=document.querySelector('.hero-eyebrow-row');
    const hero=document.querySelector('.hero');
    const eyebrow=row?.querySelector('.eyebrow');
    const rect=button.getBoundingClientRect();
    const heroRect=hero?.getBoundingClientRect();
    const heroStyle=hero&&getComputedStyle(hero);
    const label=eyebrow?.getBoundingClientRect();
    const heroContentRight=heroRect&&heroStyle
      ? heroRect.right-parseFloat(heroStyle.borderRightWidth)-parseFloat(heroStyle.paddingRight)
      : Infinity;
    const hit=getComputedStyle(button,'::before');
    return {sameRow:!!row&&row.contains(button)&&button.parentElement===row,
      eyebrow:eyebrow?.textContent.trim(),position:getComputedStyle(button).position,
      topDelta:label?Math.abs(rect.top-label.top):Infinity,
      topInset:label&&heroRect?label.top-heroRect.top:Infinity,
      heroRightGap:heroContentRight-rect.right,
      height:rect.height,eyebrowHeight:label?.height??0,width:rect.width,
      horizontalGap:label?rect.left-label.right:0,
      hitWidth:parseFloat(hit.width),hitHeight:parseFloat(hit.height),
      borderRadius:getComputedStyle(button).borderRadius,
      ariaLabel:button.getAttribute('aria-label'),hidden:button.hidden};
  });
  if(!themePlacement.sameRow || themePlacement.eyebrow!=='FIELDNOTES / HR' ||
     themePlacement.topDelta>1 ||
     themePlacement.topInset<18 || themePlacement.topInset>30 || Math.abs(themePlacement.heroRightGap)>1 ||
     Math.abs(themePlacement.height-themePlacement.eyebrowHeight)>1 ||
     Math.abs(themePlacement.width-themePlacement.height)>1 || themePlacement.horizontalGap<6 ||
     themePlacement.hitWidth<44 || themePlacement.hitHeight<44 ||
     themePlacement.borderRadius!=='50%' || themePlacement.ariaLabel!=='Toggle color theme' || themePlacement.hidden) {
    themeFailures.push('theme toggle is not far-right in a compact, hero-edge-aligned eyebrow row with no excess hero top space: '+JSON.stringify(themePlacement));
  }
  const darkAudit=await auditThemeContrast(page);
  contrastAudits.push({theme:'dark',...darkAudit});
  if(!darkAudit.yellowText.length) contrastFailures.push('dark theme yellow backgrounds were not detected');
  if(!darkAudit.shadows.length) contrastFailures.push('dark theme box shadows were not detected');
  if(darkAudit.yellowFailures.length) contrastFailures.push('dark theme yellow text <4.5:1: '+JSON.stringify(darkAudit.yellowFailures));
  if(darkAudit.shadowFailures.length) contrastFailures.push('dark theme box shadow <3:1: '+JSON.stringify(darkAudit.shadowFailures));
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
  await page.waitForFunction(()=>document.documentElement.dataset.theme==='light' && document.documentElement.dataset.themeSource==='system');
  const systemLight=await page.evaluate(()=>{
    const button=document.getElementById('theme-toggle');
    return {
      theme:document.documentElement.dataset.theme,
      source:document.documentElement.dataset.themeSource,
      pressed:button.getAttribute('aria-pressed'),
      icon:button.getAttribute('data-theme-icon'),
      sunVisible:getComputedStyle(button.querySelector('.theme-icon-sun')).display!=='none',
      moonVisible:getComputedStyle(button.querySelector('.theme-icon-moon')).display!=='none',
      scheme:getComputedStyle(document.documentElement).colorScheme,
      surface:getComputedStyle(document.querySelector('.app')).backgroundColor,
      text:getComputedStyle(document.body).color,
      meta:document.querySelector('meta[name="theme-color"]').content,
    };
  });
  if(systemLight.theme!=='light' || systemLight.source!=='system' || systemLight.pressed!=='false' ||
     systemLight.icon!=='sun' || !systemLight.sunVisible || systemLight.moonVisible ||
     systemLight.scheme!=='light' || systemLight.surface!=='rgb(255, 248, 231)' ||
     systemLight.text!=='rgb(17, 20, 43)' || systemLight.meta!=='#11142B') {
    themeFailures.push('light system default or sun icon failed: '+JSON.stringify(systemLight));
  }
  const lightAudit=await auditThemeContrast(page);
  contrastAudits.push({theme:'light',...lightAudit});
  if(!lightAudit.yellowText.length) contrastFailures.push('light theme yellow backgrounds were not detected');
  if(!lightAudit.shadows.length) contrastFailures.push('light theme box shadows were not detected');
  if(lightAudit.yellowFailures.length) contrastFailures.push('light theme yellow text <4.5:1: '+JSON.stringify(lightAudit.yellowFailures));
  if(lightAudit.shadowFailures.length) contrastFailures.push('light theme box shadow <3:1: '+JSON.stringify(lightAudit.shadowFailures));
  await page.$eval('#theme-toggle',button=>button.click());
  const override=await page.evaluate(()=>({
    theme:document.documentElement.dataset.theme,
    source:document.documentElement.dataset.themeSource,
    pressed:document.getElementById('theme-toggle').getAttribute('aria-pressed'),
    icon:document.getElementById('theme-toggle').getAttribute('data-theme-icon'),
    saved:localStorage.getItem('fieldnotes-hr-theme-v1'),
  }));
  if(override.theme!=='dark' || override.source!=='user' || override.pressed!=='true' || override.icon!=='moon' || override.saved!=='dark') {
    themeFailures.push('theme toggle did not save its dark override: '+JSON.stringify(override));
  }
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'dark'}]);
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
  if(await page.$eval('#theme-toggle',button=>button.getAttribute('aria-pressed'))!=='true') {
    themeFailures.push('saved theme changed with the system setting');
  }
  await page.reload({waitUntil:'load'});
  await waitForPals(page);
  const persistedTheme=await page.evaluate(()=>({
    theme:document.documentElement.dataset.theme,
    source:document.documentElement.dataset.themeSource,
    icon:document.getElementById('theme-toggle').getAttribute('data-theme-icon'),
    saved:localStorage.getItem('fieldnotes-hr-theme-v1'),
  }));
  if(persistedTheme.theme!=='dark' || persistedTheme.source!=='user' || persistedTheme.icon!=='moon' || persistedTheme.saved!=='dark') {
    themeFailures.push('saved dark theme did not survive reload: '+JSON.stringify(persistedTheme));
  }
  await page.$eval('#theme-toggle',button=>button.click());
  const lightOverride=await page.evaluate(()=>({
    theme:document.documentElement.dataset.theme,
    source:document.documentElement.dataset.themeSource,
    pressed:document.getElementById('theme-toggle').getAttribute('aria-pressed'),
    icon:document.getElementById('theme-toggle').getAttribute('data-theme-icon'),
    saved:localStorage.getItem('fieldnotes-hr-theme-v1'),
  }));
  if(lightOverride.theme!=='light' || lightOverride.source!=='user' || lightOverride.pressed!=='false' || lightOverride.icon!=='sun' || lightOverride.saved!=='light') {
    themeFailures.push('theme toggle did not save its light override: '+JSON.stringify(lightOverride));
  }
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'dark'}]);
  const lightStays=await page.evaluate(()=>({
    theme:document.documentElement.dataset.theme,
    source:document.documentElement.dataset.themeSource,
    pressed:document.getElementById('theme-toggle').getAttribute('aria-pressed'),
    icon:document.getElementById('theme-toggle').getAttribute('data-theme-icon'),
  }));
  if(lightStays.theme!=='light' || lightStays.source!=='user' || lightStays.pressed!=='false' || lightStays.icon!=='sun') {
    themeFailures.push('saved light override changed with the dark system setting: '+JSON.stringify(lightStays));
  }
  await page.reload({waitUntil:'load'});
  await waitForPals(page);
  const persistedLight=await page.evaluate(()=>({
    theme:document.documentElement.dataset.theme,
    source:document.documentElement.dataset.themeSource,
    icon:document.getElementById('theme-toggle').getAttribute('data-theme-icon'),
    saved:localStorage.getItem('fieldnotes-hr-theme-v1'),
  }));
  if(persistedLight.theme!=='light' || persistedLight.source!=='user' || persistedLight.icon!=='sun' || persistedLight.saved!=='light') {
    themeFailures.push('saved light theme did not survive reload: '+JSON.stringify(persistedLight));
  }
  await page.evaluate(()=>localStorage.removeItem('fieldnotes-hr-theme-v1'));
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
  await page.reload({waitUntil:'load'});
  await waitForPals(page);
  if(await page.$eval('#theme-toggle',button=>button.getAttribute('aria-pressed'))!=='false' || await page.evaluate(()=>document.documentElement.dataset.themeSource)!=='system') {
    themeFailures.push('clearing the theme override did not restore the system default');
  }

  const scrollButtonAtTop=await page.$eval('#back-to-top',button=>({hidden:button.hidden,
    label:button.getAttribute('aria-label'),hasIcon:!!button.querySelector('svg')}));
  if(!scrollButtonAtTop.hidden || scrollButtonAtTop.label!=='Back to top' || !scrollButtonAtTop.hasIcon) {
    scrollFailures.push('back-to-top control should start hidden at the top with an accessible arrow');
  }
  await page.evaluate(()=>window.scrollTo({top:600,behavior:'instant'}));
  await page.waitForFunction(()=>!document.getElementById('back-to-top').hidden);
  const scrollButtonPinned=await page.$eval('#back-to-top',button=>{
    const rect=button.getBoundingClientRect();
    return {position:getComputedStyle(button).position,width:rect.width,height:rect.height,
      rightGap:innerWidth-rect.right,bottomGap:innerHeight-rect.bottom};
  });
  if(scrollButtonPinned.position!=='fixed' || scrollButtonPinned.width<44 || scrollButtonPinned.height<44 || scrollButtonPinned.rightGap<8 || scrollButtonPinned.rightGap>32 || scrollButtonPinned.bottomGap<8 || scrollButtonPinned.bottomGap>32) {
    scrollFailures.push('back-to-top control is not fixed at the bottom-right: '+JSON.stringify(scrollButtonPinned));
  }
  await new Promise(resolve=>setTimeout(resolve,3150));
  if(!(await page.$eval('#back-to-top',button=>button.hidden))) {
    scrollFailures.push('back-to-top control did not hide after three seconds of idle time');
  }
  await page.evaluate(()=>window.scrollTo({top:500,behavior:'instant'}));
  await page.waitForFunction(()=>!document.getElementById('back-to-top').hidden);
  await page.click('#back-to-top');
  try {
    await page.waitForFunction(()=>scrollY<=1,{timeout:5000});
    await page.waitForFunction(()=>document.getElementById('back-to-top').hidden,{timeout:2000});
  } catch (_) {
    scrollFailures.push('back-to-top click did not return to the top and hide the control');
  }

  // 8b. The default view has the stage bodies collapsed. That is what a
  // visitor sees first, and it is where the pals control panel sits directly
  // above the stage list, so check control overlap in that state too.
  const collapsed = [];
  for (const width of [320, 900, 1440]) {
    await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
    const measured = await page.evaluate(async (maxOverlap) => {
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
      const layer = document.querySelector('div[data-piixpal]');
      const canvases = layer && layer.shadowRoot
        ? [...layer.shadowRoot.querySelectorAll('.a canvas')] : [];
      let centreHits = 0;
      let worstOverlap = 0;
      let worstControl = '';
      const openStages = document.querySelectorAll('details.stage[open]').length;
      for (const control of document.querySelectorAll(
        '#theme-toggle, #back-to-top, .toolbar button, .daily-checkin-controls button, .file-button, input, summary, .resource a, .completion, .pals-controls button'
      )) {
        const r = control.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        if (r.bottom < -200 || r.top > innerHeight + 200) continue;
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        for (const canvas of canvases) {
          const p = canvas.getBoundingClientRect();
          if (!p.width || !p.height) continue;
          if (cx >= p.left && cx <= p.right && cy >= p.top && cy <= p.bottom) centreHits++;
          const ow = Math.max(0, Math.min(r.right, p.right) - Math.max(r.left, p.left));
          const oh = Math.max(0, Math.min(r.bottom, p.bottom) - Math.max(r.top, p.top));
          if (ow * oh > worstOverlap) {
            worstOverlap = ow * oh;
            worstControl = control.id || String(control.className).split(' ')[0] || control.tagName;
          }
        }
      }
      return { centreHits, worstOverlap: Math.round(worstOverlap), worstControl, openStages,
               maxOverlap };
    }, MAX_CONTROL_OVERLAP);
    collapsed.push({ width, ...measured });
  }

  const results = [];
  for (const width of WIDTHS) {
    await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
    const measured = await page.evaluate(async (expected, palCount, maxOverlap) => {
      document.querySelectorAll('details.stage').forEach((d) => { d.open = true; });
      // Let ResizeObserver and the Pals animation frame settle after the
      // viewport and accordion changes before measuring their new positions.
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r,120))));
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
      const stageNodes = [...document.querySelectorAll('details.stage')];
      if (stageNodes.length !== expected.stages) failures.push(`${stageNodes.length} stages, expected ${expected.stages}`);
      if (document.querySelector('#enable-notifications, #reminder-time, label[for="reminder-time"]')) {
        failures.push('reminder controls remain in the tracker');
      }
      const toolbar=document.querySelector('.toolbar');
      if (toolbar && /\breminders?\b|\bnotifications?\b/i.test(toolbar.textContent)) {
        failures.push('reminder copy remains in the tracker controls');
      }
      let stageHeaderDelta=0;
      for (const stage of stageNodes) {
        const summary=stage.querySelector('summary');
        const number=summary?.querySelector('.stage-num');
        const title=summary?.querySelector('.stage-heading');
        const meter=summary?.querySelector('.stage-meter');
        const toggle=summary?.querySelector('.stage-toggle-indicator');
        const subtitle=summary?.querySelector('.stage-subheading');
        if(!summary||!number||!title||!meter||!toggle) {
          failures.push('stage summary is missing a number, title, percentage or disclosure sign');
          continue;
        }
        const nr=rect(number),tr=rect(title),mr=rect(meter),ir=rect(toggle);
        const numberTitleTopDelta=Math.abs(nr.top-tr.top);
        const meterIndicatorCenterDelta=Math.abs((mr.top+mr.bottom)/2-(ir.top+ir.bottom)/2);
        stageHeaderDelta=Math.max(stageHeaderDelta,numberTitleTopDelta,meterIndicatorCenterDelta);
        const duplicateIndicator=getComputedStyle(summary,'::after');
        if(duplicateIndicator.display!=='none' && duplicateIndicator.content!=='none') {
          failures.push('duplicate default plus/minus remains below the stage number');
        }
        const toggleFont=parseFloat(getComputedStyle(toggle,'::before').fontSize);
        const meterFont=parseFloat(getComputedStyle(meter).fontSize);
        if(toggleFont<meterFont*1.5) failures.push('stage plus/minus is too small relative to its percentage counter');
        if(getComputedStyle(summary).display!=='grid' ||
           [number,title,meter,toggle].some(el=>getComputedStyle(el).gridRowStart!=='1')) {
          failures.push('stage number, title, percentage and disclosure sign are not in the same grid row');
        }
        if(numberTitleTopDelta>1.1 || meterIndicatorCenterDelta>1.1) {
          failures.push('stage number/title tops or percentage/disclosure centers are vertically misaligned');
        }
        if(nr.right>tr.left+1 || tr.right>mr.left+1 || mr.right>ir.left+1) {
          failures.push('stage summary columns overlap or are out of order');
        }
        if(subtitle && (Math.abs(rect(subtitle).left-tr.left)>1 || rect(subtitle).top<tr.bottom-1)) {
          failures.push('stage duration does not sit below the title in its own aligned column');
        }
      }

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

      // 7. Tap targets and heading outline. The compact theme icon's visible
      // circle matches the eyebrow; its transparent pseudo-element keeps a 44px hit area.
      const small = [...document.querySelectorAll(
        '#back-to-top, .toolbar button, .daily-checkin-controls button:not([hidden]), .pals-controls button, .stage summary, .milestone-label'
      )].filter((el) => !el.hidden && rect(el).height < 44).length;
      if (small) failures.push(`${small} controls are under 44px tall`);
      const themeButton=document.getElementById('theme-toggle');
      const themeHit=getComputedStyle(themeButton,'::before');
      if(parseFloat(themeHit.width)<44 || parseFloat(themeHit.height)<44 || themeHit.pointerEvents==='none') {
        failures.push('compact theme toggle has no 44px pointer target');
      }
      const eyebrowRow=document.querySelector('.hero-eyebrow-row');
      const themeEyebrow=eyebrowRow?.querySelector('.eyebrow');
      if(!eyebrowRow || !themeEyebrow) failures.push('missing hero eyebrow row');
      else {
        const buttonRect=rect(themeButton),eyebrowRect=rect(themeEyebrow),heroStyle=getComputedStyle(hero);
        const heroContentRight=hr.right-parseFloat(heroStyle.borderRightWidth)-parseFloat(heroStyle.paddingRight);
        const topInset=eyebrowRect.top-hr.top;
        if(Math.abs(heroContentRight-buttonRect.right)>1) failures.push('theme toggle is not aligned to the hero content far-right edge');
        if(Math.abs(buttonRect.top-eyebrowRect.top)>1) failures.push('theme toggle and eyebrow are not top-aligned');
        if(topInset<18 || topInset>30) failures.push(`excess space above eyebrow: ${topInset.toFixed(1)}px from hero edge`);
      }
      const outline = ['h1', 'h2', 'h3'].map((s) => document.querySelectorAll(s).length);
      if (outline[0] !== 1 || outline[2] !== expected.cards) {
        failures.push(`heading outline h1/h2/h3 = ${outline.join('/')}`);
      }
      if (!document.querySelector('.skip-link')) failures.push('skip link missing');

      // 8. Pals: count, fixed layer, no control-centre hits, bounded overlap.
      const palEls = document.querySelectorAll('piix-pal[data-fieldnotes-pal]').length;
      if (palEls !== palCount) failures.push(`${palEls} pals, expected ${palCount}`);
      const layer = document.querySelector('div[data-piixpal]');
      const canvases = layer && layer.shadowRoot
        ? [...layer.shadowRoot.querySelectorAll('.a canvas')] : [];
      if (!layer) failures.push('pals layer missing');
      else if (getComputedStyle(layer).position !== 'absolute') failures.push('pals layer is not document-positioned');
      if (canvases.length < palCount) failures.push(`only ${canvases.length} pal actors rendered`);

      let centreHits = 0;
      let worstOverlap = 0;
      let worstControl = '';
      const controls = [...document.querySelectorAll(
        '#theme-toggle, #back-to-top, .toolbar button, .daily-checkin-controls button, .file-button, input, summary, .resource a, .completion, .pals-controls button'
      )];
      for (const control of controls) {
        const r = rect(control);
        if (!r.width || !r.height) continue;
        if (r.bottom < -200 || r.top > innerHeight + 200) continue;
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        for (const canvas of canvases) {
          const p = rect(canvas);
          if (!p.width || !p.height) continue;
          if (cx >= p.left && cx <= p.right && cy >= p.top && cy <= p.bottom) centreHits++;
          const ow = Math.max(0, Math.min(r.right, p.right) - Math.max(r.left, p.left));
          const oh = Math.max(0, Math.min(r.bottom, p.bottom) - Math.max(r.top, p.top));
          const area = ow * oh;
          if (area > worstOverlap) {
            worstOverlap = area;
            worstControl = control.id || String(control.className).split(' ')[0] || control.tagName;
          }
        }
      }
      if (centreHits) failures.push(`${centreHits} pal(s) cover a control centre`);
      if (worstOverlap > maxOverlap) {
        failures.push(`pal overlaps ${worstControl} by ${Math.round(worstOverlap)}px² (max ${maxOverlap})`);
      }
      const controlsVisible = !document.getElementById('pals-controls')?.hidden;
      if (!controlsVisible) failures.push('pals control panel is hidden');
      const spider=document.getElementById('fieldnotes-spider');
      if(!spider) failures.push('dangling spider markup is missing');
      else {
        const spiderStyle=getComputedStyle(spider),spiderRect=rect(spider);
        const spiderRightGap=innerWidth-spiderRect.right;
        if(spider.hidden || spiderStyle.position!=='fixed' || spiderStyle.pointerEvents!=='none' ||
           Math.abs(spiderRect.top)>1 || spiderRightGap<0 || spiderRightGap>10) {
          failures.push('dangling spider is not visible, fixed and pointer-transparent at the viewport top-right');
        }
      }

      // Hit-test actual links, not only sprite rectangles. Shadow-root :host
      // rules can make the *empty overlay* intercept clicks even with no
      // creature overlapping a link. Scroll every link into the viewport.
      let blockedLinks = 0;
      const blockedTargets = [];
      const originalY = scrollY;
      for (const link of links) {
        link.scrollIntoView({block:'center', behavior:'instant'});
        await new Promise((resolve) => requestAnimationFrame(resolve));
        const r = rect(link);
        const hit = document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
        if (!(hit === link || link.contains(hit))) {
          blockedLinks++;
          blockedTargets.push({href:link.href,target:hit?.outerHTML.slice(0,180)});
        }
      }
      window.scrollTo({top:originalY, behavior:'instant'});
      if (blockedLinks) failures.push(`${blockedLinks} resource links intercepted: ${JSON.stringify(blockedTargets)}`);

      return {
        failures: [...new Set(failures)],
        scrollW,
        h1FontPx: h1 ? px(parseFloat(getComputedStyle(h1).fontSize)) : 0,
        tagFills: fills.size,
        worstBottomDelta: px(worstBottomDelta),
        stageHeaderDelta:px(stageHeaderDelta),
        blockedLinks,
        palEls,
        actors: canvases.length,
        centreHits,
        worstOverlap: Math.round(worstOverlap),
        worstControl,
      };
    }, EXPECTED, PAL_COUNT, MAX_CONTROL_OVERLAP);
    results.push({ width, ...measured });
  }

  // Real pointer input, with only external navigation suppressed so the
  // sandbox's YouTube egress restriction does not masquerade as a link bug.
  const activationChecks = [];
  for (const width of [390, 1440]) {
    await page.setViewport({width,height:900,deviceScaleFactor:1,hasTouch:true});
    await page.evaluate(() => {
      document.querySelector('details.stage').open = true;
      window.linkActivations = [];
      window.captureResourceActivation = event => {
        const link = event.target.closest('.resource a');
        if (!link) return;
        event.preventDefault();
        window.linkActivations.push({href:link.href, trusted:event.isTrusted});
      };
      document.addEventListener('click', window.captureResourceActivation);
    });
    const links = await page.$$('.stage[data-stage="0"] .resource a');
    for (const link of links.slice(0,2)) {
      await link.evaluate(el => el.scrollIntoView({block:'center',behavior:'instant'}));
      await link.click();
      await link.tap();
    }
    const activated = await page.evaluate(() => {
      document.removeEventListener('click',window.captureResourceActivation);
      return window.linkActivations;
    });
    const ok = activated.length === 4 && activated.every(a=>a.trusted && a.href.includes('/playlist?list='));
    activationChecks.push({width, ok, activated});
    if (!ok) runtimeErrors.push('mouse/touch link activation failed at '+width);
  }
  // Confirm default target=_blank navigation is requested, without the
  // capture/preventDefault instrumentation above. External loading itself is
  // not a test here: provider hosts are blocked by the sandbox's egress policy.
  const session = await page.createCDPSession();
  await session.send('Page.enable');
  const windowRequests = [];
  session.on('Page.windowOpen', event => windowRequests.push(event.url));
  const pagesBefore = new Set(await browser.pages());
  const firstLink = await page.$('.stage[data-stage="0"] .resource a');
  await firstLink.evaluate(el=>el.scrollIntoView({block:'center',behavior:'instant'}));
  await firstLink.click();
  await new Promise(resolve=>setTimeout(resolve,250));
  if (!windowRequests.some(url=>url.includes('list=PLeDNHX61_qlQeRK1_i5flRpz2T0wjQXN2'))) {
    runtimeErrors.push('default playlist click did not request new-tab navigation');
  }
  console.log('Default new-tab navigation requests:',JSON.stringify(windowRequests));
  for (const opened of await browser.pages()) {
    if (!pagesBefore.has(opened)) await opened.close();
  }
  await session.detach();
  console.log('Mouse + touch playlist activation:', JSON.stringify(activationChecks));

  // 9. Functional checks at desktop width, on a clean localStorage.
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'load' });
  // Stable resource identities do not depend on card order.
  const oldKeys = await page.evaluate(() => [0,1].map(i => resourceKey(0,i)));
  if (JSON.stringify(oldKeys) !== JSON.stringify(['resource:hr-essentials','resource:talent-acquisition'])) {
    runtimeErrors.push('existing Stage 1 keys shifted: '+JSON.stringify(oldKeys));
  }
  // Legacy Done credit and activity dates load without becoming new milestones/check-ins.
  await page.evaluate(() => localStorage.setItem(STORAGE_KEY, JSON.stringify({version:2,storage_id:DATA.storage_id,done:{'s0-r0':true},activityDates:[]})));
  await page.reload({waitUntil:'load'});
  const restored = await page.$$eval('.stage[data-stage="0"] .completion', els => els.map(el=>el.textContent.trim()));
  if (JSON.stringify(restored) !== JSON.stringify(['0/1','Done before update'])) {
    runtimeErrors.push('old progress did not restore as previous card credit: '+JSON.stringify(restored));
  }
  // Exercise the actual file-import handler, not only the pure normalizer.
  const importBackup = async value => {
    await page.evaluate(async value => {
      const input=document.getElementById('import-progress');
      const dt=new DataTransfer(); dt.items.add(new File([JSON.stringify(value)],'progress.json',{type:'application/json'}));
      input.files=dt.files; input.dispatchEvent(new Event('change',{bubbles:true}));
    },value);
    await page.waitForFunction(() => document.getElementById('import-progress').value==='');
  };
  const today = await page.evaluate(() => localDateKey());
  await importBackup({version:1,done:{'s0-r0':true},activityDates:[today],reminderTime:'08:30'});
  const imported=await page.evaluate(() => ({
    cards:[...document.querySelectorAll('.stage[data-stage="0"] .completion')].map(el=>el.textContent.trim()),
    status:document.getElementById('today-status').textContent,
    checked:document.getElementById('daily-checkin').disabled,
    undoHidden:document.getElementById('undo-checkin').hidden,
    saved:JSON.parse(localStorage.getItem(STORAGE_KEY)),
  }));
  if(JSON.stringify(imported.cards)!==JSON.stringify(['0/1','Done before update'])) runtimeErrors.push('legacy backup card migration failed: '+JSON.stringify(imported.cards));
  if(imported.saved.manualCheckinDates.length!==0 || !imported.saved.legacyActivityDates.includes(today)) runtimeErrors.push('legacy activity was not kept separate from manual check-ins');
  if(imported.status!=='Checked in today' || !imported.checked || !imported.undoHidden) runtimeErrors.push('legacy activity should show as logged, not as a new manual check-in');
  const savedBeforeInvalid=await page.evaluate(()=>localStorage.getItem(STORAGE_KEY));
  await importBackup({version:999,done:{},activityDates:[]});
  if(await page.evaluate(()=>localStorage.getItem(STORAGE_KEY))!==savedBeforeInvalid) runtimeErrors.push('invalid import changed saved progress');

  await page.evaluate(() => localStorage.clear());
  await page.reload({waitUntil:'load'});
  const before = await page.$eval('#progress-label', (el) => el.textContent.trim());
  const functional = [];
  const copySurface = await page.evaluate(() => {
    const first=document.querySelector('[data-resource-id="hr-essentials"]');
    const access=[...document.querySelectorAll('.resource-access')];
    return {
      stageOutcomeLists:document.querySelectorAll('.stage .outcomes').length,
      stageIntroLines:document.querySelectorAll('.stage .stage-description').length,
      stageDescriptionSourcePreserved:DATA.stages.length===8 &&
        DATA.stages.every(stage=>typeof stage.description==='string' && stage.description.trim().length>0),
      cards:document.querySelectorAll('.resource').length,
      taskBoxes:document.querySelectorAll('input[data-milestone-id]').length,
      summaries:document.querySelectorAll('.access-summary').length,
      summaryLists:[...document.querySelectorAll('.access-summary')].every(list=>list.tagName==='UL' && list.children.length>1 && getComputedStyle(list).listStyleType==='square'),
      evidenceLists:document.querySelectorAll('.access-note-list').length,
      evidenceBullets:[...document.querySelectorAll('.access-note-list')].every(list=>list.tagName==='UL' && list.children.length>1 && getComputedStyle(list).listStyleType==='square'),
      accessCopyPreserved:DATA.stages.every(stage=>stage.resources.every(resource=>{
        const card=document.querySelector(`[data-resource-id="${resource.id}"]`);
        const summary=[...card.querySelectorAll('.access-summary > li')].map(item=>item.textContent.trim());
        summary[0]=summary[0].replace(/^Access:\s*/,'');
        const evidence=[...card.querySelectorAll('.access-note-list > li')].map(item=>item.textContent.trim());
        const normalise=value=>value.toLowerCase().replace(/\s+/g,' ').trim();
        return normalise(summary.join(' '))===normalise(resource.access_summary) && normalise(evidence.join(' '))===normalise(resource.access_note);
      })),
      accessClosed:access.every(item=>!item.open),
      firstSummary:first?.querySelector('.access-summary')?.textContent.trim()||'',
      firstTask:first?.querySelector('.milestone-label')?.textContent.trim()||'',
    };
  });
  if(copySurface.cards!==20 || copySurface.taskBoxes!==20 || copySurface.summaries!==20 || copySurface.evidenceLists!==20 || !copySurface.summaryLists || !copySurface.evidenceBullets || !copySurface.accessCopyPreserved || !copySurface.accessClosed) {
    functional.push('concise copy, square-bullet access details, or collapsed evidence missing: '+JSON.stringify(copySurface));
  }
  if(copySurface.stageOutcomeLists!==0) {
    functional.push(`${copySurface.stageOutcomeLists} redundant stage outcome list(s) remain in the tracker`);
  }
  if(copySurface.stageIntroLines!==0) {
    functional.push(`${copySurface.stageIntroLines} stage intro line(s) remain in the tracker`);
  }
  if(!copySurface.stageDescriptionSourcePreserved) {
    functional.push('stage description source copy is missing');
  }
  if(!copySurface.firstSummary.includes('Public playlist') || !copySurface.firstTask.startsWith('Watch lessons 1–4')) {
    functional.push('plain-language resource copy did not reach the tracker: '+JSON.stringify(copySurface));
  }
  const accessDetails=await page.$('.resource-access');
  await accessDetails.$eval('summary',el=>el.click());
  const accessExpanded=await accessDetails.evaluate(el=>el.open && el.textContent.includes('Checked 2026-10-27'));
  if(!accessExpanded) functional.push('full access evidence did not open');
  await accessDetails.$eval('summary',el=>el.click());
  await page.evaluate(() => {
    const details=document.querySelector('.stage .milestones');
    details.open=true;
    details.querySelector('input[data-milestone-id]').click();
  });
  const after = await page.evaluate(() => ({
    label: document.getElementById('progress-label').textContent.trim(),
    pct: document.getElementById('overall-percent').textContent.trim(),
    today: document.getElementById('today-status').textContent,
    stored: JSON.parse(localStorage.getItem(STORAGE_KEY)),
  }));
  if (!before.includes('0 of 20')) functional.push(`initial label unexpected: ${before}`);
  if (!after.label.includes('1 of 20')) functional.push(`after task: ${after.label}`);
  if (after.pct !== '5%') functional.push(`after task percent: ${after.pct}`);
  if (!after.stored || after.stored.version!==3 || !after.stored.milestones) functional.push('version 3 task progress was not written to localStorage');
  if (after.stored.activityDates.length || after.stored.manualCheckinDates.length) functional.push('task completion incorrectly created a daily check-in');
  if (after.today !== 'Not checked in yet') functional.push('task completion changed today’s check-in status');

  // Explicit attendance is independent and can be undone for the same day.
  await page.click('#daily-checkin');
  const checkedIn=await page.evaluate(() => ({
    status:document.getElementById('today-status').textContent,
    disabled:document.getElementById('daily-checkin').disabled,
    manual:JSON.parse(localStorage.getItem(STORAGE_KEY)).manualCheckinDates,
  }));
  if(checkedIn.status!=='Checked in today' || !checkedIn.disabled || !checkedIn.manual.includes(today)) functional.push('manual daily check-in did not save explicitly');
  await page.click('#undo-checkin');
  const undone=await page.evaluate(() => ({
    status:document.getElementById('today-status').textContent,
    manual:JSON.parse(localStorage.getItem(STORAGE_KEY)).manualCheckinDates,
  }));
  if(undone.status!=='Not checked in yet' || undone.manual.length) functional.push('manual check-in could not be undone');
  await page.click('#daily-checkin');

  // Capture the real export Blob, then round-trip it through the file handler.
  const exportedBackup = await page.evaluate(async () => {
    const original=URL.createObjectURL; let exported;
    URL.createObjectURL = blob => { exported=blob; return original.call(URL,blob); };
    try { document.getElementById('export-progress').click(); }
    finally { URL.createObjectURL=original; }
    return JSON.parse(await exported.text());
  });
  if(exportedBackup.version!==3 || !exportedBackup.storage_id || !exportedBackup.milestones || !exportedBackup.manualCheckinDates.includes(today)) functional.push('version 3 backup missing roadmap, task or check-in progress');
  await importBackup(exportedBackup);
  const roundTrip=await page.evaluate(() => ({
    status:document.getElementById('today-status').textContent,
    card:document.querySelector('.stage .completion').textContent.trim(),
    checked:document.getElementById('daily-checkin').disabled,
  }));
  if(roundTrip.status!=='Checked in today' || roundTrip.card!=='1/1' || !roundTrip.checked) functional.push('version 3 backup round-trip lost task/check-in progress');

  // Reminder controls are retired; backup/import/reset paths remain available.
  await page.evaluate(() => document.getElementById('reset-progress').click());
  await new Promise((r) => setTimeout(r, 150));
  const reset = await page.evaluate(() => ({
    label:document.getElementById('progress-label').textContent.trim(),
    manual:JSON.parse(localStorage.getItem(STORAGE_KEY)).manualCheckinDates,
    checkin:document.getElementById('today-status').textContent,
  }));
  if (!reset.label.includes('0 of 20')) functional.push(`after reset: ${reset.label}`);
  if (reset.manual.length || reset.checkin!=='Not checked in yet') functional.push('reset did not clear current attendance');

  // 10. Pause toggle removes every pal; enabling brings them back.
  try { await waitForPals(page); } catch (_) { functional.push('pals did not return after reset'); }
  const toggleChecks = [];
  await page.click('#pals-toggle');
  await new Promise((r) => setTimeout(r, 200));
  const paused = await page.evaluate(() => ({
    count: document.querySelectorAll('piix-pal[data-fieldnotes-pal]').length,
    spiderHidden: document.getElementById('fieldnotes-spider').hidden,
    pressed: document.getElementById('pals-toggle').getAttribute('aria-pressed'),
    status: document.getElementById('pals-status').textContent,
  }));
  if (paused.count !== 0) toggleChecks.push(`pause left ${paused.count} Piixpal creatures`);
  if (!paused.spiderHidden) toggleChecks.push('pausing tiny pals left the dangling spider visible');
  if (paused.pressed !== 'false') toggleChecks.push('aria-pressed not false when paused');
  if (!/paused/i.test(paused.status)) toggleChecks.push('status line does not say paused');
  await page.click('#pals-toggle');
  try { await waitForPals(page); } catch (_) { toggleChecks.push('pals did not return after enable'); }
  const resumed = await page.evaluate(() => ({
    pressed:document.getElementById('pals-toggle').getAttribute('aria-pressed'),
    spiderHidden:document.getElementById('fieldnotes-spider').hidden,
  }));
  if (resumed.pressed !== 'true') toggleChecks.push('aria-pressed not true when enabled');
  if (resumed.spiderHidden) toggleChecks.push('enabling tiny pals did not restore the dangling spider');

  // 11. Reduced motion: no pal elements at all.
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.reload({ waitUntil: 'load' });
  await new Promise((r) => setTimeout(r, 700));
  const reduced = await page.evaluate(() => ({
    count: document.querySelectorAll('piix-pal[data-fieldnotes-pal]').length,
    spiderHidden:document.getElementById('fieldnotes-spider').hidden,
    status: document.getElementById('pals-status').textContent,
    pressed: document.getElementById('pals-toggle').getAttribute('aria-pressed'),
  }));
  if (reduced.count !== 0 || !reduced.spiderHidden) toggleChecks.push(`${reduced.count} Piixpal creatures or spider under reduced motion`);
  if (!/reduced-motion/i.test(reduced.status)) toggleChecks.push('reduced-motion status text missing');
  await page.evaluate(()=>window.scrollTo({top:600,behavior:'instant'}));
  await page.waitForFunction(()=>!document.getElementById('back-to-top').hidden);
  const reducedScrollBehavior=await page.evaluate(()=>{
    const original=window.scrollTo;
    let behavior=null;
    window.scrollTo=function(options){behavior=options&&options.behavior;return original.call(window,options);};
    document.getElementById('back-to-top').click();
    window.scrollTo=original;
    return behavior;
  });
  if(reducedScrollBehavior!=='auto') scrollFailures.push('back-to-top did not disable smooth scrolling for reduced motion');
  await page.waitForFunction(()=>scrollY<=1,{timeout:2000});
  await page.emulateMediaFeatures([]);

  // ---- report ------------------------------------------------------------
  console.log(`\nFieldNotes-HR visual check — Chromium ${await browser.version()}`);
  console.log('-'.repeat(94));
  console.log('width  overflow  h1(px)  tags  foot Δ  pals  hits  overlap  result');
  for (const r of results) {
    const ok = r.failures.length === 0;
    console.log(
      `${String(r.width).padEnd(6)} ${String(r.scrollW).padEnd(9)} ` +
      `${String(r.h1FontPx).padEnd(7)} ${String(r.tagFills).padEnd(5)} ` +
      `${String(r.worstBottomDelta).padEnd(6)} ${String(r.palEls).padEnd(5)} ` +
      `${String(r.centreHits).padEnd(5)} ${String(r.worstOverlap).padEnd(8)} ${ok ? 'PASS' : 'FAIL'}`
    );
    for (const f of r.failures) console.log(`         - ${f}`);
  }
  console.log('-'.repeat(94));
  const maxStageHeaderDelta=Math.max(0,...results.map(result=>result.stageHeaderDelta));
  const stageHeaderAlignment=maxStageHeaderDelta<=1.1;
  console.log(`stage header alignment: ${stageHeaderAlignment?'PASS':'FAIL'} (${stageHeaderAlignment?'all stages':'misaligned'} at 13 widths; max number/title top or percentage/icon center delta ${maxStageHeaderDelta.toFixed(1)}px)`);
  const collapsedFailures = [];
  for (const c of collapsed) {
    const ok = c.centreHits === 0 && c.worstOverlap <= MAX_CONTROL_OVERLAP;
    console.log(`collapsed @${c.width}px: ${String(c.openStages)} stage(s) open, ` +
                `${c.centreHits} centre hits, worst overlap ${c.worstOverlap}px² ` +
                `(${c.worstControl || 'none'}) — ${ok ? 'PASS' : 'FAIL'}`);
    if (c.centreHits) collapsedFailures.push(`${c.width}px: ${c.centreHits} control-centre hits`);
    if (c.worstOverlap > MAX_CONTROL_OVERLAP) {
      collapsedFailures.push(`${c.width}px: ${c.worstOverlap}px² over ${c.worstControl}`);
    }
  }
  console.log('-'.repeat(94));
  if (!palsMounted) console.log('initial pals mount: TIMED OUT');
  console.log(`functional: ${functional.length ? 'FAIL' : 'PASS'}` +
              (functional.length ? ` — ${functional.join('; ')}` : ` (${before} → ${after.label} / ${after.pct} → reset: ${reset.label}, ${reset.checkin})`));
  console.log(`pause + reduced motion: ${toggleChecks.length ? 'FAIL' : 'PASS'}` +
              (toggleChecks.length ? ` — ${toggleChecks.join('; ')}` : ` (10 Piixpal + spider pause together; ${reduced.count} under reduced motion; ${palsMounted ? TOTAL_PAL_COUNT : '?'} on)`));
  console.log(`dangling spider: ${spiderFailures.length ? 'FAIL' : 'PASS'}` +
              (spiderFailures.length ? ` — ${spiderFailures.join('; ')}` : ' (fixed top-right; remains visible while scrolling)'));
  console.log(`theme preference: ${themeFailures.length ? 'FAIL' : 'PASS'}` +
              (themeFailures.length ? ` — ${themeFailures.join('; ')}` : ' (system light/dark, sun/moon icon, saved override, dark check-in ink, eyebrow-row sizing/alignment)'));
  const minYellowRatio=contrastAudits.length?Math.min(...contrastAudits.map(a=>a.minYellowRatio)):0;
  const minShadowRatio=contrastAudits.length?Math.min(...contrastAudits.map(a=>a.minShadowRatio)):0;
  console.log(`targeted contrast audit: ${contrastFailures.length ? 'FAIL' : 'PASS'}` +
              (contrastFailures.length ? ` — ${contrastFailures.join('; ')}` :
                ` (yellow text min ${minYellowRatio.toFixed(2)}:1; shadow min ${minShadowRatio.toFixed(2)}:1; light + dark)`));
  console.log(`back-to-top: ${scrollFailures.length ? 'FAIL' : 'PASS'}` +
              (scrollFailures.length ? ` — ${scrollFailures.join('; ')}` : ' (fixed bottom-right; hides at top and after 3s idle)'));
  console.log(`runtime errors: ${runtimeErrors.length ? runtimeErrors.join('; ') : 'none'}`);
  const failures = results.filter((r) => r.failures.length).length + functional.length +
                   toggleChecks.length + themeFailures.length + contrastFailures.length +
                   scrollFailures.length + spiderFailures.length + runtimeErrors.length + collapsedFailures.length +
                   (palsMounted ? 0 : 1);
  console.log(`RESULT: ${WIDTHS.length - results.filter((r) => r.failures.length).length}/${WIDTHS.length} widths passed, ${failures} failure(s)`);

  await mkdir(REPORT_DIR, { recursive: true });
  await writeFile(join(REPORT_DIR, 'last-run.json'), JSON.stringify({
    generatedAt: new Date().toISOString(),
    chromium: await browser.version(),
    widths: results,
    collapsed,
    collapsedFailures,
    activationChecks,
    windowRequests,
    functional,
    toggleChecks,
    themeFailures,
    themePlacement,
    darkCheckin,
    contrastAudits,
    contrastFailures,
    scrollButtonAtTop,
    scrollButtonPinned,
    scrollFailures,
    spiderScroll,
    spiderFailures,
    systemDark,
    systemLight,
    override,
    persistedTheme,
    lightOverride,
    lightStays,
    persistedLight,
    reduced,
    reducedScrollBehavior,
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
