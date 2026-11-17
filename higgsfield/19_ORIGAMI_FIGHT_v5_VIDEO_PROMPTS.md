# 19 — THE ORIGAMI ASCENSION (v5) — VIDEO PROMPTS (SkyReels-V2 DF, I2V)

Supersedes the single generic video prompt in the v2_*.sh scripts.
Supersedes 17_ORIGAMI_FIGHT_v4_CONTINUITY.md only for the VIDEO-TEXT layer;
the continuity chain (IN/OUT states) is unchanged and is the source of truth here.

These prompts follow `18_PROMPT_COMPOSITION_GUIDE.md` §2 (V2-specific rules):

1. **Describe the first-frame image** — the text must AGREE with the seed keyframe,
   never contradict it. The seed for beat N is the beat-N keyframe still rendered by
   `build_origami_jobs.py`. The earlier $3 failure came from text describing a
   parchment seraph while the seed was an Azulon hero frame: anchor won, text ignored.
2. **State the camera grammar explicitly** — SkyReels-V2 is trained on it and it is
   its highest-scoring dimension (shot angle 90%, camera motion 85%, shot position 83%).
3. **State continuity** — what must not drift across the clip.
4. Keep each prompt SHORT (~250-450 chars). Do NOT use --prompt_enhancer:
   it over-saturates long prompts and needs 64G+ VRAM. Hand-write.

## I2V parameter corrections (were T2V values)

| param | T2V (wrong for I2V) | I2V (correct) |
|---|---|---|
| --shift | 8.0 | **5.0** |
| --guidance_scale | 6.0 | **5.0** |
| --inference_steps | 30 | **50** |
| --num_frames | - | 97 (540P) / 121 (720P) per clip |

12 clips x 97 frames (540P) = ~48 s fight reel.

---

## THE 12 BEATS

Seed keyframe names assume `or_XX_<tag>.png` from the keyframe runner.

### 01 · corruption_revealed — MONSTER
**Seed:** or_01_corruption_revealed.png
> The first frame shows a colossal seraph of folded parchment, six ragged wings
> dripping glossy black goo, its head a blank folded paper mask weeping black, looming
> in a starless void over a wide black mirror. The goo keeps dripping in long slow
> strands and the pooled mirror ripples; drifting parchment pages float past its wings.
> Camera: low-angle wide shot, very slow push-in. Its blank mask and six wings stay fixed.

### 02 · hunter_descends — HERO
**Seed:** or_02_hunter_descends.png
> The first frame shows Azulon mid-descent, ivory wings snapping open with cold white
> flame racing every edge, folded pages around his raised hand, the Stain far below.
> He keeps plummeting, wings flaring, white flame streaking upward behind him.
> Camera: high-angle tracking shot descending with him. His clean-shaven face stays fixed.

### 03 · thousand_cranes — HERO
**Seed:** or_03_thousand_cranes.png
> The first frame shows Azulon with six ragged thinned wings firing thousands of folded
> paper cranes, each edged in cold white fire. The crane storm keeps streaking outward
> in a comet swarm, motion streaks and shockwave rings expanding across the frame.
> Camera: wide shot with a slight lateral track, swarm filling the frame.

### 04 · stain_devours — MONSTER
**Seed:** or_04_stain_devours.png
> The first frame shows the corrupted seraph's wings unfolded into a cathedral wall of
> stained parchment swallowing the incoming white crane swarm. The wall keeps expanding,
> tar tentacles snapping up the last cranes, goo brightening as it feeds.
> Camera: static colossal wide shot, slow steady push forward.

### 05 · tar_tide — CLASH
**Seed:** or_05_tar_tide.png
> The first frame shows a tidal ocean of glossy black tar surging upward from the
> collapsed wings toward a small blazing white Azulon hanging above it. The wave keeps
> rising and rolling, goo screaming off its crest, his flame reflected in the slick.
> Camera: low angle, slow tilt up as the wave climbs. His white figure stays fixed.

### 06 · blade_splits_tide — HERO
**Seed:** or_06_blade_splits_tide.png
> The first frame shows Azulon re-folded into a single ivory blade diving into the tar
> wave, the ocean parting around him in a deep steaming canyon. He keeps diving through,
> the canyon walls screaming to white steam and collapsing behind him in black spray.
> Camera: fast tracking shot following the blade through the parting wave.

### 07 · colossus_against_cathedral — CLASH
**Seed:** or_07_colossus_against_cathedral.png
> The first frame shows Azulon unfolded into a towering colossus of angular ivory plates
> facing an ever-growing mass of stained dripping pages. Both keep growing, goo dripping
> from one, white fire pouring off the other, the void shaking.
> Camera: extreme wide shot, slow crane upward revealing their scale.

### 08 · sphere_of_annihilation — CLASH
**Seed:** or_08_sphere_of_annihilation.png
> The first frame shows white flame and black tar locked in a blinding sphere at frame
> centre, both silhouettes inside it. Shockwave rings keep blasting outward, parchment
> shredding to confetti, lens bloom pulsing, the void bowing.
> Camera: locked wide shot with a subtle shake, very slow push toward the core.

### 09 · thousandfold_dawn — HERO
**Seed:** or_09_thousandfold_dawn.png
> The first frame shows Azulon bursting out of the burning sphere, all six wings
> detonating into uncountable paper blades in a radial star. The blades keep spiralling
> outward in every direction at once, the white star expanding as he breaks free.
> Camera: wide, gently rotating, fixed on the expanding radial storm.

### 10 · final_unfold — MONSTER
**Seed:** or_10_final_unfold.png
> The first frame shows the corrupted seraph unfolded into a cathedral nest of stained
> pages and tar tentacles, swallowing the blade storm, white blades glowing faintly
> inside it. The tentacles keep writhing, it swells, goo cascading off in curtains.
> Camera: slow push-in on the gorged mass.

### 11 · spear_pierce — HERO
**Seed:** or_11_spear_pierce.png
> The first frame shows Azulon compressed into a single white dart punching a thin
> perfect line of light through the black mass. The line keeps piercing in one side and
> out the other, the holes rimmed white and spraying black vapour, white fire glowing
> up inside the body.
> Camera: fast tracking shot following the dart's path through the body.

### 12 · annihilation_ascension — CLASH
**Seed:** or_12_annihilation_ascension.png
> The first frame shows white fire erupting from inside the corrupted seraph, its body
> crumbling to glowing dust with clean white cranes rising, Azulon landing in the
> foreground. The body keeps crumbling outward, tar boiling to vapour, the dust cloud
> expanding as the cranes rise through the wreckage.
> Camera: wide, slow pull-back revealing the empty void.

---

## Render plan

- 12 clips, 97 frames each (540P 1.3B DF-1.3B), ~4 s each -> ~48 s fight reel.
- Seeds 800-811 (deterministic, match the keyframe builder).
- I2V params: shift 5.0, guidance 5.0, steps 50, no prompt_enhancer.
- Each clip's seed = its beat keyframe (hash-verified NOT an Azulon hero-only frame
  where the beat is monster-only; that is the wrong-anchor gate).
