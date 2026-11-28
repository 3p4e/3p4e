// usage: node render_logo_anim.js <scratch> <mode: sheet|frames> [t0 t1 fps outdir transparent layout W H]
const { chromium } = require('playwright'); const fs = require('fs');
const [S, mode, t0 = '0', t1 = '8', fps = '30', outdir = '', transp = '0', layout = 'lockup', W = '1920', H = '1080'] = process.argv.slice(2);
const svg = fs.readFileSync(S + '/brand/mark.svg', 'utf8'); const vb = svg.match(/viewBox="0 0 (\d+) (\d+)"/); const d = svg.match(/ d="([^"]+)"/)[1];
const font = fs.readFileSync(S + '/brand/fonts/RussoOne-400.ttf').toString('base64');
(async () => {
  const b = await chromium.launch({ args: ['--disable-gpu-vsync'] }); const p = await b.newPage({ viewport: { width: +W, height: +H } });
  await p.setContent(`<body style="margin:0;background:${transp === '1' ? 'transparent' : '#000'}"><canvas id="c" width="${W}" height="${H}"></canvas></body>`);
  await p.addScriptTag({ path: S + '/fx/dogma_logo.js' });
  await p.evaluate(async ({ font, d, w, h, transp, layout }) => { const f = new FontFace('Russo', `url(data:font/ttf;base64,${font})`); await f.load(); document.fonts.add(f);
    window.L = DogmaLogo(document.getElementById('c'), { d, vbW: +w, vbH: +h, transparent: transp === '1', layout }); }, { font, d, w: vb[1], h: vb[2], transp, layout });
  const grab = async t => { const u = await p.evaluate(t => { L.render(t); return document.getElementById('c').toDataURL('image/png'); }, t); return Buffer.from(u.split(',')[1], 'base64'); };
  if (mode === 'sheet') { const ts = [0.8, 1.6, 2.4, 3.2, 3.7, 4.4, 6.5, 7.7, 9.5, 11.7, 13.5, 15.4]; fs.mkdirSync(S + '/fx/sheet', { recursive: true });
    for (const t of ts) fs.writeFileSync(`${S}/fx/sheet/t_${t.toFixed(1)}.png`, await grab(t)); }
  else { fs.mkdirSync(outdir, { recursive: true }); const n = Math.round((+t1 - +t0) * +fps); const st = Date.now();
    for (let i = 0; i < n; i++) { fs.writeFileSync(`${outdir}/f_${String(i).padStart(5, '0')}.png`, await grab(+t0 + i / +fps)); if (i % 60 === 0) console.log(i, '/', n, ((Date.now() - st) / 1000).toFixed(0) + 's'); } }
  await b.close(); console.log('DONE');
})();
