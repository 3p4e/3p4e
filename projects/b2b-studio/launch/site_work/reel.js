/* BIG DOGMA reel v2 (owner, 2026-11-26): full screen, all BD videos in random order (the BD logo films and the BD logo effects),
   no text. Between every two videos the header logo's transition runs at full size: the outgoing video sheds particles off the
   BD strokes in its own colour, an energy front sweeps the strokes in the incoming colour, and the videos cross underneath.
   Effect clips are placed so their mark lands exactly on the screen's mark box (bb from logo_fx/reel_bb.js); logo films fill the screen.
   - First visit of a session: the reel is the splash (ends on any interaction, or after ~12 s).
   - After 3 minutes without input it returns as a screensaver; any mouse move, click, key, touch or scroll goes back to the page.
     Never starts while a film plays with sound, a dialog is open, or the tab is hidden.
   API: BDReel.splash(list, skipLabel, ms), BDReel.idle(listFn, ms), BDReel.show(list), BDReel.hide(), BDReel.all(base, filmUrls).
   list item: {src, poster, bb?:[x,y,w,h] of the mark in the 1280x704 frame (0..1), col?:[r,g,b]} */
(function () {
  if (window.BDReel) return;
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches, SAVE = navigator.connection && navigator.connection.saveData;
  const SHOW = 5200, TR = 1300, GOLD = [242, 193, 78];
  let VB = [0, 0, 4436, 3625], SEG = [], ORD = [];
  function geo() { const M = window.DOGMA_FXMARK; if (!M || SEG.length) return; VB = M.viewBox; SEG = M.segs; ORD = SEG.map((s, i) => [Math.min(s[0], s[2]), i]).sort((a, b) => a[0] - b[0]).map(x => x[1]); }
  let el = null, vs = [], tv = null, t = null, cur = 0, on = false, list = [], order = [], k = 0, paused = [], since = 0, mx = -1, my = -1;
  let raf = 0, segEnd = 0, inT = false, swapped = false, nextItem = null, curItem = null, colOut = GOLD, colIn = GOLD, P = [], box = null;
  function css() {
    const s = document.createElement('style');
    s.textContent = '.bdreel{position:fixed;inset:0;z-index:200;background:#000;opacity:0;visibility:hidden;transition:opacity .7s ease,visibility .7s;cursor:none;overflow:hidden}' +
      '.bdreel.on{opacity:1;visibility:visible}.bdreel video{position:absolute;max-width:none;opacity:0;transition:opacity .45s ease}.bdreel video.v{opacity:1}' +
      '.bdreel video.cover{left:0;top:0;width:100%;height:100%;object-fit:cover}.bdreel canvas{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}' +
      '.bdreel .sk{position:absolute;right:22px;bottom:22px;z-index:3;background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.25);color:#ddd;border-radius:999px;padding:8px 16px;font:13px system-ui,sans-serif;cursor:pointer}';
    document.head.appendChild(s);
  }
  function build() {
    if (el) return; css(); el = document.createElement('div'); el.className = 'bdreel'; el.setAttribute('aria-hidden', 'true');
    vs = [0, 1].map(() => { const v = document.createElement('video'); v.muted = v.defaultMuted = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.setAttribute('muted', ''); v.preload = 'auto'; v.loop = true; el.appendChild(v); return v; });
    tv = document.createElement('canvas'); el.appendChild(tv); t = tv.getContext('2d');
    document.body.appendChild(el);
  }
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  // the screen's mark box (CSS px): centred, 46 % of the viewport height (narrow screens: 78 % of the width)
  function layout() {
    const W = innerWidth, H = innerHeight, ar = (VB[2] - VB[0]) / (VB[3] - VB[1]); let h = H * 0.46, w = h * ar;
    if (w > W * 0.78) { w = W * 0.78; h = w / ar; } box = { x: (W - w) / 2, y: (H - h) / 2, w, h, k: w / (VB[2] - VB[0]) };
    const d = Math.min(devicePixelRatio || 1, 2); tv.width = W * d; tv.height = H * d; t.setTransform(d, 0, 0, d, 0, 0);
  }
  function place(v, it) {   // effect clip: its mark onto the mark box; logo film: fill the screen
    const vis = v.classList.contains('v');
    if (!it.bb) { v.className = 'cover' + (vis ? ' v' : ''); v.style.cssText = ''; return; }
    v.className = vis ? 'v' : ''; const s = box.h / (it.bb[3] * 704), vw = 1280 * s, vh = 704 * s;
    v.style.cssText = `width:${vw}px;height:${vh}px;left:${box.x + box.w / 2 - (it.bb[0] + it.bb[2] / 2) * vw}px;top:${box.y + box.h / 2 - (it.bb[1] + it.bb[3] / 2) * vh}px`;
  }
  function load(v, it) { v.poster = it.poster || ''; v.src = it.src; v.load(); place(v, it); }
  function pick() { if (k >= order.length) { order = shuffle(list); k = 0; } return order[k++]; }
  // ---- the header transition, full size
  const pt = (s, u) => [box.x + (s[0] + (s[2] - s[0]) * u - VB[0]) * box.k, box.y + (s[1] + (s[3] - s[1]) * u - VB[1]) * box.k];
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  function spawn() { P = []; for (let i = 0; i < 420 && SEG.length; i++) { const s = SEG[i % SEG.length], p = pt(s, Math.random()); P.push({ x: p[0], y: p[1], a: Math.random() * 6.283, sp: .4 + Math.random(), r: .8 + Math.random() * 2.2, ph: Math.random() }); } }
  function trans(q) {
    const W = innerWidth, H = innerHeight, u = box.h / 300; t.clearRect(0, 0, W, H); t.globalCompositeOperation = 'lighter';
    const out = Math.max(0, 1 - q / .55), inn = Math.max(0, (q - .45) / .55);
    P.forEach(p => {
      if (out > 0) { const dd = (1 - out) * 60 * u * p.sp; t.fillStyle = rgba(colOut, out * .9); t.beginPath(); t.arc(p.x + Math.cos(p.a) * dd, p.y + Math.sin(p.a) * dd - (1 - out) * 26 * u, p.r * u, 0, 6.283); t.fill(); }
      if (inn > 0) { const di = (1 - inn) * 70 * u * p.sp; t.fillStyle = rgba(colIn, inn * (1 - inn) * 3); t.beginPath(); t.arc(p.x - Math.cos(p.a + p.ph) * di, p.y - Math.sin(p.a + p.ph) * di, p.r * u * .9, 0, 6.283); t.fill(); }
    });
    const front = Math.min(1, q / .62) * (ORD.length + 8), lw = Math.max(3, 58 * box.k); t.lineCap = 'round'; t.shadowBlur = Math.max(14, box.h / 14);   // bolder than the header: full-screen size
    for (let j = 0; j < ORD.length; j++) {
      const age = front - j; if (age <= 0) break; const s = SEG[ORD[j]];
      const g = Math.max(0, 1 - age / 8) + .35 * Math.sin(Math.PI * Math.min(1, q * 1.3)) * (q < .8 ? 1 : (1 - q) / .2); if (g <= .01) continue;
      const a = pt(s, 0), b = pt(s, 1), mix = Math.min(1, age / 4), col = colIn.map(c => c * mix + 255 * (1 - mix) | 0);
      t.shadowColor = rgba(colIn, 1); t.strokeStyle = rgba(col, Math.min(1, g)); t.lineWidth = lw * (.6 + .5 * Math.max(0, 1 - age / 6));
      t.beginPath(); t.moveTo(a[0], a[1]); t.lineTo(b[0], b[1]); t.stroke();
    }
    t.shadowBlur = 0; t.globalCompositeOperation = 'source-over';
  }
  function swap() {   // the incoming video (loaded and started at the transition's start) becomes current
    const v = vs[1 - cur], o = vs[cur]; v.classList.add('v'); o.classList.remove('v'); cur = 1 - cur; curItem = nextItem;
    setTimeout(() => { if (!o.classList.contains('v')) o.pause(); }, 600);
  }
  // a logo film plays whole (it ends on the formed logo); an effect loop shows SHOW ms
  function startSeg(now) { const v = vs[cur], d = v.duration || 0; segEnd = now + (curItem && !curItem.bb && d ? Math.max(3000, d * 1000 - 300) - (performance.now() - now) : SHOW); swapped = false; }
  function frame(now) {
    raf = requestAnimationFrame(frame); if (!on) return;
    const left = segEnd - now;
    if (left <= TR) {
      if (!inT) { inT = true; nextItem = pick(); const v = vs[1 - cur]; v.loop = !!nextItem.bb; load(v, nextItem); v.currentTime = 0; v.play().catch(() => {});
        colOut = (curItem && curItem.col) || GOLD; colIn = nextItem.col || GOLD; spawn(); }
      const q = Math.min(1, 1 - left / TR); trans(q);
      if (q >= .5 && !swapped) { swapped = true; swap(); }
      if (left <= 0) { inT = false; t.clearRect(0, 0, innerWidth, innerHeight); startSeg(now + TR / 2); }   // the new video started TR/2 ago
    }
  }
  function show(l, skipLabel) {
    if (on || !l || !l.length) return; geo(); build(); layout(); list = l; order = shuffle(l); k = 0; on = true; since = performance.now(); mx = my = -1; inT = false;
    paused = [].slice.call(document.querySelectorAll('video')).filter(v => !el.contains(v) && !v.paused); paused.forEach(v => v.pause());
    const old = el.querySelector('.sk'); if (old) old.remove();
    if (skipLabel) { const b = document.createElement('button'); b.type = 'button'; b.className = 'sk'; b.textContent = skipLabel; b.onclick = hide; el.appendChild(b); el.style.cursor = 'default'; } else el.style.cursor = 'none';
    vs.forEach(v => v.classList.remove('v')); curItem = pick(); const v = vs[cur]; v.loop = !!curItem.bb; load(v, curItem); v.classList.add('v'); v.play().catch(() => {});
    el.classList.add('on'); segEnd = performance.now() + SHOW;
    if (!curItem.bb) v.onloadedmetadata = () => { v.onloadedmetadata = null; if (on && !inT) startSeg(performance.now()); };
    cancelAnimationFrame(raf); raf = requestAnimationFrame(frame);
  }
  function hide() {
    if (!on) return; on = false; cancelAnimationFrame(raf); el.classList.remove('on'); if (t) t.clearRect(0, 0, innerWidth, innerHeight);
    setTimeout(() => { if (on) return; vs.forEach(v => { v.pause(); v.classList.remove('v'); v.removeAttribute('src'); v.load(); }); }, 800);
    paused.forEach(v => v.play().catch(() => {})); paused = []; arm();
  }
  addEventListener('resize', () => { if (on) { layout(); vs.forEach((v, i) => { const it = i === cur ? curItem : nextItem; if (it) place(v, it); }); } });
  // any real input ends the reel (a tiny pointer jitter or the move fired when the overlay appears does not)
  function input(e) {
    if (on) {
      if (performance.now() - since < 700) return;
      if (e.type === 'mousemove') { if (mx < 0) { mx = e.clientX; my = e.clientY; return; } if (Math.abs(e.clientX - mx) + Math.abs(e.clientY - my) < 12) return; }
      hide(); if (e.type === 'mousedown' || e.type === 'touchstart') { e.preventDefault(); e.stopPropagation(); } return;
    }
    arm();
  }
  let idleMs = 0, idleT = 0, idleList = null;
  function busy() {
    if (document.hidden || document.querySelector('dialog[open]')) return true;
    return [].slice.call(document.querySelectorAll('video')).some(v => !v.paused && !v.muted);
  }
  function arm() { if (!idleMs) return; clearTimeout(idleT); idleT = setTimeout(() => { if (busy()) return arm(); show(idleList()); }, idleMs); }
  ['mousemove', 'mousedown', 'keydown', 'wheel', 'touchstart', 'scroll'].forEach(ty => addEventListener(ty, input, { passive: false, capture: true }));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) arm(); });
  window.BDReel = {
    show, hide,
    splash(l, skipLabel, ms) { if (RM || SAVE || !l || !l.length) return false; show(l, skipLabel); setTimeout(() => { if (on && performance.now() - since >= (ms || 12000) - 50) hide(); }, ms || 12000); return true; },
    idle(fn, ms) { if (RM || SAVE) return; idleList = fn; idleMs = ms || 180000; arm(); },
    // all BD videos: the logo films (URLs given) + every logo effect in logo_fx/reel_bb.js; base = the site root URL ('' on bigdogma.tech)
    all(base, films) {
      const fx = (window.DOGMA_REEL_FX || []).map(x => ({ src: base + 'media/bd/' + x.id + '.mp4', poster: base + 'media/bd/' + x.id + '.jpg', bb: x.bb, col: x.col }));
      return films.map(u => ({ src: u, poster: u.replace(/\.mp4(\?.*)?$/, '.jpg') })).concat(fx);
    }
  };
})();
