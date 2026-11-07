#!/bin/bash
# Pull the DHPF weights with HF authentication. Unauthenticated pulls stall
# at ~12 KB because the Hub throttles anonymous clients.
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/weights_hf.log
say(){ echo "[WHF $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

# --- auth ---
if [ -f /workspace/.hfenv ]; then
  set -a; . /workspace/.hfenv; set +a
fi
if [ -n "${HF_TOKEN:-}" ]; then
  export HF_TOKEN HUGGING_FACE_HUB_TOKEN="$HF_TOKEN"
  say "HF token present (len ${#HF_TOKEN})"
else
  say "WARN no HF token; anonymous download may throttle"
fi
export HF_HOME=/workspace/hf

# --- stop anything stalled ---
pkill -9 -f 'prov2.sh' 2>/dev/null || true
pkill -9 -f 'hf_hub_download' 2>/dev/null || true
pkill -9 -f 'weights' 2>/dev/null || true
sleep 2
say "cleared stalled workers"

# --- dirs ---
CDIR=/workspace/ComfyUI
DM=$CDIR/models/diffusion_models
TE=$CDIR/models/text_encoders
VA=$CDIR/models/vae
mkdir -p "$DM" "$TE" "$VA" /workspace/stage
say "targets: $DM | $TE | $VA"

# --- pull ---
python3 - "$DM" "$TE" "$VA" <<'PY'
import os, shutil, sys, time
from huggingface_hub import hf_hub_download

dm, te, va = sys.argv[1], sys.argv[2], sys.argv[3]
stage = '/workspace/stage'
os.makedirs(stage, exist_ok=True)

token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN')
print('token_present', bool(token), flush=True)

jobs = [
 ('Comfy-Org/Qwen-Image-Edit_ComfyUI',
  'split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors', dm),
 ('Comfy-Org/Qwen-Image_ComfyUI',
  'split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors', te),
 ('Comfy-Org/Qwen-Image_ComfyUI',
  'split_files/vae/qwen_image_vae.safetensors', va),
]

for repo, fn, dest in jobs:
    name = fn.split('/')[-1]
    tgt = os.path.join(dest, name)
    if os.path.exists(tgt) and os.path.getsize(tgt) > 1_000_000:
        print('skip', name, os.path.getsize(tgt), flush=True)
        continue
    t0 = time.time()
    print('get', name, flush=True)
    try:
        p = hf_hub_download(repo_id=repo, filename=fn, local_dir=stage,
                            token=token, resume_download=True)
    except TypeError:
        p = hf_hub_download(repo_id=repo, filename=fn, local_dir=stage, token=token)
    os.makedirs(dest, exist_ok=True)
    shutil.move(p, tgt)
    dt = max(1.0, time.time() - t0)
    sz = os.path.getsize(tgt)
    print('ok', name, sz, '%.1fs' % dt, '%.2fMB/s' % (sz / 1e6 / dt), flush=True)

print('ALL_WEIGHTS_DONE', flush=True)
PY
RC=$?
say "weights exit=$RC"
if grep -q ALL_WEIGHTS_DONE /workspace/weights_hf.log; then
  say "WEIGHTS_OK"
else
  say "WEIGHTS_FAIL"
  exit 1
fi

ls -lh "$DM" "$TE" "$VA" >> $LOG 2>&1
du -sh "$DM" "$TE" "$VA" >> $LOG 2>&1
say "WEIGHTS_ALL_DONE"
