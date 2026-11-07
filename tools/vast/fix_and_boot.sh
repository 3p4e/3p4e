#!/bin/bash
# Install comfy-aimdo (a real ComfyUI dependency that requirements.txt omits)
# then boot ComfyUI and gate the DHPF edit stack.
set -uo pipefail
export LC_ALL=C.UTF-8 HF_HOME=/workspace/hf
LOG=/workspace/fixboot.log
say(){ echo "[FIX $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

CDIR=/workspace/ComfyUI
cd $CDIR || { say FATAL_NO_DIR; exit 1; }

say "installing comfy-aimdo from PyPI"
timeout 300 python3 -m pip install --no-input --break-system-packages \
  --progress-bar off comfy-aimdo >> /workspace/aimdo_pip.log 2>&1
say "comfy-aimdo rc=$?"
tail -4 /workspace/aimdo_pip.log

say "installing remaining requirements (torch satisfied)"
timeout 600 python3 -m pip install --no-input --break-system-packages \
  --progress-bar off -r requirements.txt >> /workspace/req_pip.log 2>&1
say "requirements rc=$?"
tail -6 /workspace/req_pip.log

say "import gate"
python3 - <<'PY'
import importlib
bad=[]
for m in ['torch','einops','safetensors','transformers','av','comfy_aimdo']:
    try:
        importlib.import_module(m); print('ok',m)
    except Exception as e:
        print('FAIL',m,type(e).__name__,e); bad.append(m)
print('GATE_PASS' if not bad else 'GATE_FAIL')
PY

say "booting ComfyUI"
pkill -f 'main.py.*8188' 2>/dev/null || true
sleep 3
setsid nohup python3 main.py --listen 0.0.0.0 --port 8188 \
  > /workspace/comfy.log 2>&1 < /dev/null &
disown

for i in $(seq 1 72); do
  sleep 5
  curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json 2>/dev/null && { say "ComfyUI up after $((i*5))s"; break; }
done
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json 2>/dev/null \
  || { say COMFY_DOWN; tail -25 /workspace/comfy.log; exit 1; }

say "preflight"
python3 - <<'PY'
import json,sys
oi=json.load(open('/workspace/object_info.json'))
want='qwen_image_edit_2511_fp8mixed.safetensors'
opts=oi.get('UNETLoader',{}).get('input',{}).get('required',{}).get('unet_name',[[]])[0]
print('UNET_LISTED:', want in opts)
need=['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','LoadImage',
      'ImageScaleToTotalPixels','TextEncodeQwenImageEditPlus','EmptySD3LatentImage',
      'KSampler','VAEDecode','SaveImage']
miss=[n for n in need if n not in oi]
print('MISSING_NODES:',miss)
ok=(want in opts) and not miss
print('PREFLIGHT_OK' if ok else 'PREFLIGHT_FAIL')
sys.exit(0 if ok else 2)
PY
RC=$?
say "preflight rc=$RC"
[ $RC -eq 0 ] && say "FIXBOOT_ALL_DONE" || say "FIXBOOT_FAILED"
