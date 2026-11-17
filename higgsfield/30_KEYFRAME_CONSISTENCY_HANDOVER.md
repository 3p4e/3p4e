# KEYFRAME CONSISTENCY — COMPLETE HANDOVER & CORRECTION ORDER

> Status: **HALTED — CORRECTION IN PROGRESS**  
> Generated: 2026-11-06 23:27 CET  
> Project: VAST — Demon Hunter + Paladin boss-fight cinematic  
> Vast.ai credit: **$14.7425**  
> Instances: **0 (all destroyed)**  
> This document is self-contained. Give it to any agent or platform to continue the work.

---

## 1. WHAT THIS PROJECT IS

A ~2-minute, photoreal, Macedonian-language boss-fight cinematic.

- **Hero 1 — DD ("Demon Hunter")**: dual-crossbow hunter, cold/arcane theme, glowing underwater-wave hair, Immortal-style wings.
- **Hero 2 — Azulon (body) / Blagoj (face)**: greatsword Retribution Paladin, gold rune tattoo that surges with each ability.
- **Boss — Mal'garot ("Lord of Ash")**: faceless, forge-core, molten whip-arm. **Must remain faceless.**
- **Scale**: 50 shots (start/end frame each → 100 keyframes → 50 FLF video clips).
- **Look**: photoreal. Stylised/game-art is rejected. (Known unresolved risk — see §7.)

Canonical spec: `higgsfield/26_DEMONHUNTER_PALADIN_BOSSFIGHT_SPEC_v2.md`  
Master spec: `higgsfield/27_DEMONHUNTER_PALADIN_MASTER_SPEC.md`

---

## 2. THE CORE LESSON (READ THIS FIRST)

**Text descriptions do NOT lock anything. Only reference IMAGES lock identity, costume, weapons, and markings.**

Every keyframe failure we hit came from one architectural error:

```
WHAT WE DID     fed text prompts describing weapons/costume/tattoo,
                plus TINY FACE CROPS as images

WHAT WAS NEEDED locked full-figure REFERENCE IMAGES for every recurring
                asset: hero look, weapons, hood state, tattoo, boss
```

Consequences observed (all diagnosed, confirmed by user):

| Symptom | Root cause | Fix |
|---|---|---|
| Weapons vary / merge into blobs | crossbows described in text only | locked **weapon prop sheet** reference |
| Paladin tattoo changes randomly per frame | tattoo is text, not baked image | bake it into locked **full-figure character card** |
| Hood appears, then disappears | wardrobe state in text only | separate **hooded vs bare** reference states |
| Faces fail / drift | weak ref (tiny crop) + too many text anchors | clean reference + **3–5 geometric anchors max** |
| Boss drifts badly | **no boss reference card at all** | build locked **Mal'garot look card** |

This maps one-to-one onto Higgsfield's official methodology — see §6.

---

## 3. WHAT IS PROVEN AND WORKING (DO NOT RE-TEST)

These were measured and verified. Treat them as settled.

### 3.1 First-Last-Frame (FLF) video chain — WORKS

- Model: **Wan2.1-FLF2V-14B-720P** (Apache-2.0, open, EU-legal).
- Node: `WanFirstLastFrameToVideo` (start image + end image → 5s interpolated clip).
- fp8 weights total ≈ **23.4 GB** (UNet 16.40G + umt5-xxl 6.74G + VAE 0.25G).

### 3.2 Step-count measurement — SETTLED AT 8 STEPS

| Config | Time/clip | Mean motion (frame-diff) | Verdict |
|---|---|---|---|
| 20-step fp8 | 28:33 | 14.83 | strong, unaffordable |
| **8-step fp8** | **15:15** | **14.20** | **96% motion at 53% time — PRODUCTION SETTING** |
| 4-step + LoRA | 3:13 | 6.42 | motion collapsed + face smear — REJECTED |

8-step output: 16fps · 81 frames · 5.06s · 1280×720 · h264 · zero static frames.

### 3.3 Blocking / staging — FIXED AND VERIFIED

`higgsfield/28_BLOCKING_AND_STAGING_LAW.md` — the mandatory geometric preamble injected into every prompt:

- 3/4 side camera, off-axis framing (not frontal poster pose).
- Bodies oriented INTO the fight; weapons aimed at the threat.
- Converging sightlines between hero and boss.
- Fix confirmed visually: bodies no longer squared to camera; no "backs to the boss".

The winning example frame is **`media/dhpf_proof_v2/proof_s19_end.png`** — off-axis three-quarter pose, converging sightlines. Use it as the staging reference.

