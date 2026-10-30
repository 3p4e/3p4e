# Film 4 *The Lunar Purge*: review of the v1 test stills, and script v2

**Date:** 2026-10-30. **Status:** script v2 is waiting for approval. No video has been generated.
**Evidence:** 8 Soul Cinema stills from the v1 script (`keyframes/film4_v1/`, local only), ~8 credits.

---

## 1. What the v1 stills proved

| # | Finding | Evidence | Severity |
|---|---|---|---|
| 1 | **The Soul paints your face onto every face in the frame.** The goddess in the moon (4.2_b) and the two angels of decay (4.3_b, 4.4A_b) came out as bald, moustached versions of you. | 4.2_b, 4.3_b, 4.4A_b | **Critical.** It breaks the story and makes the angels look comic. |
| 2 | **"Pasted selfie" look.** Your face is lit flat from the front, like the training selfies, while the scene is lit by moonlight from above. Expression is the neutral selfie face, not acting. | 4.2_b, 4.4B_b | High |
| 3 | **Costume drifts between shots.** The mace has 4 different shapes and the armour changes from scale to plate. The "two feminine eyes" symbol rendered as a whole human face on a disc, which reads as creepy or comic. | all hero frames | High: continuity |
| 4 | **Scale is wrong.** The "nine-foot" angels are the same height as you. | 4.3_b, 4.4A_b | Medium |
| 5 | **Shots without you work well.** The angels of decay and the cathedral (4.1_a / 4.1_b) are strong and on-lore. | 4.1 | Good: keep |
| 6 | **The restored Shards are close to canon** (blue hair, pearly skin, wings) but have feathered wings, not wings of light. | 4.4B_a / b | Minor |
| 7 | **The independently generated 4.4A and 4.4B don't share a composition,** so a start→end video transition between them would jump. | 4.4A_b vs 4.4B | High for the transformation shot |
| 8 | The likeness check found a face in only 2 of 8 frames (0.71 and 0.85). The detector misses small, tilted or rim-lit faces. | verify log | Tool limit: judge those frames by eye |

**Root cause of #1, #3 and #7:** Soul Cinema is a single-identity, single-image model. It cannot keep other characters' faces separate, and it can't edit an existing frame. That needs a reference-capable image-edit model.

## 2. The "initial video style" you asked me to check: it is still missing

I have **never received your original reference video**, and Gemini never described it. The only traces of it in the Gemini chat are:
- your screenshot filename `Screenshot_2026-10-30-10-11-12-188_com.google.android.googlequicksearchbox.png` (a white paper-origami seraph);
- the phrase "the celestial energy seen in the reference video" (light radiating from the chest).

So the v1 style lock ("photoreal dark fantasy, moonlight volumetrics, film grain") is my **assumption**, not your reference. **Upload the reference video and the screenshot to the same Drive folder** (or a new one) and I'll extract frames and match grade, lighting, camera language, pacing and texture before spending video credits. Without it, v2 below keeps the assumed style.

## 3. Models: revised plan with real prices (queried 2026-10-30)

| Stage | Model | Why | Cost |
|---|---|---|---|
| Hero-only plates (only your face in frame) | **Soul Cinema** + soul_id `b3ba42a8…` | Best likeness (0.85–0.87) | ~1 cr / image |
| Shots without you (angels, moon, cathedral) | **Soul Cinema without soul_id** | 4.1 proved it works | ~1 cr / image |
| Adding other characters to a hero plate; continuity edits (end frame from start frame) | **Nano Banana Pro** (image-to-image, `image_references`) | Keeps your face from the plate and gives others their own faces; edits a frame instead of re-rolling it | 2 cr / image |
| Animation (default) | **Kling 3.0 Pro**, sound off, start (+ end) frame | Start→end interpolation suits the transformation | 12.25 cr / 7 s; 17.5 cr / 10 s |
| Animation (premium, optional for one hero shot) | Cinema Studio Video 3.0, genre epic | Best motion quality, but 3–7× the price | 35 cr / 7 s @720p; 91 cr / 7 s @1080p 21:9 |
| Rejected for now | Seedance 2.0 1080p | 84 cr / 7 s; identity is already carried by the start frame | – |

