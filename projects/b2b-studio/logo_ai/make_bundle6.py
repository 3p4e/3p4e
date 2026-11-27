# LTX jobs for logo films round 6 (scenes6.py): start -> end keyframe, 5 s, 1280x704. Writes /dev/shm/vall/b6/{kf/*.png, logo6_jobs.json,
# only6} and /dev/shm/vall/b6.tgz; on the box the jobs are merged into v3bundle/jobs.json and rendered ahead of the remaining queue.
import os, sys, json, hashlib, shutil, tarfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from scenes6 import S6
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; K = f"{S}/logo_ai/kf6"; B = "/dev/shm/vall/b6"
STY = " Photorealistic premium commercial cinematography, crisp detail, the logo keeps its exact shape at the end, no text."
def seed(x): return int(hashlib.sha1(x.encode()).hexdigest()[:6], 16) % 100000
ok = sys.argv[1:] or [s[0] for s in S6]          # only the scenes that passed keyframe QC
shutil.rmtree(B, ignore_errors=True); os.makedirs(f"{B}/kf")
jobs = []
for sid, scene, empty, motion, style in S6:
    if sid not in ok: continue
    for k in "ab": shutil.copy(f"{K}/{sid}_{k}.png", f"{B}/kf/{sid}_{k}.png")
    jobs.append({"id": "logo_" + sid, "w": 1280, "h": 704, "frames": 121, "seed": seed(sid), "strength": .8, "start": f"{sid}_a.png", "end": f"{sid}_b.png", "prompt": motion + STY})
json.dump(jobs, open(f"{B}/logo6_jobs.json", "w"), indent=1); open(f"{B}/only6", "w").write(",".join(j["id"] for j in jobs))
with tarfile.open("/dev/shm/vall/b6.tgz", "w:gz") as t: t.add(B, arcname=".")
print("logo6 jobs", len(jobs), "|", os.path.getsize("/dev/shm/vall/b6.tgz") // 1024, "KB")
