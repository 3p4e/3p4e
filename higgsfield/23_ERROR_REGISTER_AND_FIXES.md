# 23 — Complete Error Register, Fixes & Preventions (VAST project)

> Honest accounting of every wrong result and wrong claim across the VAST project,
> each with the fix applied and the prevention adopted. Grouped by root theme.
> The ordering is thematic, not chronological. Compil​ed 2026-11-05.

---

## Part A — Verification discipline (the recurring meta-failure)

### A1. Reported a hash match as proof of correctness
- **What went wrong:** I reported KORY as “feminised ✓” because `sha256` matched a previously
  stored card. A hash only proves a file is byte-identical — it says nothing about gender,
  identity quality, or whether the image is correct.
- **Fix:** Re-examined the actual pixels; found the moustache/beard shadow intact.
- **Prevention:** A hash is an *integrity* gate, never a *correctness* gate. Every
  visual/output claim must be checked by eye (and an appropriate classifier) before being
  reported as success.

### A2. Reported an SFace similarity score as proof of gender/quality
- **What went wrong:** Gated 6/8 user-uploaded KORY images as “passing” on SFace cosine
  similarity alone. SFace measures *identity* (“same person?”), not gender. All six
  “passes” were the same bearded man in a red wig — several bare-chested.
- **Fix:** Eyeballed every image and rejected the batch regardless of score.
- **Prevention:** Separate the axes. Identity (SFace) and gender presentation (facial-hair /
  femininity check) must be independent gates; a pass on one never implies a pass on the other.

### A3. Trusted “fingerprint-verified” numeric passes as success
- **What went wrong:** The same pattern recurred three times: hash-then-claim (KORY),
  score-then-claim (KORY uploads), and seed-hash-as-anchor (Origami).
- **Fix:** Named the pattern explicitly as a systemic defect and added visual-first review.
- **Prevention:** Rule: “No numeric pass alone justifies a ‘done’ claim. Look at the output.”

### A4. Trusted training-data memory instead of live sources
- **What went wrong:** Claimed SkyReels V2 offered “infinite length”, recommended Wan 2.5
  (no open weights), and assumed the Anthropic API could generate images (404) — all from
  stale memory.
- **Fix:** Re-verified model availability, gating, and licence against official docs
  (`source-driven-development` skill).
- **Prevention:** For any model/API/licence claim: consult the current source, not memory.
  Record the source URL and date.

---

## Part B — Identity & face cards

### B1. KORY was never actually feminised
- **What went wrong:** All 15 “KORY” source photos on disk were the same bearded man in a red
  wig. The card I rendered KORY frames from was DD's face with a moustache and beard shadow,
  contradicting canon (“clean-shaven, female read”).
- **Fix:** Generated a new six-card female KORY set (Nano Banana Pro, single reference,
  instruction-phrased), gate-verified (pairwise 0.579, faces 379–515 px).
- **Prevention:** Before enrolling a persona, inspect the source set by eye. Never accept a
  card whose provenance is “we copied a file.”

### B2. Qwen feminisation edit failed because the reference set repeated the male face
- **What went wrong:** The edit job fed two identical bearded references (`image1` and
  `image2` both DD). Two male references outvote the text instruction “make female”; the
  model preserved the moustache. Negatives cannot override a reference image.
- **Fix:** Dropped the duplicate male reference and used one distinct anchor.
- **Prevention:** Audit reference-image sets for conflicting identity signals before rendering.

### B3. Silent face-detection downscale bug destroyed Geni's enrolability
- **What went wrong:** Detection ran on downscaled frames, so every Geni face measured
  14–116 px — far below the 256 px enrolment minimum — and zero cards were produced.
- **Fix:** Ran detection at full resolution; relabelled unsupported “geni” labels.
- **Prevention:** Face-QC must run at native resolution; add an assertion that detected crops
  exceed the enrolment minimum and fail loudly otherwise.

### B4. Classifier was single-identity (Oleg vs not-Oleg)
- **What went wrong:** No Geni or Kory material was wireable into the classifier.
- **Fix:** Designed a multi-identity nearest-of-N schema with an UNKNOWN band; KORY later
  enrolled from the generated set.
- **Prevention:** Identity infrastructure must be N-way from the start when the cast has N
  people.

---

## Part C — The film itself (Susanoo & Orochi)

### C1. Delivered a slideshow, not a movie
- **What went wrong:** Six clips, each from a *single* keyframe reference, gently animated for
  5 seconds with narration over them. Single-reference image-to-video is definitionally a
  moving still.
- **Fix (planned):** First-last-frame (FLF) generation — a start keyframe *and* an end
  keyframe, so the model renders the action *between* them. The capability already exists
  unused in `tools/vast/run_wan_i2v.py` (`WanFirstLastFrameToVideo` + `--endimage`).
- **Prevention:** A “movie” request requires shot grammar: every beat is multiple shots
  (wide/medium/close/insert) with a camera move. Single-reference I2V is banned for
  narrative work.

