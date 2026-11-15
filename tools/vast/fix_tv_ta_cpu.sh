#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
say(){ echo "[TVTA $(date -u +%H:%M:%S)] $*"; }
say "uninstall broken cu132 torchvision/torchaudio"
uv pip uninstall -y torchvision torchaudio 2>&1 | tail -6
say "install CPU torchvision 0.28.0 + torchaudio 2.13.0 (ABI match torch 2.13)"
uv pip install torchvision==0.28.0 torchaudio==2.13.0 2>&1 | tail -12
say "verify imports"
$PY -c "import torch, torchvision, torchaudio; print('torch', torch.__version__, torch.cuda.is_available()); print('torchvision', torchvision.__version__); print('torchaudio', torchaudio.__version__)" 2>&1 | tail -6
say "import distilled pipeline"
$PY -c "import ltx_pipelines.distilled; print('DISTILLED_IMPORT_OK')" 2>&1 | tail -20
say "DONE_TVTA"
