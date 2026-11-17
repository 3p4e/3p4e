#!/usr/bin/env python3
"""Author GROK DESIGN-LOOK PROMPT packs for every story missing one.

Format mirrors 13_GROK_DESIGN_LOOK_PROMPTS.md / 23_GROK_DESIGN_LOOK_PROMPTS.md:
one prompt per hero (look + face card in one sheet) + a single supporting-cast
plate. Zero cost — deterministic authoring from character_designs + cast + env motifs.
Skips stories that already have a pack (13, 23).
"""
import json, glob, os, re, collections

DATA = 'storybook_ocr/data'
SPECS = 'storybook_ocr/specs'
EXISTING = {'13', '23'}

ARCH_DESC = {
    'warrior':   'A battle-hardened man in his 30s with an athletic scarred build and resolute eyes.',
    'heroine':   'A determined young woman in her 20s with an athletic build and fierce intelligent eyes.',
    'monarch':   'A commanding ruler in their 50s with a dignified weathered face and heavy royal presence.',
    'mage':      'An ageless keen-eyed spellcaster with long-fingered hands and a faintly luminous gaze.',
    'trickster': 'A lean sharp-featured figure with a sly knowing half-smile and quick restless eyes.',
    'elder':     'A wise white-bearded elder in their 70s with a deeply lined kind face, straight-backed.',
    'child':     'A child around 10 years old with bright curious eyes and an unguarded open face.',
    'beast':     'A massive powerful beast with dense fur and predatory amber eyes.',
    'monster':   'A terrifying inhuman monster with unnatural proportions and wrong-seeming anatomy.',
    'divine':    'An unearthly divine figure with radiant skin and impossibly perfect features.',
    'creature':  'A strange otherworldly creature of ambiguous nature, unsettling to look at.',
    'guardian':  'A vigilant armored guardian with a massive patient presence and watchful eyes.',
    'villain':   'A cold calculating villain with predatory stillness and cruel intelligent eyes.',
    'waterfolk': 'A graceful sea-adapted humanoid with faintly iridescent skin and large dark eyes.',
    'servant':   'An unremarkable attentive servant with a forgettable face and watchful posture.',
}
COLOR_NAMES = {'#c85a32':'ember orange','#5a3a1a':'dark bronze','#2e5a4a':'deep forest green',
    '#153026':'near-black green','#4a6a8a':'storm blue','#8a2a2a':'dried-blood red',
    '#c8a832':'antique gold','#e8e0d0':'aged ivory','#3a3a4a':'charcoal slate',
    '#6a4a8a':'royal violet','#8a6a4a':'weathered leather brown','#2a4a6a':'midnight blue'}
