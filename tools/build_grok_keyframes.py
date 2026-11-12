#!/usr/bin/env python3
"""Author Grok-format START-keyframe image prompts for every story (story-generic
characters), and align each shot's video continuation prompt to its keyframe.

Per story: for every shot, produce kf_NN_start.png image prompt in the Fenrir-pack
format (Cinematic film still -> subject -> environment -> camera -> style anchor),
plus a relaxed video continuation prompt keyed to that keyframe. Writes the pack to
storybook_ocr/specs/NN_<slug>_GROK_START_KEYFRAME_PROMPTS.md and rewrites the data
JSON's image_prompt_start/video_prompt_start fields to match.

Characters are STORY-GENERIC (face_lock AI-default): identity comes from the story
cast trait + character_designs, named ONCE per prompt, never restated (39/43).
Deterministic; no LLM; zero GPU.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path('/a0/usr/projects/vast')
DATA = ROOT / 'storybook_ocr' / 'data'
SPECS = ROOT / 'storybook_ocr' / 'specs'
SPECS.mkdir(parents=True, exist_ok=True)

STYLE = "Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, 35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting."
NEG = "duplicate face, extra limbs, extra fingers, deformed hands, text, watermark, logo, cartoon, anime, illustration, cel-shaded, 3d render, plastic skin, gore, blood"

# map archetype -> short label for the subject line
ARCH_LABEL = {
    'divine':'god', 'warrior':'warrior', 'heroine':'woman', 'monarch':'king',
    'mage':'mage', 'trickster':'trickster', 'elder':'old man', 'child':'child',
    'beast':'beast', 'monster':'monster', 'villain':'giant', 'guardian':'guardian',
    'waterfolk':'water-spirit', 'creature':'creature', 'servant':'servant',
}
PROP_WORD = {'sword':'sword','greatsword':'greatsword','spear':'spear','staff':'staff',
    'wand':'wand','bow':'bow','crossbow':'crossbow','hammer':'hammer','shield':'shield','lyre':'lyre'}
FX_WORD = {'holy_aura':'a pale holy aura','golden_glow':'a soft golden glow','divine_glow':'a radiant divine glow',
    'storm_aura':'a storm aura crackling around them','rune_ring':'a ring of glowing runes','wings':'broad wings',
    'shadow_smoke':'wisps of shadow smoke','ice_motes':'drifting ice motes','fire_wisps':'drifting fire wisps',
    'lightning':'flickering lightning','petals':'drifting petals','frost_aura':'a rim of frost aura'}

def load(fn):
    return json.load(open(fn, encoding='utf-8'))

def slug_num(fn):
    return fn.name.split('_')[0]

def char_by_ref(d, ref):
    """Map an asset_ref like 'thor_A1_fused' to (display_name, design)."""
    key = ref
    for suffix in ('_fused','_sheet','_prop'):
        key = key.replace(suffix,'')
    # strip scene suffix _A1, _A2, _B1 ...
    key = re.sub(r'_[A-Z]\d+$', '', key)
    cd = d.get('character_designs', {})
    design = cd.get(key)
    if design is None:
        design = cd.get(ref)
    return key, design

ABILITY_VERB = {'storm_aura':'Stormmantle','lightning':'Skyfire Judgment','holy_aura':'Consecration',
    'divine_glow':'Radiant Decree','golden_glow':'Aurum Halo','rune_ring':'Sigil Circle',
    'shadow_smoke':'Umbral Step','ice_motes':'Rimebind','fire_wisps':'Cinderwake',
    'wings':'Ascendant Wings','petals':'Blossom Veil','frost_aura':'Hoarfrost Crown'}
ABILITY_FALLBACK = ['Cleave','Bulwark','War Cry','Overload','Last Stand']
TAGLINE_BANK = {
    'divine':'The Sky Itself Answers','trickster':'Every Promise Has a Second Edge',
    'warrior':'The Line Does Not Break','heroine':'The Quiet That Outlasts Storms',
    'monarch':'The Crown Remembers','mage':'Knowledge Is the Only Fire',
    'elder':'The Mountain Does Not Hurry','child':'Small Hands, Long Shadow',
    'beast':'The Wild Keeps Its Word','monster':'What the Dark Bred First',
    'villain':'What the Cold Keeps','guardian':'Nothing Passes Unanswered',
    'waterfolk':'The Tide Owes No Explanation','creature':'Older Than the Name',
    'servant':'Unseen, Never Unfelt'}
WEAPON_TITLE = {
    'sword':('Oathkeeper','Edge of the Vow'),'greatsword':('Doombringer','Scale-Tipper of Wars'),
    'spear':('Godsreach','First Light of Battle'),'staff':('Worldroot','the Speaking Staff'),
    'wand':('Sparkling Verdict',"the Judge's Thumb"),'bow':('Skyneedle','the Far Whisper'),
    'crossbow':('Twin Argument','the Last Word'),'hammer':('Thunderhead','Voice of the Sky'),
    'shield':('Aegisward','the Unbroken No'),'lyre':('Heartstring','the War-Singer')}

def p_art(w):
    return 'an' if w[0].lower() in 'aeiou' else 'a'

def template_fields(name, design, trait=''):
    """Derive the 44-template P1/P2 fields from a character_designs entry."""
    arch = design.get('archetype','figure')
    loadout = f"{arch.title()} Loadout"
    tagline = TAGLINE_BANK.get(arch, arch.title())
    costume = design.get('costume', [])
    pal = design.get('palette', {})
    mats = []
    if costume:
        mats.append(f"{costume[0].replace('_',' ')} weave")
    if pal.get('primary'):
        mats.append(f"dyed {pal['primary']}")
    if 'armor' in costume:
        mats.append('tempered plate')
    mats.append('weathered leather trim')
    materials = (mats + ['story-linen','oiled hide'])[:4]
    abilities = [ABILITY_VERB.get(f, f.replace('_',' ').title()) for f in design.get('fx', [])]
    abilities = (abilities + ABILITY_FALLBACK)[:5]
    armor_map = {}
    for c in costume:
        if c in ('cloak','armor'):
            armor_map.setdefault('chest', c)
    armor = [
        armor_map.get('chest', costume[0] if costume else 'tunic') + ' (chest)',
        costume[1] if len(costume)>1 else 'pauldron' + ' (pauldron)',
        'bracers' + ' (gauntlet)',
        costume[-1] if costume else 'cape' + ' (back/cape)',
        'greaves' + ' (boot)',
    ]
    props = design.get('props', [])
    wname = WEAPON_TITLE.get(props[0], ('Relic',''))[0] if props else None
    wtitle = WEAPON_TITLE.get(props[0], ('','the Nameless'))[1] if props else None
    wquote = f"It does not serve the {arch}; it chooses them." if props else None
    return {'loadout':loadout,'tagline':tagline,'materials':materials,
            'abilities':abilities,'armor':armor,'weapon_name':wname,
            'weapon_title':wtitle,'weapon_quote':wquote}

def template_block(d, ref, cast_map, trait=''):
    """P1+P2 template info lines for one character ref."""
    key, design = char_by_ref(d, ref)
    if design is None or 'motif' in design:
        return []
    name = cast_map.get(key, key.replace('_',' ').title())
    tf = template_fields(name, design, trait)
    lines = []
    lines.append(f"Loadout: {name} — {tf['loadout']} \"{tf['tagline']}\"")
    lines.append(f"Materials: {'; '.join(tf['materials'])}.")
    if tf['abilities']:
        lines.append(f"Abilities: {', '.join(tf['abilities'])}.")
    if tf['weapon_name']:
        lines.append(f"Weapon: {tf['weapon_name']} «{tf['weapon_title']}» — {tf['weapon_quote']}")
    return lines

def p_art(w):
    w = w.lstrip()
    art = 'an' if w[:1].lower() in 'aeiou' else 'a'
    return f'{art} {w}'

def subject_sentence(d, ref, cast_map):
    """One-sentence identity naming: role + archetype descriptor + key costume/prop/fx.
    Names identity ONCE; no face descriptor (story-generic)."""
    key, design = char_by_ref(d, ref)
    name = cast_map.get(key, key.replace('_',' ').title())
    if design is None:
        return f"{name}"
    arch = ARCH_LABEL.get(design.get('archetype',''), '')
    bits = []
    art = 'an' if design.get('build','').startswith(('a','e','i','o','u')) else 'a'
    bits.append(f"{name}, {art} {design.get('build','')} {arch or design.get('archetype','figure')}".replace('  ',' '))
    cost = design.get('costume', [])
    if cost:
        bits.append('wearing ' + ' and '.join(p_art(c) for c in cost))
    props = [PROP_WORD.get(p,p) for p in design.get('props', [])]
    if props:
        bits.append('holding a ' + ', a '.join(props))
    fx = [FX_WORD.get(f, f.replace('_',' ')) for f in design.get('fx', [])]
    if fx:
        bits.append('with ' + ', '.join(fx))
    return ', '.join(bits)

def env_sentence(d, refs):
    """Environment sentence from the first env-motif design in the shot's refs."""
    cd = d.get('character_designs', {})
    for ref in refs:
        r = ref
        for suffix in ('_prop',): r = r.replace(suffix,'')
        r = re.sub(r'_[A-Z]\d+$','', r)
        # env designs carry 'motif'
        v = cd.get(r) or cd.get(ref)
        if isinstance(v, dict) and 'motif' in v:
            motif = v['motif']
            return f"Environment: a {motif} setting in the story's palette, {ACT_LIGHT.get(motif,'atmospheric light')}."
    # fallback: derive from kf_first environment clause
    return "Environment: the story setting, matched to the shot's palette and light direction."

