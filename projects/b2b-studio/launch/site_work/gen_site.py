# BIG DOGMA public studio website generator (one long page, MK primary + EN toggle).
# All copy lives in TX (key -> (mk, en)); the template marks elements with @="key" (text), @h="key" (HTML)
# and @a="attr:key;attr2:key2" (attributes). MK is rendered into the HTML, both languages go to i18n.js.
# Run:  /usr/bin/python3 gen_site.py    (media is built separately by build_media.py)
import os, re, json, html, shutil, subprocess, hashlib, glob
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUT = f"{S}/launch/site"; WORK = f"{S}/launch/site_work"
SITE_URL = "https://bigdogma.tech"
E = html.escape
import sys; sys.path.insert(0, f"{S}/launch/site_work"); import gallery_data as G

# ------------------------------------------------------------------ contact details: brand/brand.json is the only source
# Only fields that hold a real value are rendered. A field that still looks like a placeholder (an example.* domain, XXX digits)
# is dropped with a warning, so the page never links to someone else's domain or to a made-up phone number.
BRAND = json.load(open(f"{S}/brand/brand.json", encoding="utf-8"))
def _field(k):
    v = str(BRAND.get(k) or "").strip()
    if v and ("example." in v.lower() or "XXX" in v.upper()):
        print(f"WARNING: brand.json {k!r} looks like a placeholder ({v}); left off the site"); return ""
    return v
CONTACT = {k: _field(k) for k in ("email", "phone", "whatsapp", "web")}
CONTACT["tel"] = ("+" + re.sub(r"\D", "", CONTACT["phone"])) if CONTACT["phone"] else ""
CONTACT["wa"] = re.sub(r"\D", "", CONTACT["whatsapp"])
CONTACT["web_href"] = (CONTACT["web"] if CONTACT["web"].startswith("http") else "https://" + CONTACT["web"]) if CONTACT["web"] else ""
if not CONTACT["email"]: print("WARNING: no email in brand.json: the quote form is left out")

# ------------------------------------------------------------------ films (public-safe studio demos only)
FILMS = [  # id, category, title mk, title en, line mk, line en
 # timelapse_renovation is left out on purpose: its VO lines land on "before" shots (it was pulled from the social kit too)
 ("sector_automotive", "sec", "Автомобилска индустрија", "Automotive industry", "Направено во Македонија, возено низ Европа.", "Made in North Macedonia, driven across Europe."),
 ("sector_food", "sec", "Прехранбена индустрија", "Food industry", "Вкусот што го знаете.", "The taste you know."),
 ("sector_pharma", "sec", "Фармација", "Pharma", "Спакувано за пациентите.", "Packed for patients."),
 ("sector_wine", "sec", "Винарии", "Wineries", "Секое шише, една приказна.", "Every bottle, a story."),
 ("sector_steel_cement", "sec", "Челик и цемент", "Steel and cement", "Материјал на кој градиме.", "The material we build on."),
 ("sector_real_estate", "sec", "Недвижности", "Real estate", "Живот над градот.", "Life above the city."),
 ("sector_recruitment", "sec", "Вработување", "Recruitment", "Работа на која сте горди.", "Work you can be proud of."),
 ("sector_product_launch", "sec", "Лансирање производ", "Product launch", "Направено за вашиот живот.", "Made for your life."),
 ("showreel_macedonian_industry", "sec", "Македонска индустрија", "Industry of North Macedonia", "Македонија произведува. Ние го покажуваме.", "North Macedonia makes it. We show it."),
 ("timelapse_construction", "tl", "Градба", "Construction", "Од празен плац до вашите клучеви.", "From an empty plot to your keys."),
 ("timelapse_developer", "tl", "Инвеститори", "Property developers", "Резервирајте пред да се изгради.", "Reserve before it is built."),
 ("timelapse_apartment_staging", "tl", "Опремување станови", "Apartment staging", "Дом од првиот ден.", "Home from day one."),
 ("timelapse_interior_design", "tl", "Внатрешен дизајн", "Interior design", "Простор што личи на вас.", "A space that feels like you."),
 ("timelapse_office_fitout", "tl", "Опремување канцеларии", "Office fit-out", "Подготвено за вселување.", "Ready to move in."),
 ("timelapse_store_fitout", "tl", "Опремување продавници", "Store fit-out", "Подготвено за отворање.", "Ready to open."),
 ("timelapse_expo_stand", "tl", "Саемски штандови", "Expo stands", "Штанд што привлекува погледи.", "A stand that draws the eye."),
 ("timelapse_landscaping", "tl", "Хортикултура", "Landscaping", "Градина за уживање.", "A garden to enjoy."),
 ("timelapse_solar", "tl", "Соларни системи", "Solar systems", "Енергија од сонцето, секој ден.", "Energy from the sun, every day."),
 ("timelapse_road", "tl", "Патна инфраструктура", "Road infrastructure", "Пат што ги поврзува луѓето.", "A road that connects people."),
]
# card labels come from the web encodes that are served (durations.txt holds the master durations, ~0.15 s longer,
# which rounded up to one second too many); floored like a video player shows them
def _probe(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True, check=True).stdout)
DUR = {f[0]: _probe(f"{OUT}/films/{f[0]}.mp4") for f in FILMS}
def mmss(s): s = int(s); return f"{s // 60}:{s % 60:02d}"

