# DOGMA pitch sites v2: sector-themed, dark cinematic, with the shared "AI magic" effects layer (fx/):
# live logo preloader, glowing nav mark, AI-render HUD over the hero film with typed prompt, aurora light, grain,
# capability marquee, count-up stats, glowing film cards, prompt -> key frame -> AI video pipeline + compare slider,
# animated logo loop at the close. Private: unguessable path per company, root 404, noindex. LTX films only.
import os, re, json, shutil, secrets, html, subprocess, ast
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
REPO = "/home/user/3p4e/projects/b2b-studio"
V1 = ast.parse(open(f"{S}/cut/gen_sites_v1.py").read())
NS = {}
for node in V1.body:  # reuse the texts and themes from v1 without running it
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in ("THEMES", "CO", "UI", "SEC"):
        NS[node.targets[0].id] = eval(compile(ast.Expression(node.value), "v1", "eval"))
THEMES, CO, UI, SEC = NS["THEMES"], NS["CO"], NS["UI"], NS["SEC"]
O = json.load(open(f"{S}/cut/offers.json")); B = json.load(open(f"{S}/brand/brand.json"))
ROOT = f"{S}/pitch_site/site"; shutil.rmtree(f"{S}/pitch_site", ignore_errors=True); os.makedirs(ROOT)
tokfile = f"{S}/cut/page_tokens.json"; tokens = json.load(open(tokfile)) if os.path.exists(tokfile) else {}
E = html.escape
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)

# dark cinematic variants for the formerly light themes (video and glow read far better on dark)
THEMES["pharma"].update(bg="#07131d", sf="#0d1e2c", fg="#eaf3fa", mu="#93a9bb", ink="#ffffff")
THEMES["retail"].update(bg="#0a130d", sf="#122019", fg="#f0f6ee", mu="#9fb1a2", ink="#ffffff")
THEMES["fmcg"].update(bg="#150a06", sf="#22130d", fg="#fbefe4", mu="#c3a594", ink="#ffffff")
ACCENT_FIX = {"02_alkaloid_MK": "#2f8fe0", "03_replek_MK": "#19b3a3", "01_zito_marketi_MK": "#2bb35a", "11_viva_fresh_XK": "#ff4d3d", "04_vincinni_MK": "#e0283f"}

UI2 = {
 "mk": dict(skip="Прескокни", render="AI рендер", prompt="Промпт", gen="Генерирање…", done="Готово ✓", pipe_e="AI процес", pipe_h="Од текст до филм",
            pipe_p="Еден кадар од вашиот филм: опишан со текст, претворен во клучен кадар за ваше одобрување, па оживеан со AI.",
            s1="01 · Промпт", s2="02 · Клучен кадар", s3="03 · AI видео", c1="Слика", c2="AI видео", hint="Повлечете за да споредите статичниот кадар и AI анимацијата.",
            marq=["Текст → Видео", "Слика → Видео", "AI глас на македонски", "Оригинална музика", "16:9 · 9:16", "Одобрување на кадри", "MK · SR · SQ", "Full HD"],
            stats=[("7–10", None, "дена до готов филм"), ("0", 0, "дена снимање"), ("2", 2, "формати: 16:9 и 9:16"), ("3", 3, "јазици: MK · SR · SQ")]),
 "sr": dict(skip="Preskoči", render="AI render", prompt="Prompt", gen="Generisanje…", done="Gotovo ✓", pipe_e="AI proces", pipe_h="Od teksta do filma",
            pipe_p="Jedan kadar iz vašeg filma: opisan tekstom, pretvoren u ključni kadar za vaše odobrenje, pa oživljen uz AI.",
            s1="01 · Prompt", s2="02 · Ključni kadar", s3="03 · AI video", c1="Slika", c2="AI video", hint="Prevucite da uporedite statični kadar i AI animaciju.",
            marq=["Tekst → Video", "Slika → Video", "AI glas na srpskom", "Originalna muzika", "16:9 · 9:16", "Odobrenje kadrova", "MK · SR · SQ", "Full HD"],
            stats=[("7–10", None, "dana do gotovog filma"), ("0", 0, "dana snimanja"), ("2", 2, "formata: 16:9 i 9:16"), ("3", 3, "jezika: MK · SR · SQ")]),
 "sq": dict(skip="Kalo", render="Render AI", prompt="Prompti", gen="Gjenerim…", done="Gati ✓", pipe_e="Procesi AI", pipe_h="Nga teksti te filmi",
            pipe_p="Një kuadër nga filmi juaj: i përshkruar me tekst, i kthyer në kuadër kryesor për miratimin tuaj, pastaj i gjallëruar me AI.",
            s1="01 · Prompti", s2="02 · Kuadri kryesor", s3="03 · Video AI", c1="Imazh", c2="Video AI", hint="Tërhiqni për të krahasuar kuadrin statik me animacionin AI.",
            marq=["Tekst → Video", "Imazh → Video", "Zë AI në shqip", "Muzikë origjinale", "16:9 · 9:16", "Miratim i kuadrove", "MK · SR · SQ", "Full HD"],
            stats=[("7–10", None, "ditë deri te filmi"), ("0", 0, "ditë xhirimi"), ("2", 2, "formate: 16:9 dhe 9:16"), ("3", 3, "gjuhë: MK · SR · SQ")])}