ACT_LIGHT = {'ocean':'water reflecting the key light','hall':'arched hall light','forest':'leaf-filtered light',
    'gate':'cold gate light','cavern':'dim cavern light','spires':'spire-lit cold light','peaks':'mountain light'}

def camera_line(s):
    return (f"Camera: {s.get('size','medium')} shot at {s.get('angle','eye-level')}, composed as the frozen "
            f"opening frame of a {s.get('move','static')} move — subject sharp, background softly blurred, shallow depth of field.")

def pose_line(s):
    """Frozen action from kf_first (the opening pose), lightly de-motioned."""
    kf = (s.get('kf_first') or '').strip().rstrip('.,')
    # strip resolution / style brands
    kf = re.sub(r',?\s*\d{3,4}x\d{3,4}\s*$','',kf)
    kf = re.sub(r',?\s*photoreal\s+(?:Diablo2|StarCraft|World of Warcraft|WoW)?\s*cinematic.*$','',kf, flags=re.I)
    kf = re.sub(r',?\s*(?:photoreal|cinematic)(?:\s+(?:cinematic|grade))?\s*$','',kf, flags=re.I)
    if not kf:
        kf = 'the opening pose of the shot'
    return f"Action: {kf}."

def grok_prompt(d, act, s, cast_map):
    refs = s.get('asset_refs', [])
    char_refs = [r for r in refs if not (r.endswith('_prop') or '_env' in r)]
    subjects = [subject_sentence(d, r, cast_map) for r in char_refs]
    subj = ' and '.join(subjects) if subjects else 'the scene'
    # first line: subject summary
    head = f"Cinematic film still, photoreal: {s.get('size','medium').lower()} of {subj}, {s.get('angle','eye-level')}."
    pose = pose_line(s)
    env = env_sentence(d, refs)
    cam = camera_line(s)
    parts = [head, pose]
    for r in char_refs:
        parts.extend(template_block(d, r, cast_map))
    parts.extend([env, cam, STYLE])
    block = {
        'file': kf_filename(s),
        'attach': char_refs,
        'prompt': '\n'.join(parts),
        'negative': NEG,
    }
    return block

