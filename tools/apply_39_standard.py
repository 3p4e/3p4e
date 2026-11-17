#!/usr/bin/env python3
"""Align every story data JSON + rebuilt storyboard/spec to 39_CORRECTED_PROMPT_STANDARD.md.

Rules applied (from higgsfield/39_CORRECTED_PROMPT_STANDARD.md):
  ONE flowing present-tense paragraph (4-8 beats)  ·  style named early
  motion-first opening  ·  camera vocabulary folded in  ·  identity stated ONCE
  post-motion endpoint described in WORDS (no second image)  ·  native-audio SFX
  intent in motion lines  ·  continuity lock at the end  ·  motion calibrated to
  shot scale  ·  per-shot model assignment (DEV 30-step for identity-critical
  hero closeups; distilled 8-step for action/boss)  ·  strength 0.7
  ·  start-frame-only clip chain (LTX-2.3 is start-image-only).

Deterministic (no LLM), so it runs even while the subagent model backend is out
of balance. Inputs per shot: kf_first/kf_last, move/motion, beat_timeline,
asset_refs, character_designs, dialogue_mk, continuity, positive_locks.
"""
import json, pathlib, re, collections

ROOT = pathlib.Path('/a0/usr/projects/vast')
DATA_DIR = ROOT / 'storybook_ocr' / 'data'

# --- design ~> sound (native-audio SFX intent) -----------------------------
PROP_SFX = {
    'sword': 'steel rings', 'greatsword': 'steel rings', 'fire_sword': 'blazing steel rings',
    'bow': 'the bowstring hums', 'crossbow': 'crossbow strings hum',
    'staff': 'arcane energy crackles', 'wand': 'a wand sizzles',
    'hammer': 'the hammer-swing thunders', 'spear': 'the spear whistles through the air',
    'shield': 'the shield clangs', 'bagpipe': 'the bagpipes drone',
    'thunderbolt': 'thunder rolls', 'book': 'pages flutter', 'scroll': 'the scroll rustles',
}
FX_SFX = {
    'storm_aura': 'thunder rolls', 'storm_clouds': 'thunder rolls', 'lightning': 'lightning cracks',
    'lightning_aura': 'lightning cracks',
    'fire_wisps': 'flames crackle', 'fire_breath': 'flames roar', 'firelight': 'flames crackle',
    'ember_trail': 'embers hiss', 'ember_eyes': 'embers hiss',
    'frost_aura': 'ice cracks and groans', 'frost_mist': 'ice crackles', 'frost_glow': 'ice groans',
    'water_surge': 'water churns and surges',
    'wings': 'wings beat the air',
    'golden_glow': 'a low radiant hum', 'holy_aura': 'a low radiant hum',
    'divine_glow': 'a low radiant hum', 'radiant_glow': 'a low radiant hum',
    'grail_light': 'a low radiant hum', 'healing_aura': 'a low radiant hum',
    'royal_aura': 'a low radiant hum', 'wisdom_glow': 'a low radiant hum', 'gold_light': 'a low radiant hum',
    'shadow_smoke': 'shadows whisper', 'night_stalker': 'shadows whisper',
    'petals': 'petals swirl and rustle',
    'rune_ring': 'magic sizzles', 'magic_sparkles': 'magic sizzles', 'magic_glow': 'magic sizzles',
    'green_magic': 'magic sizzles', 'teal_glow': 'magic sizzles', 'silver_sparkle': 'magic sizzles',
    'gold_sparkle': 'magic sizzles',
    'venom_drip': 'venom drips and hisses', 'sea_salt_air': 'waves wash against the shore',
    'mist': 'mist trails and settles', 'mist_veil': 'mist trails and settles',
}
ENV_SFX = {
    'ocean': 'water churns and surges', 'sea': 'water churns and surges',
    'river': 'water washes past', 'water': 'water churns',
    'forest': 'leaves rustle', 'meadow': 'grass rustles', 'garden': 'leaves stir',
    'cavern': 'echoes roll', 'cave': 'echoes roll',
    'spires': 'stone groans', 'palace': 'stone groans', 'hall': 'stone groans',
    'peaks': 'wind howls', 'mountain': 'wind howls', 'storm': 'thunder rolls',
    'marsh': 'water seeps and bubbles', 'swamp': 'water seeps and bubbles',
}

