#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
say(){ echo "[TVTA2 $(date -u +%H:%M:%S)] $*"; }
say "install CPU torchvision 0.28.0 + torchaudio 2.11.1 (no CUDA dep -> ABI-safe with cu126 torch)"
uv pip install --index-strategy unsafe-best-match torchvision==0.28.0 torchaudio==2.11.1 2>&1 | tail -14
say "VERIFY torch family"
$PY -c "import torch, torchvision, torchaudio; print('torch', torch.__version__, 'cuda', torch.cuda.is_available()); print('torchvision', torchvision.__version__); print('torchaudio', torchaudio.__version__)" 2>&1 | tail -6
say "IMPORT distilled pipeline (decisive)"
$PY -c "import ltx_pipelines.distilled; print('DISTILLED_IMPORT_OK')" 2>&1 | grep -vE 'leaked|nanobind|OpenImageIO|skipped remainder|refcounting|readthedocs|^  - ' | tail -12
say "DONE_TVTA2"
