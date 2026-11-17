# 60 — LTX-2.5 Character LoRA Training Standard (DD)
# Source: Grok deep research, 2026-11-16. Trainer: official open-source LTX Trainer (Lightricks/LTX-2 monorepo).

## Key requirements
| Item | Value |
|---|---|
| Trainable base | ltx-2.5-22b-dev-transformer-bf16.safetensors (DEV ONLY) |
| Text encoder | LTX fine-tuned Gemma 4 (gemma4-12b-with-proj-ltx-2.5-...). Vanilla Google Gemma 4 FAILS. |
| OS | Linux (Triton) |
| VRAM | 80GB recommended; 48GB comfortable; 32GB w/ t2v_lora_low_vram.yaml |
| License | LTX-2.x Community (<$10M) — same as inference |

## DD dataset
- 20-30+ high-quality images/short clips: multi-angle, expressions, lighting, armor + floating teal-blue hair views.
- Metadata JSON/JSONL/CSV pairing media + caption. Unique trigger token: `dd_demon_hunter`.
- Buckets: w/h ÷32; frame count (F-1)%8==0 (49/81/121). Mix stills + clips OK.

## Starting config (official default)
```yaml
lora:
  rank: 32            # start here; 64 if weak; rarely 128
  alpha: 32           # ALWAYS = rank (effective scaling 1.0)
  dropout: 0.0        # official default; 0.05 only if overfit + can't step back
  target_modules: ["to_k","to_q","to_v","to_out.0"]   # attention ONLY; do NOT touch MLPs
steps: 1000-2000 (up to 3000 if weak)
lr: 1e-4 to 1.5e-4 cosine
batch: 1 (grad accum as needed)
validation: every 100-250 steps, video_dims [960,544,49], seed 42
checkpoints: interval 250, keep_last_n -1 (keep ALL)
```

## Rank decision tree
Start rank 32 → validate → identity weak? → rank 64 → still weak? → 128 + check captions/data. Identity good but scenes rigid? → step back a checkpoint (NOT higher rank).

## Why these target modules
to_k/q/v/out.0 = attention projections → strongest influence on identity/appearance/style; leaves MLPs untouched → preserves motion + temporal coherence (critical for combat). Expanding to MLPs risks quality faster than it helps identity. Audio modules: leave alone.

## Workflow
1. Prepare dataset.json (captions + trigger)
2. Preprocess: `uv run python scripts/process_dataset.py dataset.json --resolution-buckets "960x544x49;1280x704x81" --model-path <dev ckpt> --text-encoder-path <gemma4> --lora-trigger dd_demon_hunter`
3. Configure from configs/t2v_lora.yaml (or low_vram variant)
4. Train: `uv run python scripts/train.py configs/dd_lora.yaml`
5. Select checkpoint (see doc 61) → `lora_weights_step_XXXXX.safetensors`

## Inference
Load via LoraLoaderModelOnly, strength 0.8-1.2. Works on Distilled AND Dev paths. Combine with first-frame I2V for strongest lock. Keep trigger out of prompts unless forcing the character.

---

## GENERALIZATION — this standard applies to ANY character / face card, not just DD

The recipe above is written for DD, but every rule is **character-agnostic**. For any new hero,
villain, or recurring character, parameterize only these — the config, workflow, gates, and
validation protocol do NOT change:

| Slot | DD example | Any character |
|---|---|---|
| `<CHAR>` name | dd_demon_hunter | short lowercase snake token, e.g. `az_paladin`, `perseus_hero`, `fenrir_wolf` |
| `<CHAR>` trigger | `dd_demon_hunter` | the same token; keep it unique, never a real word |
| Dataset source | `faces/dd_cards_final/` + DD originals | that character's `faces/<name>_cards_final/` + originals (enrolled, identity-locked) |
| Distinctive features | floating teal-blue hair, frost-arcane armor | the 2-4 features that define the character — prioritize these in captions |
| Armor/weapon views | included | include if they must stay locked across shots |

**Universal steps (unchanged for every character):**
1. Confirm the character's face cards / originals are enrolled + identity-locked (SFace centroid in `faces/identity_index.json`).
2. Build the dataset: 20-30+ multi-angle images/clips, captions + `<CHAR>` trigger, ÷32 buckets, (F-1)%8==0 frames.
3. Train on the **ltx-2.5-22b-dev** transformer with **Gemma-4-LTX** encoder — never vanilla Gemma.
4. Config exactly: `rank 32 / alpha 32 / dropout 0.0 / target [to_k,to_q,to_v,to_out.0]`; 1000-2000 steps, lr 1e-4.
5. Validate per doc 61 (two samples, keep all checkpoints, pick latest-holds-identity).
6. Deploy: `LoraLoaderModelOnly` strength 0.8-1.2 on Distilled or Dev + first-frame I2V + IC-LoRA control.

**Multi-character films (e.g. DD + AZ in the same shot):**
- Train **one LoRA per character** (do NOT combine two identities into one adapter — it blends them).
- Load each via its own `LoraLoaderModelOnly`; keep the **total stack under ~2.0** combined strength.
- If VRAM won't fit two full LoRAs on the 48GB path, use the 80GB box or run two passes with a shared scene plate.

**Face-card → LoRA handoff rule:** a character is ready to train when it has (a) enrolled face cards,
(b) an SFace centroid in `identity_index.json`, and (c) 20-30 usable multi-angle assets. No card, no LoRA.


---

## Training Order (Sunder 60s cut)

Train **AZ first**, then **DD**. Both LoRAs must pass identity validation before batch rendering.
- **AZ LoRA**: source from `faces/az_cards_final/`, reference `az_armor_base.jpg`
- **DD LoRA**: source from `faces/dd_cards_final/`, reference `dd_armor_base.jpg`
- Validate each with 3 seed renders against enrolled face cards before proceeding
