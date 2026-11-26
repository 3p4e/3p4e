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
    document.documentElement.classList.toggle('l-en', lang !== 'mk');   // any non-MK visit: MK text hidden until applied
    $$('[data-i]').forEach(e => { e.textContent = t(e.dataset.i); });
    $$('[data-ih]').forEach(e => { e.innerHTML = t(e.dataset.ih); });
    $$('[data-ia]').forEach(e => e.dataset.ia.split(';').forEach(p => { const [a, k] = p.split(':'); e.setAttribute(a, t(k)); }));
    document.documentElement.classList.add('i18n');   // site.css hides the MK text of a ?lang=en visit until this point
    $$('.langsel').forEach(x => { x.value = lang; });
    if (window.BD_LANGDD) window.BD_LANGDD(lang);
    const og = $('meta[property="og:locale"]'); if (og) og.content = { mk: 'mk_MK', en: 'en_GB', sq: 'sq_AL', sr: 'sr_RS', hr: 'hr_HR', sl: 'sl_SI', bg: 'bg_BG', zh: 'zh_CN' }[lang] || 'mk_MK';
    // hero HUD prompt: the status span has no data-i (it is driven by data-gen / data-done); on a switch the prompt is retyped
    // at once in the new language instead of keeping the old text until the next 5 s cycle
    if (save && window.BD_HUD) window.BD_HUD.restart(); else { const hs = $('.hud .st'); if (hs) hs.textContent = hs.dataset.gen; }
    if (save) { try { localStorage.setItem('bd_lang', lang); } catch (e) {} }
    if (lb.open && cur >= 0) setTracks();
    if (window.BD_RELABEL) window.BD_RELABEL();
  }
  $$('.langsel').forEach(x => x.addEventListener('change', () => apply(x.value, true)));

  // ---------- mobile menu
  const nav = $('.nav'), burger = $('.burger');
  const setMenu = o => { nav.classList.toggle('open', o); burger.setAttribute('aria-expanded', String(o)); document.body.classList.toggle('menu-open', o); };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  $$('#menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); burger.focus(); } });
  addEventListener('resize', () => { if (innerWidth > 1080) setMenu(false); }, { passive: true });

  // ---------- film filter
  $$('.chip[data-f]').forEach(c => c.addEventListener('click', () => {
    const f = c.dataset.f; $$('.chip[data-f]').forEach(x => x.setAttribute('aria-pressed', String(x === c)));
    $$('#grid .fc').forEach(li => { li.hidden = !(f === 'all' || li.dataset.cat === f); if (!li.hidden) li.classList.add('in'); });
  }));
  // industry films (category films v2): same pattern, own grid
  $$('.chip[data-c]').forEach(c => c.addEventListener('click', () => {
    const f = c.dataset.c; $$('.chip[data-c]').forEach(x => x.setAttribute('aria-pressed', String(x === c)));
    $$('#cgrid .fc').forEach(li => { li.hidden = !(f === 'all' || li.dataset.c === f); if (!li.hidden) li.classList.add('in'); });
  }));

  // ---------- lightbox
  const lb = $('#lb'), v = $('video', lb), ttl = $('#lbT'), line = $('.mt p', lb);
  const ids = FILMS.map(f => f.id); let cur = -1, opener = null;
  const visible = () => $$('.fc:not([hidden]) a', (opener && opener.closest('ul')) || $('#grid')).map(a => a.dataset.film);   // step within the grid the film was opened from
  function subLang(langs) { if (langs.includes(lang)) return lang; const p = ['sr', 'hr', 'sl', 'bg'].includes(lang) ? 'mk' : 'en'; return langs.includes(p) ? p : langs[0]; }
  function setTracks() {
    $$('track', v).forEach(tr => tr.remove());
    const f = FILMS[cur]; if (!f) return; const langs = Object.keys(f.sub || {});
    langs.forEach(L => { const tr = document.createElement('track'); tr.kind = 'subtitles'; tr.srclang = L; tr.label = L === 'mk' ? 'Македонски' : 'English';
      tr.src = f.sub[L]; if (L === subLang(langs)) tr.default = true; v.appendChild(tr); });
    // some browsers ignore `default` on tracks added after load: set the modes explicitly
    setTimeout(() => { const sl = subLang(langs); for (const tt of v.textTracks) tt.mode = (tt.language === sl) ? 'showing' : 'disabled'; }, 50);
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
  $$('a[data-film]').forEach(a => a.addEventListener('click', e => { if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return; e.preventDefault(); openFilm(a.dataset.film, a); }));

  // only one video with sound at a time
  document.addEventListener('play', e => { $$('video').forEach(x => { if (x !== e.target && !x.muted && !x.paused) x.pause(); }); }, true);

  // ---------- muted in-view loops (gallery, sector shots, image -> motion): the src is set when a clip nears the viewport,
  // it plays only while visible and pauses off screen; reduced motion keeps the posters
  const lio = new IntersectionObserver(es => es.forEach(e => { const x = e.target;
    if (e.isIntersecting) { if (RM) return; if (!x.getAttribute('src')) x.src = x.dataset.loop; const p = x.play(); if (p && p.catch) p.catch(() => {}); }
    else if (!x.paused) x.pause(); }), { rootMargin: '120px 0px', threshold: 0.01 });
  $$('video[data-loop]').forEach(x => lio.observe(x));

  // ---------- gallery: the first rows only until "show all"; sector filter
  const gw = $('#gw'), gmore = $('#gmore');
  if (gw) {
    const tiles = $$('.gt', gw);
    if (tiles.some(li => li.classList.contains('x'))) { gw.classList.add('clip'); gmore.hidden = false; }
    gmore.addEventListener('click', () => { gw.classList.remove('clip'); gmore.hidden = true; });
    $$('.gchips .chip').forEach(c => c.addEventListener('click', () => {
      const f = c.dataset.g; $$('.gchips .chip').forEach(x => x.setAttribute('aria-pressed', String(x === c)));
      if (f !== 'all') { gw.classList.remove('clip'); gmore.hidden = true; }
      gw.classList.toggle('flt', f !== 'all');
      tiles.forEach(li => { li.hidden = !(f === 'all' || li.dataset.sec === f); });
    }));
  }

  // ---------- tabs (sectors, build-up projects): click or arrow keys
  function tabs(list) {
    if (!list) return; const ts = $$('[role=tab]', list);
    const sel = t => ts.forEach(x => { const on = x === t; x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1;
      const pn = document.getElementById(x.getAttribute('aria-controls')); if (pn) pn.hidden = !on; });
    ts.forEach((t, i) => { t.addEventListener('click', () => sel(t)); t.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!d) return; e.preventDefault(); const n = ts[(i + d + ts.length) % ts.length]; n.focus(); sel(n); }); });
  }
  tabs($('.stabs'));

  // ---------- build-up viewer: key frame -> its clip -> next key frame ..., runs only while on screen
  const views = $$('.bview').map(v => {
    const st = $('.bstage', v), img = $('.bk', st), vid = $('video', st), bl = $('.bl', st), bn = $('.bn b', st), bar = $('.bprog i', st), bp = $('.bp', st);
    const steps = $$('.bsteps button', v); let i = 0, tm = 0, seen = false, paused = RM, tok = 0;
    const lab = k => steps[k].querySelector('span span').textContent;
    const setBtn = () => { bp.classList.toggle('on', !paused); bp.setAttribute('aria-label', paused ? bp.dataset.play : bp.dataset.pause); };
    const prog = () => { bar.style.width = (100 * (i + (vid.duration && st.classList.contains('play') ? Math.min(1, vid.currentTime / vid.duration) : 0)) / steps.length) + '%'; };
    vid.addEventListener('timeupdate', prog);
    function go(k, quick) {
      const my = ++tok; clearTimeout(tm); i = k; const b = steps[k];
      steps.forEach(x => x === b ? x.setAttribute('aria-current', 'step') : x.removeAttribute('aria-current'));
      img.src = b.dataset.kf; st.classList.remove('play'); vid.pause(); bl.textContent = lab(k); bn.textContent = String(k + 1).padStart(2, '0'); prog();
      if (paused || !seen) return;
      tm = setTimeout(() => { if (my !== tok) return;
        if (b.dataset.clip) { vid.src = b.dataset.clip; const p = vid.play(); if (p && p.catch) p.catch(() => {}); }
        else tm = setTimeout(() => { if (my === tok) go(0); }, 2600); }, quick ? 150 : 1100);
    }
    vid.addEventListener('playing', () => st.classList.add('play'));
    vid.addEventListener('ended', () => { if (i + 1 < steps.length) go(i + 1); else tm = setTimeout(() => go(0), 2200); });
    steps.forEach((b, k) => b.addEventListener('click', () => { if (paused) { paused = false; setBtn(); } go(k, true); }));
    bp.addEventListener('click', () => { paused = !paused; setBtn();
      if (paused) { clearTimeout(tm); vid.pause(); } else if (st.classList.contains('play') && !vid.ended) vid.play().catch(() => {}); else go(i, true); });
    new IntersectionObserver(es => es.forEach(e => { seen = e.isIntersecting;
      if (seen) { if (!paused) { if (st.classList.contains('play') && !vid.ended) vid.play().catch(() => {}); else go(i); } } else { clearTimeout(tm); vid.pause(); } }), { threshold: 0.35 }).observe(st);
    setBtn(); bl.textContent = lab(0);
    return () => { bl.textContent = lab(i); setBtn(); };
  });
  tabs($('.btabs'));
  window.BD_RELABEL = () => views.forEach(f => f());

  // ---------- pricing buttons preselect the package in the form
  const form = $('#qf');
  if (form) $$('.plan a[data-pkg]').forEach(a => a.addEventListener('click', () => { const sel = form.querySelector('select'); sel.value = a.dataset.pkg.split('.')[0]; }));

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
  try { const q = new URLSearchParams(location.search).get('lang'); l0 = ['mk', 'en', 'sq', 'sr', 'hr', 'sl', 'bg', 'zh'].includes(q) ? q : (localStorage.getItem('bd_lang') || 'mk'); } catch (e) {}
  apply(l0, false);
})();

