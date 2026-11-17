#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
say(){ echo "[AUDIO $(date -u +%H:%M:%S)] $*"; }
set +u
say "=== distilled --help (audio-related lines) ==="
$PY -m ltx_pipelines.distilled --help 2>&1 | grep -iE 'audio|sample_rate|save|voice|sound|--' | head -60
say "=== grep torchaudio / torchvision imports in packages ==="
grep -rn "torchaudio" packages/ 2>/dev/null | head -30
echo '--- torchvision ---'
grep -rn "torchvision" packages/ 2>/dev/null | head -30
say "=== grep import torch(audio|vision) in .venv site-packages ltx/ltx_* ==="
grep -rn "import torchaudio\|import torchvision\|from torchaudio\|from torchvision" packages/ltx-core packages/ltx-pipelines 2>/dev/null | head -30
say "=== does the video encoder (flash) need torchvision? search imageio/opencv/PIL ==="
grep -rn "import PIL\|from PIL\|import cv2\|imageio" packages/ltx-core/ltx_core 2>/dev/null | head -15
say "DONE_AUDIO_DIAG"
