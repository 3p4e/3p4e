#!/usr/bin/env python3
"""Build p23_hb_wanfc_116.json — Hollow Bloom v2 Wan 2.2 Fun Control jobfile.
Sources: p23_hb_k6c2_116.json (clip list, seeds, frames, keyframes)
         higgsfield/57_HB_V2_OPERATIONAL_CLARIFICATIONS.md (routing Q3/Q4)
Prompts: HOLD-form re-wrap of c2 ACTION clauses only; scene/character restatement
         and banned tails stripped (doc 43/50 anti-slop rules).
Output: tools/vast/jobs/p23_hb_wanfc_116.json
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C2 = os.path.join(ROOT, 'tools/vast/jobs/p23_hb_k6c2_116.json')
OUT = os.path.join(ROOT, 'tools/vast/jobs/p23_hb_wanfc_116.json')

BANNED = ["nothing settles into a held pose", "The movement stays strong and continuous",
          "No morphing, no drift", "bystanders", "morphing, drift"]

LTX_DEV = {7, 22, 31, 44, 45}
CHAOS = {6, 7, 8, 9, 15, 21, 24, 35, 36, 37, 46, 47}

MOTION_WORDS = ['stand','drift','creep','pulse','fire','flash','freeze','shatter','whip',
 'gouge','open','erupt','lift','dim','exhale','cock','crystallise','streak','sprint',
 'dodge','vault','land','brace','recoil','rise','kneel','charge','slash','cleave','strike',
 'bring','cross','rupture','widen','advance','curl','uncoil','bloom','crack','splinter',
 'flood','glow','brighten','darken','fall','settle','breathe','turn','push','thrust',
 'snap','burst','spill','spread','swell','sink','tilt','spin','sweep','collapse','part',
 'freeze-freeze','punch','blasts','hits','impacts','blooms','wakes','ignites','speaks']
POSE_VERBS = ['crossbow','sword','greatsword','vault','draw','fire','strike','dodge','dive',
 'cock','raise','cleave','slash','lunge','roll','plant','brace','recoil','kneel','rise',
 'sprint','charge','thrust','snap','bring']
SCENE_ONLY = ['marsh at dusk','dd (','az (','both heroes','spore-mist,','teal water','giant mushroom']

def is_motion(seg):
    s = seg.lower()
    return any(w in s for w in MOTION_WORDS)

def is_scene_only(seg):
    s = seg.lower()
    return any(t in s for t in SCENE_ONLY) and not is_motion(seg)

def extract_action(prompt):
    core = prompt.split('BLOCKING')[0].split('One continuous phase')[0]
    segs = [s.strip().rstrip('.') for s in core.split(';') if s.strip()]
    act = [s for s in segs if not is_scene_only(s)]
    if not act:
        act = segs[-1:] if segs else ['the named beat plays out']
    act = [re.sub(r'\s*\((?:[^()]|\([^()]*\))*\)', '', a) for a in act]
    txt = '; '.join(act)
    txt = txt[0].upper() + txt[1:]
    return txt[:300]

def extract_camera(prompt):
    m = re.search(r'Camera:\s*([^.]+)', prompt)
    if not m:
        return 'locked'
    move = m.group(1).strip()
    return move[:90]

def route(job):
    shot = job.get('shot'); kind = job.get('kind', 'start')
    snum = shot if isinstance(shot, int) else None
    if kind == 'cu' or snum in LTX_DEV:
        return dict(model='ltx23_dev', control='none', steps='30-40', cfg='3.0-3.5',
                    strength='0.7-0.8', fallback=None)
    p = job.get('prompt', '').lower()
    has_pose = any(v in p for v in POSE_VERBS)
    bloom = any(w in p for w in ['tendril','bloom','maw','spore rain','widen','corruption'])
    if has_pose and bloom: ctl, strength = 'pose+depth', '0.6-0.8'
    elif has_pose: ctl, strength = 'pose', '0.6-0.8'
    elif bloom: ctl, strength = 'depth', '0.5-0.7'
    else: ctl, strength = 'none', '0.5-0.7'
    fb = 'ltx_distilled' if snum in CHAOS else None
    return dict(model='wan22_fun_control', control=ctl, steps='4step-lightx2v',
                cfg='1.0-1.5', strength=strength, fallback=fb)

def hold_prompt(job, r):
    m = re.search(r'(kf_\w+\.(?:png|jpg))', job.get('kf', ''))
    kf = m.group(1) if m else job.get('kf', '')
    act = extract_action(job.get('prompt', ''))
    cam = extract_camera(job.get('prompt', ''))
    if 'camera' in act.lower():
        cam_s = ''
    else:
        cam_s = 'Camera locked.' if cam == 'locked' else f'Camera: {cam}.'
    if r['model'] == 'ltx23_dev':
        return (f"Using start frame {kf}. Composition, subjects, lighting direction, palette "
                f"and subject count hold. Only {act}. Nothing else changes. {cam_s}")
    ctl = '' if r['control'] == 'none' else f" Driven by {r['control']} control video."
    return (f"Using start frame {kf}. Composition, subjects, lighting direction, palette and "
            f"subject count hold. Only {act}.{ctl} {cam_s}")

def main():
    c2 = json.load(open(C2))
    out = []
    for job in c2:
        r = route(job)
        p = hold_prompt(job, r)
        low = p.lower()
        for b in BANNED:
            assert b.lower() not in low, f"banned tail leaked: {b}"
        assert 'new people' not in low and 'morphing' not in low and 'negative' not in low
        # anti-slop: scene restatement guard — prompt must not open with the marsh/DD/AZ description
        assert 'marsh at dusk;' not in low.split('only')[0], f"scene leak in {job['n']}"
        out.append(dict(n=job['n'], shot=job['shot'], kind=job.get('kind','start'),
            edit_slot=job.get('edit_slot'), kf=job['kf'], out=job['out'],
            seed=job['seed'], frames=job.get('frames', 81),
            model=r['model'], control=r['control'], steps=r['steps'], cfg=r['cfg'],
            strength=r['strength'], fallback=r['fallback'], prompt=p))
    json.dump(out, open(OUT,'w'), indent=1, ensure_ascii=False)
    models = {}; ctrls = {}
    for j in out:
        models[j['model']] = models.get(j['model'],0)+1
        ctrls[j['control']] = ctrls.get(j['control'],0)+1
    print('WROTE', OUT, len(out), 'jobs'); print('models:', models); print('controls:', ctrls)
    for i in (0, 1, 18, 43, 115):
        j = out[i]
        print('---', j['n'], j['shot'], j['model'], j['control'], '|', j['prompt'])

if __name__ == '__main__':
    main()
