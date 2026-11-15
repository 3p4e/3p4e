# HOLLOW BLOOM — COMPLETE PRODUCTION PACKAGE
# Ready-to-use keyframe + video prompts + pipeline order
# Generated for actual video production

## 0. HOW TO ACTUALLY GENERATE THE FILM (recommended order)

1. Generate all 100 keyframes first (use the prompts in Section 1).  
   - Attach the exact reference images listed.  
   - Prefer a strong identity-locked image model (Flux, SD3, or the image model you trust most for faces).  
   - Save exactly as kf_01_start.png … kf_50_end.png.

2. Prepare control videos where needed (Section 3).  
   - Character action shots → DWPose control video from a clean real/realistic reference.  
   - Environment/spatial shots → Depth Anything V2 control video.  
   - Pure atmosphere or wide chaos → no control video required.

3. Generate video clips (Section 2).  
   - Primary model: Wan 2.2 Fun Control (with preprocessed control video when available).  
   - Identity-critical close-ups: LTX-2.3 Dev 30-step if Fun Control loses hair detail.  
   - Wide chaos / thrash: LTX Distilled or Qwen/K6 acceptable.  
   - Always use the HOLD-style motion prompts below.

4. Assemble in editing software. Match frame counts and FPS (recommend 16 fps, ≤81 frames per clip for best Wan alignment).

Shared style header for every keyframe (do not repeat in every prompt if your interface allows a style prefix):  
Photoreal cinematic still, 35mm anamorphic, real skin, fine film grain, dusk light, teal/slate palette with pale-blue bioluminescence and one molten-gold accent.

---

## 1. KEYFRAME IMAGE PROMPTS (all 100)

Each pair is the first and last frame of one continuous movement.  
Start = opening beat. End = completed action. Identity locked with positive language only.

### SHOT 1 — stand on hummock, dolly-in
**kf_01_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg, set_plate.jpg  
Photoreal cinematic still. Demon hunter DD (bare head, glowing teal-blue hair floating weightless, frost-arcane armor) and paladin AZ (full plate, face visible, molten-gold forearm rune, greatsword) stand on a hummock at the grey corruption ring edge. Mist drifts. Giant pale-blue mushroom towers, teal-glowing water. Camera begins slow dolly-in. Opening frame.

**kf_01_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg, set_plate.jpg  
Same characters and location. Dolly-in completed; they are closer in frame, still standing, mist continuing. Corruption edge visible at their feet. End frame.

### SHOT 2 — corruption advances
**kf_02_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg, set_plate.jpg  
DD and AZ face the creeping grey corruption. Blight edge sits a short distance ahead. Slow push begins. Opening frame.

**kf_02_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg, set_plate.jpg  
Same framing. Grey corruption has advanced roughly a handspan closer. Push complete. End frame.

### SHOT 3 — cock crossbow
**kf_03_start.png**  
Attach: dd_face.jpg, dd_weapon.jpg  
DD alone, bare head, teal hair weightless. She begins cocking one crystal crossbow. Frost starts forming on the bolt. Opening frame.

**kf_03_end.png**  
Attach: dd_face.jpg, dd_weapon.jpg  
Crossbow fully cocked. Frost-arrow fully crystallised in the groove. End frame.

### SHOT 4 — hair wave + freeze spores
**kf_04_start.png**  
Attach: dd_face.jpg  
DD’s glowing teal-blue hair begins a slow weightless roll. Neon teal brightens. Nearby spores start to freeze. Opening frame.

**kf_04_end.png**  
Attach: dd_face.jpg  
Hair has completed the wave. Teal fully bright. Spores have frozen and are falling. End frame.

### SHOT 5 — AZ rune wakes
**kf_05_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
AZ’s gauntlet grips the greatsword hilt. Molten-gold rune-tattoo begins to wake along the wrist. Opening frame.

**kf_05_end.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
Grip firm. Rune fully ember-gold and active. End frame.

### SHOT 6 — Bloom rises
**kf_06_start.png**  
Attach: boss_main.jpg, set_plate.jpg  
Hollow Bloom (corpse-flower maw, braided black-green vines, spore-sacs, root-feet) begins rising from the corrupted patch. Spore-sacs start inflating. Opening frame.

**kf_06_end.png**  
Attach: boss_main.jpg, set_plate.jpg  
Fully risen. Maw open. Spore-sacs inflated. End frame.

### SHOT 7 — tendril snaps
**kf_07_start.png**  
Attach: boss_main.jpg  
A thorned tendril coils tight. Opening frame.

