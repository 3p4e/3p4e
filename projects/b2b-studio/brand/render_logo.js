const { chromium } = require('playwright'); const fs = require('fs');
const b = JSON.parse(fs.readFileSync(__dirname + '/brand.json'));
const ff = [[400,'RussoOne-400']].map(([w,n]) => `@font-face{font-family:'Russo';font-weight:${w};src:url(data:font/ttf;base64,${fs.readFileSync(__dirname + '/fonts/' + n + '.ttf').toString('base64')}) format('truetype')}`).join('');
const mark = fs.readFileSync(__dirname + '/mark.svg', 'utf8'), bold = fs.readFileSync(__dirname + '/mark_bold.svg', 'utf8');
(async () => {
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1600, height: 400 } });
  const html = fs.readFileSync(__dirname + '/logo.html', 'utf8').replace('FONTFACES', ff).replace('MARK_SVG', mark).replace('NAME_SHORT', b.name_short).replace('CITY', b.subline || b.city);
  await p.setContent(html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); await p.screenshot({ path: __dirname + '/logo.png', omitBackground: true });
  // mark-only assets: gold, white, black (large), bold gold square icon for favicon / watermark
  for (const [name, col, svg, size] of [['mark_gold', b.accent, mark, 1024], ['mark_white', '#ffffff', mark, 1024], ['mark_black', '#111111', mark, 1024], ['icon_512', b.accent, bold, 512]]) {
    const q = await br.newPage({ viewport: { width: size, height: size } });
    const bg = name === 'icon_512' ? `background:${b.bg};border-radius:96px;` : '';
    await q.setContent(`<body style="margin:0;background:transparent"><div style="width:${size}px;height:${size}px;display:grid;place-items:center;${bg}"><div style="width:${name === 'icon_512' ? 82 : 94}%;height:${name === 'icon_512' ? 72 : 94}%;color:${col}">${svg.replace('<svg ', '<svg style="width:100%;height:100%;display:block" ')}</div></div></body>`);
    await q.screenshot({ path: `${__dirname}/${name}.png`, omitBackground: true }); await q.close();
  }
  await br.close(); console.log('logo ok');
})();
