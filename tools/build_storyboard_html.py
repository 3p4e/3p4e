#!/usr/bin/env python3
"""Cinematic storyboard generator — human pre-vis + machine render spec in one file.

A storyboard must do two jobs:
  1. Let a human (or director) SEE the film: acts, shots, blocking, camera moves, cues.
  2. Let an AI (SkyReels-V3 job builder) EXECUTE the film: per-shot FLF keyframes,
     camera grammar, continuity anchors, motion validation, and a global render spec.

This generator emits a single self-contained HTML that carries BOTH layers.
The machine layer is embedded as <script type="application/json" id="storyboard-spec">
so a downstream agent can scrape it directly with zero re-interpretation.

Data schema (dict):
{
  "title_mk": str, "title_en": str, "genre": str, "logline": str,
  "spec": {                                  # global render contract
      "aspect": "16:9", "resolution": "1280x720", "fps": 24, "model": "SkyReels-V3-identity",
      "style": "photoreal", "flf": true, "language": "mk",
      "shot_floor": 40, "shot_max": 60,
      "seed_policy": "fixed-per-shot",
      "negative_prompt": "...",
      "style_anchor": ["Diablo 2 cinematic", "WoW cinematic", "StarCraft cinematic"]
  },
  "cast": [ {"role": str, "trait": str, "source": str, "face_lock": str} ],
  "acts": [ {"id","num","title","color","pct","synopsis","shots":[
      {"id":"S01","size":"WIDE","angle":"low-angle","move":"push-in","dur":4.0,
       "clip_s":5.0,                          # rendered clip length (5s per SkyReels)
       "narration_mk":"...",                  # voice-over (narration) line
       "dialogue_mk":"...",                   # actor line ('' if none)
       "kf_first":"ENGLISH prompt for the START frame",
       "kf_last":"ENGLISH prompt for the END frame (FLF)",
       "mid":"optional mid-frame prompt",
       "continuity":"what carries over from the previous shot",
       "motion":"expected motion to validate (e.g. push-in on subject's eyes)",
       "scene":"<svg> for the human view", "span":"sp4"}
  ]}
}
"""
import json, pathlib, html as H

