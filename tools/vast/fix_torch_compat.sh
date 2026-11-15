#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
PY=/workspace/LTX-2/.venv/bin/python
say(){ echo "[COMPAT $(date -u +%H:%M:%S)] $*"; }
say "install cuda-compat-13-2 shim"
apt-get update -qq 2>&1 | tail -2
apt-get install -y -qq cuda-compat-13-2 2>&1 | tail -5
say "register compat dir"
mkdir -p /etc/ld.so.conf.d
echo '/usr/local/cuda-13.2/compat' > /etc/ld.so.conf.d/cuda-compat.conf
ldconfig
echo "compat dir exists: $(ls -d /usr/local/cuda-13.2/compat 2>/dev/null || echo MISSING)"
echo "compat libs:"
ls /usr/local/cuda-13.2/compat/ 2>/dev/null | head
export LD_LIBRARY_PATH=/usr/local/cuda-13.2/compat:$LD_LIBRARY_PATH
say "verify cuda availability"
$PY -c "import torch; print('torch', torch.__version__, 'cuda_avail', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')" 2>&1 | tail -3
