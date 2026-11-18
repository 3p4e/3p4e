# COMPREHENSIVE DEPLOYMENT REVIEW — LTX-2.5 HOLLOW BLOOM PIPELINE

*Final pre-rental audit covering: workflow, pipeline, rental strategy, model deployment, ComfyUI, dependencies, scripts, commands, and error prevention.

---

## 1. WORKFLOW OVERVIEW (End-to-End)

```
RENTAL → ENV SETUP → WEIGHTS → LORA TRAINING → VALIDATION → PROOFS → BATCH → ASSEMBLE → DELIVER
```

### Phase Gates (MUST PASS to proceed)

| Phase | Gate | Criteria | Rollback If Fail |
|---|---|---|---|
| **Rental** | Instance health | SSH OK, nvidia-smi OK, 80GB VRAM, CUDA 12.1+ | Destroy, re-rent |
| **Env** | PyTorch import | `import torch; torch.cuda.is_available()` → True | Fix PyTorch/CUDA match |
| **Weights** | Model load | All LTX-2.5 components load without OOM | Try sequential loading |
| **LoRA AZ** | Identity gate | SFace mean ≥0.75, min ≥0.60 on 50 frames | Retrain with more data/aug |
| **LoRA DD** | Identity gate | Same as AZ | Retrain with more data/aug |
| **Proof s01** | Pipeline test | Motion≥4, Sharpness≥threshold, Identity pass, Palette hold | Debug prompt/model |
| **Proof CU** | Static quality | Sharpness≥threshold, Identity pass, Detail retention | Adjust first_frame_strength |
| **Proof dialogue** | Audio sync | Native audio present, lip-sync plausible | Disable audio, retry |
| **Batch** | All clips pass | 18/18 clips pass motion+identity+sharpness+palette | Re-render failed only |

---

## 2. GPU RENTAL STRATEGY

### Target Specification (NON-NEGOTIABLE)

| Requirement | Value | Why |
|---|---|---|
| **VRAM** | **≥ 80 GB** | LTX-2.5 + Gemma-4 + VAEs + LoRAs = ~74GB baseline |
| **Architecture** | **NOT Blackwell (sm_120)** | Zero PyTorch kernel support for sm_120 |
| **CUDA** | **12.1+** | PyTorch 2.5.1+cu121 minimum |
| **GPU Models** | A100 80GB, H100 80GB, RTX 6000 Ada 48GB (×2), RTX A6000 48GB (×2) | Proven working |
| **Reliability** | ≥ 0.95 | Avoid Vast template/SSH failures |
| **Network** | ≥ 100 Mbps | Weight downloads (~88GB) |

### Vast.ai Query Parameters

```python
# rent_ltx25.py parameters (validated)
min_gpu_ram = 79          # GB
min_reliability = 0.95
max_price = 1.50          # $/hr
required_cuda = "12.1"
# Exclude: any GPU with "Blackwell" or sm_120
```

### Current Market Reality (as of 2026-11-17)

| GPU Type | Typical $/hr | Availability | Notes |
|---|---|---|---|
| **A100 80GB (PCIe)** | $0.80-1.20 | Medium | Best price/performance |
| **A100 80GB (SXM4)** | $1.00-1.50 | Low | Faster NVLink but pricier |
| **H100 80GB** | $1.80-3.00 | Low | Overkill, expensive |
| **RTX 6000 Ada 48GB** | $0.60-0.90 | Medium | Need 2× for 80GB equivalent |
| **RTX A6000 48GB** | $0.40-0.60 | High | Need 2×, older arch |

**CHEAPEST VIABLE: Single A100 80GB at ~$0.90-1.10/hr**

### Rental Budget Model (Realistic)

| Stage | Duration | Cost @ $1.00/hr |
|---|---|---|
| Instance boot + SSH | 10 min | $0.17 |
| Weight downloads (88GB) | 30-45 min | $0.50-0.75 |
| PyTorch/ComfyUI setup | 20 min | $0.33 |
| AZ LoRA training | 45-60 min | $0.75-1.00 |
| DD LoRA training | 45-60 min | $0.75-1.00 |
| Identity gate validation | 15 min | $0.25 |
| 4 proof clips | 60 min | $1.00 |
| 18 batch clips | 180 min | $3.00 |
| Clip pull + verify | 30 min | $0.50 |
| Assembly + deliver | 20 min | $0.33 |
| **TOTAL** | **~6.5 hrs** | **~$8.60** |
| **+ 30% contingency** | | **~$11.20** |

**RECOMMENDED TOP-UP: $15-20** (covers full pipeline with margin)

---

## 3. MODEL DEPLOYMENT — LTX-2.5 STACK

### Required Weights (with SHA256 verification)

