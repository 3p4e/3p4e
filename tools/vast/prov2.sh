#!/bin/bash
# Weights + boot for the DHPF look/keyframe pipeline, on a box that now HAS torch.
# Never installs torch: that is done separately and verified.
set -uo pipefail
export LC_ALL=C.UTF-8 HF_HOME=/workspace/hf
LOG=/workspace/prov2.log
say(){ echo "[PROV2 $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"
mkdir -p /workspace/hf /workspace/out

# --- light deps only, torch untouched ---
say "light deps"
python3 -m pip install --no-input --break-system-packages --progress-bar off \
  einops safetensors av transformers accelerate >> /workspace/deps2.log 2>&1
say "deps exit=$?"
python3 -c "import einops,safetensors,transformers,torch,av;print('deps_ok')" >> /workspace/deps2.log 2>&1
say "deps_gate=$?"

# --- ComfyUI present? ---
CDIR=/workspace/ComfyUI
[ -f $CDIR/main.py ] || { say FATAL_NO_COMFY; exit 1; }

# --- weights ---
DM=$CDIR/models/diffusion_models; TE=$CDIR/models/text_encoders; VA=$CDIR/models/vae
mkdir -p $DM $TE $VA
export DM TE VA
say "fetching weights (~30 GB)"
python3 - <<'PY' >> /workspace/weights.log 2>&1
import os, shutil, time
from huggingface_hub import hf_hub_download
dm,te,va = os.environ['DM'], os.environ['TE'], os.environ['VA']
stage='/workspace/stage'; os.makedirs(stage,exist_ok=True)
jobs=[
 ('Comfy-Org/Qwen-Image-Edit_ComfyUI','split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors',dm),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors',te),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/vae/qwen_image_vae.safetensors',va),
]
for repo,fn,dest in jobs:
    name=fn.split('/')[-1]; tgt=os.path.join(dest,name)
    if os.path.exists(tgt) and os.path.getsize(tgt)>1000000:
        print('skip',name,os.path.getsize(tgt),flush=True); continue
    t0=time.time(); print('get',name,flush=True)
    p=hf_hub_download(repo_id=repo,filename=fn,local_dir=stage)
    os.makedirs(dest,exist_ok=True); shutil.move(p,tgt)
    sz=os.path.getsize(tgt)
    print('ok',name,sz,'%.1fs'%(time.time()-t0),'%.2fMB/s'%(sz/1e6/max(1,time.time()-t0)),flush=True)
print('ALL_WEIGHTS_DONE',flush=True)
PY
grep -q ALL_WEIGHTS_DONE /workspace/weights.log && say "weights done" || say "FATAL_WEIGHTS"
ls -lh $DM $TE $VA >> $LOG 2>&1

# --- boot ComfyUI ---
say "booting ComfyUI"
pkill -f 'main.py.*8188' 2>/dev/null; sleep 2
cd $CDIR && nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 90); do sleep 5; curl -sf http://127.0.0.1:8188/object_info >/dev/null 2>&1 && { say "ComfyUI up after $((i*5))s"; break; }; done
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json 2>/dev/null || { say COMFY_DOWN; exit 1; }

# --- preflight ---
python3 - <<'PY' >> $LOG 2>&1
import json,sys
oi=json.load(open('/workspace/object_info.json'))
want='qwen_image_edit_2511_fp8mixed.safetensors'
opts=oi['UNETLoader']['input']['required']['unet_name'][0]
print('UNET_LISTED', want in opts)
need=['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','LoadImage',
      'ImageScaleToTotalPixels','TextEncodeQwenImageEditPlus','EmptySD3LatentImage',
      'KSampler','VAEDecode','SaveImage']
miss=[n for n in need if n not in oi]
print('MISSING_NODES',miss)
ok=(want in opts) and not miss
print('PREFLIGHT_OK' if ok else 'PREFLIGHT_FAIL')
PY
grep -q PREFLIGHT_OK $LOG && say "PROV2_ALL_DONE" || say "PROV2_FAILED"
