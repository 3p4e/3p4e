# usage: oai_kf.py <out.png> <WxH api size> <final WxH> "<prompt>" ref1.png [ref2.png ...]
import os, sys, json, base64, io, uuid, urllib.request
from PIL import Image
out, size, final, prompt, refs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
model = os.environ.get("KF_MODEL", "gpt-image-2"); quality = os.environ.get("KF_QUALITY", "high")
b = uuid.uuid4().hex; parts = []
def field(n, v): parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode())
for n, v in (("model", model), ("prompt", prompt), ("size", size), ("quality", quality), ("n", "1")): field(n, v)
for r in refs:
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="{os.path.basename(r)}"\r\nContent-Type: image/png\r\n\r\n'.encode() + open(r, "rb").read() + b"\r\n")
body = b"".join(parts) + f"--{b}--\r\n".encode()
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
for a in range(3):
    try: r = json.loads(urllib.request.urlopen(req, timeout=600).read()); break
    except urllib.error.HTTPError as e:
        msg = e.read()[:400]
        if e.code in (429, 500, 502, 503) and a < 2: import time; time.sleep(20 * (a + 1)); continue
        sys.exit(f"HTTP {e.code} {msg}")
im = Image.open(io.BytesIO(base64.b64decode(r["data"][0]["b64_json"]))).convert("RGB")
W, H = map(int, final.split("x")); s = max(W / im.width, H / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); l, t = (im.width - W) // 2, (im.height - H) // 2
im.crop((l, t, l + W, t + H)).save(out); print("ok", out, r.get("usage", {}))
