# HOLLOW BLOOM (Шупливиот Цвет) — FULL PROJECT ARCHIVE
**For sharing with another agent**  
**Generated:** 2026-11-15  
**Project:** Photoreal ~4.5-min boss-fight film (50 shots / 100 keyframes + 116 video clips)

---

## 1. PROJECT OVERVIEW & CANON

**Mission**  
Photoreal ~4.5-minute boss-fight film, 50 shots / 100 keyframes (kf_NN_start.png + kf_NN_end.png) + 116 video clips from start-frame Image-to-Video.

**Canon (fixed)**  
- **DD** = female demon hunter, bare head (no helmet/hood), glowing teal-blue hair floating weightless, frost-arcane armor, twin crossbows.  
- **AZ** = retribution paladin, full plate + helm (open/closed face), one-sided molten-gold rune-tattoo on forearm, greatsword.  
- **VILLAIN** = the Hollow Bloom: grey fungal bloom, black veins, spore-mist, tendrils, a heart.  
- **WORLD** = dying fungal marsh at dusk: pale-blue mushroom towers, luminous spore-mist, teal-glowing water, corruption ring.  
- **LOOK** = photoreal, 35mm anamorphic, real skin, film grain, dusk light; teal/slate palette, pale-blue bioluminescence, one molten-gold accent.

**Logline**  
DD and AZ enter the marsh to end the Hollow Bloom, which speaks, with a Freeze-and-Sunder combo.

**Dialogue (MK canon / EN, sparse)**  
D1 after #07 BLOOM: „Дојдовте да расцветате во мене, како сите што дојдоа пред вас.“ / "You came to bloom inside me, like all who came before you."

**Measured failures (original pipeline)**  
- 78% scene replacement (re-dream)  
- 53% extra people  
- 19% palette-flip  
Root cause: global “nothing settles into a held pose” tails + negative lists that named concepts (“morphing, drift, new people”).

---

## 2. PRODUCTION PACKAGE (CURRENT STATE)

The main production package is located at:  
`/workspace/artifacts/hollow_bloom_production/HOLLOW_BLOOM_COMPLETE_PRODUCTION_PACKAGE.md`

It contains:
- Rewritten 100 keyframe prompts (start/end pairs)
- Model-specific video motion prompts (Wan Fun Control HOLD style, LTX fallback)
- Control-video notes (DWPose, Depth Anything V2)
- Generation order recommendations
- **Negative Prompt Guidance** section (added 2026-11-15)

### Negative Prompt Guidance (summary)
**Core rule**: Naming unwanted concepts in the negative prompt increased the exact failures on LTX-2.3.

| Model | Recommendation |
|-------|----------------|
| **LTX-2.3** | Prefer none. If required: only `blur, flicker, jitter, distorted hands, extra fingers, text, watermark`. Never name morphing, extra people, or palette/identity change. |
| **Wan 2.2 Fun Control** | Optional minimal artifact list. Control video handles structure better. |
| **Qwen / K6** | Same short artifact list. |

Better alternative: put constraints in the **positive** prompt (“Lighting, color palette, subject count, and composition remain exactly as in the start frame throughout. Only [the single action] occurs.”).

---

## 3. LTX-2.3 ARCHITECTURE DEEP DIVE

### Core Specs
- **Parameters**: 22B (video stream ~14B, audio stream ~5B)
- **Architecture**: Asymmetric dual-stream Diffusion Transformer (DiT)
- **Blocks**: 48 shared blocks with bidirectional audio-visual cross-attention
- **Text encoder**: Gemma 3 12B (all 49 hidden states stacked → 8-layer connectors)
- **Objective**: Rectified flow
- **Distilled**: 8 steps, CFG=1

### Key Upgrades in 2.3 vs LTX-2
- Rebuilt VAE → sharper hair, edges, textures
- 4× larger text connector → better prompt adherence
- Improved I2V training → reduced Ken Burns freezing
- Native 9:16 + up to 4K, 24/48/50 fps
- Joint audio-video generation in one pass

### Cross-Attention Mechanism
Each block:
1. Self-attention (intra-modality)
2. Text cross-attention
3. **Bidirectional audio-visual cross-attention** (parallel, using pre-update latents)
4. Feed-forward

