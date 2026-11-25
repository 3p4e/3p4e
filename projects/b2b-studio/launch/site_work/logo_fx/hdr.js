// Header logo: AI effect loops (LTX clips of the BD mark alone on black) alternating with the canvas effects of logo_fx.js.
// The black is keyed out per frame (alpha = brightest channel) on a small canvas, so the logo floats on the page with no box,
// in every browser, from plain mp4. Reduced motion / Save-Data: canvas engine only (which itself shows the still mark on reduced motion).
(function () {
  var el = document.querySelector('.brand .lfx-in'); if (!el) return;
  var CL = (window.DOGMA_HDR || []).slice(), BASE = 'logo_fx/hdr/', mode = '', shown = 0, last = '', fx = null;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, save = navigator.connection && navigator.connection.saveData;
  if (window.DogmaLogoFX) fx = DogmaLogoFX.mount(el, { text: '', pad: .22, padY: .27, res: 70, dur: .85, minMark: .55, skip: ['text'], mode: 'random',
    onchange: function () { if (mode === 'canvas' && ++shown > 1 && CL.length) toVideo(); } });
  if (!CL.length || reduce || save || !fx || !fx.pause) return;
  var cv = document.createElement('canvas'), c = cv.getContext('2d', { willReadFrequently: true }), v = document.createElement('video'), raf = 0;
  cv.setAttribute('aria-hidden', 'true'); cv.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none;opacity:0;transition:opacity .35s';
  v.muted = v.defaultMuted = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.setAttribute('muted', ''); v.preload = 'auto'; v.crossOrigin = 'anonymous';
  el.appendChild(cv);
  function pick() { var o = CL.filter(function (x) { return x !== last; }); last = o[Math.floor(Math.random() * o.length)] || CL[0]; return last; }
  function draw() {
    raf = requestAnimationFrame(draw); if (v.readyState < 2) return;
    var w = v.videoWidth, h = v.videoHeight; if (!w) return; if (cv.width !== w) { cv.width = w; cv.height = h; }
    c.drawImage(v, 0, 0, w, h); var im = c.getImageData(0, 0, w, h), d = im.data;
    for (var i = 0; i < d.length; i += 4) {
      var m = Math.max(d[i], d[i + 1], d[i + 2]), a = (m - 14) * 1.12;
      if (a <= 0) { d[i + 3] = 0; continue; } if (a > 255) a = 255; var k = 255 / Math.max(m, 1);
      d[i] = d[i] * k; d[i + 1] = d[i + 1] * k; d[i + 2] = d[i + 2] * k; d[i + 3] = a;
    }
    c.putImageData(im, 0, 0);
  }
  function toVideo() {
    mode = 'video'; fx.pause(); v.src = BASE + pick() + '.mp4';
    var p = v.play(); if (p && p.catch) p.catch(toCanvasForever);
    cv.style.opacity = 1; cancelAnimationFrame(raf); draw();
  }
  function toCanvas() { mode = 'canvas'; shown = 0; cv.style.opacity = 0; cancelAnimationFrame(raf); fx.resume(); }
  function toCanvasForever() { CL = []; toCanvas(); }
  v.addEventListener('ended', function () { Math.random() < .3 ? toCanvas() : toVideo(); });
  v.addEventListener('error', toCanvasForever);
  document.addEventListener('visibilitychange', function () { if (mode === 'video') { if (document.hidden) v.pause(); else v.play().catch(function () {}); } });
  toVideo();
})();
