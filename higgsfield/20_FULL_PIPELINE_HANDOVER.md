# VAST Film Project — Complete Pipeline Handover

> **Audience:** DeepSeek Harness on Windows laptop. This document is self-contained: a new session can read this alone and operate the full pipeline correctly.
> **Written:** 2026-11-04 CET
> **State:** covers the complete Origami Seraph fight video pipeline + all prior film work + all operating rules and discoveries.

---

## 0. What this project is

A generative-AI film studio run from an Agent Zero sandbox. Films are made from:

1. **Keyframes** — still images rendered from face-locked reference photos via **Qwen-Image-Edit-2511** (Apache-2.0).
2. **Video** — each keyframe animated into a ~4 s clip via **SkyReels-V2 Diffusion Forcing** (Skywork Community License, EU-legal) on a rented GPU.
3. **Assembly** — local ffmpeg concatenation of clips into a final film.

GPU compute is rented on **Vast.ai** on demand. All paid work requires an itemised cap agreed with the user first.

---

## 1. Live facts you MUST verify before acting (do not trust stale notes)

The operating rules are explicit about this — notes and handovers go stale. Always check these three things first, every session:

```bash
# 1. Current Vast.ai credit + active instances
#    API: GET https://console.vast.ai/api/v0/users/current/  (field: credit)
#         GET https://console.vast.ai/api/v0/instances/      (active vs exited)

# 2. Repository branch
cd /a0/usr/projects/vast && git status && git branch

# 3. The canonical media that exists
ls -la media/out_v3/ media/origami_keyframes/ media/v2_test/
```

Known instances that have existed (do NOT re-rent without checking live state):

| Contract | GPU | Fate |
|---|---|---|
| 59077464 | RTX 4090 48GB | keyframe render — DESTROYED after copy-verify |
| 59086740 | RTX 3090 24GB | origami video render — [status tracked below] |
| 59014386 | — | exited (stale, not billing) |

---

## 2. The current work-in-progress: Origami Seraph fight

### The story (canon v2)

A seraph of folded parchment **is the corruption**: black tar-like goo enters at the wing edges, drips in long strands, pools beneath, soaks dark tide-lines inward along the folds, smearing blackletter script. Six ragged wings, too many joints.

**Azulon is the sent seraph** — clean ivory parchment, cold white flame on every feather, long high-elf ears, clean-shaven, silver crescent on the forehead — sent to hunt and destroy the corruption.

This **reverses** the original BLOCK 3 (which wrongly made the paper seraph the hero). Canon files:
- `higgsfield/15_ORIGAMI_ASCENSION_v2_CANON.md` — story
- `higgsfield/16_ORIGAMI_SERAPH_FIGHT_v3_SCRIPT.md` — 12-beat fight structure
- `higgsfield/17_ORIGAMI_FIGHT_v4_CONTINUITY.md` — IN/OUT state per beat + causal spine
- `higgsfield/19_ORIGAMI_FIGHT_v5_VIDEO_PROMPTS.md` — per-beat I2V prompts

### The 12 beats (tag = seed map = 800..811)

| # | Tag | Kind | Content |
|---|---|---|---|
| 1 | or_01_corruption_revealed | monster | goo dripping from six stained wings |
| 2 | or_02_hunter_descends | hero | Azulon sees the stain, wings open |
| 3 | or_03_thousand_cranes | hero | wings shatter into fire-swarm |
| 4 | or_04_stain_devours | monster | eats the cranes → grows |
| 5 | or_05_tar_tide | hero | goo ocean → blade splits the tide |
| 6 | or_06_blade_splits_tide | hero | re-folds to a blade |
| 7 | or_07_colossus_against_cathedral | clash | colossus vs cathedral |
| 8 | or_08_sphere_of_annihilation | clash | shockshredding pages |
| 9 | or_09_thousandfold_dawn | hero | wings detonate into blades |
| 10 | or_10_final_unfold | monster | eats blade storm — blades now inside |
| 11 | or_11_spear_pierce | hero | compresses to dart, punches through |
| 12 | or_12_annihilation_ascension | clash | swallowed blades detonate inside |

### Current status (this session)

