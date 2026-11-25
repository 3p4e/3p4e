const { chromium } = require('playwright'); const [url, out] = process.argv.slice(2);
const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
(async () => { const b = await chromium.launch({ proxy, ignoreDefaultArgs: ['--disable-dev-shm-usage'] });
 for (const [tag, vp] of [['d', { width: 1440, height: 900 }], ['m', { width: 390, height: 844 }]]) {
  const c = await b.newContext({ viewport: vp }); const p = await c.newPage(); await p.addInitScript(() => sessionStorage.setItem('dogma_pre', '1'));
  await p.goto(url, { waitUntil: 'networkidle' }); await p.evaluate(() => document.querySelectorAll('.rv').forEach(e => e.classList.add('in')));
  await p.evaluate(() => document.querySelector('.pm').scrollIntoView({ block: 'center' })); await p.waitForTimeout(2500); await p.screenshot({ path: `${out}/${tag}_pm.png` });
  await p.evaluate(() => document.querySelector('#showreel .film').scrollIntoView({ block: 'center' })); await p.click('.seg button[data-v="1"]'); await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/${tag}_reel916.png` });
  console.log(tag, await p.evaluate(() => { const v = document.querySelector('#showreel video'); return v.currentSrc + ' ' + v.poster; }));
  await c.close(); }
 const c = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const p = await c.newPage();
 await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/d_reduced.png` });
 console.log('reduced', JSON.stringify(await p.evaluate(() => ({ pre: !!document.querySelector('.pre'), heroPaused: document.querySelector('.hero video').paused, rv: getComputedStyle(document.querySelector('.rv')).opacity }))));
 await b.close(); })().catch(e => { console.error(e); process.exit(1); });
