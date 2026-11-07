#!/bin/bash
# Susanoo & Oroki — render ONLY the missing beat 3 (vp_3_wedding).
# Weights + keyframes + vp_1/vp_2 clips are already on disk; this avoids re-rendering.
set -x
cd /workspace
export HF_HOME=/workspace/hf
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TOKENIZERS_PARALLELISM=false

OUT=/workspace/v3_out
KEYFR=/workspace/keyframes
MODEL=/workspace/models/r2v
JOBS=/workspace/v3_jobs.json
mkdir -p "$OUT"
[ -f "$JOBS" ] || { echo "FATAL: no $JOBS"; exit 1; }
[ -d "$MODEL" ] || { echo "FATAL: no weights at $MODEL"; exit 1; }

python3 - "$JOBS" "$KEYFR" "$MODEL" "$OUT" <<'PY'
import json, subprocess, sys, os, time, shutil
jobs, keyfr, model, out = sys.argv[1:5]
data = json.load(open(jobs))
target = "vp_3_wedding"
for b in data["beats"]:
    if b["tag"] != target:
        continue
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
           "--seed", str(b.get("seed", 8003)),
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
print("BEAT3_DONE", flush=True)
PY
