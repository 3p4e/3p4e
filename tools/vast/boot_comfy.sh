#!/bin/bash
# Boot ComfyUI and prove the DHPF edit stack is actually usable.
# Weights are already on disk; this only starts the server and gates it.
set -uo pipefail
export LC_ALL=C.UTF-8 HF_HOME=/workspace/hf
LOG=/workspace/boot.log
say(){ echo "[BOOT $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

CDIR=/workspace/ComfyUI
[ -f $CDIR/main.py ] || { say FATAL_NO_COMFY; exit 1; }

# --- report what we actually have on disk ---
say "weights on disk"
ls -lh $CDIR/models/diffusion_models/*.safetensors \
       $CDIR/models/text_encoders/*.safetensors \
       $CDIR/models/vae/*.safetensors 2>&1 | tail -10

# --- restart clean ---
pkill -f 'main.py.*8188' 2>/dev/null || true
sleep 3
say "starting ComfyUI on 8188"
cd $CDIR
setsid nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 < /dev/null &
disown

for i in $(seq 1 60); do
  sleep 5
  if curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json 2>/dev/null; then
    say "ComfyUI up after $((i*5))s"
    break
  fi
done
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json 2>/dev/null \
  || { say COMFY_DOWN; tail -30 /workspace/comfy.log; exit 1; }

# --- preflight: model listed by UNETLoader + all edit nodes present ---
python3 - <<'PY'
import json, sys
oi = json.load(open('/workspace/object_info.json'))

want = 'qwen_image_edit_2511_fp8mixed.safetensors'
opts = oi.get('UNETLoader', {}).get('input', {}).get('required', {}).get('unet_name', [[]])[0]
print('UNET_OPTIONS:', opts)
listed = want in opts
print('UNET_LISTED:', listed)

need = ['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','LoadImage',
        'ImageScaleToTotalPixels','TextEncodeQwenImageEditPlus','EmptySD3LatentImage',
        'KSampler','VAEDecode','SaveImage']
missing = [n for n in need if n not in oi]
print('MISSING_NODES:', missing)

ok = listed and not missing
print('PREFLIGHT_OK' if ok else 'PREFLIGHT_FAIL')
sys.exit(0 if ok else 2)
PY
RC=$?
say "preflight rc=$RC"
[ $RC -eq 0 ] && say "BOOT_ALL_DONE" || say "BOOT_FAILED"
