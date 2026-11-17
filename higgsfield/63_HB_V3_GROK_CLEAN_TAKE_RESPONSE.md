# 63 — HOLLOW BLOOM v3: GROK CLEAN-TAKE RESPONSE (partial)

> **Source:** Grok, responding to doc 62 handoff packet (2026-11-16)
> **Status:** PARTIAL — skeleton + examples only. Shots 03-50, most both-sides, and ~112 of 116 video prompts are NOT authored (Grok used an ellipsis pattern). Needs follow-up for the full set.
> **What's solid:** the shared style header, the example patterns (kf_01, kf_02, CU1-3, A1), the 6 cinematography answers, and the 2 example video prompts (s01a, s02a) are all complete and usable as templates.

---

## Shared Style Header (pin on every keyframe)

Photoreal, 35mm anamorphic, real skin, subtle film grain, dusk light. Fungal marsh: pale-blue mushroom towers (6-8 m), luminous spore-mist, teal-glowing water pools, blackrock causeway, gnarled mangrove roots. Glacial Colour System — teal-slate base, pale-blue bioluminescence, one molten-gold accent only. Cool side-key + blue underlight. Clear body silhouettes, depth-readable background, space for pose/depth control. Identity locked to enrolled face cards.

---

## Complete Keyframe Examples

### kf_01_start.png
Medium-wide, eye-level, locked. DD and AZ stand on the blackrock causeway at the marsh edge, facing the distant pale-blue mushroom towers. DD (bare head, floating teal-blue hair, frost-arcane Aurora Weave armor, twin crossbows lowered) three-quarter view, weight on back foot. AZ (open-face Stormlight plate, greatsword point-down) profile, grounded. Spore-mist drifts at knee height, teal water glows below. Teal-slate palette, pale-blue bioluminescence, single molten-gold rune glint on AZ's forearm. Face cards: DD front + three-quarter, AZ open-face. Audio intent: low wind, distant spore hiss.

### kf_01_end.png
Same composition. DD has shifted weight forward, crossbows half-raised. AZ's greatsword has lifted slightly off the rock. Spore-mist has thickened one layer. Palette and lighting identical. Face cards same. Audio intent: soft armor shift, water lap.

### kf_02_start.png
Medium, slight low angle. DD alone, three-quarter, drawing both crossbows in parallel. Floating teal hair lifts. Clear silhouette against mushroom towers. Depth-readable marsh layers. Face card: DD three-quarter. Audio intent: string tension creak.

### kf_02_end.png
Same frame. Crossbows fully drawn, bolts nocked, DD's gaze locked forward. Hair settled into new float position. Palette hold. Audio intent: final click of latch.

### kf_CU1_dd_eye_ignite.jpg
Extreme close-up, locked. DD's left eye filling frame, teal iris catching bioluminescent underlight, frost-arcane armor edge just visible at bottom. No helmet. Face card: DD extreme close-up. Audio intent: soft breath, distant string tension.

### kf_CU2_az_rune_wake.jpg
Extreme close-up, locked. AZ's forearm, molten-gold rune beginning to glow against Stormlight plate. Clear skin texture. Face card not required. Audio intent: low rune hum.

### kf_CU3_bloom_maw_pore.jpg
Extreme close-up, locked. Bloom's fungal maw, black veins, single pore releasing pale-blue spore mist. No human face. Audio intent: wet spore release.

### kf_A1_both_start.png
Wide, eye-level. DD left third, AZ right third, both facing Bloom direction. Clear separation, full body silhouettes, depth-readable marsh. Face cards for both. Audio intent: joint breath, distant mist.

---

## Complete Video Prompt Examples

### s01a
Start: kf_01_start.png | End: kf_01_end.png | Control: none | Frames: 121 | 1280x720 | Audio: true

The composition, subjects, teal-slate palette, pale-blue bioluminescence, dusk light and single molten-gold accent remain exactly as in the start frame. Only the named action moves. DD shifts weight onto the front foot and begins to raise both crossbows. AZ's greatsword lifts two centimeters off the rock. Spore-mist drifts one layer thicker. Audio: soft armor creak, water lap against blackrock, distant spore hiss.

### s02a
Start: kf_02_start.png | End: kf_02_end.png | Control: pose | Frames: 121 | 1280x720 | Audio: true

The composition, subjects, teal-slate palette, pale-blue bioluminescence, dusk light and single molten-gold accent remain exactly as in the start frame. Only the named action moves. DD completes the parallel draw; both crossbows lock fully drawn. Floating teal hair settles into the new position. Audio: string tension creak rising to a sharp latch click, DD's controlled breath.

---

## Cinematography Answers (all 6 — solid)

1. **IC-LoRA pose conditioning:** Best from medium-to-medium-wide frames, full-body clear silhouette, body oriented 30-45° to camera, minimal limb overlap, background separation of at least one depth layer. Avoid extreme foreshortening and heavy spore occlusion on joints.

2. **Native audio:** Short, concrete, present-tense phrases: "Audio: crossbow string snap, wet spore hiss, DD's sharp exhale." Avoid abstract adjectives. Place audio cue at end of prompt. LTX-2.5 responds cleanly to material-specific sounds (string, metal, wet fungus, breath).

3. **Two-stage upscaling:** Prefer keyframes with mix of sharp edge detail (armor, hair, weapons) and smooth areas (water, mist). Extreme high-frequency texture across the entire frame increases artifact risk. Keep important identity detail in central two-thirds.

4. **Depth control:** Cleanest maps from compositions with distinct foreground (causeway/water), midground (characters), background (mushroom towers) planes. Avoid flat mist-filled frames. Slight low or eye-level angles with visible ground plane improve depth readability.

5. **Face-card conditioning:** Attach 1-2 strongest cards per character per prompt (front + preferred three-quarter). More than two begins to over-constrain expression and lighting. For hero close-ups use matching extreme close-up card.

6. **CU inserts:** Extreme close-ups work well when the feature of interest (eye, rune, pore) is centered and surrounding area is simple. Keep the CU under 15% of original framing so the two-stage upscaler preserves texture without inventing new detail.

---

## What's Missing (need follow-up from Grok)

- kf_03_start through kf_50_end (96 keyframe prompts)
- kf_A2 through kf_F2 (12 both-sides keyframes)
- s03a through s116 (114 video/continuation prompts)

**Grok's note:** "*(Pattern continues for shots 03-50...)*" — the pattern is established but the full set is NOT authored.

---

## Assessment

The examples + cinematography answers are high quality and establish a clear, repeatable pattern. The shared style header is excellent. But this is a **starting skeleton, not the full 116-prompt package** we need. Follow-up required for the complete set.