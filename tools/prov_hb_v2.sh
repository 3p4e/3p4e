#!/bin/bash
# prov_hb_v2.sh — Hollow Bloom v2 box provisioning (48GB). Run ON the vast.ai box.
# Sources: docs 55/56/57/58. Idempotent; safe to re-run.
set -e
cd /workspace
echo "== [1/6] ComfyUI (use template's pre-installed if present — KB §20: never pip-reinstall torch) =="
if [ ! -d ComfyUI ]; then git clone --depth 1 https://github.com/comfyanonymous/ComfyUI; fi
cd ComfyUI && pip install -r requirements.txt -q && cd /workspace

echo "== [2/6] Wan 2.2 Fun Control weights (doc 56 exact filenames) =="
mkdir -p ComfyUI/models/{diffusion_models,loras,text_encoders,vae}
HF_WAN=Wan-AI/Wan2.2-Fun-A14B-Control   # verify repo id at pull time
for f in wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors; do
  [ -s ComfyUI/models/diffusion_models/$f ] || huggingface-cli download $HF_WAN $f --local-dir ComfyUI/models/diffusion_models
 done
for f in wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors; do
  [ -s ComfyUI/models/loras/$f ] || huggingface-cli download $HF_WAN $f --local-dir ComfyUI/models/loras
 done
[ -s ComfyUI/models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors ] || huggingface-cli download $HF_WAN umt5_xxl_fp8_e4m3fn_scaled.safetensors --local-dir ComfyUI/models/text_encoders
[ -s ComfyUI/models/vae/wan_2.1_vae.safetensors ] || huggingface-cli download $HF_WAN wan_2.1_vae.safetensors --local-dir ComfyUI/models/vae

echo "== [3/6] Control-video tooling: DWPose aux + Video Depth Anything (doc 55) =="
cd ComfyUI/custom_nodes
git clone --depth 1 https://github.com/Fannovel16/comfyui_controlnet_aux 2>/dev/null || true
git clone --depth 1 https://github.com/yuvraj108c/ComfyUI-Video-Depth-Anything 2>/dev/null || true
for d in comfyui_controlnet_aux ComfyUI-Video-Depth-Anything; do
  [ -d $d ] && (cd $d && pip install -r requirements.txt -q)
done
cd /workspace/ComfyUI

echo "== [4/6] Gate dependencies (doc 57 Q7) =="
pip install -q opencv-contrib-python open_clip_torch insightface 2>/dev/null || pip install -q opencv-contrib-python open_clip_torch

echo "== [5/6] LTX-2.3 fallback (KB §22 recipe — skip if disk tight; only needed for CU escalation) =="
echo "   (distilled checkpoint + gemma-3-12b-it + LoRA — pull on demand per KB §22)"

echo "== [6/6] Verify =="
python3 -c "import cv2, torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), 'vram GB', round(torch.cuda.get_device_properties(0).total_memory/2**30,1))"
ls ComfyUI/models/diffusion_models/ ComfyUI/models/loras/
echo "PROV_DONE"
