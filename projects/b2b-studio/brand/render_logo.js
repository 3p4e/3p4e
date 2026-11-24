const { chromium } = require('playwright'); const fs = require('fs');
const b = JSON.parse(fs.readFileSync(__dirname + '/brand.json'));
const mark = fs.readFileSync(__dirname + '/mark.svg', 'utf8'), bold = fs.readFileSync(__dirname + '/mark_bold.svg', 'utf8');
(async () => {
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1200, height: 400 } });
  const html = fs.readFileSync(__dirname + '/logo.html', 'utf8').replace('MARK_SVG', mark).replace('NAME_SHORT', b.name_short).replace('CITY', b.city);
  await p.setContent(html); await p.screenshot({ path: __dirname + '/logo.png', omitBackground: true });
  // mark-only assets: gold, white, black (large), bold gold square icon for favicon / watermark
  for (const [name, col, svg, size] of [['mark_gold', b.accent, mark, 1024], ['mark_white', '#ffffff', mark, 1024], ['mark_black', '#111111', mark, 1024], ['icon_512', b.accent, bold, 512]]) {
    const q = await br.newPage({ viewport: { width: size, height: size } });
    const bg = name === 'icon_512' ? `background:${b.bg};border-radius:96px;` : '';
    await q.setContent(`<body style="margin:0;background:transparent"><div style="width:${size}px;height:${size}px;display:grid;place-items:center;${bg}"><div style="height:${name === 'icon_512' ? 70 : 92}%;color:${col}">${svg.replace('<svg ', '<svg style="height:100%;width:auto;display:block" ')}</div></div></body>`);
    await q.screenshot({ path: `${__dirname}/${name}.png`, omitBackground: true }); await q.close();
  }
  await br.close(); console.log('logo ok');
})();
