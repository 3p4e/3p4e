# Keyframes for the category films (Gemini 3.1 Flash Image, ~$0.04/image): <id>_s<n>.png (start) and <id>_s<n>e.png (transform end,
# made from the start frame as reference so the framing stays identical). Social films are 9:16 (704x1280), the rest 16:9 (1280x704).
# Resume-safe; writes KF_DONE when every frame exists.  python3 genkf.py [cat ...]
import json, glob, os, sys, base64, io, time, urllib.request, concurrent.futures as cf
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KEY = open(f"{S}/.gemini_paid").read().strip()
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{S}/catfilms/kf"; os.makedirs(OUT, exist_ok=True)
STYLE = " Photorealistic premium commercial photography, natural skin and materials, no text, no letters, no logos, no signage, no watermark."
def gen(out, prompt, ar, ref=None):
    if os.path.exists(out): return "skip"
    parts = [{"text": prompt + STYLE}]
    if ref: parts.insert(0, {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(open(ref, "rb").read()).decode()}})
    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ar}}}
    for a in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={KEY}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=240).read())
            b = next(p["inlineData"]["data"] for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p)
            im = Image.open(io.BytesIO(base64.b64decode(b))).convert("RGB"); W, H = (704, 1280) if ar == "9:16" else (1280, 704)
            s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            l, t = (im.width - W) // 2, (im.height - H) // 2; im.crop((l, t, l + W, t + H)).save(out); return "ok"
        except urllib.error.HTTPError as e:
            if e.code == 402: raise SystemExit("GEMINI_402")
            time.sleep(5 * (a + 1)); err = e
        except Exception as e: time.sleep(5 * (a + 1)); err = e
    return f"FAIL {err}"
def film_jobs(f):
    ar = "9:16" if f["type"] == "social" else "16:9"
    for n, s in enumerate(f["shots"], 1):
        st = f"{OUT}/{f['id']}_s{n}.png"; yield (st, s["kf"], ar, None)
        if f["type"] == "transform" and s.get("end_kf"):
            yield (f"{OUT}/{f['id']}_s{n}e.png", "Same exact camera position, framing, lens and light as the reference image, but now: " + s["end_kf"], ar, st)
cats = sys.argv[1:] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(f"{HERE}/plan/*.json"))]
films = [f for c in cats for f in json.load(open(f"{HERE}/plan/{c}.json"))["films"]]
starts, ends = [], []
for f in films:
    for j in film_jobs(f): (ends if j[3] else starts).append(j)
with cf.ThreadPoolExecutor(3) as ex:
    for r, j in zip(ex.map(lambda j: gen(*j), starts), starts):
        if r.startswith("FAIL"): print(r, os.path.basename(j[0]), flush=True)
    for r, j in zip(ex.map(lambda j: gen(*j), ends), ends):
        if r.startswith("FAIL"): print(r, os.path.basename(j[0]), flush=True)
need = starts + ends; have = sum(os.path.exists(j[0]) for j in need); print("frames", have, "/", len(need), flush=True)
if have == len(need): open(f"{OUT}/KF_DONE", "w").write("ok")
