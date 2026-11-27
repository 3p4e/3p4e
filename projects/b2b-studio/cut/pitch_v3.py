# Pitch pages v3 (owner, 2026-11-26): every private company page looks like bigdogma.tech.
#  1. splash: fullscreen BD logo films (streamed from bigdogma.tech), the animated header logo, "prepared for <company>" + short info;
#  2. one click -> burst/flash transition -> the company's content: their films (16:9 + 9:16), AI shots, key frame -> motion,
#     concept stills, a ready-to-run 4-week campaign package, the offer, matching industry films and the whole BD gallery.
# The company's own files stay where they are in its token folder (the old page is kept as classic.html); BD media and the header
# engine are loaded from bigdogma.tech (CORS is allowed for pitch.bigdogma.tech in launch/site_work/site_nginx.conf).
#   python3 pitch_v3.py <company key> <out dir>     (reads the company config below, writes <out dir>/index.html)
import os, sys, json, html, glob, urllib.parse
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__)); P = "/home/user/3p4e/projects/b2b-studio"
sys.path.insert(0, f"{P}/logo_ai"); import bd_titles as BDT
SCR = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"   # built site (which industry films are live)
SITE = "https://bigdogma.tech"; MAIL = "inf.unit@bigdogma.tech"

# ------------------------------------------------------------------ strings (company language)
T = {"mk": dict(
  for_="Подготвено за", lead="AI видео студио од Скопје. Реклами и брендирани филмови без снимање: готови за 7–10 дена по одобрување на клучните кадри.",
  pts=["{n} AI филмови направени само за вас", "Предлог-распоред за објава за 4 недели", "16:9 и вистинска 9:16 верзија за телефон"], pt_nv="16:9 за YouTube, веб и екрани",
  f_p_nv="Филмовите се во 16:9 за YouTube, веб и екрани.", enter="Отворете ја презентацијата",
  scroll="Сите кадри на оваа страница се генерирани со AI.",
  nav=[("films", "Филмови"), ("shots", "Кадри"), ("campaign", "Распоред"), ("offer", "Понуда"), ("dl", "Преземање"), ("bd", "BD галерија")], cta="Закажи 15 минути",
  h1="Концепт-видео за <em>{c}</em>", sub="Сè на оваа страница е направено со AI специјално за вас: филмови, кадри, клучни кадри и предлог-распоред за објава.",
  f_e="Филмови", f_h="{n} филмови за {c}", f_p="Филмовите се во 16:9 (YouTube, веб, екрани). Со копчето 9:16 ги гледате вертикалните верзии: секој кадар е генериран одново за телефон, не исечен од хоризонталниот филм.",
  h169="16:9", v916="9:16", play="Пушти",
  v_e="9:16 за Reels, TikTok и Stories", v_h="Генерирано за телефон", v_p="Секој кадар е генериран одново во вертикален формат: главниот мотив е блиску и го полни екранот, а текстовите стојат над копчињата на апликациите. Истиот глас и музика.", gif="Тизер · GIF",
  s_e="Секој кадар", s_h="Сите AI кадри", s_p="{n} кадри генерирани специјално за {c}. Поминете со глувчето (или допрете) за да оживеат.", mont="Сите кадри во еден монтаж",
  k_e="AI процес", k_h="Од клучен кадар до движење", k_p="Прво го одобрувате статичниот клучен кадар, па AI го анимира. Повлечете за да споредите.", img="Слика", vid="AI видео",
  a_e="Следен концепт", a_h="Акциски клучни кадри", a_p="Клучни кадри за следниот филм, подготвени за ваше одобрување пред анимација.",
  c_e="Предлог за објава", c_h="Предлог-распоред за 4 недели, со готови текстови", c_p="Како можете да ги објавите филмовите на вашите канали: ден, канал, формат и текст со хаштагови. Објавувањето е ваше: ние ја изработуваме содржината.",
  c_cols=["Ден", "Канал", "Формат", "Филм", "Текст за објава"], week="Недела",
  o_e="Понуда", i_e="Од вашата индустрија", i_h="Уште AI филмови од вашата индустрија", i_p="Примери од нашето студио кои можеме да ги прилагодиме за вас.",
  b_e="BD галерија", b_h="Што може AI со едно лого", b_p="{n} филмови и ефекти со нашето лого: материјали, светлина, природа, магија. Истото можеме за вашето лого.",
  b_all="Сите", b_f="Лого филмови", b_x="Лого ефекти",
  end_h="Следен чекор: 15 минути разговор", end_p="Во Скопје или онлајн. Кажете ни кој филм ви се допаѓа најмногу: го прилагодуваме за вашата кампања.",
  mail="Пишете ни", legal="Концепт само за презентација. Не е објавен и нема да биде објавен без ваше изречно писмено одобрение. Видеата се изработени со вештачка интелигенција. Логата и марките им припаѓаат на нивните сопственици.",
  close="Затвори", subj="{c} - Закажи 15 минути", dl_e="Преземање", dl_h="Понуда за преземање",
  dl_p="Деталната понуда во PDF. Филмовите ги гледате на оваа страница.", dl_pdf="Понуда (PDF)", dl_zip="Сите филмови (ZIP, {s} MB)", b_f1="Лого филм", b_x1="Лого ефект", days=["Пон", "Вто", "Сре", "Чет", "Пет", "Саб", "Нед"], more="Повеќе на",
  ind_types={"social": "9:16", "explainer": "Објаснувачки", "story": "Приказна", "transform": "Пред / потоа", "commercial": "Реклама"}, ai_film="AI филм")}
for _l in ("sr", "sq"): T[_l] = json.load(open(f"{HERE}/pitch_v3_data/strings_{_l}.json", encoding="utf-8"))   # written by hand 2026-11-26
# H3 section strings (geo-gated, see cut/h3_geo)
H3S = {"mk": {"h3_e": "Made with MiniMax H3", "h3_h": "Уште филмови за {c}", "h3_p": "Дополнителни AI филмови направени со моделот MiniMax H3, хоризонтално и вертикално. Се прикажуваат само во региони каде што лиценцата на моделот го дозволува тоа.", "h3_ad": "Реклама", "h3_film": "Филм", "h3_lbl": "AI · Made with MiniMax H3"}, "sr": {"h3_e": "Made with MiniMax H3", "h3_h": "Još filmova za {c}", "h3_p": "Dodatni AI filmovi napravljeni modelom MiniMax H3, horizontalno i vertikalno. Prikazuju se samo u regionima u kojima licenca modela to dozvoljava.", "h3_ad": "Reklama", "h3_film": "Film", "h3_lbl": "AI · Made with MiniMax H3"}, "sq": {"h3_e": "Made with MiniMax H3", "h3_h": "Më shumë filma për {c}", "h3_p": "Filma shtesë AI të krijuar me modelin MiniMax H3, horizontalisht dhe vertikalisht. Shfaqen vetëm në rajonet ku licenca e modelit e lejon.", "h3_ad": "Reklamë", "h3_film": "Film", "h3_lbl": "AI · Made with MiniMax H3"}}
for _l in H3S: T[_l].update(H3S[_l])
XL = json.load(open(f"{P}/launch/site_work/i18n_extra.json", encoding="utf-8"))   # site translations (BD and industry film titles)

