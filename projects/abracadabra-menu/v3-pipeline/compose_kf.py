"""Builds LTX start/end keyframes for the per-item wand animations.

Methodology copied from the original Higgsfield clips: the wand character is in the
first AND the last frame (Kling start+end frames for the cinematics), so the video
model cannot lose it. Each end frame = wand character card + the item's dish.

usage: compose_kf.py <dish_dir> <out_dir>
  dish_dir: one PNG per item, dish on a black background (name = item key)
  writes:  small_start.png (768x1024), small_end_<key>.png,
           big_start.png (1280x704), big_end_<key>.png
"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO = "/home/user/3p4e/projects/abracadabra-menu/assets"
dish_dir, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
wand = Image.open(f"{REPO}/mascot_day.png").convert("RGBA")


def cover(img, w, h):
    r = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))


def cutout(img):
    """dish on black -> RGBA with a solid interior (dark parts of the food stay opaque)."""
    img = img.convert("RGB")
    lum = img.convert("L")
    m = lum.point(lambda v: 255 if v > 48 else 0)
    # exterior = flood fill from the border on the inverted mask; everything else is the dish
    ext = Image.new("L", (m.width + 2, m.height + 2), 0)
    ext.paste(m, (1, 1))
    ImageDraw.floodfill(ext, (0, 0), 128)
    ext = ext.crop((1, 1, m.width + 1, m.height + 1))
    solid = ext.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2))
    # keep thin bright steam/sparkles as soft luminance alpha
    soft = lum.point(lambda v: min(255, max(0, (v - 14) * 2)))
    a = ImageChops.lighter(solid, soft)
    rgba = img.convert("RGBA"); rgba.putalpha(a)
    bb = solid.getbbox() or (0, 0, img.width, img.height)
    return rgba.crop(bb)


def glow(size, center, radius, color, strength=0.55):
    g = Image.new("RGB", size, (0, 0, 0))
    d = ImageDraw.Draw(g)
    for k in range(radius, 0, -4):
        f = (1 - k / radius) ** 1.6 * strength
        d.ellipse((center[0] - k, center[1] - k, center[0] + k, center[1] + k), fill=tuple(int(c * f) for c in color))
    return g.filter(ImageFilter.GaussianBlur(12))


def place(base, sprite, cx, cy, h):
    s = h / sprite.height
    sp = sprite.resize((max(1, round(sprite.width * s)), round(h)), Image.LANCZOS)
    base.alpha_composite(sp, (round(cx - sp.width / 2), round(cy - sp.height / 2)))


# ---- small (3:4 wand panel, like wand_burger) ----
SW, SH = 768, 1024
stage = Image.open(f"{REPO}/stage_day.jpg").convert("RGB")
panel = Image.blend(cover(stage, SW, SH).filter(ImageFilter.GaussianBlur(26)), Image.new("RGB", (SW, SH), (8, 5, 12)), 0.8).convert("RGBA")
WX, WY, WH = SW * 0.26, SH * 0.50, SH * 0.80          # wand on the left, room on the right for the dish
start = panel.copy(); place(start, wand, WX, WY, WH)
start.convert("RGB").save(f"{out}/small_start.png")

# ---- big (16:9 stage, like the Kling summon end frames: dish centre, wand presenting at the right) ----
BW, BH = 1280, 704
bstage = cover(stage, BW, BH).convert("RGBA")
summon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf_summon_start.png")
if os.path.exists(summon):
    cover(Image.open(summon).convert("RGB"), BW, BH).save(f"{out}/big_start.png")

for f in sorted(glob.glob(os.path.join(dish_dir, "*.png"))):
    key = os.path.splitext(os.path.basename(f))[0]
    dish = cutout(Image.open(f))
    # small end
    e = panel.copy()
    e.alpha_composite(Image.merge("RGBA", (*glow((SW, SH), (int(SW * 0.64), int(SH * 0.56)), 300, (255, 170, 70)).split(), Image.new("L", (SW, SH), 150))))
    place(e, wand, WX, WY, WH)
    dw = SW * 0.52; dh = min(SH * 0.42, dish.height * dw / dish.width)
    place(e, dish, SW * 0.68, SH * 0.57, dh)
    e.convert("RGB").save(f"{out}/small_end_{key}.png")
    # big end
    b = bstage.copy()
    gl = glow((BW, BH), (int(BW * 0.47), int(BH * 0.52)), 380, (255, 165, 60), 0.7)
    b = Image.alpha_composite(b, Image.merge("RGBA", (*gl.split(), gl.convert("L").point(lambda v: min(255, v * 2)))))
    dh = min(BH * 0.62, dish.height * (BW * 0.46) / dish.width)
    place(b, dish, BW * 0.47, BH * 0.53, dh)
    place(b, wand, BW * 0.80, BH * 0.50, BH * 0.86)
    b.convert("RGB").save(f"{out}/big_end_{key}.png")
print("done", len(glob.glob(os.path.join(out, "small_end_*.png"))), "items")
