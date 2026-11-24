const { chromium } = require('playwright'); const fs = require('fs');
const b = JSON.parse(fs.readFileSync(__dirname + '/brand.json'));
(async () => {
  const html = fs.readFileSync(__dirname + '/logo.html', 'utf8').replace('NAME_SHORT', b.name_short).replace('CITY', b.city);
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1200, height: 400 }, deviceScaleFactor: 1 });
  await p.setContent(html); await p.screenshot({ path: __dirname + '/logo.png', omitBackground: true }); await br.close(); console.log('logo ok');
})();
