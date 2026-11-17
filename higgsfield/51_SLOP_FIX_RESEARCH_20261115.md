# 51 · SLOP FIX RESEARCH — problems → knowledge-bases → fixes (2026-11-15)

Live web search returned empty results at 21:10 CET (service gave no payloads on 3 tries) —
this report grounds in the project's saved research KB (higgsfield/research/*.txt, 2026 Higgsfield
blog + audits) + the measured HB autopsy (doc 50). Sources cited inline.

## The six problems (measured / confirmed)
| # | Problem | Evidence |
|---|---------|----------|
| P1 | REDREAM — clip starts on keyframe, scene replaced by final frame | drift-first→last drop >0.55 on 78% of measured clips (autopsy 50) |
| P2 | RANDOM_PEOPLE — 3-5 faces where keyframes carry ≤2 heroes | 53% of clips (YuNet@0.75) |
| P3 | PALETTE_FLIP — teal→warm hue rotation | 19% of clips (HSV-Bhatt 0.6-0.735) |
| P4 | Identity drift unmeasured — SFace refs failed to build; face-count proxy only | tooling gap (autopsy) |
| P5 | Weak anchor tier — K6 Lite 3B (2-step distill) cannot hold composition | drift pattern + why_generations_fail ('choice of model matters') |
| P6 | Verification gap — motion≠content; analyzer 255× scale bug; repo slop tool not run at proof | autopsy |

## What the knowledge bases say (local KB, verbatim anchors)
- why_generations_fail: 'visual errors: facial drift, broken physics, prompt misreads,
  frame-to-frame inconsistency and weak reference input. Clearer input reduces them,
  and the choice of model matters too.' → P1/P4/P5 are BOTH prompt and model.
- tools_consistent_characters: 'Text descriptions reduce drift but don't fix it.
  Identity anchors do.' 2026 tools: Soul ID (persistent identity from 20+ photos),
  Flux.2 LoRA, Seedance 2.0, Kling 3.0, Midjourney, Runway Gen-4.5.
- ltx2_prompting_guide: 'single flowing paragraph'; camera vocabulary 'slow dolly in',
  'handheld tracking', 'over-the-shoulder' improve consistency; avoid 'complex physics
  or chaotic motion'.
- ai_human_motion: weight loads before action and releases after; consistency must hold
  across every frame; identity still needs checking across generations.
- cinematic_generators: 2026 cinematic stacks ship up to 50 reference inputs per
  generation + synchronized dialogue/SFX/ambience + AI Cast/Elements for consistent
  characters, locations, props.
- soul_id_guide / persona_consistent_popcorn / consistent_characters_locations:
  identity persistence = trained identity, not text.

## Fixes (mapped)
F1 PROMPT (immediate, zero-GPU): strip the global anti-freeze tail; per-shot ONE motion
   verb + camera + endpoint (39/43 form); add hold-anchor: 'composition, subjects and
   palette hold; only the named action moves'; NEVER name concepts in negatives
   ('morphing, drift, new people…' — named embeddings fire anyway; our 53% RANDOM_PEOPLE
   is the proof). Max 3-4 hard negatives of the non-concept kind (watermark, text, logo).
F2 IDENTITY ANCHOR (project-level, the big one): KB consensus — text can't hold identity;
   anchors do. Our approved self-hosted route (SDXL+InstantID, family-privacy) extends to
   video as: per-hero IP-Adapter/InstantID face-lock at keyframe gen (already doing) +
   per-clip post-identity pass using our enrolled SFace centroids (faces/*.npy exist) to
   snap faces back to canon after render; for finals, train a per-hero LoRA from the
   enrolled card set (the Soul-ID pattern, self-hosted).
F3 MODEL TIER: Lite/2-step models for previs and motion blocking only; finals on K6 Pro
   29B or Wan-FLF (stronger anchor). The proof-tier must be the SAME model as the batch.
F4 VERIFICATION GATES (now hard law, tools/): per-clip before any batch approval:
   drift-drop ≤0.35 · faces ≤ kf_faces+1 · palette ≤0.5 · motion in 4-20 band (0-255
   scale) · sharpness-last ≥100. Proof must pass ALL five. Fix SFace ref build (dd/az
   cards → centroid) so identity-sim reports; add it as gate 6 (sim-last ≥0.30 vs hero
   centroid or a flagged manual review).
F5 CORPUS SWEEP: every story jobfile (tools/vast/jobs + jobfiles) gets the F1 treatment
   before its next render; the six problem classes become the audit checklist for the
   existing 44_VAST_P23_ERROR_LESSONS register.

## Specialized agent/tool landscape (2026, for reference when cloud spend is approved)
Soul ID · Flux.2 LoRA · Seedance 2.0 · Kling 3.0 · Runway Gen-4.5 · Higgsfield stack —
all cloud, all identity-anchor-first. Our self-hosted equivalents: InstantID/IP-Adapter
(image lock) + SFace centroid post-pass (video snap-back) + optional per-hero LoRA.
---

## LIVE WEB SEARCH RESULTS (2026-11-15 21:51 CET, via Playwright chromium)
The search_engine plugin returned empty payloads; per user approval, Playwright + chromium
were installed and live searches ran (chrome-headless-shell direct extraction). Key sources:

### Identity drift / consistency (validates F2 + the autopsy)
- DEV Community: 'Why Your AI Video Has Face Drift (And How to Fix It)' — drift is the #1
  failure class; fixed by reference anchoring, not text.
- Segmind: 'Smoother Consistency: Reduce Flickering and Identity Drift in AI-Generated Videos'.
- Higgsfield (live, matches our saved KB): 'AI Consistency: Character, Location & Cinematography'.
- Hedra Character-3; OpenArt: 'Identity Anchor' (consistent character across scenes).
- Reddit r/StableDiffusion: face-drift threads — community consensus: anchor > prompt.

### I2V scene drift / re-dream (validates F1 hold-anchor + REDREAM diagnosis)
- OpenCV.org: 'Image to Video in 2026: The Complete Guide'.
- Segmind: 'Structural Coherence' — start-frame fidelity techniques.
- Reddit: 'The scene just changes completely' — the exact REDREAM symptom we measured.
- dev.to: 'Wan 2.2 Hands-On: Prompting, Resolution, Scene-Swap'.

### Negative prompts (validates hard rule 1 — never name concepts in negatives)
- ModelScope / OpenArt / AI RTools negative-prompt guides.
- Reddit: 'negative prompts don't work' — named concepts leak through negation.
- Maxin.ai: 'Negative Prompts: The Untold Story'.

### Agentic video pipelines (the 'specialised agents' direction)
- arXiv: 'From Prompt to Preview: Agentic AI Video Generation' (study).
- arXiv: 'VideoAgent'; arXiv: 'A Survey of Agentic ...'.
- Medium: 'The Agentic AI Video Pipeline'.
→ industry direction = agent-directed generation with per-shot verification loops —
exactly the content-gate law (F4) we just hardened into doc 43.
