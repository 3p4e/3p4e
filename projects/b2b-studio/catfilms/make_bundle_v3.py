# LTX jobs for the v3 site films only (batch "v3"), same settings as make_bundle.py; keyframes from kf_v3/ (JPEG, named as the jobs
# expect). The runner skips a job whose keyframe is not in the bundle yet, so the bundle can go out before round 2 of the keyframes.
#   python3 make_bundle_v3.py   -> /dev/shm/vall/cfb/{jobs.json,kf/} + /dev/shm/vall/cfb.tgz
import json, glob, os, hashlib, shutil, tarfile
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; HERE = os.path.dirname(os.path.abspath(__file__))
KF = f"{S}/catfilms/kf_v3"; B = "/dev/shm/vall/cfb"; shutil.rmtree(B, ignore_errors=True); os.makedirs(f"{B}/kf")
STY = " Smooth realistic motion, premium commercial cinematography, stable shapes and faces, natural physics, no text."
NEG = "blurry, warped faces, deformed hands, extra limbs, morphing objects, text, letters, logo, subtitles, watermark, flicker, jitter, low quality, cartoon"
jobs = []
for p in sorted(glob.glob(f"{HERE}/plan/*.json")):
    for f in json.load(open(p, encoding="utf-8"))["films"]:
        if f.get("batch") != "v3": continue
        w, h = (704, 1280) if f["type"] == "social" else (1280, 704)
        for n, s in enumerate(f["shots"], 1):
            jid = f"{f['id']}_s{n}"; seed = int(hashlib.sha1(jid.encode()).hexdigest()[:6], 16) % 100000
            j = {"id": jid, "w": w, "h": h, "frames": 121, "seed": seed, "strength": .85, "start": f"{jid}.jpg", "prompt": s["motion"] + STY}
            if f["type"] == "transform" and s.get("end_kf"):
                j.update(end=f"{jid}e.jpg", strength=.8, prompt=s["motion"] + " A smooth continuous timelapse transformation from the first frame to the last frame, same camera position." + STY)
            jobs.append(j)
ready = 0
for j in jobs:
    need = [j["start"]] + ([j["end"]] if j.get("end") else [])
    if all(os.path.exists(f"{KF}/{x}") for x in need):
        for x in need: shutil.copy(f"{KF}/{x}", f"{B}/kf/{x}")
        ready += 1
json.dump({"fps": 24, "steps": 8, "cfg": 1.0, "strength": .85, "negative": NEG, "jobs": jobs}, open(f"{B}/jobs.json", "w"), indent=1)
with tarfile.open("/dev/shm/vall/cfb.tgz", "w:gz") as t: t.add(B, arcname=".")
print("jobs", len(jobs), "ready now", ready, "| bundle", os.path.getsize("/dev/shm/vall/cfb.tgz") // 1048576, "MB")
