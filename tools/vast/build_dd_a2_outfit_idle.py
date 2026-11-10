#!/usr/bin/env python3
"""Build dd_a2_outfit_idle_jobs.json — DD A2 Outfit Sheet (idle state).

Per VAST Production KB §5.1 A2: Full-body, ONE state, grey studio background,
no scene lighting, one subject per sheet. Director must visually accept.

Per §13.1 DD HEADWEAR: Bare head, NO cap/hood/mask on head. Hood ONLY as
back piece (cowl on shoulders/back). Glowing teal-blue underwater-wave hair
fully visible.

Per §13.2 WEAPONS: Twin legendary HAND crossbows (Frostbite-class) - ice-blue
arcane crystal limbs, frost runes, string of frozen light, teal-blue glow.
MUST appear in hero's hands.

Per weapon prompt pack (33_WEAPON_SHEET_PROMPT_PACK_EXTERNAL.md): fantasy
construction only, bowstring and limbs, NO firearm silhouette.

Identity wiring for Qwen-Image-Edit-2511:
  image1 = dd_fused_idle.png      accepted outfit reference (1280x720)
  image2 = dd_identity_1024.png   sharp DD frontal identity anchor (1024x1024)
"""
import json
import sys
from pathlib import Path

ROOT = Path("/a0/usr/projects/vast")
STAGE = ROOT / "tools" / "vast" / "jobs"

REF_OUTFIT = "dd_fused_idle.png"
REF_IDENTITY = "dd_identity_1024.png"

for name in (REF_OUTFIT, REF_IDENTITY):
    p = STAGE / name
    if not p.exists():
        sys.exit(f"missing staged reference: {p}")
    if p.stat().st_size < 50_000:
        sys.exit(f"suspiciously small reference: {p} ({p.stat().st_size} bytes)")
    print(f"OK: {p} ({p.stat().st_size} bytes)")

ANCHORS = (
    "keep the exact same face, eyes, eye spacing and iris colour, "
    "nose shape and nostrils, hairline and forehead proportion, "
    "jaw shape, and the same short dark beard and moustache as the reference man. "
    "The glowing teal-blue underwater-wave hair is fully visible, bare head, no cap or hood on head."
)

OUTFIT = (
    "Full-body character outfit sheet for DD the Demon Hunter in idle state, standing centred on a "
    "plain neutral grey studio background, soft even lighting, no cast shadows except soft contact shadow. "
    "BARE HEAD - no cap, no hood, no mask, no bandana on the head. Hood is ONLY a back piece: a cowl "
    "resting on the shoulders and back like a cape, draped naturally. "
    "Glowing teal-blue underwater-wave hair flows free and fully visible around the face and shoulders. "
    "Dark worn leather Demon Hunter armour with steel shoulder pauldrons, engraved bracers, "
    "utility belt with pouches, worn leather pants, heavy combat boots. "
    "TWIN LEGENDARY HAND CROSSBOWS (Frostbite-class) HELD IN BOTH HANDS, raised in ready pose: "
    "each is a compact pistol-grip hand crossbow with a curved bow limb of translucent ice-blue arcane "
    "crystal glowing teal-blue from within; slender dark steel body with engraved frost runes running along it; "
    "the bowstring is a line of frozen pale-blue light; faint frost mist curls off the limbs; "
    "matched twin pair, mirror-imaged left and right. FANTASY DESIGN - medieval hand crossbows with bowstrings "
    "and bolts, NO barrel, NO magazine, NO gun parts, NO firearm silhouette."
)

STYLE = (
    "Photorealistic full-body character reference sheet, ultra-detailed, high dynamic range, "
    "sharp focus, consistent proportions, 85mm lens-corrected, game-cinematic quality."
)

NEG = (
    "cap, hood on head, mask, bandana, head covering, covered hair, hidden face, "
    "firearm, gun, machinegun, Uzi, SMG, barrel, magazine, ammo clip, muzzle, stock, modern weapon, "
    "feminine, woman, female face, feminine jaw, softened jaw, smooth upper lip, different face, "
    "blurry, deformed, distorted, asymmetric, plastic skin, cartoon, illustration, painting, "
    "text, watermark, logo, busy background, multiple characters, low quality, low resolution, "
    "cropped by frame edge, extra limbs, missing weapon, empty hands"
)

jobs = []

def make_job(tag, seed, extra_view=""):
    prompt = f"{OUTFIT}{extra_view} {ANCHORS}. {STYLE}."
    jobs.append({
        "tag": tag,
        "seed": seed,
        "image1": REF_OUTFIT,
        "image2": REF_IDENTITY,
        "prompt": prompt,
        "negative": NEG,
        "width": 1024,
        "height": 1024,
        "steps": 50,
        "cfg": 4.0,
    })

# Primary full-body frontal view
make_job("dd_a2_outfit_idle_front_s1", 8701,
  "Frontal view, standing straight, both crossbows raised in ready pose, eyes on camera, calm neutral expression.")

# Slight angle to show side profile of outfit and crossbow details
make_job("dd_a2_outfit_idle_three_quarter_s1", 8802,
  "Three-quarter view turned slightly left, showing side profile of armour, cowl back-piece draping, and crossbow limb detail, eyes on camera.")

# Wider stance to show full body proportions
make_job("dd_a2_outfit_idle_full_stance_s1", 8903,
  "Full-body stance, feet shoulder-width, both crossbows at ready, weight evenly distributed, showing complete outfit from head to boots.")

out = STAGE / "dd_a2_outfit_idle_jobs.json"
out.write_text(json.dumps(jobs, indent=1))

print(json.dumps({
    "jobs": len(jobs),
    "file": str(out),
    "bytes": out.stat().st_size,
    "images": sorted({j["image1"] for j in jobs} | {j["image2"] for j in jobs}),
}, indent=1))
