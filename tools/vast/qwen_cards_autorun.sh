#!/bin/bash
# Qwen character-card render for KORY + DD on a BARE pytorch image.
# Waits for the V3 film test to finish first so the 381 Mbps link is not split.
# Downloads ONLY Qwen-Image-Edit-2511 + text encoder + VAE (~29 GB), skipping
# the 2512 T2I checkpoint (20 GB) which cards do not need.
set -x
export LC_ALL=C
LOG=/workspace/cards.log
say(){ echo "[CARDS $(date -u +%H:%M:%S)] $*" | tee -a $LOG; }
mkdir -p /workspace/out /workspace/refs
[ -f /workspace/.hfenv ] && set -a && . /workspace/.hfenv && set +a
export HF_HUB_ENABLE_HF_TRANSFER=1

# ---------- gate: wait for the V3 render to finish ----------
say "waiting for V3 to finish before downloading (shared 381 Mbps link)"
for i in $(seq 1 360); do
  grep -q 'V3_ALL_DONE\|TEST_DONE' /workspace/out/test.log 2>/dev/null && { say "V3 finished - proceeding"; break; }
  sleep 30
done
if ! grep -q 'V3_ALL_DONE\|TEST_DONE' /workspace/out/test.log 2>/dev/null; then
  say "WARN: V3 gate timeout after 3h - proceeding anyway"
fi
say "GPU now: $(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader)"

# ---------- ComfyUI on a bare pytorch image ----------
CDIR=/workspace/ComfyUI
if [ ! -f $CDIR/main.py ]; then
  say "installing ComfyUI"
  git clone --depth 1 https://github.com/comfyanonymous/ComfyUI $CDIR >> $LOG 2>&1
  python3 -m pip install -q -r $CDIR/requirements.txt >> $LOG 2>&1
fi
DM=$CDIR/models/diffusion_models; TE=$CDIR/models/text_encoders; VA=$CDIR/models/vae
mkdir -p $DM $TE $VA $CDIR/input

say "downloading Qwen edit weights (~29 GB)"
python3 - <<'PY' 2>&1 | tee -a /workspace/cards.log
import os
from huggingface_hub import hf_hub_download
dm,te,va=os.environ['DM'],os.environ['TE'],os.environ['VA']
jobs=[
 ('Comfy-Org/Qwen-Image-Edit_ComfyUI','split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors',dm),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors',te),
 ('Comfy-Org/Qwen-Image_ComfyUI','split_files/vae/qwen_image_vae.safetensors',va),
]
for repo,f,d in jobs:
    print('get',f,flush=True)
    p=hf_hub_download(repo_id=repo,filename=f,local_dir=d)
    print('ok',p,os.path.getsize(p),flush=True)
print('CARD_WEIGHTS_DONE',flush=True)
PY

# ---------- stage reference images into ComfyUI/input ----------
for f in kory_start_1024.png dd_identity_1024.png; do
  if [ -f /workspace/refs/$f ]; then
    cp -v /workspace/refs/$f $CDIR/input/ >> $LOG 2>&1 && say "staged $f"
  else
    say "MISSING ref $f"
    exit 1
  fi
done
ls -la $CDIR/input/ | tail -6

# ---------- start ComfyUI ----------
pkill -f 'main.py.*8188' 2>/dev/null; sleep 2
cd $CDIR && nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 60); do sleep 5; curl -sf http://127.0.0.1:8188/object_info >/dev/null 2>&1 && { say "ComfyUI up after $((i*5))s"; break; }; done
curl -sf http://127.0.0.1:8188/object_info >/dev/null || { say "FATAL comfy not up"; tail -20 /workspace/comfy.log; exit 1; }

# ---------- render: KORY then DD, full 40 steps (no Lightning) ----------
for JOBS in kory_jobs.json dd_jobs.json; do
  say "rendering $JOBS"
  python3 /workspace/run_qwen_edit.py --host http://127.0.0.1:8188 \
    --jobs /workspace/jobs/$JOBS --out /workspace/out --comfy-dir $CDIR \
    --steps 40 --cfg 3.0 >> $LOG 2>&1
  say "$JOBS exit=$?"
done

cat /workspace/cards.log | tail -40
find /workspace/out -name 'kory_*' -o -name 'dd_card*' | head -20
echo "CARDS_DONE"
