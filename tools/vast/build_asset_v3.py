#!/usr/bin/env python3
"""Build corrected asset jobs (v3) from the director's 2026-11-07 verdicts.

STAGE 1 (no new deps): crossbow_v3, greatsword_v1, boss_v3, loc_v2,
                        dd_fused_glacier_v2
STAGE 2 (needs stage-1 output): dd_turnaround_v2 (dd master v2),
                        az_*_w re-issues (conditioned on greatsword sheet)
"""
import json

APPEAR = ("Appearance, texture and color reference ONLY; ignore the reference's "
          "background and lighting. Grey studio background never appears in output.")

WEAPON_FMT = ("Orthographic multi-view weapon reference sheet on a plain neutral grey "
              "studio background, soft even lighting, weapon rendered full-frame and "
              "centered in each view, consistent scale across views, no hands, no "
              "person, no text, no watermark. Views arranged in a 2x3 grid: (1) front "
              "three-quarter view, (2) side profile, (3) top view, (4) rear "
              "three-quarter view, (5) detail close-up of the weapon head, (6) detail "
              "close-up of the grip.")

FIREARM_NEG = ("firearm, gun, machinegun, Uzi, SMG, barrel, magazine, ammo clip, "
               "muzzle, gun stock, modern weapon, blurry, deformed, text, watermark, "
               "low quality")

DEFAULT_NEG = ("blurry, deformed face, distorted eyes, extra limbs, extra fingers, "
               "melted or smudged armour, cartoon, illustration, plastic skin, text, "
               "watermark, low quality, different person, wrong identity")

STAGE1 = [
 {
  "tag": "crossbow_sheet_v3",
  "refs": [],
  "prompt": ("Legendary fantasy HAND CROSSBOW weapon reference sheet: a matched TWIN PAIR "
             "of compact hand crossbows for a demon hunter. Pistol-grip hand crossbows "
             "with a curved bow limb of translucent ice-blue arcane crystal glowing "
             "teal-blue from within; slender dark steel body with engraved frost runes; "
             "bowstring is a line of frozen pale-blue light; faint frost mist curls off "
             "the limbs; matching pair, mirror-imaged left and right. This is a "
             "medieval-fantasy hand crossbow strung with a bowstring that fires bolts — "
             "NO barrel, NO magazine, NO gun parts of any kind. " + WEAPON_FMT),
  "negative": FIREARM_NEG, "steps": 50, "seed": 8301, "stage": 1,
 },
 {
  "tag": "greatsword_sheet_v1",
  "refs": [],
  "prompt": ("Legendary fantasy TWO-HANDED GREATSWORD weapon reference sheet: a massive "
             "retribution-paladin greatsword, blade of pale sunsteel with a broad "
             "fuller, molten-gold runes glowing and running the full length of the "
             "blade, the edge wreathed in soft golden holy fire; a sunburst crossguard "
             "of gold and steel; a long two-handed grip wrapped in dark leather with a "
             "gold pommel; faint golden light aura around the whole weapon. Oversized "
             "heroic scale, clearly a two-handed sword, no firearm parts. " + WEAPON_FMT),
  "negative": FIREARM_NEG, "steps": 50, "seed": 8302, "stage": 1,
 },
 {
  "tag": "boss_sheet_v3",
  "refs": [],
  "prompt": ("Full-body character reference sheet of an epic fantasy demon boss on a plain "
             "grey studio background: a colossal molten-forge demon. His face is a "
             "prolific molten-lava face — a skull-like visage of cracked black volcanic "
             "crust over blinding molten lava, lava dripping and running down the face "
             "and body everywhere, drops of molten rock falling from his jaw and "
             "shoulders to the ground, small fires where the drops land. Massive "
             "obsidian-plated shoulders, one arm ending in a long molten whip-crack of "
             "living lava. Front three-quarter and back views side by side, consistent "
             "design across views, full-frame, game-cinematic concept-art quality, "
             "photoreal materials, no text, no watermark."),
  "negative": DEFAULT_NEG, "steps": 50, "seed": 8303, "stage": 1,
 },
 {
  "tag": "loc_canyon_plate_v2",
  "refs": [],
  "prompt": ("Epic fantasy environment establishing shot: a vast basalt canyon gorge at "
             "late golden afternoon, bright and clearly readable exposure — deep shadows "
             "but luminous highlights, sun striking the canyon rim, drifting ash motes "
             "glowing in the light, scorched ground with cooling lava veins far below, "
             "ruined stone bridge spanning the gorge in the mid-distance. Cinematic "
             "wide composition, subjects silhouette-readable at thumbnail size, "
             "photoreal, high dynamic range, no murk-dark grade, no text."),
  "negative": "too dark, murky, underexposed, pitch black, muddy shadows, text, watermark",
  "steps": 50, "seed": 8304, "stage": 1,
 },
 {
  "tag": "dd_fused_glacier_v2",
  "refs": ["dd_look_glacier_v3.png", "ddface_a.jpg"],
  "prompt": ("Full-body character reference sheet of a fantasy demon hunter woman on a plain "
             "grey studio background: she wears the glacier-blue arcane combat outfit — "
             "fitted ice-blue and dark leather armour, twin hand crossbows of ice-blue "
             "crystal held at her sides. The character from image 1 keeps the exact same "
             "outfit, armour, weapons, and palette; the face from image 2 is her face. "
             "CRITICAL: her head is completely BARE — no helmet, no hood, no bandana, no "
             "mask, nothing on her head or face; a loose hood hangs as a BACK PIECE only, "
             "draped over her shoulders and back like a cowl. Her teal-to-blue hair is "
             "fully visible, glowing softly and waving weightlessly as if underwater. "
             "Front and back views, consistent across views, photoreal, no text. " + APPEAR),
  "negative": ("helmet, hood on head, headwear, bandana, mask, head covering, "
               + DEFAULT_NEG), "steps": 50, "seed": 8305, "stage": 1,
 },
]

