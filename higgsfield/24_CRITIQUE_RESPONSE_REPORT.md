# 24 — Critique Response Report: Susanoo & Orochi

> A point-by-point response to the user's critique of the delivered Susanoo & Orochi
> film (45.7 s), which was rejected as a slideshow rather than a movie.
> Each claim from the critique is quoted, ruled on (Valid / Partly valid), supported
> with measured evidence, and resolved into a root cause, a fix, and a prevention.
> Companion to `23_ERROR_REGISTER_AND_FIXES.md`.

---

## Critique claim 1 — "the video clip is rubbish, more like catastrophic failure"

**Verdict: Valid.**

The delivered film is `media/susanoo_film/susanoo_photoreal_832x1104.mp4`:

```
45.667 s · H.264 832x1104 · 24 fps · AAC 48 kHz mono
built from 6 clips · 5.041667 s each · 30.25 s of unique footage
```

Six clips of five seconds each cannot carry 45 seconds of narration as a film. The
motion is minimal because the model was never asked to produce motion between two
composed states — it was asked to animate a still.

- **Root cause:** single-reference image-to-video, one keyframe per clip.
- **Fix:** switch to first-last-frame (FLF) generation — a start keyframe **and** an end
  keyframe so the model renders the action *between* them.
- **Prevention:** single-reference I2V is banned for narrative work.

---

## Critique claim 2 — "it's not the models problem. It's your ignorant prompts and your inability to create a proper scenario"

**Verdict: Valid, with one correction.**

It is not the model's fault — the model did exactly what the inputs described. But the
primary defect was not in individual prompt *wording*; it was in the **scenario structure**
(6 beats) and the **generation mode** (animate one still). The prompts carried a wrong
style spec in addition (see claim 2b), so wording was also at fault in one respect.

Evidence that this is a craft failure, not a model ceiling:

```
SkyReels-V3 rendered the Paladin teaser photoreal to the user's satisfaction.
That is the only user-accepted reference. Karsus was NOT accepted: it was the
same single-reference still animation, and the user rejected it too.
```

- **Root cause:** I authored an outline and called it a story; I carried
  "cel-shaded watercolor storybook" from `story.md` §1 into every prompt while the
  accepted reference was photoreal.
- **Fix:** full shot-by-shot storyboard first; photoreal style kit matched to the
  accepted Paladin reference.
- **Prevention:** diff every new story's style kit against the user-accepted reference
  before any render. A rejected deliverable is never a style benchmark.

---

## Critique claim 2b — wrong style (cartoon instead of photoreal)

**Verdict: Valid.**

The first Susanoo render came out cel-shaded watercolor because that exact phrase lived
in the scenario spec, contradicting the photoreal standard the user established with the
Paladin teaser.

