#!/bin/bash
# Provision RTX A6000 box for the LTX-2.3 22B distilled v4 batch (story #23).
# Reuses the PROVEN route from ltx23_s01_render.sh (uv sync + unsloth gemma mirror + curl -C resume).
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/prov_p23_final.log
say(){ echo "[PROV $(date -u +%H:%M:%S)] $*"; }
exec >> "$LOG" 2>&1
say "START on $(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
df -h /workspace | tail -1

# 1. uv
if ! command -v uv >/dev/null 2>&1; then
  say "installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
say "uv: $(uv --version 2>/dev/null)"

# 2. LTX-2 repo + uv sync
cd /workspace
if [ ! -d LTX-2 ]; then
  say "clone Lightricks/LTX-2"
  git clone --depth 1 https://github.com/Lightricks/LTX-2.git 2>&1 | tail -3
fi
cd /workspace/LTX-2
say "uv sync"
uv sync 2>&1 | tail -8
PY=/workspace/LTX-2/.venv/bin/python
"$PY" -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available())" 2>&1 | tail -3

# 3. weights
MODELS=/workspace/models/ltx23
mkdir -p "$MODELS"
say "gemma dir present: $(ls $MODELS/gemma-3-12b-it 2>/dev/null | wc -l)"
if [ ! -f "$MODELS/gemma-3-12b-it/config.json" ]; then
  say "pull FULL gemma-3-12b-it via UNSLOTH mirror (google/ is 403-gated)"
  ( uvx hf download unsloth/gemma-3-12b-it --local-dir "$MODELS/gemma-3-12b-it" 2>&1 || \
    "$PY" -m huggingface_hub.snapshot_download unsloth/gemma-3-12b-it --local-dir "$MODELS/gemma-3-12b-it" 2>&1 ) | tail -6
fi
say "gemma file count: $(ls $MODELS/gemma-3-12b-it 2>/dev/null | wc -l)"

fetch(){
  repo="$1"; path="$2"; name="${path##*/}"; out="$MODELS/$name"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" -gt 1000000000 ]; then say "have $name ($(stat -c%s "$out") B)"; return; fi
  url="https://huggingface.co/$repo/resolve/main/$path"
  # ungated repos: try anon first, token only as fallback
  if [ -n "${HF_TOKEN:-}" ] && [ -f /workspace/.hfenv ]; then set -a; . /workspace/.hfenv; set +a; fi
  say "GET $name"
  for attempt in $(seq 1 12); do
    curl -L --fail --connect-timeout 20 --max-time 7200 -C - -o "$out" "$url" 2>>/workspace/prov_curl.log
    rc=$?; sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
    say "  attempt $attempt rc=$rc bytes=$sz"
    [ "$rc" = "0" ] && break
    [ "$rc" = "33" ] && { say "resume unsupported, restart"; rm -f "$out"; }
    sleep 5
  done
  say "DONE $name bytes=$(stat -c%s "$out" 2>/dev/null || echo 0)"
}
fetch Lightricks/LTX-2.3 ltx-2.3-22b-distilled-1.1.safetensors
fetch Lightricks/LTX-2.3 ltx-2.3-22b-distilled-lora-384-1.1.safetensors
fetch Lightricks/LTX-2.3 ltx-2.3-spatial-upscaler-x2-1.1.safetensors

say "SUMMARY"
ls -lh "$MODELS"
echo "gemma files: $(ls $MODELS/gemma-3-12b-it 2>/dev/null | wc -l)"
df -h /workspace | tail -1
say "PROV_ALL_DONE"
