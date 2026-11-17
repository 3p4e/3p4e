#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
say(){ echo "[CU126B $(date -u +%H:%M:%S)] $*"; }
set +u
say "nvcc: $(nvcc --version 2>/dev/null | tail -1)"
say "CUDA_HOME=${CUDA_HOME:-unset}; toolkit dirs:"; ls -d /usr/local/cuda* 2>/dev/null
say "kernel .so files under packages:"
find /workspace/LTX-2/packages -name '*.so' 2>/dev/null | head -20
echo "(end .so list)"
set -u
say "INSTALL torch 2.13.0+cu126 (torch only)"
uv pip install \
  --index-url https://download.pytorch.org/whl/cu126 \
  --index-strategy unsafe-best-match \
  "torch==2.13.0+cu126" 2>&1 | tail -20
say "VERIFY torch cuda"
$PY -c "import torch; print('torch', torch.__version__, 'cuda_build', torch.version.cuda, 'avail', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')" 2>&1 | tail -5
say "IMPORT ltx_pipelines.distilled"
$PY -c "import ltx_pipelines.distilled; print('IMPORT_OK')" 2>&1 | tail -15
say "DONE_CU126B"
