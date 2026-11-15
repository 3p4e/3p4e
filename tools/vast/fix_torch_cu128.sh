#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=/workspace/LTX-2/.venv/bin/python
echo "=== DRIVER ==="
nvidia-smi --query-gpu=driver_version,name --format=csv,noheader
echo "=== CURRENT TORCH ==="
$PY -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())" 2>&1 | tail -2
TV=$($PY -c "import torch; print(torch.__version__.split('+')[0])")
echo "=== REINSTALL torch $TV+cu128 (with deps) ==="
uv pip install --index-url https://download.pytorch.org/whl/cu128 "torch==${TV}+cu128" 2>&1 | tail -12
if $PY -c "import torchvision" 2>/dev/null; then
  TT=$($PY -c "import torchvision; print(torchvision.__version__.split('+')[0])")
  echo "=== REINSTALL torchvision $TT+cu128 ==="
  uv pip install --index-url https://download.pytorch.org/whl/cu128 "torchvision==${TT}+cu128" 2>&1 | tail -8
fi
echo "=== VERIFY ==="
$PY -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')" 2>&1 | tail -4