CSS = """
:root{--bg:#050507;--ink:#f5f2ea;--mut:#98988f;--hair:rgba(255,255,255,.08);--gold:#d4af37;--ease:cubic-bezier(0.32,0.72,0,1);}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:
  radial-gradient(1100px 520px at 88% -8%,rgba(212,175,55,.13),transparent 60%),
  radial-gradient(900px 480px at -8% 12%,rgba(45,212,191,.10),transparent 55%),
  radial-gradient(1000px 680px at 50% 112%,rgba(239,68,68,.09),transparent 60%),
  var(--bg);color:var(--ink);font-family:'Clash Display','Plus Jakarta Sans',system-ui,-apple-system,sans-serif;
  line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;}
body::before{content:"";position:fixed;inset:0;z-index:60;pointer-events:none;opacity:.05;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
.nav{position:sticky;top:0;z-index:50;display:flex;justify-content:center;padding:14px 0;}
.nav-in{display:flex;gap:4px;align-items:center;padding:5px;background:rgba(10,10,14,.72);
  backdrop-filter:blur(22px);border:1px solid var(--hair);border-radius:999px;}
.nav-in a{color:var(--mut);text-decoration:none;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;padding:7px 14px;border-radius:999px;transition:all .6s var(--ease);}
.nav-in a:hover{color:var(--ink);background:rgba(255,255,255,.06)}
.wrap{max-width:1360px;margin:0 auto;padding:40px 26px 140px;}
.eyebrow{display:inline-flex;gap:8px;align-items:center;padding:6px 14px;border-radius:999px;
  border:1px solid var(--hair);font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);}
.eyebrow i{width:6px;height:6px;border-radius:50%;background:var(--gold);box-shadow:0 0 12px var(--gold)}
h1{font-size:clamp(2.6rem,7vw,5.6rem);line-height:.98;letter-spacing:-.035em;margin:20px 0 12px;
  background:linear-gradient(120deg,#fff 22%,#d8d4c8 68%,#8f8b81);-webkit-background-clip:text;background-clip:text;color:transparent;}
.lede{max-width:760px;color:var(--mut);font-size:1.05rem;}
.meta{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 6px;}
.chip{padding:9px 16px;border-radius:14px;border:1px solid var(--hair);background:rgba(255,255,255,.03);font-size:13px;color:var(--mut);}
.chip b{color:var(--ink);font-weight:600}
.chip.gold{color:var(--gold);border-color:rgba(212,175,55,.35)}
.shell{border-radius:2rem;padding:8px;background:rgba(255,255,255,.04);border:1px solid var(--hair);margin:40px 0;}
.core{border-radius:calc(2rem - 8px);background:rgba(8,8,11,.72);box-shadow:inset 0 1px 1px rgba(255,255,255,.07);padding:28px;overflow:hidden;}
.g{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;}
.c{border-radius:1.3rem;padding:14px;background:rgba(255,255,255,.025);border:1px solid var(--hair);
  transition:transform .7s var(--ease),border-color .7s var(--ease),background .7s var(--ease),box-shadow .7s var(--ease);}
.c:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.2);background:rgba(255,255,255,.05);box-shadow:0 18px 40px -24px rgba(0,0,0,.8)}
.sp2{grid-column:span 2}.sp3{grid-column:span 3}.sp4{grid-column:span 4}.sp5{grid-column:span 5}.sp6{grid-column:span 6}.sp8{grid-column:span 8}.sp12{grid-column:span 12}
.frame{position:relative;border-radius:11px;overflow:hidden;aspect-ratio:16/10;background:linear-gradient(160deg,#12121a,#0b0b10);border:1px solid var(--hair);}
.frame svg{width:100%;height:100%;display:block}
.sid{position:absolute;top:12px;left:12px;font-size:9px;letter-spacing:.16em;color:var(--gold);font-weight:600;
  padding:3px 9px;border-radius:999px;background:rgba(0,0,0,.6);border:1px solid var(--hair)}
.gm{margin-top:12px;font-size:11.5px;color:var(--mut);line-height:1.45}
.gm b{color:var(--ink);font-weight:600;letter-spacing:.03em}
.cue{margin-top:8px;font-size:12.3px;border-left:2px solid;padding-left:9px;}
.cue.narr{border-color:#2dd4bf;color:#bfe8e1}.cue.dlg{border-color:#f59e0b;color:#f3d9a8}
.cue .tag{font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;display:block;margin-bottom:2px}
.spec{margin-top:10px;border-top:1px dashed var(--hair);padding-top:10px;font-size:11.5px;color:var(--mut);}
.spec .kv{display:grid;gap:5px;margin-top:6px}
.spec .row{display:flex;gap:8px;align-items:baseline}
.spec .k{flex:none;width:58px;font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);opacity:.8}
.spec .v{color:#d7d4ca;}
.spec code{font-family:'SFMono-Regular',ui-monospace,Menlo,monospace;font-size:10.5px;color:#b9e3dc;word-break:break-word;line-height:1.5}
.spec code.endl{color:#f3d9a8}
.rail{display:flex;align-items:center;gap:12px;margin-bottom:20px}
.dot{width:11px;height:11px;border-radius:50%;flex:none}
.rail .n{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut)}
.rail h2{margin:0;font-size:1.45rem;letter-spacing:-.02em;font-weight:600}
.rail .bar{flex:1;height:1px;background:linear-gradient(90deg,var(--hair),transparent)}
.note{font-size:13px;color:var(--mut);max-width:900px;margin:0 0 6px}
.note b{color:var(--ink)}
.specgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin-top:14px}
.specbox{border:1px solid var(--hair);border-radius:14px;padding:12px 14px;background:rgba(255,255,255,.02)}
.specbox .sk{font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);opacity:.85}
.specbox .sv{font-size:13px;color:#d7d4ca;margin-top:4px;word-break:break-word}
.specbox .sv code{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#b9e3dc}
.specbox.wide{grid-column:1 / -1}
@keyframes pu{0%{transform:scale(1)}100%{transform:scale(1.3)}}
@keyframes pl{0%{transform:translateX(0)}100%{transform:translateX(-30px)}}
@keyframes pr{0%{transform:translateX(0)}100%{transform:translateX(30px)}}
@keyframes tr{0%{transform:translate(0,0)}100%{transform:translate(20px,-14px)}}
@keyframes cr{0%{transform:translateY(0)}100%{transform:translateY(-24px)}}
@keyframes dash{to{stroke-dashoffset:-24}}
.m-push{animation:pu 4s var(--ease) infinite alternate}
.m-panl{animation:pl 4.6s var(--ease) infinite alternate}
.m-panr{animation:pr 4.6s var(--ease) infinite alternate}
.m-track{animation:tr 4s var(--ease) infinite alternate}
.m-crane{animation:cr 4.4s var(--ease) infinite alternate}
.m-arrow{stroke-dasharray:24;animation:dash 1.5s linear infinite}
svg *{transform-box:fill-box;transform-origin:center}
.rv{opacity:0;transform:translateY(34px);filter:blur(8px);transition:opacity .9s var(--ease),transform .9s var(--ease),filter .9s var(--ease)}
.rv.in{opacity:1;transform:none;filter:none}
.tl{position:relative;height:70px;border-radius:16px;background:rgba(255,255,255,.025);border:1px solid var(--hair);overflow:hidden}
.tl .seg{position:absolute;top:0;bottom:0;display:flex;align-items:center;padding:0 16px;font-size:12px;font-weight:600;letter-spacing:.05em}
.playhead{position:absolute;top:-8px;bottom:-8px;width:2px;background:var(--gold);box-shadow:0 0 14px var(--gold);animation:scrub 16s var(--ease) infinite alternate}
@keyframes scrub{0%{left:0%}100%{left:100%}}
.legend{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}
.legend .li{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--mut)}
.sw{width:24px;height:12px;border-radius:4px;border:1px solid var(--hair)}
.glyph{font-family:monospace;font-size:11px;color:var(--ink)}
.blocking{position:relative;border-radius:16px;border:1px solid var(--hair);background:radial-gradient(circle at 50% 50%,#101018,#07070b);min-height:260px;overflow:hidden}
.blocking .stage{position:absolute;inset:0}
.filmstrip{display:flex;gap:10px;overflow:hidden;padding:8px 0;mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.fs-track{display:flex;gap:10px;animation:roll 38s linear infinite}
@keyframes roll{to{transform:translateX(-50%)}}
.fs{width:170px;flex:none;border-radius:10px;overflow:hidden;border:1px solid var(--hair);background:#0c0c12}
.fs svg{width:100%;display:block;aspect-ratio:16/10}
.fs .lbl{font-size:10px;color:var(--mut);padding:6px 8px;letter-spacing:.06em}
.castrow{display:flex;justify-content:space-between;gap:12px;align-items:center}
.castrow b{font-size:14px}
.castrow .sub{font-size:12px;color:var(--mut)}
.castrow .lock{font-size:11px;letter-spacing:.05em;color:var(--gold)}
@media(max-width:900px){.g{grid-template-columns:repeat(6,1fr)}}
@media(max-width:768px){.wrap{padding:26px 14px 80px}.core{padding:18px}.g{grid-template-columns:1fr 1fr;gap:10px}
  .sp2,.sp3,.sp4,.sp5,.sp6,.sp8,.sp12{grid-column:span 1}.nav-in a{padding:6px 9px;font-size:9px}}
@media(max-width:480px){.g{grid-template-columns:1fr}}
"""