```
KEYFRAMES (12/12)  ✓ rendered on RTX 4090 @40 steps
                   ✓ media/origami_keyframes/or_01..or_12.png
                   ✓ sha256 verified local==remote
                   ✓ instance 59077464 DESTROYED

VIDEO (first pass)  ✓ or_07..or_12  (6 clips, ~18 min each @50 steps)

VIDEO (re-run)      ✓ or_01..or_06 re-rendered after config.json fix — all exit=0

VIDEO (correction)  ✓ or_01, or_04, or_08 re-rendered with fresh seeds 812/813/814
                    + strengthened motion prompts (motion +104%/+116%/+195%)

VIDEO (final)       ✓ 12/12 clips at media/vast11111/clips/  (corrected versions promoted)
                    ✓ assembled 48.5s film + sha256 verified
                    ✓ instance 59086740 DESTROYED (success:true)
```

---

## 3. The pipeline scripts (exact inventory)

### 3.1 Keyframe engine (Qwen-Image-Edit-2511)

| Script | Purpose |
|---|---|
| `tools/vast/rent_qwen.py` | rent RTX 4090 48GB for keyframes |
| `tools/vast/qwen_kf_run.sh` | setup: download 3 weights → start ComfyUI → node preflight → render |
| `tools/vast/run_qwen_edit_full.py` | the ComfyUI graph runner (full 40-step, no Lightning LoRA) |
| `tools/vast/build_origami_jobs.py` | emits 12-beat keyframe job manifest |
| `tools/vast/jobs/origami_jobs.json` | the 12 keyframe jobs |

Weights (all Apache-2.0, fetched from HuggingFace):
```
Comfy-Org/Qwen-Image-Edit_ComfyUI  split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors
Comfy-Org/Qwen-Image_ComfyUI       split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
Comfy-Org/Qwen-Image_ComfyUI       split_files/vae/qwen_image_vae.safetensors
```

### 3.2 Video engine (SkyReels-V2 Diffusion Forcing)

| Script | Purpose |
|---|---|
| `tools/vast/rent_v2.py` | rent RTX 3090 24GB for video (refuses double-rent, caps price) |
| `tools/vast/v2_origami_setup.sh` | deps → repo → flash-attn → model fetch → render |
| `tools/vast/v2_render_origami.sh` | per-beat I2V driver with wrong-anchor gate |
| `tools/vast/v2_verify_render.sh` | verify weights (hardcoded sizes) + launch render |
| `tools/vast/v2_fetch_small.sh` | fetch config.json + tokenizer files |
| `tools/vast/v2_repair_dl.sh` | (superseded — had a size-compare bug) |
| `tools/vast/jobs/v2_video_jobs.json` | 12 per-beat video jobs |

Weights (Skywork Community License, EU-legal):
```
Skywork/SkyReels-V2-DF-1.3B-540P
  model.safetensors                 = 5,742,186,488 bytes
  Wan2.1_VAE.pth                    =   507,609,880 bytes
  models_t5_umt5-xxl-enc-bf16.pth   = 11,361,920,418 bytes
  + config.json + google/umt5-xxl/ tokenizer files
```

---

## 4. The critical correctness rules (each learned from a real failure)

These are the highest-value discoveries. They MUST be honoured or the pipeline silently produces wrong output.

### 4.1 Wrong-anchor gate (THE big one)

A video render must be conditioned on the correct seed image. The failure: a render was seeded with `tools/vast/seed.png`, which was byte-identical (`sha256 7f9381d8...`) to `media/azulon_keyframes/az_2_hero.png` — an **Azulon** hero frame — while the prompt asked for the corrupted paper seraph. The image anchor won; text was ignored. Result: a "rubbish" 15s video with nothing to do with the seraph.

**Rule:** before ANY video render, print the sha256 of the seed and prove it is the intended keyframe, not an identity ref. The driver enforces this: monster beats must not use an Azulon ref as seed.

### 4.2 First-frame agreement (SkyReels V2 I2V)

The prompt for I2V must **describe the first-frame image itself**, then add motion + camera.

```
GOOD: "The first frame shows {exact keyframe}. {motion}. Camera: {grammar}."
BAD:  "A corrupted seraph hovers..." (text contradicts the anchor)
```

### 4.3 Corrected I2V parameters (were wrong as T2V leftovers)

```
          official I2V   wrong values previously used
shift           5.0       8.0
guidance_scale  5.0       6.0
inference_steps 50        30
```

### 4.4 Qwen prompt truncation (≤1400 chars, identity early)

