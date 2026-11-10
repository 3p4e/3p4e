#!/usr/bin/env python3
"""Migrate all story data JSONs from Wan2.1-FLF to LTX-2.3-22B-distilled.

Corrections applied (source: higgsfield/research/ltx23_readme.md model card,
ltx2_prompting_guide.txt, 38_LTX_VIDEO_GENERATION_SPEC.md):
  spec.model      -> LTX-2.3-22B-distilled-1.1
  spec.resolution -> 1216x704 (multiple of 32, NOT 1280x720)
  spec.frames     -> 121 (8k+1 rule; 81 fallback)
  spec.steps      -> 8 (distilled), spec.cfg -> 1.0
  spec.negative_prompt -> LTX standard set
  spec.audio_mode -> native (LTX-2.3 joint audio-video)
  per-shot kf prompts  -> 1280x720 replaced with 1216x704
  per-shot clip_s      -> aligned to 121 frames @ 24fps = 5.04s
  per-shot ltx_prompt  -> motion-first single-paragraph form derived from
                          existing kf_first + move + motion + beat_timeline
"""
import json, pathlib, re, sys

DATA_DIR = pathlib.Path('/a0/usr/projects/vast/storybook_ocr/data')

NEG = ("deformed, extra limbs, morphing, watermark, text, static frame, "
       "blurry, low quality, cropped head, cut-off face")

MOVE_VERB = {
    'static': 'holds in a static frame',
    'pan-left': 'pans left',
    'pan-right': 'pans right',
    'pan-up': 'tilts upward',
    'pan-down': 'tilts downward',
    'tilt-up': 'tilts upward',
    'tilt-down': 'tilts downward',
    'dolly-in': 'dollies in slowly',
    'dolly-out': 'dollies out slowly',
    'push-in': 'pushes in steadily',
    'pull-back': 'pulls back steadily',
    'track-left': 'tracks left',
    'track-right': 'tracks right',
    'crane-up': 'cranes up',
    'crane-down': 'cranes down',
    'orbit': 'orbits slowly around the subject',
    'handheld': 'drifts with a handheld feel',
    'shot-reverse': 'cuts to the reverse angle',
    'whip-pan': 'whip-pans across',
    'aerial': 'glides overhead',
    'follow': 'follows the subject smoothly',
    'zoom-in': 'zooms in',
    'zoom-out': 'zooms out',
}

def clean_motion(mv):
    mv = (mv or '').strip()
    if not mv:
        return ''
    mv = mv.replace('slow ', '').replace('slowly ', '')
    return mv.rstrip(';.,')

def make_ltx_prompt(shot, act):
    """Derive a clean motion-first LTX/T5 prompt (4-8 sentences, present tense)."""
    kf = (shot.get('kf_first') or '').strip()
    kf = re.sub(r',?\s*\d{3,4}x\d{3,4}\s*$', '', kf)
    kf = re.sub(r',?\s*photoreal Diablo2 cinematic grade\s*$', '', kf, flags=re.I)
    kf = re.sub(r'\.{2,}', '.', kf).strip().rstrip('.,')
    move = shot.get('move', '')
    cam = MOVE_VERB.get(move, 'holds steady')
    motion = clean_motion(shot.get('motion', ''))
    if move and move in (motion or ''):
        motion = ''
    light = (act.get('light_direction') or '').strip().rstrip('.,')
    dlg = (shot.get('dialogue_mk') or '').strip()

    sentences = []
    if kf:
        sentences.append(kf + '.')
    if motion:
        sentences.append(motion[0].upper() + motion[1:] + '.')
    sentences.append(f'Camera {cam}.')
    if light:
        sentences.append(f'{light[0].upper() + light[1:]} lighting.')
    if dlg:
        sentences.append(f'A character speaks in Macedonian: "{dlg}"')
    return ' '.join(sentences)

def migrate(path):
    d = json.load(open(path, encoding='utf-8'))
    spec = d.get('spec') or {}
    spec['model'] = 'LTX-2.3-22B-distilled-1.1'
    spec['resolution'] = '1216x704'
    spec['aspect'] = '16:9'
    spec['fps'] = 24
    spec['frames'] = 121
    spec['frames_fallback'] = 81
    spec['steps'] = 8
    spec['cfg'] = 1.0
    spec['negative_prompt'] = NEG
    spec['audio_mode'] = 'native-ltx23'
    spec['audio_note'] = ('LTX-2.3 is a joint audio-video model. Dialogue in the '
                          'ltx_prompt is rendered as native speech; narration stays '
                          'a separate TTS/score track.')
    d['spec'] = spec
    n = 0
    for act in d.get('acts', []):
        for s in act.get('shots', []):
            for kf in ('kf_first', 'kf_last'):
                if s.get(kf) and '1280x720' in s[kf]:
                    s[kf] = s[kf].replace('1280x720', '1216x704')
            s['frames'] = 121
            if s.get('clip_s'):
                s['clip_s'] = 5.04
            s['ltx_prompt'] = make_ltx_prompt(s, act)
            n += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return n

def main():
    files = sorted(DATA_DIR.glob('*_data.json'))
    ok = 0
    for f in files:
        n = migrate(f)
        ok += 1
        print(f'{f.name}: {n} shots -> LTX-2.3')
    print(f'OK {ok}/{len(files)}')

if __name__ == '__main__':
    main()
