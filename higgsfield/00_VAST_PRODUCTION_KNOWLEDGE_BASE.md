# VAST PRODUCTION KNOWLEDGE BASE
> Standard practice + knowledge document for the VAST film pipeline.
> Governs every production. Supersedes all per-film notes where they conflict.
> Built 2026-11-07 from: production doctrine, 31 rethink review, 32 master
> methodology, Higgsfield study digest (11 tutorials), MiniMax H3 research.
> Audience: any agent or human continuing this work.

---

## 0. HOW TO USE THIS DOCUMENT
1. Read §1-§3 before any production decision.
2. The phase gates in §4 are mandatory. Do not skip a gate.
3. The asset library in §5 must exist before any keyframe renders.
4. Every prompt follows the scaffold in §7. Free prose is not allowed.
5. Every film has a storyboard HTML per §8. It is the single source of truth.
6. Money rules in §10 are hard rules, not guidelines.

---

## 1. THE ONE LAW
**A text description is NOT a lock. An image reference IS a lock.**
Every recurring asset — face, weapon, costume, tattoo, location, prop —
is built ONCE as a frozen reference image and attached to EVERY frame
that uses it. Text alone guarantees drift. This law overrides every
prompt-writing habit. (Higgsfield, all tutorials; confirmed by MiniMax Ref2VA.)

---

## 2. PRODUCTION DOCTRINE (user-declared, binding)
1. Research first. References and source material before prompts/models/shots.
2. Narration and dialogue are written as their own step, before visuals.
3. Visual-first. Design the shot as an image problem before choosing models.
4. Photoreal is the default target look. Stylised only by explicit exemption.
5. First-last-frame (FLF) construction, 40–60 shots per film.
6. Explicit camera grammar per shot; vary scale/angle/movement deliberately.
7. Validate motion at the sequence level, not just per clip.
8. No self-made benchmark. Quality bars come from external/user-named targets.
9. Proof before scale. One FLF proof scene at the target resolution before a batch.

---

## 3. IDENTITY STANDARD
- Close-up likeness is judged by the DIRECTOR'S EYES. Always.
- SFace is a batch-regression detector only. Its absolute scores are
  unvalidated for generated faces; use it to catch drift between frames,
  not to certify identity.
- Face-size floor: any verified face box < 120px = AUTO-REJECT (machine gate).

---

## 4. PHASE GATES (mandatory order)
```
P0  ASSET LIBRARY    Build + director-accept every asset in §5.
                     Grey backgrounds, multi-view. ~$0.60-0.80.
                     NOTHING renders before this gate passes.
P1  IDENTITY PROOF   One CLOSE-UP still, all gates at once: real face card
                     as image1, fused master as image2, face >=200px,
                     director's likeness call, weapon matches, look accepted.
P2  SHOT GRAMMAR     Per-shot table from the storyboard: shot_type, anchors,
                     face floors, screen direction, positive locks.
P3  CHAIN PROOF      One MEDIUM shot pair -> FLF -> verify motion +
                     mid-clip identity + weapon in ONE artifact.
P4  SCENE PROOF      One complete 4-6 shot scene (~20-30s) at the locked look.
                     The first product-level proof.
P5  PRODUCTION       Scene batches. Per-batch gates; any failure stops the line.
```
A gate fails = stop, diagnose, fix at the lowest level, re-proof. Never scale on a failed gate.

---

## 5. ASSET LIBRARY STANDARD
Every asset: neutral grey/white studio background, no scene lighting,
no extra faces, one subject per sheet. Director must visually accept
each asset before it enters the library.

### 5.1 Per hero, per wardrobe state
```
A1  FACE CARD       Enrolled identity (real-photo centroid). EXISTS for
                    DD and AZ (ddface_a/b, azface_a/b).
A2  OUTFIT SHEET    Full-body, ONE state (hooded / bare / idle / wrath),
                    every gear detail written explicitly. LOOK CARDS EXIST.
A3  FUSED MASTER    "character from image 1 wearing outfit from image 2,
                    full body, white studio bg, realistic" -> ONE sheet.
                    THIS IS THE MISSING LINK. Build it before anything else.
A4  TURNAROUND      Front / back / left / right profiles of the A3 master.
A5  WEAPON SHEET    ~6 orthographic views per recurring weapon:
                    front-3/4, lateral, top, rear, bottom. No hand, no figure.
```
### 5.2 Boss
```
B1  BOSS SHEET      Multi-view turnaround. Faceless by canon. Forge-core,
                    molten whip-arm. NO human refs (face-leak gate).
```
### 5.3 Locations & props
```
L1  LOCATION PLATE   3/4 establishing still, no people, fixed light direction,
                     3-4 checkable landmarks. One per scene.
P1  PROP/ MATERIAL   Real internet photographs (CC0 / public domain / CC-BY
                     with attribution logged). Real photos pull output toward
                     photoreal; generated art pulls toward stylised art.
```
### 5.4 Storage
All accepted assets live under media/<project>_assets/ with SHA256SUMS.txt.
Asset identity is by filename; the storyboard references assets by these names.

---

## 6. SHOT GRAMMAR STANDARD
Shot types drive everything. This table resolves the three conflicting
gates (fight blocking vs face readability vs wides).

| SHOT TYPE    | FACE RULE                     | image1 (strongest slot) | image2                 |
|--------------|-------------------------------|-------------------------|------------------------|
| CLOSE-UP     | face >=200px, front 3/4       | real FACE CARD (A1)     | FUSED MASTER (A3)      |
| MEDIUM       | face >=120px, >=1 hero front  | FUSED MASTER (A3)       | real FACE CARD (A1)    |
| WIDE (2hero) | >=1 hero 3/4-front, 80-120px  | FUSED MASTER (A3)       | WEAPON SHEET (A5)      |
| BOSS-ONLY    | zero human refs               | BOSS SHEET (B1)         | (none)                 |

