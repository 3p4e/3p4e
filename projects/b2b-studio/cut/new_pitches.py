# Pitch pages + emails for the companies that have no classic page (AutoNesi MK 2026-11-27, Drugi tir SI 2026-11-27).
# Reuses pitch_v3.build (same look as the other 13 pages) with a synthetic classic.html that only carries the offer section.
#   python3 new_pitches.py autonesi|drugitir     -> /dev/shm/pub/<token>/ (page, films, posters, email thumbs, offer.pdf) and email in /dev/shm/pub/email_<key>.{html,txt,json}
# Tokens live in the scratchpad (cut/page_tokens_new.json), never in the repo.
import os, sys, json, secrets, subprocess, shutil, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, f"{P}/outreach/email")
import pitch_v3 as PV, bd_email as M
from PIL import Image, ImageDraw
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
PRICES = json.load(open(f"{P}/launch/site_work/prices_by_lang.json", encoding="utf-8"))
OFFER_TXT = {
 "mk": dict(eb="Понуда", pil="Пилот", pild="1 филм 20–30 сек., 16:9 + 9:16, музика, лого, повик за акција", hot="Најчест избор", lan="Лансирање",
            land="Главен филм 45–60 сек. + 3 спота + 10 кратки клипови за мрежи", mon="Месечна содржина", mond="6–8 нови клипови месечно, минимум 3 месеци", mo="месец",
            head="Пакети за вашиот сектор", terms="Рок: 7–10 дена од одобрување на клучните кадри · 2 рунди корекции · права: веб, социјални мрежи, екрани (ТВ и платени кампањи по договор) · секое видео е означено како изработено со AI. Цени во евра без ДДВ.", per="по кампања",
            pk=dict(b5=("Сезонска кампања", "по кампања", "Семеен рекламен филм, филм од производството или продавницата и сезонски спотови за празници и акции."))),
 "sl": dict(eb="Ponudba", pil="Pilot", pild="1 film 20–30 s, 16:9 + 9:16, glasba, logotip, poziv k dejanju", hot="Najpogostejša izbira", lan="Lansiranje",
            land="Glavni film 45–60 s + 3 spoti + 10 kratkih posnetkov za omrežja", mon="Mesečna vsebina", mond="6–8 novih posnetkov na mesec, najmanj 3 mesece", mo="mesec",
            head="Paketi za vaš sektor", terms="Rok: 7–10 dni od potrditve ključnih kadrov · 2 kroga popravkov · pravice: splet, družbena omrežja, zasloni (TV in plačane kampanje po dogovoru) · vsak video je označen kot izdelan z umetno inteligenco. Cene v evrih brez DDV.",
            pk=dict(b4=("Časovni zamik projekta", "po projektu", "Vaš projekt korak za korakom, od začetka do konca, z vašim logotipom: objekti, predori, mostovi, ceste."),
                    b6=("Blagovna znamka delodajalca", "po paketu", "Film za zaposlovanje, film o vaši ekipi in procesu ter kratki posnetki za oglase za delo."))),
}
OFFER_TXT["en"] = dict(eb="Offer", pil="Pilot", pild="1 film 20–30 s, 16:9 + 9:16, music, logo, call to action", hot="Most common", lan="Launch",
            land="Main film 45–60 s + 3 spots + 10 short clips for social", mon="Monthly content", mond="6–8 new clips a month, minimum 3 months", mo="month",
            head="Packages for your sector", terms="Delivery: 7–10 days after key-frame approval · 2 rounds of revisions · rights: web, social media, screens, showrooms and trade fairs (TV and paid campaigns by agreement) · every video is labelled as made with AI. Prices in euros excluding VAT.",
            pk=dict(b4=("Project timelapse", "per project", "Your project step by step, from start to finish, with your logo: product lines, installations, cities."),
                    b5=("Seasonal campaign", "per campaign", "A brand commercial, a factory or product film and short spots for trade fairs and launches.")))
