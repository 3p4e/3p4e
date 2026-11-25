# Sector-themed private pitch site per company (LTX films only). Static output for an nginx container behind Traefik.
# Each company lives under an unguessable path; the root returns 404; every response is noindex.
import os, json, shutil, secrets, html, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
O = json.load(open(f"{S}/cut/offers.json")); B = json.load(open(f"{S}/brand/brand.json"))
ROOT = f"{S}/pitch_site/site"; shutil.rmtree(f"{S}/pitch_site", ignore_errors=True); os.makedirs(ROOT)
tokfile = f"{S}/cut/page_tokens.json"; tokens = json.load(open(tokfile)) if os.path.exists(tokfile) else {}
E = html.escape

THEMES = {  # bg, surface, fg, muted, accent, ink-on-accent, head font, body font, radius, google family query, mode
 "realestate":   dict(bg="#0c111b", sf="#141b28", fg="#f3efe7", mu="#a9a59c", ac="#c9a96e", ink="#14110b", hf="'Cormorant Garamond',serif", bf="'Inter',sans-serif", r="2px",  gf="Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600", hw="600", ls="0.01em", tt="none"),
 "construction": dict(bg="#17191c", sf="#202328", fg="#eef0f2", mu="#9aa1a9", ac="#ffc400", ink="#17191c", hf="'Oswald',sans-serif",         bf="'Inter',sans-serif", r="0px",  gf="Oswald:wght@500;600;700&family=Inter:wght@400;500;600",           hw="600", ls="0.02em", tt="uppercase"),
 "pharma":       dict(bg="#f5f8fb", sf="#ffffff", fg="#0f2233", mu="#5b6b7a", ac="#0a6ebd", ink="#ffffff", hf="'Manrope',sans-serif",       bf="'Manrope',sans-serif", r="18px", gf="Manrope:wght@400;500;600;700;800",                             hw="800", ls="-0.02em", tt="none"),
 "retail":       dict(bg="#fbf6ec", sf="#ffffff", fg="#1f2a1f", mu="#61695f", ac="#138a3e", ink="#ffffff", hf="'Lora',serif",               bf="'Rubik',sans-serif", r="22px", gf="Lora:wght@600;700&family=Rubik:wght@400;500;600",              hw="700", ls="-0.01em", tt="none"),
 "fmcg":         dict(bg="#fbf3e8", sf="#ffffff", fg="#3b1f14", mu="#7a5a4c", ac="#c8102e", ink="#ffffff", hf="'Playfair Display',serif",   bf="'Montserrat',sans-serif", r="20px", gf="Playfair+Display:wght@700;800&family=Montserrat:wght@400;500;600", hw="800", ls="-0.01em", tt="none"),
 "automotive":   dict(bg="#0a0a0c", sf="#141418", fg="#f2f2f4", mu="#9a9aa3", ac="#d71920", ink="#ffffff", hf="'Exo 2',sans-serif",         bf="'Inter',sans-serif", r="4px",  gf="Exo+2:ital,wght@0,700;0,800;1,800&family=Inter:wght@400;500;600", hw="800", ls="0", tt="uppercase"),
 "logistics":    dict(bg="#071b36", sf="#0d2547", fg="#eef4fb", mu="#9fb3cc", ac="#ff7a00", ink="#ffffff", hf="'Unbounded',sans-serif",     bf="'Inter',sans-serif", r="12px", gf="Unbounded:wght@600;700&family=Inter:wght@400;500;600",          hw="700", ls="-0.01em", tt="none"),
 "bpo":          dict(bg="#1a0833", sf="#26104a", fg="#f6f1ff", mu="#b9a8d6", ac="#00e5c0", ink="#10061f", hf="'Unbounded',sans-serif",     bf="'Manrope',sans-serif", r="16px", gf="Unbounded:wght@600;700&family=Manrope:wght@400;500;600",       hw="700", ls="-0.01em", tt="none"),
}
CO = {  # company id -> sector, accent override, explainer
 "01_zito_marketi_MK": ("retail", "#138a3e", "howto_retail"), "02_alkaloid_MK": ("pharma", "#0a5fae", "howto_pharma"),
 "03_replek_MK": ("pharma", "#00897b", "howto_pharma"), "04_vincinni_MK": ("fmcg", "#c8102e", "howto_fmcg"),
 "05_foton_MK": ("automotive", "#d71920", "howto_automotive"), "06_beograd_na_vodi_RS": ("realestate", None, "howto_06_beograd_na_vodi_RS"),
 "07_millennium_team_RS": ("construction", None, "howto_07_millennium_team_RS"), "08_nelt_RS": ("logistics", None, "howto_08_nelt_RS"),
 "09_gener2_AL": ("realestate", None, "howto_09_gener2_AL"), "10_concord_AL": ("realestate", None, "howto_10_concord_AL"),
 "11_viva_fresh_XK": ("retail", "#d6312b", "howto_11_viva_fresh_XK"), "12_speeex_XK": ("bpo", None, "howto_12_speeex_XK")}
