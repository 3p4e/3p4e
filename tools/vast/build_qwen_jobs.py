#!/usr/bin/env python3
"""Build qwen_jobs.json for run_qwen_edit.py — THE PALADIN'S JUDGEMENT (Azulon).

FULL-QUALITY face-locked edit (40 steps, cfg 3.0, NO Lightning LoRA).

Hero = AZULON, the canonical protagonist, face-locked to the user's real reference
photos via Qwen-Image-Edit-2511:
  image1 = existing gated Paladin keyframe (restage base + scene)
  image2 = A_bust.png   (primary identity reference photo)
  image3 = sheet_front.png (character sheet: costume + Selûne tattoo)

Dense composition rule (per user): every frame contains MULTIPLE content elements —
hero, villain and/or minions, environment architecture, and particles — never a lone
figure on an empty ground.

Two seeds per shot so the SFace gate has candidates to choose from.
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KF = os.path.join(ROOT, "media", "paladin_keyframes")
REFS = os.path.join(ROOT, "media", "refs")
STAGE = os.path.join(ROOT, "tools", "vast", "jobs")
os.makedirs(STAGE, exist_ok=True)

for f in ("p1_1.png", "p1_3.png", "p1_4a.png"):
    src = os.path.join(KF, f)
    if not os.path.exists(src):
        sys.exit(f"missing keyframe {src}")
    shutil.copy2(src, os.path.join(STAGE, f))
for f in ("A_bust.png", "sheet_front.png"):
    src = os.path.join(REFS, f)
    if not os.path.exists(src):
        sys.exit(f"missing identity ref {src}")
    shutil.copy2(src, os.path.join(STAGE, f))

AZULON = (
    "Azulon, completely hairless smooth shaved head, clean-shaven face with no moustache, "
    "no beard and no stubble, eyebrows kept, natural grey-green eyes open with direct gaze, "
    "very long high-elf ears sweeping backward and upward at forty degrees, lean wiry build, "
    "fine Selûne lunar-sacred-geometry tattoo in faded silver-grey and moon-blue ink, "
    "unretouched photographic skin, wearing silver plate armour with golden runes, a white "
    "wolf-fur mantle, a white tabard with a gold sunburst"
)

KING = ("a towering skeletal frost king, blackened bones in rusted plate and a jagged iron "
        "crown, hollow eye sockets glowing pale cyan-edged, frost-rimed shroud")

STYLE = (
    "Cinematic photorealistic film still, 16:9 widescreen, dense detailed composition, "
    "shallow depth of field, real snow and ice particles, volumetric backlight through the "
    "blizzard, muted steel-blue grade, gold light only from the hero, deep shadows, "
    "ultra-detailed, high dynamic range"
)

NEG = (
    "blurry, deformed face, distorted eyes, extra limbs, extra fingers, melted armor, cartoon, "
    "illustration, plastic skin, text, watermark, low quality, low resolution, different face, "
    "moustache, beard, stubble, hair on head, empty flat background, lone figure, sparse "
    "composition, duplicate face, cropped by frame edge"
)

jobs = []

def j(tag, seed, image1, prompt):
    jobs.append({"tag": tag, "seed": seed, "image1": image1,
                 "image2": "A_bust.png", "image3": "sheet_front.png",
                 "prompt": prompt, "negative": NEG})

# 1.1 — head bowed, hammer planted in ice, dense glacial environment
j("kf_1_1_s1", 1101, "p1_1.png",
  f"Lower Azulon's head until he bows over the massive square gold-inlaid warhammer, both hands "
  f"gripping the haft as the hammer head is planted into the cracked glacier ice at his feet, snow "
  f"settling on his mantle, while a standing ring of frost-carved monoliths and a wall of white "
  f"blizzard close the background. {STYLE}.")
j("kf_1_1_s2", 2202, "p1_1.png",
  f"Bend Azulon's neck so his chin drops near his chest in grief, lean both gauntleted hands on the "
  f"warhammer with its head resting on the broken ice, a wide frozen lake and snow-buried pine trees "
  f"receding behind him, falling snow filling the air. {STYLE}.")

# 1.3 — raised gauntlet, king recoiling, dense crowd/particles
j("kf_1_3_s1", 3303, "p1_3.png",
  f"Raise Azulon's left gauntlet, palm open toward the camera, as golden light floods from his "
  f"breastplate runes; directly behind him {KING} recoils from the gold light, its frost-rimed crown "
  f"glinting, while shards of ice and snow swirl in the backlight and a broad altar of black stone "
  f"sits at the frame edge. {STYLE}.")
j("kf_1_3_s2", 4404, "p1_3.png",
  f"Lift Azulon's left arm, palm open and warding, gold radiance streaming off his gauntlet; {KING} "
  f"flinches at the edge of the light, hollow sockets flaring pale cyan, broken columns and drifting "
  f"storm-snow filling the middle ground. {STYLE}.")

# 1.4A — king mid-lunge 3m away, gold ring burst, dense
j("kf_1_4a_s1", 5505, "p1_4a.png",
  f"Three metres away across the glacier ice {KING} lunges at Azulon with one skeletal claw raised, "
  f"as a perfect ring of golden light bursts outward across the cracked ice from the planted warhammer, "
  f"gold runes flaring up through the frost, snow and ice fragments tossed into the air between them. "
  f"{STYLE}.")
j("kf_1_4a_s2", 6606, "p1_4a.png",
  f"Place {KING} mid-lunge at the far edge of the expanding golden rune-ring that races across the "
  f"glacier from the planted warhammer, Azulon braced behind it, palm thrust forward, a shockwave of "
  f"light and blown snow ripping over the ice ridges. {STYLE}.")

out = os.path.join(STAGE, "qwen_jobs.json")
json.dump(jobs, open(out, "w"), indent=1)
print(json.dumps({"jobs": len(jobs), "file": out, "staged": sorted(os.listdir(STAGE))}, indent=1))
