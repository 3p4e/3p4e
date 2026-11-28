# Private pitch pages + draft emails for leads WITHOUT their own films (flexible-LED makers, non-EU Europe companies), 2026-11-28.
# Same look as the ten lead pages (cut/pitch_v3.build via a synthetic classic.html carrying the offer), but the films section shows
# example films from bigdogma.tech for the company's sector (absolute URLs, every one checked for HTTP 200), plus the BD gallery and the offer.
# No campaign plan (the films are not theirs), no industry duplicate, no H3 section, no model names.
# Private data stays in the scratchpad: leads_more/cfg.json (names, emails, notes), leads_more/tokens.json; drafts in leads_more/drafts/.
#   python3 build_sector_pages.py [key ...]        -> /dev/shm/pub_more/<token>/ (index.html, hero, icon, font, email thumbs, offer.pdf)
import os, sys, json, re, secrets, string, subprocess, shutil, html as H, urllib.request
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
P = "/home/user/3p4e/projects/b2b-studio"; sys.path.insert(0, f"{P}/cut"); sys.path.insert(0, f"{P}/outreach/email")
import pitch_v3 as PV, new_pitches as N, bd_email as M
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; LM = f"{S}/leads_more"
OUT = os.environ.get("PUB_MORE", "/dev/shm/pub_more"); WORK = "/dev/shm/pub_more_work"; SITE = "https://bigdogma.tech"
CFG = json.load(open(f"{LM}/cfg.json", encoding="utf-8")); TOKF = f"{LM}/tokens.json"
TOK = json.load(open(TOKF)) if os.path.exists(TOKF) else {}
XL = PV.XL

# ------------------------------------------------------------------ films per sector (catfilms/plan categories or single film ids)
PLAN = {}
for fn in sorted(os.listdir(f"{P}/catfilms/plan")):
    for f in json.load(open(f"{P}/catfilms/plan/{fn}", encoding="utf-8"))["films"]: PLAN[f["id"]] = dict(f, cat=fn[:-5])
for fn in sorted(os.listdir(f"{P}/catfilms/plan_more")):   # the later films of each category (same fields), used only if live on the site
    if fn.startswith("cf_") and fn.endswith(".json"):
        f = json.load(open(f"{P}/catfilms/plan_more/{fn}", encoding="utf-8")); PLAN.setdefault(f["id"], f)
