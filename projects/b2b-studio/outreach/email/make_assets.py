# BD email logo lockups (owner, 2026-11-26): BD mark + "BIG" / "DOGMA" (Russo One) + "AI STUDIO | MK" (Manrope 700, gold),
# the small line exactly as wide as DOGMA. Transparent PNG, rendered at 2x. A faint dark halo behind the white letters is invisible
# on the dark email but keeps them readable if a mail app shows the image on white.
#   python3 make_assets.py <manrope.ttf (static file from the site's manrope-lat.woff2)> <out dir>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
B = "/home/user/3p4e/projects/b2b-studio/brand"; MANROPE, OUT = sys.argv[1], sys.argv[2]
GOLD, FG = (242, 193, 78), (242, 242, 244)

def mark(h, GOLD=GOLD):
    m = Image.open(f"{B}/mark_bd_M2_P3_gold.png").convert("RGB"); g = ImageOps.grayscale(m)
    g = g.crop(g.point(lambda v: 255 if v > 40 else 0).getbbox())
    mk = Image.new("RGBA", g.size, GOLD + (0,)); mk.putalpha(g.point(lambda v: max(0, min(255, int((v - 18) * 1.6)))))
    return mk.resize((round(mk.width * h / mk.height), h), Image.LANCZOS)

def tracked(d, xy, text, font, track, fill):   # draw with letter spacing, return the width; "|" is a thin rule (a glyph reads as "I")
    x, y = xy; asc = font.getbbox("M")
    for i, ch in enumerate(text):
        if ch == "|": bw = max(1, font.size * .09); d.rectangle([x + font.getlength(ch) / 2 - bw / 2, y + asc[1] - font.size * .08, x + font.getlength(ch) / 2 + bw / 2, y + asc[3] + font.size * .08], fill=fill)
        else: d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + (track if i < len(text) - 1 else 0)
    return x - xy[0]

def width(text, font, track): return sum(font.getlength(c) for c in text) + track * (len(text) - 1)

def lockup(mh, size, name, light=False):   # light=True: for white / light-mode backgrounds (near-black letters, deeper gold, white halo)
    GOLD_, FG_, HALO = ((176, 124, 14), (17, 17, 20), (255, 255, 255)) if light else (GOLD, FG, (0, 0, 0))
    R = ImageFont.truetype(f"{B}/fonts/RussoOne-400.ttf", size); tr = size * .11
    wd = width("DOGMA", R, tr)
    sm = "AI STUDIO | MK"; ss = size * .30
    M = ImageFont.truetype(MANROPE, round(ss)); M.set_variation_by_axes([700])
    st = (wd - sum(M.getlength(c) for c in sm)) / (len(sm) - 1)            # spacing that makes the small line = DOGMA's width
    mk = mark(mh, GOLD_); gap = round(size * .62); lh = size * 1.02
    th = lh * 2 + ss * 1.6; H = max(mh, round(th)) + 8; W = mk.width + gap + round(wd) + 8
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ty = (H - th) / 2
    txt = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(txt); x = mk.width + gap
    tracked(d, (x, ty), "BIG", R, tr, FG_); tracked(d, (x, ty + lh), "DOGMA", R, tr, FG_)
    tracked(d, (x + 1, ty + lh * 2 + ss * .45), sm, M, st, GOLD_)
    halo = Image.new("RGBA", im.size, HALO + (0,)); halo.putalpha(txt.getchannel("A").filter(ImageFilter.GaussianBlur(size * .08)).point(lambda v: int(v * .35)))
    im.alpha_composite(halo); im.alpha_composite(mk, (4, (H - mh) // 2)); im.alpha_composite(txt)
    im.save(f"{OUT}/{name}", optimize=True); print(name, im.size, "DOGMA", round(wd), "small line", round(width(sm, M, st)))

lockup(156, 48, "bd_logo_header.png")   # header, shown at ~half size (220 px wide)
lockup(110, 34, "bd_logo_sig.png")      # signature, shown at ~half size (150 px wide)
lockup(156, 48, "bd_logo_header_light.png", True)
lockup(110, 34, "bd_logo_sig_light.png", True)
