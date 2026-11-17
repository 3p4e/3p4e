#!/bin/bash
# SkyReels-V3 R2V-14B single-clip FACELESS de-risk test.
# Goal: prove V3 does NOT paint a face onto the blank-mask seraph when seeded ONLY
# with seraph_ref.png (faceless). This is the failure V2 could not guard against.
set -x
cd /workspace
export HF_HOME=/workspace/hf
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TOKENIZERS_PARALLELISM=false
[ -f /workspace/.hfenv ] && set -a && . /workspace/.hfenv && set +a
mkdir -p /workspace/refs /workspace/out

pip install -q --no-input \
  diffusers==0.34.0 transformers==4.53.2 tokenizers==0.21.4 accelerate==1.8.1 \
  ftfy==6.3.1 imageio-ffmpeg==0.5.1 omegaconf==2.3.0 kornia easydict \
  pyloudnorm librosa moviepy==2.2.1 torchao==0.10.0 \
  "numpy<2" opencv-python-headless tqdm wget huggingface_hub hf_transfer \
  einops timm easydict 2>&1 | tail -5
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 -c "import torch,diffusers,transformers;print('torch',torch.__version__,'cuda',torch.version.cuda)"

[ -d SkyReels-V3 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V3
cd SkyReels-V3

# repo requirements are the authoritative dep list
python3 -m pip install -q -r requirements.txt 2>&1 | tail -5
python3 -c "import einops, timm; print(\"RENDER_DEPS_OK\")"

echo "DOWNLOAD_START $(date -u +%H:%M:%S)"
python3 - <<'PY'
from huggingface_hub import snapshot_download
p = snapshot_download("Skywork/SkyReels-V3-R2V-14B", local_dir="/workspace/models/r2v", max_workers=8)
print("WEIGHTS_OK", p)
PY
echo "DOWNLOAD_END $(date -u +%H:%M:%S)"

REF=/workspace/refs/seraph_ref.png
[ -f "$REF" ] || { echo "FATAL: missing seraph_ref.png"; exit 1; }
ls -la "$REF"

echo "RENDER_START $(date -u +%H:%M:%S)"
timeout 3000 python3 generate_video.py \
  --task_type reference_to_video \
  --model_id /workspace/models/r2v \
  --ref_imgs "$REF" \
  --prompt "The reference image shows a colossal seraph built from folded parchment, six ragged wings dripping glossy black goo, its head a blank folded paper mask weeping black, looming in a starless void over a wide black mirror. The goo keeps dripping in long slow strands and the pooled mirror ripples; drifting parchment pages float past its wings. Camera: low-angle wide shot, very slow push-in. Its blank faceless mask and six wings stay fixed. No human face appears." \
  --duration 5 \
  --resolution 720P \
  --seed 800 \
  --offload \
  2>&1 | tee /workspace/out/render.log
echo "RENDER_END $(date -u +%H:%M:%S)"

find /workspace -name '*.mp4' -newermt '-40 minutes' -not -path '*/hf/*' -exec cp -v {} /workspace/out/ \;
ls -la /workspace/out/
echo "TEST_DONE"
