# Text overlays for post_hello_intro_9x16.mp4 (1080x1920): wordmark + subline, rule + tagline, AI disclosure.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; T = f"{S}/launch/static/_work/intro916"
RUSSO = f"{S}/brand/fonts/RussoOne-400.ttf"; DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H = 1080, 1920; GOLD = (242, 193, 78); WHITE = (255, 255, 255); CREAM = (236, 230, 218)

def run_width(parts, font, track):
    return sum(font.getlength(ch) + track for txt, _ in parts for ch in txt) - track

def draw_line(d, y, parts, font, track):
    """parts = [(text, rgba)], centred horizontally, manual letter-spacing"""
    x = (W - run_width(parts, font, track)) / 2
    for txt, col in parts:
        for ch in txt:
            d.text((x, y), ch, font=font, fill=col); x += font.getlength(ch) + track

def layer(draw_fn, shadow=0.75, blur=10):
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(fg))
    a = fg.getchannel("A").filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * shadow))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a)
    return Image.alpha_composite(sh, fg)

f_name, f_sub, f_tag = ImageFont.truetype(RUSSO, 112), ImageFont.truetype(RUSSO, 32), ImageFont.truetype(RUSSO, 56)
f_ai = ImageFont.truetype(DEJAVU, 30)

def name(d):
    draw_line(d, 960, [("BIG DOGMA", WHITE + (255,))], f_name, 112 * .045)
    draw_line(d, 1102, [("AI STUDIO  |  Skopje", GOLD + (255,))], f_sub, 32 * .3)
layer(name).save(f"{T}/ov_name.png")

def tag(d):
    for i in range(560):  # gold rule, fading at both ends
        a = int(190 * (1 - abs(i - 280) / 280)); d.point((260 + i, 1170), fill=GOLD + (a,))
    draw_line(d, 1196, [("AI", GOLD + (255,)), (" видео за вашиот бизнис", CREAM + (255,))], f_tag, 56 * .02)
layer(tag).save(f"{T}/ov_tag.png")

def ai(d):
    draw_line(d, 1330, [("Видео изработено со вештачка интелигенција", CREAM + (205,))], f_ai, 30 * .04)
layer(ai, shadow=.9, blur=6).save(f"{T}/ov_ai.png")
print("ok")

# 16:9 companion: AI line for brand/anim/dogma_logo_intro_1080p.mp4 (1920x1080), centred low in the frame
W, H = 1920, 1080
def ai169(d):
    draw_line(d, 950, [("Видео изработено со вештачка интелигенција", CREAM + (205,))], ImageFont.truetype(DEJAVU, 34), 34 * .04)
layer(ai169, shadow=.9, blur=6).save(f"{T}/ov_ai_169.png")
print("ok 16:9")
