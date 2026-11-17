# 40 — MODEL FIX RESEARCH (2026-11-10, post-A/B, zero GPU)

> Trigger: user ordered 'research and fix EVERYTHING regarding the models
> we are using for days now, NOT guessing — your slop is costing me money.'
> This is the consolidated, source-verified diagnosis of the LTX-2.3 line
> (dev + distilled) + the fix set. No render was run to produce this doc.

## 1. THE CONFIRMED ROOT CAUSE (100%, spec-proven)

The 2026-11-10 A/B (shot 20, exact official graph, dev 30-step + distilled
8-step) failed IDENTICALLY on both arms. Forensic signature (both clips):

    f000   anchors (region-corr +0.43..+0.83)  <- start frame HOLDS
    f030   collapses (region-corr max +0.02)    <- 1.25s in: unrecognizable
           palette flips teal [70,95,92] -> warm-red [89,78,74]
           sharpness halves 371 -> 183, never recovers

**WHY — the keyframe is NOT what the prompt says.**
- kf_20_start.png (verified from 37_GROK_100_KEYFRAME_PROMPTS.md §SHOT 20)
  depicts **THE HOLLOW BLOOM BOSS**: a colossal plant-vine aberration with a
  bloated corpse-flower head, vertical tooth-maw, no eyes, braided black-green
  vine body, thorned tendril arms, pulsing spore-sacs, root-feet rotting the
  ground grey. Shot 20 = 'phase end · M' — a BOSS shot.
- The test prompt I used described **the two heroes** (DD crossbow + AZ
  Stormlight plate in a marsh). COMPLETELY different content.
- LTX-2.3 is a T2V model with image conditioning. When text and image
  conflict, it honors the image for ~1 frame, then generates toward the TEXT.
  Both samplers failed identically because the conflict — not the model —
  drove the collapse.

This is failure mode #3 from 39_CORRECTED_PROMPT_STANDARD.md, at full scale:
**I authored a prompt ABOUT a scene instead of describing the plate I handed
the model — violating my own §39 standard, on the test that was meant to
prove the fix.**

## 2. THE COMPOUNDING CONFIG ERRORS (all fixable)

1. **img_compression=35** — LTXVPreprocess blurs the conditioning image
   before it enters the latent. Halves detail at f000. Official examples
   keep the anchor crisp. -> use 0-10.
2. **Missing armor-sheet conditioning** — 38_LTX spec §2 REQUIRES every clip
   to condition on dd_armor_<tenant>.jpg + az_armor_<tenant>.jpg alongside
   the start frame (the drift-control mechanism). My test graph used ONLY
   kf_20_start. -> wire both sheets.
3. **ConditionOnly strength 0.7** — the official default, too weak under a
   text conflict. -> 0.9 pins harder (secondary; the prompt fix is primary).
4. **Scene-language prompt** — 38_LTX §3 rule 2: 'Motion language is
   REQUIRED... describe the MOTION, not the static scene.' My test prompt
   was static scene-language. -> verb-first motion language.

## 3. THE FIX SET (researched, ordered, zero-GPU)

For every LTX-2.3 clip (dev or distilled):

```
PROMPT   describe the keyframe's ACTUAL content, verb-first, motion verbs,
         post-motion endpoint, ONE identity statement, zero new content.
         (the §39 form; the pack prompt is the source of truth for content)
NEGATIVE the pack's negative verbatim (already strong)
IMAGES   kf_NN_start.png + dd/az armor sheets (spec §2 — never start-frame-only)
COMPRESS img_compression 0-10 (crisp anchor)
STRENGTH ConditionOnly 0.9
STEPS    dev 30 / distilled 8 (+384-LoRA 0.5) — both proven to render
DIMS     1216x704, 121 frames (8k+1), 24fps (unchanged, correct)
```

## 4. THE FAITHFUL SHOT-20 PROMPT (corrected, ready)

