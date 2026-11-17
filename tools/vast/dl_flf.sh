#!/usr/bin/env bash
set -u
B=https://huggingface.co/Comfy-Org/Wan-2.1/resolve/main/split_files
DM=/workspace/ComfyUI/models/diffusion_models
TE=/workspace/ComfyUI/models/text_encoders
VA=/workspace/ComfyUI/models/vae
mkdir -p $DM $TE $VA
get() { # url dest label
  local url=$1 dest=$2 label=$3
  echo "[$(date -u +%H:%M:%S)] START $label"
  curl -L -C - --retry 12 --retry-delay 5 --retry-all-errors \
       --connect-timeout 30 --speed-time 120 --speed-limit 10000 \
       -o "$dest" "$url" 2>/dev/null
  echo "[$(date -u +%H:%M:%S)] DONE $label rc=$? bytes=$(stat -c%s "$dest" 2>/dev/null)"
}
get "$B/diffusion_models/wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors" "$DM/wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors" unet_fp8
get "$B/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors" "$TE/umt5_xxl_fp8_e4m3fn_scaled.safetensors" umt5_fp8
get "$B/vae/wan_2.1_vae.safetensors" "$VA/wan_2.1_vae.safetensors" vae
echo "[$(date -u +%H:%M:%S)] ALL_DOWNLOADS_DONE"
df -BG --output=avail /workspace | tail -1