# ------------------------------------------------------------------ copy
TX = {
 "meta.title": ("BIG DOGMA · AI видео студио, Скопје", "BIG DOGMA · AI video studio, Skopje"),
 "meta.desc": ("AI видео за вашиот бизнис: реклами и брендирани филмови без снимање, готови за 7–10 дена по одобрување на клучните кадри. AI студио од Скопје за Македонија, Србија, Албанија и Косово.",
               "AI video for your business: ads and branded films with no filming, ready 7–10 days after key-frame approval. An AI studio in Skopje for North Macedonia, Serbia, Albania and Kosovo."),
 "skip": ("Прескокнете до содржината", "Skip to content"),
 "pre.skip": ("Прескокнете", "Skip"),
 "nav.label": ("Главна навигација", "Main navigation"),
 "nav.home": ("BIG DOGMA, на почеток", "BIG DOGMA, back to top"),
 "nav.reel": ("Шоурил", "Showreel"), "nav.work": ("Филмови", "Films"), "nav.how": ("Процес", "Process"),
 "nav.price": ("Цени", "Pricing"), "nav.faq": ("Прашања", "FAQ"), "nav.contact": ("Контакт", "Contact"),
 "nav.cta": ("Побарајте понуда", "Get a quote"),
 "nav.menu": ("Мени", "Menu"), "nav.lang": ("Јазик", "Language"),
 "hud.tag": ("AI рендер · 720p · 24 fps", "AI render · 720p · 24 fps"),
 "hud.prompt": ("Сцена", "Scene"),
 "hud.gen": ("Генерирање…", "Generating…"), "hud.done": ("Готово ✓", "Done ✓"),
 "hud.text": ("Лого филм: знакот BD излеан во злато, издлабен во мраз, нацртан со огномет, тетовиран на кожа. Секој кадар е генериран со AI.",
              "Logo film: the BD mark cast in gold, carved in ice, drawn by fireworks, tattooed on skin. Every shot generated with AI."),
 "hero.pill": ("AI видео студио · Скопје", "AI video studio · Skopje"),
 "hero.h1": ("AI видео за <em>вашиот бизнис</em>", "AI video for <em>your business</em>"),
 "hero.sub": ("Готова реклама за 7–10 дена по одобрување на клучните кадри, без снимање.", "A finished ad 7–10 days after you approve the key frames, with no filming."),
 "hero.cta1": ("Погледнете го шоурилот", "Watch the showreel"), "hero.cta2": ("Побарајте понуда", "Get a quote"),
 "hero.ai": ("Сите кадри на оваа страница се генерирани со вештачка интелигенција.", "Every shot on this page is generated with artificial intelligence."),
 "m1": ("Текст → Видео", "Text → Video"), "m2": ("Слика → Видео", "Image → Video"), "m3": ("AI глас на македонски", "AI voice in Macedonian"),
 "m4": ("Оригинална музика", "Original music"), "m5": ("16:9 · 9:16", "16:9 · 9:16"), "m6": ("Вие ги одобрувате клучните кадри", "You approve the key frames"),
 "m7": ("MK · SR · SQ", "MK · SR · SQ"), "m8": ("Испорака во Full HD", "Full HD delivery"), "m9": ("Титлови", "Subtitles"),
 "st1": ("дена од одобрени клучни кадри до готов филм", "days from approved key frames to a finished film"), "st2": ("дена снимање", "days of filming"),
 "st3": ("формати: 16:9 и 9:16", "formats: 16:9 and 9:16"), "st4": ("јазици: MK · SR · SQ", "languages: MK · SR · SQ"),
 "reel.e": ("Шоурил", "Showreel"),
 "reel.h": ("56 секунди. Ниту еден снимен кадар.", "56 seconds. Not a single filmed shot."),
 "reel.p": ("Индустрија, градба, храна, вино, енергија: сè што ќе видите е генерирано со вештачка интелигенција. Без камера, без екипа, без локација.",
            "Industry, construction, food, wine, energy: everything you see is generated with artificial intelligence. No camera, no crew, no location. (On-screen text in Macedonian.)"),
 "reel.t": ("Шоурил на студиото", "Studio showreel"),
 "reel.h169": ("16:9 хоризонтално", "16:9 landscape"), "reel.v916": ("9:16 вертикално", "9:16 vertical"),
 "reel.fmt": ("Формат на видеото", "Video format"),
 "reel.vid": ("Шоурил на BIG DOGMA, AI-генерирано видео со музика", "BIG DOGMA showreel, AI-generated video with music"),
 "reel.note": ("Видео изработено со вештачка интелигенција · AI-generated video.", "AI-generated video · Видео изработено со вештачка интелигенција."),
 "work.e": ("Демо филмови", "Demo films"),
 "work.h": ("Филм за секој сектор", "A film for every sector"),
 "work.p": ("Демо концепти на студиото, генерирани со вештачка интелигенција, без ниту еден ден снимање. Кликнете на филм за да го пуштите со глас, музика и титлови.",
            "Studio demo concepts, generated with AI, without a single day of filming. Click a film to play it with voice, music and subtitles (on-screen text in Macedonian; English subtitles on every film)."),
 "work.filter": ("Филтер по тип", "Filter by type"),
 "f.all": ("Сите", "All"), "f.sec": ("Сектори", "Sectors"), "f.tl": ("Тајмлапс", "Timelapse"),
 "cat.sec": ("Сектор", "Sector"), "cat.tl": ("Тајмлапс", "Timelapse"),
 "work.play": ("Пуштете го филмот", "Play film"),
 "work.note": ("Сите филмови се демо концепти на студиото: сцените се генерирани и не прикажуваат вистински објекти, производи или луѓе.",
               "All films are studio demo concepts: the scenes are generated and do not show real sites, products or people."),
 "lb.close": ("Затворете", "Close"), "lb.prev": ("Претходен филм", "Previous film"), "lb.next": ("Следен филм", "Next film"),
 "lb.ai": ("Демо концепт на студиото · Видео изработено со вештачка интелигенција", "Studio demo concept · AI-generated video"),
 "how.e": ("Процес", "Process"),
 "how.h": ("Од бриф до готов филм", "From brief to finished film"),
 "how.p": ("Вие не снимате ништо. Ни треба само идеја, неколку фотографии или рендери и вашето лого. Готовиот филм го добивате за 7–10 дена по одобрувањето на клучните кадри.",
            "You do not film anything. All we need is an idea, a few photos or renders and your logo. You get the finished film 7–10 days after you approve the key frames."),
 "s1.h": ("Бриф", "Brief"), "s1.p": ("15 минути разговор, во живо или онлајн: цел, публика, порака. Ни праќате фотографии, рендери или производи.",
                                  "A 15-minute call, in person or online: goal, audience, message. You send us photos, renders or products."),
 "s2.h": ("Клучни кадри", "Key frames"), "s2.p": ("Пишуваме сценарио и подготвуваме клучни кадри. Вие ги одобрувате пред да почне анимацијата.",
                                              "We write the script and prepare the key frames. You approve them before any animation starts."),
 "s3.h": ("AI продукција", "AI production"), "s3.p": ("AI анимација на кадрите, глас, оригинална музика, титлови и вашиот завршен кадар.",
                                                   "AI animation of every shot, voice-over, original music, subtitles and your end card."),
 "s4.h": ("Испорака", "Delivery"), "s4.p": ("Готови формати 16:9 и 9:16 за веб, мрежи и екрани. Една рунда корекции е вклучена.",
                                         "Finished 16:9 and 9:16 files for web, social and screens. One round of revisions is included."),
 "how.vt": ("Како настанува рекламата", "How an ad is made"),
 "how.vc": ("Пример од градежништво: од фотографија на плацот до готова реклама (видеото е на македонски).",
            "A construction example: from a photo of the plot to a finished ad (video in Macedonian)."),
 "how.vid": ("Видео: како настанува AI реклама за градежништво", "Video: how an AI construction ad is made"),
 "cmp.t": ("Од една слика до AI видео", "From one image to AI video"),
 "cmp.c": ("Лево е клучниот кадар, десно истиот кадар оживеан со AI: светлото минува од зајдисонце во вечер. Повлечете ја линијата.",
           "On the left is the key frame, on the right the same frame brought to life with AI: the light turns from sunset to evening. Drag the line."),
 "cmp.l": ("Слика", "Image"), "cmp.r": ("AI видео", "AI video"),
 "cmp.aria": ("Споредба: клучен кадар наспроти AI видео", "Comparison: key frame versus AI video"),
 "cmp.alt": ("Клучен кадар: кровна тераса со маслинови дрвца и лежалки над градот на зајдисонце", "Key frame: a rooftop terrace with olive trees and loungers above the city at sunset"),
 "price.e": ("Цени", "Pricing"),
 "price.h": ("Јасни пакети, без изненадувања", "Clear packages, no surprises"),
 "price.p": ("Почнете со пилот-филм. Ако ви се допадне, продолжуваме со кампања или месечна содржина.", "Start with a pilot film. If you like it, we continue with a campaign or monthly content."),
 "p1.n": ("Пилот", "Pilot"), "p1.a": ("€600–900", "€600–900"),
 "p1.l1": ("1 филм, 20–30 секунди", "1 film, 20–30 seconds"), "p1.l2": ("Формати 16:9 и 9:16", "16:9 and 9:16 formats"),
 "p1.l3": ("Музика, вашето лого и повик за акција", "Music, your logo and a call to action"), "p1.l4": ("Готово за 7–10 дена по одобрување на клучните кадри", "Ready 7–10 days after key-frame approval"),
 "p2.n": ("Лансирање", "Launch"), "p2.a": ("€1.800–3.500", "€1,800–3,500"), "p2.tag": ("Препорачан", "Recommended"),
 "p2.l1": ("Главен филм, 45–60 секунди", "Hero film, 45–60 seconds"), "p2.l2": ("3 рекламни спота", "3 ad spots"),
 "p2.l3": ("10 кратки клипови за мрежи", "10 short clips for social media"), "p2.l4": ("Сите формати за кампања", "Every format for the campaign"),
 "p3.n": ("Месечна содржина", "Monthly content"), "p3.a": ("€400–900", "€400–900"), "p3.per": ("месечно", "per month"),
 "p3.l1": ("6–8 нови клипови секој месец", "6–8 new clips every month"), "p3.l2": ("Формати за Reels, TikTok и Stories", "Formats for Reels, TikTok and Stories"),
 "p3.l3": ("Минимум 3 месеци", "Minimum 3 months"), "p3.l4": ("Постојан визуелен стил", "A consistent visual style"),
 "price.vat": ("без ДДВ", "excl. VAT"),
 "bund.h": ("Пакети по сектор", "Packages by sector"),
 "bund.p": ("Готови пакети за најчестите проекти. Секој почнува со вашите фотографии, планови или рендери.", "Ready-made packages for the most common projects. Each one starts from your own photos, plans or renders."),
 "b1.n": ("Девелопер", "Developer"), "b1.a": ("€1.500–4.000", "€1,500–4,000"), "b1.u": ("по проект", "per project"),
 "b1.l1": ("Тајмлапс на градбата, од ископ до клучеви", "Construction timelapse, from excavation to keys"), "b1.l2": ("Продажен филм за станови пред изградба", "Sales film for off-plan apartments"), "b1.l3": ("Формати за огласи, мрежи и продажна канцеларија", "Formats for ads, social media and the sales office"),
 "b2.n": ("Опремување станови", "Apartment staging"), "b2.a": ("€300–800", "€300–800"), "b2.u": ("по стан", "per apartment"),
 "b2.l1": ("Од празен до целосно опремен стан", "From an empty to a fully furnished apartment"), "b2.l2": ("Од фотографиите на вашите станови", "From photos of your apartments"), "b2.l3": ("Пакет од 5 станови: €1.500", "Bundle of 5 apartments: €1,500"),
 "b3.n": ("Ентериер и реновирање", "Interiors and renovation"), "b3.a": ("€300–1.000", "€300–1,000"), "b3.u": ("по простор", "per space"),
 "b3.l1": ("Пред и потоа, во еден тајмлапс", "Before and after in one timelapse"), "b3.l2": ("Од голи ѕидови до готов простор", "From bare walls to a finished space"), "b3.l3": ("За студија за ентериер, кујни и бањи", "For interior studios, kitchens and bathrooms"),
 "b4.n": ("Тајмлапс проект", "Project timelapse"), "b4.a": ("€500–2.000", "€500–2,000"), "b4.u": ("по проект", "per project"),
 "b4.l1": ("Сончеви централи, патишта и дворови", "Solar plants, roads and gardens"), "b4.l2": ("Уредување продавници и саемски штандови", "Shop fit-outs and exhibition stands"), "b4.l3": ("Фаза по фаза, со вашето лого", "Stage by stage, with your logo"),
 "b5.n": ("Сезонска кампања", "Seasonal campaign"), "b5.a": ("€2.500–6.000", "€2,500–6,000"), "b5.u": ("по кампања", "per campaign"),
 "b5.l1": ("Семеен рекламен филм", "A family ad film"), "b5.l2": ("Филм од производството", "A film from your production"), "b5.l3": ("Сезонски спотови за празници и акции", "Seasonal spots for holidays and promotions"),
 "b6.n": ("Бренд на работодавач", "Employer branding"), "b6.a": ("€1.500–3.500", "€1,500–3,500"), "b6.u": ("по пакет", "per package"),
 "b6.l1": ("Филм за вработување", "A recruitment film"), "b6.l2": ("Филм за вашиот тим и процес", "A film about your team and process"), "b6.l3": ("Кратки клипови за огласи за работа", "Short clips for job ads"),
 "price.cta": ("Побарајте понуда", "Get a quote"),
 "price.terms": ("Цените се во евра, без ДДВ. Рок 7–10 дена од одобрувањето на клучните кадри · 1 рунда корекции · права за веб, социјални мрежи и екрани (ТВ и платени кампањи по договор) · секое видео е означено како изработено со AI.",
                 "Prices in euro, excluding VAT. Delivery 7–10 days after key-frame approval · 1 round of revisions · usage rights for web, social media and screens (TV and paid campaigns by agreement) · every video is labelled as AI-generated."),
 "faq.e": ("Прашања", "FAQ"), "faq.h": ("Често поставувани прашања", "Frequently asked questions"),
 "q1": ("Што е AI видео?", "What is AI video?"),
 "a1": ("Видео во кое кадрите не се снимаат со камера, туку се генерираат со модели за вештачка интелигенција. Ние го пишуваме сценариото, ги создаваме клучните кадри, ги анимираме и додаваме глас, музика и титлови, па монтираме готов филм со вашиот бренд.",
        "Video where the shots are not filmed with a camera but generated with artificial intelligence models. We write the script, create the key frames, animate them, add voice-over, music and subtitles, and edit a finished film with your brand."),
 "q2": ("Дали треба да снимаме нешто?", "Do we need to film anything?"),
 "a2": ("Не. Доволни се идеја, неколку фотографии или рендери, вашето лого и кратко објаснување. Ако веќе имате фотографии од производ или објект, ги користиме како појдовна точка.",
        "No. An idea, a few photos or renders, your logo and a short explanation are enough. If you already have photos of a product or site, we use them as the starting point."),
 "q3": ("Колку трае изработката?", "How long does it take?"),
 "a3": ("Пилот-филмот е готов за 7–10 дена од одобрувањето на клучните кадри. За пакетот Лансирање и за месечна содржина рокот го договараме според обемот.",
        "A pilot film is ready 7–10 days after you approve the key frames. For the Launch package and monthly content we agree the timeline based on the scope."),
 "q4": ("Можеме ли да ги користиме нашите производи и лого?", "Can we use our own products and logo?"),
 "a4": ("Да. Вашето лого, боите и завршниот кадар се дел од секој филм, а производите ги поставуваме врз основа на ваши фотографии. Секој клучен кадар го одобрувате пред анимацијата, па на екранот оди само она што сте го потврдиле.",
        "Yes. Your logo, colours and end card are part of every film, and we build your products from your own photos. You approve every key frame before animation, so only what you have signed off goes on screen."),
 "q5": ("Кој ги има правата и дали видеото е означено како AI?", "Who owns the rights, and is the video labelled as AI?"),
 "a5": ("Добивате право на користење на веб, социјални мрежи и екрани; ТВ и платени кампањи по договор. Секое видео е јасно означено како изработено со вештачка интелигенција, како што бараат и платформите (Meta, TikTok, YouTube).",
        "You get usage rights for web, social media and screens; TV and paid campaigns by agreement. Every video is clearly labelled as made with artificial intelligence, as the platforms (Meta, TikTok, YouTube) also require."),
 "q6": ("На кои јазици работите?", "Which languages do you work in?"),
 "a6": ("Глас и титлови на македонски, српски и албански, за пазарите во Македонија, Србија, Албанија и Косово. Англиски титлови по барање.",
        "Voice-over and subtitles in Macedonian, Serbian and Albanian, for markets in North Macedonia, Serbia, Albania and Kosovo. English subtitles on request."),
 "c.e": ("Контакт", "Contact"),
 "c.h": ("Да го направиме вашиот прв AI филм", "Let's make your first AI film"),
 "c.p": ("Следен чекор: 15 минути разговор, во живо во Скопје или онлајн. Кажете ни што продавате и каде сакате да го прикажете.",
         "Next step: a 15-minute call, in person in Skopje or online. Tell us what you sell and where you want to show it."),
 "c.phone": ("Телефон", "Phone"), "c.mail": ("Е-пошта", "Email"), "c.wa": ("WhatsApp", "WhatsApp"), "c.wa.v": ("Пишете ни порака", "Send us a message"),
 "c.web": ("Веб", "Web"), "c.where": ("Студио", "Studio"), "c.where.v": ("Скопје, Македонија", "Skopje, North Macedonia"),
 "fm.h": ("Побарајте понуда", "Request a quote"),
 "fm.name": ("Име и презиме", "Full name"), "fm.company": ("Компанија", "Company"), "fm.email": ("Е-пошта", "Email"), "fm.phone": ("Телефон (по желба)", "Phone (optional)"),
 "fm.pkg": ("Пакет", "Package"), "fm.pkg0": ("Сè уште не знам", "Not sure yet"),
 "fm.msg": ("Што сакате да прикажеме?", "What would you like us to show?"),
 "fm.msg.ph": ("На пр. нов производ, градба, вработување, кампања за празници…", "E.g. a new product, a building project, recruitment, a holiday campaign…"),
 "fm.send": ("Испратете барање", "Send request"),
 "fm.note": ("Копчето ја отвора вашата апликација за е-пошта со пополнета порака. Ништо не се зачувува на оваа страница.", "The button opens your email app with the message filled in. Nothing is stored on this website."),
 "fm.subj": ("Барање за понуда", "Quote request"),
 "fm.err": ("Пополнете име, е-пошта и порака.", "Please fill in your name, email and message."),
 "ft.ai": ("Видео изработено со вештачка интелигенција · AI-generated video. Сите филмови и кадри на оваа страница се демо концепти на студиото, генерирани со AI; не прикажуваат вистински објекти, производи или луѓе.",
           "AI-generated video · Видео изработено со вештачка интелигенција. All films and shots on this page are studio demo concepts generated with AI; they do not show real sites, products or people."),
 "ft.rights": ("© 2026 BIG DOGMA · AI STUDIO | Skopje", "© 2026 BIG DOGMA · AI STUDIO | Skopje"),
 "ft.top": ("Нагоре", "Back to top"),
 "logo.alt": ("BIG DOGMA, AI студио, Скопје", "BIG DOGMA, AI studio, Skopje"),
}
for k, f in (("c.phone", "phone"), ("c.wa", "whatsapp"), ("c.wa.v", "whatsapp"), ("c.web", "web")):
    if not CONTACT[f]: TX.pop(k)
