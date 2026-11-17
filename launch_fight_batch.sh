#!/usr/bin/env bash
set -e
JOB=/workspace/p23_fight10_v4.json
LOG=/workspace/batch_fight.log
if [ -f "$LOG" ]; then mv "$LOG" "$LOG.prev.$(date +%s)"; fi
python3 - << 'PY'
import json, os
j = json.load(open('/workspace/p23_fight10_v4.json'))
print('jobs:', len(j))
print('n:', [x['n'] for x in j])
print('seeds:', [x['seed'] for x in j])
missing = [x['kf'] for x in j if not os.path.exists(x['kf'])]
print('missing keyframes:', missing if missing else 'NONE')
PY
cd /workspace
STRENGTH=0.5 nohup python3 /workspace/render_p23_batch.py "$JOB" 1 10 > "$LOG" 2>&1 &
echo "LAUNCHED pid=$!"
sleep 5
echo '=== first log lines ==='
tail -5 "$LOG" 2>/dev/null || true