### C2. Executed the wrong style spec
- **What went wrong:** `story.md` §1 read “cel-shaded watercolor storybook”, so every
  keyframe and clip carried it — while the project's photoreal doctrine calls for
  “photorealistic cinematic still”. I rendered the wrong spec without challenging it.
- **Fix:** Rebuilt all six keyframes photoreal (photorealistic cinematic, 35mm, real skin,
  film grain; cartoon/watercolor/illustration in negatives).
- **Prevention:** A new story's style kit must match the photoreal doctrine (and be validated
  against researched external cinematic references — Diablo 2, WoW, StarCraft) — never
  against any self-made deliverable, none of which qualifies as a reference.

### C3. Shot the outline, not the coverage
- **What went wrong:** Six 5-second beats for 45s of narration. A real film is 40–60 shots,
  each with start+end keyframes.
- **Fix (planned):** Full shot-by-shot storyboard with start+end keyframe pairs, 40–60 shots.
- **Prevention:** Minimum shot density is a hard requirement, not a soft suggestion. Shot
  count is judged against the researched external cinematic standard (Diablo 2 / WoW /
  StarCraft), never against any self-made deliverable.

### C4. Cited Karsus as the working standard when it was the same failure
- **What went wrong:** Register entry C3 and the critique report called Karsus the project's
  working bar — "24 shots / ~2 minutes", "working photoreal 118 s film". That was false.
  Karsus was built by the same single-reference still-animation method: of its 25 segments,
  only `sp5a` set an `--endimage`; the other 24 had `end=None`, so each clip animated one
  still (`prev` chaining fed the previous clip's last frame as the next start still — still
  single-reference generation). It shipped at 16 fps, 480p upscaled to 720p, and the user
  had already rejected it as "terrible."
- **Fix:** Corrected both documents. Karsus is recorded as a failed deliverable, not a
  benchmark.
- **Prevention:** Never cite a rejected deliverable as evidence of correct method. See C5
  for the wider rule.

### C5. Cited any self-made deliverable (incl. Paladin) as a reference
- **What went wrong:** After the user rejected Karsus, I pivoted to citing the Paladin
  teaser as "the user-accepted reference" for style, format and quality. That was the same
  error one level shallower. The user's rule is absolute: **no self-made deliverable may be
  cited as a reference or benchmark at all** — including Paladin.
- **Fix:** Removed every self-deliverable citation from the register and the critique
  report. The only legitimate references are researched external cinematic sources
  (Diablo 2 / WoW / StarCraft, per the production doctrine) and the source material itself.
- **Prevention:** A reference is external by definition. Any sentence that treats one of
  our own outputs as a quality or style benchmark is wrong and must be flagged before it
  ships.

---

## Part D — GPU rental & billing discipline

### D1. Dual rental + watchdog self-stop wasted $1.60 for zero clips
- **What went wrong:** A misread first rental created an unintended A6000 while a second 4080S
  was also rented; dual billing plus a leaked self-stop watchdog produced nothing.
- **Fix:** Added duplicate-rental protection; fixed the watchdog; destroyed the unintended
  A6000 and a leaked instance.
- **Prevention:** One rental at a time; assert only one live instance before renting; watchdog
  must never self-stop without an explicit, logged trigger.

### D2. Watchdog self-stop killed a running render
- **What went wrong:** A leaked self-stop rule terminated the SkyReels-V2 render mid-run after
  ~$0.60 spend, leaving no mp4.
- **Fix:** Removed the self-stop; re-rendered clean.
- **Prevention:** Watchdog scope must exclude the active render process; a kill must require a
  separate explicit signal.

### D3. Left idle/stopped instances billing
- **What went wrong:** ~8h idle billing cost ~$3.14 on one run; an early run idled ~$0.60.
- **Fix:** Added `stop_instance.sh`; per-run rule: stop/destroy immediately after outputs are
  verified.
- **Prevention:** Every render script ends with an explicit stop/destroy, gated on verification.

### D4. Claimed a stopped instance was not billing (WRONG)
- **What went wrong:** After stopping instance 59145133 I told the user it was not costing
  anything. In fact Vast bills **disk storage** on a stopped (non-destroyed) instance —
  $0.2667/hr for 200 GB. Credit kept draining ~$0.07/hr until destroyed.
- **Fix:** Destroyed the instance after verifying all outputs were copied home and
  sha256-verified; confirmed instances=0 and volumes=0 and a stable credit reading.
- **Prevention (saved to memory):** Only DESTROY stops Vast billing. Teardown checklist:
  ffprobe-prove local copies → DELETE instances → confirm empty instances AND empty volumes
  (orphan volumes bill separately) → confirm credit stops moving.

### D5. Destroyed a warm box the user intended to keep
- **What went wrong:** After the user said “continue the pipeline,” I destroyed the warm
  instance (59201834), forcing a 49 GB weight re-download on the next run.
- **Fix:** Recognised the mistake; later used the persistent-volume/cached-weight approach.
- **Prevention:** Destroy is a billing decision: confirm with the user before destroying a
  warm cache, unless an explicit destroy instruction supersedes standing keep-alive.

---

## Part E — Render & assembly engineering

