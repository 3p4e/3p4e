#!/bin/bash
# Package 18 keyframes on the WARM V3 instance: install ComfyUI, pull Qwen-Edit-2511, render 3 KFs.
set -uo pipefail
export LC_ALL=C HF_HOME=/workspace/hf
LOG=/workspace/susanoo_kf.log
say(){ echo "[KF $(date -u +%H:%M:%S)] $*" | tee -a $LOG; }
mkdir -p /workspace/out /workspace/hf
say "start"

CDIR=/workspace/ComfyUI
if [ ! -f $CDIR/main.py ]; then
  say "cloning ComfyUI"
  git clone -q --depth 1 https://github.com/comfyanonymous/ComfyUI $CDIR >> $LOG 2>&1 || { say FATAL_CLONE; exit 1; }
fi
say "installing ComfyUI deps"
python3 -m pip install -q --no-input -r $CDIR/requirements.txt >> $LOG 2>&1 || say "pip warn"
python3 -c "import einops,safetensors,transformers" 2>>$LOG || python3 -m pip install -q einops safetensors transformers >> $LOG 2>&1

DM=$CDIR/models/diffusion_models; TE=$CDIR/models/text_encoders; VA=$CDIR/models/vae
export DM="$DM" TE="$TE" VA="$VA"
mkdir -p $DM $TE $VA $CDIR/input

say "fetching weights (CDN ~48MB/s)"
python3 - <<'PY' 2>&1 | tee -a /workspace/susanoo_kf.log
import os, shutil
from huggingface_hub import hf_hub_download
dm = os.environ['DM']; te = os.environ['TE']; va = os.environ['VA']
stage = '/workspace/stage'; os.makedirs(stage, exist_ok=True)
jobs = [
 ('Comfy-Org/Qwen-Image-Edit_ComfyUI','split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors',dm),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors',te),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/vae/qwen_image_vae.safetensors',va),
]
for repo, fn, dest in jobs:
    name = fn.split('/')[-1]
    tgt = os.path.join(dest, name)
    if os.path.exists(tgt) and os.path.getsize(tgt) > 1000000:
        print('skip', tgt, os.path.getsize(tgt), flush=True); continue
    print('get', name, flush=True)
    p = hf_hub_download(repo_id=repo, filename=fn, local_dir=stage)
    shutil.move(p, tgt)
    print('ok', tgt, os.path.getsize(tgt), flush=True)
print('ALL_WEIGHTS_DONE', flush=True)
PY
[ -f /workspace/out/.noweights ] && { say FATAL_WEIGHTS; exit 1; }
grep -q ALL_WEIGHTS_DONE $LOG || { say FATAL_WEIGHTS_MARKER; exit 1; }
say "weights done"

cp -f /workspace/refs/Susanoo_bust.png /workspace/refs/Kushinada_bust.png $CDIR/input/ 2>/dev/null
say "refs staged"; sha256sum $CDIR/input/*.png >> $LOG 2>&1

say "starting ComfyUI"
pkill -f 'main.py.*8188' 2>/dev/null; sleep 2
cd $CDIR && nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 60); do sleep 5; curl -sf http://127.0.0.1:8188/object_info >/dev/null 2>&1 && { say "ComfyUI up $((i*5))s"; break; }; done
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json || { say COMFY_DOWN; exit 1; }
python3 - <<'PY' 2>&1 | tee -a /workspace/susanoo_kf.log
import json
need=['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','LoadImage','FluxKontextImageScale','TextEncodeQwenImageEditPlus','VAEEncode','KSampler','VAEDecode','SaveImage']
oi=json.load(open('/workspace/object_info.json'))
miss=[n for n in need if n not in oi]
print('MISSING_NODES:',miss)
print('NODE_CHECK_PASS' if not miss else 'NODE_CHECK_FAIL')
PY
grep -q NODE_CHECK_PASS /workspace/susanoo_kf.log || { say NODE_CHECK_FAILED; exit 2; }
say "node preflight pass"

say "rendering 3 keyframes"
cd /workspace
python3 /workspace/run_qwen_edit_full.py --host http://127.0.0.1:8188 \
  --jobs /workspace/kf_jobs.json --out /workspace/out --steps 50 \
  --comfy-dir $CDIR >> /workspace/susanoo_kf.log 2>&1
say "jobs exit=$?"
ls -lh /workspace/out >> $LOG 2>&1
say "KF_ALL_DONE"
