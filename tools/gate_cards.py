#!/usr/bin/env python3
"""Gate character cards against an identity centroid.

  python3 tools/gate_cards.py <cards_dir> <centroid.npz> [--min-sim 0.50] [--min-px 256]

Per-file failure isolation: one unreadable or faceless image never aborts the run.
Reports a table plus an explicit PASS list for adoption.
"""
import sys
import traceback
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import face_qc as F  # noqa: E402

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def largest_face(det, img):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _, faces = det.detect(img)
    if faces is None or len(faces) == 0:
        return None
    return sorted(faces, key=lambda b: float(b[2]) * float(b[3]), reverse=True)[0]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cards_dir, centroid_path = Path(sys.argv[1]), Path(sys.argv[2])
    min_sim = float(sys.argv[sys.argv.index("--min-sim") + 1]) if "--min-sim" in sys.argv else 0.50
    min_px = int(sys.argv[sys.argv.index("--min-px") + 1]) if "--min-px" in sys.argv else 256

    centroid = np.load(centroid_path)["centroid"]
    centroid = centroid / np.linalg.norm(centroid)

    det, rec = F.load_models()
    files = sorted(p for p in cards_dir.iterdir() if p.suffix.lower() in EXTS)

    passed, failed, skipped = [], [], []
    for p in files:
        try:
            img = cv2.imread(str(p))
            if img is None:
                skipped.append((p.name, "unreadable"))
                print(f"{p.name:54s} SKIP unreadable")
                continue

            box = largest_face(det, img)
            if box is None:
                skipped.append((p.name, "no face"))
                print(f"{p.name:54s} {img.shape[1]}x{img.shape[0]:<6d} SKIP no face detected")
                continue

            emb = rec.feature(rec.alignCrop(img, box)).flatten()
            norm = np.linalg.norm(emb)
            if norm == 0:
                skipped.append((p.name, "zero embedding"))
                print(f"{p.name:54s} SKIP zero embedding")
                continue
            emb /= norm

            sim = float(np.dot(emb, centroid))
            px = int(box[3])
            ok = sim >= min_sim and px >= min_px
            verdict = "PASS" if ok else "fail"
            reasons = []
            if sim < min_sim:
                reasons.append(f"sim<{min_sim}")
            if px < min_px:
                reasons.append(f"face<{min_px}px")
            reason = ("  " + ",".join(reasons)) if reasons else ""
            print(f"{p.name:54s} {img.shape[1]}x{img.shape[0]:<6d} face={px:4d}px  sim={sim:.3f}  {verdict}{reason}")
            (passed if ok else failed).append((p.name, sim, px))
        except Exception as exc:  # isolate: one bad file must not abort the batch
            skipped.append((p.name, f"error {exc}"))
            print(f"{p.name:54s} SKIP error: {exc}")
            traceback.print_exc(limit=1)

    print()
    print(f"checked={len(files)}  pass={len(passed)}  fail={len(failed)}  skip={len(skipped)}")
    if passed:
        print("\nADOPT:")
        for name, sim, px in passed:
            print(f"  {name}  sim={sim:.3f} face={px}px")
    if skipped:
        print("\nSKIPPED:")
        for name, why in skipped:
            print(f"  {name}  ({why})")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
