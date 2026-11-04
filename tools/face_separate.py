#!/usr/bin/env python3
"""Multi-identity face separation: Oleg vs Geni, Kory-ready.

Runs on CPU with OpenCV only (YuNet detector + SFace recognizer).
No network, no upload, no GPU. Raw photos never leave this directory.

  python3 tools/face_separate.py

WHY ORDER-INDEPENDENT
  cluster_labels.txt records face labels in detector order, but detector order
  is not a contract. Filing faces by label position could file Oleg as Geni.
  So instead:
    1. The Oleg centroid is seeded from faces/oleg_originals, 13 human-verified
       single-face crops that contain exactly one person each.
    2. Faces in a multi-person plate are grouped by MUTUAL similarity using the
       SFace same-person threshold (0.363).
    3. A group is Oleg when its mean similarity to the Oleg centroid clears that
       same threshold; otherwise it is the other identity.
  Every face is then re-scored against BOTH centroids and written to a report,
  so each assignment is checkable rather than asserted.

OUTPUT
  faces/geni/srcs/            raw Geni face crops
  faces/geni/cards/           1024x1024 head-and-shoulders Geni cards
  faces/geni/centroid.npz     Geni identity centroid
  faces/oleg/centroid.npz     Oleg identity centroid
  faces/identity_index.json   multi-identity registry (Kory slots in here)
  faces/separation_report.csv every detected face with both similarity scores
"""
import csv
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import face_qc  # noqa: E402  reuse the exact gates and crop geometry

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
FACES = PROJ / "faces"
SAME_PERSON = face_qc.SAME_PERSON   # 0.363 cosine
CONFIRM = 0.72                      # own-centroid similarity for a card
MARGIN = 0.10                       # required lead over the runner-up


def detect_all(det, rec, path):
    """Return (image, [face dict]) for every face detected in the image."""
    img = cv2.imread(str(path))
    if img is None:
        return None, []
    h, w = img.shape[:2]
    # Detect at FULL resolution. face_qc.DETECT_MAX_SIDE (640) is tuned for
    # single-face acceptance and silently drops small faces: on a 1600x902
    # plate it found 2 faces where there are 4, and erased Geni completely.
    det.setInputSize((w, h))
    _, faces = det.detect(img)
    if faces is None:
        return img, []
    faces = faces.copy()
    out = []
    for f in faces:
        emb = rec.feature(rec.alignCrop(img, f)).flatten()
        emb = emb / np.linalg.norm(emb)
        x, y, fw, fh = f[:4].astype(int)
        out.append({"face": f, "emb": emb, "px": int(min(fw, fh)),
                    "box": (max(x, 0), max(y, 0), int(fw), int(fh))})
    return img, out


def centroid(embs):
    c = np.mean(np.stack(embs), axis=0)
    return c / np.linalg.norm(c)


def cluster(embs, thresh=SAME_PERSON):
    """Greedy grouping by similarity to the running group centroid."""
    groups = []
    for i, e in enumerate(embs):
        for g in groups:
            if float(e @ centroid([embs[j] for j in g])) >= thresh:
                g.append(i)
                break
        else:
            groups.append([i])
    return groups


def rec_row(file, idx, n, label, sim_oleg, emb):
    return {"file": file, "face_idx": idx, "faces": n, "label": label,
            "sim_oleg": round(sim_oleg, 3), "sim_geni": "", "margin": "",
            "_emb": emb}


