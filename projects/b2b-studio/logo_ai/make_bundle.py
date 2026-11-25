# LTX 2.5 bundle for the AI logo films (render/ltx_batch.py format). FLF where both keyframes are good; end-keyframe-only where the
# start frame had the logo pasted on (drone_show, constellation, chrome_liquid); billboard dropped (Gemini drew only the D).
import os, sys, json, hashlib, tarfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from scenes import S as SC
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KF = f"{S}/logo_ai/kf"
END_ONLY = {"drone_show": "The gold drone lights hover and twinkle in formation above the city as the camera slowly rises; the logo holds steady on the final frame.",
            "constellation": "Star dust drifts and the constellation lines pulse with light as the camera slowly pushes in; the glowing logo holds on the final frame.",
            "chrome_liquid": "Ripples spread across the chrome pool and reflections slide over the mirror-chrome logo as the camera slowly orbits; the logo holds on the final frame."}
DROP = {"billboard"}
STY = " Photorealistic premium commercial cinematography, crisp detail, the logo keeps its exact shape, no text."
NEG = "blurry, warped logo, deformed shapes, extra letters, text, subtitles, watermark, flicker, low quality, cartoon"
jobs = []; B = f"{S}/logo_ai/bundle"; shutil.rmtree(B, ignore_errors=True); os.makedirs(f"{B}/kf")
for sid, cap, a, b, mo in SC:
    if sid in DROP: continue
    seed = int(hashlib.sha1(sid.encode()).hexdigest()[:6], 16) % 100000
    j = {"id": "logo_" + sid, "w": 1280, "h": 704, "frames": 121, "seed": seed, "strength": .8}
    if sid in END_ONLY: j.update(start=f"{sid}_b.png", prompt=END_ONLY[sid] + STY)
    elif b: j.update(start=f"{sid}_a.png", end=f"{sid}_b.png", prompt=mo + STY)
    else: j.update(start=f"{sid}_a.png", prompt=mo + STY)
    for k in ("start", "end"):
        if j.get(k): shutil.copy(f"{KF}/{j[k]}", f"{B}/kf/{j[k]}")
    jobs.append(j)
json.dump({"fps": 24, "steps": 8, "cfg": 1.0, "strength": .8, "negative": NEG, "jobs": jobs}, open(f"{B}/jobs.json", "w"), indent=1)
with tarfile.open(f"{S}/logo_ai/logo_bundle.tgz", "w:gz") as t: t.add(B, arcname=".")
print("jobs", len(jobs), "flf", sum(1 for j in jobs if j.get("end")), os.path.getsize(f"{S}/logo_ai/logo_bundle.tgz"))
