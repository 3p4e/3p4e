#!/bin/bash
# ComfyUI main.py imports comfy_aimdo. torch is now installed, so the proper
# fix is to finally run ComfyUI's own requirements.txt (it wedged before only
# because torch was missing and pip tried to resolve multi-GB wheels silently).
set -uo pipefail
export LC_ALL=C.UTF-8 HF_HOME=/workspace/hf
LOG=/workspace/aimdo.log
say(){ echo "[AIMDO $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

CDIR=/workspace/ComfyUI
cd $CDIR || { say FATAL_NO_DIR; exit 1; }

say "--- what main.py imports ---"
grep -n 'comfy_aimdo\|^import\|^from' main.py | head -20
say "--- requirements mentions ---"
grep -in 'aimdo' requirements.txt || say "aimdo not named in requirements"

say "--- torch already present, so requirements can resolve ---"
python3 -c "import torch;print('torch',torch.__version__)" 2>&1 | tail -2

say "--- installing ComfyUI requirements (torch satisfied, no re-download) ---"
timeout 900 python3 -m pip install --no-input --break-system-packages \
  --progress-bar off -r requirements.txt >> /workspace/req_pip.log 2>&1
say "requirements rc=$?"
tail -12 /workspace/req_pip.log

say "--- import gate ---"
python3 - <<'PY'
import importlib
for m in ['torch','einops','safetensors','transformers','av','accelerate','comfy_aimdo']:
    try:
        importlib.import_module(m); print('ok', m)
    except Exception as e:
        print('FAIL', m, type(e).__name__, e)
PY

say "AIMDO_FIX_DONE"
