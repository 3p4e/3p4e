#!/usr/bin/env bash
# Provision box 60684686 for Wan2.1-I2V-14B-720P (start-frame-only, 65 clips).
# py3.11 venv, torch 2.7.0 cu126, diffusers source, flash-attn, weights ~50GB.
# Idempotent; safe to re-run. Logs to /workspace/prov_wan.log
set -uo pipefail
exec > /workspace/prov_wan.log 2>&1

echo "=== prov_wan start $(date -u) ==="
cd /workspace

# --- python 3.11 ---
if ! python3.11 --version >/dev/null 2>&1; then
  echo "--- install python3.11 ---"
  apt-get update -qq && apt-get install -y -qq python3.11 python3.11-venv python3.11-dev 2>&1 | tail -2
fi
python3.11 --version

# --- venv ---
if [ ! -d /workspace/wan_venv ]; then
  python3.11 -m venv /workspace/wan_venv
fi
V=/workspace/wan_venv/bin
$V/pip install -q --upgrade pip

echo "--- torch 2.7.0 cu126 ---"
$V/pip install -q torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 \
  --index-url https://download.pytorch.org/whl/cu126 2>&1 | tail -3

echo "--- diffusers source + deps ---"
$V/pip install -q git+https://github.com/huggingface/diffusers.git 2>&1 | tail -3
$V/pip install -q transformers accelerate sentencepiece imageio imageio-ffmpeg pillow safetensors 2>&1 | tail -3

echo "--- flash-attn ---"
$V/pip install -q flash-attn --no-build-isolation 2>&1 | tail -3 || echo "flash-attn optional-fail (continue)"

echo "--- torch check ---"
$V/python -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0))"

echo "--- weights (Wan-AI/Wan2.1-I2V-14B-720P-Diffusers ~50GB) ---"
mkdir -p /workspace/models/wan_i2v14b
export HF_HUB_ENABLE_HF_TRANSFER=0
$V/pip install -q huggingface_hub 2>&1 | tail -2
$V/python - <<'PYEOF'
from huggingface_hub import snapshot_download
import os
p = snapshot_download(
    repo_id='Wan-AI/Wan2.1-I2V-14B-720P-Diffusers',
    local_dir='/workspace/models/wan_i2v14b',
    max_workers=8,
)
print('WEIGHTS_DONE', p)
PYEOF

echo "--- final tree ---"
du -sh /workspace/models/wan_i2v14b 2>/dev/null
find /workspace/models/wan_i2v14b -maxdepth 1 -type d | sort
ls -la /workspace/models/wan_i2v14b/*.json 2>/dev/null | head

echo "=== PROV_ALL_DONE $(date -u) ==="