_LED = dict(lang="en", accent="#3da9fc", cats=["it", "product_launch"], tags="#LED #TransparentLED #FlexibleLED #AIcontent", site=None, pk=["b4", "b5"], cc=[], dur={"cn_showreel": 29, "cn_maker": 31}, films=[
     ("led_showreel", "cn_showreel", "Content for transparent and flexible LED", "Facade, window, column, curved wall and 3D corner: original loops built for each shape."),
     ("led_maker", "cn_maker", "Light, made to order", "A commercial about your screens: from the factory floor to the skyline.")],
    greeting="Hello,", cta="Watch the films", role="Founder and creative director", sec="s", voice="English voice-over", closing="Best regards,", vw="video")
def _led(key, name, to):
    return dict(_LED, key=key, name=name, to=[to],
      subject=f"{name}: two short AI films made for your LED screens (concept)",
      paras=[f"We prepared two short films for {name}: a content reel for transparent, flexible and creative LED screens, and a commercial about the screens themselves. Both are made with AI, with no shoot.",
             "Most makers show the same stock loops at fairs and in showrooms. We make original content for each screen shape (film on glass, curved walls, columns, 3D corners), so your demo is not the one everybody else is playing. We also make commercials for the brand itself.",
             "Nothing here is published and nothing will be without your written approval. If you like the direction, we would be glad to show you in 15 minutes what the same work looks like on your own screens and products. A pilot film starts from €900."],
      note=f"A private page only for {name}: the films, a publishing plan and the offer as a PDF.",
      optout=f"This message was sent only to {name}. If you do not want more messages from us, reply with “no, thank you” and we will not write again.")
CO = {
 "autonesi": dict(key="autonesi", name="AutoNesi", lang="mk", accent="#e0b04a", cats=["automotive", "product_launch"], tags="#AutoNesi #Скопје #Македонија #половниАвтомобили", site="autonesi.mk", pk=["b5"],
    to=["info@autonesi.mk"], cc=[], dur={"an_evoque": 19, "an_jaguar": 19, "an_discovery": 19}, films=[
     ("autonesi_evoque", "an_evoque", "Range Rover Evoque: добрите возила имаат адреса", "Проверен Evoque, директно од Европа."),
     ("autonesi_jaguar", "an_jaguar", "Jaguar E-Pace: тивка моќ", "Градот ноќе, секој детал проверен."),
     ("autonesi_discovery", "an_discovery", "Discovery Sport: секое време, секој пат", "Снег, магла, есен: проверено возило од Европа.")],
    subject="AutoNesi: три кратки AI филма за вашите возила (концепт)", greeting="Почитувани,",
    paras=["Подготвивме три кратки рекламни филма за AutoNesi, направени со вештачка интелигенција од вашите вистински возила, без снимање: Range Rover Evoque, Jaguar E-Pace и Land Rover Discovery Sport.",
           "Од секое возило од вашата понуда можеме да направиме нов филм за неколку дена, во 16:9 за екрани и YouTube и во вистинска 9:16 верзија за Reels, TikTok и Stories, со глас на македонски и музика.",
           "Ништо од ова не е објавено и нема да биде без ваше писмено одобрение. Ако ви се допаѓа насоката, би сакале за 15 минути да ви покажеме како изгледа истото со вашите нови возила и акции. Пилот-филм чини од €600."],
    cta="Погледнете ги филмовите", note="Приватна страница само за AutoNesi: филмовите, предлог-распоред за објава и понуда во PDF.", role="Основач и креативен директор", sec="сек.", voice="глас на македонски",
    optout="Оваа порака е испратена само до AutoNesi. Ако не сакате повеќе пораки од нас, одговорете со „не, благодарам“ и нема повторно да ви пишеме.", closing="Со почит,", vw="видео"),
 "drugitir": dict(key="drugitir", name="Drugi tir (2TDK)", lang="sl", accent="#2f8fe0", cats=["construction", "steel_cement"], tags="#DrugiTir #2TDK #Slovenija #Koper #Divača", site=None, pk=["b4", "b6"],
    to=["info@2-tdk.si"], cc=["drugitir@2-tdk.si"], dur={"dt_povezava": 39, "dt_gradnja": 31}, films=[
     ("drugitir_povezava", "dt_povezava", "Povezava do morja", "Med Divačo in Koprom raste nova železnica."),
     ("drugitir_gradnja", "dt_gradnja", "Korak za korakom", "Skozi kras, od predora do prvega vlaka.")],
    subject="Drugi tir: dva kratka AI-filma, narejena samo za vas (koncept)", greeting="Spoštovani,",
    paras=["Pripravili smo dva kratka filma o projektu Drugi tir Divača–Koper: koncept samo za vas, narejen z umetno inteligenco in navdihnjen z uradnimi fotografijami projekta, brez snemanja.",
           "Prvi prikazuje povezavo od krasa do morja, drugi gradnjo predorov in viaduktov, vse do prvega vlaka. Filma imata slovenski glas in glasbo, na voljo sta v 16:9 za splet in zaslone ter v pokončni različici 9:16 za družbena omrežja.",
           "Nič od tega ni objavljeno in ne bo brez vašega pisnega soglasja. Gre za neodvisen koncept in ni naročen; ni uradni material projekta. Če vam je smer všeč, vam radi v 15 minutah pokažemo, kako bi izgledal film z vašimi dejanskimi posnetki gradnje. Pilotni film stane od €900."],
    cta="Oglejte si filme", note="Zasebna stran samo za Drugi tir: filmi, predlog razporeda objav in ponudba v PDF-ju.", role="Ustanovitelj in kreativni direktor", sec="s", voice="slovenski glas",
    optout="To sporočilo je bilo poslano samo Drugemu tiru (2TDK). Če ne želite več sporočil od nas, odgovorite z »ne, hvala« in vam ne bomo več pisali.", closing="Lep pozdrav,", vw="video"),
}

