#!/usr/bin/env python3
"""Authenticity check of generated portraits against the real reference photos.

For every generated image it reports:
  * SFace cosine similarity to each real photo: mean / max / min over the whole set
    (>= 0.363 same person per OpenCV reference; we require mean >= 0.50).
  * Facial geometry: landmark ratios normalised by inter-ocular distance (IOD),
    compared to the mean of the least lens-distorted selfies (given with --geometry-refs).
    Ratios: eye-to-nose, nose-to-mouth, mouth width. A deviation > 10 % is flagged.

  python3 tools/authenticity_check.py <real_dir> <generated_dir> [--geometry-refs a.jpg b.jpg ...]
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

MODELS = Path(__file__).parent / "models"
DET = MODELS / "face_detection_yunet_2023mar.onnx"
REC = MODELS / "face_recognition_sface_2021dec.onnx"
EXT = {".jpg", ".jpeg", ".png", ".webp"}


def load(det, path):
    img = cv2.imread(str(path))
    if img is None:
        return None, None
    h, w = img.shape[:2]
    s = 640 / max(h, w)
    small = cv2.resize(img, (int(w * s), int(h * s)))
    det.setInputSize((small.shape[1], small.shape[0]))
    _, faces = det.detect(small)
    if faces is None:
        return img, None
    f = faces[np.argmax(faces[:, 2] * faces[:, 3])].copy()
    f[:14] /= s
    return img, f


def ratios(f):
    le, re, nose, ml, mr = f[4:14].reshape(5, 2)
    iod = np.linalg.norm(re - le)
    return np.array([
        np.linalg.norm(nose - (le + re) / 2) / iod,
        np.linalg.norm(nose - (ml + mr) / 2) / iod,
        np.linalg.norm(mr - ml) / iod,
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("real_dir")
    ap.add_argument("gen_dir")
    ap.add_argument("--geometry-refs", nargs="*", default=[])
    a = ap.parse_args()

    det = cv2.FaceDetectorYN.create(str(DET), "", (320, 320), 0.6)
    rec = cv2.FaceRecognizerSF.create(str(REC), "")

    def embed(img, f):
        return rec.feature(rec.alignCrop(img, f))

    real = []
    for p in sorted(Path(a.real_dir).iterdir()):
        if p.suffix.lower() in EXT:
            img, f = load(det, p)
            if f is not None:
                real.append(embed(img, f))
    if not real:
        sys.exit("No reference faces found.")

    geo = []
    for p in a.geometry_refs:
        img, f = load(det, p)
        if f is not None:
            geo.append(ratios(f))
    geo_mean = np.mean(geo, axis=0) if geo else None

    print(f"{'image':28} {'mean':>6} {'max':>6} {'min':>6}  geometry dev % (eye-nose, nose-mouth, mouth-w)  verdict")
    for p in sorted(Path(a.gen_dir).iterdir()):
        if p.suffix.lower() not in EXT:
            continue
        img, f = load(det, p)
        if f is None:
            print(f"{p.name:28}  NO FACE")
            continue
        e = embed(img, f)
        sims = np.array([rec.match(e, r, cv2.FaceRecognizerSF_FR_COSINE) for r in real])
        line = f"{p.name:28} {sims.mean():6.3f} {sims.max():6.3f} {sims.min():6.3f}"
        flags = []
        if sims.mean() < 0.50:
            flags.append("LOW-LIKENESS")
        if geo_mean is not None:
            dev = (ratios(f) - geo_mean) / geo_mean * 100
            line += "  " + ", ".join(f"{d:+5.1f}" for d in dev)
            if np.any(np.abs(dev) > 10):
                flags.append("GEOMETRY")
        print(line + "   " + ("OK" if not flags else " ".join(flags)))


if __name__ == "__main__":
    main()
