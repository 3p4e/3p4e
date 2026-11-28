# Builds HTML sources for every still asset of the video kit (end cards, watermark, title card, posts)
# and a jobs.json for shoot.js. Contact data comes from brand/brand.json via contact.py: only non-empty fields are shown,
# the contact row disappears when all are empty, and outputs get a _PLACEHOLDER-CONTACT suffix while a value is a placeholder.
import base64, json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import ITEMS as CONTACT, SUFFIX
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; H = f"{W}/html"; OUT = f"{S}/launch/video"
os.makedirs(H, exist_ok=True); os.makedirs(f"{W}/png", exist_ok=True)
B = json.load(open(f"{S}/brand/brand.json"))
GOLD = B["accent"]; BG = B["bg"]
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
russo = b64(f"{S}/brand/fonts/RussoOne-400.ttf"); osw4 = b64(f"{S}/brand/fonts/Oswald-400.ttf"); osw6 = b64(f"{S}/brand/fonts/Oswald-600.ttf")
svg = open(f"{S}/brand/mark_bold.svg").read()
svg_thin = open(f"{S}/brand/mark.svg").read()
def sized(w, h): return svg.replace("<svg ", '<svg width="%d" height="%d" ' % (w, h), 1)
STILL = f"file://{W}/stills"
LOGO = f"file://{W}/stills/logo_crop.png"
GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")
DISC_MK = "Видео изработено со вештачка интелигенција"
DISC_EN = "AI-generated video"
TAGLINE = "Break the dogma."          # studio sign-off on every outro (owner 2026-11-27); English in every language
def tagline(top, fs, ls):
    rule = f'<span style="display:inline-block;width:{fs * 1.3:.0f}px;height:2px;background:var(--gold);opacity:.7;vertical-align:middle;margin:0 {fs * .55:.0f}px {fs * .12:.0f}px"></span>'
    return (f'<div class="abs c" style="top:{top}px;font-size:{fs}px;font-weight:600;letter-spacing:{ls}px;color:#f3efe6;text-transform:uppercase;'
            f'text-shadow:0 0 18px rgba(242,193,78,.35),0 2px 14px rgba(0,0,0,.6)">{rule}{TAGLINE}{rule}</div>')

def page(w, h, body, css="", transparent=False):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Russo;src:url(data:font/ttf;base64,{russo})}}
@font-face{{font-family:Osw;font-weight:400;src:url(data:font/ttf;base64,{osw4})}}
@font-face{{font-family:Osw;font-weight:600;src:url(data:font/ttf;base64,{osw6})}}
:root{{--gold:{GOLD};--bg:{BG}}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{width:{w}px;height:{h}px;overflow:hidden;position:relative;color:#fff;font-family:Osw,sans-serif;
  background:{'transparent' if transparent else 'var(--bg)'}}}
