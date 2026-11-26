# Keyframes for the v3 site films (batch "v3" in plan/*.json) with Gemini 3.1 Flash Lite Image through the Batch API (half price,
# ~$0.017 per 1K image; owner, 2026-11-26: "find a cheaper keyframe model"). Two rounds: round 1 = every frame that needs no reference;
# round 2 = commercial shots that show the recurring character (made from that film's first character frame, so the person stays the same)
# and transform end frames (made from their start frame). Output: <scratch>/catfilms/kf_v3/<film>_s<n>.jpg (+ s<n>e.jpg), 1280x704 or
# 704x1280, exactly what make_bundle expects.  python3 genkf_v3.py [--sync] [cat ...]
import json, glob, os, sys, base64, io, time, urllib.request, urllib.error, concurrent.futures as cf
from PIL import Image
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KEY = open(f"{S}/.gemini_paid").read().strip()
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{S}/catfilms/kf_v3"; os.makedirs(OUT, exist_ok=True)
MODEL = "gemini-3.1-flash-lite-image"; API = "https://generativelanguage.googleapis.com"
STYLE = " Photorealistic premium commercial photography, natural skin and materials, no text, no letters, no logos, no signage, no watermark."
CHAR = "The same main character as in the reference image: identical face, age, hair, build and clothes. New shot, new framing: "
END = "Same exact camera position, framing, lens and light as the reference image, but now: "

def req(url, data=None, headers=None, method=None, raw=False, timeout=300):
    h = {"x-goog-api-key": KEY}; h.update(headers or {})
    r = urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h, method=method), timeout=timeout)
    return r if raw else json.loads(r.read() or b"{}")

def body(prompt, ar, ref):
    parts = [{"text": prompt + STYLE}]
    if ref: parts.insert(0, {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(open(ref, "rb").read()).decode()}})
    return {"contents": [{"role": "user", "parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ar}}}

def save(out, ar, b64):
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB"); W, H = (704, 1280) if ar == "9:16" else (1280, 704)
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2; im.crop((l, t, l + W, t + H)).save(out, quality=94)

def img_of(resp): return next(p["inlineData"]["data"] for p in resp["candidates"][0]["content"]["parts"] if "inlineData" in p)

def sync_one(j):
    out, prompt, ar, ref = j
    for a in range(4):
        try: save(out, ar, img_of(req(f"{API}/v1beta/models/{MODEL}:generateContent", json.dumps(body(prompt, ar, ref)).encode(), {"Content-Type": "application/json"}))); return "ok"
        except urllib.error.HTTPError as e:
            if e.code == 402: raise SystemExit("GEMINI_402")
            time.sleep(5 * (a + 1)); err = e
        except Exception as e: time.sleep(5 * (a + 1)); err = e
    return f"FAIL {err}"

def batch_run(jobs, tag):
    """One Batch API job for these frames; returns the ones that came back without an image (to retry synchronously)."""
    lines = "".join(json.dumps({"key": os.path.basename(o), "request": body(p, ar, ref)}) + "\n" for o, p, ar, ref in jobs).encode()
    st = req(f"{API}/upload/v1beta/files", json.dumps({"file": {"display_name": f"kf_v3_{tag}"}}).encode(), {"Content-Type": "application/json",
             "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(len(lines)),
             "X-Goog-Upload-Header-Content-Type": "application/jsonl"}, raw=True)
    up = st.headers["X-Goog-Upload-URL"]
    f = req(up, lines, {"Content-Length": str(len(lines)), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, timeout=900)["file"]["name"]
    b = req(f"{API}/v1beta/models/{MODEL}:batchGenerateContent", json.dumps({"batch": {"display_name": f"kf_v3_{tag}", "input_config": {"file_name": f}}}).encode(),
            {"Content-Type": "application/json"})
    name = b["name"]; print("batch", tag, name, len(jobs), "frames", flush=True); t0 = time.time()
    while True:
        time.sleep(60); s = req(f"{API}/v1beta/{name}"); state = json.dumps(s)
        if any(x in state for x in ("BATCH_STATE_SUCCEEDED", "JOB_STATE_SUCCEEDED")) and "responsesFile" in state: break
        if any(x in state for x in ("BATCH_STATE_FAILED", "BATCH_STATE_CANCELLED", "BATCH_STATE_EXPIRED", "JOB_STATE_FAILED")): print("batch", tag, "ended", state[:300], flush=True); return jobs
        if (time.time() - t0) > 3 * 3600: print("batch", tag, "too slow: falling back to direct calls", flush=True); return [j for j in jobs if not os.path.exists(j[0])]
        print("batch", tag, "waiting", int(time.time() - t0) // 60, "min", flush=True)
    rf = next(v for k, v in _walk(s) if k == "responsesFile")
    by = {os.path.basename(j[0]): j for j in jobs}; got = 0
    with req(f"{API}/download/v1beta/{rf}:download?alt=media", raw=True, timeout=1800) as r:
        for line in r:
            d = json.loads(line); j = by.get(d.get("key"))
            try: save(j[0], j[2], img_of(d["response"])); got += 1
            except Exception: pass
    print("batch", tag, "saved", got, "of", len(jobs), flush=True)
    return [j for j in jobs if not os.path.exists(j[0])]

def _walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k, v; yield from _walk(v)
    elif isinstance(o, list):
        for v in o: yield from _walk(v)

def plan_jobs(cats):
    r1, r2 = [], []
    for c in cats:
        for f in json.load(open(f"{HERE}/plan/{c}.json", encoding="utf-8"))["films"]:
            if f.get("batch") != "v3": continue
            ar = "9:16" if f["type"] == "social" else "16:9"; first_char = None
            for n, s in enumerate(f["shots"], 1):
                out = f"{OUT}/{f['id']}_s{n}.jpg"
                if f["type"] == "commercial" and s.get("char"):
                    if first_char: r2.append((out, CHAR + s["kf"], ar, first_char))
                    else: first_char = out; r1.append((out, s["kf"], ar, None))
                else: r1.append((out, s["kf"], ar, None))
                if f["type"] == "transform" and s.get("end_kf"): r2.append((f"{OUT}/{f['id']}_s{n}e.jpg", END + s["end_kf"], ar, out))
    return r1, r2

if __name__ == "__main__":
    sync = "--sync" in sys.argv; cats = [a for a in sys.argv[1:] if not a.startswith("--")] or [os.path.basename(p)[:-5] for p in sorted(glob.glob(f"{HERE}/plan/*.json"))]
    r1, r2 = plan_jobs(cats)
    for tag, jobs in (("r1", r1), ("r2", r2)):
        todo = [j for j in jobs if not os.path.exists(j[0]) and (not j[3] or os.path.exists(j[3]))]
        if not todo: continue
        left = todo if sync else batch_run(todo, tag)
        if left:
            print("direct calls for", len(left), flush=True)
            with cf.ThreadPoolExecutor(4) as ex:
                for res, j in zip(ex.map(sync_one, left), left):
                    if res != "ok": print(res, os.path.basename(j[0]), flush=True)
    need = r1 + r2; have = sum(os.path.exists(j[0]) for j in need)
    print("KF_V3", have, "/", len(need), "frames", flush=True)
