#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace/LTX-2
PY=.venv/bin/python
say(){ echo "[READY $(date -u +%H:%M:%S)] $*"; }
say "1) distilled import exit code"
$PY -c "import ltx_pipelines.distilled; print('DISTILLED_IMPORT_OK')" > /tmp/imp.log 2>&1
rc=$?
echo "  rc=$rc"
tail -6 /tmp/imp.log
say "2) does pipeline tree import torchvision?"
grep -rIl 'torchvision' packages/ltx-pipelines/ 2>/dev/null || echo "  NO torchvision reference in ltx-pipelines"
say "3) does ltx-core import torchvision?"
grep -rIl 'torchvision' packages/ltx-core/ 2>/dev/null || echo "  NO torchvision reference in ltx-core"
say "4) torchvision installed version"
$PY -c "import torchvision; print(torchvision.__version__)" 2>&1 | tail -1
say "5) any other torch-linked .so under venv that could mismatch (nms/cublasLt)"
find .venv/lib/python3.11/site-packages -maxdepth 3 -name '*.so' 2>/dev/null | grep -iE 'torch|kernel|ltx' | head -20
say "DIAG_DONE"
