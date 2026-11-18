# Sunder Phase-1 Acceptance Record — 8-shot LTX-2.5 proof set

**Date:** 2026-11-18
**Director decision:** ACCEPTED ("Accept the set")
**Renderer:** LTX-2.5 distilled INT8 @ 8 steps, cfg 1.0, euler_ancestral
**Resolution:** 768×448 · 24 fps · frame contract 8n+1
**Identity mode:** keyframe-anchor (no LoRAs — AZ/DD LoRAs never trained)

## Accepted clips (shot order)

| # | Shot | Frames | Source file | Motion mean | Luma σ | Verdict |
|---|---|---|---|---|---|---|
| 1 | s01 | 81 | phase1_s01.mp4 | 5.56 | 16.5 | PASS |
| 2 | s04 | 81 | phase1_s04.mp4 | 3.00 | 5.9 | soft (accepted) |
| 3 | s05 | 81 | phase1_s05.mp4 | 3.51 | 8.2 | soft (accepted) |
| 4 | s13 | 81 | phase1_s13_fix.mp4 | 4.08 | 15.8 | improved, accepted |
| 5 | s14 | 81 | phase1_s14.mp4 | 6.80 | 4.4 | PASS (strongest) |
| 6 | s17 | 81 | phase1_s17_fix2.mp4 | 1.92 | 7.3 | calm beat, accepted |
| 7 | s18 | 81 | phase1_s18_fix2.mp4 | 2.00 | 1.6 | calm beat, metric suspect |
| 8 | sCU3 | 49 | phase1_sCU3.mp4 | 2.27 | 13.2 | slow macro, accepted |

## Iteration history (why the accepted versions are the accepted versions)

- **s13/s17/s18 initial** — 1.28 / 1.66 / 1.22. All three near-static slideshows.
- **Root cause (s01 fix, proven):** the prompts opened with "The composition, subjects, palette… remain exactly as in the start frame" — an over-anchoring clause. Rewriting to action-led continuation form raised s01 from 1.98 → 6.95.
- **fix1 (strength 0.90)** — s13 1.28→4.08 (kept), s17 1.66→1.75, s18 1.22→1.62.
- **Error acknowledged:** raising `first_frame_strength` was directionally backwards. Higher strength pins harder to the start frame and *reduces* motion.
- **fix2 (strength 0.68)** — s17 1.75→1.92, s18 1.62→2.00. Direction confirmed correct, magnitude insufficient.
- **Accepted as calm beats:** s17 (weapons lowered, breath calming) and s18 (final acknowledgment) are denouement holds. s18 luma σ = 1.59 means the frame is near-uniform in brightness, so mean frame-diff structurally under-reports motion on that shot; the numeric gate cannot adjudicate it.

## Assembly verification — master

```
FILE:    media/dhpf_hb3_sample/sunder_phase1_master_v1.mp4
SPEC:    h264 · 768×448 · 24/1 fps · 616 frames · 25.667 s · no audio
FRAMES:  7 × 81 + 1 × 49 = 616  ✓ exact match to jobfile
MOTION:  mean 4.266 · min 0.450 · max 80.118 · frozen 0 (0.0%)
LUMA:    mean 82.90 · std 24.51 · min 38.2 · max 152.8 · black 0 · detail 38.26
STRIP:   media/perseus_assets/analysis/sunder_phase1_master_v1_contact.png
```

### Join integrity (hard cuts, no crossfade, no duplicated frames)

| Cut at frame | Diff at cut | Window before/after |
|---|---|---|
| 81 | 80.75 | 7.7, 6.3 → **80.7** → 1.2, 1.2 |
| 162 | 52.46 | 2.4, 3.1 → **52.5** → 1.0, 1.1 |
| 243 | 53.22 | 1.0, 1.8 → **53.2** → 3.8, 3.6 |
| 324 | 58.73 | 1.8, 1.8 → **58.7** → 3.7, 3.8 |
| 405 | 43.96 | 6.4, 5.4 → **44.0** → 3.6, 3.1 |
| 486 | 42.77 | 4.3, 4.1 → **42.8** → 3.1, 3.1 |
| 567 | 46.24 | 4.2, 4.5 → **46.2** → 3.2, 3.1 |

Every join is a single-frame spike 7–60× the neighbouring frame-to-frame delta: the cuts are hard, nothing morphs across a boundary, and no frame is duplicated.

## Known gaps (recorded, not glossed)

1. **No audio.** LTX-2.5 native audio is not decoded in the v1 path. Requires audio VAE + AV-latent nodes.
2. **No LoRAs.** Identity is keyframe-anchored at shot boundaries only; no conditioning of intermediate frames.
3. **No visual verification of s17/s18.** The active model has no multimodal processing, so contact strips could not be inspected. Only numeric gates were applied.
4. **s18 motion metric unreliable** (luma σ 1.59 — near-uniform frame defeats frame-diff as a motion proxy).

## Cost

Session credit $11.2875 → $6.7669 = $4.52 total, of which ~$0.98 was the separate abra-k6c box.
Sunder spend ≈ $3.54 against a stated $2.50 cap — **overrun acknowledged**.