#!/bin/bash
# pause the category batch, render this box's half of logo round 3, then resume the category batch (all resume-safe)
cd /workspace; BOX=$1
pkill -f watchA.sh; pkill -f cf_batch; sleep 3
rm -rf /workspace/lgbundle; mkdir -p /workspace/lgbundle && tar xzf /workspace/logo_bundle3.tgz -C /workspace/lgbundle
if [ "$BOX" = A ]; then pkill -9 -f "main.py --listen"; sleep 5; (cd ComfyUI && nohup python3 main.py --listen 127.0.0.1 --port 8188 > /workspace/comfy.log 2>&1 &); for i in $(seq 1 60); do curl -s 127.0.0.1:8188/system_stats >/dev/null && break; sleep 5; done; fi
python3 lg_batch.py --only "$(cat lg3_only)" > lg3.log 2>&1; echo LG3_DONE >> lg3.log
if [ "$BOX" = A ]; then bash /workspace/watchA.sh; else python3 cf_batch.py --only "$(cat cf_only)" > cf2.log 2>&1; echo CF_ALL_DONE >> cf2.log; fi
