#!/bin/bash
# box A: ComfyUI sometimes starts returning wrong-size images from LoadImage (every job then fails in seconds).
# Run the batch; when it ends with failures, restart ComfyUI and run it again (resume-safe), up to 6 rounds.
cd /workspace
for r in 1 2 3 4 5 6; do
  pkill -9 -f "main.py --listen"; sleep 5
  (cd /workspace/ComfyUI && nohup python3 main.py --listen 127.0.0.1 --port 8188 > /workspace/comfy.log 2>&1 &)
  for i in $(seq 1 60); do curl -s 127.0.0.1:8188/system_stats >/dev/null && break; sleep 5; done
  python3 cf_batch.py --only "$(cat cf_only)" > cf_w$r.log 2>&1
  grep -q FAIL cf_w$r.log || break
done
echo WATCH_DONE >> cf_w$r.log
