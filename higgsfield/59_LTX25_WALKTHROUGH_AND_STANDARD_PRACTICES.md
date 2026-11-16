# 59 — LTX-2.5 Comprehensive Walkthrough & Standard Practices
# High-end cinematic commercial video (Hollow Bloom class). Source: Grok deep research, 2026-11-16.
# License: LTX-2.x Community License — FREE under $10M annual revenue; paid above; affiliates counted.
#   No rights claimed in outputs (§5). AI-generation disclosure required in some contexts (EU AI Act).

## 1. Hardware & model choice (48 GB)
| Component | Recommended | Notes |
|---|---|---|
| Transformer | Distilled INT8 ConvRot, or BF16 w/ offload | Distilled = 8 steps, CFG 1. Dev = for training LoRAs. |
| Text encoder | Gemma 4 12B + projection (INT8 or BF16) | Custom for LTX-2.5. |
| VAEs | Official video + audio VAEs | BOTH required for synced audio. |
| Spatial upscaler | Official x2 latent spatial upscaler | Two-stage pipeline. |
| Resolution | 1280×720 or 1280×736 (÷32, 16:9) | Safe on 48GB; go higher w/ two-stage. |
| Frame counts | 8n+1 (121 = 5s @ 24fps) | STRICT. |

**Practice:** official ComfyUI templates are the baseline. Iterate at lower res/length, then upscale.

## 2. Identity lock (the DD problem — LAYERED, not single-method)
LTX-2.5 does NOT hold faces reliably without reinforcement. Stack these:
1. **First-frame I2V conditioning** — strong start keyframe, strength 0.75-0.85 (stage 1), higher in stage 2.
2. **Character LoRA (best long-term)** — train on DEV ckpt, 20-30+ multi-angle DD images/video, rank 32-64, 500-2000+ steps, trigger token. Validate with and without a first frame.
3. **IC-LoRA / Ingredients / Face-ID adapters** — Ingredients IC-LoRA (reference-sheet method) locks character+props+environment. Prefer 2.5-trained adapters over older 2.3 ones. Face Identity Reinforcer nodes help with I2V.
4. **Prompt discipline** — fixed 50-80 word character block on every shot; strip appearance from the action part when a strong ref/LoRA is present.

**Practice:** hero shots = strong first-frame keyframe + character LoRA. Multi-shot consistency = Ingredients reference sheet.

## 3. Motion & structural control (IC-LoRA based)
| Control | Preprocessor | Best for |
|---|---|---|
| Pose | DWPose | Human action, combat (DD crossbow / AZ sword) |
| Depth | Video Depth Anything / DepthCrafter | Camera moves, marsh/spatial consistency |
| Canny | Canny edges | Composition / silhouette lock |
| Union | Combined | Multiple signals (higher VRAM) |
| Motion Track | Sparse point trajectories | Precise object/character path |

**Rules:** prompt describes STYLE+LOOK, not motion (control video provides motion). Reference control video often 0.5× res. Strength typically 1.0 (lower if it fights the first frame). One control group at a time.

**HB practice:** Pose IC-LoRA for combat + Depth for environment/camera, layered on the identity lock.

## 4. Prompting standard (cinematic consistency)
Structure: (1) shot type + camera move (2) full environment/ lighting/palette (3) specific measurable action (4) audio description (5) style anchors (photoreal, 35mm anamorphic, teal/slate, film grain, dusk).
- One primary action per clip. State that composition/subjects/palette hold except the named action (HOLD discipline).
- Positive constraints only — NEVER name negative concepts (they get generated).
- Multi-shot: native multi-shot where available; keep the same character+environment block across related shots; Ingredients sheet for recurring elements.
- Audio: describe dialogue + sound design in the SAME prompt (native sync). For precise timing (D5/D6), generate longer and cut, or post-sync.

## 5. World consistency across shots
- Shared style header w/ full environment block (fungal marsh, pale-blue towers, spore-mist, teal water, dusk, teal/slate + molten-gold accent).
- Depth control from consistent reference plates / approved previous shots.
- Ingredients reference sheet for environment elements.
- Same seed family + locked character/environment LoRAs where possible.

