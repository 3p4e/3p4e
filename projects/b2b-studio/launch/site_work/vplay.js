// BIG DOGMA video helper (studio site + company pages). Films with a player stream adaptively: HLS 720p / 480p / 360p, built on the
// server by hls_build.sh (<dir>/hls/<name>/master.m3u8 next to <dir>/<name>.mp4). Playback starts on a light level and climbs as the
// connection allows; capped to the player size. A film without an HLS copy (yet), or a browser that can play neither, falls back to the
// 720p MP4. hls.js (Apache-2.0, self-hosted in vendor/) is loaded on the first film only.
(function () {
  const me = document.currentScript && document.currentScript.src;
  const BASE = me ? new URL('.', me).href : 'https://bigdogma.tech/';
  const NATIVE = !!document.createElement('video').canPlayType('application/vnd.apple.mpegurl');
  let lib = null;
  const load = () => lib || (lib = new Promise((res, rej) => {
    const s = document.createElement('script'); s.src = BASE + 'vendor/hls.light.min.js'; s.async = true;
    s.onload = () => res(window.Hls); s.onerror = rej; document.head.appendChild(s); }));
  // only films that hls_build.sh covers: studio films, showreel, how-to film, company films in a pitch page's own folder
  function hlsUrl(src) {
    try {
      const u = new URL(src, location.href), p = u.pathname;
      const ok = /\/films\/[^/]+\.mp4$/.test(p) || /\/media\/(showreel|showreel_9x16|howto)\.mp4$/.test(p) ||
                 (/^pitch\./.test(u.host) && /^\/[A-Za-z0-9_-]{8,}\/[^/]+\.mp4$/.test(p));
      if (!ok) return null;
      const m = p.match(/^(.*\/)([^/]+)\.mp4$/); return u.origin + m[1] + 'hls/' + m[2] + '/master.m3u8' + u.search;
    } catch (e) { return null; }
  }
  function detach(v) { if (v._hls) { try { v._hls.destroy(); } catch (e) {} v._hls = null; } }
  function mp4(v, src, play) { detach(v); v.src = src; if (play) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } }
  function native(v, h, src, play) {
    v.addEventListener('error', function f() { v.removeEventListener('error', f); if ((v.currentSrc || '').indexOf('.m3u8') > 0) mp4(v, src, play); });
    v.src = h; if (play) { const p = v.play(); if (p && p.catch) p.catch(() => {}); }
  }
  // attach a film to a <video>; play = start as soon as it can
  function attach(v, src, play) {
    detach(v); const tok = (v._tok = (v._tok || 0) + 1), h = hlsUrl(src);
    if (!h) return mp4(v, src, play);
    load().then(Hls => {
      if (tok !== v._tok) return;                                   // another film was opened meanwhile
      if (Hls && Hls.isSupported()) {
        const hls = new Hls({ capLevelToPlayerSize: true, maxBufferLength: 20, abrEwmaDefaultEstimate: 1200000 });
        let parsed = false; v._hls = hls;
        hls.on(Hls.Events.MANIFEST_PARSED, () => { parsed = true; if (play) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } });
        hls.on(Hls.Events.ERROR, (e, d) => {
          if (!d.fatal) return;
          if (parsed && d.type === Hls.ErrorTypes.MEDIA_ERROR) { hls.recoverMediaError(); return; }
          const t = v.currentTime || 0; mp4(v, src, play); if (t) v.currentTime = t;   // no HLS copy / network trouble: the MP4
        });
        hls.loadSource(h); hls.attachMedia(v);
      } else if (NATIVE) native(v, h, src, play); else mp4(v, src, play);
    }).catch(() => { if (tok === v._tok) (NATIVE ? native(v, h, src, play) : mp4(v, src, play)); });
  }
  // a <video controls preload="none"> whose src is the MP4: switch it to adaptive streaming on the first play
  function lazy(v) {
    v.addEventListener('play', function f() {
      if (v._hls || (v.currentSrc || '').indexOf('.m3u8') > 0) return;
      const src = v.getAttribute('src') || v.currentSrc; if (!src || !hlsUrl(src)) return;
      v.removeEventListener('play', f); v.pause(); attach(v, src, true);
    });
  }
  window.BDV = { attach, detach, lazy, hlsUrl };
})();