CATS = {}
for fid, f in PLAN.items(): CATS.setdefault(f["cat"], []).append(fid)
REC = {
 "wine": ["wine", "cf_tourism_2_story", "cf_agro_1_story", "cf_agro_5_commercial", "cf_agro_4_commercial", "cf_tourism_4_commercial"], "wine_hotel": ["wine", "cf_tourism_4_commercial", "cf_tourism_2_story", "cf_beauty_1_commercial"],
 "wine_tour": ["tourism", "cf_wine_2_story", "cf_agro_1_story", "cf_agro_5_commercial"],   # alcohol-ad-ban markets: wine tourism / export angle, no pour shots
 "banking": ["banking"], "insurance": ["insurance"], "telecom": ["telecom"], "education": ["education"],
 "developer": ["cf_developer_3_commercial", "cf_developer_1_explainer", "cf_developer_2_transform", "cf_apartment_staging_1_transform", "cf_real_estate_3_commercial", "cf_apartment_staging_3_commercial", "developer", "real_estate"],
 "resort": ["cf_developer_3_commercial", "cf_developer_1_explainer", "cf_developer_2_transform", "tourism"],
 "realestate": ["real_estate", "cf_apartment_staging_1_transform", "cf_apartment_staging_2_social", "cf_developer_3_commercial"],
 "automotive_ev": ["automotive", "cf_energy_1_commercial"], "horeca": ["horeca", "cf_food_4_commercial"], "cafes": ["horeca", "cf_product_launch_4_commercial"],
 "solar": ["solar", "cf_energy_3_social", "cf_energy_4_explainer", "cf_energy_5_story"],
 "solar_steel": ["solar", "cf_energy_4_explainer", "cf_steel_cement_3_commercial", "cf_steel_cement_1_explainer"],
 "ev": ["energy", "cf_automotive_3_commercial"], "health": ["health", "cf_pharma_1_explainer"], "pharma": ["pharma", "cf_health_5_commercial"],
 "ecommerce": ["it", "cf_retail_3_social", "cf_product_launch_1_social"], "recruitment": ["recruitment", "cf_it_2_social"],
 "logistics": ["logistics", "cf_recruitment_4_commercial"], "roads": ["road", "cf_construction_3_commercial", "cf_construction_1_transform", "cf_steel_cement_3_commercial"],
 "construction_energy": ["road", "cf_construction_3_commercial", "cf_energy_5_story", "cf_construction_1_transform"],
 "furniture": ["furniture", "cf_interior_design_1_transform", "cf_interior_design_3_commercial"],
 "beer": ["beverages", "cf_fitness_3_social"],
 "beverages_na": ["cf_beverages_1_commercial", "cf_beverages_4_explainer", "cf_beverages_3_social", "cf_product_launch_4_commercial", "cf_food_2_social"],
 "industry": ["industry_showreel", "cf_steel_cement_1_explainer", "cf_steel_cement_3_commercial", "cf_recruitment_1_story"],
 "agro": ["agro", "cf_tourism_3_explainer", "cf_food_1_story"], "food": ["food", "cf_retail_2_commercial", "cf_retail_4_explainer"],
 "sport": ["fitness", "cf_retail_1_commercial", "cf_product_launch_1_social"], "hotels": ["tourism", "cf_events_2_commercial", "cf_horeca_2_story"],
 "led": ["cf_oled_4_commercial", "cf_oled_5_commercial", "cf_oled_6_commercial", "cf_oled_1_commercial", "cf_oled_2_commercial", "cf_oled_3_commercial", "cf_expo_stand_2_social"],
}
PK = {"developer": ["b1", "b2", "b4"], "resort": ["b1", "b2", "b4"], "realestate": ["b1", "b2", "b4"], "roads": ["b4", "b6"], "construction_energy": ["b4", "b6"],
      "solar": ["b4", "b5"], "solar_steel": ["b4", "b5"], "ev": ["b4", "b5"], "led": ["b4", "b5"], "recruitment": ["b6", "b5"]}
ACC = {"wine": "#8e2b45", "wine_hotel": "#8e2b45", "wine_tour": "#8e2b45", "led": "#3da9fc", "developer": "#2f8fe0", "resort": "#2fa6a0", "realestate": "#2f8fe0", "solar": "#e0a52f", "solar_steel": "#e0a52f", "ev": "#36c48a"}

# films whose visible title/line names a Macedonian place or brand: only on pages of North Macedonian companies
LOCAL = re.compile(r"tikve|vranec|macedon|makedon|skopj|skoplj|shkup|resen|strumic|ohrid|kavadar|bazaa?r|тиквеш|вранец|македон|скопј|ресен|струмиц|охрид|чаршија|пазар", re.I)
def visible(fid, lang):
    f = PLAN[fid]; return " ".join([f["title_en"], f["line_en"], f.get("title_mk", ""), f.get("line_mk", "")] + [XL.get(l, {}).get(f"{fid}.{x}", "") for l in ("sr", "sq") for x in "tl"])
def recipe(r, local_ok=False, live=None):
    ids = []
    for x in REC[r]:
        for fid in (CATS[x] if x in CATS else [x]):
            if fid in ids or (live is not None and not live.get(fid)) or (not local_ok and LOCAL.search(visible(fid, "en"))): continue
            ids.append(fid)
    ids = ids[:8]; assert len(ids) >= 4, (r, ids)
    return sorted(ids, key=lambda i: PLAN[i]["type"] == "social")   # landscape films first (hero, email thumbs), vertical social clips last

def head(url):
    try: return urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30).status
    except Exception as e: return getattr(e, "code", 0)

