#!/bin/bash
# Susanoo & Oroki — SkyReels-V3 R2V-14B 3-beat video runner (identity-locked, 720P).
# Fresh-box path: deps + repo + weights + 3 beats. Verified CLI:
#   generate_video.py --task_type reference_to_video --model_id <r2v>
#   --ref_imgs "a,b" --duration --resolution --prompt --seed
# Keyframes come from /workspace/keyframes (gate-passing kf_1/2/3).
set -x
cd /workspace
export HF_HOME=/workspace/hf
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TOKENIZERS_PARALLELISM=false

# ---------- 1. python deps (NO flash_attn: single-GPU path does not need it) ----------
pip install -q --no-input \
  diffusers==0.34.0 transformers==4.53.2 tokenizers==0.21.4 accelerate==1.8.1 \
  ftfy==6.3.1 imageio-ffmpeg==0.5.1 omegaconf==2.3.0 kornia easydict av einops timm \
  pyloudnorm librosa moviepy==2.2.1 torchao==0.10.0 \
  "numpy<2" opencv-python-headless tqdm wget huggingface_hub hf_transfer \
  2>&1 | tail -5
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 -c "import torch,diffusers,transformers;print('torch',torch.__version__,'cuda',torch.version.cuda,'diffusers',diffusers.__version__)"

# ---------- 2. repo + repo deps ----------
[ -d SkyReels-V3 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V3
cd SkyReels-V3
python3 -m pip install -q -r requirements.txt 2>&1 | tail -5
python3 -c "import einops, timm, av; print('RENDER_DEPS_OK')" || { echo "FATAL: render deps missing"; exit 1; }
cd /workspace

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

# ---------- 4. render 3 beats from v3_jobs.json ----------
ROOT=/workspace
OUT=$ROOT/v3_out
KEYFR=$ROOT/keyframes
MODEL=$ROOT/models/r2v
JOBS=$ROOT/v3_jobs.json
mkdir -p $OUT

[ -f $JOBS ] || { echo "FATAL: no $JOBS"; exit 1; }

python3 - <<'PY' "$JOBS" "$KEYFR" "$MODEL" "$OUT"
import json, subprocess, sys, os, time, shutil
jobs, keyfr, model, out = sys.argv[1:5]
data = json.load(open(jobs))
for b in data["beats"]:
    tag = b["tag"]
    kf = os.path.join(keyfr, b.get("keyframe", tag + ".png"))
    if not os.path.exists(kf):
        raise SystemExit(f"missing keyframe {kf} for {tag}")
    cmd = [sys.executable, "/workspace/SkyReels-V3/generate_video.py",
           "--task_type", "reference_to_video",
           "--model_id", model,
           "--ref_imgs", kf,
           "--prompt", b["prompt"],
           "--duration", str(b.get("duration", 5)),
           "--resolution", b.get("resolution", "720P"),
           "--seed", str(b.get("seed", 8001)),
           "--offload"]
    print(f"[V3] {tag} refs={kf}", flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, cwd="/workspace/SkyReels-V3")
    print(f"[V3] {tag} exit={r.returncode} secs={round(time.time()-t0,1)}", flush=True)
    found = []
    for root,_,fs in os.walk("/workspace/SkyReels-V3/result"):
        for f in fs:
            if f.endswith(".mp4"): found.append(os.path.join(root,f))
    if found:
        newest = max(found, key=os.path.getmtime)
        dst = os.path.join(out, tag + "_v3.mp4")
        shutil.copy2(newest, dst)
        print(f"[V3] {tag} saved {dst}", flush=True)
print("V3_ALL_DONE", flush=True)
PY
