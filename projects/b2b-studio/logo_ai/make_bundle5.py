# LTX jobs for logo films round 5 (scenes5.py): start -> end keyframe, 5 s, 1280x704, merged into the v3 site-films bundle so one box renders
# them first and then block C. Writes /dev/shm/vall/cfb/{jobs.json, kf/<id>_a.png|_b.png, onlyC5} and /dev/shm/vall/cfb5.tgz.
import os, sys, json, hashlib, shutil, tarfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from scenes5 import S5
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; K = f"{S}/logo_ai/kf5"; B = "/dev/shm/vall/cfb"
STY = " Photorealistic premium commercial cinematography, crisp detail, the logo keeps its exact shape at the end, no text."
def seed(x): return int(hashlib.sha1(x.encode()).hexdigest()[:6], 16) % 100000
d = json.load(open(f"{B}/jobs.json")); d["jobs"] = [j for j in d["jobs"] if not j["id"].startswith("logo_")]
new = []
for sid, kind, a, b, mo in S5:
    for k in "ab": shutil.copy(f"{K}/{sid}_{k}.png", f"{B}/kf/{sid}_{k}.png")
    new.append({"id": "logo_" + sid, "w": 1280, "h": 704, "frames": 121, "seed": seed(sid), "strength": .8, "start": f"{sid}_a.png", "end": f"{sid}_b.png", "prompt": mo + STY})
d["jobs"] = new + d["jobs"]; json.dump(d, open(f"{B}/jobs.json", "w"), indent=1)
open(f"{B}/onlyC5", "w").write(",".join([j["id"] for j in new] + open(f"{B}/onlyC").read().split(",")))
with tarfile.open("/dev/shm/vall/cfb5.tgz", "w:gz") as t: t.add(B, arcname=".")
print("logo jobs", len(new), "| total jobs", len(d["jobs"]), "| box-1 queue", len(open(f"{B}/onlyC5").read().split(",")), "|", os.path.getsize("/dev/shm/vall/cfb5.tgz") // 1048576, "MB")