# ------------------------------------------------------------------ page strings (overrides on cut/pitch_v3 T) and offer texts
UI = {
 "en": dict(h1="AI video for <em>{c}</em>", sub_ns="Example films from our studio for {sect}. After a short brief we make a version with your own photos, products and logo.",
            pts=["{n} example films for {sect}", "A version made for you after a short brief", ""], f_h="{n} example films for {sect}",
            f_p_nv="Examples from our studio, landscape (16:9) and vertical (9:16). The version for {name} is made after a short brief, in both formats.",
            lead="AI video studio from Skopje. Commercials and brand films without a shoot: ready 7–10 days after key-frame approval.",
            end_p="Online or in person. Tell us which example you like most and we will make a version for your brand.",
            nav=[("films", "Films"), ("offer", "Offer"), ("dl", "Download"), ("bd", "BD gallery")]),
 "mk": dict(h1="AI видео за <em>{c}</em>", sub_ns="Примери-филмови од нашето студио за {sect}. По краток бриф правиме верзија со ваши фотографии, производи и лого.",
            pts=["{n} примери-филмови за {sect}", "Верзија направена за вас по краток бриф", ""], f_h="{n} примери-филмови за {sect}",
            f_p_nv="Примери од нашето студио, хоризонтално (16:9) и вертикално (9:16). Верзијата за {name} ја правиме по краток бриф, во двата формати.",
            end_p="Во Скопје или онлајн. Кажете ни кој пример ви се допаѓа најмногу: правиме верзија за вашиот бренд.",
            nav=[("films", "Филмови"), ("offer", "Понуда"), ("dl", "Преземање"), ("bd", "BD галерија")]),
 "sr": dict(h1="AI video za <em>{c}</em>", sub_ns="Primeri filmova iz našeg studija za {sect}. Posle kratkog brifa pravimo verziju sa vašim fotografijama, proizvodima i logom.",
            pts=["{n} primera filmova za {sect}", "Verzija napravljena za vas posle kratkog brifa", ""], f_h="{n} primera filmova za {sect}",
            f_p_nv="Primeri iz našeg studija, horizontalno (16:9) i vertikalno (9:16). Verziju za {name} pravimo posle kratkog brifa, u oba formata.",
            end_p="Uživo ili onlajn. Recite nam koji vam se primer najviše dopada: pravimo verziju za vaš brend.",
            nav=[("films", "Filmovi"), ("offer", "Ponuda"), ("dl", "Preuzimanje"), ("bd", "BD galerija")]),
 "sq": dict(h1="Video AI për <em>{c}</em>", sub_ns="Filma shembull nga studioja jonë për {sect}. Pas një brifi të shkurtër krijojmë një version me fotot, produktet dhe logon tuaj.",
            pts=["{n} filma shembull për {sect}", "Një version i bërë për ju pas një brifi të shkurtër", ""], f_h="{n} filma shembull për {sect}",
            f_p_nv="Shembuj nga studioja jonë, horizontalisht (16:9) dhe vertikalisht (9:16). Versionin për {name} e krijojmë pas një brifi të shkurtër, në të dy formatet.",
            end_p="Takim fizik ose online. Na tregoni cili shembull ju pëlqen më shumë dhe ne krijojmë një version për markën tuaj.",
            nav=[("films", "Filma"), ("offer", "Oferta"), ("dl", "Shkarkime"), ("bd", "Galeria BD")]),
}
UI_LED = dict(UI["en"], h1="Flexible LED content for <em>{c}</em>", sub_ns="Concept films from our studio for flexible and creative LED. After a short brief we make a version for your own screens and products.",
              pts=["{n} concept films for flexible and creative LED", "A version for your screens after a short brief", ""], f_h="{n} concept films: curves, wraps and shapes",
              f_p_nv="Concepts from our studio in 16:9 for showrooms, trade fairs and the web. The version for {name} is produced to each screen's exact pixel map after a short brief.")
UI_LED.pop("lead"); UI_LED.pop("end_p")   # keep the LED lead and closing line of strings_en.json

OFF = json.load(open(f"{P}/cut/offers.json", encoding="utf-8")); BU = json.load(open(f"{P}/cut/bundles.json", encoding="utf-8"))
OT = {"en": dict(N.OFFER_TXT["en"], pk=dict(N.OFFER_TXT["en"]["pk"]))}
for l, hot, mo in (("mk", "Најчест избор", "месец"), ("sr", "Najčešći izbor", "mesec"), ("sq", "Zgjedhja më e shpeshtë", "muaj")):
    t = OFF["text"][l]; b = BU[l]
    OT[l] = dict(eb=t["offer"], pil=t["pilot"], pild=t["pilot_d"], hot=hot, lan=t["launch"], land=t["launch_d"], mon=t["monthly"], mond=t["monthly_d"], mo=mo, head=b["head"],
                 terms=t["terms"] + " " + t["price_note"], pk={k: (b[k]["n"], b[k]["u"], b[k]["d"]) for k in ("b1", "b2", "b4", "b5", "b6")})
