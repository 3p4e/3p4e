# DOGMA pitch sites v2: sector-themed, dark cinematic, with the shared "AI magic" effects layer (fx/):
# live logo preloader, glowing nav mark, AI-render HUD over the hero film with typed prompt, aurora light, grain,
# capability marquee, count-up stats, glowing film cards, prompt -> key frame -> AI video pipeline + compare slider,
# animated logo loop at the close. v3: every LTX shot per company (gallery, key frame -> motion pairs, 9:16 phones, GIF teasers, montage). Private: unguessable path per company, root 404, noindex. LTX films only.
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

# ---- v3: every LTX shot of the company (gallery, key frame -> motion pairs, 9:16 phones, GIF teasers, silent montage) ----
# Asset map, worked out from cut.py / cut2.py (vo/batch2.py CUTS) / zito_cut.py and the cb* job bundles:
#   commercial = ltx610/comm_<key>_1..5 (key frames cb7/kf), second film = prop_<base>_s1..s4 (ltx25 s1-2, ltx610 s3-4; key frames cb5/cb6),
#   Vincinni = ltx610/vc1_*, vc2_* (cb10/kf; vc1_3 left out: dropped from the edit as an unnatural composite),
#   Foton = ltx610/fs1-6 (cb10/kf) + the 21 showreel shots (ltx25/foton_*, the 4 re-generated *_fix from ltx610; key frames foton/kf, cb9/kf),
#   plus the 10 Foton action key frames (fotonact/kf; their fotonact/standin clips are only copies of fs*/foton_* clips, so not shown twice),
#   Alkaloid also has the text-to-video shot ltx25/ltx_t2v_alkaloid_pharma. All web files get neutral names (x/c01.mp4 ...).
from concurrent.futures import ThreadPoolExecutor
L25, L610 = f"{S}/ltx25", f"{S}/ltx610"
WEBC = f"{S}/cut/tmp_web"; os.makedirs(WEBC, exist_ok=True)
def lp(n):
    for dd in (L610, L25):
        if os.path.exists(f"{dd}/{n}.mp4"): return f"{dd}/{n}.mp4"
    raise FileNotFoundError(n)
def kfp(n):
    for dd in ("cb5/kf", "cb6/kf", "cb7/kf", "cb10/kf"):
        for ext in ("png", "jpg"):
            if os.path.exists(f"{S}/{dd}/{n}.{ext}"): return f"{S}/{dd}/{n}.{ext}"
    return None
STD = {"01_zito_marketi_MK": ("kam", "kam_skopje"), "02_alkaloid_MK": ("alkaloid", "alkaloid_skopje"), "03_replek_MK": ("replek", "replek_skopje"),
       "06_beograd_na_vodi_RS": ("bw", "bw_belgrade_waterfront"), "07_millennium_team_RS": ("millennium", "millennium_team_belgrade"),
       "08_nelt_RS": ("nelt", "nelt_group"), "09_gener2_AL": ("gener2", "gener2_albania"), "10_concord_AL": ("concord", "concord_kastrati_tirana"),
       "11_viva_fresh_XK": ("viva", "viva_fresh_kosovo"), "12_speeex_XK": ("speeex", "speeex_kosovo")}
FILM2_ORDER = {"kam_skopje": [3, 1, 4, 2], "alkaloid_skopje": [2, 1, 3, 4], "replek_skopje": [3, 1, 4, 2], "bw_belgrade_waterfront": [1, 3, 4, 2],
               "nelt_group": [1, 4, 2, 3], "speeex_kosovo": [3, 4, 1, 2]}
FOTON_SR = ['A1_dawn-teaser', 'A2_drive-by', 'A3_studio-turn', 'B1_v9-character', 'B2_v7_fix', 'B3_g7_fix', 'C1_approach_fix', 'C2_climb', 'C3_summit',
            'D1_cockpit-reveal', 'D2_details', 'D3_seats', 'E1_auman-tractor', 'E2_aumark_fix', 'E3_eme4-electric', 'E4_cargo-van', 'F1_showroom-arrival',
            'F2_test-drive', 'F3_key-handover', 'G1_service-bay', 'G2_fleet-lineup']