SHOT_TEMPLATE = """
<div class="c {span} rv"><div class="frame">
<svg viewBox="0 0 160 100" aria-hidden="true">{scene}</svg>
<span class="sid">{sid}</span></div>
<div class="gm"><b>{size}</b> · {angle} · <b>{move}</b> · {dur}s · clip {clip_s}s</div>
<div class="cue {cue}"><span class="tag">{cue_label}</span>{cue_txt}</div>
<div class="spec">
{spec_rows}
</div></div>"""

NL = chr(10)

def _placeholder(sh):
    sid = sh.get("id",""); size = sh.get("size","")
    return ('<rect width="160" height="100" fill="#0d0d12"/>'
            '<rect x="5" y="5" width="150" height="90" fill="none" stroke="#ffffff12" rx="6"/>'
            '<text x="80" y="46" text-anchor="middle" font-size="12" fill="#4a4a58" font-family="monospace">'+H.escape(size)+'</text>'
            '<text x="80" y="62" text-anchor="middle" font-size="8" fill="#33333c" font-family="monospace">'+H.escape(sid)+'</text>'
            '<path d="M24 82 L136 82" stroke="#ffffff0d"/>')


def _spec_rows(sh):
    rows = []
    if sh.get("kf_first"):
        rows.append(f'<div class="row"><span class="k">KF·A</span><code>{H.escape(sh["kf_first"])}</code></div>')
    if sh.get("kf_last"):
        rows.append(f'<div class="row"><span class="k">KF·B</span><code class="endl">{H.escape(sh["kf_last"])}</code></div>')
    if sh.get("mid"):
        rows.append(f'<div class="row"><span class="k">MID</span><code>{H.escape(sh["mid"])}</code></div>')
    if sh.get("continuity"):
        rows.append(f'<div class="row"><span class="k">CONT</span><span class="v">{H.escape(sh["continuity"])}</span></div>')
    if sh.get("motion"):
        rows.append(f'<div class="row"><span class="k">MOTION</span><span class="v">{H.escape(sh["motion"])}</span></div>')
    return '<div class="kv">' + NL.join(rows) + '</div>'

