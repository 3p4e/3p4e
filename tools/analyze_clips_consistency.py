#!/usr/bin/env python3
"""FENRIR 46-clip inconsistency analysis: palette per act, brightness continuity,
audio presence, face counts, cut-smoothness (last->first frame diff)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

ROOT = Path('/a0/usr/projects/vast')
CLIPS = ROOT / 'media/fenrir_assets/clips'
KF = ROOT / 'media/fenrir_assets/keyframes'
RERUNNING = {5, 15, 16, 17, 46}
ACTS = {'act1': range(1, 15), 'act2': range(15, 37), 'act3': range(37, 47)}

def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'stream=codec_type,width,height,nb_frames',
                        '-show_entries', 'format=duration',
                        '-of', 'json', str(path)], capture_output=True, text=True)
    d = json.loads(r.stdout)
    st = [s for s in d.get('streams', []) if s.get('codec_type') == 'video'][0]
    au = [s for s in d.get('streams', []) if s.get('codec_type') == 'audio']
    return {'w': st.get('width'), 'h': st.get('height'),
            'frames': st.get('nb_frames'), 'dur': float(d['format'].get('duration', 0)),
            'audio': len(au) > 0}

def grab(path, n):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf',
                        f'select=eq(n\\,{n})', '-vsync', '0', '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True)
    arr = np.frombuffer(r.stdout, np.uint8)
    return arr.reshape(704, 1216, 3) if arr.size == 704 * 1216 * 3 else None

def palette(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    return {'hue_mean': float(h.mean()), 'sat_mean': float(s.mean()),
            'val_mean': float(v.mean()), 'val_p10': float(np.percentile(v, 10)),
            'warm_pct': float(((h < 30) | (h > 160)).mean() * 100)}

rows = []
for i in range(1, 47):
    name = f'fenrir_s{i:02d}.mp4'
    p = CLIPS / name
    if not p.exists():
        rows.append({'shot': i, 'error': 'missing'})
        continue
    info = probe(p)
    f0, f60, f120 = grab(p, 0), grab(p, 60), grab(p, 120)
    pal0 = palette(f0) if f0 is not None else None
    pal120 = palette(f120) if f120 is not None else None
    # cut smoothness: last frame of THIS clip vs first frame of NEXT clip
    cut = None
    if i < 46:
        nxt = CLIPS / f'fenrir_s{i+1:02d}.mp4'
        if nxt.exists() and f120 is not None:
            nf0 = grab(nxt, 0)
            if nf0 is not None:
                a = cv2.cvtColor(f120, cv2.COLOR_BGR2GRAY).astype(np.float32)
                b = cv2.cvtColor(nf0, cv2.COLOR_BGR2GRAY).astype(np.float32)
                cut = float(np.abs(a - b).mean())
    faces0 = 0
    if f0 is not None:
        det = cv2.FaceDetectorYN.create(str(ROOT / 'tools/models/face_detection_yunet_2023mar.onnx'), '', (1216, 704))
        det.setInputSize((1216, 704))
        _, fs = det.detect(f0)
        faces0 = 0 if fs is None else int(len(fs))
    rows.append({'shot': i, 'rerendering': i in RERUNNING, **info,
                 'pal0': pal0, 'pal120': pal120, 'cut_diff_next': cut, 'faces_f0': faces0})

# act-level palette stats
act_stats = {}
for act, rng in ACTS.items():
    vals = [r['pal0']['val_mean'] for r in rows if r.get('shot') in rng and r.get('pal0')]
    hues = [r['pal0']['hue_mean'] for r in rows if r.get('shot') in rng and r.get('pal0')]
    warms = [r['pal0']['warm_pct'] for r in rows if r.get('shot') in rng and r.get('pal0')]
    act_stats[act] = {'n': len(vals), 'val_mean': round(float(np.mean(vals)), 1),
                      'val_spread': round(float(np.std(vals)), 1),
                      'warm_pct_mean': round(float(np.mean(warms)), 1)}

# within-act outliers (val beyond 2 std of act mean)
flags = []
for r in rows:
    if not r.get('pal0') or r.get('error'):
        continue
    act = 'act1' if r['shot'] < 15 else ('act2' if r['shot'] < 37 else 'act3')
    s = act_stats[act]
    if abs(r['pal0']['val_mean'] - s['val_mean']) > 2 * max(s['val_spread'], 1):
        flags.append({'shot': r['shot'], 'type': 'brightness_outlier',
                      'val': r['pal0']['val_mean'], 'act_mean': s['val_mean']})
    if r.get('cut_diff_next') is not None and r['cut_diff_next'] > 40:
        flags.append({'shot': r['shot'], 'type': 'hard_cut',
                      'cut_diff': round(r['cut_diff_next'], 1)})
    if not r.get('audio'):
        flags.append({'shot': r['shot'], 'type': 'no_audio_stream'})

out = {'clips': rows, 'act_stats': act_stats, 'flags': flags}
(ROOT / 'storybook_ocr/specs/13_CLIP_CONSISTENCY_ANALYSIS.json').write_text(json.dumps(out, indent=1))
print('ACT STATS:', json.dumps(act_stats, indent=1))
print('FLAGS:', len(flags))
for f in flags:
    print(' ', f)
noau = [r['shot'] for r in rows if not r.get('audio') and not r.get('error')]
print('no-audio clips:', len(noau), noau[:10])