SUFFIXES = ('_a1_fused', '_a2_fused', '_a3_fused', '_a4_fused', '_a5_fused', '_a6_fused',
            '_a7_fused', '_a8_fused', '_a1', '_a2', '_a3', '_a4', '_a5', '_a6', '_a7', '_a8',
            '_env', '_A1_fused', '_A2_fused', '_A3_fused', '_A4_fused', '_A5_fused',
            '_fused', '_sheet', '_b1_sheet', '_b2_sheet', '_b3_sheet', '_b4_sheet',
            '_prop', '_A1_prop', '_A2_prop', '_A3_prop', '_A4_prop', '_group', '_insert')

def strip_ref(r):
    s = r.strip()
    low = s.lower()
    for suf in SUFFIXES:
        if low.endswith(suf):
            s = s[:len(s)-len(suf)]
            break
    return s.replace('_', ' ').strip()

def red(dd):
    # derive rich physical-descriptor from a design dict
    if not dd:
        return None
    arch = dd.get('archetype') or ''
    build = dd.get('build') or ''
    costume = dd.get('costume') or []
    props = dd.get('props') or []
    fx = dd.get('fx') or []
    bits = []
    if build:
        bits.append(build)
    bits.append(arch or 'figure')
    if costume:
        bits.append('in ' + ', '.join(costume))
    if props:
        bits.append('carrying ' + ', '.join(p.replace('_', ' ') for p in props))
    if fx:
        bits.append('wreathed in ' + ', '.join(x.replace('_', ' ') for x in fx))
    if costume:
        # cosmetic: costumes already humanized in the joined list above, but ensure no snake_case
        pass
    bits = [b.replace('_', ' ') for b in bits]
    return ', '.join(bits)

def clean(kf):
    kf = (kf or '').strip()
    kf = re.sub(r',?\s*\d{3,4}x\d{3,4}\s*$', '', kf)
    kf = re.sub(r',?\s*photoreal Diablo2 cinematic grade\s*$', '', kf, flags=re.I)
    kf = re.sub(r',?\s*diablo2? cinematic grade\s*$', '', kf, flags=re.I)
    kf = re.sub(r'\.{2,}', '.', kf).strip().rstrip('.,;')
    return kf

def title_case(s):
    return ' '.join(w[:1].upper()+w[1:] if w else w for w in s.split())