## 6. Resolution, aspect, delivery pipeline (48 GB)
- Generate 1280×720 / 1280×736. Two-stage (low-res + spatial upscaler) for higher final res.
- 121 frames ≈ 5s @ 24fps. Post-upscale / Diffusion Video Decoder for sharper faces.
- Commercial: keep provenance/metadata where license requires disclosure.

## 7. Verification gates (numeric, before accepting a clip)
- Start-frame correlation ≥ 0.90 (SSIM or similar)
- Face identity holds (ArcFace or visual)
- Palette HSV distance within tolerance vs reference
- No extra people / scene replacement
- Motion matches the single intended action
- Audio sync acceptable (or plan post-sync for critical lines)

## 8. Commercial compliance checklist
- Under $10M annual revenue (or obtain paid license)
- Disclose AI generation where required (EU AI Act)
- Do NOT use outputs to train competing models
- Keep watermarking/provenance intact if present
- Document model version + settings for client records

## 9. Recommended production order for Hollow Bloom
1. Finalize high-quality start/end keyframes
2. Train / select DD character LoRA (AZ if needed)
3. Build control videos (DWPose action / Depth environment)
4. Iterate: Distilled + I2V + IC-LoRA (Pose/Depth) + character LoRA
5. Lock seeds/settings that pass the gates
6. Final high-quality passes + audio
7. Post: color, grain, dialogue timing, AI disclosure

**This is the strongest cinematic + identity + motion + commercial-usable open-weights stack on 48GB.**

---

## 10. Concrete node chain — LTX-2.5 combat shot (I2V + Pose IC-LoRA)
Production chain for a Hollow Bloom combat shot (DD crossbow / AZ greatsword). Base: official
LTX-2.5 I2V two-stage template + Union/Pose IC-LoRA (ComfyUI-LTXVideo/example_workflows/2.5/).

1. **Model loading**
   - UNETLoader → ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors (or BF16 if VRAM)
   - CLIPLoader (type ltxv) → gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors
   - VAELoader → ltx-2.5-video-vae-bf16.safetensors AND ltx-2.5-audio-vae-bf16.safetensors
   - Optional 2nd CLIPLoader for prompt enhancer (gemma4_e2b_it_int8_convrot)
2. **Character LoRA (DD — recommended)**
   - LoraLoaderModelOnly after UNET → trained DD LoRA, strength 0.8-1.2, feed to all sampler stages
3. **First-frame identity lock**
   - LoadImage → kf_XX_start.png into the I2V conditioning path (strength 0.75-0.85 stage 1, higher stage 2)
4. **Pose control (IC-LoRA)**
   - LoadVideo → reference action video → DWPreprocessor/DWPose Estimator (skeletons) → resize ÷32
   - LTXICLoRALoaderModelOnly → pose/union IC-LoRA (ltx-2.5-22b-ic-lora-union-control-ref0.5.safetensors) strength 1.0
   - LTXAddVideoICLoRAGuide → injects pose guide frames
5. **Prompt** — style/lighting/environment/audio, NOT body motion. CLIPTextEncode positive; optional prompt_enhance.
6. **Two-stage sampling** — Stage 1: 8 steps, CFG 1.0, euler_ancestral. LTXVCropGuides. Stage 2: x2 spatial upscale (ltx-2.5-latent-spatial-upscaler-x2) + 3-4 refine steps, re-inject first frame at higher strength.
7. **Decode + output** — video VAE + audio VAE decode → VideoCombine/official output → MP4 with synced audio. Optional Diffusion Video Decoder for sharper faces.

| Setting | Value | Notes |
|---|---|---|
| Steps (stage 1) | 8 | distilled fixed |
| CFG | 1.0 | baked in |
| Frames | 121 (8n+1) | ~5s @ 24fps |
| Resolution | 1280×720 / 736 | ÷32 |
| IC-LoRA strength | 1.0 | lower only if it fights first frame |
| First-frame strength | 0.75-0.85 (stg1) | higher stg2 |
| Character LoRA | 0.8-1.2 | total stack < ~2.0 |

**HB tips:** align pose-ref first frame to keyframe pose; one control type at a time (Pose for combat);
identical character block across related shots; generate longer for D5/D6 sync beats and cut in post;
save the graph once it passes gates (start-corr, ArcFace identity, palette, no extra people).