### 3.4 8-step face-melt trade-off — MEASURED AND HONEST

- 8-step: 96% of 20-step motion, occasional mid-clip face softening (1–2 frames at peak motion).
- 20-step: no melt but 2× cost.
- Accept the trade at $0.166/clip, or pay $0.28/clip for 20-step. **Decision pending.**

---

## 4. THE FAILURE BEING CORRECTED (CURRENT BLOCKER)

**The 100-keyframe batch produced rubbish.** All keyframes were stopped and the instances destroyed.

Defects (user-confirmed):
1. Weapons differ from pair to pair; weapon merges = slop.
2. Paladin tattoo random per frame.
3. Hunter hood appears then disappears.
4. Faces fail.

**Root cause:** renderer fed only **face crops** (`dhpf_refs/`) as image references, leaving weapon/costume/tattoo/boss to free text.

Only 14/100 keyframes were rendered before the kill. They are **NOT to be used as film frames** — they are evidence of the failure. See §8 for their path.

---

## 5. THE FIX — WHAT MUST CHANGE

### 5.1 Renderer rewiring (THE critical change)

File: `tools/vast/run_kf_batch.py`

```
BEFORE (wrong):  reference = [face_crop] only
AFTER (correct): reference = [full-figure look card] + [face crop]
                 boss-only shots: reference = [Mal'garot look card] ONLY
```

Per job:
- Hero shot → **look card (image1) + face card (image2)** = weapon+hood+tattoo locked AND identity strong.
- Boss shot → **boss look card** as image1, NO hero face refs (no face-leak on faceless boss).

### 5.2 Prompt hygiene (Higgsfield rules)

1. **3–5 geometric anchors max** per prompt — not a wall of text (overloaded text makes the model choose motion over identity).
2. Add the appearance-only scope clause verbatim:
   > "Appearance, texture and color reference ONLY; ignore the reference's background and lighting."
3. Change **one variable at a time** — multi-variable changes cause identity drift.
4. Erase faces from all but ONE view on any reference sheet — multiple faces confuse the tracker.

### 5.3 Assets that ALREADY EXIST (use them, do not rebuild)

Full-figure look cards with CORRECT weapons/armour/tattoo — built and verified earlier:

```
media/dhpf_looks/dd_look_idle.png          DD — twin crossbows, hood correct
media/dhpf_looks/dd_look_glacier_v3.png    DD — glacier state, TWO crossbows (fixed)
media/dhpf_looks/az_look_idle.png          Azulon idle armour
media/dhpf_looks/az_look_wrath_v2.png      Azulon — gold rune tattoo CONFIRMED
```

Face crops (identity anchors):

```
media/dhpf_refs/ddface_a.jpg, ddface_b.jpg
media/dhpf_refs/azface_a.jpg, azface_b.jpg
```

### 5.4 Assets that are MISSING and MUST be built (ordered)

1. **Crossbow prop sheet** — lateral + 3/4 view, NO hand/figure, on grey background. This is the weapon that keeps merging. Highest priority.
2. **Mal'garot boss look card** — faceless, forge-core body, molten whip-arm, grey-background character sheet. Boss has drifted reference-less the whole project.

Both are two quick Qwen-Image renders (~$0.05 each) on the next rental.

### 5.5 Asset sourcing strategy — NOT everything must be generated (USER RULE)

Reference assets split into two classes by what they must do:

```
CLASS A — SOURCE FROM THE INTERNET (prefer real photos)
  props, weapons, armour materials, textures, surfaces, environments,
  lighting, atmosphere, debris, terrain
  → real photographs are BETTER than generated art here, because they
    drag the output toward photorealism (our unresolved risk, §7)

CLASS B — GENERATE / ENROL OURSELVES (must match locked identity)
  character faces, the specific hero looks, the specific boss design,
  anything that must be CONSISTENT with an enrolled identity
  → these must come from our gated pipeline, never the internet
```

Examples applied to our missing assets:

```
Crossbow prop sheet → CLASS A: source real photos of equivalent
  hand crossbows / arbalests for structure + a generated sheet for
  the exact fantasy form
Mal'garot boss      → CLASS B: generate (it must be OUR faceless
  forge-core design, not a found demon image)
Charred canyon / ash environment → CLASS A: real volcanic/ember
  photography references
```

**Licensing (mandatory for monetization):** internet-sourced references
must be CC0 / public-domain / CC-BY with attribution recorded. The VAST
stack is EU-legal Apache-2.0 everywhere; a copyrighted reference image
baked into a commercial film reintroduces the exact legal risk the
project has been engineered to avoid. Record source + license in
`asset_registry.json` for every fetched asset.