.abs{{position:absolute}} .c{{left:0;right:0;text-align:center}}
.russo{{font-family:Russo}} .gold{{color:var(--gold)}}
.grain{{position:absolute;inset:0;background-image:{GRAIN};opacity:.07;mix-blend-mode:overlay;pointer-events:none}}
.pill{{display:inline-block;background:var(--gold);color:#111;font-family:Russo;border-radius:999px;box-shadow:0 0 40px rgba(242,193,78,.35)}}
{css}</style></head><body>{body}</body></html>"""

jobs = []
def add(name, w, h, body, css="", transparent=False, out=None):
    p = f"{H}/{name}.html"; open(p, "w").write(page(w, h, body, css, transparent))
    sfx = SUFFIX if name in ("post_offer", "post_hello") else ""      # posts that carry contact details
    jobs.append({"html": p, "png": out or f"{W}/png/{name}{sfx}.png", "w": w, "h": h, "transparent": transparent})

# ---------- watermark: gold monogram, 110 px wide (+ soft dark halo for bright shots)
for name, mw in [("wm_110", 110), ("wm_96", 96)]:
    mh = round(mw * 3590 / 5776)
    add(name, mw + 24, mh + 24, f'<div class="abs" style="left:12px;top:12px;width:{mw}px;height:{mh}px;color:var(--gold);'
        f'filter:drop-shadow(0 0 3px rgba(0,0,0,.75)) drop-shadow(0 1px 6px rgba(0,0,0,.45))">{sized(mw, mh)}</div>',
        transparent=True)

# ---------- end card layers
glow = "radial-gradient(ellipse 60% 45% at 50% 32%, rgba(242,193,78,.17), rgba(242,193,78,0) 70%)"
vign = "radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)"
def endcard(tag, w, h, logo_w, logo_top, tag_top, tag_fs, head_html, head_top, head_fs, pill_top, pill_fs, contact_html, contact_top, contact_fs, disc_html, disc_top, disc_fs, disc_col="#9b978e"):
    add(f"end_{tag}_A", w, h, f'<div class="abs" style="inset:0;background:{glow}"></div><div class="abs" style="inset:0;background:{vign}"></div>'
        f'<img class="abs" src="{LOGO}" style="width:{logo_w}px;left:{(w - logo_w) // 2}px;top:{logo_top}px;filter:drop-shadow(0 0 28px rgba(242,193,78,.28))">'
        + tagline(tag_top, tag_fs, round(tag_fs * .3)) + '<div class="grain"></div>')
    add(f"end_{tag}_B", w, h, f'<div class="abs c russo" style="top:{head_top}px;font-size:{head_fs}px;line-height:1.12;letter-spacing:.5px;text-shadow:0 4px 30px rgba(0,0,0,.6)">{head_html}</div>'
        f'<div class="abs c" style="top:{pill_top}px"><span class="pill" style="font-size:{pill_fs}px;padding:{pill_fs*0.32:.0f}px {pill_fs*0.85:.0f}px">Пилот-филм од €600</span></div>', transparent=True)
    crow = (f'<div class="abs c" style="top:{contact_top}px;font-size:{contact_fs}px;font-weight:600;letter-spacing:1px;color:#ece7dc;line-height:1.5">{contact_html}</div>'
            if contact_html else "")                                   # no contact row when brand.json has no contact fields
    add(f"end_{tag}_C", w, h, crow + f'<div class="abs c" style="top:{disc_top}px;font-size:{disc_fs}px;color:{disc_col};letter-spacing:.6px;line-height:1.45">{disc_html}</div>',
        transparent=True)
dot = '<span class="gold" style="padding:0 .7em">·</span>'
endcard("16x9", 1920, 1080, 700, 150, 366, 34, "AI видео за вашиот бизнис", 470, 88, 618, 50,
        dot.join(CONTACT), 790, 38, f"{DISC_MK}{dot}{DISC_EN}", 975, 27)
# 9:16: lockup 740 px wide (x 170-910, clear of the right-hand action rail); contact lines stacked, disclosure right under them
C9_TOP = 1110; C9_H = round(len(CONTACT) * 42 * 1.5)
endcard("9x16", 1080, 1920, 740, 370, 600, 36, "AI видео за<br>вашиот бизнис", 728, 96, 984, 52,
        "<br>".join(CONTACT), C9_TOP, 42, f"{DISC_MK}<br>{DISC_EN}", C9_TOP + C9_H + (50 if CONTACT else 0), 30, disc_col="#b9b4aa")

# ---------- native 9:16 end cards for reels 01-05 (replace the DejaVu end card baked into the 9:16 film masters)
# three layers with the same flex layout (groups not in a layer are visibility:hidden, so positions match):
# A = background + monogram, B = sector title + tagline, C = turnaround claim, offer, demo note, AI disclosure
REEL_CARDS = {"construction": ("Градба", "Од празен плац до вашите клучеви."),
              "real_estate": ("Недвижности", "Живот над градот."),
              "food": ("Прехранбена индустрија", "Вкусот што го знаете."),
              "automotive": ("Автомобилска индустрија", "Направено во Македонија,<br>возено низ Европа."),
              "interior_design": ("Внатрешен дизајн", "Простор што личи на вас.")}
CLAIM = "Готов филм за 7–10 дена<br>по одобрување на клучните кадри."
reel_css = (".col{position:absolute;left:150px;right:150px;top:0;height:1800px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}"
            ".hide{visibility:hidden}"
            ".rt{font-family:Russo;font-size:84px;line-height:1.1;margin-top:44px;text-shadow:0 4px 30px rgba(0,0,0,.6)}"
            ".tg{font-size:44px;font-weight:600;line-height:1.28;color:var(--gold);margin-top:22px}"
            ".rl{width:130px;height:4px;border-radius:2px;background:var(--gold);margin:42px 0 40px}"
            ".cl{font-size:35px;line-height:1.35;color:#e9e4d9}"
            ".pl{margin-top:34px}"
            ".nt{font-size:26px;line-height:1.4;color:#a7a39a;margin-top:40px}"
            ".dc{font-size:31px;font-weight:600;line-height:1.35;color:#d6d1c6;margin-top:16px;letter-spacing:.3px}")
def reelcard(key, title, tagline):
    def col(show):
        h = lambda g: "" if g in show else " hide"
        return (f'<div class="col"><div class="{h("A")}" style="width:150px;height:93px;color:var(--gold);filter:drop-shadow(0 0 18px rgba(242,193,78,.45))">{sized(150, 93)}</div>'
                f'<div class="rt{h("B")}">{title}</div><div class="tg{h("B")}">{tagline}</div><div class="rl{h("B")}"></div>'
                f'<div class="cl{h("C")}">{CLAIM}</div>'
                f'<div class="pl{h("C")}"><span class="pill" style="font-size:40px;padding:13px 34px">Пилот-филм од €600</span></div>'
                f'<div class="nt{h("C")}">Демо концепт на студиото. Сцените се генерирани<br>и не прикажуваат вистински објект.</div>'
                f'<div class="dc{h("C")}">{DISC_MK}<br><span class="gold">{DISC_EN}</span></div></div>')
    add(f"reelend_{key}_A", 1080, 1920, f'<div class="abs" style="inset:0;background:{glow}"></div><div class="abs" style="inset:0;background:{vign}"></div>'
        + col("A") + '<div class="grain"></div>', reel_css)
    add(f"reelend_{key}_B", 1080, 1920, col("B"), reel_css, transparent=True)
    add(f"reelend_{key}_C", 1080, 1920, col("C"), reel_css, transparent=True)
for k, (t, g) in REEL_CARDS.items(): reelcard(k, t, g)

# ---------- AI disclosure on the body of reels 01-05: top blurred band, ends above the picture band (y 656) and left of the action rail
def disc_pill(top, fs_mk=33, fs_en=24):
    return (f'<div class="abs c" style="top:{top}px"><div style="display:inline-block;background:rgba(13,13,15,.66);border:1px solid rgba(242,193,78,.5);'
            'border-radius:24px;padding:13px 32px 15px;box-shadow:0 6px 30px rgba(0,0,0,.35)">'
            f'<div style="font-size:{fs_mk}px;font-weight:600;color:#fff;letter-spacing:.3px;line-height:1.25">{DISC_MK}</div>'
            f'<div style="font-size:{fs_en}px;font-weight:600;color:var(--gold);letter-spacing:3px;line-height:1.35;margin-top:2px">{DISC_EN.upper()}</div></div></div>')
add("disc_top_9x16", 1080, 1920, disc_pill(498), transparent=True)
# same pill on the showreel hook (0-4.2 s): the 9:16 showreel reuses disc_top_9x16 (above the hook text, which starts near y 780);
# 16:9: centred under the hook line (hook text ends near y 615, pill y 700-810, above the player-control strip)
add("disc_top_16x9", 1920, 1080, disc_pill(700, 36, 26), transparent=True)

# ---------- how-to title card (vertical) for reel_06; AI disclosure at y 1300-1390, like the outro (y 1320), above TikTok's caption zone (~1436)
add("howto_title_9x16", 1080, 1920,
    f'<div class="abs" style="inset:0;background:{glow}"></div><div class="abs" style="inset:0;background:{vign}"></div>'
    f'<img class="abs" src="{LOGO}" style="width:640px;left:220px;top:600px">'
    f'<div class="abs c russo" style="top:860px;font-size:78px;line-height:1.15">Како настанува<br>рекламата</div>'
    f'<div class="abs c" style="top:1075px;font-size:44px;font-weight:600;letter-spacing:2px;color:var(--gold)">ГРАДЕЖНИШТВО · ТАЈМЛАПС</div>'
    f'<div class="abs c" style="top:1300px;font-size:31px;font-weight:600;color:#cfcabf;letter-spacing:.4px;line-height:1.45">{DISC_MK}<br><span class="gold">{DISC_EN}</span></div><div class="grain"></div>')

# transparent variant of the how-to title (laid over a blurred, darkened timelapse)
add("howto_title_9x16_t", 1080, 1920,
    f'<img class="abs" src="{LOGO}" style="width:640px;left:220px;top:600px;filter:drop-shadow(0 0 24px rgba(0,0,0,.8))">'
    f'<div class="abs c russo" style="top:860px;font-size:78px;line-height:1.15;text-shadow:0 4px 30px rgba(0,0,0,.85)">Како настанува<br>рекламата</div>'
    f'<div class="abs c" style="top:1075px;font-size:44px;font-weight:600;letter-spacing:2px;color:var(--gold);text-shadow:0 2px 16px rgba(0,0,0,.9)">ГРАДЕЖНИШТВО · ТАЈМЛАПС</div>'
    f'<div class="abs c" style="top:1300px;font-size:31px;font-weight:600;color:#e2ddd2;letter-spacing:.4px;line-height:1.45;text-shadow:0 2px 10px rgba(0,0,0,.9)">{DISC_MK}<br><span class="gold">{DISC_EN}</span></div>', transparent=True)

# ---------- AI outro (owner 2026-11-27: no drawn logo ignition; the outro uses the AI logo render smoke_reveal instead).
# outro_ai.py lays the film (feathered by outro_mask_*) over the background, then these text layers fade in:
#   16:9 film 1400x770 at y 0 -> wordmark 768, studio line 878, tagline 944 (the how-to's disclosure sits at the bottom)
#   9:16 film 1240x682 at y 380 -> wordmark 1084, studio line 1196; tagline + disclosure from outro_disc_9x16
outro_bg = f'<div class="abs" style="inset:0;background:#030304"></div><div class="abs" style="inset:0;background:{glow}"></div><div class="abs" style="inset:0;background:{vign}"></div><div class="grain"></div>'
add("outro_bg_16x9", 1920, 1080, outro_bg.replace("at 50% 32%", "at 50% 36%"))
add("outro_bg_9x16", 1080, 1920, outro_bg.replace("at 50% 32%", "at 50% 38%"))
def wordmark(top, fs, sub_gap, sub_fs):
    return (f'<div class="abs c russo" style="top:{top}px;font-size:{fs}px;line-height:1;letter-spacing:2px;color:#fbf8f1;'
            f'text-shadow:0 0 26px rgba(242,193,78,.45),0 3px 18px rgba(0,0,0,.7)">BIG DOGMA</div>'
            f'<div class="abs c russo" style="top:{top + fs + sub_gap}px;font-size:{sub_fs}px;letter-spacing:{sub_fs * .22:.0f}px;color:var(--gold);'
            f'text-shadow:0 2px 12px rgba(0,0,0,.7)">AI STUDIO&nbsp;&nbsp;|&nbsp;&nbsp;Skopje</div>')
add("outro_word_16x9", 1920, 1080, wordmark(768, 96, 18, 30) + tagline(944, 38, 12), transparent=True)
add("outro_word_9x16", 1080, 1920, wordmark(1084, 104, 16, 30), transparent=True)
def mask(w, h, core=58): return f'<div class="abs" style="inset:0;background:radial-gradient(ellipse 50% 50% at 50% 50%,#fff {core}%,#000 100%)"></div>'
add("outro_mask_16x9", 1400, 770, mask(1400, 770))
add("outro_mask_9x16", 1240, 682, mask(1240, 682, 34))   # longer falloff: the smoke at the film top must not show an edge
# reel outro overlay: tagline + disclosure under the 9:16 wordmark (outro_word_9x16 ends near y 1230)
add("outro_disc_9x16", 1080, 1920, tagline(1272, 40, 12) + f'<div class="abs c" style="top:1348px;font-size:31px;font-weight:600;color:#cfcabf;letter-spacing:.4px;line-height:1.45">{DISC_MK}<br>{DISC_EN}</div>', transparent=True)

# ---------- posts 1080x1350
PW, PH = 1080, 1350
post_css = f"""
.bgglow{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 15% 0%, rgba(242,193,78,.16), rgba(242,193,78,0) 65%),
  radial-gradient(ellipse 70% 40% at 100% 100%, rgba(242,193,78,.08), rgba(242,193,78,0) 70%)}}
