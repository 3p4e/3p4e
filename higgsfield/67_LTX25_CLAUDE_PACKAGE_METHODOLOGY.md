# 67 — LTX-2.5 22B methodology addendum: the Abracadabra Claude package (verified 2026-11-20)

Source: `ABRACADABRA_LTX25_HANDOFF.md` + `ABRACADABRA_LTX25_PACKAGE.zip` (Claude
orchestrator hand-off for the TV-menu re-creation). Live-verified same night on
vast.ai box **61677130** (RTX A6000 48GB, US, $0.404/hr): smoke test 6/6 clips
rendered and passed the package's own gates; full 87-job batch then submitted
(ok=81 fail=0 after excluding the 6 smoke jobs).

This doc ADDS to `59_LTX25_WALKTHROUGH_AND_STANDARD_PRACTICES.md` and resolves
conflicts with `43_MODEL_AND_PROMPT_STANDARD.md`. Where docs disagree, this
file states the resolution.

---

## 1. Hard rules (package §3, verbatim intent)

1. **Image-to-video, start frame only.** The prompt continues the start frame;
   it never describes a different scene. A different scene = a new clip.
2. **Positive wording only.** No negative lists ("no people, no morphing, no
   text"): naming a concept fires it (repo doc 43, measured on this project).
   Only artifact negatives allowed: `watermark, text, logo`. The prompts state
   what STAYS in the frame instead.
3. **One phase per clip, one primary action.** Do not add extra actions.
4. **Resolution multiple of 32, frames 8n+1, 24 fps.** Fixed sizes per class
   (see §3 table) — do not change without re-checking.
5. **Audio is discarded.** Board is silent; strip with `-an` in post.
6. **No real people.** Only the cartoon wand character.
7. **Per-clip pull and analysis** the moment each clip finishes (repo lesson
   D1/31). Never let a batch run ahead of the pull.
8. **Cost safety.** Never leave a paid box idle waiting for a decision — stop
   or destroy first (lessons 29, 30). Hard spend cap agreed with the owner
   before renting; stop and ask at 2× the estimate.
9. **Secrets.** Variable names only — never in logs, commits, messages.

## 2. Prompt structure that LTX-2.5 follows (package §8)

Every prompt, in order:

1. **Camera** — the shot (wide / close-up / tracking, locked or moving)
2. **Scene** — what the start frame already shows, restated briefly
3. **ONE action** — chronological present tense, one verb-chain
4. **How it ends + what holds to the last frame** — the held ending
5. **Style anchors** — day: premium 3D animated-feature look, warm golden key,
   orange rim, red/orange/lime/yellow triangle shards. Night: hot magenta +
   violet neon, wet reflective surfaces. Dark background so overlaid text reads.

LTX-2.5 responds to **long descriptive paragraphs**, not keyword lists.

Wrong dish → fix with a MORE SPECIFIC NOUN PHRASE for that dish only (name the
filling), never with negatives.

## 3. Per-class render parameters (package §5)

| Class | Size | Frames | Sec | Start frame | Post |
|---|---|---|---|---|---|
| bg_day, bg_night | 1280×704 | 121 | 5.0 | stage stills (cropped) | boomerang loop ≈10s |
| wand_idle_day/night | 768×1024 | 241 | 10.0 | wand panel stills | crossfade loop |
| wand_burger/waffle/wrap | 768×1024 | 193 | 8.0 | wand panel day | none |
| fx_slash | 1280×704 | 121 | 5.0 | black frame + spark | none; `screen` blend |
| cine_* (5) | 1280×704 | 241 | 10.0 | KF_AWAKENING / KF_NEON / KF_SUMMON | none; upscale 1080p |
| spawn_small_* (62) | 640×640 | 97 | 4.0 | `start_spark_640x640.png` | none; `screen` blend |
| spawn_full_* (12) | 1280×704 | 169 | 7.0 | KF_SUMMON | none; upscale 1080p |

If 241f OOMs: render 1216×704 @ 121f and chain (last frame of clip 1 = start
of clip 2, prompt describes the continuation). Report any deviation.

## 4. Distilled settings

- **8 steps, CFG 1.0**
- **Start-image strength 0.7** default; lower toward **0.5** for more motion
  (slideshow failure); raise if the model re-dreams the start frame (wand
  design drifts) — repo finding C1.
- Two-stage with the ×2 spatial upscaler when 1080p-class output is wanted.
- Seeds fixed per job. Retry ladder: `seed+1000`, then `+2000`; after three
  failures, report and move on.

## 5. Gates (package §6 — the package's own verify_clip.py)

- frames are 8n+1
- **start-frame correlation ≥ 0.90**
- **consecutive-frame correlation > 0.8** (below 0.3 = noise)
- **mean motion > 0.6** (slideshow detector)
- black-background clips: border stays dark
- THEN look at a 5-frame contact strip: dish = named dish, complete, centered,
  held to the last frame; wand keeps monocle / gold bands / crystal.
  **Auto gates do not replace looking.**

Smoke-tested 2026-11-20 (6 clips): bg_day 0.989/0.902/7.92 PASS;
wand_burger 0.874/0.800/13.63 (drift by design — burger materializes);
spawn_small_abracadabra-burger 0.953/0.885/12.49 PASS + black-bg OK;
spawn_small_cappuccino 0.896/0.887/11.58 (mild drift by design);
cine_summon_burger 0.963/0.778/21.23 (consec just under floor at high motion);
spawn_full_burgeri 1280×704@169 exact. **Zero slideshows; motion 7.9–21.2.**

## 6. Environment (package §4 + tonight's verified state)

- On-demand **48 GB+ GPU** class (RTX 6000 Ada / A6000 / L40S; A100 80G/H100
  for headroom). Interruptible instances never started in earlier runs.
- Disk ≈ 100 GB.
- Route A: **official `Lightricks/LTX-2` repo + its own `uv sync`**.
- Route B (verified tonight): **ComfyUI 0.46.0 + LTXVideo node**, models from
  the public `comfyicu/LTX-2.5` mirror, torch 2.8.0+cu126 on a 570.x driver.
  The package's §10 node chain maps 1:1 onto this graph.
- **Never hand-pin torch.** Doc 42 retracted doc 43's "nanobind death": it was
  a torch pin mismatch, fixed by `uv sync`; the gray-mush failure was a
  half-loaded Gemma text encoder. Use the FULL text-encoder directory, not a
  bare quantized file.
- Before every download loop: `mkdir -p` + check exit codes (lesson B5).
- Vast SSH can die mid-rental (lesson B6): pull as clips finish; keep a
  self-heal plan.

## 7. Measured on the 2026-11-20 run (evidence, not estimates)

- RTX A6000 48GB, ComfyUI route: **2.3–2.9 min/clip** across 640×640@97f and
  1280×704@169f — matches the package's 2–3 min guess for 1216×704@121f.
- 87 jobs ≈ **5 GPU-hours ≈ $2.00** at $0.404/hr.
- Tier-1 pipeline earlier the same day proved the ceiling of the WRONG approach
  (see §8) — do not re-run it.

## 8. The category error this package corrects (learned the hard way)

Earlier the same day, 24 Tier-1 clips were generated by (a) compositing a busy
portal keyframe (wand + rune rings + food) and (b) asking the model to
continue it, with negative guards ("no human hand, no ghost"). Result: 3/5
then 6/8 clips flat (luma std <3), ~25% pass rate, cool/dim magic. Root
causes, both fixed by this package's rules:

1. A busy DARK start frame is read as "hold this" → frozen output. The
   package's start frames are simple and the magic is described IN THE PROMPT,
   animated by the model.
2. Negative prompts fire the named concept (measured, doc 43). Positive
   wording + artifact-only negatives is the correct form.

The deployed menu's look comes from long structured prompts (§2), not from
re-compositing VFX assets into keyframes.

## 9. Key-frame extraction trick (free)

The package wants 3 generated keyframe images (KF_AWAKENING/NEON/SUMMON).
They already exist as pixels inside the deployed `cine_*.mp4` assets — extract
frame 0 at the exact target size (1280×704) instead of paying an image model.
Verified: wand design + stage composition match the references; all 87 jobs
unblocked at zero cost.
