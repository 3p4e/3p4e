/* BIG DOGMA logo FX engine: a transparent, frameless canvas that cycles 50+ animations of the tattoo mark.
   Needs window.DOGMA_FXMARK (mark_data.js: exact path, viewBox, stroke centre lines grouped by triangle 0 = B top, 1 = B bottom, 2 = D).
   Families: STENCIL (the lines are the only openings; elemental light flows behind them), LINE (the strokes move: fold, scatter,
   stick-men fight, ...), MAGIC (bursts and enchantments on the lines), TEXT (the wordmark joins in).
   Every animation starts and ends on the exact mark, so they chain seamlessly.
   Usage: DogmaLogoFX.mount(element, {color:'#f2c14e', text:'BIG DOGMA', font:'Russo One', mode:'sequence'|'random', only:[names], dur:1})
*/
(function () {
  'use strict';
  const M = window.DOGMA_FXMARK; if (!M) { console.warn('DogmaLogoFX: mark_data.js missing'); return; }
  const VB = M.viewBox, SEGS = M.segs, TRIS = M.tris, TAU = Math.PI * 2;
  const clamp = (v, a = 0, b = 1) => v < a ? a : v > b ? b : v, lerp = (a, b, t) => a + (b - a) * t;
  const ss = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, easeOutBack = t => { const c = 1.7; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
  // ---------- seeded random + value noise ----------
  let seed = 1; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647; const rr = (a, b) => a + (b - a) * rnd();
  const PERM = new Uint8Array(512); (function () { const p = [...Array(256).keys()]; let s = 7; for (let i = 255; i > 0; i--) { s = (s * 16807) % 2147483647; const j = s % (i + 1); [p[i], p[j]] = [p[j], p[i]]; } for (let i = 0; i < 512; i++) PERM[i] = p[i & 255]; })();
  function vn(x, y) {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const h = (i, j) => PERM[(PERM[i & 255] + j) & 255] / 255;
    return lerp(lerp(h(xi, yi), h(xi + 1, yi), u), lerp(h(xi, yi + 1), h(xi + 1, yi + 1), u), v);
  }
  function fbm(x, y, o = 4) { let a = .5, s = 0; for (let i = 0; i < o; i++) { s += a * vn(x, y); x = x * 2.03 + 17.1; y = y * 2.03 + 3.7; a *= .5; } return s / (1 - Math.pow(.5, o)); }
  function lut(stops) { const L = new Uint8ClampedArray(256 * 3); for (let i = 0; i < 256; i++) { const t = i / 255; let k = 0; while (k < stops.length - 2 && t > stops[k + 1][0]) k++; const [t0, c0] = stops[k], [t1, c1] = stops[k + 1]; const f = clamp((t - t0) / (t1 - t0)); for (let c = 0; c < 3; c++) L[i * 3 + c] = lerp(c0[c], c1[c], f); } return L; }
  const hsl = (h, s, l, a = 1) => `hsla(${h},${s}%,${l}%,${a})`;

  // ---------- engine ----------
  class FX {
    constructor(el, o) {
      this.o = Object.assign({ color: '#f2c14e', text: 'BIG DOGMA', font: 'Russo One', mode: 'sequence', only: null, skip: null, res: 150, dur: 1, pad: .08, textRoom: .13, onchange: null }, o || {});
      if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
      this.cv = document.createElement('canvas'); this.cv.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;background:transparent;pointer-events:none';
      this.cv.setAttribute('aria-hidden', 'true'); el.appendChild(this.cv); this.c = this.cv.getContext('2d');
      this.off = document.createElement('canvas'); this.oc = this.off.getContext('2d');
      this.fc = document.createElement('canvas'); this.fcx = this.fc.getContext('2d');
      this.path = new Path2D(M.d); this.list = EFFECTS.filter(e => (!this.o.only || this.o.only.includes(e.name)) && !(this.o.skip || []).includes(e.cat) && !(this.o.skip || []).includes(e.name));
      this.i = -1; this.next(); this.ro = new ResizeObserver(() => this.resize()); this.ro.observe(el); this.resize();
      this.reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!this.o.paused) this.raf = requestAnimationFrame(t => this.frame(t));
      document.addEventListener('visibilitychange', () => { if (!document.hidden) this.t0 = performance.now() - this.el * 1000; });
    }
    resize() {
      const r = this.cv.getBoundingClientRect(), d = Math.min(2, window.devicePixelRatio || 1);
      this.W = this.cv.width = this.off.width = Math.max(2, Math.round(r.width * d)); this.H = this.cv.height = this.off.height = Math.max(2, Math.round(r.height * d)); this.dpr = d;
      const tr = this.o.text ? this.o.textRoom : 0, padY = this.o.padY ?? this.o.pad, aw = this.W * (1 - 2 * this.o.pad), ah = this.H * (1 - 2 * padY - tr);
      this.k = Math.min(aw / VB[2], ah / VB[3]); this.bw = VB[2] * this.k; this.bh = VB[3] * this.k;
      this.ox = (this.W - this.bw) / 2; this.oy = (this.H * (1 - tr) - this.bh) / 2 + (tr ? this.H * padY * .25 : 0);
      this.ty = this.oy + this.bh + this.H * tr * .55; this.ts = Math.min(this.H * tr * .5, this.W * .085);
      if (this.o.paused && this.e && this.lastNow != null) this.draw(this.lastNow);   // resizing clears the canvas
    }
    next(i) {
      const n = this.list.length; this.i = i != null ? (i + n) % n : this.o.mode === 'random' ? Math.floor(Math.random() * n) : (this.i + 1) % n;
      this.e = this.list[this.i]; this.t0 = performance.now(); this.el = 0; seed = 1 + this.i * 7919; this.st = {};
      if (this.o.onchange) this.o.onchange(this.e, this.i, n);
    }
    pause() { cancelAnimationFrame(this.raf); this.raf = 0; this.c.setTransform(1, 0, 0, 1, 0, 0); this.c.clearRect(0, 0, this.W, this.H); }   // hand the slot to another player
    resume() { if (this.raf) return; this.next(); this.raf = requestAnimationFrame(t => this.frame(t)); }
    mt(c) { c.setTransform(this.k, 0, 0, this.k, this.ox - VB[0] * this.k, this.oy - VB[1] * this.k); }   // mark units -> device px
    renderAt(i, sec) { this.resize(); this.next(i); this.t0 = 0; this.draw(sec * 1000); }        // deterministic frame for QC / thumbnails
    frame(now) {
      this.raf = requestAnimationFrame(t => this.frame(t));
      const e = this.e, dur = (e.dur || 7) * this.o.dur; this.el = (now - this.t0) / 1000;
      if (this.el >= dur) { this.next(); return; }
      this.draw(now);
    }
    draw(now) {
      this.lastNow = now; const e = this.e, dur = (e.dur || 7) * this.o.dur; this.el = (now - this.t0) / 1000;
      const c = this.c; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, this.W, this.H);
      const p = this.el / dur, env = { fx: this, c, t: this.el, p, dur, W: this.W, H: this.H, k: this.k, st: this.st,
        f: ss(0, .13, p) * (1 - ss(.86, 1, p)),                     // effect intensity envelope (0 at both ends)
        m: ss(.04, .22, p) * (1 - ss(.78, .96, p)) };                // motion envelope for line effects
      if (this.reduce) { this.mark(1); return; }
      c.save(); e.draw(env); c.restore();
    }
    // --- drawing helpers ---
    mark(a = 1, col, c = this.c, glow = 0) {
      if (a <= 0) return; c.save(); this.mt(c); c.globalAlpha = a; c.fillStyle = col || this.o.color;
      if (glow) { c.shadowColor = col || this.o.color; c.shadowBlur = glow * this.dpr; }
      c.fill(this.path, 'evenodd'); c.restore();
    }
    // paint(oc) draws light in device px; it is cut to the mark lines, then composited with a glow
    stencil(env, paint, glowCol = '#fff', glow = 16, under = .18) {
      const o = this.oc; o.setTransform(1, 0, 0, 1, 0, 0); o.globalCompositeOperation = 'source-over'; o.globalAlpha = 1; o.clearRect(0, 0, this.W, this.H);
      paint(o); o.globalCompositeOperation = 'destination-in'; this.mt(o); o.fill(this.path, 'evenodd');
      o.setTransform(1, 0, 0, 1, 0, 0); o.globalCompositeOperation = 'source-over';
      this.mark(Math.max(this.o.minMark || 0, 1 - env.f + env.f * under));   // header: keep the mark readable at small sizes
      const c = env.c; c.save(); c.globalAlpha = env.f; c.shadowColor = glowCol; c.shadowBlur = glow * this.dpr; c.drawImage(this.off, 0, 0);
      c.shadowBlur = 0; c.globalCompositeOperation = 'lighter'; c.globalAlpha = env.f * .35; c.drawImage(this.off, 0, 0); c.restore();
    }
    // low-res per-pixel field over the mark box; fn(u, v, t, out) writes r,g,b,a (0..255) into out
    field(o, fn, t, res) {
      const w = Math.min(res || 150, this.o.res), h = Math.max(8, Math.round(res * this.bh / this.bw)), F = this.fc;
      if (F.width !== w || F.height !== h) { F.width = w; F.height = h; this.img = this.fcx.createImageData(w, h); }
      const d = this.img.data, out = [0, 0, 0, 255]; let i = 0;
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { out[3] = 255; fn(x / w, y / h, t, out); d[i] = out[0]; d[i + 1] = out[1]; d[i + 2] = out[2]; d[i + 3] = out[3]; i += 4; }
      this.fcx.putImageData(this.img, 0, 0); o.imageSmoothingEnabled = true; o.drawImage(F, this.ox, this.oy, this.bw, this.bh);
    }
    // stroke segments with a per-segment transform; tf(s, i) -> {x, y, r, l, a, col, w} (mid point in mark units, rotation, length scale)
    segs(env, tf, base = this.o.color, glow = 0) {
      const c = env.c; c.save(); this.mt(c); c.lineCap = 'round';
      if (glow) { c.shadowBlur = glow * this.dpr; }
      SEGS.forEach((s, i) => {
        const mx = (s[0] + s[2]) / 2, my = (s[1] + s[3]) / 2, hx = (s[2] - s[0]) / 2, hy = (s[3] - s[1]) / 2;
        const q = tf(s, i, mx, my) || {}; if ((q.a ?? 1) <= 0) return;
        const r = q.r || 0, l = q.l ?? 1, cs = Math.cos(r), sn = Math.sin(r), X = q.x ?? mx, Y = q.y ?? my;
        const ex = (hx * cs - hy * sn) * l, ey = (hx * sn + hy * cs) * l;
        c.globalAlpha = q.a ?? 1; c.strokeStyle = q.col || base; if (glow) c.shadowColor = q.col || base; c.lineWidth = (q.w ?? s[5]);
        c.beginPath(); c.moveTo(X - ex, Y - ey); c.lineTo(X + ex, Y + ey); c.stroke();
      });
      c.restore();
    }
    skin(i) {
      const L = window.DOGMA_SKINS; if (!L || !L.length) return null; i = ((i % L.length) + L.length) % L.length;
      const k = L[i]; if (!k.p) k.p = new Path2D(k.d); return k;
    }
    // draw variant i (falls back to the main mark) in mark units; sx = horizontal squash for flips
    drawSkin(i, a = 1, col, c = this.c, sx = 1, glow = 0) {
      const k = this.skin(i); if (!k) return this.mark(a, col, c, glow);
      if (a <= 0) return; c.save(); this.mt(c); const cx = VB[0] + VB[2] / 2, cy = VB[1] + VB[3] / 2, s = Math.min(VB[2] / k.vb[2], VB[3] / k.vb[3]);
      c.translate(cx, cy); c.scale(s * sx, s); c.translate(-(k.vb[0] + k.vb[2] / 2), -(k.vb[1] + k.vb[3] / 2));
      c.globalAlpha = a; c.fillStyle = col || this.o.color; if (glow) { c.shadowColor = col || this.o.color; c.shadowBlur = glow * this.dpr; }
      c.fill(k.p, 'evenodd'); c.restore();
    }
    skinIndex(name) { const L = window.DOGMA_SKINS || []; const i = L.findIndex(k => k.name === name); return i < 0 ? 0 : i; }
    // exact mark while still, segments while moving
    lines(env, tf, base, glow) { const m = env.m; this.mark(1 - ss(0, .08, m)); if (m > 0) { const c = env.c; c.save(); c.globalAlpha = ss(0, .08, m); this.segs(env, tf, base, glow); c.restore(); } }
    text(env, a = 1, col, opts = {}) {
      if (!this.o.text || a <= 0) return; const c = env.c; c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = a;
      c.font = `${opts.size || this.ts}px "${this.o.font}", Impact, sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.letterSpacing && (c.letterSpacing = `${this.ts * .12}px`);
      if (opts.glow) { c.shadowColor = opts.glow; c.shadowBlur = 18 * this.dpr; }
      c.fillStyle = col || '#fff'; const s = opts.sub != null ? this.o.text.slice(0, opts.sub) : this.o.text; c.fillText(s, this.W / 2 + (opts.dx || 0), this.ty + (opts.dy || 0)); c.restore();
    }
    // mark-unit <-> device px
    px(x, y) { return [this.ox + (x - VB[0]) * this.k, this.oy + (y - VB[1]) * this.k]; }
  }
  const tri = g => TRIS[g], DC = TRIS[2];                    // D triangle box/centroid
  const segCol = (s, h) => hsl(h, 90, 62);

  // ---------- effects ----------
  const EFFECTS = [];
  const add = (name, cat, draw, dur = 7) => EFFECTS.push({ name, cat, draw, dur });

  // ===== STENCIL LIGHT (light passes only through the lines) =====
  const LAVA = lut([[0, [20, 0, 0]], [.35, [140, 10, 0]], [.6, [255, 80, 0]], [.8, [255, 180, 20]], [1, [255, 250, 200]]]);
  add('Lava flow', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const n = fbm(u * 5 + t * .25, v * 4 - t * .6, 4) * .8 + fbm(u * 9 - t * .4, v * 9, 2) * .35; const i = (clamp(n * 1.25 - .25) * 255) | 0; r[0] = LAVA[i * 3]; r[1] = LAVA[i * 3 + 1]; r[2] = LAVA[i * 3 + 2]; }, E.t), '#ff5a00', 22));
  const WATER = lut([[0, [0, 30, 70]], [.5, [0, 120, 200]], [.8, [80, 210, 255]], [1, [230, 255, 255]]]);
  add('Water caustics', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const a = Math.sin(u * 22 + t * 2 + Math.sin(v * 9 + t)) + Math.sin(v * 25 - t * 1.6 + Math.sin(u * 7 - t * .7)) + Math.sin((u + v) * 18 + t * 2.4); const c = Math.pow(clamp((a + 3) / 6), 2.2); const i = (c * 255) | 0; r[0] = WATER[i * 3]; r[1] = WATER[i * 3 + 1]; r[2] = WATER[i * 3 + 2]; }, E.t), '#3cc8ff', 18));
  const ICE = lut([[0, [10, 40, 80]], [.5, [120, 200, 255]], [.85, [220, 245, 255]], [1, [255, 255, 255]]]);
  add('Ice crystals', 'stencil', E => { const P = E.st.p || (E.st.p = Array.from({ length: 26 }, () => [rnd(), rnd(), rr(-.03, .03), rr(-.03, .03)]));
    E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { let d1 = 9, d2 = 9; for (const q of P) { const dx = u - (q[0] + q[2] * t), dy = (v - (q[1] + q[3] * t)) * .8, d = dx * dx + dy * dy; if (d < d1) { d2 = d1; d1 = d; } else if (d < d2) d2 = d; } const e = clamp(1 - (Math.sqrt(d2) - Math.sqrt(d1)) * 9); const i = (clamp(e * .9 + Math.sin(t * 3 + u * 30) * .05 + .1) * 255) | 0; r[0] = ICE[i * 3]; r[1] = ICE[i * 3 + 1]; r[2] = ICE[i * 3 + 2]; }, E.t, 120), '#bfe9ff', 20); });
  add('Wind streaks', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = 'rgba(30,60,90,1)'; o.fillRect(0, 0, W, H); o.lineCap = 'round';
    for (let i = 0; i < 90; i++) { const sp = .25 + (i % 7) * .07, y = ((i * 97) % 100) / 100 * H, x = ((i * 53) % 100 / 100 + E.t * sp) % 1.4 * W * 1.1 - W * .2, len = W * (.08 + (i % 5) * .04);
      o.strokeStyle = `rgba(220,245,255,${.25 + (i % 4) * .18})`; o.lineWidth = (1 + (i % 3)) * E.fx.dpr * 1.5; o.beginPath(); o.moveTo(x, y + Math.sin(E.t * 2 + i) * 6); o.quadraticCurveTo(x + len * .5, y - 10, x + len, y + Math.sin(E.t * 2 + i + 1) * 6); o.stroke(); } }, '#dff6ff', 12));
  const FIRE = lut([[0, [0, 0, 0]], [.3, [120, 0, 0]], [.55, [255, 60, 0]], [.78, [255, 170, 0]], [1, [255, 255, 210]]]);
  add('Fire', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const n = fbm(u * 6, v * 3 + t * 1.6, 4); const h = clamp((v * 1.25 - .15) + n * .65 - .35); const i = (h * h * 255) | 0; r[0] = FIRE[i * 3]; r[1] = FIRE[i * 3 + 1]; r[2] = FIRE[i * 3 + 2]; }, E.t), '#ff7a00', 24));
  function bolt(o, x1, y1, x2, y2, d, w) { if (d <= 0) { o.lineWidth = w; o.beginPath(); o.moveTo(x1, y1); o.lineTo(x2, y2); o.stroke(); return; } const mx = (x1 + x2) / 2 + rr(-1, 1) * Math.hypot(x2 - x1, y2 - y1) * .22, my = (y1 + y2) / 2 + rr(-1, 1) * Math.hypot(x2 - x1, y2 - y1) * .22; bolt(o, x1, y1, mx, my, d - 1, w); bolt(o, mx, my, x2, y2, d - 1, w); if (rnd() < .25) bolt(o, mx, my, mx + rr(-1, 1) * 80, my + rr(0, 1) * 120, d - 2, w * .6); }
  add('Lightning', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#3a2a8a'; o.fillRect(0, 0, W, H); const k = Math.floor(E.t * 7); seed = 99 + k;
    if (rnd() < .7) { o.strokeStyle = '#e8dcff'; o.shadowColor = '#9f7bff'; o.shadowBlur = 20; for (let b = 0; b < 3; b++) bolt(o, rr(0, W), 0, rr(0, W), H, 7, 4 * E.fx.dpr); o.shadowBlur = 0; o.fillStyle = `rgba(180,150,255,${rnd() * .35})`; o.fillRect(0, 0, W, H); } }, '#b9a0ff', 26, .25));
  add('Shooting star', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E, hue = (E.t * 50 + 200) % 360; o.fillStyle = hsl(hue + 180, 55, 26); o.fillRect(0, 0, W, H);
    for (let s = 0; s < 3; s++) { const q = ((E.t / 2.2 + s / 3) % 1), x = lerp(-W * .2, W * 1.2, q), y = lerp(H * (.1 + s * .3), H * (.5 + s * .2), q), hh = (hue + s * 120) % 360;
      const g = o.createLinearGradient(x - W * .45, y - H * .2, x, y); g.addColorStop(0, hsl(hh, 100, 60, 0)); g.addColorStop(1, hsl(hh, 100, 75, 1)); o.strokeStyle = g; o.lineWidth = H * .05; o.lineCap = 'round'; o.beginPath(); o.moveTo(x - W * .45, y - H * .2); o.lineTo(x, y); o.stroke();
      const r = o.createRadialGradient(x, y, 0, x, y, H * .22); r.addColorStop(0, '#fff'); r.addColorStop(.25, hsl(hh, 100, 70, .9)); r.addColorStop(1, hsl(hh, 100, 50, 0)); o.fillStyle = r; o.fillRect(x - H * .22, y - H * .22, H * .44, H * .44); } }, '#fff', 20, .22));
  add('Aurora', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const w1 = Math.sin(u * 7 + t * .9 + fbm(u * 3, t * .2) * 4) * .5 + .5, b = Math.exp(-Math.pow((v - .3 - w1 * .4) * 4, 2)); const g = fbm(u * 12 + t * .3, v * 2, 2); r[0] = 40 + 160 * b * (1 - u); r[1] = 60 + 195 * b * g * 1.3; r[2] = 90 + 150 * b * u; }, E.t), '#5dffb0', 22, .2));
  add('Rainbow sweep', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E, a = E.t * .8; const g = o.createLinearGradient(W / 2 - Math.cos(a) * W, H / 2 - Math.sin(a) * W, W / 2 + Math.cos(a) * W, H / 2 + Math.sin(a) * W); for (let i = 0; i <= 12; i++) g.addColorStop(i / 12, hsl((i * 30 + E.t * 90) % 360, 100, 60)); o.fillStyle = g; o.fillRect(0, 0, W, H); }, '#fff', 14));
  add('Gold shimmer', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; const x = lerp(-.3, 1.3, (E.t / 2.3) % 1) * W; const g = o.createLinearGradient(x - W * .3, 0, x + W * .3, H * .4); g.addColorStop(0, '#6b4a10'); g.addColorStop(.42, '#c9922a'); g.addColorStop(.5, '#fff6cf'); g.addColorStop(.58, '#e0aa3e'); g.addColorStop(1, '#6b4a10'); o.fillStyle = g; o.fillRect(0, 0, W, H); }, '#ffd36b', 16, .3));
  add('Plasma', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const a = Math.sin(u * 10 + t) + Math.sin(v * 10 + t * 1.3) + Math.sin((u + v) * 10 + t * .7) + Math.sin(Math.hypot(u - .5, v - .5) * 18 - t * 2); r[0] = 128 + 127 * Math.sin(a * Math.PI); r[1] = 128 + 127 * Math.sin(a * Math.PI + 2.1); r[2] = 128 + 127 * Math.sin(a * Math.PI + 4.2); }, E.t), '#ff6bd6', 18));
  add('Nebula', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const n = fbm(u * 3 + t * .1, v * 3 - t * .05, 5), m = fbm(u * 5 - t * .07 + 9, v * 5, 3); const st = vn(u * 140, v * 140) > .985 ? 255 * (.6 + .4 * Math.sin(t * 5 + u * 99)) : 0; r[0] = Math.min(255, 255 * n * n * 1.4 + st); r[1] = Math.min(255, 60 * m + st); r[2] = Math.min(255, 255 * m * 1.1 + 40 + st); }, E.t, 170), '#b06bff', 22, .2));
  add('Matrix rain', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E, fs = Math.max(10, H / 26), cols = Math.ceil(W / fs), ch = 'BIGDOGMA▲△◢◣'; o.fillStyle = '#04501f'; o.fillRect(0, 0, W, H); o.font = `bold ${fs}px monospace`;
    for (let i = 0; i < cols; i++) { const sp = 3 + (i * 7) % 5, hd = ((E.t * sp + i * 1.7) % 30) * fs; for (let j = 0; j < 14; j++) { const y = hd - j * fs; if (y < -fs || y > H + fs) continue; o.fillStyle = j ? `rgba(40,255,120,${1 - j / 14})` : '#d8ffe8'; o.fillText(ch[(i * 3 + j + Math.floor(E.t * 8)) % ch.length], i * fs, y); } } }, '#2dff7a', 14, .25));
  add('Neon pulse', 'stencil', E => { const h = (E.t * 60) % 360, b = .5 + .5 * Math.sin(E.t * 6); E.fx.stencil(E, o => { o.fillStyle = hsl(h, 100, 55 + b * 20); o.fillRect(0, 0, E.W, E.H); }, hsl(h, 100, 60), 18 + b * 30, .1); });
  add('Laser scan', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#200006'; o.fillRect(0, 0, W, H); for (const k of [0, .5]) { const y = ((E.t / 1.6 + k) % 1) * H; const g = o.createLinearGradient(0, y - H * .12, 0, y + H * .02); g.addColorStop(0, 'rgba(255,0,40,0)'); g.addColorStop(.85, 'rgba(255,40,60,.9)'); g.addColorStop(1, '#fff'); o.fillStyle = g; o.fillRect(0, y - H * .12, W, H * .14); } }, '#ff2040', 22, .2));
  add('Ocean waves', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#bfefff'; o.fillRect(0, 0, W, H); for (let l = 0; l < 5; l++) { const lvl = H * (.35 + l * .13 + .08 * Math.sin(E.t * .8 + l)); o.fillStyle = `rgba(${10 + l * 8},${90 + l * 25},${170 + l * 15},.85)`; o.beginPath(); o.moveTo(0, H); for (let x = 0; x <= W; x += W / 60) o.lineTo(x, lvl + Math.sin(x / W * 9 + E.t * (1.2 + l * .3) + l) * H * .03 + Math.sin(x / W * 23 - E.t * 2) * H * .01); o.lineTo(W, H); o.fill(); } }, '#46c3ff', 16));
  add('Sunrise', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E, sy = lerp(H * .9, H * .2, ss(0, .45, E.p)); const g = o.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#2b1b5a'); g.addColorStop(.6, '#ff6a5b'); g.addColorStop(1, '#ffc46b'); o.fillStyle = g; o.fillRect(0, 0, W, H);
    o.save(); o.translate(W / 2, sy); for (let i = 0; i < 18; i++) { o.rotate(TAU / 18 + E.t * .02); o.fillStyle = 'rgba(255,230,160,.25)'; o.beginPath(); o.moveTo(0, 0); o.lineTo(W, -W * .06); o.lineTo(W, W * .06); o.fill(); } o.restore(); const r = o.createRadialGradient(W / 2, sy, 0, W / 2, sy, H * .3); r.addColorStop(0, '#fffbe0'); r.addColorStop(.5, '#ffd27a'); r.addColorStop(1, 'rgba(255,150,60,0)'); o.fillStyle = r; o.fillRect(0, 0, W, H); }, '#ffb35a', 20));
  add('Toxic bubbles', 'stencil', E => E.fx.stencil(E, o => { E.fx.field(o, (u, v, t, r) => { const n = fbm(u * 6, v * 6 + t * .5, 3); r[0] = 40 + 90 * n; r[1] = 160 + 95 * n; r[2] = 20; }, E.t, 110);
    for (let i = 0; i < 40; i++) { const x = ((i * 0.618) % 1) * E.W, y = E.H - ((E.t * (40 + i % 9 * 12) + i * 37) % (E.H * 1.2)), rr2 = (4 + (i % 5) * 4) * E.fx.dpr; o.strokeStyle = 'rgba(230,255,180,.9)'; o.lineWidth = 2 * E.fx.dpr; o.beginPath(); o.arc(x + Math.sin(E.t * 3 + i) * 8, y, rr2, 0, TAU); o.stroke(); } }, '#9dff2e', 22));
  add('Smoke', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const n = fbm(u * 3 + fbm(u * 2, v * 2 + t * .2) * 2, v * 3 - t * .35, 5); const g = 70 + 185 * n * n; r[0] = g; r[1] = g * .98; r[2] = g * 1.02; }, E.t), '#e8e8ef', 14, .3));
  add('Sandstorm', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#8a5a22'; o.fillRect(0, 0, W, H); for (let i = 0; i < 700; i++) { const x = ((i * 0.7548 + E.t * (0.15 + (i % 13) * .02)) % 1) * W, y = ((i * 0.5698) % 1) * H + Math.sin(E.t * 2 + i) * 10; o.fillStyle = `rgba(255,${200 + i % 50},${120 + i % 60},${.4 + (i % 5) * .12})`; o.fillRect(x, y, 2.5 * E.fx.dpr, 2.5 * E.fx.dpr); } }, '#ffcf80', 12, .3));
  add('Molten gold pour', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E, lv = lerp(H * 1.05, H * -.05, ss(.05, .55, E.p)) + lerp(0, H * 1.1, ss(.7, .95, E.p)); o.fillStyle = '#2a1600'; o.fillRect(0, 0, W, H);
    const g = o.createLinearGradient(0, lv, 0, H); g.addColorStop(0, '#fff3b0'); g.addColorStop(.1, '#ffc23a'); g.addColorStop(1, '#a86800'); o.fillStyle = g; o.beginPath(); o.moveTo(0, H); for (let x = 0; x <= W; x += W / 50) o.lineTo(x, lv + Math.sin(x / W * 12 + E.t * 3) * H * .015); o.lineTo(W, H); o.fill(); }, '#ffc23a', 22, .25));
  add('Ink bloom', 'stencil', E => { const hue = (E.st.h ??= rr(0, 360)); E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const n = fbm(u * 4, v * 4, 4), g = Math.hypot(u - .5, v - .5); const a = clamp((ss(0, .6, E.p) * 1.1 - g - n * .35 + .3) * 6); const [R, G, B] = [Math.sin(hue / 57) * 127 + 128, Math.sin(hue / 57 + 2) * 127 + 128, Math.sin(hue / 57 + 4) * 127 + 128]; r[0] = lerp(240, R * .5, a); r[1] = lerp(240, G * .5, a); r[2] = lerp(245, B * .5, a); }, E.t, 130), '#ffffff', 14, .25); });
  add('Kintsugi veins', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const n = Math.abs(fbm(u * 5, v * 5, 4) - .5) * 2, vein = clamp(1 - n * 8), sweep = ss(-.2, .1, ((u + v * .5) - E.p * 1.6)) * (1 - ss(.1, .4, (u + v * .5) - E.p * 1.6)); r[0] = 30 + 225 * vein + 80 * sweep; r[1] = 25 + 180 * vein + 60 * sweep; r[2] = 20 + 60 * vein; }, E.t, 160), '#ffcf5a', 18, .25));
  add('Electric arcs', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#04061a'; o.fillRect(0, 0, W, H); seed = 5 + Math.floor(E.t * 14); o.strokeStyle = '#a8f0ff'; o.shadowColor = '#38d9ff'; o.shadowBlur = 16;
    const [cx, cy] = E.fx.px(DC.cx, DC.cy); for (let i = 0; i < 7; i++) { const s = SEGS[(rnd() * SEGS.length) | 0], [x, y] = E.fx.px(s[0], s[1]); bolt(o, cx, cy, x, y, 5, 2.5 * E.fx.dpr); } o.shadowBlur = 0; }, '#5fe2ff', 22, .25));
  add('Blood moon', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E, mx = lerp(W * .1, W * .9, E.p); o.fillStyle = '#4a0008'; o.fillRect(0, 0, W, H); const r = o.createRadialGradient(mx, H * .45, 0, mx, H * .45, H * .7); r.addColorStop(0, '#ffb09a'); r.addColorStop(.3, '#d0201a'); r.addColorStop(1, 'rgba(60,0,0,0)'); o.fillStyle = r; o.fillRect(0, 0, W, H); }, '#ff3018', 24, .2));
  add('Warp speed', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#000014'; o.fillRect(0, 0, W, H); o.lineCap = 'round';
    for (let i = 0; i < 160; i++) { const a = i * 2.39996, z = (i * .137 + E.t * .5) % 1, r1 = Math.pow(z, 2) * W, r2 = r1 + W * .04 * (1 + z * 3); o.strokeStyle = hsl(200 + (i % 60), 80, 70 + z * 30, z); o.lineWidth = (1 + z * 3) * E.fx.dpr; o.beginPath(); o.moveTo(W / 2 + Math.cos(a) * r1, H / 2 + Math.sin(a) * r1); o.lineTo(W / 2 + Math.cos(a) * r2, H / 2 + Math.sin(a) * r2); o.stroke(); } }, '#9fdcff', 16, .2));
  add('Prism split', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; for (let i = 0; i < 7; i++) { const x = ((i / 7 + E.t * .12) % 1) * W * 1.4 - W * .2; o.fillStyle = hsl(i * 51, 100, 60); o.save(); o.translate(x, 0); o.transform(1, 0, -.4, 1, 0, 0); o.fillRect(0, 0, W * .2, H); o.restore(); } }, '#fff', 14));
  add('Fireflies', 'stencil', E => E.fx.stencil(E, o => { const { W, H } = E; o.fillStyle = '#1d4a2a'; o.fillRect(0, 0, W, H); for (let i = 0; i < 60; i++) { const x = (fbm(i * 3.1, E.t * .15) * 1.6 - .3) * W, y = (fbm(i * 7.3 + 4, E.t * .15 + 2) * 1.6 - .3) * H, b = .5 + .5 * Math.sin(E.t * 4 + i); const r = o.createRadialGradient(x, y, 0, x, y, H * .08); r.addColorStop(0, `rgba(230,255,120,${b})`); r.addColorStop(1, 'rgba(230,255,120,0)'); o.fillStyle = r; o.fillRect(x - H * .08, y - H * .08, H * .16, H * .16); } }, '#e6ff78', 20, .25));
  add('Galaxy spiral', 'stencil', E => E.fx.stencil(E, o => E.fx.field(o, (u, v, t, r) => { const x = (u - .5) * 2, y = (v - .5) * 1.6, d = Math.hypot(x, y), a = Math.atan2(y, x) + t * .6 - d * 4; const arm = Math.pow(.5 + .5 * Math.cos(a * 2), 3) * Math.exp(-d * 1.2); const st = vn(u * 120 + t, v * 120) > .98 ? 200 : 0; r[0] = Math.min(255, 60 + 255 * arm + st); r[1] = Math.min(255, 30 + 170 * arm + st); r[2] = Math.min(255, 120 + 255 * arm + st); }, E.t, 170), '#c98bff', 20, .2));

  // ===== LINE MOTION (the strokes move, then return to the exact mark) =====
  add('Tattoo draw-on', 'line', E => { const c = E.c, n = SEGS.length, q = E.p; E.fx.mark(ss(.86, 1, q));
    const order = E.st.o || (E.st.o = SEGS.map((s, i) => i).sort((a, b) => SEGS[a][4] - SEGS[b][4] || SEGS[a][0] - SEGS[b][0]));
    c.save(); E.fx.mt(c); c.lineCap = 'round'; c.strokeStyle = E.fx.o.color; const prog = ss(.03, .8, q) * n;
    order.forEach((i, k) => { const f = clamp(prog - k); if (f <= 0) return; const s = SEGS[i]; c.globalAlpha = 1 - ss(.86, 1, q); c.lineWidth = s[5]; c.beginPath(); c.moveTo(s[0], s[1]); c.lineTo(lerp(s[0], s[2], f), lerp(s[1], s[3], f)); c.stroke();
      if (f < 1) { const x = lerp(s[0], s[2], f), y = lerp(s[1], s[3], f); c.fillStyle = '#fff'; c.shadowColor = '#ffd36b'; c.shadowBlur = 30; c.beginPath(); c.arc(x, y, s[5] * 1.6, 0, TAU); c.fill(); c.shadowBlur = 0; } }); c.restore(); }, 8);
  add('Scatter and re-form', 'line', E => { const R = E.st.r || (E.st.r = SEGS.map(() => [rr(-1, 1), rr(-1, 1), rr(-6, 6)])); const m = ease(E.m);
    E.fx.lines(E, (s, i) => ({ x: (s[0] + s[2]) / 2 + R[i][0] * VB[2] * .7 * m, y: (s[1] + s[3]) / 2 + R[i][1] * VB[3] * .7 * m, r: R[i][2] * m, a: 1 })); });
  add('Shockwave explode', 'line', E => { const m = E.m, cx = VB[0] + VB[2] / 2, cy = VB[1] + VB[3] / 2;
    E.fx.lines(E, (s, i, mx, my) => { const dx = mx - cx, dy = my - cy, d = Math.hypot(dx, dy) + 1; const push = easeOutBack(m) * VB[2] * .45 * (1 - d / (VB[2] * 1.4)); return { x: mx + dx / d * push, y: my + dy / d * push, r: m * (i % 2 ? 1.2 : -1.2) }; }); });
  // golden-spiral fold: the two B triangles spiral into the D (r = a·φ^(2θ/π)) and unfold again; the D turns a little
  add('Golden spiral fold', 'line', E => { const m = ease(E.m), PHI = 1.618;
    E.fx.lines(E, (s, i, mx, my) => { const g = s[4]; if (g === 2) { const th = m * .35, dx = mx - DC.cx, dy = my - DC.cy; return { x: DC.cx + dx * Math.cos(th) - dy * Math.sin(th), y: DC.cy + dx * Math.sin(th) + dy * Math.cos(th), r: th }; }
      const T = tri(g), th = m * (g ? 2.2 : 1.6) * Math.PI, rad = Math.hypot(T.cx - DC.cx, T.cy - DC.cy) * Math.pow(PHI, -2 * th / Math.PI), a0 = Math.atan2(T.cy - DC.cy, T.cx - DC.cx) + th;
      const nx = DC.cx + Math.cos(a0) * rad, ny = DC.cy + Math.sin(a0) * rad, sc = lerp(1, .5, m), lx = (mx - T.cx) * sc, ly = (my - T.cy) * sc, rot = th;
      return { x: nx + lx * Math.cos(rot) - ly * Math.sin(rot), y: ny + lx * Math.sin(rot) + ly * Math.cos(rot), r: rot, l: sc }; }); }, 8);
  add('Orbit', 'line', E => { const m = E.m, ang = ease(E.p) * TAU;
    E.fx.lines(E, (s, i, mx, my) => { const g = s[4]; if (g === 2) return {}; const T = tri(g), R0 = Math.hypot(T.cx - DC.cx, T.cy - DC.cy), a0 = Math.atan2(T.cy - DC.cy, T.cx - DC.cx), a = a0 + ang * (g ? 1 : -1);
      const R = lerp(R0, R0 * 1.25, Math.sin(m * Math.PI)); const nx = lerp(T.cx, DC.cx + Math.cos(a) * R, m), ny = lerp(T.cy, DC.cy + Math.sin(a) * R * .55, m); return { x: nx + (mx - T.cx), y: ny + (my - T.cy) }; }); }, 8);
  add('Ripple wave', 'line', E => E.fx.lines(E, (s, i, mx, my) => ({ y: my + Math.sin((mx - VB[0]) / VB[2] * TAU * 1.5 - E.t * 5) * VB[3] * .08 * E.m, r: Math.cos((mx - VB[0]) / VB[2] * TAU * 1.5 - E.t * 5) * .25 * E.m })));
  add('Tornado', 'line', E => { const m = E.m, cx = VB[0] + VB[2] / 2; E.fx.lines(E, (s, i, mx, my) => { const h = (my - VB[1]) / VB[3], a = E.t * 4 + h * 6 + i, R = VB[2] * (.08 + h * .25); return { x: lerp(mx, cx + Math.cos(a) * R, ease(m)), y: lerp(my, my - Math.sin(a) * R * .15, m), r: a * m }; }); });
  add('Rainfall rebuild', 'line', E => { const R = E.st.r || (E.st.r = SEGS.map(() => [rr(.2, .5), rr(-3, 3), rr(-.15, .15)])), floor = VB[1] + VB[3] * 1.05;
    E.fx.lines(E, (s, i, mx, my) => { const q = E.p; let y = my, r = 0, x = mx; if (q < .5) { const tt = ss(R[i][0] * .5, .48, q); y = lerp(my, floor - Math.abs(Math.sin(tt * 9)) * (1 - tt) * VB[3] * .2, Math.min(1, tt * 1.4)); r = R[i][1] * tt; x = mx + R[i][2] * VB[2] * tt; }
      else { const tt = ease(ss(.55, .92, q)); y = lerp(floor, my, tt); r = R[i][1] * (1 - tt); x = mx + R[i][2] * VB[2] * (1 - tt); } return { x, y, r }; }); }, 7);
  add('Magnetic snap', 'line', E => { const R = E.st.r || (E.st.r = SEGS.map(() => [rr(-1, 1), rr(-1, 1), rr(-3, 3)])); const q = E.p, out = ss(.05, .35, q), back = easeOutBack(ss(.6, .85, q)); const m = out * (1 - back);
    E.fx.lines({ ...E, m: Math.max(m, ss(.02, .06, q) * (1 - ss(.9, .97, q))) }, (s, i, mx, my) => ({ x: mx + R[i][0] * VB[2] * .35 * m, y: my + R[i][1] * VB[3] * .35 * m, r: R[i][2] * m })); });
  add('Kaleidoscope', 'line', E => { const c = E.c, f = E.f, [cx, cy] = E.fx.px(VB[0] + VB[2] / 2, VB[1] + VB[3] / 2); E.fx.mark(1 - f * .7);
    for (let k = 1; k < 6; k++) { c.save(); c.translate(cx, cy); c.rotate(k * TAU / 6 + E.t * .4 * f); c.scale(.75, .75); c.translate(-cx, -cy); c.globalAlpha = f * .55; E.fx.mark(1, hsl((k * 60 + E.t * 40) % 360, 90, 65), c); c.restore(); } });
  add('Origami flip', 'line', E => E.fx.lines(E, (s, i, mx, my) => { const g = s[4], T = tri(g), q = clamp(E.p * 1.3 - g * .18), a = Math.sin(ss(.05, .75, q) * Math.PI), sx = Math.cos(ss(.05, .75, q) * TAU) ; return { x: T.cx + (mx - T.cx) * sx, y: my - a * VB[3] * .04, l: 1, r: 0, a: 1 }; }), 7);
  add('Breathing', 'line', E => { const b = Math.sin(E.p * TAU * 2) * E.f, c = E.c, [cx, cy] = E.fx.px(VB[0] + VB[2] / 2, VB[1] + VB[3] / 2); c.save(); c.translate(cx, cy); c.scale(1 + b * .06, 1 + b * .06); c.translate(-cx, -cy); E.fx.mark(1, E.fx.o.color, c, 10 + 30 * Math.abs(b)); c.restore(); }, 6);
  add('Domino', 'line', E => E.fx.lines(E, (s, i, mx, my) => { const g = s[4], T = tri(g), q = ss(g * .12, .4 + g * .12, E.p) * (1 - ss(.65 + g * .08, .9 + g * .03, E.p)), a = q * Math.PI / 2 * .95, px = T.x1, py = T.y1, dx = mx - px, dy = my - py;
    return { x: px + dx * Math.cos(a) - dy * Math.sin(a), y: py + dx * Math.sin(a) + dy * Math.cos(a), r: a }; }), 7);
  add('Shatter', 'line', E => { const R = E.st.r || (E.st.r = SEGS.map(() => [rr(-1, 1), rr(.2, 1), rr(-8, 8)])); const m = E.m;
    E.fx.lines(E, (s, i, mx, my) => ({ x: mx + R[i][0] * VB[2] * .2 * m, y: my + R[i][1] * VB[3] * .5 * m * m, r: R[i][2] * m, l: 1 - m * .45 })); });
  add('String art', 'line', E => E.fx.lines(E, (s, i) => ({ l: 1 + ease(E.m) * 3.2, a: 1 - E.m * .35, w: s[5] * (1 - E.m * .6) })), 7);
  add('Pendulum swing', 'line', E => { const c = E.c, a = Math.sin(E.t * 2.6) * .32 * E.f, [cx, cy] = E.fx.px(VB[0] + VB[2] / 2, VB[1] - VB[3] * .3); c.save(); c.translate(cx, cy); c.rotate(a); c.translate(-cx, -cy);
    E.fx.lines({ ...E, m: E.f }, (s, i, mx, my) => ({ r: -a * (.4 + (i % 5) * .15), x: mx - Math.sin(a) * (i % 3) * VB[2] * .01 })); c.restore(); });
  add('Glitch', 'line', E => { const c = E.c, { W, H } = E; E.fx.mark(1); if (E.f <= 0) return; seed = 3 + Math.floor(E.t * 12); const o = E.fx.oc; o.setTransform(1, 0, 0, 1, 0, 0); o.clearRect(0, 0, W, H); E.fx.mark(1, '#fff', o);
    c.clearRect(0, 0, W, H); c.globalCompositeOperation = 'lighter'; for (const [col, dx] of [['#ff0040', -8], ['#00ffd0', 8], ['#ffffff', 0]]) { c.save(); c.globalAlpha = .8; const sl = 12; for (let k = 0; k < sl; k++) { const y = k * H / sl, off = (rnd() < .3 ? rr(-40, 40) : 0) * E.f * E.fx.dpr + dx * E.f * E.fx.dpr; c.drawImage(E.fx.off, 0, y, W, H / sl, off, y, W, H / sl); } c.globalCompositeOperation = 'source-in'; c.fillStyle = col; c.fillRect(0, 0, W, H); c.restore(); c.globalCompositeOperation = 'lighter'; }
    c.globalCompositeOperation = 'source-over'; }, 5);
  add('Hologram', 'line', E => { const c = E.c, { W, H } = E, fl = .75 + .25 * Math.sin(E.t * 40) * Math.sin(E.t * 7); E.fx.mark(1 - E.f, undefined); c.save(); c.globalAlpha = E.f * fl; c.translate(Math.sin(E.t * 30) * 2 * E.f, 0); E.fx.mark(1, '#5ff3ff', c, 18); c.restore();
    c.save(); c.globalCompositeOperation = 'destination-out'; c.globalAlpha = E.f * .5; for (let y = (E.t * 40) % 6; y < H; y += 6 * E.fx.dpr) c.fillRect(0, y, W, 2 * E.fx.dpr); c.restore(); });
  // two stick men built from the strokes fight, then fall back into the mark
  add('Stick-men fight', 'line', E => fight(E), 10);

  // ===== MAGIC (bursts and enchantments on the lines) =====
  add('Spark run', 'magic', E => { const c = E.c; E.fx.mark(1, undefined, c, 6 * E.f); c.save(); E.fx.mt(c); c.globalCompositeOperation = 'lighter';
    SEGS.forEach((s, i) => { const q = (E.t * (.4 + (i % 5) * .08) + i * .37) % 1; const x = lerp(s[0], s[2], q), y = lerp(s[1], s[3], q); const g = c.createRadialGradient(x, y, 0, x, y, s[5] * 5); g.addColorStop(0, `rgba(255,255,230,${E.f})`); g.addColorStop(.3, `rgba(255,200,80,${E.f * .7})`); g.addColorStop(1, 'rgba(255,120,0,0)'); c.fillStyle = g; c.fillRect(x - s[5] * 5, y - s[5] * 5, s[5] * 10, s[5] * 10); }); c.restore(); });
  add('Rune circle', 'magic', E => { const c = E.c, f = E.f, [cx, cy] = E.fx.px(VB[0] + VB[2] / 2, VB[1] + VB[3] / 2), R = Math.max(E.fx.bw, E.fx.bh) * .62;
    c.save(); c.translate(cx, cy); c.globalAlpha = f; c.strokeStyle = '#8ff7ff'; c.shadowColor = '#3ce0ff'; c.shadowBlur = 16 * E.fx.dpr; c.lineWidth = 2 * E.fx.dpr;
    for (const [rf, sp, n] of [[1, .3, 3], [.86, -.45, 6], [.7, .6, 9]]) { c.save(); c.rotate(E.t * sp); c.beginPath(); c.arc(0, 0, R * rf, 0, TAU); c.stroke(); for (let k = 0; k < n; k++) { c.rotate(TAU / n); c.beginPath(); c.moveTo(R * rf, 0); c.lineTo(R * rf * .93, -R * .05); c.lineTo(R * rf * .93, R * .05); c.closePath(); c.stroke(); } c.restore(); }
    c.font = `${R * .08}px serif`; c.fillStyle = '#bffcff'; for (let k = 0; k < 24; k++) { c.save(); c.rotate(k / 24 * TAU - E.t * .2); c.fillText('ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃ'[k % 12], R * .74, 0); c.restore(); } c.restore();
    E.fx.mark(1, f > .5 ? '#bffcff' : undefined, c, 20 * f); });
  add('Magic burst', 'magic', E => { const c = E.c, P = E.st.p || (E.st.p = Array.from({ length: 160 }, () => { const s = SEGS[(rnd() * SEGS.length) | 0], q = rnd(); return [lerp(s[0], s[2], q), lerp(s[1], s[3], q), rr(0, TAU), rr(.3, 1.2), rr(0, 360)]; }));
    E.fx.mark(1, undefined, c, 10 * E.f); const b = ss(.15, .2, E.p), q = ss(.2, .9, E.p); if (!b) return; c.save(); E.fx.mt(c); c.globalCompositeOperation = 'lighter';
    for (const p of P) { const d = q * VB[2] * .35 * p[3], x = p[0] + Math.cos(p[2]) * d, y = p[1] + Math.sin(p[2]) * d + q * q * VB[3] * .3; c.fillStyle = hsl(p[4], 100, 70, (1 - q)); c.beginPath(); c.arc(x, y, VB[2] * .006 * (1 - q * .5), 0, TAU); c.fill(); }
    if (q < .5) { c.strokeStyle = `rgba(255,255,255,${(.5 - q) * 2})`; c.lineWidth = VB[2] * .01; c.beginPath(); c.arc(DC.cx, DC.cy, q * VB[2] * .9, 0, TAU); c.stroke(); } c.restore(); });
  add('Fireworks', 'magic', E => { const c = E.c; E.fx.mark(1); c.save(); E.fx.mt(c); c.globalCompositeOperation = 'lighter'; const tips = [[TRIS[0].x1, TRIS[0].cy], [TRIS[1].x1, TRIS[1].cy], [DC.x1, DC.cy]];
    tips.forEach(([tx, ty], k) => { const t0 = .1 + k * .22, q = ss(t0, t0 + .45, E.p); if (q <= 0 || q >= 1) return; const hy = ty - VB[3] * .45 * Math.min(1, q * 3), ex = Math.max(0, q * 3 - 1) / 2, hue = k * 110 + 20;
      if (ex <= 0) { c.fillStyle = '#fff'; c.beginPath(); c.arc(tx, hy, VB[2] * .006, 0, TAU); c.fill(); return; }
      for (let i = 0; i < 48; i++) { const a = i / 48 * TAU, d = ease(ex) * VB[2] * .16; c.fillStyle = hsl(hue + (i % 3) * 20, 100, 65, 1 - ex); c.beginPath(); c.arc(tx + Math.cos(a) * d, hy + Math.sin(a) * d + ex * ex * VB[3] * .1, VB[2] * .005, 0, TAU); c.fill(); } }); c.restore(); }, 7);
  add('Enchanted glow', 'magic', E => { const h = (E.t * 40) % 360; E.fx.mark(1 - E.f); E.fx.segs({ ...E }, (s, i) => ({ col: hsl((h + i * 9) % 360, 100, 65), a: E.f * (.6 + .4 * Math.sin(E.t * 6 + i)) }), undefined, 18); });
  add('Ember drift', 'magic', E => { const c = E.c; E.fx.mark(1, undefined, c, 8 * E.f); c.save(); E.fx.mt(c); c.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 140; i++) { const s = SEGS[i % SEGS.length], q = (i * .618) % 1, life = (E.t * .35 + i * .13) % 1, x = lerp(s[0], s[2], q) + Math.sin(E.t * 2 + i) * VB[2] * .02 * life, y = lerp(s[1], s[3], q) - life * VB[3] * .35;
      c.fillStyle = `rgba(255,${120 + (i % 80)},20,${(1 - life) * E.f})`; c.beginPath(); c.arc(x, y, VB[2] * .004 * (1 - life), 0, TAU); c.fill(); } c.restore(); });
  add('Frost creep', 'magic', E => { const c = E.c; E.fx.mark(1); c.save(); E.fx.mt(c); c.strokeStyle = '#d9f6ff'; c.shadowColor = '#7fd8ff'; c.shadowBlur = 12; c.lineCap = 'round'; const g = ss(.05, .6, E.p) * (1 - ss(.85, 1, E.p));
    SEGS.forEach((s, i) => { seed = 11 + i; const L = Math.hypot(s[2] - s[0], s[3] - s[1]), n = Math.floor(L / (VB[2] * .03)); for (let k = 0; k < n; k++) { const q = (k + .5) / n, x = lerp(s[0], s[2], q), y = lerp(s[1], s[3], q), a = Math.atan2(s[3] - s[1], s[2] - s[0]) + (k % 2 ? 1 : -1) * rr(.6, 1.1), l = VB[2] * .02 * g * rr(.5, 1.2);
      c.globalAlpha = g; c.lineWidth = s[5] * .35; c.beginPath(); c.moveTo(x, y); c.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); c.stroke(); } }); c.restore(); });
  add('Lightning strike', 'magic', E => { const c = E.c, q = E.p, hit = ss(.3, .32, q) * (1 - ss(.45, .7, q)); E.fx.mark(1, hit > .3 ? '#e9e2ff' : undefined, c, 40 * hit);
    if (q > .28 && q < .5) { const [x, y] = E.fx.px(DC.x1, DC.cy); seed = 17 + Math.floor(q * 60); c.save(); c.strokeStyle = '#f1ecff'; c.shadowColor = '#9f7bff'; c.shadowBlur = 24; bolt(c, x + rr(-50, 50), 0, x, y, 7, 4 * E.fx.dpr); c.restore(); c.save(); c.fillStyle = `rgba(200,180,255,${hit * .3})`; c.fillRect(0, 0, E.W, E.H); c.restore(); } }, 6);
  add('Water ripple rings', 'magic', E => { const c = E.c; E.fx.mark(1); c.save(); E.fx.mt(c); c.strokeStyle = '#8fdcff'; c.lineWidth = VB[2] * .004;
    for (let k = 0; k < 6; k++) { const q = (E.t * .35 + k / 6) % 1; c.globalAlpha = (1 - q) * E.f; c.beginPath(); c.ellipse(DC.cx, DC.cy, q * VB[2] * .7, q * VB[3] * .5, 0, 0, TAU); c.stroke(); } c.restore(); });

  // ===== TEXT =====
  add('Wordmark light sweep', 'text', E => { E.fx.mark(1); const c = E.c, a = ss(.05, .25, E.p) * (1 - ss(.85, 1, E.p)); E.fx.text(E, a, '#fff'); const x = lerp(-.2, 1.2, ss(.25, .75, E.p)) * E.W;
    c.save(); c.globalCompositeOperation = 'source-atop'; const g = c.createLinearGradient(x - 60, 0, x + 60, 0); g.addColorStop(0, 'rgba(255,215,110,0)'); g.addColorStop(.5, 'rgba(255,230,160,1)'); g.addColorStop(1, 'rgba(255,215,110,0)'); c.fillStyle = g; c.fillRect(0, 0, E.W, E.H); c.restore(); }, 6);
  add('Typewriter', 'text', E => { E.fx.mark(1, undefined, undefined, 6 * Math.abs(Math.sin(E.t * 8)) * E.f); const n = E.fx.o.text.length, k = Math.floor(ss(.08, .55, E.p) * n * (1 - ss(.85, .98, E.p)) + .001 + (E.p > .85 ? 0 : 0)), a = 1 - ss(.92, 1, E.p);
    E.fx.text(E, a, '#fff', { sub: Math.min(n, k) }); });
  add('Letters from lines', 'text', E => lettersMorph(E), 9);
  add('Neon wordmark', 'text', E => { const h = (E.t * 50) % 360, fl = E.p > .1 && E.p < .25 ? (Math.sin(E.t * 50) > 0 ? 1 : .2) : 1; E.fx.mark(1, hsl(h, 100, 65), undefined, 22 * E.f); E.fx.text(E, E.f * fl, hsl((h + 180) % 360, 100, 70), { glow: hsl((h + 180) % 360, 100, 60) }); }, 6);
  add('Gravity letters', 'text', E => { E.fx.mark(1); const c = E.c, t = E.fx.o.text, n = t.length; if (!t) return; c.save(); c.font = `${E.fx.ts}px "${E.fx.o.font}", Impact, sans-serif`; c.textBaseline = 'middle'; c.fillStyle = '#fff';
    const tw = c.measureText(t).width; let x = E.W / 2 - tw / 2; for (let i = 0; i < n; i++) { const w = c.measureText(t[i]).width, q = clamp(ss(.05 + i * .03, .3 + i * .03, E.p)) * (1 - ss(.82, .97, E.p)), y = E.fx.ty - (1 - easeOutBack(q)) * E.H * .5;
      c.globalAlpha = q; c.fillText(t[i], x, y); x += w; } c.restore(); }, 6);

  // ===== VARIANTS (all hand-drawn versions of the BD, same size; owner's request) =====
  const nSk = () => (window.DOGMA_SKINS || []).length;
  add('Variant carousel', 'variant', E => { const n = nSk(); if (!n) return E.fx.mark(1); const turns = 4, q = ss(.06, .94, E.p) * turns, k = Math.floor(q), f = q - k, sx = Math.cos(f * Math.PI);
    const front = k === 0 ? -1 : (E.st.base ??= Math.floor(rnd() * n)) + k - 1, back = k === turns - 1 ? -1 : (E.st.base ??= Math.floor(rnd() * n)) + k;
    const idx = sx >= 0 ? front : back, col = sx >= 0 ? E.fx.o.color : hsl((k * 70 + 30) % 360, 85, 65); if (q >= turns || q <= 0) return E.fx.mark(1);
    if (idx < 0) { const c = E.c; c.save(); const [cx] = E.fx.px(VB[0] + VB[2] / 2, 0); c.translate(cx, 0); c.scale(Math.abs(sx), 1); c.translate(-cx, 0); E.fx.mark(1, col, c); c.restore(); }
    else E.fx.drawSkin(idx, 1, col, E.c, Math.abs(sx), 8); }, 8);
  add('Ink saturation', 'variant', E => { const c = E.c, q = ss(.1, .45, E.p) * (1 - ss(.6, .92, E.p)), [cx, cy] = E.fx.px(VB[0] + VB[2] / 2, VB[1] + VB[3] / 2), R = Math.hypot(E.W, E.H) * q * .6;
    E.fx.mark(1); if (q <= 0 || !nSk()) return; const o = E.fx.oc; o.setTransform(1, 0, 0, 1, 0, 0); o.clearRect(0, 0, E.W, E.H); E.fx.drawSkin(E.fx.skinIndex('inknet_31_47'), 1, '#111', o);
    o.globalCompositeOperation = 'destination-in'; const g = o.createRadialGradient(cx, cy, R * .7, cx, cy, R); g.addColorStop(0, '#000'); g.addColorStop(1, 'rgba(0,0,0,0)'); o.fillStyle = g; o.fillRect(0, 0, E.W, E.H); o.globalCompositeOperation = 'source-over';
    c.save(); c.globalCompositeOperation = 'destination-out'; c.drawImage(E.fx.off, 0, 0); c.restore(); c.save(); c.globalAlpha = 1; const o2 = E.fx.oc;
    o2.globalCompositeOperation = 'source-in'; o2.fillStyle = E.fx.o.color; o2.fillRect(0, 0, E.W, E.H); o2.globalCompositeOperation = 'source-over'; c.shadowColor = '#ff9a3c'; c.shadowBlur = 14 * E.fx.dpr * q; c.drawImage(E.fx.off, 0, 0); c.restore(); }, 7);
  add("Tattooist's flip-book", 'variant', E => { const n = nSk(); if (!n) return E.fx.mark(1); const on = ss(.08, .14, E.p) * (1 - ss(.86, .92, E.p)); if (on < .5) return E.fx.mark(1);
    const ink = (window.DOGMA_SKINS || []).map((k, i) => [k.name, i]).filter(([nm]) => /^(ink|tattoo|straight|organic)/.test(nm)).map(x => x[1]); const i = ink[Math.floor(E.t * 8) % ink.length];
    E.fx.drawSkin(i, 1, undefined, E.c, 1, 4); }, 6);
  add('Dream crossfade', 'variant', E => { const gem = (window.DOGMA_SKINS || []).map((k, i) => [k.name, i]).filter(([nm]) => /^gemini/.test(nm)).map(x => x[1]); if (!gem.length) return E.fx.mark(1);
    const q = ss(.08, .92, E.p) * (gem.length + 1), k = Math.floor(q), f = ss(.6, 1, q - k), cur = k === 0 ? -1 : gem[(k - 1) % gem.length], nxt = k >= gem.length ? -1 : gem[k], h = (E.t * 40) % 360;
    const draw = (i, a) => i < 0 ? E.fx.mark(a, undefined, undefined, 12) : E.fx.drawSkin(i, a, hsl(h, 70, 72), E.c, 1, 20); draw(cur, 1 - f); draw(nxt, f); }, 9);
  add('Deck shuffle', 'variant', E => { const n = nSk(); if (!n) return E.fx.mark(1); const c = E.c, m = ss(.05, .2, E.p) * (1 - ss(.8, .95, E.p)), base = (E.st.b ??= Math.floor(rnd() * n));
    E.fx.mark(1 - m); for (let j = 0; j < 4; j++) { const ph = (E.t * .9 + j / 4) % 1, x = Math.sin(ph * TAU) * E.fx.bw * .42 * m, sc = .55 + .25 * Math.cos(ph * TAU), a = m * (.35 + .65 * (Math.cos(ph * TAU) * .5 + .5));
      c.save(); const [cx, cy] = E.fx.px(VB[0] + VB[2] / 2, VB[1] + VB[3] / 2); c.translate(cx + x, cy); c.scale(sc, sc); c.translate(-cx, -cy); E.fx.drawSkin(base + j, a, j % 2 ? '#ffffff' : undefined, c, 1, 6); c.restore(); } }, 7);

  // ---------- stick-men fight ----------
  const SK = ['head0', 'head1', 'head2', 'head3', 'head4', 'head5', 'torso', 'uarmL', 'larmL', 'uarmR', 'larmR', 'ulegL', 'llegL', 'ulegR', 'llegR'];
  function pose(t, side) {        // joint angles (rad) for a simple fight loop; side = +1 faces right, -1 faces left
    const ph = t % 4, s = side, jab = ph < 1 ? Math.sin(ph * Math.PI) : 0, kick = ph > 2 && ph < 3 ? Math.sin((ph - 2) * Math.PI) : 0, hit = ph > 3 ? Math.sin((ph - 3) * Math.PI) : 0;
    const bob = Math.sin(t * 6) * .04;
    return { lean: s * (.08 + jab * .15 - hit * .3) + bob, sh: [s * (-.6 + jab * 1.5), s * (.9 - jab * .4)], el: [s * (1.2 - jab * 1.1), s * 1.6], hip: [s * (.25 + kick * 1.3), s * -.3], kn: [s * (-.3 + kick * .2), s * .4], dx: s * (jab * .08 + kick * .05 - hit * .12) };
  }
  function figure(cx, cy, H, P) {   // returns bone list [x1,y1,x2,y2] in order of SK
    const L = { torso: H * .34, upper: H * .2, lower: H * .2, thigh: H * .24, shin: H * .24, head: H * .1 }, out = [];
    const hipX = cx + P.dx * H, hipY = cy, nx = hipX + Math.sin(P.lean) * L.torso, ny = hipY - Math.cos(P.lean) * L.torso, hx = nx + Math.sin(P.lean) * L.head * 1.2, hy = ny - Math.cos(P.lean) * L.head * 1.2;
    for (let k = 0; k < 6; k++) { const a1 = k / 6 * TAU, a2 = (k + 1) / 6 * TAU; out.push([hx + Math.cos(a1) * L.head, hy + Math.sin(a1) * L.head, hx + Math.cos(a2) * L.head, hy + Math.sin(a2) * L.head]); }
    out.push([hipX, hipY, nx, ny]);
    for (let a = 0; a < 2; a++) { const sa = P.lean + Math.PI / 2 + P.sh[a], ex = nx + Math.cos(sa) * L.upper, ey = ny + Math.sin(sa) * L.upper * -1 * -1, ea = sa - P.el[a]; out.push([nx, ny, ex, ey], [ex, ey, ex + Math.cos(ea) * L.lower, ey + Math.sin(ea) * L.lower]); }
    for (let l = 0; l < 2; l++) { const ha = Math.PI / 2 + P.hip[l], kx = hipX + Math.cos(ha) * L.thigh, ky = hipY + Math.sin(ha) * L.thigh, ka = ha + P.kn[l]; out.push([hipX, hipY, kx, ky], [kx, ky, kx + Math.cos(ka) * L.shin, ky + Math.sin(ka) * L.shin]); }
    return out;
  }
  function fight(E) {
    const q = E.p, asm = ease(ss(.03, .16, q)), dis = ease(ss(.84, .97, q)), on = asm * (1 - dis), tt = Math.max(0, E.t - E.dur * .14);
    const H = VB[3] * .8, cy = VB[1] + VB[3] * .62, x1 = VB[0] + VB[2] * .33, x2 = VB[0] + VB[2] * .67;
    const A = figure(x1, cy, H, pose(tt, 1)), B = figure(x2, cy, H, pose(tt + 2, -1)), bones = A.concat(B);
    const pick = E.st.pick || (E.st.pick = SEGS.map((s, i) => i).sort((a, b) => Math.hypot(SEGS[b][2] - SEGS[b][0], SEGS[b][3] - SEGS[b][1]) - Math.hypot(SEGS[a][2] - SEGS[a][0], SEGS[a][3] - SEGS[a][1])).slice(0, bones.length));
    const map = new Map(pick.map((si, k) => [si, k]));
    E.fx.mark(1 - ss(0, .1, on)); if (on <= 0) return;
    const c = E.c; c.save(); E.fx.mt(c); c.lineCap = 'round'; c.strokeStyle = E.fx.o.color;
    SEGS.forEach((s, i) => { const k = map.get(i); c.lineWidth = s[5];
      if (k == null) { c.globalAlpha = 1 - on; c.beginPath(); c.moveTo(s[0], s[1]); c.lineTo(s[2], s[3]); c.stroke(); return; }
      const b = bones[k]; c.globalAlpha = 1; c.beginPath(); c.moveTo(lerp(s[0], b[0], on), lerp(s[1], b[1], on)); c.lineTo(lerp(s[2], b[2], on), lerp(s[3], b[3], on)); c.stroke(); });
    // impact flashes
    const ph = tt % 4; if (on > .9 && ((ph > .45 && ph < .6) || (ph > 2.45 && ph < 2.6))) { c.globalCompositeOperation = 'lighter'; const xx = (x1 + x2) / 2, yy = cy - H * .55; const g = c.createRadialGradient(xx, yy, 0, xx, yy, H * .18); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.4, 'rgba(255,210,90,.8)'); g.addColorStop(1, 'rgba(255,120,0,0)'); c.fillStyle = g; c.fillRect(xx - H * .2, yy - H * .2, H * .4, H * .4); }
    c.restore();
  }
  // ---------- strokes become the letters B I G  D O G M A (an angular stroke font in the mark's spirit) ----------
  const FONT = { B: [[0, 0, 0, 1], [0, 0, .8, .25], [.8, .25, 0, .5], [0, .5, .9, .75], [.9, .75, 0, 1]], I: [[.4, 0, .4, 1]], G: [[.9, .1, .3, 0], [.3, 0, 0, .5], [0, .5, .3, 1], [.3, 1, .9, .85], [.9, .85, .9, .55], [.9, .55, .55, .55]],
    D: [[0, 0, 0, 1], [0, 0, .9, .5], [.9, .5, 0, 1]], O: [[.5, 0, 0, .3], [0, .3, 0, .7], [0, .7, .5, 1], [.5, 1, 1, .7], [1, .7, 1, .3], [1, .3, .5, 0]], M: [[0, 1, 0, 0], [0, 0, .5, .6], [.5, .6, 1, 0], [1, 0, 1, 1]], A: [[0, 1, .5, 0], [.5, 0, 1, 1], [.2, .62, .8, .62]], ' ': [] };
  function lettersMorph(E) {
    const t = (E.fx.o.text || 'BIG DOGMA').toUpperCase(), q = E.p, on = ease(ss(.08, .3, q)) * (1 - ease(ss(.72, .94, q)));
    const lw = VB[2] / (t.length * 1.25), lh = lw * 1.5, y0 = VB[1] + VB[3] / 2 - lh / 2, x0 = VB[0] + (VB[2] - lw * 1.25 * t.length) / 2; const tgt = [];
    [...t].forEach((ch, i) => (FONT[ch] || []).forEach(s => tgt.push([x0 + i * lw * 1.25 + s[0] * lw, y0 + s[1] * lh, x0 + i * lw * 1.25 + s[2] * lw, y0 + s[3] * lh])));
    E.fx.mark(1 - ss(0, .1, on)); if (on <= 0) return; const c = E.c; c.save(); E.fx.mt(c); c.lineCap = 'round'; c.strokeStyle = E.fx.o.color;
    SEGS.forEach((s, i) => { c.lineWidth = s[5]; const b = tgt[i % tgt.length], extra = i >= tgt.length; c.globalAlpha = extra ? 1 - on : 1; const o2 = extra ? 0 : on;
      c.beginPath(); c.moveTo(lerp(s[0], b[0], o2), lerp(s[1], b[1], o2)); c.lineTo(lerp(s[2], b[2], o2), lerp(s[3], b[3], o2)); c.stroke(); }); c.restore();
  }

  (function loadSkins() {
    if (window.DOGMA_SKINS) return; const me = document.currentScript && document.currentScript.src; if (!me) return;
    const go = () => { const sc = document.createElement('script'); sc.src = me.replace(/logo_fx(\.min)?\.js.*$/, 'skins.js'); sc.async = true; document.head.appendChild(sc); };
    document.readyState === 'complete' ? setTimeout(go, 400) : addEventListener('load', () => setTimeout(go, 400));
  })();
  window.DogmaLogoFX = { mount: (el, o) => new FX(el, o), effects: EFFECTS };
})();
