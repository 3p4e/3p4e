#!/bin/bash
# Install ONLY the small ComfyUI dependencies, never torch.
# The full requirements.txt makes pip re-resolve multi-GB torch on a
# PyTorch base image, which wedges silently for an hour.
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/deps.log
say(){ echo "[DEPS $(date -u +%H:%M:%S)] $*" | tee -a $LOG; }

say "killing any wedged pip"
pkill -9 -f 'pip install' 2>/dev/null; sleep 2

say "torch check"
python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available())" 2>&1 | tee -a $LOG

say "installing small deps only (no torch)"
timeout 420 python3 -m pip install --no-input --break-system-packages \
  --progress-bar off --no-deps \
  einops safetensors av scipy 2>&1 | tail -8 | tee -a $LOG

say "installing deps that need resolution (still torch-free)"
timeout 420 python3 -m pip install --no-input --break-system-packages \
  --progress-bar off \
  transformers accelerate 2>&1 | tail -8 | tee -a $LOG

say "import gate"
python3 - <<'PY' 2>&1 | tee -a $LOG
import importlib
mods = ['torch','einops','safetensors','transformers','av','accelerate','numpy','PIL']
bad = []
for m in mods:
    try:
        importlib.import_module(m); print('ok', m)
    except Exception as e:
        print('FAIL', m, type(e).__name__, e); bad.append(m)
print('IMPORT_GATE_PASS' if not bad else 'IMPORT_GATE_FAIL ' + ','.join(bad))
PY
say DEPS_DONE
