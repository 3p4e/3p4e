#!/bin/bash
# SkyReels-V3 R2V single-clip test. Runs on the rented instance.
set -x
cd /workspace
export HF_HOME=/workspace/hf
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TOKENIZERS_PARALLELISM=false

# ---------- 1. python deps (NO flash_attn: single-GPU path does not need it) ----------
pip install -q --no-input \
  diffusers==0.34.0 transformers==4.53.2 tokenizers==0.21.4 accelerate==1.8.1 \
  ftfy==6.3.1 imageio-ffmpeg==0.5.1 omegaconf==2.3.0 kornia easydict \
  pyloudnorm librosa moviepy==2.2.1 torchao==0.10.0 \
  "numpy<2" opencv-python-headless tqdm wget huggingface_hub hf_transfer \
  2>&1 | tail -5
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 -c "import torch,diffusers,transformers;print('torch',torch.__version__,'cuda',torch.version.cuda,'diffusers',diffusers.__version__)"

# ---------- 2. repo ----------
[ -d SkyReels-V3 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V3
cd SkyReels-V3

# ---------- 3. weights (51.83 GB) ----------
echo "DOWNLOAD_START $(date -u +%H:%M:%S)"
python3 - <<'PY'
from huggingface_hub import snapshot_download
p = snapshot_download("Skywork/SkyReels-V3-R2V-14B",
                      local_dir="/workspace/models/r2v",
                      max_workers=8)
print("WEIGHTS_OK", p)
PY
echo "DOWNLOAD_END $(date -u +%H:%M:%S)"

# ---------- 4. ONE test clip ----------
REF=$(ls /workspace/refs/*.png | head -1)
echo "REF=$REF"
echo "RENDER_START $(date -u +%H:%M:%S)"
timeout 3000 python3 generate_video.py \
  --task_type reference_to_video \
  --model_id /workspace/models/r2v \
  --ref_imgs "$REF" \
  --prompt "A lone knight in weathered silver plate armour and a deep crimson cloak stands on a black basalt ridge at dusk. His helm is open at the face, revealing a scarred middle-aged man with grey stubble and exhausted eyes. Ash falls through the air around him. He turns his head slowly toward the camera, jaw set, breath visible in the cold. Cinematic anamorphic lens, low warm rim light from a dying sun, deep shadow, volumetric ash, shallow depth of field, 35mm film grain." \
  --duration 5 \
  --resolution 720P \
  --offload \
  2>&1 | tee /workspace/out/render.log
echo "RENDER_END $(date -u +%H:%M:%S)"

# ---------- 5. collect output ----------
find /workspace -name '*.mp4' -newermt '-40 minutes' -not -path '*/hf/*' -exec cp -v {} /workspace/out/ \;
ls -la /workspace/out/
echo "ALL_DONE"
