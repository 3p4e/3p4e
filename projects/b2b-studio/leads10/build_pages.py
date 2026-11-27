# Pages and emails for the ten non-EU Europe leads (cfg in the scratchpad: leads10/cfg.json). Reuses cut/new_pitches.py.
#   PITCH_FIN=/dev/shm/vall/ld/final python3 build_pages.py [key ...]
import os, sys, json
sys.path.insert(0, "/home/user/3p4e/projects/b2b-studio/cut"); import new_pitches as N, subprocess
S = N.S; CFG = json.load(open(f"{S}/leads10/cfg.json", encoding="utf-8")); OFF = json.load(open("/home/user/3p4e/projects/b2b-studio/cut/offers.json", encoding="utf-8")); BU = json.load(open("/home/user/3p4e/projects/b2b-studio/cut/bundles.json", encoding="utf-8"))
HOT = {"mk": "Најчест избор", "sr": "Najčešći izbor", "sq": "Zgjedhja më e shpeshtë"}; MO = {"mk": "месец", "sr": "mesec", "sq": "muaj"}
for l in ("mk", "sr", "sq"):
    t = OFF["text"][l]; b = BU[l]
    N.OFFER_TXT[l] = dict(eb=t["offer"], pil=t["pilot"], pild=t["pilot_d"], hot=HOT[l], lan=t["launch"], land=t["launch_d"], mon=t["monthly"], mond=t["monthly_d"], mo=MO[l], head=b["head"],
                          terms=t["terms"] + " " + t["price_note"], pk={k: (b[k]["n"], b[k]["u"], b[k]["d"]) for k in ("b1", "b2", "b4", "b5", "b6")})
N.OFFER_TXT["en"]["pk"].update(b1=("Developer", "per project", "A construction timelapse from groundbreaking to keys and a sales film for apartments before they are built, in formats for ads, social and the sales office."),
                              b2=("Apartment staging", "per apartment", "From empty to fully furnished, made from the photos of your apartments. A bundle of 5 apartments: €1,200."), b6=("Employer brand", "per package", "A recruitment film, a film about your team and short clips for job ads."))
