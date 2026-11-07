#!/usr/bin/env bash
set -u
B=https://huggingface.co/Comfy-Org/Wan-2.1/resolve/main/split_files
DM=/workspace/ComfyUI/models/diffusion_models
TE=/workspace/ComfyUI/models/text_encoders
VA=/workspace/ComfyUI/models/vae
mkdir -p $DM $TE $VA
get() {
  local url=$1 dest=$2 label=$3
  echo "[$(date -u +%H:%M:%S)] START $label"
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    curl -L -C - --retry 6 --retry-delay 3 --retry-all-errors \
         --connect-timeout 20 --speed-time 30 --speed-limit 40000 \
         --http1.1 -o "$dest" "$url"
    rc=$?
    echo "[$(date -u +%H:%M:%S)] attempt=$attempt rc=$rc bytes=$(stat -c%s "$dest" 2>/dev/null)"
    [ $rc -eq 0 ] && break
    sleep 3
  done
  echo "[$(date -u +%H:%M:%S)] DONE $label bytes=$(stat -c%s "$dest" 2>/dev/null)"
}
get "$B/diffusion_models/wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors" "$DM/wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors" unet_fp8
get "$B/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors" "$TE/umt5_xxl_fp8_e4m3fn_scaled.safetensors" umt5_fp8
get "$B/vae/wan_2.1_vae.safetensors" "$VA/wan_2.1_vae.safetensors" vae
echo "[$(date -u +%H:%M:%S)] ALL_DOWNLOADS_DONE"
df -BG --output=avail /workspace | tail -1
