const fs = require('fs');
const path = require('path');
const dir = __dirname;

const spec = JSON.parse(fs.readFileSync(path.join(dir, 'clip_specification.json'), 'utf8'));

// Unique effect + prompt per clip id
const EFFECTS = {
  'burgeri_hamburger': ['Ember Stamp', 'the crystal tip taps the sesame crown once; a thin ring of embers brands the bun and a curl of smoke lifts away'],
  'burgeri_chizburger': ['Gold Cascade', 'molten gold cheese pours upward and folds itself over the patty in one continuous sheet'],
  'burgeri_abrakadabra_burger': ['Signature Ignition', 'the crystal taps twice; a rune circle blooms open and the stack assembles itself upright in mid-air'],
  'burgeri_hamburger_so_jajce': ['Yolk Sunburst', 'an egg cracks in mid-air, the yolk flares like a small sun and settles onto the patty'],
  'burgeri_chiken_burger': ['Feather Fry', 'a single golden feather bursts into fine crumb that rains down onto the chicken fillet'],
  'burgeri_chiken_chizburger': ['Ember & Feather', 'a feather spirals inward and melts into a ribbon of molten cheese'],
  'burgeri_drpan_burger': ['Pull-Apart Shred', 'the crystal forks outward and the meat unfurls into long strands that re-stack themselves'],
  'burgeri_smachkan_burger': ['Press of the Palm', 'an unseen weight presses the burger flat and dark sear marks flare across the crust'],

  'sendvichi_pileshka_shunka_i_kashkaval': ['Alchemist Seal', 'a wax seal stamps down and the bread seals itself along the cut'],
  'sendvichi_vrat_i_kashkaval': ['Smoke Ring Press', 'a ring of smoke descends and is pressed into the toasted crust'],
  'sendvichi_kulen_i_kashkaval': ['Spice Spark', 'small pepper sparks arc between the layers and vanish'],
  'sendvichi_svinska_shunka_i_kashkaval': ['Hearth Fold', 'the bread folds over like warm linen and settles'],
  'sendvichi_hot_dog': ['Rune Skewer', 'a rune-etched skewer drives down and lifts the hot dog as steam rises'],
  'sendvichi_korn_dog': ['Golden Crust Lace', 'a lattice of golden corn weaves itself around the sausage'],

  'tostovi_pileshka_shunka_i_kashkaval': ['Grid Brand', 'grill bars brand themselves across the toast and the cheese bubbles up'],
  'tostovi_vrat_i_kashkaval': ['Toast Levitation', 'the toast lifts, turns slowly once, and lands toasted'],
  'tostovi_kulen_i_kashkaval': ['Curing Glow', 'a warm amber glow passes through the slice from edge to edge'],
  'tostovi_svinska_shunka_i_kashkaval': ['Butter Gleam', 'butter melts into a thin sheet of gold across the surface'],

  'vrapovi_drpano_juneshko': ['Spiral Bind', 'the tortilla spirals closed on its own and ribbons of light stitch the seam'],
  'vrapovi_drpano_pileshko': ['Feather Spiral', 'feathers orbit inward and become the wrap'],

  'skara_razhnich_so_pileshki_dziger': ['Skewer Flame Lick', 'three small flames lick along the skewer and die back'],
  'skara_kebapche': ['Coal Breath', 'the coals beneath exhale once and ember dust settles on the meat'],

  'deserti_vafla_so_nutela_i_banani': ['Chocolate Lattice', 'a lattice weaves itself and chocolate floods every square'],
  'deserti_vafla_so_marmelad': ['Jewel Drops', 'marmalade drops fall and set like small gems'],
  'deserti_vafla_so_krem_od_fstak': ['Pistachio Dust Storm', 'a green dust storm settles down into the cream'],
  'deserti_abrakadabra_vafla': ['Signature Snow', 'powdered sugar snow falls upward, pauses, then drifts back down'],
  'deserti_sutlijash': ['Cinnamon Sigil', 'cinnamon writes a sigil on the surface and sinks into it'],

  'dodatoci_lepche': ['Dough Rise', 'the flat dough swells in one breath and crusts over'],
  'dodatoci_pomfrit_mal': ['Arc Cut', 'one thin arc of light splits a potato and the fries fall into place'],
  'dodatoci_pomfrit_golem': ['Arc Storm', 'three arcs strike in sequence and a cascade of fries lands'],
  'dodatoci_chips': ['Crisp Snap', 'a single snap ripples through the stack and the chips curl'],

  'kafe_neskafe': ['Dark Brew Conjure', 'dark liquid rises into the glass and a foam crown forms'],
  'kafe_frape': ['Frost Vortex', 'ice shards spiral up into a frosted vortex and settle'],

  'pijaloci_milkshejk': ['Cream Cyclone', 'a cyclone of cream spins up and a cherry lands last'],
  'pijaloci_sok': ['Citrus Bloom', 'citrus segments bloom outward and juice arcs into the glass'],
};

