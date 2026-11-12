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

---

# §13 DIRECTOR CORRECTIONS — 2026-11-07 — USE FROM NOW ON

These override and extend everything above. Every asset and keyframe
from this date forward is judged against this section.

## 13.1 DD HEADWEAR — BACK-PIECE RULE
DD wears NO cap, hood, bandana, or mask on the head. A hood is allowed
ONLY as a back piece — a cowl resting on the shoulders/back like a cape.
The head is always bare so the glowing teal-blue underwater-wave hair
is fully visible in every asset and every frame. Any DD render with
head/face covering = REJECT.

## 13.2 BOTH WEAPONS ARE LEGENDARY GRADE — AND MUST APPEAR
DD: twin legendary HAND crossbows (Frostbite-class) — ice-blue arcane
crystal limbs, frost runes, string of frozen light, teal-blue glow.
AZ: legendary TWO-HANDED greatsword (Dawnbreaker-class) — pale sunsteel
blade, molten-gold runes, golden holy fire on the edge, sunburst crossguard.
Weapons are part of the character's identity: hero asset sheets and hero
keyframes must SHOW the legendary weapon in the hero's hands. A hero
sheet with no weapon is INCOMPLETE (director verdict on az_fused_idle,
az_fused_wrath, az_turnaround: armour good, weapon missing).

## 13.3 WEAPON SHEETS — ANTI-SLOP LAW
Weapon reference sheets are mandatory Elements. Every sheet:
- one weapon per sheet, grey studio background, 6 orthographic views
  (front-3/4, side, top, rear-3/4, head detail, grip detail)
- FANTASY CONSTRUCTION ONLY: a crossbow has a bowstring and limbs and
  fires bolts — it must NEVER read as a firearm. Any barrel, magazine,
  gun stock, Uzi/SMG/machinegun silhouette = total slop = REJECT.
- anti-slop negatives always appended: "firearm, gun, machinegun, Uzi,
  barrel, magazine, ammo clip, muzzle, modern weapon"
- canonical prompt pack for ANY platform (self-contained): higgsfield/
  jobpacks/33_WEAPON_SHEET_PROMPT_PACK_EXTERNAL.md

## 13.4 BOSS FACE
Mal'garot HAS a face, invented by us: a prolific molten-lava face —
lava dripping and running everywhere, drops falling to the ground.
(Faceless boss sheets are superseded.)

## 13.5 LOCATION BRIGHTNESS FLOOR
Environment plates must read clearly: no murk-dark grades. Minimum
exposure floor: subjects and terrain silhouette-readable at thumbnail
size. loc_canyon_plate v1 failed (too dark); v2 must lift exposure.

## 13.6 VERDICT LOG (asset library v4, 2026-11-07)
REJECT:  dd_fused_glacier, dd_turnaround   (headwear violation)
REJECT:  crossbow_sheet_v2                  (firearm silhouette + slop row)
REJECT:  boss_sheet_v2                      (wrong design: faceless)
REJECT:  loc_canyon_plate                   (too dark)
ACCEPT:  az_fused_idle, az_fused_wrath, az_turnaround
         (armour approved — RE-ISSUE with greatsword per §13.2)
ACCEPT:  dd_fused_idle (bare head confirmed by director)


## 14 P0 ASSET LIBRARY — COMPLETE AND ACCEPTED (2026-11-07)

The P0 deliverable for the Demonhunter-Paladin boss fight rendered, corrected,
sha256-verified, and DIRECTOR-ACCEPTED this date.

### The 12 accepted sheets (media/dhpf_assets_v4/)

```
DD  (bare head, back-cowl only, glowing teal-blue underwater hair):
  dd_fused_idle.png            idle master (face+outfit fused)
  dd_fused_glacier_v2.png      glacier master (headwear defect fixed)
  dd_turnaround_v2.png         4-view turnaround, bare head
AZ  (accepted armour, legendary greatsword added):
  az_fused_idle.png / az_fused_wrath.png      accepted masters
  az_fused_idle_w.png / az_fused_wrath_w.png  re-issued WITH greatsword
  az_turnaround_w.png                         turnaround + greatsword
WEAPONS/BOSS/LOCATION:
  crossbow_sheet_v3.png        anti-firearm legendary twin hand crossbows
  greatsword_sheet_v1.png      NEW legendary paladin greatsword
  boss_sheet_v3.png            molten-lava face, dripping
  loc_canyon_plate_v2.png      brightened canyon
```

