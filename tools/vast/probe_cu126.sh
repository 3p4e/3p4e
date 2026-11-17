#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
echo "=== exact cu126 torch 2.13.x filenames (cp311 linux x86_64) ==="
curl -s https://download.pytorch.org/whl/cu126/torch/ | grep -oE 'torch-2\.13\.[0-9]+%2Bcu126-[^"]*\.whl' | sed 's/%2B/+/g' | sort -uV
echo "=== exact cu126 torchvision 0.2x filenames ==="
curl -s https://download.pytorch.org/whl/cu126/torchvision/ | grep -oE 'torchvision-[0-9.]+%2Bcu126-[^"]*\.whl' | sed 's/%2B/+/g' | sort -uV | tail -8
echo "=== exact cu126 torchaudio 2.x filenames ==="
curl -s https://download.pytorch.org/whl/cu126/torchaudio/ | grep -oE 'torchaudio-[0-9.]+%2Bcu126-[^"]*\.whl' | sed 's/%2B/+/g' | sort -uV | tail -8
echo "=== nvcc present? ==="
which nvcc || echo NO_NVCC
echo "CUDA_HOME=$CUDA_HOME env_cuda=$GOPATH"
ls /usr/local/ | grep -i cuda || echo NO_CUDA_TOOLKIT_DIR
echo "=== installed kernels: compiled ext or pure python? ==="
$PY -c "import ltx_core, ltx_pipelines, os; print('ltx_core', os.path.dirname(ltx_core.__file__)); print('ltx_pipelines', os.path.dirname(ltx_pipelines.__file__))" 2>&1 | tail -6
find /workspace/LTX-2 -name '*.so' -path '*ltx*' 2>/dev/null | head -20
find /workspace/LTX-2/packages -name '*.so' 2>/dev/null | head -20
echo "=== torch/lib cudnn under cu132 now ==="
find .venv/lib -name 'libcudnn*' 2>/dev/null | head -5
echo "=== does distilled submodule import cleanly without kernels? ==="
$PY -c "import ltx_pipelines.distilled" 2>&1 | tail -8
