#!/bin/bash
# Susanoo & Oroki — SkyReels-V3 phase 2 (no flash_attn).
# Single-GPU reference_to_video does NOT need flash_attn; building it from source
# idles the GPU 30-60 min. This runner cleans strays, installs filtered deps,
# downloads weights, renders the 3 beats, and is idempotent-safe to relaunch.
set -x
cd /workspace
export HF_HOME=/workspace/hf
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TOKENIZERS_PARALLELISM=false
export HF_HUB_ENABLE_HF_TRANSFER=1

# ---------- 0. kill any stray source build (bracket tricks: cannot self-match) ----------
pkill -9 -f '[n]vcc' 2>/dev/null
pkill -9 -f '[f]lash_attn' 2>/dev/null
pkill -9 -f '[p]ip install' 2>/dev/null
pkill -9 -f '[s]usanoo_v3_autorun' 2>/dev/null
sleep 3

# ---------- 1. filtered requirements (NO flash_attn) ----------
[ -d /workspace/SkyReels-V3 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V3
cd /workspace/SkyReels-V3
grep -v -i '^flash_attn' requirements.txt > /workspace/requirements_nofa.txt
echo "filtered_requirements_lines=$(wc -l < /workspace/requirements_nofa.txt)"
python3 -m pip install -q -r /workspace/requirements_nofa.txt 2>&1 | tail -5
python3 -c "import einops, timm, av; print('RENDER_DEPS_OK')" || { echo "FATAL: render deps missing"; exit 1; }
cd /workspace

# ---------- 2. weights (51.83 GB) ----------
echo "DOWNLOAD_START $(date -u +%H:%M:%S)"
python3 - <<'PY'
from huggingface_hub import snapshot_download
p = snapshot_download("Skywork/SkyReels-V3-R2V-14B",
                      local_dir="/workspace/models/r2v",
                      max_workers=8)
print("WEIGHTS_OK", p)
PY
echo "DOWNLOAD_END $(date -u +%H:%M:%S)"

# ---------- 3. render 3 beats from v3_jobs.json ----------
OUT=/workspace/v3_out
KEYFR=/workspace/keyframes
MODEL=/workspace/models/r2v
JOBS=/workspace/v3_jobs.json
mkdir -p "$OUT"

[ -f "$JOBS" ] || { echo "FATAL: no $JOBS"; exit 1; }

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