CO.update({k: _led(k, n, t) for k, n, t in (("nexnovo", "Nexnovo", "sale@nexnovo.com"), ("muxwave", "Muxwave", "info@muxwave.com"), ("sostron", "SoStron", "info@sostron.com"), ("gloshine", "Gloshine", "international@gloshine.cn"), ("yestech", "YES TECH", "yestech@yes-led.com"), ("aoto", "AOTO", "led@aoto.com"), ("ledman", "Ledman", "marketing@ledman.com"), ("qiangli", "Qiangli Jucai", "sales@qiangliled.com"), ("esdlumen", "ESDlumen", "sale@esdled.com"))})

def offer_section(c):
    t = OFFER_TXT[c["lang"]]; pr = PRICES[c["lang"]]; mo = t["mo"]
    cards = lambda ids: "".join(f'<div class="card rv"><h3>{H.escape(t["pk"][i][0])}</h3><div class="amt">{pr[i + ".a"]}</div><span class="u">{H.escape(t["pk"][i][1])}</span><p>{H.escape(t["pk"][i][2])}</p></div>' for i in ids)
    return (f'<section id="offer"><div class="wrap"><div class="eyebrow rv">{t["eb"]}</div><h2 class="sh rv">{t["eb"]}</h2>\n<div class="price"><div class="card rv"><h3>{t["pil"]}</h3><div class="amt">{pr["p1.a"]}</div><p>{t["pild"]}</p></div>\n'
            f'<div class="card hot rv"><span class="tag">{t["hot"]}</span><h3>{t["lan"]}</h3><div class="amt">{pr["p2.a"]}</div><p>{t["land"]}</p></div>\n'
            f'<div class="card rv"><h3>{t["mon"]}</h3><div class="amt">{pr["p3.a"]} / {mo}</div><p>{t["mond"]}</p></div></div>\n'
            f'<h3 class="bh rv">{t["head"]}</h3><div class="price bund">{cards(c["pk"])}</div>\n<p class="terms rv">{t["terms"]}</p></div></section>')

def thumb(src, dst):
    im = Image.open(src).convert("RGB"); w, h = im.size; r = min(w, h) * 0.12; cx, cy = w / 2, h / 2
    d = ImageDraw.Draw(im, "RGBA"); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(242, 193, 78, 235))
    d.polygon([(cx - r * 0.3, cy - r * 0.5), (cx - r * 0.3, cy + r * 0.5), (cx + r * 0.55, cy)], fill=(17, 17, 17, 255)); im.save(dst, quality=88)