TX.update({
 "nav.gal": ("Галерија", "Gallery"),
 "ai.note": ("Видео изработено со вештачка интелигенција · AI-generated video.", "AI-generated video · Видео изработено со вештачка интелигенција."),
 "sec.e": ("Сектори", "Sectors"),
 "sec.h": ("Вашиот сектор, кадар по кадар", "Your sector, shot by shot"),
 "sec.p": ("Покрај секој демо филм има уште кадри од истиот свет. Од ваков материјал ја монтираме вашата реклама, само со вашите производи, простори и лого.",
           "Beside every demo film are more shots from the same world. This is the kind of material we cut your ad from, only with your products, sites and logo."),
 "sec.tabs": ("Изберете сектор", "Choose a sector"),
 "sec.film": ("Демо филм · глас, музика и титлови", "Demo film · voice, music and subtitles"),
 "sec.shots": ("Уште кадри од истиот сектор", "More shots from the same sector"),
 "gal.e": ("AI галерија", "AI gallery"),
 "gal.h": (f"{len(G.CLIPS)} кадри. Ниту една камера.", f"{len(G.CLIPS)} shots. Not one camera."),
 "gal.p": ("Кратки кадри генерирани со вештачка интелигенција за различни индустрии. Се пуштаат сами, без звук, кога ќе се појават на екранот.",
           "Short AI-generated shots for different industries. They play on their own, muted, as they scroll into view."),
 "gal.filter": ("Филтер по сектор", "Filter by sector"),
 "gal.more": (f"Прикажете ги сите {len(G.CLIPS)} кадри", f"Show all {len(G.CLIPS)} shots"),
 "i2v.e": ("Слика → движење", "Image → motion"),
 "i2v.h": ("Од една слика до живо видео", "From one image to living video"),
 "i2v.p": ("Секој кадар почнува како слика: ваша фотографија, рендер или клучен кадар што вие го одобрувате. Потоа AI ја анимира според краток опис на движењето.",
           "Every shot starts as an image: your photo, a render or a key frame you approve. AI then animates it from a short description of the motion."),
 "i2v.img": ("Клучен кадар", "Key frame"), "i2v.vid": ("AI видео", "AI video"), "i2v.prompt": ("Додадено движење:", "Added motion:"),
 "bu.e": ("Тајмлапс", "Timelapse"),
 "bu.h": ("Фаза по фаза, од нула до клучеви", "Stage by stage, from zero to the keys"),
 "bu.p": ("Секоја фаза е клучен кадар, а AI го анимира преминот до следната. Изберете проект, па гледајте како расте или кликнете на која било фаза.",
          "Each stage is a key frame, and AI animates the move to the next one. Choose a project and watch it grow, or click any stage."),
 "bu.tabs": ("Изберете проект", "Choose a project"),
 "bu.steps": ("Фази на проектот", "Project stages"),
 "bu.pause": ("Паузирајте", "Pause"), "bu.play": ("Пуштете", "Play"),
})
for k, mk_, en_ in G.SECTORS: TX[f"g.{k}"] = (mk_, en_)
for cid, _src, _sec, cmk, cen in G.CLIPS: TX[f"cl.{cid}"] = (cmk, cen)
for cid, _k, tmk, ten, pmk, pen in G.I2V: TX[f"i2v.{cid}.t"] = (tmk, ten); TX[f"i2v.{cid}.p"] = (pmk, pen)
for bk, bmk, ben, stages in G.BUILDS:
    TX[f"bu.{bk}"] = (bmk, ben)
    for i, (_k, _c, smk, sen) in enumerate(stages): TX[f"bu.{bk}.{i}"] = (smk, sen)