---

## 6. HIGGSFIELD METHODOLOGY (LEARNED FROM OFFICIAL SOURCES)

Read and saved locally:

```
higgsfield/research/elements_and_consistency.md
higgsfield/research/keep_characters_consistent.html
higgsfield/research/persona_consistent_popcorn.html
```

Distilled rules:

1. **Elements library**: build each recurring asset once as a named, frozen image; attach it to every generation that uses it. Text is not a lock.
2. **Persistent identity**: one clean reference + `@ElementName` exact references.
3. **Wardrobe states**: separate frozen images per state (hooded / bare / wrath / idle).
4. **Prop sheets**: separate reference per weapon/object.
5. **Grey-background sheets**: no distracting scene context in reference images.
6. **Erase duplicate faces**: one face per sheet view.
7. **3–5 anchored positions**: schematic position locks, not prose.
8. **Appearance-only scoping**: explicit "ignore background/lighting" clause in every prompt.
9. **Asset-first workflow**: build all Elements before generating any scene.

---

## 7. KNOWN UNRESOLVED RISK — PHOTOREALISM

**Six+ rounds, three models, aggressive prompts — every still is stylised high-fantasy art, not photoreal.** This has NOT moved.

Options if photoreal remains mandatory:
1. Photo-bashing real textures into keyframes.
2. Real-photo style-transfer pass.
3. Accept stylised cinematic look (explicit user sign-off required).
4. A different keyframe model.

**Rule: prove photorealism on ONE still before any batch.** Do not scale a look the user has rejected.

---

## 8. ASSET INVENTORY (EXACT PATHS)

### Rejected keyframes (evidence only, not usable)
```
media/dhpf_keyframes/kf_01_start.png … kf_03_end.png   (6 of 100 + partials)
```

### Proven proof artifacts
```
media/dhpf_proof_v2/proof_s19_start.png, proof_s19_end.png   ← staging reference
media/dhpf_proof_v2/flf_8step_base.mp4                       ← 8-step proof clip
media/dhpf_proof_v2/sheet_8step.png                          ← 17-frame strip
media/dhpf_proof/s19_flf_20step.mp4, s19_flf_4step_lora.mp4
```

### Look cards (CORRECT — use as references)
```
media/dhpf_looks/ (6 files + SHA256SUMS.txt)
media/dhpf_gate/  (gate_*.png identity-gate crops)
media/dhpf_refs/  (ddface_a/b, azface_a/b)
```

### Keyframe prompt pack (pre-correction — REGENERATE after rewire)
```
higgsfield/29_KEYFRAME_PROMPT_PACK.md
```

---

## 9. CORRECTION ORDER (EXECUTE IN THIS SEQUENCE)

All authoring steps are zero-cost. Only the renders cost money.

```
STEP 1  (free)   Rewire tools/vast/run_kf_batch.py:
                 reference = look card + face card per hero job
                 boss job = boss card only, zero hero face refs

STEP 2  (free)   Correct tools/vast/build_keyframes.py:
                 - each hero prompt → 3-5 geometric anchors
                 - append appearance-only scope clause
                 - regenerate 100-job set (50 start + 50 end)

STEP 3  (free)   Write prompts for the two MISSING assets:
                 crossbow prop sheet + Mal'garot boss look card

STEP 4  (~$0.10) Rent RTX 6000 Ada (48GB, $0.539-0.65/h, native FP8):
                 - render the two missing asset sheets
                 - render ONE corrected proof pair (shot 03, crossbow insert)
                 - USER INSPECTS: same crossbow both frames? hood stable?
                   tattoo stable? face holds?

STEP 5  (gate)   USER APPROVES the corrected proof pair.
                 DO NOT scale until approval.

STEP 6  (~$5.4)  Render the full 100 keyframes (offer split across 2 boxes
                 to halve wall-clock; same total cost).

STEP 7  (gate)   Pull all, sha256-verify, SFace identity-gate on hero
                 frames, build labelled contact sheet. USER REVIEWS.

STEP 8  (~$8.3)  Render 50 video clips at 8-step FLF on verified keyframes.

STEP 9  (local)  Assemble film + narration + score locally (zero GPU).
```

---

## 10. PIPELINE / TOOLING MAP