The Qwen 2.5-VL encoder truncates long captions **from the end** (no max_length passed). Trailing "volumetric light, ultra detailed" was being silently eaten. Rule: **≤1400 chars**, identity+action early, density in the middle. Best renders clustered ~1100 chars.

### 4.5 Composition density (anti-slop)

Sparse single-figure frames = "slop". Every prompt must spec foreground/midground/background. Never "lone figure in an empty void."

### 4.6 Copy-before-destroy

Copy + sha256-verify every artifact off the instance BEFORE destroying it. A prior run destroyed a rendered clip during a copy-in-flight.

### 4.7 Teardown discipline (idle billing)

Idle GPU time is money: a finished render was left running ~8h, costing ~$1.60 idle. Rule: destroy the instance **immediately** after copy-verify, and confirm zero billing after.

### 4.8 Model download speed (HF throttling)

HuggingFace serves at 2-4 MB/s regardless of the instance's advertised link. The 11 GB encoder took ~40 min. Use `aria2c -x16 -s16 -c` for multi-connection resume. **Do NOT pass multiple URLs with multiple `-o` in one aria2c invocation — the files collide/corrupt.**

### 4.9 Config.json is a hard dependency

The SkyReels pipeline fails with `OSError: ...config.json is not the path to a directory` if the small files (config.json + google/umt5-xxl tokenizer files) are missing. The big weights are not enough.

---

## 5. The complete failure ledger (this session + prior)

| # | Failure | Root cause | Fix |
|---|---|---|---|
| 1 | 4s clip instead of 15.7s | regex matched main `--num_frames` instead of chunk flag | discover chunk flag from source, hard-fail on bare flag |
| 2 | rendered clip was Azulon, not seraph | seed.png == az_2_hero.png (wrong anchor) | wrong-anchor gate + sha256 proof |
| 3 | no output, instance killed mid-run | leaked self-stop watchdog from earlier failed launches | no in-instance watchdog; host controls teardown |
| 4 | render crash on config.json | small files never fetched (setup killed earlier) | fetch_small.sh + verify |
| 5 | aria2c file collision | multi-URL single-invocation with two -o flags | separate aria2c per file |
| 6 | corrupt copy of a clip mid-write | copied before write completed | copy-verify-before-destroy |

---

## 6. Cost ledger (verified against Vast API)

```
keyframe rental  59077464 (RTX 4090 48GB, $0.670/h)   → DESTROYED after copy-verify
video rental     59086740 (RTX 3090 24GB, $0.256/h)   → DESTROYED success:true
final credit                                        = $9.9276 (2026-11-04 18:15 CET)
remaining instances                                 = 59014386 exited (stale, not billing)
```

Final deliverable:
```
media/vast11111/origami_seraph_fight_540p.mp4
  544×960 · 24 fps · 1164 frames (12 × 97) · 48.5 s · 82.4 MB
  sha256 58bb5c2ab1acaceb4a741d216f4fc8e2146db531ab19643ab5086529f29b5d1d
```

---

## 7. How to continue (recovery runbook)

### To re-render any keyframe set
```bash
cd /a0/usr/projects/vast/tools/vast
# 1. rent
VASTAI_API=... MAXPRICE=0.75 /opt/venv/bin/python rent_qwen.py
# 2. deploy jobs + refs + runner
# 3. launch qwen_kf_run.sh
```

### To re-render video (SkyReels V2)
```bash
VASTAI_API=... MAXPRICE=0.45 /opt/venv/bin/python rent_v2.py
# scp 12 keyframes → /workspace/origami_keyframes/
# scp A_bust.png sheet_front.png v2_video_jobs.json v2_render_origami.sh v2_origami_setup.sh
# launch setup (it fetches everything), then render
```

### To assemble the film
```bash
# local ffmpeg concat of the 12 clips in beat order
/opt/venv/bin/python tools/vast/assemble_film.py   # (or ffmpeg concat demuxer)
```

---

## 8. Broader project state (verified inventory)

### Finished films
- **Karsus's Folly v3** — 118.0s 720p film (`media/out_v3/karsus_v3_FULL.mp4`), Wan 2.2 14B I2V, 24/25 clips.
- **The Paladin's Judgement v3** — 22.6s 1080p teaser (`media/paladin_v3/film/`), Kandinsky 6.0 + VSR.

