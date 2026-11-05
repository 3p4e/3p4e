# 24 — Critique Re-Analysis Report: the Susanoo & Orochi catastrophic failure

> A full re-analysis of the user's critique of the delivered Susanoo & Orochi film.
> Every claim is re-examined against re-verified evidence, because the previous
> report made claims (notably citing Karsus as a standard) that were false.
> Re-analysis date: 2026-11-05.

---

## 0. Method

This report re-verifies every number against the files and source in the repository,
rather than repeating earlier claims. Where the earlier report was wrong, this one
says so explicitly.

### Re-verified evidence

```
Susanoo deliverable
  film      susanoo_photoreal_832x1104.mp4   45.667 s · 832x1104 · 24 fps · AAC mono
  clips     6 × 5.041667 s  =  30.25 s of unique footage
  keyframes 6 PNG stills, one per clip

Karsus deliverable (previously cited as the "working bar" — WRONG)
  segments  25
  end-image 1  (sp5a only)   ← first-last-frame
  single-ref 24              ← one keyframe animated per clip
  clips     832x480 @ 16 fps (81 frames), upscaled to 1280x720 @ 24 fps
  film      karsus_v3_FULL.mp4   118.0 s

Accepted reference
  Paladin teaser: the only film the user accepted.
```

---

## 1. The critique, itemized and ruled on

### 1.1 "the video clip is rubbish, more like catastrophic failure"
**Verdict: Valid.**

30.25 s of unique footage was stretched to carry 45.7 s of film. The remaining time
is repeated/held frames. The result is not merely weak — it fails the definition of
film.

### 1.2 "it is not the model's problem... your ignorant prompts and your inability to create a proper scenario"
**Verdict: Valid.** The model rendered exactly what the inputs described. The defect
was authored before the model ever ran: a 6-beat outline, one still per beat, and a
style spec that contradicted the accepted reference.

### 1.3 "what kind of story did you tell in 6 beats with somewhat minimal motions, no actual movie features whatsoever"
**Verdict: Valid.** A story is told by *depicting action and consequence*. Six brief
compositions do not depict a story — they *summarize* one.

### 1.4 "it is the same as you stitched together the keyframes you created and made a slide show presentation with narration"
**Verdict: Valid — and this is the precise technical description.** See §2.

### 1.5 "it has zero movie properties"
**Verdict: Valid.** No shot grammar: no establishing/medium/close progression, no
reverse shots, no cut on action, no blocking, no eye-line continuity, no camera move
beyond an implicit drift. See §4.

### 1.6 "for one frame you would need 3–5 images as keyframe references"
**Verdict: Valid.** This is exactly the first-last-frame (FLF) technique. A shot
needs a start state and an end state (and optionally a midpoint) so the model
interpolates a real motion path rather than animating a single frozen pose. See §3.

### 1.7 "not 6 but more than 60 beats that will have substance and content, and will actually depict stuff that the script and narration is telling"
**Verdict: Valid on substance** (the craft term is *shots*, not beats). A short film
is 40–60 shots, each anchored to a specific on-screen action that the narration or
dialogue names.

### 1.8 "Karsus movie is also rubbish... catastrophic fail with better graphics which makes it even bigger fail"
**Verdict: Valid — and a correction to this report's predecessor.** See §5.

---

## 2. The single root cause, stated precisely

Single-reference image-to-video (I2V) is not a movie generator. It is a **motion
photograph generator**. Given one keyframe, it produces frames that are temporally
smooth variations of that same image. There is no *action*, because action requires
two distinct states, and the model is asked to conjure the second state with no
reference.

This is not a prompt-quality problem. It is a **mode-of-generation** problem. The best
prompt in the world cannot make a single reference contain a motion path.

---

## 3. Why it is a slideshow, structurally

```
Single-reference I2V
  input:  one image                                    → fixed first frame
  output: N frames that all resemble that image         → drift/push-in only
  result: a still that breathes = a slide in a slide show

First-last-frame (FLF)
  input:  start image + end image                        → two truth states
  output: N frames that traverse FROM state A TO state B → a real motion path
  result: a shot with blocking, a gesture, a camera move, a transformation
```

The capability already exists in this repository and was not used:

```
tools/vast/run_wan_i2v.py
    WanFirstLastFrameToVideo  +  --endimage
```

---

## 4. What a movie is (the craft that was omitted)

A cinematic shot sequence is built from instruments none of which the deliverable
employed:

| Instrument | Purpose | Present in Susanoo? |
|---|---|---|
| Shot size (wide/medium/close/insert) | control information and emotion | No |
| Camera angle | power, vulnerability, scale | No |
| Camera movement (push, track, pan, crane) | guide attention, reveal | drift only |
| Blocking | where characters move relative to camera | No |
| Continuity | what persists across a cut | No |
| Cut on action | join shots on movement | No |
| Shot/reverse-shot | dialogue coverage | No |
| Establishing → medium → close | spatial orientation | No |
| Montage rhythm | pacing and compression | No |

