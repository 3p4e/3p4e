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
python3 - <<'PY'
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import hf_hub_download
for f in ["diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors",
          "text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors",
          "vae/ltx-2.5-video-vae-bf16.safetensors"]:
    p = hf_hub_download("comfyicu/LTX-2.5", f, local_dir="/workspace/hf")
    print("GOT", p, os.path.getsize(p), flush=True)
PY
ln -sf /workspace/hf/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors models/diffusion_models/
ln -sf /workspace/hf/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors models/checkpoints/
ln -sf /workspace/hf/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors models/text_encoders/
ln -sf /workspace/hf/vae/ltx-2.5-video-vae-bf16.safetensors models/vae/
ls -la /workspace/hf/*/ 
pgrep -f "main.py --listen" >/dev/null || nohup python3 main.py --listen 127.0.0.1 --port 8188 > /workspace/comfy.log 2>&1 &
for i in $(seq 1 90); do curl -sf http://127.0.0.1:8188/system_stats >/dev/null && break; sleep 5; done
curl -s http://127.0.0.1:8188/system_stats | head -c 400; echo
echo SETUP_DONE
