# Private, unlisted pitch page per company (LTX films only: hostable anywhere). Static HTML + video files, noindex.
# Layout: studio header, film player (16:9 / 9:16 toggle), stills, short offer, PDF, one CTA (WhatsApp / email), concept note.
import os, json, shutil, secrets, html
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
O = json.load(open(f"{S}/cut/offers.json")); B = json.load(open(f"{S}/brand/brand.json"))
ROOT = f"{S}/pitch_pages"; shutil.rmtree(ROOT, ignore_errors=True); os.makedirs(ROOT)
tokfile = f"{S}/cut/page_tokens.json"
tokens = json.load(open(tokfile)) if os.path.exists(tokfile) else {}
UI = {"mk": dict(watch="Погледнете", h="Хоризонтално 16:9", v="Вертикално 9:16 (мобилен)", offer="Понуда", pdf="Преземи понуда (PDF)", cta="Закажи 15 минути", mail="Пиши е-пошта",
                 note="Концепт само за презентација. Не е објавен и нема да биде објавен без ваше изречно писмено одобрение. Видеото е изработено со вештачка интелигенција."),
      "sr": dict(watch="Pogledajte", h="Horizontalno 16:9", v="Vertikalno 9:16 (mobilni)", offer="Ponuda", pdf="Preuzmi ponudu (PDF)", cta="Zakaži 15 minuta", mail="Pošalji e-poštu",
                 note="Koncept samo za prezentaciju. Nije objavljen i neće biti objavljen bez vašeg izričitog pisanog odobrenja. Video je napravljen uz pomoć veštačke inteligencije."),
      "sq": dict(watch="Shikoni", h="Horizontal 16:9", v="Vertikal 9:16 (celular)", offer="Oferta", pdf="Shkarko ofertën (PDF)", cta="Cakto 15 minuta", mail="Dërgo email",
                 note="Koncept vetëm për prezantim. Nuk është publikuar dhe nuk do të publikohet pa miratimin tuaj të shprehur me shkrim. Video e krijuar me inteligjencë artificiale.")}
for c in O["companies"]:
    tok = tokens.setdefault(c["id"], secrets.token_urlsafe(9)); d = f"{ROOT}/{tok}"; os.makedirs(d)
    t = O["text"][c["lang"]]; u = UI[c["lang"]]; p = O["prices"][c["lang"]]; name = html.escape(c["name"])
    films = ""
    for fid, label in c["films"]:
        for src, dst in ((f"{S}/pitch/{fid}_pitch.mp4", f"{fid}.mp4"), (f"{S}/pitch_9x16/{fid}_pitch_9x16.mp4", f"{fid}_9x16.mp4"), (f"{S}/previews/{fid}_poster.jpg", f"{fid}.jpg")):
            shutil.copy(src, f"{d}/{dst}")
        films += f"""<section class="film"><h3>{html.escape(label)}</h3>
<div class="tabs"><button class="on" onclick="sw(this,'{fid}.mp4')">{u['h']}</button><button onclick="sw(this,'{fid}_9x16.mp4')">{u['v']}</button></div>
<video controls playsinline preload="metadata" poster="{fid}.jpg" src="{fid}.mp4"></video></section>"""
    shutil.copy(f"{S}/offers_pdf/{c['id']}_offer.pdf", f"{d}/offer.pdf"); shutil.copy(f"{S}/brand/logo.png", f"{d}/logo.png")
    wa = f"https://wa.me/{B['whatsapp']}?text=" + html.escape(f"{c['name']} – {u['cta']}").replace(" ", "%20")
    page = f"""<!doctype html><html lang="{c['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive"><title>{name} · {html.escape(B['name'])}</title>
<style>:root{{--bg:#0d0d0f;--fg:#f4f4f6;--mut:#a8a8b0;--acc:{B['accent']}}}*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}}
header{{display:flex;justify-content:space-between;align-items:center;padding:16px;max-width:980px;margin:auto}} header img{{height:44px}}
main{{max-width:980px;margin:auto;padding:0 16px 40px}} h1{{font-size:clamp(24px,5vw,36px);margin:12px 0}} .intro{{color:var(--mut);line-height:1.6}}
.film{{margin:26px 0}} .film h3{{margin:0 0 10px}} video{{width:100%;max-height:78vh;background:#000;border-radius:12px;display:block}}
.tabs{{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}} .tabs button{{background:#1d1d22;color:var(--fg);border:1px solid #333;border-radius:20px;padding:8px 14px;cursor:pointer}}
.tabs button.on{{background:var(--acc);color:#111;border-color:var(--acc)}} table{{width:100%;border-collapse:collapse;margin-top:8px}}
td{{padding:10px 8px;border-bottom:1px solid #26262c;vertical-align:top}} td.p{{color:var(--acc);font-weight:700;text-align:right;white-space:nowrap}}
.cta{{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0}} .cta a{{text-decoration:none;padding:14px 20px;border-radius:10px;font-weight:700}}
.cta .a{{background:var(--acc);color:#111}} .cta .b{{border:1px solid #444;color:var(--fg)}} .note{{font-size:13px;color:var(--mut);border-top:1px solid #26262c;padding-top:14px}}</style></head>
<body><header><img src="logo.png" alt="{html.escape(B['name'])}"><span style="color:var(--mut);font-size:14px">{html.escape(B['phone'])}</span></header>
<main><h1>{html.escape(t['title'].replace('{c}', c['name']))}</h1><p class="intro">{html.escape(t['intro'].replace('{c}', c['name']))}</p>
{films}<h2>{u['offer']}</h2><table><tr><td><b>{t['pilot']}</b><br><span style="color:var(--mut)">{t['pilot_d']}</span></td><td class="p">{p['pilot']}</td></tr>
<tr><td><b>{t['launch']}</b><br><span style="color:var(--mut)">{t['launch_d']}</span></td><td class="p">{p['launch']}</td></tr>
<tr><td><b>{t['monthly']}</b><br><span style="color:var(--mut)">{t['monthly_d']}</span></td><td class="p">{p['monthly']}</td></tr></table>
<p class="intro" style="font-size:14px">{t['terms']} {t['price_note']}</p>
<div class="cta"><a class="a" href="{wa}">{u['cta']}</a><a class="b" href="mailto:{B['email']}">{u['mail']}</a><a class="b" href="offer.pdf">{u['pdf']}</a></div>
<p class="note">{u['note']}</p></main>
<script>function sw(b,src){{var s=b.closest('.film');s.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');var v=s.querySelector('video');v.src=src;v.play()}}</script></body></html>"""
    open(f"{d}/index.html", "w").write(page); print("OK", c["id"], tok, flush=True)
json.dump(tokens, open(tokfile, "w"), indent=1)
open(f"{ROOT}/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
print("PAGES_DONE")
