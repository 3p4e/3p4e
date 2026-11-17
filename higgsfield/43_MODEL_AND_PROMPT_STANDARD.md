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

## 2026-11-15 — Kandinsky-6.0-Lite-distill-5s locked as the #23 48GB render model
- **Model:** `kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers` (Apache-2.0, ungated), TI2VA, T5-umt5-XXL prompts.
- **Recipe:** 480×832 (portrait) or 832×480, 121 frames @ 24fps, 16 steps, guidance_scale 1.0 (distilled), seed per shot, start keyframe only. `enable_model_cpu_offload()` fits 48GB (~10GB used).
- **Per-clip:** ~140s on RTX 6000Ada. Native AAC 44.1kHz stereo audio generated in the same pass.
- **Prompt form:** single motion verb sentence → camera-move sentence → endpoint-in-words (same form as the Wan/LTX action rewrites; see `tools/vast/jobs/p23_wan65.json`, 65 prompts).
- **Not chosen:** Wan2.1-I2V-14B (48GB noise-output failure, lesson 26); Wan2.2-Animate-2-14B (driving-video animator, no template videos); K6 Pro 29B (int8 ComfyUI-only / bf16 OOMs 48GB); Wan 3.0 (API-only, family faces → Alibaba).
- **Batch runner:** `tools/vast/render_k6_batch.py` (resume-safe, skips existing >100KB clips, per-shot seed, native-audio mux).
- **Master assembler:** `tools/assemble_23_k6_master.py` (picture-lock order S01–S20, F01–F10, S26–S60).
- **Audio:** 3-layer mix per `23_AUDIO_MIX_SPEC_v4_K6.md`; script `23_AUDIO_SCRIPT_MK_EN_v3_65clips.md` (65 lines, ElevenLabs casting table; MOSS-TTS = free MK route).

---

## Delivery addendum — dual-language audio (2026-11-15)
Bilingual delivery is ONE file with selectable audio tracks (MKV, per-stream language metadata, MK default). See 48_BILINGUAL_DELIVERY_SPEC.md for the mux recipe. Never ship two separate videos per language.

---

## 2026-11-15 (Hollow Bloom autopsy) — HARD RULES added after the measured slop failure
Source: 50_HB_SLOP_AUTOPSY_20261115.md + 51_SLOP_FIX_RESEARCH_20261115.md. These override
any earlier clause they contradict.

1. **NEVER name concepts in negatives.** 'morphing, drift, new people, duplicate face,
   extra limbs' in a negative list still fires the concept embeddings — T2V/I2V models
   generate what is named. Measured: 53% of HB clips grew random people after the
   negative-list tail was added. Negatives are for artifacts only: watermark, text, logo.
   Control people/composition by POSITIVE anchors and the frame budget, not negation.
2. **No global motion tails.** Per-shot prompt = ONE specific motion verb-phrase + camera
   + endpoint (39 form). NEVER append global 'the movement stays strong and continuous
   through the final frame / nothing settles into a held pose' clauses — they fight the
   start-frame anchor and cause full scene re-dream (measured 78% REDREAM).
3. **Hold-anchor instead:** add 'the composition, subjects and palette hold; only the
   named action moves' — tells the model what NOT to touch.
4. **Content gates are mandatory before any batch approval** (tools/analyze_hb_slop.py):
   drift-drop ≤0.35 · faces ≤ kf_faces+1 (YuNet 0.75) · palette ≤0.5 · motion 4-20
   (0-255 scale) · sharpness-last ≥100 · identity-sim vs hero centroid ≥0.30 (once the
   SFace ref build is fixed). The PROOF clip must pass ALL gates; motion pass alone is
   NOT approval.
5. **Anchor tier rule:** Lite/2-step-distill models (K6 Lite, LTX-2B) are previs/motion-
   blocking tiers ONLY. Finals render on the strongest available anchor (K6 Pro 29B,
   Wan-FLF, LTX-2.3 22B) with the SAME model for proof and batch.
