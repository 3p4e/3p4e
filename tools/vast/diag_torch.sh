#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
echo "=== undo compat shim (restore real 12.8 driver) ==="
rm -f /etc/ld.so.conf.d/cuda-compat.conf 2>/dev/null; ldconfig
echo "=== nvidia-smi head ==="
nvidia-smi | head -12
echo "=== driver CUDA version via nvml ==="
$PY -c "import ctypes;c=ctypes.CDLL('libcuda.so.1');v=ctypes.c_int(0);c.cuDriverGetVersion(ctypes.byref(v));print('cuDriverGetVersion',v.value)" 2>&1 | tail -2
echo "=== current torch/torchvision ==="
$PY -c "import torch;print('torch',torch.__version__,'cuda_build',torch.version.cuda)" 2>&1 | tail -1
$PY -c "import torchvision;print('torchvision',torchvision.__version__)" 2>&1 | tail -1
echo "=== cu128 latest torch cp311 ==="
curl -s https://download.pytorch.org/whl/cu128/torch/ | grep -oE 'torch-2\.[0-9]+\.[0-9]+\+cu128-cp311-cp311-linux_x86_64\.whl' | sort -uV | tail -6
echo "=== cu126 latest torch cp311 ==="
curl -s https://download.pytorch.org/whl/cu126/torch/ | grep -oE 'torch-2\.[0-9]+\.[0-9]+\+cu126-cp311-cp311-linux_x86_64\.whl' | sort -uV | tail -6
echo "=== LTX-2 pyproject torch pin ==="
grep -nE 'torch' pyproject.toml 2>/dev/null | head -10