### Rules derived from the P0 work — USE FROM NOW ON

1. **Fusion is mandatory.** A face card + a look card are NOT enough. Every
   hero needs the Higgsfield 3-step: face → outfit → fused master. The fused
   master is the asset every keyframe references.
2. **Headwear is a defect for DD.** Bare head at all times. A hood may exist
   only as a BACK PIECE (cowl on shoulders/back). Any cap, hood on head,
   bandana, or mask = automatic reject and re-render.
3. **Weapons must appear in hero sheets.** Both heroes carry legendary-grade
   weapons. A hero sheet without the weapon is incomplete.
4. **Weapon sheets carry the anti-slop law.** One clearly readable weapon per
   view, no merged/duplicated/rescaled props, same design from every angle,
   NO firearm silhouette (barrel/magazine/stock/machinegun). Reference-class
   assets may be sourced from the internet under CC0/CC-BY, logged.
5. **Boss needs a face reference sheet.** Mal'garot renders reference-less
   and drifts — his multi-view sheet (boss_sheet_v3.png) is now the locked
   image1 for all boss shots.
6. **Location plates need a brightness floor.** Judge the plate at final
   display size; if the set reads too dark, re-render brighter before any
   keyframe uses it.
7. **Stage sequencing.** Stage-1 renders (no dependencies) can batch
   immediately. Stage-2 renders (turnarounds) condition on stage-1 outputs;
   the runner must copy stage-1 outputs into ComfyUI input/ BEFORE the
   dependent job starts. A missed chain copy fails the job — verify refs in
   input/ before launch.
8. **Idle look cards live locally too.** dhpf_looks/ holds the accepted
   idle look cards; never assume they are only on a rented box.

## 15 P1 IDENTITY PROOF — RUNNING STANDARD

P1 is the single-figure close-up that proves the fusion method at scale.
The acceptance contract (all gates on ONE image):

```
1  face >=160px box (gate floor 120, target 160)
2  SFace sim vs enrolled centroid >= 0.50 (advisory only)
3  DIRECTOR'S EYES = final likeness call (SFace demoted to batch detector)
4  bare head, hair visible, no headwear
5  armour matches the fused master
6  weapon reads as the sheet's weapon, not a firearm
7  photoreal cinematic, no cartoon wash
FAIL ANY -> re-render (~$0.10). PASS -> P2 shot grammar.
```

The proof job references: real-photo face card (image1 = likeness source),
fused master (image2 = body/armour lock), weapon sheet (image3 = weapon lock).
Close-up scale fills the frame with head-and-shoulders; face >=160px.

## 16 OPERATIONAL LESSONS — 2026-11-07 P2 PREP

16.1 PROMPT-CANON SYNC AUDIT. Every time a director correction lands,
     RE-AUDIT every existing prompt that character/prop appears in.
     Corrections changed the assets but the 100 P2 job prompts still
     carried pre-correction text (male DD, hood up, faceless boss) —
     text that contradicts the references fights them and silently
     poisons batches. Caught and fixed 146 stale descriptions before
     the P2 render. USE FROM NOW ON.
16.2 READ BEFORE FLAGGING. A flagged defect ('insert prompts generic')
     was wrong on full read — the Action lines were specific; only the
     shared prefix was generic. Always read the FULL prompt before
     raising a defect against it.
16.3 HOST SELECTION. A California node sat in 'loading' 13+ min with
     SSH timing out — destroyed ($0, loading does not bill) and
     re-rented the China 4090 cluster that provisioned in 3-5 min
     every time tonight. Prefer recently-proven hosts over the
     nominally-cheapest unfamiliar node.
16.4 STALE FILE PROBES. scp can fail silently; always confirm pulled
     files exist with byte counts before reporting them delivered.

