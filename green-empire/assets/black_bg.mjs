// Re-renders each growth stage onto a flat black background using Venice's
// image edit endpoint. Black keys far more cleanly than the painted
// checkerboard Venice returns for "transparent", which left a white halo
// baked into the semi-transparent leaf edges.
// Usage: node assets/black_bg.mjs
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const RAW = new URL('./raw/', import.meta.url).pathname;
const KEY = process.env.VENICE_API_KEY;
if (!KEY) { console.error('VENICE_API_KEY not set'); process.exit(1); }

const SUBJECT = {
  stage_seedling: 'the tiny cannabis seedling and its black fabric pot',
  stage_veg: 'the leafy vegetative cannabis plant and its black fabric pot',
  stage_flower: 'the early-flowering cannabis plant and its black fabric pot',
  stage_harvest: 'the mature frosty cannabis plant and its black fabric pot',
};

for (const [name, subject] of Object.entries(SUBJECT)) {
  const src = RAW + name + '.png';
  const out = RAW + name + '_black.png';
  if (!existsSync(src)) { console.warn('missing', name); continue; }
  if (existsSync(out)) { console.log('have', name); continue; }

  const prompt =
    `Keep ${subject} exactly as they are — same shape, size, position and framing. ` +
    'Replace the background with pure solid black (#000000), perfectly flat, no gradient, ' +
    'no wall, no floor, no shadow. Light the plant clearly so its edges read against the black. ' +
    'No text, no watermark.';

  const res = await fetch('https://api.venice.ai/api/v1/image/edit', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'flux-2-max-edit',
      image: readFileSync(src).toString('base64'),
      prompt,
      output_format: 'png',
      safe_mode: false,
    }),
  });
  if (!res.ok) { console.error(name, 'HTTP', res.status, (await res.text()).slice(0, 200)); continue; }

  const buf = Buffer.from(await res.arrayBuffer());
  const sig = buf.subarray(0, 4).toString('hex');
  if (sig !== '89504e47' && sig.slice(0, 4) !== 'ffd8') {
    console.error(name, 'unexpected body:', buf.toString('utf8').slice(0, 160));
    continue;
  }
  writeFileSync(out, buf);
  console.log('black', name, (buf.length / 1024).toFixed(0) + 'KB', sig === '89504e47' ? 'png' : 'jpg');
}
