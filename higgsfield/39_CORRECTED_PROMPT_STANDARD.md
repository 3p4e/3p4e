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
stance to the last frame, face unchanged from media/dhpf_master_sheets/dd_master_sheet.jpg. No identity
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
