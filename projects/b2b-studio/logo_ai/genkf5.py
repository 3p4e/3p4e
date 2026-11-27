# Keyframes for logo films round 5 (scenes5.py). The logo's exact form comes from the mark file (brand/mark_bd_M2_P3.png, black strokes on
# white), never from the image model:
#  - energy blades: end frame drawn here (every stroke of the mark = a glowing blade, B and D in their colours); start = gpt-image-2 duel
#  - spaceships: a guide with the mark's three triangles (B top, B bottom, D) at their exact places -> gpt-image-2 paints the ships over it;
#    start = the same scene without the ships (gpt-image-2 edit of the end frame)
#  - Nazca: start = gpt-image-2 desert; end = the mark scraped into that desert as pale geoglyph lines (top-down, or in perspective)
# Output 1280x704 PNG: <scratch>/logo_ai/kf5/<id>_a.png (start), <id>_b.png (end).   python3 genkf5.py [id ...]
import os, sys, io, base64, json, random
import numpy as np, requests
from PIL import Image, ImageFilter, ImageDraw, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from scenes5 import S5, SHIP
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; OUT = f"{S}/logo_ai/kf5"; os.makedirs(OUT, exist_ok=True)
MARK = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; W, H = 1280, 704
STY = " Photorealistic cinematic still, premium lighting, crisp detail, no text, no letters, no symbols, no logos, no watermark."
COL = {"red": (255, 40, 30), "blue": (40, 120, 255)}
OA = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}

def mark_alpha():   # stroke opacity 0..1 from the black-on-white mark, cropped to its ink
    a = 1 - np.asarray(Image.open(MARK).convert("L"), dtype=np.float32) / 255
    ys, xs = np.nonzero(a > .3); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1], xs.min()
SPLIT = 529   # B | D column in the mark file (measured: the B ends at x 528, the D starts at 529)

def place(a, h_frac=.72, cx=.5, cy=.5, w=W, h=H):
    """The mark scaled to h_frac of the frame height, centred at (cx, cy): returns full-frame alpha and the split column in frame coords."""
    s = h_frac * h / a.shape[0]; im = Image.fromarray((a * 255).astype(np.uint8)).resize((round(a.shape[1] * s), round(a.shape[0] * s)), Image.LANCZOS)
    f = Image.new("L", (w, h)); x0, y0 = round(cx * w - im.width / 2), round(cy * h - im.height / 2); f.paste(im, (x0, y0))
    return np.asarray(f, dtype=np.float32) / 255, x0, s

def oa_image(prompt, refs=(), size="1536x1024", quality="high"):
    for a in range(4):
        try:
            if refs:
                files = [("image[]", (f"r{i}.png", open(r, "rb"), "image/png")) for i, r in enumerate(refs)]
                r = requests.post("https://api.openai.com/v1/images/edits", headers=OA, timeout=400, files=files,
                                  data={"model": "gpt-image-2", "prompt": prompt, "size": size, "quality": quality, "n": "1"})
            else:
                r = requests.post("https://api.openai.com/v1/images/generations", headers=OA, timeout=400,
                                  json={"model": "gpt-image-2", "prompt": prompt, "size": size, "quality": quality, "n": 1})
            r.raise_for_status(); return Image.open(io.BytesIO(base64.b64decode(r.json()["data"][0]["b64_json"]))).convert("RGB")
        except Exception as e: print("retry", str(e)[:200], getattr(r, "text", "")[:200] if 'r' in locals() else "", flush=True)
    raise SystemExit("image failed")

def fit(im):   # 1536x1024 -> 1280x704, centre crop
    s = W / im.width; im = im.resize((W, round(im.height * s)), Image.LANCZOS); t = (im.height - H) // 2; return im.crop((0, t, W, t + H))