### E1. A regex matched the wrong flag, rendering the wrong clip spec
- **What went wrong:** A parameter bug substituted a 4s / 544×960 clip for an approved
  ~15.7s (377-frame) test — burning the cap without testing the intended case.
- **Fix:** Tightened the chunk-flag regex to match only the target flag.
- **Prevention:** A job builder must log *what it emitted* (duration, resolution, frame
  count, checkpoint, input list) and the run log must confirm what actually executed.

### E2. Copied a clip mid-write and destroyed the instance before verification
- **What went wrong:** The TI2V-5B test clip was fetched while still writing; the instance was
  destroyed before the corruption was discovered (~$1.088).
- **Fix:** Copy-then-ffprobe-before-delete discipline adopted.
- **Prevention:** Never copy a file while its render process is alive; verify every remote
  artifact locally before teardown.

### E3. Assembler defects corrupted/omitted segments
- **What went wrong:** `-shortest` truncated audio/video; an interleaved SP4 was regrouped;
  stale end-card targets pointed at the wrong file.
- **Fix:** Rewrote the assembler without `-shortest`, preserved SP4 ordering, fixed end-card
  targets.
- **Prevention:** Assemblies are verified end-to-end (segment count, per-segment duration,
  audio presence) and the end card is a resolved path, not a stale hardcoded target.

### E4. Wrong seed anchor rendered the wrong scene
- **What went wrong:** The Origami render used `seed.png` byte-identical to the Azulon hero
  keyframe rather than `seraph_ref.png`, producing footage unrelated to the seraph.
- **Fix:** Added a wrong-anchor hash gate; per-beat seed-describing prompts.
- **Prevention:** A seed-anchor hash gate runs before render; the seed file must match the
  beat's declared reference.

### E5. Render launched with a missing script (GPU billed while idle)
- **What went wrong:** The video render was launched, but the script wasn't on the box
  (`No such file or directory`); the GPU idled at $1.14/h.
- **Fix:** Uploaded the script and relaunched; verified the process and GPU load in the log.
- **Prevention:** Preflight asserts every script/input exists remotely, then confirm a live
  render process in the log before leaving it unattended.

### E6. `pkill -f` matched its own SSH command line
- **What went wrong:** Killing a TTS autorun with `pkill -f tts_pack_autorun` also matched the
  SSH command carrying that string, dropping my own session (rc=255).
- **Fix:** Killed explicit PIDs instead.
- **Prevention:** Terminate by PID; never `pkill -f` a pattern that can match your own shell.

### E7. HF xet download hang not anticipated
- **What went wrong:** OmniVoice model download hung on HuggingFace's xet backend, blocking
  the child process.
- **Fix:** `HF_HUB_DISABLE_XET=1` and relaunch; download completed.
- **Prevention:** For large HF pulls, disable xet pre-emptively on flaky connections.

---

## Part F — API keys & credit accounting

### F1. Misread OpenRouter key cap as available balance
- **What went wrong:** Reported “$250 remaining” when that was the key's *spending cap*, not
  money in the account. Actual balance was $0 (and −$0.016 at one point, below the $1 image
  gate).
- **Fix:** Queried `/credits` and reported the true balance.
- **Prevention:** For OpenRouter, always read the credits endpoint; a limit is not a balance.

### F2. Underestimated image-generation cost
- **What went wrong:** Estimated ~$0.13/call; the real KORY batch moved balance
  364.04 → 367.32.
- **Fix:** Reported the actual spend.
- **Prevention:** Estimate from the provider's real per-image price and a measured sample,
  not from memory.

### F3. Confused consumer subscriptions with API access
- **What went wrong:** Assumed a Gemini/Grok *subscription* implied usable API credits; both
  turned out to be separate billing products (Gemini API returned 402 depleted; xAI keys were
  empty placeholders).
- **Fix:** Verified each key's actual auth and balance endpoints.
- **Prevention:** Subscription ≠ API. Prove a key authenticates and has balance before
  promising a capability.

---

## Part G — Systemic root causes & standing preventions

1. **Numeric proof ≠ correctness.** Hash = integrity, score = one axis. Look at the output.
2. **Reference-set hygeine.** A conflicting reference silently outvotes the prompt.
3. **Zero-cost storyboard is mandatory before any rental.** Authoring is free; the render is
   the only paid step.
4. **Shot grammar is a requirement, not a preference.** FLF (start+end keyframes), multiple
   shots per beat, camera moves, 40–60 shots for a real film.
5. **Style kit must match the project's photoreal doctrine, validated against researched
   external cinematic references (Diablo 2 / WoW / StarCraft).** No self-made deliverable
   is ever a style reference.
6. **Billing truth:** only DESTROY stops Vast billing; stopped instances still bill disk.
7. **Verify live state from the provider**, never from notes or hashes: credit, instances,
   volumes, balance.
8. **Log what actually executed**, not what was intended (render params, emitted jobs, run
   logs).
9. **Copy-then-prove-before-delete** for every remote artifact.
10. **Estimate from measured/provider values, not memory.**

---

*Register compiled after the user's rejection of the Susanoo deliverable as a slideshow.
Supersedes any earlier framing that downplayed these failures.*
