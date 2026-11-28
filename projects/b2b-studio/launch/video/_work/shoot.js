// node shoot.js jobs.json [filter]  -> renders each HTML job to PNG (transparent where asked)
const { chromium } = require('playwright'); const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).filter(j => !process.argv[3] || j.png.includes(process.argv[3]));
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await p.goto('file://' + j.html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    const bad = await p.evaluate(() => [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src));
    if (bad.length) console.log('MISSING IMG', j.png, bad);
    await p.screenshot({ path: j.png, omitBackground: !!j.transparent, clip: { x: 0, y: 0, width: j.w, height: j.h } });
    console.log('ok', j.png.split('/').pop()); await p.close();
  }
  await b.close();
})();
