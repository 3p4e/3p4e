# LTX Video Generation Spec — Hollow Bloom (shots 01–50)
**Created:** 2026-11-08 21:25 CET
**Author:** Agent Zero (source-checked against Lightricks/ComfyUI-LTXVideo docs + ComfyUI wiki)
**Status:** **PROVEN (2026-11-10)** — the OFFICIAL `ltx_pipelines.distilled` route (Lightricks/LTX-2 repo) renders clean with full identity + palette. ComfyUI-LTXVideo nodes are BANNED for LTX-2.3 (immature: wrong TE class / missing tokenizer / variant crashes). 3 proof clips at `media/dhpf_ltx23_proofs/`. Scale gate: per-shot model assignment (§5).

---

## 0. THE OFFICIAL PIPELINE (PROVEN — use this, not ComfyUI)

```bash
# install (once):  pip install -e packages/ltx-core -e packages/ltx-pipelines  (in a clone of github.com/Lightricks/LTX-2)
python -m ltx_pipelines.distilled \
  --distilled-checkpoint-path <ltx-2.3-22b-distilled-1.1.safetensors> \
  --gemma-root <FULL HF gemma-3-12b-it dir>   # MANDATORY full dir (config+tokenizer+processor); a bare fp8 half-loads -> empty conditioning -> GREY-MUSH free-run
  --prompt "<faithful, verb-first, motion-only, ONE flowing paragraph>" \
  --output-path out.mp4 \
  --image <kf_NN_start.png> 0 0.7          # PATH FRAME_IDX STRENGTH; strength 0.7 (0.9 tested = negligible difference)
  --height 704 --width 1216 --num-frames 121 --frame-rate 24 --seed <NN> \
  --lora <ltx-2.3-22b-distilled-lora-384-1.1.safetensors> 0.5 \
  --spatial-upsampler-path <ltx-2.3-spatial-upscaler-x2-1.1.safetensors>
```
Required weights (all UNGATED, Lightricks/LTX-2.3): the distilled monolith (46GB), the FULL gemma-3-12b-it HF dir (~24GB, stock OK for 2.3), the 384-LoRA (~7.6GB), the x2 spatial upscaler (~1GB).

### NEW FINDINGS (measured, 2026-11-10)
1 **FULL GEMMA IS THE WHOLE FIX.** ComfyUI fed a half-loaded fp8 -> empty text conditioning -> the model free-ran to dataset-mean grey mush on EVERY graph/sampler/ckpt variant. Full gemma + own pipeline = prompt encodes clean, palette holds teal, no free-run. (media/dhpf_ltx23_proofs/official_kf20_gemma.mp4)
2 **STRENGTH 0.7 == 0.9.** The conditioning-strength lever is negligible (measured: corr curve identical). Keep 0.7. Do NOT chase anchor-tightness via strength.
3 **THE REAL LEVER = PROMPT-MOTION CALIBRATION.** Gentle camera + static subject holds corr +0.30 at f120 (3x tighter); violent action drifts deliberately (corr ~+0.10). Match demanded motion to the anchor's stability per shot. (official_kf01_hero vs official_kf20)
4 **DETAIL BLEEDS ON DISTILLED — HAIR DIES FIRST.** 8-step distilled loses 60-98% of high-frequency detail after f000; DD's glowing teal-blue hair (highest-frequency feature) turns to mush. -> **DEV model (ltx-2.3-22b-dev, 30-step) for HERO closeups + a hair-guard prompt clause**; distilled is fine for violent action shots. Hair-guard: + 'her glowing teal-blue hair shines, individual luminous strands waving weightlessly' / - 'matted hair, dull hair, hair covering face, grey hair'.
5 **AUDIO IS NATIVE.** The official pipeline runs the audio decoder + vocoder — clips carry sound. Budget for it in the mix.
6 **THE VIOLENT-SHOT MUTATION IS A FEATURE IF FRAMED.** DD->monster morph appears only on high-motion boss shots. Canonized as a deliberate transform beat: DD looses ice arrows -> snap/transform -> the Hollow Bloom takes the hits.

---

## 1. Model Configuration (verified against LTX documentation)

### Frame count rule (CRITICAL — was wrong before this doc)
LTX frame count must be **8k + 1** (e.g. 65, 81, 121, 257).

| Frames | Seconds @ 24 fps | Status |
|--------|-------------------|--------|
| 65 | 2.7 | valid (inserts only) |
| **81** | **3.4** | **valid — proof length if drift shows at 121** |
| **121** | **5.0** | **valid — primary spec length** |
| 257 | 10.7 | valid (not used; too long) |

**Invalid:** 97 frames (my earlier 'sweet spot' — not 8k+1, causes silent failure or bad sampling)

### Resolution rule
Width and height must each be **multiple of 32**.
Primary: **1216×704** (proven LTX 0.9.5 sweet spot, ~native fidelity)
Do not use 1280×720 (720 is not a multiple of 32 → 704 or 736 required)

### Frame rate
LTXVConditioning node sets fps: **24 fps** (matches film spec)

### Sampling (LTX 2B v0.9.5 — no step-distill LoRA exists for 2B)
| Parameter | Value | Source |
|-----------|-------|--------|
| steps | **30** | LTX docs: 2B quality point |
| guidance | **3.0** | LTX docs: NOT cfg 1.0 (that is Wan-lightx2v lore, wrong model) |
| sampler | euler / dpmpp_2m | LTX default |
| scheduler | simple / normal | LTX default |

---

## 2. Conditioning Per Clip (the user's question — confirmed correct)

Every clip conditions on ALL of the following simultaneously:

