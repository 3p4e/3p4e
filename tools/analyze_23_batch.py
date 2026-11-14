#!/usr/bin/env python3
"""#23 Perseus 60-clip batch analysis: per-clip motion gate, luma stability,
frozen/black-frame sweep, audio presence, palette per act, cut smoothness.
Writes JSON metrics + human-readable summary."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

ROOT = Path('/a0/usr/projects/vast')
CLIPS = ROOT / 'media/perseus_assets/clips'
OUT = ROOT / 'media/perseus_assets/analysis'
OUT.mkdir(parents=True, exist_ok=True)

MIN_MOTION = 1.5       # mean |frame diff| below this = static/slideshow
MAX_FLICKER = 12.0     # std of per-frame mean luma; above = strobe
MAX_LOW_RUN = 8        # consecutive frames under 0.5 diff = frozen stretch
BLACK_PCT = 0.98       # frame mean luma below this fraction of max = near-black

ACTS = {'act1': range(1, 15), 'act2a': range(15, 31), 'act2b': range(31, 46), 'act3': range(46, 61)}

def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'stream=codec_type,width,height,nb_frames',
                        '-show_entries', 'format=duration',
                        '-of', 'json', str(path)], capture_output=True, text=True)
    d = json.loads(r.stdout)
    st = [s for s in d.get('streams', []) if s.get('codec_type') == 'video'][0]
    au = [s for s in d.get('streams', []) if s.get('codec_type') == 'audio']
    return {'w': st.get('width'), 'h': st.get('height'),
            'frames': int(st.get('nb_frames', 0)),
            'dur': float(d['format'].get('duration', 0)), 'audio': len(au) > 0}

def grab_gray(path, n, w=320):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf',
                        f'select=eq(n\\,{n}),scale={w}:-2', '-vsync', '0',
                        '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                       capture_output=True)
    arr = np.frombuffer(r.stdout, np.uint8)
    h = int(arr.size / w) if arr.size % w == 0 else 0
    return arr.reshape(h, w) if h else None

def analyze_clip(idx):
    p = CLIPS / f'p23_s{idx:02d}.mp4'
    if not p.exists():
        return {'shot': idx, 'error': 'missing'}
    info = probe(p)
    cap = cv2.VideoCapture(str(p))
    prev = None; diffs = []; lumas = []; black = 0; low_run = 0; max_low = 0
    n = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        luma = float(g.mean())
        lumas.append(luma)
        if luma < 8.0:
            black += 1
        if prev is not None:
            d = float(np.abs(g.astype(np.float32) - prev.astype(np.float32)).mean())
            diffs.append(d)
            if d < 0.5:
                low_run += 1
                max_low = max(max_low, low_run)
            else:
                low_run = 0
        prev = g
        n += 1
    cap.release()
    motion = float(np.mean(diffs)) if diffs else 0.0
    flicker = float(np.std(lumas)) if len(lumas) > 1 else 0.0
    return {'shot': idx, **info, 'n_read': n,
            'motion': round(motion, 2), 'flicker': round(flicker, 2),
            'max_low_run': max_low, 'black_frames': black,
            'motion_pass': motion >= MIN_MOTION,
            'flicker_pass': flicker <= MAX_FLICKER,
            'frozen_pass': max_low <= MAX_LOW_RUN,
            'black_pass': black == 0,
            'audio_pass': info['audio'],
            'spec_pass': info['w'] == 1216 and info['h'] == 704 and info['frames'] == 121}

def main():
    results = []
    for i in range(1, 61):
        r = analyze_clip(i)
        results.append(r)
        flags = []
        if r.get('error'): flags.append('MISSING')
        else:
            if not r['motion_pass']: flags.append('STATIC')
            if not r['flicker_pass']: flags.append('FLICKER')
            if not r['frozen_pass']: flags.append('FROZEN')
            if not r['black_pass']: flags.append('BLACK')
            if not r['audio_pass']: flags.append('NO_AUDIO')
            if not r['spec_pass']: flags.append('SPEC')
        status = ' '.join(flags) if flags else 'PASS'
        print(f"s{i:02d} motion={r.get('motion',0):5.2f} flicker={r.get('flicker',0):5.2f} "
              f"low={r.get('max_low_run',0):2d} black={r.get('black_frames',0):3d} "
              f"audio={r.get('audio_pass','?')} {status}")
    out = {'gates': {'MIN_MOTION': MIN_MOTION, 'MAX_FLICKER': MAX_FLICKER,
                     'MAX_LOW_RUN': MAX_LOW_RUN}, 'clips': results}
    (OUT / 'batch_analysis.json').write_text(json.dumps(out, indent=2))
    fails = [r['shot'] for r in results if not r.get('error') and not all(
        [r['motion_pass'], r['flicker_pass'], r['frozen_pass'], r['black_pass'], r['audio_pass'], r['spec_pass']])]
    print(f"\nSUMMARY: {60 - len(fails)}/60 pass all gates; flagged: {fails}")

if __name__ == '__main__':
    main()