def main(key):
    c = CO[key]; FIN = {"autonesi": "/dev/shm/vall/an/final", "drugitir": "/dev/shm/vall/dt/final"}.get(key, "/dev/shm/vall/cn/final")
    tokf = f"{S}/cut/page_tokens_new.json"; T = json.load(open(tokf)) if os.path.exists(tokf) else {}
    tok = T.setdefault(key, secrets.token_urlsafe(12)); json.dump(T, open(tokf, "w"))
    pub = f"/dev/shm/pub/{tok}"; shutil.rmtree(pub, ignore_errors=True); os.makedirs(f"{pub}/email")
    films = []
    for fid, src, title, line in c["films"]:
        for ar, suf in (("16x9", ""), ("9x16", "_9x16")):
            if not os.path.exists(f"{FIN}/{src}_{ar}.mp4"): continue
            shutil.copy(f"{FIN}/{src}_{ar}.mp4", f"{pub}/{fid}{suf}.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", f"{pub}/{fid}{suf}.mp4", "-frames:v", "1", "-vf", "scale=" + ("1280:-2" if not suf else "-2:1280"), f"{pub}/{fid}{suf}.jpg"], check=True)
        thumb(f"{pub}/{fid}.jpg", f"{pub}/email/{fid}.jpg")
        hv = os.path.exists(f"{pub}/{fid}_9x16.mp4")
        films.append(dict(id=fid, t=title, l=line, src=f"{fid}.mp4", poster=f"{fid}.jpg", **(dict(v=f"{fid}_9x16.mp4", vposter=f"{fid}_9x16.jpg") if hv else {})))
        if hv: PV.NATIVE_V[fid] = (f"{fid}_9x16.mp4", f"{fid}_9x16.jpg")
    PV.COMPANIES[key] = lambda: dict(key=key, name=c["name"], lang=c["lang"], accent=c["accent"], films=[dict(f) for f in films], caps={}, shots=0, stills=0, gifs=0, industry=c["cats"], tags=c["tags"], cta_site=c["site"])
    PV.SCRP = f"{S}/pv3"; os.makedirs(f"{PV.SCRP}/{key}", exist_ok=True)
    open(f"{PV.SCRP}/{key}/classic.html", "w", encoding="utf-8").write(f'<html lang="{c["lang"]}"><body>{offer_section(c)}</body></html>')
    PV.build(key, pub)
    # email
    page = f"https://pitch.bigdogma.tech/{tok}/"
    x = dict(en=dict(pre="Two short AI films made only for {n}, with no shoot. Private page, 2 minutes."), mk=dict(pre="Три кратки AI филма направени само за {n}, без снимање. Приватна страница, 2 минути."), sl=dict(pre="Dva kratka AI-filma, narejena samo za {n}, brez snemanja. Zasebna stran, 2 minuti."))[c["lang"]]
    src_of = {fid: src for fid, src, _, _ in c["films"]}
    items = [dict(title=f["t"], meta=f'{c["dur"][src_of[f["id"]]]} {c["sec"]} · {c["voice"]}', img=f"{page}email/{f['id']}.jpg", href=page + "#films") for f in films]
    content = dict(lang=c["lang"], subject=c["subject"], preheader=x["pre"].format(n=c["name"]), greeting=c["greeting"], paras=c["paras"], films=items, cta=dict(label=c["cta"], href=page), note=c["note"],
                   sign=dict(name="Blagoj N.", role=c["role"]), closing=c["closing"], optout=c["optout"], video_word=c["vw"])
    h, t = M.render(content)
    for ext, body in (("html", h), ("txt", t)): open(f"/dev/shm/pub/email_{key}.{ext}", "w", encoding="utf-8").write(body)
    json.dump({"subject": c["subject"], "lang": c["lang"], "name": c["name"], "films": [f["t"] for f in films]}, open(f"/dev/shm/pub/email_{key}.json", "w"), ensure_ascii=False)
    print("built", key, tok[:4] + "…", len(films), "films")

if __name__ == "__main__":
    main(sys.argv[1])
