#!/usr/bin/env python3
"""Rewrite slideshow-template video prompts into physics-driven K6 continuations.

Doc-44 A1/A5: every motion prompt must describe SUBJECT action with concrete
verbs; 'slow motion' and the 'camera-static + beat-resolves' skeleton are the
Ken-Burns slideshow signature and are banned. A3: one phase per clip.
K6 contract: TI2VA 121 frames, guidance 1.0, native audio, start-frame only.

Rewriter derives everything from the shot's own move/motion/beat fields —
never invents content. Idempotent: prompts without template markers pass.
"""
import json, glob, os, re

DATA = 'storybook_ocr/data'
SKIP = {'13', '23'}  # fenrir + perseus handled in their own workstreams

# --- slideshow signature (doc-44 A1) ---------------------------------------
TEMPLATE_MARKERS = (
    'the beat resolves into the next matching frame',
    'the frozen moment extends forward',
    'motion stays gentle, holding identity',
    'the action plays at full force',
    'continuity held:',
)

def is_template(p):
    if not p:
        return True
    low = p.lower()
    return any(m in low for m in TEMPLATE_MARKERS)

# --- camera-move sentences --------------------------------------------------
CAM_SENT = [
    (r'push',   'the lens pushes in'),
    (r'crane-up|crane up', 'the camera cranes up'),
    (r'crane-down|crane down', 'the camera cranes down'),
    (r'crane',  'the camera cranes'),
    (r'pan-left|pan left', 'the camera pans left'),
    (r'pan-right|pan right', 'the camera pans right'),
    (r'pan',    'the camera pans'),
    (r'swish',  'the camera whips in a swish-pan'),
    (r'tilt-up|tilt up', 'the camera tilts up'),
    (r'tilt-down|tilt down', 'the camera tilts down'),
    (r'tilt',   'the camera tilts'),
    (r'track',  'the camera tracks'),
    (r'dolly',  'the camera dollies'),
    (r'pull-back|pull back', 'the lens pulls back'),
    (r'zoom',   'the lens zooms'),
]

def cam_sentence(move):
    m = (move or 'static').lower()
    if 'static' in m or 'held' in m or 'hold' in m:
        return 'The frame holds steady — only the action moves'
    for pat, sent in CAM_SENT:
        if re.search(pat, m):
            return sent[0].upper() + sent[1:]
    return 'The frame holds steady — only the action moves'

WORLD_REACT = [
    (r'push',   'foreground detail sharpens as the background melts into soft blur'),
    (r'pull|zoom', 'depth planes separate, near objects swelling past the lens'),
    (r'pan|swish', 'the landscape streams past, parallax layers sliding at different speeds'),
    (r'crane|tilt', 'the horizon re-settles as the vertical move completes'),
    (r'track|dolly', 'foreground elements slide past, the subject holding center as the world moves'),
]

def world_clause(move):
    m = (move or '').lower()
    for pat, clause in WORLD_REACT:
        if re.search(pat, m):
            return clause
    return 'dust motes drift through the light, loose fabric and hair breathing with a faint breeze'

CAM_TOKENS = {'static','held','hold','stillness','push-in','push in','push','pan-left','pan-right',
              'pan','crane-up','crane-down','crane','tilt-up','tilt-down','tilt','track','dolly',
              'swish-pan','swish','zoom','pull-back','pull back','slow','fast','resolve','reveal',
              'shot-reverse','shot reverse'}

def action_fragments(motion_text):
    """Keep the subject-action parts of the motion field, drop camera tokens."""
    parts = [p.strip() for p in re.split(r'[;—]', motion_text or '') if p.strip()]
    out = []
    for p in parts:
        toks = [t for t in re.split(r'[\s,]+', p.lower()) if t]
        if toks and all(t in CAM_TOKENS for t in toks):
            continue  # pure camera fragment
        out.append(p)
    return out

def rewrite(s):
    move = s.get('move', 'static')
    frags = action_fragments(s.get('motion', ''))
    cam = cam_sentence(move)
    world = world_clause(move)
    if frags:
        label = '; '.join(frags)
        label = label[0].upper() + label[1:]
        action = (f'{label} — the motion carries real weight, follow-through readable '
                  f'in fabric, debris and light')
    else:
        action = ('The scene breathes with ambient life — weight settles, small movements '
                  'ripple through frame, nothing sits frozen')
    return f'{cam}; {world}. {action}. The move completes in a single phase and holds.'

def main():
    stats = {'rewritten': 0, 'clean': 0, 'files': 0}
    for f in sorted(glob.glob(os.path.join(DATA, '[0-9]*_data.json'))):
        num = f.split('/')[-1].split('_')[0]
        if num in SKIP:
            continue
        d = json.load(open(f, encoding='utf-8'))
        changed = False
        for a in d['acts']:
            for s in a['shots']:
                for fld in ('video_prompt_start', 'video_prompt_end'):
                    if is_template(s.get(fld)):
                        s[fld] = rewrite(s)
                        stats['rewritten'] += 1
                        changed = True
                    else:
                        stats['clean'] += 1
        if changed:
            json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            stats['files'] += 1
    print(json.dumps(stats))

if __name__ == '__main__':
    main()
