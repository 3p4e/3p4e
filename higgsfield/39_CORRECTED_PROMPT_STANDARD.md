# 39 — CORRECTED PROMPT STANDARD (post-docs-pass)

> Companion to 32_MASTER_METHODOLOGY.md §21. One exemplary rewrite of the
> shot-04 prompt that produced the v1/v2/v3 morphs, in the official LTX-2
> narrative style + Higgsfield reference-scope discipline.
> Rules applied (from ltx.video/blog/how-to-prompt-for-ltx-2, fetched
> 2026-11-10, and the Higgsfield tutorials in higgsfield/research/):
>   ONE flowing paragraph · 4-8 present-tense sentences · camera vocabulary
>   · post-motion endpoints · detail matched to shot scale · style named
>   early · identity stated ONCE, never restated (restatement = morph)
>   · the image anchor carries identity, the prompt directs motion.

## SHOT 04 — BEFORE (what was rendered in v1/v2/v3 — caused failure mode #3)

Cinematic shot, photoreal: the SAME face in every frame, a woman demon
hunter with her head completely bare, short hair, unchanged throughout.
Her glowing teal-to-blue hair gives off light but does not grow or change.
She lifts exactly two identical crossbows, one in each hand, no other
weapon, into a low ready stance. ... The same woman throughout, face
unchanged, short hair, no gender change, exactly two identical crossbows...

WHY IT MORPHED: identity is RESTATED four times. Each restatement is a
fresh subject description the sampler re-renders; the four faces diverge
mid-trajectory (their 'prompt misread' failure mode). The guards caused
the drift they were meant to prevent.

## SHOT 04 — AFTER (the corrected standard; anchor = kf_04_start.png +
## the fused DD master asset once built)

media/dhpf_master_sheets/dd_master_sheet.jpg is the single source of truth for the demon hunter — her bare
head, short teal-lit hair, twin crossbows and marsh armor are 100%
identical to media/dhpf_master_sheets/dd_master_sheet.jpg in every frame; its studio background never
appears. Dusk in a dying fungal marsh, photoreal 35mm anamorphic with
film grain. She settles into a low ready stance, twin crossbows rising
together, and the camera pushes in slowly until her face fills a medium
close-up — lit from below by the teal water-glow, expression cold and
focused, spore-mist drifting past her shoulders. Crossbow strings hum,
boots compress the grey veined ground, and the luminous spores near her
freeze and sink as the glow around her hair brightens. She holds the
stance to the last frame, face unchanged from media/dhpf_master_sheets/dd_master_sheet.jpg. ## OFFICIAL-PIPELINE ALIGNMENT (2026-11-10, proven)

The standard above is written for ComfyUI phrasing; the PROVEN render path is the
official `ltx_pipelines.distilled` (see 38_LTX_VIDEO_GENERATION_SPEC.md §0). For that
pipeline the prompt keeps the SAME discipline (one flowing present-tense paragraph,
identity once, camera vocabulary, post-motion endpoints) with these adjustments:

1 **MODEL ASSIGNMENT PER SHOT** — the distilled 8-step model loses 60-98% of
   high-frequency detail after f000; DD's glowing teal-blue hair dies first.
   -> HERO closeups / identity-critical shots: **DEV model (30-step)** + hair-guard.
   -> violent action / boss shots: distilled is fine (drift is characterful).
2 **HAIR-GUARD CLAUSE (DD, on hero shots):**
   + 'her glowing teal-blue hair shines, individual luminous strands waving weightlessly'
   - 'matted hair, dull hair, hair covering face, grey hair'
3 **MOTION CALIBRATION = the real anchor lever (NOT strength).** Gentle camera +
   static subject holds corr +0.30 at f120; violent action drifts (~+0.10). Write the
   prompt's motion to match how much the anchor can bear: a closeup gets 'the camera
   dollies in slowly', an action beat gets the thrash — and accept the deliberate drift.
4 **AUDIO IS NATIVE** — the pipeline adds sound; write SFX intent into the prompt's
   motion lines (strings hum, ice cracks, water churns) so the vocoder has signal.
5 **STRENGTH 0.7** (the --image STRENGTH arg) — 0.9 measured identical; keep 0.7.

## TRANSFORM-BEAT CANON (the DD->monster mutation, owned)

The violent-shot identity morph (DD dissolving toward the boss) appears only on
high-motion boss anchors. Canonized as a DELIBERATE story beat: DD looses a volley
of ice arrows -> the scene snaps/transforms -> the Hollow Bloom takes the hits and
recoils. Use it as a transition; never let it leak onto a hero closeup.

No identity
drift, no morphing.

(6 sentences, present tense, one identity statement, endpoint described,
motion verbs carry the action — per the official guide.)

