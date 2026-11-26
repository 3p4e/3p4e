// Header logo player v4 (owner, 2026-11-26): one mark size for every effect, transparent everywhere, no visible box, and transitions
// that belong to the two effects they join.
//  * AI effect loops (LTX clips of the BD mark alone on black): list.js gives each clip's mark box and main colour; every frame is drawn
//    so the clip's mark lands exactly on the canvas engine's mark box (same size, same place), then keyed to transparent (alpha = brightness).
//  * The slot fades out softly at its edges (CSS mask in site.css), so glows dissolve instead of being cut.
//  * Each effect runs 3-5 s. In its last ~1.2 s the transition runs ALONG THE MARK'S OWN STROKES (the 70 segments of DOGMA_FXMARK):
//    the outgoing effect sheds particles in its own colour off the lines, an energy front sweeps the strokes in the incoming effect's
//    colour, the effects cross under the front, and incoming particles gather back onto the lines.
// Reduced motion / Save-Data: canvas engine only (still mark on reduced motion).
(function () {
  var el = document.querySelector('.brand .lfx-in'); if (!el) return;
  var RAW = (window.DOGMA_HDR || []).slice(), BASE = window.DOGMA_HDR_BASE || 'logo_fx/hdr/', fx = null;
  var CL = RAW.map(function (x) { return typeof x === 'string' ? { id: x, bb: [.2, .2, .6, .6], col: [242, 193, 78] } : x; });
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, save = navigator.connection && navigator.connection.saveData;
  if (window.DogmaLogoFX) fx = DogmaLogoFX.mount(el, { text: '', pad: .2, padY: .13, res: 70, dur: .6, fixed: 4.6, minMark: .55, skip: ['text'], mode: 'random' });
  if (reduce || !fx || !fx.pause) return;
  if (save) CL = [];
  var M = window.DOGMA_FXMARK, VB = M.viewBox, SEG = M.segs;
  function mk(z) { var c = document.createElement('canvas'); c.setAttribute('aria-hidden', 'true'); c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none;' + z; el.appendChild(c); return c; }
  var cv = mk('opacity:0'), c = cv.getContext('2d', { willReadFrequently: true });       // keyed AI clip, same box as the engine canvas
  var tv = mk('z-index:2'), t = tv.getContext('2d');                                     // transition layer
  var vids = [0, 1].map(function () { var v = document.createElement('video'); v.muted = v.defaultMuted = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.setAttribute('muted', ''); v.preload = 'auto'; v.crossOrigin = 'anonymous'; return v; });
  var cur = null, curItem = null, nextItem = null, mode = 'canvas', segEnd = 0, swapped = false, last = '', P = [], colOut = [242, 193, 78], colIn = [242, 193, 78];
  var GOLD = [242, 193, 78], TR = 1200;
  function pick() { var o = CL.filter(function (x) { return x.id !== last; }); var it = o[Math.floor(Math.random() * o.length)] || CL[0]; last = it.id; return it; }
  function size() { [cv, tv].forEach(function (x) { if (x.width !== fx.W || x.height !== fx.H) { x.width = fx.W; x.height = fx.H; } }); }
  // ---- colours: the clip's own colour, or a sample of what the canvas engine is drawing right now
  function sampleEngine() {
    try { var w = fx.W, h = fx.H, d = fx.c.getImageData(0, 0, w, h).data, r = 0, g = 0, b = 0, n = 0;
      for (var i = 0; i < d.length; i += 4 * 7) if (d[i + 3] > 120) { r += d[i]; g += d[i + 1]; b += d[i + 2]; n++; }
      if (!n) return GOLD; var m = Math.max(r, g, b) / n || 1; return [r / n * 255 / m | 0, g / n * 255 / m | 0, b / n * 255 / m | 0];
    } catch (e) { return GOLD; }
  }
  // ---- mark geometry in device px (engine transform: x = ox + (mx - VB0) * k)
  function pt(s, u) { return [fx.ox + (s[0] + (s[2] - s[0]) * u - VB[0]) * fx.k, fx.oy + (s[1] + (s[3] - s[1]) * u - VB[1]) * fx.k]; }
  function spawn() {   // particles sit on the strokes; each knows the stroke point it belongs to
    P = []; for (var i = 0; i < 150; i++) { var s = SEG[i % SEG.length], u = Math.random(), p = pt(s, u), a = Math.random() * 6.283;
      P.push({ x: p[0], y: p[1], a: a, sp: .4 + Math.random(), r: .6 + Math.random() * 1.4, ph: Math.random() }); }
  }
  // stroke order for the energy front: left to right along the mark, so it reads as one sweep
  var ORD = SEG.map(function (s, i) { return [Math.min(s[0], s[2]), i]; }).sort(function (a, b) { return a[0] - b[0]; }).map(function (x) { return x[1]; });
  function rgba(c3, a) { return 'rgba(' + c3[0] + ',' + c3[1] + ',' + c3[2] + ',' + a + ')'; }
  function trans(q) {   // q 0 -> 1 over the transition, swap at .5
    size(); var W = tv.width, H = tv.height, d = fx.dpr || 1, k = fx.k; t.clearRect(0, 0, W, H); t.globalCompositeOperation = 'lighter';
    var out = Math.max(0, 1 - q / .55), inn = Math.max(0, (q - .45) / .55);
    // 1) outgoing effect sheds particles off its own strokes, in its own colour, drifting outward and up
    P.forEach(function (p) {
      if (out > 0) { var dd = (1 - out) * 14 * d * p.sp; t.fillStyle = rgba(colOut, out * .9);
        t.beginPath(); t.arc(p.x + Math.cos(p.a) * dd, p.y + Math.sin(p.a) * dd - (1 - out) * 6 * d, p.r * d, 0, 6.283); t.fill(); }
      // 3) incoming particles gather back onto the strokes, in the incoming colour
      if (inn > 0) { var di = (1 - inn) * 16 * d * p.sp; t.fillStyle = rgba(colIn, inn * (1 - inn) * 3);
        t.beginPath(); t.arc(p.x - Math.cos(p.a + p.ph) * di, p.y - Math.sin(p.a + p.ph) * di, p.r * d * .9, 0, 6.283); t.fill(); }
    });
    // 2) energy front sweeps the strokes in the incoming colour, brightest at the swap, then settles into the new effect
    var front = Math.min(1, q / .62) * (ORD.length + 8), lw = Math.max(1.2, 30 * k);
    t.lineCap = 'round'; t.shadowBlur = 10 * d;
    for (var j = 0; j < ORD.length; j++) {
      var age = front - j; if (age <= 0) break; var s = SEG[ORD[j]], g = Math.max(0, 1 - age / 8) + .35 * Math.sin(Math.PI * Math.min(1, q * 1.3)) * (q < .8 ? 1 : (1 - q) / .2);
      if (g <= 0.01) continue; var a = pt(s, 0), b = pt(s, 1), mix = Math.min(1, age / 4);
      var col = [colIn[0] * mix + 255 * (1 - mix) | 0, colIn[1] * mix + 255 * (1 - mix) | 0, colIn[2] * mix + 255 * (1 - mix) | 0];
      t.shadowColor = rgba(colIn, 1); t.strokeStyle = rgba(col, Math.min(1, g)); t.lineWidth = lw * (.6 + .5 * Math.max(0, 1 - age / 6));
      t.beginPath(); t.moveTo(a[0], a[1]); t.lineTo(b[0], b[1]); t.stroke();
    }
    t.shadowBlur = 0; t.globalCompositeOperation = 'source-over';
    // cross the effects underneath the front
    var oo = q < .38 ? 1 : q < .5 ? 1 - (q - .38) / .12 : 0, io = q < .5 ? 0 : q < .66 ? (q - .5) / .16 : 1;
    if (mode === 'video') cv.style.opacity = q < .5 ? oo : io; fx.cv.style.opacity = mode === 'video' ? (q < .5 ? 0 : 0) : (q < .5 ? oo : io);
  }
  function key() {   // clip frame -> canvas: the clip's mark box onto the engine's mark box, black keyed out
    var v = cur, it = curItem; if (!v || v.readyState < 2 || !it) return; size(); var vw = v.videoWidth, vh = v.videoHeight; if (!vw) return;
    var bb = it.bb, sx = fx.bw / (bb[2] * vw), sy = fx.bh / (bb[3] * vh), s = Math.min(sx, sy), dw = vw * s, dh = vh * s;
    var dx = fx.ox + fx.bw / 2 - (bb[0] + bb[2] / 2) * vw * s, dy = fx.oy + fx.bh / 2 - (bb[1] + bb[3] / 2) * vh * s;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, cv.width, cv.height); c.drawImage(v, dx, dy, dw, dh);
    var im = c.getImageData(0, 0, cv.width, cv.height), dd = im.data;
    for (var i = 0; i < dd.length; i += 4) {
      var m = Math.max(dd[i], dd[i + 1], dd[i + 2]), a = (m - 16) * 1.15;
      if (a <= 0) { dd[i + 3] = 0; continue; } if (a > 255) a = 255; var kk = 255 / Math.max(m, 1);
      dd[i] *= kk; dd[i + 1] *= kk; dd[i + 2] *= kk; dd[i + 3] = a;
    }
    c.putImageData(im, 0, 0);
  }
  function plan() {   // what comes next; preload a clip
    nextItem = CL.length && Math.random() < .65 ? pick() : null;
    if (nextItem) { var v = vids[cur === vids[0] ? 1 : 0]; v.src = BASE + nextItem.id + '.mp4'; v.load(); }
  }
  function startSeg(now) { segEnd = now + 3000 + Math.random() * 2000; swapped = false; plan(); }
  function swap() {
    if (nextItem) { var v = cur === vids[0] ? vids[1] : vids[0]; if (cur) cur.pause(); cur = v; curItem = nextItem; v.currentTime = 0; v.play().catch(function () { CL = []; });
      if (mode !== 'video') fx.pause(); mode = 'video';
    } else { if (cur) cur.pause(); cur = null; curItem = null; if (mode === 'canvas') fx.next(); else fx.resume(); mode = 'canvas'; }
  }
  var inT = false;
  function frame(now) {
    requestAnimationFrame(frame); if (document.hidden) return;
    if (mode === 'video') key();
    var left = segEnd - now;
    if (left <= TR) {
      if (!inT) { inT = true; colOut = mode === 'video' && curItem ? curItem.col : sampleEngine(); colIn = nextItem ? nextItem.col : GOLD; spawn(); }
      var q = Math.min(1, 1 - left / TR); trans(q);
      if (q >= .5 && !swapped) { swapped = true; swap(); }
      if (left <= 0) { inT = false; t.clearRect(0, 0, tv.width, tv.height); cv.style.opacity = mode === 'video' ? 1 : 0; fx.cv.style.opacity = mode === 'video' ? 0 : 1; startSeg(now); }
    }
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden) { if (cur) cur.pause(); } else { if (mode === 'video' && cur) cur.play().catch(function () {}); segEnd = performance.now() + 3000; inT = false; } });
  startSeg(performance.now()); requestAnimationFrame(frame);
})();