def act_section(act):
    cells = []
    for sh in act["shots"]:
        cue_txt = sh.get("dialogue_mk") or sh.get("narration_mk") or ""
        cue = "dlg" if sh.get("dialogue_mk") else "narr"
        cue_label = "DIALOGUE" if cue == "dlg" else "NARRATION"
        cells.append(SHOT_TEMPLATE.format(
            span=sh.get("span","sp4"), sid=sh["id"], scene=sh.get("scene") or _placeholder(sh),
            size=sh["size"], angle=sh["angle"], move=sh["move"], dur=sh["dur"],
            clip_s=sh.get("clip_s", 5.0), cue=cue, cue_label=cue_label,
            cue_txt=H.escape(cue_txt), spec_rows=_spec_rows(sh)))
    dot = f'<span class="dot" style="background:{act["color"]};box-shadow:0 0 18px {act["color"]}"></span>'
    return f"""<div class="shell" id="{act['id']}"><div class="core">
<div class="rail rv">{dot}<span class="n">{act['num']}</span><h2>{H.escape(act['title'])}</h2><span class="bar"></span></div>
<p class="note rv">{H.escape(act['synopsis'])}</p>
<div class="g">{NL.join(cells)}</div></div></div>"""

def timeline(data):
    total = sum(a.get("pct", 33.3) for a in data["acts"])
    left = 0; segs = []
    for a in data["acts"]:
        w = a.get("pct", 33.3)/total*100
        segs.append(f'<div class="seg" style="left:{left}%;width:{w}%;background:{a["color"]}22;border-right:1px solid var(--hair)">{a["num"]} · {H.escape(a["title"])}</div>')
        left += w
    return f'<div class="tl">{NL.join(segs)}<div class="playhead"></div></div>'

def filmstrip(data):
    items=[]
    for a in data["acts"]:
        for sh in a["shots"]:
            micro = sh.get("scene_micro") or f'<svg viewBox="0 0 160 100">{sh.get("scene") or _placeholder(sh)}</svg>'
            items.append(f'<div class="fs">{micro}<div class="lbl">{sh["id"]} · {sh["move"]}</div></div>')
    half="".join(items)
    return f'<div class="filmstrip"><div class="fs-track">{half}{half}</div></div>'

def blocking_map(data):
    cams = ['<circle cx="42" cy="58" r="4" fill="#d4af37"/>','<circle cx="84" cy="32" r="4" fill="#d4af37"/>','<circle cx="128" cy="62" r="4" fill="#d4af37"/>']
    actors = ['<circle cx="80" cy="70" r="5" fill="#2dd4bf"/>','<circle cx="108" cy="60" r="5" fill="#f59e0b"/>','<circle cx="58" cy="42" r="5" fill="#ef4444"/>']
    cones = ['<path d="M42 54 L58 18 L100 18" fill="none" stroke="#d4af37" stroke-width="1" opacity=".5"/>']
    grid = ''.join(f'<line x1="0" y1="{y}" x2="160" y2="{y}"/><line x1="{x}" y1="0" x2="{x}" y2="100"/>' for y in range(10,100,18) for x in range(10,160,20))
    c = data.get("cast", [])
    tags = []
    for i, name in enumerate(["PERSEUS","HERMES","MEDUSA"]):
        tags.append(f'<text x="84" y="{80+i*0}" fill="#9a9a92" font-size="7">CAM</text>')
    labels = ['<text x="70" y="84" fill="#2dd4bf" font-size="7">PERSEUS</text>',
              '<text x="100" y="72" fill="#f59e0b" font-size="7">HERMES</text>',
              '<text x="46" y="56" fill="#ef4444" font-size="7">MEDUSA</text>']
    # derive actor labels from cast where possible
    if len(c) >= 3:
        labels = [f'<text x="70" y="84" fill="#2dd4bf" font-size="7">{H.escape(c[0]["role"].split(" ")[0])}</text>',
                  f'<text x="100" y="72" fill="#f59e0b" font-size="7">{H.escape(c[1]["role"].split(" ")[0])}</text>',
                  f'<text x="46" y="56" fill="#ef4444" font-size="7">{H.escape(c[2]["role"].split(" ")[0])}</text>']
    return f"""<div class="blocking"><svg class="stage" viewBox="0 0 160 100" preserveAspectRatio="xMidYMid meet">
<g stroke="#1c1c26" stroke-width="1">{grid}</g>
{''.join(cams)}{''.join(cones)}{''.join(actors)}{''.join(labels)}
<text x="42" y="76" fill="#9a9a92" font-size="7">CAM</text>
</svg></div>"""

