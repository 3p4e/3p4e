// Builds assets/art.js: window.GE_ART = { hero, room, cut{...}, strains{...} }
// from the raw generations in assets/raw/ (see README for the pipeline).
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

// Each growth stage is rendered on flat black, then added over a darkened
// grow-room plate with an additive blend (see below). Compositing here, once,
// rather than blending in CSS at runtime keeps the dark fabric pot fully
// opaque, and using pure black instead of an alpha cut-out avoids the white
// halo that keying left around the leaves.
// Every stage came from the same reference frame, so the pot lines up across
// stages without any trimming or rescaling.
async function toStage(file, roomB64, w, q) {
  if (!existsSync(file)) { console.warn('missing', file); return null; }
  const b64 = readFileSync(file).toString('base64');
  return await pg.evaluate(async ({ b64, roomB64, w, q }) => {
    const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
    // The scene in the card is landscape, so the tall source frame is drawn
    // into a 3:2 plate: centred horizontally and anchored to the bottom, with
    // the top of the frame cropped (it is empty black above the plant anyway).
    const W = w, H = Math.round(w / 1.5);
    const srcScale = H / img.height * 1.42;      // plant fills most of the height
    const dw = img.width * srcScale, dh = img.height * srcScale;

    // Plant plate at target size, on black so the matte stays valid.
    const plate = document.createElement('canvas'); plate.width = W; plate.height = H;
    const px = plate.getContext('2d');
    px.fillStyle = '#000'; px.fillRect(0, 0, W, H);
    px.drawImage(img, (W - dw) / 2, H - dh, dw, dh);

    // The room is laid in behind and the plant plate is added on top with a
    // `lighter` (additive) blend. Because the plate's background is a true
    // black it adds nothing there and the room shows through, while the plant
    // and its dark fabric pot keep every pixel they have. No threshold, so
    // there is no matte to punch holes in the pot and no keyed halo.
    const room = new Image(); room.src = roomB64; await room.decode();
    const out = document.createElement('canvas'); out.width = W; out.height = H;
    const ox = out.getContext('2d');
    ox.filter = 'brightness(.30) saturate(.5)';
    const rs = Math.max(W / room.width, H / room.height);
    ox.drawImage(room, (W - room.width * rs) / 2, (H - room.height * rs) / 2,
      room.width * rs, room.height * rs);
    ox.filter = 'none';

    // Darken the room directly behind the plant so it does not glow through
    // the leaves, then add the plant.
    const shade = ox.createRadialGradient(W / 2, H * 0.62, 0, W / 2, H * 0.62, W * 0.42);
    shade.addColorStop(0, 'rgba(0,0,0,.85)');
    shade.addColorStop(1, 'rgba(0,0,0,0)');
    ox.fillStyle = shade; ox.fillRect(0, 0, W, H);

    ox.globalCompositeOperation = 'lighter';
    ox.drawImage(plate, 0, 0);
    ox.globalCompositeOperation = 'source-over';
    return out.toDataURL('image/jpeg', q);
  }, { b64, roomB64, w, q });
}

const slugs = ['ohrid_crystal','pelister_frost','vardar_gold','skopje_haze','bitola_kush',
  'shar_diesel','galicica_dream','prespa_punch','macedonian_royal','imperial_reserve'];

const art = { hero: null, room: null, dryRoom: null, cureRoom: null, trimRoom: null,
              cut: {}, looks: {}, strains: {} };
art.hero = await toJpeg(RAW + '/hero.png', 760, 0.82);
art.room = await toJpeg(RAW + '/room.jpg', 420, 0.78);
art.dryRoom = await toJpeg(RAW + '/dry_room.jpg', 720, 0.78);
art.cureRoom = await toJpeg(RAW + '/cure_room.jpg', 720, 0.78);
art.trimRoom = await toJpeg(RAW + '/trim_room.jpg', 720, 0.78);
const STAGES = [['seedling','stage_seedling'],['veg','stage_veg'],['flower','stage_flower'],['harvest','stage_harvest']];
for (const [k, f] of STAGES) {
  // Plant matted onto the room at build time (see toStage).
  art.cut[k] = await toStage(RAW + '/' + f + '_black.png', art.room, 460, 0.84);
}
// Per-strain flowering looks: the same plant re-coloured, composited the same
// way so a strain's mature plant reads as its own while the grow stays aligned.
for (const look of ['frost','purple','orange','gold','pink']) {
  art.looks[look] = await toStage(RAW + '/look_' + look + '.png', art.room, 460, 0.84);
}
for (let i = 0; i < 10; i++) art.strains[slugs[i]] = await toJpeg(RAW + '/strain_' + (i + 1) + '.png', 240, 0.82);

writeFileSync('/home/user/3p4e/green-empire/assets/art.js', 'window.GE_ART=' + JSON.stringify(art) + ';\n');
console.log('art.js written ~', (JSON.stringify(art).length / 1048576).toFixed(2), 'MB',
  '| hero', !!art.hero, '| room', !!art.room,
  '| cut', Object.entries(art.cut).map(([k,v])=>k+':'+(v?'ok':'MISS')).join(','),
  '| looks', Object.values(art.looks).filter(Boolean).length+'/5',
  '| rooms', [art.dryRoom,art.cureRoom,art.trimRoom].filter(Boolean).length+'/3',
  '| strains', Object.values(art.strains).filter(Boolean).length + '/10');
await b.close();
