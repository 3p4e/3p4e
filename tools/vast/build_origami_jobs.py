#!/usr/bin/env python3
"""Build origami_jobs.json for run_qwen_edit_full.py — ORIGAMI ASCENSION v4 (FIGHT).

SCRIPT:   higgsfield/17_ORIGAMI_FIGHT_v4_CONTINUITY.md  (supersedes 16_v3)
          12 beats, ~60s. Hero vs villain, spectacular mutual attack, vast release.

CONTINUITY IS ENFORCED HERE, NOT JUST DESCRIBED
  Every beat declares the state it ENTERS from and the state it LEAVES. A single
  STATE_CHAIN list is asserted end-to-end: out[i] must equal enter[i+1]. If someone
  edits a beat into a new tableau, the builder fails instead of rendering a jump cut.

  The six v3 defects this fixes (D1-D6, see the continuity doc):
    D1 wings never shatter  - cranes tear FREE, six wings remain, thinned.
    D2 blade -> colossus    - beat 07 explicitly unfolds FROM the blade.
    D3 sphere ignored       - beat 09 bursts OUT of the sphere.
    D4 "ultimate" loses     - beat 09 is not the kill; beat 12 is, via D4 fix:
    D4 CAUSAL SPINE         - beat 10 eats the blade storm, so the blades are
                              INSIDE it; beat 12 detonates them from within.
    D5 wall never resets    - beat 05 collapses the wall back into its wings.
    D6 size grows for free  - it grows by EATING his attacks (04, 10).

IDENTITY CONDITIONING (AZULON_CANON.md lesson 1)
  image1 is fed to TextEncodeQwenImageEditPlus as the FIRST edit reference, so image1
  alone can paste a face onto the render.
    monster()  image1 = seraph_ref.png, NO identity refs. Azulon absent from frame.
    hero()     image1 = A_bust.png + image2/3 refs. Azulon is the subject.
    clash()    BOTH. Anchored on Azulon; the prompt denies a human face on the Stain
               and the negative forbids a duplicate face.

PROMPT BUDGET (why the earlier sets came back "slop")
  run_qwen_edit_full.py passes NO max_length, so the Qwen 2.5-VL encoder truncates from
  the END - exactly where STYLE and density language sit. The sets that rendered well
  averaged 1084-1149 chars, peaking at 1496 (ashfall). MAX=1400 here, enforced.

Quality: Qwen-Image-Edit-2511 FP8, full 40-step schedule, cfg 3.0, no Lightning LoRA.
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REFS = os.path.join(ROOT, "media", "refs")
STAGE = os.path.join(ROOT, "tools", "vast", "jobs")
os.makedirs(STAGE, exist_ok=True)

MAX = 1400

for f in ("A_bust.png", "sheet_front.png"):
    src = os.path.join(REFS, f)
    if not os.path.exists(src):
        raise SystemExit(f"missing identity ref {src}")
    shutil.copy2(src, os.path.join(STAGE, f))

# The corrupted seraph's OWN visual reference (the user's original paper-seraph
# screenshot). NOT an identity ref - monster shots are conditioned on it instead of
# Azulon, so his face cannot enter through image1 either.
SERAPH_REF = "seraph_ref.png"
_src = os.path.join(REFS, SERAPH_REF)
if not os.path.exists(_src):
    raise SystemExit(f"missing seraph reference {_src}")
shutil.copy2(_src, os.path.join(STAGE, SERAPH_REF))

# ---- canon blocks (every canon fact kept, prose tight for the token budget) ----
AZULON = (
    "Azulon as a clean seraph, hairless shaven head, clean-shaven face with no moustache "
    "no beard and no stubble, eyebrows kept, grey-green eyes, very long high-elf ears "
    "sweeping back, lean wiry build, unretouched photographic skin, a faded silver Selune "
    "crescent on his forehead; from the neck down his armour and six wings are immaculate "
    "folded ivory parchment, visible paper fibre, every feather edge burning with a cold "
    "white flame that does not consume the paper"
)

STAIN_FULL = (
    "the corrupted seraph, a colossal parchment thing rotted from the wing edges inward, "
    "six ragged wings stained black whose edges drip glossy tar-like black goo in long "
    "strands that pool beneath it, dark tide-lines soaked along the folds where blackletter "
    "script smears and bleeds, too many wing joints, and a head that is a blank folded "
    "paper mask with NO human face and no eyes, only two dark holes weeping black"
)

STAIN_BRIEF = (
    "the corrupted seraph, a colossal parchment thing whose wing edges drip glossy black "
    "tar-goo and pool black beneath it, its head a blank folded paper mask with NO human "
    "face and no eyes, only two holes weeping black"
)

VOID = (
    "a starless black void bending under the released force, drifting loose parchment "
    "pages and dissolving blackletter fragments, faint cold white light far behind"
)

STYLE = (
    "Cinematic photorealistic film still, 16:9, dense maximalist composition filling the "
    "frame, soft key light from above, macro detail of paper fibre and wet tar, high "
    "contrast, shallow depth of field, ivory parchment against cold white flame and oily "
    "black corruption, volumetric light, ultra-detailed"
)

NEG = (
    "blurry, deformed face, distorted eyes, extra limbs, extra fingers, melted armour, "
    "cartoon, illustration, plastic skin, text, watermark, low quality, low resolution, "
    "different face, moustache, beard, stubble, human hair, earrings, modern clothing, "
    "empty flat background, lone figure, sparse composition, duplicate face, human face on "
    "the second figure, smiling, fire consuming paper, cropped by frame edge, static pose, "
    "new scene, restarting"
)

jobs = []


def add(tag, seed, kind, enter, out, prompt):
    row = {"tag": tag, "seed": seed, "prompt": prompt, "negative": NEG,
           "enter": enter, "out": out, "kind": kind}
    if kind == "monster":
        row["image1"] = SERAPH_REF
    else:  # hero and clash are both anchored on Azulon's identity
        row["image1"] = "A_bust.png"
        row["image2"] = "A_bust.png"
        row["image3"] = "sheet_front.png"
    jobs.append(row)


# ------------------------------------------------------------------ ACT 1
add("or_01_corruption_revealed", 800, "monster",
  "void_empty", "stain_revealed_dripping",
  f"Wide low angle. {STAIN_FULL} looms over a vast invisible plane in {VOID}, goo "
  f"dripping from six stained wing edges and pooling into a wide glossy black mirror "
  f"beneath it. No human figure. {STYLE}")

add("or_02_hunter_descends", 801, "hero",
  "stain_revealed_dripping", "hunter_above_wings_open",
  f"Dynamic wide shot. Above the dripping Stain, {AZULON} plummets out of the dark "
  f"trailing a searing white streak, wings snapping open as cold flame races every edge, "
  f"folded pages spiralling up around his raised hand. Far below, {STAIN_BRIEF} waits, "
  f"unimpressed. He does not slow. {VOID}. {STYLE}")

# ------------------------------------------------------------------ ACT 2
add("or_03_thousand_cranes", 802, "hero",
  "hunter_above_wings_open", "crane_swarm_descending_wings_ragged",
  f"Explosive wide shot, massive release of force. Still falling, {AZULON} fires his "
  f"opening attack: thousands of folded paper cranes tear free from his outstretched "
  f"wings, which stay six but are left ragged and thinned, and streak away as a comet "
  f"storm of white fire filling the frame with burning motion streaks and shockwave "
  f"rings. {VOID}. {STYLE}")

add("or_04_stain_devours", 803, "monster",
  "crane_swarm_descending_wings_ragged", "stain_cathedral_wall_swarm_eaten",
  f"Colossal wide shot. {STAIN_FULL} does not dodge - its wings UNFOLD into a cathedral "
  f"wall of stained parchment and swallow the incoming crane swarm whole, white fire "
  f"drowning in black glossy goo that brightens as it feeds; thick tar tentacles snatch "
  f"the last cranes mid-flight. It swells visibly larger, fed. {VOID}. {STYLE}")

add("or_05_tar_tide", 804, "clash",
  "stain_cathedral_wall_swarm_eaten", "tar_ocean_surging",
  f"Overwhelming wide shot, vast destructive release. The cathedral wall of {STAIN_BRIEF} "
  f"COLLAPSES back into its wings, and from them a tidal ocean of glossy black tar erupts "
  f"upward at {AZULON}, taller than a cathedral, goo screaming off its crest; he hangs "
  f"small and blazing white above it, six ragged wings spread, his flame reflected in the "
  f"oncoming slick, unfrightened. {STYLE}")

add("or_06_blade_splits_tide", 805, "hero",
  "tar_ocean_surging", "tide_cut_collapsing_hero_as_blade",
  f"Epic action shot. {AZULON} has re-folded himself into a single elongated blade of "
  f"ivory parchment and dives into the tar wave; the ocean of goo parts around him in a "
  f"deep canyon whose walls scream into white steam, his edges blazing cold white, the "
  f"whole tidal wall cut cleanly in half and collapsing on both sides behind him in "
  f"sheets of black spray. {VOID}. {STYLE}")

# ------------------------------------------------------------------ ACT 3
add("or_07_colossus_against_cathedral", 806, "clash",
  "tide_cut_collapsing_hero_as_blade", "both_colossal_facing",
  f"Titanic wide shot. {AZULON} UNFOLDS from the blade into a towering colossus of angular "
  f"ivory plates burning cold white, while {STAIN_BRIEF} unfolds into an ever-growing mass "
  f"of stained dripping pages dwarfing mountains; goo drips from one, white fire pours off "
  f"the other. {STYLE}")

add("or_08_sphere_of_annihilation", 807, "clash",
  "both_colossal_facing", "collision_sphere_burning",
  f"The largest release of force so far. The two titans slam together at frame centre and "
  f"white flame meets black tar in a blinding sphere of annihilation - a searing core with "
  f"concentric shockwave rings blasting outward, parchment pages shredded to confetti, "
  f"lens bloom, the void visibly bowing under the detonation. {AZULON} and {STAIN_BRIEF} "
  f"are locked as silhouettes inside the blast. {STYLE}")

add("or_09_thousandfold_dawn", 808, "hero",
  "collision_sphere_burning", "blade_storm_expanding",
  f"Azulon bursts OUT of that burning sphere - not a fresh attack but the continuation of "
  f"the collision. {AZULON} with all six wings detonating into uncountable folded paper "
  f"blades edged in cold white fire, thousands of burning edges spiralling outward in "
  f"every direction at once, a radial star of white light shredding the void as he "
  f"breaks free, his face lit from beneath. {STYLE}")

# ------------------------------------------------------------------ ACT 4
add("or_10_final_unfold", 809, "monster",
  "blade_storm_expanding", "stain_unfolded_blades_inside",
  f"Grotesque colossal shot. Cornered, {STAIN_FULL} unfolds COMPLETELY into a "
  f"cathedral-sized nest of stained pages and writhing black tar tentacles and EATS the "
  f"blade storm, swallowing it whole as fast as it arrives, swelling far beyond the frame "
  f"with black goo cascading off it in curtains - but the burning white blades are now "
  f"glowing faintly from INSIDE its body. No human figure. {VOID}. {STYLE}")

add("or_11_spear_pierce", 810, "hero",
  "stain_unfolded_blades_inside", "hole_punched_fire_igniting_inside",
  f"Decisive action shot. {AZULON} has compressed into a single folded white dart of pure "
  f"cold flame and dives straight through the gorged black mass; a thin perfect "
  f"pencil-line of white light punches in one side and out the other, the entry and exit "
  f"holes rimmed with burning white and spraying black vapour, and white fire already "
  f"glowing up inside the body it entered. Wings folded flat, eyes fixed. {VOID}. {STYLE}")

add("or_12_annihilation_ascension", 811, "clash",
  "hole_punched_fire_igniting_inside", "stain_destroyed_hero_lands_void_empty",
  f"Wide shot, the payoff. The swallowed blade storm DETONATES INSIDE it - white fire "
  f"erupts out through its body, {STAIN_BRIEF} burning from within as its tar boils to "
  f"vapour and its paper body crumbles into glowing dust and clean white cranes rise "
  f"through the wreckage; {AZULON} lands in the foreground, wings folding, edges smoking "
  f"white, lit by his enemy's dying fire. {STYLE}")

# ------------------------------------------------------------------ write
out = os.path.join(STAGE, "origami_jobs.json")
with open(out, "w") as fh:
    json.dump(jobs, fh, indent=2)

print(f"wrote {out}")
print(f"jobs: {len(jobs)}  cap: {MAX}")

# ---- continuity chain: out[i] must be enter[i+1] ----
for a, b in zip(jobs, jobs[1:]):
    assert a["out"] == b["enter"], (
        f"CONTINUITY BREAK between {a['tag']} and {b['tag']}: "
        f"{a['tag']} leaves '{a['out']}' but {b['tag']} enters from '{b['enter']}'")

# ---- per-shot gates ----
counts = {"hero": 0, "monster": 0, "clash": 0}
for r in jobs:
    counts[r["kind"]] += 1
    n = len(r["prompt"])
    anchored = r["kind"] in ("hero", "clash")
    hero_phrase = "no moustache" in r["prompt"]
    faceless = "NO human face" in r["prompt"] or "no human face" in r["prompt"]
    print(f"  {r['tag']:32s} {r['kind'].upper():7s} seed={r['seed']} "
          f"refs={len([k for k in ('image1','image2','image3') if k in r])} "
          f"hero_lock={hero_phrase} faceless={faceless} chars={n}")

    assert n <= MAX, f"{r['tag']} prompt {n} over cap {MAX} - the encoder would truncate STYLE"
    assert "moustache" in r["negative"]
    assert "duplicate face" in r["negative"]
    assert "restarting" in r["negative"], f"{r['tag']} must forbid restaging the scene"
    if r["kind"] == "monster":
        assert r["image1"] == SERAPH_REF, f"{r['tag']} monster must be conditioned on seraph_ref"
        assert not hero_phrase, f"{r['tag']} monster must not carry the hero identity lock"
        assert faceless, f"{r['tag']} monster must keep the faceless mask"
    else:
        assert r["image1"] == "A_bust.png", f"{r['tag']} must be anchored on Azulon"
        assert hero_phrase, f"{r['tag']} hero shot missing the clean-shaven lock"
        if r["kind"] == "clash":
            assert faceless, f"{r['tag']} clash must deny a human face on the Stain"

assert counts == {"hero": 5, "monster": 3, "clash": 4}, f"unexpected shot mix {counts}"
print(f"shot mix: {counts['hero']} hero / {counts['clash']} clash / {counts['monster']} monster")
print(f"continuity: {len(jobs)} beats chained, 0 breaks")
print("validation OK")
