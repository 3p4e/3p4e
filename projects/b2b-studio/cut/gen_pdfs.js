// One-page A4 offer PDF per company (local language), rendered from HTML with Playwright/Chromium.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const S = '/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad';
const O = JSON.parse(fs.readFileSync(S + '/cut/offers.json')); const B = JSON.parse(fs.readFileSync(S + '/brand/brand.json'));
const b64 = f => 'data:image/' + (f.endsWith('.png') ? 'png' : 'jpeg') + ';base64,' + fs.readFileSync(f).toString('base64');
const OSW = w => 'data:font/ttf;base64,' + fs.readFileSync(S + '/brand/fonts/RussoOne-400.ttf').toString('base64');
const OUT = S + '/offers_pdf'; fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage();
  for (const c of O.companies) {
    const t = O.text[c.lang], p = O.prices[c.lang], f = x => x.replace('{c}', c.name);
    const posters = c.films.map(([id, label]) => `<div class="film"><img src="${b64(`${S}/previews/${id}_poster.jpg`)}"><div>${label}</div></div>`).join('');
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>
      @font-face{font-family:Russo;font-weight:400;src:url(${OSW(600)})} @page{size:A4;margin:0} body{margin:0;font-family:'DejaVu Sans',sans-serif;color:#1d1d22;font-size:12.2px}
      .top{background:${B.bg};color:#fff;padding:22px 34px;display:flex;align-items:center;justify-content:space-between}
      .top img{height:54px} .top .c{font-size:11px;color:#bbb;text-align:right;line-height:1.6}
      .wrap{padding:22px 34px} h1{font-family:Russo;font-weight:400;font-size:30px;margin:4px 0 8px;letter-spacing:.5px} h2{font-family:Russo;font-weight:400;font-size:16px;margin:18px 0 8px;color:#b7791f;text-transform:uppercase;letter-spacing:1px}
      .intro{font-size:13px;line-height:1.55} .films{display:flex;gap:14px} .film{flex:1;font-size:11.5px;font-weight:bold} .film img{width:100%;border-radius:8px;display:block;margin-bottom:5px}
      table{width:100%;border-collapse:collapse} td{padding:9px 10px;border-bottom:1px solid #eee;vertical-align:top} td.p{font-weight:bold;white-space:nowrap;color:#b7791f;text-align:right}
      td.n{font-weight:bold;width:120px} .small{font-size:10.5px;color:#666;line-height:1.5} .cta{margin-top:18px;background:#fff7e0;border-left:5px solid ${B.accent};padding:12px 16px;font-size:13.5px}
      .foot{position:absolute;bottom:18px;left:34px;right:34px;font-size:9.5px;color:#888;border-top:1px solid #eee;padding-top:8px}
    </style></head><body>
      <div class="top"><img src="${b64(S + '/brand/logo.png')}"><div class="c">${[B.phone, B.email, B.web].filter(Boolean).join('<br>')}</div></div>
      <div class="wrap"><h1>${f(t.title)}</h1><div class="intro">${f(t.intro)}</div>
      <h2>${t.made}</h2><div class="films">${posters}</div><div class="small" style="margin-top:6px">${t.formats}</div>
      <h2>${t.offer}</h2><table>
        <tr><td class="n">${t.pilot}</td><td>${t.pilot_d}</td><td class="p">${p.pilot}</td></tr>
        <tr><td class="n">${t.launch}</td><td>${t.launch_d}</td><td class="p">${p.launch}</td></tr>
        <tr><td class="n">${t.monthly}</td><td>${t.monthly_d}</td><td class="p">${p.monthly}</td></tr></table>
      <div class="small" style="margin-top:6px">${t.terms} ${t.price_note}</div>
      <h2>${t.how}</h2><div class="small" style="font-size:12px;color:#333">${t.how_d}</div>
      <div class="cta"><b>${t.next}</b><br>${[B.phone, B.email].filter(Boolean).join(' · ')}</div></div>
      <div class="foot">${B.name} · ${f(t.intro).split('.').slice(-2).join('.').trim()}</div></body></html>`;
    await pg.setContent(html, { waitUntil: 'load' });
    await pg.pdf({ path: `${OUT}/${c.id}_offer.pdf`, format: 'A4', printBackground: true });
    console.log('OK', c.id);
  }
  await br.close(); console.log('PDFS_DONE');
})();
