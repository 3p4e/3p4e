#!/bin/bash
cd /workspace/ComfyUI
pgrep -f "main.py --listen" >/dev/null || nohup python3 main.py --listen 127.0.0.1 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 90); do curl -sf http://127.0.0.1:8188/system_stats >/dev/null && break; sleep 5; done
for b in 10 9 8; do
  [ -f /workspace/done_$b ] && continue
  rm -rf /workspace/v3bundle && mkdir -p /workspace/v3bundle && tar xzf /workspace/cb$b.tgz -C /workspace/v3bundle
  cd /workspace && python3 /workspace/v3bundle/batch.py > /workspace/batch$b.log 2>&1 && touch /workspace/done_$b
done
echo ALL_DONE > /workspace/all_done