def make_prompt_39(shot, act, designs):
    kf1 = clean(shot.get('kf_first'))
    kf2 = clean(shot.get('kf_last'))
    move = shot.get('move', '')
    motion = (shot.get('motion') or '').strip()
    beats = shot.get('beat_timeline') or []
    refs = shot.get('asset_refs') or []
    dlg = (shot.get('dialogue_mk') or '').strip()
    cont = (shot.get('continuity') or '').strip()
    palette = act.get('palette') or []
    tod = act.get('time_of_day', '')
    light = act.get('light_direction', '')

    # classify subject refs (characters vs env)
    chars = []   # (name, design)
    envs = []    # names
    for r in refs:
        nm = strip_ref(r)
        dl = designs.get(nm) or designs.get(nm.replace(' ', '_'))
        if dl and 'env' not in nm and dl.get('motif') is None:
            chars.append((nm, dl))
        else:
            envs.append(nm)

    # sentences
    S = []
    # 1) style + setting, named early
    style = 'photoreal cinematic'
    opening = kf1
    if opening:
        opening = opening[0].lower() + opening[1:] if opening else opening
        S.append(f'{style}: {opening}')
    else:
        S.append(style)

    # 2) identity ONCE (each present character named once with their look)
    named = {}
    for nm, dl in chars:
        look = red(dl)
        if look:
            named[nm] = look
            S.append(f'{title_case(nm)} {look}')
        else:
            named[nm] = None
            S.append(f'{nm}')

    # 3) motion-first (beat_timeline beats, present tense) + camera
    beat_txts = [b[2].strip() for b in beats if len(b) > 2 and b[2].strip()]
    if beat_txts:
        S.append('then ' + ', then '.join(beat_txts))
    elif motion:
        S.append(motion.strip())
    # camera folded in unless already in the beats
    if move and not any(move.lower() in b.lower() for b in beat_txts):
        S.append(f'the camera {move}')

    # 4) post-motion endpoint in words (from kf_last)
    if kf2 and kf2.lower() not in ' '.join(S).lower():
        S.append('settling into ' + kf2[0].lower() + kf2[1:])
    elif kf2:
        pass

    # 5) native-audio SFX intent
    sfx = []
    for nm, dl in chars:
        for p in (dl.get('props') or []):
            if PROP_SFX.get(p) and PROP_SFX[p] not in sfx:
                sfx.append(PROP_SFX[p])
        for x in (dl.get('fx') or []):
            if FX_SFX.get(x) and FX_SFX[x] not in sfx:
                sfx.append(FX_SFX[x])
    for nm in envs:
        for key, snd in ENV_SFX.items():
            if key in nm.lower() and snd not in sfx:
                sfx.append(snd)
    if sfx:
        S.append('with ' + ', '.join(sfx[:2]))

    # 6) native-audio dialogue
    if dlg:
        S.append(f'a voice speaks in Macedonian: "{dlg}"')

    # 7) continuity lock at end
    if cont:
        S.append(f'continuity held: {cont}')

    return ' '.join(S)

def model_assign(shot, designs):
    st = (shot.get('shot_type') or shot.get('size') or '').upper()
    refs = [strip_ref(r) for r in (shot.get('asset_refs') or [])]
    motion = (shot.get('motion') or '').lower()
    has_char = any((designs.get(n) and designs[n].get('motif') is None) for n in refs)
    is_boss = ('BOSS' in st) or any('boss' in n.lower() for n in refs) or \
              any(((designs.get(n) or {}).get('archetype') or '') in ('monster','beast','creature','serpent','titan','giant','draconic') for n in refs)
    violent = any(w in motion for w in ('thrash','strike','attack','slash','viol','blast','expl','lunge','slam','collide','rage'))
    if is_boss or violent:
        return 'distilled-8', 8
    if st in ('CLOSE-UP','CLOSE','MACRO','INSERT') and has_char:
        return 'DEV-30', 30
    return 'distilled-8', 8

def apply(path):
    d = json.load(open(path, encoding='utf-8'))
    designs = d.get('character_designs') or {}
    spec = d.get('spec') or {}
    spec['strength'] = 0.7
    spec['frame_model'] = 'start-frame-only'
    spec['clip_chain'] = ('100 keyframes -> 100 start-clips -> concat; '
                          'LTX-2.3 is start-image-only (no in-prompt end frame). '
                          'Continuity lives in the keyframe chain, not in a clip reaching a target.')
    d['spec'] = spec
    n = 0
    for act in d.get('acts', []):
        for s in act.get('shots', []):
            s['ltx_prompt'] = make_prompt_39(s, act, designs)
            ma, steps = model_assign(s, designs)
            s['model_assign'] = ma
            s['steps'] = steps
            n += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return n

def main():
    files = sorted(DATA_DIR.glob('*_data.json'))
    ok = 0
    for f in files:
        n = apply(f)
        ok += 1
        print(f'{f.name}: {n} shots aligned')
    print(f'OK {ok}/{len(files)}')

if __name__ == '__main__':
    main()
