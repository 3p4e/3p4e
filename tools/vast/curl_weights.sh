#!/bin/bash
# Pull DHPF weights with curl. hf_hub_download died silently twice at ~1 GB;
# curl resumes with -C -, retries, and every byte is visible on disk.
set -uo pipefail
export LC_ALL=C.UTF-8
LOG=/workspace/curl_weights.log
say(){ echo "[CURL $(date -u +%H:%M:%S)] $*"; }
exec >> $LOG 2>&1
say "start on $(hostname)"

# --- stop the stalled python worker ---
pkill -9 -f 'weights_hf.sh' 2>/dev/null || true
pkill -9 -f 'python3 -' 2>/dev/null || true
sleep 2
say "killed stalled workers"

# --- token ---
if [ -f /workspace/.hfenv ]; then set -a; . /workspace/.hfenv; set +a; fi
if [ -z "${HF_TOKEN:-}" ]; then say "FATAL_NO_TOKEN"; exit 1; fi
say "token len ${#HF_TOKEN}"

CDIR=/workspace/ComfyUI
DM=$CDIR/models/diffusion_models
TE=$CDIR/models/text_encoders
VA=$CDIR/models/vae
mkdir -p "$DM" "$TE" "$VA"

fetch(){
  repo="$1"; path="$2"; dest="$3"; name="${path##*/}"; out="$dest/$name"
  url="https://huggingface.co/$repo/resolve/main/$path"
  say "GET $name"
  # resume if partial exists, retry hard, no silent thread death
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    curl -L --fail --retry 0 --connect-timeout 20 --max-time 3600 \
      -C - -H "Authorization: Bearer $HF_TOKEN" \
      -o "$out" "$url" >> /workspace/curl_progress.log 2>&1
    rc=$?
    sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
    say "attempt $attempt rc=$rc size=$sz"
    [ "$rc" = "0" ] && break
    # 33 = server does not support resume; restart clean
    if [ "$rc" = "33" ]; then say "resume unsupported, restarting"; rm -f "$out"; fi
    sleep 5
  done
  sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
  say "DONE $name bytes=$sz"
}

fetch Comfy-Org/Qwen-Image-Edit_ComfyUI \
  split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors "$DM"
fetch Comfy-Org/Qwen-Image_ComfyUI \
  split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors "$TE"
fetch Comfy-Org/Qwen-Image_ComfyUI \
  split_files/vae/qwen_image_vae.safetensors "$VA"

say "SUMMARY"
ls -lh "$DM" "$TE" "$VA" >> $LOG 2>&1
du -sh "$DM" "$TE" "$VA" >> $LOG 2>&1
say "CURL_WEIGHTS_ALL_DONE"