def kf_filename(s):
    # S01 -> kf_01_start.png  (2-digit zero pad)
    m = re.match(r'^S(\d+)$', s['id'])
    n = int(m.group(1)) if m else 0
    return f"kf_{n:02d}_start.png"

def align_video_prompt(s):
    """Relaxed continuation keyed to this keyframe: present-tense, motion-first,
    continuation-not-scene-change, no endpoint frame (39/43)."""
    beats = [b[2].strip() for b in (s.get('beat_timeline') or []) if len(b)>2 and b[2].strip()]
    motion = (s.get('motion') or '').strip()
    move = s.get('move','')
    dlg = (s.get('dialogue_mk') or '').strip()
    cont = (s.get('continuity') or '').strip()
    st = (s.get('shot_type') or s.get('size') or '').upper()
    S = []
    if beats:
        first = beats[0][0].upper()+beats[0][1:]
        S.append(first+'.')
        for b in beats[1:3]: S.append(b+'.')
    elif motion:
        S.append(motion[0].upper()+motion[1:]+'.')
    else:
        S.append('The frozen moment extends forward.')
    if move and move not in ' '.join(S):
        S.append(f'The camera {move}.')
    if st in ('CLOSE-UP','CLOSE','MACRO','INSERT'):
        S.append('Motion stays gentle, holding identity, settling into a still close-up.')
    elif 'BOSS' in st:
        S.append('The action plays at full force and lands in a held, readable pose.')
    else:
        S.append('The beat resolves into the next matching frame.')
    if dlg:
        S.append(f'A voice speaks in Macedonian: "{dlg}"')
    if cont:
        S.append(f'Continuity held: {cont}.')
    return ' '.join(S)

