#!/bin/bash
# comfy_kitchen registers a custom op with `stride: list[int]`, which torch 2.6
# rejects as an unsupported schema type. ComfyUI requires torch >= 2.8
# (2.12+ recommended). Upgrade, verify CUDA, then reboot ComfyUI.
set -uo pipefail
export LC_ALL=C.UTF-8 HF_HOME=/workspace/hf
LOG=/workspace/torch_up.log
say(){ echo "[TORCHUP $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

python3 -c "import torch;print('before', torch.__version__, torch.version.cuda)" 2>&1 | tail -1
nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>&1 | tail -1

say "upgrading torch 2.11.0 + cu128 (driver 595.84 supports cu128)"
timeout 2400 python3 -m pip install --no-input --break-system-packages \
  --progress-bar off --upgrade \
  --index-url https://download.pytorch.org/whl/cu128 \
  torch==2.11.0 torchvision torchaudio >> /workspace/torch_up_pip.log 2>&1
RC=$?
say "pip rc=$RC"
tail -8 /workspace/torch_up_pip.log

say "verifying cuda"
python3 - <<'PY'
import torch, sys
print('torch', torch.__version__)
print('cuda_build', torch.version.cuda)
print('available', torch.cuda.is_available())
if torch.cuda.is_available():
    print('device', torch.cuda.get_device_name(0))
    x = torch.randn(64, 64, device='cuda')
    y = (x @ x).sum().item()
    print('matmul_ok', round(y, 4))
PY

say "--- does comfy_kitchen import now? ---"
python3 -c "import comfy_kitchen; print('comfy_kitchen ok')" 2>&1 | tail -6

say "--- reboot ComfyUI ---"
CDIR=/workspace/ComfyUI
pkill -f 'main.py.*8188' 2>/dev/null || true
sleep 3
cd $CDIR || { say FATAL_NO_DIR; exit 1; }
setsid nohup python3 main.py --listen 0.0.0.0 --port 8188 \
  > /workspace/comfy.log 2>&1 < /dev/null &
disown

for i in $(seq 1 90); do
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
RC2=$?
say "preflight rc=$RC2"
[ $RC2 -eq 0 ] && say "TORCHUP_ALL_DONE" || say "TORCHUP_FAILED"
