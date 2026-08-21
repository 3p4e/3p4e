// Generates the second wave of artwork with the Venice API:
//   * drying-room and curing-room banners for those tabs
//   * per-strain flowering variants, edited from the existing harvest plate so
//     the pot, framing and lighting stay identical across every variant
// Usage: VENICE_API_KEY=... node assets/gen_more.mjs
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const RAW = new URL('./raw/', import.meta.url).pathname;
const KEY = process.env.VENICE_API_KEY;
if (!KEY) { console.error('VENICE_API_KEY not set'); process.exit(1); }

const NEG = 'No text, no words, no letters, no watermark, no people, no hands.';

// ── Scene banners (fresh generations) ───────────────────────────────────
const SCENES = [
  ['dry_room',
    'Interior of a dark cannabis drying room: trimmed branches hanging upside down in ' +
    'neat rows from horizontal wires, dim warm light from the side, gentle haze, ' +
    'shallow depth of field, moody and atmospheric, photoreal. ' + NEG,
    1024, 576],
  ['cure_room',
    'A row of large glass mason jars on a dark wooden shelf, each packed with cured ' +
    'cannabis buds, warm rim lighting catching the glass, a hygrometer visible inside ' +
    'one jar, dark moody background, shallow depth of field, photoreal. ' + NEG,
    1024, 576],
  ['trim_room',
    'Close-up of trimming scissors and freshly manicured cannabis buds on a stainless ' +
    'steel tray, sugar leaves scattered around, warm task lighting, dark background, ' +
    'photoreal, shallow depth of field. ' + NEG,
    1024, 576],
];

for (const [name, prompt, width, height] of SCENES) {
  const out = RAW + name + '.jpg';
  if (existsSync(out)) { console.log('have', name); continue; }
  const res = await fetch('https://api.venice.ai/api/v1/image/generate', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'flux-2-pro', prompt, width, height,
      format: 'png', safe_mode: false, return_binary: true }),
  });
  if (!res.ok) { console.error(name, 'HTTP', res.status, (await res.text()).slice(0, 160)); continue; }
  writeFileSync(out, Buffer.from(await res.arrayBuffer()));
  console.log('scene', name, (existsSync(out) ? 'ok' : 'fail'));
}

// ── Per-strain flowering looks (edits of the harvest plate) ─────────────
// Each entry keeps the same plant shape but changes the bud colouring, so
// strains read as visually distinct while staying the same "grow".
const LOOKS = [
  ['look_frost', 'Make the buds bright frosty silver-white, caked in glittering trichomes, ' +
    'with pale mint-green leaves.'],
  ['look_purple', 'Make the buds deep violet-purple with dark plum sugar leaves and ' +
    'contrasting orange pistils.'],
  ['look_orange', 'Make the buds burnt-orange and amber, dense with fiery orange pistils ' +
    'over olive-green leaves.'],
  ['look_gold', 'Make the buds warm golden-yellow and honey-toned, with amber resin ' +
    'and yellow-green leaves.'],
  ['look_pink', 'Make the buds rose-pink and magenta-tipped with silvery frost and ' +
    'deep green leaves.'],
];

const base = RAW + 'stage_harvest_black.png';
if (!existsSync(base)) { console.error('missing base plate', base); process.exit(1); }
const baseB64 = readFileSync(base).toString('base64');

for (const [name, change] of LOOKS) {
  const out = RAW + name + '.png';
  if (existsSync(out)) { console.log('have', name); continue; }
  const prompt =
    `Keep the plant's exact shape, size, pose, pot and framing identical to the reference, ` +
    `and keep the background pure solid black (#000000), flat with no gradient. ${change} ` +
    `Photoreal, sharp, evenly lit. ${NEG}`;
  const res = await fetch('https://api.venice.ai/api/v1/image/edit', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'flux-2-max-edit', image: baseB64, prompt,
      output_format: 'png', safe_mode: false }),
  });
  if (!res.ok) { console.error(name, 'HTTP', res.status, (await res.text()).slice(0, 160)); continue; }
  const buf = Buffer.from(await res.arrayBuffer());
  const sig = buf.subarray(0, 4).toString('hex');
  if (sig !== '89504e47' && !sig.startsWith('ffd8')) {
    console.error(name, 'unexpected body:', buf.toString('utf8').slice(0, 140)); continue;
  }
  writeFileSync(out, buf);
  console.log('look', name, (buf.length / 1024).toFixed(0) + 'KB');
}
console.log('done');
