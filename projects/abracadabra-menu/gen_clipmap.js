const fs = require('fs');
const path = require('path');
const dir = __dirname;

const spec = JSON.parse(fs.readFileSync(path.join(dir, 'clip_specification.json'), 'utf8'));
const map = {};
for (const c of spec.clips) {
  // key is category id + '::' + item name (names are unique within a category)
  map[c.category_id + '::' + c.name] = {
    clip: 'assets/video/' + c.day_clip,
    effect: c.effect,
    theme: c.magic_theme,
    price: c.price,
    screen: c.screen,
  };
}

const out = '/* AUTO-GENERATED from clip_specification.json — do not edit by hand */\n' +
  'window.CLIP_MAP = ' + JSON.stringify(map, null, 2) + ';\n' +
  'window.CLIP_COUNT = ' + spec.clips.length + ';\n';

fs.writeFileSync(path.join(dir, 'assets', 'clip-map.js'), out);
console.log('clip-map.js written, entries:', Object.keys(map).length);
console.log('sample key:', Object.keys(map)[2]);
