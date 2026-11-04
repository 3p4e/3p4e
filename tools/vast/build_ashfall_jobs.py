#!/usr/bin/env python3
"""Build ashfall_jobs.json for run_qwen_edit.py — ASHFALL (Azulon as hero).

FULL-QUALITY face-locked edit (40 steps, cfg 3.0, NO Lightning LoRA).

Hero = AZULON, the canonical protagonist (same face as the Paladin and the corrected
ASHAFALL sets), face-locked to the user's real reference photos:
  image1 = A_bust.png   (primary identity reference photo — restaged into the scene)
  image2 = sheet_front.png (character sheet: costume + Selûne tattoo)

Villain = THE ASH KING (original, no reference needed).
World   = a dead volcano's caldera. Dense compositions throughout.
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REFS = os.path.join(ROOT, "media", "refs")
STAGE = os.path.join(ROOT, "tools", "vast", "jobs")
os.makedirs(STAGE, exist_ok=True)

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
    "unretouched photographic skin, wearing dark travel-worn plate over a grey tabard "
    "bearing a silver crescent"
)

ASH_KING = (
    "The Ash King, a towering gaunt figure over nine feet tall formed of black volcanic "
    "cinders and hardened ash, wearing a jagged crown of frozen grey smoke, hollow eye "
    "sockets glowing pale cyan, his tattered mantle of ash fraying at the edges into "
    "drifting cinders, radiating cold and darkness"
)

SET = (
    "a dead volcano's caldera, a field of black ash and cracked basalt, a ring of broken "
    "standing stones, and a colossal tilted stone sky-sundial against a storm-grey sky"
)

STYLE = (
    "Cinematic photorealistic film still, 16:9 widescreen, dense detailed composition, "
    "epic scale, volumetric lighting, a muted ashen-grey palette warmlit by the hero's "
    "gold radiance, fine drifting ash and ember particles, deep shadows, ultra-detailed, "
    "high dynamic range"
)

NEG = (
    "blurry, deformed face, distorted eyes, extra limbs, extra fingers, melted armor, "
    "cartoon, illustration, plastic skin, text, watermark, low quality, low resolution, "
    "different face, moustache, beard, stubble, hair on head, empty flat background, "
    "lone figure, sparse composition, duplicate face, cropped by frame edge"
)

START = "A_bust.png"

jobs = []

def j(tag, seed, prompt):
    jobs.append({"tag": tag, "seed": seed, "image1": START,
                 "image2": "sheet_front.png",
                 "prompt": prompt, "negative": NEG})

# BEAT 1 — ARRIVAL (dense establishing)
j("ash_1_arrival_wide", 101,
  f"Wide establishing shot across {SET}. In the mid-foreground {AZULON} crests a low ridge "
  f"of black ash, a sealed iron-and-glass lantern glowing gold at his hip. Across the caldera "
  f"on the far rim stands {ASH_KING}, utterly still beneath the tilted sky-sundial, a loose "
  f"mob of shambling ash-ghouls with guttering ember eyes climbing the ridge behind him. "
  f"{STYLE}.")

j("ash_2_hero", 202,
  f"Medium shot of {AZULON} holding the glowing lantern out at arm's length, its gold light "
  f"catching his silver-marble pauldron and the point of one long elven ear, while crouched "
  f"ash-ghouls with guttering ember eyes close in through the ash-fog behind him and the "
  f"tilted sky-sundial looms in the background. {STYLE}.")

j("ash_3_ashking", 303,
  f"Low-angle shot of {ASH_KING} striding through {SET}, ash-ghouls rising out of the cinders "
  f"around his feet, a few crackling golden barrier-runes collapsing in the foreground, "
  f"cinders streaming off his shoulders. {STYLE}.")

# BEAT 2 — THE FIGHT (dense action)
j("ash_4_flame_strike", 404,
  f"Action shot. {AZULON} thrusts the lantern forward and a torrent of golden flame erupts "
  f"across the ash, searing through a line of ash-ghouls that burst into burning embers, "
  f"while {ASH_KING} raises one huge cinder arm to shield himself, fire splashing around him "
  f"against the standing stones. {STYLE}.")

j("ash_5_lowpoint", 505,
  f"{AZULON} down on one knee in the ash, the lantern's flame guttering almost out between "
  f"his hands, surrounded on all sides by ash-ghouls closing in, while {ASH_KING} looms "
  f"above and a vast grey wave of frost rolls across the caldera floor, snuffing every spark. "
  f"{STYLE}.")

j("ash_6_rise", 606,
  f"{AZULON} rises among the ash-ghouls, his lunar tattoo beginning to blaze moon-white and "
  f"pale blue as arcs of silver light chase up his arms, the broken standing stones catching "
  f"the glow, {ASH_KING} watching from beneath the sky-sundial. {STYLE}.")

# BEAT 3 — THE SACRIFICE / VICTORY
j("ash_7_shatter", 707,
  f"Climactic shot. {AZULON} shatters the lantern overhead and a blinding golden pillar of "
  f"fire erupts down through him, his outline white-hot, a shockwave ring of gold and "
  f"moon-silver racing outward that hurls back the massed ash-ghouls and ignites the cinders "
  f"on {ASH_KING}, who throws up his jagged arms. {STYLE}.")

j("ash_8_fall", 808,
  f"{ASH_KING} crumbling apart and lifting upward as a column of burning embers like reversed "
  f"snow, his jagged crown dissolving into gold-lit cinders, while every remaining ash-ghoul "
  f"shivers into ash and the caldera is flooded with warm firelight. {STYLE}.")

j("ash_9_aftermath", 909,
  f"Aftermath. The caldera now quiet and still, dawn warming the grey sky over {SET}, and "
  f"where {AZULON} stood remains a single small steady golden flame burning in the ash, the "
  f"broken standing stones catching the first light. {STYLE}.")

out = os.path.join(STAGE, "ashfall_jobs.json")
json.dump(jobs, open(out, "w"), indent=1)
print(json.dumps({"jobs": len(jobs), "file": out, "staged": sorted(os.listdir(STAGE))}, indent=1))
