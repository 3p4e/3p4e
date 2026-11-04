# Karsus's Folly — Project Rethink (PDP-first)

Date: 2026-11-02 · Grounded in live state, not recall.

## PDP doctrine

PDP = **Plan → Do → Prove**, enforced as hard gates. No action without a plan and a written success criterion + cost ceiling. No claim of "done" without proof: a checksum, probe, or measurement. No proceeding to the next step — and never spending again — until the prior proof is green.

Every systemic failure in this project was a broken gate:

| Failure | Broken gate |
|---|---|
| Dual rental + wrong instance destroyed | Acted on ambiguous API response without Prove |
| Watchdog self-stop (pkill sleep) | No Plan review of subshell semantics |
| Lost TI2V-5B clip (scp+DELETE chained) | Do without Prove (ffprobe) before destroy |
| TI2V-5B 25x slower | Plan did not price the missing distill LoRA as a blocker |
| HunyuanVideo trap | License not Proven before recommendation |
| gpu_ram unit error (MB vs GB) | Plan did not verify API units |
| Stale credit / branch mismatch | No Prove of live state before acting |
| Draft film shipped with v1 audio | No Prove (audio probe) at assemble time |
| Frozen tail (sp6c missing) | Destroyed mid-render, no Prove of clip count |

## Ground truth (proven 2026-11-02 23:36)

- Credit: **$8.838** · Instances: **0**
- Film: `media/out_v3/karsus_v3_FULL.mp4` — 118.000 s, 1280x720@24, sha256 `59bd5ec93796b24911d2495f4ac5b5f7b2903468a2c9a394f479abd061ea0911`, 65,137,042 bytes
- Clips: 24/25 (sp6c intentionally absent after the drop-patch)
- Stills: 12 · Audio stems: 5 · Canon docs: 18
- Likeness reference photos: **NONE** (face_dataset/faces absent; k_sp4 rear-shot; 14/16 frames no detectable face)
- Git: branch `claude/elegant-thompson-uqhred`, uncommitted modified/untracked pipeline files, 2 superseded drafts, `.bak` file
- TTS: 2 lines silent (K4 "Be unmade.", M4 "It is too much, Karsus."); voice slots 3/3
- Model: Wan 2.2 14B I2V, 4-step LightX2V distill, Apache-2.0, EU-safe

## The single decision

Stop oscillating. Name the objective: **complete v3 to "done", not re-render it.**

Three candidate goals:
- **A. Stabilise & ship as-is** — free, local.
- **B. Finish the known gaps** — sp6c (~$0.30), 2 TTS lines (free), likeness gate (needs photos). **← primary**
- **C. Re-render on a better model** — LTX-2.3/2.5, 48 GB GPU, full rebuild, ~$5-15 + days. Quality gain speculative (we never even saw TI2V-5B output).

C is parked until B is proven complete. The model is not the critical path.

## The real #1 risk: likeness, not the model

The film stars a real person (Blagoj). Canon requires likeness verification; current state is **UNVERIFIED** with no reference photos. This is a persona-integrity/consent issue, not cosmetics. It must be resolved before "complete" or "publishable" can be claimed.

Blocker: the real reference photos (gitignored by design). This is a human-input dependency.

## Cost envelope

- Spent to date: ~$3.05 (~$1.96 valid + ~$1.09 wasted on failed runs)
- Remaining: $8.838
- Finish envelope: **≤ $1.00** (sp6c + buffer). Anything beyond needs a written price + cap and explicit approval.

## Model upgrade — parked, verified facts on file

For AFTER v3 is done, if sharpness is still the complaint:
- **LTX-2.3 fp8** (ungated): Kijai ComfyUI port — `ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors` 25.23 GB + `text_encoders/ltx-2.3_text_projection_bf16.safetensors` 2.31 GB + `vae/LTX23_video_vae_bf16.safetensors` 1.45 GB. 8-step stage 1 + 4-step stage 2, CFG=1.
- GPU: Ada 48 GB (RTX 6000Ada $0.539/h, RTX 4090 48 GB $0.474-0.670/h). Test ONE clip, measure wall time, compare on OUR frames.
- **LTX-2.5**: still 403-gated (account `Azzulon` not in authorised list) — requires a manual access request; do not block on it.
- HunyuanVideo: EU/UK/ROK-excluded. Wan 2.5/2.6: no open weights. TI2V-5B: measured 25x slower.

## PDP phase plan (every phase ends in Prove + human gate)

- **Phase 0 — Freeze & Prove (free):** delete superseded drafts (`karsus_v3_final.mp4`, `karsus_v3_draft.mp4`), remove `.bak`/`__pycache__`, commit pipeline files, update `MANIFEST.txt` with final sha256 + "sp6c intentionally absent". **Gate:** human confirms commit.
- **Phase 1 — sp6c (≤$0.60 cap):** rent ONE Wan 14B host (the proven 80 s path), render sp6c natively, copy local + ffprobe + checksum BEFORE destroy, re-assemble, verify tail motion 41-43%. **Gate:** watch the ending.
- **Phase 2 — TTS (free):** place K4 + M4, re-mix, verify placement by loudness probe at target timestamps. **Gate:** human listens.
- **Phase 3 — Likeness (free, blocked on input):** obtain real reference photos; run SFace gate; report threshold vs canon 0.50. If photos are absent, label the deliverable explicitly "likeness unverified". **Gate:** HUMAN provides photos.
- **Phase 4 — Final:** single canonical file, checksum recorded, WotC fan-content notice intact.

## One-sentence doctrine

No spend without a written success criterion and cap; no claim of done without a checksum or measurement; no proceed without the prior proof being green.
