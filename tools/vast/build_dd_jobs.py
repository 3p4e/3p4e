#!/usr/bin/env python3
"""Build dd_jobs.json — character cards for DD (the real person, male Demon Hunter).

Unlike KORY (DD's female in-game persona, which must be feminised and have the
beard/moustache removed), DD's card keeps HIS OWN presentation exactly: bearded,
male, same identity. The negative prompt therefore must NOT contain
beard/moustache/stubble — that would fight the canon identity.

Identity wiring for Qwen-Image-Edit-2511:
  image1 = dd_identity_1024.png   the sharp, well-lit DD frontal: identity anchor
  image2 = dd_identity_1024.png   same image, reinforces the anchors

Costs nothing to build or validate; only the render is paid.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "tools" / "vast" / "jobs"

REF = "dd_identity_1024.png"
p = STAGE / REF
if not p.exists():
    sys.exit(f"missing staged reference: {p}")
if p.stat().st_size < 50_000:
    sys.exit(f"suspiciously small reference: {p} ({p.stat().st_size} bytes)")

ANCHORS = (
    "keep the exact same eyes, the same eye spacing and iris colour, "
    "the same nose shape and nostrils, the same hairline and forehead proportion, "
    "the same jaw shape and the same short dark beard and moustache as the reference man"
)

PRESERVE = (
    "The same man from the reference, unchanged in identity: a real bearded man, "
    "clean sharp photography, natural skin texture with visible pores and stubble detail. "
)

LOOK = (
    "Male Demon Hunter presence, dark worn leather and steel shoulder detail, "
    "natural light, 85 mm lens-corrected proportions"
)

STYLE = (
    "Photorealistic character card portrait, head and shoulders, centred, "
    "even studio key light, shallow depth of field, ultra-detailed, high dynamic range"
)

NEG = (
    "feminine, woman, female face, feminine jaw, softened jaw, smooth upper lip, "
    "different face, blurry, deformed face, distorted eyes, asymmetric eyes, "
    "plastic skin, cartoon, illustration, painting, text, watermark, "
    "low quality, low resolution, cropped by frame edge"
)

jobs = []

def j(tag, seed, extra):
    prompt = f"{PRESERVE}{extra} {ANCHORS}. {LOOK}. {STYLE}."
    jobs.append({
        "tag": tag,
        "seed": seed,
        "image1": REF,
        "image2": REF,
        "prompt": prompt,
        "negative": NEG,
    })

j("dd_card_front_s1", 9401,
  "Frontal view, looking directly at the camera with a calm neutral expression.")

j("dd_card_front_s2", 9502,
  "Frontal view, facing the camera with a faint confident smile, gentle catchlights in the eyes.")

j("dd_card_three_quarter_s1", 9603,
  "Head turned about thirty degrees to his left in a three-quarter view, eyes still on the camera.")

out = STAGE / "dd_jobs.json"
out.write_text(json.dumps(jobs, indent=1))

print(json.dumps({
    "jobs": len(jobs),
    "file": str(out),
    "bytes": out.stat().st_size,
    "images": sorted({j["image1"] for j in jobs}),
}, indent=1))
