#!/bin/bash
exec >> /workspace/logs/render_strengthened.log 2>&1
set -uo pipefail
if [ -f /workspace/.hfenv ]; then . /workspace/.hfenv; fi
MODELS=/workspace/models/ltx23
PY=/workspace/LTX-2/.venv/bin/python
LORA=$MODELS/ltx-2.3-22b-distilled-lora-384-1.1.safetensors
UP=$MODELS/ltx-2.3-spatial-upscaler-x2-1.1.safetensors
CKPT=$MODELS/ltx-2.3-22b-distilled-1.1.safetensors
while [ "$(stat -c%s "$CKPT" 2>/dev/null || echo 0)" -lt 46000000000 ] || [ ! -f "$MODELS/gemma-3-12b-it/config.json" ]; do sleep 15; done
echo "models ready $(date +%H:%M:%S)"
$PY - <<'PYEOF'
import json
jobs = json.load(open('/workspace/fenrir_strengthened_jobfile.json'))['jobs']
jobs.sort(key=lambda j: int(''.join(c for c in j['job_id'] if c.isdigit())))
lines = ['#!/bin/bash', 'set -uo pipefail', 'source /workspace/.hfenv',
         'MODELS=/workspace/models/ltx23',
         'LORA=$MODELS/ltx-2.3-22b-distilled-lora-384-1.1.safetensors',
         'UP=$MODELS/ltx-2.3-spatial-upscaler-x2-1.1.safetensors']
for j in jobs:
    n = int(''.join(c for c in j['job_id'] if c.isdigit()))
    kf = 'kf_%02d_start' % n
    st = j.get('image_strength', 0.85)
    seed = j['seed']
    jid = j['job_id']
    prompt = json.dumps(open('/workspace/stills/%s.txt' % kf).read().strip())
    lines.append("echo 'RENDER %s seed=%s'" % (jid, seed))
    lines.append("if [ ! -f /workspace/out/%s.done ]; then" % jid)
    lines.append("  /workspace/LTX-2/.venv/bin/python -m ltx_pipelines.distilled --distilled-checkpoint-path $MODELS/ltx-2.3-22b-distilled-1.1.safetensors --gemma-root $MODELS/gemma-3-12b-it --prompt %s --output-path /workspace/out/%s.mp4 --image /workspace/stills/%s.png 0 %s --height 704 --width 1216 --num-frames 121 --frame-rate 24 --seed %s --lora $LORA 0.5 --spatial-upsampler-path $UP 2>&1 | tail -3" % (prompt, jid, kf, st, seed))
    lines.append("  test -f /workspace/out/%s.mp4 && { echo 'DONE %s'; sha256sum /workspace/out/%s.mp4 >> /workspace/out/SHA256SUMS.txt; touch /workspace/out/%s.done; } || echo 'FAIL %s'" % (jid, jid, jid, jid, jid))
    lines.append('fi')
open('/workspace/render_q.sh', 'w').write('\n'.join(lines) + '\n')
print('queue built', sum(1 for l in lines if l.startswith('if [')))
PYEOF
bash /workspace/render_q.sh
echo "RENDER_DONE $(date +%H:%M:%S)"
