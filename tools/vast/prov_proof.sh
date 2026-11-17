#!/bin/bash
# Provision ComfyUI + Qwen-Image-Edit-2511 fp8 for the DHPF proof shot.
# Lessons baked in from instance 59361633:
#   * this image ships WITHOUT torch -> install it first, visibly (never -q)
#   * comfy_aimdo is imported by main.py but not in requirements.txt
#   * hf_hub_download dies silently -> use curl -C - with retries
set -u
exec > /workspace/prov.log 2>&1
TS() { date -u '+%H:%M:%S'; }

echo "[$(TS)] PROV START"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
df -h /workspace | tail -1

# ---------------------------------------------------------------- 1. torch
echo "[$(TS)] installing torch 2.11.0+cu128 (visible, ~2.5GB)"
python3 -m pip install --no-cache-dir --upgrade pip
python3 -m pip install --no-cache-dir \
  --index-url https://download.pytorch.org/whl/cu128 \
  torch==2.11.0 torchvision torchaudio
echo "[$(TS)] torch exit=$?"
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0))"

# ---------------------------------------------------------------- 2. ComfyUI
cd /workspace
echo "[$(TS)] cloning ComfyUI"
if [ ! -d ComfyUI ]; then
  git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git
fi
cd /workspace/ComfyUI
echo "[$(TS)] installing requirements"
python3 -m pip install --no-cache-dir -r requirements.txt
echo "[$(TS)] requirements exit=$?"
# undeclared but imported by main.py
echo "[$(TS)] installing comfy_aimdo (undeclared dependency)"
python3 -m pip install --no-cache-dir comfy_aimdo
echo "[$(TS)] comfy_aimdo exit=$?"

mkdir -p models/diffusion_models models/text_encoders models/vae input output temp user

# ---------------------------------------------------------------- 3. weights
pull() {  # url  dest  label
  local url="$1" dest="$2" label="$3"
  if [ -s "$dest" ]; then
    echo "[$(TS)] $label already present $(stat -c%s "$dest") bytes"
    return 0
  fi
  echo "[$(TS)] pulling $label"
  curl -L --retry 10 --retry-delay 5 --retry-all-errors -C - \
       --connect-timeout 30 --max-time 5400 \
       -H "Authorization: Bearer ${HF_TOKEN:-}" \
       -o "$dest" "$url"
  echo "[$(TS)] $label exit=$? size=$(stat -c%s "$dest" 2>/dev/null || echo 0)"
}

H=https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files

pull "$H/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors" \
     models/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors "edit fp8mixed UNet (~20GB)"

pull "$H/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" \
     models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors "qwen2.5-vl fp8_scaled CLIP (~9.4GB)"

pull "$H/vae/qwen_image_vae.safetensors" \
     models/vae/qwen_image_vae.safetensors "qwen image VAE"

echo "[$(TS)] weight sizes:"
ls -la models/diffusion_models models/text_encoders models/vae

# ---------------------------------------------------------------- 4. boot
echo "[$(TS)] booting ComfyUI on 8188"
cd /workspace/ComfyUI
nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfy.log 2>&1 &
sleep 25
echo "[$(TS)] comfy proc: $(pgrep -f 'main.py --listen' | head -1)"
curl -s -o /dev/null -w "[$(TS)] HTTP %{http_code}\n" http://127.0.0.1:8188/object_info/UNETLoader || echo "[$(TS)] object_info not ready"
echo "[$(TS)] tail of comfy.log:"
tail -15 /workspace/comfy.log
echo "[$(TS)] free disk:"; df -h /workspace | tail -1
echo "PROV_DONE"
