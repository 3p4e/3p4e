// Header logo player (owner, 2026-11-26): every effect runs 3-5 s; in its last second a burst transition (flash, particle burst,
// shockwave, sparkle swirl or lightning crackle) blooms over the mark and the next effect is swapped in under the peak of the flash.
// Effects alternate between AI effect loops (LTX clips of the BD mark alone on black, keyed to transparent on a canvas, so the mark
// floats on the page with no box) and the canvas effects of logo_fx.js. Reduced motion / Save-Data: canvas engine only (still mark).
(function () {
  var el = document.querySelector('.brand .lfx-in'); if (!el) return;
  var CL = (window.DOGMA_HDR || []).slice(), BASE = window.DOGMA_HDR_BASE || 'logo_fx/hdr/', fx = null;   // pitch pages load the loops from bigdogma.tech
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, save = navigator.connection && navigator.connection.saveData;
  if (window.DogmaLogoFX) fx = DogmaLogoFX.mount(el, { text: '', pad: .08, padY: .1, res: 70, dur: .6, fixed: 4.6, minMark: .55, skip: ['text'], mode: 'random' });
  if (reduce || !fx || !fx.pause) return;
  if (save) CL = [];
  function mk(z) { var c = document.createElement('canvas'); c.setAttribute('aria-hidden', 'true'); c.style.cssText = 'position:absolute;pointer-events:none;display:block;' + z; el.appendChild(c); return c; }
  var cv = mk('inset:-4% -6%;width:112%;height:108%;opacity:0'), c = cv.getContext('2d', { willReadFrequently: true });
  var bv = mk('inset:0;width:100%;height:100%;z-index:2'), b = bv.getContext('2d');   // burst layer, larger than the slot
  var vids = [0, 1].map(function () { var v = document.createElement('video'); v.muted = v.defaultMuted = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.setAttribute('muted', ''); v.preload = 'auto'; v.crossOrigin = 'anonymous'; return v; });
  var cur = null, mode = '', segEnd = 0, swapped = false, nextKind = '', last = '', tStyle = 0, parts = [], t0 = performance.now();
  var STY = ['flash', 'burst', 'ring', 'swirl', 'bolt'], GOLD = [242, 193, 78];
  function pick() { var o = CL.filter(function (x) { return x !== last; }); last = o[Math.floor(Math.random() * o.length)] || CL[0]; return last; }
  function plan() {   // choose what comes next and preload it if it is a clip
    nextKind = CL.length && Math.random() < .6 ? 'video' : 'canvas';
    if (nextKind === 'video') { var v = vids[cur === vids[0] ? 1 : 0]; v.src = BASE + pick() + '.mp4'; v.load(); }
  }
  function startSeg() { segEnd = performance.now() + (3000 + Math.random() * 2000); swapped = false; tStyle = STY[Math.floor(Math.random() * STY.length)]; parts = []; plan(); }
  function swap() {
    if (nextKind === 'video') {
      var v = cur === vids[0] ? vids[1] : vids[0]; if (cur) cur.pause(); cur = v; v.currentTime = 0;
      var p = v.play(); if (p && p.catch) p.catch(function () { CL = []; });
      if (mode !== 'video') { fx.pause(); cv.style.opacity = 1; } mode = 'video';
    } else {
      if (cur) cur.pause(); cv.style.opacity = 0;
      if (mode === 'canvas') fx.next(); else fx.resume(); mode = 'canvas';
    }
  }
  function key() {   // video frame -> canvas with alpha = brightest channel (the black drops out)
    var v = cur; if (!v || v.readyState < 2) return; var w = v.videoWidth, h = v.videoHeight; if (!w) return;
    if (cv.width !== w) { cv.width = w; cv.height = h; }
    c.drawImage(v, 0, 0, w, h); var im = c.getImageData(0, 0, w, h), d = im.data;
    for (var i = 0; i < d.length; i += 4) {
      var m = Math.max(d[i], d[i + 1], d[i + 2]), a = (m - 14) * 1.12;
      if (a <= 0) { d[i + 3] = 0; continue; } if (a > 255) a = 255; var k = 255 / Math.max(m, 1);
      d[i] *= k; d[i + 1] *= k; d[i + 2] *= k; d[i + 3] = a;
    }
    c.putImageData(im, 0, 0);
  }
  function rgba(c3, a) { return 'rgba(' + c3[0] + ',' + c3[1] + ',' + c3[2] + ',' + a + ')'; }
  function burst(q) {   // q: 0 -> 1 over the last second; peak (swap) at q = .5
    var W = bv.width, H = bv.height, cx = W / 2, cy = H / 2, R = Math.min(W, H) * .5, pk = Math.sin(Math.PI * q);
    b.clearRect(0, 0, W, H); b.globalCompositeOperation = 'lighter';
    if (!parts.length) for (var i = 0; i < 70; i++) { var an = Math.random() * 6.283, sp = .35 + Math.random() * .75; parts.push([an, sp, Math.random(), 1 + Math.random() * 2.2]); }
    var g = b.createRadialGradient(cx, cy, 0, cx, cy, R * (.35 + .65 * pk));
    g.addColorStop(0, 'rgba(255,250,235,' + (.95 * pk) + ')'); g.addColorStop(.35, rgba(GOLD, .55 * pk)); g.addColorStop(1, 'rgba(242,120,40,0)');
    if (tStyle !== 'bolt' || pk > .6) { b.fillStyle = g; b.fillRect(0, 0, W, H); }
    if (tStyle === 'burst' || tStyle === 'flash') parts.forEach(function (p) {
      var r = R * p[1] * q * 1.1, x = cx + Math.cos(p[0]) * r, y = cy + Math.sin(p[0]) * r * .7, al = (1 - q) * (q < .1 ? q * 10 : 1);
      b.fillStyle = p[2] > .6 ? 'rgba(255,255,255,' + al + ')' : rgba(GOLD, al); b.beginPath(); b.arc(x, y, p[3] * (W / 260), 0, 6.283); b.fill();
    });
    if (tStyle === 'ring') for (var k = 0; k < 3; k++) {
      var rr = R * (q * 1.2 - k * .12); if (rr <= 0) continue;
      b.strokeStyle = rgba(k ? [255, 240, 200] : GOLD, (1 - q) * .9); b.lineWidth = (6 - k * 2) * (W / 260) * (1 - q * .6);
      b.beginPath(); b.ellipse(cx, cy, rr, rr * .62, 0, 0, 6.283); b.stroke();
    }
    if (tStyle === 'swirl') parts.forEach(function (p, i) {
      var an = p[0] + q * 6 * (i % 2 ? 1 : -1), r = R * (.15 + p[1] * .7) * (1 - Math.abs(q - .5)), x = cx + Math.cos(an) * r, y = cy + Math.sin(an) * r * .65;
      b.fillStyle = i % 3 ? rgba(GOLD, pk) : 'rgba(255,255,255,' + pk + ')'; b.beginPath(); b.arc(x, y, p[3] * .8 * (W / 260), 0, 6.283); b.fill();
    });
    if (tStyle === 'bolt') for (var j = 0; j < 4; j++) {
      if (Math.random() > .55 + pk * .4) continue; var a0 = Math.random() * 6.283, x0 = cx, y0 = cy;
      b.strokeStyle = j % 2 ? 'rgba(200,190,255,' + pk + ')' : 'rgba(255,255,255,' + pk + ')'; b.lineWidth = 1.6 * (W / 260); b.beginPath(); b.moveTo(x0, y0);
      for (var s = 1; s <= 7; s++) { x0 = cx + Math.cos(a0) * R * .14 * s + (Math.random() - .5) * R * .12; y0 = cy + Math.sin(a0) * R * .1 * s + (Math.random() - .5) * R * .1; b.lineTo(x0, y0); }
      b.stroke();
    }
    b.globalCompositeOperation = 'source-over';
  }
  function size() { var r = bv.getBoundingClientRect(), d = Math.min(2, devicePixelRatio || 1); bv.width = Math.max(2, r.width * d); bv.height = Math.max(2, r.height * d); }
  size(); addEventListener('resize', size);
  function frame(now) {
    requestAnimationFrame(frame);
    if (document.hidden) return;
    if (mode === 'video') key();
    var left = segEnd - now;
    if (left <= 1000) {
      var q = Math.min(1, 1 - left / 1000); burst(q);
      if (q >= .5 && !swapped) { swapped = true; swap(); }
      if (left <= 0) { b.clearRect(0, 0, bv.width, bv.height); startSeg(); }
    }
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden) { if (cur) cur.pause(); } else { if (mode === 'video' && cur) cur.play().catch(function () {}); segEnd = performance.now() + 3000; } });
  mode = 'canvas'; startSeg(); requestAnimationFrame(frame);
})();
