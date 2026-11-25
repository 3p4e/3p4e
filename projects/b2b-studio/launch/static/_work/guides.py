# Safe-zone check sheets for the BIG DOGMA static kit (review only, not for upload).
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1]; O = f"{S}/launch/static"; P = f"{O}/_preview"; os.makedirs(P, exist_ok=True)
BOX = json.load(open(f"{O}/_work/boxes.json"))
F = lambda n: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", n)

def dashed_rect(d, r, col, w=3, dash=18):
    x0, y0, x1, y1 = r
    for x in range(int(x0), int(x1), dash * 2):
        d.line([(x, y0), (min(x + dash, x1), y0)], fill=col, width=w); d.line([(x, y1), (min(x + dash, x1), y1)], fill=col, width=w)
    for y in range(int(y0), int(y1), dash * 2):
        d.line([(x0, y), (x0, min(y + dash, y1))], fill=col, width=w); d.line([(x1, y), (x1, min(y + dash, y1))], fill=col, width=w)

def sheet(name, zones, shade=None, extra=None):
    im = Image.open(f"{O}/{name}.png").convert("RGB"); W, H = im.size
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    if shade:  # darken what the main view crops away
        for r in shade: d.rectangle(r, fill=(0, 0, 0, 120))
    if extra: extra(d)
    im = Image.alpha_composite(im.convert("RGBA"), ov); d = ImageDraw.Draw(im)
    fs = max(12, W // 90)
    for r, col, label in zones:
        dashed_rect(d, r, col, w=max(2, W // 700)); d.text((r[0] + 8, r[1] + 6), label, fill=col, font=F(fs))
    b = BOX[name]; d.rectangle(b, outline=(80, 255, 120), width=max(1, W // 1200))
    d.text((b[2] + 6, b[1]), "logo + text", fill=(80, 255, 120), font=F(fs))
    nb = BOX.get(name + "_note")
    if nb:  # AI disclosure note
        d.rectangle(nb, outline=(0, 255, 255), width=max(1, W // 1200))
        d.text((nb[2] + 6, nb[1]), "AI note", fill=(0, 255, 255), font=F(max(10, fs * 3 // 4)))
    im.convert("RGB").save(f"{P}/{name}_safezones.jpg", quality=88); return b, nb

inside = lambda b, z: b[0] >= z[0] and b[1] >= z[1] and b[2] <= z[2] and b[3] <= z[3]

ok = {}
# Facebook 1640x624: desktop band 1640x462, mobile ~16:9 centre, conservative key-content zone 820x312
b = sheet("facebook_cover_1640x624", [((0, 81, 1639, 543), (255, 200, 60), "desktop visible 1640x462"),
          ((265, 0, 1375, 623), (90, 180, 255), "mobile visible ~1110x624"), ((410, 156, 1230, 468), (255, 90, 90), "key content 820x312")],
          shade=[(0, 0, 1640, 81), (0, 543, 1640, 624)])
b, nb = b
ok["facebook"] = inside(b, (410, 156, 1230, 468)); ok["facebook_note"] = inside(nb, (265, 81, 1375, 543)) and inside(nb, (410, 156, 1230, 468))
# YouTube 2560x1440: TV full, desktop 2560x423 band, text-and-logo safe 1546x423
b = sheet("youtube_banner_2560x1440", [((0, 508, 2559, 931), (255, 200, 60), "desktop band 2560x423"),
          ((507, 508, 2053, 931), (255, 90, 90), "text & logo safe 1546x423")], shade=[(0, 0, 2560, 508), (0, 932, 2560, 1440)])
b, nb = b
ok["youtube"] = inside(b, (507, 508, 2053, 931)); ok["youtube_note"] = inside(nb, (507, 508, 2053, 931))
# X 1500x500: avatar overlaps bottom-left (~335 px circle), some clients trim ~60 px top/bottom
b = sheet("x_header_1500x500", [((0, 60, 1499, 440), (255, 200, 60), "safe band (top/bottom trim)")],
          extra=lambda d: d.ellipse((40, 333, 375, 668), fill=(120, 120, 120, 200), outline=(255, 255, 255, 255), width=3))
b, nb = b
ok["x"] = b[1] >= 60 and b[3] <= 440 and b[0] > 375; ok["x_note"] = inside(nb, (376, 60, 1500, 440))
# LinkedIn 1128x191: company logo overlaps bottom-left (approx.), mobile trims the sides
b = sheet("linkedin_cover_1128x191", [((180, 0, 948, 190), (90, 180, 255), "safe 180-948 (logo left, mobile sides)")],
          extra=lambda d: d.rectangle((24, 115, 168, 259), fill=(120, 120, 120, 210), outline=(255, 255, 255, 255), width=2))
b, nb = b
ok["linkedin"] = b[0] >= 180 and b[2] <= 948; ok["linkedin_note"] = inside(nb, (180, 0, 948, 191))

# profile pictures: circle crop + small-size previews on dark and light UI
for n in ("profile_1080", "profile_white_bg_1080"):
    im = Image.open(f"{O}/{n}.png").convert("RGB")
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, 1079, 1079), fill=255)
    circ = Image.new("RGB", im.size, (40, 40, 44)); circ.paste(im, (0, 0), mask)
    d = ImageDraw.Draw(circ); d.ellipse((540 - 459, 540 - 459, 540 + 459, 540 + 459), outline=(255, 90, 90), width=3)
    d.text((300, 1000), "red = 85% safe circle", fill=(255, 90, 90), font=F(26))
    canvas = Image.new("RGB", (1080 + 560, 1080), (24, 24, 27)); canvas.paste(circ, (0, 0))
    y = 40
    for sz in (320, 180, 110, 40):
        for k, bg in enumerate(((24, 24, 27), (245, 245, 245))):
            tile = Image.new("RGB", (sz + 20, sz + 20), bg); sm = im.resize((sz, sz), Image.LANCZOS)
            m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse((0, 0, sz - 1, sz - 1), fill=255); tile.paste(sm, (10, 10), m)
            canvas.paste(tile, (1100 + k * (sz + 30) if sz < 320 else 1100 + k * 0, y if sz < 320 or k == 0 else y))
            if sz == 320: break
        y += sz + 40
    canvas.save(f"{P}/{n}_circlecheck.jpg", quality=88)
print(json.dumps(ok))