# one real shot per company: (prompt, key frame, LTX clip)
CB5 = {j["id"]: j for j in json.load(open(f"{S}/cb5/jobs.json"))["jobs"]}; CB10 = {j["id"]: j for j in json.load(open(f"{S}/cb10/jobs.json"))["jobs"]}
def shot(cid):
    m = {"04_vincinni_MK": ("vc1_2", f"{S}/vincinni/kf/vc1_2.png", f"{S}/ltx610/vc1_2.mp4"), "05_foton_MK": ("fs1", f"{S}/fotonspec/kf/fs1.png", f"{S}/ltx610/fs1.mp4")}
    if cid in m: k, kf, clip = m[cid]; return CB10[k]["prompt"], kf, clip
    base = {"01_zito_marketi_MK": "kam_skopje", "02_alkaloid_MK": "alkaloid_skopje", "03_replek_MK": "replek_skopje", "06_beograd_na_vodi_RS": "bw_belgrade_waterfront",
            "07_millennium_team_RS": "millennium_team_belgrade", "08_nelt_RS": "nelt_group", "09_gener2_AL": "gener2_albania", "10_concord_AL": "concord_kastrati_tirana",
            "11_viva_fresh_XK": "viva_fresh_kosovo", "12_speeex_XK": "speeex_kosovo"}[cid]
    return CB5[f"prop_{base}_s1"]["prompt"], f"{S}/cb5/kf/{base}_s1.png", f"{S}/ltx25/prop_{base}_s1.mp4"
def short_prompt(p):  # first two sentences: the creative part, not the style boilerplate
    parts = [x.strip() for x in p.split(". ") if x.strip()]
    return ". ".join(parts[:2]).rstrip(".") + "."

# shared fx bundle (copied into each company folder: nginx only serves the token paths)
FX = f"{S}/fx"; mk = open(f"{S}/brand/mark.svg").read()
vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', mk); dpath = re.search(r' d="([^"]+)"', mk).group(1)
open(f"{FX}/mark.js", "w").write(f"window.DOGMA_MARK={{w:{vb.group(1)},h:{vb.group(2)},d:{json.dumps(dpath)}}};")
LOOPWEB = f"{S}/fx/logo_loop_web.mp4"
run(["ffmpeg","-v","error","-y","-i",f"{S}/brand/anim/dogma_logo_loop_1080p.mp4","-vf","scale=1280:-2","-c:v","libx264","-crf","26","-preset","slow","-pix_fmt","yuv420p","-an","-movflags","+faststart",LOOPWEB])