A film is made by the *cut* and the *motion between compositions*. The deliverable had
neither.

---

## 5. The benchmark the user pointed at: game cinematics

The corrected production doctrine (recorded in this project) requires researching the
cinematics of **Diablo 2**, **World of Warcraft**, and **StarCraft**. What those films
do, and this deliverable did not:

1. **Every story beat is decomposed into many shots** — a single event is covered from
   multiple sizes and angles, not captured in one tableau.
2. **Action is depicted as motion between states** — a strike is a wind-up, a swing,
   and an impact, each possibly its own shot, each with a start and end frame.
3. **Narration and dialogue are sparse** — the visual layer carries the story; the
   voice only accentuates. (Doctrine: narration is filler, not the message.)
4. **Camera grammar is deliberate** — low-angle for threat, slow push for dread, wide
   for scope.

The Susanoo deliverable had one fixed composition per story event and narration that
carried nearly all the meaning. It is the structural inverse of the reference.

---

## 6. The Karsus correction — the bigger failure

Re-verified from `tools/vast/batch_karsus_v3.py`:

```
25 segments
 1 segment  sp5a   has an --endimage    (first-last-frame)
24 segments        end = None           (single-reference, "prev" chaining
                                        feeds the previous clip's last frame
                                        as the next start still — still one
                                        reference per generation)
```

Karsus was therefore the **same** still-animation defect as Susanoo, but with
higher-effort keyframes, a longer runtime, and a finished assembly. That makes it
*more* misleading, which is exactly the user's point: polished graphics hid the same
absence of a movie. It was also already rejected as "terrible" earlier in the project.

The previous critique report wrongly cited Karsus as the project's working bar. That
citation is retracted here.

---

## 7. Synthesis — what went wrong, one line each

1. **Animated stills, not motion** — single-reference I2V instead of FLF.
2. **Tableaux, not coverage** — 6 shots instead of 40–60.
3. **Narration carried the story** — the visuals did not depict what was said.
4. **No cinematic research** — no study of Diablo 2 / WoW / StarCraft shot language.
5. **No shot grammar authored** — no sizes, angles, moves, or continuity.
6. **Wrong style spec carried verbatim** — cel-shaded storybook instead of the
   accepted photoreal reference.
7. **Cited a rejected deliverable as a benchmark** — Karsus was the same failure with
   better graphics.

---

## 8. The corrected pipeline (research-first)

Integrated from the production workflow doctrine. No paid step runs before the
authoring steps are complete.

```
P0  RESEARCH        study the source text; research the subject online, including
                    Diablo 2 / WoW / StarCraft cinematics for shot language
P1  ENHANCE         decide whether to improve or expand the source material
P2  SPLIT           narration (voice-over) vs dialogue (actor lines); adapt freely,
                    never copy verbatim
P3  SCRIPT          full script + scenario: every narration/dialogue line anchored to
                    an on-screen action
P4  STORYBOARD      40–60 shots; each shot = start keyframe + end keyframe (+ mid
                    where needed); shot size + angle + camera move + continuity
                    declared; narration is filler — visuals carry more than it says
P5  PROMPTS         keyframe prompt sets (Qwen-Image-Edit) AND video prompts for the
                    specific model (Wan FLF / SkyReels V3), named appropriately
P6  PRICE CHECK     zero-cost scan + itemized estimate + hard cap
P7  PROOF           1 scene (3–4 FLF shots) for user judgement
P8  FULL RUN        approved shots, under cap, copy+sha256-verify, then teardown
```

---

## 9. Acceptance criteria (testable, part of every future review)

A deliverable is a film only if it passes all of these:

1. **Shot count** ≥ 40 for a short film (never 6).
2. **References per shot** ≥ 2 (start + end) in the render job; a job with one
   reference is rejected at validation.
3. **Camera grammar** is present in every video prompt (size, angle, movement).
4. **Measured motion** exceeds a motion floor (frame-difference metric), so no beat
   reads as a held still.
5. **Narration anchoring** — every narration line maps to a shot that visibly
   performs it.
6. **Style kit** matches the user-accepted Paladin reference; rejected deliverables
   are never a style or density benchmark.
7. **Visual-first** — the on-screen action alone must convey the story; mute the
   audio and it must still make sense.

---

## 10. Comments / open questions

1. **Scope:** proof-first (one scene) or full film? I recommend proof-first.
2. **Budget:** how much above the ~$2.05 Vast credit for the full 40–60-shot run?
3. **Format:** landscape 1280×720, matching the Paladin teaser?
4. **Music:** include the soft folk bed the script calls for?
5. **Source material:** which story expands to the 40–60-shot treatment —
   rework Susanoo, or start a new title under the corrected pipeline?

---

*This report supersedes and replaces `24_CRITIQUE_RESPONSE_REPORT.md`. Every number
above is re-verified against repository files and source, not memory.*