FOTON_KF = {"B2_v7_fix": "B2_v7-character", "B3_g7_fix": "B3_g7-character", "C1_approach_fix": "C1_approach", "E2_aumark_fix": "E2_aumark-city-delivery"}
PROMPTS = {}
for b in ("cb2", "cb5", "cb6", "cb7", "cb9", "cb10"):
    for j in json.load(open(f"{S}/{b}/jobs.json"))["jobs"]: PROMPTS[j["id"]] = j.get("prompt", "")
def company_assets(cid, films):
    """[(group key, [(clip, key frame or None, shot id)])]; group key is a film id, 't2v' or 'stills' (key frames without a clip)"""
    f1, f2 = films
    if cid in STD:
        ck, pk = STD[cid]
        g = [(f1, [(lp(f"comm_{ck}_{i}"), kfp(f"comm_{ck}_{i}"), f"comm_{ck}_{i}") for i in range(1, 6)]),
             (f2, [(lp(f"prop_{pk}_s{i}"), kfp(f"{pk}_s{i}"), f"prop_{pk}_s{i}") for i in FILM2_ORDER.get(pk, [1, 2, 3, 4])])]
        if cid == "02_alkaloid_MK": g.append(("t2v", [(f"{L25}/ltx_t2v_alkaloid_pharma.mp4", None, "t2v_pharma")]))
        return g
    if cid == "04_vincinni_MK":
        return [(f1, [(lp(f"vc1_{i}"), kfp(f"vc1_{i}"), f"vc1_{i}") for i in (1, 2, 4, 5)]), (f2, [(lp(f"vc2_{i}"), kfp(f"vc2_{i}"), f"vc2_{i}") for i in range(1, 6)])]
    if cid == "05_foton_MK":
        sr = []
        for n in FOTON_SR:
            k = FOTON_KF.get(n, n); kp = f"{S}/cb9/kf/foton_{k}.jpg" if n in FOTON_KF else f"{S}/foton/kf/{k}.jpg"
            sr.append((lp(f"foton_{n}"), kp if os.path.exists(kp) else None, f"foton_{n}"))
        return [(f1, [(lp(f"fs{i}"), kfp(f"fs{i}"), f"fs{i}") for i in range(1, 7)]), (f2, sr),
                ("stills", [(None, f"{S}/fotonact/kf/a{i:02d}.png", f"a{i:02d}") for i in range(1, 11)])]
    raise KeyError(cid)
def webloop(clip):  # cached 480p silent loop + poster (first frame)
    k = os.path.splitext(os.path.basename(clip))[0]; mp, jp = f"{WEBC}/{k}.mp4", f"{WEBC}/{k}.jpg"
    if not os.path.exists(mp):
        run(["ffmpeg","-v","error","-y","-i",clip,"-vf","scale=-2:480,fps=24","-an","-c:v","libx264","-crf","28","-preset","slow","-pix_fmt","yuv420p","-movflags","+faststart",mp+".tmp.mp4"]); os.replace(mp+".tmp.mp4", mp)
    if not os.path.exists(jp): run(["ffmpeg","-v","error","-y","-i",mp,"-frames:v","1","-q:v","5",jp])
    return mp, jp
