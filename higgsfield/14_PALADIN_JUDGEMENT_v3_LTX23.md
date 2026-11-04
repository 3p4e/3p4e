# The Paladin's Judgement v3: LTX-2.3 open-source batch

Adapted from `08_PALADIN_JUDGEMENT_v2.md` after a live model re-selection (2026-11-03).
Target stack: LTX-2.3 22B distilled (Community License, no territory ban, personal use OK) on a rented Vast.ai GPU through ComfyUI + ComfyUI-LTXVideo (LTXV* nodes). Keyframes already generated locally (Gemini, free) and gated.

## 0. Why we changed the stack

| Candidate | Verdict | Evidence |
|---|---|---|
| Wan 2.2 14B I2V (v2 stack) | keep only as fallback | 832x480@16fps upscaled = soft/smeary; the word the director used was "terrible" |
| Wan 2.2 TI2V-5B | rejected | measured 33:53 per 5s clip vs 80s (25x slower), no 5B distill LoRA |
| **LTX-2.3 22B distilled** | **chosen** | ungated, 8-step distilled CFG=1, native 720p/24, 121 frames = 5.04s, keyframe interpolation |
| LTX-2.5 | blocked | HF `resolve` returns HTTP 403 (account not granted access) even with a valid Read token |
| HunyuanVideo 1.5/2.0 | illegal | license line 3 excludes EU/UK/South Korea |

## 1. LTX-2.3 prompt engineering (verified from primary sources)

- **One prompt per shot**, not keyframe-lock + short-motion split. LTX-2.3 reads rich cinematic prose: camera, subject detail, action, environment, light, and (optionally) sound cues in a single string.
- **Positive wording, one mover.** Keep the v2 rule: camera OR subject OR light moves. LTX obeys one clear action and smears the rest.
- **Landscape is explicit.** Native default is 1024x1536 portrait; landscape requires `--width/--height` (Comfy nodes: `EmptyLTXVLatentVideo`) divisible by 32. We use 960x544 (the official stream example) for a 16:9 film.
- **Distilled schedule = 8 steps.** Distilled sigma string from the official workflow: `1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0` (9 sigmas = 8 denoise steps). No CFG (CFG=1).
- **121 frames at 24 fps = 5.04 s per clip.** The VAE grid is 8k+1; 121 is the documented standard.
- **Keyframe interpolation** (shot 1.4) binds two stills by frame index via guide conditioning, not a separate FLF node.
- **Faces only in medium/close shots.** Confirmed again by the Gemini keyframe gate: the two-subject action frame mangled the face (+271%/+334% geometry), the static close frames passed (0.65-0.70).

## 2. Keyframes (already generated, SFace-gated)

All four hero keyframes pass the project likeness gate `>= 0.50 mean, geometry OK`:

| Frame | Gate (mean / geom) | Use |
|---|---|---|
| p1_1 | 0.692 / OK | shot 1.1 start |
| p1_2 | NO FACE (skeletal king, expected) | shot 1.2 start |
| p1_3 | 0.661 / OK | shot 1.3 start |
| p1_4a | 0.696 / OK | shot 1.4 frame 0 (hero, hammer planted, rune ring) |
| p1_4b | 0.652 / OK | shot 1.4 frame 120 (kneeling in rune circle, ash + fallen crown) |

Hero identity: `media/refs/A_bust.png`, `media/refs/sheet_front.png`. No real photos go to the GPU.

## 3. v3 shot list (20 s, LTX prompts)

HERO: "a broad-shouldered man, shaved bald head, clean-shaven, weathered skin, calm grave eyes, heavy articulated silver plate armour with gold runes, thick white wolf-fur mantle, long white tabard with a gold sunburst, two-handed warhammer with a gold-inlaid square head"
KING: "a towering skeletal king, blackened bones in rusted frost-rimed plate, jagged iron crown fused to the skull, hollow eye sockets glowing pale cyan, ribcage lit sickly green, rune-etched broadsword"
STYLE: "photorealistic cinematic still, anamorphic framing, shallow depth of field, volumetric backlight through blizzard, film grain, muted steel-blue grade, warm gold only from the hero"

