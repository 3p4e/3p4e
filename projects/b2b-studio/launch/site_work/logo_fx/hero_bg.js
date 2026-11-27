// Page background: the AI logo films (light copies, media/lite/intro) in random order, all the time, in a fixed layer behind the whole page
// (owner, 2026-11-26: "BD logo videos rotating at random all the time in the background, even when you scroll"). Picking an industry no
// longer changes it.
// Two stacked videos: while one plays, the next film is already loading in the other; near the end of the film the next one starts and the
// crossfade happens only once it is really playing (no slideshow effect). If the next film is not ready, the current one holds its last frame.
// Paused while the tab is hidden. Reduced motion / Save-Data: the poster image only.
(function () {
  var box = document.getElementById('bdbg') || document.querySelector('.hero'), D = window.DOGMA_HERO; if (!box || !D) return;
  var first = box.querySelector('video'); if (!first) return;
  if ((window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) || (navigator.connection && navigator.connection.saveData)) {
    first.removeAttribute('autoplay'); first.pause(); return;
  }
  var vs = [first, first.cloneNode(false)], cur = 0, all = [], bag = [], curSrc = null, nextSrc = null, busy = false, pend = null;
  vs[1].innerHTML = ''; first.parentNode.insertBefore(vs[1], first.nextSibling);
  vs.forEach(function (v) { v.removeAttribute('loop'); v.removeAttribute('autoplay'); v.muted = true; v.playsInline = true; v.preload = 'auto'; v.style.transition = 'opacity .9s'; });
  vs[1].style.opacity = 0; first.style.opacity = 1;
  function shuffle(a) { a = a.slice(); for (var k = a.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)), t = a[k]; a[k] = a[j]; a[j] = t; } return a; }
  function load(v, src) { while (v.firstChild) v.removeChild(v.firstChild); v.src = src; v.load(); }
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  function draw() {   // shuffled queue, refilled when empty, never the film that is playing now
    if (!bag.length) { bag = shuffle(all); if (bag[0] === curSrc && bag.length > 1) bag.push(bag.shift()); }
    return bag.shift();
  }
  function preload() { if (all.length) { nextSrc = draw(); load(vs[1 - cur], nextSrc); } }
  function swap() {   // start the preloaded film; fade over to it once it is playing
    if (busy || !all.length || document.hidden) return; busy = true;
    var nv = vs[1 - cur], ov = vs[cur];
    function go() {
      nv.removeEventListener('playing', go); pend = null; nv.style.opacity = 1; ov.style.opacity = 0; cur = 1 - cur; curSrc = nextSrc; busy = false;
      setTimeout(function () { ov.pause(); preload(); }, 950);
    }
    pend = go; nv.addEventListener('playing', go); nv.currentTime = 0; play(nv);
  }
  vs.forEach(function (v) {
    v.addEventListener('timeupdate', function () { if (v === vs[cur] && v.duration && v.duration - v.currentTime < 0.45) swap(); });
    v.addEventListener('ended', function () { if (v === vs[cur]) swap(); });
    v.addEventListener('error', function () { if (v === vs[cur]) { busy = false; curSrc = draw(); load(v, curSrc); play(v); preload(); } else preload(); });
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) vs.forEach(function (v) { v.pause(); }); else { busy = false; play(vs[cur]); }
  });
  function start() { if (start.done) return; start.done = true; all = (D.intro || []).slice(); if (!all.length) return; preload(); swap(); }
  if (window.BDBG_WAIT) window.BDBG_START = start; else start();   // company pages start it when their splash ends
})();
