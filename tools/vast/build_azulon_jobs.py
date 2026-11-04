#!/usr/bin/env python3
"""Build azulon_jobs.json for run_qwen_edit_full.py — the corrected hero.

Hero = AZULON, the project's canonical protagonist, face-locked to the user's real
reference photos (image2/image3 = A_bust.png + sheet_front.png) via Qwen-Image-Edit-2511
FULL quality (40 steps, cfg 3.0, NO Lightning LoRA — the 4-step shortcut is what mushed
the previous set).

Dense composition rule: every frame must contain MULTIPLE content elements — hero,
villain and/or minions, environment architecture, and particles/props — never a lone
figure on an empty ground.

Azulon canon (AZULON_CANON.md, current default):
  completely hairless smooth shaved head, clean-shaven, no moustache/beard/stubble,
  eyebrows kept, natural grey-green eyes, very long high-elf ears sweeping back 30-40deg,
  fine Selûne lunar tattoo (dormant: silver-grey + moon-blue), lean wiry build,
  unretouched photographic skin.
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REFS = os.path.join(ROOT, "media", "refs")
STAGE = os.path.join(ROOT, "tools", "vast", "jobs")
os.makedirs(STAGE, exist_ok=True)

# identity reference photos, copied to staging
for f in ("A_bust.png", "sheet_front.png"):
    src = os.path.join(REFS, f)
    if not os.path.exists(src):
        raise SystemExit(f"missing identity ref {src}")
    shutil.copy2(src, os.path.join(STAGE, f))

AZULON = (
    "Azulon, completely hairless smooth shaved head, clean-shaven face with no moustache, "
    "no beard and no stubble, eyebrows kept, natural grey-green eyes open with direct gaze, "
    "very long high-elf ears sweeping backward and upward at forty degrees, lean wiry build, "
    "fine Selûne lunar-sacred-geometry tattoo in faded silver-grey and moon-blue ink, "
    "unretouched photographic skin"
)

ASH_KING = (
    "The Ash King, a towering nine-foot gaunt figure of black volcanic cinders and hardened "
    "ash, jagged crown of frozen grey smoke, pale cyan-glowing hollow eye sockets, tattered "
    "mantle fraying into drifting cinders"
)

GHOULS = "ash-ghoul minions, shambling humanoid figures of packed grey ash with guttering ember eyes"

SET = (
    "a ruined moon-temple of Selûne, cracked colonnades and toppled silver-marble statues, "
    "a colossal broken stone sky-sundial tilted against a storm-grey sky, a field of black "
    "ash and dead trees"
)

STYLE = (
    "Cinematic photorealistic film still, 16:9 widescreen, dense detailed composition, "
    "volumetric lighting, drifting ash and ember particles, moon-silver and ash-grey palette "
    "warmlit by Azulon's gold radiance, deep shadows, ultra-detailed, high dynamic range"
)

NEG = (
    "blurry, deformed face, distorted eyes, extra limbs, extra fingers, melted armor, cartoon, "
    "illustration, plastic skin, text, watermark, low quality, low resolution, different face, "
    "moustache, beard, stubble, hair on head, empty flat background, lone figure, sparse "
    "composition, duplicate face, cropped by frame edge"
)

START = "A_bust.png"

jobs = []

def j(tag, seed, prompt):
    jobs.append({"tag": tag, "seed": seed, "image1": START,
                 "image2": "A_bust.png", "image3": "sheet_front.png",
                 "prompt": prompt, "negative": NEG})

# BEAT 1 — ARRIVAL (dense establishing)
j("az_1_arrival", 111,
  f"Wide establishing shot. {AZULON} stands on a ridge of black ash in {SET}, gripping a "
  f"sealed iron-and-glass lantern that holds a single dying golden ember. Behind him {GHOULS} "
  f"climb the ridge in a loose mob, ember eyes burning. Across the caldera {ASH_KING} waits "
  f"beneath the tilted sky-sundial. {STYLE}.")

j("az_2_hero", 222,
  f"Medium shot of {AZULON} from the side, holding the glowing lantern, its gold light catching "
  f"his silver-marble pauldron and the point of a long elven ear, while crouched {GHOULS} with "
  f"guttering ember eyes close in through the ash-fog behind him, and the tilted sky-sundial "
  f"looms in the background. {STYLE}.")

j("az_3_king", 333,
  f"Low-angle shot of {ASH_KING} striding through the {SET}, {GHOULS} rising out of the ash around "
  f"his feet, a few crackling golden barrier-runes collapsing in the foreground, cinders "
  f"streaming off his shoulders. {STYLE}.")

# BEAT 2 — THE FIGHT (dense action)
j("az_4_strike", 444,
  f"Action shot. {AZULON} thrusts the lantern forward and a torrent of golden flame erupts "
  f"across the ash, searing through a line of {GHOULS} that burst into burning embers, while "
  f"{ASH_KING} raises one huge cinder arm to shield himself, fire splashing around him. {STYLE}.")

j("az_5_lowpoint", 555,
  f"{AZULON} down on one knee in the ash, his lantern's flame guttering almost out between his "
  f"hands, surrounded on all sides by {GHOULS} closing in, while {ASH_KING} looms above and a vast "
  f"grey wave of frost rolls across the ruined temple floor, snuffing every spark. {STYLE}.")

j("az_6_rise", 666,
  f"{AZULON} rises among the {GHOULS}, his lunar tattoo beginning to blaze moon-white and pale "
  f"blue as arcs of silver light chase up his arms, the ruined temple colonnades catching the "
  f"glow, {ASH_KING} watching from the sky-sundial. {STYLE}.")

# BEAT 3 — THE SACRIFICE / VICTORY
j("az_7_shatter", 777,
  f"Climactic shot. {AZULON} shatters the lantern overhead and a blinding golden pillar of fire "
  f"erupts down through him, his outline white-hot, a shockwave ring of gold and moon-silver "
  f"racing outward that hurls back the massed {GHOULS} and ignites the cinders on {ASH_KING}, "
  f"who throws up his jagged arms. {STYLE}.")

j("az_8_fall", 888,
  f"{ASH_KING} crumbling apart and lifting upward as a column of burning embers like reversed "
  f"snow, his jagged crown dissolving into gold-lit cinders, while every remaining {GHOULS} "
  f"shivers into ash and the ruined temple is flooded with warm firelight. {STYLE}.")

j("az_9_aftermath", 999,
  f"Aftermath. The ash-fields now quiet, dawn warming the grey sky over the {SET}, and where "
  f"{AZULON} stood remains a single small steady golden flame burning in the ash, the silver "
  f"temple statues catching the first light. {STYLE}.")

out = os.path.join(STAGE, "azulon_jobs.json")
json.dump(jobs, open(out, "w"), indent=1)
print(json.dumps({"jobs": len(jobs), "file": out, "staged": sorted(os.listdir(STAGE))}, indent=1))
