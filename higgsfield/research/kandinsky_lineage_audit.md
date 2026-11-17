# Kandinsky Video Model Lineage Audit — VAST (zero-cost, web/HF/GitHub only)

**Date:** 2026-11-09
**Auditor:** Agent Zero (model-lineage audit)
**Scope:** Kandinsky VIDEO model lineage; is anything newer/stronger than Kandinsky 6.0 Lite (our Paladin teaser model)? VSR identification and modern open alternatives. Verdict vs LTX-2.3 22B distilled for Hollow Bloom.
**Cost:** $0 — Hugging Face API, model cards, GitHub API only.

---

## 1. TL;DR — the definitive answer

- **The newest general-purpose Kandinsky VIDEO generation family is Kandinsky 6.0 (Lite 3B / Pro 29B), released by `kandinskylab` on 2026-09-09 (arXiv 2610.05608). There is no Kandinsky 6.1, no Kandinsky 7, and no K6 successor anywhere on Hugging Face or in the `kandinskylab` GitHub org as of 2026-11-09.**
- **The strongest Kandinsky video model in existence is Kandinsky 6.0 Pro (29B), MIT licence.** We deployed the **Lite (3B) distilled** variant for the Paladin teaser. Pro is ~10x the parameters and is the only "better than Lite" candidate in the Kandinsky line.
- The only newer kandinskylab release is **Kandinsky S2V 1.0 (2026-09-25, arXiv 2610.19290)** — a **speech-to-video avatar** model (animate a reference face from a speech track), not a general text/image-to-video successor. Different task; not a K6 replacement.
- **VSR in our stack** was `kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers` — Kandinsky's own 1.4B video super-resolution DiT (×2/×2.25/×4, KVAE latent-space tiling, distilled to 2 model evals/tile). It OOM'd on our 48GB box.
- **Verdict vs LTX-2.3 22B distilled for Hollow Bloom: NO Kandinsky beats it.** K6 Pro 29B is the closest and is still a 5-second 864×480-with-audio clip generator needing a separate SR stage; LTX-2.3 22B distilled generates native 720p/24, 121-frame clips with keyframe interpolation in 8 steps, purpose-built for chained FLF filmmaking. Different class of tool for our 40–60-shot photoreal doctrine.

---

## 2. Verified lineage — Kandinsky VIDEO models in release order

All dates/licences from the Hugging Face API (`createdAt` / `license` tags) and model cards, retrieved 2026-11-09.

| # | Model | HF repo | Created | Licence | Releasing org | Notes |
|---|-------|---------|---------|---------|---------------|-------|
| 1 | Kandinsky Video 1.0 | `ai-forever/KandinskyVideo` | 2023-11-21 | Apache-2.0 | ai-forever (Sber) | Two-stage: low-FPS keyframes + interpolation. Project page: ai-forever.github.io/Kandinsky-3 |
| 2 | Kandinsky Video 1.1 | `ai-forever/KandinskyVideo_1_1` | 2024-05-27 | Apache-2.0 | ai-forever (Sber) | Adds T2I-conditioned keyframes (Kandinsky 3.0 first frame); "SoTA among open-source on EvalCrafter" (their claim, 2024) |
| 3 | Kandinsky 4.0 V2A | `ai-forever/kandinsky-4-v2a` | 2024-12-10 | Apache-2.0 | ai-forever (Sber) | Video-to-audio (sound generation for video), part of K4 |
| 4 | Kandinsky 4.0 T2V Flash | `ai-forever/kandinsky-4-t2v-flash` | 2024-12-10 | Apache-2.0 | ai-forever (Sber) | K4 text-to-video; Habr post 866156; project page ai-forever.github.io/Kandinsky-4/K40 |
| 5 | Kandinsky 5.0 family | `kandinskylab/Kandinsky-5.0-*` | 2025-12-02 | MIT | kandinskylab | T2V/I2V, Lite & Pro, 5s/10s, pretrain/sft/distilled16steps/nocfg variants; GitHub repo `kandinskylab/kandinsky-5` (last push 2026-08-07) |
| 6 | **Kandinsky 6.0 family** | `kandinskylab/Kandinsky-6.0-*` | **2026-09-09** | **MIT** | **kandinskylab** | **Latest general video family. Lite=3B, Pro=29B. 5s clips 864×480 @ 24fps + synced 44kHz audio (T2AV/TI2AV). arXiv 2610.05608. GitHub `kandinskylab/kandinsky-6` (last push 2026-11-08 — still active).** |
| 7 | Kandinsky 6.0 VSR | `kandinskylab/Kandinsky-6.0-VSR-*` | 2026-09-15 / 2026-09-21 | MIT | kandinskylab | Video super-resolution companion (see §5). GitHub `kandinskylab/kandinsky-6-sr` (last push 2026-10-20) |
| 8 | Kandinsky S2V 1.0 | `kandinskylab/Kandinsky-S2V-1.0-*` | 2026-09-25 | MIT | kandinskylab | Speech-to-video **avatar** (reference frame + speech track → talking-figure video). Pro transformer alone is 39.8GiB; needs ~50GiB peak w/ offload. arXiv 2610.19290. GitHub `kandinskylab/kandinsky-s2v` (last push 2026-11-05). NOT a general T2V/I2V successor. |
| 9 | Kandinsky WM 1.0 | `kandinskylab/Kandinsky-WM-1.0-*` | (org listing) | MIT | kandinskylab | World model / Physical AI: I2V for autonomous driving, robotics. GitHub `kandinskylab/kandinsky-wm` (last push 2026-08-05). Niche, not filmmaking. |