for fid, cat, tmk, ten, lmk, len_ in FILMS:
    TX[f"{fid}.t"] = (tmk, ten); TX[f"{fid}.l"] = (lmk, len_)
    TX[f"{fid}.alt"] = (f"Кадар од демо филмот: {tmk}", f"Still from the demo film: {ten}")

# ------------------------------------------------------------------ cache-busting
# nginx serves media for 30 days without revalidation, so every media URL carries ?v=<content hash>: a rebuilt file gets a new URL.
def u(rel):
    return f"{rel}?v={hashlib.md5(open(f'{OUT}/{rel}', 'rb').read()).hexdigest()[:10]}"

# ------------------------------------------------------------------ template
mk = lambda k: TX[k][0]
FILM_CARDS = "\n".join(f"""<li class="fc rv" data-cat="{cat}"><a href="{u(f'films/{fid}.mp4')}" data-film="{fid}">
<span class="im"><img src="{u(f'films/{fid}.jpg')}" @a="alt:{fid}.alt" width="960" height="540" loading="lazy" decoding="async"><span class="ct" @="cat.{cat}"></span><span class="pl" aria-hidden="true"></span><span class="du">{mmss(DUR[fid])}</span></span>
<span class="tx"><span class="h3" @="{fid}.t"></span><span class="ln" @="{fid}.l"></span></span><span class="sr" @="work.play"></span></a></li>""" for fid, cat, *_ in FILMS)
n_sec = sum(1 for f in FILMS if f[1] == "sec"); n_tl = len(FILMS) - n_sec
FILM_JSON = json.dumps([{"id": f[0], "src": u(f"films/{f[0]}.mp4"), "poster": u(f"films/{f[0]}.jpg"),
                         "sub": {L: u(f"subs/{f[0]}.{L}.vtt") for L in ("mk", "en") if os.path.exists(f"{OUT}/subs/{f[0]}.{L}.vtt")}} for f in FILMS])
