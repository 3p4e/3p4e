# LTX bundle round 3: 20 header effects (FX2, loops: start and end are the same frame, saved as two files because ComfyUI on one box
# mis-loads the same file twice) + 11 logo films (S3, start -> end). Halves for the two boxes in onlyA3 / onlyB3.
import os, sys, json, hashlib, tarfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fx_scenes2 import FX2
from scenes3 import S3
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; B = f"{S}/logo_ai/bundle3"
shutil.rmtree(B, ignore_errors=True); os.makedirs(f"{B}/kf")
STY = " Photorealistic premium commercial cinematography, crisp detail, the logo keeps its exact shape, no text."
LOCK = " Locked-off static camera, the logo stays exactly in place and keeps its exact shape; pure black background, nothing else in frame."
NEG = "blurry, warped logo, deformed shapes, extra letters, text, subtitles, watermark, flicker, low quality, cartoon"
def seed(x): return int(hashlib.sha1(x.encode()).hexdigest()[:6], 16) % 100000
jobs = []
for fid, _, mo in FX2:
    shutil.copy(f"{S}/logo_ai/kf_fx2/{fid}.png", f"{B}/kf/fx2_{fid}.png"); shutil.copy(f"{S}/logo_ai/kf_fx2/{fid}.png", f"{B}/kf/fx2_{fid}_end.png")
    jobs.append({"id": "hdr_" + fid, "w": 1280, "h": 704, "frames": 121, "seed": seed(fid), "strength": .85, "start": f"fx2_{fid}.png", "end": f"fx2_{fid}_end.png", "prompt": mo + LOCK + STY})
for sid, cap, a, b, mo in S3:
    for k in ("a", "b"): shutil.copy(f"{S}/logo_ai/kf/{sid}_{k}.png", f"{B}/kf/{sid}_{k}.png")
    jobs.append({"id": "logo_" + sid, "w": 1280, "h": 704, "frames": 121, "seed": seed(sid), "strength": .8, "start": f"{sid}_a.png", "end": f"{sid}_b.png", "prompt": mo + STY})
json.dump({"fps": 24, "steps": 8, "cfg": 1.0, "strength": .8, "negative": NEG, "jobs": jobs}, open(f"{B}/jobs.json", "w"), indent=1)
with tarfile.open(f"{S}/logo_ai/logo_bundle3.tgz", "w:gz") as t: t.add(B, arcname=".")
ids = [j["id"] for j in jobs]; open(f"{S}/logo_ai/onlyA3", "w").write(",".join(ids[0::2])); open(f"{S}/logo_ai/onlyB3", "w").write(",".join(ids[1::2]))
print("jobs", len(jobs), os.path.getsize(f"{S}/logo_ai/logo_bundle3.tgz"))
