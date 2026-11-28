# LTX 2.5 jobs for the category films: one 5 s clip per shot (transform shots: start -> end keyframe). Films alternate between the
# two boxes (onlyA / onlyB). Keyframes are fed separately as JPEG (feeder.py), so the bundle holds only jobs.json.
import json, glob, os, hashlib
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; HERE = os.path.dirname(os.path.abspath(__file__))
B = f"{S}/catfilms/bundle"; os.makedirs(f"{B}/kf", exist_ok=True)
STY = " Smooth realistic motion, premium commercial cinematography, stable shapes and faces, natural physics, no text."
NEG = "blurry, warped faces, deformed hands, extra limbs, morphing objects, text, letters, logo, subtitles, watermark, flicker, jitter, low quality, cartoon"
jobs, A, Bx = [], [], []
films = [f for p in sorted(glob.glob(f"{HERE}/plan/*.json")) for f in json.load(open(p))["films"]]
for k, f in enumerate(films):
    fl = []
    w, h = (704, 1280) if f["type"] == "social" else (1280, 704)
    for n, s in enumerate(f["shots"], 1):
        jid = f"{f['id']}_s{n}"; seed = int(hashlib.sha1(jid.encode()).hexdigest()[:6], 16) % 100000
        j = {"id": jid, "w": w, "h": h, "frames": 121, "seed": seed, "strength": .85, "start": f"{jid}.jpg", "prompt": s["motion"] + STY}
        if f["type"] == "transform" and s.get("end_kf"): j.update(end=f"{jid}e.jpg", strength=.8, prompt=s["motion"] + " A smooth continuous timelapse transformation from the first frame to the last frame, same camera position." + STY)
        jobs.append(j); fl.append(jid)
    (A if len(A) <= len(Bx) else Bx).extend(fl)   # whole films to the box with fewer jobs
json.dump({"fps": 24, "steps": 8, "cfg": 1.0, "strength": .85, "negative": NEG, "jobs": jobs}, open(f"{B}/jobs.json", "w"), indent=1)
open(f"{S}/catfilms/onlyA", "w").write(",".join(A)); open(f"{S}/catfilms/onlyB", "w").write(",".join(Bx))
print("films", len(films), "jobs", len(jobs), "A", len(A), "B", len(Bx), "flf", sum(1 for j in jobs if j.get("end")))