def spec_section(data):
    s = data["spec"]
    boxes = []
    def box(k, v, wide=False, code=False):
        inner = f'<code>{H.escape(v)}</code>' if code else H.escape(v)
        return f'<div class="specbox{" wide" if wide else ""}"><div class="sk">{H.escape(k)}</div><div class="sv">{inner}</div></div>'
    boxes.append(box("resolution", s.get("resolution","1280x720")))
    boxes.append(box("aspect", s.get("aspect","16:9")))
    boxes.append(box("fps", str(s.get("fps",24))))
    boxes.append(box("model", s.get("model","SkyReels-V3")))
    boxes.append(box("style", s.get("style","photoreal")))
    boxes.append(box("FLF", "start+end keyframes" if s.get("flf",True) else "single-ref"))
    boxes.append(box("shot floor", str(s.get("shot_floor",40))))
    boxes.append(box("shot max", str(s.get("shot_max",60))))
    boxes.append(box("seed policy", s.get("seed_policy","fixed-per-shot"), code=True))
    boxes.append(box("style anchor", " · ".join(s.get("style_anchor",[])), wide=True))
    boxes.append(box("negative prompt", s.get("negative_prompt",""), wide=True, code=True))
    return '<div class="specgrid">' + NL.join(boxes) + '</div>'

def cast_table(data):
    rows=[]
    for c in data["cast"]:
        rows.append(f'<div class="c sp12 rv"><div class="castrow"><div><b>{H.escape(c["role"])}</b><div class="sub">{H.escape(c.get("trait",""))}</div></div>'\
                   f'<div style="text-align:right"><div class="lock">{H.escape(c.get("face_lock","AI-default"))}</div><div class="sub">{H.escape(c.get("source",""))}</div></div></div></div>')
    return "".join(rows)

def machine_payload(data):
    """Strip display-only fields (scene/svg) to produce a clean, executable spec."""
    def clean_shot(sh):
        return {k:v for k,v in sh.items() if k not in ("scene","scene_micro","span")}
    return {
        "meta": {"title_mk": data["title_mk"], "title_en": data.get("title_en",""),
                 "genre": data.get("genre",""), "logline": data.get("logline","")},
        "spec": data["spec"],
        "cast": data["cast"],
        "acts": [{"id":a["id"],"num":a["num"],"title":a["title"],"color":a["color"],
                   "synopsis":a["synopsis"],"shots":[clean_shot(s) for s in a["shots"]]} for a in data["acts"]],
    }

