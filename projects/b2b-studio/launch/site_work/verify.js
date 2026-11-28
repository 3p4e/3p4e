// node verify.js <url> <outdir>  -> checks the review fixes on a running copy of the site (local or live)
const { chromium } = require('playwright'); const fs = require('fs');
const [url, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const local = /localhost|127\.0\.0\.1/.test(url);
const proxy = (!local && process.env.HTTPS_PROXY) ? { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } : undefined;
const errs = [];
const hook = p => { p.on('pageerror', e => errs.push('pageerror ' + e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push('console ' + m.type() + ' ' + m.text()); });
  p.on('response', r => { if (r.status() >= 400) errs.push('http ' + r.status() + ' ' + r.url()); }); };
const CYR = /[Ѐ-ӿ]/;
(async () => {
  const b = await chromium.launch({ proxy });
  // 1. static checks on the HTML
  { const c = await b.newContext(); const p = await c.newPage(); const r = await p.goto(url, { waitUntil: 'domcontentloaded' }); const html = await r.text();
    console.log('HTML placeholders', ['example.mk', 'example.com', 'XXX', 'tel:', 'wa.me', 'data-placeholder'].map(x => x + ':' + (html.split(x).length - 1)).join(' '));
    console.log('FORM attrs', await p.evaluate(() => { const f = document.querySelector('#qf'); return f ? [...f.attributes].map(a => a.name + '=' + a.value).join(' ') : 'none'; }));
    console.log('CONTACT links', JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('.ways a, .fc2 a')].map(a => a.getAttribute('href') + ' | ' + a.textContent.trim()))));
    console.log('BD_CONTACT', JSON.stringify(await p.evaluate(() => window.BD_CONTACT)));
    console.log('MEDIA urls', JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('video[src],video[poster],video[data-src],source,[data-src],[data-poster],img')].flatMap(e => ['src', 'poster', 'data-src', 'data-poster'].map(a => e.getAttribute(a)).filter(Boolean)).filter(s => /media\/|films\//.test(s)).filter(s => !/\?v=/.test(s)))), '(unversioned media URLs, should be [])');
    console.log('CHIPS', await p.evaluate(() => [...document.querySelectorAll('.chip')].map(c => c.textContent.trim().replace(/\s+/g, ' ')).join(' / ')));
    console.log('ST span', await p.evaluate(() => { const s = document.querySelector('.hud .st'); return s.outerHTML; }));
    const rb = await (await p.request.get(new URL('robots.txt', url).href)).text(); console.log('ROBOTS', JSON.stringify(rb));
    await c.close(); }
  // 2. no JavaScript: no preloader, content visible, form hidden
  { const c = await b.newContext({ viewport: { width: 1440, height: 900 }, javaScriptEnabled: false }); const p = await c.newPage(); await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(800);
    await p.screenshot({ path: `${out}/nojs.png` });
    console.log('NOJS', JSON.stringify(await p.evaluate(() => ({ pre: getComputedStyle(document.querySelector('.pre')).display, h2op: getComputedStyle(document.querySelector('#showreel .sh')).opacity, form: getComputedStyle(document.querySelector('#qf')).display }))));
    await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelector('#contact .cgrid').scrollIntoView(); }); await p.waitForTimeout(800); await p.screenshot({ path: `${out}/nojs_contact.png` }); await c.close(); }
  // 3. preloader with the logo scripts failing: must still go away (fx.js catch -> hide)
  { const c = await b.newContext({ viewport: { width: 1280, height: 800 } }); const p = await c.newPage();
    await p.route(/dogma_logo\.js|mark\.js/, r => r.abort()); await p.goto(url, { waitUntil: 'domcontentloaded' });
    const t0 = Date.now(); let gone = null; while (Date.now() - t0 < 9000) { const s = await p.evaluate(() => { const e = document.querySelector('.pre'); return !e || e.classList.contains('out') || getComputedStyle(e).visibility === 'hidden'; }); if (s) { gone = Date.now() - t0; break; } await p.waitForTimeout(150); }
    console.log('PRELOADER logo scripts blocked: hidden after', gone, 'ms'); await c.close(); }
  // 4. preloader with fx.js itself failing: the CSS failsafe must hide it (~7.6 s)
  { const c = await b.newContext({ viewport: { width: 1280, height: 800 } }); const p = await c.newPage();
    await p.route(/fx\.js/, r => r.abort()); await p.goto(url, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(3000); const a = await p.evaluate(() => getComputedStyle(document.querySelector('.pre')).visibility);
    await p.waitForTimeout(5200); const z = await p.evaluate(() => { const e = getComputedStyle(document.querySelector('.pre')); return e.visibility + ' op=' + e.opacity; });
    await p.screenshot({ path: `${out}/nofx_8s.png` }); console.log('PRELOADER fx.js blocked: at 3 s', a, '| at 8.2 s', z); await c.close(); }
  // 5. normal run: preloader auto-hide, HUD language switch
  { const c = await b.newContext({ viewport: { width: 1440, height: 900 } }); const p = await c.newPage(); hook(p);
    await p.goto(url, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(1200); const a = await p.evaluate(() => !!document.querySelector('.pre'));
    await p.waitForTimeout(6000); const z = await p.evaluate(() => !!document.querySelector('.pre')); console.log('PRELOADER normal: present at 1.2 s', a, '| present at 7.2 s', z);
    await p.waitForTimeout(3500);   // mid-typing / done state in MK
    await p.click('.lang button[data-lang="en"]'); await p.waitForTimeout(350);
    const h1 = await p.evaluate(() => ({ txt: document.querySelector('.hud .txt').textContent, st: document.querySelector('.hud .st').textContent, tag: document.querySelector('.hud .tag').textContent }));
    await p.screenshot({ path: `${out}/d_en_after_toggle.png` });
    await p.waitForTimeout(6500); const h2 = await p.evaluate(() => ({ txt: document.querySelector('.hud .txt').textContent.slice(-40), st: document.querySelector('.hud .st').textContent }));
    console.log('HUD after EN toggle 0.35 s', JSON.stringify(h1), 'cyrillic:', CYR.test(h1.txt + h1.st), '| 6.8 s', JSON.stringify(h2));
    await p.click('.lang button[data-lang="mk"]'); await p.waitForTimeout(350);
    const h3 = await p.evaluate(() => ({ txt: document.querySelector('.hud .txt').textContent, st: document.querySelector('.hud .st').textContent })); console.log('HUD back to MK', JSON.stringify(h3));
    // lightbox + versioned film src + subtitles
    await p.click('.lang button[data-lang="en"]'); await p.evaluate(() => document.querySelector('#films').scrollIntoView()); await p.waitForTimeout(500);
    await p.click('#grid a[data-film="timelapse_landscaping"]'); await p.waitForTimeout(2000);
    console.log('LIGHTBOX', JSON.stringify(await p.evaluate(() => { const v = document.querySelector('#lb video'); return { src: v.getAttribute('src'), poster: v.getAttribute('poster'), tracks: [...v.querySelectorAll('track')].map(t => t.getAttribute('src') + (t.default ? ' default' : '')), title: document.querySelector('#lbT').textContent }; })));
    await p.keyboard.press('Escape'); await c.close(); }
  // 6. layout at 320 / 390 / desktop
  for (const [tag, vp, ex] of [['s', { width: 320, height: 640 }, { isMobile: true, hasTouch: true, deviceScaleFactor: 2 }], ['m', { width: 390, height: 844 }, { isMobile: true, hasTouch: true, deviceScaleFactor: 2 }], ['d', { width: 1440, height: 900 }, {}]]) {
    const c = await b.newContext(Object.assign({ viewport: vp }, ex)); const p = await c.newPage(); hook(p);
    await p.addInitScript(() => { try { sessionStorage.setItem('dogma_pre', '1'); } catch (e) {} });
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
    await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.rv').forEach(e => e.classList.add('in')); });
    const nav = await p.evaluate(() => { const W = document.documentElement.clientWidth, R = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return r.width ? [Math.round(r.left), Math.round(r.right)] : 'hidden'; };
      const amt = [...document.querySelectorAll('.plan .amt')].map(e => Math.round(e.getBoundingClientRect().height) + 'px/' + e.textContent);
      return { W, sw: document.documentElement.scrollWidth, brand: R('.brand'), lang: R('.lang'), burger: R('.burger'), amt }; });
    console.log(tag, 'NAV', JSON.stringify(nav));
    await p.screenshot({ path: `${out}/${tag}_top.png` });
    if (tag !== 'd') { await p.click('.burger'); await p.waitForTimeout(500); console.log(tag, 'MENU open', await p.evaluate(() => document.querySelector('.nav').classList.contains('open'))); await p.screenshot({ path: `${out}/${tag}_menu.png` }); await p.click('.burger'); await p.waitForTimeout(400); }
    for (const sec of ['pricing', 'contact', 'process']) { await p.evaluate(s => document.querySelector('#' + s).scrollIntoView(), sec); await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${tag}_${sec}.png` }); }
    await p.evaluate(() => document.querySelector('.foot').scrollIntoView()); await p.waitForTimeout(400); await p.screenshot({ path: `${out}/${tag}_foot.png` });
    await c.close(); }
  console.log('ERRORS', JSON.stringify([...new Set(errs)], null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
