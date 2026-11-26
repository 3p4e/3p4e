# Foton v2 films page for the private Foton pitch link (<token>/v2/): the 11 new Tunland films, 16:9 and 9:16, Macedonian.
# Builds $S/fv2/web (index.html + films + posters); cut/gen_sites.py copies it into the Foton token folder on every rebuild.
import os, sys, json, html, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from films import FILMS
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; CUTS = f"{S}/fv2/cuts"; W = f"{S}/fv2/web"
shutil.rmtree(W, ignore_errors=True); os.makedirs(f"{W}/f"); E = html.escape
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
cards = []
for f in FILMS:
    fid = f["id"]
    for suf in ("", "_9x16"):
        os.link(f"{CUTS}/{fid}{suf}.mp4", f"{W}/f/{fid}{suf}.mp4")   # hardlink: same bytes, no extra disk
        run(["ffmpeg", "-v", "error", "-y", "-ss", "2.8", "-i", f"{CUTS}/{fid}{suf}.mp4", "-frames:v", "1", "-vf", "scale=-2:540" if not suf else "scale=-2:640", "-q:v", "4", f"{W}/f/{fid}{suf}.jpg"])
    d = int(dur(f"{CUTS}/{fid}.mp4"))
    t = f"{f['title']} · Tunland {f['model']}"
    cards.append(f'<li class="c" data-id="{fid}"><button type="button" class="pl" aria-label="Пушти: {E(t)}"><img src="f/{fid}.jpg" alt="" loading="lazy" width="960" height="540"><span class="du">0:{d:02d}</span></button>'
                 f'<div class="m"><b>{E(t)}</b><span>{E(f["card"][1])}</span></div></li>')
page = f'''<!doctype html><html lang="mk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Foton Tunland · 11 нови AI филмови · BIG DOGMA</title>
<style>:root{{--bg:#0b0b0d;--sf:#16161a;--fg:#f2f2f4;--mu:#9a9aa5;--ac:#d71920}}*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}}
.w{{max-width:1180px;margin:0 auto;padding:0 16px}}header{{padding:40px 0 18px}}h1{{font-size:clamp(28px,5vw,46px);line-height:1.1;margin:0 0 10px}}
h1 em{{font-style:normal;color:var(--ac)}}p.s{{color:var(--mu);max-width:62ch;margin:0}}.t{{display:flex;gap:8px;margin:22px 0 6px}}
.t button{{background:var(--sf);color:var(--fg);border:1px solid #2a2a30;border-radius:999px;padding:8px 16px;font:inherit;cursor:pointer}}
.t button[aria-pressed=true]{{background:var(--ac);border-color:var(--ac)}}
ul{{list-style:none;padding:0;margin:18px 0 40px;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px}}
.c{{background:var(--sf);border-radius:14px;overflow:hidden}}.pl{{display:block;position:relative;width:100%;padding:0;border:0;background:#000;cursor:pointer}}
.pl img{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}}.v .pl img{{aspect-ratio:9/16}}
.du{{position:absolute;right:8px;bottom:8px;background:rgba(0,0,0,.7);border-radius:6px;padding:2px 7px;font-size:13px}}
.pl::after{{content:"";position:absolute;left:50%;top:50%;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;background:rgba(215,25,32,.9) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M8 5v14l11-7z'/%3E%3C/svg%3E") center/26px no-repeat}}
.m{{padding:12px 14px 14px}}.m b{{display:block}}.m span{{color:var(--mu);font-size:14px}}
.v ul{{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}}
#lb{{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:9;padding:16px}}#lb.o{{display:flex}}
#lb video{{max-width:100%;max-height:88vh;border-radius:10px}}#x{{position:absolute;top:12px;right:14px;background:none;border:0;color:#fff;font-size:34px;cursor:pointer}}
footer{{color:var(--mu);font-size:13px;padding:0 0 40px}}</style></head><body>
<header class="w"><h1>Foton Tunland: <em>11 нови AI филмови</em></h1>
<p class="s">Концепт подготвен за Фотон Македонија: 11 енергични реклами со Tunland V9, G7 и V7 во различни бои, во Скопје, Матка, Водно, Треска и на Пелистерски Очи. Секој филм има свој глас и оригинална музика, во 16:9 и 9:16. Сите кадри се генерирани со AI; ништо не е снимено.</p>
<div class="t" role="group" aria-label="Формат"><button type="button" aria-pressed="true" data-v="">16:9</button><button type="button" aria-pressed="false" data-v="_9x16">9:16 мобилен</button></div></header>
<main class="w"><ul id="g">{"".join(cards)}</ul></main>
<div id="lb" role="dialog" aria-modal="true" aria-label="Видео"><button id="x" type="button" aria-label="Затвори">×</button><video controls playsinline></video></div>
<footer class="w">Концепт · не е за објава · BIG DOGMA AI видео студио, Скопје</footer>
<script>(function(){{var suf='',lb=document.getElementById('lb'),v=lb.querySelector('video'),op=null;
document.querySelectorAll('.t button').forEach(function(b){{b.onclick=function(){{suf=b.dataset.v;document.querySelectorAll('.t button').forEach(function(x){{x.setAttribute('aria-pressed',String(x===b))}});
document.body.classList.toggle('v',!!suf);document.querySelectorAll('.c').forEach(function(c){{c.querySelector('img').src='f/'+c.dataset.id+suf+'.jpg'}})}}}});
document.querySelectorAll('.pl').forEach(function(p){{p.onclick=function(){{op=p;v.src='f/'+p.parentNode.dataset.id+suf+'.mp4';lb.classList.add('o');v.play();document.getElementById('x').focus()}}}});
function cl(){{v.pause();v.removeAttribute('src');v.load();lb.classList.remove('o');if(op)op.focus()}}
document.getElementById('x').onclick=cl;lb.onclick=function(e){{if(e.target===lb)cl()}};addEventListener('keydown',function(e){{if(e.key==='Escape'&&lb.classList.contains('o'))cl()}});}})();</script>
</body></html>'''
open(f"{W}/index.html", "w").write(page); print("ok", len(FILMS), "films")
