#!/bin/bash
# SkyReels-V3 R2V-14B 12-beat Origami fight runner (identity-locked, 720P).
# Replaces the V2-DF path. Verified CLI (generate_video.py, SkyworkAI/SkyReels-V3):
#   --task_type reference_to_video --ref_imgs "a,b" --duration --resolution --prompt --seed
# Ref rule per beat: hero -> A_bust.png, monster -> seraph_ref.png (faceless), clash -> both.
set -x
cd /workspace
export HF_HOME=/workspace/hf

# ---------- deps (required: einops, timm, av; repo requirements is authoritative) ----------
pip install -q --no-input einops timm av easydict omegaconf kornia ftfy 2>&1 | tail -3
[ -d SkyReels-V3 ] || git clone --depth 1 https://github.com/SkyworkAI/SkyReels-V3
( cd SkyReels-V3 && python3 -m pip install -q -r requirements.txt 2>&1 | tail -5 )
python3 -c "import einops, timm, av; print('RENDER_DEPS_OK')" || { echo "FATAL: render deps missing"; exit 1; }

ROOT=/workspace
OUT=$ROOT/v3_out
KEYFR=$ROOT/origami_keyframes
REFS=$ROOT/refs
MODEL=$ROOT/models/r2v
JOBS=$ROOT/v3_jobs.json
mkdir -p $OUT

[ -f $JOBS ] || { echo "FATAL: no $JOBS"; exit 1; }
[ -x /usr/sbin/sshd ] || true

python3 - <<'PY' "$JOBS" "$KEYFR" "$REFS" "$MODEL" "$OUT"
import json, subprocess, sys, os, time
jobs, keyfr, refs, model, out = sys.argv[1:6]
data = json.load(open(jobs))
hero = os.path.join(refs, "A_bust.png")
monster = os.path.join(refs, "seraph_ref.png")
for b in data["beats"]:
    tag = b["tag"]
    # resolve reference images: replaceable tokens
    wanted = b.get("refs", "hero")
    imgs = []
    for r in wanted.split("+"):
        r = r.strip()
        if r == "hero": imgs.append(hero)
        elif r == "monster": imgs.append(monster)
        elif r == "keyframe":
            kf = os.path.join(keyfr, b.get("keyframe", tag + ".png"))
            imgs.append(kf)
        elif os.path.exists(r): imgs.append(r)
    for p in imgs:
        if not os.path.exists(p):
            raise SystemExit(f"missing ref {p} for {tag}")
    cmd = [sys.executable, "/workspace/SkyReels-V3/generate_video.py",
           "--task_type", "reference_to_video",
           "--model_id", model,
           "--ref_imgs", ",".join(imgs),
           "--prompt", b["prompt"],
           "--duration", str(b.get("duration", 5)),
           "--resolution", b.get("resolution", "720P"),
           "--seed", str(b.get("seed", 808)),
           "--offload"]
    print(f"[V3] {tag} refs={','.join(imgs)}", flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, cwd="/workspace/SkyReels-V3")
    print(f"[V3] {tag} exit={r.returncode} secs={round(time.time()-t0,1)}", flush=True)
    # collect newest mp4 for this beat
    os.makedirs(out, exist_ok=True)
    found = []
    for root,_,fs in os.walk("/workspace/SkyReels-V3/result"):
        for f in fs:
            if f.endswith(".mp4"): found.append(os.path.join(root,f))
    if found:
        newest = max(found, key=os.path.getmtime)
        dst = os.path.join(out, tag + "_v3.mp4")
        import shutil; shutil.copy2(newest, dst)
        print(f"[V3] {tag} saved {dst}", flush=True)
print("V3_ALL_DONE", flush=True)
PY