MARQ = "".join(f'<span @="m{i}"></span>' for i in range(1, 10))
CHECK = '<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def plan(n, hot=False):
    per = f'<span class="per"><span @="p3.per"></span> · <span @="price.vat"></span></span>' if n == 3 else '<span class="per" @="price.vat"></span>'
    tag = '<span class="tag" @="p2.tag"></span>' if hot else ""
    lis = "".join(f'<li>{CHECK}<span @="p{n}.l{i}"></span></li>' for i in range(1, 5))
    return f"""<article class="plan rv{' hot' if hot else ''}">{tag}<h3 @="p{n}.n"></h3><div class="amt" @="p{n}.a"></div>{per}<ul>{lis}</ul>
<a class="btn {'a' if hot else 'b'}" href="#contact" data-pkg="p{n}.n" @="price.cta"></a></article>"""
def bundle(n):
    lis = "".join(f'<li>{CHECK}<span @="b{n}.l{i}"></span></li>' for i in range(1, 4))
    return f"""<article class="plan sm rv"><h3 @="b{n}.n"></h3><div class="amt" @="b{n}.a"></div><span class="per"><span @="b{n}.u"></span> · <span @="price.vat"></span></span><ul>{lis}</ul>
<a class="btn b" href="#contact" data-pkg="b{n}.n" @="price.cta"></a></article>"""
BUNDLES = "".join(bundle(i) for i in range(1, 7))
FAQ = "".join(f'<details class="rv"><summary><span @="q{i}"></span><i aria-hidden="true"></i></summary><p @="a{i}"></p></details>' for i in range(1, 7))
STEPS = "".join(f'<li class="step rv"><span class="n">0{i}</span><h3 @="s{i}.h"></h3><p @="s{i}.p"></p></li>' for i in range(1, 5))
I_PHONE = '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z"/></svg>'
I_MAIL = '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4.2l-8 5-8-5V6l8 5 8-5z"/></svg>'
I_WA = '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.15l-.3-.18-3 .78.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.25-.12-1.47-.72-1.7-.8s-.39-.12-.56.12-.64.8-.78.97-.29.18-.54.06a6.7 6.7 0 01-3.3-2.9c-.25-.43.25-.4.71-1.33a.45.45 0 00-.02-.42c-.06-.12-.56-1.34-.76-1.84s-.4-.42-.56-.43h-.48a.92.92 0 00-.66.31 2.8 2.8 0 00-.87 2.07 4.86 4.86 0 001 2.58 11.1 11.1 0 004.27 3.77c1.58.68 2.2.74 3 .62a2.55 2.55 0 001.68-1.18 2.1 2.1 0 00.14-1.18c-.06-.1-.23-.16-.48-.28z"/></svg>'
I_WEB = '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 6h-2.95a15.7 15.7 0 00-1.38-3.56A8.03 8.03 0 0118.9 8zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82A13.6 13.6 0 0112 4.04zM4.26 14a8.2 8.2 0 010-4h3.38a16.5 16.5 0 000 4H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56A7.99 7.99 0 015.08 16zM8.03 8H5.08a7.99 7.99 0 014.33-3.56A15.7 15.7 0 008.03 8zM12 19.96A13.6 13.6 0 0110.09 16h3.82A13.6 13.6 0 0112 19.96zM14.34 14H9.66a14.7 14.7 0 010-4h4.68a14.7 14.7 0 010 4zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 01-4.33 3.56zM16.36 14a16.5 16.5 0 000-4h3.38a8.2 8.2 0 010 4h-3.38z"/></svg>'
I_PIN = '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1114.5 9 2.5 2.5 0 0112 11.5z"/></svg>'
C = {k: E(v) for k, v in CONTACT.items()}
WAYS = "".join(x for x in (
    C["phone"] and f'<li class="rv"><a href="tel:{C["tel"]}">{I_PHONE}<span><small @="c.phone"></small><b>{C["phone"]}</b></span></a></li>',
    C["email"] and f'<li class="rv"><a href="mailto:{C["email"]}">{I_MAIL}<span><small @="c.mail"></small><b>{C["email"]}</b></span></a></li>',
    C["wa"] and f'<li class="rv"><a href="https://wa.me/{C["wa"]}" rel="noopener">{I_WA}<span><small @="c.wa"></small><b @="c.wa.v"></b></span></a></li>',
    C["web"] and f'<li class="rv"><a href="{C["web_href"]}" rel="noopener">{I_WEB}<span><small @="c.web"></small><b>{C["web"]}</b></span></a></li>',
    f'<li class="rv"><div>{I_PIN}<span><small @="c.where"></small><b @="c.where.v"></b></span></div></li>') if x)
FOOT_CT = "".join(x for x in (C["phone"] and f'<a href="tel:{C["tel"]}">{C["phone"]}</a>', C["email"] and f'<a href="mailto:{C["email"]}">{C["email"]}</a>',
                              C["web"] and f'<a href="{C["web_href"]}" rel="noopener">{C["web"]}</a>') if x)
CT_JS = json.dumps({k: CONTACT[k] for k in ("email",) if CONTACT[k]})

# ------------------------------------------------------------------ AI gallery, sectors, image -> motion, build-up
CLIP = {c[0]: c for c in G.CLIPS}
_INTRO = sorted(os.path.basename(f) for f in glob.glob(f"{OUT}/media/intro/*.mp4"))
_HC = {k: [f"media/g/{c[0]}.mp4" for c in G.CLIPS if c[2] == k] for k, *_ in G.SECTORS}
_HC["sec"] = [x for k in ("food", "wine", "steel", "auto", "pharma", "rec", "prod") for x in _HC[k]]
_HC["tl"] = [x for k in ("con", "re", "int", "energy") for x in _HC[k]]
HERO_JSON = json.dumps({"intro": [f"media/intro/{f}" for f in _INTRO], "cat": _HC}, separators=(",", ":"))
def loop(cid, cls="lv", poster=None):
    # muted in-view loop: no src until site.js sees it near the viewport; the poster shows first
    return f'<video class="{cls}" muted loop playsinline preload="none" poster="{u(poster or f"media/g/{cid}.jpg")}" data-loop="{u(f"media/g/{cid}.mp4")}" aria-hidden="true" tabindex="-1"></video>'
# gallery order: round-robin over the sectors, so the first rows already show the range
_by = {k: [c for c in G.CLIPS if c[2] == k] for k, *_ in G.SECTORS}; ORDER = []
while any(_by.values()):
    for k, *_ in G.SECTORS:
        if _by[k]: ORDER.append(_by[k].pop(0))
GAL_N0 = 12
GAL = "\n".join(f'''<li class="gt{' x' if i >= GAL_N0 else ''}{' w' if i % 9 == 0 else ''}" data-sec="{sec}"><figure>{loop(cid)}<span class="aib" aria-hidden="true">AI</span><figcaption><b @="g.{sec}"></b><span @="cl.{cid}"></span></figcaption></figure></li>''' for i, (cid, _s, sec, *_r) in enumerate(ORDER))
GAL_CHIPS = f'<button type="button" class="chip" data-g="all" aria-pressed="true"><span @="f.all"></span> <b>{len(G.CLIPS)}</b></button>' + "".join(
    f'<button type="button" class="chip" data-g="{k}" aria-pressed="false"><span @="g.{k}"></span> <b>{sum(1 for c in G.CLIPS if c[2] == k)}</b></button>' for k, *_ in G.SECTORS)
FILM_BY = {f[0]: f for f in FILMS}
SEC_TABS = "".join(f'<button type="button" role="tab" id="st-{fid}" aria-controls="sp-{fid}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" @="{fid}.t"></button>' for i, (fid, _sh) in enumerate(G.SECTOR_SHOTS))
SEC_PANELS = "\n".join(f'''<div class="spanel" role="tabpanel" id="sp-{fid}" aria-labelledby="st-{fid}"{'' if i == 0 else ' hidden'}>
 <a class="sfilm" href="{u(f'films/{fid}.mp4')}" data-film="{fid}"><span class="im"><img src="{u(f'films/{fid}.jpg')}" @a="alt:{fid}.alt" width="960" height="540" loading="lazy" decoding="async"><span class="pl" aria-hidden="true"></span><span class="du">{mmss(DUR[fid])}</span></span>
  <span class="tx"><small @="sec.film"></small><span class="h3" @="{fid}.t"></span><span class="ln" @="{fid}.l"></span></span><span class="sr" @="work.play"></span></a>
 <div class="sside"><p class="sl" @="sec.shots"></p><ul class="sshots">{"".join(f'<li><figure>{loop(c)}<figcaption @="cl.{c}"></figcaption></figure></li>' for c in shots)}</ul></div>
</div>''' for i, (fid, shots) in enumerate(G.SECTOR_SHOTS))
I2V_CARDS = "\n".join(f'''<li class="pair rv"><div class="pp">
 <figure class="pi"><img src="{u(f'media/k/{G.kf_id(k)}.jpg')}" @a="alt:i2v.{cid}.t" width="960" height="528" loading="lazy" decoding="async"><span class="t" @="i2v.img"></span></figure>
 <span class="arr" aria-hidden="true"></span>
 <figure class="pv">{loop(cid, poster=f"media/g/{cid}_end.jpg")}<span class="t" @="i2v.vid"></span></figure></div>
 <div class="pc"><b @="i2v.{cid}.t"></b><p><small @="i2v.prompt"></small> <span @="i2v.{cid}.p"></span></p></div></li>''' for cid, k, *_ in G.I2V)
