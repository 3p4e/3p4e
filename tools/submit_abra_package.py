#!/usr/bin/env python3
"""ABRACADABRA_LTX25_PACKAGE jobs.json -> sunder-format jobfile. Positive wording only (artifact negatives per handoff rule 2)."""
import json, sys
from pathlib import Path

PKG = Path('/a0/usr/uploads/abra_ltx25_pkg/ABRACADABRA_LTX25_PACKAGE')
KF = PKG/'keyframes'
NEG = 'watermark, text, logo'

def main(only=None):
    jobs = json.load(open(PKG/'jobs.json'))
    jobs = jobs if isinstance(jobs, list) else jobs['jobs']
    shots, blocked = [], []
    for j in jobs:
        if only and j['id'] not in only: continue
        sf = j.get('start_file') or (j['start'] if j['start'].endswith('.png') else None)
        if not sf or not (PKG/sf).exists():
            blocked.append((j['id'], sf)); continue
        shots.append({
            'id': j['id'], 'resolution': f"{j['w']}x{j['h']}", 'frames': j['frames'],
            'seed': j['seed'], 'prompt': j['prompt'], 'negative': NEG,
            'start': sf, 'steps': j.get('steps', 8), 'cfg': j.get('cfg', 1.0),
            'first_frame_strength': 0.7, 'post': j.get('post', 'none'),
            'group': j.get('group'), 'fps': j.get('fps', 24),
        })
    op = Path(sys.argv[1])
    json.dump({'shots': shots}, open(op, 'w'), ensure_ascii=False, indent=1)
    print(f'jobs={len(jobs)} usable={len(shots)} blocked={len(blocked)} -> {op}')
    for b in blocked: print('  BLOCKED', b)

if __name__ == '__main__':
    main(set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None)