**kf_07_end.png**  
Attach: boss_main.jpg  
Tendril has snapped fully open. End frame.

### SHOT 8 — Glacial Aura
**kf_08_start.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
DD raises an arm. Rotating frost-and-sigil ring begins to bloom. Opening frame.

**kf_08_end.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
Full rotating frost-and-sigil ring active. Nearby spores crystallising and falling. End frame.

### SHOT 9 — tendril whip
**kf_09_start.png**  
Attach: boss_main.jpg  
Tendril whip begins its swing. Opening frame.

**kf_09_end.png**  
Attach: boss_main.jpg  
Whip complete. Blight-furrow gouged across the marsh. End frame.

### SHOT 10 — Frost Rush
**kf_10_start.png**  
Attach: dd_face.jpg  
DD kicks off. Ice comet begins forming. Opening frame.

**kf_10_end.png**  
Attach: dd_face.jpg  
Full Frost Rush in flight over the water, rime trail behind. End frame.

### SHOT 11 — dual crossbow fire
**kf_11_start.png**  
Attach: dd_face.jpg, dd_weapon.jpg  
DD fires both crossbows. Bolts just leaving. Opening frame.

**kf_11_end.png**  
Attach: dd_face.jpg, dd_weapon.jpg  
Three crystalline frost-bolts streaking forward. End frame.

### SHOT 12 — bolts freeze tendril
**kf_12_start.png**  
Attach: dd_weapon.jpg, boss_main.jpg  
Frost-bolts strike a tendril. Flash-freeze begins. Opening frame.

**kf_12_end.png**  
Attach: boss_main.jpg  
Freeze complete. Vine brittle white. End frame.

### SHOT 13 — gold shockwave
**kf_13_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
AZ plants the greatsword tip. Gold shockwave begins. Opening frame.

**kf_13_end.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
Shockwave has cracked the corrupted floor. End frame.

### SHOT 14 — radiant arc
**kf_14_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
AZ begins a radiant two-handed swing. Opening frame.

**kf_14_end.png**  
Attach: az_armor_base.jpg, boss_main.jpg  
Arc detonates on the Bloom. End frame.

### SHOT 15 — Bloom reels
**kf_15_start.png**  
Attach: boss_main.jpg  
Bloom begins to reel. Maw twists. Spore-sacs flare. Opening frame.

**kf_15_end.png**  
Attach: boss_main.jpg  
Full reel completed. Maw twisted, sacs brighter. End frame.

### SHOT 16 — heroes vault
**kf_16_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg, boss_main.jpg  
Bloom sweeps a tendril. DD and AZ begin vaulting opposite ways. Opening frame.

**kf_16_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
Both heroes airborne, moving opposite. End frame.

### SHOT 17 — DD lands
**kf_17_start.png**  
Attach: dd_face.jpg  
DD in mid-flip. Frost-smoke curling. Opening frame.

**kf_17_end.png**  
Attach: dd_face.jpg  
Landed in crouch. Frost-smoke settling. End frame.

### SHOT 18 — white-blue lances
**kf_18_start.png**  
Attach: dd_face.jpg  
DD’s eyes ignite. Twin white-blue lances begin to form. Opening frame.

**kf_18_end.png**  
Attach: dd_face.jpg  
Lances fully slashed out. End frame.

### SHOT 19 — Freeze-and-Sunder combo
**kf_19_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg, boss_main.jpg  
DD’s Rime Beams freeze a tendril mid-swing. AZ’s Verdict begins. Opening frame.

**kf_19_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg, boss_main.jpg  
Verdict shatters the frozen tendril in a golden shockwave. End frame.

### SHOT 20 — Bloom staggers
**kf_20_start.png**  
Attach: boss_main.jpg  
Frozen vine begins to fracture. Maw opens. Opening frame.

**kf_20_end.png**  
Attach: boss_main.jpg  
Vine fully fractured. Maw in silent roar. End frame.

### SHOT 21 — spore-sacs rupture
**kf_21_start.png**  
Attach: boss_main.jpg  
Bloom hunches. First spore-sacs begin to rupture. Opening frame.

**kf_21_end.png**  
Attach: boss_main.jpg  
Multiple sacs ruptured in sequence. End frame.

### SHOT 22 — light-blade summons
**kf_22_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
AZ raises the sword. Light-blade begins to form above. Opening frame.

**kf_22_end.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
Light-blade fully summoned. End frame.

### SHOT 23 — light-blade plunges
**kf_23_start.png**  
Attach: az_armor_base.jpg, boss_main.jpg  
Light-blade begins its plunge. Opening frame.

