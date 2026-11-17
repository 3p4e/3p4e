# Reference video: style analysis, and Film 4 v3 rewritten in that style

**Source:** your reference video (Drive, 2026-10-30). 1:40 (99.99 s), 1280×720 HEVC with AAC audio. It's a phone screen recording of a social-media post (UI overlays in the first and last frames). Kept locally at `keyframes/_reference/` (not in git). A 24-frame style board was sent to you separately.

---

## 1. What the reference actually is

### 1.1 Story structure: a **litany**
The voice-over is a sparse, solemn English monologue (transcribed with Whisper; small model, so some words are uncertain):

> "In the beginning there was darkness. **Gabriel** grants you voice. [**Uriel**] grants punishment. **Jegudiel** grants heavenly lightning. **Barachiel** grants love. **Raphael** grants healing. **Selaphiel** grants prayer. … [the monster speaks] … **Jeremiel** grants purification of the soul. … You never knew the love of God."

These are the **seven archangels of the Orthodox and Catholic tradition** (Gabriel, Uriel, Jegudiel, Barachiel, Raphael, Selaphiel, Jeremiel; the hero is implicitly Michael). The film is a call-and-response:

> **one line naming an angel and its gift → one visual set piece showing that gift hitting the monster**

| Time | Invocation | Visual set piece |
|---|---|---|
| 0–16 s | "In the beginning…", Gabriel (voice) | Red dust desert at dusk, then a black void; the hero speaks to camera; the monster crawls |
| 17–24 s | Uriel (punishment) | Burning suns rain down as a fire comet and explosion |
| 27–30 s | Jegudiel (lightning) | A flaming demon face, then a fan of white-blue lightning |
| 33–40 s | Barachiel (love) | The paper monster crumbles into **white roses** (Barachiel's traditional emblem) |
| 41–47 s | Raphael (healing) | A tidal wave of ice-blue water |
| 48–55 s | Selaphiel (prayer) | Thousands of floating lit candles in the void |
| 56–77 s | The monster's answer | It rises in a violet nebula; a giant toothed face with a veil of pale hair |
| 78–90 s | Jeremiel (purification) | The hero pushes his hand at the lens; a violet pillar of light; the monster burns from inside |
| 91–100 s | "You never knew the love of God." | Tears, eyes closed, face cracking with light; fade |

### 1.2 Visual grammar
- **A/B alternation.**
  - (A) **Frontal, symmetric close-ups** of the hero talking to camera. Crown centred, shallow depth of field, hands reaching into the lens with strong foreshortening.
  - (B) **Extreme wide shots** on a **black void stage with a wet, mirror-black floor**. A tiny glowing white figure faces a colossal creature. Almost no set.
- **The hero is the light source.** A glowing sapphire-blue gem at the sternum and blue-glowing crystals along the robe seams; otherwise near-black frames.
- **One saturated colour per beat:** orange fire, blue-white lightning, white roses, ice-blue water, amber candles, violet purification. The base palette is black, ivory and ice-blue.
- **Camera:** mostly locked or a slow push-in. Hard cuts on the beat. About 35 shots in 100 s (average shot length ~2.8 s). Macro inserts: candle flame, burning paper, lips.
- **Sound:** voice-over plus a choral or ambient score with heavy low end.

### 1.3 Character design
- **Hero:** ivory and white **ceremonial ecclesiastical cape** with a very high stiff collar, quilted embroidery, pearls, glowing sapphire crystals, a gem at the sternum, and a **silver crystalline crown of thorns**. Unarmed: all power comes from hand gestures.
- **Monster (the "paper seraph"):** a colossal emaciated fallen angel whose **skin is made of old book pages printed in blackletter script**. It has rib-like page layers, a **halo of concentric iron thorn rings**, chained wrists, a gaping mouth of needle teeth and amber eyes. Its final form is a violet cosmic veiled giant.

### 1.4 What this changes in everything we've done

| Earlier assumption | Reality from the video | Consequence |
|---|---|---|
| Gemini: "the paper seraph is the hero; put your face on it" | **The paper creature is the monster.** The hero is the white saint. | You can still play a paper seraph, but that's a *new* idea, not "like the video". Your call (see §4). |
| My v1/v2: dark-fantasy realism in full environments (cathedral, glacier) | Minimalist **black void stage + mirror floor**; environment almost absent | Much easier to generate consistently. **Identity bleed mostly disappears:** in the wides the hero is too small to show a face, and the close-ups contain only the hero. |
| 4–5 shots, ~30 s, action-driven | ~35 shots, 100 s, **litany-driven**, with spoken lines | Needs a voice-over script and more, shorter shots |
| Mace/hammer combat | Unarmed; **gestures to the lens** | Simpler costume lock, stronger close-ups |
| Silent film | Narrated | Needs a voice: yours (recorded) or a cloned/TTS voice |

## 2. Model plan for this style (live prices, 2026-10-30)

| Shot type | Model | Cost |
|---|---|---|
| Close-up still of you (frontal) | Soul Cinema + soul_id, *with the mandatory head phrase* | ~1 cr |
| Wide/void still, monster, VFX inserts | Soul Cinema without soul_id | ~1 cr |
| Your face and another character in the same frame (rare in this style) | Nano Banana Pro edit of a Soul plate | 2 cr |
| Animate each shot (3–5 s) | Kling 3.0 Pro, start image (+ end image for transformations) | ~8.75 cr per 5 s; 12.25 per 7 s |
| Voice | **Your own recorded narration** laid in during edit (recommended), or a Higgsfield/ElevenLabs voice clone | 0 for your own recording |
| Lip-synced talking close-ups | Kling 3.0 with sound on, only if you want mouth-synced speech | more cost and more failure risk, so optional |

**Recommendation:** voice-over, not lip-sync. The reference's close-ups mostly hold a gaze or say a line or two. Record your lines on your phone in a quiet room. That gives the most authentic voice at zero credit cost, and the edit (ffmpeg) puts it on the cut.

## 3. Film 4 v3: *The Lunar Purge* rebuilt as a litany (~60 s, 16 shots)

**Why the D&D story fits this format perfectly:** Selûne's holy symbol is **seven stars**, one per Shard [Faiths & Pantheons p. 55; Mistress of the Night p. 13]. The reference names **seven archangels**. Our hero names **Selûne's gifts**, one per star, like the archangel litany. **Two stars are dark**: the two Shards Shar has corrupted into angels of decay [Vanrakdoom p. 24]. The climax relights them.

### Locks (repeat word for word)

**HERO LOCK** (reference costume adapted to Selûne, unarmed)
> a man with a completely shaved bald head, short ginger-brown moustache and light stubble, eyes open, wearing an ivory-white ceremonial cape with a very high stiff collar, quilted silver embroidery of crescent moons, rows of pearls, pale-blue glowing moonstone crystals along the seams, a glowing pale-blue moonstone at his sternum, and a crown of seven silver crystal star-points, five glowing and two dark

**VOID LOCK**
> an endless black void stage, a perfectly still wet mirror-black floor reflecting every light, faint drifting mist at floor level, a single cold top light

**ANGEL LOCK** (×2; canon: undead, rotting, streaming corruption, once Selûne's priestesses [Libris Mortis pp. 83–84])
> a gaunt winged undead angel half again the height of a man, once a beautiful woman, rotting grey-violet skin streaming oily purple-black liquid corruption that spreads across the mirror floor, ragged wings of rotting black feathers and bare bone, long matted grey-black hair, a cracked silver priestess circlet, dull violet glowing eyes

**SHARD LOCK** (×2; canon: female planetars, long flowing blue hair, pearly-white skin, wings shown at will, formed of moonlight and fire [Faiths & Avatars p. 135; Player's Guide to Faerûn p. 154])
> a radiant female planetar with her own delicate face, pearly-white luminous skin, long flowing blue hair drifting as if underwater, silver-glowing eyes, pale robes of moonlight, vast translucent wings made of light rather than feathers, a whole silver circlet, a faint inner glow like moonlight over banked white fire

**STYLE LOCK** (from the reference)
> photorealistic cinematic film still, minimalist composition, near-total darkness, the figure is the main light source, deep blacks, ice-blue and ivory palette, shallow depth of field, subtle film grain

### Voice-over script (your voice, slow, low, ~1 s pauses)
1. "Before the first dawn there were two sisters. One kept the dark. One kept the light."
2. "Our Lady of Silver grants light."
3. "The Moonmaiden grants the tide."
4. "The Night White Lady grants the way home."
5. "Seven stars kept watch over the night. Two of them fell."
6. *(Angel, slurred, wet, almost a whisper):* "She… forgot… us."
7. "She never forgot you."
8. "Selûne grants… return."
9. *(final, almost silent)* "Welcome home, sisters."

The titles *Our Lady of Silver*, *the Moonmaiden* and *the Night White Lady* are Selûne's canonical titles [Faiths & Pantheons p. 55].

### Shot list (16 shots ≈ 60 s; A = close-up of you alone, B = wide/void/insert)

| # | Type | s | Still prompt (keyframe) | Motion prompt (Kling 3.0 Pro) | VO |
|---|---|---|---|---|---|
| 1 | B | 4 | [VOID LOCK]; an enormous full moon low on the horizon, the floor reflecting it; on the far left a vast shadow eclipses part of the sky. [STYLE LOCK] | Very slow push-in; mist drifts; the shadow creeps a little further over the moon | 1 |
| 2 | A | 4 | Frontal symmetric close-up. [HERO LOCK]. He looks straight into the lens, calm and grave; his moonstone glows. Black background, cold top light, rim light on his scalp. [STYLE LOCK] | Locked; he slowly lifts his eyes to the lens; the sternum gem pulses once | 1 (cont.) |
| 3 | B | 3 | Extreme wide. [VOID LOCK]; tiny in the centre, a figure in an ivory cape glows pale blue, facing a black horizon. [STYLE LOCK] | Locked; his glow brightens; the reflection ripples | – |
| 4 | A | 3 | Close-up. [HERO LOCK]. He raises his open right hand toward the lens, palm out, in strong foreshortening. [STYLE LOCK] | His hand pushes slowly toward camera; light gathers in the palm | 2 |
| 5 | B | 4 | Extreme wide. [VOID LOCK]; a column of pure silver moonlight slams down onto the floor, lighting the whole void silver; tiny figure in the centre. [STYLE LOCK] | The beam lands and blooms outward across the mirror floor | 2 |
| 6 | B | 4 | Wide. [VOID LOCK]; a towering wave of liquid silver moonlight rises behind the tiny figure, curling over him. [STYLE LOCK] | The silver wave rises and curls, droplets of light spraying | 3 |
| 7 | B | 4 | Wide. [VOID LOCK]; constellations of silver stars appear across the black, joined by thin glowing lines into a path leading to the figure. [STYLE LOCK] | Stars ignite one after another; light-lines draw themselves | 4 |
| 8 | A | 4 | Close-up. [HERO LOCK]. His face falls into sorrow; two of the seven crown points are dark. [STYLE LOCK] | Slow push-in; his eyes glisten; the two dark points flicker once | 5 |
| 9 | B | 4 | Wide, low. [VOID LOCK]; two [ANGEL LOCK] crawl out of the darkness toward the tiny glowing figure, corruption spreading across the mirror floor. [STYLE LOCK] | The two angels drag themselves forward; violet-black corruption spreads; wings twitch | 5 (cont.) |
| 10 | B | 3 | Macro close-up of one angel's face, [ANGEL LOCK], beautiful features under rot, violet eyes, lips cracking open. [STYLE LOCK] | Her lips part; corruption drips; her eyes narrow | 6 |
| 11 | A | 4 | Close-up. [HERO LOCK]. Tears on his face, a gentle determined look; he reaches his hand toward the lens. [STYLE LOCK] | He leans in slightly; a single tear falls; the moonstone brightens | 7 |
| 12 | B | 3 | Macro insert: his crown, two dark star-points beginning to glow faint silver. [STYLE LOCK] (no face) | Light creeps into the two dark points | 8 |
| 13 | B | 6 | **START:** Wide. [VOID LOCK]; the tiny glowing figure with arms open; before him the two [ANGEL LOCK] rear up. [STYLE LOCK] — **END:** (Nano Banana Pro edit of START, same composition) the two angels are now [SHARD LOCK], kneeling, wings of light spread; the corruption on the floor has become reflected moonlight. | A shockwave of silver moonlight sweeps over the angels; the rotting crust cracks and falls away as silver ash; blue hair unfurls; wings of light open; they sink to their knees | 8 |
| 14 | B | 3 | Macro: a restored Shard's face, [SHARD LOCK], eyes opening, silver light in them. [STYLE LOCK] | Her eyes open; a soft smile of recognition | – |
| 15 | A | 4 | Close-up. [HERO LOCK], now all seven crown points glowing; eyes closed, serene, faint tears. [STYLE LOCK] | Locked; moonlight brightens his face; he slowly opens his eyes | 9 |
| 16 | B | 4 | Extreme wide. [VOID LOCK]; the full moon whole again; the tiny figure between two kneeling winged figures of light; seven stars above. [STYLE LOCK] | Very slow pull-back; then fade to black | – |

**Identity rule in v3:** your face appears only in the A shots (2, 4, 8, 11, 15), always alone in frame. In every B shot the hero is tiny or not shown. So Soul bleed (§1 of `03_…`) can't happen, and Nano Banana Pro is needed only once (shot 13 END).

### Budget v3

| Item | Credits |
|---|---|
| 16 stills × 2 variants (Soul Cinema, ~1 cr) | ~32 |
| 1 Nano Banana Pro end frame × 2 | 4 |
| 16 Kling 3.0 Pro clips (3–6 s; ~1.75 cr/s) | ~110 |
| Re-roll reserve (~25 %) | ~35 |
| **Total** | **≈ 180 credits** for a 60 s film (balance ~704) |

A 100 s version, the reference's length, would be ~300 credits.

## 4. Decisions only you can make
1. **Format:** adopt the reference's litany/void style for all four films (recommended), or keep the earlier environment-heavy scripts?
2. **Voice:** record the voice-over yourself (recommended) or use a cloned/TTS voice? English, or Macedonian?
3. **Length:** 60 s (~180 cr) or 100 s like the reference (~300 cr)?
4. **The paper seraph:** in the reference it's the *monster*. Keep it as a monster in Film 3 (the hero being a white saint like the reference), or make you the paper seraph as Gemini proposed?
