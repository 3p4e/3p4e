# HIGGSFIELD METHODOLOGY STUDY DIGEST
> Compiled from 11 official Higgsfield blog tutorials, read in full.
> Sources in higgsfield/research/*.txt (extraction dates 2026-11-07)
> Tutorials: consistent_characters_locations, why_generations_fail, soul_id_guide,
> zephyr_kpop_breakdown, cinema_studio_guide, tools_consistent_characters,
> ai_human_motion, seedance2_tutorial, beginners_guide, cinematic_generators,
> + elements_and_consistency master guide (earlier)

---

## THE ONE CORE LESSON (repeated in every tutorial)
**A text description is NOT a lock. An image reference IS a lock.**
Every recurring asset — face, weapon, costume, tattoo, location, prop —
must exist ONCE as a frozen reference image, attached to EVERY generation
that uses it. Text alone guarantees drift. This is stated verbatim in
soul_id_guide ("re-prompting drifts because the model re-interprets the
description every generation"), consistent_characters_locations, and
the elements master guide.

---

## 1. THE CHARACTER PIPELINE (Zephyr K-Pop 3-step — the director's method)
Source: zephyr_kpop_breakdown.txt — "Before You Start: Build Your Characters"

The directors locked 5 characters across a full series using exactly 3 steps:

**STEP 1 — Build the FACE**
Lock the face's bone structure, eyes, presence. Run the same identity prompt
across multiple generations until the right face appears. Grey/white studio
bg, realistic, high-end.

**STEP 2 — Build the OUTFIT separately**
Generate the wardrobe/props independently for maximum control. EVERY detail
that matters — belt, bandage, accessory — gets written explicitly HERE,
before it becomes a problem across 40+ shots.

**STEP 3 — FUSE into a MASTER ASSET**
Merge face + outfit into ONE production-ready full-body sheet:
  "The character from image 1 wearing this outfit from image 2.
   Full body shot, white studio background, soft cinematic lighting, realistic."
THIS fused sheet is what the video model checks against every time.

> THIS IS THE EXACT "body+clothes+weapons assigned to a face" the director
> described. We skipped Step 2 and 3 entirely.

---

## 2. MULTI-VIEW / TURNAROUND REFERENCE SHEETS
From elements master guide + consistent_characters_locations:

- A single front-view image CANNOT constrain a character seen from many angles.
- Character sheets need FRONT + BACK at minimum; left/right profile for full turn.
- MULTI-VIEW WEAPON SHEETS: orthographic-style, ~6 views
  (front 3/4, lateral, top, rear, bottom), object on plain grey bg,
  NO hand, NO figure.
- GREY/neutral studio background for ALL reference sheets.
- ERASE duplicate faces from sheets — one sheet = one face.
- Wardrobe states (hooded/bare, idle/wrath) are SEPARATE sheets, not text toggles.

---

## 3. SOUL ID (Higgsfield's trained identity — what we approximate with SFace)
Source: soul_id_guide.txt

- Train from 20–80 photos of ONE person, varied angles, no sunglasses,
  at least one full-height, recent (last 4-5 months).
- Trained identity is a REUSABLE LAYER, not a per-generation reference.
- More control than a prompt, less overhead than a LoRA.
- Consistency is HIGH, not absolute — "clearly the same person", not
  pixel-identical.
> OUR EQUIVALENT: enrolled face centroids (SFace) + real-photo reference
> fed as image1. The Zephyr pipeline feeds the REAL generated face, not
> an illustration-of-the-person.

---

## 4. THE MASTERCLASS PROMPT TEMPLATE (Cinema Studio 4.0)
Source: consistent_characters_locations.txt + cinema_studio_guide.txt

Higgsfield structures every multi-shot prompt as:

SCENE CONTEXT      — mood, world, what happens, tone
ACTIVE REFERENCES  — verbatim per-reference scope clause:
  "<<<image_1>>>: the location only — geometry, materials, landmarks.
   Its camera angle/scale/brightness are NOT used."
  "<<<image_2>>>: the single source of truth for [character] —
   100% identical in every shot: face, hair, outfit, weapon [explicit list].
   The white studio background never appears."
SCALE              — explicit size relationships (bridge 100m, figure 1.75m,
                   3-5% of frame height in wides)
SHOT-BY-SHOT      — per shot: camera position, lens, distance, body position,
                   action with TIMESTAMPS, screen direction ("always
                   screen-left to screen-right"), NEVER mirrored
CAMERA LANGUAGE   — tripod/dolly/crane/rigid rig, "no handheld shake,
                   no drone glide, no fast pans" for large-format look
LIGHTING          — source direction, one light rule, palette, exposure
PHYSICS           — how mass moves, cause and effect written literally
AUDIO             — no music / specific SFX, spatial
POSITIVE LOCKS    — the 5-6 things that MUST hold across every shot

> CRITICAL DIFFERENCE FROM OUR PROMPTS: they bind the reference with an
> explicit "source of truth, 100% identical in every shot" clause AND a
> "the reference's own background/angle/scale are NOT used" scope.
> We described weapons in prose; they attach a scoped reference image.

---

## 5. THE FIVE FAILURE MODES (why_generations_fail.txt)
1. FACIAL/IDENTITY DRIFT — no fixed reference → small differences add up
2. UNNATURAL PHYSICS — model predicts plausible motion, doesn't simulate
3. PROMPT MISREAD — ambiguous phrases, model picks wrong reading
4. TEMPORAL INCONSISTENCY — details change/disappear between frames
5. LOW-QUALITY/MISMATCHED REFERENCE — blurry, wrong angle, wrong context

FIXES AT INPUT: sharper reference, concrete literal descriptions, same
reference across every clip, explicit physics, shorter/simpler shots,
match reference to actual scene, REVIEW FIRST GENERATION BEFORE SCALING.

---

## 6. WHAT WE GOT WRONG — MAPPED
| OUR DEFECT | THEIR RULE WE BROKE |
|---|---|
| weapons vary/merge | no multi-view prop sheet attached to every frame |
| hood on/off | wardrobe state in text, not a separate frozen sheet |
| tattoo random | tattoo in text, not baked into the fused master asset |
| faces fail | illustration-of-person as ref, not the enrolled face; face crops too weak |
| boss drifts | NO reference at all for Mal'garot |
| single stills that don't compose | no SCENE CONTEXT/ACTIVE REFS/POSITIVE LOCKS structure |

---

## 7. THE DIRECTOR'S PRESCRIPTION (now codified)
1. Multi-view weapon sheets (~6 perspectives) for every recurring weapon
2. Full character turnaround sheets (front/back/profile) per hero, per state
3. FUSE each turnaround with the enrolled face → ONE master asset per hero
4. Boss gets his own multi-view sheet
5. Every keyframe references: hero master asset (identity+body+weapon)
   + scoped clause; boss shots → boss sheet only
6. Internet-sourced real photos for props/materials (photoreal pull, CC0)
7. Prompts follow the SCENE CONTEXT/ACTIVE REFS/SHOTS/POSITIVE LOCKS template
