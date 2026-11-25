// usage: node shots.js <url> <outdir> [quick]
const { chromium } = require('playwright'); const fs = require('fs');
const [url, out, mode] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } : undefined;
const errs = [];
(async () => {
  const b = await chromium.launch({ proxy, ignoreDefaultArgs: ['--disable-dev-shm-usage'] }); // root disk is nearly full: keep shared memory in /dev/shm
  const mk = async (vp, skip, extra) => { const c = await b.newContext(Object.assign({ viewport: vp, deviceScaleFactor: 1 }, extra || {})); const p = await c.newPage();
    p.on('pageerror', e => errs.push('pageerror ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
    p.on('requestfailed', r => errs.push('reqfail ' + r.url() + ' ' + (r.failure() || {}).errorText));
    p.on('response', r => { if (r.status() >= 400) errs.push('http ' + r.status() + ' ' + r.url()); });
    if (skip) await p.addInitScript(() => { try { sessionStorage.setItem('dogma_pre', '1'); } catch (e) {} }); return p; };
  const reveal = p => p.evaluate(() => document.querySelectorAll('.rv').forEach(e => e.classList.add('in')));
  const sections = ['#showreel', '#films', '#process', '#pricing', '#faq', '#contact', '.foot'];
  // 1. preloader frame
  { const p = await mk({ width: 1440, height: 900 }, false); await p.goto(url, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(2600); await p.screenshot({ path: `${out}/d_preloader.png` }); await p.context().close(); }
  // 2. desktop
  for (const [tag, vp] of [['d', { width: 1440, height: 900 }], ['m', { width: 390, height: 844 }]]) {
    const p = await mk(vp, true, tag === 'm' ? { isMobile: true, hasTouch: true } : {}); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(3500);
    await p.screenshot({ path: `${out}/${tag}_hero.png` });
    await p.evaluate(() => window.scrollTo(0, innerHeight * 0.9)); await p.waitForTimeout(1800); await p.screenshot({ path: `${out}/${tag}_stats.png` });
    if (mode !== 'quick') for (const s of sections) { await p.evaluate(s => document.querySelector(s).scrollIntoView({ block: 'start' }), s); await p.waitForTimeout(900); await reveal(p); await p.waitForTimeout(900);
      await p.screenshot({ path: `${out}/${tag}_${s.replace(/[#.]/g, '')}.png` }); }
    // overflow check
    const ov = await p.evaluate(() => { const W = document.documentElement.clientWidth; const bad = []; document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > W + 1) && getComputedStyle(e).position !== 'fixed' && !e.closest('.marq,.aurora,.spot,.pre,dialog,.links')) bad.push(e.tagName + '.' + e.className + ' ' + Math.round(r.right)); }); return { W, sw: document.documentElement.scrollWidth, bad: bad.slice(0, 12) }; });
    console.log(tag, 'overflow', JSON.stringify(ov));
    if (tag === 'm') { await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400); await p.click('.burger'); await p.waitForTimeout(600); await p.screenshot({ path: `${out}/m_menu.png` }); await p.click('.burger'); }
    // EN toggle + lightbox
    await p.evaluate(() => window.scrollTo(0, 0)); await p.click('.lang button[data-lang="en"]'); await p.waitForTimeout(800); await p.screenshot({ path: `${out}/${tag}_hero_en.png` });
    if (mode !== 'quick') { await p.evaluate(() => document.querySelector('#pricing').scrollIntoView()); await p.waitForTimeout(800); await reveal(p); await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${tag}_pricing_en.png` }); }
    await p.evaluate(() => document.querySelector('#films').scrollIntoView()); await p.waitForTimeout(500); await reveal(p);
    await p.click('#grid a[data-film="timelapse_solar"]'); await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/${tag}_lightbox.png` });
    const lbs = await p.evaluate(() => { const v = document.querySelector('#lb video'); return { open: document.querySelector('#lb').open, src: v.currentSrc || v.src, tracks: [...v.textTracks].map(t => t.language + ':' + t.mode), title: document.querySelector('#lbT').textContent, lang: document.documentElement.lang }; });
    console.log(tag, 'lightbox', JSON.stringify(lbs));
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    console.log(tag, 'closed', await p.evaluate(() => document.querySelector('#lb').open));
    await p.click('.lang button[data-lang="mk"]');
    await p.context().close();
  }
  console.log('ERRORS', JSON.stringify([...new Set(errs)].slice(0, 30), null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