BU_TABS = "".join(f'<button type="button" role="tab" id="bt-{bk}" aria-controls="bv-{bk}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" @="bu.{bk}"></button>' for i, (bk, *_r) in enumerate(G.BUILDS))
def bview(i, bk, stages):
    k0 = u(f"media/k/{G.kf_id(stages[0][0])}.jpg"); n = len(stages)
    steps = "".join(f'''<li><button type="button" data-kf="{u(f'media/k/{G.kf_id(k)}.jpg')}" data-clip="{u(f'media/g/{c}.mp4') if c else ''}"{' aria-current="step"' if j == 0 else ''}><img src="{u(f'media/k/{G.kf_id(k)}_t.jpg')}" alt="" width="320" height="176" loading="lazy" decoding="async"><span><i>{j + 1:02d}</i> <span @="bu.{bk}.{j}"></span></span></button></li>''' for j, (k, c, *_r) in enumerate(stages))
    return f'''<div class="bview{' few' if n <= 3 else ''}" role="tabpanel" id="bv-{bk}" aria-labelledby="bt-{bk}"{'' if i == 0 else ' hidden'}>
 <div class="bstage"><img class="bk" src="{k0}" alt="" width="960" height="528" loading="lazy" decoding="async"><video muted playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
  <span class="bn" aria-hidden="true"><b>01</b> / {n:02d}</span><span class="bl" aria-live="polite"></span><span class="aib" aria-hidden="true">AI</span>
  <button type="button" class="bp" @a="aria-label:bu.pause;data-pause:bu.pause;data-play:bu.play"></button><div class="bprog"><i></i></div></div>
 <ol class="bsteps" style="--n:{n}" @a="aria-label:bu.steps">{steps}</ol>
</div>'''
BU_VIEWS = "\n".join(bview(i, bk, st) for i, (bk, _m, _e, st) in enumerate(G.BUILDS))

