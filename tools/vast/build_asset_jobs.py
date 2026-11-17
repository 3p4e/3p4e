#!/usr/bin/env python3
"""Build the two MISSING lock-asset still jobs (Higgsfield Element-first workflow).

Unlike keyframes, these are standalone T2I (refs=[]) renders that become
REFERENCE images for the keyframe batch:
  - malgarot_look_card   -> boss look card (CLASS B: our unique faceless design)
  - crossbow_prop_sheet  -> twin-crossbow prop sheet (CLASS A: structure from
                            real arbalest photos externally, exact fantasy form here)

Grey-background character/prop sheets per Higgsfield rules; NO hands, NO figure
on the prop sheet; boss card has NO human face (faceless canon).

Output: tools/vast/jobfiles/asset_jobs.json (BARE LIST for run_kf_batch.py)
"""
import json

SEED = 555000

PROP_SHEET = (
    "Product reference sheet for two identical infernal hand crossbows, "
    "displayed side by side on a flat neutral mid-grey studio background, "
    "even soft lighting, no shadows cast on the background, no hand, no arm, "
    "no figure, no text, no watermark. Each crossbow is a compact twin-armed "
    "hand crossbow with a frost-rimed blackened-metal frame, a recurved steel "
    "bow, a short stock, and a loaded bolt. Both crossbows are idlers and "
    "share a single locked design: glacial blue-white frost crawling along the "
    "metal limbs, fine magenta-violet arcane sigils glowing along the stock, "
    "cold vapour drifting off the bolts. Left crossbow shown in direct lateral "
    "side view; right crossbow shown in three-quarter view. Photoreal still, "
    "high detail, sharp focus, consistent design between the two views."
)

BOSS_CARD = (
    "Full-figure character reference sheet of Mal'garot the Ash Lord, standing "
    "centred on a flat neutral mid-grey studio background, even soft lighting, "
    "no cast shadow on the background, full body from crown to feet visible, "
    "no text, no watermark. A colossal ember demon: hulking statue-like body "
    "sheathed in cracked obsidian plating with molten seams glowing between "
    "the plates, an exposed incandescent forge-core burning in its chest, a "
    "crown of dead grey coals atop its head, a long right arm that ends in a "
    "living molten whip of liquid fire instead of a hand, swirling ash and "
    "sparks rising from its shoulders, feet like cracked stone cradling embers. "
    "Crucially it has NO human face and no recognisable facial features: the "
    "head is a smooth black iron mask-like slab with only a faint forge glow "
    "seeping from its seam. Photoreal still, high detail, sharp focus."
)

NEG = ("cartoon, illustration, anime, stylised painting, plastic skin, human face, "
       "eyes, nose, mouth, hands, fingers, text, watermark, label, logo, "
       "busy background, multiple characters, low quality, blurry")

jobs = [
    {
        "id": "asset_crossbow_prop_sheet",
        "tag": "crossbow_prop_sheet",
        "shot": 0,
        "phase": "asset",
        "cast": [],
        "prompt": PROP_SHEET,
        "negative": NEG,
        "refs": [],
        "width": 1024,
        "height": 1024,
        "steps": 50,
        "cfg": 4.0,
        "seed": SEED + 1,
    },
    {
        "id": "asset_malgarot_look_card",
        "tag": "malgarot_look_card",
        "shot": 0,
        "phase": "asset",
        "cast": ["boss"],
        "prompt": BOSS_CARD,
        "negative": NEG,
        "refs": [],
        "width": 1024,
        "height": 1024,
        "steps": 50,
        "cfg": 4.0,
        "seed": SEED + 2,
    },
]

out = "tools/vast/jobfiles/asset_jobs.json"
json.dump(jobs, open(out, "w"), indent=1)

for j in jobs:
    print(f"{j['tag']}: {len(j['prompt'])} chars, {j['width']}x{j['height']}, refs={j['refs']}")
print(f"wrote {len(jobs)} asset jobs -> {out}")
print("note: crossbow uses an external real-arbalest photo as STRUCTURE reference",
      "in the keyframe pass per handover §5.5 (CLASS A).")