### Image (keyframes)
- Model: **Qwen-Image-Edit-2511** (Apache-2.0, 20B, identity-locked multi-reference editing).
- fp8 working set ≈ **30 GB** (CLIP ~9.4G + transformer ~20.5G + VAE 0.25G).
- Node graph: ComfyUI (`/opt/workspace-internal/ComfyUI` on rental).
- Builders: `tools/vast/build_keyframes.py` (job file) + `tools/vast/run_kf_batch.py` (executor).
- Prompt cap: **≤1400 chars** (model truncation point).

### Video (FLF clips)
- Model: **Wan2.1-FLF2V-14B-720P** fp8.
- Node: `WanFirstLastFrameToVideo`.
- Jobs: `tools/vast/jobfiles/bossfight_flf_jobs.json` (100 jobs, blocking law embedded).

### Identity gate
- **SFace** similarity (local `tools/pick_face_refs.py`, YuNet + SFace).
- Pass thresholds observed: hero passes ≈ 0.70–0.84.
- Boss shots: **0 faces** (faceless canon).
- Faces < ~120px are below gate reliability — three-figure wides need bigger faces or a different gate.

### TTS (for later assembly)
- OmniVoice (Apache-2.0, 646 langs incl. Macedonian) — primary.
- MOSS-TTS-v1.5 (Apache-2.0, Macedonian) — secondary.
- VoxCPM2 (48kHz) — cloned voice only; Macedonian NOT an official language.

### Audio / score
- `score_lyria` bed; ffmpeg local assembly.

---

## 11. GPU / COST REFERENCE (MEASURED)

```
RTX 6000 Ada  48GB   $0.539-0.654/h   native FP8 (Ada)   ← preferred
L40S          45GB   $0.429-0.508/h   native FP8
RTX 4090      48GB   $0.443-0.48/h    native FP8
AVOID: Ampere (no native FP8 → OOM on 30GB stack)
AVOID: China hosts (unpredictable connectivity)
Disk: 100GB ($0.09-0.20/h) fits image+video models together (~53GB + OS).

Still cost @50 steps:  ~298s ≈ $0.054 each
Clip cost  @8 steps:   ~915s ≈ $0.166 each
Full 100 kf + 50 clips ≈ $13.7 + provisioning ≈ $15
```

---

## 12. VAST.AI OPERATING RULES (MANDATORY)

1. **Never auto-rent.** List-only mode first; read price/GPU from live API before submitting ask.
2. **Verify what executes, not what was intended** (a regex bug once substituted a 4s/544×960 clip).
3. **Stopped ≠ free**: stopped instance still bills storage (~$0.13-0.20/h for 100GB). Destroy when done.
4. **Credit is unknown if a provider call fails or times out.** Re-verify before quoting.
5. **Hard cap per run**, agreed in advance, itemized. Report actual vs cap after.
6. **Offload every finished artifact** (pull + sha256) BEFORE destroying an instance.
7. **SSH key**: `~/.ssh/vast_karsus`. Credentials live in `.a0proj/secrets.env` (gitignored).
8. Instance state files (`*.instance.json` at repo root) go stale — always re-read from live API.

---

## 13. COMMANDS / ENTRY POINTS

```bash
# Vast API state check (read-only)
export VASTAI_API=<from .a0proj/secrets.env>
# GET  /instances/            → list
# GET  /users/current/        → credit

# Build 100 keyframe jobs (local, free)
/opt/venv/bin/python tools/vast/build_keyframes.py

# Render keyframes on the rented box
/opt/venv/bin/python tools/vast/run_kf_batch.py --comfy-dir /opt/workspace-internal/ComfyUI

# Identity gate (hero frames)
/opt/venv/bin/python tools/pick_face_refs.py
```

---

## 14. OPERATING DOCTRINE (GOVERNING, FROM COMMIT 448a147)

```
1. Research first — no paid work on an unresearched premise.
2. Narration/dialogue written as THEIR OWN STEP before visuals.
3. Visual-first — design the shot before choosing models.
4. Photoreal default — cartoon/stylised is off-doctrine unless exempted.
5. First-Last-Frame, 40–60 shots per film.
6. Camera grammar — explicit scale/angle/movement per shot, varied.
7. Validate motion at SEQUENCE level, not per-clip.
8. No self-made benchmark — no VAST deliverable may be cited as the bar.
9. Proof before scale — one FLF proof scene, user-approved, before any batch.
```

---

## 15. WHERE TO CONTINUE FROM

```
NEXT ACTION: execute STEP 1 (§9) — rewire run_kf_batch.py to use
look-card + face-card references, and build_keyframes.py to emit
3-5 anchors + appearance-only clause. ZERO cost. Then STOP and
report the rework is ready for the user's review before any rental.
```

---

*End of handover.*
