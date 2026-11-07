#!/bin/bash
# Provision ComfyUI + Qwen-Image T2I (2512) on the bare RTX PRO 5000 box,
# then render the 4 composable SUIT cards (head-covered, zero faces) at full 50-step quality.
# No in-instance watchdog: teardown is controlled from the host after copy-verify.
set -uo pipefail
export LC_ALL=C HF_HOME=/workspace/hf
LOG=/workspace/suits.log
say(){ echo "[SUITS $(date -u +%H:%M:%S)] $*" | tee -a $LOG; }
mkdir -p /workspace/out /workspace/hf
say "start on $(hostname)"

# --- ComfyUI ---
CDIR=/workspace/ComfyUI
if [ ! -f $CDIR/main.py ]; then
  say "cloning ComfyUI"
  git clone -q --depth 1 https://github.com/comfyanonymous/ComfyUI $CDIR >> $LOG 2>&1 || { say FATAL_CLONE; exit 1; }
fi
say "installing ComfyUI deps"
python3 -m pip install -q --no-input -r $CDIR/requirements.txt >> $LOG 2>&1 \
  || python3 -m pip install -q --no-input --break-system-packages -r $CDIR/requirements.txt >> $LOG 2>&1 \
  || say "pip warn (continuing)"
python3 -c "import einops,safetensors,transformers,torch" 2>>$LOG \
  || python3 -m pip install -q --break-system-packages einops safetensors transformers >> $LOG 2>&1
python3 -c "import einops,safetensors,transformers,torch" 2>>$LOG || { say FATAL_DEPS; exit 1; }
say "deps ok"

# --- weights: T2I 2512 fp8 + clip fp8 scaled + vae ---
DM=$CDIR/models/diffusion_models; TE=$CDIR/models/text_encoders; VA=$CDIR/models/vae
mkdir -p $DM $TE $VA
export DM="$DM" TE="$TE" VA="$VA"
say "fetching weights (~18 GB)"
python3 - <<'PY' 2>&1 | tee -a /workspace/suits.log
import os, shutil
from huggingface_hub import hf_hub_download
dm = os.environ['DM']; te = os.environ['TE']; va = os.environ['VA']
stage = '/workspace/stage'; os.makedirs(stage, exist_ok=True)
jobs = [
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors',dm),
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
    os.makedirs(dest, exist_ok=True)
    shutil.move(p, tgt)
    print('ok', tgt, os.path.getsize(tgt), flush=True)
print('ALL_WEIGHTS_DONE', flush=True)
PY
grep -q ALL_WEIGHTS_DONE $LOG || { say FATAL_WEIGHTS; exit 1; }
say "weights done"; ls -lh $DM $TE $VA >> $LOG

# --- start ComfyUI ---
say "starting ComfyUI"
pkill -f 'main.py.*8188' 2>/dev/null; sleep 2
cd $CDIR && nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 60); do sleep 5; curl -sf http://127.0.0.1:8188/object_info >/dev/null 2>&1 && { say "ComfyUI up after $((i*5))s"; break; }; done
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json || { say COMFY_DOWN; exit 1; }

# --- node preflight (T2I set) ---
python3 - <<'PY' 2>&1 | tee -a /workspace/suits.log
import json
need=['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','CLIPTextEncode','EmptySD3LatentImage','KSampler','VAEDecode','SaveImage']
oi=json.load(open('/workspace/object_info.json'))
miss=[n for n in need if n not in oi]
print('MISSING_NODES:',miss)
print('NODE_CHECK_PASS' if not miss else 'NODE_CHECK_FAIL')
PY
grep -q NODE_CHECK_PASS /workspace/suits.log || { say NODE_CHECK_FAILED; exit 2; }
say "node preflight pass"

# --- render the 4 suit cards ---
say "rendering 4 suit cards"
cd /workspace
python3 /workspace/run_qwen_t2i.py --host http://127.0.0.1:8188 \
  --jobs /workspace/suit_jobs.json --out /workspace/out \
  --comfy-dir $CDIR >> /workspace/suits.log 2>&1
say "jobs exit=$?"
ls -lh /workspace/out >> $LOG 2>&1
say "SUITS_ALL_DONE"
