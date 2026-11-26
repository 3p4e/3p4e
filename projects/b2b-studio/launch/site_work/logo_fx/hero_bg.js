// Hero background: a fullscreen playlist of the AI logo films (the BD mark cast in gold, carved in ice, drawn by fireworks...) until
// the visitor picks a category (film or gallery chip); then it plays that category's clips. "All" goes back to the logo films.
// Two stacked videos crossfade so there is no black gap between clips. Reduced motion / Save-Data: the poster image only.
(function () {
  var hero = document.querySelector('.hero'), D = window.DOGMA_HERO; if (!hero || !D) return;
  var first = hero.querySelector('video');
  if ((window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) || (navigator.connection && navigator.connection.saveData)) return;
  var vs = [first, first.cloneNode(false)], cur = 1, list = [], i = 0, key = '';
  vs[1].innerHTML = ''; first.parentNode.insertBefore(vs[1], first.nextSibling);
  vs.forEach(function (v) { v.removeAttribute('loop'); v.muted = true; v.style.transition = 'opacity .9s'; v.addEventListener('ended', next); v.addEventListener('error', next); });
  vs[1].style.opacity = 0; first.style.opacity = 1;
  function shuffle(a) { a = a.slice(); for (var k = a.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)), t = a[k]; a[k] = a[j]; a[j] = t; } return a; }
  function load(v, src) { while (v.firstChild) v.removeChild(v.firstChild); v.src = src; v.load(); }
  function next() {
    if (!list.length) return; var nv = vs[1 - cur], ov = vs[cur]; i = (i + 1) % list.length;
    load(nv, list[i]); var p = nv.play(); if (p && p.catch) p.catch(function () {});
    nv.style.opacity = 1; ov.style.opacity = 0; cur = 1 - cur;
  }
  function use(k) {
    var l = k === 'all' || !D.cat[k] ? D.intro : D.cat[k]; if (!l || !l.length || k === key) return; key = k;
    list = shuffle(l); i = -1; next();
  }
  use('all');
  document.addEventListener('click', function (e) {
    var c = e.target.closest && e.target.closest('.chip'); if (!c) return;
    use(c.dataset.g || c.dataset.f || 'all');
  });
})();
