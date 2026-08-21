// Compresses the raw Higgsfield PNGs into small JPEG data URIs and writes
// assets/art.js exposing window.GE_ART = { hero, stages{...}, strains{...} }.
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const RAW = '/home/user/3p4e/green-empire/assets/raw';
const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
const pg = await b.newPage();

async function toJpeg(file, w, q) {
  if (!existsSync(file)) { console.warn('missing', file); return null; }
  const b64 = readFileSync(file).toString('base64');
  return await pg.evaluate(async ({ b64, w, q }) => {
    const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
    const s = w / img.width; const c = document.createElement('canvas');
    c.width = w; c.height = Math.round(img.height * s);
    c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL('image/jpeg', q);
  }, { b64, w, q });
}

const slugs = ['ohrid_crystal','pelister_frost','vardar_gold','skopje_haze','bitola_kush',
  'shar_diesel','galicica_dream','prespa_punch','macedonian_royal','imperial_reserve'];

const art = { hero: null, stages: {}, strains: {} };
art.hero = await toJpeg(RAW + '/hero.png', 760, 0.82);
for (const [k, f] of [['seedling','stage_seedling'],['veg','stage_veg'],['flower','stage_flower'],['harvest','stage_harvest']]) {
  art.stages[k] = await toJpeg(RAW + '/' + f + '.png', 380, 0.85);
}
for (let i = 0; i < 10; i++) art.strains[slugs[i]] = await toJpeg(RAW + '/strain_' + (i + 1) + '.png', 240, 0.82);

writeFileSync('/home/user/3p4e/green-empire/assets/art.js', 'window.GE_ART=' + JSON.stringify(art) + ';\n');
console.log('art.js written ~', (JSON.stringify(art).length / 1048576).toFixed(2), 'MB',
  '| hero', !!art.hero, '| stages', Object.entries(art.stages).map(([k,v])=>k+':'+(v?'ok':'MISS')).join(','),
  '| strains', Object.values(art.strains).filter(Boolean).length + '/10');
await b.close();
