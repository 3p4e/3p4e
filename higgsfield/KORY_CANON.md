# KORY — canon record

Recorded 2026-11-04. Source: direct statements from the director.

## What KORY is

KORY is **not a separate person from DD**. KORY is the **alternate character** the real player **DD** plays — a **female Demon Hunter** in-game persona.

| Field | Value |
|---|---|
| Real person | **DD** (he) |
| Character | **KORY** (she) |
| Relationship | DD plays KORY as an in-game female Demon Hunter avatar |
| Character gender | **female** |
| Character look | long red-and-black hair (wig in reference photos) |

## Identity evidence (measured, local, zero cost)

Face embeddings from the 2026-11-04 photo sets, YuNet + SFace, full resolution:

| Comparison | Cosine | Reading |
|---|---|---|
| DD centroid ↔ KORY centroid | **0.7199** | same person (confirm line 0.72) |
| DD ↔ Oleg (known different person) | 0.1633 | control: correctly different |
| KORY ↔ Oleg (known different person) | 0.1407 | control: correctly different |
| Per-pair DD ↔ KORY | 87% above 0.363 | systematically same person |

Visual confirmation: identical arched eyebrows, nose and nostril shape, eye spacing, lip shape, jawline, and **the same mole on the left cheek** below the eye.

**Conclusion: one actor, two presentations. This is intentional, not contamination.**

## The facial-hair rule

The real DD wears a **beard and moustache** in every reference photo. KORY is a **female character**, so the facial hair must be **removed** on the KORY render, not carried over.

This is an identity-spec requirement, not a cosmetic preference. It carries into every KORY generation.

## The feminisation requirement

Removing the moustache and beard alone is **not enough**. The face must also be **softened toward female reading** while staying recognisably the same person.

**To remove / soften:**
- moustache, beard, chin and jaw stubble (all of it)
- jaw width and chin mass trimmed slightly softer
- brow ridge softened, eyebrows slightly narrowed and lifted
- cheek volume subtly fuller
- lips slightly fuller
- neck and shoulders softened

**To preserve (identity anchors — must not drift):**
- eye shape, eye spacing, iris colour
- nose shape, width and nostril form
- the mole on the left cheek
- hairline and forehead proportion
- overall facial proportions within ±10 % frontal geometry tolerance

**Acceptance gate:** the feminised KORY must still score **SFace ≥ 0.50** against the DD reference centroid. If it drops below, the feminisation has drifted too far and must be re-derived.

## Source material status (2026-11-04)

| Set | Files | Passing both gates (≥256 px, sharpness ≥60) |
|---|---|---|
| DD | 17 | **17 / 17** |
| KORY | 16 | **2 / 16** |

KORY's set is critically thin: 13 of 15 detected faces are below the 256 px minimum, sharpness runs 6.5–44 against a 60 gate, and the only 2 passing frames are near-duplicates of one frontal pose (cos 0.9789).

**Consequence:** DD is the usable identity source. KORY's own photos serve only to confirm the persona look (wig, styling), not to train or anchor identity.

## Generation approach

1. Anchor on the **DD centroid** — the strongest available likeness evidence.
2. Apply the **feminisation edit** (beard removal + softening) with **Qwen-Image-Edit-2511** (Apache-2.0, already in the VAST stack, zero new install).
3. Re-verify with the likeness gate against the DD centroid.
4. Render the card set with long red-and-black hair as the character look.

**Never** carry KORY's beard into a render. **Never** build KORY from a single bearded frontal frame as if it were a full identity set.

## Open items

- Better KORY reference photos (well lit, face filling the frame, wig on) would materially improve the result. This is the current bottleneck.
- Confirm whether the red-and-black long hair is the final character look.
