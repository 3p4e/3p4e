#!/usr/bin/env bash
# Qwen-Image-Edit-2511 FULL-quality keyframe render for the 12-beat Origami fight.
# No in-instance watchdog: teardown is controlled from the host after copy-verify.
set -uo pipefail
export LC_ALL=C
export HF_HOME=/workspace/hf
LOG=/workspace/qwen_kf.log
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> $LOG; }
say "start"; mkdir -p /workspace/out /workspace/stage

CDIR=/opt/workspace-internal/ComfyUI
DM=$CDIR/models/diffusion_models; TE=$CDIR/models/text_encoders; VA=$CDIR/models/vae
mkdir -p $DM $TE $VA $CDIR/input
P=/venv/main/bin/python; [ -x $P ] || P=python3

# ---- download 3 weights FLAT into the correct model dirs (full quality, no LoRA) ----
say "fetching weights"
DM="$DM" TE="$TE" VA="$VA" $P - <<'PY' 2>&1 | tail -40 >> /workspace/qwen_kf.log
import os, shutil
from huggingface_hub import hf_hub_download
dm, te, va = os.environ['DM'], os.environ['TE'], os.environ['VA']
stage = '/workspace/stage'
os.makedirs(stage, exist_ok=True)
jobs = [
 ('Comfy-Org/Qwen-Image-Edit_ComfyUI', 'split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors', dm),
 ('Comfy-Org/Qwen-Image_ComfyUI', 'split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors', te),
 ('Comfy-Org/Qwen-Image_ComfyUI', 'split_files/vae/qwen_image_vae.safetensors', va),
]
for repo, filename, destdir in jobs:
    print('get', filename, flush=True)
    p = hf_hub_download(repo_id=repo, filename=filename, local_dir=stage)
    name = filename.split('/')[-1]
    dst = os.path.join(destdir, name)
    os.makedirs(destdir, exist_ok=True)
    shutil.move(p, dst)
    print('ok', dst, os.path.getsize(dst), flush=True)
print('ALL_WEIGHTS_DONE', flush=True)
PY
say "weights done"; ls -lh $DM $TE $VA >> $LOG

# ---- refs into ComfyUI input/ (LoadImage resolves bare filenames there) ----
cp /workspace/A_bust.png /workspace/sheet_front.png /workspace/seraph_ref.png $CDIR/input/
say "refs staged"; sha256sum $CDIR/input/A_bust.png $CDIR/input/sheet_front.png $CDIR/input/seraph_ref.png >> $LOG

# ---- start ComfyUI ----
say "starting ComfyUI"
pkill -f 'main.py' 2>/dev/null; sleep 3
cd $CDIR && nohup $P main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 60); do sleep 5; curl -sf http://127.0.0.1:8188/object_info >/dev/null 2>&1 && { say "ComfyUI up after $((i*5))s"; break; }; done
curl -sf http://127.0.0.1:8188/object_info >/dev/null || { say "COMFY NOT READY"; exit 1; }

# ---- node preflight (must be present before paying for render time) ----
curl -sf http://127.0.0.1:8188/object_info > /workspace/object_info.json
$P - <<'PY' 2>&1 >> /workspace/qwen_kf.log
import json
oi = json.load(open('/workspace/object_info.json'))
need = ['UNETLoader','ModelSamplingAuraFlow','CLIPLoader','VAELoader','LoadImage',
        'FluxKontextImageScale','TextEncodeQwenImageEditPlus','VAEEncode','KSampler','VAEDecode','SaveImage']
missing = [n for n in need if n not in oi]
print('MISSING_NODES:', missing, flush=True)
print('NODE_CHECK_PASS' if not missing else 'NODE_CHECK_FAIL', flush=True)
PY
grep -q NODE_CHECK_PASS /workspace/qwen_kf.log || { say "NODE CHECK FAILED"; exit 2; }
say "node preflight pass"

# ---- render the 12 keyframes ----
say "running keyframe jobs"
cd /workspace
$P run_qwen_edit_full.py --host http://127.0.0.1:8188 --jobs /workspace/origami_jobs.json --out /workspace/out --comfy-dir $CDIR 2>&1 | tee -a /workspace/qwen_kf.log
say "jobs exit=${PIPESTATUS[0]:-$?}"
ls -lh /workspace/out >> $LOG
say "QWEN_KF_DONE"