// films are for viewing on this site only (owner, 2026-11-26): no "save video as" menu and no dragging on videos and film cards
document.addEventListener('contextmenu', e => { if (e.target.closest && e.target.closest('video, .fc, .gal, .bstage, .cmp')) e.preventDefault(); });
document.addEventListener('dragstart', e => { if (e.target.tagName === 'VIDEO' || (e.target.closest && e.target.closest('.fc'))) e.preventDefault(); });

// ---------- language menu with flags (owner, 2026-11-26): button + list over the native select, which stays the source of truth
(function () {
  const NAMES = { mk: 'Македонски', en: 'English', sq: 'Shqip', sr: 'Srpski', hr: 'Hrvatski', sl: 'Slovenščina', bg: 'Български', zh: '中文' };
  document.querySelectorAll('.langsel').forEach(sel => {
    const box = sel.closest('.lang'); if (!box) return; box.classList.add('dd');
    const btn = document.createElement('button'); btn.type = 'button'; btn.className = 'ldb'; btn.setAttribute('aria-haspopup', 'listbox'); btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', sel.getAttribute('aria-label') || 'Language');
    const ul = document.createElement('ul'); ul.className = 'ldl'; ul.setAttribute('role', 'listbox'); ul.hidden = true;
    [...sel.options].forEach(o => { const li = document.createElement('li'); li.setAttribute('role', 'option'); li.tabIndex = -1; li.dataset.v = o.value; li.lang = o.value;
      li.innerHTML = '<i class="fl fl-' + o.value + '"></i><b>' + o.value.toUpperCase() + '</b><span>' + (NAMES[o.value] || '') + '</span>'; ul.appendChild(li); });
    box.appendChild(btn); box.appendChild(ul);
    const show = v => { btn.innerHTML = '<i class="fl fl-' + v + '"></i><b>' + v.toUpperCase() + '</b>'; ul.querySelectorAll('li').forEach(li => li.setAttribute('aria-selected', String(li.dataset.v === v))); };
    const open = o => { ul.hidden = !o; btn.setAttribute('aria-expanded', String(o)); if (o) (ul.querySelector('[aria-selected="true"]') || ul.firstChild).focus(); };
    const pick = v => { open(false); btn.focus(); if (sel.value !== v) { sel.value = v; sel.dispatchEvent(new Event('change')); } show(v); };
    btn.addEventListener('click', e => { e.stopPropagation(); open(ul.hidden); });
    ul.addEventListener('click', e => { const li = e.target.closest('li'); if (li) pick(li.dataset.v); });
    ul.addEventListener('keydown', e => { const items = [...ul.children], i = items.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); items[Math.min(items.length - 1, i + 1)].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); items[Math.max(0, i - 1)].focus(); }
      else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (i >= 0) pick(items[i].dataset.v); }
      else if (e.key === 'Escape' || e.key === 'Tab') { open(false); if (e.key === 'Escape') btn.focus(); } });
    document.addEventListener('click', e => { if (!box.contains(e.target)) open(false); });
    show(sel.value);
    const prev = window.BD_LANGDD; window.BD_LANGDD = v => { if (prev) prev(v); show(v); };
  });
})();