OT["en"]["pk"].update(b1=("Developer", "per project", "A construction timelapse from groundbreaking to keys and a sales film for apartments before they are built, in formats for ads, social and the sales office."),
                      b2=("Apartment staging", "per apartment", "From empty to fully furnished, made from the photos of your apartments. A bundle of 5 apartments: €1,200."),
                      b6=("Employer brand", "per package", "A recruitment film, a film about your team and short clips for job ads."))
B5 = {"en": "A brand commercial, a film from your production, store or venue and seasonal spots for holidays and promotions.",
      "mk": "Рекламен филм за брендот, филм од производството или продавницата и сезонски спотови за празници и акции.",
      "sr": "Reklamni film za brend, film iz proizvodnje ili prodavnice i sezonski spotovi za praznike i akcije.",
      "sq": "Film reklamues për markën, film nga prodhimi ose dyqani dhe spote sezonale për festa dhe oferta."}
B4_EN = "Your project step by step, from start to finish, with your logo: buildings, interiors, solar plants, roads."

def offer_section(c):
    t = dict(OT[c["lang"]]); t["pk"] = dict(t["pk"]); pr = N.PRICES[c["lang"]]
    if c["recipe"] != "led":   # the English b4/b5 texts of new_pitches are written for LED makers
        t["pk"]["b5"] = (t["pk"]["b5"][0], t["pk"]["b5"][1], B5[c["lang"]])
        if c["lang"] == "en": t["pk"]["b4"] = (t["pk"]["b4"][0], t["pk"]["b4"][1], B4_EN)
    cards = "".join(f'<div class="card rv"><h3>{H.escape(t["pk"][i][0])}</h3><div class="amt">{pr[i + ".a"]}</div><span class="u">{H.escape(t["pk"][i][1])}</span><p>{H.escape(t["pk"][i][2])}</p></div>' for i in c["pk"])
    return (f'<section id="offer"><div class="wrap"><div class="eyebrow rv">{t["eb"]}</div><h2 class="sh rv">{t["eb"]}</h2>\n<div class="price"><div class="card rv"><h3>{t["pil"]}</h3><div class="amt">{pr["p1.a"]}</div><p>{t["pild"]}</p></div>\n'
            f'<div class="card hot rv"><span class="tag">{t["hot"]}</span><h3>{t["lan"]}</h3><div class="amt">{pr["p2.a"]}</div><p>{t["land"]}</p></div>\n'
            f'<div class="card rv"><h3>{t["mon"]}</h3><div class="amt">{pr["p3.a"]} / {t["mo"]}</div><p>{t["mond"]}</p></div></div>\n'
            f'<h3 class="bh rv">{t["head"]}</h3><div class="price bund">{cards}</div>\n<p class="terms rv">{t["terms"]}</p></div></section>')

