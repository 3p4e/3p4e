#!/usr/bin/env python3
"""P7 proof gate for the Fenrir S10 clip: measured motion, luma flicker, static-frame
sweep, start-frame fidelity, face-region stability. Emits metrics + sample frames."""
import re
import json, sys
from pathlib import Path
import cv2
import numpy as np

ROOT = Path('/a0/usr/projects/vast')
CLIP = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'media/fenrir_assets/proofs/fenrir_s10_p7.mp4'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else CLIP.parent
OUT.mkdir(parents=True, exist_ok=True)

MIN_MOTION = 1.5       # mean |frame diff| (0-255) below this = slideshow/static
MAX_FLICKER = 12.0     # std of per-frame mean luma; above = strobe/flicker
MAX_LOW_RUN = 8        # consecutive frames under 0.5 diff = frozen stretch

cap = cv2.VideoCapture(str(CLIP))
if not cap.isOpened():
    sys.exit('FATAL: cannot open clip')

frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
cap.release()
n = len(frames)
print(f'frames: {n}')
if n < 100:
    sys.exit('FATAL: clip too short')

gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]
luma = np.array([g.mean() for g in gray])

# 1. motion: consecutive frame diffs (downscaled for speed)
diffs = []
for i in range(1, n):
    a = cv2.resize(gray[i - 1], (304, 176))
    b = cv2.resize(gray[i], (304, 176))
    diffs.append(float(np.abs(a.astype(np.int16) - b.astype(np.int16)).mean()))
diffs = np.array(diffs)

# 2. static runs
low = diffs < 0.5
runs, cur = [], 0
for v in low:
    cur = cur + 1 if v else 0
    runs.append(cur)
max_low_run = max(runs)

# 3. flicker (detrended luma std)
flicker = float(np.std(np.diff(luma)))

# 4. start fidelity: frame 0 vs this shot's keyframe (parsed from clip name)
_m = re.search(r's(\d+)', CLIP.name)
_kf = f'kf_{int(_m.group(1)):02d}_start.png' if _m else 'kf_10_start.png'
kf10 = cv2.imread(str(ROOT / 'media/fenrir_assets/keyframes' / _kf))
a = cv2.resize(gray[0], (304, 176)).astype(np.float32)
b = cv2.resize(cv2.cvtColor(kf10, cv2.COLOR_BGR2GRAY), (304, 176)).astype(np.float32)
start_diff = float(np.abs(a - b).mean())

# 5. face-region stability (largest face in first vs last frame)
sys.path.insert(0, str(ROOT / 'tools'))
import face_qc as F
det, rec = F.load_models()

import tempfile
def biggest_face_emb(img):
    from pathlib import Path as _P
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as t:
        cv2.imwrite(t.name, img)
        tmp = _P(t.name)
    try:
        row, payload, _ = F.analyse(det, rec, tmp)
        if payload is None:
            return None
        return payload[0]
    finally:
        import os; os.unlink(tmp)

e0 = biggest_face_emb(frames[0])
e1 = biggest_face_emb(frames[-1])
face_sim = None
if e0 is not None and e1 is not None:
    face_sim = float(np.dot(e0, e1) / (np.linalg.norm(e0) * np.linalg.norm(e1)))

# sample frames + contact sheet
for idx in (0, 30, 60, 90, 120):
    if idx < n:
        cv2.imwrite(str(OUT / f'{CLIP.stem}_f{idx:03d}.png'), frames[idx])
sheet = np.hstack([cv2.resize(frames[i], (304, 176)) for i in (0, 30, 60, 90, 120) if i < n])
cv2.imwrite(str(OUT / f'{CLIP.stem}_contact_sheet.png'), sheet)

verdict = 'PASS'
reasons = []
if diffs.mean() < MIN_MOTION:
    verdict = 'FAIL'; reasons.append(f'motion {diffs.mean():.2f} < {MIN_MOTION} (static/slideshow)')
if flicker > MAX_FLICKER:
    verdict = 'FAIL'; reasons.append(f'flicker {flicker:.2f} > {MAX_FLICKER}')
if max_low_run > MAX_LOW_RUN:
    verdict = 'FAIL'; reasons.append(f'frozen run {max_low_run} frames > {MAX_LOW_RUN}')
if start_diff > 60:
    verdict = 'FAIL'; reasons.append(f'start fidelity diff {start_diff:.1f} > 60 (frame 0 does not match shot keyframe)')
if face_sim is not None and face_sim < 0.60:
    verdict = 'FAIL'; reasons.append(f'face stability {face_sim:.3f} < 0.60')

report = {
    'clip': str(CLIP), 'frames': n,
    'motion_mean': round(float(diffs.mean()), 3),
    'motion_p95': round(float(np.percentile(diffs, 95)), 3),
    'motion_max': round(float(diffs.max()), 3),
    'luma_flicker': round(flicker, 3),
    'max_low_diff_run': int(max_low_run),
    'start_fidelity_diff': round(start_diff, 2),
    'face_first_last_sim': None if face_sim is None else round(face_sim, 3),
    'verdict': verdict, 'reasons': reasons,
}
(OUT / (CLIP.stem + '_gate_report.json')).write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