PK = {"re": ["b1", "b2", "b4"], "retail": ["b5"], "fuel": ["b5", "b6"], "food": ["b5", "b6"]}
TX = {  # per language: subject, greeting, p1, p2, p3, cta, note, role, voice, closing, optout
 "mk": dict(subject="{n}: два кратки AI филма, направени само за вас (концепт)", greeting="Почитувани,", p1="Подготвивме два кратки рекламни филма за {n}: концепт само за вас, изработен со вештачка интелигенција за неколку дена, без снимање.",
            p2="Од вашите вистински фотографии, производи и простори можеме да направиме нови филмови за неколку дена, хоризонтално за екрани и YouTube и вертикално за Reels, TikTok и Stories, со глас на македонски и музика.",
            p3="Ништо од ова не е објавено и нема да биде без ваше писмено одобрение. Ако ви се допаѓа насоката, би сакале за 15 минути да ви покажеме како изгледа истото со ваши вистински материјали. Пилот-филм чини од €600.",
            cta="Погледнете ги филмовите", note="Приватна страница само за {n}: филмовите, предлог-распоред за објава и понуда во PDF.", role="Основач и креативен директор", voice="глас на македонски", closing="Со почит,", sec="сек.", vw="видео",
            optout="Оваа порака е испратена само до {n}. Ако не сакате повеќе пораки од нас, одговорете со „не, благодарам“ и нема повторно да ви пишеме.", pre="Два кратки AI филма направени само за {n}, без снимање. Приватна страница, 2 минути."),
 "sr": dict(subject="{n}: dva kratka AI filma napravljena samo za vas (koncept)", greeting="Poštovani,", p1="Pripremili smo dva kratka reklamna filma za {n}: koncept samo za vas, napravljen uz pomoć veštačke inteligencije za nekoliko dana, bez snimanja.",
            p2="Od vaših pravih fotografija, proizvoda i prostora možemo za nekoliko dana da napravimo nove filmove, horizontalno za ekrane i YouTube i vertikalno za Reels, TikTok i Stories, sa glasom na srpskom i muzikom.",
            p3="Ništa od ovoga nije objavljeno i neće biti bez vašeg pisanog odobrenja. Ako vam se dopada pravac, rado bismo vam za 15 minuta pokazali kako to izgleda sa vašim pravim materijalima. Pilot-film košta od €700.",
            cta="Pogledajte filmove", note="Privatna stranica samo za {n}: filmovi, predlog rasporeda objava i ponuda u PDF-u.", role="Osnivač i kreativni direktor", voice="glas na srpskom", closing="Srdačan pozdrav,", sec="sek.", vw="video",
            optout="Ova poruka je poslata samo kompaniji {n}. Ako ne želite više poruka od nas, odgovorite sa „ne, hvala“ i nećemo vam ponovo pisati.", pre="Dva kratka AI filma napravljena samo za {n}, bez snimanja. Privatna stranica, 2 minuta."),
 "sq": dict(subject="{n}: dy filma të shkurtër AI, të krijuar vetëm për ju (koncept)", greeting="Të nderuar,", p1="Kemi përgatitur dy filma të shkurtër reklamues për {n}: një koncept vetëm për ju, i krijuar me inteligjencë artificiale për pak ditë, pa xhirime.",
            p2="Nga fotot, produktet dhe hapësirat tuaja të vërteta mund të bëjmë filma të rinj për pak ditë, horizontalisht për ekrane dhe YouTube dhe vertikalisht për Reels, TikTok dhe Stories, me zë në shqip dhe muzikë.",
            p3="Asgjë nga kjo nuk është publikuar dhe nuk do të publikohet pa miratimin tuaj me shkrim. Nëse ju pëlqen drejtimi, do të na vinte mirë t'ju tregonim për 15 minuta si duket e njëjta gjë me materialet tuaja të vërteta. Një film pilot kushton nga €600.",
            cta="Shikoni filmat", note="Faqe private vetëm për {n}: filmat, një propozim për kalendarin e publikimeve dhe oferta në PDF.", role="Themelues dhe drejtor kreativ", voice="zë në shqip", closing="Me respekt,", sec="sek.", vw="video",
            optout="Ky mesazh u dërgua vetëm për {n}. Nëse nuk dëshironi më mesazhe nga ne, përgjigjuni me „jo, faleminderit“ dhe nuk do t'ju shkruajmë më.", pre="Dy filma të shkurtër AI, të krijuar vetëm për {n}, pa xhirime. Faqe private, 2 minuta."),
 "en": dict(subject="{n}: two short AI films made only for you (concept)", greeting="Hello,", p1="We prepared two short commercial films for {n}: a concept made only for you, built with AI in a few days, with no shoot.",
            p2="From your real photos, products and spaces we can make new films in days, landscape for screens and YouTube and vertical for Reels, TikTok and Stories, with an English voice-over and music.",
            p3="Nothing here is published and nothing will be without your written approval. If you like the direction, we would be glad to show you in 15 minutes what the same looks like with your real material. A pilot film starts from €900.",
            cta="Watch the films", note="A private page only for {n}: the films, a publishing plan and the offer as a PDF.", role="Founder and creative director", voice="English voice-over", closing="Best regards,", sec="s", vw="video",
            optout="This message was sent only to {n}. If you do not want more messages from us, reply with “no, thank you” and we will not write again.", pre="Two short AI films made only for {n}, with no shoot. Private page, 2 minutes."),
}
FIN = os.environ.get("PITCH_FIN", "/dev/shm/vall/ld/final")
def dur(f): return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout))
keys = sys.argv[1:] or [c["key"] for c in CFG["companies"]]
for c in CFG["companies"]:
    if c["key"] not in keys: continue
    t = TX[c["lang"]]; n = c["name"]; k = c["key"]
    N.CO[k] = dict(key=k, name=n, lang=c["lang"], accent=c["accent"], cats=c["cats"], tags=c["tags"], site=None, pk=PK[c["sector"]], to=[c["to"]], cc=[],
        dur={f"l_{k}_{x}": dur(f"{FIN}/l_{k}_{x}_16x9.mp4") for x in "ab"},
        films=[(f"{k}_film_{x}", f"l_{k}_{x}", c["titles"][i], c["titles"][i + 1]) for x, i in (("a", 0), ("b", 2))],
        subject=t["subject"].format(n=n), greeting=t["greeting"], paras=[t["p1"].format(n=n), t["p2"], t["p3"]], cta=t["cta"], note=t["note"].format(n=n), role=t["role"], sec=t["sec"], voice=t["voice"],
        optout=t["optout"].format(n=n), closing=t["closing"], vw=t["vw"], pre=t["pre"])
    N.main(k)
