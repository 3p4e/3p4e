#!/usr/bin/env python3
"""Pick the strongest identity reference cards for each character.

Scores every enrolled card against that person's SFace centroid (OpenCV
YuNet detector + SFace recognizer, the same pair face_qc.py uses) and copies
the two best matches into media/dhpf_refs/ under the names the ComfyUI
Edit jobs expect.

  /opt/venv/bin/python tools/pick_face_refs.py

Read-only on the card folders; only writes into media/dhpf_refs/.
"""
import os
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
DET = HERE / "models" / "face_detection_yunet_2023mar.onnx"
REC = HERE / "models" / "face_recognition_sface_2021dec.onnx"
ROOT = HERE.parent
OUT = ROOT / "media" / "dhpf_refs"

PEOPLE = [
    ("dd", ROOT / "faces" / "dd" / "centroid.npz", ROOT / "faces" / "dd_cards_final"),
    ("az", ROOT / "faces" / "blagoj" / "centroid.npz", ROOT / "faces" / "blagoj_cards_final"),
]


def main():
    for p in (DET, REC):
        if not p.exists():
            sys.exit(f"missing model: {p}")
    det = cv2.FaceDetectorYN.create(str(DET), "", (320, 320), 0.6, 0.3, 5000)
    rec = cv2.FaceRecognizerSF.create(str(REC), "")
    OUT.mkdir(parents=True, exist_ok=True)

    for person, cpath, cards in PEOPLE:
        if not cpath.exists():
            print(f"{person}: MISSING centroid {cpath}")
            continue
        cen = np.load(cpath)["centroid"].astype(np.float32).ravel()
        cen = cen / (np.linalg.norm(cen) + 1e-9)

        scores = []
        files = sorted([f for f in cards.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}])
        for f in files:
            img = cv2.imread(str(f))
            if img is None:
                continue
            h, w = img.shape[:2]
            det.setInputSize((w, h))
            ok, faces = det.detect(img)
            if not ok or faces is None or len(faces) == 0:
                continue
            best = max(faces, key=lambda r: r[2] * r[3])
            aligned = rec.alignCrop(img, best)
            feat = rec.feature(aligned).astype(np.float32).ravel()
            feat = feat / (np.linalg.norm(feat) + 1e-9)
            scores.append((float(feat @ cen), f))

        if not scores:
            print(f"{person}: no detectable faces")
            continue

        scores.sort(key=lambda t: t[0], reverse=True)
        print(f"{person}: scored {len(scores)} cards, best ->")
        for s, f in scores[:4]:
            print(f"    {s:.3f}  {f.name}")

        for i, (s, f) in enumerate(scores[:2]):
            dst = OUT / f"{person}face_{'ab'[i]}.jpg"
            shutil.copy2(f, dst)
            print(f"    staged {dst.name} from {f.name} (sim {s:.3f})")


if __name__ == "__main__":
    main()