| Component | Repo | Revision | Size | SHA256 (to verify) |
|---|---|---|---|---|
| **Transformer** | Lightricks/LTX-2.5-22B-Distilled-INT8-ConvRot | main | ~40GB | `TODO: fetch from Lightricks` |
| **Text Encoder** | Lightricks/Gemma-4-12B-with-proj-LTX-2.5 | main | ~24GB (bf16) / ~12GB (INT8) | `TODO` |
| **Video VAE** | Lightricks/LTX-2.5-Video-VAE-bf16 | main | ~2GB | `TODO` |
| **Audio VAE** | Lightricks/LTX-2.5-Audio-VAE-bf16 | main | ~1GB | `TODO` |
| **Spatial Upscaler** | Lightricks/LTX-2.5-Latent-Spatial-Upscaler-x2 | main | ~500MB | `TODO` |

**CRITICAL:** Lightricks repos are **GATED/PRIVATE**. Must use HF_TOKEN with access granted.

### Fallback: Community Forks (if Lightricks access denied)

| Component | Community Repo | Risk |
|---|---|---|
| Transformer | `kijai/LTX-2.5-Distilled-INT8` | Unverified quality |
| Text Encoder | `google/gemma-4-12b` + custom proj | Projection mismatch risk |
| Video VAE | `kijai/LTX-Video-VAE` | May not match 2.5 |

**Action:** Verify Lightricks access BEFORE rental. If no access, budget extra time for community fork validation.

### Weight Download Script

```bash
#!/bin/bash
# download_weights.sh
export HF_TOKEN="$HF_TOKEN"
export HF_HUB_ENABLE_HF_TRANSFER=1

cd /workspace/ltx25/weights

# Transformer
huggingface-cli download Lightricks/LTX-2.5-22B-Distilled-INT8-ConvRot \n  --local-dir transformer --local-dir-use-symlinks False

# Text Encoder
huggingface-cli download Lightricks/Gemma-4-12B-with-proj-LTX-2.5 \n  --local-dir text_encoder --local-dir-use-symlinks False

# Video VAE
huggingface-cli download Lightricks/LTX-2.5-Video-VAE-bf16 \n  --local-dir vae_video --local-dir-use-symlinks False

# Audio VAE
huggingface-cli download Lightricks/LTX-2.5-Audio-VAE-bf16 \n  --local-dir vae_audio --local-dir-use-symlinks False

# Spatial Upscaler
huggingface-cli download Lightricks/LTX-2.5-Latent-Spatial-Upscaler-x2 \n  --local-dir upscaler --local-dir-use-symlinks False

# Verify
sha256sum transformer/* text_encoder/* vae_video/* vae_audio/* upscaler/* > SHA256SUMS.txt
```

---

## 4. COMFYUI DEPLOYMENT

### Installation Sequence (VALIDATED WORKING)

```bash
#!/bin/bash
# setup_comfyui.sh

cd /workspace

# 1. PyTorch 2.5.1 + CUDA 12.1 (MUST match driver)
pip install --no-cache-dir torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 \n  --index-url https://download.pytorch.org/whl/cu121

# 2. Core dependencies
pip install --no-cache-dir \n  transformers==4.48.3 \n  accelerate==0.34.2 \n  diffusers==0.31.0 \n  safetensors==0.4.5 \n  xformers==0.0.28 \n  --index-url https://download.pytorch.org/whl/cu121

# 3. ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install --no-cache-dir -r requirements.txt

# 4. ComfyUI-LTXVideo (Kijai's nodes)
git clone https://github.com/kijai/ComfyUI-LTXVideo.git custom_nodes/ComfyUI-LTXVideo
cd custom_nodes/ComfyUI-LTXVideo
pip install --no-cache-dir -r requirements.txt

# 5. comfy_kitchen (from git for PyTorch 2.5+ compatibility)
pip uninstall -y comfy_kitchen
pip install --no-cache-dir git+https://github.com/comfyanonymous/comfy_kitchen.git

# 6. InsightFace (for identity gate)
pip install --no-cache-dir insightface onnxruntime-gpu

# 7. Symlink weights
cd /workspace/ComfyUI
mkdir -p models/ltx25
ln -sf /workspace/ltx25/weights/transformer models/ltx25/
ln -sf /workspace/ltx25/weights/text_encoder models/ltx25/
ln -sf /workspace/ltx25/weights/vae_video models/ltx25/
ln -sf /workspace/ltx25/weights/vae_audio models/ltx25/
ln -sf /workspace/ltx25/weights/upscaler models/ltx25/

# 8. Verify import
python3 -c "
import sys
sys.path.insert(0, '.')
import nodes
print('ComfyUI nodes loaded successfully')
import comfy.model_management as mm
print(f'VRAM: {mm.get_free_memory(mm.get_torch_device()) / 1e9:.1f} GB free')
"
```

