/* DOGMA animated logo: the hand-drawn mark ignites stroke by stroke, then glows like heated metal and cycles
   through 3 colours of "magic" (gold -> arcane blue -> violet), each change landing on a power burst
   (shockwave ring, light rays, spark shower, glint across the wordmark). Fully deterministic in t (seconds),
   so the same code renders video frames and runs live in the browser. Loop: 12 s, seamless after the 3.5 s intro. */
(function (root) {
  const INTRO = 3.5, SEG = 4, T = 12;
  const PAL = [
    [[0, 40, 5, 0], [.25, 110, 15, 0], [.45, 200, 50, 0], [.62, 255, 130, 20], [.78, 242, 193, 78], [.92, 255, 240, 190], [1, 255, 255, 255]],
    [[0, 0, 8, 40], [.25, 5, 30, 110], [.45, 20, 80, 220], [.62, 40, 150, 255], [.78, 90, 210, 255], [.92, 200, 245, 255], [1, 255, 255, 255]],
    [[0, 25, 0, 40], [.25, 70, 5, 120], [.45, 130, 30, 220], [.62, 175, 80, 255], [.78, 205, 130, 255], [.92, 240, 210, 255], [1, 255, 255, 255]]];
  const ACC = [[242, 193, 78], [70, 180, 255], [190, 110, 255]];
  const lut = p => { const o = new Float32Array(256 * 3); for (let i = 0; i < 256; i++) { const x = i / 255; let k = 0; while (k < p.length - 2 && x > p[k + 1][0]) k++; const a = p[k], b = p[k + 1], f = Math.min(1, Math.max(0, (x - a[0]) / (b[0] - a[0]))); for (let c = 0; c < 3; c++) o[i * 3 + c] = a[c + 1] + (b[c + 1] - a[c + 1]) * f; } return o; };
  const LUT = PAL.map(lut);
  const rng = seed => { let s = (seed >>> 0) || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return (s >>> 0) / 4294967296; }; };
  const ss = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const rgba = (c, a) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${Math.max(0, Math.min(1, a))})`;
  const mix = (a, b, w) => [a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w, a[2] + (b[2] - a[2]) * w];
  function noise(seed, cell, w, h) {
    const r = rng(seed), gw = Math.ceil(w / cell) + 2, gh = Math.ceil(h / cell) + 2, g = new Float32Array(gw * gh);
    for (let i = 0; i < g.length; i++) g[i] = r();
    return (x, y) => { const gx = x / cell, gy = y / cell, ix = Math.floor(gx), iy = Math.floor(gy), u0 = gx - ix, v0 = gy - iy, u = u0 * u0 * (3 - 2 * u0), v = v0 * v0 * (3 - 2 * v0);
      const a = g[iy * gw + ix], b = g[iy * gw + ix + 1], c = g[(iy + 1) * gw + ix], d = g[(iy + 1) * gw + ix + 1]; return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; };
  }
  function palette(t) {
    const p = t - INTRO; if (p < 0) return { a: 0, b: 0, w: 0 };
    const seg = Math.floor(p / SEG), local = p - seg * SEG, cur = seg % 3, prev = seg === 0 ? 0 : (seg - 1) % 3;
    return { a: prev, b: cur, w: ss(0, 0.7, local) };
  }
  function bursts(t) { const out = []; if (t < INTRO) return out; const k = Math.floor((t - INTRO) / SEG); for (let j = Math.max(0, k - 1); j <= k; j++) out.push(INTRO + j * SEG); return out; }

  function DogmaLogo(canvas, o) {
    o = Object.assign({ layout: 'lockup', transparent: false, font: 'Russo', title: 'BIG DOGMA', sub: 'AI STUDIO  |  Skopje', lite: false, bg: '#0d0d0f' }, o || {});
    const ctx = canvas.getContext('2d');
    let W, H, mw, mh, mx, my, cx, cy, mc, mctx, img, A, IG, PH, idx, samples, igSamples, embers, fs, tx, txL, ty, tc, tctx;
    const path = new Path2D(o.d);
    function setup() {
      W = canvas.width; H = canvas.height;
      const lock = o.layout === 'lockup';
      mh = Math.round(lock ? H * 0.5 : H * 0.8); let tw = 0, gap = 0;
      for (let it = 0; it < 4; it++) {   // shrink until the whole lockup (or the mark alone) fits 88% of the width
        mw = Math.round(mh * o.vbW / o.vbH); fs = Math.round(mh * 0.36);
        ctx.font = `${fs}px ${o.font}`; ctx.letterSpacing = `${Math.round(fs * 0.06)}px`;
        tw = lock ? ctx.measureText(o.title).width : 0; gap = lock ? mh * 0.16 : 0;
        const tot = mw + gap + tw; if (tot <= W * 0.88) break; mh = Math.floor(mh * (W * 0.88) / tot); }
      mx = Math.round((W - (mw + gap + tw)) / 2); my = Math.round((H - mh) / 2);
      tx = mx + mw + gap; ty = H / 2 + fs * 0.12;
      if (o.layout === 'stack') {   // vertical: mark centred above the wordmark, whole block <= 68% of the width
        mw = Math.round(W * 0.5); mh = Math.round(mw * o.vbH / o.vbW); fs = Math.round(mh * 0.36);
        ctx.font = `${fs}px ${o.font}`; ctx.letterSpacing = `${Math.round(fs * 0.06)}px`; tw = ctx.measureText(o.title).width;
        if (tw > W * 0.64) { fs = Math.floor(fs * W * 0.64 / tw); ctx.font = `${fs}px ${o.font}`; ctx.letterSpacing = `${Math.round(fs * 0.06)}px`; tw = ctx.measureText(o.title).width; }
        gap = Math.round(mh * 0.12); const blockH = mh + gap + fs * 0.74 + fs * 0.52;
        mx = Math.round((W - mw) / 2); my = Math.round((H - blockH) / 2); tx = Math.round((W - tw) / 2); ty = my + mh + gap + fs * 0.74; }
      txL = tx; cx = mx + mw * 0.5; cy = my + mh * 0.5;
      mc = document.createElement('canvas'); mc.width = mw; mc.height = mh; mctx = mc.getContext('2d');
      mctx.setTransform(mw / o.vbW, 0, 0, mh / o.vbH, 0, 0); mctx.fillStyle = '#fff'; mctx.fill(path, 'evenodd'); mctx.setTransform(1, 0, 0, 1, 0, 0);
      const src = mctx.getImageData(0, 0, mw, mh).data; img = mctx.createImageData(mw, mh);
      A = new Float32Array(mw * mh); IG = new Float32Array(mw * mh); PH = new Float32Array(mw * mh); const list = [];
      const n1 = noise(7, Math.max(8, mh / 14), mw, mh), n2 = noise(11, Math.max(8, mh / 9), mw, mh);
      const sx = mw * 0.06, sy = mh * 0.97, diag = Math.hypot(mw, mh);
      for (let y = 0; y < mh; y++) for (let x = 0; x < mw; x++) { const i = y * mw + x, a = src[i * 4 + 3] / 255; if (a < 0.02) continue;
        A[i] = a; list.push(i); IG[i] = 0.35 + 2.1 * Math.hypot(x - sx, y - sy) / diag + 0.35 * (n1(x, y) - 0.5); PH[i] = (x / mw - y / mh) * 0.5 + 0.35 * n2(x, y); }
      idx = Int32Array.from(list);
      const r = rng(3); samples = []; for (let k = 0; k < 600; k++) { const i = idx[Math.floor(r() * idx.length)]; samples.push([mx + (i % mw), my + Math.floor(i / mw), IG[i]]); }
      igSamples = samples.slice(0, 160);
      const re = rng(5); embers = []; const Ls = [3, 4, 6, 12];
      const spanW = lock ? (tx + tw - mx) : mw;
      for (let k = 0; k < 46; k++) embers.push({ x: mx - mw * 0.05 + re() * spanW * 1.1, y: my + mh * (0.45 + 0.7 * re()), L: Ls[Math.floor(re() * 4)], off: re(),
        rise: H * (0.22 + 0.35 * re()), sway: H * 0.02 * (re() + 0.3), s: H * (0.0018 + 0.0032 * re()) });
      tc = document.createElement('canvas'); tc.width = W; tc.height = H; tctx = tc.getContext('2d');
    }
    function render(t) {
      if (canvas.width !== W || canvas.height !== H) setup();
      const P = palette(t), Ra = LUT[P.a], Rb = LUT[P.b], w = P.w, acc = mix(ACC[P.a], ACC[P.b], w);
      let B = 0; const bl = bursts(t); for (const tb of bl) if (t >= tb) B += Math.exp(-(t - tb) * 2.5);
      const fi = ss(1.5, INTRO, t);
      // ---- mark pixels: heat -> colour
      const d = img.data, om = 2 * Math.PI / 2.4, of = 2 * Math.PI / 0.3;
      for (let n = 0; n < idx.length; n++) { const i = idx[n], ig = IG[i], j = i * 4;
        if (t < ig - 0.3) { d[j + 3] = 0; continue; }
        const base = 0.70 + 0.14 * Math.sin(t * om - PH[i] * 9) + 0.035 * Math.sin(t * of + PH[i] * 40);
        let h, al = A[i];
        if (t < ig) { const q = (t - (ig - 0.3)) / 0.3; h = 0.2 + 0.25 * q; al *= q * 0.8; }
        else h = base + (1.08 - base) * Math.exp(-(t - ig) * 1.8);
        h += 0.32 * B; const k = Math.max(0, Math.min(255, (h * 255) | 0)) * 3;
        d[j] = Ra[k] + (Rb[k] - Ra[k]) * w; d[j + 1] = Ra[k + 1] + (Rb[k + 1] - Ra[k + 1]) * w; d[j + 2] = Ra[k + 2] + (Rb[k + 2] - Ra[k + 2]) * w; d[j + 3] = al * 255; }
      mctx.putImageData(img, 0, 0);
      // ---- background
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none'; ctx.globalAlpha = 1; ctx.shadowBlur = 0;
      if (o.transparent) ctx.clearRect(0, 0, W, H);
      else { ctx.fillStyle = o.bg; ctx.fillRect(0, 0, W, H); const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, H) * 0.7);
        g.addColorStop(0, rgba(acc, 0.10 + 0.10 * B)); g.addColorStop(1, rgba(acc, 0)); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }
      ctx.globalCompositeOperation = 'lighter';
      // ---- light rays
      { const n = 14, R = Math.hypot(W, H) * 0.6, rot = (2 * Math.PI / n) * (t / T), ga = (0.08 + 0.30 * B) * fi;
        if (ga > 0.005) { if (!o.lite) ctx.filter = `blur(${H * 0.008}px)`; const g = ctx.createRadialGradient(cx, cy, mh * 0.08, cx, cy, R);
          g.addColorStop(0, rgba(acc, ga)); g.addColorStop(0.5, rgba(acc, ga * 0.25)); g.addColorStop(1, rgba(acc, 0)); ctx.fillStyle = g; ctx.beginPath();
          for (let k = 0; k < n; k++) { const a = rot + k * 2 * Math.PI / n; ctx.moveTo(cx, cy); ctx.arc(cx, cy, R, a - 0.035, a + 0.035); ctx.closePath(); } ctx.fill(); ctx.filter = 'none'; } }
      // ---- glow + crisp mark
      ctx.filter = `blur(${mh * 0.09}px)`; ctx.globalAlpha = Math.min(1, 0.5 + 0.6 * B); ctx.drawImage(mc, mx, my, mw, mh);
      ctx.filter = `blur(${mh * 0.022}px)`; ctx.globalAlpha = 0.85; ctx.drawImage(mc, mx, my, mw, mh);
      ctx.filter = 'none'; ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.drawImage(mc, mx, my, mw, mh);
      ctx.globalCompositeOperation = 'lighter';
      // ---- shockwave rings
      for (const tb of bl) { const dt = t - tb; if (dt < 0 || dt > 1.6) continue; const q = dt / 1.6, r = mh * 0.15 + Math.max(W, H) * 0.55 * (1 - Math.pow(1 - q, 3)), a = Math.pow(1 - q, 1.6);
        const col = mix(acc, [255, 255, 255], 0.35); ctx.lineWidth = H * 0.012 * (1 - q) + 1;
        for (const [bl2, al] of [[H * 0.02, 0.7], [0, 0.9]]) { ctx.filter = bl2 && !o.lite ? `blur(${bl2}px)` : 'none'; ctx.strokeStyle = rgba(col, a * al); ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI); ctx.stroke(); }
        ctx.filter = 'none'; }
      // ---- sparks: ignition (intro) + bursts
      ctx.lineCap = 'round';
      const spark = (px, py, vx, vy, dt, life, lam, g, wd) => { const e = Math.exp(-lam * dt), k = (1 - e) / lam; const x = px + vx * k, y = py + vy * k + 0.5 * g * dt * dt;
        const cvx = vx * e, cvy = vy * e + g * dt, a = Math.pow(1 - dt / life, 1.3), hot = Math.max(0, 1 - dt / (life * 0.5));
        ctx.strokeStyle = rgba(mix(acc, [255, 255, 255], hot), a); ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - cvx * 0.035, y - cvy * 0.035); ctx.stroke(); };
      if (t < INTRO + 1) { const r = rng(9); for (const s of igSamples) { const vx = (r() - 0.5) * H * 0.25, vy = -H * (0.1 + 0.3 * r()), life = 0.5 + 0.5 * r(), dt = t - s[2];
        if (dt > 0 && dt < life) spark(s[0], s[1], vx, vy, dt, life, 2.5, H * 0.3, H * 0.002); } }
      for (const tb of bl) { const dt0 = t - tb; if (dt0 < 0 || dt0 > 2) continue; const r = rng(Math.round(tb * 10) + 17);
        for (let k = 0; k < 90; k++) { const s = samples[Math.floor(r() * samples.length)]; let ang = Math.atan2(s[1] - cy, s[0] - cx) + (r() - 0.5) * 1.2;
          const sp = H * (0.35 + 0.9 * r()), life = 0.7 + 1.1 * r(); if (dt0 < life) spark(s[0], s[1], Math.cos(ang) * sp, Math.sin(ang) * sp, dt0, life, 2.2, H * 0.25, H * 0.0028); } }
      // ---- ambient embers
      for (const e of embers) { const q = ((t / e.L) + e.off) % 1, x = e.x + e.sway * Math.sin(2 * Math.PI * (q * 2 + e.off)), y = e.y - e.rise * q, a = Math.sin(Math.PI * q) * 0.85 * fi;
        if (a < 0.01) continue; ctx.fillStyle = rgba(mix(acc, [255, 255, 255], 0.3), a); ctx.shadowColor = rgba(acc, a); ctx.shadowBlur = o.lite ? 0 : e.s * 4;
        ctx.beginPath(); ctx.arc(x, y, e.s, 0, 2 * Math.PI); ctx.fill(); }
      ctx.shadowBlur = 0; ctx.globalCompositeOperation = 'source-over';
      // ---- wordmark with glint
      if (o.layout === 'lockup' || o.layout === 'stack') { const ft = ss(2.2, 3.3, t); if (ft > 0) {
        tctx.clearRect(0, 0, W, H); tctx.globalCompositeOperation = 'source-over';
        tctx.font = `${fs}px ${o.font}`; tctx.letterSpacing = `${Math.round(fs * (0.06 + 0.04 * (1 - ft)))}px`; tctx.textBaseline = 'alphabetic';
        const tw = tctx.measureText(o.title).width, st = o.layout === 'stack', tx = st ? Math.round((W - tw) / 2) : txL;
        tctx.fillStyle = '#fff'; tctx.fillText(o.title, tx, ty);
        tctx.font = `${Math.round(fs * 0.26)}px ${o.font}`; tctx.letterSpacing = `${Math.round(fs * 0.05)}px`; tctx.fillStyle = rgba(acc, 1);
        tctx.fillText(o.sub, st ? Math.round((W - tctx.measureText(o.sub).width) / 2) : tx + fs * 0.02, ty + fs * (st ? 0.52 : 0.46));
        const lb = bl.filter(tb => t >= tb).pop(); const dt = lb === undefined ? 9 : t - lb;
        if (dt < 1.1) { const gx = tx - tw * 0.3 + tw * 1.6 * (dt / 1.1), g = tctx.createLinearGradient(gx - tw * 0.12, 0, gx + tw * 0.12, 0);
          g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, rgba(mix(acc, [255, 255, 255], 0.5), 1)); g.addColorStop(1, 'rgba(255,255,255,0)');
          tctx.globalCompositeOperation = 'source-atop'; tctx.fillStyle = g; tctx.fillRect(tx - tw, ty - fs, tw * 3, fs * 1.6); }
        ctx.globalAlpha = ft; ctx.shadowColor = rgba(acc, 0.55 + 0.4 * B); ctx.shadowBlur = H * 0.03; ctx.drawImage(tc, 0, 0); ctx.shadowBlur = 0; ctx.globalAlpha = 1; } }
    }
    setup();
    let raf = 0;
    return { render, setup, INTRO, T, play(startAt) { const t0 = performance.now() / 1000 - (startAt || 0); const loop = () => { render(performance.now() / 1000 - t0); raf = requestAnimationFrame(loop); }; cancelAnimationFrame(raf); loop(); }, stop() { cancelAnimationFrame(raf); } };
  }
  DogmaLogo.INTRO = INTRO; DogmaLogo.T = T;
  root.DogmaLogo = DogmaLogo;
})(typeof window !== 'undefined' ? window : this);