def css(t):
    return f"""@import url('https://fonts.googleapis.com/css2?family={t['gf']}&display=swap');
:root{{--bg:{t['bg']};--sf:{t['sf']};--fg:{t['fg']};--mu:{t['mu']};--ac:{t['ac']};--ink:{t['ink']};--r:{t['r']};--hf:{t['hf']};--bf:{t['bf']}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;background:var(--bg)}}body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--bf);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}img,video{{display:block;max-width:100%}}
.wrap{{max-width:1160px;margin:0 auto;padding:0 20px;position:relative}}
h1,h2,h3{{font-family:var(--hf);font-weight:{t['hw']};letter-spacing:{t['ls']};text-transform:{t['tt']};line-height:1.08;margin:0}}
nav{{position:fixed;top:0;left:0;right:0;z-index:20;transition:background .3s,backdrop-filter .3s}}
nav.s{{background:color-mix(in srgb,var(--bg) 78%,transparent);backdrop-filter:blur(14px);box-shadow:0 1px 0 color-mix(in srgb,var(--fg) 10%,transparent)}}
nav .wrap{{display:flex;align-items:center;gap:22px;height:70px}}
nav .links{{margin-left:auto;display:flex;gap:22px;font-size:15px}} nav .links a{{text-decoration:none;opacity:.85}} nav .links a:hover{{opacity:1;color:var(--ac)}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;border-radius:var(--r);font-weight:600;text-decoration:none;border:1.5px solid transparent;transition:transform .2s,box-shadow .2s;cursor:pointer;font-size:16px}}
.btn:hover{{transform:translateY(-2px)}} .btn.a{{background:var(--ac);color:var(--ink);box-shadow:0 10px 34px -8px var(--ac)}} .btn.b{{border-color:currentColor}}
nav .btn{{padding:9px 16px;font-size:14px}}
.hero{{position:relative;min-height:100svh;display:flex;align-items:flex-end;overflow:hidden;color:#fff}}
.hero>video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none}}
.hero:after{{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,.05) 35%,rgba(0,0,0,.82) 100%)}}
.hero .wrap{{padding-bottom:11vh;width:100%}}
.pill{{display:inline-block;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;padding:7px 12px;border:1px solid rgba(255,255,255,.45);border-radius:999px;margin-bottom:22px;backdrop-filter:blur(6px);background:rgba(0,0,0,.25)}}
.hero h1{{font-size:clamp(40px,7.4vw,96px);max-width:14ch;text-shadow:0 2px 24px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5)}}
.hero h1 em{{font-style:normal;color:#fff;text-decoration:underline;text-decoration-color:var(--ac);text-decoration-thickness:.09em;text-underline-offset:.14em;text-decoration-skip-ink:none}}
.hero p{{font-size:clamp(17px,2vw,21px);max-width:44ch;margin:22px 0 30px;opacity:.92}} .hero .btns{{display:flex;gap:12px;flex-wrap:wrap}} .hero .btn.b{{color:#fff}}
section{{padding:clamp(64px,10vw,120px) 0;position:relative}} .eyebrow{{color:var(--ac);font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}}
.sh{{font-size:clamp(32px,4.6vw,56px);max-width:18ch}} .sp{{color:var(--mu);max-width:58ch;margin:16px 0 0}}
.films{{display:grid;gap:28px;margin-top:44px}} @media(min-width:900px){{.films{{grid-template-columns:1fr 1fr}}}}
.film{{background:var(--sf);border-radius:calc(var(--r) + 4px);overflow:hidden}}
.film .vw{{background:#000;display:flex;justify-content:center}} .film video{{width:100%;aspect-ratio:16/9;background:#000}} .film.v video{{aspect-ratio:9/16;width:auto;height:min(70vh,640px)}}
.film .meta{{padding:18px 20px 22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}} .film h3{{font-size:22px;flex:1 1 200px;text-transform:none}}
.seg{{display:inline-flex;background:color-mix(in srgb,var(--fg) 8%,transparent);border-radius:999px;padding:4px}}
.seg button{{border:0;background:transparent;color:var(--fg);padding:8px 14px;border-radius:999px;font:500 14px var(--bf);cursor:pointer}} .seg button.on{{background:var(--ac);color:var(--ink)}}
.why{{display:grid;gap:18px;margin-top:44px}} @media(min-width:800px){{.why{{grid-template-columns:repeat(3,1fr)}}}}
.card{{background:color-mix(in srgb,var(--sf) 70%,transparent);border-radius:var(--r);padding:28px;border:1px solid color-mix(in srgb,var(--fg) 9%,transparent);backdrop-filter:blur(8px);transition:transform .3s,border-color .3s}}
.card:hover{{transform:translateY(-4px);border-color:color-mix(in srgb,var(--ac) 60%,transparent)}}
.card .n{{font-family:var(--hf);font-size:44px;color:var(--ac);line-height:1;margin-bottom:18px;font-weight:{t['hw']}}} .card h3{{font-size:22px;margin-bottom:10px;text-transform:none}} .card p{{color:var(--mu);margin:0}}
.steps{{display:grid;gap:18px;margin-top:44px}} @media(min-width:900px){{.steps{{grid-template-columns:repeat(4,1fr)}}}}
.step{{padding-top:22px;border-top:2px solid var(--ac)}} .step b{{display:block;font-family:var(--hf);font-size:15px;color:var(--ac);letter-spacing:.1em;margin-bottom:8px}}
.expl{{margin-top:44px;border-radius:calc(var(--r) + 4px);overflow:hidden;max-width:900px;background:#000}} .expl video{{width:100%;aspect-ratio:16/9}}
.price{{display:grid;gap:18px;margin-top:44px}} @media(min-width:900px){{.price{{grid-template-columns:repeat(3,1fr);align-items:stretch}}}}
.price .card{{display:flex;flex-direction:column}} .price .amt{{font-family:var(--hf);font-size:30px;margin:14px 0 10px;font-weight:{t['hw']}}}
.price .hot{{border:2px solid var(--ac);position:relative;box-shadow:0 20px 60px -30px var(--ac)}} .price .tag{{position:absolute;top:-13px;left:24px;background:var(--ac);color:var(--ink);font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px}}
.terms{{color:var(--mu);font-size:14.5px;margin-top:22px;max-width:80ch}}
.final{{text-align:center;overflow:hidden}} .final .sh{{margin:0 auto;max-width:20ch}} .final p{{max-width:52ch;margin:18px auto 30px;color:var(--mu)}} .final .btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
footer{{padding:36px 0 48px;color:var(--mu);font-size:13.5px;border-top:1px solid color-mix(in srgb,var(--fg) 8%,transparent)}} footer .wrap{{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}} footer img{{height:30px;width:auto;opacity:.9}} footer p{{margin:0;flex:1 1 300px}}
.rv{{opacity:0;transform:translateY(24px);transition:opacity .8s ease,transform .8s ease}} .rv.in{{opacity:1;transform:none}}
@media(max-width:720px){{nav .links{{display:none}} nav .btn{{margin-left:auto}} body{{font-size:16px}}}}
@media(prefers-reduced-motion:reduce){{.rv{{opacity:1;transform:none;transition:none}} html{{scroll-behavior:auto}} .btn,.card{{transition:none}}}}"""

