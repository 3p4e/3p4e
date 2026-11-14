# #23 Perseus & Medusa — PROOF SCENE SPEC (S53–S55, the Ketos confrontation)
> Doctrine gate: proof before scale. ONE proof scene at the target contract
> before any paid batch. Zero-GPU authoring. Spend requires a separate GO
> (see 23_VAST_DEPLOY_PLAN.md).
> RENDER STACK: LTX-2.3 22B distilled, official ltx_pipelines.distilled route.
> START-IMAGE-ONLY (note 42 durable lesson): each keyframe is its own clip
> start; the prompt is a CONTINUATION of that start frame's motion, not a
> description of different content. NO FLF end-frame pairs needed.

## Why S53–S55
- Highest-risk elements in one scene: human hero + serpent creature +
  severed-head prop + petrification beat + water/storm environment.
- Pass here = whole film render-ready. Fail = fix at lowest level, re-proof.

## The three proof clips
| Shot | Model | Dur | Content |
|------|-------|-----|---------|
| S53 | distilled-1.1 8-step | ~5.0s | Perseus opens the kibisis, head swings free |
| S54 | distilled-1.1 8-step | ~5.0s | Perseus presents the head; ketos locks gaze; sea stills |
| S55 | distilled-1.1 8-step | ~5.0s | Ketos grey stone; waves over fossilized coils |
All: 1216x704, 121 frames @ 24fps, --image kf_NN_start.png 0 0.7,
LoRA 0.5, x2 upsampler, seed = shot number.

## LTX-form motion-continuation prompts (verb-first, ONE flowing paragraph)
S53: "Perseus slowly raises the opened sack; the severed head swings free by
its hair; his eyes stay shut; the polished shield rises to guard his face;
wind and sea-spray drift across the rock."
S54: "Perseus holds the severed head high toward the sea; the great serpent
rears from the foam then stills, its gaze catching the head's stare; the sea
calms unnaturally around them; spray hangs suspended; the camera descends
slowly onto the frozen moment."
S55: "Waves break over the petrified serpent's grey stone coils; gulls
circle low; the two figures at the rock's edge turn from the sea as the
storm finally eases."
Negative (all): deformed, extra limbs, morphing face, flicker, watermark,
text, static frame, head in mouth, gore, blood spray.

## Optional END stills (NOT required for LTX23)
The 3 END-keyframe Grok prompts from the earlier draft are retained below as
optional cut-target references only — LTX23 distilled is START-IMAGE-ONLY,
so they are not inputs to the render. Consecutive keyframes already carry
continuity by construction (end of shot N matches start of shot N+1).
S53e: medium, kibisis fully open, head held at arm's length by the hair, eyes
averted, shield raised. Save kf_53_end.png.
S54e: wide, serpent frozen mid-rear, eyes locked on the head, sea gone still.
Save kf_54_end.png.
S55e: wide, serpent entirely grey stone in the surf, gulls circling, pair at
rock's edge in foreground. Save kf_55_end.png.
(Attach sets identical to the START blocks in the keyframe pack.)

## Proof acceptance gates (measured, not vibes)
1. Motion: frame-diff mean > 2.0 and < 40 adjacent; no static run > 8 frames;
   no black/blank frames; no freeze/crossfade disease.
2. Identity: Perseus face vs azface centroid >= 0.30 (SFace regression gate);
   face box >= 120px in S53/S54 mediums.
3. Continuity: serpent design vs asset_sea_serpent_p1 accepted by director;
   head vs medusa_sheet_p1 accepted.
4. Detail: hair/face readable at f120 on the hero mediums (if the 8-step
   distilled mushes the CUs, the affected shots move to the dev model at
   30-step per the per-shot assignment table in the deploy plan).
5. Concat: the 3-clip chain plays as one scene with no seam glitch
   (scan_join_glitches.py).
Fail any gate = stop, diagnose, fix lowest level, re-proof. No batch.