.head{{position:absolute;left:72px;top:64px;right:72px;height:70px;display:flex;align-items:center;justify-content:space-between}}
.head img{{height:64px}}
.kick{{font-size:24px;font-weight:600;letter-spacing:4px;color:var(--gold);text-transform:uppercase}}
.foot{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:flex-end;font-size:24px;color:#a7a39a;letter-spacing:.5px}}
.rule{{position:absolute;left:72px;right:72px;height:1px;background:linear-gradient(90deg,rgba(242,193,78,.7),rgba(242,193,78,0))}}
"""
foot_contact = '<div>' + '<span class="gold" style="padding:0 .6em">·</span>'.join(CONTACT) + '</div>'   # empty div when there is no contact

# offer card
tiers = [("Пилот", "1 филм 20–30 с · 16:9 + 9:16<br>музика, лого, повик за акција", "€600", "", False),
         ("Лансирање", "Главен филм 45–60 с + 3 спота<br>+ 10 кратки клипови за мрежи", "€1.800", "", True),
         ("Месечна содржина", "6–8 нови клипови секој месец<br>минимум 3 месеци", "€400", "/месец", False)]
cards = ""
for i, (n, d, p, per, hot) in enumerate(tiers):
    top = 560 + i * 196
    brd = "border:2px solid var(--gold);box-shadow:0 0 50px rgba(242,193,78,.18), inset 0 0 60px rgba(242,193,78,.06)" if hot else "border:1px solid rgba(255,255,255,.14)"
    badge = '<span style="position:absolute;top:-17px;left:40px;background:var(--gold);color:#111;font-family:Russo;font-size:20px;padding:5px 16px;border-radius:999px">ПРЕПОРАЧАН</span>' if hot else ""
    cards += (f'<div class="abs" style="left:72px;right:72px;top:{top}px;height:170px;border-radius:22px;background:rgba(255,255,255,.035);{brd}">{badge}'
              f'<div class="abs russo" style="left:40px;top:30px;font-size:44px">{n}</div>'
              f'<div class="abs" style="left:40px;top:92px;font-size:25px;line-height:1.3;color:#bdb8ad">{d}</div>'
              f'<div class="abs" style="right:40px;top:44px;text-align:right"><div style="font-size:24px;color:#a7a39a;letter-spacing:2px">ОД</div>'
              f'<div class="russo gold" style="font-size:66px;line-height:1">{p}<span style="font-size:26px;color:#d9c48c">{per}</span></div></div></div>')
add("post_offer", PW, PH,
    f'<div class="bgglow"></div><div class="head"><img src="{LOGO}"><div class="kick">Понуда</div></div><div class="rule" style="top:160px"></div>'
    f'<div class="abs kick" style="left:72px;top:215px">AI видео продукција · Скопје</div>'
    f'<div class="abs russo" style="left:72px;top:262px;font-size:96px;line-height:1.06">AI видео<br>за вашиот <span class="gold">бизнис</span></div>'
    f'<div class="abs" style="left:72px;top:482px;font-size:28px;color:#cfcabf">Готов филм за 7–10 дена по одобрување на клучните кадри.</div>'
    f'{cards}'
    f'<div class="abs" style="left:72px;right:72px;top:1158px;font-size:22px;color:#8f8b83;line-height:1.4">1 рунда корекции · цени во евра без ДДВ · секое видео е означено како изработено со AI</div>'
    f'<div class="foot">{foot_contact}<div class="gold" style="font-family:Russo;font-size:24px">Пишете ни →</div></div><div class="grain"></div>', post_css)

# process carousel (the developer demo: br_c09 clip + timelapse_developer film, a generic low-rise suburb)
def frame_img(src, l, t, w, h, extra=""):
    return (f'<div class="abs" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;border-radius:24px;overflow:hidden;'
            f'box-shadow:0 30px 80px rgba(0,0,0,.6), 0 0 0 1px rgba(255,255,255,.12)"><img src="{src}" style="width:100%;height:100%;object-fit:cover;display:block">{extra}</div>')
def chip(txt, l, t, fs=22):
    return f'<div class="abs" style="left:{l}px;top:{t}px;background:rgba(13,13,15,.78);border:1px solid rgba(242,193,78,.6);color:var(--gold);font-family:Russo;font-size:{fs}px;padding:8px 16px;border-radius:999px;letter-spacing:1px">{txt}</div>'
def dots(k):
    return "".join(f'<span style="display:inline-block;width:{44 if i == k else 14}px;height:14px;border-radius:7px;margin-right:10px;background:{"var(--gold)" if i == k else "rgba(255,255,255,.25)"}"></span>' for i in range(3))
steps = [
    ("Клучен кадар", "Од ваша фотографија или рендер правиме<br>клучен кадар. Го одобрувате пред анимацијата.",
     frame_img(f"{STILL}/dev_kf.png", 72, 500, 936, 540) + chip("КЛУЧЕН КАДАР · ЗА ОДОБРУВАЊЕ", 100, 528)),
    ("AI анимација", "Вештачката интелигенција го оживува кадарот —<br>кран, скеле, кат по кат, фаза по фаза.",
     frame_img(f"{STILL}/dev_anim_3.0.png", 72, 500, 936, 540,
               '<div class="abs" style="left:0;right:0;bottom:0;height:120px;background:linear-gradient(0deg,rgba(0,0,0,.75),rgba(0,0,0,0))"></div>'
               '<div class="abs" style="left:32px;right:32px;bottom:34px;height:8px;border-radius:4px;background:rgba(255,255,255,.25)"><div style="width:42%;height:100%;border-radius:4px;background:var(--gold)"></div></div>'
               '<div class="abs" style="left:calc(32px + 42% - 12px);bottom:26px;width:24px;height:24px;border-radius:12px;background:#fff;box-shadow:0 0 16px rgba(242,193,78,.9)"></div>')
     + chip("▶ AI ВИДЕО", 100, 528)),
    ("Готова реклама", "Монтажа, глас на македонски, музика и лого —<br>во 16:9 и 9:16, подготвено за мрежи.",
     frame_img(f"{STILL}/dev_final.png", 72, 500, 780, 439) + frame_img(f"{STILL}/dev_final_916.png", 770, 560, 238, 423) + chip("16:9", 100, 528) + chip("9:16", 852, 1000)),
]
for k, (title, desc, visual) in enumerate(steps):
    cta = ('<div class="gold" style="font-family:Russo;font-size:24px">Повлечете →</div>' if k < 2 else
           '<div class="gold" style="font-family:Russo;font-size:26px">Пилот-филм од €600</div>')
    add(f"post_process_{k + 1}", PW, PH,
        f'<div class="bgglow"></div><div class="head"><img src="{LOGO}"><div class="kick">Како работиме · {k + 1}/3</div></div><div class="rule" style="top:160px"></div>'
        f'<div class="abs russo" style="left:60px;top:170px;font-size:300px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(242,193,78,.85)">{k + 1}</div>'
        f'<div class="abs russo" style="left:300px;top:250px;font-size:80px;line-height:1.05">{title}</div>'
        f'<div class="abs" style="left:302px;top:362px;font-size:29px;line-height:1.38;color:#cfcabf">{desc}</div>'
        f'{visual}'
        f'<div class="abs" style="left:72px;top:1090px;font-size:21px;color:#8f8b83;letter-spacing:.4px">Демо на студиото · визуелите се генерирани со вештачка интелигенција</div>'
        f'<div class="foot"><div>{dots(k)}</div>{cta}</div><div class="grain"></div>', post_css)

# hello / brand intro
add("post_hello", PW, PH,
    f'<div class="bgglow"></div>'
    f'<div class="abs" style="inset:0;background:radial-gradient(ellipse 55% 35% at 50% 34%, rgba(242,193,78,.20), rgba(242,193,78,0) 70%)"></div>'
    f'<div class="abs" style="left:190px;top:200px;width:700px;height:435px;color:var(--gold);filter:drop-shadow(0 0 22px rgba(242,193,78,.55)) drop-shadow(0 0 70px rgba(242,140,40,.35))">'
    f'{sized(700, 435)}</div>'
    f'<div class="abs c russo" style="top:735px;font-size:82px;line-height:1.12">Здраво,<br>ние сме <span class="gold">BIG DOGMA</span></div>'
    f'<div class="abs c" style="top:950px;left:90px;right:90px;font-size:32px;line-height:1.38;color:#d8d3c8">Правиме AI видео реклами за бизниси —<br>готов филм за 7–10 дена по одобрување<br>на клучните кадри.</div>'
    f'<div class="abs c" style="top:1128px;font-size:23px;font-weight:600;letter-spacing:3px;color:#a7a39a">ГРАДЕЖНИШТВО · НЕДВИЖНОСТИ · ХРАНА · ВИНО · ИНДУСТРИЈА</div>'
    f'<div class="foot" style="justify-content:center;gap:0">{foot_contact}</div>'
    f'<div class="abs c" style="top:64px;font-size:24px;font-weight:600;letter-spacing:6px;color:var(--gold)">AI STUDIO  |  SKOPJE</div><div class="grain"></div>', post_css)

json.dump(jobs, open(f"{W}/jobs.json", "w"), indent=1)
print(len(jobs), "jobs")