# ------------------------------------------------------------------ email texts (short, honest: examples from the studio, a version after a brief)
PILOT = {"mk": "€600", "sq": "€600", "sr": "€700", "en": "€900"}
EM = {
 "en": dict(subject="{n}: AI video examples for {sect} (private page)", greeting="Hello,",
            p1="We are BIG DOGMA, an AI video studio in Skopje. We put together a private page for {n} with short example films from our studio for {sect}: commercials and social clips made with AI, with no shoot.",
            p2="These are examples, not films about {n}. After a short brief (your photos, products or renders and your logo) we make a version for you in 7–10 days, landscape for screens and YouTube and vertical for Reels, TikTok and Stories.",
            p3="Nothing is published without your written approval. If the direction is interesting, we would be glad to show you in 15 minutes how it would look with your own material. A pilot film starts from {p}.",
            cta="See the examples", note="A private page only for {n}: the example films, the offer and a PDF.", role="Founder and creative director", closing="Best regards,", vw="video", ex="example",
            pre="Example AI films for {sect}, and how a version for {n} would work. Private page, 2 minutes.",
            optout="This message was sent only to {n}. If you do not want more messages from us, reply with “no, thank you” and we will not write again."),
 "mk": dict(subject="{n}: AI видео примери за {sect} (приватна страница)", greeting="Почитувани,",
            p1="Ние сме BIG DOGMA, AI видео студио од Скопје. За {n} подготвивме приватна страница со кратки примери-филмови од нашето студио за {sect}: реклами и клипови за мрежи изработени со вештачка интелигенција, без снимање.",
            p2="Ова се примери, не филмови за {n}. По краток бриф (ваши фотографии, производи или рендери и лого) правиме верзија за вас за 7–10 дена, хоризонтално за екрани и YouTube и вертикално за Reels, TikTok и Stories.",
            p3="Ништо не се објавува без ваше писмено одобрение. Ако насоката ви е интересна, би сакале за 15 минути да ви покажеме како би изгледало со ваш материјал. Пилот-филм чини од {p}.",
            cta="Погледнете ги примерите", note="Приватна страница само за {n}: примерите, понудата и PDF.", role="Основач и креативен директор", closing="Со почит,", vw="видео", ex="пример",
            pre="Примери AI филмови за {sect} и како би изгледала верзија за {n}. Приватна страница, 2 минути.",
            optout="Оваа порака е испратена само до {n}. Ако не сакате повеќе пораки од нас, одговорете со „не, благодарам“ и нема повторно да ви пишеме."),
 "sr": dict(subject="{n}: AI video primeri za {sect} (privatna stranica)", greeting="Poštovani,",
            p1="Mi smo BIG DOGMA, AI video studio iz Skoplja. Za {n} smo pripremili privatnu stranicu sa kratkim primerima filmova iz našeg studija za {sect}: reklame i klipovi za mreže napravljeni pomoću veštačke inteligencije, bez snimanja.",
            p2="Ovo su primeri, a ne filmovi o kompaniji {n}. Posle kratkog brifa (vaše fotografije, proizvodi ili renderi i logo) pravimo verziju za vas za 7–10 dana, horizontalno za ekrane i YouTube i vertikalno za Reels, TikTok i Stories.",
            p3="Ništa se ne objavljuje bez vašeg pisanog odobrenja. Ako vam je pravac zanimljiv, rado ćemo vam za 15 minuta pokazati kako bi to izgledalo sa vašim materijalom. Pilot-film košta od {p}.",
            cta="Pogledajte primere", note="Privatna stranica samo za {n}: primeri, ponuda i PDF.", role="Osnivač i kreativni direktor", closing="Srdačan pozdrav,", vw="video", ex="primer",
            pre="Primeri AI filmova za {sect} i kako bi izgledala verzija za {n}. Privatna stranica, 2 minuta.",
            optout="Ova poruka je poslata samo kompaniji {n}. Ako ne želite više poruka od nas, odgovorite sa „ne, hvala“ i nećemo vam ponovo pisati."),
 "sq": dict(subject="{n}: shembuj videosh AI për {sect} (faqe private)", greeting="Të nderuar,",
            p1="Ne jemi BIG DOGMA, një studio video AI nga Shkupi. Për {n} kemi përgatitur një faqe private me filma të shkurtër shembull nga studioja jonë për {sect}: reklama dhe klipe për rrjete sociale të krijuara me inteligjencë artificiale, pa xhirime.",
            p2="Këta janë shembuj, jo filma për {n}. Pas një brifi të shkurtër (fotot, produktet ose render-at tuaja dhe logoja) krijojmë një version për ju për 7–10 ditë, horizontalisht për ekrane dhe YouTube dhe vertikalisht për Reels, TikTok dhe Stories.",
            p3="Asgjë nuk publikohet pa miratimin tuaj me shkrim. Nëse drejtimi ju intereson, do të na vinte mirë t'ju tregonim për 15 minuta si do të dukej me materialet tuaja. Një film pilot kushton nga {p}.",
            cta="Shikoni shembujt", note="Faqe private vetëm për {n}: shembujt, oferta dhe PDF-ja.", role="Themelues dhe drejtor kreativ", closing="Me respekt,", vw="video", ex="shembull",
            pre="Shembuj filmash AI për {sect} dhe si do të dukej një version për {n}. Faqe private, 2 minuta.",
            optout="Ky mesazh u dërgua vetëm për {n}. Nëse nuk dëshironi më mesazhe nga ne, përgjigjuni me „jo, faleminderit“ dhe nuk do t'ju shkruajmë më."),
}
EM_LED = dict(EM["en"], subject="{n}: AI content concepts for flexible LED (private page)",
    p1="We are BIG DOGMA, an AI video studio in Skopje. We made a set of concept films for flexible and creative LED (S-curved walls, wrapped columns, spheres and totems) and put them on a private page for {n}.",
    p2="They are concepts from our studio, not yet made with your products. After a short brief we make a version for your {series}, mapped to the real screen shape, for your showroom, trade-fair stand and website.",
    p3="Nothing is published without your written approval. If the direction is interesting, we would be glad to show you in 15 minutes how it would look on your own screens. A pilot film starts from {p}.",
    cta="See the concepts", note="A private page only for {n}: the concept films, the offer and a PDF.", ex="concept",
    pre="Concept films for flexible and creative LED, and how a version for {n} would work. Private page, 2 minutes.")