**kf_23_end.png**  
Attach: az_armor_base.jpg, boss_main.jpg  
Plunge complete. Bloom staggered under white pillar. End frame.

### SHOT 24 — spore rain
**kf_24_start.png**  
Attach: boss_main.jpg, set_plate.jpg  
Root-feet slam. Spore rain begins. Sky starts dimming green. Opening frame.

**kf_24_end.png**  
Attach: boss_main.jpg, set_plate.jpg  
Full spore rain. Sky dim green. End frame.

### SHOT 25 — Glacial Aura shelter
**kf_25_start.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
DD curls under her wings. Glacial Aura forms. Spores begin turning to snow. Opening frame.

**kf_25_end.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
Full shelter. Spores hissing to snow on the membrane. End frame.

### SHOT 26 — AZ strides through rain
**kf_26_start.png**  
Attach: az_armor_base.jpg  
AZ begins striding through spore rain. Light starts shedding it. Opening frame.

**kf_26_end.png**  
Attach: az_armor_base.jpg  
Stride complete. Ground flushed teal at his boots. End frame.

### SHOT 27 — spore gout
**kf_27_start.png**  
Attach: boss_main.jpg  
Bloom exhales. Choking green spore gout begins rising. Opening frame.

**kf_27_end.png**  
Attach: boss_main.jpg  
Full rising column of spore gout. End frame.

### SHOT 28 — vault + charge
**kf_28_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
DD begins vaulting the gout. AZ begins charging through its shadow. Opening frame.

**kf_28_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
DD over the gout, AZ through the shadow. End frame.

### SHOT 29 — white-gold cone
**kf_29_start.png**  
Attach: az_armor_base.jpg  
AZ stands square. White-gold cone begins scouring the ground. Opening frame.

**kf_29_end.png**  
Attach: az_armor_base.jpg  
Cone complete. Blight receded in a wave. End frame.

### SHOT 30 — snow coils
**kf_30_start.png**  
Attach: dd_face.jpg  
DD winds up. Wings fold. Snow coils begin concentrating. Opening frame.

**kf_30_end.png**  
Attach: dd_face.jpg  
Full concentration of snow coils. End frame.

### SHOT 31 — dive
**kf_31_start.png**  
Attach: dd_face.jpg, dd_weapon.jpg  
DD begins dive, lance-first, crossbows leading. Frozen trail starts. Opening frame.

**kf_31_end.png**  
Attach: dd_face.jpg, dd_weapon.jpg  
Full dive with frozen trail. End frame.

### SHOT 32 — impact
**kf_32_start.png**  
Attach: boss_main.jpg, dd_face.jpg  
Impact begins. Crater forms. Spore-sacs flicker. Opening frame.

**kf_32_end.png**  
Attach: boss_main.jpg  
Bloom forced to one root-knee. End frame.

### SHOT 33 — Hoarfrost Judgement
**kf_33_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg, boss_main.jpg  
AZ marks the sac-cluster with a rune. DD’s frost begins locking it. Opening frame.

**kf_33_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg, boss_main.jpg  
Rune detonates in a light column. End frame.

### SHOT 34 — runes blaze
**kf_34_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
AZ regrips. Holy runes begin blazing up the blade. Opening frame.

**kf_34_end.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
Runes fully blazing. End frame.

### SHOT 35 — Bloom enrages
**kf_35_start.png**  
Attach: boss_main.jpg  
Bloom begins to swell. Spores spiral into a vortex. Opening frame.

**kf_35_end.png**  
Attach: boss_main.jpg  
Fully enraged, open, vortex active. End frame.

### SHOT 36 — spore-voice
**kf_36_start.png**  
Attach: boss_main.jpg  
Maw begins opening full. Opening frame.

**kf_36_end.png**  
Attach: boss_main.jpg  
Maw fully open. Spore-voice moment. End frame.

### SHOT 37 — Pollen Nova
**kf_37_start.png**  
Attach: boss_main.jpg, set_plate.jpg  
Pollen Nova ignites. Spore supernova begins rising. Opening frame.

**kf_37_end.png**  
Attach: boss_main.jpg, set_plate.jpg  
Nova drowning the marsh light. End frame.

### SHOT 38 — glacier peak
**kf_38_start.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
Wing-flare begins. Crossbows raised. Glacier energy peaks. Opening frame.

**kf_38_end.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
Full peak. End frame.

### SHOT 39 — golden wings
**kf_39_start.png**  
Attach: az_armor_base.jpg  
AZ plants his hands. Tattoo surges gold-to-white. Golden wings begin blooming. Opening frame.

