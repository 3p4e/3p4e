const fs = require('fs');
const path = require('path');

const dir = __dirname;
global.window = {};
require(path.join(dir, 'menu-data.js'));
const DATA = global.window.MENU_DATA;

const CYR = {
  'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ж':'zh','з':'z','и':'i','ј':'j',
  'к':'k','л':'l','љ':'lj','м':'m','н':'n','њ':'nj','о':'o','п':'p','р':'r','с':'s',
  'т':'t','ќ':'kj','у':'u','ф':'f','х':'h','ц':'c','ч':'ch','џ':'dz','ш':'sh',
};
function slug(s) {
  return s.toLowerCase()
    .split('').map(ch => CYR[ch] !== undefined ? CYR[ch] : ch).join('')
    .replace(/\s+/g, '_')
    .replace(/[^a-z0-9_]/g, '');
}

const clips = [];
let itemId = 0;
for (const cat of DATA.categories) {
  for (const item of cat.items) {
    const price = item.price;
    const avail = item.available !== false;
    if (price === null || price === undefined || price === '' || !avail) continue;
    itemId++;
    const catL = cat.name.toLowerCase();
    const nameL = item.name.toLowerCase();
    let theme = 'unknown', gesture = 'cast';

    if (catL.includes('бургер')) {
      if (nameL.includes('веге')) { theme = 'garden_bloom'; gesture = 'vine_weave'; }
      else if (nameL.includes('чикен') || nameL.includes('пилеш')) { theme = 'phoenix_feather'; gesture = 'feather_flutter'; }
      else { theme = 'forge_fire'; gesture = 'hammer_strike'; }
    } else if (catL.includes('сендвич') || catL.includes('тост')) {
      theme = 'alchemy_press'; gesture = 'press_seal';
    } else if (catL.includes('врап')) {
      theme = 'spiral_binding'; gesture = 'spiral_bind';
    } else if (catL.includes('скара') || nameL.includes('ражнич') || nameL.includes('кебапче')) {
      theme = 'dragon_breath'; gesture = 'flame_breathe';
    } else if (catL.includes('похова') || nameL.includes('фри') || nameL.includes('помфрит') || nameL.includes('чипс')) {
      theme = 'lightning_cut'; gesture = 'arc_slash';
    } else if (catL.includes('вафл') || nameL.includes('вафла')) {
      theme = 'crystal_lattice'; gesture = 'lattice_weave';
    } else if (catL.includes('десерт') || nameL.includes('нутел') || nameL.includes('мармелад') || nameL.includes('фъстак') || nameL.includes('сутлијаш')) {
      theme = 'sugar_sorcery'; gesture = 'chocolate_write';
    } else if (catL.includes('кафе') || nameL.includes('еспресо') || nameL.includes('капучино') || nameL.includes('макијато') || nameL.includes('фрап') || nameL.includes('нес-кафе')) {
      theme = 'dark_elixir'; gesture = 'brew_conjure';
    } else if (catL.includes('пијало') || nameL.includes('милкшејк') || nameL.includes('смути') || nameL.includes('чај') || nameL.includes('бабл') || nameL.includes('сок') || nameL.includes('вода')) {
      theme = 'potion_mastery'; gesture = 'vortex_stir';
    } else if (catL.includes('салат')) {
      theme = 'fresh_conjuration'; gesture = 'seed_unfurl';
    }

    const clipId = cat.id + '_' + slug(item.name);
    clips.push({
      id: clipId,
      item_id: itemId,
      name: item.name,
      category: cat.name,
      category_id: cat.id,
      screen: cat.screen || 1,
      price: price,
      badge: item.badge || '',
      magic_theme: theme,
      gesture: gesture,
      day_clip: 'wand_' + clipId + '_day.mp4',
      night_clip: 'wand_' + clipId + '_night.mp4',
      duration_sec: 4.0,
      combos: [],
    });
  }
}

const out = {
  generated: new Date().toISOString().slice(0, 10),
  project: 'abracadabra-menu',
  total_clips: clips.length,
  themes: [...new Set(clips.map(c => c.magic_theme))],
  clips,
};
fs.writeFileSync(path.join(dir, 'clip_specification.json'), JSON.stringify(out, null, 2));

console.log('Total priced items needing clips:', clips.length);
console.log('Themes:', out.themes.join(', '));
console.log('Saved: clip_specification.json');
console.log('');
for (const c of clips) {
  console.log(`  screen ${c.screen}  ${c.id.padEnd(34)} ${c.name.padEnd(28)} ${c.magic_theme} / ${c.gesture}`);
}
