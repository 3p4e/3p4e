#!/usr/bin/env python3
"""Build kory_jobs.json — feminisation pass for KORY (female Demon Hunter).

KORY is the in-game female persona played by the real person DD.
See higgsfield/KORY_CANON.md for the canon record and identity evidence.

Identity wiring for Qwen-Image-Edit-2511:
  image1 = kory_start_1024.png   her own wig frame: hair, styling, real KORY presentation
  image2 = dd_identity_1024.png  the sharp, well-lit DD frontal: identity anchor

The edit must STRIP the beard and moustache and SOFTEN the face toward female
reading, while preserving the identity anchors (eyes, eye spacing, nose,
nostrils, the mole on the left cheek, hairline).

Three seeds so the SFace gate has candidates to choose from.
Costs nothing to build or validate; only the render is paid.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "tools" / "vast" / "jobs"

START = "kory_start_1024.png"
REF = "dd_identity_1024.png"

for name in (START, REF):
    p = STAGE / name
    if not p.exists():
        sys.exit(f"missing staged reference: {p}")
    if p.stat().st_size < 50_000:
        sys.exit(f"suspiciously small reference: {p} ({p.stat().st_size} bytes)")

# --- the identity anchors that must survive the edit -------------------------
ANCHORS = (
    "keep the exact same eyes, the same eye spacing and iris colour, "
    "the same nose shape and nostrils, the same hairline and forehead proportion, "
    "and the same small mole on the left cheek below the eye"
)

# --- the feminisation instruction -------------------------------------------
# Deliberately describes the TARGET state instead of naming the features to
# delete: edit models can latch onto a noun like "beard" in the positive prompt.
# The exclusions live in NEG below, where they belong.
FEMINISE = (
    "Turn this into KORY, the same person as the reference man, now a young woman. "
    "Her face is a young woman's face with a perfectly smooth, clean-shaven upper "
    "lip, chin and jaw, flawless bare skin across the whole lower face. "
    "Feminine bone structure: a narrower jawline, a softer chin, a softened brow "
    "ridge, subtly fuller cheeks, slightly fuller lips, a slender softened neck "
    "and shoulders. "
)

LOOK = (
    "Long flowing red-and-black hair, striking female Demon Hunter presence, "
    "real unretouched skin with visible pores, natural light, 85 mm lens-corrected "
    "proportions"
)

STYLE = (
    "Photorealistic character card portrait, head and shoulders, centred, "
    "even studio key light, shallow depth of field, ultra-detailed, high dynamic range"
)

NEG = (
    "moustache, beard, stubble, facial hair, five o'clock shadow, shadow on upper lip, "
    "masculine heavy jaw, heavy brow ridge, adam's apple, blurry, deformed face, "
    "distorted eyes, asymmetric eyes, different face, plastic skin, cartoon, "
    "illustration, painting, text, watermark, low quality, low resolution, "
    "cropped by frame edge"
)

jobs = []

def j(tag, seed, extra):
    prompt = f"{FEMINISE}{extra} {ANCHORS}. {LOOK}. {STYLE}."
    jobs.append({
        "tag": tag,
        "seed": seed,
        "image1": START,
        "image2": REF,
        "prompt": prompt,
        "negative": NEG,
    })

# Frontal, neutral, the primary candidate
j("kory_fem_front_s1", 9101,
  "Frontal view, looking directly at the camera with a calm neutral expression.")

# Frontal, softer, slightly warmer expression
j("kory_fem_front_s2", 9202,
  "Frontal view, facing the camera with a faint confident smile, "
  "gentle catchlights in the eyes.")

# Three-quarter turn for the card set
j("kory_fem_three_quarter_s1", 9303,
  "Head turned about thirty degrees to her left in a three-quarter view, "
  "eyes still on the camera.")

out = STAGE / "kory_jobs.json"
out.write_text(json.dumps(jobs, indent=1))

print(json.dumps({
    "jobs": len(jobs),
    "file": str(out),
    "bytes": out.stat().st_size,
    "images": sorted({j["image1"] for j in jobs} | {j["image2"] for j in jobs}),
}, indent=1))