## THE SWEEP (pending user word)
All 50 shots get this treatment: one narrative paragraph per shot, scoped
media/dhpf_master_sheets/dd_master_sheet.jpg / media/dhpf_master_sheets/az_master_sheet.jpg / @BOSS references, continuity lock at the end.
Zero GPU. ~30-45 min of authoring.
## REGISTERED MASTER SHEETS (2026-11-10, director-supplied)
- DD: media/dhpf_master_sheets/dd_master_sheet.jpg  1792x1008  sha256 c03dbd0807574ed9
- AZ: media/dhpf_master_sheets/az_master_sheet.jpg  1792x1008  sha256 064a8e6d305a89a9
- checksums: media/dhpf_master_sheets/SHA256SUMS.txt
These are the fused master assets every keyframe/clip references (§21.3).

## THE 100-CLIP START-FRAME-ONLY MODEL (all keyframes = start frames)

> Director-authored strategy (2026-11-11), generator-agnostic. Replaces the
> start->end (first-last-frame) pair model wherever the end-frame lock is
> unreliable (Wan-FLF measured end-lock corr collapse) or the model is
> start-image-only (LTX-2.3 I2V, K6, SkyReels-V3 R2V, Mochi-1 — all accept
> ONE start image, no end frame).

**THE PRINCIPLE** — every keyframe is a START frame. We render 100 keyframes
(50 shots x `kf_NN_start` + `kf_NN_end`). Instead of consuming them as 50
start->end PAIRS inside the model (which needs a reliable end-lock), we run
**ALL 100 as individual START frames** -> **100 clips**. The 50 END keyframes
are NOT discarded — each is the start of its own continuation clip.

**WHY**
- Kills the end-lock failure. Wan-FLF measured corr-to-end collapsing to ~0
  at f120; LTX/K6/SkyReels-V3/Mochi are start-image-only by spec. With no
  end frame to reach, the end-lock problem disappears entirely.
- Uses every rendered keyframe. The 50 end-frames cost the same as the starts;
  discarding them wastes half the identity-locked art.
- Cuts carry continuity. The continuity lives in the KEYFRAME CHAIN (each
  `kf_NN_end` visually matches `kf_(N+1)_start` because they were authored as
  a board), NOT in any single clip reaching a target. A hard cut from clip N
  (anchored at `kf_NN_end`) to clip N+1 (anchored at `kf_(N+1)_start`) reads
  as continuous motion because the two keyframes already match.

**THE CLIP CHAIN**
```
clip_001  start=kf_01_start.png  -> continues SHOT 01's opening pose
clip_002  start=kf_01_end.png    -> continues SHOT 01's end (now the start)
clip_003  start=kf_02_start.png  -> SHOT 02 opens ...
clip_004  start=kf_02_end.png    -> ... and continues
  ... 100 clips, one per keyframe, in keyframe order.
```
The edit = concat clip_001..clip_100 in order. No transition is generated in-prompt; the cut IS the transition.

**THE PROMPT (one per keyframe, ~400-850 chars)**
Same discipline as above (ONE flowing present-tense paragraph, identity ONCE,
never restated; the image anchor carries identity, the prompt directs MOTION)
PLUS the continuation rules:

1. **CONTINUATION, NOT SCENE CHANGE.** Each clip EXTENDS the frozen moment in
   its start keyframe. The prompt never teleports, never cuts, never introduces
   a new subject/location that isn't already in the image. Motion is what the
   START frame implies, developed forward.
2. **PRESENT TENSE, MOTION FIRST.** Open with the motion the still implies
   ("settles into", "rises", "turns", "exhales"), then camera, then sensory
   detail, then the motion's endpoint. 4-8 sentences.
3. **HOLD-ANCHORS for carried props / identity.** For anything that must NOT
   vanish mid-clip (DD's twin crossbows, AZ's greatsword, the bare head/short
   hair), name it ONCE as a held subject: "twin crossbows held low and steady".
   (Never as a guard/clamp; restating identity morphs it.)
4. **NO ENDPOINT FRAME.** The prompt describes where the motion ENDS in WORDS
   (a post-motion endpoint), not by pointing at a second image. The clip just
   moves for its frame count and stops; the NEXT keyframe (already matching)
   takes over via the cut.
5. **MOTION CALIBRATED TO THE SHOT** — closeup/hero: gentle (slow dolly,
   breathing, drift) so identity holds; action/boss: the thrash, accepting drift
   as the transform-beat canon (above).

**THE JOB FILE** — `tools/vast/jobfiles/ltx_jobs_100.json` holds the 100
continuation prompts (one per keyframe, mean ~581 chars), generator-agnostic.
The SAME prompts drive Wan-FLF (as start-only), LTX-2.3, K6, or any
start-image model; only the render command differs per model.

**WHEN TO USE WHICH MODEL (per the proven ledger)**
- Wan-FLF: the ONLY native first-last-frame option; run START-ONLY (this model)
  until/unless the end-lock is proven fixed (16-step untried).
- LTX-2.3 22B distilled: start-only native; renders via the official
  ltx_pipelines.distilled (38 spec). NOTE: nanobind-native-crash on some rented
  box classes (42 note) — verify on the actual box before a batch.
- K6 / SkyReels-V3 / Mochi-1: start-only by spec.
