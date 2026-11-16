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