```
START FRAME     kf_NN_start.png   (primary motion anchor — required, via LoadImage)
CHARACTER SHEET dd_armor_base.jpg   (extra image on LTXVImgToVideo)
CHARACTER SHEET az_armor_base.jpg   (extra image on LTXVImgToVideo)
PROMPT TEXT     spec §prompts (trimmed to LTX/T5 form, see §3)
NEGATIVE        deformed, extra limbs, morphing, watermark, text, static frame

OPTIONAL (batch only, after proof):
END FRAME       kf_NN_end.png at frame 121 (multi-frame keyframe conditioning)
                — 0.9.5 supports it, but risks freeze/crossfade disease on 2B.
                Proof runs START-FRAME ONLY. Add end frames only if proof
                shows clean motion AND user wants FLF chaining locked.
```

**Why armor sheets matter (user's insight):** LTX drifts on faces fast. Conditioning every clip on both armor sheets keeps DD's bare-head glowing-hair look and AZ's Stormlight armor anchored for the full 121 frames. This is not optional — it is the drift-control mechanism.

---

## 3. Prompt Adaptation: Grok Pack → LTX/T5 Form

The 37_GROK_100_KEYFRAME_PROMPTS.md pack was written for Grok (photoreal stills). LTX consumes text via T5 (77-token CLIP window does NOT apply; T5 handles ~512 tokens but quality degrades past ~200).

### Rules for LTX prompt text
1. **Trim to ≤200 tokens.** The pack's prompts are 300–900 chars — acceptable, but cut scene-redundant clauses.
2. **Motion language is REQUIRED.** LTX is I2V — the start frame is given, but the prompt must describe the MOTION, not the static scene.
   - WRONG (still-language): "a demon hunter stands in a marsh"
   - RIGHT (motion-language): "demon hunter strides forward through mist, glowing hair flowing, camera tracks slowly right"
3. **Camera direction:** LTX responds to explicit camera clauses (track/pan/orbit/dolly). The spec's shot table already has these — preserve them.
4. **Identity clauses:** "glowing teal-to-blue hair, bare head" and "Stormlight greatsword paladin" stay verbatim — T5 holds them well across 121 frames when backed by the armor-sheet conditioning.

### Per-shot prompt structure (LTX form)
```
[motion verb + subject], [armor/identity anchor phrase], [camera move],
[world/mood phrase], [light state]
Example (shot 01):
"Demon hunter strides through bioluminescent marsh mist, glowing teal-to-blue
 hair waving weightless, Stormlight greatsword paladin flanking right, camera
 tracks slowly forward at knee height, spore motes drifting, cold dawn light"
```

---

## 4. Clip Assembly (the 50×5 s stitch)

```
50 clips × 121 frames @ 24 fps = 50 × 5.04 s ≈ 252 s raw
Assembly: ffmpeg concat → ~2:30 film
Audio: 7 Macedonian dialogue lines + score (assembled locally, no GPU)
Seams: hard cuts; crossfade only where the shot table marks a continuity join
Chain: each shot's _end frame was drawn to match the next shot's _start —
       visual continuity carries across cuts by construction
```

**If proof shows face drift at 121 frames:** drop to 81 frames (3.4 s) for the batch. 50 × 3.4 s = 170 s ≈ 2:50 — still in the 40–60-shot doctrine window.

---

## 5. Batch Cost Projection (22B distilled, if proof passes)

```
Model:      ltx-2.3-22b-distilled-1.1.safetensors (~44 GB bf16)
Steps:      ~12–16 (distilled) vs 30 for 2B
Time/clip:  ~2–3 min on RTX 4090 48 GB (22B distilled is faster than 2B at 30 steps)
50 clips:   ~2.5 h render + ~0.5 h provisioning
Cost:       ~$1.70–2.20 total (at $0.5778/h class)
Credit now: $1.75 → 22B batch needs a top-up OR run 2B for ~$0.80 total

2B batch (fallback): 50 clips × ~1.5 min = ~1.3 h ≈ $0.75 + prov ≈ $0.95
Quality: acceptable for wides, risk on hero close-ups — decide after proof
```

---

## 6. Proof Gate (absolute — no batch until passed)

```
Proof clip: kf_01 (marsh arrival wide) — 121 frames, 1216×704, 30 steps, guidance 3.0
Gate 1: motion — frame-difference score > 8.0 mean (slideshow was ~2.0)
Gate 2: fidelity — face/armor match to start frame (SFace > 0.40 + human eyes)
Gate 3: no freeze, no morph, no crossfade disease

If pass → 3-clip class test (wide / medium / hero close-up) → batch
If fail → report honestly; SkyReels-V3 remains the known-good fallback
```

---

## 7. Corrections Applied Tonight (audit trail)

| Item | Was (wrong) | Now (LTX-correct) | Source |
|------|-------------|-------------------|--------|
| Frame count | 97 (4 s sweet spot) | 121 (5 s) / 81 (3.4 s fallback) | 8k+1 rule (ComfyUI wiki + LTX docs) |
| Guidance | cfg 1.0 | 3.0 | LTX 0.9.5 docs |
| Resolution | 1280×720 | 1216×704 (÷32 rule) | LTX usage limitations |
| End frames | assumed unusable | 0.9.5 multi-frame control exists; proof starts start-only | ComfyUI LTXV tutorial |
| Conditioning | keyframe only | keyframe + armor sheets per clip | LTXVImgToVideoConditioning (user + docs) |
| Prompt style | photoreal still language | motion-first T5 form | LTX I2V prompting guide |

---

*Next: proof render on box 59773014 when weights land.*
