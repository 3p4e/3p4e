# Builds the LTX 2.5 render bundle for render/ltx_batch.py: jobs.json + kf/ (start keyframes) -> fv2_bundle.tgz.
# One job per shot: 1280x704, 121 frames (5 s at 24 fps), 8 steps, CFG 1, start-frame strength from the shot (default 0.75).
import os, sys, json, hashlib, tarfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from films import FILMS, SHOT_STYLE, NEGATIVE
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KF = f"{S}/fv2/kf"; B = f"{S}/fv2/bundle"
shutil.rmtree(B, ignore_errors=True); os.makedirs(f"{B}/kf")
jobs = []
for f in FILMS:
    for sh in f["shot_defs"]:
        src = f"{KF}/{sh['id']}.png"
        if not os.path.exists(src): sys.exit(f"missing keyframe {src}")
        shutil.copy(src, f"{B}/kf/{sh['id']}.png")
        seed = int(hashlib.sha1(sh["id"].encode()).hexdigest()[:6], 16) % 100000
        jobs.append({"id": sh["id"], "start": f"{sh['id']}.png", "w": 1280, "h": 704, "frames": 121, "seed": seed,
                     "strength": sh.get("strength", 0.75), "prompt": sh["motion"] + " " + SHOT_STYLE})
json.dump({"fps": 24, "steps": 8, "cfg": 1.0, "strength": 0.75, "negative": NEGATIVE, "jobs": jobs}, open(f"{B}/jobs.json", "w"), indent=1, ensure_ascii=False)
with tarfile.open(f"{S}/fv2/fv2_bundle.tgz", "w:gz") as t: t.add(B, arcname=".")
print("BUNDLE", len(jobs), "jobs", os.path.getsize(f"{S}/fv2/fv2_bundle.tgz"))
