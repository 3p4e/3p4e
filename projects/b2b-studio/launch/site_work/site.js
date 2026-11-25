/* BIG DOGMA public site: language toggle, mobile menu, film filter + lightbox, mailto quote form.
   window.BD_FILMS = [{id, src, poster, sub: {lang: vtt url}}] and window.BD_CONTACT = {email} come from gen_site.py (URLs carry ?v= hashes). */
(function () {
  const D = window.BD_I18N, FILMS = window.BD_FILMS || [], CT = window.BD_CONTACT || {};
  const $ = (s, r) => (r || document).querySelector(s), $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let lang = 'mk';

  // ---------- language
  const t = k => (D[lang] && D[lang][k] != null) ? D[lang][k] : (D.mk[k] || '');
  function apply(l, save) {
    lang = D[l] ? l : 'mk';
    document.documentElement.lang = lang;
    document.documentElement.classList.toggle('l-en', lang === 'en');
    $$('[data-i]').forEach(e => { e.textContent = t(e.dataset.i); });
    $$('[data-ih]').forEach(e => { e.innerHTML = t(e.dataset.ih); });
    $$('[data-ia]').forEach(e => e.dataset.ia.split(';').forEach(p => { const [a, k] = p.split(':'); e.setAttribute(a, t(k)); }));
    document.documentElement.classList.add('i18n');   // site.css hides the MK text of a ?lang=en visit until this point
    $$('.lang button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
    const og = $('meta[property="og:locale"]'); if (og) og.content = lang === 'en' ? 'en_GB' : 'mk_MK';
    // hero HUD prompt: the status span has no data-i (it is driven by data-gen / data-done); on a switch the prompt is retyped
    // at once in the new language instead of keeping the old text until the next 5 s cycle
    if (save && window.BD_HUD) window.BD_HUD.restart(); else { const hs = $('.hud .st'); if (hs) hs.textContent = hs.dataset.gen; }
    if (save) { try { localStorage.setItem('bd_lang', lang); } catch (e) {} }
    if (lb.open && cur >= 0) setTracks();
  }
  $$('.lang button').forEach(b => b.addEventListener('click', () => apply(b.dataset.lang, true)));

  // ---------- mobile menu
  const nav = $('.nav'), burger = $('.burger');
  const setMenu = o => { nav.classList.toggle('open', o); burger.setAttribute('aria-expanded', String(o)); document.body.classList.toggle('menu-open', o); };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  $$('#menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); burger.focus(); } });
  addEventListener('resize', () => { if (innerWidth > 1080) setMenu(false); }, { passive: true });

  // ---------- film filter
  $$('.chip').forEach(c => c.addEventListener('click', () => {
    const f = c.dataset.f; $$('.chip').forEach(x => x.setAttribute('aria-pressed', String(x === c)));
    $$('#grid .fc').forEach(li => { li.hidden = !(f === 'all' || li.dataset.cat === f); if (!li.hidden) li.classList.add('in'); });
  }));

  // ---------- lightbox
  const lb = $('#lb'), v = $('video', lb), ttl = $('#lbT'), line = $('.mt p', lb);
  const ids = FILMS.map(f => f.id); let cur = -1, opener = null;
  const visible = () => $$('#grid .fc:not([hidden]) a').map(a => a.dataset.film);
  function setTracks() {
    $$('track', v).forEach(tr => tr.remove());
    const f = FILMS[cur]; if (!f) return; const langs = Object.keys(f.sub || {});
    langs.forEach(L => { const tr = document.createElement('track'); tr.kind = 'subtitles'; tr.srclang = L; tr.label = L === 'mk' ? 'Македонски' : 'English';
      tr.src = f.sub[L]; if (L === lang || (lang === 'en' && !langs.includes('en') && L === 'mk')) tr.default = true; v.appendChild(tr); });
    // some browsers ignore `default` on tracks added after load: set the modes explicitly
    setTimeout(() => { for (const tt of v.textTracks) tt.mode = (tt.language === lang) ? 'showing' : 'disabled'; }, 50);
  }
  function show(i) {
    cur = i; const id = ids[i];
    ttl.textContent = t(id + '.t'); ttl.dataset.i = id + '.t'; line.textContent = t(id + '.l'); line.dataset.i = id + '.l';
    v.poster = FILMS[i].poster; v.src = FILMS[i].src; setTracks();
    const p = v.play(); if (p && p.catch) p.catch(() => {});
  }
  function openFilm(id, from) {
    opener = from || null; const i = ids.indexOf(id); if (i < 0) return;
    if (typeof lb.showModal === 'function') { lb.showModal(); } else { location.href = FILMS[i].src; return; }
    document.body.classList.add('lb-open'); show(i); $('.x', lb).focus({ preventScroll: true });
  }
  function closeFilm() { if (lb.open) lb.close(); }
  lb.addEventListener('close', () => { v.pause(); v.removeAttribute('src'); $$('track', v).forEach(tr => tr.remove()); v.load(); cur = -1; document.body.classList.remove('lb-open'); if (opener) opener.focus({ preventScroll: true }); });
  lb.addEventListener('click', e => { if (e.target === lb || e.target.closest('[data-close]')) closeFilm(); });
  $$('.pn button', lb).forEach(b => b.addEventListener('click', () => step(+b.dataset.step)));
  function step(d) { const vis = visible(); if (!vis.length) return; let k = vis.indexOf(ids[cur]); k = (k + d + vis.length) % vis.length; show(ids.indexOf(vis[k])); }
  lb.addEventListener('keydown', e => { if (e.target.tagName === 'VIDEO') return; if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1); });
  $$('#grid a[data-film]').forEach(a => a.addEventListener('click', e => { if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return; e.preventDefault(); openFilm(a.dataset.film, a); }));

  // only one video with sound at a time
  document.addEventListener('play', e => { $$('video').forEach(x => { if (x !== e.target && !x.muted && !x.paused) x.pause(); }); }, true);

  // ---------- pricing buttons preselect the package in the form
  const form = $('#qf');
  if (form) $$('.plan a[data-pkg]').forEach(a => a.addEventListener('click', () => { const sel = form.querySelector('select'); const n = a.dataset.pkg.slice(1, 2); sel.value = 'p' + n; }));

  // ---------- mailto form (no backend). The form ships `hidden` (and with a mailto: action as a safety net): it is shown only
  // here, after the submit handler is attached, so a blocked or broken site.js can never let a native submit reach the server.
  if (form && CT.email) form.addEventListener('submit', e => {
    e.preventDefault();
    const fd = new FormData(form), err = $('.err', form), g = k => (fd.get(k) || '').toString().trim();
    if (!g('name') || !g('email') || !g('message') || !form.querySelector('[name=email]').checkValidity()) { err.hidden = false; (form.querySelector(':invalid') || form.querySelector('[name=name]')).focus(); return; }
    err.hidden = true;
    const pkgSel = form.querySelector('select'), pkg = pkgSel.options[pkgSel.selectedIndex].textContent;
    const lines = [[t('fm.name'), g('name')], [t('fm.company'), g('company')], [t('fm.email'), g('email')], [t('fm.phone'), g('phone')], [t('fm.pkg'), pkg]]
      .filter(r => r[1]).map(r => `${r[0]}: ${r[1]}`);
    const body = lines.join('\n') + '\n\n' + g('message') + '\n';
    const subj = `${t('fm.subj')} · BIG DOGMA${g('company') ? ' · ' + g('company') : ''}`;
    location.href = `mailto:${CT.email}?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(body)}`;
  });
  if (form && CT.email) form.hidden = false;

  // ---------- live BIG DOGMA lockup in the contact section: ignites when it scrolls into view, runs only while visible
  const lc = $('.logo-live');
  if (lc && window.DogmaLogo && window.DOGMA_MARK) {
    const M = window.DOGMA_MARK; let L = null, on = false, first = true;
    const font = new FontFace('Russo', 'url(russo.ttf)'), fontReady = font.load().then(f => document.fonts.add(f)).catch(() => {});
    const size = () => { const w = lc.clientWidth || 640, d = Math.min(devicePixelRatio || 1, 1.5); lc.width = Math.round(w * d); lc.height = Math.round(w * d * 9 / 16); };
    const start = () => { if (!L) { size(); L = DogmaLogo(lc, { d: M.d, vbW: M.w, vbH: M.h, font: 'Russo', transparent: true, lite: innerWidth < 800 }); }
      if (RM) { L.render(DogmaLogo.INTRO + 2); return; } if (!on) { on = true; L.play(first ? 0 : DogmaLogo.INTRO + 0.2); first = false; } };
    new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) fontReady.then(start); else if (L && on) { L.stop(); on = false; } }), { threshold: 0.2 }).observe(lc);
    addEventListener('resize', () => { if (L) { size(); if (!on) L.render(DogmaLogo.INTRO + 2); } }, { passive: true });
  }

  // ---------- reduced motion: no autoplaying decorative video
  if (RM) $$('video[autoplay]').forEach(x => { x.removeAttribute('autoplay'); x.pause(); });

  // ---------- initial language: ?lang= beats the saved choice, MK is the default
  let l0 = 'mk';
  try { const q = new URLSearchParams(location.search).get('lang'); l0 = (q === 'en' || q === 'mk') ? q : (localStorage.getItem('bd_lang') || 'mk'); } catch (e) {}
  apply(l0, false);
})();