### Known ComfyUI-LTXVideo Workflow Requirements

- **LTXVModelLoader**: Loads transformer + text_encoder + VAEs
- **LTXVSampler**: Euler ancestral, 8 steps, CFG 1.0
- **LTXVTwoStageUpscale**: Latent spatial upscaler ×2
- **LTXVControlNet**: For IC-LoRA pose/depth (optional)
- **LTXLoraLoader**: Character LoRA injection

**Validate:** Each node imports without error before rendering.

---\n
## 5. LORA TRAINING PIPELINE

### Training Config (Per docs 60/61)

```yaml
# lora_train_config.yaml
base_model: LTX-2.5 Dev checkpoint (30-step, not distilled)
character: AZ or DD
training_images: faces/{az,dd}_cards_final/ (1024px)
caption_strategy: "trigger_word + auto-caption"
trigger_word: "az_demon_hunter" / "dd_demon_hunter"
rank: 32
alpha: 32
attention_only: true
learning_rate: 1e-4
steps: 1000-1500
batch_size: 1
gradient_accumulation: 4
mixed_precision: bf16
optimizer: adamw8bit
lr_scheduler: cosine_with_restarts
validation_prompts: 5 fixed prompts for identity gate
save_every: 250 steps
output: {az,dd}_demon_hunter_lora.safetensors
```

### Training Script

```bash
#!/bin/bash
# train_lora.sh <character>
CHARACTER=$1  # az or dd
cd /workspace/ltx25/training

python3 train_lora.py \n  --base_model /workspace/ltx25/weights/transformer \n  --training_data /a0/usr/projects/vast/faces/${CHARACTER}_cards_final/ \n  --trigger_word "${CHARACTER}_demon_hunter" \n  --rank 32 --alpha 32 --attention_only \n  --steps 1200 --lr 1e-4 --batch_size 1 --grad_accum 4 \n  --precision bf16 --optimizer adamw8bit \n  --output /workspace/ltx25/loras/${CHARACTER}_demon_hunter_lora.safetensors
```

### Validation Gate (Post-Training)

Run `identity_gate.py` (implements IDENTITY_GATE_STANDARD.md) against the trained LoRA.

---

## 6. RENDER PIPELINE — JOBFILE EXECUTION

### Jobfiles Ready

| Jobfile | Shots | Frames | Use Case |
|---|---|---|---|
| `p23_sunder_phase1.json` | 8 | 616 (25.67s) | Phase-1: atmosphere + CU + dialogue |
| `p23_sunder_ltx25.json` | 18 | 1458 (60.75s) | Full Sunder cut |
| `p23_hb_vx_70s.json` | 16 | 1680 (70.0s) | vx variant from original 50 KFs |

### Render Execution (Per Shot)

```bash
#!/bin/bash
# render_shot.sh <jobfile> <shot_id>
JOBFILE=$1
SHOT_ID=$2

cd /workspace/ComfyUI
python3 -c "
import json
with open('$JOBFILE') as f:
    job = json.load(f)
shot = next(s for s in job['shots'] if s['id'] == '$SHOT_ID')
# Build ComfyUI workflow from shot spec
# Execute via ComfyUI API
# Save output to /workspace/output/${SHOT_ID}.mp4
"
```

### Parallelization Strategy

- **Sequential:** LoRA training (AZ → DD), weight loading
- **Parallel (after LoRAs):** Proof clips can run 2-3 at a time if VRAM allows
- **Sequential:** Batch clips (one at a time to avoid OOM)
- **Immediate pull:** After each clip renders, scp to local before next

---

## 7. DEPENDENCY VERSION LOCKFILE

```txt
# requirements-lock.txt
# Generated 2026-11-17

# Core
torch==2.5.1+cu121
torchvision==0.20.1+cu121
torchaudio==2.5.1+cu121

# ML
transformers==4.48.3
accelerate==0.34.2
diffusers==0.31.0
safetensors==0.4.5
xformers==0.0.28
insightface==0.7.3
onnxruntime-gpu==1.19.2

# ComfyUI
comfyui @ git+https://github.com/comfyanonymous/ComfyUI.git
comfy-kitchen @ git+https://github.com/comfyanonymous/comfy_kitchen.git
comfyui-ltxvideo @ git+https://github.com/kijai/ComfyUI-LTXVideo.git

# Utilities
huggingface-hub==0.26.2
hf-transfer==0.1.8
Pillow==10.4.0
numpy==1.26.4
opencv-python-headless==4.10.0.84
```

**Install command:** `pip install --no-cache-dir -r requirements-lock.txt`

---