## §17 Unsupervised-burn incident (2026-11-08) — structural rules

Incident: Wan-FLF batch on instance 59683562 launched at ~09:19 CET with a direct
`flf_batch.py` launch (bypassing the rent script's autorun watchdog), no supervision
loop, and no copy-home step. The agent reported progress at 09:28 and then did not
check the box for ~6.5 hours. vast.ai billed at $0.41/h until credit hit $0 and the
instance EXITED. 0 of 35 rendered clips were copied home — total loss of the rental.

Hard rules that now apply to every GPU run:

1. **No launch without a live watchdog.** Every batch runner must call `watchdog()`
   with a ceiling at-or-below the user's approved cap hours, and must exit on
   `SERVER DEAD` (ComfyUI unreachable) instead of looping.
2. **Supervision cadence is part of the job.** A running GPU requires a poll at least
   every 20 minutes while the agent is active, and the render must be launched only
   when the agent can actually poll. If the agent must step away, stop the box first.
3. **Copy-home is incremental, never end-of-batch.** Every finished clip is scp'd
   home and sha256-verified the moment it lands; the batch never holds all output
   hostage on a billing box.
4. **Cap = watchdog.** The watchdog seconds are derived from the approved dollar cap
   at rent time, not a fixed default.
5. **Credit-exhaustion = exit = data loss.** Treat any 'exited' state as potential
   total loss of everything not yet copied home; report it that way.

---

## §18 No batch renders before a measured-motion proof gate (2026-11-08)

Two failed video attempts tonight (see §19, §20) burned real credit producing
unusable output. The common failure: a batch or near-batch run was attempted
before ONE proof clip had passed an objective motion check.

Hard rules that now apply to every video batch:

1. **Proof clip first, always.** One clip (typically kf_01), rendered with the
   exact batch parameters, must exist and pass all gates before any further
   clip is queued.
2. **The motion gate is MEASURED, not eyeballed.** Compute a frame-difference
   score (mean absolute pixel diff between consecutive decoded frames).
   Slideshow/crossfade degenerate output scores ~2.0; real motion scores >8.0.
   The proof clip must score above the gate before the batch proceeds.
3. **The fidelity gate is separate.** Face/armor match to the start frame
   (SFace or equivalent > 0.40) plus a human review for freeze/morph/crossfade.
4. **A failed proof stops the line.** Report honestly; do not scale a failing
   recipe. SkyReels-V3 14B at 720p with identity conditioning remains the
   known-good fallback tier.

---

## §19 Wan-FLF without its lightx2v LoRA degenerates to crossfade (2026-11-08)

Incident: Wan2.1-FLF2V-14B was launched with 12 plain steps because the
4-step lightx2v distillation LoRA (Kijai's
`Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors`, 302 MB)
returned HF 404 from the auto-downloader at that moment. The run completed
but produced a degenerate crossfade — the user verdict: "powerpoint slide
show of 2 images". The clip (media/dhpf_hb_clips/vp_01.mp4) is kept as
FAILED / REFERENCE-ONLY.

Hard rules:

1. **Never run plain steps on the distilled FLF graph.** Wan-FLF with lightx2v
   expects ~8 steps at cfg ~1.0; plain steps at cfg >1 silently degrade into
   a crossfade between the two keyframes.
2. **Resolve the LoRA before renting.** Confirm the LoRA file resolves live
   (HTTP 200, correct size ~302 MB) as part of zero-cost preflight, the same
   way the checkpoint itself is verified. A 404 on the LoRA is a BLOCKER,
   not a warning — fix the download URL or use a different revision.
3. **Degenerate output is still billed.** The slideshow clip consumed GPU time
   at full rate. Do not treat a technically-successful exit code as a passed
   test — the motion gate in §18 is the arbiter.

---

## §20 vast.ai template boxes with autorun watchdogs reap tenant processes (2026-11-08)

Incident: two rental boxes (59730020 "lemon", then 59734990) shipped a
template whose autorun script reaped any process it did not start and wiped
/workspace on a schedule. Two carefully prepared ComfyUI + weights deploys
were destroyed mid-setup. Both boxes were destroyed; ~$1.10 of credit churned
on setup alone.

Hard rules:

1. **Prefer plain pytorch templates** (or templates with a documented, passive
   autorun) over marketplace "one-click" templates with active watchdogs.
2. **If a template box must be used, work within the autorun window**: either
   hook your work into the template's own startup path, or disable/patch the
   autorun before it fires (tools/vast/edit_autorun.sh exists for this).
3. **Detect early, destroy fast.** If /workspace vanishes or processes die
   unexpectedly minutes after launch, do not retry into the same template —
   destroy and re-rent a plain image. Two strikes on one template class is
   enough.
4. **Setup cost is real cost.** Weight download time is inside the billed
   window (existing rule, now restated): a box destroyed during setup has
   burned provisioning + download + teardown with zero output.

---

## §21 LTX 2B/2.3 wiring reference — the exact working node chain (2026-11-08)

After ~400 wiring iterations on box 59773014 the correct ComfyUI graph for
LTX 2B v0.9.5 + T5-fp8 was established. This chain is canonical; do not
substitute node names from other ComfyUI-LTXVideo forks without re-proofing.

```
CheckpointLoaderSimple        -> MODEL + VAE           (ltx-2.1-2b-distilled or 2.3 ckpt)
LTXVGemmaCLIPModelLoader      -> CLIP                  (REQUIRES FULL Gemma HF layout:
                                                          config.json + tokenizer files +
                                                          processor files; safetensors alone
                                                          is INSUFFICIENT — loader fails
                                                          with tokenizer/processor errors)
CLIPTextEncode                -> positive + negative CONDITIONING  (T5 text)
LTXVConditioning              -> combines CONDITIONING + width + height + length + fps
BasicGuider                   -> GUIDER                (conditioning + model)
KSamplerSelect                -> SAMPLER               (euler / dpmpp_2m)
LTXVScheduler                 -> SIGMAS                (simple / normal; LTX-specific)
RandomNoise                   -> NOISE
LoadImage                     -> start-frame IMAGE
LTXVImgToVideo                -> LATENT                (image + positive cond + negative cond)
LTXVBaseSampler               -> samples LATENT -> LATENT (guider+sampler+sigmas+noise)
VAEDecode                     -> IMAGE
CreateVideo                   -> VIDEO                 (frames -> video container)
SaveVideo                     -> save VIDEO input, format video/h264
```

Parameter contract (2B v0.9.5, no step-distill LoRA exists for 2B):

- frames = 8k + 1 (65 / 81 / 121 / 257); 97 is invalid
- width/height multiples of 32; primary 1216x704; NOT 1280x720 (720 % 32 != 0)
- fps 24 via LTXVConditioning
- steps 30, guidance 3.0 (NOT cfg 1.0 — that is Wan-lightx2v lore)
- sampler euler / dpmpp_2m, scheduler simple / normal
- 4-step LoRA applies ONLY to the 22B distilled variant (ltx-2.3-22b-distilled-1.1)

Proof status at handover: graph correct, kf_01 proof clip PENDING on box
59773014. See higgsfield/39_2026-11-08_LTX_DEPLOY_HANDOVER.md and
higgsfield/38_LTX_VIDEO_GENERATION_SPEC.md.

---

## Armor-sheet naming convention (FINAL, 2026-11-08)

After a ~60+ rename cycle during tonight's consistency pass, the canonical
armor/character-card names for the Hollow Bloom (Shup liviot Cvet) design
settle as:

```
media/dhpf_design_v5/dd_armor_base.jpg   (Demon Hunter — complete character card)
media/dhpf_design_v5/az_armor_base.jpg   (Azulon Paladin — complete character card)
```

`_base` = the complete, hash-locked character card for that hero.
Sibling state/base variants keep their stable names: dd_armor_state.jpg,
az_armor_state_a.jpg, az_armor_state_b.jpg, dd_armor_base.jpg, az_armor_base.jpg.

Hard rules:

1. **All references resolve by content hash, never by filename.** Every prompt
   pack, spec, job file and registry entry references the SHA256 of the sheet,
   so renames do not break the look-lock. Renaming is safe; re-hashing is not.
2. **These two names are canon from now on.** Do not introduce a third naming
   scheme for the same sheets. New states get new stable suffixes
   (`_state_c`, `_wounded`, etc.), never a rename of the `_base` card.
3. **Record the convention in ASSET_REGISTRY.md + asset_registry.json** so
   external generators receive the same names.

---

## Credit ledger — 2026-11-08 session

```
2026-11-08 16:00-22:40 CET session:
  start balance   ~$4.87
  Wan2.1-FLF 12-step no-LoRA attempt (slideshow)      ~part of spend
  Wan-FLF 8-step lightx2v lemon box 59730020 + 59734990  ~$1.10 setup churn
  LTX 2B box 59773014 provisioning (still in progress at handover)
  total spent     ~$2.4
  end balance     ~$1.79-2.60 (verify: /opt/venv/bin/python tools/vast.py balance)
```

Live balance must be verified with the vast.ai API before the next spend
decision; do not quote this table as current.

---

## §18 ALWAYS rent with the onstart SSH-key-injection script — and let the boot finish (2026-11-11)

**Rule.** Every rental MUST be made with a `rent_k6.py`-style **`onstart` script
that injects the SSH public key directly into the box** at boot:
`echo '<PUBKEY>' > /root/.ssh/authorized_keys` + enable
`PermitRootLogin yes` + `PubkeyAuthentication yes` + restart sshd. This
**bypasses the Vast account SSH gateway entirely** — the box gets the key
locally, so SSH works regardless of gateway key-provisioning issues.

**Why.** On 2026-11-11 a run of fresh rentals all returned
"Connection closed" on SSH. The key WAS registered and correct. Root cause was
NOT an outage: the boxes were simply **still booting** (the `onstart` script
had not finished installing the key yet), and the boxes were **destroyed after
only ~2 minutes / 6-8 SSH attempts** — before `onstart` completed. ~6 boxes
were churned and ~$4.4 burned on this misdiagnosis.

**Standing practice.**
1. Rent via `tools/vast/rent_k6.py` (or replicate its `onstart` body) — never a bare rental that relies on gateway key propagation.
2. **Let the box boot.** `rent_k6.py` self-waits for `SSH_OK` (its log shows the handshake). Do NOT destroy a box on early "Connection closed" — that is the normal mid-boot state. Wait the full ~3-4 minutes.
3. Only destroy a box after `SSH_OK` was reached AND a real fault is confirmed, or after a genuinely long (≥10 min) unreachable window.
4. "The user said the key is fine" is a signal to re-examine the boot/patience assumption, not to re-explain key registration.

---

## §19 THE N-CLIP START-FRAME-ONLY MODEL (all keyframes = start frames; N = keyframe count) — director-authored (2026-11-11)

**The principle.** Render N keyframes for the storyboard (typically 2 per shot: `kf_NN_start` + `kf_NN_end`; N = 2 × shot count, any keyframe set works). Run **ALL N as individual START frames → N clips**. The END keyframes are NOT discarded — each is the start of its own continuation clip. **N is NOT a fixed number — it follows the shot list** (a 23-shot storyboard → 46 keyframes → 46 clips; the current Hollow Bloom board is 50 shots → 100 keyframes → 100 clips). This REPLACES the start→end (FLF) pair model wherever the end-frame lock is unreliable or the model is start-image-only.

**Why it wins.**
- Kills the end-lock failure. Wan-FLF measured corr-to-end collapsing to ~0 at f120; LTX-2.3 / K6 / SkyReels-V3 / Mochi-1 are start-image-only by spec. No end frame to reach = no end-lock problem.
- Uses every rendered keyframe (the 50 end-frames cost the same as the starts; discarding them wastes half the identity-locked art).
- Cuts carry continuity. Continuity lives in the KEYFRAME CHAIN (`kf_NN_end` matches `kf_(N+1)_start`, authored as a board), NOT in any single clip reaching a target. A hard cut from clip N (anchored at `kf_NN_end`) to clip N+1 (anchored at `kf_(N+1)_start`) reads as continuous motion because the keyframes already match.

**The clip chain.**
```
clip_001  start=kf_01_start.png   → continues SHOT 01's opening pose
clip_002  start=kf_01_end.png     → continues SHOT 01's end (now the start)
clip_003  start=kf_02_start.png   → SHOT 02 opens ...
clip_004  start=kf_02_end.png     → ... and continues
  ... 100 clips, one per keyframe, in keyframe order.
```
Edit = concat clip_001..clip_100 in order. No in-prompt transition; the cut IS the transition.

**The prompt (one per keyframe, ~400-850 chars)** — see `39_CORRECTED_PROMPT_STANDARD.md` (100-CLIP section) + `tools/vast/jobfiles/ltx_jobs_100.json`. Rules: ONE present-tense narrative paragraph; CONTINUATION not scene-change (extend the frozen moment, never teleport); MOTION FIRST; IDENTITY STATED ONCE (restatement = morph); HOLD-ANCHORS for carried props (twin crossbows, greatsword) as a held subject, never a guard/clamp; NO ENDPOINT FRAME (describe the motion's end in words); motion calibrated to the shot (gentle for hero closeup, thrash for boss).

**Job file.** `tools/vast/jobfiles/ltx_jobs_100.json` — 100 continuation prompts, one per keyframe, generator-agnostic. The SAME prompts drive Wan-FLF (start-only), LTX-2.3, K6, or any start-image model; only the render command differs.

**Model routing (proven ledger).**
- Wan-FLF: only native FLF option; run START-ONLY under this model until the end-lock is proven fixed (16-step untried).
- LTX-2.3 22B distilled: start-only native; renders via official `ltx_pipelines.distilled` (38 spec). **"Dead" verdict (42) is UNRESOLVED — neither confirmed nor retracted.** The 2026-11-12 uv-sync retry on box 60279666 NEVER RENDERED: blocked by a DEAD HF_TOKEN (whoami 401) + the LTX-Video repo returning 401 even anonymously (repo now possibly gated) + google/gemma gated (unsloth mirror OK, 307). So the uv-sync-vs-nanobind question is untested on this box. The earlier top-tier clips ran on a DIFFERENT box (A100 60075318) with a working token. **Prereq: a VALID HF_TOKEN with access to the LTX-Video repo; else use the unsloth gemma mirror + anonymous/valid-token download.** ~2-3 min/clip on 48GB if it runs — the fast high-quality lane, but UNPROVEN until a render completes.
- K6 / SkyReels-V3 / Mochi-1: start-only by spec.

---

## §20 USE THE TEMPLATE'S PRE-INSTALLED COMFYUI — never pip-reinstall torch (2026-11-11)

**Rule.** Vast's `vastai/comfy_v0.44.0-*` template images ship **ComfyUI + a working torch already installed** (in the image or a venv). On rental, FIND and USE that existing install. Do NOT clone a fresh ComfyUI and `pip install -r requirements.txt` into the system python — that reinstalls torch (~35 min stuck, several GB) and is the single biggest setup-time/cost waste observed.

**Why.** On 2026-11-11 a box burned ~$6.9 (2.3× a $3 cap) largely because the setup cloned a fresh ComfyUI and a `pip install torch` into the system env hung for ~35 min. The template's torch was already there. The redundant reinstall was the whole stall.

**Standing practice.**
1. Rent a ComfyUI template image (`vastai/comfy_v0.44.0-*`).
2. On SSH, look for the existing install first: `ls -d /opt/ComfyUI /workspace/ComfyUI /ComfyUI /opt/workspace-internal/ComfyUI`, and check `python -c 'import torch; print(torch.__version__)'` in any venv. USE IT.
3. Only the MODEL WEIGHTS + the model's LoRA need downloading (~23 GB, ~5 min at 4.7 Gbps) — not the framework.
4. If a dependency is genuinely missing, install just that package (pin torch to the template's existing version), never a blanket requirements reinstall.
