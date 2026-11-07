#!/usr/bin/env python3
"""Gate the 4 proof keyframes against DD + Blagoj centroids; build a contact sheet."""
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import face_qc as F

ROOT = Path('/a0/usr/projects/vast')
PROOF = ROOT / 'media/dhpf_proof_v3'

DD_CEN = np.load(ROOT / 'faces/dd/centroid.npz')['centroid']
BL_CEN = np.load(ROOT / 'faces/blagoj/centroid.npz')['centroid']
DD_CEN = DD_CEN / np.linalg.norm(DD_CEN)
BL_CEN = BL_CEN / np.linalg.norm(BL_CEN)

MIN_PX = getattr(F, 'MIN_FACE_PX', 120)
THRESH = 0.50


def detect_faces(img):
    h, w = img.shape[:2]
    side = getattr(F, 'DETECT_MAX_SIDE', 1280)
    scale = min(1.0, side / max(h, w))
    small = cv2.resize(img, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA)
    det.setInputSize((small.shape[1], small.shape[0]))
    _, faces = det.detect(small)
    if faces is None:
        return []
    faces = faces.copy()
    faces[:, :14] /= scale
    return faces


def emb_of(img, face):
    e = rec.feature(rec.alignCrop(img, face)).flatten()
    return e / np.linalg.norm(e)


det, rec = F.load_models()

rows = []
for fn in ['kf_03_start.png', 'kf_03_end.png', 'kf_19_start.png', 'kf_19_end.png']:
    p = PROOF / fn
    img = cv2.imread(str(p))
    faces = detect_faces(img)
    dets = []
    for i, f in enumerate(faces):
        px = int(min(f[2], f[3]))
        e = emb_of(img, f)
        sdd = float(e @ DD_CEN)
        sbl = float(e @ BL_CEN)
        who = 'DD' if sdd > sbl else ('AZ' if sbl > sdd else '?')
        best = max(sdd, sbl)
        verdict = 'PASS' if (best >= THRESH and px >= MIN_PX) else ('UNRELIABLE' if best >= THRESH else 'FAIL')
        dets.append({'i': i, 'px': px, 'dd': round(sdd, 3), 'az': round(sbl, 3),
                     'who': who, 'best': round(best, 3), 'verdict': verdict})
    rows.append({'file': fn, 'dim': f'{img.shape[1]}x{img.shape[0]}', 'faces': len(faces), 'det': dets})
    print(f"{fn:18s} {rows[-1]['dim']:12s} faces={len(faces)}")
    for d in dets:
        print(f"   face{d['i']} px={d['px']:4d} dd={d['dd']:.3f} az={d['az']:.3f} "
              f"-> {d['who']} best={d['best']:.3f} {d['verdict']}")

import json
(PROOF / 'proof_gate.json').write_text(json.dumps(rows, indent=1))

# ---- contact sheet ----
names = ['crossbow_prop_sheet.png', 'malgarot_look_card.png',
         'kf_03_start.png', 'kf_03_end.png', 'kf_19_start.png', 'kf_19_end.png']
TW, TH = 640, 360
COLS, ROWS = 3, 2
canvas = Image.new('RGB', (TW * COLS, TH * ROWS + 26 * ROWS), (24, 24, 24))
dr = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
except Exception:
    font = ImageFont.load_default()

for idx, name in enumerate(names):
    img = Image.open(PROOF / name).convert('RGB')
    w, h = img.size
    scale = max(TW / w, TH / h)
    nw, nh = round(w * scale), round(h * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - TW) // 2
    top = (nh - TH) // 2
    img = img.crop((left, top, left + TW, top + TH))
    x = (idx % COLS) * TW
    y = (idx // COLS) * (TH + 26)
    canvas.paste(img, (x, y))
    dr.text((x + 8, y + TH + 4), name, fill=(255, 255, 255), font=font)

sheet = PROOF / 'proof_contact_sheet.png'
canvas.save(sheet)
print('\ncontact sheet ->', sheet)