def main():
    src = FACES / "all_originals"
    args = sys.argv[1:]
    if "--src" in args:
        src = Path(args[args.index("--src") + 1]).resolve()

    det, rec = face_qc.load_models()

    # ---- 1. seed Oleg from the human-verified single-face crops ----------
    oleg_embs = []
    seed_dir = FACES / "oleg_originals"
    for f in face_qc.images(seed_dir):
        _, fs = detect_all(det, rec, f)
        if fs:
            oleg_embs.append(max(fs, key=lambda d: d["px"])["emb"])
    if not oleg_embs:
        sys.exit(f"No faces found in {seed_dir}")
    oleg_c = centroid(oleg_embs)
    print(f"Oleg centroid from {len(oleg_embs)} verified crops")

    # ---- 2. classify every plate; cluster the multi-person ones ----------
    plates = face_qc.images(src)
    print(f"Scanning {len(plates)} plates in {src}")
    records = []
    geni_crops = []   # (file, img, face, box, emb)
    small_rejects = []  # faces below MIN_FACE_PX: real pixels, unusable as cards

    for f in plates:
        img, fs = detect_all(det, rec, f)
        if not fs:
            continue
        sims = [float(d["emb"] @ oleg_c) for d in fs]

        if len(fs) == 1:
            label = "oleg" if sims[0] >= face_qc.HERO_LIKENESS else "unknown"
            records.append(rec_row(f.name, 0, 1, label, sims[0], fs[0]["emb"]))
            continue

        # multi-person plate: group by mutual similarity, never by detector order
        for g in cluster([d["emb"] for d in fs]):
            group_sim = float(np.mean([sims[i] for i in g]))
            is_oleg = group_sim >= SAME_PERSON
            for i in g:
                # Never name an identity we cannot verify: a face below
                # MIN_FACE_PX cannot produce a card, so it stays unverified.
                if is_oleg:
                    lab = "oleg"
                elif fs[i]["px"] >= face_qc.MIN_FACE_PX:
                    lab = "geni"
                else:
                    lab = "other-tiny-unverified"
                records.append(rec_row(f.name, i, len(fs), lab,
                                       sims[i], fs[i]["emb"]))
            if not is_oleg:
                for i in g:
                    if fs[i]["px"] >= face_qc.MIN_FACE_PX:
                        geni_crops.append((f, img, fs[i]["face"],
                                           fs[i]["box"], fs[i]["emb"]))
                    else:
                        small_rejects.append((f.name, fs[i]["px"]))

    # ---- 3. Geni centroid, then re-score every face against both ---------
    if geni_crops:
        geni_c = centroid([c[4] for c in geni_crops])
        print(f"Geni centroid from {len(geni_crops)} faces")
    else:
        geni_c = None
        print("WARNING: no Geni faces isolated")

    if geni_c is not None:
        for r in records:
            so = float(r["_emb"] @ oleg_c)
            sg = float(r["_emb"] @ geni_c)
            r["sim_oleg"], r["sim_geni"] = round(so, 3), round(sg, 3)
            r["margin"] = round(so - sg, 3)
            best = "oleg" if so > sg else "geni"
            r["label"] = best + "*" if abs(so - sg) < MARGIN else best

    # ---- 4. write Geni raw crops and 1024 cards --------------------------
    gdir = FACES / "geni"
    (gdir / "srcs").mkdir(parents=True, exist_ok=True)
    (gdir / "cards").mkdir(parents=True, exist_ok=True)
    for n, (f, img, face, box, _) in enumerate(geni_crops):
        x, y, fw, fh = box
        cv2.imwrite(str(gdir / "srcs" / f"{f.stem}_f{n}.jpg"),
                    img[y:y + fh, x:x + fw], [cv2.IMWRITE_JPEG_QUALITY, 95])
        card = face_qc.square_crop(img, face, 1024)
        cv2.imwrite(str(gdir / "cards" / f"{f.stem}_f{n}_1024.jpg"), card,
                    [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"Wrote {len(geni_crops)} Geni faces -> {gdir}")

    # ---- 5. persist centroids and the multi-identity registry ------------
    (FACES / "oleg").mkdir(parents=True, exist_ok=True)
    np.savez(FACES / "oleg" / "centroid.npz", centroid=oleg_c)
    index = {"schema": "multi-identity-v1", "same_person": SAME_PERSON,
             "confirm": CONFIRM, "margin": MARGIN, "identities": {}}
    index["identities"]["oleg"] = {
        "centroid": "faces/oleg/centroid.npz",
        "seed_faces": len(oleg_embs), "status": "enrolled"}
    if geni_c is not None:
        np.savez(gdir / "centroid.npz", centroid=geni_c)
        index["identities"]["geni"] = {
            "centroid": "faces/geni/centroid.npz",
            "cards": len(geni_crops),
            "status": "enrolled-thin" if len(geni_crops) < 6 else "enrolled"}
    index["identities"]["kory"] = {"status": "awaiting-photos-and-consent"}
    (FACES / "identity_index.json").write_text(json.dumps(index, indent=2) + "\n")

    # ---- 6. report -------------------------------------------------------
    out_csv = FACES / "separation_report.csv"
    cols = ["file", "face_idx", "faces", "label", "sim_oleg", "sim_geni", "margin"]
    with out_csv.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(sorted(records, key=lambda r: (r["file"], r["face_idx"])))

    o = sum(1 for r in records if r["label"].startswith("oleg"))
    g = sum(1 for r in records if r["label"].startswith("geni"))
    u = sum(1 for r in records if r["label"] == "unknown")
    amb = sum(1 for r in records if r["label"].endswith("*"))
    print(f"\nfaces classified: oleg={o} geni={g} unknown={u} ambiguous={amb}")
    print(f"report -> {out_csv}")
    print(f"index  -> {FACES / 'identity_index.json'}")
    if small_rejects:
        print(f"\nfaces below MIN_FACE_PX={face_qc.MIN_FACE_PX} (cannot become cards):")
        for n, px in small_rejects:
            print(f"  {n}  px={px}")
    print("DONE")


if __name__ == "__main__":
    main()