FX_DESC = {
    'storm_aura':'A faint crackling storm aura plays across their shoulders',
    'lightning':'Thin veins of lightning crawl over their arms',
    'holy_aura':'A soft white-gold holy light haloes their silhouette',
    'divine_glow':'A warm divine glow emanates from their skin',
    'golden_glow':'Threads of molten-gold light trace their veins',
    'rune_ring':'Slow-turning glowing runes orbit at ankle height',
    'shadow_smoke':'Wisps of living shadow coil off their silhouette',
    'ice_motes':'Drifting motes of rime-frost crystallize in the air around them',
    'fire_wisps':'Small fire-wisps dance in their wake',
    'wings':'Great wings folded against their back',
    'petals':'A slow spiral of luminous petals orbits them',
    'frost_aura':'A pale blue frost-haze breathes off their armor',
}
def slugify(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')

def hero_frequency(d):
    freq = collections.Counter()
    for a in d['acts']:
        for s in a['shots']:
            for r in (s.get('asset_refs') or []):
                base = re.split(r'_(A\d|env|fused|kf|start|end)', r)[0]
                freq[base] += 1
    return freq

def char_description(name, design, trait):
    arch = design.get('archetype', 'figure')
    build = design.get('build', '')
    costume = [c.replace('_',' ') for c in design.get('costume', [])]
    props = [pr.replace('_',' ') for pr in design.get('props', [])]
    fx = design.get('fx', [])
    pal = design.get('palette', {})
    desc = ARCH_DESC.get(arch, f'A striking {arch} figure.').rstrip('.')
    if build and build not in desc.lower():
        desc += f', {build} build'
    desc += '.'
    parts = [f'One character only: {name.upper()} — {trait}.', desc]
    if costume:
        parts.append('Wearing ' + ', '.join(costume[:-1]) + (' and ' if len(costume)>1 else '') + costume[-1] + '.')
    if props:
        held = ' and '.join(props[:2])
        art = 'an' if held[0].lower() in 'aeiou' else 'a'
        parts.append(f'Carries {art} {held}.')
    if fx:
        parts.append(FX_DESC.get(fx[0], f'A faint {fx[0].replace("_"," ")} effect') + '.')
    prim = COLOR_NAMES.get(pal.get('primary',''), pal.get('primary',''))
    sec = COLOR_NAMES.get(pal.get('secondary',''), pal.get('secondary',''))
    if prim and sec:
        parts.append(f'Palette owned by this character: {prim} and {sec} tones.')
    return ' '.join(parts)

def hero_prompt(name, design, trait, env_motif):
    return (
        'Cinematic photoreal character design sheet, Diablo 2 / World of Warcraft / StarCraft cinematic quality. '
        + char_description(name, design, trait)
        + ' Two views on one sheet, side by side: (A) full-body front view standing on neutral ground, '
          'neutral authoritative expression; (B) separate head-and-shoulders portrait, face turned 3/4 toward camera, '
          'soft cinematic key light. Background: softly blurred ' + env_motif + ', shallow depth of field. '
          '35mm anamorphic, real skin texture with pores, visible fine film grain, dramatic cinematic lighting. '
          'This is a design reference sheet — keep the face identical in both views.\n'
          'Negative: cartoon, anime, illustration, low poly, 3d render, plastic skin, text, watermark, logo, '
          'extra fingers, deformed hands, duplicate different face between views, modern clothing, firearm'
    )

def support_prompt(names, designs, traits, env_motif):
    n = len(names)
    panels = []
    for i, nm in enumerate(names):
        d = designs.get(nm, {})
        tr = traits.get(nm, nm)
        panels.append(f'panel {chr(65+i)}: ' + char_description(nm, d, tr))
    return (
        'Cinematic photoreal character design sheet, Diablo 2 / World of Warcraft / StarCraft cinematic quality. '
        f'{n} clearly separated panels on one sheet — ' + ' | '.join(panels)
        + f'. Each panel holds one full-body design view. Background per panel: softly blurred {env_motif}, '
          'shallow depth of field. 35mm anamorphic, real skin texture, visible fine film grain, '
          'dramatic cinematic lighting. Design reference sheet — one character per panel, no overlap.\n'
          'Negative: cartoon, anime, illustration, low poly, 3d render, plastic skin, text, watermark, logo, '
          'extra fingers, deformed hands, merged characters, merged panels, duplicate faces, modern clothing, firearm'
    )

def env_motif_for(d):
    for k, v in (d.get('character_designs') or {}).items():
        if 'env' in k and isinstance(v, dict) and v.get('motif'):
            return v['motif'] + ' setting'
    return 'story setting'

def main():
    authored = []
    for f in sorted(glob.glob(os.path.join(DATA, '[0-9]*_data.json'))):
        num = os.path.basename(f).split('_')[0]
        if num in EXISTING:
            continue
        d = json.load(open(f, encoding='utf-8'))
        title_mk = d.get('title') or os.path.basename(f)
        story_glob = glob.glob(os.path.join('storybook_ocr/stories', f'{num}_*.md'))
        if story_glob:
            title_mk = open(story_glob[0], encoding='utf-8').readline().lstrip('# ').strip() or title_mk
        cd = d.get('character_designs') or {}
        cast = d.get('cast') or []
        traits = {c.get('role','').lower(): c.get('trait','') for c in cast if c.get('role')}
        freq = hero_frequency(d)
        heroes = [k for k, _ in freq.most_common(4) if k in cd]
        support = [k for k in cd if k not in heroes and 'env' not in k][:3]
        env = env_motif_for(d)
        lines = [f'# {num} — {title_mk} — GROK DESIGN-LOOK PROMPTS', '']
        lines.append('> Mirrors the Fenrir/DHPF design-look workflow (`13_GROK_DESIGN_LOOK_PROMPTS.md`).')
        lines.append('> Zero cost — authoring only. Each prompt yields a **look + face card in one image** '
                     '(full-body sheet + head-and-shoulders portrait).')
        lines.append('> Once approved, each look becomes canon and is hash-locked under a stable file name.')
        lines.append('> Style anchor: **Diablo 2 cinematic · World of Warcraft cinematic · StarCraft cinematic**. '
                     'Photoreal. No cross-character contamination.')
        lines.append('')
        lines.append('## NAMING — save every image EXACTLY like this')
        lines.append('')
        lines.append('```')
        for i, h in enumerate(heroes, 1):
            lines.append(f'look_{i:02d}_{slugify(h)}.png')
        lines.append(f'look_{len(heroes)+1:02d}_support_cast.png')
        lines.append('```')
        lines.append('')
        if support:
            lines.append(f'- `look_{len(heroes)+1:02d}_support_cast.png` must contain {len(support)} clearly separated panels ('
                         + ' · '.join(s.title() for s in support) + ').')
        lines.append('- One file per prompt. Later I will cut the face portraits out of these sheets into standalone '
                     'face cards for the keyframe stage — so **keep every face large, front-lit and symmetrical**.')
        lines.append('')
        lines.append('---')
        lines.append('')
        for i, h in enumerate(heroes, 1):
            trait = traits.get(h) or f'central figure of the tale'
            lines.append(f'## PROMPT {i} of {len(heroes)+1} — {h.upper()}')
            lines.append(f'**Save as:** `look_{i:02d}_{slugify(h)}.png`')
            lines.append('')
            lines.append('```')
            lines.append(hero_prompt(h, cd.get(h, {}), trait, env))
            lines.append('```')
            lines.append('')
            lines.append('---')
            lines.append('')
        j = len(heroes) + 1
        strait = {s: (traits.get(s) or f'supporting figure of the tale') for s in support}
        lines.append(f'## PROMPT {j} of {j} — SUPPORTING CAST')
        lines.append(f'**Save as:** `look_{j:02d}_support_cast.png`')
        lines.append('')
        lines.append('```')
        lines.append(support_prompt(support, cd, strait, env) if support else
                     'Cinematic photoreal group design sheet — one clearly separated panel per supporting character.')
        lines.append('```')
        lines.append('')
        out = os.path.join(SPECS, f'{num}_GROK_DESIGN_LOOK_PROMPTS.md')
        open(out, 'w', encoding='utf-8').write('\n'.join(lines))
        authored.append(f'{num} ({len(heroes)} heroes + support)')
    print('AUTHORED', len(authored))
    for a in authored:
        print(' ', a)

if __name__ == '__main__':
    main()
