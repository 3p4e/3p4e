# Builds the LTX 2.5 render bundle for render/ltx_batch.py: jobs.json + kf/ (start keyframes) -> fv2_bundle.tgz.
# One job per shot: 1280x704, 121 frames (5 s at 24 fps), 8 steps, CFG 1, start-frame strength from the shot (default 0.75).
import os, sys, json, hashlib, tarfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from films import FILMS, SHOT_STYLE, NEGATIVE
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KF = f"{S}/fv2/kf"
# usage: make_bundle.py <name> [film_id ...]  (keyframes that do not exist yet are left out; ltx_batch.py --loop waits for them)
NAME = sys.argv[1] if len(sys.argv) > 1 else "all"; ONLY = set(sys.argv[2:]); B = f"{S}/fv2/bundle_{NAME}"
shutil.rmtree(B, ignore_errors=True); os.makedirs(f"{B}/kf")
jobs = []
for f in FILMS:
    if ONLY and f["id"] not in ONLY: continue
    for sh in f["shot_defs"]:
        src = f"{KF}/{sh['id']}.png"
        if os.path.exists(src): shutil.copy(src, f"{B}/kf/{sh['id']}.png")
        else: print("keyframe not ready yet:", sh["id"])
        seed = int(hashlib.sha1(sh["id"].encode()).hexdigest()[:6], 16) % 100000
        jobs.append({"id": sh["id"], "start": f"{sh['id']}.png", "w": 1280, "h": 704, "frames": 121, "seed": seed,
                     "strength": sh.get("strength", 0.75), "prompt": sh["motion"] + " " + SHOT_STYLE})
json.dump({"fps": 24, "steps": 8, "cfg": 1.0, "strength": 0.75, "negative": NEGATIVE, "jobs": jobs}, open(f"{B}/jobs.json", "w"), indent=1, ensure_ascii=False)
T = f"{S}/fv2/fv2_bundle_{NAME}.tgz"
with tarfile.open(T, "w:gz") as t: t.add(B, arcname=".")
print("BUNDLE", NAME, len(jobs), "jobs", os.path.getsize(T))
