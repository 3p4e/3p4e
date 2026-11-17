#!/bin/bash
# Face-conditioned look cards on the rented box: Qwen-Image-Edit 2511.
# Restarts ComfyUI so the freshly downloaded Edit checkpoint appears in its
# model list, verifies it is actually offered by UNETLoader, then renders.
# No in-instance watchdog: teardown is controlled from the host after verify.
set -uo pipefail
export LC_ALL=C.UTF-8 HF_HOME=/workspace/hf
CDIR=/workspace/ComfyUI
LOG=/workspace/edit.log
say(){ echo "[EDIT $(date -u +%H:%M:%S)] $*" | tee -a $LOG; }

say "start on $(hostname)"

# --- restart ComfyUI so new checkpoints are scanned ---
say "restarting ComfyUI"
pkill -f 'main.py.*8188' 2>/dev/null
sleep 3
cd $CDIR && nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 60); do
  sleep 5
  curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json 2>/dev/null && { say "ComfyUI up after $((i*5))s"; break; }
done
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json || { say COMFY_DOWN; exit 1; }

# --- verify the Edit checkpoint is offered by UNETLoader ---
python3 - <<'PY' 2>&1 | tee -a /workspace/edit.log
import json, sys
oi = json.load(open('/workspace/object_info.json'))
opts = oi['UNETLoader']['input']['required']['unet_name'][0]
want = 'qwen_image_edit_2511_fp8mixed.safetensors'
print('UNET options:', opts)
if want not in opts:
    print('FATAL_EDIT_MODEL_NOT_LISTED')
    sys.exit(3)
need = ['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','LoadImage',
        'ImageScaleToTotalPixels','TextEncodeQwenImageEditPlus','EmptySD3LatentImage',
        'KSampler','VAEDecode','SaveImage']
miss = [n for n in need if n not in oi]
print('MISSING_NODES:', miss)
if miss:
    print('FATAL_NODES'); sys.exit(4)
print('PREFLIGHT_OK')
PY
grep -q PREFLIGHT_OK /workspace/edit.log || { say PREFLIGHT_FAILED; exit 2; }
say "preflight pass"

# --- stage references into ComfyUI input ---
mkdir -p $CDIR/input
for f in ddface_a.jpg ddface_b.jpg azface_a.jpg azface_b.jpg; do
  if [ -f /workspace/refs/$f ]; then
    cp -f /workspace/refs/$f $CDIR/input/$f
    say "staged $f $(stat -c%s /workspace/refs/$f) bytes"
  else
    say "MISSING_REF $f"
  fi
done
ls -lh $CDIR/input/ddface_a.jpg $CDIR/input/azface_a.jpg >> $LOG 2>&1

# --- render ---
say "rendering look cards (40 steps each)"
cd /workspace
python3 /workspace/run_qwen_edit.py --host http://127.0.0.1:8188 \
  --jobs /workspace/edit_jobs.json --out /workspace/out_edit \
  --comfy-dir $CDIR >> /workspace/edit.log 2>&1
say "jobs exit=$?"
ls -lh /workspace/out_edit >> $LOG 2>&1
say "EDIT_ALL_DONE"
