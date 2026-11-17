# 31 - FULL RETHINK REVIEW (2026-11-07)

Director request: step back, review every decision, every loose end, every
variable, every pipeline, methodology and solution in full.

VERDICT UP FRONT: the system is mis-architected. My error was patching local
variables inside a bad architecture instead of seeing the architecture. Every
patch produced a new failure mode. That is the signature of a structural
problem, not a bag of bugs. This document re-derives the structure, audits
every loose end, and defines the rebuilt pipeline.

---

## 1. THE PATTERN

Six deliverables, six rejections, each a DIFFERENT failure mode:

- Karsus v3 (118s): slideshow, upscaled, faces unresolved
- Paladin teaser: praised then barred as benchmark; 1080p was software upscale
- Susanoo photoreal: slideshow, ignorant prompts
- Origami seraph: wrong anchor, unrelated to the angel
- Bossfight v1 keyframes (14 stills): weapon slop, hood toggle, tattoo random, faces fail
- Bossfight v3 proof (6 stills): identity gate FAILED all 4 hero frames (0.22/0.06 vs 0.50; 2 frames zero faces)

Every fix was local: better prompt, more steps, LoRA, look cards, blocking law.
Each produced a NEW failure. A system that trades one failure for another after
every patch has the patches aimed at the wrong level.

---

## 2. ROOT CAUSES (the architecture, not the prompts)

### RC1 - LOSSY IDENTITY CHAIN (core defect)
real photos -> enrolled centroid -> GENERATED fantasy illustration of a person
-> keyframes conditioned on the ILLUSTRATION + tiny face crop -> gated against
the ORIGINAL real-photo centroid.

The model never sees the person. It sees an illustration of a person who
resembles the person. Then I measure the result against ground truth. Identity
degrades at every hop. No prompt fixes a lossy reference chain.

### RC2 - THREE GATES THAT CONTRADICT EACH OTHER
- Blocking law (my rule): bodies turned INTO the fight -> 3/4-back views -> faces hidden
- Identity gate (my rule): readable faces >=120px
- Cinematic wides (doctrine): 1280x720 with two figures -> faces 60-100px

All three cannot hold in the same frame. I wrote all three as mandatory and
never noticed the contradiction until the proof failed. Architecture error,
not a render error.

### RC3 - NO LOOK LOCK
Film practice: approve concept frames (THE LOOK) before production. We never
did. Every film emerged with a look never signed off on; every rejection was a
look rejection delivered on delivery day. The photoreal question was deferred
into "fix it with prompting" for six rounds. Prompts cannot override a model's
training distribution. The achievable look must be confronted as a DECISION.

### RC4 - WRONG PROOF PROTOCOL
Every proof tested ONE variable: motion, then blocking, then identity. A film
requires ALL gates simultaneously in ONE shot. A motion-passing proof is
worthless when the same shot fails identity. Proof unit must be the product,
not the variable.

### RC5 - WRONG ANCHOR PRIORITY
Qwen transfers strongest from image1. I spent image1 on the costume card for
EVERY shot type, so identity got the weak slot. Correct design is shot-type
dependent:
- CU/MED (face is subject): image1 = best REAL PHOTO, image2 = look card
- WIDE/INSERT (figure/env subject): image1 = look card, no face gate
One anchor policy for all shot types was the bug.

### RC6 - COMPOUNDING STAGES
Stylized/drifting stills feed Wan FLF, which interpolates BETWEEN inconsistent
endpoints, amplifying still defects into in-between mush. Stills and video
gated separately; the chain was never gated as one.

### RC7 - FACE-GATE DOMAIN MISMATCH
SFace is calibrated on real photos. A generated 64px face vs a real-photo
centroid is cross-domain noise. Thresholds (same_person 0.363, confirm 0.72)
never validated for generated content; my ad-hoc 0.50 is unmoored. For the
director's own face, the ground truth is the director's eyes, not SFace.

### RC8 - VISUAL-FIRST INVERTED
Doctrine says design the shot as an image problem before choosing models. I
chose models first, forced shots into their constraints, then patched prompts.
Inverted, exactly as the doctrine warns.

---

