// Page background: the AI logo films in random order, all the time, in a fixed layer behind the whole page (owner, 2026-11-26: "BD logo
// videos rotating at random all the time in the background, even when you scroll").
// 2026-11-27 (owner: "poor resolution and takes time to load"): desktop plays sharper 720p copies (media/lite/intro, 1280x704), phones and
// slow connections 480p copies (media/lite480/intro). Every next film is downloaded completely (fetch -> blob) while the current one plays,
// and the switch happens only once it is in memory, so a slow server never shows a frozen or buffering frame: until the next film is
// ready the current one simply loops. Paused while the tab is hidden. Reduced motion / Save-Data: the poster image only.
(function () {
  var box = document.getElementById('bdbg') || document.querySelector('.hero'), D = window.DOGMA_HERO; if (!box || !D) return;
  var first = box.querySelector('video'); if (!first) return;
  var C = navigator.connection || {};
  if ((window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) || C.saveData) { first.removeAttribute('autoplay'); first.pause(); return; }
  var LOW = Math.min(screen.width, screen.height) < 600 || innerWidth < 760 || /(^|-)2g|3g/.test(C.effectiveType || '') || (C.downlink && C.downlink < 1.5);
  var vs = [first, first.cloneNode(false)], cur = 0, all = [], bag = [], curSrc = null, next = null, busy = false;
  vs[1].innerHTML = ''; first.parentNode.insertBefore(vs[1], first.nextSibling);
  vs.forEach(function (v) { v.removeAttribute('loop'); v.removeAttribute('autoplay'); v.removeAttribute('src'); v.muted = true; v.playsInline = true; v.preload = 'auto'; v.style.transition = 'opacity .9s'; });
  vs[1].style.opacity = 0; first.style.opacity = 1;   // the first video shows its poster until the first film is in memory
  function shuffle(a) { a = a.slice(); for (var k = a.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)), t = a[k]; a[k] = a[j]; a[j] = t; } return a; }
  function variant(src) { return LOW ? src.replace('/lite/intro/', '/lite480/intro/') : src; }
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  function draw() { if (!bag.length) { bag = shuffle(all); if (bag[0] === curSrc && bag.length > 1) bag.push(bag.shift()); } return bag.shift(); }
  function setSrc(v, url) { if (v._blob && v._blob !== url) URL.revokeObjectURL(v._blob); v._blob = url; v.src = url; v.load(); }
  // download the next film completely, then put it in the idle video; tries another film if one fails
  function prefetch(tries) {
    if (!all.length || next) return; tries = tries || 0; var src = draw(), want = variant(src);
    fetch(want, { mode: 'cors', credentials: 'omit' }).then(function (r) { if (!r.ok) throw r.status; return r.blob(); }).then(function (b) {
      var url = URL.createObjectURL(b), nv = vs[1 - cur];
      nv.addEventListener('canplaythrough', function ok() { nv.removeEventListener('canplaythrough', ok); next = src; if (!curSrc) swap(); }, { once: true });
      setSrc(nv, url);
    }).catch(function () { if (want !== src && tries < 2) { LOW = false; } if (tries < 4) setTimeout(function () { prefetch(tries + 1); }, 800); });
  }
  function swap() {   // the next film is in memory: start it and crossfade
    if (busy || !next || document.hidden) return; busy = true;
    var nv = vs[1 - cur], ov = vs[cur];
    function go() { nv.removeEventListener('playing', go); nv.style.opacity = 1; ov.style.opacity = 0; cur = 1 - cur; curSrc = next; next = null; busy = false;
      setTimeout(function () { ov.pause(); prefetch(); }, 950); }
    nv.addEventListener('playing', go); nv.currentTime = 0; play(nv);
  }
  vs.forEach(function (v) {
    v.addEventListener('timeupdate', function () { if (v === vs[cur] && v.duration && v.duration - v.currentTime < 0.45 && next) swap(); });
    v.addEventListener('ended', function () { if (v !== vs[cur]) return; if (next) swap(); else { v.currentTime = 0; play(v); } });   // not ready yet: loop
  });
  document.addEventListener('visibilitychange', function () { if (document.hidden) vs.forEach(function (v) { v.pause(); }); else if (curSrc) { busy = false; play(vs[cur]); } });
  function start() { if (start.done) return; start.done = true; all = (D.intro || []).slice(); if (!all.length) return; prefetch(); }
  if (window.BDBG_WAIT) window.BDBG_START = start; else start();   // company pages start it when their splash ends
})();