| Shot | Keyframe | LTX prompt (one string) | Mover |
|---|---|---|---|
| 1.1 | p1_1 | "{HERO}. {STYLE}. Wide shot on a glacier ridge, the hero stands head bowed, both hands on the hammer haft planted in the snow, snow settling around him. The camera slowly pushes in. No other movement." | camera |
| 1.2 | p1_2 | "{KING}. {STYLE}. Low-angle shot in the blizzard, the sword point driven into the ice, green light blazing from the ribcage. The king slowly raises its skull. The camera holds low and still." | head |
| 1.3 | p1_3 | "{HERO}. {STYLE}. Medium close-up, chest up, calm and resolute, face sharply in focus. The gold light from his chest runes slowly brightens and rims his jaw. The camera does not move." | light |
| 1.4 | p1_4a (frame 0) + p1_4b (frame 120) | "{HERO}. {STYLE}. Keyframe interpolation: the golden rune ring on the ice spreads outward and the skeletal king distant burns to ash, resolving to the hero kneeling inside a circle of golden runes, a column of ash and a fallen iron crown beside him, a shaft of sunlight breaking through." | ring/change carried by end frame |

Order: 1.1 (5.04s) > 1.2 (5.04s) > 1.3 (5.04s) > 1.4 (5.04s). Hard cuts. Sound: wind bed throughout, low drone rising through 1.3, impact + ember hiss on 1.4 (procedural ffmpeg, no model).

## 4. Batch design (one GPU session)

1. Rent a 48GB-class verified card (RTX A6000/A100 PCIE 40G) on the official vastai/comfy template (hash 2188dfd3e0a0b83691bb468ddae0a4e5).
2. Install ComfyUI-LTXVideo custom nodes (git clone into custom_nodes, restart ComfyUI).
3. Download LTX-2.3 distilled checkpoint + spatial upscaler x2 + temporal upscaler x2 + Gemma text encoder + audio VAE to the documented folders.
4. Push the 5 keyframes to ComfyUI input/.
5. Submit 4 clips via /prompt using the official two-stage distilled I2V workflow, patched per shot (image, prompt, 960x544, 121 frames, distilled sigmas, seed 100+index).
6. Pull each clip over SSH **and ffprobe + checksum before deleting anything**.
7. Assemble with ffmpeg (hard cuts, grade, procedural sound), stamp the manifest.
8. Destroy the instance only after every clip is verified locally.

Quality gate: hero keyframes already >= 0.50. Any clip with new objects (people, animals, vehicles) is regenerated once with a new seed.

## 5. Risks (honest)

- Custom-node install + Gemma encoder path on the template is the main failure surface; the preflight prints mismatches to the job channel and I adapt (same pattern as the Wan batch that worked).
- LTX landscape output is off-native-orientation; quality at 960x544 is documented but may be slightly weaker than portrait. Two-stage upsampling mitigates.
- 22B distilled at bf16 needs ~48GB; fp8 (Kijai `transformer_only_fp8_scaled`) is the fallback if the A100 40G OOMs.
- Skeleton king is far from the tested face scenes: expect one regen.

## 6. Cost

Paladin is 4 clips (~20s), far smaller than Karsus. Projected: downloads (~70GB) + 4x 5s renders on a $0.40-0.46/h 48GB class ≈ **$1.5-2.5**, hard cap $4.00. Credit at start: $8.838.

## References
- Lightricks. LTX-2.3 weights (ungated, distilled-1.1, upscalers). https://huggingface.co/Lightricks/LTX-2.3
- Lightricks. LTX-2.x Community License Agreement. https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2
- Lightricks. ComfyUI-LTXVideo (LTXV* nodes, 32GB+ VRAM, 100GB disk). https://github.com/Lightricks/ComfyUI-LTXVideo
- Lightricks. LTX-2 pipelines docs (DistilledPipeline 8+4 steps, keyframe interpolation, I2V conditioning). https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-pipelines/docs/pipelines.md
- Kijai. LTX2.3_comfy fp8 split files (fallback). https://huggingface.co/Kijai/LTX2.3_comfy
- Wan-AI. Wan2.2 models (Apache-2.0). https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- Tencent Hunyuan. HunyuanVideo license (EU/UK/South Korea excluded). https://github.com/Tencent-Hunyuan/HunyuanVideo/blob/main/LICENSE.txt
