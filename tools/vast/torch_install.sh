#!/bin/bash
# Install CUDA torch on a bare box. This image ships WITHOUT torch,
# which is what wedged ComfyUI's requirements.txt for an hour.
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/torch.log
say(){ echo "[TORCH $(date -u +%H:%M:%S)] $*"; }

say "start; torch absent check"
python3 -c "import torch" 2>/dev/null && { say "torch ALREADY present"; exit 0; }

say "installing cu124 torch (~2.5 GB)"
START=$(date +%s)
python3 -m pip install --no-input --break-system-packages --progress-bar off \
  --index-url https://download.pytorch.org/whl/cu124 \
  torch torchvision torchaudio > /workspace/torch_pip.log 2>&1
RC=$?
END=$(date +%s)
say "pip exit=$RC elapsed=$((END-START))s"

say "verify"
python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),'dev',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')" > /workspace/torch_verify.log 2>&1
say "verify exit=$?"
cat /workspace/torch_verify.log >> /workspace/torch.log 2>&1

say TORCH_ALL_DONE
