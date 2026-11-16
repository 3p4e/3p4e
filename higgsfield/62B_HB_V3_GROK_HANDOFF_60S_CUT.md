# 62B — HOLLOW BLOOM v3: GROK HANDOFF — 60-SECOND BOSS-FIGHT CUT ("Sunder")

> **Purpose:** A tight 60-second proof-of-pipeline cut — boss fight + victory only. Exercises the full LTX-2.5 stack (atmosphere, pose/depth control, CU inserts, native audio dialogue, two-stage upscale) in one watchable deliverable before committing to the full 4.5-min film.
>
> **Status:** READY TO SEND TO GROK. Zero-cost authoring.

---

## 1. CANON (unchanged from doc 62)

Same world, same characters, same enrolled face cards, same Glacial Colour System, same 7 MK/EN dialogue lines. Armor canonical names unchanged.

---

## 2. THE 20-SHOT STRUCTURE (60 seconds @ 24fps)

| # | Shot | Time | Content | Control |
|---|------|------|---------|---------|
| 01 | Wide | 0:00-0:03 | DD + AZ on causeway, Bloom silhouette in mist | none |
| 02 | Medium | 0:03-0:06 | DD draws crossbows | pose |
| 03 | Medium | 0:06-0:09 | AZ raises greatsword, rune glints | pose |
| 04 | CU | 0:09-0:12 | DD eye ignite (CU1) | none |
| 05 | CU | 0:12-0:15 | AZ rune wake (CU2) | none |
| 06 | Wide | 0:15-0:19 | First exchange — DD fires, AZ blocks | pose+depth |
| 07 | Medium | 0:19-0:23 | DD vaults to flank | pose |
| 08 | Medium | 0:23-0:27 | AZ sweeps greatsword | pose |
| 09 | Wide | 0:27-0:31 | Both-sides frame, crossfire + counter | pose+depth |
| 10 | Medium | 0:31-0:34 | DD lands, rolls, re-nocks | pose |
| 11 | Close | 0:34-0:38 | AZ presses forward, heavy steps | depth |
| 12 | Medium | 0:38-0:42 | DD fires both crossbows point-blank | pose |
| 13 | CU | 0:42-0:45 | DD: "Замрзни." / "Freeze." (D5) | none |
| 14 | Medium | 0:45-0:49 | AZ: "Суди." / "Judge." — greatsword arcs (D6) | pose |
| 15 | Wide | 0:49-0:52 | Combined impact — Bloom's maw appears (CU3) | pose+depth |
| 16 | Medium | 0:52-0:55 | The shatter — ice + gold light burst | none |
| 17 | Wide | 0:55-0:58 | Aftermath — spore-mist settles, silence | none |
| 18 | Medium | 0:58-1:00 | Victory — DD + AZ stand, weapons lowered, breath visible | none |

Total: 18 shots × ~3.3s avg = 59.4s. Two additional micro-shots (19-20) can pad if needed.

---

## 3. KEYFRAME PROMPTS TO AUTHOR (36 + 3 CU)

- 18 shots × start/end = 36 keyframes
- CU1 (DD eye), CU2 (AZ rune), CU3 (Bloom maw) = 3 CU inserts
- Both-sides variants for shots 06, 09, 15 = 3 additional wide keyframes
- **Total: 42 keyframe prompts**

Same 7-point requirements as doc 62 §3. Same naming: kf_XX_start/end.

---

## 4. VIDEO PROMPTS TO AUTHOR (18-20)

One HOLD-form continuation prompt per shot. Same rules as doc 62 §4 (palette lock, single action, audio cue, prop anchors, no scene re-describe).

D5 (shot 13) and D6 (shot 14) are the sync-critical dialogue beats — native audio must land the MK line cleanly.

---

## 5. WHAT WE ASK GROK TO PRIORITIZE

1. **Combat pose clarity** — shots 06, 07, 08, 12, 14 are pose-controlled. Silhouettes must be unambiguous for DWPose extraction.
2. **Native audio quality** — every prompt gets a concrete audio cue. D5/D6 dialogue must be phonetically clear for Macedonian.
3. **Both-sides composition** — shots 06, 09, 15 need both fighters readable in frame for spatial coherence.
4. **Two-stage upscale safety** — keep identity detail (faces, hair, armor edges) in the central two-thirds per Grok's answer #3 in doc 63.

---

## 6. DELIVERABLES FROM GROK

1. 42 keyframe prompts (36 start/end + 3 CU + 3 both-sides)
2. 18-20 video/continuation prompts (HOLD-form, audio cues)
3. Any composition notes specific to the 60s cut's pacing

Format: one Markdown file, clearly sectioned.