def build(data):
    nshots = sum(len(a["shots"]) for a in data["acts"])
    total_dur = round(sum(sh["dur"] for a in data["acts"] for sh in a["shots"]),1)
    total_clip = round(sum(sh.get("clip_s",5.0) for a in data["acts"] for sh in a["shots"]),1)
    acts_html = "".join(act_section(a) for a in data["acts"])
    spec = data["spec"]
    meta = f"""<div class="meta rv">
<div class="chip">Формат <b>{H.escape(spec.get('resolution','1280x720'))}</b></div><div class="chip">Кадри <b>{nshots}</b></div>
<div class="chip">Траење <b>~{total_dur}s</b></div><div class="chip">Рендер <b>{total_clip}s</b></div>
<div class="chip">Модел <b>{H.escape(spec.get('model','SkyReels-V3'))}</b></div>
<div class="chip gold">Статус <b>proof exemplar</b></div></div>"""
    legend = f"""<div class="legend rv">
<div class="li"><span class="sw" style="background:{data['acts'][0]['color']}"></span> {data['acts'][0]['num']}</div>
<div class="li"><span class="sw" style="background:{data['acts'][1]['color']}"></span> {data['acts'][1]['num']}</div>
<div class="li"><span class="sw" style="background:{data['acts'][2]['color']}"></span> {data['acts'][2]['num']}</div>
<div class="li"><span class="glyph">→</span> track/pan</div><div class="li"><span class="glyph">◎</span> push-in</div>
<div class="li"><span class="glyph">↗</span> crane</div><div class="li"><span class="glyph">⟲</span> shot/reverse</div></div>"""
    payload_json = json.dumps(machine_payload(data), ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html><html lang="mk"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(data['title_mk'])} — Cinematic Storyboard</title><style>{CSS}</style></head><body>
<div class="nav"><div class="nav-in">
<a href="#spec">Spec</a><a href="#{data['acts'][0]['id']}">{data['acts'][0]['num']}</a><a href="#{data['acts'][1]['id']}">{data['acts'][1]['num']}</a><a href="#{data['acts'][2]['id']}">{data['acts'][2]['num']}</a><a href="#timeline">Timeline</a><a href="#blocking">Blocking</a></div></div>
<div class="wrap">
<span class="eyebrow rv"><i></i> SkyReels-V3 · Cinematic Storyboard · Machine-ready</span>
<h1 class="rv">{H.escape(data['title_mk'])}</h1>
<p class="lede rv">{H.escape(data['genre'])} · {H.escape(data['logline'])}</p>
{meta}
<div class="shell" id="spec"><div class="core">
<div class="rail rv"><span class="dot" style="background:var(--gold);box-shadow:0 0 18px var(--gold)"></span><span class="n">Render contract</span><h2>Продукциски спецификации</h2></div>
{spec_section(data)}
<p class="note rv" style="margin-top:14px">Овој договор е вграден како <b>machine-readable JSON</b> во <code>&lt;script id="storyboard-spec"&gt;</code> — секој агент може да го преземе директно без повторно толкување.</p>
</div></div>
{legend}
<div class="shell" id="timeline"><div class="core">
<div class="rail rv"><span class="dot" style="background:var(--gold);box-shadow:0 0 18px var(--gold)"></span><span class="n">Master timeline</span><h2>Пат на приказната</h2></div>
{timeline(data)}</div></div>
{acts_html}
<div class="shell" id="blocking"><div class="core">
<div class="rail rv"><span class="dot" style="background:var(--gold);box-shadow:0 0 18px var(--gold)"></span><span class="n">Blocking map</span><h2>Топ-поглед · камера &amp; ликови</h2></div>
{blocking_map(data)}</div></div>
<div class="shell"><div class="core"><div class="rail rv"><span class="dot" style="background:var(--gold);box-shadow:0 0 18px var(--gold)"></span><span class="n">Film strip</span><h2>Секвенца</h2></div>
{filmstrip(data)}</div></div>
<div class="shell"><div class="core"><div class="rail rv"><span class="dot" style="background:var(--gold)"></span><span class="n">Cast</span><h2>Кастинг</h2></div><div class="g">{cast_table(data)}</div></div></div>
<div style="height:1px;background:linear-gradient(90deg,transparent,var(--hair),transparent);margin:44px 0"></div>
<p class="note rv" style="text-align:center;margin:0 auto">Доказен шаблон (proof exemplar) · {nshots} кадри / {len(data['acts'])} чина · може да се прошири до {spec.get('shot_floor',40)}–{spec.get('shot_max',60)} кадри според доктрината.</p>
</div>
<script type="application/json" id="storyboard-spec">{H.escape(payload_json, quote=False)}</script>
<script>const io=new IntersectionObserver((es)=>{{es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.06}});document.querySelectorAll('.rv').forEach(el=>io.observe(el));</script>
</body></html>"""

if __name__ == "__main__":
    import sys
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    pathlib.Path(out).write_text(build(data), encoding="utf-8")
    print(f"wrote {out}")
