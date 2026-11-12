# 43 — MODEL + PROMPT STANDARD (generator-agnostic; the N-clip start-frame-only model + the two-prompt discipline)

> Status: the rectified master standard (2026-11-11). Supersedes the LTX-centric
> framing of §21/§38 wherever they conflict. The director chooses the AI video
> model per story at the moment of generation — this standard is model-agnostic.

---

## 1. WHY LTX IS NO LONGER PROPAGATED

The earlier docs (§21, §38) were written when LTX-2.3 22B looked like the lead.
Two things changed:
- **LTX-2.3 22B is DEAD** on the rented-box route — a nanobind native-binding
  crash, reproducible across torch 2.15/2.7.1/2.8.0 (a native ltx-core C-ext bug,
  environment-specific, not a version issue). Recorded in `42_LTX23_22B_FAILURE_NOTE.md`.
- **The strategy moved to the N-clip start-frame-only model** (§19 below and
  `39_CORRECTED_PROMPT_STANDARD.md`), which is GENERATOR-AGNOSTIC — the same
  keyframes + the same continuation prompts drive ANY start-image model.

LTX is retained only as a documented route (LTX-2B, §6), not the default.

---

## 2. THE N-CLIP START-FRAME-ONLY MODEL (the primary strategy)

Every keyframe is a **START** frame. Render N keyframes for the storyboard
(typically 2 per shot: `kf_NN_start` + `kf_NN_end`; N = 2 × shot count, but any
keyframe set works). Run **ALL N as individual START frames → N clips**. N is NOT
fixed — it follows the shot list (a 23-shot board → 46 keyframes → 46 clips;
the current Hollow Bloom board is 50 shots → 100 keyframes → 100 clips).

- **Kills the end-lock failure.** Wan-FLF measured corr-to-end collapsing to ~0
  at f120; LTX/K6/SkyReels-V3/Mochi are start-image-only by spec. With no end
  frame to reach, the end-lock problem disappears.
- **Uses every rendered keyframe.** The N/2 end-frames cost the same as the
  starts; each becomes the start of its own continuation clip (not discarded).
- **Cuts carry continuity.** Continuity lives in the KEYFRAME CHAIN (each
  `kf_NN_end` visually matches `kf_(N+1)_start` — they were authored as a board),
  NOT in any single clip reaching a target.

---

## 3. THE TWO-PROMPT MODEL (image-gen ≠ video-gen)

**These are TWO distinct prompt types. Author them separately.**

### 3a. THE IMAGE-GEN KEYFRAME PROMPT (creates the START keyframe still)
- **Purpose:** produce the still image `kf_NN_start.png` / `kf_NN_end.png`.
- **What it controls:** SUBJECT (who/what is in frame, identity-locked to the
  face/armor/master asset), POSE (the frozen body position), SETTING (location,
  time, atmosphere), LIGHTING, CAMERA (shot scale, angle), STYLE (photoreal is
  the doctrine default).
- **What it does NOT control:** motion. A still has no motion — do not write
  motion verbs into the image prompt.
- **Discipline:** the fused master asset is the identity lock (attach it as a
  reference image where the model allows); the image prompt names subject/pose/
  setting/lighting/camera/style; ONE flowing description, not stacked guards.

### 3b. THE VIDEO-GEN CONTINUATION PROMPT (drives the clip FROM the keyframe)
- **Purpose:** given the frozen start keyframe, direct what MOVES.
- **What it controls:** MOTION (what moves, how, the motion's endpoint in
  WORDS), CAMERA movement, the pacing. Identity/props are carried by the IMAGE,
  not restated.
- **Discipline (the continuation rules):**
  1. **CONTINUATION, NOT SCENE CHANGE** — extend the frozen moment; never teleport/cut/introduce.
  2. **PRESENT TENSE, MOTION FIRST** — open with the motion the still implies, then camera, then the endpoint.
  3. **HOLD-ANCHORS for carried props/identity** — name a must-not-vanish prop ONCE as a held subject ("twin crossbows held low"); never as a guard/clamp.
  4. **NO ENDPOINT FRAME** — the motion's endpoint is described in WORDS; the clip moves for its frame count and stops; the NEXT keyframe takes over via the cut.
  5. **MOTION CALIBRATED TO THE SHOT** — closeup/hero: gentle; action/boss: the thrash.

**The rule:** one image-gen keyframe prompt PER keyframe (3a), one video-gen
continuation prompt PER keyframe (3b) — N of each, paired by `kf_NN_*`.

---

## 4. THE ESTABLISHED MODEL ROUTES (the proven ledger; choose per story)

| Model | Input | Proven route | Status |
|---|---|---|---|
| **Wan2.1-FLF2V-14B-720P** | start+end native (run START-ONLY) | renders; motion-OK; the ONLY FLF option | **WORKING** (the lead for 14B quality) |
| **Kandinsky 6.0 Lite / Pro** | start-image-only | motion-OK; fidelity-fail on detail (weapon collapse) at Lite | WORKING (Pro-distill untested at scale) |
| **SkyReels-V3 R2V-14B** | start-image-only | rendered; start-frame-only confirmed | WORKING (fallback) |
| **LTX-Video 2B v0.9.5** | start-image-only | rendered kf_01 (ambient motion; 2B ceiling) | WORKING (small/fast, low ceiling) |
| **Mochi-1** | start-image-only | on the list, start-only by spec | untested here |
| **LTX-2.3 22B distilled** | start-image-only | nanobind native-crash on rented boxes | **DEAD** (42 note) |

**The model is chosen per story at generation time.** The keyframes + the
continuation prompts are the SAME regardless of model (generator-agnostic); only
the render command differs.

---

## 5. THE KEYFRAME CONSISTENCY LAW (unchanged)
The keyframes are authored as a BOARD — each `kf_NN_end` visually matches
`kf_(N+1)_start` (blocking/staging law, §28). The edit = concat the N clips in
keyframe order; no transition is generated in-prompt.

---

## 6. LTX-Video 2B (the retained LTX route)
For small/fast LTX work: LTX-Video 2B v0.9.5 + T5, start-image-only, ambient
motion (the 2B ceiling). Use only where its look is acceptable; it is NOT the
lead. The LTX-2.3 22B route is dead (nanobind, §1).

## Per-model condition strength (added 2026-11-12, from the LTX-2.3 shot-01 extra-person defect)

Identity-silent continuation prompts (§3b) are MODEL-SPECIFIC, not universal. How strongly the
video model conditions on the start keyframe decides how much prompt anchoring it needs:

| Model | start-frame hold | continuation-prompt identity |
|---|---|---|
| **Wan-FLF 14B** | STRONG (start+end native) | fully identity-silent is SAFE |
| **LTX-2.3 22B** (img-strength 0.7) | WEAK (re-dreams the scene) | needs a LIGHT count/subject anchor |
| **Kandinsky 6.0 Pro** | MEDIUM (start-only I2V) | light anchor; close-ups hold better |

LTX-2.3 weak conditioning failure mode: it INVENTS extra people not in the start frame
(verified shot 01 grew a random third figure; YuNet counted a transient 2nd face at f015/f030).
The fix is NOT a full identity restatement (that caused the shot-04 morph) but a count anchor:
`...the two armored figures ... no other people in frame.` Verified in ltx23_s02_kf02.mp4.

Rule: for weak-conditioning models, every multi-character continuation prompt carries an explicit
count + 'no other people in frame'; single-character shots carry a subject anchor.