UI = {
 "mk": dict(films="Филмови", how="Како работиме", offer="Понуда", pill="Концепт · не е за објава", watch="Погледнете ги филмовите",
            cta="Закажи 15 минути", mail="Пиши е-пошта", pdf="Понуда (PDF)", h="16:9", v="9:16 мобилен", films_h="Два филма за {c}",
            films_p="Секој филм постои хоризонтално (YouTube, екрани) и вертикално (Reels, TikTok, Stories). Изберете формат.",
            why="Што добивате", popular="Најчест избор", expl="Од фотографија до реклама", expl_p="Вака изгледа процесот на еден ваш производ, чекор по чекор.",
            final="Да ја направиме вистинската верзија?", final_p="15 минути, во живо или онлајн. Ви покажуваме како изгледа со ваши фотографии и производи.",
            note="Концепт само за презентација. Не е објавен и нема да биде објавен без ваше изречно писмено одобрение. Видеата се изработени со вештачка интелигенција (LTX-Video). Логата и марките им припаѓаат на нивните сопственици."),
 "sr": dict(films="Filmovi", how="Kako radimo", offer="Ponuda", pill="Koncept · nije za objavu", watch="Pogledajte filmove",
            cta="Zakaži 15 minuta", mail="Pošalji e-poštu", pdf="Ponuda (PDF)", h="16:9", v="9:16 mobilni", films_h="Dva filma za {c}",
            films_p="Svaki film postoji horizontalno (YouTube, ekrani) i vertikalno (Reels, TikTok, Stories). Izaberite format.",
            why="Šta dobijate", popular="Najčešći izbor", expl="Od fotografije do reklame", expl_p="Ovako izgleda proces za vaš projekat, korak po korak.",
            final="Da napravimo pravu verziju?", final_p="15 minuta, uživo ili onlajn. Pokazaćemo kako izgleda sa vašim fotografijama i proizvodima.",
            note="Koncept samo za prezentaciju. Nije objavljen i neće biti objavljen bez vašeg izričitog pisanog odobrenja. Video snimci su napravljeni uz pomoć veštačke inteligencije (LTX-Video). Logotipi i robne marke pripadaju njihovim vlasnicima."),
 "sq": dict(films="Filmat", how="Si punojmë", offer="Oferta", pill="Koncept · jo për publikim", watch="Shikoni filmat",
            cta="Cakto 15 minuta", mail="Dërgo email", pdf="Oferta (PDF)", h="16:9", v="9:16 celular", films_h="Dy filma për {c}",
            films_p="Çdo film ekziston horizontal (YouTube, ekrane) dhe vertikal (Reels, TikTok, Stories). Zgjidhni formatin.",
            why="Çfarë fitoni", popular="Zgjedhja më e shpeshtë", expl="Nga fotografia te reklama", expl_p="Kështu duket procesi për projektin tuaj, hap pas hapi.",
            final="Ta bëjmë versionin e vërtetë?", final_p="15 minuta, ballë për ballë ose online. Ju tregojmë si duket me fotot dhe produktet tuaja.",
            note="Koncept vetëm për prezantim. Nuk është publikuar dhe nuk do të publikohet pa miratimin tuaj të shprehur me shkrim. Videot janë krijuar me inteligjencë artificiale (LTX-Video). Logot dhe markat u përkasin pronarëve të tyre.")}
