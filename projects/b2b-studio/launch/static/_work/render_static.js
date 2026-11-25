// BIG DOGMA static social kit renderer: profile pictures + platform covers (HTML -> Playwright PNG).
// usage: node render_static.js <S> [only-name ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const S = process.argv[2]; const ONLY = process.argv.slice(3);
const OUT = `${S}/launch/static`, W = `${OUT}/_work`, HTML = `${W}/html`;
fs.mkdirSync(HTML, { recursive: true });
const B = JSON.parse(fs.readFileSync(`${S}/brand/brand.json`, 'utf8'));
const FONT = `file://${S}/brand/fonts/RussoOne-400.ttf`;
const svgOf = f => fs.readFileSync(`${S}/brand/${f}`, 'utf8');
const D_REG = svgOf('mark.svg').match(/ d="([^"]+)"/)[1], D_BOLD = svgOf('mark_bold.svg').match(/ d="([^"]+)"/)[1];
const VB = '0 0 5776 3590', AR = 5776 / 3590;
const ST = n => `file://${W}/src/s_${n}.png`;

// metallic gold monogram (fill gradient instead of flat currentColor)
function mark({ h, bold = true, id = 'g', colors = ['#ffe7a3', '#f2c14e', '#c98f24'], glow = true }) {
  const w = Math.round(h * AR);
  return `<svg class="mk" width="${w}" height="${h}" viewBox="${VB}" style="display:block;${glow ? 'filter:drop-shadow(0 0 ' + Math.round(h * .09) + 'px rgba(242,193,78,.42)) drop-shadow(0 0 ' + Math.round(h * .03) + 'px rgba(255,214,120,.5))' : ''}">
<defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${colors[0]}"/><stop offset=".45" stop-color="${colors[1]}"/><stop offset="1" stop-color="${colors[2]}"/></linearGradient></defs>
<path fill="url(#${id})" fill-rule="evenodd" d="${bold ? D_BOLD : D_REG}"/></svg>`;
}
const GRAIN = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;

const BASE_CSS = `@font-face{font-family:'Russo';src:url(${FONT}) format('truetype')}
*{box-sizing:border-box;margin:0;padding:0} html,body{background:#0d0d0f}
.c{position:relative;overflow:hidden;background:#0d0d0f;font-family:'Russo',sans-serif;color:#fff}
.layer{position:absolute;inset:0}
.grain{position:absolute;inset:0;background-image:${GRAIN};opacity:.07;mix-blend-mode:overlay;pointer-events:none}
.name{white-space:nowrap;line-height:1;color:#fff;letter-spacing:.045em;text-shadow:0 2px 18px rgba(0,0,0,.6)}
.sub{white-space:pre;line-height:1;color:#f2c14e;letter-spacing:.3em}
.tag{white-space:nowrap;line-height:1;color:#ece6da;letter-spacing:.02em;text-shadow:0 2px 16px rgba(0,0,0,.7)}
.tag b{font-weight:400;color:#f2c14e}
.rule{height:1px;background:linear-gradient(90deg,transparent,rgba(242,193,78,.75),transparent)}
.fr{position:absolute;overflow:hidden;border-radius:var(--rad,10px);box-shadow:0 18px 50px rgba(0,0,0,.65),0 0 0 1px rgba(242,193,78,.32)}
.fr img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.78) saturate(.92) contrast(1.04)}
.note{position:absolute;white-space:nowrap;color:rgba(236,230,218,.8);letter-spacing:.08em;font-family:'DejaVu Sans',sans-serif;line-height:1;transform:translateX(-50%);text-shadow:0 1px 6px rgba(0,0,0,.85)}
`;

// background: aurora glows (brand gold + the animated logo's arcane blue / violet), all very low key
function aurora(Wd, Ht, cx, cy, r) {
  return `<div class="layer" style="background:
   radial-gradient(${r * 1.0}px ${r * .62}px at ${cx}px ${cy}px, rgba(242,193,78,.16), transparent 70%),
   radial-gradient(${r * 1.4}px ${r * 1.0}px at ${Wd * .12}px ${Ht * .1}px, rgba(70,180,255,.07), transparent 70%),
   radial-gradient(${r * 1.4}px ${r * 1.0}px at ${Wd * .9}px ${Ht * .95}px, rgba(190,110,255,.07), transparent 70%),
   linear-gradient(180deg,#0f0f12,#0b0b0d)"></div>`;
}
// a row of stills receding in perspective toward the centre (lockup sits at the vanishing point)
function wing({ side, x, y, fw, h, frames, gap, rot = 38, rad = 10, fade = .5, persp = 1600 }) {
  const n = frames.length, w = fw * n + gap * (n - 1);
  const items = frames.map((f, i) => `<div class="fr" style="--rad:${rad}px;left:${i * (fw + gap)}px;top:0;width:${fw}px;height:${h}px"><img src="${ST(f)}"></div>`).join('');
  const dir = side === 'L' ? 'to right' : 'to left';
  const mask = `linear-gradient(${dir}, #000 0%, rgba(0,0,0,.9) ${Math.round((1 - fade) * 100)}%, transparent 100%)`;
  const left = side === 'L' ? x : x - w; // x = outer edge (L: left edge, R: right edge)
  return `<div style="position:absolute;left:${left}px;top:${y}px;width:${w}px;height:${h}px;perspective:${persp}px;perspective-origin:50% 50%">
  <div style="position:absolute;inset:0;transform-origin:${side === 'L' ? 'left' : 'right'} center;transform:rotateY(${side === 'L' ? rot : -rot}deg);-webkit-mask-image:${mask};mask-image:${mask}">${side === 'L' ? items : frames.slice().reverse().map((f, i) => `<div class="fr" style="--rad:${rad}px;left:${i * (fw + gap)}px;top:0;width:${fw}px;height:${h}px"><img src="${ST(f)}"></div>`).join('')}</div></div>`;
}
// central dark veil so the lockup always reads over the stills
const veil = (cx, cy, rx, ry, a = .92) => `<div class="layer" style="background:radial-gradient(${rx}px ${ry}px at ${cx}px ${cy}px, rgba(13,13,15,${a}) 0%, rgba(13,13,15,${a * .8}) 45%, transparent 100%)"></div>`;

// lockup: mark + (name / sub), optional tagline under, all centred on (cx, cy)
function lockup({ cx, cy, mh, nameSize, subSize, tagSize, gapMark, gapTag, layout = 'stack', bold = true, ruleW = 0 }) {
  const mw = mh * AR;
  const tag = `<div class="tag" style="font-size:${tagSize}px"><b>AI</b> видео за вашиот бизнис</div>`;
  const rule = ruleW ? `<div class="rule" style="width:${ruleW}px;margin:${Math.round(gapTag * .55)}px auto ${Math.round(gapTag * .55)}px"></div>` : `<div style="height:${gapTag}px"></div>`;
  if (layout === 'row') { // one line: [mark][name/sub] | tagline
    return `<div style="position:absolute;left:${cx}px;top:${cy}px;transform:translate(-50%,-50%);display:flex;align-items:center;gap:${gapMark}px">
      ${mark({ h: mh, bold })}
      <div><div class="name" style="font-size:${nameSize}px">BIG DOGMA</div><div class="sub" style="font-size:${subSize}px;margin-top:${Math.round(nameSize * .26)}px">${B.subline}</div></div>
      <div style="width:1px;align-self:stretch;margin:${Math.round(mh * .08)}px ${Math.round(gapMark * .7)}px;background:linear-gradient(180deg,transparent,rgba(242,193,78,.7),transparent)"></div>
      ${tag}</div>`;
  }
  return `<div style="position:absolute;left:${cx}px;top:${cy}px;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center">
    <div style="display:flex;align-items:center;gap:${gapMark}px">${mark({ h: mh, bold })}
      <div><div class="name" style="font-size:${nameSize}px">BIG DOGMA</div><div class="sub" style="font-size:${subSize}px;margin-top:${Math.round(nameSize * .26)}px">${B.subline}</div></div></div>
    ${rule}${tag}</div>`;
}
// AI disclosure for the AI stills: centred at (cx, top), inside each platform's safe area (checked by guides.py)
const note = (cx, top, size) => `<div class="note" style="left:${cx}px;top:${top}px;font-size:${size}px">AI-генерирани кадри</div>`;
const page = (Wd, Ht, body, extra = '') => `<!doctype html><html><head><meta charset="utf-8"><style>${BASE_CSS}${extra}</style></head><body><div class="c" style="width:${Wd}px;height:${Ht}px">${body}<div class="grain"></div></div></body></html>`;

// ---------- assets ----------
const A = {}; const BOXES = {};

// Profile pictures: monogram inside the central circle (platform crop), bold strokes for small display sizes
A.profile_1080 = { w: 1080, h: 1080, html: page(1080, 1080, `
  <div class="layer" style="background:radial-gradient(520px 420px at 540px 540px, rgba(242,193,78,.17), transparent 70%),radial-gradient(900px 900px at 540px 540px,#141417,#0b0b0d 75%)"></div>
  <div style="position:absolute;left:540px;top:540px;transform:translate(-50%,-50%)" id="mk">${mark({ h: 495, bold: true })}</div>`) };
A.profile_white_bg_1080 = { w: 1080, h: 1080, html: page(1080, 1080, `
  <div class="layer" style="background:radial-gradient(900px 900px at 540px 540px,#ffffff,#f4f1ea 80%)"></div>
  <div style="position:absolute;left:540px;top:540px;transform:translate(-50%,-50%)" id="mk">${mark({ h: 495, bold: true, id: 'gw', colors: ['#c9932a', '#b07c14', '#8a5c06'], glow: false })}</div>`, '.grain{display:none}') };

// LinkedIn company cover 1128x191: logo overlaps bottom-left on desktop, sides crop on mobile -> compact stacked lockup in the centre
A.linkedin_cover_1128x191 = { w: 1128, h: 191, html: page(1128, 191, `
  ${aurora(1128, 191, 564, 95, 560)}
  ${wing({ side: 'L', x: 0, y: 30, fw: 170, h: 131, frames: ['construction', 'steel'], gap: 10, rot: 40, rad: 7, persp: 600 })}
  ${wing({ side: 'R', x: 1128, y: 30, fw: 170, h: 131, frames: ['product', 'realestate'], gap: 10, rot: 40, rad: 7, persp: 600 })}
  ${veil(564, 92, 400, 140, .92)}
  ${lockup({ cx: 564, cy: 84, mh: 80, nameSize: 50, subSize: 14, tagSize: 31, gapMark: 18, gapTag: 16, ruleW: 360 })}
  ${note(564, 160, 13)}`) };

// Facebook cover 1640x624: desktop shows the central 1640x462 band, mobile crops the sides; all key content inside the central 820x312
A.facebook_cover_1640x624 = { w: 1640, h: 624, html: page(1640, 624, `
  ${aurora(1640, 624, 820, 312, 900)}
  ${wing({ side: 'L', x: 0, y: 177, fw: 290, h: 270, frames: ['construction', 'steel'], gap: 14, rot: 40, rad: 10, persp: 900 })}
  ${wing({ side: 'R', x: 1640, y: 177, fw: 290, h: 270, frames: ['product', 'realestate'], gap: 14, rot: 40, rad: 10, persp: 900 })}
  ${veil(820, 318, 500, 250, .9)}
  ${lockup({ cx: 820, cy: 298, mh: 126, nameSize: 80, subSize: 22, tagSize: 40, gapMark: 28, gapTag: 42, ruleW: 460 })}
  ${note(820, 428, 24)}`) };

// YouTube banner 2560x1440: TV shows everything, desktop the 2560x423 band, mobile the 1546x423 centre -> lockup in the centre safe area
A.youtube_banner_2560x1440 = { w: 2560, h: 1440, html: page(2560, 1440, `
  ${aurora(2560, 1440, 1280, 720, 1500)}
  ${wing({ side: 'L', x: 0, y: 552, fw: 300, h: 336, frames: ['construction', 'steel', 'food'], gap: 20, rot: 40, rad: 12, persp: 1400 })}
  ${wing({ side: 'R', x: 2560, y: 552, fw: 300, h: 336, frames: ['product', 'realestate', 'wine'], gap: 20, rot: 40, rad: 12, persp: 1400 })}
  ${veil(1280, 720, 720, 290, .9)}
  ${lockup({ cx: 1280, cy: 702, mh: 172, nameSize: 112, subSize: 30, tagSize: 58, gapMark: 38, gapTag: 56, ruleW: 640 })}
  ${note(1280, 874, 32)}`) };

// X header 1500x500: avatar overlaps bottom-left, some clients crop top/bottom -> lockup centred, slightly above middle
A.x_header_1500x500 = { w: 1500, h: 500, html: page(1500, 500, `
  ${aurora(1500, 500, 750, 235, 820)}
  ${wing({ side: 'L', x: 0, y: 120, fw: 245, h: 230, frames: ['construction', 'steel'], gap: 14, rot: 40, rad: 9, persp: 900 })}
  ${wing({ side: 'R', x: 1500, y: 120, fw: 245, h: 230, frames: ['product', 'realestate'], gap: 14, rot: 40, rad: 9, persp: 900 })}
  ${veil(750, 245, 470, 225, .9)}
  ${lockup({ cx: 750, cy: 228, mh: 116, nameSize: 72, subSize: 20, tagSize: 37, gapMark: 26, gapTag: 38, ruleW: 420 })}
  ${note(750, 350, 24)}`) };

(async () => {
  const br = await chromium.launch();
  for (const [name, a] of Object.entries(A)) {
    if (ONLY.length && !ONLY.includes(name)) continue;
    const f = `${HTML}/${name}.html`; fs.writeFileSync(f, a.html);
    const p = await br.newPage({ viewport: { width: a.w, height: a.h }, deviceScaleFactor: 1 });
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
    await p.screenshot({ path: `${OUT}/${name}.png`, clip: { x: 0, y: 0, width: a.w, height: a.h } });
    const box = await p.evaluate(() => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const e of document.querySelectorAll('.mk,.name,.sub,.tag')) { const r = e.getBoundingClientRect(); x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); } return [x0, y0, x1, y1].map(Math.round); });
    BOXES[name] = box;
    const nb = await p.evaluate(() => { const e = document.querySelector('.note'); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(Math.round); });
    if (nb) BOXES[name + '_note'] = nb;
    // mark-only layer for the circle-crop check of the profile pictures
    if (name.startsWith('profile')) {
      await p.evaluate(() => { document.querySelectorAll('.layer,.grain').forEach(e => e.remove()); document.documentElement.style.background = 'transparent'; document.body.style.background = 'transparent'; document.querySelector('.c').style.background = 'transparent'; });
      await p.screenshot({ path: `${W}/${name}_markonly.png`, omitBackground: true });
    }
    await p.close(); console.log('ok', name);
  }
  await br.close();
  const bf = `${W}/boxes.json`; const old = fs.existsSync(bf) ? JSON.parse(fs.readFileSync(bf)) : {}; fs.writeFileSync(bf, JSON.stringify(Object.assign(old, BOXES), null, 1));
})();