STAGE2 = [
 {
  "tag": "dd_turnaround_v2",
  "refs": ["dd_fused_glacier_v2.png"],
  "prompt": ("Four-view character turnaround sheet of the exact same fantasy demon hunter "
             "from image 1, on a plain grey studio background: front view, back view, "
             "left profile, right profile, consistent design and palette across all four "
             "views, full body, consistent scale. Her head remains completely BARE — no "
             "helmet, no hood on the head; the cowl stays on her back; her glowing "
             "teal-to-blue underwater-wave hair fully visible from every angle. Twin "
             "ice-crystal hand crossbows on her back and in hand. Photoreal, no text. "
             + APPEAR),
  "negative": ("helmet, hood on head, headwear, bandana, mask, " + DEFAULT_NEG),
  "steps": 50, "seed": 8306, "stage": 2,
 },
 {
  "tag": "az_fused_idle_w",
  "refs": ["az_fused_idle.png", "greatsword_sheet_v1.png"],
  "prompt": ("Full-body character reference sheet of a fantasy retribution paladin on a "
             "plain grey studio background: the EXACT same paladin from image 1 — same "
             "face, same armour — now HOLDING the legendary two-handed greatsword from "
             "image 2 planted upright beside him, one gauntleted hand resting on its "
             "pommel, molten-gold runes glowing along the blade. Front view, full body, "
             "photoreal, no text. " + APPEAR),
  "negative": DEFAULT_NEG, "steps": 50, "seed": 8307, "stage": 2,
 },
 {
  "tag": "az_fused_wrath_w",
  "refs": ["az_fused_wrath.png", "greatsword_sheet_v1.png"],
  "prompt": ("Full-body character reference sheet of a fantasy retribution paladin in his "
             "wrath state on a plain grey studio background: the EXACT same paladin from "
             "image 1 — same face, same armour, gold rune tattoo blazing — now WIELDING "
             "the legendary two-handed greatsword from image 2 raised in both hands, "
             "molten-gold runes on the blade surging in sync with his tattoo. Front "
             "three-quarter view, full body, photoreal, no text. " + APPEAR),
  "negative": DEFAULT_NEG, "steps": 50, "seed": 8308, "stage": 2,
 },
 {
  "tag": "az_turnaround_w",
  "refs": ["az_fused_wrath_w.png"],
  "prompt": ("Four-view character turnaround sheet of the exact same wrath-state paladin "
             "from image 1 holding his legendary two-handed greatsword, on a plain grey "
             "studio background: front, back, left profile, right profile, consistent "
             "armour, tattoo, and sword across all four views, full body, consistent "
             "scale, photoreal, no text. " + APPEAR),
  "negative": DEFAULT_NEG, "steps": 50, "seed": 8309, "stage": 2,
 },
]

jobs = STAGE1 + STAGE2
for i, j in enumerate(jobs):
    j.update({"id": j["tag"], "width": 1024, "height": 1024, "cfg": 4.0})

json.dump(STAGE1, open("tools/vast/jobfiles/asset_v3_stage1.json", "w"), indent=1)
json.dump(STAGE2, open("tools/vast/jobfiles/asset_v3_stage2.json", "w"), indent=1)

for f in ("tools/vast/jobfiles/asset_v3_stage1.json", "tools/vast/jobfiles/asset_v3_stage2.json"):
    arr = json.load(open(f))
    assert all(j["seed"] and j["prompt"] for j in arr)
    print(f, len(arr), "jobs OK; max chars:", max(len(j["prompt"]) for j in arr))
print("refs needed stage1:", sorted({r for j in STAGE1 for r in j["refs"]}))
print("refs needed stage2:", sorted({r for j in STAGE2 for r in j["refs"]}))