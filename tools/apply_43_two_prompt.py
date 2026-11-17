#!/usr/bin/env python3
"""Apply 43_MODEL_AND_PROMPT_STANDARD.md (two-prompt model + model-agnostic routing)
to every story data JSON.

Per shot, produces the TWO prompt types (43 §3), paired by kf_NN_*:
  image_prompt_start / image_prompt_end  (3a IMAGE-GEN KEYFRAME — still, no motion verbs)
  video_prompt_start / video_prompt_end  (3b VIDEO-GEN CONTINUATION — motion-first, present tense)

Model-agnostic (43 §4): removes per-shot model_assign/steps; adds motion_intensity.
spec.model -> 'model-agnostic (chosen at generation)'; adds the routes ledger.
Story content/shot structure untouched. Deterministic (no LLM).
"""
import json, pathlib, re

ROOT = pathlib.Path('/a0/usr/projects/vast')
DATA_DIR = ROOT / 'storybook_ocr' / 'data'

ROUTES = [
    {"model": "Wan2.1-FLF2V-14B-720P", "input": "start+end native (run START-ONLY)", "status": "WORKING (lead for 14B quality)"},
    {"model": "Kandinsky 6.0 Lite/Pro", "input": "start-image-only", "status": "WORKING (Pro-distill untested at scale)"},
    {"model": "SkyReels-V3 R2V-14B", "input": "start-image-only", "status": "WORKING (fallback)"},
    {"model": "LTX-Video 2B v0.9.5", "input": "start-image-only", "status": "WORKING (small/fast, low ceiling)"},
    {"model": "Mochi-1", "input": "start-image-only", "status": "untested here"},
    {"model": "LTX-2.3 22B distilled", "input": "start-image-only", "status": "DEAD (nanobind native-crash, 42 note)"},
]

# motion verbs / camera words that must NOT appear in an IMAGE-GEN still prompt
MOTION_PAT = re.compile(
    r'\b(crane[- ]?(down|up)|tracking shot|track(?:ing)?|push[- ]?in|pull[- ]?back|dolly|'
    r'pan(?:s|ning)?|tilt|zoom|whip|orbit|follow(?:s|ing)?|aerial|glide|'
    r'static shot|camera|descend|ascend|rises|moves|walks|runs|turns|'
    r'settles?|shifts?|flies|slices|skims)\b', re.I)

def clean_still(kf, style_anchor='photoreal cinematic'):
    """(3a) image-gen keyframe prompt: still, no motion verbs, style named early."""
    kf = (kf or '').strip()
    kf = re.sub(r',?\s*\d{3,4}x\d{3,4}\s*$', '', kf)
    kf = re.sub(r',?\s*photoreal (Diablo2|StarCraft|World of Warcraft) cinematic(,? grade)?\s*$', '', kf, flags=re.I)
    kf = re.sub(r'\.{2,}', '.', kf).strip().rstrip('.,;')
    # strip leading motion/camera fragments
    kf = MOTION_PAT.sub('', kf)
    kf = re.sub(r'\s{2,}', ' ', kf).strip(' ,.;')
    kf = re.sub(r'^(a |an |the )?(high-angle|low-angle|eye-level|medium|wide|close-up|close|extreme)\s+', '', kf, flags=re.I)
    if not kf:
        return f'{style_anchor} still frame.'
    return f'{style_anchor}: {kf}.'

def make_continuation(shot, act, kf_side='start'):
    """(3b) video-gen continuation prompt: motion-first, present tense, continuation rules."""
    beats = shot.get('beat_timeline') or []
    beat_txts = [b[2].strip() for b in beats if len(b) > 2 and b[2].strip()]
    move = shot.get('move', '')
    motion = (shot.get('motion') or '').strip()
    dlg = (shot.get('dialogue_mk') or '').strip()
    cont = (shot.get('continuity') or '').strip()
    st = (shot.get('shot_type') or shot.get('size') or '').upper()

    S = []
    # 1. present-tense motion-first opening from the beats
    if beat_txts:
        S.append(beat_txts[0][0].upper() + beat_txts[0][1:] + '.')
        for b in beat_txts[1:3]:
            S.append(b + '.')
    elif motion:
        S.append(motion[0].upper() + motion[1:] + '.')
    else:
        S.append('The frozen moment extends forward.')
    # 2. camera folded in
    if move and move.lower() not in ' '.join(S).lower():
        S.append(f'The camera {move}.')
    # 3. motion calibrated to shot + post-motion endpoint in words
    if st in ('CLOSE-UP', 'CLOSE', 'MACRO', 'INSERT'):
        S.append('The motion stays gentle, holding identity, and settles into a still close-up.')
    elif 'BOSS' in st:
        S.append('The action plays out at full force and lands in a held, readable end pose.')
    else:
        S.append('The beat resolves into the next matching frame.')
    # 4. hold-anchor for dialogue (native audio)
    if dlg:
        S.append(f'A voice speaks in Macedonian: "{dlg}"')
    # 5. continuity lock
    if cont:
        S.append(f'Continuity held: {cont}.')
    return ' '.join(S)

def motion_intensity(shot):
    st = (shot.get('shot_type') or shot.get('size') or '').upper()
    motion = (shot.get('motion') or '').lower()
    if 'BOSS' in st or any(w in motion for w in ('thrash','strike','attack','slash','blast','lunge','slam','collide','rage','viol')):
        return 'action'
    if st in ('CLOSE-UP','CLOSE','MACRO','INSERT'):
        return 'gentle'
    return 'moderate'

def apply(path):
    d = json.load(open(path, encoding='utf-8'))
    spec = d.get('spec') or {}
    # model-agnostic spec (43 §4)
    spec['model'] = 'model-agnostic (chosen at generation)'
    spec['routes'] = ROUTES
    spec['model_note'] = ('Model chosen per story at generation (43 §4). Keyframes + continuation '
                          'prompts are generator-agnostic; only the render command differs per model.')
    # drop LTX-specific fields
    for k in ('steps', 'cfg', 'strength', 'audio_mode', 'audio_note', 'frame_model', 'clip_chain', 'model_assign'):
        spec.pop(k, None)
    d['spec'] = spec
    n = 0
    for act in d.get('acts', []):
        for s in act.get('shots', []):
            s['image_prompt_start'] = clean_still(s.get('kf_first'))
            s['image_prompt_end'] = clean_still(s.get('kf_last'))
            s['video_prompt_start'] = make_continuation(s, act, 'start')
            s['video_prompt_end'] = make_continuation(s, act, 'end')
            s['motion_intensity'] = motion_intensity(s)
            # legacy fields kept for back-compat but no longer authoritative
            for k in ('model_assign', 'steps'):
                s.pop(k, None)
            n += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return n

def main():
    files = sorted(DATA_DIR.glob('*_data.json'))
    ok = 0
    for f in files:
        n = apply(f)
        ok += 1
        print(f'{f.name}: {n} shots -> two-prompt model')
    print(f'OK {ok}/{len(files)}')

if __name__ == '__main__':
    main()
