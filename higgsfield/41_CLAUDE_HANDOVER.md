# 41 — HANDOVER TO CLAUDE: the LTX-2.3 render-consistency problem (2026-11-10)

> Read this + 40_MODEL_FIX_RESEARCH.md §6 + 38_LTX_VIDEO_GENERATION_SPEC.md §0 first.
> Goal: a REPRODUCIBLE recipe that renders 50 first-last-frame I2V clips of the
> Hollow Bloom boss fight (media/dhpf_grok_keyframes/kf_01..50_start/end.png)
> at 1216x704, 121 frames, 24fps, photoreal, identity-locked, palette-stable.
> The director calls the current state CATASTROPHIC — do not trust any prior
> render as a reference.

## THE PROBLEM (unsolved)

LTX-2.3 22B (Lightricks, official `ltx_pipelines` from github.com/Lightricks/LTX-2)
renders EITHER crisp-but-unanchored (dev model) OR anchored-but-mush (distilled).
No single recipe reproduced the one genuinely-good clip the director approved.

## WHAT IS PROVEN (measured, reproducible)

1 **The official pipeline is the only correct route.** ComfyUI-LTXVideo nodes are
   BANNED (immature: wrong TE class, missing tokenizer, variant-detection crashes).
   The whole day's grey-mush free-run was ComfyUI feeding a HALF-LOADED fp8 gemma
   -> empty text conditioning -> dataset-mean collapse. Recipe in 38 §0.
2 **FULL gemma-3-12b-it HF dir (~24GB, unsloth/gemma-3-12b-it ungated) is mandatory**
   for the text encoder (--gemma-root). A bare fp8 file half-loads -> grey mush.
3 **Ungated weights** (all at Lightricks/LTX-2.3): ltx-2.3-22b-distilled-1.1 (46GB),
   ltx-2.3-22b-dev (46GB, has embedded audio VAE), the 384-LoRA (7.6GB),
   spatial-upscaler-x2-1.1 (1GB), the full gemma above.
4 **CLI shape:** `python -m ltx_pipelines.distilled --distilled-checkpoint-path <ckpt>
   --gemma-root <full gemma dir> --prompt '<one flowing present-tense paragraph>'
   --output-path out.mp4 --image <kf_start.png> 0 0.7 --height 704 --width 1216
   --num-frames 121 --frame-rate 24 --seed <N>
   --lora <384-lora> 0.5 --spatial-upscaler-path <upscaler>`
   DEV variant: `python -m ltx_pipelines.ti2vid_one_stage --checkpoint-path <dev ckpt>
   --num-inference-steps 30 --gemma-root <full gemma> ... --image <kf> 0 0.7`
5 **--image strength 0.7 == 0.9** (measured identical corr curves). Do not chase
   the anchor via strength.
6 **Audio is native** (the pipeline runs audio-decoder + vocoder).

## THE TWO FAILURE MODES (the actual problem to solve)

```
DISTILLED (8-step, +384-LoRA): holds the palette (teal/dusk holds across 121f) and
  anchors f000 (+0.78) BUT decays to structure-mush on any violent/high-motion shot:
  sharpness 534->8 (98% loss), corr -0.13 by f120. Good = the one 'top-tier' boss clip
  (media/dhpf_ltx23_proofs/official_kf20_gemma.mp4) was the lucky side of this variance.
  Bad = its repro (r3_shot20_distilled.mp4) is mush.

DEV (30-step): holds DETAIL beautifully — sharpness 608->593 (2% loss), the glowing
  hair survives — BUT drifts the global structure + palette: corr negative mid-clip,
  warm dusk [91,85,78] flips to blue-teal [60,91,100]. See r3_shot01_dev_hairguard.mp4.
```

## THE CANON THE RENDERS MUST SERVE

- DD (demon hunter): bare head, glowing teal-blue hair (individual luminous strands,
  the highest-frequency feature — dies first on distilled), twin crystal crossbows, ICE.
- AZ (paladin): open-face helm, molten-gold rune-tattoo, two-handed greatsword, LIGHT.
- Boss: Hollow Bloom, plant-vine aberration. Dying fungal marsh, teal-glowing water,
  grey corruption ring widening as a spatial timer.
- 50 shots, kf_NN_start + kf_NN_end keyframes exist (media/dhpf_grok_keyframes/, 106 files).
- Per-shot model assignment canon (36 §0A): hero closeups -> dev + hair-guard;
  violent action -> distilled; the DD->monster morph is a deliberate transform beat.

## OPEN QUESTIONS FOR CLAUDE

1. Why does the distilled model's corr collapse to negative on violent shots while the
   palette holds — is it temporal attention, the 8-step LoRA, or the VAE decode? What
   single change makes it reproducible-good (the official_kf20_gemma clip proved it's
   possible from the same weights+prompt)?
2. Why does the dev model re-light (warm->blue) + recompose? Is it CFG 3.0 + the
   monolith audio-joint path? Does a neutral-temperature prompt clause fix it, or is a
   lower CFG / different sampler needed?
3. Is there a first-last-frame (--image with an END frame) mode in LTX-2.3's official
   pipeline we missed (the ti2vid flags show only one image)? The 50-clip film needs
   start->end continuity.
4. GPU floor: is A100 80GB sufficient for a 50-clip batch, or does the dev path OOM?

## STATE / COST

- vast.ai credit after destroy: $13.572. The A100 box (60075318) is DESTROYED.
- A leftover STOPPED instance 60049564 (Swiss RTX PRO 6000) bills storage only.
- All proofs, keyframes, master sheets, docs are local (media/ is gitignored).
- Production doctrine: photoreal, FLF, 40-60 shots, camera grammar, no self-made
  benchmark, proof-before-scale (32_MASTER_METHODOLOGY.md §21, production_doctrine).
