# Start frames for round-6 fleet films whose start keyframe could not be generated (OpenAI credit ran out 2026-11-27): built from the end
# frame itself. The ships' area (the mark's three triangles, as in genkf5.ship_guide, dilated) is filled by OpenCV inpainting and then
#  - "mist": covered with drifting cloud built from the scene's own cloud colours (the ships then rise out of the cloud), or
#  - "warp": crossed by three white-blue hyperspace streaks at the ships' positions (the ships then drop out of hyperspace).
#   python3 start6.py overlay           -> QC overlay of the triangles on every end frame
#   python3 start6.py <id>=<mist|warp> ...
import os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import genkf5 as G
K = f"{G.S}/logo_ai/kf6"; W, H = 1280, 704

def triangles():
    a, _ = G.mark_alpha(); hh, ww = a.shape; s = (.6 * 845) / hh; ox, oy = 768 - ww * s / 2, 512 - hh * s / 2; by = 582 - 13; sx = G.SPLIT - 13
    k = W / 1536; t = (round(1024 * k) - H) // 2
    P = lambda x, y: ((ox + x * s) * k, (oy + y * s) * k - t)
    return [[P(0, 0), P(0, by), P(sx, by / 2)], [P(0, by), P(0, hh), P(sx, (by + hh) / 2)], [P(sx, 8), P(sx, hh - 8), P(ww, hh / 2)]]

def mask(grow=34, scale=1.4, shift=-22):
    # the painted ships come out 15-25 % bigger than the guide (QC overlay 2026-11-27): use the formation's outline scaled about its centre
    pts = np.array([p for tri in triangles() for p in tri], np.float32); hull = cv2.convexHull(pts).reshape(-1, 2); c = hull.mean(0)
    hull = c + (hull - c) * scale + np.array([shift, 0]); m = Image.new("L", (W, H)); d = ImageDraw.Draw(m); d.polygon([tuple(p) for p in hull], fill=255)
    return np.asarray(m.filter(ImageFilter.MaxFilter(2 * (grow // 2) + 1)).filter(ImageFilter.MaxFilter(2 * (grow // 2) + 1)))

def noise(seed, scale):   # soft fractal noise 0..1
    rnd = np.random.default_rng(seed); acc = np.zeros((H, W), np.float32); amp = 1.0
    for o in range(5):
        sz = (max(2, W // (scale >> o)), max(2, H // (scale >> o)))
        acc += amp * np.asarray(Image.fromarray((rnd.random(sz[::-1]) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255; amp *= .5
    acc -= acc.min(); return acc / acc.max()

def build(sid, mode, seed=7):
    end = np.asarray(Image.open(f"{K}/{sid}_b.png").convert("RGB")); m = mask()
    keep = (m < 128).astype(np.float32); e = end.astype(np.float32)
    fill = None   # multi-scale: the widest blur everywhere, finer ones wherever enough untouched pixels are near (no dark core in big holes)
    for sg in (500, 200, 90, 40):
        num = cv2.GaussianBlur(e * keep[..., None], (0, 0), sg); den = cv2.GaussianBlur(keep, (0, 0), sg)[..., None]; f = num / np.maximum(den, 1e-4)
        fill = f if fill is None else np.where(den > .12, f, fill)
    fill = cv2.GaussianBlur(fill, (0, 0), 12)
    if mode == "warp":   # space: scatter stars over the filled area like the surrounding starfield
        rnd = np.random.default_rng(seed + 5); ys, xs = np.nonzero(m > 128); pick = rnd.choice(len(ys), 900, replace=False)
        for y, x in zip(ys[pick], xs[pick]): fill[y, x] = np.minimum(255, fill[y, x] + rnd.uniform(60, 220))
    soft = np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(28)), np.float32)[..., None] / 255
    if mode == "mist":
        lum = end.astype(np.float32).mean(2); tone = np.percentile(end.reshape(-1, 3)[lum.reshape(-1) > np.percentile(lum, 70)], 60, axis=0)   # the scene's bright cloud colour
        n = noise(seed, 256); cloud = np.clip((n - .25) / .6, 0, 1)[..., None]
        reach = np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(61)).filter(ImageFilter.GaussianBlur(60)), np.float32)[..., None] / 255
        shade = (.55 + .6 * noise(seed + 1, 128))[..., None]
        out = end * (1 - soft) + fill * soft
        a = np.clip(reach * (.55 + .5 * cloud), 0, .97); out = out * (1 - a) + (tone * shade) * a
    else:   # warp streaks
        out = end * (1 - soft) + fill * soft
        st = Image.new("L", (W, H)); d = ImageDraw.Draw(st)
        rnd = np.random.default_rng(seed + 9); ramp = np.zeros((H, W), np.float32)
        for tri in triangles():   # a bundle of thin tapered streaks per ship, brightest at the head (where the bow will be)
            xs_ = [p[0] for p in tri]; ys_ = [p[1] for p in tri]; head = max(xs_) + 30; y0, y1 = min(ys_), max(ys_)
            for _ in range(9):
                y = rnd.uniform(y0 + .2 * (y1 - y0), y1 - .2 * (y1 - y0)); L = rnd.uniform(500, 1100); x0 = head - L
                d.line([(x0, y), (head - rnd.uniform(0, 60), y)], fill=int(rnd.uniform(150, 255)), width=int(rnd.choice([1, 2, 2, 3])))
        xs = np.arange(W, dtype=np.float32)[None, :]; heads = max(max(p[0] for p in t) for t in triangles()) + 30
        taper = np.clip(1 - (heads - xs) / 1000, 0, 1) ** 1.6          # fade to the left
        line = np.asarray(st.filter(ImageFilter.GaussianBlur(.8)), np.float32) / 255 * taper
        glow = np.asarray(st.filter(ImageFilter.GaussianBlur(14)), np.float32) / 255 * taper
        out = out + line[..., None] * np.array([255, 255, 255]) * 1.1 + glow[..., None] * np.array([80, 140, 255]) * 2.2
    rnd = np.random.default_rng(seed); out = out + rnd.normal(0, 2.2, out.shape)   # film grain over the filled area too
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f"{K}/{sid}_a.png"); print("start", sid, mode)

if __name__ == "__main__":
    if sys.argv[1] == "overlay":
        from scenes6 import S6
        tiles = []
        for sid, *_ in S6:
            im = Image.open(f"{K}/{sid}_b.png").convert("RGB"); d = ImageDraw.Draw(im)
            for tri in triangles(): d.line(tri + [tri[0]], fill=(0, 255, 120), width=3)
            mm = Image.fromarray(mask()).filter(ImageFilter.FIND_EDGES); im.paste((255, 60, 60), mask=mm.point(lambda v: 255 if v > 0 else 0))
            tiles.append(im.resize((480, 264)))
        sh = Image.new("RGB", (960, 264 * 5))
        for i, t in enumerate(tiles): sh.paste(t, ((i % 2) * 480, (i // 2) * 264))
        sh.save("/dev/shm/vall/sr/kf6_overlay.jpg", quality=85)
    else:
        for arg in sys.argv[1:]: build(*arg.split("="))
