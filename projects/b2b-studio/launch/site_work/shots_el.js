// node shots_el.js <url> <outdir> : element screenshots of the parts the review touched
const { chromium } = require('playwright'); const fs = require('fs');
const [url, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const local = /localhost|127\.0\.0\.1/.test(url);
const proxy = (!local && process.env.HTTPS_PROXY) ? { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } : undefined;
(async () => {
  const b = await chromium.launch({ proxy });
  for (const [tag, vp, ex] of [['d', { width: 1440, height: 900 }, {}], ['s', { width: 320, height: 640 }, { isMobile: true, hasTouch: true, deviceScaleFactor: 2 }]]) {
    for (const lang of ['mk', 'en']) {
      const c = await b.newContext(Object.assign({ viewport: vp }, ex)); const p = await c.newPage();
      await p.addInitScript(() => { try { sessionStorage.setItem('dogma_pre', '1'); } catch (e) {} });
      await p.goto(url + (lang === 'en' ? '?lang=en' : ''), { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
      await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.rv').forEach(e => e.classList.add('in')); document.querySelectorAll('.cmp').forEach(c => { c.querySelector('input').dispatchEvent(new Event('input')); c.style.setProperty('--p', '50%'); }); });
      for (const [name, sel] of [['pm', '.pm'], ['plans', '.plans'], ['cgrid', '.cgrid'], ['foot', '.foot'], ['marq', '.marq']]) {
        const el = await p.$(sel); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(name === 'pm' ? 2500 : 400);
        await el.screenshot({ path: `${out}/${tag}_${lang}_${name}.png` });
      }
      await c.close();
    }
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
