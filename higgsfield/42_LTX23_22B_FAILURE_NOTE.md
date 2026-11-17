# 42_LTX23_22B_FAILURE_NOTE
**2026-11-11 · box 60123928 (RTX 6000D, ssh1.vast.ai:28416)**

## Verdict (CORRECTED 2026-11-12): LTX-2.3 22B distilled is NOT dead — the old verdict below was wrong.

**The 2026-11-11 "STOP the route" verdict is retracted.** The official `ltx_pipelines.distilled`
route rendered clean and the director rated the output top-tier (`official_kf20_gemma.mp4`,
`official_kf01_hero.mp4`, `official_kf20_s09.mp4`). The two "failures" had specific, fixable causes:

- **The nanobind `refcount` crash = a torch-pin mismatch, NOT a model defect.** `ltx-core 1.6.1`
  calls a torch 2.8+ API (`torch.compiler.nested_compile_region`); the readme's `~2.7` pin is stale.
  Rebuilding torch 2.7.1/2.8.0 BY HAND (pip cycling) is what kept crashing. The correct fix is the
  repo's own `uv sync`, which pins the matching torch/transformers for this env — no hand-pinning.
- **The grey-mush = ComfyUI fed a HALF-LOADED fp8 Gemma**, producing EMPTY text conditioning → free-run
  to dataset mean. The fix is the FULL `gemma-3-12b-it` directory (config + tokenizer + processor +
  weights all resolving), which is exactly what the official pipeline uses — not a bare fp8 safetensors.

**The correct fast-lane recipe (from `38` §0, already proven):**
```
uv sync   # clone Lightricks/LTX-2 — never hand-pin torch
python -m ltx_pipelines.distilled \
  --distilled-checkpoint-path ltx-2.3-22b-distilled-1.1.safetensors \
  --gemma-root <FULL gemma-3-12b-it dir> \
  --lora ltx-2.3-22b-distilled-lora-384-1.1.safetensors 0.5 \
  --spatial-upsampler-path ltx-2.3-spatial-upscaler-x2-1.1.safetensors \
  --image kf_NN_start.png 0 0.7 \
  --height 704 --width 1216 --num-frames 121 --frame-rate 24 --seed NN
```
1216×704 (÷32), 121 frames (8k+1), 24fps, 8 steps, CFG=1 (distilled card). Native audio in. ~44GB bf16
fits a 48GB card directly → ~2-3 min/clip, no offload — the fastest high-QUALITY route we have.

The original (wrong) verdict is preserved below for archaeology only.

- 88 GB stack pulled + verified (distilled-1.1 byte-exact 46,149,345,334 B, LoRA, upscaler, full gemma-3-12b-it).
- torch 2.7.1 = missing `torch.compiler.nested_compile_region` (ltx-core 1.6.1 uses a 2.8+ API; the LTX-2 readme's ~2.7 pin is STALE vs its own code).
- torch 2.8.0 = has the API, but the nanobind crash returns anyway.
- 0 clips rendered across 4 setups (ComfyUI + 3 official-repo torch versions). The one good clip (official_kf20_gemma) was on a now-destroyed box.

**The 100-continuation-prompt set is a real durable artifact** (tools/vast/jobfiles/ltx_jobs_100.json),
continuation-of-start-frame style, ready for ANY working generator.

## The DURABLE lesson (the user's strategy — keep it)
LTX-2.3 distilled is START-IMAGE-ONLY. **Each keyframe (all 100, incl the 50 end-frames) becomes a
START frame for its own clip; the prompt is a CONTINUATION of that start frame's motion, NOT a
description of different content.** A scene shift = a NEW clip with a new start keyframe (a cut),
never an in-prompt transition. This is what kills drift. Applicable to whatever generator works.