def webkf(src, out, w=872, h=480):
    run(["ffmpeg","-v","error","-y","-i",src,"-vf",f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}","-q:v","4",out])
def montage(clips, out, seglen):
    a = ["ffmpeg","-v","error","-y"]; fc = []
    for i, c in enumerate(clips): a += ["-ss", "1.4", "-t", f"{seglen}", "-i", c]; fc.append(f"[{i}:v]scale=872:480:force_original_aspect_ratio=increase,crop=872:480,setsar=1,fps=24[v{i}]")
    tot = seglen * len(clips)
    fc.append("".join(f"[v{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=0,fade=t=in:st=0:d=0.4,fade=t=out:st={tot-0.4:.2f}:d=0.4[o]")
    run(a + ["-filter_complex", ";".join(fc), "-map", "[o]", "-an", "-c:v","libx264","-crf","28","-preset","slow","-pix_fmt","yuv420p","-movflags","+faststart", out]); return tot
OTHER = {"01_zito_marketi_MK": ["Жито", "Zito", "Žito"], "02_alkaloid_MK": ["Alkaloid", "Алкалоид"], "03_replek_MK": ["Replek", "Реплек"], "04_vincinni_MK": ["Vincinni", "Makprogres", "Макпрогрес"],
         "05_foton_MK": ["Foton", "Tunland", "Auman", "Aumark"], "06_beograd_na_vodi_RS": ["Beograd na vodi", "Belgrade Waterfront"], "07_millennium_team_RS": ["Millennium"],
         "08_nelt_RS": ["Nelt"], "09_gener2_AL": ["Gener"], "10_concord_AL": ["Concord"], "11_viva_fresh_XK": ["Viva"], "12_speeex_XK": ["Speeex", "SPEEEX"], "_x": ["KAM", "КАМ", "Kastrati"]}
def caption(sid, cid):  # first sentence of the LTX motion prompt, dropped if it names anyone else
    p = PROMPTS.get(sid, "")
    if not p: return ""
    s = p.split(". ")[0].rstrip(".") + "."
    if len(s) < 40 and len(p.split(". ")) > 1: s = ". ".join(p.split(". ")[:2]).rstrip(".") + "."
    for k, names in OTHER.items():
        if k != cid and any(n.lower() in s.lower() for n in names): return ""
    return s if len(s) <= 150 else s[:147].rsplit(" ", 1)[0] + "…"
UI3 = {
 "mk": dict(nav="Кадри", sh_e="Секој кадар", sh_h="Сите AI кадри од вашите филмови", sh_p="{n} кадри генерирани со LTX-Video специјално за {c}. Секој трае 5–6 секунди; тука се без звук и во намалена резолуција за брз преглед.",
            mont="Сите кадри во {s} секунди", shot="Кадар", ai="AI видео", t2v="Текст → видео", i2m_e="Од слика до движење", i2m_h="Секој клучен кадар, оживеан",
            i2m_p="Прво го одобрувате статичниот клучен кадар, па AI го анимира. Повлечете преку секој пар за да ги споредите.", swipe="Лизгајте за сите парови →",
            vert_e="Вертикално 9:16", vert_h="Подготвено за телефон", vert_p="Истите филмови во вертикален формат за Reels, TikTok и Stories, плус 6-секундни GIF тизери за порака или е-пошта.",
            teaser="Тизер 6 сек. · GIF", stills_h="Следен концепт: акциски клучни кадри", stills_p="10 AI клучни кадри за акциски филм со Tunland V9, подготвени за ваше одобрување пред анимација.", kf="Клучен кадар"),
 "sr": dict(nav="Kadrovi", sh_e="Svaki kadar", sh_h="Svi AI kadrovi iz vaših filmova", sh_p="{n} kadrova generisanih uz LTX-Video posebno za {c}. Svaki traje 5–6 sekundi; ovde su bez zvuka i u smanjenoj rezoluciji radi brzog pregleda.",
            mont="Svi kadrovi za {s} sekundi", shot="Kadar", ai="AI video", t2v="Tekst → video", i2m_e="Od slike do pokreta", i2m_h="Svaki ključni kadar, oživljen",
            i2m_p="Prvo odobravate statični ključni kadar, zatim ga AI animira. Prevucite preko svakog para da uporedite.", swipe="Prevucite za sve parove →",
            vert_e="Vertikalno 9:16", vert_h="Spremno za telefon", vert_p="Isti filmovi u vertikalnom formatu za Reels, TikTok i Stories, plus GIF tizeri od 6 sekundi za poruku ili e-poštu.",
            teaser="Tizer 6 sek. · GIF", stills_h="", stills_p="", kf="Ključni kadar"),
 "sq": dict(nav="Kuadrot", sh_e="Çdo kuadër", sh_h="Të gjithë kuadrot AI nga filmat tuaj", sh_p="{n} kuadro të gjeneruara me LTX-Video posaçërisht për {c}. Secili zgjat 5–6 sekonda; këtu shfaqen pa zë dhe në rezolucion të reduktuar për shikim të shpejtë.",
            mont="Të gjithë kuadrot në {s} sekonda", shot="Kuadri", ai="Video AI", t2v="Tekst → video", i2m_e="Nga imazhi te lëvizja", i2m_h="Çdo kuadër kryesor, i gjallëruar",
            i2m_p="Fillimisht miratoni kuadrin kryesor statik, pastaj AI e animon. Tërhiqni mbi çdo çift për t’i krahasuar.", swipe="Rrëshqitni për të gjitha çiftet →",
            vert_e="Vertikal 9:16", vert_h="Gati për telefon", vert_p="Të njëjtat filma në format vertikal për Reels, TikTok dhe Stories, plus teaser GIF 6-sekondësh për mesazh ose email.",
            teaser="Teaser 6 sek. · GIF", stills_h="", stills_p="", kf="Kuadri kryesor")}
CSS3 = """
.gal{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr));margin-top:18px} @media(min-width:760px){.gal{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}} @media(min-width:1100px){.gal{grid-template-columns:repeat(4,minmax(0,1fr))}}
.gh{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-top:48px;padding-top:18px;border-top:1px solid color-mix(in srgb,var(--fg) 10%,transparent)} .gh h3{font-size:clamp(20px,2.4vw,26px);text-transform:none} .gh span{color:var(--mu);font-size:14px}
.tile{margin:0;position:relative;border-radius:var(--r);overflow:hidden;background:#000;border:1px solid color-mix(in srgb,var(--fg) 9%,transparent);transition:transform .3s,border-color .3s,box-shadow .3s}
.tile:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--ac) 70%,transparent);box-shadow:0 18px 40px -22px var(--ac)}
.tile video,.tile img{width:100%;aspect-ratio:872/480;object-fit:cover;background:#000}
.tile .b{position:absolute;top:8px;left:8px;display:flex;gap:6px;pointer-events:none} .tile .b i{font:600 10.5px/1 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;font-style:normal;padding:5px 7px;border-radius:999px;background:rgba(0,0,0,.6);color:#fff;backdrop-filter:blur(4px)}
.tile .b i.ai{background:color-mix(in srgb,var(--ac) 85%,#000);color:var(--ink)}
.tile figcaption{padding:10px 12px 12px;font:12.5px/1.45 ui-monospace,Menlo,monospace;color:var(--mu);background:var(--sf);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;min-height:3.2em}
@media(max-width:560px){.tile figcaption{font-size:11px;-webkit-line-clamp:2;padding:8px 9px 10px}}
.mont{position:relative;margin-top:40px;border-radius:calc(var(--r) + 4px);overflow:hidden;background:#000;box-shadow:0 30px 80px -40px var(--ac)} .mont video{width:100%;aspect-ratio:872/480;object-fit:cover}
.mont .lbl{position:absolute;left:14px;bottom:14px;padding:7px 12px;border-radius:999px;background:rgba(0,0,0,.6);color:#fff;font:600 12.5px system-ui;letter-spacing:.06em;backdrop-filter:blur(6px)}
.mont .lbl b{color:var(--ac)}
.strip{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 2px 18px;margin-top:30px;scrollbar-width:thin;scrollbar-color:var(--ac) transparent;overscroll-behavior-x:contain}
.pair{flex:0 0 min(84%,420px);scroll-snap-align:start;margin:0}
.pair .cmp{margin-top:0;max-width:none;aspect-ratio:872/480;border-radius:var(--r)} .pair .cmp .hd::after{width:34px;height:34px;font-size:15px} .pair .cmp .t{font-size:10.5px;bottom:10px;padding:5px 8px}
.pair figcaption{margin-top:10px;font-size:14px;color:var(--mu)} .pair figcaption b{color:var(--fg);font-weight:600}
.swipe{color:var(--mu);font-size:13.5px;margin-top:4px}
.phones{display:flex;gap:clamp(18px,4vw,48px);justify-content:center;flex-wrap:wrap;margin-top:44px}
.ph{margin:0;display:flex;flex-direction:column;align-items:center;gap:14px;max-width:100%}
.phone{position:relative;width:min(270px,72vw);aspect-ratio:9/19;border-radius:42px;padding:11px;background:linear-gradient(160deg,#2a2a2e,#0b0b0d);box-shadow:0 0 0 1.5px #3a3a40,0 40px 90px -40px var(--ac),inset 0 0 0 1px #000}
.phone:before{content:"";position:absolute;top:19px;left:50%;transform:translateX(-50%);width:30%;height:22px;border-radius:999px;background:#000;z-index:2}
.phone video{width:100%;height:100%;object-fit:cover;border-radius:32px;background:#000}
.ph figcaption{font-size:15px;text-align:center;max-width:270px} .ph figcaption small{display:block;color:var(--mu);font-size:13px;margin-top:2px}
.teasers{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));margin-top:40px;max-width:980px;margin-left:auto;margin-right:auto}
.teasers figure{margin:0;border-radius:var(--r);overflow:hidden;background:var(--sf);border:1px solid color-mix(in srgb,var(--fg) 9%,transparent)} .teasers img{width:100%;aspect-ratio:16/9;object-fit:cover;background:#000}
.teasers figcaption{padding:10px 14px;font-size:13.5px;color:var(--mu)} .teasers figcaption b{color:var(--fg)}
.stills{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr));margin-top:18px} @media(min-width:760px){.stills{grid-template-columns:repeat(5,minmax(0,1fr))}}
"""
GJS = """<script>(function(){var RM=matchMedia('(prefers-reduced-motion: reduce)').matches,FINE=matchMedia('(pointer: fine)').matches;
var vs=document.querySelectorAll('video[data-lz]');function load(v){if(!v.src){v.src=v.dataset.lz;}}
function play(v){load(v);var p=v.play();if(p&&p.catch)p.catch(function(){});}
if(!('IntersectionObserver' in window)){vs.forEach(function(v){v.preload='metadata';load(v);});return;}
var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){if(!RM)play(v);}else if(!v.paused){v.pause();}});},{threshold:0.35});
vs.forEach(function(v){io.observe(v);if(RM||FINE){var h=v.closest('.tile,.cmp,.mont')||v;h.addEventListener('pointerenter',function(){play(v);});if(RM)h.addEventListener('pointerleave',function(){v.pause();});}});})();</script>"""
STATS3 = {}

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
@media(max-width:480px){{nav .wrap{{gap:10px}} .brand b{{font-size:15px;letter-spacing:.06em;white-space:nowrap}} nav .btn{{padding:8px 11px;font-size:12.5px;white-space:nowrap}}}}
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
        label = re.sub(r"\((\d+)(\s*\w+\.?)\)", lambda m: f"({round(dur(f'{S}/pitch/{fid}_pitch.mp4'))}{m.group(2)})", label)
        shutil.copy(f"{S}/pitch/{fid}_pitch.mp4", f"{d}/{fid}.mp4"); shutil.copy(f"{S}/pitch_9x16/{fid}_pitch_9x16.mp4", f"{d}/{fid}_9x16.mp4"); shutil.copy(f"{S}/previews/{fid}_poster.jpg", f"{d}/{fid}.jpg")
        films += f"""<article class="film rv"><div class="vw"><video controls playsinline preload="none" poster="{fid}.jpg" src="{fid}.mp4"></video></div>
<div class="meta"><h3>{E(label)}</h3><div class="seg"><button class="on" data-src="{fid}.mp4">{u['h']}</button><button data-v="1" data-src="{fid}_9x16.mp4">{u['v']}</button></div></div></article>"""
    # ---- v3 sections: every shot, key frame -> motion pairs, 9:16 phones + GIF teasers, silent montage ----
    u3 = UI3[L]; X = f"{d}/x"; os.makedirs(X)
    groups = company_assets(c["id"], [f for f, _ in c["films"]])
    flabel = {fid: re.sub(r"\s*\([^)]*\)\s*$", "", lab) for fid, lab in c["films"]}
    allclips = [cl for g, items in groups for (cl, kf, sid) in items if cl]
    with ThreadPoolExecutor(4) as ex: list(ex.map(webloop, allclips))
    n = 0; gal = pairs = stills = ""; ncl = nkf = 0
    for g, items in groups:
        if g == "stills":
            tl = ""
            for j, (_, kf, sid) in enumerate(items, 1):
                webkf(kf, f"{X}/a{j:02d}.jpg"); nkf += 1
                tl += f'<figure class="tile rv"><img src="x/a{j:02d}.jpg" alt="" loading="lazy" width="872" height="480"><div class="b"><i class="ai">AI</i><i>{E(u3["kf"])} {j:02d}</i></div></figure>'
            stills = f'<div class="gh rv"><h3>{E(u3["stills_h"])}</h3><span>{E(u3["stills_p"])}</span></div><div class="stills">{tl}</div>'
            continue
        tl = ""; gt = flabel.get(g, u3["t2v"])
        for (cl, kf, sid) in items:
            n += 1; k = f"c{n:02d}"; mp, jp = webloop(cl); shutil.copy(mp, f"{X}/{k}.mp4"); shutil.copy(jp, f"{X}/{k}.jpg"); ncl += 1
            cap = E(caption(sid, c["id"])) or "&nbsp;"
            tl += (f'<figure class="tile rv"><video muted loop playsinline preload="none" poster="x/{k}.jpg" data-lz="x/{k}.mp4" aria-label="{E(u3["ai"])} {n:02d}"></video>'
                   f'<div class="b"><i class="ai">AI</i><i>{E(u3["shot"])} {n:02d}</i></div><figcaption>{cap}</figcaption></figure>')
            if kf:
                webkf(kf, f"{X}/k{n:02d}.jpg"); nkf += 1
                pairs += (f'<figure class="pair"><div class="cmp"><video muted loop playsinline preload="none" poster="x/k{n:02d}.jpg" data-lz="x/{k}.mp4"></video>'
                          f'<img src="x/k{n:02d}.jpg" alt="" loading="lazy"><div class="hd"></div><span class="t t1">{E(u2["c1"])}</span><span class="t t2">{E(u2["c2"])}</span>'
                          f'<input type="range" min="0" max="100" value="50" aria-label="{E(u2["hint"])}"></div><figcaption><b>{E(u3["shot"])} {n:02d}</b> · {E(gt)}</figcaption></figure>')
        gal += f'<div class="gh rv"><h3>{E(gt)}</h3><span>{len(items)} × {E(u3["ai"])} · LTX-Video</span></div><div class="gal">{tl}</div>'
    tot = montage(allclips, f"{X}/m.mp4", 1.0 if len(allclips) <= 14 else 0.75)
    run(["ffmpeg","-v","error","-y","-ss","0.6","-i",f"{X}/m.mp4","-frames:v","1","-q:v","4",f"{X}/m.jpg"])
    mont = f'<div class="mont rv"><video muted loop playsinline preload="none" poster="x/m.jpg" data-lz="x/m.mp4" aria-label="{E(u3["ai"])}"></video><span class="lbl"><b>AI</b> · {E(u3["mont"].format(s=round(tot)))}</span></div>'
    shots_sec = (f'<section id="shots"><div class="wrap"><div class="eyebrow rv">{E(u3["sh_e"])}</div><h2 class="sh rv">{E(u3["sh_h"])}</h2>'
                 f'<p class="sp rv">{E(u3["sh_p"].format(n=ncl, c=c["name"]))}</p>{mont}{gal}{stills}</div></section>')
    i2m = (f'<div class="gh rv"><h3>{E(u3["i2m_h"])}</h3><span>{E(u3["i2m_p"])}</span></div><div class="strip">{pairs}</div><p class="swipe">{E(u3["swipe"])}</p>') if pairs else ""
    phones = teas = ""
    for i, (fid, lab) in enumerate(c["films"], 1):
        v9 = f"{S}/pitch_9x16/{fid}_pitch_9x16.mp4"; run(["ffmpeg","-v","error","-y","-ss",f"{dur(v9)*0.3:.2f}","-i",v9,"-frames:v","1","-vf","scale=540:-2","-q:v","4",f"{X}/v{i}.jpg"])
        phones += (f'<figure class="ph rv"><div class="phone"><video controls playsinline preload="none" poster="x/v{i}.jpg" src="{fid}_9x16.mp4"></video></div>'
                   f'<figcaption>{E(flabel[fid])}<small>9:16 · Reels · TikTok · Stories · {E(u3["ai"])}</small></figcaption></figure>')
        gif = f"{S}/previews/{fid}_teaser6s.gif"
        if os.path.exists(gif):
            shutil.copy(gif, f"{X}/t{i}.gif")
            teas += f'<figure class="rv"><img src="x/t{i}.gif" alt="" loading="lazy"><figcaption><b>{E(u3["teaser"])}</b> · {E(flabel[fid])}</figcaption></figure>'
    vert_sec = (f'<section id="vertical" class="alt"><div class="wrap"><div class="eyebrow rv">{E(u3["vert_e"])}</div><h2 class="sh rv">{E(u3["vert_h"])}</h2>'
                f'<p class="sp rv">{E(u3["vert_p"])}</p><div class="phones">{phones}</div>{f"<div class=teasers>{teas}</div>" if teas else ""}</div></section>')
    STATS3[c["id"]] = (ncl, nkf)
    explh = ""
    if expl and L == "mk":
        shutil.copy(f"{S}/explainers/{expl}.mp4", f"{d}/how.mp4"); explh = f"""<div class="expl rv"><video controls playsinline preload="none" src="how.mp4" poster="kf.jpg"></video></div>"""
    steps = [s.split(". ", 1)[-1] for s in tx["how_d"].split(" → ")]
    from urllib.parse import quote
    wa = (f"https://wa.me/{B['whatsapp']}?text=" + quote(c["name"] + " - " + u["cta"])) if B.get("whatsapp") else f"mailto:{B['email']}?subject=" + quote(c["name"] + " - " + u["cta"])
    title = tx["title"].replace("{c}", c["name"])
    h1 = f"{E(title.split(c['name'])[0])}<em>{name}</em>" if c["name"] in title else E(title)
    marq = "".join(f"<span>{E(m)}</span>" for m in u2["marq"]) * 2
    stats = "".join(f'<div class="stat rv"><div class="v"{f" data-to={n}" if n is not None else ""}>{E(v)}</div><div class="l">{E(l)}</div></div>' for v, n, l in u2["stats"])
    page = f"""<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet"><meta name="referrer" content="no-referrer"><meta name="theme-color" content="{t['bg']}">
<title>{E(title)} · {E(B['name'])}</title><link rel="icon" type="image/png" href="icon.png"><link rel="apple-touch-icon" href="icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preload" href="russo.ttf" as="font" type="font/ttf" crossorigin>
<style>{css(t)}{CSS3}</style><link rel="stylesheet" href="fx.css"></head><body>
<div class="pre" aria-hidden="true"><canvas></canvas><button type="button">{u2['skip']}</button></div>
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="grain" aria-hidden="true"></div><div class="spot" aria-hidden="true"></div>
<nav><div class="wrap"><a class="brand" href="#top" aria-label="{E(B['name'])}"><canvas aria-hidden="true"></canvas><b>{E(B['name_short'])}</b></a>
<div class="links"><a href="#films">{u['films']}</a><a href="#shots">{u3['nav']}</a><a href="#ai">{u2['pipe_e']}</a><a href="#offer">{u['offer']}</a></div><a class="btn a" href="{wa}">{u['cta']}</a></div></nav>
<header class="hero" id="top"><video autoplay muted loop playsinline poster="hero.jpg" src="hero.mp4"></video><canvas class="embers" aria-hidden="true"></canvas>
<div class="hud" aria-hidden="true"><i class="c c1"></i><i class="c c2"></i><i class="c c3"></i><i class="c c4"></i><div class="scan"></div>
<div class="tag"><span class="rec"></span>{u2['render']} · LTX-Video · 24 fps</div><div class="tc">TC 00:00:00:00</div>
<div class="prompt"><div class="lbl"><span>{u2['prompt']}</span><span class="st" data-done="{E(u2['done'])}">{E(u2['gen'])}</span></div><div class="txt" data-text="{E(sp)}"></div><div class="bar"><i></i></div></div></div>
<div class="wrap"><span class="pill">{u['pill']}</span><h1>{h1}</h1><p>{E(hook)}</p><div class="btns"><a class="btn a" href="#films">{u['watch']}</a><a class="btn b" href="{wa}">{u['cta']}</a></div></div></header>
<div class="marq" aria-hidden="true"><div class="row">{marq}</div></div>
<section><div class="wrap"><div class="stats">{stats}</div></div></section>
<section id="films" style="padding-top:0"><div class="wrap"><div class="eyebrow rv">{u['films']}</div><h2 class="sh rv">{E(u['films_h'].replace('{c}', c['name']))}</h2><p class="sp rv">{E(u['films_p'])}</p>
<div class="films">{films}</div></div></section>
{vert_sec}{shots_sec}
<section id="ai" class="alt"><div class="wrap"><div class="eyebrow rv">{u2['pipe_e']}</div><h2 class="sh rv">{E(u2['pipe_h'])}</h2><p class="sp rv">{E(u2['pipe_p'])}</p>
<div class="pipe"><div class="pstep rv"><div class="k">{u2['s1']}</div><div class="ptxt" data-type="{E(sp)}"></div></div><i class="arrow"></i>
<div class="pstep rv"><div class="k">{u2['s2']}</div><img src="kf.jpg" alt="" loading="lazy"></div><i class="arrow"></i>
<div class="pstep rv"><div class="k">{u2['s3']}</div><video muted loop playsinline poster="kf.jpg" data-src="shot.mp4"></video></div></div>
<div class="cmp rv"><video muted loop playsinline data-src="shot.mp4" poster="kf.jpg"></video><img src="kf.jpg" alt=""><div class="hd"></div><span class="t t1">{u2['c1']}</span><span class="t t2">{u2['c2']}</span>
<input type="range" min="0" max="100" value="50" aria-label="{E(u2['hint'])}"></div><p class="hint">{E(u2['hint'])}</p>{i2m}</div></section>
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
<footer><div class="wrap"><img src="logo.png" alt="{E(B['name'])}"><p>{E(u['note'])}</p><p>{E(' · '.join(x for x in (B['phone'], B['email'], B['web']) if x))}</p></div></footer>
<script src="dogma_logo.js"></script><script src="mark.js"></script><script src="fx.js"></script>{GJS}</body></html>"""
    open(f"{d}/index.html", "w").write(page); print("OK", c["id"], sec, flush=True)
json.dump(tokens, open(tokfile, "w"), indent=1)
open(f"{ROOT}/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
shutil.copy(f"{REPO}/cut/pitch_site_nginx.conf", f"{S}/pitch_site/nginx.conf"); shutil.copy(f"{REPO}/cut/pitch_site_compose.yml", f"{S}/pitch_site/docker-compose.yml")
for k, (a, b) in STATS3.items(): print("ASSETS", k, "clips", a, "keyframes", b)
print("SITES_DONE")