Notes on releasing orgs: the **ai-forever** org (Sber's open-source arm) carried KVideo 1.0→K4. The **kandinsky-community** org only holds K2.x/K3 image models (no video). **kandinskylab** is the current releasing org for K5.0/K6.0/S2V/WM. No Kandinsky video models exist under `sberbank-ai` (empty) or `SberDevices`.

### 2.1 Existence checks that came back NEGATIVE (as of 2026-11-09)
- HF full-text search `kandinsky 6.1` → no model repos.
- HF full-text search `kandinsky 7` → no model repos.
- HF full-text search `kandinsky 6` → only K6.0 Lite/Pro/VSR variants + community quants (kabachuha, coolthor, realrebelai, WaveCut, etc.). No "6.0 full" beyond Pro.
- GitHub `kandinskylab` org repo list: kandinsky-6, kandinsky-6-sr, kandinsky-s2v, kandinsky-5, kandinsky-5-lora-train, kandinsky-wm, kvae, kvae-audio. **No kandinsky-7 / 6.1 repo.**
- kandinskylab.ai/models/video (linked from every K6 card) is the K6.0 video page — no newer family advertised on the cards.

**Conclusion: Kandinsky 6.0 is the head of the Kandinsky video lineage. The question is closed — 6.0 Lite is NOT superseded by any K7/6.1; the only step up within Kandinsky is 6.0 Pro (29B).**

---

## 3. WHERE IS K6 — exact repos (this corrects the earlier ai-forever scan)

The earlier HF scan of `ai-forever` correctly found **no K6** — K6 lives under **`kandinskylab`**, not `ai-forever`. The deployed stack (from `tools/vast/paladin_k6_run.py` and `tools/vast/sr_chunk.py`):

| Role | Repo id | Licence | Created | Last modified | HF downloads |
|------|---------|---------|---------|---------------|--------------|
| Generation (deployed) | `kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers` | MIT | 2026-09-09 | 2026-10-12 | 1,508 |
| Generation (non-distilled Lite) | `kandinskylab/Kandinsky-6.0-Lite-5s-Diffusers` | MIT | 2026-09-09 | 2026-10-12 | 538 |
| Generation (**strongest**) | `kandinskylab/Kandinsky-6.0-Pro-distill-5s-Diffusers` | MIT | 2026-09-09 | 2026-10-12 | 1,156 |
| Generation (Pro full) | `kandinskylab/Kandinsky-6.0-Pro-5s-Diffusers` | MIT | 2026-09-09 | 2026-10-12 | 528 |
| VSR (deployed, OOM'd) | `kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers` | MIT | 2026-09-15 | 2026-10-12 | 1,088 |
| VSR (teacher, 4 Euler steps/tile) | `kandinskylab/Kandinsky-6.0-VSR-5s-Diffusers` | MIT | 2026-09-21 | 2026-10-12 | 278 |

Third-party quants relevant to a 48GB box (from HF search): `kabachuha/Kandinsky-6.0-Pro-distill-5s-int8-convrot` (3,852 dl), `kabachuha/Kandinsky-6.0-Lite-distill-5s-int8-convrot`, `coolthor/Kandinsky-6.0-Pro-distill-5s-NVFP4`, `realrebelai/Kandinsky-6.0-Pro-5s_GGUFs`, `WaveCut/Kandinsky-6.0-Lite-distill-5s-OrbitQuant-W4A4`. These exist because Pro is heavy (see §4).

---

## 4. Is there anything better than 6.0 Lite? — comparison table

| Candidate | Params | Native output | Audio | Licence | Motion-quality reputation | 48GB vast.ai deployability | ComfyUI support |
|-----------|--------|---------------|-------|---------|---------------------------|----------------------------|-----------------|
| **Kandinsky 6.0 Lite distill (DEPLOYED)** | 3B | 5s, 864×480 @ 24fps (121 frames) | Yes — synced 44kHz, lip-sync | MIT | Fast, decent; our teaser rendered 4 clips quickly at $1.538 total run | Trivial — fits easily; it is what we ran | Yes — registry.comfy.org/nodes/kandinsky6 |
| **Kandinsky 6.0 Pro distill** | 29B | 5s, 864×480 @ 24fps (121 frames) | Yes — synced 44kHz, lip-sync | MIT | Best in Kandinsky line; ~10x params over Lite; same published clip spec (quality, not resolution, is the gain) | **Borderline on 48GB.** Official card uses `enable_model_cpu_offload()`; S2V card states Pro-family VAE decode needs ~50GiB peak with offload on 80GB cards. Community int8/NVFP4/GGUF quants exist precisely to fit consumer/48GB cards. Feasible with int8 quant + offload; slow | Yes — registry.comfy.org/nodes/kandinsky6 |
| **Kandinsky 6.0 Pro (full)** | 29B | same | Yes | MIT | Same family, non-distilled (more steps, marginal quality gain) | Heavier than distill; same quant route | Yes |
| Kandinsky 5.0 Pro (T2V/I2V distilled) | (K5 card) | 5s/10s variants | No dedicated synced-audio story on card | MIT | Superseded by K6 in the same lab | Fine | Partial (diffusers) |
| Kandinsky S2V 1.0 Pro | ~40B total bundle (39.8GiB transformer + 16.6GiB Qwen Omni Thinker + VAE) | avatar clip from 1 reference frame + speech | Input speech drives animation; model does not synthesize new sound | MIT | Excellent for talking-figure avatar shots; NOT a general scene generator | No — card states ~50GiB peak **on top of** 80GB-class cards via ComponentsManager offload | Diffusers ModularPipeline; no standard ComfyUI node |
| Kandinsky 4.0 T2V Flash | — | K4-era, 2024 | No | Apache-2.0 | Dated; two generations behind | Easy | Legacy ai-forever code |
| Kandinsky Video 1.1 | — | 2024-era, keyframe+interpolation | No | Apache-2.0 | Dated | Easy | Legacy |

**Answer to Q3:** Within the Kandinsky universe, the only "better than 6.0 Lite" is **6.0 Pro (29B)**, and only in generation quality at the same 864×480/5s spec — not in resolution, duration or workflow. S2V 1.0 is newer but solves a different problem (speech-driven avatars). No K7 exists.

**Practical note for VAST:** if we ever return to Kandinsky (e.g. for synced-audio dialogue shots where its T2AV/TI2AV + lip-sync is genuinely distinctive), the upgrade path is K6.0 Pro-distill + an int8/NVFP4 quant, with VSR run as a separate chunked job (our `tools/vast/sr_chunk.py` already implements chunking — the OOM was in full-clip VSR decode, so chunked VSR with `tiles_batch_size=1` and CPU offload is the documented fix).

---

## 5. The VSR question — what it was, and what to use now

### 5.1 What VSR was in our K6 stack
- Repo: **`kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers`** (also `tools/vast/sr_chunk.py` hard-codes this id).
- What it is (from the model card): a **1.4B SR DiT** distilled with π-Flow DX to **2 model evaluations per tile**, plus the KVAE video VAE and an x2/x4 latent-upscaler bank. It upscales video **×2, ×2.25 or ×4** with tiled diffusion in KVAE latent space; the default ×2.25 path (×1.125 bilinear pre-upscale + ×2) is exactly the 864×480 → 1080p route we attempted. Video-only pipeline (audio must be re-muxed). MIT. GitHub: `kandinskylab/kandinsky-6-sr`.
- Why it OOM'd: tiled diffusion SR with a video VAE decode is VRAM-hungry; the card itself requires torch.compile/flex-attention and recommends CPU offload with `tiles_batch_size=1` trading speed for VRAM. Our full-clip invocation skipped the chunked path on the first attempt.

### 5.2 Open VSR/upscaling options today (verified repos)
| Upscaler | Repo | Licence | Created | Status / fit |
|----------|------|---------|---------|--------------|
| **SeedVR2 (7B / 3B)** | `ByteDance-Seed/SeedVR2-7B`, `ByteDance-Seed/SeedVR2-3B` | Apache-2.0 | 2025-06 | Current top open image+video restoration/upscale diffusion family; native ComfyUI support via `Comfy-Org/SeedVR2` (created 2026-06-06, 774k downloads). Strong candidate to replace K6-VSR for general upscaling. |
| Comfy-Org SeedVR2 packaging | `Comfy-Org/SeedVR2` | Apache-2.0 | 2026-06 | Official ComfyUI-native SeedVR2 nodes — the lowest-friction VSR on a rented Comfy box. |
| Real-ESRGAN (image; video via per-frame or video variants) | `TencentARC/Real-ESRGAN` (and ai-forever's `ai-forever/Real-ESRGAN`) | BSD-3 / Apache-2.0 | 2021+ | What our assembler's software fallback effectively resembles. Fast, cheap, no temporal consistency — the softness we saw on the teaser. |
| Kandinsky 6.0 VSR (teacher) | `kandinskylab/Kandinsky-6.0-VSR-5s-Diffusers` | MIT | 2026-09-21 | 4 Euler steps/tile flow-matching teacher — higher quality than the 2-step distill but slower; same VRAM class. |

**Recommendation:** keep **K6-VSR-distilled with proper chunking + CPU offload** as the matched SR for K6 footage (it is trained for exactly that latent stack), and adopt **SeedVR2 (7B, Apache-2.0, Comfy-Org nodes)** as the general-purpose VSR for non-Kandinsky clips (LTX-2.3 output included). Either way: never run full-clip VSR in one pass on a 48GB card — chunk first (we already own `tools/vast/sr_chunk.py`).

---

## 6. Verdict — does any Kandinsky beat LTX-2.3 22B distilled for Hollow Bloom?

**No — with evidence:**

1. **Class mismatch.** LTX-2.3 22B distilled (per VAST KB doc 14, verified from Lightricks sources) is an 8-step CFG=1 distilled model with **native 720p/24 output, 121-frame (5.04s) clips, keyframe interpolation (first-last-frame conditioning)** — engineered for exactly our doctrine: chained FLF shots, 40–60-shot photoreal films. Kandinsky 6.0 (even Pro 29B) generates **5s clips at 864×480** with synced audio — a clip generator with a separate SR stage, not an FLF filmmaking stack.
2. **Resolution/workflow.** K6 needs VSR to reach 1080p (and VSR OOM'd on our 48GB box); LTX-2.3 ships its own spatial ×2 + temporal ×2 upscalers and renders at native 720p.
3. **Deployability.** LTX-2.3 distilled runs comfortably on 48GB (we proved it on the vast.ai A6000); K6 Pro distill needs int8/NVFP4 quants and aggressive offload to fit the same box.
4. **Kandinsky's genuine edge is audio:** T2AV/TI2AV with synchronized 44kHz sound and lip-sync is something LTX does not do in our deployment. That makes K6 (Lite or Pro) a **specialist tool for dialogue/lip-sync shots**, not the Hollow Bloom backbone.
5. **No hidden successor:** no K6.1/K7 exists as of 2026-11-09 (§2.1), so the Kandinsky line cannot leapfrog LTX-2.3 in this production cycle.

**One-line verdict:** Kandinsky 6.0 Pro is the strongest Kandinsky ever shipped and still loses to LTX-2.3 22B distilled for Hollow Bloom — different class: 5s 480p+audio clip generator vs native-720p FLF filmmaking stack — keep LTX-2.3 as the boss-fight backbone and reserve K6-family (Lite, it's cheap) only if a future shot needs in-model lip-synced audio.

---

## 7. Sources (all retrieved 2026-11-09)
- K6.0 Lite distill card: https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers (family spec: Lite 3B / Pro 29B, 5s, 864×480, 44kHz synced audio, MIT, arXiv 2610.05608, ComfyUI/vLLM/SGLang/FastVideo badges)
- K6.0 Pro distill card + component table + family repo table: https://huggingface.co/kandinskylab/Kandinsky-6.0-Pro-distill-5s-Diffusers
- K6.0 VSR distill card (1.4B SR DiT, ×2/×2.25/×4, 2 steps/tile, KVAE latent tiling): https://huggingface.co/kandinskylab/Kandinsky-6.0-VSR-distilled2steps-5s-Diffusers
- K6.0 VSR teacher: https://huggingface.co/kandinskylab/Kandinsky-6.0-VSR-5s-Diffusers
- K6 GitHub (pushed 2026-11-08): https://github.com/kandinskylab/kandinsky-6
- K6-SR GitHub (pushed 2026-10-20): https://github.com/kandinskylab/kandinsky-6-sr
- S2V 1.0 Pro card (speech-to-video avatar, 39.8GiB transformer, ~50GiB peak w/ offload, arXiv 2610.19290): https://huggingface.co/kandinskylab/Kandinsky-S2V-1.0-Pro-Diffusers ; GitHub (pushed 2026-11-05): https://github.com/kandinskylab/kandinsky-s2v
- K5.0 repos (created 2025-12-02): https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-distilled-5s-Diffusers ; GitHub: https://github.com/kandinskylab/kandinsky-5 (pushed 2026-08-07)
- ai-forever video lineage: https://huggingface.co/ai-forever/KandinskyVideo (2023-11-21), https://huggingface.co/ai-forever/KandinskyVideo_1_1 (2024-05-27, EvalCrafter claim), https://huggingface.co/ai-forever/kandinsky-4-t2v-flash (2024-12-10), https://huggingface.co/ai-forever/kandinsky-4-v2a (2024-12-10)
- kandinskylab GitHub org listing (no 6.1/7 repo): https://github.com/orgs/kandinskylab/repositories
- SeedVR2: https://huggingface.co/ByteDance-Seed/SeedVR2-7B (2025-06-11, Apache-2.0), https://huggingface.co/ByteDance-Seed/SeedVR2-3B (2025-06-10, Apache-2.0), https://huggingface.co/Comfy-Org/SeedVR2 (2026-06-06, Apache-2.0)
- Real-ESRGAN: https://huggingface.co/TencentARC/Real-ESRGAN ; https://huggingface.co/ai-forever/Real-ESRGAN
- VAST internal: tools/vast/paladin_k6_run.py, tools/vast/sr_chunk.py, tools/vast/k6_autorun.sh (deployed repo ids), higgsfield/20_FULL_PIPELINE_HANDOVER.md (K6 teaser record), higgsfield/14_PALADIN_JUDGEMENT_v3_LTX23.md (LTX-2.3 22B distilled spec and sources)
- arXiv 2610.05608 (Kandinsky 6.0 Video report), arXiv 2610.19290 (Kandinsky S2V)

### Negative results (existence checks, 2026-11-09)
- HF model search `kandinsky 6.1`: no results. `kandinsky 7`: no results. `kandinsky 6.0 full`: no K6-family repo beyond Lite/Pro/VSR + community quants.
- HF orgs `sberbank-ai` (empty), `SberDevices` (ASR only), `kandinsky` (empty), `kandinsky-community` (K2.x/K3 image only — no video).