# site.js validates the form and opens a mailto: link (no backend). The form ships `hidden` and site.js shows it only after the submit
# handler is attached; the mailto: action is a second safety net, so a native submit can never send the fields to this web server.
FORM_OPEN, FORM_CLOSE = (f'<form class="form rv" id="qf" novalidate hidden>', '') if CONTACT["email"] else ('<!-- no email in brand.json: quote form left out', ' -->')
PAGE = f"""<!doctype html>
<html lang="mk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{SITE_URL}/">
<title @="meta.title"></title>
<meta name="description" @a="content:meta.desc">
<meta name="theme-color" content="#0d0d0f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BIG DOGMA">
<meta property="og:title" @a="content:meta.title">
<meta property="og:description" @a="content:meta.desc">
<meta property="og:image" content="{SITE_URL}/media/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:locale" content="mk_MK"><meta property="og:locale:alternate" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="i32.png"><link rel="icon" type="image/png" sizes="64x64" href="i64.png"><link rel="apple-touch-icon" href="icon.png">
<link rel="preload" href="manrope-cyr.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="russo.ttf" as="font" type="font/ttf" crossorigin>
<link rel="preload" href="{u('media/hero.jpg')}" as="image">
<link rel="stylesheet" href="fx.css?v={{V}}">
<link rel="stylesheet" href="site.css?v={{V}}">
<noscript><style>.pre{{display:none}}.rv{{opacity:1;transform:none}}#qf{{display:none}}</style></noscript>
<script>try{{var l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('bd_lang');if(l==='en'){{var d=document.documentElement;d.classList.add('l-en');setTimeout(function(){{d.classList.add('i18n')}},2500)}}}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main" @="skip"></a>
<div class="pre" aria-hidden="true"><canvas></canvas><button type="button" @="pre.skip"></button></div>
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="grain" aria-hidden="true"></div><div class="spot" aria-hidden="true"></div>

<nav class="nav" @a="aria-label:nav.label">
 <div class="wrap">
  <a class="brand" href="#top" @a="aria-label:nav.home"><span class="lfx" aria-hidden="true"><span class="lfx-in"></span></span><b>BIG DOGMA</b></a>
  <div class="links" id="menu">
   <a href="#showreel" @="nav.reel"></a><a href="#films" @="nav.work"></a><a href="#gallery" @="nav.gal"></a><a href="#process" @="nav.how"></a><a href="#pricing" @="nav.price"></a><a href="#faq" @="nav.faq"></a><a href="#contact" @="nav.contact"></a>
   <a class="btn a mcta" href="#contact" @="nav.cta"></a>
  </div>
  <div class="lang" role="group" @a="aria-label:nav.lang"><button type="button" data-lang="mk" aria-pressed="true" lang="mk">MK</button><button type="button" data-lang="en" aria-pressed="false" lang="en">EN</button></div>
  <a class="btn a cta" href="#contact" @="nav.cta"></a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="menu" @a="aria-label:nav.menu"><i></i><i></i><i></i></button>
 </div>
</nav>

<header class="hero" id="top">
 <video autoplay muted loop playsinline preload="auto" poster="{u('media/hero.jpg')}" aria-hidden="true" tabindex="-1"><source src="{u('media/hero.mp4')}" type="video/mp4"></video>
 <canvas class="embers" aria-hidden="true"></canvas>
 <div class="hud" aria-hidden="true"><i class="c c1"></i><i class="c c2"></i><i class="c c3"></i><i class="c c4"></i><div class="scan"></div>
  <div class="tag"><span class="rec"></span><span @="hud.tag"></span></div><div class="tc">TC 00:00:00:00</div>
  <div class="prompt"><div class="lbl"><span @="hud.prompt"></span><span class="st" @a="data-gen:hud.gen;data-done:hud.done">{E(mk('hud.gen'))}</span></div><div class="txt" @a="data-text:hud.text"></div><div class="bar"><i></i></div></div>
 </div>
 <div class="wrap">
  <span class="pill" @="hero.pill"></span>
  <h1 @h="hero.h1"></h1>
  <p class="sub" @="hero.sub"></p>
  <div class="btns"><a class="btn a" href="#showreel" @="hero.cta1"></a><a class="btn b" href="#contact" @="hero.cta2"></a></div>
  <p class="aino"><span class="dot" aria-hidden="true"></span><span @="hero.ai"></span></p>
 </div>
</header>

<main id="main">
<div class="marq" aria-hidden="true"><div class="row">{MARQ}{MARQ}</div></div>

<section class="stats-s">
 <div class="wrap"><div class="stats">
  <div class="stat rv"><div class="v"><span>7–</span><span data-to="10">10</span></div><div class="l" @="st1"></div></div>
  <div class="stat rv"><div class="v" data-to="0">0</div><div class="l" @="st2"></div></div>
  <div class="stat rv"><div class="v" data-to="2">2</div><div class="l" @="st3"></div></div>
  <div class="stat rv"><div class="v" data-to="3">3</div><div class="l" @="st4"></div></div>
 </div></div>
</section>

<section id="showreel" class="reel-s">
 <div class="wrap">
  <div class="eyebrow rv" @="reel.e"></div>
  <h2 class="sh rv" @="reel.h"></h2>
  <p class="sp rv" @="reel.p"></p>
  <article class="film rv">
   <div class="vw"><video controls playsinline preload="none" poster="{u('media/showreel.jpg')}" src="{u('media/showreel.mp4')}" @a="aria-label:reel.vid"></video></div>
   <div class="meta"><h3 @="reel.t"></h3><span class="du">0:56</span>
    <div class="seg" role="group" @a="aria-label:reel.fmt"><button type="button" class="on" data-src="{u('media/showreel.mp4')}" data-poster="{u('media/showreel.jpg')}" @="reel.h169"></button><button type="button" data-v="1" data-src="{u('media/showreel_9x16.mp4')}" data-poster="{u('media/showreel_9x16.jpg')}" @="reel.v916"></button></div>
   </div>
  </article>
  <p class="hint rv" @="reel.note"></p>
 </div>
</section>

<section id="films" class="alt">
 <div class="wrap">
  <div class="eyebrow rv" @="work.e"></div>
  <h2 class="sh rv" @="work.h"></h2>
  <p class="sp rv" @="work.p"></p>
  <div class="chips rv" role="group" @a="aria-label:work.filter">
   <button type="button" class="chip" data-f="all" aria-pressed="true"><span @="f.all"></span> <b>{len(FILMS)}</b></button>
   <button type="button" class="chip" data-f="sec" aria-pressed="false"><span @="f.sec"></span> <b>{n_sec}</b></button>
   <button type="button" class="chip" data-f="tl" aria-pressed="false"><span @="f.tl"></span> <b>{n_tl}</b></button>
  </div>
  <ul class="grid" id="grid">
{FILM_CARDS}
  </ul>
  <p class="hint rv" @="work.note"></p>
 </div>
</section>

<section id="sectors" class="sec-s">
 <div class="wrap">
  <div class="eyebrow rv" @="sec.e"></div>
  <h2 class="sh rv" @="sec.h"></h2>
  <p class="sp rv" @="sec.p"></p>
  <div class="tabs stabs rv" role="tablist" @a="aria-label:sec.tabs">{SEC_TABS}</div>
  <div class="spanels rv">
{SEC_PANELS}
  </div>
  <p class="hint rv" @="ai.note"></p>
 </div>
</section>

<section id="gallery" class="alt gal-s">
 <div class="wrap">
  <div class="eyebrow rv" @="gal.e"></div>
  <h2 class="sh rv" @="gal.h"></h2>
  <p class="sp rv" @="gal.p"></p>
  <div class="chips gchips rv" role="group" @a="aria-label:gal.filter">{GAL_CHIPS}</div>
  <ul class="gw" id="gw">
{GAL}
  </ul>
  <div class="gmore"><button type="button" class="btn b" id="gmore" hidden @="gal.more"></button></div>
  <p class="hint rv" @="ai.note"></p>
 </div>
</section>

<section id="i2v" class="i2v-s">
 <div class="wrap">
  <div class="eyebrow rv" @="i2v.e"></div>
  <h2 class="sh rv" @="i2v.h"></h2>
  <p class="sp rv" @="i2v.p"></p>
  <ul class="pairs">
{I2V_CARDS}
  </ul>
  <p class="hint rv" @="ai.note"></p>
 </div>
</section>

<section id="buildup" class="alt bu-s">
 <div class="wrap">
  <div class="eyebrow rv" @="bu.e"></div>
  <h2 class="sh rv" @="bu.h"></h2>
  <p class="sp rv" @="bu.p"></p>
  <div class="tabs btabs rv" role="tablist" @a="aria-label:bu.tabs">{BU_TABS}</div>
  <div class="bviews rv">
{BU_VIEWS}
  </div>
  <p class="hint rv" @="ai.note"></p>
 </div>
</section>

<section id="process">
 <div class="wrap">
  <div class="eyebrow rv" @="how.e"></div>
  <h2 class="sh rv" @="how.h"></h2>
  <p class="sp rv" @="how.p"></p>
  <ol class="steps">{STEPS}</ol>
  <div class="pm">
   <figure class="rv">
    <div class="box"><video controls playsinline preload="none" poster="{u('media/howto.jpg')}" src="{u('media/howto.mp4')}" @a="aria-label:how.vid"></video></div>
    <figcaption><b @="how.vt"></b><span @="how.vc"></span></figcaption>
   </figure>
   <figure class="rv">
    <div class="cmp" @a="aria-label:cmp.aria" role="group"><video muted loop playsinline preload="none" poster="{u('media/kf_terrace.jpg')}" data-src="{u('media/ai_terrace.mp4')}" aria-hidden="true"></video><img src="{u('media/kf_terrace.jpg')}" @a="alt:cmp.alt" width="1280" height="704" loading="lazy"><div class="hd"></div><span class="t t1" @="cmp.l"></span><span class="t t2" @="cmp.r"></span>
     <input type="range" min="0" max="100" value="50" @a="aria-label:cmp.aria"></div>
    <figcaption><b @="cmp.t"></b><span @="cmp.c"></span></figcaption>
   </figure>
  </div>
 </div>
</section>

<section id="pricing" class="alt">
 <div class="wrap">
  <div class="eyebrow rv" @="price.e"></div>
  <h2 class="sh rv" @="price.h"></h2>
  <p class="sp rv" @="price.p"></p>
  <div class="plans">{plan(1)}{plan(2, True)}{plan(3)}</div>
  <h3 class="bh rv" @="bund.h"></h3>
  <p class="sp rv" @="bund.p"></p>
  <div class="plans bundles">{BUNDLES}</div>
  <p class="terms rv" @="price.terms"></p>
 </div>
</section>

<section id="faq">
 <div class="wrap narrow">
  <div class="eyebrow rv" @="faq.e"></div>
  <h2 class="sh rv" @="faq.h"></h2>
  <div class="faq">{FAQ}</div>
 </div>
</section>

<section id="contact" class="contact alt">
 <div class="wrap">
  <canvas class="logo-live" aria-hidden="true"></canvas>
  <div class="eyebrow rv" @="c.e"></div>
  <h2 class="sh rv" @="c.h"></h2>
  <p class="sp rv" @="c.p"></p>
  <div class="cgrid">
   <!-- contact details come from brand/brand.json (only filled-in fields are shown); edit it there and re-run gen_site.py -->
   <ul class="ways">{WAYS}</ul>
   {FORM_OPEN}
    <h3 @="fm.h"></h3>
    <div class="row2">
     <label><span @="fm.name"></span><input name="name" autocomplete="name" required></label>
     <label><span @="fm.company"></span><input name="company" autocomplete="organization"></label>
    </div>
    <div class="row2">
     <label><span @="fm.email"></span><input name="email" type="email" autocomplete="email" required></label>
     <label><span @="fm.phone"></span><input name="phone" type="tel" autocomplete="tel"></label>
    </div>
    <label><span @="fm.pkg"></span><select name="package"><option value="p0" @="fm.pkg0"></option><option value="p1" @="p1.n"></option><option value="p2" @="p2.n"></option><option value="p3" @="p3.n"></option><option value="b1" @="b1.n"></option><option value="b2" @="b2.n"></option><option value="b3" @="b3.n"></option><option value="b4" @="b4.n"></option><option value="b5" @="b5.n"></option><option value="b6" @="b6.n"></option></select></label>
    <label><span @="fm.msg"></span><textarea name="message" rows="4" required @a="placeholder:fm.msg.ph"></textarea></label>
    <p class="err" role="alert" hidden @="fm.err"></p>
    <button class="btn a" type="submit" @="fm.send"></button>
    <p class="fnote" @="fm.note"></p>
   </form>{FORM_CLOSE}
  </div>
 </div>
</section>
</main>

<footer class="foot">
 <div class="wrap">
  <div class="fg">
   <div><img src="{u('media/logo.png')}" width="1600" height="400" @a="alt:logo.alt" loading="lazy"><p class="ai" @="ft.ai"></p></div>
   <div class="fc2">
    {FOOT_CT}
   </div>
   <div class="fl"><a href="#showreel" @="nav.reel"></a><a href="#films" @="nav.work"></a><a href="#gallery" @="nav.gal"></a><a href="#process" @="nav.how"></a><a href="#pricing" @="nav.price"></a><a href="#faq" @="nav.faq"></a><a href="#contact" @="nav.contact"></a></div>
  </div>
  <div class="fb"><span @="ft.rights"></span><a href="#top" @="ft.top"></a></div>
 </div>
</footer>

<dialog class="lb" id="lb" aria-labelledby="lbT">
 <div class="in">
  <button class="x" type="button" data-close @a="aria-label:lb.close">×</button>
  <div class="lv"><video controls playsinline preload="metadata"></video></div>
  <div class="meta"><div class="mt"><h3 id="lbT"></h3><p></p></div>
   <div class="pn"><button type="button" data-step="-1" @a="aria-label:lb.prev">‹</button><button type="button" data-step="1" @a="aria-label:lb.next">›</button></div></div>
  <p class="ai" @="lb.ai"></p>
 </div>
</dialog>

<script>window.BD_FILMS={FILM_JSON};window.BD_CONTACT={CT_JS};</script>
<script src="i18n.js?v={{V}}"></script>
<script src="dogma_logo.js?v={{V}}"></script><script src="mark.js?v={{V}}"></script><script src="fx.js?v={{V}}"></script><script src="site.js?v={{V}}"></script>
<script src="logo_fx/mark_data.js?v={{V}}"></script><script src="logo_fx/logo_fx.js?v={{V}}"></script><script src="logo_fx/hdr/list.js?v={{V}}"></script><script src="logo_fx/hdr.js?v={{V}}"></script>
<script>window.DOGMA_HERO={HERO_JSON};</script><script src="logo_fx/hero_bg.js?v={{V}}"></script>
</body>
</html>
"""

