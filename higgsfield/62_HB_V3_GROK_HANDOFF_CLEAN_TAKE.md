# 62 — HOLLOW BLOOM v3: GROK HANDOFF PACKET (CLEAN LTX-2.5 TAKE)

> **Purpose:** Author a completely fresh set of keyframe prompts and video/continuation prompts for Hollow Bloom, purpose-built for LTX-2.5 as the primary renderer. This is a clean-slate rebuild — the old prompts were authored for K6 and Wan-FC, not LTX-2.5.
>
> **Status:** READY TO SEND TO GROK. Zero-cost authoring task.

---

## 1. CANON (carry over — DO NOT rewrite)

**Story:** Hollow Bloom — 50-shot boss fight film (~4.5 min). Demon Hunter (DD) vs Retribution Paladin (AZ) in a fungal marsh.

**World:**
- Environment: fungal marsh, pale-blue mushroom towers (6-8m), luminous spore-mist, teal-glowing water pools, blackrock causeway, gnarled mangrove-roots
- Palette: Glacial Colour System — teal-slate base + pale-blue bioluminescence + ONE molten-gold accent
- Lighting: dusk, cool side-key + blue bioluminescent underlight

**Characters:**
- **DD (Demon Hunter):** enrolled face cards at `faces/dd_cards_final/` (11 files). Frost-arcane armor (Aurora Weave). Floating teal-blue hair. Twin crossbows. Agile, precise.
- **AZ (Retribution Paladin):** enrolled face cards at `faces/az_cards_final/` (20 files). Stormlight open-face plate armor. Greatsword (Oathkeeper). Grounded, heavy.
- **Bloom (boss):** plant-vine aberration (shots 37-50). No face card needed — creature.

**Dialogue:** 7 lines, MK + EN (doc 49). D5 ("Замрзни." / "Freeze.") sync-critical to shot 44. D6 ("Суди." / "Judge.") sync-critical to shot 45.

**Audio:** Native LTX-2.5 audio generation. Describe all audio in-prompt.

**Armor canonical names:** `dd_armor_<tenant>.jpg` / `az_armor_<tenant>.jpg` (hash-immune, settled).

---

## 2. RENDERER: LTX-2.5 (PRIMARY, all shots)

| Component | Detail |
|---|---|
| Transformer | ltx-2.5-22b-distilled (INT8 ConvRot, 8 steps, CFG 1.0) |
| Text encoder | gemma4-12b-with-proj-ltx-2.5 (custom LTX-tuned, NOT vanilla Gemma) |
| VAEs | video + audio (both required) |
| Identity lock | first-frame I2V (0.75-0.85) + DD character LoRA (rank 32/alpha 32) + IC-LoRA |
| Control | IC-LoRA: DWPose (pose), Video Depth Anything Large (depth) |
| Resolution | 1280x720 or 1280x736 (16:9, divisible by 32) |
| Frames | 8n+1 (121 = 5s @ 24fps) |
| Sampling | two-stage: low-res + x2 spatial upscaler + 3-4 refine steps |

---

## 3. KEYFRAME PROMPTS — author ALL 100 fresh (50 shots x start/end)

### What changed from the old keyframe prompts (why rebuild):
- Old prompts were written for K6/Wan-FC — they don't leverage LTX-2.5's identity-lock stack or native audio
- Old prompts had prompt-form weaknesses that contributed to the v1 slop (78% re-dream, 53% extra people)
- LTX-2.5's IC-LoRA control needs keyframes with clear silhouettes and depth-readable composition

### Requirements for each keyframe prompt:
1. **Camera:** shot type + angle + any movement intent
2. **Environment:** full scene description (marsh elements, lighting, palette)
3. **Character:** which character(s) + pose/action + expression
4. **Composition notes for IC-LoRA:** clear body silhouette, depth-readable background, space for pose control
5. **Palette lock:** state teal-slate + pale-blue + molten-gold explicitly
6. **Identity reference:** note which enrolled face card to use for I2V conditioning
7. **Audio intent:** what sound belongs at this moment (informs the video prompt)