6. **Identity is anchored, not described** (KB consensus: 'Text descriptions reduce
   drift but do not fix it. Identity anchors do.'): keyframe gen uses InstantID/IP-Adapter
   face-lock; finals add the per-clip SFace-centroid post pass or a per-hero LoRA
   (Soul-ID pattern, self-hosted).

## 2026-11-16 — Wan 2.2 Fun Control locked as PRIMARY renderer (HB v2 + all future films)
Source: official ComfyUI tutorial (docs.comfy.org, doc 56) + Grok production package (doc 53)
+ operational clarifications (doc 57). This section supersedes the 'K6-Lite bulk' default.

### The v2 canonical stack
- PRIMARY: Wan 2.2 Fun Control (Alibaba PAI, Apache 2.0). Models
  wan2.2_fun_control_high/low_noise_14B_fp8_scaled.safetensors; acceleration
  wan2.2_i2v_lightx2v_4steps_lora_v1_high/low_noise.safetensors (HIGH↔HIGH, LOW↔LOW only);
  umt5_xxl_fp8_e4m3fn_scaled.safetensors; wan_2.1_vae.safetensors.
  Template: ComfyUI Workflow → Browse Templates → Video → Wan2.2 Fun Control.
- CONTROL VIDEOS (the anti-re-dream mechanism):
  · body action (heroes) → DWPose control video, clean single-subject real reference footage
  · space/environment (marsh, Bloom, wide geometry) → Video Depth Anything LARGE
    (doc 55; temporal-consistent, never frame-by-frame DAv2 for >2-3s)
  · both → pose+depth. atmosphere → none (start frame + HOLD only).
- FALLBACK: LTX-2.3 Dev 30-40 steps CFG 3.0-3.5 start-strength 0.7-0.8 for extreme CUs
  (face/hair/tattoo); LTX Distilled 8-12 steps for violent chaos where drift reads as energy.
  Identity escalation: start-strength → TASS-RoPE tools (LTX-Best-Face-ID / Likeness Guide).

### The canonical video prompt (HOLD form — every clip, asserted in the jobfile builder)
"Using start frame kf_XX_start.png. Composition, subjects, lighting direction, palette and
subject count hold. Only <one concrete action>. Driven by <pose/depth> control video.
Camera: <move or locked>."
Builder: tools/build_hb_wanfc_jobfile.py — the build FAILS on any banned tail, scene
restatement, or named-concept negative.

### Verification gates (Q7 — reject on 2+ failures, per clip, BEFORE batch)
start-corr ≥0.92 (CLIP cosine) · drift-drop ≤15% (RAFT/Farneback) · face-count exact
(InsightFace/MTCNN vs keyframe) · palette HSV ≤12 (OpenCV hist) · motion band 2-18 px/frame
· sharpness ≥80 (Laplacian var).

### Reference jobfile
p23_hb_wanfc_116.json (Hollow Bloom v2: 108 Wan FC + 8 LTX Dev; pose 29 / depth 25 /
pose+depth 23 / none 21; chaos fallback flags 12).

---

## Wan 2.2 motion-control routes (research addendum 2026-11-16, from Grok)
| Model | Use when | Notes |
|---|---|---|
| Wan 2.2 Fun Control | Combat / clear humanoid action, camera moves / environment | Primary. DWPose for body action, Video Depth Anything Large for space. Auto-detects control type. HOLD prompt essential. |
| Wan Animate 2 | Long continuous takes | Better face/identity retention + viewpoint control; heavier, less mature tooling. |
| Wan 2.1/2.2 VACE | Outfit + face consistency matters more than pure motion | Stronger identity/clothing lock, higher compute. |

**Rule:** single control_video input. Multi-control (pose+depth) requires blending frames first or a custom node. Identity drift is a known Fun Control weakness — HOLD prompt + strong start-frame conditioning helps but is not perfect.

## DWPose parameter tuning for Wan Fun Control (research addendum 2026-11-16, from Grok)
| Parameter | Default | Recommended for combat |
|---|---|---|
| detect_body | true | true — keep on |
| detect_hands | true | true (false if fingers jitter) |
| detect_face | true | **false** — face keypoints cause identity/expression leakage |
| score_threshold | 0.3-0.45 | 0.40 — raise to cut jitter, lower if limbs drop out |
| detection_threshold | 0.45 | 0.45 — raise to kill background ghosts |
| stick_width | 4 | 4 |

**Starting profile:** body=true, hands=true, face=false, score=0.40, stick=4. Spot-check 5-10 frames: no black frames, no limb teleporting, hands present when needed, single clean skeleton. Jittery limbs → raise threshold; hands garbage → disable detect_hands; face fighting identity → keep detect_face off.

## Temporal filtering for control videos (research addendum 2026-11-16, from Grok)
| Method | Complexity | Best for |
|---|---|---|
| 5-frame median | Very low | Outlier spikes, combat clips |
| Savitzky-Golay (window 5-9, poly 2) | Low | Most combat — preserves peaks |
| EMA zero-lag | Low | Online |
| Kalman | Medium | Limbs temporarily vanish |
| SmoothNet | Medium | Offline high quality |

**Chain for Hollow Bloom:** (1) re-extract DWPose with detect_face=false, score=0.40; (2) apply 5-frame median or SavGol window 7; (3) spot-check 10-15 frames for limb stability; (4) feed cleaned control video. Depth flicker → switch to Video Depth Anything (already standard, doc 55).

---

## Commercial-license decision matrix (research addendum 2026-11-16, from Grok)

| Model | License | Commercial use | Hollow Bloom verdict |
|---|---|---|---|
| Wan 2.2 (Fun Control / I2V / Animate) | Apache 2.0 | YES — unrestricted, no revenue/territory/attribution clauses. 'We claim no rights over your generated contents.' | PRIMARY. Cleanest license among strong motion-control models. We own outputs. |
| Mochi 1 / Open-Sora 2.0 | Apache 2.0 | Yes | Older / limited — not competitive. |
| LTX-2.3 / 2.5 | LTX-2.x Community License (2026-08-11) | FREE under $10M annual revenue; paid license above. No rights claimed in outputs (§5). Derivatives must use same license. AI-disclosure required in some publishing contexts. | SECONDARY (identity CUs only) — usable commercially below the $10M threshold. |
| MiniMax H3 | MiniMax H3 Community License (2026-08-02) | EXCLUDES US/EU/UK/KR (territory clause extends to outputs §V.4). 'MiniMax H3' display required on commercial UI (§IV.2). >$20M needs approval. | **CORRECTION 2026-11-16:** North Macedonia is NOT an EU member (candidate only) — the territory exclusion does NOT apply. H3 is legally usable from MK under $20M, BUT stays OUT of Hollow Bloom for production reasons (API-only, no local IC-LoRA control). |
| HunyuanVideo 1.5 | Tencent Community License | Excludes EU/UK/KR | **CORRECTION 2026-11-16:** Same as H3 — North Macedonia is not an EU member, so the exclusion does not apply from MK. Production-unfit for Hollow Bloom (no local control), not legally banned. |

**Rule (binding):** For Hollow Bloom and any client/commercial VAST delivery, LTX-2.5 is the PRIMARY renderer
(director decision 2026-11-16). LTX-2.x is usable commercially under $10M annual revenue; we accept the threshold.
Wan 2.2 (Apache 2.0) is the BACKUP. MiniMax H3 / HunyuanVideo are NOT banned for North Macedonia (not an EU
member) — they remain excluded from Hollow Bloom for PRODUCTION reasons (API-only, no local control). Wan 2.2's
Apache 2.0 means no revenue cap, no territory restriction, no required attribution — we own the outputs.

---

## MODEL ASSIGNMENT UPDATE (director decision 2026-11-16, supersedes the Wan-2.2-primary rule above)

**LTX-2.5 is the PRIMARY renderer for ALL Hollow Bloom clips** — bulk, combat, close-ups, atmosphere,
everything. The director explicitly chose LTX-2.5 for everything ("i want LTX 2.5 for everything").

Rationale (director's call, recorded):
- Strongest identity lock + native synced audio + first/last-frame support in the open-weights tier.
- Commercially usable under the $10M revenue threshold — the director is comfortable with that threshold
  ("glad to reach $1M", threshold is 10x that).
- One pipeline, one prompt standard, one verification stack — simpler than a dual-model split.

**Revised routing:**
| Role | Model | License |
|---|---|---|
| PRIMARY (everything) | LTX-2.5 (Distilled + IC-LoRA control, Dev for LoRA training) | LTX-2.x Community (<$10M) |
| Backup / fallback if LTX-2.5 fails a class of shots | Wan 2.2 Fun Control | Apache 2.0 |
| Depth control | Video Depth Anything Large | Apache 2.0 |
| Pose control | DWPose (face off, score 0.40) | — |

**Standard for every LTX-2.5 shot** (per doc 59):
- First-frame I2V lock (strength 0.75-0.85) + DD character LoRA (once trained) on hero shots.
- IC-LoRA control: DWPose for combat action, Video Depth Anything for environment/spatial.
- Cinematic prompt standard (5-part: camera → environment → single action → audio → style anchors).
- HOLD discipline: one action, composition/subjects/palette hold, positive constraints only.
- Two-stage sampling (8-step distilled + x2 spatial upscale) at 1280×720, 121 frames @ 24fps.
- Verification gates from doc 59 §7 before accepting any clip.