Energy comes from weapon/body LINE, not from hiding faces. A fight shot
can be intense with a readable face. Screen direction is locked per scene
("moves screen-left to right, never mirrored") and written into every prompt.

---

## 7. PROMPT SCAFFOLD STANDARD (every shot, no exceptions)
```
SCENE CONTEXT      one line: world + mood + what happens
ACTIVE REFERENCES  one scoped clause per reference image:
                   "<<<image_1>>>: the fused master of [hero] — 100%
                   identical in every shot: [exact face/hair/armour/weapon
                   list]. Its studio background, pose, and lighting are
                   NOT used."
ACTION             chronological beats: "first... then... as... finally"
                   (2-3 beats for a 5s shot; cause -> effect, literal physics)
CAMERA             shot size + ONE camera path + pace + lens + distance
                   (never combine drone + whip-pan + orbit + zoom in one shot)
SCREEN DIRECTION   locked per scene; never mirrored
LIGHTING           one light source, direction, palette, exposure
AUDIO              spatial SFX + restrained music + any dialogue (mk)
POSITIVE LOCKS     the 5-6 things that MUST hold across every shot
NEGATIVE           standard negative + state-specific terms
```
Cap visual anchors at 3-5. Overloaded text makes the model choose motion
over identity. (Higgsfield rule.)

---

## 8. STORYBOARD HTML STANDARD
One self-contained HTML per film. Two layers:
- HUMAN LAYER: director pre-vis (acts, shots, blocking, camera, cues).
- MACHINE LAYER: <script type="application/json" id="storyboard-spec">
  scraped directly by the render pipeline with zero re-interpretation.

### 8.1 Machine-layer per-shot schema (required keys)
```
shot_type, face_floor_px, asset_refs[], ref_scope, screen_dir,
positive_locks[], beat_timeline[[t0,t1,beat]...],
size, angle, move, dur, clip_s, kf_first, kf_last,
narration_mk, dialogue_mk, continuity, motion
```
### 8.2 Machine-layer per-scene schema (required keys)
```
location_ref, global_locks[], palette[], light_direction, time_of_day
```
### 8.3 Global render contract (per film)
```
aspect 16:9, 1280x720, 24fps, FLF true, language mk, 40-60 shots,
fixed-per-shot seeds, negative_prompt, style_anchor (external refs only)
```

---

## 9. MODEL STACK STANDARD (current, proven)
```
Keyframes    Qwen-Image-Edit-2511 fp8, 50 steps, on Vast (native-FP8 GPU)
Video        Wan2.1-FLF2V-14B-720P, 8 steps (96% of 20-step motion, ~$0.166/clip)
Audio        OmniVoice/MOSS-TTS (Macedonian) + ffmpeg assembly; VoxCPM2 for EN
Gates        SFace regression detector + director's eyes (identity),
             frame-diff motion check (no static frames), faceless gate (boss)
Alternative  MiniMax H3 (open-weights, native audio, FL2VA + Ref2VA) —
             documented, not pivoted; revisit only if Wan path blocks
```

---

## 10. FINANCIAL & OPERATIONAL RULES (hard)
- Zero-cost prep before any rental: scripts validated, jobs built, estimate
  itemized. The render is the only step that should cost money.
- Every rental is explicit: named offer, stated rate, hard cap agreed BEFORE
  the API call. Report actual spend against the cap afterwards.
- Validate what a job builder emits (duration, resolution, frames, checkpoint,
  input list) before spending; confirm from the run log what executed.
- Never silently downgrade model tier/resolution/conditioning for cost.
- Copy -> checksum-verify -> THEN destroy. Per-file, never batch.
- Stopped instances still bill storage; destroy when idle unless re-rendering soon.
- No external reference may be non-free-licence (CC0/PD/CC-BY only, attribution logged).
- Do not commit biometrics. faces/ is gitignored.

---

## 11. CONSISTENCY CHECKLIST (run before every multi-shot batch)
```
[ ] Location plate saved + accepted (layout, light, 3-4 landmarks listed)
[ ] Character fused masters saved + accepted (face+body+gear in one sheet)
[ ] Weapon sheets saved + accepted (multi-view)
[ ] Description lists the fixed details per asset
[ ] Settings identical for every angle of a scene (palette, light, lens class)
[ ] Every prompt carries its asset refs + scoped clause
[ ] Screen direction locked; no mirroring
[ ] Every frame checked against the asset sheets BEFORE moving on
[ ] First generation reviewed before scaling
```

---

## 12. DOCUMENT INDEX
```
00_VAST_PRODUCTION_KNOWLEDGE_BASE.md   <- this file (governing)
23_ERROR_REGISTER_AND_FIXES.md         25-item error register + preventions
24_CRITIQUE_REANALYSIS_REPORT.md       critique response, verified claims
26/27_BOSSFIGHT_SPEC(_v2).md           demonhunter+paladin bossfight spec
28_BLOCKING_AND_STAGING_LAW.md         composition law (kept, refined by §6)
30_KEYFRAME_CONSISTENCY_HANDOVER.md    keyframe correction + Higgsfield method
31_FULL_RETHINK_REVIEW.md              8 root causes + loose-ends audit
32_MASTER_METHODOLOGY.md               aligned method (merged into this KB)
research/STUDY_DIGEST.md               Higgsfield 11-tutorial digest
research/minimax/                      MiniMax H3 sources + format guides
research/*.txt                         full tutorial texts (11 files)
```