### Naming:
```
kf_XX_start.png   (shot XX opening frame)
kf_XX_end.png     (shot XX closing frame)
kf_CU1_dd_eye_ignite.jpg    (CU insert, before shot 18)
kf_CU2_az_rune_wake.jpg     (CU insert, before shot 22)
kf_CU3_bloom_maw_pore.jpg   (CU insert, before shot 37)
```

### Both-sides coverage (13 additional keyframes):
Author 13 keyframes showing BOTH fighters in frame for the major combat beats (A1-F2 from doc 45 pattern). These are essential for the fight's spatial coherence.

---

## 4. VIDEO / CONTINUATION PROMPTS — author ALL 116 fresh

### Form: HOLD-form continuation prompt for LTX-2.5

Each video prompt describes:
1. **What HOLDS** (composition, subjects, palette, lighting — locked from the keyframe)
2. **The ONE action** (single active verb-phrase, present tense)
3. **Audio cue** (native LTX-2.5 audio — describe it explicitly)
4. **Camera movement** (if any) + endpoint
5. **Prop anchors** (crossbows in DD's hands / greatsword in AZ's hands — name them with their end state)

### Rules (from docs 43 + 59):
- **NEVER re-describe the scene** — the keyframe carries it. Re-describing = re-dreaming.
- **Identity stated once at most** — the keyframe + LoRA carry identity.
- **Palette lock clause:** 'The teal-slate palette, pale-blue bioluminescence, dusk light and one molten-gold accent remain exactly as in the start frame.'
- **Positive constraints only** — no named negative concepts (they get generated).
- **No generic filler** — every sentence anchors something.
- **Scene change = hard cut** to a new keyframe, never morph within a clip.
- **Audio described naturally:** 'Audio: crossbow string snap, distant spore hiss, DD's breath.'

### For pose/depth-controlled shots:
Prompt describes style + look + audio only. The IC-LoRA control video carries motion. Do NOT describe body motion in the prompt when pose control is active.

### Structure per clip:
```json
{
  "id": "sXX[a|c]",
  "shot": XX,
  "start": "kf_XX_start.png",
  "end": "kf_XX_end.png",
  "control": "none|pose|depth|pose+depth",
  "control_ref": "path/to/control.mp4 (if applicable)",
  "model": "ltx25",
  "frames": 121,
  "resolution": "1280x720",
  "audio": true,
  "prompt": "[HOLD-form continuation prompt with audio cue]"
}
```

---

## 5. CINEMATOGRAPHY QUESTIONS FOR GROK

1. **IC-LoRA conditioning:** What keyframe composition maximizes pose-control accuracy? (silhouette clarity, body orientation, background separation)
2. **Native audio:** How to write audio descriptions that produce clean, usable sound in LTX-2.5? (what level of detail, what phrasing)
3. **Two-stage upscaling:** Any composition considerations for the x2 spatial upscaler? (fine detail vs. smooth areas, where artifacts appear)
4. **Depth control:** What marsh/environment compositions give the cleanest depth maps for Video Depth Anything?
5. **Face-card conditioning:** How many face cards to attach per prompt for strongest identity without over-constraining?
6. **CU inserts:** Optimal framing for the 3 CU texture shots (DD eye, AZ rune, Bloom maw) given LTX-2.5's face rendering?

---

## 6. DELIVERABLES FROM GROK

1. **100 keyframe prompts** (50 start + 50 end), numbered kf_01_start through kf_50_end
2. **3 CU insert prompts** (kf_CU1, kf_CU2, kf_CU3)
3. **13 both-sides keyframe prompts** (A1-F2)
4. **116 video/continuation prompts** (HOLD-form, LTX-2.5-ready, with audio cues)
5. **Answers to the 6 cinematography questions above**

Format: one Markdown file, clearly sectioned, each prompt in its own block.