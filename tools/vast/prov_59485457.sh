#!/bin/bash
# Provision the RTX 6000Ada instance 59485457 for the DHPF proof (6 stills).
# Template puts ComfyUI at /opt/workspace-internal/ComfyUI and python in /venv/main.
# Reuses the proven curl -C - resume approach (hf_hub_download dies silently).
set -u
export LC_ALL=C.UTF-8
LOG=/workspace/prov_59485457.log
say(){ echo "[PROV $(date -u +%H:%M:%S)] $*"; }
exec >> "$LOG" 2>&1
say "START on $(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
df -h /workspace | tail -1

CDIR=/opt/workspace-internal/ComfyUI
DM="$CDIR/models/diffusion_models"
TE="$CDIR/models/text_encoders"
VA="$CDIR/models/vae"
mkdir -p "$DM" "$TE" "$VA" /workspace/hf

# token
if [ -f /workspace/.hfenv ]; then set -a; . /workspace/.hfenv; set +a; fi
if [ -z "${HF_TOKEN:-}" ]; then say "FATAL_NO_TOKEN"; exit 1; fi
say "HF token len ${#HF_TOKEN}"

fetch(){
  repo="$1"; path="$2"; dest="$3"; name="${path##*/}"; out="$dest/$name"
  url="https://huggingface.co/$repo/resolve/main/$path"
  say "GET $name"
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    curl -L --fail --connect-timeout 20 --max-time 3600 -C - \
      -H "Authorization: Bearer $HF_TOKEN" -o "$out" "$url" >> /workspace/curl_59485457.log 2>&1
    rc=$?
    sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
    say "attempt $attempt rc=$rc size=$sz"
    [ "$rc" = "0" ] && break
    [ "$rc" = "33" ] && rm -f "$out"
    sleep 5
  done
  say "DONE $name bytes=$(stat -c%s "$out" 2>/dev/null || echo 0)"
}

fetch Comfy-Org/Qwen-Image-Edit_ComfyUI \
  split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors "$DM"
fetch Comfy-Org/Qwen-Image_ComfyUI \
  split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors "$TE"
fetch Comfy-Org/Qwen-Image_ComfyUI \
  split_files/vae/qwen_image_vae.safetensors "$VA"

say "weights on disk:"
ls -lh "$DM" "$TE" "$VA"
du -sh "$DM" "$TE" "$VA"

# verify each file is non-trivial size
for f in "$DM/qwen_image_edit_2511_fp8mixed.safetensors" \
         "$TE/qwen_2.5_vl_7b_fp8_scaled.safetensors" \
         "$VA/qwen_image_vae.safetensors"; do
  s=$(stat -c%s "$f" 2>/dev/null || echo 0)
  [ "$s" -gt 1000000 ] || { say "WEIGHT_TOO_SMALL $f size=$s"; }
done

# boot ComfyUI with the venv python
say "booting ComfyUI on 8188"
pkill -f 'main.py --listen' 2>/dev/null || true
cd "$CDIR"
nohup /venv/main/bin/python main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy_59485457.log 2>&1 &
echo "$!" > /workspace/comfy.pid
say "comfy pid $(cat /workspace/comfy.pid)"

for i in $(seq 1 40); do
  code=$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8188/system_stats 2>/dev/null || echo 000)
  say "wait $i http=$code"
  [ "$code" = "200" ] && break
  sleep 3
done
curl -s -o /dev/null -w "final http=%{http_code}\n" http://127.0.0.1:8188/object_info/UNETLoader || true
say "free disk:"; df -h /workspace | tail -1
say "PROV_DONE"