SEC = {  # (sector, lang) -> hero hook, 3 benefits
 ("retail","mk"): ("Свежина, луѓе и акции во 30 секунди, за екраните во продавница и за мрежите.",
   [("Акции секоја недела","Нов клип за секоја акција или нова продавница, без снимање."),("Екрани во продавница","Вертикални и хоризонтални верзии за каса, излог и мрежи."),("Локален глас","Македонски глас, позната атмосфера, ваш завршен кадар.")]),
 ("retail","sq"): ("Freski, njerëz dhe oferta në 30 sekonda, për ekranet në dyqan dhe rrjetet sociale.",
   [("Oferta çdo javë","Klip i ri për çdo ofertë apo dyqan të ri, pa xhirime."),("Ekrane në dyqan","Versione vertikale dhe horizontale për arkë, vitrinë dhe rrjete."),("Zë vendor","Zë në shqip, atmosferë e njohur, kuadri juaj përmbyllës.")]),
 ("pharma","mk"): ("Науката, прецизноста и луѓето зад вашите производи, раскажани со мерка.",
   [("Јасно и одговорно","Производство, контрола и луѓе, без претерани ветувања."),("Кариера и извоз","Една содржина за кампањи за вработување, саеми и партнери."),("Лесно одобрување","Клучни кадри пред анимација, удобно за правен и регулаторен преглед.")]),
 ("fmcg","mk"): ("Вашиот производ и вашето пакување, во сцени што будат апетит.",
   [("Производот е ѕвездата","Вистинското пакување, не генеричко, во секој кадар."),("Сезонски кампањи","Празници, училиште, лето: нови верзии без ново снимање."),("Од рафт до Reels","Формати за ТВ, мрежи и екрани во маркети.")]),
 ("automotive","mk"): ("Вашите модели во студио, на терен и во ноќ, без логистика и без снимање.",
   [("Секој модел, секоја боја","Возилото во студио, на терен и ноќе, без транспорт и дозволи."),("Спецификации што се гледаат","4×4, товар и опрема прикажани визуелно, не само во табела."),("Салон и мрежи","Екрани во салонот, Reels и кампањи за тест-возење.")]),
 ("realestate","sr"): ("Prodajte pogled, svetlo i život u stanu pre nego što zgrada bude gotova.",
   [("Prodaja pre izgradnje","Kupci vide život u stanu pre nego što zgrada postoji."),("Od rendera do filma","Vaši arhitektonski renderi postaju kretanje, svetlo i atmosfera."),("Za svaku fazu","Lansiranje, napredak gradnje, predaja ključeva.")]),
 ("realestate","sq"): ("Shisni pamjen, dritën dhe jetën në apartament para se ndërtesa të përfundojë.",
   [("Shitje para ndërtimit","Blerësit shohin jetën në apartament para se ndërtesa të ekzistojë."),("Nga render-i në film","Render-at tuaj arkitektonikë bëhen lëvizje, dritë dhe atmosferë."),("Për çdo fazë","Lansimi, përparimi i ndërtimit, dorëzimi i çelësave.")]),
 ("construction","sr"): ("Kapacitet, mehanizacija i timovi, prikazani u filmu za tendere i partnere.",
   [("Pokažite kapacitet","Mehanizacija, timovi i složeni projekti u jednom filmu za tendere."),("Timelapse bez kamere","Faze gradnje prikazane od iskopa do predaje."),("Zapošljavanje","Film koji privlači inženjere i majstore.")]),
 ("logistics","sr"): ("Od skladišta do police: vaša mreža u jednom kratkom filmu.",
   [("Pokažite mrežu","Skladišta, rute i isporuke u jednoj priči."),("Za principale","Prezentacija za brendove koje distribuirate."),("Zapošljavanje","Vozači, magacioneri i tim koji drži ritam.")]),
 ("bpo","sq"): ("Kultura juaj, ekipi juaj dhe karriera që rritet, në video të shkurtra.",
   [("Rekrutim që tërheq","Filma të shkurtër që tregojnë jetën e vërtetë në zyrë."),("Për klientët ndërkombëtarë","Prezantim i kapaciteteve dhe gjuhëve për partnerët."),("Përmbajtje çdo muaj","Klipe të reja për rrjete pa ndalur punën.")]),
}
def css(t):
    return f"""@import url('https://fonts.googleapis.com/css2?family={t['gf']}&display=swap');
:root{{--bg:{t['bg']};--sf:{t['sf']};--fg:{t['fg']};--mu:{t['mu']};--ac:{t['ac']};--ink:{t['ink']};--r:{t['r']};--hf:{t['hf']};--bf:{t['bf']}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--bf);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}img,video{{display:block;max-width:100%}}
.wrap{{max-width:1160px;margin:0 auto;padding:0 20px}}
h1,h2,h3{{font-family:var(--hf);font-weight:{t['hw']};letter-spacing:{t['ls']};text-transform:{t['tt']};line-height:1.08;margin:0}}
nav{{position:fixed;top:0;left:0;right:0;z-index:20;transition:background .3s,backdrop-filter .3s}}
nav.s{{background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px);box-shadow:0 1px 0 color-mix(in srgb,var(--fg) 10%,transparent)}}
nav .wrap{{display:flex;align-items:center;gap:22px;height:68px}} nav img{{height:34px;width:auto}}
nav .links{{margin-left:auto;display:flex;gap:22px;font-size:15px}} nav .links a{{text-decoration:none;opacity:.85}} nav .links a:hover{{opacity:1;color:var(--ac)}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;border-radius:var(--r);font-weight:600;text-decoration:none;border:1.5px solid transparent;transition:transform .2s,box-shadow .2s;cursor:pointer;font-size:16px}}
.btn:hover{{transform:translateY(-2px)}} .btn.a{{background:var(--ac);color:var(--ink);box-shadow:0 10px 30px -10px var(--ac)}} .btn.b{{border-color:currentColor}}
nav .btn{{padding:9px 16px;font-size:14px}}
.hero{{position:relative;min-height:100svh;display:flex;align-items:flex-end;overflow:hidden;color:#fff}}
.hero video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none}}
.hero:after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,.05) 35%,rgba(0,0,0,.78) 100%)}}
.hero .wrap{{position:relative;z-index:2;padding-bottom:9vh;width:100%}}
.pill{{display:inline-block;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;padding:7px 12px;border:1px solid rgba(255,255,255,.45);border-radius:999px;margin-bottom:22px;backdrop-filter:blur(6px);background:rgba(0,0,0,.25)}}
.hero h1{{font-size:clamp(40px,7.4vw,96px);max-width:14ch;text-shadow:0 2px 24px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5)}} .hero h1 em{{font-style:normal;color:#fff;text-decoration:underline;text-decoration-color:var(--ac);text-decoration-thickness:.09em;text-underline-offset:.14em;text-decoration-skip-ink:none}}
.hero p{{font-size:clamp(17px,2vw,21px);max-width:44ch;margin:22px 0 30px;opacity:.92}} .hero .btns{{display:flex;gap:12px;flex-wrap:wrap}} .hero .btn.b{{color:#fff}}
section{{padding:clamp(64px,10vw,120px) 0}} .eyebrow{{color:var(--ac);font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}}
.sh{{font-size:clamp(32px,4.6vw,56px);max-width:18ch}} .sp{{color:var(--mu);max-width:56ch;margin:16px 0 0}}
.films{{display:grid;gap:28px;margin-top:44px}} @media(min-width:900px){{.films{{grid-template-columns:1fr 1fr}}}}
.film{{background:var(--sf);border-radius:calc(var(--r) + 4px);overflow:hidden;box-shadow:0 30px 60px -35px rgba(0,0,0,.45);border:1px solid color-mix(in srgb,var(--fg) 8%,transparent)}}
.film .vw{{background:#000;display:flex;justify-content:center}} .film video{{width:100%;aspect-ratio:16/9;background:#000}} .film.v video{{aspect-ratio:9/16;width:auto;height:min(70vh,640px)}}
.film .meta{{padding:18px 20px 22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}} .film h3{{font-size:22px;flex:1 1 200px;text-transform:none}}
.seg{{display:inline-flex;background:color-mix(in srgb,var(--fg) 7%,transparent);border-radius:999px;padding:4px}}
.seg button{{border:0;background:transparent;color:var(--fg);padding:8px 14px;border-radius:999px;font:500 14px var(--bf);cursor:pointer}} .seg button.on{{background:var(--ac);color:var(--ink)}}
.why{{display:grid;gap:18px;margin-top:44px}} @media(min-width:800px){{.why{{grid-template-columns:repeat(3,1fr)}}}}
.card{{background:var(--sf);border-radius:var(--r);padding:28px;border:1px solid color-mix(in srgb,var(--fg) 8%,transparent)}}
.card .n{{font-family:var(--hf);font-size:44px;color:var(--ac);line-height:1;margin-bottom:18px;font-weight:{t['hw']}}} .card h3{{font-size:22px;margin-bottom:10px;text-transform:none}} .card p{{color:var(--mu);margin:0}}
.alt{{background:var(--sf)}} .alt .card{{background:var(--bg)}}
.steps{{display:grid;gap:18px;margin-top:44px;counter-reset:s}} @media(min-width:900px){{.steps{{grid-template-columns:repeat(4,1fr)}}}}
.step{{position:relative;padding-top:22px;border-top:2px solid var(--ac)}} .step b{{display:block;font-family:var(--hf);font-size:15px;color:var(--ac);letter-spacing:.1em;margin-bottom:8px}}
.expl{{margin-top:44px;border-radius:calc(var(--r) + 4px);overflow:hidden;max-width:900px;background:#000}} .expl video{{width:100%;aspect-ratio:16/9}}
.price{{display:grid;gap:18px;margin-top:44px}} @media(min-width:900px){{.price{{grid-template-columns:repeat(3,1fr);align-items:stretch}}}}
.price .card{{display:flex;flex-direction:column}} .price .amt{{font-family:var(--hf);font-size:30px;margin:14px 0 10px;font-weight:{t['hw']}}}
.price .hot{{border:2px solid var(--ac);position:relative}} .price .tag{{position:absolute;top:-13px;left:24px;background:var(--ac);color:var(--ink);font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px}}
.terms{{color:var(--mu);font-size:14.5px;margin-top:22px;max-width:80ch}}
.final{{background:var(--ac);color:var(--ink);text-align:center}} .final .sh{{margin:0 auto;max-width:20ch}} .final p{{max-width:52ch;margin:18px auto 30px;opacity:.85}}
.final .btn.a{{background:var(--ink);color:var(--ac);box-shadow:none}} .final .btn.b{{border-color:var(--ink);color:var(--ink)}} .final .btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
footer{{padding:36px 0 48px;color:var(--mu);font-size:13.5px}} footer .wrap{{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}} footer img{{height:28px;width:auto;opacity:.85}} footer p{{margin:0;flex:1 1 300px}}
.rv{{opacity:0;transform:translateY(24px);transition:opacity .8s ease,transform .8s ease}} .rv.in{{opacity:1;transform:none}}
@media(max-width:720px){{nav .links{{display:none}} nav .btn{{margin-left:auto}} body{{font-size:16px}}}}
@media(prefers-reduced-motion:reduce){{.rv{{opacity:1;transform:none;transition:none}} html{{scroll-behavior:auto}} .btn{{transition:none}}}}"""
JS = """<script>
const n=document.querySelector('nav');addEventListener('scroll',()=>n.classList.toggle('s',scrollY>40),{passive:true});
document.querySelectorAll('.film').forEach(f=>f.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{
 f.querySelectorAll('.seg button').forEach(x=>x.classList.remove('on'));b.classList.add('on');const v=f.querySelector('video');
 f.classList.toggle('v',b.dataset.v==='1');v.src=b.dataset.src;v.play().catch(()=>{});}));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
const hv=document.querySelector('.hero video');if(matchMedia('(prefers-reduced-motion: reduce)').matches&&hv){hv.removeAttribute('autoplay');hv.pause()}
</script>"""
for c in O["companies"]:
    sec, acc, expl = CO[c["id"]]; t = dict(THEMES[sec]); t["ac"] = acc or t["ac"]; L = c["lang"]
    tok = tokens.setdefault(c["id"], secrets.token_urlsafe(9)); d = f"{ROOT}/{tok}"; os.makedirs(d)
    tx = O["text"][L]; u = UI[L]; p = O["prices"][L]; hook, why = SEC[(sec, L)]; name = E(c["name"])
    first = c["films"][0][0]
    src = f"{S}/final_music/{first}.mp4"; du = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{du*0.12:.2f}","-t","8","-i",src,"-vf","scale=1280:-2,fade=t=in:st=0:d=0.5,fade=t=out:st=7.5:d=0.5","-an","-c:v","libx264","-crf","24","-preset","slow","-pix_fmt","yuv420p","-movflags","+faststart",f"{d}/hero.mp4"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{du*0.12+1:.2f}","-i",src,"-frames:v","1","-vf","scale=1280:-2","-q:v","4",f"{d}/hero.jpg"],check=True)
    shutil.copy(f"{S}/offers_pdf/{c['id']}_offer.pdf", f"{d}/offer.pdf"); shutil.copy(f"{S}/brand/logo.png", f"{d}/logo.png"); shutil.copy(f"{S}/brand/icon_512.png", f"{d}/icon.png")
    films = ""
    for fid, label in c["films"]:
        shutil.copy(f"{S}/pitch/{fid}_pitch.mp4", f"{d}/{fid}.mp4"); shutil.copy(f"{S}/pitch_9x16/{fid}_pitch_9x16.mp4", f"{d}/{fid}_9x16.mp4")
        shutil.copy(f"{S}/previews/{fid}_poster.jpg", f"{d}/{fid}.jpg")
        films += f"""<article class="film rv"><div class="vw"><video controls playsinline preload="none" poster="{fid}.jpg" src="{fid}.mp4"></video></div>
<div class="meta"><h3>{E(label)}</h3><div class="seg"><button class="on" data-src="{fid}.mp4">{u['h']}</button><button data-v="1" data-src="{fid}_9x16.mp4">{u['v']}</button></div></div></article>"""
    explh = ""
    if expl and L == "mk":
        shutil.copy(f"{S}/explainers/{expl}.mp4", f"{d}/how.mp4")
        explh = f"""<div class="expl rv"><video controls playsinline preload="none" src="how.mp4" poster="hero.jpg"></video></div>"""
    steps = [s.split(". ", 1)[-1] for s in tx["how_d"].split(" → ")]
    wa = f"https://wa.me/{B['whatsapp']}?text=" + (c["name"] + " - " + u["cta"]).replace(" ", "%20")
    title = tx["title"].replace("{c}", c["name"])
    page = f"""<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet"><meta name="referrer" content="no-referrer"><meta name="theme-color" content="{t['bg']}">
<title>{E(title)} · {E(B['name'])}</title><link rel="icon" type="image/png" href="icon.png"><link rel="apple-touch-icon" href="icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>{css(t)}</style></head><body>
<nav><div class="wrap"><img src="logo.png" alt="{E(B['name'])}"><div class="links"><a href="#films">{u['films']}</a><a href="#how">{u['how']}</a><a href="#offer">{u['offer']}</a></div><a class="btn a" href="{wa}">{u['cta']}</a></div></nav>
<header class="hero"><video autoplay muted loop playsinline poster="hero.jpg" src="hero.mp4"></video>
<div class="wrap"><span class="pill">{u['pill']}</span><h1>{E(title.split(name)[0] if name in title else title)}<em>{name if name in title else ''}</em></h1>
<p>{E(hook)}</p><div class="btns"><a class="btn a" href="#films">{u['watch']}</a><a class="btn b" href="{wa}">{u['cta']}</a></div></div></header>
<section id="films"><div class="wrap"><div class="eyebrow rv">{u['films']}</div><h2 class="sh rv">{E(u['films_h'].replace('{c}', c['name']))}</h2><p class="sp rv">{E(u['films_p'])}</p>
<div class="films">{films}</div></div></section>
<section class="alt"><div class="wrap"><div class="eyebrow rv">{u['why']}</div><h2 class="sh rv">{E(hook.split(':')[0].split(',')[0])}</h2>
<div class="why">{''.join(f'<div class="card rv"><div class="n">0{i}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i,(a,b) in enumerate(why,1))}</div></div></section>
<section id="how"><div class="wrap"><div class="eyebrow rv">{u['how']}</div><h2 class="sh rv">{E(u['expl'] or tx['how'])}</h2>{f'<p class="sp rv">{E(u["expl_p"])}</p>' if u['expl_p'] and explh else ''}
<div class="steps">{''.join(f'<div class="step rv"><b>0{i}</b>{E(s)}</div>' for i,s in enumerate(steps,1))}</div>{explh}</div></section>
<section id="offer" class="alt"><div class="wrap"><div class="eyebrow rv">{u['offer']}</div><h2 class="sh rv">{E(tx['offer'])}</h2>
<div class="price"><div class="card rv"><h3>{E(tx['pilot'])}</h3><div class="amt">{E(p['pilot'])}</div><p>{E(tx['pilot_d'])}</p></div>
<div class="card hot rv"><span class="tag">{u['popular']}</span><h3>{E(tx['launch'])}</h3><div class="amt">{E(p['launch'])}</div><p>{E(tx['launch_d'])}</p></div>
<div class="card rv"><h3>{E(tx['monthly'])}</h3><div class="amt">{E(p['monthly'])}</div><p>{E(tx['monthly_d'])}</p></div></div>
<p class="terms rv">{E(tx['terms'])} {E(tx['price_note'])}</p></div></section>
<section class="final"><div class="wrap"><h2 class="sh rv">{E(u['final'])}</h2><p class="rv">{E(u['final_p'])}</p>
<div class="btns rv"><a class="btn a" href="{wa}">{u['cta']}</a><a class="btn b" href="mailto:{E(B['email'])}">{u['mail']}</a><a class="btn b" href="offer.pdf">{u['pdf']}</a></div></div></section>
<footer><div class="wrap"><img src="logo.png" alt=""><p>{E(u['note'])}</p><p>{E(B['phone'])} · {E(B['email'])} · {E(B['web'])}</p></div></footer>
{JS}</body></html>"""
    open(f"{d}/index.html", "w").write(page); print("OK", c["id"], sec, flush=True)
