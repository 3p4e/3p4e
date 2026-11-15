#!/usr/bin/env python3
"""Apply director-approved fixes from the corpus review (doc 46).

FLAT-PACING stories (07,08,15,17,30,32,34,36): filmic duration variation.
  Pattern per shot position [3.5, 2.5, 4.0, 3.0, 2.0] scaled so each ACT's
  total duration is preserved; beat_timeline re-chained to new durations.
  Only numbers change - no beat text touched.

STATIC-HEAVY stories (10,21,22,24,25,26,29): convert static moves to
  MOTIVATED moves chosen from the shot's own beat keywords (push-in on
  gaze/recognition, pan/track on traverse/chase, crane-up on scale/reveal),
  converting just enough statics to bring static%% <= 45. video_prompts of
  changed shots regenerated via the physics rewriter; motion field's
  'static' token replaced so future rewrites stay consistent.

Skips 13 (Fenrir) and 23 (Perseus) - own workstreams.
"""
import json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_k6_physics import rewrite as physics_rewrite, is_template

DATA = 'storybook_ocr/data'
FLAT = {'07','08','15','17','30','32','34','36'}
STATICY = {'10','21','22','24','25','26','29'}
SKIP = {'13','23'}

PATTERN = [3.5, 2.5, 4.0, 3.0, 2.0]
TARGET_STATIC_PCT = 45

MOVE_RULES = [
    (r'\b(eyes|gaze|stare|glare|realiz|recogni|dawns|whisper|secret|close[- ]?up|face)\b', 'push-in'),
    (r'\b(chase|pursu|gallop|ride|rides|riding|run|running|cross|traverse|flee|sprint)\b', 'pan-left'),
    (r'\b(walk|procession|march|journey|follow|alongside|approach|approaches)\b', 'track'),
    (r'\b(scale|vast|reveal|establish|vista|tower|kingdom|city|overhead|panorama)\b', 'crane-up'),
    (r'\b(rise|ascend|lift|soar|climb)\b', 'tilt-up'),
]

def motivated_move(s):
    blob = ' '.join(str(s.get(k) or '') for k in
                    ('action','motion','beat_timeline','kf_first','video_prompt_start')).lower()
    for pat, mv in MOVE_RULES:
        if re.search(pat, blob):
            return mv
    return 'push-in'

def rechain(s):
    bt = s.get('beat_timeline')
    if not isinstance(bt, list) or not bt:
        return
    dur = float(s.get('dur') or 3.0)
    out, t = [], 0.0
    for i, b in enumerate(bt):
        if not isinstance(b, list) or len(b) < 3:
            return
        t1 = float(b[1]) if i < len(bt)-1 else dur
        if t1 <= t: t1 = t + dur/len(bt)
        out.append([round(t,2), round(t1,2), b[2]])
        t = t1
    out[-1][1] = round(dur,2)
    s['beat_timeline'] = out

def fix_pacing(d):
    n = 0
    for a in d['acts']:
        shots = a.get('shots') or []
        if not shots:
            continue
        old_total = sum(float(s.get('dur') or 3.0) for s in shots)
        raw = [PATTERN[i % len(PATTERN)] for i in range(len(shots))]
        scale = old_total / sum(raw)
        new_durs = [round(v*scale, 1) for v in raw]
        drift = round(old_total - sum(new_durs), 1)
        new_durs[-1] = round(new_durs[-1] + drift, 1)
        for s, nd in zip(shots, new_durs):
            if float(s.get('dur') or 0) != nd:
                s['dur'] = nd
                s['clip_s'] = nd
                n += 1
            rechain(s)
    return n

def fix_statics(d):
    shots = [s for a in d['acts'] for s in (a.get('shots') or [])]
    total = len(shots)
    statics = [s for s in shots if (s.get('move') or 'static').lower() in ('static','held','hold')]
    need = len(statics) - int(total * TARGET_STATIC_PCT / 100)
    if need <= 0:
        return 0
    converted = 0
    for s in statics:
        if converted >= need:
            break
        new_move = motivated_move(s)
        s['move'] = new_move
        m = s.get('motion') or ''
        s['motion'] = re.sub(r'^(static|held|hold)\s*;\s*', f'{new_move}; ', m, flags=re.I) if m else new_move
        s['video_prompt_start'] = physics_rewrite(s)
        s['video_prompt_end'] = physics_rewrite(s)
        converted += 1
    return converted

def main():
    out = {'pacing': {}, 'statics': {}}
    for f in sorted(glob.glob(os.path.join(DATA, '[0-9]*_data.json'))):
        num = os.path.basename(f).split('_')[0]
        if num in SKIP:
            continue
        d = json.load(open(f, encoding='utf-8'))
        changed = False
        if num in FLAT:
            n = fix_pacing(d)
            if n: out['pacing'][num] = n; changed = True
        if num in STATICY:
            n = fix_statics(d)
            if n: out['statics'][num] = n; changed = True
        if changed:
            json.dump(d, open(f,'w',encoding='utf-8'), indent=2, ensure_ascii=False)
    print(json.dumps(out))

if __name__ == '__main__':
    main()