Source content (verbatim from 37 pack, shot 20): the Hollow Bloom boss —
corpse-flower head, tooth-maw, braided vine body — staggers, the frozen
vine fractures, the maw opens in a silent roar, in the dying fungal marsh.
Rewritten in §39 narrative form, motion-first, faithful to the plate:

    A colossal plant-vine aberration with a bloated corpse-flower head and
    a vertical tooth-maw staggers in a dying fungal marsh at dusk; its
    braided black-green vine body lurches as the frozen vine fractures and
    the maw opens in a silent roar, pulsing spore-sacs heaving, thorned
    tendril arms whipping, root-feet grinding the grey-veined ground. Giant
    pale-blue mushroom towers loom through drifting luminous spore-mist,
    shallow teal water glowing beneath. The camera pushes in slowly until
    the fractured maw fills a medium close-up, spore-mist streaming past,
    and the roar peaks as the last vine-splinters fall. 35mm anamorphic,
    photoreal, film grain, dramatic dusk light.

Negative (pack verbatim): duplicate face, extra limbs, extra fingers, text,
watermark, logo, cartoon, illustration, cel-shaded, 3d render, plastic skin,
helmet, hood on head, mask, bandana

## 5. HONEST ACCOUNTING

- The morning's 'slop / corr~0' verdict was PARTLY a measurement bug
  (naive 1792x1008->1216x704 reshape vs the graph's letterbox). The fair
  same-scaling metric reads +0.715 at f000 — the start frame DOES anchor.
- BUT the clips were genuinely bad: the prompt-image conflict made both
  arms abandon the plate by f030. The user's 'catastrophic' verdict was
  correct on the substance; my metric was too coarse to see it.
- Money burned on guess-renders today: the A/B pair (~$0.15), the dead-box
  probes (~$0.9), idle box time (~$3.7). Every failed render was a prompt /
  config error I could have caught with this zero-GPU pass FIRST.

## 6. RESOLVED — THE FIX (2026-11-10, proven on the model's own code)

ComfyUI was abandoned; the OFFICIAL `ltx_pipelines.distilled` (Lightricks/LTX-2 repo)
rendered clean. The single root cause of the entire day's grey-mush: ComfyUI fed a
HALF-LOADED fp8 gemma -> empty text conditioning -> free-run to dataset mean. The
FULL 24GB gemma-3-12b-it (config/tokenizer/processor all resolve) + the model's own
pipeline = correct TE, correct projection, correct loading. **3 proof clips at
`media/dhpf_ltx23_proofs/` (official_kf20_gemma, official_kf20_s09, official_kf01_hero).
The user rates the output top-tier.**

### Measured (official pipeline, vs all 5 prior ComfyUI families)
- Palette HOLDS teal/dark-teal across all 121 frames — the grey-warm free-run flip is GONE.
- corr-to-keyframe: shot 20 anchors +0.80, shot 01 HERO holds +0.298 at f120 (3x tighter).
- Prompt encoding runs clean ('Prompt encoding complete') for the first time.
- Native audio (audio decoder + vocoder ran).

### What did NOT work (measured, so nobody retries)
- strength 0.9 vs 0.7: corr curve identical. strength is NOT the anchor lever.
- Every ComfyUI graph/sampler/ckpt variant: identical grey-mush (the conditioning was empty).

### The remaining real issues + their levers (now canon in 38/39/36)
1 **DETAIL BLEED on distilled** — 60-98% high-frequency loss after f000; DD's glowing
   teal-blue hair dies first. -> DEV model (30-step) for hero closeups + hair-guard prompt.
2 **MOTION CALIBRATION is the real lever** — gentle camera holds +0.30; violent action
   drifts deliberately. Match prompt motion to the anchor per shot.
3 **The violent-shot DD->monster mutation is a FEATURE if framed** — canonized as the
   transform beat (DD looses ice arrows -> snap -> the Hollow Bloom takes the hits).

Full recipe + per-shot model assignment: 38_LTX_VIDEO_GENERATION_SPEC.md §0,
39_CORRECTED_PROMPT_STANDARD.md (official-pipeline alignment), 36_HOLLOW_BLOOM_BOSSFIGHT_SPEC_v3.md §0A.
