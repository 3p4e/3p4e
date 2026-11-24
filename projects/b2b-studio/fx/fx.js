/* DOGMA pitch-site effects (shared). Needs dogma_logo.js + mark.js (window.DOGMA_MARK) loaded first. */
(function () {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches, FINE = matchMedia('(pointer: fine)').matches;
  const M = window.DOGMA_MARK, $ = s => document.querySelector(s), $$ = s => document.querySelectorAll(s);
  const font = new FontFace('Russo', 'url(russo.ttf)'); const fontReady = font.load().then(f => document.fonts.add(f)).catch(() => {});
  const logo = (cv, opts) => DogmaLogo(cv, Object.assign({ d: M.d, vbW: M.w, vbH: M.h, font: 'Russo' }, opts));
  // preloader: live ignition of the DOGMA logo, once per session
  const pre = $('.pre');
  if (pre) {
    let seen = false; try { seen = sessionStorage.getItem('dogma_pre') === '1'; } catch (e) {}
    if (RM || seen) pre.remove();
    else {
      const cv = pre.querySelector('canvas'), dpr = Math.min(devicePixelRatio || 1, 1.5);
      cv.width = Math.round(Math.min(innerWidth * 0.96, 1200) * dpr); cv.height = Math.round(cv.width * 9 / 16);
      const hide = () => { pre.classList.add('out'); try { sessionStorage.setItem('dogma_pre', '1'); } catch (e) {} setTimeout(() => { L && L.stop(); pre.remove(); }, 1000); };
      let L = null; fontReady.then(() => { L = logo(cv, { lite: innerWidth < 800, transparent: true }); L.play(0); setTimeout(hide, 4700); });
      pre.querySelector('button').onclick = hide;
    }
  }
  // nav mark: always-on glow, colour cycle and bursts
  const nm = $('.brand canvas');
  if (nm) { nm.width = 96; nm.height = 96; fontReady.then(() => { const L = logo(nm, { layout: 'mark', transparent: true, lite: true }); if (RM) L.render(DogmaLogo.INTRO + 2); else L.play(DogmaLogo.INTRO + 0.5); }); }
  // nav background on scroll
  const nav = $('nav'); addEventListener('scroll', () => nav.classList.toggle('s', scrollY > 40), { passive: true });
  // hero embers
  const em = $('.embers');
  if (em && !RM) { const c = em.getContext('2d'); let W, H; const cols = ['242,193,78', '70,180,255', '190,110,255'];
    const size = () => { const d = Math.min(devicePixelRatio || 1, 2); W = em.width = em.offsetWidth * d; H = em.height = em.offsetHeight * d; }; size(); addEventListener('resize', size);
    const P = Array.from({ length: innerWidth < 700 ? 26 : 55 }, () => ({ x: Math.random(), y: Math.random(), s: 0.5 + Math.random() * 1.2, v: 0.02 + Math.random() * 0.05, ph: Math.random() * 6.28, c: cols[Math.floor(Math.random() * 3)] }));
    let last = performance.now(); const tick = now => { const dt = Math.min(0.05, (now - last) / 1000); last = now; c.clearRect(0, 0, W, H); c.globalCompositeOperation = 'lighter';
      for (const p of P) { p.y -= p.v * dt; if (p.y < -0.05) { p.y = 1.05; p.x = Math.random(); } const x = (p.x + 0.015 * Math.sin(now / 1300 + p.ph)) * W, y = p.y * H, a = 0.22 + 0.4 * Math.sin(now / 600 + p.ph) ** 2, r = p.s * (W / 1400 + 0.6);
        const g = c.createRadialGradient(x, y, 0, x, y, r * 3.6); g.addColorStop(0, `rgba(${p.c},${a})`); g.addColorStop(1, `rgba(${p.c},0)`); c.fillStyle = g; c.beginPath(); c.arc(x, y, r * 3.6, 0, 6.283); c.fill(); }
      requestAnimationFrame(tick); }; requestAnimationFrame(tick); }
  // HUD: timecode + typed prompt with generation progress
  const tc = $('.hud .tc'); if (tc) { const t0 = performance.now(); setInterval(() => { const f = Math.floor((performance.now() - t0) / 1000 * 24), p2 = n => String(n).padStart(2, '0');
    tc.textContent = `TC ${p2(Math.floor(f / 86400) % 24)}:${p2(Math.floor(f / 1440) % 60)}:${p2(Math.floor(f / 24) % 60)}:${p2(f % 24)}`; }, 42); }
  const typeInto = (el, text, ms, bar, done) => { let i = 0; el.classList.add('typing'); const step = () => { el.textContent = text.slice(0, i); if (bar) bar.style.width = (100 * i / text.length) + '%';
      if (i++ < text.length) setTimeout(step, ms); else { el.classList.remove('typing'); done && done(); } }; step(); };
  const hp = $('.hud .prompt');
  if (hp) { const txt = hp.querySelector('.txt'), bar = hp.querySelector('.bar i'), st = hp.querySelector('.st'), full = txt.dataset.text, lab = st.textContent, ok = st.dataset.done;
    const run = () => { st.textContent = lab; typeInto(txt, full, RM ? 0 : 28, bar, () => { st.textContent = ok; setTimeout(run, 5200); }); }; setTimeout(run, RM ? 0 : 900); }
  // cursor spotlight
  const sp = $('.spot'); if (sp && FINE && !RM) { addEventListener('pointermove', e => { sp.style.opacity = 1; sp.style.transform = `translate(${e.clientX}px,${e.clientY}px)`; }, { passive: true }); }
  // reveal on scroll, count-ups, lazy videos, typed pipeline prompt
  const io = new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) return; const el = e.target; io.unobserve(el);
    if (el.classList.contains('rv')) el.classList.add('in');
    if (el.dataset.to) { const to = +el.dataset.to, t0 = performance.now(); const f = now => { const q = Math.min(1, (now - t0) / 1400); el.textContent = Math.round(to * (1 - Math.pow(1 - q, 3))); if (q < 1) requestAnimationFrame(f); }; RM ? el.textContent = to : requestAnimationFrame(f); }
    if (el.dataset.src) { el.src = el.dataset.src; el.play && el.play().catch(() => {}); }
    if (el.dataset.type) typeInto(el, el.dataset.type, RM ? 0 : 22); }), { threshold: 0.15 });
  $$('.rv,[data-to],video[data-src],[data-type]').forEach(el => io.observe(el));
  // film format toggle
  $$('.film').forEach(f => f.querySelectorAll('.seg button').forEach(b => b.onclick = () => { f.querySelectorAll('.seg button').forEach(x => x.classList.remove('on')); b.classList.add('on');
    const v = f.querySelector('video'); f.classList.toggle('v', b.dataset.v === '1'); v.src = b.dataset.src; v.play().catch(() => {}); }));
  // before/after slider: auto-sweeps until touched
  $$('.cmp').forEach(c => { const r = c.querySelector('input'); let user = false; const set = v => c.style.setProperty('--p', v + '%');
    r.addEventListener('input', () => { user = true; set(r.value); }); if (!RM) { const t0 = performance.now(); const f = now => { if (user) return; const v = 50 + 38 * Math.sin((now - t0) / 1600); r.value = v; set(v); requestAnimationFrame(f); }; requestAnimationFrame(f); } });
  const hv = $('.hero video'); if (RM && hv) { hv.removeAttribute('autoplay'); hv.pause(); }
})();