# ------------------------------------------------------------------ companies
def foton():
    sys.path.insert(0, f"{P}/foton_v2"); from films import FILMS as FV
    films = [dict(id="foton_tunland_v9_specs", t="Tunland V9: моќ и спецификации", l="Моќ, погон и спецификации во 48 секунди.", src="foton_tunland_v9_specs.mp4", v="foton_tunland_v9_specs_9x16.mp4", poster="foton_tunland_v9_specs.jpg"),
             dict(id="foton_showreel_v2", t="Foton: целата палета", l="Целата палета на Foton во еден филм.", src="foton_showreel_v2.mp4", v="foton_showreel_v2_9x16.mp4", poster="foton_showreel_v2.jpg")]
    for f in FV:
        films.append(dict(id=f["id"], t=f"{f['title']} · Tunland {f['model']}", l=f["card"][1], src=f"v2/f/{f['id']}.mp4", v=f"v2/f/{f['id']}_9x16.mp4", poster=f"v2/f/{f['id']}.jpg", vposter=f"v2/f/{f['id']}_9x16.jpg"))
    caps = json.load(open(f"{HERE}/pitch_v3_data/foton_caps.json", encoding="utf-8"))
    return dict(key="foton", name="Foton Македонија", lang="mk", accent="#d71920", films=films, caps=caps, shots=27, stills=10, gifs=2,
                industry=["automotive", "product_launch"], tags="#Foton #Tunland #4x4 #Пикап #Македонија #Скопје", cta_site="foton.mk",
                skip_shots={19, 20, 21, 22}, skip_ind={"cf_automotive_1_social"})   # Auman, Aumark, EME4, cargo van; a sports car: Tunland only (owner)
import re
CO = {  # key: (industry categories on bigdogma.tech, hashtags)
 "01_zito_marketi_MK": (["food", "horeca"], "#Жито #Маркети #Македонија #Скопје"), "02_alkaloid_MK": (["pharma", "health"], "#Алкалоид #Здравје #Македонија"),
 "03_replek_MK": (["pharma", "health"], "#Реплек #Здравје #Македонија"), "04_vincinni_MK": (["food", "product_launch"], "#Винчини #Македонија"),
 "06_beograd_na_vodi_RS": (["real_estate", "developer"], "#BeogradNaVodi #Beograd #Srbija"), "07_millennium_team_RS": (["construction", "steel_cement"], "#MillenniumTeam #Beograd #Srbija"),
 "08_nelt_RS": (["industry_showreel", "food"], "#Nelt #Logistika #Srbija"), "09_gener2_AL": (["construction", "developer"], "#Gener2 #Tirana #Shqipëri"),
 "10_concord_AL": (["real_estate", "developer"], "#Concord #Tirana #Shqipëri"), "11_viva_fresh_XK": (["food", "horeca"], "#VivaFresh #Prishtina #Kosova"),
 "12_speeex_XK": (["industry_showreel", "it"], "#Speeex #Prishtina #Kosova"),
 "13_telekom_MK": (["telecom", "it"], "#МакедонскиТелеком #Magenta1 #Македонија")}
SCRP = f"{SCR}/pv3"
def generic(cid):
    old = open(f"{SCRP}/{cid}/classic.html", encoding="utf-8").read(); files = open(f"{SCRP}/{cid}/files.txt").read().split()
    lang = re.search(r'<html lang="(\w+)"', old).group(1); name = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>.*?<em>(.*?)</em>", old, re.S).group(1))).strip()
    acc = (re.findall(r"--(?:ac|co|accent)\s*:\s*(#[0-9a-fA-F]{3,6})", old) or ["#f2c14e"])[0]
    films = []
    for a in re.findall(r'<article class="film.*?</article>', re.search(r'<section id="films".*?</section>', old, re.S).group(0), re.S):
        src = re.search(r'<video[^>]*\ssrc="([^"]+)"', a).group(1); poster = re.search(r'poster="([^"]+)"', a).group(1)
        t = html.unescape(re.search(r"<h3>(.*?)</h3>", a).group(1)); t = re.sub(r"\s*\([^)]*\)\s*$", "", t).strip()
        v = re.search(r'data-v="1" data-src="([^"]+)"', a); films.append(dict(id=src[:-4], t=t, l=t, src=src, v=v.group(1) if v else None, poster=poster))
    caps = {}
    sec = re.search(r'<section id="shots"(.*?)</section>', old, re.S)
    if sec:
        for f in re.findall(r"<figure.*?</figure>", sec.group(1), re.S):
            c = re.search(r"x/(c\d\d)\.jpg", f)
            if c: caps[c.group(1)] = [x.strip() for x in re.sub(r"<[^>]+>", "|", html.unescape(f)).split("|") if x.strip()]
    n = lambda pre, ext: len([f for f in files if re.fullmatch(pre + r"\d\d" + ext, f)])
    ind, tags = CO[cid]
    return dict(key=cid, name=name, lang=lang, accent=acc, films=films, caps=caps, shots=n("c", r"\.mp4"), stills=n("a", r"\.jpg"), gifs=len([f for f in files if re.fullmatch(r"t\d\.gif", f)]),
                keys=n("k", r"\.jpg"), industry=ind, tags=tags, cta_site=None)
COMPANIES = {"foton": foton, **{k: (lambda k=k: generic(k)) for k in CO}}

