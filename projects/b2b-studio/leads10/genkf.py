# Pitch films for ten non-EU Europe leads (retail, fuel, food, real estate): key frames with the OpenAI image API, each built on one or two official
# photos from drugitir.si as references (so tunnels, portals, viaducts and the karst look like the real line).
# Slovenia is in the EU: the films are rendered with LTX only (no MiniMax H3).
# Shots (prompts) live in the scratchpad (leads10/shots.json, kept out of the repo); references and outputs in /dev/shm.
#   python3 genkf.py [shot_id ...]      -> <OUT>/<id>.jpg, 1280x704 (16:9) or 704x1280 (9:16)
import os, sys, json, io, base64, time, concurrent.futures as cf
import requests
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
SHOTS = json.load(open(f"{S}/leads10/shots.json", encoding="utf-8"))
REF = os.environ.get("DT_REF", "/dev/shm/vall/ld/refs"); OUT = os.environ.get("DT_KF", "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/leads10/kf"); os.makedirs(OUT, exist_ok=True)
MODEL = os.environ.get("OA_IMAGE_MODEL", "gpt-image-2"); QUALITY = os.environ.get("OA_QUALITY", "medium")
STYLE = (" Photorealistic, cinematic commercial photography, natural light, true-to-life materials, no text, no letters, no logos, no signage, no watermark.")
H = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}

def save(path, ar, b64):
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB"); W, Hh = (704, 1280) if ar == "9:16" else (1280, 704)
    s = max(W / im.width, Hh / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - Hh) // 2; im.crop((l, t, l + W, t + Hh)).save(path, quality=94)

def one(sh):
    out = f"{OUT}/{sh['id']}.jpg"
    if os.path.exists(out): return sh["id"], "exists"
    size = "1024x1536" if sh.get("ar") == "9:16" else "1536x1024"
    for attempt in range(3):
        try:
            files = [("image[]", (os.path.basename(r), open(f"{REF}/{r}", "rb"), "image/jpeg")) for r in sh.get("refs", [])]
            data = {"model": MODEL, "prompt": sh["prompt"] + STYLE, "size": size, "quality": QUALITY, "n": "1"}
            r = (requests.post("https://api.openai.com/v1/images/edits", headers=H, files=files, data=data, timeout=300) if files else
                 requests.post("https://api.openai.com/v1/images/generations", headers=H, json={**data, "n": 1}, timeout=300))
            if r.status_code == 200:
                save(out, sh.get("ar", "16:9"), r.json()["data"][0]["b64_json"]); return sh["id"], "ok"
            err = r.text[:200]
            if r.status_code in (400, 401, 403): return sh["id"], f"error {r.status_code} {err}"
        except Exception as e:
            err = str(e)[:200]
        time.sleep(10 * (attempt + 1))
    return sh["id"], "failed " + err

want = sys.argv[1:]
jobs = [s for s in SHOTS if not want or s["id"] in want]
with cf.ThreadPoolExecutor(4) as ex:
    for sid, st in ex.map(one, jobs): print(sid, st, flush=True)
