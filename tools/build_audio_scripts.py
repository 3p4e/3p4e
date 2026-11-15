#!/usr/bin/env python3
"""Author NN_AUDIO_SCRIPT_MK_EN.md for every in-scope story.

Deterministic, zero-cost. Per shot:
  **SNN** CHAR: „MK line" / "EN line"   (MK from narration_mk/nar_mk; dialogue_mk
                                          lines keep their character cue)
  SFX: <keyword-derived tag>            AMB: <act env motif>
EN lines: left empty for director/LLM fill (MK is the authored source; EN is a
translation pass - deterministic EN would be machine-translation quality and we
do not fake it). A missing MK line is derived from the shot's beat text.
Skips 13 (Fenrir) and 23 (Perseus) - scripts already exist.
"""
import json, glob, os, re

DATA = 'storybook_ocr/data'
SPECS = 'storybook_ocr/specs'
SKIP = {'13', '23'}

SFX_RULES = [
    (r'\b(strike|slash|clash|lunge|parry|impact|smash|crush|hit)\b', 'combat-impact'),
    (r'\b(run|chase|gallop|ride|riding|sprint|flee|pursu)\b', 'movement-rush'),
    (r'\b(sea|wave|storm|rain|ocean|river|water)\b', 'water-bed'),
    (r'\b(flame|torch|fire|ember|burn)\b', 'fire-crackle'),
    (r'\b(wind|gale|gust|breeze)\b', 'wind-bed'),
    (r'\b(glow|rune|aura|spell|transform|magic|shimmer)\b', 'magic-shimmer'),
    (r'\b(roar|hiss|growl|snarl|scream)\b', 'creature-vocal'),
    (r'\b(open|creak|gate|door)\b', 'stone-groan'),
    (r'\b(thunder|lightning|grm)\b', 'thunder'),
    (r'\b(whisper|breath|sigh)\b', 'intimate-breath'),
]

def sfx_for(s):
    blob = ' '.join(str(s.get(k) or '') for k in
                    ('action','motion','kf_first','video_prompt_start')).lower()
    tags = []
    for pat, tag in SFX_RULES:
        if re.search(pat, blob) and tag not in tags:
            tags.append(tag)
    return '+'.join(tags[:2]) if tags else 'room-tone'

AMB_RULES = [
    (r'(sea|ocean|wave|shore|beach|coast|harbor|harbour)', 'ocean-shore'),
    (r'(river|stream|lake|pond|waterfall|waters)', 'river-water'),
    (r'(forest|wood|grove|glade|trees?|jungle)', 'forest'),
    (r'(mountain|peak|cliff|crag|ridge|highland|alps?)', 'mountain-wind'),
    (r'(cave|cavern|grotto|underground|tunnel|crypt)', 'cavern'),
    (r'(hall|throne|castle|palace|keep|tower|fortress|chamber)', 'stone-hall'),
    (r'(village|town|city|market|street|house|farm|mill)', 'village-day'),
    (r'(gate|door|portal|threshold|wall)', 'gate-stone'),
    (r'(sky|cloud|heaven|olympus|asgard|wind)', 'high-wind'),
    (r'(desert|dune|sand|waste)', 'desert-dry'),
    (r'(garden|meadow|field|orchard|bloom)', 'garden-birds'),
    (r'(night|dark|shadow|moon|dusk|midnight)', 'night-cricket'),
    (r'(snow|ice|frost|winter|frozen)', 'ice-hollow'),
    (r'(fire|flame|ember|forge|torch)', 'fire-crackle-bed'),
]

def amb_for_shot(s, fallback):
    blob = ' '.join(str(s.get(k) or '') for k in
                    ('action','motion','kf_first','kf_last','video_prompt_start')).lower()
    for pat, tag in AMB_RULES:
        if re.search(pat, blob):
            return tag
    return fallback

def amb_for(d, act_idx):
    cd = d.get('character_designs') or {}
    for k, v in cd.items():
        if 'env' in k and isinstance(v, dict) and v.get('motif'):
            return v['motif']
    return 'hall'

def mk_line(s):
    return (s.get('narration_mk') or s.get('nar_mk') or '').strip()

def dlg_line(s):
    return (s.get('dialogue_mk') or '').strip()

def beat_fallback(s):
    bt = s.get('beat_timeline') or []
    for b in bt:
        if isinstance(b, list) and len(b) > 2 and b[2]:
            return str(b[2]).strip()
    return ''

def main():
    authored = 0
    for f in sorted(glob.glob(os.path.join(DATA, '[0-9]*_data.json'))):
        num = os.path.basename(f).split('_')[0]
        if num in SKIP:
            continue
        d = json.load(open(f, encoding='utf-8'))
        title = d.get('title') or os.path.basename(f)
        lines = [f'# {num} — {title} — AUDIO SCRIPT (MK + EN)', '',
                 '> Grammar: `**SNN** CHAR: „MK…" / "EN…"` (EN filled at translation pass).',
                 '> SFX/AMB tags are deterministic, keyword-derived from the shot text.',
                 '> TTS: ElevenLabs eleven_multilingual_v2. Save: audio/narration/sNN_{MK,EN}.wav.',
                 '> Budget: 5.05 s/clip → dialogue ≤ 14 EN words, narration ≤ ~16 EN words.', '']
        for ai, a in enumerate(d['acts']):
            act_amb = amb_for(d, ai)
            lines.append(f'## ACT {ai+1} — ambience: {act_amb}')
            lines.append('')
            for s in a['shots']:
                sid = s['id']
                dlg = dlg_line(s)
                mk = mk_line(s) or beat_fallback(s)
                if dlg:
                    cue = dlg.split(':')[0].strip() if ':' in dlg[:6] else 'CHAR'
                    text = dlg.split(':', 1)[1].strip() if ':' in dlg[:6] else dlg
                    lines.append(f'**{sid}** {cue}: „{text}” / ""')
                elif mk:
                    lines.append(f'**{sid}** N: „{mk}” / ""')
                else:
                    lines.append(f'**{sid}** N: (no line — visual beat) / ""')
                lines.append(f'  SFX: {sfx_for(s)} · AMB: {amb_for_shot(s, act_amb)}')
                lines.append('')
        out = os.path.join(SPECS, f'{num}_AUDIO_SCRIPT_MK_EN.md')
        open(out, 'w', encoding='utf-8').write('\n'.join(lines))
        authored += 1
    print('audio scripts authored:', authored)

if __name__ == '__main__':
    main()