# ------------------------------------------------------------------ campaign: 4 weeks from the company's films
def campaign(c, s):
    F = c["films"]; rows = []; slots = [(0, "YouTube + Facebook", "16:9"), (1, "Instagram Reels + TikTok", "9:16"), (3, "Instagram + Facebook Stories", "9:16"), (5, "Reels + TikTok", "9:16")]
    order = F[2:] + F[:2] if len(F) > 6 else F
    if len(F) < 6 and c.get("shots"):   # few films: alternate them with single AI shots as short teaser posts
        sh = [dict(t=(c["caps"].get(f"c{i:02d}", ["", f"AI {i:02d}"])[1] if len(c["caps"].get(f"c{i:02d}", [])) > 2 else f"AI {i:02d}"), l=(c["caps"].get(f"c{i:02d}", [""])[-1] or F[0]["l"]), src=f"x/c{i:02d}.mp4", v=None) for i in range(1, c["shots"] + 1, 2)]   # t: the shot's own label
        order = [x for pair in zip(sh, F * 8) for x in pair]
    k = 0
    for w in range(4):
        for d, ch, fm in slots:
            f = order[k % len(order)]; k += 1
            cap = f"{f['l']} {(s['more'] + ' ' + c['cta_site'] + '.') if c.get('cta_site') else ''} {c['tags']}".replace("  ", " ").strip()
            rows.append((w + 1, s["days"][d], ch, fm, f, cap))
    tb = []
    for w in range(1, 5):
        tb.append(f'<tr class="wk"><th colspan="5">{s["week"]} {w}</th></tr>')
        for ww, d, ch, fm, f, cap in rows:
            if ww != w: continue
            tb.append(f'<tr><td>{d}</td><td>{E(ch)}</td><td><span class="fm">{fm if f.get("v") else "16:9"}</span></td><td><a href="#" data-play="{(f.get("v") or f["src"]) if fm == "9:16" else f["src"]}" data-t="{E(f["t"])}">{E(f["t"])}</a></td><td class="cap">{E(cap)}</td></tr>')
    head = "".join(f"<th>{E(x)}</th>" for x in s["c_cols"])
    # owner, 2026-11-26: no paid-promotion tiers and no KPI list (BIG DOGMA sells content; the client publishes it)
    return f'''<div class="tw"><table class="plan"><thead><tr>{head}</tr></thead><tbody>{"".join(tb)}</tbody></table></div>'''

# ------------------------------------------------------------------ page
# films with a native vertical version (generated for 9:16, not the 16:9 film on a blurred background): id -> (file, poster)
NATIVE_V = {"foton_tunland_v9_specs": ("foton_tunland_v9_specs_9x16.mp4", "foton_tunland_v9_specs_9x16.jpg"),   # vertical/ pilot 2026-11-26
            "foton_showreel_v2": ("foton_showreel_v2_9x16.mp4", "foton_showreel_v2_9x16.jpg")}
