#!/usr/bin/env python3
"""Build the Wan2.1-FLF2V-14B-720P jobfile for #23 Perseus & Medusa.

Picture-lock order: S01-S20 -> F01-F10 -> S26-S60  (65 clips).
Prompt form per §39/§43 two-prompt discipline (Wan-FLF is identity-silent-safe):
  [verb-first motion sentence, endpoint in words] + [camera movement sentence]
  NO scene restatement, NO guard-boilerplate (Wan holds the start frame strong).
Sources:
  - keyframe doc Action/Camera lines (the frozen-moment beats)
  - fight expansion spec F01-F10 beats
Outputs tools/vast/jobs/p23_wan65.json
"""
import json, os, re

ROOT = '/a0/usr/projects/vast'
KF_DIR = f'{ROOT}/media/perseus_assets/keyframes'
FIGHT_KF = f'{KF_DIR}/fight'
OUT = f'{ROOT}/tools/vast/jobs/p23_wan65.json'
DOC = f'{ROOT}/storybook_ocr/specs/23_GROK_60_KEYFRAME_PROMPTS.md'
FIGHT_DOC = f'{ROOT}/storybook_ocr/specs/23_GROK_FIGHT_EXPANSION_PROMPTS.md'

# ---------------- camera line -> camera movement sentence ----------------
# The keyframe doc Camera lines are static framing intents ("composed as the frozen
# opening frame of a X move"). For the video-gen prompt we name the MOVE itself.
CAMERA_MOVE = {
    'crane-down': 'The camera cranes down slowly toward the scene.',
    'crane-up': 'The camera cranes up and away, revealing the wider scene.',
    'push-in': 'The camera pushes in steadily toward the subject.',
    'pull-back': 'The camera pulls back to widen the frame.',
    'static': 'The camera holds static, letting the action play out in frame.',
    'pan-left': 'The camera pans left, tracking the movement.',
    'pan-right': 'The camera pans right, tracking the movement.',
    'tilt-up': 'The camera tilts up to follow the rising action.',
    'tilt-down': 'The camera tilts down to follow the descending action.',
    'tracking': 'The camera tracks laterally, keeping pace with the subject.',
    'orbit': 'The camera orbits slowly around the subject.',
    'dolly-in': 'The camera dollies in closer.',
    'dolly-out': 'The camera dollies out.',
    'whip': 'The camera whips with the action.',
}

def camera_sentence(camera_line):
    cl = camera_line.lower()
    for key, sent in CAMERA_MOVE.items():
        if key in cl:
            return sent
    # default: push-in for close, pull-back for wide, static otherwise
    if 'close' in cl:
        return 'The camera pushes in slowly.'
    if 'wide' in cl:
        return 'The camera holds wide, then eases in.'
    return 'The camera holds steady on the subject.'

# ---------------- parse keyframe doc ----------------
def parse_keyframe_doc(path):
    """Return {shot_int: {'action': str, 'camera': str, 'scale': str}}."""
    txt = open(path, encoding='utf-8').read()
    shots = {}
    # split on SHOT headers
    blocks = re.split(r'## SHOT (\d{2})\s+\(([^)]*)\)', txt)
    # blocks: [pre, num, paren, body, num, paren, body, ...]
    for i in range(1, len(blocks) - 2, 3):
        num = int(blocks[i])
        paren = blocks[i + 1].strip()
        body = blocks[i + 2]
        am = re.search(r'\*{0,2}Action:\*{0,2}\s*(.+)', body)
        cm = re.search(r'\*{0,2}Camera:\*{0,2}\s*(.+)', body)
        action = am.group(1).strip() if am else ''
        action = re.sub(r'§§secret\([^)]*\)','',action).strip()
        camera = cm.group(1).strip() if cm else ''
        # paren like 'WIDE · high-angle · crane-down' -> scale + move
        parts = [p.strip() for p in paren.split('·')]
        scale = parts[0] if parts else ''
        shots[num] = {'action': action, 'camera': camera, 'scale': scale, 'paren': paren}
    return shots

# ---------------- parse fight doc ----------------
def parse_fight_doc(path):
    txt = open(path, encoding='utf-8').read()
    beats = {}
    blocks = re.split(r'## (F\d{2}) — ([^\n(]+)\(([^)]*)\)', txt)
    for i in range(1, len(blocks) - 3, 4):
        fid = blocks[i]
        name = blocks[i + 1].strip()
        paren = blocks[i + 2].strip()
        body = blocks[i + 3]
        am = re.search(r'\*{0,2}Action:\*{0,2}\s*(.+)', body)
        action = am.group(1).strip() if am else name
        beats[fid] = {'action': action, 'name': name, 'paren': paren}
    return beats

# ---------------- Wan-FLF prompt assembly ----------------
def wan_prompt(action, camera_line, scale=''):
    """Assemble the identity-silent continuation prompt for Wan-FLF."""
    cam = camera_sentence(camera_line)
    act = action.rstrip('.')
    # ensure verb-first: keep the action as-is (keyframe doc actions are already
    # descriptive of the frozen moment); append camera + a continuation cue.
    p = (f"{act}. {cam} The motion continues in one unbroken take, "
         f"resolving as the action completes.")
    return p

def main():
    kf = parse_keyframe_doc(DOC)
    fb = parse_fight_doc(FIGHT_DOC) if os.path.exists(FIGHT_DOC) else {}
    print(f'parsed keyframe doc: {len(kf)} shots; fight doc: {len(fb)} beats')

    jobs = []
    seed = 400
    # picture-lock order: S01-S20, F01-F10, S26-S60
    order = list(range(1, 21)) + [f'F{i:02d}' for i in range(1, 11)] + list(range(26, 61))
    n = 0
    for item in order:
        n += 1
        seed += 1
        if isinstance(item, int):
            kfpath = f'{KF_DIR}/kf_{item:02d}_start.png'
            info = kf.get(item, {})
            if not info:
                print(f'WARN: no keyframe doc entry for S{item:02d}')
                continue
            action = info['action']
            camera = info['camera']
            scale = info['scale']
            out = f'/workspace/out_wan/p23_s{item:02d}_wan.mp4'
        else:
            kfpath = f'{FIGHT_KF}/kf_{item}_start.jpg'
            info = fb.get(item, {})
            if not info:
                print(f'WARN: no fight doc entry for {item}')
                continue
            action = info['action']
            camera = info.get('paren', '')
            scale = ''
            out = f'/workspace/out_wan/p23_{item.lower()}_wan.mp4'
        if not os.path.exists(kfpath):
            print(f'WARN: missing keyframe {kfpath}')
            continue
        prompt = wan_prompt(action, camera, scale)
        jobs.append({'n': n, 'shot': str(item), 'kf': kfpath, 'out': out,
                     'seed': seed, 'prompt': prompt})

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(jobs, open(OUT, 'w'), ensure_ascii=False, indent=2)
    print(f'WROTE {OUT}: {len(jobs)} jobs')
    for j in jobs[:3]:
        print(f"\n--- n{j['n']} {j['shot']} ---\n{j['prompt'][:400]}")

if __name__ == '__main__':
    main()