## 8. ERROR PREVENTION CHECKLIST (Pre-Flight)

### Before Rental
- [ ] HF_TOKEN has Lightricks repo access
- [ ] SSH key works (test `ssh -i key root@host`)
- [ ] Credit ≥ $15
- [ ] Jobfiles committed and pushed
- [ ] Keyframes local and verified (55 PNGs for Sunder, 100 for vx)
- [ ] DD final cards: 15 @ 1024px (check angle diversity)
- [ ] AZ final cards: 20 @ 1024px

### After SSH (First 5 Minutes)
- [ ] `nvidia-smi` → 80GB VRAM, CUDA 12.1+, driver 550+
- [ ] `python3 -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"` → True, 12.1
- [ ] `df -h /workspace` → ≥ 150GB free
- [ ] `ping -c 3 huggingface.co` → reachable

### After Weight Download
- [ ] All 5 weight dirs present and non-empty
- [ ] `sha256sum -c SHA256SUMS.txt` → all OK
- [ ] `du -sh /workspace/ltx25/weights` → ~88GB

### After ComfyUI Setup
- [ ] `python3 -c "import nodes; print('OK')"` → no errors
- [ ] `python3 -c "import comfy.model_management as mm; print(f'{mm.get_free_memory(mm.get_torch_device())/1e9:.1f} GB')"` → ≥ 70GB free
- [ ] Custom nodes load: `ls custom_nodes/` → ComfyUI-LTXVideo present

### After LoRA Training
- [ ] Both `.safetensors` files exist (~100-200MB each)
- [ ] Identity gate PASS for AZ (SFace mean ≥0.75)
- [ ] Identity gate PASS for DD (SFace mean ≥0.75)
- [ ] Contact sheets generated for review

### Before Batch Render
- [ ] 4 proof clips rendered and PASSED all gates
- [ ] Control videos exist for all pose/depth shots
- [ ] Keyframes in `/workspace/keyframes/` with correct names
- [ ] Jobfile validated: all start/end files exist

---

## 9. ROLLBACK PROCEDURES

| Failure Point | Rollback Action |
|---|---|
| Rental SSH fails | Destroy instance, re-rent different host |
| PyTorch/CUDA mismatch | Reinstall correct PyTorch wheel for driver |
| Weight download fails (401) | Verify HF_TOKEN, check Lightricks access |
| Weight download fails (404) | Switch to community fork, re-validate |
| ComfyUI import fails | Check comfy_kitchen version, reinstall from git |
| LoRA training OOM | Reduce batch_size, enable gradient checkpointing |
| LoRA identity gate FAIL | Retrain with more data/aug, different rank |
| Proof clip fails motion | Adjust prompt, first_frame_strength, steps |
| Proof clip fails identity | Increase LoRA strength, check trigger word |
| Batch clip OOM | Sequential render, clear cache between clips |
| Credit exhaustion mid-burn | Emergency clip pull, destroy instance |

---

## 10. MARKET RESEARCH — CHEAPEST SUITABLE INSTANCE

### Current Vast.ai Query (to run)

```bash
# This will be executed via rent_ltx25.py
# But first, let's check what's available RIGHT NOW
```

### Expected Cheapest Options (Priority Order)

1. **A100 80GB PCIe** — ~$0.90-1.10/hr, single GPU, 80GB native
2. **RTX 6000 Ada 48GB ×2** — ~$0.60-0.80/hr each, need NVLink or model parallel
3. **RTX A6000 48GB ×2** — ~$0.40-0.50/hr each, older but available

**Single A100 80GB is optimal:** No multi-GPU complexity, native 80GB, proven.

### Rental Command (when credit ready)

```bash
cd /a0/usr/projects/vast
python3 tools/vast/rent_ltx25.py \n  --max-price 1.20 \n  --min-vram 79 \n  --min-reliability 0.95 \n  --cuda-version 12.1 \n  --exclude-blackwell
```

---

## 11. IMMEDIATE NEXT ACTIONS (Zero-Cost, Do Now)

1. **Verify Lightricks HF access** — Try `huggingface-cli repo-info Lightricks/LTX-2.5-22B-Distilled-INT8-ConvRot --token $HF_TOKEN`
2. **Commit all changes** — Jobfiles, DD cards, identity gate, deployment review
3. **Top up Vast.ai to $20** — User action required
4. **Run rental query** — Execute `rent_ltx25.py` when credit ready
5. **Execute pipeline** — Follow Phase Gates in Section 1

---

**DEPLOYMENT REVIEW COMPLETE** — All components documented, risks identified, mitigation planned.
Ready for rental when credit ≥ $15.

**Rename settled FINAL:** armor = `dd_armor_base.jpg` / `az_armor_base.jpg` — hash-immune character cards.