- **Root cause:** I executed the scenario spec without challenging it.
- **Fix:** rebuilt all six keyframes photoreal ("photorealistic cinematic film still,
  35mm, real skin, film grain"; cartoon/watercolor/illustration in negatives).
- **Prevention:** style kit is a quality requirement; never honor a spec that contradicts
the one film the user approved (Paladin) without flagging it. Karsus was rejected and is
not a style reference.

---

## Critique claim 3 — "what kind of story did you tell in 6 beats with somewhat minimal motions, no actual movie features whatsoever"

**Verdict: Valid.**

Measured shot density:

```
Susanoo   6 shots  /  30.25 s   = 0.20 shots per second of film
Paladin   4 shots  /  20.25 s   = teaser, not a full film
```

Six beats is an outline, not coverage — but the corrective benchmark is NOT Karsus. Karsus
was built by the same single-reference still animation (25 segments, only one used an end
frame), shipped at 16 fps at 480p upscaled, and was already rejected as "terrible." It is a
failed deliverable, not a standard.

- **Root cause:** I treated one beat as one shot. A single story beat needs multiple
  shots (wide / medium / close / insert).
- **Fix:** every beat decomposes into 3–6 shots; a real film is 40–60 shots.
- **Prevention:** shot density is a hard requirement, not a suggestion. Only a
  user-accepted film may serve as the benchmark.

---

## Critique claim 4 — "it's the same as you stitched together the keyframes you created and made a slide show presentation with narration"

**Verdict: Valid — this is the precise technical description of what happened.**

Single-reference image-to-video takes one keyframe and applies it as the first frame,
then generates a gentle, temporally-smooth variation of that same image. The result is a
*slow push-in on a photograph*. Stitching six of those under a narration is, by
construction, a slideshow.

The contrary capability already exists in the repository, unused:

```
tools/vast/run_wan_i2v.py
    WanFirstLastFrameToVideo  +  --endimage   (first-last-frame mode)
```

- **Root cause:** I used the single-frame mode; the FLF mode was present but never used.
- **Fix:** FLF generation for every shot — start frame + end frame = real camera motion,
  blocking, and action.
- **Prevention:** a shot is two keyframes, never one. Motion comes from the *distance*
  between them.

---

## Critique claim 5 — "it has zero movie properties"

**Verdict: Valid.**

The deliverable had no reverse shots, no shot/reverse-shot dialogue coverage, no
establishing→medium→close escalation, no camera moves beyond the implicit slow push-in,
no blocking, no cut on action. Those are the properties that make footage read as film.

- **Root cause:** no shot grammar was authored before rendering.
- **Fix:** every scene gets a shot list with explicit shot size + camera move + continuity
  between shots (what stays fixed across the cut).
- **Prevention:** camera grammar is graded and explicit in every video prompt
  ("slow push-in", "low-angle tracking", "shot/reverse-shot"), following the project's
  own `production_shablon.md` §5.

---

## Critique claim 6 — "for one single frame you would need 3–5 images as keyframe references"

**Verdict: Valid, and this maps exactly to the FLF technique.**

The user's instinct is not a guess; it is the correct craft. Where the user says
"3–5 references per frame," the technique is at minimum a **start frame** and an **end
frame**, and in richer shots an additional midpoint or staging reference. This gives the
model a motion path to interpolate instead of a single frozen pose to wiggle.

- **Root cause:** I supplied one reference per shot (3–5× too few).
- **Fix:** per shot, author a start keyframe and an end keyframe (and a midframe where the
  action demands it), then generate with FLF.
- **Prevention:** each shot's render job must declare its start AND end reference; a job
  with a single reference is rejected at validation time.

---

## Critique claim 7 — "in one entire movie, not 6 but more than 60 beats with substance, depicting what the script and narration is telling"

**Verdict: Valid on substance; terminology corrected.**

The precise term is **shots**, not beats (a beat is a story event; a shot is a camera
setup). The user is right on the content: an entire short film is 40–60 shots minimum,
each depicting specific action that the narration names — never a tableau over which
narration floats.

```
6 shots for 45 s  →  broken coverage
40–60 shots       →  a short film with substance
```

- **Root cause:** I compressed the whole story into 6 setups.
- **Fix:** a shot-by-shot board where narration lines are *anchored to on-screen action*,
  each beat expanded into 3–6 shots.
- **Prevention:** the storyboard must map every narration line to a shot that visibly
  performs it — narration names an action, the shot shows it.

---

## Budget reality attached to the correct fix

A real 40–60 shot film cannot be produced on the remaining credit:

```
Vast credit         ~$2.05
OpenRouter          ~$0.00
60-shot film        above the current balance (SkyReels-V3 just cost ~$0.21/shot)
Wan FLF on 4080S    cheaper per shot — to be verified by a zero-cost auction scan
```

This does not change the craft conclusion; it changes the sequencing: storyboard and
price-check first (zero cost), then one-scene proof, then the user-approved full run.

---

## Corrected pipeline (what "produce a movie" now means)

```
STEP 0  ZERO-COST storyboard — every narration line mapped to a shot;
        each shot has start+end keyframes, shot size, camera move, continuity
STEP 1  ZERO-COST price check — live 4080S/Wan FLF scan + itemized estimate
STEP 2  ONE-SCENE PROOF — 3–4 FLF shots (~$0.30–0.50) for the user to judge
STEP 3  FULL RUN — approved shots under an explicit hard cap
```

---

## Comments / open questions for the user

1. **Scope:** proof-first (one scene) or full film first? I recommend proof-first.
2. **Budget top-up:** how much above the $2.05 credit are you willing to allocate for
   the full run?
3. **Format:** the current 832×1104 portrait came from V3's 720P geometry for a portrait
   seed. Do you want landscape 1280×720, to match the Paladin teaser, as the target for
   the rebuild?
4. **Music:** the script calls for a soft folk bed, which was never produced. Include it
   in the rebuild?

*(With apologies for the YouTube-style sign-off — no subscribes are required here, but the
comment request is honoured in full above.)*

---

*Report compiled 2026-11-05. Every claim is answered against measured evidence, not
memory. The wrong result was mine; the register in `23_ERROR_REGISTER_AND_FIXES.md` holds
the full accounting with preventions.*