def build_cast_map(d):
    """role -> short English name (after the '/'), keyed by design key as available."""
    m = {}
    # build name from cast role (English side after '/')
    for c in d.get('cast', []):
        role = c.get('role','')
        parts = [p.strip() for p in role.split('/')]
        en = parts[-1] if len(parts) > 1 else role
        # store by lowercased first token and full
        m[en.lower()] = en
    # map design keys to cast names by substring match
    out = {}
    for c in d.get('cast', []):
        role = c.get('role','')
        en = role.split('/')[-1].strip() if '/' in role else role
        out[en.lower().replace(' ','_')] = en
    # also key by raw design key -> fall back later in subject_sentence
    return out

def process(fn):
    d = load(fn)
    d['spec']['keyframe_type'] = 'Grok START keyframes (story-generic characters)'
    cast_map = build_cast_map(d)
    lines = []
    n = int(fn.name.split('_')[0])
    title = d.get('title_mk','') or fn.stem
    lines.append(f"# {n:02d} — {title} — START KEYFRAME PROMPTS FOR GROK")
    lines.append("")
    lines.append("> Generator: Grok (image). Characters STORY-GENERIC (AI-default, no enrolled faces).")
    lines.append("> Strategy: N-clip START-FRAME-ONLY (43 sec.2). Every keyframe is a START frame; each drives one clip.")
    lines.append("> Authoring only — this pack grants no render and no spend.")
    lines.append("")
    shots_total = sum(len(a['shots']) for a in d['acts'])
    lines.append(f"> {shots_total} start keyframes, one per shot.")
    lines.append("")
    # naming table
    lines.append("## NAMING")
    lines.append("")
    lines.append("| Keyframe file | Shot | Act |")
    lines.append("|---|---|---|")
    for a in d['acts']:
        for s in a['shots']:
            lines.append(f"| `{kf_filename(s)}` | {s['id']} | {a['num']} — {a['title']} |")
    lines.append("")
    lines.append("- `kf_NN` = shot number, two digits. `_start` = the frozen opening frame.")
    lines.append(f"- {shots_total} files total. Nothing else in the filename.")
    lines.append("")
    # shot blocks
    for a in d['acts']:
        for s in a['shots']:
            b = grok_prompt(d, a, s, cast_map)
            lines.append("")
            lines.append(f"## SHOT {s['id']} ({s['id']}) — {s.get('size','').upper()} · {s.get('angle','')} · {s.get('move','')}")
            lines.append("")
            lines.append(f"### {b['file']}")
            att = ', '.join(b['attach']) if b['attach'] else 'none — environment/establishing frame'
            lines.append(f"**Attach:** {att}")
            lines.append("**Prompt:**")
            lines.append(b['prompt'])
            lines.append(f"**Negative:** {b['negative']}")
            # write back aligned prompts to the data JSON
            s['image_prompt_start'] = b['prompt']
            s['video_prompt_start'] = align_video_prompt(s)
    text = '\n'.join(lines) + '\n'
    slug = fn.stem
    out = SPECS / f"{n:02d}_{slug}_GROK_START_KEYFRAME_PROMPTS.md"
    out.write_text(text, encoding='utf-8')
    json.dump(d, open(fn,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    return shots_total, out.name

def main():
    files = sorted(DATA.glob('*_data.json'))
    total = 0
    for fn in files:
        n, name = process(fn)
        total += n
        print(f"{name}: {n} keyframes")
    print(f"DONE {len(files)} stories / {total} keyframes authored")

if __name__ == '__main__':
    main()