for c in O["companies"]:
    sec, acc, expl = CO[c["id"]]; t = dict(THEMES[sec]); t["ac"] = ACCENT_FIX.get(c["id"]) or acc or t["ac"]; L = c["lang"]
    tok = tokens.setdefault(c["id"], secrets.token_urlsafe(9)); d = f"{ROOT}/{tok}"; os.makedirs(d)
    tx = O["text"][L]; u = dict(UI[L]); u2 = UI2[L]; p = O["prices"][L]; hook, why = SEC[(sec, L)]; name = E(c["name"])
    for f in ("fx.css", "fx.js", "dogma_logo.js", "mark.js"): shutil.copy(f"{FX}/{f}", f"{d}/{f}")
    shutil.copy(f"{S}/brand/fonts/RussoOne-400.ttf", f"{d}/russo.ttf"); shutil.copy(LOOPWEB, f"{d}/logo_loop.mp4")
    shutil.copy(f"{S}/brand/logo.png", f"{d}/logo.png"); shutil.copy(f"{S}/brand/icon_512.png", f"{d}/icon.png"); shutil.copy(f"{S}/offers_pdf/{c['id']}_offer.pdf", f"{d}/offer.pdf")
    first = c["films"][0][0]; src = {"05_foton_MK": f"{S}/ltx610/fs1.mp4"}.get(c["id"], f"{S}/final_music/{first}.mp4"); du = dur(src); hs = 0.0 if c["id"] == "05_foton_MK" else 0.12; hl = min(8.0, du - du * hs)
    run(["ffmpeg","-v","error","-y","-ss",f"{du*hs:.2f}","-t",f"{hl:.2f}","-i",src,"-vf",f"scale=1280:-2,fade=t=in:st=0:d=0.5,fade=t=out:st={hl-0.5:.2f}:d=0.5","-an","-c:v","libx264","-crf","24","-preset","slow","-pix_fmt","yuv420p","-movflags","+faststart",f"{d}/hero.mp4"])
    run(["ffmpeg","-v","error","-y","-ss",f"{du*hs+1:.2f}","-i",src,"-frames:v","1","-vf","scale=1280:-2","-q:v","4",f"{d}/hero.jpg"])
    prompt, kf, clip = shot(c["id"])
    run(["ffmpeg","-v","error","-y","-i",kf,"-vf","scale=1280:-2","-q:v","3",f"{d}/kf.jpg"])
    run(["ffmpeg","-v","error","-y","-i",clip,"-vf","scale=1280:-2","-an","-c:v","libx264","-crf","24","-preset","slow","-pix_fmt","yuv420p","-movflags","+faststart",f"{d}/shot.mp4"])
    sp = short_prompt(prompt)
    films = ""
    for fid, label in c["films"]:
        shutil.copy(f"{S}/pitch/{fid}_pitch.mp4", f"{d}/{fid}.mp4"); shutil.copy(f"{S}/pitch_9x16/{fid}_pitch_9x16.mp4", f"{d}/{fid}_9x16.mp4"); shutil.copy(f"{S}/previews/{fid}_poster.jpg", f"{d}/{fid}.jpg")
        films += f"""<article class="film rv"><div class="vw"><video controls playsinline preload="none" poster="{fid}.jpg" src="{fid}.mp4"></video></div>
<div class="meta"><h3>{E(label)}</h3><div class="seg"><button class="on" data-src="{fid}.mp4">{u['h']}</button><button data-v="1" data-src="{fid}_9x16.mp4">{u['v']}</button></div></div></article>"""
    explh = ""
    if expl and L == "mk":
        shutil.copy(f"{S}/explainers/{expl}.mp4", f"{d}/how.mp4"); explh = f"""<div class="expl rv"><video controls playsinline preload="none" src="how.mp4" poster="kf.jpg"></video></div>"""
    steps = [s.split(". ", 1)[-1] for s in tx["how_d"].split(" → ")]
    wa = f"https://wa.me/{B['whatsapp']}?text=" + (c["name"] + " - " + u["cta"]).replace(" ", "%20")
    title = tx["title"].replace("{c}", c["name"])
    h1 = f"{E(title.split(c['name'])[0])}<em>{name}</em>" if c["name"] in title else E(title)
    marq = "".join(f"<span>{E(m)}</span>" for m in u2["marq"]) * 2
    stats = "".join(f'<div class="stat rv"><div class="v"{f" data-to={n}" if n is not None else ""}>{E(v)}</div><div class="l">{E(l)}</div></div>' for v, n, l in u2["stats"])
    page = f"""<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet"><meta name="referrer" content="no-referrer"><meta name="theme-color" content="{t['bg']}">
<title>{E(title)} · {E(B['name'])}</title><link rel="icon" type="image/png" href="icon.png"><link rel="apple-touch-icon" href="icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preload" href="russo.ttf" as="font" type="font/ttf" crossorigin>
<style>{css(t)}</style><link rel="stylesheet" href="fx.css"></head><body>
<div class="pre" aria-hidden="true"><canvas></canvas><button type="button">{u2['skip']}</button></div>
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="grain" aria-hidden="true"></div><div class="spot" aria-hidden="true"></div>
<nav><div class="wrap"><a class="brand" href="#top" aria-label="{E(B['name'])}"><canvas aria-hidden="true"></canvas><b>{E(B['name_short'])}</b></a>
<div class="links"><a href="#films">{u['films']}</a><a href="#ai">{u2['pipe_e']}</a><a href="#offer">{u['offer']}</a></div><a class="btn a" href="{wa}">{u['cta']}</a></div></nav>
<header class="hero" id="top"><video autoplay muted loop playsinline poster="hero.jpg" src="hero.mp4"></video><canvas class="embers" aria-hidden="true"></canvas>
<div class="hud" aria-hidden="true"><i class="c c1"></i><i class="c c2"></i><i class="c c3"></i><i class="c c4"></i><div class="scan"></div>
<div class="tag"><span class="rec"></span>{u2['render']} · LTX-Video · 24 fps</div><div class="tc">TC 00:00:00:00</div>
<div class="prompt"><div class="lbl"><span>{u2['prompt']}</span><span class="st" data-done="{E(u2['done'])}">{E(u2['gen'])}</span></div><div class="txt" data-text="{E(sp)}"></div><div class="bar"><i></i></div></div></div>
<div class="wrap"><span class="pill">{u['pill']}</span><h1>{h1}</h1><p>{E(hook)}</p><div class="btns"><a class="btn a" href="#films">{u['watch']}</a><a class="btn b" href="{wa}">{u['cta']}</a></div></div></header>
<div class="marq" aria-hidden="true"><div class="row">{marq}</div></div>
<section><div class="wrap"><div class="stats">{stats}</div></div></section>
<section id="films" style="padding-top:0"><div class="wrap"><div class="eyebrow rv">{u['films']}</div><h2 class="sh rv">{E(u['films_h'].replace('{c}', c['name']))}</h2><p class="sp rv">{E(u['films_p'])}</p>
<div class="films">{films}</div></div></section>
<section id="ai" class="alt"><div class="wrap"><div class="eyebrow rv">{u2['pipe_e']}</div><h2 class="sh rv">{E(u2['pipe_h'])}</h2><p class="sp rv">{E(u2['pipe_p'])}</p>
<div class="pipe"><div class="pstep rv"><div class="k">{u2['s1']}</div><div class="ptxt" data-type="{E(sp)}"></div></div><i class="arrow"></i>
<div class="pstep rv"><div class="k">{u2['s2']}</div><img src="kf.jpg" alt="" loading="lazy"></div><i class="arrow"></i>
<div class="pstep rv"><div class="k">{u2['s3']}</div><video muted loop playsinline poster="kf.jpg" data-src="shot.mp4"></video></div></div>
<div class="cmp rv"><video muted loop playsinline data-src="shot.mp4" poster="kf.jpg"></video><img src="kf.jpg" alt=""><div class="hd"></div><span class="t t1">{u2['c1']}</span><span class="t t2">{u2['c2']}</span>
<input type="range" min="0" max="100" value="50" aria-label="{E(u2['hint'])}"></div><p class="hint">{E(u2['hint'])}</p></div></section>
<section><div class="wrap"><div class="eyebrow rv">{u['why']}</div><h2 class="sh rv">{E(hook.split(':')[0].split(',')[0])}</h2>
<div class="why">{''.join(f'<div class="card rv"><div class="n">0{i}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i,(a,b) in enumerate(why,1))}</div></div></section>
<section id="how" class="alt"><div class="wrap"><div class="eyebrow rv">{u['how']}</div><h2 class="sh rv">{E(u['expl'] or tx['how'])}</h2>{f'<p class="sp rv">{E(u["expl_p"])}</p>' if u['expl_p'] and explh else ''}
<div class="steps">{''.join(f'<div class="step rv"><b>0{i}</b>{E(s)}</div>' for i,s in enumerate(steps,1))}</div>{explh}</div></section>
<section id="offer"><div class="wrap"><div class="eyebrow rv">{u['offer']}</div><h2 class="sh rv">{E(tx['offer'])}</h2>
<div class="price"><div class="card rv"><h3>{E(tx['pilot'])}</h3><div class="amt">{E(p['pilot'])}</div><p>{E(tx['pilot_d'])}</p></div>
<div class="card hot rv"><span class="tag">{u['popular']}</span><h3>{E(tx['launch'])}</h3><div class="amt">{E(p['launch'])}</div><p>{E(tx['launch_d'])}</p></div>
<div class="card rv"><h3>{E(tx['monthly'])}</h3><div class="amt">{E(p['monthly'])}</div><p>{E(tx['monthly_d'])}</p></div></div>
<p class="terms rv">{E(tx['terms'])} {E(tx['price_note'])}</p></div></section>
<section class="final"><div class="wrap"><video class="logo-loop" autoplay muted loop playsinline src="logo_loop.mp4" aria-hidden="true"></video><h2 class="sh rv">{E(u['final'])}</h2><p class="rv">{E(u['final_p'])}</p>
<div class="btns rv"><a class="btn a" href="{wa}">{u['cta']}</a><a class="btn b" href="mailto:{E(B['email'])}">{u['mail']}</a><a class="btn b" href="offer.pdf">{u['pdf']}</a></div></div></section>
<footer><div class="wrap"><img src="logo.png" alt="{E(B['name'])}"><p>{E(u['note'])}</p><p>{E(B['phone'])} · {E(B['email'])} · {E(B['web'])}</p></div></footer>
<script src="dogma_logo.js"></script><script src="mark.js"></script><script src="fx.js"></script></body></html>"""
    open(f"{d}/index.html", "w").write(page); print("OK", c["id"], sec, flush=True)
json.dump(tokens, open(tokfile, "w"), indent=1)
open(f"{ROOT}/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
shutil.copy(f"{REPO}/cut/pitch_site_nginx.conf", f"{S}/pitch_site/nginx.conf"); shutil.copy(f"{REPO}/cut/pitch_site_compose.yml", f"{S}/pitch_site/docker-compose.yml")
print("SITES_DONE")
