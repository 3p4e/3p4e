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

def _hx(c, default="#3a4a5a"):
    c = (c or "").strip()
    return c if (len(c) == 7 and c.startswith("#")) else default

def _scene_svg(sh, act):
    """Design-driven cinematic shot frame. Characters are rendered from the story's
    character_designs map (archetype silhouette, costume, props, enchantment FX);
    environment refs render as background motifs. Fallback = upgraded generic."""
    import hashlib as _hl
    pal = act.get("palette") or ["#3d5a73", "#7a6a55", "#1c2833"]
    sky1 = _hx(pal[0] if len(pal) > 0 else None, "#3d5a73")
    acc  = _hx(pal[1] if len(pal) > 1 else None, "#7a6a55")
    gnd  = _hx(pal[2] if len(pal) > 2 else None, "#1c2833")
    tod  = (act.get("time_of_day") or "day").lower()
    sid  = sh.get("id", "") or "s"
    seed = int(_hl.md5(sid.encode()).hexdigest()[:6], 16)
    rnd  = lambda n: (seed >> (n % 20)) & 7
    DESIGN = globals().get("_DESIGNS") or {}

    # ---- classify refs
    refs = sh.get("asset_refs") or []
    def is_env(r):   return "_env_" in r or "env_" in r
    def is_prop(r):  return any(k in r.lower() for k in ("_sheet", "weapon", "prop")) and not is_env(r)
    def is_char(r):  return not is_env(r) and not is_prop(r)
    env_refs   = [r for r in refs if is_env(r)]
    prop_refs  = [r for r in refs if is_prop(r)]
    char_refs  = [r for r in refs if is_char(r)]
    boss_refs  = [r for r in char_refs if any(k in r.lower() for k in ("boss", "dragon", "monster", "wolf", "serpent", "hydra", "chimera", "yaga", "fenrir"))]
    hero_refs  = [r for r in char_refs if r not in boss_refs]

    def design_for(ref):
        if ref in DESIGN: return DESIGN[ref]
        parts = ref.split("_")
        for i in range(len(parts), 0, -1):
            k = "_".join(parts[:i])
            if k in DESIGN: return DESIGN[k]
        return None

    # ---- sky
    if tod == "night":
        sky_top, body = "#0a0d1f", 'moon'
        stars = ''.join(f'<circle cx="{(x*37+seed)%160}" cy="{(y*13+seed)%34+4}" r="0.7" fill="#ffffff" opacity="0.55"/>'
                        for x, y in [(1,1),(2,2),(3,1),(4,3),(5,1),(6,2),(7,1),(8,3),(9,2),(10,1),(11,2),(12,1)])
    elif tod == "dusk":   sky_top, body, stars = "#2a1a2e", 'sun-low', ''
    elif tod == "dawn":   sky_top, body, stars = "#33222a", 'sun-low', ''
    else:                 sky_top, body, stars = "#1a2438", 'sun', ''
    glow = {'sun': ('#f4d488', 18, 0.85), 'sun-low': ('#ff9a5a', 30, 0.9), 'moon': ('#e8e4da', 20, 0.8)}[body]
    body_svg = (f'<circle cx="128" cy="{glow[1]}" r="11" fill="{glow[0]}" opacity="0.28"/>'
                f'<circle cx="128" cy="{glow[1]}" r="8" fill="{glow[0]}" opacity="{glow[2]}"/>')
    if body == 'moon':
        body_svg += f'<circle cx="125" cy="{glow[1]-3}" r="6.6" fill="{sky_top}" opacity="0.85"/>'
    rays = ''
    if body == 'sun-low':
        rays = (f'<path d="M128 {glow[1]} L60 100 L86 100 Z" fill="#ffcf8a" opacity="0.07"/>'
                f'<path d="M128 {glow[1]} L100 100 L130 100 Z" fill="#ffcf8a" opacity="0.09"/>'
                f'<path d="M128 {glow[1]} L142 100 L160 100 Z" fill="#ffcf8a" opacity="0.06"/>')

    # ---- environment motif layer (from env ref design or keyword)
    def env_motif(ref):
        d = design_for(ref) or {}
        m = (d.get("motif") or ref.lower())
        tone = d.get("tone") or sky1
        if any(k in m for k in ("ocean", "wave", "sea")):
            return (''.join(f'<path d="M{xx} 62 q6 -4 12 0 q6 4 12 0" stroke="{tone}" stroke-width="1.4" fill="none" opacity="0.5"/>'
                            for xx in range(-4, 160, 24)))
        if any(k in m for k in ("hall", "column", "temple", "palace")):
            cols = ''.join(f'<rect x="{18+i*34}" y="34" width="7" height="40" fill="{tone}" opacity="0.45"/>' for i in range(4))
            return f'<rect x="8" y="28" width="144" height="7" fill="{tone}" opacity="0.5"/>{cols}'
        if any(k in m for k in ("forest", "wood")):
            return ''.join(f'<path d="M{xx} 74 L{xx+6} 52 L{xx+12} 74 Z" fill="{tone}" opacity="0.5"/>' for xx in range(6, 160, 22))
        if any(k in m for k in ("gate", "door")):
            return (f'<rect x="60" y="30" width="9" height="46" fill="{tone}" opacity="0.55"/>'
                    f'<rect x="91" y="30" width="9" height="46" fill="{tone}" opacity="0.55"/>'
                    f'<rect x="52" y="24" width="56" height="8" fill="{tone}" opacity="0.6"/>'
                    f'<rect x="70" y="36" width="20" height="40" fill="{acc}" opacity="0.25"/>')
        if any(k in m for k in ("cavern", "underworld", "cave")):
            return (f'<path d="M0 76 Q20 30 44 44 Q64 20 88 40 Q116 22 138 46 Q150 34 160 60 L160 78 L0 78 Z" '
                    f'fill="#050508" opacity="0.7"/>')
        if any(k in m for k in ("spires", "city", "castle", "tower", "asgard", "mountain", "peak", "olympus")):
            return ''.join(f'<path d="M{xx} 76 L{xx+8} {44+(xx%3)*6} L{xx+16} 76 Z" fill="{tone}" opacity="0.45"/>'
                           for xx in range(10, 150, 30))
        return ''.join(f'<path d="M{xx} 76 L{xx+10} {50+(xx%4)*5} L{xx+20} 76 Z" fill="{tone}" opacity="0.4"/>'
                       for xx in range(14, 150, 34))
    env_svg = env_motif(env_refs[0]) if env_refs else ''

    # ---- parallax ridges + ground
    def ridge(base, amp, col, op, step=26):
        pts = [f'L{x} {base + ((rnd(x//step) % 5) - 2)*amp}' for x in range(step, 161, step)]
        return (f'<path d="M0 {base + ((rnd(0) % 5) - 2)*amp} ' + ' '.join(pts) +
                f' L160 {base+8} L160 100 L0 100 Z" fill="{col}" opacity="{op}"/>')
    ridge_far, ridge_mid = ridge(56, 2.2, sky1, "0.38", 32), ridge(66, 2.8, acc, "0.30", 24)
    haze = f'<rect x="0" y="58" width="160" height="22" fill="{sky1}" opacity="0.10"/>'
    ground = f'<path d="M0 78 L26 74 L52 79 L84 73 L116 78 L140 74 L160 78 L160 100 L0 100 Z" fill="{gnd}" opacity="0.95"/>'
    grit = ''.join(f'<circle cx="{(seed*7+i*23)%160}" cy="{82+(i*11)%16}" r="0.5" fill="#ffffff" opacity="0.05"/>' for i in range(10))

    # ---- enchantment FX layers (behind figure)
    def fx_layers(x, y, h, fx, glow_col):
        out = []
        if any(k in fx for k in ("holy_aura", "golden_glow", "divine_glow")):
            out.append(f'<circle cx="{x}" cy="{y-h*0.5}" r="{h*0.75}" fill="{glow_col}" opacity="0.16"/>'
                       f'<circle cx="{x}" cy="{y-h*0.5}" r="{h*0.5}" fill="{glow_col}" opacity="0.14"/>')
        if "storm_aura" in fx:
            out.append(f'<path d="M{x-h*0.7} {y-h*0.7} q{h*0.3} -6 {h*0.7} 0 M{x-h*0.5} {y-h*0.4} q{h*0.3} -6 {h*0.7} 0" '
                       f'stroke="{glow_col}" stroke-width="1" fill="none" opacity="0.6"/>')
        if "rune_ring" in fx:
            ticks = ''.join(f'<line x1="{x+h*0.62*__import__("math").cos(a)}" y1="{y-h*0.55+h*0.62*__import__("math").sin(a)}" '
                            f'x2="{x+h*0.68*__import__("math").cos(a)}" y2="{y-h*0.55+h*0.68*__import__("math").sin(a)}" stroke="{glow_col}" stroke-width="0.8"/>'
                            for a in [i*0.785 for i in range(8)])
            out.append(f'<circle cx="{x}" cy="{y-h*0.55}" r="{h*0.65}" fill="none" stroke="{glow_col}" '
                       f'stroke-width="1" stroke-dasharray="4 3" opacity="0.55"/>{ticks}')
        if "wings" in fx:
            out.append(f'<path d="M{x-h*0.2} {y-h*0.72} Q{x-h*1.1} {y-h*1.0} {x-h*0.9} {y-h*0.35} Q{x-h*0.5} {y-h*0.55} {x-h*0.2} {y-h*0.6} Z" '
                       f'fill="{glow_col}" opacity="0.4"/>'
                       f'<path d="M{x+h*0.2} {y-h*0.72} Q{x+h*1.1} {y-h*1.0} {x+h*0.9} {y-h*0.35} Q{x+h*0.5} {y-h*0.55} {x+h*0.2} {y-h*0.6} Z" '
                       f'fill="{glow_col}" opacity="0.4"/>')
        if "shadow_smoke" in fx:
            out.append(f'<circle cx="{x}" cy="{y-h*0.4}" r="{h*0.6}" fill="#0a0a12" opacity="0.4"/>'
                       f'<circle cx="{x+h*0.2}" cy="{y-h*0.6}" r="{h*0.4}" fill="#0a0a12" opacity="0.3"/>')
        if "ice_motes" in fx:
            out.append(''.join(f'<rect x="{x-h*0.6+i*h*0.3}" y="{y-h*0.9+(i%3)*h*0.22}" width="1.6" height="1.6" '
                               f'transform="rotate(45 {x-h*0.6+i*h*0.3} {y-h*0.9+(i%3)*h*0.22})" fill="{glow_col}" opacity="0.8"/>' for i in range(5)))
        if "fire_wisps" in fx:
            out.append(''.join(f'<path d="M{xx} {y} q-2 -6 0 -9 q2 3 0 9 Z" fill="{glow_col}" opacity="0.75"/>'
                               for xx in (x-h*0.4, x+h*0.1, x+h*0.45)))
        if "lightning" in fx:
            out.append(f'<path d="M{x+h*0.5} {y-h} L{x+h*0.3} {y-h*0.65} L{x+h*0.55} {y-h*0.6} L{x+h*0.2} {y-h*0.25}" '
                       f'stroke="{glow_col}" stroke-width="1.2" fill="none" opacity="0.85"/>')
        if "petals" in fx:
            out.append(''.join(f'<ellipse cx="{x-h*0.5+i*h*0.28}" cy="{y-h*0.85+(i%4)*h*0.18}" rx="1.4" ry="0.8" '
                               f'fill="{glow_col}" opacity="0.6" transform="rotate({20+i*25} {x-h*0.5+i*h*0.28} {y-h*0.85+(i%4)*h*0.18})"/>' for i in range(4)))
        return ''.join(out)

    # ---- designed figure renderer
    def dfigure(x, y, h, d, flip=False):
        s = -1 if flip else 1
        p   = d.get("palette", {})
        col = p.get("primary") or acc
        col2= p.get("secondary") or "#5a6a72"
        gl  = p.get("glow") or "#ffd166"
        cos = d.get("costume", [])
        pr  = d.get("props", [])
        fx  = d.get("fx", [])
        arch= d.get("archetype", "warrior")
        build_t = d.get("build", "athletic")
        scale_m = {"human": 1.0, "large": 1.35, "huge": 1.75}.get(d.get("scale", "human"), 1.0)
        h *= scale_m
        hr = h * (0.16 if build_t == "hulking" else 0.19)
        hy = y - h + hr
        parts = [f'<ellipse cx="{x}" cy="{y+1.2}" rx="{h*0.36}" ry="{h*0.07}" fill="#000" opacity="0.35"/>']
        parts.append(fx_layers(x, y, h, fx, gl))
        # body per build
        if build_t == "robed":
            parts.append(f'<path d="M{x-h*0.22} {hy+hr} Q{x-h*0.5} {y-h*0.4} {x-h*0.42} {y} L{x+h*0.42} {y} Q{x+h*0.5} {y-h*0.4} {x+h*0.22} {hy+hr} Z" fill="{col}" opacity="0.92"/>'
                         f'<path d="M{x-h*0.30} {y-h*0.35} Q{x} {y-h*0.44} {x+h*0.30} {y-h*0.35}" stroke="{col2}" stroke-width="1.6" fill="none" opacity="0.8"/>')
        elif build_t == "hulking":
            parts.append(f'<path d="M{x-h*0.46} {hy+hr*1.2} L{x-h*0.40} {y} L{x+h*0.40} {y} L{x+h*0.46} {hy+hr*1.2} L{x+h*0.2} {hy} L{x-h*0.2} {hy} Z" fill="{col}" opacity="0.95"/>'
                         f'<path d="M{x-h*0.34} {y-h*0.4} L{x+h*0.34} {y-h*0.4}" stroke="{col2}" stroke-width="2" opacity="0.7"/>')
        elif build_t == "slender":
            parts.append(f'<path d="M{x-h*0.16} {hy+hr} L{x-h*0.26} {y} L{x+h*0.26} {y} L{x+h*0.16} {hy+hr} Z" fill="{col}" opacity="0.92"/>')
        else:  # athletic / armored
            parts.append(f'<path d="M{x-h*0.28} {hy+hr*1.3} L{x-h*0.36} {y} L{x+h*0.36} {y} L{x+h*0.28} {hy+hr*1.3} Z" fill="{col}" opacity="0.93"/>'
                         f'<path d="M{x-h*0.24} {y-h*0.42} L{x+h*0.24} {y-h*0.42}" stroke="{col2}" stroke-width="1.8" opacity="0.8"/>'
                         f'<path d="M{x-h*0.20} {y-h*0.28} L{x+h*0.20} {y-h*0.28}" stroke="{col2}" stroke-width="1.4" opacity="0.7"/>')
        # arms hint
        parts.append(f'<path d="M{x-h*0.30} {hy+hr*1.6} L{x-h*0.44} {y-h*0.28} M{x+h*0.30} {hy+hr*1.6} L{x+h*0.44} {y-h*0.28}" stroke="{col}" stroke-width="2.2" opacity="0.85"/>')
        # head + headgear
        parts.append(f'<circle cx="{x}" cy="{hy}" r="{hr}" fill="{col}"/>'
                     f'<path d="M{x-hr*0.7} {hy-hr*0.35} Q{x} {hy-hr*1.2} {x+hr*0.7} {hy-hr*0.35}" stroke="{gl}" stroke-width="0.9" fill="none" opacity="0.6"/>')
        if "crown" in cos or arch == "monarch":
            parts.append(f'<path d="M{x-hr*0.8} {hy-hr*0.8} L{x-hr*0.8} {hy-hr*1.5} L{x-hr*0.4} {hy-hr*1.1} L{x} {hy-hr*1.6} L{x+hr*0.4} {hy-hr*1.1} L{x+hr*0.8} {hy-hr*1.5} L{x+hr*0.8} {hy-hr*0.8} Z" fill="{gl}" opacity="0.95"/>')
        if "horned_helm" in cos:
            parts.append(f'<path d="M{x-hr*0.6} {hy-hr*0.7} Q{x-hr*1.7} {hy-hr*1.6} {x-hr*1.1} {hy-hr*0.2} M{x+hr*0.6} {hy-hr*0.7} Q{x+hr*1.7} {hy-hr*1.6} {x+hr*1.1} {hy-hr*0.2}" stroke="{col2}" stroke-width="1.8" fill="none"/>')
        if "hood" in cos:
            parts.append(f'<path d="M{x-hr*1.05} {hy+hr*0.5} Q{x} {hy-hr*2.0} {x+hr*1.05} {hy+hr*0.5} L{x+hr*0.7} {hy-hr*0.4} Q{x} {hy-hr*1.2} {x-hr*0.7} {hy-hr*0.4} Z" fill="{col2}" opacity="0.95"/>')
        if "beard" in cos:
            parts.append(f'<path d="M{x-hr*0.55} {hy+hr*0.3} Q{x} {hy+hr*1.6} {x+hr*0.55} {hy+hr*0.3} L{x+hr*0.4} {hy+hr*0.5} Q{x} {hy+hr*1.2} {x-hr*0.4} {hy+hr*0.5} Z" fill="#d8d2c4" opacity="0.9"/>')
        if "laurel" in cos:
            parts.append(f'<path d="M{x-hr*0.9} {hy-hr*0.5} Q{x} {hy-hr*1.25} {x+hr*0.9} {hy-hr*0.5}" stroke="{gl}" stroke-width="1.6" fill="none" stroke-dasharray="2 1.4"/>')
        # cloak
        if "cloak" in cos:
            parts.append(f'<path d="M{x-h*0.2} {hy+hr} Q{x-s*h*0.75} {y-h*0.45} {x-s*h*0.55} {y} L{x-h*0.30} {y} Q{x-h*0.36} {y-h*0.4} {x-h*0.2} {hy+hr} Z" fill="{col2}" opacity="0.75"/>')
        # props (right hand)
        handx, handy = x+s*h*0.44, y-h*0.28
        for pr in pr[:2]:
            if pr in ("spear", "gungnir"):
                parts.append(f'<path d="M{handx} {handy} L{handx+s*h*0.18} {handy-h*0.62}" stroke="#e8e4da" stroke-width="1.2"/>'
                             f'<path d="M{handx+s*h*0.18} {handy-h*0.62} L{handx+s*h*0.12} {handy-h*0.5} L{handx+s*h*0.24} {handy-h*0.5} Z" fill="{gl}"/>')
            elif pr in ("sword", "blade", "greatsword"):
                parts.append(f'<path d="M{handx} {handy} L{handx+s*h*0.30} {handy-h*0.42}" stroke="#e8e4da" stroke-width="1.6"/>'
                             f'<path d="M{handx+s*h*0.30} {handy-h*0.42} L{handx+s*h*0.22} {handy-h*0.34} M{handx+s*h*0.30} {handy-h*0.42} L{handx+s*h*0.36} {handy-h*0.33}" stroke="{gl}" stroke-width="1"/>')
            elif pr in ("staff", "wand"):
                parts.append(f'<path d="M{handx} {handy} L{handx+s*h*0.12} {handy-h*0.7}" stroke="#8a6a4a" stroke-width="1.4"/>'
                             f'<circle cx="{handx+s*h*0.12}" cy="{handy-h*0.7}" r="2" fill="{gl}"/>'
                             f'<circle cx="{handx+s*h*0.12}" cy="{handy-h*0.7}" r="3.6" fill="none" stroke="{gl}" opacity="0.4"/>')
            elif pr in ("bow",):
                parts.append(f'<path d="M{handx} {handy-h*0.34} Q{handx+s*h*0.42} {handy-h*0.17} {handx} {handy}" stroke="#a8895a" stroke-width="1.3" fill="none"/>'
                             f'<path d="M{handx} {handy-h*0.34} L{handx} {handy}" stroke="#e8e4da" stroke-width="0.7"/>')
            elif pr in ("crossbow",):
                parts.append(f'<path d="M{handx} {handy-h*0.2} L{handx+s*h*0.34} {handy-h*0.2}" stroke="#6a6a72" stroke-width="1.6"/>'
                             f'<path d="M{handx+s*h*0.34} {handy-h*0.2} L{handx+s*h*0.26} {handy-h*0.3} M{handx+s*h*0.34} {handy-h*0.2} L{handx+s*h*0.26} {handy-h*0.1}" stroke="{gl}" stroke-width="1"/>')
            elif pr in ("hammer", "mjolnir"):
                parts.append(f'<path d="M{handx} {handy} L{handx+s*h*0.16} {handy-h*0.4}" stroke="#8a6a4a" stroke-width="1.4"/>'
                             f'<rect x="{handx+s*h*0.16-3}" y="{handy-h*0.4-4}" width="7" height="6" fill="{col2}"/>')
            elif pr in ("shield",):
                parts.append(f'<path d="M{x-s*h*0.4} {y-h*0.5} L{x-s*h*0.52} {y-h*0.5} L{x-s*h*0.52} {y-h*0.2} Q{x-s*h*0.46} {y-h*0.1} {x-s*h*0.4} {y-h*0.2} Z" fill="{col2}" stroke="{gl}" stroke-width="0.8"/>')
            elif pr in ("lyre", "harp"):
                parts.append(f'<path d="M{handx} {handy} q{h*0.2} -{h*0.3} 0 -{h*0.42} q-{h*0.2} {h*0.12} 0 {h*0.42}" stroke="{gl}" stroke-width="1.2" fill="none"/>')
        return ''.join(parts)

    def gfigure(x, y, h, col, boss=False, flip=False):
        s = -1 if flip else 1
        hr = h*0.20
        hy = y-h+hr
        parts = [f'<ellipse cx="{x}" cy="{y+1.2}" rx="{h*0.34}" ry="{h*0.07}" fill="#000" opacity="0.35"/>']
        if boss:
            parts.append(f'<path d="M{x-h*0.5} {y} L{x-h*0.62} {y-h*0.55} L{x-h*0.28} {y-h*0.75} L{x-h*0.34} {y-h} L{x} {y-h*0.88} L{x+h*0.34} {y-h} L{x+h*0.28} {y-h*0.75} L{x+h*0.62} {y-h*0.55} L{x+h*0.5} {y} Z" fill="{col}" opacity="0.95"/>'
                         f'<circle cx="{x-h*0.2}" cy="{y-h*0.8}" r="1.1" fill="#ff5533"/><circle cx="{x+h*0.2}" cy="{y-h*0.8}" r="1.1" fill="#ff5533"/>'
                         f'<circle cx="{x}" cy="{y-h*0.5}" r="{h*0.1}" fill="#ff7a3c" opacity="0.8"/>')
        else:
            parts.append(f'<path d="M{x-h*0.30} {hy+hr*1.4} Q{x} {hy-h*0.06} {x+h*0.30} {hy+hr*1.4} L{x+h*0.40} {y} L{x-h*0.40} {y} Z" fill="{col}" opacity="0.9"/>'
                         f'<circle cx="{x}" cy="{hy}" r="{hr}" fill="{col}"/>')
        return ''.join(parts)

    # ---- figure layout by shot scale
    st = (sh.get("shot_type") or sh.get("size") or "WIDE").upper()
    gy = 80
    figs = []
    def render_ref(ref, x, h, hero, flip):
        d = design_for(ref)
        if d: return dfigure(x, gy, h, d, flip)
        if ref in boss_refs: return gfigure(x, gy, h, "#40282a", boss=True, flip=flip)
        return gfigure(x, gy, h, acc if hero else "#5a6a72", flip=flip)

    if not hero_refs and boss_refs:
        figs.append(render_ref(boss_refs[0], 80, 54, True, False))
    elif st.startswith("CLOSE") or st in ("INSERT", "MACRO"):
        figs.append(render_ref(hero_refs[0], 80, 58, True, False) if hero_refs else gfigure(80, gy, 58, acc))
        if boss_refs: figs.append(render_ref(boss_refs[0], 128, 34, False, True))
    elif st.startswith("MEDIUM"):
        n = max(1, min(2, len(hero_refs)) or 1)
        xs = [62, 98] if n > 1 else [80]
        for i, x in enumerate(xs):
            ref = hero_refs[i] if i < len(hero_refs) else None
            figs.append(render_ref(ref, x, 42, i == 0, i == 1) if ref else gfigure(x, gy, 42, acc if i == 0 else "#5a6a72"))
        if boss_refs: figs.append(render_ref(boss_refs[0], 132, 30, False, False))
    else:
        n = max(1, min(3, len(hero_refs)) or 1)
        xs = {1: [70], 2: [54, 96], 3: [40, 76, 112]}[n]
        for i, x in enumerate(xs):
            ref = hero_refs[i] if i < len(hero_refs) else None
            figs.append(render_ref(ref, x, 26, i == 0, i > 0) if ref else gfigure(x, gy, 26, acc if i == 0 else "#5a6a72"))
        if boss_refs: figs.append(render_ref(boss_refs[0], 138, 40, False, False))
    figs_s = ''.join(figs)

    # ---- floating prop sheet refs (drawn as a glowing insert chip)
    prop_chip = ''
    if prop_refs and not any(design_for(r) for r in prop_refs):
        prop_chip = (f'<g opacity="0.85"><rect x="112" y="10" width="42" height="12" rx="2" fill="#0a0a10" stroke="#ffd16655"/>'
                     f'<text x="133" y="18.5" text-anchor="middle" font-size="6.4" fill="#ffd166" font-family="monospace">{H.escape(prop_refs[0][:12].upper())}</text></g>')

    # ---- camera move + streaks + screen dir + vignette (unchanged grammar)
    mv = (sh.get("move") or "static").lower()
    gold = "#ffd166"
    streaks = {
        "push-in":    '<path d="M14 86 L48 62 M20 90 L52 66" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
        "pull-back":  '<path d="M48 62 L14 86 M52 66 L20 90" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
        "pan-left":   '<path d="M118 84 L44 84 M118 88 L52 88" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
        "pan-right":  '<path d="M42 84 L116 84 M48 88 L116 88" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
        "track":      '<path d="M22 92 L58 68 M26 94 L62 70" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
        "crane-up":   '<path d="M22 88 L22 38 M27 88 L27 42" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
        "crane-down": '<path d="M22 38 L22 88 M27 42 L27 88" stroke="#ffd166" stroke-width="1" opacity="0.3"/>',
    }.get(mv, '')
    cam = {
        "push-in":    f'<path d="M12 88 L52 60" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "pull-back":  f'<path d="M52 60 L12 88" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "pan-left":   f'<path d="M120 88 L40 88" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "pan-right":  f'<path d="M40 88 L120 88" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "track":      f'<path d="M20 90 L60 66 L110 66" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "crane-up":   f'<path d="M20 88 L20 34" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "crane-down": f'<path d="M20 34 L20 88" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
        "shot-reverse": f'<path d="M30 88 L60 70" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>'
                          f'<path d="M130 88 L100 70" stroke="{gold}" stroke-width="2.2" fill="none" marker-end="url(#ah{sid})"/>',
    }.get(mv, f'<circle cx="20" cy="88" r="3" fill="none" stroke="{gold}" stroke-width="1.4"/>'
              f'<path d="M16 88 L24 88 M20 84 L20 92" stroke="{gold}" stroke-width="1.2"/>')
    sd = (sh.get("screen_dir") or "").lower()
    sd_svg = ('<text x="150" y="94" text-anchor="end" font-size="8" fill="#8fd3c7" font-family="monospace">L→R</text>'
              if "l-to-r" in sd or "left" in sd else
              '<text x="150" y="94" text-anchor="end" font-size="8" fill="#8fd3c7" font-family="monospace">R→L</text>'
              if "r-to-l" in sd or "right" in sd else '')
    vignette = ('<radialGradient id="vg%s" cx="0.5" cy="0.5" r="0.72">'
                '<stop offset="0.6" stop-color="#000" stop-opacity="0"/>'
                '<stop offset="1" stop-color="#000" stop-opacity="0.45"/></radialGradient>'
                '<rect width="160" height="100" fill="url(#vg%s)"/>') % (sid, sid)
    letterbox = '<rect x="0" y="0" width="160" height="4" fill="#050505"/><rect x="0" y="96" width="160" height="4" fill="#050505"/>'

    return (f'<defs>'
            f'<linearGradient id="sky{sid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{sky_top}"/>'
            f'<stop offset="0.55" stop-color="{sky1}" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="#0a0a10"/></linearGradient>'
            f'<marker id="ah{sid}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">'
            f'<path d="M0 0 L6 3 L0 6 Z" fill="#ffd166"/></marker></defs>'
            f'<rect width="160" height="100" fill="url(#sky{sid})"/>'
            f'{stars}{body_svg}{rays}'
            f'{env_svg}'
            f'{ridge_far}{haze}{ridge_mid}'
            f'{ground}{grit}'
            f'{figs_s}{prop_chip}{streaks}{cam}{sd_svg}'
            f'{vignette}{letterbox}'
            f'<path d="M53 0 L53 100 M106 0 L106 100 M0 33 L160 33 M0 66 L160 66" stroke="#ffffff0a"/>'
            f'<rect x="1" y="5" width="158" height="90" fill="none" stroke="#ffffff22" rx="3"/>'
            f'<text x="6" y="13" font-size="8" fill="#e8e4da" opacity="0.9" font-family="monospace" font-weight="bold">{H.escape(sid)}</text>'
            f'<text x="6" y="93" font-size="7" fill="#e8e4da" opacity="0.6" font-family="monospace">{H.escape(st)}</text>')

def _placeholder(sh):
    # legacy single-arg shim (act context unavailable) -> minimal sky frame
    return _scene_svg(sh, {"palette": ["#3d5a73", "#7a6a55", "#1c2833"], "time_of_day": "day"})


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
            span=sh.get("span","sp4"), sid=sh["id"], scene=sh.get("scene") or _scene_svg(sh, act),
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
            micro = sh.get("scene_micro") or f'<svg viewBox="0 0 160 100">{sh.get("scene") or _scene_svg(sh, a)}</svg>'
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
        "acts": [dict({k:a[k] for k in ("id","num","title","color","synopsis")},
                     **{k:a[k] for k in ("location_ref","global_locks","palette","light_direction","time_of_day") if k in a},
                     shots=[clean_shot(s) for s in a["shots"]]) for a in data["acts"]],
    }

def build(data):
    global _DESIGNS
    _DESIGNS = data.get("character_designs") or {}
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
