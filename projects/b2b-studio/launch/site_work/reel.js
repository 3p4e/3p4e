/* BIG DOGMA reel (owner, 2026-11-26): full-screen random rotation of the BD logo films, muted, no text.
   - First visit of a session: the reel is the splash (ends on any interaction, or after ~10 s).
   - After 3 minutes without input the reel comes back as a screensaver; any mouse move, click, key, touch or scroll returns
     to the page exactly where it was. Never starts while a film plays with sound, a dialog is open, or the tab is hidden.
   Used by bigdogma.tech (window.BD_FILMS, ids bd_*) and by the private company pages (BDReel.idle with window.DOGMA_INTRO).
   API: BDReel.splash(list), BDReel.idle(listFn, ms), BDReel.show(list), BDReel.hide(). list = [{src, poster}] */
(function () {
  if (window.BDReel) return;
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches, SAVE = navigator.connection && navigator.connection.saveData;
  const SHOW = 6500, FADE = 900;
  let el = null, vs = [], cur = 0, timer = 0, on = false, list = [], order = [], k = 0, paused = [], since = 0, mx = -1, my = -1;
  function css() {
    const s = document.createElement('style');
    s.textContent = '.bdreel{position:fixed;inset:0;z-index:200;background:#000;opacity:0;visibility:hidden;transition:opacity .7s ease,visibility .7s;cursor:none}' +
      '.bdreel.on{opacity:1;visibility:visible}.bdreel video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity ' + FADE + 'ms ease}' +
      '.bdreel video.v{opacity:1}.bdreel .sk{position:absolute;right:22px;bottom:22px;z-index:2;background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.25);color:#ddd;border-radius:999px;padding:8px 16px;font:13px system-ui,sans-serif;cursor:pointer}';
    document.head.appendChild(s);
  }
  function build() {
    if (el) return; css(); el = document.createElement('div'); el.className = 'bdreel'; el.setAttribute('aria-hidden', 'true');
    vs = [0, 1].map(() => { const v = document.createElement('video'); v.muted = v.defaultMuted = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.setAttribute('muted', ''); v.preload = 'auto'; el.appendChild(v); return v; });
    document.body.appendChild(el);
  }
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  function load(v, f) {
    v.poster = f.poster || ''; v.src = f.src;
    v.onloadedmetadata = () => { const d = v.duration || 0; if (d > SHOW / 1000 + 4) try { v.currentTime = 1 + Math.random() * (d - SHOW / 1000 - 3); } catch (e) {} };
  }
  function next() {
    if (!on || !list.length) return;
    if (k >= order.length) { order = shuffle(list); k = 0; }
    const v = vs[1 - cur], o = vs[cur]; load(v, order[k++]);
    const go = () => { v.play().catch(() => {}); v.classList.add('v'); o.classList.remove('v'); cur = 1 - cur; setTimeout(() => { if (!o.classList.contains('v')) o.pause(); }, FADE + 50);
      // a short film (the ~5 s BD logo films) plays whole and hands over just before its end; longer ones show SHOW ms
      const d = v.duration || 0; clearTimeout(timer); timer = setTimeout(next, d && d * 1000 < SHOW + 1500 ? Math.max(1500, d * 1000 - FADE / 2) : SHOW); };
    if (v.readyState >= 2) go(); else { v.oncanplay = () => { v.oncanplay = null; go(); }; }
    clearTimeout(timer); timer = setTimeout(next, SHOW + 4000);   // safety net if a film never becomes playable
  }
  function show(l, skipLabel) {
    if (on || !l || !l.length) return; build(); list = l; order = shuffle(l); k = 0; on = true; since = performance.now(); mx = my = -1;
    paused = [].slice.call(document.querySelectorAll('video')).filter(v => !el.contains(v) && !v.paused); paused.forEach(v => v.pause());
    const old = el.querySelector('.sk'); if (old) old.remove();
    if (skipLabel) { const b = document.createElement('button'); b.type = 'button'; b.className = 'sk'; b.textContent = skipLabel; b.onclick = hide; el.appendChild(b); el.style.cursor = 'default'; } else el.style.cursor = 'none';
    el.classList.add('on'); next();
  }
  function hide() {
    if (!on) return; on = false; clearTimeout(timer); el.classList.remove('on');
    setTimeout(() => { if (on) return; vs.forEach(v => { v.pause(); v.classList.remove('v'); v.removeAttribute('src'); v.load(); }); }, 800);
    paused.forEach(v => v.play().catch(() => {})); paused = []; arm();
  }
  // any real input ends the reel (a tiny pointer jitter or the move fired when the overlay appears does not)
  function input(e) {
    if (on) {
      if (performance.now() - since < 700) return;
      if (e.type === 'mousemove') { if (mx < 0) { mx = e.clientX; my = e.clientY; return; } if (Math.abs(e.clientX - mx) + Math.abs(e.clientY - my) < 12) return; }
      hide(); if (e.type === 'mousedown' || e.type === 'touchstart' || e.type === 'click') { e.preventDefault(); e.stopPropagation(); } return;
    }
    arm();
  }
  let idleMs = 0, idleT = 0, idleList = null;
  function busy() {
    if (document.hidden) return true;
    if (document.querySelector('dialog[open]')) return true;
    return [].slice.call(document.querySelectorAll('video')).some(v => !v.paused && !v.muted);
  }
  function arm() { if (!idleMs) return; clearTimeout(idleT); idleT = setTimeout(() => { if (busy()) return arm(); show(idleList()); }, idleMs); }
  ['mousemove', 'mousedown', 'keydown', 'wheel', 'touchstart', 'scroll'].forEach(t => addEventListener(t, input, { passive: false, capture: true }));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) arm(); });
  window.BDReel = {
    show, hide,
    splash(l, skipLabel, ms) { if (RM || SAVE || !l || !l.length) return false; show(l, skipLabel); setTimeout(() => { if (on && performance.now() - since >= (ms || 10000) - 50) hide(); }, ms || 10000); return true; },
    idle(fn, ms) { if (RM || SAVE) return; idleList = fn; idleMs = ms || 180000; arm(); }
  };
})();
