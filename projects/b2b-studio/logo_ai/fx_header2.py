# Header-logo loops v2 (owner, 2026-11-26: "logos are different sizes", "effects cut off by the box"):
# 1) find the BD mark in each clip by multi-scale template matching against the approved mark (its exact box, whatever glow surrounds it);
# 2) crop around that box with a 40 % margin (room for the effect to breathe), 384 px wide, h264;
# 3) list.js gets, per clip, the mark box inside the crop (0..1) and the effect's main colour, so the player draws every clip with the
#    mark at exactly the canvas engine's size and position, and the transition uses the real colours of both effects.
#   python3 fx_header2.py <clipdir>
import sys, os, glob, json, subprocess, numpy as np, cv2
from PIL import Image
SRC = sys.argv[1]; OUT = "/home/user/3p4e/projects/b2b-studio/launch/site_work/logo_fx/hdr"; os.makedirs(OUT, exist_ok=True)
DROP = {"black_hole", "blood_moon", "storm", "holy_light", "phoenix", "lightning", "butterflies", "ink"}   # objects slapped behind the mark / mark deforms
ref = np.array(Image.open("/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png").convert("RGBA"))
a = ref[..., 3] if ref[..., 3].min() < 250 else (255 - ref[..., :3].mean(axis=2))
ys, xs = np.where(a > 60); ref = (a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] > 60).astype(np.float32)
ref = cv2.GaussianBlur(ref, (0, 0), 3)
def frame(src, t=0.0):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(704, 1280, 3)
def locate(img):
    g = img.max(axis=2).astype(np.float32) / 255; g = cv2.GaussianBlur(g, (0, 0), 2)
    best = (-1, None)
    for h in np.arange(520, 700, 6):   # the keyframes put the mark at 75-97 % of the frame height
        w = int(h * ref.shape[1] / ref.shape[0]); 
        if w >= 1280: continue
        t = cv2.resize(ref, (w, int(h)), interpolation=cv2.INTER_AREA)
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED); _, v, _, p = cv2.minMaxLoc(r)
        if v > best[0]: best = (v, (p[0], p[1], w, int(h)))
    return best
items = []
for src in sorted(glob.glob(f"{SRC}/hdr_*.mp4")):
    k = os.path.basename(src)[4:-4]
    if k in DROP: continue
    f0 = frame(src, 0.2); score, (x, y, w, h) = locate(f0)
    m = .40; cw, ch = w * (1 + 2 * m), h * (1 + 2 * m); cx, cy = x + w / 2, y + h / 2
    # crop may go past the frame: pad with black first (black keys to transparent)
    P = 400; vf = f"pad=1280+{2*P}:704+{2*P}:{P}:{P}:black,crop={cw:.0f}:{ch:.0f}:{cx - cw/2 + P:.0f}:{cy - ch/2 + P:.0f},scale=384:-2:flags=lanczos,format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-crf", "23", "-preset", "slow", "-movflags", "+faststart", f"{OUT}/{k}.mp4"], check=True)
    # main colour: mean of the bright pixels on the mark
    reg = f0[max(0, y):y + h, max(0, x):x + w].reshape(-1, 3).astype(np.float32); br = reg[reg.max(axis=1) > 90]
    col = [int(v) for v in (np.median(br, axis=0) if len(br) else [242, 193, 78])]
    s = max(col); col = [int(v * 255 / max(s, 1)) for v in col]
    bb = [round(m / (1 + 2 * m), 4), round(m / (1 + 2 * m), 4), round(1 / (1 + 2 * m), 4), round(1 / (1 + 2 * m), 4)]
    items.append({"id": k, "bb": bb, "col": col}); print(k, f"match {score:.2f}", f"mark {w}x{h} at {x},{y}", col)
for f in glob.glob(f"{OUT}/*.mp4"):
    if os.path.basename(f)[:-4] not in {i["id"] for i in items}: os.remove(f)
open(f"{OUT}/list.js", "w").write("window.DOGMA_HDR=" + json.dumps(items, separators=(",", ":")) + ";\n"); print("list", len(items))