**kf_39_end.png**  
Attach: az_armor_base.jpg  
Golden wings fully bloomed. End frame.

### SHOT 40 — still beat
**kf_40_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
Both heroes hold under the rising spore-nova. Opening of the still beat.

**kf_40_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
Same hold, slightly closer or more resolved. End of the still beat.

### SHOT 41 — Glacier Form leap
**kf_41_start.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
DD begins leap in full Glacier Form. Immortal wings wide. Opening frame.

**kf_41_end.png**  
Attach: dd_face.jpg, dd_armor_state.jpg  
Full leap, snowstorm against the spores. End frame.

### SHOT 42 — AZ radiant rise
**kf_42_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
AZ begins rising. Greatsword burning white-gold. Opening frame.

**kf_42_end.png**  
Attach: az_armor_base.jpg, az_weapon.jpg  
Fully radiant. End frame.

### SHOT 43 — Blizzard & Verdict combo
**kf_43_start.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
Both launch together. Frost streak and gold streak begin winding. Opening frame.

**kf_43_end.png**  
Attach: dd_face.jpg, az_armor_base.jpg  
Full intertwined streaks. End frame.

### SHOT 44 — Rime Beams + crossbows
**kf_44_start.png**  
Attach: dd_face.jpg, dd_weapon.jpg, boss_main.jpg  
DD fires Rime Beams and both crossbows. Violet-white lance begins punching through. Opening frame.

**kf_44_end.png**  
Attach: dd_face.jpg, boss_main.jpg  
Lance through the Bloom heart. End frame.

### SHOT 45 — final Verdict
**kf_45_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg, boss_main.jpg  
Final Verdict arc begins. Opening frame.

**kf_45_end.png**  
Attach: az_armor_base.jpg, boss_main.jpg  
Arc splits the Bloom. Light floods out. End frame.

### SHOT 46 — Nova collapses
**kf_46_start.png**  
Attach: boss_main.jpg, set_plate.jpg  
Pollen Nova begins collapsing inward. Light versus spore. Opening frame.

**kf_46_end.png**  
Attach: boss_main.jpg, set_plate.jpg  
Collapse advanced. End frame.

### SHOT 47 — head wilts
**kf_47_start.png**  
Attach: boss_main.jpg  
Corpse-flower head begins to crack. Opening frame.

**kf_47_end.png**  
Attach: boss_main.jpg  
Head folded shut and wilted. End frame.

### SHOT 48 — spores settle
**kf_48_start.png**  
Attach: set_plate.jpg  
Spores begin settling like grey snow. Two silhouettes over the purifying patch. Opening frame.

**kf_48_end.png**  
Attach: set_plate.jpg  
Spores mostly settled. Silhouettes clear. End frame.

### SHOT 49 — DD almost smiles
**kf_49_start.png**  
Attach: dd_face.jpg  
DD exhales a wisp of frost. Hair begins dimming to idle gradient. Opening frame.

**kf_49_end.png**  
Attach: dd_face.jpg  
Wisp finished. Hair at idle. She almost smiles. End frame.

### SHOT 50 — AZ turns, dawn
**kf_50_start.png**  
Attach: az_armor_base.jpg, az_weapon.jpg, set_plate.jpg  
AZ begins turning, greatsword over shoulder. Dawn starts breaking. Marsh water begins glowing teal. Opening frame.

**kf_50_end.png**  
Attach: az_armor_base.jpg, az_weapon.jpg, set_plate.jpg  
Turn complete. Dawn full. Water glowing teal again. End frame.

---

## 2. VIDEO MOTION PROMPTS (Wan 2.2 Fun Control primary)

Use these with the matching start keyframe.  
Template:  
Using start frame kf_XX_start.png.  
Composition, subjects, lighting direction, palette and subject count hold.  
Only [action] moves.  
[Control note if used.]  
Camera locked.

Examples (apply the same pattern to every shot):