_NV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vertical", "native_v.json")   # the 11 other companies' films, as uploaded (vertical/upload_v.py)
if os.path.exists(_NV): NATIVE_V.update({k: (f"{k}_9x16.mp4", f"{k}_9x16.jpg") for k in json.load(open(_NV))})
def build(key, out):
    c = COMPANIES[key](); s = dict(T[c["lang"]]); n_f = len(c["films"]); name = E(c["name"])
    for f in c["films"]:   # drop blur-fill 9:16 files
        nv = NATIVE_V.get(f.get("id") or os.path.basename(f["src"])[:-4])
        if nv: f["v"], f["vposter"] = nv
        else: f.pop("v", None); f.pop("vposter", None)
    has_v = any(f.get("v") for f in c["films"])
    if not has_v: s["pts"] = s["pts"][:2] + [s["pt_nv"]]; s["f_p"] = s["f_p_nv"]
    old = open(f"{SCRP}/{key}/classic.html", encoding="utf-8").read() if key != "foton" else open(f"{out}/classic.html", encoding="utf-8").read() if os.path.exists(f"{out}/classic.html") else open(f"{out}/index.html", encoding="utf-8").read()
    import re
    offer = re.search(r'<section id="offer".*?</section>', old, re.S).group(0)
    # BD gallery and splash playlist (public files on bigdogma.tech)
    tl = lambda key, v: (v if c["lang"] == "mk" else (XL.get(c["lang"], {}).get(key, "BD · " + v[1])[5:], v[1]))
    live = lambda rel: os.path.exists(f"{SCR}/launch/site/{rel}.mp4")
    bd = [(f"{SITE}/media/intro/{k}", tl(f"bd_{k}.t", v), "f") for k, v in BDT.FILMS.items() if live(f"media/intro/{k}")] + [(f"{SITE}/media/bd/{k}", tl(f"bdx_{k}.t", v), "x") for k, v in BDT.FX.items() if live(f"media/bd/{k}")]
    intro = [f"{SITE}/media/lite/intro/{k}.mp4" for k in BDT.FILMS if os.path.exists(f"{SCR}/launch/site/media/lite/intro/{k}.mp4")]   # light copies
    # industry films (bigdogma.tech, category films v2)
    ind = []
    for cat in c["industry"]:
        p = f"{P}/catfilms/plan/{cat}.json"
        if os.path.exists(p):
            for f in json.load(open(p, encoding="utf-8"))["films"]:
                if os.path.exists(f"{SCR}/launch/site/films/{f['id']}.mp4") and f["id"] not in c.get("skip_ind", ()): ind.append((f"{SITE}/films/{f['id']}", (f["title_mk"] if c["lang"] == "mk" else XL.get(c["lang"], {}).get(f"{f['id']}.t", f["title_en"])), (f["line_mk"] if c["lang"] == "mk" else XL.get(c["lang"], {}).get(f"{f['id']}.l", f["line_en"])), f["type"]))
    def card(src, poster, t, l, tag, v=None, vposter=None):
        dv = f' data-v="{v}" data-vp="{vposter or poster}"' if v else ""
        return (f'<li class="fc"><a href="{src}" data-play="{src}" data-t="{E(t)}" data-p="{poster}"{dv}><span class="im"><img src="{poster}" alt="" loading="lazy">'
                f'<span class="ct">{E(tag)}</span><span class="pl"></span></span><span class="tx"><b>{E(t)}</b><span>{E(l)}</span></span></a></li>')
    films = "".join(card(f["src"], f["poster"], f["t"], f["l"], s["ai_film"], f.get("v"), f.get("vposter")) for f in c["films"])
    vert = "".join(f'<li><video data-src="{f["v"]}" poster="{f.get("vposter", f["poster"])}" muted loop playsinline preload="none"></video><span>{E(f["t"])}</span></li>' for f in c["films"] if f.get("v"))
    vert += "".join(f'<li class="gif"><img src="x/t{i}.gif" alt="" loading="lazy"><span>{E(s["gif"])}</span></li>' for i in range(1, c["gifs"] + 1))
    SHOTS = [i for i in range(1, c["shots"] + 1) if i not in c.get("skip_shots", ())]
    shots = "".join(f'<li><video data-src="x/c{i:02d}.mp4" poster="x/c{i:02d}.jpg" muted loop playsinline preload="none"></video><span><b>{E(c["caps"].get(f"c{i:02d}", ["", ""])[1] if len(c["caps"].get(f"c{i:02d}", [])) > 1 else f"{i:02d}")}</b> {E(c["caps"].get(f"c{i:02d}", ["", "", ""])[-1])}</span></li>' for i in SHOTS)
    pairs = "".join(f'<li class="cmp" style="--x:50%"><video data-src="x/c{i:02d}.mp4" muted loop playsinline preload="none" poster="x/c{i:02d}.jpg"></video><img src="x/k{i:02d}.jpg" alt="" loading="lazy"><input type="range" min="0" max="100" value="50" aria-label="{E(s["img"])} / {E(s["vid"])}"><span class="l">{E(s["img"])}</span><span class="r">{E(s["vid"])}</span></li>' for i in [x for x in (1, 4, 7, 10, 13, 16) if x <= c.get("keys", 27)])
    stills = "".join(f'<li><img src="x/a{i:02d}.jpg" alt="" loading="lazy"></li>' for i in range(1, c["stills"] + 1))
    indc = "".join(card(f"{u}.mp4", f"{u}.jpg", t, l, s["ind_types"][ty]) for u, t, l, ty in ind)
    bdc = "".join(f'<li class="fc" data-k="{k}"><a href="{u}.mp4" data-play="{u}.mp4" data-t="BD · {E(m)}" data-p="{u}.jpg"><span class="im"><img src="{u}.jpg" alt="" loading="lazy"><span class="ct">{s["b_f1"] if k == "f" else s["b_x1"]}</span><span class="pl"></span></span><span class="tx"><b>BD · {E(m)}</b></span></a></li>' for u, (m, e), k in bd)
    stills_sec = (f'<section><div class="wrap"><div class="eyebrow rv">{E(s["a_e"])}</div><h2 class="sh rv">{E(s["a_h"])}</h2><p class="sp rv">{E(s["a_p"])}</p><ul class="stills">{stills}</ul></div></section>') if c["stills"] else ""
    mont = '<div class="mont rv"><video controls muted playsinline controlslist="nodownload" disablepictureinpicture preload="none" poster="x/m.jpg"><source src="x/m.mp4" type="video/mp4"></video></div>' if c["shots"] else ""
    mailto = f"mailto:{MAIL}?subject=" + urllib.parse.quote(s["subj"].format(c=c["name"]))
    pts = "".join(f"<li>{E(x.format(n=n_f))}</li>" for x in s["pts"])
    navl = "".join(f'<a href="#{a}">{E(b)}</a>' for a, b in s["nav"])
    page = f'''<!doctype html><html lang="{c["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>BIG DOGMA × {name}</title><link rel="icon" href="icon.png">
<style>
@font-face{{font-family:R;src:url(russo.ttf) format("truetype");font-display:swap}}
@font-face{{font-family:M;src:url({SITE}/manrope-cyr.woff2) format("woff2");unicode-range:U+0400-04FF;font-display:swap}}
@font-face{{font-family:M;src:url({SITE}/manrope-lat.woff2) format("woff2");font-display:swap}}
:root{{--bg:#0b0b0d;--sf:#141418;--sf2:#1b1b21;--fg:#f2f2f4;--mu:#a2a2ad;--ac:#f2c14e;--co:{c["accent"]};--line:rgba(255,255,255,.1)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}html{{background:var(--bg)}}body{{margin:0;background:transparent;color:var(--fg);font:16px/1.55 M,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
body.lock{{overflow:hidden}}a{{color:inherit}}img,video{{max-width:100%;display:block}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 20px}}
/* MiniMax H3 mark on H3 thumbnails (the only H3 attribution on the page) */
.h3m{{position:absolute;right:8px;bottom:8px;height:13px;width:auto;z-index:2;pointer-events:none;filter:drop-shadow(0 0 3px rgba(0,0,0,.6))}}.vrow li{{position:relative}}
/* nav + header logo (same engine as bigdogma.tech) */
.nav{{position:fixed;top:0;left:0;right:0;z-index:30;transition:background .3s}}.nav.s{{background:rgba(11,11,13,.86);backdrop-filter:blur(14px);box-shadow:0 1px 0 var(--line)}}
.nav .wrap{{display:flex;align-items:center;gap:18px;height:72px}}
.brand{{display:flex;align-items:center;gap:8px;text-decoration:none;flex:none}}.brand .lfx{{position:relative;display:block;width:80px;height:52px}}.brand .lfx-in{{position:absolute;inset:-6px -10px;pointer-events:none;-webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent),linear-gradient(180deg,transparent,#000 10%,#000 90%,transparent);-webkit-mask-composite:source-in;mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent),linear-gradient(180deg,transparent,#000 10%,#000 90%,transparent);mask-composite:intersect}}
.brand .bt{{display:flex;flex-direction:column;justify-content:center;align-items:flex-start;text-align:left;line-height:.92;gap:1px}}.brand .bt b{{font:400 19px R,sans-serif;letter-spacing:.11em}}
.brand .bt small{{font:700 8.5px/1.2 M,sans-serif;letter-spacing:.2em;color:var(--ac);margin-top:3px;white-space:nowrap}}.sep{{display:inline-block;width:1px;height:.95em;background:currentColor;opacity:.7;margin:0 .55em;vertical-align:-.12em}}
.links{{display:flex;gap:20px;margin-left:auto;font-weight:600;font-size:14.5px}}.links a{{text-decoration:none;opacity:.86}}.links a:hover{{opacity:1;color:var(--ac)}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:999px;padding:13px 24px;font:700 15px M,sans-serif;text-decoration:none;border:0;cursor:pointer}}
.btn.a{{background:var(--ac);color:#111;box-shadow:0 0 0 0 rgba(242,193,78,.5);animation:pulse 2.6s infinite}}.btn.b{{background:transparent;color:var(--fg);border:1px solid rgba(255,255,255,.3)}}
@keyframes pulse{{70%{{box-shadow:0 0 0 14px rgba(242,193,78,0)}}100%{{box-shadow:0 0 0 0 rgba(242,193,78,0)}}}}
.nav .btn{{padding:10px 18px;font-size:14px}}
@media(max-width:980px){{.links{{display:none}}.nav .btn{{margin-left:auto}}}}
@media(max-width:420px){{.brand .bt b{{font-size:16px}}.brand .lfx{{width:66px;height:44px}}.nav .btn{{padding:9px 13px;font-size:13px}}}}
/* splash */
#splash{{position:fixed;inset:0;z-index:20;background:#000;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden;transition:opacity .9s .25s,visibility 0s 1.2s}}
#splash.out{{opacity:0;visibility:hidden}}#splash video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none;transition:opacity 1s}}
#splash .shade{{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,.35),rgba(0,0,0,.82) 75%)}}
.sp-in{{position:relative;z-index:2;max-width:760px;padding:90px 20px 30px}}
.for{{text-transform:uppercase;letter-spacing:.3em;font-size:13px;color:var(--ac);margin:0 0 10px;font-weight:700}}
#splash h1{{font:400 clamp(34px,6vw,76px)/1.05 R,sans-serif;margin:0 0 18px;text-shadow:0 4px 40px rgba(0,0,0,.8)}}
.lead{{font-size:clamp(16px,1.7vw,19px);color:#e8e8ec;margin:0 auto 18px;max-width:58ch}}
.pts{{list-style:none;padding:0;margin:0 0 28px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}.pts li{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:7px 14px;font-size:14px;backdrop-filter:blur(6px)}}
.note{{font-size:12.5px;color:var(--mu);margin-top:22px}}#burst{{position:fixed;inset:0;width:100%;height:100%;z-index:40;pointer-events:none}}
/* sections */
.hero{{position:relative;min-height:92vh;display:flex;align-items:flex-end;overflow:hidden}}.hero video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none}}
.hero::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,13,.2),rgba(11,11,13,.35) 50%,rgba(11,11,13,.62))}}
#bdbg{{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none;background:#000}}#bdbg video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none}}
section{{background:rgba(11,11,13,.58)}}.more-wrap{{display:flex;justify-content:center;margin-top:24px}}section.alt{{background:rgba(20,20,24,.66)}}section :is(h2,h3,p,.eyebrow,.sh,.sp){{text-shadow:0 1px 14px rgba(0,0,0,.55),0 1px 2px rgba(0,0,0,.4)}}
.hero .wrap{{position:relative;z-index:2;padding-bottom:70px}}.hero h1{{font:400 clamp(30px,4.6vw,62px)/1.08 R,sans-serif;margin:0 0 14px;max-width:18ch}}
.hero h1 em,.sh em{{font-style:normal;color:var(--ac)}}.hero p{{max-width:56ch;font-size:clamp(16px,1.6vw,19px);margin:0 0 24px;color:#eee}}.btns{{display:flex;gap:12px;flex-wrap:wrap}}
section{{padding:84px 0}}section.alt{{background:var(--sf)}}.eyebrow{{text-transform:uppercase;letter-spacing:.24em;color:var(--ac);font-weight:800;font-size:12.5px;margin-bottom:12px}}
.sh{{font:400 clamp(26px,3.6vw,46px)/1.1 R,sans-serif;margin:0 0 12px}}.sp{{color:var(--mu);max-width:64ch;margin:0 0 30px}}
.grid{{list-style:none;padding:0;margin:0;display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(270px,1fr))}}
.fc a{{display:block;text-decoration:none;background:var(--sf2);border-radius:16px;overflow:hidden;transition:transform .3s,box-shadow .3s}}.fc a:hover{{transform:translateY(-4px);box-shadow:0 14px 40px rgba(0,0,0,.5),0 0 0 1px rgba(242,193,78,.4)}}
.im{{position:relative;display:block;aspect-ratio:16/9;background:#000;overflow:hidden}}.im img{{width:100%;height:100%;object-fit:cover;transition:transform .6s}}.fc a:hover .im img{{transform:scale(1.05)}}
.ct{{position:absolute;left:10px;top:10px;background:rgba(0,0,0,.65);color:var(--ac);font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;border-radius:999px;padding:5px 10px}}
.pl{{position:absolute;left:50%;top:50%;width:54px;height:54px;margin:-27px;border-radius:50%;background:rgba(255,255,255,.18) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M8 5v14l11-7z'/%3E%3C/svg%3E") center/24px no-repeat;backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,.35)}}
.tx{{display:block;padding:13px 15px 16px}}.tx b{{display:block;font-size:15.5px}}.tx span{{color:var(--mu);font-size:13.5px}}
.fmt{{display:flex;gap:8px;margin:-10px 0 22px}}.fmt button{{background:var(--sf2);color:var(--fg);border:1px solid var(--line);border-radius:999px;padding:8px 16px;font:700 13px M,sans-serif;cursor:pointer}}.fmt button[aria-pressed=true]{{background:var(--co);border-color:var(--co)}}
.vrow{{list-style:none;padding:0 0 10px;margin:0;display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory}}.vrow li{{flex:none;width:200px;scroll-snap-align:start}}
.vrow video,.vrow img{{width:200px;aspect-ratio:9/16;object-fit:cover;border-radius:14px;background:#000}}.vrow span{{display:block;font-size:13px;color:var(--mu);margin-top:6px}}
.shots{{list-style:none;padding:0;margin:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}}.shots video{{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px;background:#000}}
.shots span{{display:block;font-size:12.5px;color:var(--mu);margin-top:6px;line-height:1.4}}.shots b{{color:var(--fg)}}
.mont{{margin:0 0 26px;border-radius:16px;overflow:hidden;max-width:880px}}
.cmps{{list-style:none;padding:0;margin:0;display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}}
.cmp{{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000}}.cmp video,.cmp img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.cmp img{{clip-path:inset(0 calc(100% - var(--x)) 0 0)}}.cmp input{{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}}
.cmp::after{{content:"";position:absolute;top:0;bottom:0;left:var(--x);width:2px;background:var(--ac);box-shadow:0 0 12px var(--ac);pointer-events:none}}
.cmp .l,.cmp .r{{position:absolute;bottom:10px;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;background:rgba(0,0,0,.6);padding:4px 9px;border-radius:999px;pointer-events:none}}.cmp .l{{left:10px}}.cmp .r{{right:10px;color:var(--ac)}}
.stills{{list-style:none;padding:0;margin:0;display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}}.stills img{{border-radius:12px;aspect-ratio:16/9;object-fit:cover}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:16px}}table.plan{{width:100%;border-collapse:collapse;font-size:14px;min-width:820px}}
.plan th,.plan td{{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}}.plan thead th{{background:var(--sf2);font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--mu)}}
.plan tr.wk th{{background:rgba(242,193,78,.1);color:var(--ac);font:400 15px R,sans-serif;letter-spacing:.06em}}.plan .cap{{color:#d8d8de;max-width:420px}}.plan a{{color:var(--ac)}}
.fm{{display:inline-block;background:var(--sf2);border-radius:6px;padding:2px 7px;font-size:12px;font-weight:700}}
.sub3{{font:400 20px R,sans-serif;margin:34px 0 14px}}.kpi{{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));padding-left:18px;color:#ddd}}
.price{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}}.card{{position:relative;background:var(--sf2);border:1px solid var(--line);border-radius:18px;padding:22px}}
.card.hot{{border-color:var(--ac);box-shadow:0 0 30px rgba(242,193,78,.15)}}.card h3{{margin:0 0 6px;font:400 19px R,sans-serif}}.amt{{font:800 26px M,sans-serif;color:var(--ac);margin-bottom:8px}}
.card p{{color:var(--mu);margin:0}}.tag{{position:absolute;top:-11px;right:16px;background:var(--ac);color:#111;font-size:11px;font-weight:800;border-radius:999px;padding:4px 10px}}.terms{{color:var(--mu);font-size:13.5px;margin-top:18px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px}}.chips button{{background:transparent;color:var(--fg);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:8px 15px;font:600 14px M,sans-serif;cursor:pointer}}.chips button[aria-pressed=true]{{background:var(--ac);color:#111;border-color:var(--ac)}}
.end{{text-align:center;background:radial-gradient(ellipse at center,rgba(242,193,78,.12),transparent 70%)}}.end .btns{{justify-content:center}}
footer{{padding:30px 0 50px;color:var(--mu);font-size:13px;border-top:1px solid var(--line);background:rgba(11,11,13,.82)}}
dialog{{border:0;padding:0;background:transparent;max-width:min(1100px,94vw);width:100%}}dialog::backdrop{{background:rgba(0,0,0,.9)}}dialog video{{width:100%;max-height:84vh;border-radius:12px;background:#000}}
dialog .x{{position:absolute;right:0;top:-44px;background:none;border:0;color:#fff;font-size:34px;cursor:pointer}}dialog p{{margin:10px 2px;font-weight:700}}
.rv{{opacity:0;transform:translateY(24px);transition:opacity .8s,transform .8s}}.rv.in{{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){{.rv{{opacity:1;transform:none}}.btn.a{{animation:none}}}}
</style></head><body class="lock"><div id="bdbg" aria-hidden="true"><video muted playsinline preload="none"></video></div>
<nav class="nav"><div class="wrap"><a class="brand" href="#top" aria-label="BIG DOGMA"><span class="lfx" aria-hidden="true"><span class="lfx-in"></span></span><span class="bt"><b>BIG</b><b>DOGMA</b><small>AI STUDIO<i class="sep"></i>MK</small></span></a>
<div class="links">{navl}</div><a class="btn a" href="{mailto}">{E(s["cta"])}</a></div></nav>
<div id="splash" role="dialog" aria-label="BIG DOGMA × {name}"><video muted playsinline autoplay></video><video muted playsinline style="opacity:0"></video><div class="shade"></div>
<div class="sp-in"><p class="for">{E(s["for_"])}</p><h1>{name}</h1><p class="lead">{E(s["lead"])}</p><ul class="pts">{pts}</ul>
<button class="btn a" id="enter" type="button">{E(s["enter"])}</button><p class="note">{E(s["scroll"])} · bigdogma.tech</p></div></div>
<canvas id="burst" aria-hidden="true"></canvas>
<main id="top">
<header class="hero"><video autoplay muted loop playsinline poster="hero.jpg"><source src="hero.mp4" type="video/mp4"></video>
<div class="wrap"><h1>{s["h1"].format(c=name)}</h1><p>{E(s["sub"])}</p><div class="btns"><a class="btn a" href="#films">{E(s["f_e"])}</a><a class="btn b" href="#campaign">{E(s["c_e"])}</a></div></div></header>
<section id="films"><div class="wrap"><div class="eyebrow rv">{E(s["f_e"])}</div><h2 class="sh rv">{E(s["f_h"].format(n=n_f, c=c["name"]))}</h2><p class="sp rv">{E(s["f_p"])}</p>
{f'<div class="fmt rv" role="group"><button type="button" data-fmt="h" aria-pressed="true">{s["h169"]}</button><button type="button" data-fmt="v" aria-pressed="false">{s["v916"]}</button></div>' if has_v else ""}
<ul class="grid" id="fg">{films}</ul></div></section>
{f'<section class="alt"><div class="wrap"><div class="eyebrow rv">{E(s["v_e"])}</div><h2 class="sh rv">{E(s["v_h"])}</h2><p class="sp rv">{E(s["v_p"])}</p><ul class="vrow">{vert}</ul></div></section>' if has_v else ""}
<section id="shots"><div class="wrap"><div class="eyebrow rv">{E(s["s_e"])}</div><h2 class="sh rv">{E(s["s_h"])}</h2><p class="sp rv">{E(s["s_p"].format(n=len(SHOTS), c=c["name"]))}</p>
{mont}<ul class="shots">{shots}</ul></div></section>
<section class="alt"><div class="wrap"><div class="eyebrow rv">{E(s["k_e"])}</div><h2 class="sh rv">{E(s["k_h"])}</h2><p class="sp rv">{E(s["k_p"])}</p><ul class="cmps">{pairs}</ul></div></section>
{stills_sec}
<section id="campaign" class="alt"><div class="wrap"><div class="eyebrow rv">{E(s["c_e"])}</div><h2 class="sh rv">{E(s["c_h"])}</h2><p class="sp rv">{E(s["c_p"])}</p>{campaign(c, s)}</div></section>
{offer.replace('<section id="offer"', '<section id="offer" ')}
<section id="dl" class="alt"><div class="wrap"><div class="eyebrow rv">{E(s["dl_e"])}</div><h2 class="sh rv">{E(s["dl_h"])}</h2><p class="sp rv">{E(s["dl_p"])}</p>
<div class="btns rv"><a class="btn a" href="offer.pdf" target="_blank" rel="noopener" download>{E(s["dl_pdf"])}</a></div></div></section>
<section class="alt"><div class="wrap"><div class="eyebrow rv">{E(s["i_e"])}</div><h2 class="sh rv">{E(s["i_h"])}</h2><p class="sp rv">{E(s["i_p"])}</p><ul class="grid">{indc}</ul></div></section>
<section id="bd"><div class="wrap"><div class="eyebrow rv">{E(s["b_e"])}</div><h2 class="sh rv">{E(s["b_h"])}</h2><p class="sp rv">{E(s["b_p"].format(n=len(bd)))}</p>
<div class="chips" role="group"><button type="button" data-k="all" aria-pressed="true">{E(s["b_all"])} {len(bd)}</button><button type="button" data-k="f" aria-pressed="false">{E(s["b_f"])} {sum(1 for x in bd if x[2] == "f")}</button><button type="button" data-k="x" aria-pressed="false">{E(s["b_x"])} {len(BDT.FX)}</button></div>
<ul class="grid" id="bdg">{bdc}</ul><div class="more-wrap"><button type="button" class="btn b bdmore" hidden>{ {"mk": "Покажи уште", "sr": "Prikaži još", "sq": "Shfaq më shumë"}.get(c["lang"], "Show more") } <b></b></button></div></div></section>
<section class="end"><div class="wrap"><h2 class="sh rv">{E(s["end_h"])}</h2><p class="sp rv" style="margin:0 auto 26px">{E(s["end_p"])}</p><div class="btns"><a class="btn a" href="{mailto}">{E(s["cta"])}</a><a class="btn b" href="mailto:{MAIL}">{E(s["mail"])}: {MAIL}</a></div></div></section>
</main>
<footer><div class="wrap">{E(s["legal"])}<br>© 2026 BIG DOGMA · AI STUDIO | MK · <a href="{SITE}">bigdogma.tech</a> · <a href="classic.html">classic</a></div></footer>
<dialog id="lb"><button class="x" type="button" aria-label="{E(s["close"])}">×</button><video controls playsinline controlslist="nodownload noplaybackrate" disablepictureinpicture></video><p></p></dialog>
<script>window.H3V=false;window.H3T={json.dumps({"ad": s["h3_ad"], "film": s["h3_film"], "ai": s["ai_film"], "mark": SITE + "/media/h3_mark.png"}, ensure_ascii=False)};</script>
<script>window.DOGMA_HDR_BASE="{SITE}/logo_fx/hdr/";window.DOGMA_INTRO={json.dumps(intro)};window.DOGMA_HERO={{intro:window.DOGMA_INTRO}};window.BDBG_WAIT=true;</script><script src="{SITE}/logo_fx/hero_bg.js"></script>
<script src="{SITE}/logo_fx/mark_data.js"></script><script src="{SITE}/logo_fx/logo_fx.js"></script><script src="{SITE}/logo_fx/hdr/list.js"></script><script src="{SITE}/logo_fx/hdr.js"></script>
<script>
(function(){{
var $=function(q,e){{return(e||document).querySelector(q)}},$$=function(q,e){{return[].slice.call((e||document).querySelectorAll(q))}};
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* splash: BD logo films, two videos crossfading */
var sp=$('#splash'),sv=$$('video',sp),L=(window.DOGMA_INTRO||[]).slice().sort(function(){{return Math.random()-.5}}),k=0,cur=0;
function pre(){{if(!L.length)return;var n=sv[1-cur];n.src=L[k++%L.length];n.preload='auto';n.load()}}   /* next film loads while this one plays */
function nx(){{if(!L.length)return;var n=sv[1-cur],o=sv[cur],go=function(){{n.removeEventListener('playing',go);n.style.opacity=1;o.style.opacity=0;cur=1-cur;setTimeout(function(){{o.pause();if(!sp.classList.contains('out'))pre()}},900)}};
 n.addEventListener('playing',go);n.currentTime=0;n.play().catch(function(){{}})}}   /* fade only once the next film really plays */
sv.forEach(function(v){{v.addEventListener('ended',function(){{if(v===sv[cur])nx()}})}});if(!RM){{sv[0].src=L[k++];sv[0].play().catch(function(){{}});setTimeout(pre,300)}}
/* enter: burst + flash, then the content */
var bc=$('#burst'),b=bc.getContext('2d');
function burst(done){{var W=bc.width=innerWidth*Math.min(2,devicePixelRatio||1),H=bc.height=innerHeight*Math.min(2,devicePixelRatio||1),cx=W/2,cy=H/2,R=Math.hypot(W,H)/2,t0=performance.now(),P=[];
 for(var i=0;i<180;i++)P.push([Math.random()*6.283,.25+Math.random()*.9,Math.random(),1+Math.random()*3]);
 var sw=false;(function f(now){{var q=Math.max(0,Math.min(1,(now-t0)/1100)),pk=Math.sin(Math.PI*Math.min(1,q*1.6));b.clearRect(0,0,W,H);b.globalCompositeOperation='lighter';
  var g=b.createRadialGradient(cx,cy,0,cx,cy,R*(.2+q));g.addColorStop(0,'rgba(255,250,235,'+pk+')');g.addColorStop(.3,'rgba(242,193,78,'+(.7*pk)+')');g.addColorStop(1,'rgba(242,120,40,0)');b.fillStyle=g;b.fillRect(0,0,W,H);
  P.forEach(function(p){{var r=R*p[1]*q,a=1-q;b.fillStyle=p[2]>.5?'rgba(255,255,255,'+a+')':'rgba(242,193,78,'+a+')';b.beginPath();b.arc(cx+Math.cos(p[0])*r,cy+Math.sin(p[0])*r*.8,p[3]*W/900,0,6.283);b.fill()}});
  b.strokeStyle='rgba(255,230,170,'+(1-q)+')';b.lineWidth=W/300*(1-q);b.beginPath();b.ellipse(cx,cy,Math.max(0,R*q*.9),Math.max(0,R*q*.55),0,0,6.283);b.stroke();
  if(q>.3&&!sw){{sw=true;done()}}if(q<1)requestAnimationFrame(f);else b.clearRect(0,0,W,H)}})(t0)}}
function enter(){{if(sp.classList.contains('out'))return;var go=function(){{sp.classList.add('out');document.body.classList.remove('lock');if(window.BDBG_START)BDBG_START();sv.forEach(function(v){{setTimeout(function(){{v.pause();v.removeAttribute('src');v.load()}},1300)}})}};RM?go():burst(go)}}
$('#enter').addEventListener('click',enter);sp.addEventListener('click',function(e){{if(e.target===sp||e.target.classList.contains('shade'))enter()}});
addEventListener('keydown',function(e){{if((e.key==='Enter'||e.key===' ')&&!sp.classList.contains('out')&&document.activeElement===document.body){{e.preventDefault();enter()}}}});
/* films are for viewing on this page only (owner, 2026-11-26): no context menu on videos, no drag */
document.addEventListener('contextmenu',function(e){{if(e.target.closest&&e.target.closest('video,.im,.vrow,.shots,.cmp'))e.preventDefault()}});
document.addEventListener('dragstart',function(e){{if(e.target.tagName==='VIDEO'||e.target.tagName==='IMG')e.preventDefault()}});
/* H3 versions sit next to the same film (grid + 9:16 row); the server only answers h3/ outside the EU, UK, USA and South Korea */
fetch('h3/',{{cache:'no-store'}}).then(function(r){{return r.ok?r.json():[]}}).then(function(d){{var N={{}},T=window.H3T,fg=$('#fg'),vr=$('.vrow');
 (d||[]).forEach(function(f){{var m=/^(.+?)(_9x16)?\\.mp4$/.exec(f.name);if(m){{N[m[1]]=N[m[1]]||{{}};if(!m[2]||window.H3V)N[m[1]][m[2]?'v':'h']=1}}}});
 var nice=function(k){{return k.replace(/^[a-z0-9]+_/,'').replace(/_/g,' ').replace(/\\b\\w/g,function(c){{return c.toUpperCase()}})}};
 Object.keys(N).sort().forEach(function(k){{var h='h3/'+k,x=N[k],tw=fg&&fg.querySelector('a[data-play="'+k+'.mp4"]'),t=tw?tw.dataset.t:nice(k),ln=(tw&&tw.querySelector('.tx span'))?tw.querySelector('.tx span').textContent:'',li;
  if(x.h&&fg){{li=document.createElement('li');li.className='fc h3';
   li.innerHTML='<a href="'+h+'.mp4" data-play="'+h+'.mp4" data-t="'+t+'" data-p="'+h+'.jpg"'+(x.v?' data-v="'+h+'_9x16.mp4" data-vp="'+h+'_9x16.jpg"':'')+'><span class="im"><img src="'+(fmt==='v'&&x.v?h+'_9x16.jpg':h+'.jpg')+'" alt="" loading="lazy"><span class="ct">'+T.ai+'</span><span class="pl"></span><img class="h3m" src="'+T.mark+'" alt="MiniMax H3"></span><span class="tx"><b>'+t+'</b><span>'+ln+'</span></span></a>';
   var at=tw&&tw.closest('li');at?at.after(li):fg.appendChild(li)}}
  if(x.v&&vr){{li=document.createElement('li');li.innerHTML='<video data-src="'+h+'_9x16.mp4" poster="'+h+'_9x16.jpg" muted loop playsinline preload="none"></video><span>'+t+'</span><img class="h3m" src="'+T.mark+'" alt="MiniMax H3">';
   var tv=vr.querySelector('video[data-src="'+k+'_9x16.mp4"]'),av=tv&&tv.closest('li');av?av.after(li):vr.insertBefore(li,vr.querySelector('.gif'));io.observe($('video',li))}}
 }})}}).catch(function(){{}});
/* nav */
var nav=$('.nav');addEventListener('scroll',function(){{nav.classList.toggle('s',scrollY>40)}},{{passive:true}});
/* lightbox */
var lb=$('#lb'),lv=$('video',lb),lt=$('p',lb),fmt='h';
function open(src,t,p){{if(typeof lb.showModal!=='function'){{location.href=src;return}}lv.poster=p||'';lv.src=src;lt.textContent=t||'';lb.showModal();lv.play().catch(function(){{}})}}
lb.addEventListener('close',function(){{lv.pause();lv.removeAttribute('src');lv.load()}});$('.x',lb).onclick=function(){{lb.close()}};lb.addEventListener('click',function(e){{if(e.target===lb)lb.close()}});
document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('[data-play]');if(!a)return;e.preventDefault();
 var src=a.dataset.play,p=a.dataset.p;if(fmt==='v'&&a.dataset.v){{src=a.dataset.v;p=a.dataset.vp}}open(src,a.dataset.t,p)}});
$$('.fmt button').forEach(function(x){{x.onclick=function(){{fmt=x.dataset.fmt;$$('.fmt button').forEach(function(y){{y.setAttribute('aria-pressed',String(y===x))}});
 $$('#fg a[data-v]').forEach(function(a){{$('img',a).src=fmt==='v'?a.dataset.vp:a.dataset.p}})}}}});
/* BD gallery filter */
var bdK='all',bdStep=matchMedia('(max-width:700px)').matches?8:12,bdLim=bdStep,bdM=document.querySelector('.bdmore');
function bdApply(){{var n=0,t=0;$$('#bdg li').forEach(function(li){{var ok=bdK==='all'||li.dataset.k===bdK;if(ok)t++;var sh=ok&&n<bdLim;if(sh)n++;li.hidden=!sh}});if(bdM){{bdM.hidden=t<=bdLim;bdM.querySelector('b').textContent='('+Math.max(0,t-bdLim)+')'}}}}
$$('#bd .chips button').forEach(function(x){{x.onclick=function(){{bdK=x.dataset.k;bdLim=bdStep;$$('#bd .chips button').forEach(function(y){{y.setAttribute('aria-pressed',String(y===x))}});bdApply()}}}});
if(bdM)bdM.onclick=function(){{bdLim+=bdStep*2;bdApply()}};bdApply();
/* in-view muted loops + hover */
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{var v=e.target;if(e.isIntersecting){{if(RM)return;if(!v.getAttribute('src'))v.src=v.dataset.src;v.play().catch(function(){{}})}}else if(!v.paused)v.pause()}})}},{{rootMargin:'100px'}});
$$('video[data-src]').forEach(function(v){{io.observe(v)}});
/* compare sliders */
$$('.cmp input').forEach(function(r){{r.addEventListener('input',function(){{r.parentNode.style.setProperty('--x',r.value+'%')}})}});
/* reveal */
var ro=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');ro.unobserve(e.target)}}}})}},{{threshold:.12}});$$('.rv').forEach(function(x){{ro.observe(x)}});
}})();
</script></body></html>'''
    os.makedirs(out, exist_ok=True)
    if not os.path.exists(f"{out}/classic.html"): open(f"{out}/classic.html", "w", encoding="utf-8").write(old)
    open(f"{out}/index.html", "w", encoding="utf-8").write(page)
    print("ok", key, len(page), "films", n_f, "bd", len(bd), "industry", len(ind))

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
