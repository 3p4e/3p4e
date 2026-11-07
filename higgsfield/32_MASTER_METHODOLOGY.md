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
