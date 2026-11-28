// usage: node logo_pipe.js <S> <t0> <t1> <fps> <layout lockup|stack|mark> <W> <H>  -> PNG frames on stdout (image2pipe)
const { chromium } = require('playwright'); const fs = require('fs');
const [S, t0, t1, fps, layout, W, H] = process.argv.slice(2);
const svg = fs.readFileSync(S + '/brand/mark.svg', 'utf8'); const vb = svg.match(/viewBox="0 0 (\d+) (\d+)"/); const d = svg.match(/ d="([^"]+)"/)[1];
const font = fs.readFileSync(S + '/brand/fonts/RussoOne-400.ttf').toString('base64');
(async () => {
  const b = await chromium.launch({ args: ['--disable-gpu-vsync'] }); const p = await b.newPage({ viewport: { width: +W, height: +H } });
  await p.setContent(`<body style="margin:0;background:#000"><canvas id="c" width="${W}" height="${H}"></canvas></body>`);
  await p.addScriptTag({ path: __dirname + '/dogma_logo_kit.js' });
  await p.evaluate(async ({ font, d, w, h, layout }) => { const f = new FontFace('Russo', `url(data:font/ttf;base64,${font})`); await f.load(); document.fonts.add(f);
    window.L = DogmaLogo(document.getElementById('c'), { d, vbW: +w, vbH: +h, transparent: false, layout }); }, { font, d, w: vb[1], h: vb[2], layout });
  const n = Math.round((+t1 - +t0) * +fps);
  for (let i = 0; i < n; i++) { const u = await p.evaluate(t => { L.render(t); return document.getElementById('c').toDataURL('image/png'); }, +t0 + i / +fps);
    const buf = Buffer.from(u.split(',')[1], 'base64'); if (!process.stdout.write(buf)) await new Promise(r => process.stdout.once('drain', r)); }
  await b.close(); process.stderr.write('DONE ' + n + '\n');
})();