- Shot 1: Using start frame kf_01_start.png. Composition, subjects, lighting direction, palette and subject count hold. Only the slow dolly-in and light mist drift move. Camera locked.
- Shot 3: Using start frame kf_03_start.png. Composition, subjects, lighting direction, palette and subject count hold. Only the crossbow cock and frost crystallising on the bolt move. Driven by DWPose control video. Camera locked.
- Shot 9: Using start frame kf_09_start.png. Composition, subjects, lighting direction, palette and subject count hold. Only the tendril whip and the blight furrow it gouges move. Driven by Depth Anything V2 control video for geometry. Camera locked.
- Shot 11: Using start frame kf_11_start.png. Composition, subjects, lighting direction, palette and subject count hold. Only the dual crossbow fire and the three frost-bolts streaking forward move. Driven by DWPose control video. Camera locked.
- Shot 19: Using start frame kf_19_start.png. Composition, subjects, lighting direction, palette and subject count hold. Only the Freeze-and-Sunder combo (Rime Beams freezing the tendril, then Verdict shattering it) moves. Driven by DWPose + Depth control. Camera locked.
- Shot 49: Using start frame kf_49_start.png. Composition, subjects, lighting direction, palette and subject count hold. Only the frost wisp exhalation and hair dimming to idle move. Camera locked.

For LTX-2.3 (fallback on identity-critical close-ups):  
Same HOLD structure, add “Nothing else changes.” Use Dev 30-step for faces/hair, Distilled for chaos.

---

## 3. CONTROL VIDEO RECOMMENDATIONS PER SHOT TYPE

| Shot type | Control | Source advice |
|-----------|---------|---------------|
| DD / AZ precise body action (draw, fire, vault, sword raise, dive) | DWPose | Clean real or realistic reference of the action. detect_hand + detect_body on. |
| Bloom tendril / spatial geometry / marsh layout | Depth Anything V2 (vitl) | Matching setting plate or previous pass. |
| Combos involving both heroes + Bloom | DWPose (heroes) + Depth (environment) | Blend or multi-control if workflow supports it. |
| Pure atmosphere, wide corruption widen, dawn, spore settle | None | Start keyframe + HOLD prompt only. |
| Extreme close-ups of face/hair | None or very light | Prefer LTX Dev if Fun Control softens hair. |

Disable built-in preprocessing in the Fun Control template once you have preprocessed videos.

---

## 4. MODEL ASSIGNMENT SUMMARY

- Primary for almost every shot: Wan 2.2 Fun Control + appropriate control video + HOLD prompt.  
- Identity-critical CU (shots with strong DD hair or face focus, e.g. 4, 49): LTX-2.3 Dev 30-step if hair detail fails.  
- Violent thrash / wide chaos (shots 6–9, 15, 21, 24, 35–37, 46–47): LTX Distilled or Qwen/K6 acceptable; drift reads as energy.  
- Transform / combo peaks (19, 33, 43–45): Fun Control first; Distilled LTX as energetic fallback.

---

End of production package.  
Generate keyframes first, prepare control videos for action shots, then run video clips with the HOLD prompts. Assemble in post.

---

## 5. NEGATIVE PROMPT GUIDANCE

### Core rule learned from Hollow Bloom tests
Naming unwanted concepts in the negative prompt (especially “morphing”, “drift”, “extra people”, “new characters”, “scene change”) **increased** the exact failures it tried to prevent on LTX-2.3 (78% re-dream, 53% extra people). The model treated the named terms as additional concepts to generate.

### Model-specific guidance

#### LTX-2.3 (Dev and Distilled)
- **Prefer no negative prompt at all** for image-to-video.
- If the interface requires one, use only short, generic artifact terms:
  ```
  blur, flicker, jitter, distorted hands, extra fingers, text, watermark
  ```
- **Never** include: morphing, drift, extra people, new characters, scene replacement, palette change, identity change, or any description of the failure modes you saw.
- Rely on a strong start frame + high image strength + the positive HOLD-style paragraph instead of negatives.

#### Wan 2.2 Fun Control
- Negatives are less harmful but still secondary to a clean control video and a tight positive prompt.
- Safe minimal negative (optional):
  ```
  blur, low quality, extra limbs, extra fingers, text, watermark
  ```
- Do not list “extra people” or “morphing”. The DWPose/Depth control video already constrains subject count and structure far more effectively than any negative.

#### Qwen / K6 / other distilled models
- Same minimal list as Wan.
- Keep negatives short. Long negative lists dilute the positive prompt.

### Recommended practice for the film
1. Generate the first pass with **no negative prompt** (or only the 6–7 generic artifact terms above).
2. If a specific artifact appears (e.g. extra fingers on a weapon hand), add **only that artifact** to the negative for a re-roll of that single shot.
3. Never add a global “anti-re-dream” negative list to every shot. It made the problem worse on LTX.

### Positive constraints that replace negatives
These belong in the **positive** prompt and are more effective:
- “Lighting, color palette, subject count, and composition remain exactly as in the start frame throughout.”
- “Camera stays locked-off.”
- “Only [the single named action] occurs.”

Use these instead of trying to forbid failure modes in the negative field.
