# 42_LTX23_22B_FAILURE_NOTE
**2026-11-11 · box 60123928 (RTX 6000D, ssh1.vast.ai:28416)**

## Verdict: LTX-2.3 22B does NOT run on this box class — STOP the route.
The official `ltx_pipelines.distilled` (Lightricks/LTX-2, ltx-core/ltx-pipelines 1.6.1)
CRASHES on a **nanobind native-binding refcount error** at import, IDENTICAL across
**torch 2.15.0+cu132 / 2.7.1+cu128 / 2.8.0+cu128**. Not a version mismatch — a
native ltx-core binding bug on this environment (RTX 6000D / CUDA / Python 3.12).

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
