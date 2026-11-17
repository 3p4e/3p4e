# 50 · HOLLOW BLOOM SLOP AUTOPSY — 2026-11-15

Status: VERDICT DELIVERED. Root causes confirmed with measurements.
Tool: `tools/analyze_hb_slop.py` (YuNet + SFace + drift/palette metrics, per clip vs its start keyframe).

## The failure (user verdict: correct)
The shipped film (`hollow_bloom_DUAL.mkv`) is content-slop even though it passes motion
metrics: nearly every clip STARTS on its keyframe and RE-DREAMS the scene by the final
frame; random extra people appear; palette flips; items/identity morph.

## Measured census (corrected thresholds; s01–s32 representative, s33–s48 same pattern)
- REDREAM (drift-first minus drift-last > 0.55): **25/32 (78%)** — e.g. s29 0.862→0.05,
  s30 0.78→−0.093, s36 0.943→0.049. Even the APPROVED PROOF s04: 0.783→0.166.
- RANDOM_PEOPLE (YuNet face_max ≥ 3 at 0.75): **17/32 (53%)** — face_max 3–5 in shots
  whose keyframes carry ≤2 heroes.
- PALETTE_FLIP (HSV-Bhattacharyya > 0.6): **6/32 (19%)**.
- Clean: 5/32 (the slow establishing s01–s03 hold best: last-drift 0.62–0.68).
- First (uncalibrated) run also showed sharpness decay into the last frames (~73%
  detail loss by f060) — consistent with Lite-tier VAE, secondary issue.

## Root causes (our side — confirmed)
1. **The anti-freeze tail I appended during the motion-strengthening pass.** Every c2
   prompt ends with the IDENTICAL block:
   "The movement stays strong and continuous through the final frame — bodies in
   visible motion, nothing settles into a held pose. … Negative: duplicate face,
   extra limbs, extra fingers, text, watermark, logo, cartoon, anime, new people,
   bystanders, morphing, drift."
   Three defects in one block:
   - 'nothing settles into a held pose' = a GLOBAL instruction to keep changing pixels
     → directly fights the start-frame anchor → scene replacement (REDREAM).
   - Naming forbidden concepts ('morphing, drift, new people, duplicate face') in a
     NEGATIVE list still fires their embeddings — T2V/I2V models generate named
     concepts despite negation. This is what seeds RANDOM_PEOPLE.
   - A generic global tail applied to all 116 prompts contradicts the per-shot
     continuation form the Perseus standard (39/43) prescribes.
2. **Weak anchor model.** K6 Lite 3B (2-step distill) cannot hold composition under
   strong-motion prompting. Same prompt form on K6 Pro 29B / Wan-FLF would drift less
   — but the prompt is the trigger we control, so the fix is mandatory regardless of
   the model tier chosen for the re-render.
3. **Verification gap (process failure).** The batch was approved and shipped on
   motion/sharpness/palette numbers only. The repo ALREADY contained
   `tools/analyze_23_slop.py` (drift-vs-keyframe + face census) — the exact detector
   for this failure. It was not run at proof time; my own first analyzer run had a
   255× motion-scale bug that buried the signal under false SLIDESHOW flags.

## The fix (mandatory before any re-render)
1. **Strip the global tail.** Per-shot prompts = ONE specific motion verb-phrase +
   camera + endpoint (the 39/43 continuation form). No 'through the final frame'
   clause. No negative laundry-lists — at most 3–4 hard negatives that are NOT
   concepts (use 'bystanders' never; prefer frame-count and identity anchors).
2. **Add a hold-anchor instead**: 'the composition, subjects, and palette hold;
   only the named action moves' — tells the model WHAT NOT TO TOUCH.
3. **Per-clip content gates BEFORE batch approval** (now in tools/): drift-first→last
   drop ≤ 0.35, face_max ≤ keyframe faces + 1, palette ≤ 0.5, motion in the 4–20
   band. Proof clip must pass ALL before the batch fires.
4. Re-render candidate: K6 Pro 29B (stronger anchor) or Wan-FLF with the corrected
   prompts; supervised proof first, per the standing proof-gate law.

## Reference
Slop report: media/dhpf_hb_clips/analysis/hb_slop_report.json
Analyzer: tools/analyze_hb_slop.py (fixed thresholds: motion <0.01 on 0–1 scale,
face score 0.75, REDREAM = drift-drop > 0.55, PALETTE > 0.6)