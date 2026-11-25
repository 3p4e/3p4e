// node shots_gal.js <url> <outdir>: full-page + section screenshots of the new media sections, console errors, horizontal scroll
const { chromium } = require('playwright'); const fs = require('fs');
const [url, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const local = /localhost|127\.0\.0\.1/.test(url);
const proxy = (!local && process.env.HTTPS_PROXY) ? { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } : undefined;
(async () => {
  const b = await chromium.launch({ proxy }); const errs = [];
  for (const [tag, vp, ex] of [['s', { width: 320, height: 640 }, { isMobile: true, hasTouch: true, deviceScaleFactor: 1 }], ['m', { width: 390, height: 844 }, { isMobile: true, hasTouch: true, deviceScaleFactor: 1 }], ['d', { width: 1440, height: 900 }, {}]]) {
    for (const lang of ['mk', 'en']) {
      const c = await b.newContext(Object.assign({ viewport: vp }, ex)); const p = await c.newPage();
      p.on('pageerror', e => errs.push(`${tag}/${lang} pageerror ${e.message}`)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(`${tag}/${lang} console ${m.text()}`); });
      p.on('response', r => { if (r.status() >= 400) errs.push(`${tag}/${lang} http ${r.status()} ${r.url()}`); });
      await p.addInitScript(() => { try { sessionStorage.setItem('dogma_pre', '1'); } catch (e) {} });
      await p.goto(url + (lang === 'en' ? '?lang=en' : ''), { waitUntil: 'load' }); await p.waitForTimeout(1500);
      await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; });
      // scroll through the page so lazy media load and reveals fire
      const H = await p.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += vp.height * 0.8) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(250); }
      await p.evaluate(() => document.querySelectorAll('.rv').forEach(e => e.classList.add('in')));
      const m = await p.evaluate(() => ({ W: document.documentElement.clientWidth, sw: document.documentElement.scrollWidth, bw: document.body.scrollWidth,
        playing: [...document.querySelectorAll('video[data-loop]')].filter(v => !v.paused).length, loaded: [...document.querySelectorAll('video[data-loop]')].filter(v => v.getAttribute('src')).length,
        wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > document.documentElement.clientWidth + 1 && getComputedStyle(e).position !== 'fixed' && !e.closest('.tabs,.bsteps,.marq,.nav .links,.lb'); }).slice(0, 5).map(e => e.tagName + '.' + e.className) }));
      console.log(tag, lang, JSON.stringify(m));
      for (const sec of ['sectors', 'gallery', 'i2v', 'buildup']) {
        await p.evaluate(s => document.getElementById(s).scrollIntoView(), sec); await p.waitForTimeout(sec === 'buildup' ? 3500 : 1200);
        await p.screenshot({ path: `${out}/${tag}_${lang}_${sec}.png` });
      }
      if (tag !== 's' || lang === 'mk') await p.screenshot({ path: `${out}/${tag}_${lang}_full.png`, fullPage: true });
      // interactions
      if (lang === 'en') {
        await p.evaluate(() => document.getElementById('gallery').scrollIntoView()); await p.click('.gchips .chip[data-g="wine"]'); await p.waitForTimeout(800);
        console.log(tag, 'wine filter visible', await p.evaluate(() => [...document.querySelectorAll('.gt')].filter(l => !l.hidden && getComputedStyle(l).display !== 'none').length));
        await p.click('.btabs [role=tab]:nth-child(3)'); await p.evaluate(() => document.getElementById('buildup').scrollIntoView()); await p.waitForTimeout(4000);
        console.log(tag, 'build-up solar', await p.evaluate(() => { const v = document.querySelector('#bv-solar'); return { hidden: v.hidden, lab: v.querySelector('.bl').textContent, playing: !v.querySelector('video').paused, src: v.querySelector('video').getAttribute('src') }; }));
        await p.click('#st-sector_wine'); await p.waitForTimeout(300); await p.click('#sp-sector_wine .sfilm'); await p.waitForTimeout(1500);
        console.log(tag, 'lightbox from sectors', await p.evaluate(() => ({ open: document.querySelector('#lb').open, t: document.querySelector('#lbT').textContent })));
        await p.keyboard.press('Escape');
      }
      await c.close();
    }
  }
  console.log('ERRORS', JSON.stringify([...new Set(errs)], null, 1)); await b.close();
})().catch(e => { console.error(e); process.exit(1); });