# the angle sentence for markets where wine or alcohol cannot be advertised (per the research file's notes)
ANGLE = {"wine_tour": "For a winery we focus on what can be shown everywhere: the estate, the landscape and visits, and films for export partners and trade fairs.",
         "beverages_na": "We would focus on your non-alcoholic brands."}

# ------------------------------------------------------------------ build one company
def tok_for(k):
    if k not in TOK:
        a = string.ascii_letters + string.digits + "_-"
        while True:   # a random token must not happen to contain a model name (e.g. "H3")
            TOK[k] = "".join(secrets.choice(a) for _ in range(14))
            if not any(b.strip() in TOK[k] for b in BAD): break
        json.dump(TOK, open(TOKF, "w"), indent=1)
    return TOK[k]

def ftitle(lang, f):
    if lang == "mk": return f["title_mk"], f["line_mk"]
    return XL.get(lang, {}).get(f"{f['id']}.t", f["title_en"]), XL.get(lang, {}).get(f"{f['id']}.l", f["line_en"])

def strip(page):
    page = re.sub(r'<section id="campaign".*?</section>\n', "", page, flags=re.S)
    page = re.sub(r'<section class="alt"><div class="wrap"><div class="eyebrow rv">[^<]*</div><h2 class="sh rv">[^<]*</h2><p class="sp rv">[^<]*</p><ul class="grid"></ul></div></section>\n', "", page)
    page = re.sub(r'<!--<section id="shots".*?-->', "", page, flags=re.S)
    page = re.sub(r"/\* H3 versions.*?(?=/\* nav \*/)", "", page, flags=re.S)
    page = re.sub(r"<script>window\.H3V=false;[^<]*</script>", "", page)
    page = re.sub(r"/\* (?:MiniMax H3|model) mark on H3 thumbnails[^\n]*\*/\n\.h3m\{[^}]*\}", "", page)
    return page

BAD = ("MiniMax", "H3", "LTX", "Seedance", "Kling", "Hailuo", "Sora", "Veo ", "Runway", "Gemini", "Wan2", "Flux", "Midjourney", "Higgsfield", "ElevenLabs", "Lyria")
class P_(HTMLParser):
    def __init__(s): super().__init__(); s.txt = []; s.skip = 0
    def handle_starttag(s, t, a): s.skip += t in ("script", "style")
    def handle_endtag(s, t): s.skip -= t in ("script", "style")
    def handle_data(s, d):
        if not s.skip: s.txt.append(d)
def validate(page):
    p = P_(); p.feed(page); p.close(); vis = " ".join(p.txt); errs = []
    if "{" in vis or "}" in vis: errs.append("brace in visible text")
    if re.search(r"\{(n|c|sect|name|link|p|series|s)\}", page): errs.append("unfilled placeholder")
    errs += [f"bad word {b}" for b in BAD if b in page]
    return errs

