// Hero background: a fullscreen playlist of the AI logo films (light copies, media/lite/intro) until the visitor picks a category (film
// or gallery chip); then it plays that category's clips. "All" goes back to the logo films.
// Two stacked videos: while one plays, the next clip is already loading in the other; at the end of the clip the next one starts and the
// crossfade happens only once it is really playing (owner, 2026-11-26: "they behave like a slide show"). If the next clip is not ready, the
// current one holds its last frame instead of going black. Reduced motion / Save-Data: the poster image only.
(function () {
  var hero = document.querySelector('.hero'), D = window.DOGMA_HERO; if (!hero || !D) return;
  var first = hero.querySelector('video');
  if ((window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) || (navigator.connection && navigator.connection.saveData)) return;
  var vs = [first, first.cloneNode(false)], cur = 0, list = [], i = 0, key = '', busy = false, pend = null;
  vs[1].innerHTML = ''; first.parentNode.insertBefore(vs[1], first.nextSibling);
  vs.forEach(function (v) { v.removeAttribute('loop'); v.removeAttribute('autoplay'); v.muted = true; v.playsInline = true; v.preload = 'auto'; v.style.transition = 'opacity .9s'; });
  vs[1].style.opacity = 0; first.style.opacity = 1;
  function shuffle(a) { a = a.slice(); for (var k = a.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)), t = a[k]; a[k] = a[j]; a[j] = t; } return a; }
  function load(v, src) { while (v.firstChild) v.removeChild(v.firstChild); v.src = src; v.load(); }
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  function preload() { if (list.length) load(vs[1 - cur], list[(i + 1) % list.length]); }
  function swap() {   // start the preloaded clip; fade over to it once it is playing
    if (busy || !list.length) return; busy = true;
    var nv = vs[1 - cur], ov = vs[cur];
    function go() {
      nv.removeEventListener('playing', go); pend = null; nv.style.opacity = 1; ov.style.opacity = 0; cur = 1 - cur; i = (i + 1) % list.length; busy = false;
      setTimeout(function () { ov.pause(); preload(); }, 950);
    }
    pend = go; nv.addEventListener('playing', go); nv.currentTime = 0; play(nv);
  }
  vs.forEach(function (v) {
    v.addEventListener('timeupdate', function () { if (v === vs[cur] && v.duration && v.duration - v.currentTime < 0.45) swap(); });
    v.addEventListener('ended', function () { if (v === vs[cur]) swap(); });
    v.addEventListener('error', function () { if (v === vs[cur]) { busy = false; i = (i + 1) % list.length; load(v, list[i]); play(v); preload(); } else preload(); });
  });
  function use(k) {
    var l = k === 'all' || !D.cat[k] ? D.intro : D.cat[k]; if (!l || !l.length || k === key) return; key = k;
    if (pend) { vs.forEach(function (v) { v.removeEventListener('playing', pend); }); pend = null; }
    list = shuffle(l); i = list.length - 1; busy = false; preload(); swap();
  }
  use('all');
  document.addEventListener('click', function (e) {
    var c = e.target.closest && e.target.closest('.chip'); if (!c) return;
    use(c.dataset.c || c.dataset.g || c.dataset.f || 'all');
  });
})();
