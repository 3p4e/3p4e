# 32 MASTER METHODOLOGY — CINEMATIC-GRADE VIDEO PRODUCTION
> Aligned 2026-11-07 from: Higgsfield STUDY_DIGEST (11 tutorials) + MiniMax H3 research
> + 31_FULL_RETHINK_REVIEW.md. This doc is the single governing method.
> It supersedes prompt-level patches wherever they conflict.

================================================================
PART 0 — THE ONE LAW EVERYTHING FOLLOWS
================================================================
A text description is NOT a lock. An image reference IS a lock.
Every recurring asset — face, weapon, costume, tattoo, location, prop —
is built ONCE as a frozen reference image and attached to EVERY
frame that uses it. Text alone guarantees drift. (Higgsfield, every tutorial)

================================================================
PART 1 — THE ASSET LIBRARY (must exist BEFORE any keyframe)
================================================================
[FROM Zephyr 3-step pipeline + Elements guide + director's correction]

Per HERO, per STATE:
  A1 FACE CARD        enrolled identity (real centroid)   [HAVE: ddface/azface]
  A2 OUTFIT SHEET     full-body, hood/armour/weapon, grey bg, ONE state
  A3 FUSED MASTER     "character from image 1 wearing outfit from image 2,
                      full body, white studio bg, realistic"
                      -> ONE production sheet (face+body+gear as one unit)
  A4 TURNAROUND       front / back / left / right profiles of the A3 master
  A5 WEAPON SHEET     ~6 orthographic views of each recurring weapon
                      (front-3/4, lateral, top, rear, bottom), NO hand/figure
Per BOSS:
  B1 BOSS SHEET       multi-view turnaround, faceless, forge-core, whip-arm
Per LOCATION:
  L1 LOCATION PLATE   3/4 establishing still, no people, fixed light direction
Prop materials: internet real photos (CC0), NOT generated art (photoreal pull)

RULE: no keyframe renders until the full asset library exists and each asset
has passed a visual acceptance by the director.

================================================================
PART 2 — SHOT GRAMMAR (reconciles the three contradictions)
================================================================
The three gates that fought each other now resolve by SHOT TYPE:

SHOT TYPE    FACE RULE                    ANCHOR POLICY (Qwen image slots)
CLOSE-UP     face >= 200px, front 3/4     image1 = REAL FACE CARD (A1)
                                          image2 = FUSED MASTER (A3)
MEDIUM       face >= 120px, one hero      image1 = FUSED MASTER (A3)
             front-facing minimum         image2 = REAL FACE CARD (A1)
WIDE (2hero) faces may be 80-120px       image1 = FUSED MASTER (A3)
             BUT >=1 hero in 3/4-front    image2 = WEAPON SHEET (A5)
BOSS-ONLY    zero human refs              image1 = BOSS SHEET (B1)
             (no face-leak possible)

FACE-SIZE FLOOR: any shot whose verified face box < 120px is AUTO-REJECT,
regardless of how good everything else looks. (This is a hard machine gate.)

================================================================
PART 3 — PROMPT TEMPLATE (the Cinema Studio scaffold, adapted)
================================================================
Every shot prompt now follows this exact scaffold, replacing free prose:

  SCENE CONTEXT      one line: world + mood + what happens
  ACTIVE REFERENCES  scoped clauses, one per reference image:
    "<<<image_1>>>: the fused master of [hero] — 100% identical in every
     shot: [exact face/hair/armour/weapon list]. Its studio background,
     pose, and lighting are NOT used."
  ACTION             chronological beats: "first... then... as... finally"
  CAMERA             shot size + ONE camera path + pace + lens + distance
  SCREEN DIRECTION   "moves screen-left to right, never mirrored" (locked)
  PHYSICS            how mass moves, cause -> effect, written literally
  LIGHTING           one light source, direction, palette, exposure
  AUDIO              SFX spatial + music restraint + any dialogue (mk)
  POSITIVE LOCKS     the 5-6 things that MUST hold across every shot
  NEGATIVE           standard negative + state-specific terms

================================================================
PART 4 — THE STORYBOARD HTML SCHEMA (machine layer correction)
================================================================
The current build_storyboard_html.py embeds a <script id="storyboard-spec">
with per-shot keys: size, angle, move, dur, kf_first, kf_last, continuity,
motion. These are necessary but no longer sufficient. ADD per shot:

  "shot_type": "CU|MED|WIDE|BOSS"         (drives the Part 2 anchor policy)
  "face_floor_px": 200|120|120|0          (auto-reject threshold)
  "asset_refs": ["dd_fused_master", "crossbow_sheet", ...]  (element IDs)
  "ref_scope": "verbatim scoped clause for this shot's references"
  "screen_dir": "L2R" | "R2L"            (locked per scene, never mirrored)
  "positive_locks": [ ... 5-6 items ... ]
  "beat_timeline": [[t0,t1,beat], ...]   (cause->effect beats for the model)

And per SCENE (new block):
  "location_ref": "loc_canyon_plate"     (one fixed location element)
  "global_locks": [ ... cross-shot invariants ... ]
  "palette": [...hex...]                 (fixed grading, set once per scene)

The storyboard HTML remains the single source of truth: the human layer
(director pre-vis) and the machine layer (render spec) stay in one file.

================================================================
PART 5 — MODEL-SPECIFIC NOTES FROM MiniMax H3 RESEARCH
================================================================
MiniMax H3 (open-weights video, native synced audio, 2K) exposes:
  - FL2VA mode: first+last frame -> continuous path between them
    (this is exactly Wan FLF's job; H3 adds NATIVE AUDIO in one pass)
  - Ref2VA: labeled multi-reference input (their "Omni Reference")
  - A strict prompt structure: three core fields, shot/cut notation,
    camera language parsed as motion-type + amplitude + speed, dialogue
    and SFX written directly into the prompt
If we ever self-host H3 on Vast (open weights), the Part 3 scaffold maps
1:1 onto its Ref2VA/FL2VA format, and native audio removes a post step.
Keep this as a documented alternative, not a pivot: Wan FLF remains the
proven open path we have already paid to validate.

================================================================
PART 6 — PHASE GATES (unchanged from 31, now fed by the asset library)
================================================================
P0  ASSET LIBRARY     build + director-accept all Part 1 assets (grey bg,
                     multi-view). Cost ~$0.60-0.80. NOTHING renders before this.
P1  IDENTITY PROOF    one CLOSE-UP still, all gates at once. Director's eyes
                     are the likeness judge; SFace is a batch regression tool.
P2  SHOT GRAMMAR      per-shot table from the storyboard, face floors + anchors
P3  CHAIN PROOF       one MEDIUM pair -> FLF -> verify motion + identity + weapon
P4  SCENE PROOF       one 4-6 shot scene (~20-30s) at the locked look
P5  PRODUCTION        scene batches with per-batch gates; any failure stops the line

================================================================
PART 7 — WHAT THIS OVERRIDES
================================================================
OVERRIDDEN:
- single look cards as the only body reference (insufficient -> A3/A4 fusion)
- text-described weapons (insufficient -> A5 sheets attached per shot)
- free-prose shot prompts (replaced by Part 3 scaffold)
- face-crop-only keyframe conditioning (replaced by Part 2 anchor policy)
- storyboard spec keys without asset bindings (Part 4 additions required)
KEPT (proven): FLF motion @ 8 steps, blocking law (into-the-fight energy
through weapon/body line, not by hiding faces), enrolled centroids,
Macedonian TTS stack, EU-legal open stack, phase-gate discipline.

---

# §21 THE 2026-11-10 CORRECTED DOCTRINE (read-the-docs pass)

> Trigger: the 22B proofs (v1 motion-16 + face morph; v2 same; v3 strength-0.5 face-held + motion-dead)
> exposed that renders were being tuned blind. This section consolidates the
> full documentation pass: 11 Higgsfield tutorials + the official LTX-2
> prompting guide + the LTX-2.3 model card. Sources in higgsfield/research/.

## 21.1 THE ONE LESSON (verbatim across every tutorial)
**A text description is NOT a lock. An image reference IS a lock.**
Identity, weapons, wardrobe, locations must exist ONCE as frozen reference
images, attached to every generation that uses them. Text alone guarantees
drift. (soul_id_guide; consistent_characters_locations; elements master guide)

## 21.2 THE FIVE FAILURE MODES (why_generations_fail.txt) — our mapping
| Failure mode | What we saw | Their fix |
|---|---|---|
| 1 Facial/identity drift | male→female morph, Lara Croft creep | fixed face reference attached per generation; multi-angle |
| 2 Unnatural physics | (not primary yet) | describe physical behavior literally; load-before-action |
| 3 Prompt misread | guards re-read as repeated subject descriptions → re-render | ONE flowing narrative; no restated identity clauses |
| 4 Temporal inconsistency | hair short→long mid-clip | shorter simpler shots; explicit key details |
| 5 Weak/mismatched reference | single start-frame only | reference matched to scene; sharper; more anchors |

## 21.3 THE CHARACTER PIPELINE WE SKIPPED (zephyr_kpop 3-step)
1. Build the FACE (run one identity prompt until the right face appears).
2. Build the OUTFIT separately (every belt/bandage written explicitly).
3. FUSE into ONE MASTER ASSET: 'The character from image 1 wearing this
   outfit from image 2. Full body shot, white studio background, soft
   cinematic lighting, realistic.' — the fused sheet is what the video
   model checks against EVERY TIME.
WE NEVER BUILT THE FUSED MASTER ASSETS for DD/AZ. That is the structural
identity hole the 22B could not paper over.

## 21.4 THE PROMPT TEMPLATE (cinema_studio 4.0 + beginners_guide)
SCENE CONTEXT → ACTIVE REFERENCES (scoped, per-image clause:
  '@image2: the single source of truth for DD — 100% identical in every
   shot: face, short hair, outfit, twin crossbows [explicit list]. Its
   white studio background never appears.') → SCALE → SHOT-BY-SHOT
  (timestamps, camera position, body position, screen direction) →
  CAMERA LANGUAGE → LIGHTING → PHYSICS (load-before-action, cause-effect) →
  AUDIO → POSITIVE LOCKS (5-6 must-holds) + Continuity clause
  ('identical in every cut and exactly as in @image1... No identity drift,
   no morphing').

## 21.5 OFFICIAL LTX-2 PROMPTING RULES (ltx.video/blog/how-to-prompt-for-ltx-2)
- ONE flowing paragraph; the story flows beginning→end.
- 4-8 descriptive sentences total.
- Present-tense verbs for movement.
- Match detail to shot scale (closeups get more detail).
- Say how subjects look AFTER camera moves ('gives the model a better
  idea of how to finish the motion').
- Camera vocabulary: follows, tracks, pans, circles, tilts, pushes in,
  pulls back, overhead, handheld, over-the-shoulder, wide establishing,
  static frame.
- Name style EARLY (photoreal/analog film/etc.).
- LTX-2's strength: single-subject emotion, subtle gesture, facial nuance.
- Audio maps to motion (rhythm/energy/timing).
- Iterate on SHORT LOW-RES tests first; scale only after review.

## 21.6 WHAT CHANGES IN OUR STACK
1. BUILD THE FUSED MASTER ASSETS (DD/AZ: face card + armor + weapon → one
   full-body sheet each). Zero GPU if done with Qwen-Image-Edit from
   existing canon, else one cheap box pass.
2. REWRITE all 50 prompts: LTX official narrative style (4-8 sentences,
   flowing, present-tense) + Higgsfield reference-scope clause pointing at
   the fused master asset + Continuity lock. NO stacked identity-guard
   clauses (they cause failure mode #3).
3. I2V ANCHORS: attach the fused master asset as a reference image where
   the node graph allows (multi-image conditioning), not just the keyframe.
4. STRENGTH: revisit AFTER 1-3 land. The 1.0-vs-0.5 ladder was measuring
   a mis-prompted model.
5. TEST DISCIPLINE: short, low-res, single proof → review → scale. Never
   three full 1216×704 proofs of an unvalidated recipe.