# ------------------------------------------------------------------ expand @ markers
used = set()
def val(k):
    if k not in TX: raise KeyError(k)
    used.add(k); return TX[k][0]
def expand(page):
    # attributes: @a="attr:key;attr2:key2"  -> attr="mk" ... data-ia="..."
    def fa(m):
        spec = m.group(1); out = []
        for p in spec.split(";"):
            a, k = p.split(":"); out.append(f'{a}="{E(val(k))}"')
        return " ".join(out) + f' data-ia="{spec}"'
    page = re.sub(r'@a="([^"]+)"', fa, page)
    # text / html content: <tag ... @="key" ...></tag>  (empty element in the template)
    def fc(m):
        tag, pre, kind, key, post = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        v = val(key); attr = "data-ih" if kind == "h" else "data-i"
        body = v if kind == "h" else E(v, quote=False)
        return f'<{tag}{pre} {attr}="{key}"{post}>{body}</{tag}>'
    page = re.sub(r'<(\w+)([^<>]*?)\s@(h?)="([^"]+)"([^<>]*)></\1>', fc, page)
    # void/option elements handled above; anything left is a bug
    left = re.findall(r'\s@h?="[^"]+"', page)
    if left: raise SystemExit(f"unexpanded markers: {left[:5]}")
    return page

V = subprocess.run(["date", "+%Y%m%d%H%M"], capture_output=True, text=True).stdout.strip()
page = expand(PAGE.replace("{V}", V))
missing = set(TX) - used
open(f"{OUT}/index.html", "w", encoding="utf-8").write(page)
i18n = {"mk": {k: v[0] for k, v in TX.items()}, "en": {k: v[1] for k, v in TX.items()}}
open(f"{OUT}/i18n.js", "w", encoding="utf-8").write("window.BD_I18N=" + json.dumps(i18n, ensure_ascii=False, separators=(",", ":")) + ";\n")

# fx layer: copy, with three small adaptations (re-read the HUD prompt per run so the language toggle reaches it,
# swap the poster with the showreel format, nav selector)
fx = open(f"{S}/fx/fx.js", encoding="utf-8").read()
a1 = "st = hp.querySelector('.st'), full = txt.dataset.text, lab = st.textContent, ok = st.dataset.done;\n    const run = () => { st.textContent = lab; typeInto(txt, full, RM ? 0 : 28, bar, () => { st.textContent = ok; setTimeout(run, 5200); }); };"
# HUD: re-read the prompt per run and make the loop restartable (window.BD_HUD.restart), so the language switch retypes it at once
b1 = ("st = hp.querySelector('.st'); let tok = 0, tm = 0;\n"
      "    const run = () => { const my = ++tok, text = txt.dataset.text; let i = 0; clearTimeout(tm); st.textContent = st.dataset.gen; txt.classList.add('typing');\n"
      "      const step = () => { if (my !== tok) return; txt.textContent = text.slice(0, i); bar.style.width = (100 * i / text.length) + '%';\n"
      "        if (i++ < text.length) tm = setTimeout(step, RM ? 0 : 28); else { txt.classList.remove('typing'); st.textContent = st.dataset.done; tm = setTimeout(run, 5200); } }; step(); };\n"
      "    window.BD_HUD = { restart: run };")
# preloader: schedule the auto-hide first and never let a missing logo script (dogma_logo.js / mark.js) leave the overlay up
a4 = "let L = null; fontReady.then(() => { L = logo(cv, { lite: innerWidth < 800, transparent: true }); L.play(0); setTimeout(hide, 4700); });"
b4 = "let L = null; fontReady.then(() => { setTimeout(hide, 4700); try { L = logo(cv, { lite: innerWidth < 800, transparent: true }); L.play(0); } catch (e) { hide(); } });"
a5 = "setTimeout(() => { L && L.stop(); pre.remove(); }, 1000); };"; b5 = "setTimeout(() => { try { L && L.stop(); } catch (e) {} pre.remove(); }, 1000); };"
a2 = "v.src = b.dataset.src;"; b2 = "if (b.dataset.poster) v.poster = b.dataset.poster; v.src = b.dataset.src;"
a3 = "const nav = $('nav');"; b3 = "const nav = $('.nav');"
# reveal: .rv is hidden only under html.rvjs, set here once the IntersectionObserver exists, so a failed fx.js leaves everything visible
a6 = "$$('.rv,[data-to],video[data-src],[data-type]').forEach(el => io.observe(el));"; b6 = "document.documentElement.classList.add('rvjs');\n  " + a6
for a, b in ((a1, b1), (a2, b2), (a3, b3), (a4, b4), (a5, b5), (a6, b6)):
    assert fx.count(a) == 1, a[:40]; fx = fx.replace(a, b)
open(f"{OUT}/fx.js", "w", encoding="utf-8").write(fx)
fx = fx.replace("DOGMA pitch-site effects (shared).", "BIG DOGMA web effects.")
open(f"{OUT}/fx.js", "w", encoding="utf-8").write(fx)
css = open(f"{S}/fx/fx.css", encoding="utf-8").read().replace("DOGMA pitch-site effects layer (shared by all 12 pages).", "BIG DOGMA web effects layer.")
open(f"{OUT}/fx.css", "w", encoding="utf-8").write(css)
for f in ("dogma_logo.js", "mark.js"): shutil.copy(f"{S}/fx/{f}", f"{OUT}/{f}")
os.makedirs(f"{OUT}/logo_fx", exist_ok=True)
for f in ("mark_data.js", "logo_fx.js", "skins.js", "hdr.js", "hero_bg.js"): shutil.copy(f"{WORK}/logo_fx/{f}", f"{OUT}/logo_fx/{f}")
shutil.rmtree(f"{OUT}/logo_fx/hdr", ignore_errors=True); shutil.copytree(f"{WORK}/logo_fx/hdr", f"{OUT}/logo_fx/hdr")
shutil.copy(f"{S}/brand/fonts/RussoOne-400.ttf", f"{OUT}/russo.ttf")
for f in ("manrope-cyr.woff2", "manrope-lat.woff2", "manrope-latx.woff2"): shutil.copy(f"{WORK}/fonts/{f}", f"{OUT}/{f}")
for f in ("site.css", "site.js", "robots.txt", "404.html"): shutil.copy(f"{WORK}/{f}", f"{OUT}/{f}")
import datetime
open(f"{OUT}/sitemap.xml", "w").write(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE_URL}/</loc><lastmod>{datetime.date.today()}</lastmod></url></urlset>
''')
pub = page + open(f"{OUT}/i18n.js", encoding="utf-8").read()
bad = ["example.mk", "example.com", "XXX", "googleapis", "gstatic"] + [x for x, f in (("tel:", "phone"), ("WhatsApp", "whatsapp"), ("wa.me", "whatsapp")) if not CONTACT[f]]
leak = [x for x in bad if x.lower() in pub.lower()]
if leak: raise SystemExit(f"placeholder / unused contact text or third-party host in index.html or i18n.js: {leak}")
print("OK", len(page), "bytes;", len(TX), "keys; unused:", sorted(missing))
