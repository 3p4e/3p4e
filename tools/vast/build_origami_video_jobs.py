#!/usr/bin/env python3
"""Build v2_video_jobs.json for SkyReels-V2 Diffusion Forcing I2V render of the
Origami Ascension v5 fight (12 beats).

Supersedes the single generic `--prompt` embedded in v2_*.sh. Corrections applied
from 18_PROMPT_COMPOSITION_GUIDE.md §2 and 19_ORIGAMI_FIGHT_v5_VIDEO_PROMPTS.md:

  1. T2V -> I2V parameters: shift 8.0->5.0, guidance 6.0->5.0, steps 30->50.
  2. Every prompt DESCRIBES ITS SEED KEYFRAME (first-frame agreement) so text and
     anchor never contradict (the root cause of the $3 Azulon-seed failure).
  3. Camera grammar stated explicitly (V2's highest-scoring dimension).
  4. No --prompt_enhancer (over-saturates long prompts; needs 64G+ VRAM).
  5. Wrong-anchor gate: each beat's seed keyframe hash must NOT equal any Azulon
     identity reference; monster-only beats must NOT be conditioned on an Azulon
     hero frame. Enforced at render time, not just documented.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STAGE = os.path.join(ROOT, "tools", "vast", "jobs")
os.makedirs(STAGE, exist_ok=True)

# Canonical keyframe output dir (produced by run_qwen_edit_full.py for
# build_origami_jobs.py; these files must exist before the video render).
KF_DIR = os.path.join(ROOT, "media", "origami_keyframes")

# I2V parameters (official SkyReels-V2 values, see 18_PROMPT_COMPOSITION_GUIDE.md)
PARAMS = {
    "resolution": "540P",
    "num_frames": 97,      # per-clip chunk length for 540P
    "shift": 5.0,           # I2V (was 8.0 T2V)
    "guidance_scale": 5.0,  # I2V (was 6.0 T2V)
    "inference_steps": 50,  # official (was 30)
    "overlap_history": 17,
    "fps": 24,
    "prompt_enhancer": False,
}

# tag -> (kind, seed, keyframe_basename, prompt)
# kind: monster | hero | clash, matching the keyframe builder's conditioning.
BEATS = [
("or_01_corruption_revealed", "monster", 800,
 "The first frame shows a colossal seraph of folded parchment, six ragged wings dripping glossy black goo, its head a blank folded paper mask weeping black, looming in a starless void over a wide black mirror. The goo keeps dripping in long slow strands and the pooled mirror ripples; drifting parchment pages float past its wings. Camera: low-angle wide shot, very slow push-in. Its blank mask and six wings stay fixed."),
("or_02_hunter_descends", "hero", 801,
 "The first frame shows Azulon mid-descent, ivory wings snapping open with cold white flame racing every edge, folded pages around his raised hand, the Stain far below. He keeps plummeting, wings flaring, white flame streaking upward behind him. Camera: high-angle tracking shot descending with him. His clean-shaven face stays fixed."),
("or_03_thousand_cranes", "hero", 802,
 "The first frame shows Azulon with six ragged thinned wings firing thousands of folded paper cranes, each edged in cold white fire. The crane storm keeps streaking outward in a comet swarm, motion streaks and shockwave rings expanding across the frame. Camera: wide shot with a slight lateral track, swarm filling the frame."),
("or_04_stain_devours", "monster", 803,
 "The first frame shows the corrupted seraph's wings unfolded into a cathedral wall of stained parchment swallowing the incoming white crane swarm. The wall keeps expanding, tar tentacles snapping up the last cranes, goo brightening as it feeds. Camera: static colossal wide shot, slow steady push forward."),
("or_05_tar_tide", "clash", 804,
 "The first frame shows a tidal ocean of glossy black tar surging upward from the collapsed wings toward a small blazing white Azulon hanging above it. The wave keeps rising and rolling, goo screaming off its crest, his flame reflected in the slick. Camera: low angle, slow tilt up as the wave climbs. His white figure stays fixed."),
("or_06_blade_splits_tide", "hero", 805,
 "The first frame shows Azulon re-folded into a single ivory blade diving into the tar wave, the ocean parting around him in a deep steaming canyon. He keeps diving through, the canyon walls screaming to white steam and collapsing behind him in black spray. Camera: fast tracking shot following the blade through the parting wave."),
("or_07_colossus_against_cathedral", "clash", 806,
 "The first frame shows Azulon unfolded into a towering colossus of angular ivory plates facing an ever-growing mass of stained dripping pages. Both keep growing, goo dripping from one, white fire pouring off the other, the void shaking. Camera: extreme wide shot, slow crane upward revealing their scale."),
("or_08_sphere_of_annihilation", "clash", 807,
 "The first frame shows white flame and black tar locked in a blinding sphere at frame centre, both silhouettes inside it. Shockwave rings keep blasting outward, parchment shredding to confetti, lens bloom pulsing, the void bowing. Camera: locked wide shot with a subtle shake, very slow push toward the core."),
("or_09_thousandfold_dawn", "hero", 808,
 "The first frame shows Azulon bursting out of the burning sphere, all six wings detonating into uncountable paper blades in a radial star. The blades keep spiralling outward in every direction at once, the white star expanding as he breaks free. Camera: wide, gently rotating, fixed on the expanding radial storm."),
("or_10_final_unfold", "monster", 809,
 "The first frame shows the corrupted seraph unfolded into a cathedral nest of stained pages and tar tentacles, swallowing the blade storm, white blades glowing faintly inside it. The tentacles keep writhing, it swells, goo cascading off in curtains. Camera: slow push-in on the gorged mass."),
("or_11_spear_pierce", "hero", 810,
 "The first frame shows Azulon compressed into a single white dart punching a thin perfect line of light through the black mass. The line keeps piercing in one side and out the other, the holes rimmed white and spraying black vapour, white fire glowing up inside the body. Camera: fast tracking shot following the dart's path through the body."),
("or_12_annihilation_ascension", "clash", 811,
 "The first frame shows white fire erupting from inside the corrupted seraph, its body crumbling to glowing dust with clean white cranes rising, Azulon landing in the foreground. The body keeps crumbling outward, tar boiling to vapour, the dust cloud expanding as the cranes rise through the wreckage. Camera: wide, slow pull-back revealing the empty void."),
]

jobs = []
for tag, kind, seed, prompt in BEATS:
    kf = os.path.join(KF_DIR, tag + ".png")
    jobs.append({"tag": tag, "kind": kind, "seed": seed,
                 "keyframe": kf, "prompt": prompt, **PARAMS})

out = os.path.join(STAGE, "v2_video_jobs.json")
with open(out, "w") as fh:
    json.dump(jobs, fh, indent=2)

print(f"wrote {out}")
print(f"beats: {len(jobs)}")

# ---- gates ----
counts = {"monster": 0, "hero": 0, "clash": 0}
for r in jobs:
    counts[r["kind"]] += 1
    n = len(r["prompt"])
    assert n <= 600, f"{r['tag']} video prompt {n} > 600 (short-prompt rule)"
    assert "Camera:" in r["prompt"], f"{r['tag']} missing explicit camera grammar"
    assert "The first frame shows" in r["prompt"], f"{r['tag']} missing first-frame agreement"
    assert r["shift"] == 5.0 and r["guidance_scale"] == 5.0 and r["inference_steps"] == 50, \
        f"{r['tag']} I2V params wrong"
    assert not r["prompt_enhancer"], f"{r['tag']} must not enhance"
    print(f"  {r['tag']:32s} {r['kind'].upper():7s} seed={r['seed']} chars={n} I2V-params=ok")

assert counts == {"monster": 3, "hero": 5, "clash": 4}, f"unexpected mix {counts}"
print(f"mix: {counts['hero']} hero / {counts['clash']} clash / {counts['monster']} monster")
print("validation OK")
