#!/bin/bash
set -uo pipefail
export LC_ALL=C.UTF-8
mkdir -p /workspace/logs /workspace/models /workspace/out /workspace/stills
LOG=/workspace/logs/ltx23_s01.log
exec >> $LOG 2>&1
say(){ echo "[S01 $(date -u +%H:%M:%S)] $*"; }
say "start on $(hostname)"

if [ -z "${HF_TOKEN:-}" ]; then
  if [ -f /workspace/.hfenv ]; then set -a; . /workspace/.hfenv; set +a; fi
fi
if [ -z "${HF_TOKEN:-}" ]; then say "FATAL_NO_TOKEN"; exit 1; fi
say "token len ${#HF_TOKEN}"

cd /workspace
if [ ! -d LTX-2 ]; then
  say "clone Lightricks/LTX-2"
  git clone --depth 1 https://github.com/Lightricks/LTX-2.git 2>&1 | tail -3
fi
cd /workspace/LTX-2
say "uv sync"
uv sync 2>&1 | tail -8
PY=/workspace/LTX-2/.venv/bin/python
$PY -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available())" 2>&1 | tail -3

MODELS=/workspace/models/ltx23
mkdir -p $MODELS
cd $MODELS
if [ ! -f gemma-3-12b-it/config.json ]; then
  say "pull FULL gemma-3-12b-it via UNSLOTH mirror (google/ is 403-gated)"
  (uvx hf download unsloth/gemma-3-12b-it --local-dir $MODELS/gemma-3-12b-it 2>&1 || \
   $PY -m huggingface_hub.snapshot_download unsloth/gemma-3-12b-it --local-dir $MODELS/gemma-3-12b-it 2>&1) | tail -6
fi
say "gemma files: $(ls $MODELS/gemma-3-12b-it 2>/dev/null | wc -l)"

fetch(){
  repo="$1"; path="$2"; name="${path##*/}"; out="$MODELS/$name"
  [ -f "$out" ] && { say "have $name"; return; }
  url="https://huggingface.co/$repo/resolve/main/$path"
  say "GET $name"
  curl -L --fail --connect-timeout 20 --max-time 7200 -C - -H "Authorization: Bearer $HF_TOKEN" -o "$out" "$url" 2>/dev/null
  rc=$?; sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
  say "$name rc=$rc bytes=$sz"
  [ "$sz" = "0" ] && { say "RETRY_NO_AUTH $name"; curl -L --fail --connect-timeout 20 --max-time 7200 -C - -o "$out" "$url" 2>/dev/null; say "$name anon bytes=$(stat -c%s "$out" 2>/dev/null || echo 0)"; }
}
fetch Lightricks/LTX-2.3 ltx-2.3-22b-distilled-1.1.safetensors
fetch Lightricks/LTX-2.3 ltx-2.3-22b-distilled-lora-384-1.1.safetensors
fetch Lightricks/LTX-2.3 ltx-2.3-spatial-upscaler-x2-1.1.safetensors

say "stills: $(ls -la /workspace/stills/ 2>/dev/null | tail -2)"
PROMPT='Mist drifts across the corruption-ring edge while the two figures hold their stance on the hummock. The camera pushes in slowly. Opening the beat. Photoreal, 35mm anamorphic, film grain, real skin.'

say "RENDER start"
cd /workspace/LTX-2
$PY -m ltx_pipelines.distilled \
  --distilled-checkpoint-path $MODELS/ltx-2.3-22b-distilled-1.1.safetensors \
  --gemma-root $MODELS/gemma-3-12b-it \
  --prompt "$PROMPT" \
  --output-path /workspace/out/ltx23_s01_kf01.mp4 \
  --image /workspace/stills/kf_01_start.png 0 0.7 \
  --height 704 --width 1216 --num-frames 121 --frame-rate 24 --seed 1 \
  --lora $MODELS/ltx-2.3-22b-384-distilled-lora.safetensors 0.5 \
  --spatial-upsampler-path $MODELS/ltx-2.3-spatial-upscaler-x2-1.1.safetensors \
  2>&1 | tail -40
say "RENDER rc=$?"
ls -la /workspace/out/ltx23_s01_kf01.mp4 2>/dev/null && say "PROOF_DONE" || say "PROOF_MISSING"
