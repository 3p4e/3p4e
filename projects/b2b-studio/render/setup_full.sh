#!/bin/bash
# Box setup for the ABRACADABRA v3 LTX-2.5 batch. Idempotent. Logs to /workspace/setup.log
set -x
cd /workspace
export DEBIAN_FRONTEND=noninteractive
which ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg) 
which git >/dev/null || apt-get install -y -qq git
[ -d ComfyUI ] || git clone --depth 1 https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
[ -d custom_nodes/ComfyUI-LTXVideo ] || git clone --depth 1 https://github.com/Lightricks/ComfyUI-LTXVideo custom_nodes/ComfyUI-LTXVideo
# torch: keep the image's working build; install the doc-verified 2.8.0+cu126 only if missing
python3 -c 'import torch; assert torch.cuda.is_available()' 2>/dev/null || pip install -q torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu126
python3 -c 'import torch; print("TORCH", torch.__version__, torch.cuda.is_available())'
# never let pip replace the box's working torch (doc 42/64): constrain to what is installed
pip freeze 2>/dev/null | grep -iE '^(torch|torchvision|torchaudio)==' > /workspace/torch_pin.txt
cat /workspace/torch_pin.txt
pip install -q -c /workspace/torch_pin.txt -r requirements.txt
pip install -q -c /workspace/torch_pin.txt -r custom_nodes/ComfyUI-LTXVideo/requirements.txt
pip install -q -U "huggingface_hub[hf_transfer]"
mkdir -p /workspace/hf models/diffusion_models models/checkpoints models/text_encoders models/vae
command -v aria2c >/dev/null || apt-get install -y -qq aria2 >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq aria2)
R=https://huggingface.co/comfyicu/LTX-2.5/resolve/main
mkdir -p hf/diffusion_models hf/text_encoders hf/vae
for f in diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors vae/ltx-2.5-video-vae-bf16.safetensors; do
  for t in 1 2 3 4 5 6; do [ -f /workspace/hf/$f ] && [ ! -f /workspace/hf/$f.aria2 ] && break; aria2c -q -x 16 -s 16 -k 20M --file-allocation=none -c -d /workspace/hf/$(dirname $f) -o $(basename $f) "$R/$f"; done
  echo "GOT $f $(stat -c %s /workspace/hf/$f)"
done
cd /workspace/ComfyUI
ln -sf /workspace/hf/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors models/diffusion_models/
ln -sf /workspace/hf/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors models/text_encoders/
ln -sf /workspace/hf/vae/ltx-2.5-video-vae-bf16.safetensors models/vae/
pgrep -f "main.py --listen" >/dev/null || nohup python3 main.py --listen 127.0.0.1 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 90); do curl -sf http://127.0.0.1:8188/system_stats >/dev/null && break; sleep 5; done
echo SETUP_DONE
