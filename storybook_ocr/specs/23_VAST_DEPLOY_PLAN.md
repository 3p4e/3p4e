# #23 Perseus & Medusa — VAST DEPLOY PLAN (market search -> rental -> proof)
> Credit verified: $11.14. No instances running.
> Money rules (KB §10): named offer, stated rate, hard cap BEFORE the API call.
> This plan is prep; no spend until director GO.
> RENDER STACK: LTX-2.3 22B distilled — the PROVEN route (corrected note 42,
> spec 38 PROVEN 2026-11-10, director-rated top-tier on DHPF proofs).

## Render stack — INCLUDE (LTX-2.3 22B distilled, official pipeline)
| Component | Detail | Size |
|-----------|--------|------|
| Repo | github.com/Lightricks/LTX-2 cloned; install via `uv sync` or `pip install -e packages/ltx-core -e packages/ltx-pipelines` | — |
| Runtime | uv sync pins matching torch/transformers — NEVER hand-pin torch (the nanobind refcount crash was a torch-pin mismatch) | — |
| Diffusion | ltx-2.3-22b-distilled-1.1.safetensors | ~46GB |
| Text enc  | FULL gemma-3-12b-it HF dir (config + tokenizer + processor + weights) — MANDATORY; a bare fp8 half-loads -> empty conditioning -> grey-mush free-run | ~24GB |
| LoRA      | ltx-2.3-22b-distilled-lora-384-1.1.safetensors at strength 0.5 | ~7.6GB |
| Upsampler | ltx-2.3-spatial-upscaler-x2-1.1.safetensors | ~1GB |
| Total weights | | ~79GB |

### Recipe (proven, spec 38 §0)
```
python -m ltx_pipelines.distilled 
  --distilled-checkpoint-path ltx-2.3-22b-distilled-1.1.safetensors 
  --gemma-root <FULL gemma-3-12b-it dir> 
  --prompt "<verb-first, motion-only, ONE flowing paragraph>" 
  --output-path out.mp4 
  --image kf_NN_start.png 0 0.7 
  --height 704 --width 1216 --num-frames 121 --frame-rate 24 --seed NN 
  --lora ltx-2.3-22b-distilled-lora-384-1.1.safetensors 0.5 
  --spatial-upsampler-path ltx-2.3-spatial-upscaler-x2-1.1.safetensors
```
8 steps, CFG 1 (distilled card), 1216x704 (both multiples of 32), 121 frames (8k+1) @ 24fps, ~5.0s/clip, START-image strength 0.7 (0.9 tested = negligible). ~44GB bf16 fits a 48GB card directly, ~2-3 min/clip, no offload. Native audio in.

### Per-shot model assignment (spec 38 §5 + finding 4)
| Shot class | Model | Why |
|------------|-------|-----|
| HERO closeups (face >=200px, S19 S24 S39 S45 S48 S51 S58 + narrator CUs) | ltx-2.3-22b-dev, 30-step | 8-step distilled loses 60-98% high-frequency detail after f000; hair/face dies first |
| Action / wides / creature (S20-S23, S25-S27, S33-S35, S42, S49-S55) | distilled-1.1, 8-step | violent-action drift is a feature; speed |
| Everything else (medium dialogue, travel) | distilled-1.1 | default |
Dev clips run at 30 steps CFG 3.0 euler/dpmpp_2m (spec 38 §1 sampling table).

## EXCLUDE (do not deploy)
| Excluded | Why |
|----------|-----|
| ComfyUI-LTXVideo nodes for LTX-2.3 | BANNED (spec 38): immature — wrong TE class / missing tokenizer / variant crashes. Official pipeline ONLY |
| ComfyUI + Wan-FLF graph | superseded by LTX23 for #23 (Wan path documented but not the chosen model) |
| Qwen-Image-Edit-2511 | keyframes are director-made in Grok; no on-box keyframe gen needed |
| SkyReels / Higgsfield stack | superseded |
| LTX-2.3 fp8 bare Gemma | the grey-mush bug: half-loaded TE = empty conditioning = free-run. FULL gemma dir only |
| Hand-pinned torch 2.7.x/2.8.x | nanobind refcount crash; uv sync resolves it |
| Vast templates with autorun watchdogs | reap tenant processes / wipe /workspace — plain pytorch template only |
| MiniMax H3 | documented fallback only |

## Disk / GPU requirement
- Weights ~79GB + repo + deps -> rent disk >= 120GB (prev box used ~88GB incl caches).
- 48GB+ VRAM: RTX 6000-class / A6000 48GB / A100 80GB / H100. bf16 44GB fits 48GB directly.
- Download time (~79GB) counts INSIDE the paid window — prefer >= 500Mbps inet_down.

## Cost model
| Item | Estimate |
|------|----------|
| Proof scene S53-S55 (3 clips + gates) on A100 @ $0.940/h | dl ~1.5h + render ~0.5h + gates ~= $2-5 |
| Full film 60 clips (mixed distilled ~2-3min + dev-30step ~10min on hero CUs) | ~$25-45 at A100 rates — EXCEEDS current $11.14 credit |
| Recommendation | proof first on the $11.14; top-up before any full-batch GO |

## Market search (dry, zero-cost API) — RUN 2026-11-14
Filters: verified, rentable, 1 GPU, gpu_ram>=48GB, disk>=120GB, reliability>=0.97,
inet_down>=500Mbps, non-CN, price asc.
Result: 16 good offers. Cheapest qualified:
  id=47195595 A100 PCIE 80GB $0.940/h disk 507GB down=697Mbps rel=0.992 Oklahoma US
  est proof window (2h dl + 3h render buffer) <= $4.70 vs credit $11.14
Alternatives: 60484178 A100 SXM4 80GB $0.989/h AE | 36602054 A100 SXM4 $1.056/h CZ
Re-run at GO time: offers churn.

## GO checklist (all boxes before the rent call)
[ ] Proof prompts S53/S54/S55 (motion-continuation, LTX form) staged in jobfiles
[ ] 3 start frames staged: media/perseus_assets/keyframes/kf_5{3,4,5}_start.png
[ ] Market search re-run at GO time; ONE named offer + hourly rate recorded
[ ] Hard cap agreed: $ ___ (proof)
[ ] Projected overage check vs $11.14 balance
[ ] Supervision plan: incremental fetch as clips land; copy->checksum->KEEP ALIVE for corrections (director order)
[ ] S54 replacement verified (final canon image re-sent and locked)