## 3. LOOSE ENDS / VARIABLE AUDIT (repo state 2026-11-07)

PROVEN, KEEP:
- Wan2.1-FLF2V-14B-720P motion @ 8 steps: 96% of 20-step, $0.166/clip, zero static frames
- Higgsfield image-lock method (look cards): v3 proof carries weapons/hood/tattoo consistently
- Macedonian TTS stack (OmniVoice/MOSS) + ffmpeg assembly
- Story layer: 50-shot spec, 7 Macedonian lines, ability-VFX map

NEW, UNVERIFIED:
- media/dhpf_proof_v3/crossbow_prop_sheet.png (rendered, never used in a shot)
- media/dhpf_proof_v3/malgarot_look_card.png (rendered, NOT wired into 100-job set)

STALE, QUARANTINED (moved to media/dhpf_keyframes/_quarantine_pre_correction):
- kf_01/02/03 start+end.png from FAILED pre-correction batch (face-crop-only refs)

DERIVED-BUT-LOSSY (RC1/RC5):
- dd_look_glacier_v3 / az_look_wrath_v2 used as image1 for identity-critical shots

REBUILD, NOT PATCH:
- tools/vast/jobfiles/bossfight_kf_jobs.json (predates composition fix, boss card, anchor redesign)
- tools/vast/build_keyframes.py (needs shot-type anchor policy)
- tools/vast/build_bossfight_jobs.py (needs camera-grammar revision)
- Docs 28/29/30 (need revision after decisions)

FINANCIAL:
- Credit $13.8925 - zero instances - nothing billing. Clean slate.

AUDIO LOOSE ENDS:
- VoxCPM voice clone BLOCKED on director's 10-30s reference recording
- Music score bed: never produced; needed before film assembly

---

## 4. RETHOUGHT METHODOLOGY (phase-gated, product-level proofs)

P0 LOOK LOCK (zero cost): director judges the six v3 stills as style frames.
Accept stylized OR demand photoreal. No rendering until this decision exists.

P1 IDENTITY PROOF (~$0.10): one close-up, all gates at once. image1 = best
real enrolled photo, image2 = look card. face >=120px, director's likeness
call, weapon matches, look per P0. Never scale on a failed P1.

P2 SHOT GRAMMAR (paper): per-shot table of shot type, faces-that-must-be-
readable, anchor policy, face-size floor. Reconciles RC2 in writing before GPU.

P3 CHAIN PROOF (~$0.35): one medium pair -> Wan FLF 8-step -> verify motion +
mid-clip identity + weapon in ONE artifact. Proves still-pair-video as a chain.

P4 SCENE PROOF (~$1): one complete 4-6 shot scene (~20-30s) at locked look.
First product-level proof.

P5 PRODUCTION (~$10-13 for full 50 shots): scene batches with per-batch gates.
Any batch failing identity/weapon/look stops the line.

---

## 5. DECISIONS ONLY THE DIRECTOR CAN MAKE

D1 - THE LOOK: judge the six v3 stills as style frames.
   ACCEPT stylized cinematic -> proceed, look locked.
   DEMAND photoreal -> open-source photoreal + enrolled identity + locked
costume is at the edge of what exists. Qwen-Edit on REAL PHOTOS is our best
available shot and lands 'cinematic realistic', not photographic.

D2 - IDENTITY STANDARD: confirm close-up likeness judged by DIRECTOR's eyes
(SFace demoted to batch-regression detector). SFace absolute thresholds
unvalidated for generated faces (RC7).

D3 - SCOPE: full 50-shot film (~$10-13 more) OR polished 12-15 shot short
(~$3-4) as first deliverable. Given history, I recommend the short.

---

## 6. NEXT ZERO-COST ACTIONS (on 'go')
1. Quarantine the 6 stale keyframes (DONE this session).
2. Rebuild build_keyframes.py with shot-type anchor policy (real-photo image1
for CU/MED; look card image1 for WIDE; boss card for all boss shots).
3. Rewrite doc 28 into full shot grammar with face-visibility table.
4. Regenerate 100-job set; machine-verify refs, no face-leak, caps.
Then P1 awaits only 'rent ~$0.10'.