**Cross-attention details**:
- Cross-modality AdaLN (each stream controls receptivity via the other’s timestep)
- **1D temporal RoPE only** on Q/K during AV cross-attention (spatial dimensions ignored)
- Additional AdaLN gate regulates integration of cross-modal information

### 1D RoPE Implementation (Cross-Attention)
- Only the temporal coordinate slice is passed to RoPE for audio-visual cross-attention.
- Forces pure temporal alignment (“what audio at time *t* matches video at time *t*”).
- Enables sub-frame precise foley, impacts, and lip-sync.
- Code: `packages/ltx-core/src/ltx_core/model/transformer/rope.py` (official) and Diffusers `LTX2AudioVideoRotaryPosEmbed`.

**Implication for Hollow Bloom**: Native synchronized sound (spore impacts, ice cracks, sword strikes) is generated jointly with the picture.

---

## 4. CONTROL & PREPROCESSING RESEARCH

### Wan 2.2 Fun Control
- Multimodal control (OpenPose/DWPose, Depth, Canny, trajectory)
- High/low-noise FP8 + LightX2V 4-step LoRAs
- Strong HOLD when paired with clean control videos

### DWPose Preprocessing
- Distilled Whole-body Pose for clean skeleton control videos
- Node chain: VHS_LoadVideo → DWPreprocessor → VHS_VideoCombine
- Best for body action shots

### Depth Anything V2
- Monocular depth estimation (vitl/vits/vitg)
- Relative depth maps for spatial layout and parallax locking
- Complements DWPose for structural control

---

## 5. PROMPTING METHODOLOGY (FINAL)

### Keyframe Prompts
- One measurable change per start↔end pair
- Strong identity lock via face card + armor/weapon references
- Explicit naming of keyframe files

### Video Motion Prompts (HOLD style)
- Name the start keyframe
- One specific motion only
- Explicit HOLD-anchor: “composition, subjects and palette hold; only the named action moves”
- No global keep-moving tail
- No named-concept negatives

### Model Assignment Guidance
- **LTX-2.3 Dev**: Identity-critical close-ups, dialogue, fine hair/armor detail
- **LTX-2.3 Distilled**: Faster drafts
- **Wan 2.2 Fun Control**: Action, chaos, multi-character, when control videos are available
- **Qwen / K6**: Supporting / experimental

---

## 6. ORIGINAL HANDOFF PACKET

Full original packet (spec + all 100 keyframe prompts + all 116 video prompts) is stored at:  
`/workspace/attachments/52_GROK_HANDOFF_PACKET_HOLLOW_BLOOM.md` (220 KB)

---

## 7. FACE CARD & IDENTITY LOCK

Character face cards were generated from attached real photographs of the DD actor (olive skin, dark curly/wavy hair, short beard/mustache, brown eyes) for use as identity references in video generation. Multiple multi-view and expression sheets were produced.

---

## 8. CHRONOLOGY OF WORK IN THIS PROJECT

1. Face card creation from real photos + concept art  
2. Full Hollow Bloom handoff packet received  
3. Keyframe prompt rewriting (Q1)  
4. Model review (LTX-2.3, Wan, Qwen/K6) + better model recommendations  
5. Deep exploration of Wan 2.2 Fun Control, DWPose, Depth Anything V2  
6. Complete production package creation  
7. LTX-2.3 fallback prompt review  
8. Negative prompt guidance added  
9. LTX-2.3 architecture investigation (dual-stream, cross-attention, 1D RoPE)  
10. This archive created

---

## 9. FILES IN THIS ARCHIVE

| File | Location | Description |
|------|----------|-------------|
| This archive | `/workspace/artifacts/hollow_bloom_archive/HOLLOW_BLOOM_FULL_PROJECT_ARCHIVE.md` | Master overview |
| Production package | `/workspace/artifacts/hollow_bloom_production/HOLLOW_BLOOM_COMPLETE_PRODUCTION_PACKAGE.md` | Prompts, methodology, negatives |
| Original packet | `/workspace/attachments/52_GROK_HANDOFF_PACKET_HOLLOW_BLOOM.md` | Full original handoff |

---

**End of Archive**  
*Ready for handoff to another agent. All major decisions, failure analyses, architecture findings, and prompting rules are captured above.*
