#!/bin/bash
# Qwen-Image-Edit-2511 keyframe autorun for Vast.ai (vastai/comfy template, ComfyUI on :8188).
# All weights Apache-2.0 -> unrestricted commercial use. No territory ban.
export LC_ALL=C
export HF_HOME=/workspace/hf
LOG=/workspace/qwen.log; mkdir -p /workspace/out /workspace/refs $HF_HOME
MAXMIN=${MAXMIN:-70}
say(){ m="[QWEN $(date -u +%H:%M:%S)] $*"; echo "$m" >> $LOG; echo "$m" > /proc/1/fd/1 2>/dev/null || true; }
stop_self(){ curl -s -X PUT -H "Authorization: Bearer $CONTAINER_API_KEY" -H "Content-Type: application/json" -d '{"state":"stopped"}' "https://console.vast.ai/api/v0/instances/$CONTAINER_ID/" >> $LOG 2>&1; }

say "start on $(hostname); cap ${MAXMIN} min"
( sleep $((MAXMIN*60)); say "CAP -> stop"; stop_self ) &

# locate ComfyUI
CDIR=$(dirname $(find / -maxdepth 6 -type f -name 'main.py' -path '*ComfyUI*' 2>/dev/null | head -1) 2>/dev/null)
say "ComfyUI: $CDIR"
[ -z "$CDIR" ] && { say "FATAL no ComfyUI"; exit 1; }

DM=$CDIR/models/diffusion_models; TE=$CDIR/models/text_encoders; VA=$CDIR/models/vae; LO=$CDIR/models/loras
mkdir -p $DM $TE $VA $LO

P=/venv/main/bin/python; [ -x $P ] || P=python3
say "prefetching Apache-2.0 weights (~32 GB)"
$P - <<'PY' 2>&1 | tail -20 | while read -r l; do say "dl: $l"; done
import os,sys
from huggingface_hub import hf_hub_download
CDIR=os.environ.get('CDIR') or ''
PY

# robust python prefetch with explicit dest dirs
CDIR="$CDIR" DM="$DM" TE="$TE" VA="$VA" LO="$LO" $P - <<'PY' 2>&1 | while read -r l; do echo "[QWEN dl] $l" >> /workspace/qwen.log; echo "[QWEN dl] $l" > /proc/1/fd/1 2>/dev/null || true; done
import os
from huggingface_hub import hf_hub_download
dm,te,va,lo=os.environ['DM'],os.environ['TE'],os.environ['VA'],os.environ['LO']
jobs=[
 ('Comfy-Org/Qwen-Image-Edit_ComfyUI','split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors',dm),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors',te),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/vae/qwen_image_vae.safetensors',va),
 ('lightx2v/Qwen-Image-Edit-2511-Lightning','Qwen-Image-Edit-2511-Lightning-4steps-V1.0-fp32.safetensors',lo),
]
for repo,f,d in jobs:
    print('get',f,flush=True)
    p=hf_hub_download(repo_id=repo,filename=f,local_dir=d)
    print('ok',p,os.path.getsize(p),flush=True)
print('ALL_WEIGHTS_DONE',flush=True)
PY

say "restarting ComfyUI to index new weights"
pkill -f 'main.py.*8188' 2>/dev/null; pkill -f ComfyUI 2>/dev/null; sleep 3
cd $CDIR && nohup $P main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 40); do sleep 5; curl -sf http://127.0.0.1:8188/object_info >/dev/null 2>&1 && { say "ComfyUI up after $((i*5))s"; break; }; done
curl -sf http://127.0.0.1:8188/object_info >/dev/null && say "READY" || say "COMFY NOT READY"
touch /workspace/QWEN_READY
say "autorun complete; waiting for jobs"
