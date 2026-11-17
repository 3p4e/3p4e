#!/usr/bin/env bash
set -u
B=https://huggingface.co/Comfy-Org/Wan-2.1/resolve/main/split_files
TE=/workspace/ComfyUI/models/text_encoders
VA=/workspace/ComfyUI/models/vae
mkdir -p $TE $VA
get() {
  echo "[$(date -u +%H:%M:%S)] START $3"
  wget --tries=20 --timeout=30 --waitretry=3 --progress=dot:giga -c -O "$2" "$1"
  echo "[$(date -u +%H:%M:%S)] DONE $3 rc=$? bytes=$(stat -c%s "$2" 2>/dev/null)"
}
get "$B/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors" "$TE/umt5_xxl_fp8_e4m3fn_scaled.safetensors" umt5_fp8
get "$B/vae/wan_2.1_vae.safetensors" "$VA/wan_2.1_vae.safetensors" vae
chown -R root:root $TE $VA 2>/dev/null
echo "[$(date -u +%H:%M:%S)] ALL_DONE"
df -BG --output=avail /workspace | tail -1
