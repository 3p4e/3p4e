#!/bin/bash
set -u
JOBFILE=$1; shift
SHOTS=$@
cd /workspace/LTX-2
source .venv/bin/activate 2>/dev/null || true
export HF_HUB_OFFLINE=1
for N in $SHOTS; do
  KF=$(python3 -c "import json;j=[x for x in json.load(open('$JOBFILE')) if x['n']==$N][0];print(j['kf'])")
  OUT=$(python3 -c "import json;j=[x for x in json.load(open('$JOBFILE')) if x['n']==$N][0];print(j['out'])")
  SEED=$(python3 -c "import json;j=[x for x in json.load(open('$JOBFILE')) if x['n']==$N][0];print(j['seed'])")
  PROMPT=$(python3 -c "import json;j=[x for x in json.load(open('$JOBFILE')) if x['n']==$N][0];print(j['prompt'].replace(chr(10),' '))")
  echo "[RENDER] START s$N seed=$SEED"
  python -m ltx_pipelines.distilled \
    --distilled-checkpoint-path /workspace/models/ltx-2.3-22b-distilled-1.1.safetensors \
    --gemma-root /workspace/models/gemma-3-12b-it \
    --lora /workspace/models/ltx-2.3-22b-distilled-lora-384-1.1.safetensors 0.5 \
    --spatial-upsampler-path /workspace/models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors \
    --prompt "$PROMPT" \
    --image $KF 0 0.5 \
    --width 1216 --height 704 --num-frames 121 --frame-rate 24 \
    --seed $SEED --offload cpu \
    --output-path $OUT 2>&1 | grep -vE "nanobind|refleaks|it/s" | tail -5
  SIZE=$(stat -c%s $OUT 2>/dev/null || echo 0)
  echo "[RENDER] END s$N size=$SIZE"
done
echo "[RENDER] ALL_PROOF_DONE"