// LTX-2.5 continuation-form prompt builder
function ltxPrompt(c) {
  const fx = EFFECTS[c.id];
  const effectText = fx ? fx[1] : 'a soft arcane shimmer crosses the dish';
  const family = {
    forge_fire: 'warm firelight, ember motes, heat haze',
    phoenix_feather: 'golden feather motes, warm backlight',
    alchemy_press: 'cool seal-light, faint smoke, brass glints',
    spiral_binding: 'ribbons of pale light, gentle rotation',
    dragon_breath: 'live coals, drifting ember dust, low heat shimmer',
    crystal_lattice: 'crystalline facet light, cool sparkle',
    sugar_sorcery: 'soft rose-gold sugar dust, sweet haze',
    lightning_cut: 'thin white arcs, brief static flash',
    golden_crust: 'warm crust glow, flour dust',
    dark_elixir: 'deep amber light, rising steam',
    potion_mastery: 'pale cyan glow, cold condensation',
    fresh_conjuration: 'green leaf-light, morning dew',
    unknown: 'soft arcane shimmer',
  }[c.magic_theme] || 'soft arcane shimmer';

  return (
    `Continuation from the start frame. ${effectText}. ` +
    `The dish stays centred and unchanged in shape; ${family} drift slowly around it. ` +
    `Camera pushes in slowly and settles, the dish filling the frame at the end. ` +
    `Audio: a soft glass chime and a faint sizzle, no music, no speech. ` +
    `Magical realism, warm practical lighting, shallow depth of field, soft film grain.`
  );
}

function keyframePrompt(c) {
  const familyLook = {
    forge_fire: 'a black stone hearth, glowing coals behind',
    phoenix_feather: 'dark slate with warm rim light',
    alchemy_press: 'an aged brass counter, dusty light',
    spiral_binding: 'dark linen cloth, soft side light',
    dragon_breath: 'charcoal grill bars, ember glow from below',
    crystal_lattice: 'dark glass surface, cool blue rim',
    sugar_sorcery: 'deep plum velvet, rose-gold light',
    lightning_cut: 'dark steel tray, hard white edge light',
    golden_crust: 'floured wooden board, warm window light',
    dark_elixir: 'dark marble bar, single warm spot',
    potion_mastery: 'dark glass, cold cyan backlight',
    fresh_conjuration: 'dark stone with green leaf shadow',
    unknown: 'dark neutral surface, soft key light',
  }[c.magic_theme] || 'dark neutral surface';

  return (
    `Photoreal food photography of ${c.name} for a restaurant menu. ` +
    `Presented on ${familyLook}. Three-quarter view, hero framing, dish fully in frame and centred, ` +
    `no text, no hands, no logos. Rich saturated colour, glossy highlights, fine crumb and texture detail, ` +
    `35mm look, shallow depth of field, subtle film grain. ` +
    `Vertical headroom for a small overlay strip at the bottom edge.`
  );
}

let missing = [];
for (const c of spec.clips) {
  const fx = EFFECTS[c.id];
  if (!fx) { missing.push(c.id); }
  c.effect = fx ? fx[0] : 'Arcane Shimmer';
  c.keyframe_prompt = keyframePrompt(c);
  c.ltx_prompt = ltxPrompt(c);
  c.negative_prompt = '';
  c.planned_output = `assets/video/${c.day_clip}`;
}

// Fix the one unknown theme
for (const c of spec.clips) {
  if (c.category_id === 'dodatoci' && c.magic_theme === 'unknown') c.magic_theme = 'golden_crust';
}

spec.effects_total = spec.clips.length;
spec.missing_effects = missing;
fs.writeFileSync(path.join(dir, 'clip_specification.json'), JSON.stringify(spec, null, 2));

console.log('clips:', spec.clips.length);
console.log('missing effects:', missing.length, missing.join(',') || '(none)');
console.log('unique effect names:', new Set(spec.clips.map(c => c.effect)).size);
console.log('');
console.log('sample:');
console.log(JSON.stringify(spec.clips[2], null, 2));