### Scenario status (stills / video)
```
Karsus's Folly        100%  (complete film)
Paladin v3             50%  (teaser only)
Azulon battle          50%  (9 stills, 0 video)
ASHFALL                50%  (9 stills, 0 video)
Paladin keyframes v4   50%  (6 stills, 0 video)
Origami Ascension      50%  (12 stills, video in progress)
The Remembering         0%  (doc only)
Lunar Purge             0%  (doc only)
Gleipnir                0%  (doc only)
```

### Face cards / identity
- Oleg: enrolled (31 faces, centroid.npz) ✓
- Geni: NOT recoverable (source crops 14-116px, below 256px min) — needs real photos
- Kory: awaiting photos + consent
- Multi-identity refactor done: `tools/face_separate.py`, `faces/identity_index.json`

### Identity lock (Azulon canon)
- Clean-shaven (no moustache/beard/stubble — stale "ginger-brown moustache" canon was removed)
- Long high-elf ears, silver crescent on forehead
- Locked to `media/refs/A_bust.png` + `media/refs/sheet_front.png`

---

## 9. License / EU-legal status

| Model | License | Verdict |
|---|---|---|
| Qwen-Image-Edit-2511 | Apache-2.0 | ✓ real |
| SkyReels-V2 DF 1.3B | Skywork Community License | ✓ EU-legal, worldwide |
| SkyReels-V3 R2V-14B | Skywork Community License | ✓ EU-legal |
| HunyuanVideo 1.5 | restricted | ✗ FORBIDDEN — excludes EU/UK/SK |
| LTX-2.3 | personal non-commercial | ✓ fallback (ungated) |
| LTX-2.5 | — | gated (access 403) |
| Kandinsky 6.0 Lite | MIT | ✓ real (used for teaser) |
| OpenMontage | AGPL-3.0 | ⚠ framework not model, copyleft caution |

---

## 10. Env / credentials (names only, never values)

```
VASTAI_API                    → account credit + instance ops
root/.ssh/vast_karsus(.pub)   → Vast instance SSH
HF_TOKEN                      → public downloads need no token
KVM4_RUNNER_URL/TOKEN         → Hostinger relay (token went stale before; see runbook)
```

---

## 11. Status — COMPLETE (all phases executed)

The full chain the user authorized is now finished and verified:

1. ✓ 12/12 keyframes rendered on RTX 4090 (full 40-step) + sha256 verified + instance 59077464 destroyed
2. ✓ 12/12 video beats rendered on RTX 3090 (SkyReels-V2 DF, I2V-correct params) — first pass + re-run of the 6 that failed pre-config-fix
3. ✓ 3 weak beats (or_01/or_04/or_08) re-rendered with fresh seeds (812/813/814) + strengthened motion prompts — on the warm instance, then re-verified home before teardown
4. ✓ Motion verification after correction: or_01 +104%, or_04 +116%, or_08 +195% (mean abs frame-diff); monster beats re-checked faceless (0 faces)
5. ✓ 12 clips copied home + sha256, corrected versions promoted; assembled 48.5 s film (1164 frames @ 24 fps)
6. ✓ Instance 59086740 destroyed (success:true); final credit $9.9276

### Closed failure modes this session (the ones that cost money/reruns before)
- Leaked self-stop watchdog killing a render mid-run → no in-instance watchdog, host controls teardown
- config.json/tokenizer missing → hard dependency enforced in setup
- Wrong-anchor (Azulon face seeded a monster beat) → sha256 wrong-anchor gate + verified the seeded file before render
- 4 s clip instead of 15.7 s → chunk-flag discovery (never bare --num_frames)
- Truncated 8.75 MB transfer (moov atom missing) → verify size + md5 before accepting any copy

### Final handover artifacts
- `higgsfield/20_FULL_PIPELINE_HANDOVER.md` — this document
- `media/vast11111/origami_seraph_fight_540p.mp4` — the complete 48.5 s film
- `media/vast11111/keyframes/` — 12 keyframes
- `media/vast11111/clips/` — 12 canonical clips (+ *_v1 superseded originals)
- `media/vast11111/seraph_ref.png` — the canonical corrupted-seraph reference

### Canonical film deliverable
```
origami_seraph_fight_540p.mp4
  544×960 · 24 fps · 1164 frames (12 × 97) · 48.5 s · 82.4 MB
  sha256 58bb5c2ab1acaceb4a741d216f4fc8e2146db531ab19643ab5086529f29b5d1d
```
