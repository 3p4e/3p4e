# Mark box of every full-size logo effect clip (launch/site/media/bd/<id>.mp4, 1280x704) for the BD reel: the reel places each clip
# so its mark lands exactly on the big canvas logo, and the stroke transition runs over the real mark.  python3 fx_reel_bb.py <site dir>
import sys, os, glob, json, subprocess, numpy as np, cv2
from PIL import Image
SITE = sys.argv[1]; OUT = "/home/user/3p4e/projects/b2b-studio/launch/site_work/logo_fx/reel_bb.js"
ref = np.array(Image.open("/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png").convert("RGBA"))
a = ref[..., 3] if ref[..., 3].min() < 250 else (255 - ref[..., :3].mean(axis=2))
ys, xs = np.where(a > 60); ref = cv2.GaussianBlur((a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] > 60).astype(np.float32), (0, 0), 3)
def frame(src, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(704, 1280, 3)
def locate(img):
    g = cv2.GaussianBlur(img.max(axis=2).astype(np.float32) / 255, (0, 0), 2); best = (-1, None)
    for h in np.arange(360, 700, 6):
        w = int(h * ref.shape[1] / ref.shape[0])
        if w >= 1280: continue
        r = cv2.matchTemplate(g, cv2.resize(ref, (w, int(h)), interpolation=cv2.INTER_AREA), cv2.TM_CCOEFF_NORMED); _, v, _, p = cv2.minMaxLoc(r)
        if v > best[0]: best = (v, (p[0], p[1], w, int(h)))
    return best
hdr = {x["id"]: x for x in json.loads(open("/home/user/3p4e/projects/b2b-studio/launch/site_work/logo_fx/hdr/list.js").read().split("=", 1)[1].rstrip(";\n"))}
out = []
for src in sorted(glob.glob(f"{SITE}/media/bd/*.mp4")):
    k = os.path.basename(src)[:-4]
    if k not in hdr: continue   # same set as the header (rejected effects stay out)
    s, (x, y, w, h) = locate(frame(src, 0.2))
    out.append({"id": k, "bb": [round(x / 1280, 4), round(y / 704, 4), round(w / 1280, 4), round(h / 704, 4)], "col": hdr[k]["col"], "q": round(float(s), 2)})
    print(k, round(float(s), 2), x, y, w, h)
# low-confidence matches (glow/petals hide the strokes) take the median box of the confident ones
med = [round(float(v), 4) for v in np.median(np.array([x["bb"] for x in out if x["q"] >= 0.5]), axis=0)]
for x in out:
    if x["q"] < 0.4: x["bb"] = med; x["fb"] = 1
open(OUT, "w").write("window.DOGMA_REEL_FX=" + json.dumps(out, separators=(",", ":")) + ";\n"); print("reel fx", len(out))
