#!/bin/bash
# FENRIR P8 BATCH — render all 46 clips sequentially on the rented 48GB box.
# Pre-req: rent_fenrir_p8.py has run, box record at .fenrir_p8_box.json, jobfile pushed to /workspace/jobfile.json,
# all 46 keyframes pushed to /workspace/stills/, HF token at /workspace/.hfenv.
# Each clip renders then is checksummed + logged; local side pulls via scp as clips land (supervised).
set -uo pipefail
export LC_ALL=C.UTF-8
mkdir -p /workspace/logs /workspace/out /workspace/stills /workspace/models
LOG=/workspace/logs/fenrir_p8.log
exec >> $LOG 2>&1
say(){ echo "[P8 $(date -u +%H:%M:%S)] $*"; }

if [ -z "${HF_TOKEN:-}" ] && [ -f /workspace/.hfenv ]; then set -a; . /workspace/.hfenv; set +a; fi
[ -z "${HF_TOKEN:-}" ] && { say FATAL_NO_TOKEN; exit 1; }

cd /workspace
if [ ! -d LTX-2 ]; then say clone; git clone --depth 1 https://github.com/Lightricks/LTX-2.git 2>&1 | tail -2; fi
cd LTX-2 && uv sync 2>&1 | tail -4
PY=/workspace/LTX-2/.venv/bin/python
$PY -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available())" 2>&1 | tail -2

MODELS=/workspace/models/ltx23
mkdir -p $MODELS
cd $MODELS
if [ ! -f gemma-3-12b-it/config.json ]; then
  say "pull FULL gemma-3-12b-it (unslooth mirror)"
  (uvx hf download unsloth/gemma-3-12b-it --local-dir $MODELS/gemma-3-12b-it 2>&1 || \
   $PY -m huggingface_hub.snapshot_download unsloth/gemma-3-12b-it --local-dir $MODELS/gemma-3-12b-it 2>&1) | tail -4
fi
fetch(){
  repo="$1"; path="$2"; name="${path##*/}"; out="$MODELS/$name"
  [ -f "$out" ] && { say "have $name"; return; }
  curl -L --fail --connect-timeout 20 --max-time 7200 -C - -H "Authorization: Bearer $HF_TOKEN" \
    -o "$out" "https://huggingface.co/$repo/resolve/main/$path" 2>/dev/null
  say "$name bytes=$(stat -c%s "$out" 2>/dev/null || echo 0)"
}
fetch Lightricks/LTX-2.3 ltx-2.3-22b-distilled-1.1.safetensors
fetch Lightricks/LTX-2.3 ltx-2.3-22b-distilled-lora-384-1.1.safetensors
fetch Lightricks/LTX-2.3 ltx-2.3-spatial-upscaler-x2-1.1.safetensors
LORA=$MODELS/ltx-2.3-22b-distilled-lora-384-1.1.safetensors

render(){
  local kf="$1" prompt="$2" seed="$3" out="$4"
  [ -f "/workspace/out/$out.done" ] && { say "skip $out (done marker)"; return 0; }
  say "RENDER $out seed=$seed"
  cd /workspace/LTX-2
  $PY -m ltx_pipelines.distilled \
    --distilled-checkpoint-path $MODELS/ltx-2.3-22b-distilled-1.1.safetensors \
    --gemma-root $MODELS/gemma-3-12b-it \
    --prompt "$prompt" \
    --output-path "/workspace/out/$out" \
    --image "/workspace/stills/$kf" 0 0.7 \
    --height 704 --width 1216 --num-frames 121 --frame-rate 24 --seed "$seed" \
    --lora $LORA 0.5 \
    --spatial-upsampler-path $MODELS/ltx-2.3-spatial-upscaler-x2-1.1.safetensors \
    2>&1 | tail -6
  local rc=$?
  if [ -f "/workspace/out/$out" ]; then
    sha256sum "/workspace/out/$out" | awk '{print $1, FILENAME}' >> /workspace/out/SHA256SUMS.txt
    echo "$(date -u +%FT%TZ) $out rc=$rc bytes=$(stat -c%s /workspace/out/$out)" >> /workspace/out/manifest.tsv
    touch "/workspace/out/$out.done"
    say "DONE $out"
  else
    echo "$(date -u +%FT%TZ) $out rc=$rc FAILED" >> /workspace/out/manifest.tsv
    say "FAILED $out rc=$rc"
  fi
  return $rc
}

$PY - << 'PYEOF'
import json, shlex
jobs = json.load(open('/workspace/jobfile.json'))['jobs']
with open('/workspace/render_queue.sh', 'w') as q:
    q.write('#!/bin/bash\nset -uo pipefail\nsource /workspace/render_lib.sh\n')
    for j in jobs:
        out = j['job_id'] + '.mp4'
        kf = j['start_frame'].split('/')[-1]
        q.write('render ' + ' '.join(shlex.quote(x) for x in (kf, j['prompt'], str(j['seed']), out)) + '\n')
PYEOF
bash /workspace/render_queue.sh
say "ALL_JOBS_COMPLETE"
ls -la /workspace/out/*.mp4 2>/dev/null | wc -l