json.dump(tokens, open(tokfile, "w"), indent=1)
open(f"{ROOT}/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
open(f"{S}/pitch_site/nginx.conf", "w").write("""server {
  listen 80; root /usr/share/nginx/html; autoindex off; server_tokens off;
  add_header X-Robots-Tag "noindex, nofollow, noarchive" always;
  add_header Referrer-Policy "no-referrer" always;
  add_header X-Content-Type-Options "nosniff" always;
  location = / { return 404; }
  location = /robots.txt { }
  location ~ "^/[A-Za-z0-9_-]{8,}/" { try_files $uri $uri/index.html =404; expires 1h; }
  location / { return 404; }
}
""")
open(f"{S}/pitch_site/docker-compose.yml", "w").write("""name: ai-studio-pitch
services:
  web:
    image: nginx:alpine
    container_name: ai-studio-pitch
    restart: unless-stopped
    volumes:
      - /opt/stacks/ai-studio-pitch/site:/usr/share/nginx/html:ro
      - /opt/stacks/ai-studio-pitch/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    mem_limit: 128m
    pids_limit: 64
    labels:
      - traefik.enable=true
      - traefik.http.routers.ai-studio-pitch.rule=Host(`pitch.srv1231216.hstgr.cloud`)
      - traefik.http.routers.ai-studio-pitch.entrypoints=websecure
      - traefik.http.routers.ai-studio-pitch.tls.certresolver=letsencrypt
      - traefik.http.services.ai-studio-pitch.loadbalancer.server.port=80
""")
print("SITES_DONE")
