#!/usr/bin/env python3
"""Face dataset QC for Higgsfield Soul ID training, and identity checks on generated frames.

Runs on CPU with OpenCV only (YuNet detector + SFace recognizer).

  python3 tools/face_qc.py dataset  <photos_dir> <out_dir>   # screen, rank, pick <=20, crop
  python3 tools/face_qc.py verify   <selected_dir> <frames>  # identity score of generated stills/frames

Thresholds come from the OpenCV SFace reference: cosine similarity >= 0.363 means "same person".
For a hero likeness we hold generated frames to a stricter internal limit (>= 0.50).
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
DET = HERE / "models" / "face_detection_yunet_2023mar.onnx"
REC = HERE / "models" / "face_recognition_sface_2021dec.onnx"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

SAME_PERSON = 0.363      # SFace published cosine threshold
HERO_LIKENESS = 0.50     # stricter acceptance limit for generated frames
DUPLICATE = 0.92         # near-identical shots add no information to training
MIN_FACE_PX = 256        # face box shorter side
MIN_SHARPNESS = 60.0     # variance of Laplacian on the face crop resized to 256 px
MAX_SOUL_IMAGES = 20     # Higgsfield Soul training accepts 5-20 images
DETECT_MAX_SIDE = 640    # YuNet works best on inputs around its training scale
YAW_BINS = [-0.3, -0.15, -0.05, 0.05, 0.15, 0.3]  # yaw index bin edges for angle diversity


def load_models():
    if not DET.exists() or not REC.exists():
        sys.exit("Missing models. Run: bash tools/fetch_models.sh")
    det = cv2.FaceDetectorYN.create(str(DET), "", (320, 320), 0.8, 0.3, 5000)
    rec = cv2.FaceRecognizerSF.create(str(REC), "")
    return det, rec


def images(path):
    p = Path(path)
    # Sub-folders starting with "_" (e.g. faces/_excluded) hold photos set aside by hand
    files = [p] if p.is_file() else sorted(
        f for f in p.rglob("*")
        if f.suffix.lower() in EXTS and not any(part.startswith("_") for part in f.relative_to(p).parts))
    return files


def analyse(det, rec, file):
    img = cv2.imread(str(file))
    if img is None:
        return {"file": file.name, "verdict": "REJECT", "reason": "unreadable"}, None, None
    h, w = img.shape[:2]
    # YuNet misses large faces at full phone resolution: detect on a <=640 px copy, scale back
    scale = min(1.0, DETECT_MAX_SIDE / max(h, w))
    small = cv2.resize(img, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA)
    det.setInputSize((small.shape[1], small.shape[0]))
    _, faces = det.detect(small)
    if faces is not None:
        faces = faces.copy()
        faces[:, :14] /= scale
    n = 0 if faces is None else len(faces)
    row = {"file": file.name, "width": w, "height": h, "faces": n}
    if n != 1:
        row.update(verdict="REJECT", reason="no face" if n == 0 else "more than one face")
        return row, None, img
    face = faces[0]
    x, y, fw, fh = face[:4].astype(int)
    crop = img[max(y, 0):y + fh, max(x, 0):x + fw]
    # Sharpness on a fixed-size crop so the score does not depend on face size or resolution
    gray = cv2.resize(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY), (256, 256), interpolation=cv2.INTER_AREA)
    # Eye line tilt and nose offset give a rough yaw/roll so we can keep angle diversity
    rx, ry, lx, ly, nx = face[4], face[5], face[6], face[7], face[8]
    roll = float(np.degrees(np.arctan2(ly - ry, lx - rx)))
    yaw = float((nx - (rx + lx) / 2) / max(abs(lx - rx), 1))
    row.update(
        face_px=int(min(fw, fh)),
        sharpness=round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 1),
        brightness=round(float(gray.mean()), 1),
        roll_deg=round(roll, 1),
        yaw_index=round(yaw, 2),
        det_score=round(float(face[-1]), 3),
    )
    emb = rec.feature(rec.alignCrop(img, face)).flatten()
    emb = emb / np.linalg.norm(emb)
    reasons = []
    if row["face_px"] < MIN_FACE_PX:
        reasons.append("face too small")
    if row["sharpness"] < MIN_SHARPNESS:
        reasons.append("blurry")
    if not 60 <= row["brightness"] <= 200:
        reasons.append("under/over-exposed")
    row.update(verdict="REJECT" if reasons else "PASS", reason="; ".join(reasons))
    return row, (emb, face), img


def square_crop(img, face, size=1024):
    # Head-and-shoulders crop: face occupies roughly the middle third
    x, y, fw, fh = face[:4]
    cx, cy = x + fw / 2, y + fh / 2.2
    side = max(fw, fh) * 2.6
    h, w = img.shape[:2]
    side = min(side, w, h)
    x0 = int(np.clip(cx - side / 2, 0, w - side))
    y0 = int(np.clip(cy - side / 2, 0, h - side))
    out = img[y0:y0 + int(side), x0:x0 + int(side)]
    return cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA if side > size else cv2.INTER_CUBIC)


def cmd_dataset(src, out):
    det, rec = load_models()
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rows, embs = [], {}
    cache = {}
    for f in images(src):
        row, data, img = analyse(det, rec, f)
        rows.append(row)
        if data is not None:
            embs[f.name] = data[0]
            cache[f.name] = (f, data[1])

    # Identity consistency: compare every face to the median embedding of all faces
    if embs:
        centre = np.median(np.stack(list(embs.values())), axis=0)
        centre /= np.linalg.norm(centre)
        for row in rows:
            if row["file"] in embs:
                sim = float(embs[row["file"]] @ centre)
                row["identity_sim"] = round(sim, 3)
                if sim < SAME_PERSON + 0.1 and row["verdict"] == "PASS":
                    row.update(verdict="REJECT", reason="identity outlier (other person, heavy filter or old photo?)")

    # Rank passes by sharpness inside head-angle bins and take the bins round-robin, so the set
    # covers turned-left, frontal and turned-right views instead of piling up frontal selfies
    bins = {}
    for r in rows:
        if r["verdict"] == "PASS":
            bins.setdefault(int(np.digitize(r["yaw_index"], YAW_BINS)), []).append(r)
    for b in bins.values():
        b.sort(key=lambda r: r["sharpness"], reverse=True)
    passes = []
    while any(bins.values()):
        for k in sorted(bins):
            if bins[k]:
                passes.append(bins[k].pop(0))
    chosen = []
    for r in passes:
        e = embs[r["file"]]
        if any(float(e @ embs[c["file"]]) > DUPLICATE for c in chosen):
            r.update(verdict="SPARE", reason="near-duplicate of a selected photo")
            continue
        if len(chosen) >= MAX_SOUL_IMAGES:
            r.update(verdict="SPARE", reason="over the 20-image Soul limit")
            continue
        chosen.append(r)
        r["verdict"] = "SELECTED"

    for r in chosen:
        f, face = cache[r["file"]]
        cv2.imwrite(str(out / (Path(r["file"]).stem + "_1024.jpg")), square_crop(cv2.imread(str(f)), face),
                    [cv2.IMWRITE_JPEG_QUALITY, 95])

    fields = ["file", "verdict", "reason", "identity_sim", "face_px", "sharpness", "brightness",
              "roll_deg", "yaw_index", "det_score", "faces", "width", "height"]
    with open(out / "qc_report.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    yaws = [r["yaw_index"] for r in chosen]
    print(f"Screened {len(rows)} | selected {len(chosen)} | report: {out / 'qc_report.csv'}")
    if yaws:
        print(f"Angle spread (yaw index) {min(yaws):+.2f} .. {max(yaws):+.2f}  "
              "(aim for both sides beyond +/-0.25 so profile views are represented)")
    if len(chosen) < 5:
        print("FAIL: Soul training needs at least 5 usable photos.")
    for r in rows:
        if r["verdict"] != "SELECTED":
            print(f"  {r['verdict']:8} {r['file']}: {r['reason']}")


def cmd_verify(ref_dir, frames):
    det, rec = load_models()
    refs = []
    for f in images(ref_dir):
        _, data, _ = analyse(det, rec, f)
        if data is not None:
            refs.append(data[0])
    if not refs:
        sys.exit("No reference faces found.")
    centre = np.mean(np.stack(refs), axis=0)
    centre /= np.linalg.norm(centre)
    for f in images(frames):
        row, data, _ = analyse(det, rec, f)
        if data is None:
            print(f"NO FACE  {f.name}")
            continue
        sim = float(data[0] @ centre)
        verdict = "PASS" if sim >= HERO_LIKENESS else "WEAK" if sim >= SAME_PERSON else "FAIL"
        print(f"{verdict:8} {sim:.3f}  {f.name}")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in {"dataset", "verify"}:
        sys.exit(__doc__)
    {"dataset": cmd_dataset, "verify": cmd_verify}[sys.argv[1]](sys.argv[2], sys.argv[3])