**Recommendation:** Kling 3.0 Pro for all shots. Re-render only the final best shot in Cinema Studio 3.0 if Kling's motion isn't good enough.

## 4. Script v2

### Changes from v1, and why
1. **Your face is generated alone.** Every frame that contains your face starts as a Soul plate with nobody else in it. Other characters are added afterwards with Nano Banana Pro, which keeps your face from the plate (fixes #1).
2. **The goddess gets her own shot (new 4.2),** generated without the Soul, so her face is hers.
3. **Lighting and acting are directed:** a moonlight key from high camera-left, a cold rim light, the face half in shadow, and specific expressions (fixes #2).
4. **Simpler costume lock** with fewer competing details, and the same words in every shot. The symbol is now an *engraved pair of almond-shaped eyes* in an abstract style, not a face (fixes #3).
5. **Scale is stated in relation to you** ("towering head and shoulders above him") (fixes #4).
6. **The transformation end frame is an *edit* of its start frame,** so composition, camera and your pose stay identical (fixes #7).
7. **The Shards' wings are "made of light, not feathers"** (fixes #6).

### Locks (repeat word for word)

**HERO LOCK**
> a man with a completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, wearing a long hauberk of small overlapping opalescent silver scales that shimmer pale blue, one sculpted crescent-moon pauldron on his left shoulder, a deep midnight-blue silk cloak flecked with tiny points of starlight, on his chest a round silver plate engraved with an abstract pair of almond-shaped eyes ringed by seven small stars, five glowing and two dark; in his right hand a heavy silver mace with a four-flanged head shaped like four crescent moons, glowing faint pale blue

**LIGHT LOCK** (hero frames)
> lit by cold moonlight from high camera-left, his face half in shadow, soft silver rim light on his scalp and shoulders, no frontal fill light

**ANGEL OF DECAY LOCK** (×2, unchanged in substance; it worked)
> nine-foot gaunt undead angels, once female, towering head and shoulders above a man, rotting grey-violet skin streaming oily purple-black liquid corruption that pools around them, ragged wings of rotting black feathers and exposed bone, long matted grey-black hair, ruined silver priestess circlets, gaunt female faces still beautiful beneath the decay, eyes glowing dull violet

**SHARD LOCK** (×2)
> two radiant female planetars with their own delicate feminine faces, pearly-white luminous skin, long flowing blue hair drifting as if underwater, silver-glowing eyes, flowing pale robes of moonlight with silver filigree, vast translucent wings made of pearlescent light rather than feathers, silver circlets

**SET LOCK**
> a vast ruined Gothic cathedral overgrown with creeping black thorns, shattered rose window, a desecrated altar, the floor flooded with a shallow pool of oily purple-black corruption

**STYLE LOCK** (provisional until I see your reference video)
> photorealistic cinematic film still, anamorphic lens, dark-fantasy realism, volumetric moonlight, wet reflective surfaces, deep violet-black shadows and silver highlights, fine film grain

### Shots (5 shots, ~36 s)

**4.1 · The Feeding: no hero · 7 s · KEEP v1 still `4.1_a`** (approved as on-lore)
- MOTION (Kling, start = 4.1_a): *"Low-angle tracking shot gliding slowly forward between thorn-wrapped columns toward the altar. The two decayed angels feed hunched over it, liquid corruption streaming from their bodies across the floor, their rotting wings twitching. Ash drifts through faint moonbeams."*

**4.2 · The Moon Opens: no hero, no Soul · 5 s · NEW**
- STILL (Soul Cinema, no soul_id): *"Low-angle shot up through the shattered rose window of [SET LOCK]. A vast full moon fills the broken window. In its light the faint luminous face of a serene woman with dusky skin, lime-green eyes and long ivory hair forms, looking down with sorrow. Black thorns silhouetted against the moon. [STYLE LOCK]"* (Selûne's avatar features per *Faiths & Avatars* pp. 134–135)
- MOTION: *"Slow push-in toward the moon. The woman's face slowly opens her eyes; a single shaft of moonlight pours down through the window into the dark cathedral below."*

**4.3 · Descent: hero alone · 7 s**
- STILL (Soul Cinema + soul_id): *"Medium-wide shot from the cathedral floor looking up. [HERO LOCK]. He descends slowly inside a single shaft of moonlight in the dark ruined cathedral, cloak lifting around him, mace held low. Expression: jaw set, brow drawn, eyes glistening with sorrowful resolve. [LIGHT LOCK]. No other people. [SET LOCK]. [STYLE LOCK]"*
- MOTION: *"Slow dolly-in as the man descends through the shaft of moonlight and lands softly in the flooded nave; the black corruption recoils from his feet in a ring of clean stone. His cloak settles. The mace head pulses pale blue."*

**4.4 · Recognition: hero + 2 · 7 s**
- STEP 1 PLATE (Soul + soul_id): *"Medium shot, chest height. [HERO LOCK]. He stands his ground in the flooded nave, looking up at something towering in front of him, his face caught between grief and recognition. [LIGHT LOCK]. Empty space left and right of him. No other people. [SET LOCK]. [STYLE LOCK]"*
- STEP 2 EDIT (Nano Banana Pro, image_references = plate + 4.1_a): *"Keep the man from image 1 exactly as he is: same face, head, armour, pose and lighting. Add the two angels of decay from image 2, [ANGEL OF DECAY LOCK], one on each side, frozen mid-lunge with blades of violet shadow raised, staring down at the engraved symbol on his chest, recognising it. They tower head and shoulders above him."*
- MOTION: *"Slow push-in. The two decayed angels falter and halt, heads tilting as if remembering, corruption dripping from their raised blades. The man slowly lowers the mace, then in one motion slams its haft into the stone floor."*

**4.5 · The Purge: hero + 2 · 10 s · TRANSFORMATION**
- STEP 1 PLATE (Soul + soul_id): *"Wide shot at floor level, the man centred. [HERO LOCK]. He kneels on one knee, the mace haft planted in the flooded stone floor, a ring of crystalline silver moonlight bursting outward from the impact. [LIGHT LOCK]. Empty space left and right behind him. No other people. [SET LOCK]. [STYLE LOCK]"*
- STEP 2 START FRAME (Nano Banana Pro, refs = plate + 4.1_a): *"Keep the man and the light burst from image 1 exactly. Add the two angels of decay from image 2, [ANGEL OF DECAY LOCK], standing behind him on either side, caught in the silver wave, corruption boiling off them as silver mist."*
- STEP 3 END FRAME (Nano Banana Pro, ref = start frame): *"Same image, same camera, same composition, same man in the same pose, but now he is rising to his feet and all seven stars on his chest glow. The two angels have become [SHARD LOCK], kneeling with heads bowed where the angels stood. The black thorns have turned to pale silver vines, the floor is clear water reflecting the moon, and soft moonglow fills the cathedral."*
- MOTION (Kling, start + end): *"Slow sweeping orbit around the three figures in slow motion. The silver shockwave washes over the decayed angels; the rotting crust cracks and falls away in flakes that dissolve into silver mist, revealing pearly skin and unfurling blue hair, their rotting wings replaced by wings of light. They sink to their knees. Moonglow fills the vault, and the two dark stars on the man's chest ignite."*

### Budget v2

| Item | Count | Credits |
|---|---|---|
| Soul plates (4.3, 4.4, 4.5) × 2 variants | 6 | ~6 |
| Moon still 4.2 × 2 | 2 | ~2 |
| Nano Banana Pro edits (4.4, 4.5 start, 4.5 end) × 2 | 6 | 12 |
| Kling 3.0 Pro: 4.1 7 s, 4.2 5 s, 4.3 7 s, 4.4 7 s, 4.5 10 s | 5 | ~63 |
| Re-roll reserve (~30 %) | | ~25 |
| **Total** | | **≈ 110 credits** (balance before this test: 712.75) |

### Acceptance criteria per frame (before any frame goes to video)
1. Your face only on the hero; every other face is clearly a different person.
2. Head shaved, moustache present, no glasses or earrings.
3. Mace and armour match the HERO LOCK; the symbol shows eyes, not a face.
4. Moonlight comes from high left, and your face is not flat-lit.
5. Angels at least head and shoulders taller than you.
6. Likeness ≥ 0.50 where the detector finds the face; otherwise checked by eye.