LIVE = {}
def build(c, live=None):
    k = c["key"]; lang = c["lang"]; name = c["name"]; tok = tok_for(k); pub = f"{OUT}/{tok}"; page_url = f"https://pitch.bigdogma.tech/{tok}/"
    shutil.rmtree(pub, ignore_errors=True); os.makedirs(f"{pub}/email")
    ids = recipe(c["recipe"], c["country"] == "MK", LIVE); c["pk"] = PK.get(c["recipe"], ["b5", "b6"])
    films = []
    for fid in ids:
        u = f"{SITE}/films/{fid}"; assert LIVE[fid], fid
        t, l = ftitle(lang, PLAN[fid]); films.append(dict(id=fid, t=t, l=l, src=u + ".mp4", poster=u + ".jpg", type=PLAN[fid]["type"]))
    led = c["recipe"] == "led"
    ui = dict(UI_LED if led else UI[lang])
    for x in ("sub_ns", "f_h", "f_p_nv"): ui[x] = ui[x].replace("{sect}", c["sect"]).replace("{name}", name)
    ui["pts"] = [x.replace("{sect}", c["sect"]) for x in ui["pts"]]; ui["sub"] = ui["sub_ns"]
    PV.COMPANIES[k] = lambda: dict(key=k, name=name, lang=lang, accent=ACC.get(c["recipe"], "#f2c14e"), films=[dict(f) for f in films], caps={}, shots=0, stills=0, gifs=0,
                                   industry=[], tags="", cta_site=None, no_h3=True, ui=ui)
    PV.SCRP = f"{WORK}/pv3"; os.makedirs(f"{PV.SCRP}/{k}", exist_ok=True)
    open(f"{PV.SCRP}/{k}/classic.html", "w", encoding="utf-8").write(f'<html lang="{lang}"><body>{offer_section(c)}</body></html>')
    PV.build(k, pub)
    page = strip(open(f"{pub}/index.html", encoding="utf-8").read()); open(f"{pub}/index.html", "w", encoding="utf-8").write(page)
    # small local assets: icon, font, hero loop (8 s of the first landscape film), email thumbnails
    for f in ("icon.png", "russo.ttf"): shutil.copy(f"{S}/launch/site/{f}", f"{pub}/{f}")
    land = [f for f in films if f["type"] != "social"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-t", "8", "-i", land[0]["src"], "-an", "-vf", "scale=1280:-2", "-c:v", "libx264", "-crf", "27", "-preset", "medium", "-movflags", "+faststart", f"{pub}/hero.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-i", land[0]["src"], "-frames:v", "1", "-vf", "scale=1280:-2", f"{pub}/hero.jpg"], check=True)
    e = dict(EM_LED if led else EM[lang]); fm = lambda s: s.format(n=name, sect=c["sect"], p=PILOT[lang], series=c.get("series", ""))
    paras = [fm(e["p1"]), fm(e["p2"]) + ((" " + ANGLE[c["recipe"]]) if c["recipe"] in ANGLE else ""), fm(e["p3"])]
    items = []
    for f in land[:2]:
        tmp = f"{WORK}/{f['id']}.jpg"
        if not os.path.exists(tmp): urllib.request.urlretrieve(f["poster"], tmp)
        N.thumb(tmp, f"{pub}/email/{f['id']}.jpg")
        items.append(dict(title=f["t"], meta=f'{PV.T[lang]["ind_types"][f["type"]]} · {e["ex"]}', img=f"{page_url}email/{f['id']}.jpg", href=page_url + "#films"))
    content = dict(lang=lang, subject=fm(e["subject"]), preheader=fm(e["pre"]), greeting=e["greeting"], paras=paras, films=items, cta=dict(label=e["cta"], href=page_url),
                   note=fm(e["note"]), sign=dict(name="Blagoj N.", role=e["role"]), closing=e["closing"], optout=fm(e["optout"]), video_word=e["vw"])
    h, t = M.render(content)
    to = c["to"]
    if to == "NO ADDRESS": h = "<!-- TO: NO ADDRESS -- " + H.escape(c["notes"]).replace("--", "-") + " -->\n" + h
    open(f"{LM}/drafts/DRAFT_{k}_email.html", "w", encoding="utf-8").write(h)
    open(f"{LM}/drafts/DRAFT_{k}_email.txt", "w", encoding="utf-8").write(content["subject"] + "\n" + ("[NO ADDRESS] " + c["notes"] + "\n" if to == "NO ADDRESS" else "") + "\n" + t + "\n")
    words = len(re.findall(r"\w+", " ".join(paras)))
    errs = validate(page) + [x + " (email)" for x in validate(h)]
    return dict(key=k, name=name, country=c["country"], lang=lang, to=to, subject=content["subject"], url=page_url, films=ids, notes=c["notes"], words=words, errs=errs, pub=pub)

def offer_pdfs(rows):
    JS = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--disable-dev-shm-usage']});for(const f of process.argv.slice(1)){const p=await b.newPage();await p.goto('file://'+f);await p.pdf({path:f.replace('offer.html','offer.pdf'),format:'A4',printBackground:true});await p.close()}await b.close()})()"
    files = []
    for r in rows:
        c = next(x for x in CFG["companies"] if x["key"] == r["key"])
        h = (f'<html lang="{c["lang"]}"><meta charset="utf-8"><style>body{{font:15px/1.5 system-ui,sans-serif;margin:40px;color:#111}}h1{{font-size:28px}}.price{{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0}}'
             f'.card{{border:1px solid #ccc;border-radius:12px;padding:14px;flex:1;min-width:200px}}.amt{{font-size:22px;font-weight:700}}.tag{{font-size:11px;background:#f2c14e;padding:2px 8px;border-radius:99px}}'
             f'.eyebrow{{display:none}}.terms{{font-size:12px;color:#555}}.u{{font-size:12px;color:#555}}</style><body><h1>BIG DOGMA · AI STUDIO | MK</h1><p>{H.escape(c["name"])}</p>{offer_section(c)}<p class="terms">inf.unit@bigdogma.tech · bigdogma.tech</p></body></html>')
        f = f"{r['pub']}/offer.html"; open(f, "w", encoding="utf-8").write(h); files.append(f)
    subprocess.run(["node", "-e", JS] + files, check=True, env=dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip(), TMPDIR="/dev/shm"))
    for f in files: os.remove(f)

