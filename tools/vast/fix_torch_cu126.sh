#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
say(){ echo "[CU126 $(date -u +%H:%M:%S)] $*"; }
say "rm compat shim + restore 12.8 driver"
rm -f /etc/ld.so.conf.d/cuda-compat.conf 2>/dev/null; ldconfig
say "exact cu126 wheels present?"
for w in torchvision-0.28.0+cu126 torchaudio-2.13.0+cu126 torch-2.13.0+cu126; do
  name=$(echo $w | sed 's/+.*//')
  hit=$(curl -s "https://download.pytorch.org/whl/cu126/$name/" | grep -oE "${w}-cp311-cp311-linux_x86_64\.whl" | head -1)
  echo "  $w -> ${hit:-MISSING}"
done
say "install torch 2.13.0+cu126 family (no deps resolve across indexes)"
uv pip install \
  --index-url https://download.pytorch.org/whl/cu126 \
  --index-strategy unsafe-best-match \
  torch==2.13.0+cu126 \
  torchvision==0.28.0+cu126 \
  torchaudio==2.13.0+cu126 2>&1 | tail -15
say "drop cu13 cudnn override deps"
uv pip uninstall -y nvidia-cudnn-cu13 2>&1 | tail -3
say "VERIFY cuda availability"
$PY -c "import torch; print('torch', torch.__version__, 'cuda_build', torch.version.cuda, 'avail', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')" 2>&1 | tail -4