def blades_end(cb, cd, seed):
    rnd = np.random.default_rng(seed); a, _ = mark_alpha(); al, x0, s = place(a, .74)
    split = x0 + round(SPLIT * s); m = Image.fromarray((al * 255).astype(np.uint8))
    core = np.asarray(m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.8)), dtype=np.float32) / 255
    img = np.zeros((H, W, 3), np.float32)
    haze = np.asarray(Image.fromarray((rnd.random((H // 16, W // 16)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30)), np.float32) / 255
    img += haze[..., None] * np.array([10, 10, 18], np.float32)
    alB = al.copy(); alB[:, split:] = 0; alD = al.copy(); alD[:, :split] = 0   # glow the B and the D strokes separately: no seam between the colours
    for part, c in ((alB, COL[cb]), (alD, COL[cd])):
        mp = Image.fromarray((part * 255).astype(np.uint8))
        for rad, wgt in ((3, 1.1), (9, .9), (24, .6), (60, .35)):
            g = np.asarray(mp.filter(ImageFilter.GaussianBlur(rad)), np.float32) / 255; img += g[..., None] * np.array(c, np.float32) * wgt * 2.2
    img += core[..., None] * np.array([255, 245, 235], np.float32) * 1.15   # white-hot cores
    ys, xs = np.nonzero(al > .5); pick = rnd.choice(len(ys), 260, replace=False); sp = Image.new("L", (W, H)); d = ImageDraw.Draw(sp)
    for k in pick:   # a few last sparks around the blades
        y, x = ys[k] + rnd.normal(0, 18), xs[k] + rnd.normal(0, 18); r_ = rnd.uniform(.6, 1.8); d.ellipse((x - r_, y - r_, x + r_, y + r_), fill=int(rnd.uniform(120, 255)))
    img += (np.asarray(sp.filter(ImageFilter.GaussianBlur(.7)), np.float32) / 255)[..., None] * np.array([255, 230, 200], np.float32)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

def ship_guide():   # the mark's three triangles as flat grey shapes at their exact places, 1536x1024 (the 1280x704 crop is the middle band)
    a, _ = mark_alpha(); hh, ww = a.shape; s = (.6 * 845) / hh; ox, oy = 768 - ww * s / 2, 512 - hh * s / 2
    g = Image.new("RGB", (1536, 1024), (120, 140, 165)); d = ImageDraw.Draw(g); by = 582 - 13; sx = SPLIT - 13
    P = lambda x, y: (ox + x * s, oy + y * s)
    for tri in ([P(0, 0), P(0, by), P(sx, by / 2)], [P(0, by), P(0, hh), P(sx, (by + hh) / 2)], [P(sx, 8), P(sx, hh - 8), P(ww, hh / 2)]):
        (ax, ay), (bx, by_), (cx, cy) = tri   # shaded like a solid hull: a lit upper facet, a dark lower facet, a thick rim
        mx, my = (ax + bx) / 2 + (cx - (ax + bx) / 2) * .35, (ay + by_) / 2
        d.polygon([(ax, ay), (cx, cy), (mx, my)], fill=(108, 112, 120)); d.polygon([(bx, by_), (cx, cy), (mx, my)], fill=(46, 48, 54))
        d.polygon([(ax, ay), (bx, by_), (mx, my)], fill=(72, 75, 82)); d.line([(ax, ay), (bx, by_), (cx, cy), (ax, ay)], fill=(225, 225, 225), width=5)
    p = f"{OUT}/ship_guide.png"; g.save(p); return p

def nazca_end(start, mode, seed):
    rnd = np.random.default_rng(seed); a, _ = mark_alpha()
    if mode == "top": al, _, _ = place(a, .78)
    else:   # lay the drawing on the ground plane: a perspective trapezoid in the lower middle of the frame
        al0, _, _ = place(a, .92, w=2 * W, h=2 * H); src = Image.fromarray((al0 * 255).astype(np.uint8))
        dst = [(W * .16, H * .93), (W * .84, H * .93), (W * .66, H * .50), (W * .34, H * .50)]; srcq = [(0, 2 * H), (2 * W, 2 * H), (2 * W, 0), (0, 0)]
        A = []; B = []
        for (x, y), (u, v) in zip(dst, srcq): A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
        co = np.linalg.solve(np.array(A), np.array(B)); al = np.asarray(src.transform((W, H), Image.PERSPECTIVE, tuple(co), Image.BICUBIC), np.float32) / 255
    m = Image.fromarray((np.clip(al * 1.6, 0, 1) * 255).astype(np.uint8))
    line = np.asarray(m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255   # scraped trench
    rim = np.clip(np.asarray(m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2.5)), np.float32) / 255 - line, 0, 1)   # pebbles piled at the edges
    base = np.asarray(start, np.float32); grain = rnd.normal(1, .08, (H, W))[..., None]
    lum = base.mean(2, keepdims=True); pale = np.clip(base * 1.42 + lum * .18 + 10, 0, 255) * grain   # the soil under the stones, lit like the scene
    out = base * (1 - .35 * rim[..., None]); out = out * (1 - .9 * line[..., None]) + pale * (.9 * line[..., None])
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for k, (sid, kind, a_prompt, extra, motion) in enumerate(S5):
        if only and sid not in only: continue
        A, B = f"{OUT}/{sid}_a.png", f"{OUT}/{sid}_b.png"
        if kind == "blades":
            if not os.path.exists(B): blades_end(*extra, seed=k).save(B)
            if not os.path.exists(A): fit(oa_image(a_prompt + STY)).save(A)
        elif kind == "ships":
            if not os.path.exists(B):
                fit(oa_image(f"Turn this layout guide into a photograph. Use the guide ONLY for where the three ships are and how big they are; replace "
                             f"the three shaded grey shapes with {SHIP}. They must not look flat or pasted on: real 3D hulls lit by the scene's light. "
                             f"The scene: {a_prompt}. Keep all three ships fully inside the frame with space around them." + STY,
                             refs=[ship_guide()])).save(B)
            if not os.path.exists(A):
                big = Image.open(B).resize((1536, 846), Image.LANCZOS); pad = Image.new("RGB", (1536, 1024)); pad.paste(big, (0, 89)); pad.save(f"{OUT}/_ref.png")
                fit(oa_image("The exact same view, sky, clouds, light, colours and camera as this image, a few moments earlier: the three spaceships are "
                             "not there yet, only the empty sky and clouds (and cloud vapour where they will appear)." + STY, refs=[f"{OUT}/_ref.png"])).save(A)
        elif kind == "nazca":
            if not os.path.exists(A): fit(oa_image(a_prompt + STY)).save(A)
            if not os.path.exists(B): nazca_end(Image.open(A).convert("RGB"), extra, seed=k).save(B)
        print("ok", sid, flush=True)
    print("KF5_DONE", sum(os.path.exists(f"{OUT}/{s[0]}_{x}.png") for s in S5 for x in "ab"), "/", 2 * len(S5))