def index(rows):
    L = ["# More lead pages and drafts, 28 Nov 2026 (NOT sent, NOT published)", "",
         "Pages: /dev/shm/pub_more/<token>/ (upload each token folder to the pitch site). Drafts: leads_more/drafts/DRAFT_<key>_email.{html,txt} (txt: subject on line 1).",
         "Films are bigdogma.tech examples by sector (each URL checked: HTTP 200), not films made for the company.", "",
         "| key | company | country | language | to (address) | subject | page URL | films used | notes |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append("| " + " | ".join(str(x).replace("|", "/") for x in (r["key"], r["name"], r["country"], r["lang"], r["to"], r["subject"], r["url"], ", ".join(f.replace("_commercial", "").replace("cf_", "") for f in r["films"]), r["notes"])) + " |")
    L += ["", "## Skipped", ""] + [f"- {s['name']} ({s['country']}): {s['why']}" for s in CFG["skipped"]]
    open(f"{LM}/INDEX.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

if __name__ == "__main__":
    keys = sys.argv[1:]; cos = [c for c in CFG["companies"] if not keys or c["key"] in keys]
    os.makedirs(WORK, exist_ok=True); os.makedirs(f"{LM}/drafts", exist_ok=True)
    urls = sorted(f"{SITE}/films/{fid}.{x}" for fid in PLAN for x in ("mp4", "jpg"))
    with ThreadPoolExecutor(16) as ex: st = dict(zip(urls, ex.map(head, urls)))
    LIVE.update({fid: st[f"{SITE}/films/{fid}.mp4"] == 200 and st[f"{SITE}/films/{fid}.jpg"] == 200 for fid in PLAN})
    print("films in plans", len(PLAN), "live (mp4 + jpg 200):", sum(LIVE.values()), flush=True)
    rows = []
    for c in cos:
        r = build(c); rows.append(r); print(r["key"], len(r["films"]), "films", r["words"], "words", r["errs"] or "ok", flush=True)
    offer_pdfs(rows)
    # every bigdogma.tech URL the pages reference (films, BD gallery, scripts, fonts) must answer 200
    refs = set()
    for r in rows: refs |= set(re.findall(r'https://bigdogma\.tech/[^"\'\s)<>]+', open(f"{r['pub']}/index.html", encoding="utf-8").read()))
    refs = {u.rstrip("\\") for u in refs if not u.endswith("/")}
    with ThreadPoolExecutor(16) as ex: st = dict(zip(sorted(refs), ex.map(head, sorted(refs))))
    bad = {u: s for u, s in st.items() if s != 200}; print("referenced bigdogma.tech urls", len(st), "not 200:", bad or "none")
    if not keys: index(rows)
    else:
        print("partial run: INDEX.md not rewritten")
    json.dump([{k: v for k, v in r.items() if k != "pub"} for r in rows], open(f"{WORK}/rows.json", "w"), ensure_ascii=False)
