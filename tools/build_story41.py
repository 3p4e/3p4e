#!/usr/bin/env python3
"""Story 41 — Ловецот и Паладинот: Господарот на Пепелта — machine-ready storyboard data."""
import sys, pathlib, importlib.util

GP = pathlib.Path('/a0/usr/projects/vast/tools/build_storyboard_html.py')
spec = importlib.util.spec_from_file_location('build_sb', GP)
sb = importlib.util.module_from_spec(spec); spec.loader.exec_module(sb)

# --- color language (story canon) ---
ICE  = '#38c8e8'   # Hunter: blue-turquoise ice
GOLD = '#f5c518'   # Paladin: white-gold light
EMBER= '#ef4444'   # Boss: ember / ash / fire

def fig(x,y,s,c):
    return f'<g fill="{c}"><circle cx="{x}" cy="{y}" r="{5*s}"/><rect x="{x-4*s}" y="{y+5*s}" width="{8*s}" height="{14*s}" rx="{3*s}"/></g>'

def crossbow(x,y):
    return f'<path d="M{x} {y} q12 -4 {x+22} {y-2} M{x+6} {y} l{x+16} {y+4}" stroke="{ICE}" stroke-width="1.4" fill="none"/>'

def greatsword(x1,y1,x2,y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GOLD}" stroke-width="2"/><rect x="{x1-1}" y="{y1+1}" width="4" height="3" fill="{GOLD}"/>'

def boss(x,y,s):
    # horned ash shadow with fire core
    return (f'<g fill="{EMBER}"><path d="M{x-7*s} {y} Q{x-11*s} {y-9*s} {x-4*s} {y-12*s} Q{x-2*s} {y-6*s} {x} {y}" opacity=".85"/>'
            f'<path d="M{x+7*s} {y} Q{x+11*s} {y-9*s} {x+4*s} {y-12*s} Q{x+2*s} {y-6*s} {x} {y}" opacity=".85"/>'
            f'<rect x="{x-5*s}" y="{y}" width="{10*s}" height="{16*s}" rx="{4*s}"/>'
            f'<circle cx="{x}" cy="{y+6*s}" r="{3.4*s}" fill="#ff9d3c"/></g>')

def whip():
    return f'<path d="M0 30 Q50 60 90 78 T160 60" fill="none" stroke="{EMBER}" stroke-width="2.4" opacity=".9"/>'

# ================= SHOTS =================
shots = [
 # ---------------- ACT I — ЗАЛОЖБА ----------------
 dict(id='S01',size='WIDE',angle='high-angle',move='crane-down',dur=4.5,clip_s=5.0,
   narration_mk='Во една изгорена клисура, каде ветрот носеше жар наместо песок, на сртот од карпата застанаа двајца.',dialogue_mk='',
   kf_first='Epic aerial establishing shot of a vast scorched canyon at dusk, windblown embers instead of sand, jagged black rock ridges, smoke pillars, photoreal Diablo2/WoW cinematic grade',
   kf_last='Camera cranes down to a high ridge where two silhouetted figures stand side by side, ember storm swirling around them',
   continuity='NONE (opening master); establish ember-red palette',
   motion='slow crane-down; embers drift past lens',
   scene=f'<g class="m-crane"><rect width="160" height="100" fill="#160d0a"/><path d="M0 70 L30 46 L52 64 L84 38 L118 62 L160 44 L160 100 L0 100Z" fill="#241410"/><circle cx="130" cy="20" r="9" fill="#ff9d3c" opacity=".5"/>{fig(64,62,1,ICE)}{fig(96,62,1,GOLD)}</g>'),

 dict(id='S02',size='MEDIUM',angle='eye-level',move='track',dur=4.0,clip_s=5.0,
   narration_mk='Првиот — ловецот, со две пеколни самострели и влакна што лебдеа во сино-тиркизно како под вода.',dialogue_mk='',
   kf_first='Medium shot of the HUNTER: lean warrior with two dark infernal crossbows, long hair glowing blue-turquoise and floating weightlessly as if underwater, embers behind him',
   kf_last='Tracking shot settles on his glowing eyes and the twin crossbows in his hands; hair ripples',
   continuity='Hunter identity LOCK: blue-turquoise floating hair, twin crossbows (carry through all shots)',
   motion='lateral track; hair floats with current; crossbows glint',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#0d1316"/>{crossbow(38,50)}{crossbow(116,50)}{fig(80,60,1,ICE)}<path d="M66 40 Q74 30 82 40 Q90 30 98 40" stroke="{ICE}" stroke-width="1.6" fill="none"/></g>'),

 dict(id='S03',size='MEDIUM',angle='low-angle',move='push-in',dur=4.0,clip_s=5.0,
   narration_mk='Вториот — паладинот, ќелав и облеан во златен вез, со лавиринт од руни што тлееше како жар врз кожата.',dialogue_mk='',
   kf_first='Low-angle medium of the PALADIN: bald, ornate golden embroidery on armor, one-sided labyrinth of glowing runes carved over face, neck and body, faint ember-light pulsing under the skin',
   kf_last='Push-in to the rune maze on his face flaring faintly white-gold',
   continuity='Paladin identity LOCK: bald, golden embroidery, face/neck rune labyrinth (carry through all shots)',
   motion='push-in; runes pulse; ember underlight flickers',
   scene=f'<g class="m-push"><rect width="160" height="100" fill="#120f09"/>{fig(80,58,1.1,GOLD)}<path d="M64 44 L78 40 L92 44 L78 50 Z" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity=".9"/><path d="M62 48 L80 44 L96 48" fill="none" stroke="{GOLD}" stroke-width="1" opacity=".7"/><circle cx="78" cy="46" r="1.4" fill="#fff"/></g>'),

 dict(id='S04',size='WIDE',angle='low-angle',move='crane-up',dur=4.5,clip_s=5.0,
   narration_mk='Од пепелта под нив се надигна Мал’гарот, Господарот на Пепелта: висока роговидна сенка завиткана во пепел.',dialogue_mk='',
   kf_first='Low-angle wide as the ash below erupts: Master of Ash MULGAROTH rises — tall horned shadow wrapped in swirling ash, half-liquid fire core burning in its chest, crown of dead embers',
   kf_last='Crane up revealing the giant boss towering over the two small figures on the ridge, ember lightning in the air',
   continuity='Boss identity LOCK: horned ash form, chest fire-core, dead-ember crown (carry through all shots)',
   motion='crane-up; ash plume billows upward; core churns',
   scene=f'<g class="m-crane"><rect width="160" height="100" fill="#170b06"/><path d="M0 86 L40 58 L80 70 L120 50 L160 64 L160 100 L0 100Z" fill="#241008"/>{boss(80,32,4.4)}{fig(58,64,.6,ICE)}{fig(102,64,.6,GOLD)}</g>'),

 dict(id='S05',size='INSERT',angle='macro',move='push-in',dur=3.0,clip_s=5.0,
   narration_mk='Една стопена рака-камшик и круна од мртви јаглени — сè што ќе допреше, издивуваше во чад.',dialogue_mk='',
   kf_first='Macro insert on a single melted whip-arm of dripping ember, smoke rising where it trails, slow liquid fire drips',
   kf_last='Push-in to the twisted crown of dead charcoals on its head, faint coals dying and reigniting',
   continuity='Boss whip-arm + charcoal crown introduced (key boss props)',
   motion='micro push-in; whip drips molten ember; smoke curls',
   scene=f'<g class="m-push"><rect width="160" height="100" fill="#140a04"/>{whip()}<path d="M110 14 L124 22 L128 12 L140 26 L148 16" fill="none" stroke="#3a1f10" stroke-width="3"/><circle cx="126" cy="20" r="2.4" fill="#ff9d3c"/></g>'),

 dict(id='S06',size='MEDIUM',angle='low-angle',move='push-in',dur=4.5,clip_s=5.0,
   narration_mk='',dialogue_mk='Мал’гарот: „Дојдовте да изгорите, како сите пред вас.“ — и камшикот од жар пукна низ воздухот.',
   kf_first='Low-angle medium of MULGAROTH speaking, fire core flaring, ember whip arcing through the air toward camera',
   kf_last='Push-in on its molten face as the whip cracks with a burst of sparks',
   continuity='Same boss; whip from S05 now in motion',
   motion='push-in; whip crack; sparks fly',
   scene=f'<g class="m-push"><rect width="160" height="100" fill="#150a04"/>{boss(80,44,3.2)}{whip()}</g>'),

 # ---------------- ACT II — ПРЕСМЕТКА ----------------
 dict(id='S07',size='WIDE',angle='eye-level',move='track',dur=4.0,clip_s=5.0,
   narration_mk='Ловецот крена рака и околу него разцвета прстен од мраз и тајни знаци — неговиот Леден ореол.',dialogue_mk='',
   kf_first='Wide shot: the Hunter raises one hand, a ring of frost and arcane symbols blooms around him, embers nearby flash-frozen into snow',
   kf_last='The Glacial Aura expands outward, freezing cinders mid-air into glittering snow',
   continuity='Hunter; introduc Glacial Aura ring — recurring ability',
   motion='track + halo expands; embers→snow transformation',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#0b1519"/>{fig(80,62,1,ICE)}<circle cx="80" cy="54" r="22" fill="none" stroke="{ICE}" stroke-width="1.6" opacity=".9"/><circle cx="80" cy="54" r="30" fill="none" stroke="#7fd8f0" stroke-width=".8" opacity=".5"/></g>'),

 dict(id='S08',size='WIDE',angle='low-angle',move='track',dur=4.0,clip_s=5.0,
   narration_mk='Се одби од земјата како комета од слана, а зад него остануваше смрзната трага.',dialogue_mk='',
   kf_first='The Hunter launches from the ground like a frost comet, a trail of ice crystal forming in the air behind his arc',
   kf_last='He soars over the boss, leaving a frozen ribbon of ice curling in his wake',
   continuity='Hunter with Glacial Aura active; frozen trail is new visual (ice vs ember contrast)',
   motion='fast tracking launch; ice ribbon trails; ember recoils',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#0a1417"/>{boss(82,48,3)}{fig(44,32,.8,ICE)}<path d="M20 64 Q50 30 96 30 Q128 30 150 46" fill="none" stroke="#7fd8f0" stroke-width="1.6" opacity=".8"/></g>'),

 dict(id='S09',size='INSERT',angle='macro',move='push-in',dur=3.5,clip_s=5.0,
   narration_mk='Неговите очи пламнаа и од нив искочија две мразни греди — бело-сини копја со виолетово јадро.',dialogue_mk='',
   kf_first='Macro on the Hunter\'s blazing eyes, two Rime Beams erupting — white-blue spears with a violet core, everything they touch flash-freezing instantly',
   kf_last='Push-in as a flame in frame freezes solid into an ice sculpture from the beam',
   continuity='Hunter Rime Beams (white-blue + violet core) — recurring attack',
   motion='micro push-in; beams flare; flame→ice sculpture',
   scene=f'<g class="m-push"><rect width="160" height="100" fill="#080e14"/><path d="M40 50 L130 50" stroke="#bcdcf0" stroke-width="2.6"/><path d="M40 56 L130 56" stroke="#c08bf5" stroke-width="1.4" opacity=".8"/><path d="M134 40 l6 10 l-10 4 l4 -6z" fill="#9fd8f0"/></g>'),

 dict(id='S10',size='MEDIUM',angle='low-angle',move='push-in',dur=4.0,clip_s=5.0,
   narration_mk='',dialogue_mk='Босот: „Мразот само ја прави пепелта поубава,“ — додека камшикот му се нишаше над двајцата.',
   kf_first='The boss taunts as its ember whip sways high above both heroes; its fire core glows with contempt',
   kf_last='Push-in on the boss\' coal-crown face, half-smile, ash curling off its jaw',
   continuity='Boss taunt beat; whip recurring across the fight',
   motion='push-in; whip sways; ash drifts from mouth',
   scene=f'<g class="m-push"><rect width="160" height="100" fill="#160a04"/>{boss(80,40,3.4)}{whip()}</g>'),

 dict(id='S11',size='WIDE',angle='low-angle',move='track',dur=4.0,clip_s=5.0,
   narration_mk='Паладинот го вкорени својот голем меч во земјата и златниот ударен бран го испука каменот.',dialogue_mk='',
   kf_first='Wide low-angle: the Paladin plants his greatsword into the ground, a golden shockwave splitting the stone outward in a radiating crack',
   kf_last='The gold blast slams into the boss, hurling ash aside as the shockwave pulses',
   continuity='Paladin; introduces Templar Verdict shockwave (gold); greatsword planted',
   motion='track with shockwave; stone cracks radiate; gold light blooms',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#100f0a"/>{greatsword(80,38,80,74)}{fig(80,64,1,GOLD)}<circle cx="80" cy="74" r="16" fill="none" stroke="{GOLD}" stroke-width="1.8" opacity=".9"/>{boss(124,46,2.6)}</g>'),

 dict(id='S12',size='INSERT',angle='macro',move='push-in',dur=3.5,clip_s=5.0,
   narration_mk='Златниот ударен бран... а руните по телото му пламнаа од тивко злато во бел оган, за секој удар посебно.',dialogue_mk='',
   kf_first='Macro on the Paladin\'s skin: the rune labyrinth flare from quiet gold into white fire, traveling along the carved paths for each strike',
   kf_last='The rune light reaches his eye and blade, both searing white-gold',
   continuity='Paladin runes (identity, S03) now actively flaring — power escalation',
   motion='micro push-in; runes crawl along skin; light intensifies',
   scene=f'<g class="m-push"><rect width="160" height="100" fill="#0e0c06"/><path d="M40 44 Q70 34 96 44 Q118 52 136 40" fill="none" stroke="{GOLD}" stroke-width="1.6"/><path d="M52 56 Q80 48 108 58" fill="none" stroke="#fff6d8" stroke-width="1.2"/><circle cx="118" cy="48" r="2.2" fill="#fff"/></g>'),

 dict(id='S13',size='WIDE',angle='eye-level',move='track',dur=4.5,clip_s=5.0,
   narration_mk='Првата заедничка техника — Замрзни-и-Скрши: мразот и светлината заедно.',dialogue_mk='',
   kf_first='Wide shot of the FIRST combined technique Freeze-and-Sunder: the Hunter\'s Rime Beams freeze the whip-arm mid-swing, then the Paladin\'s Verdict blast shatters it',
   kf_last='The frozen arm shatters into a million golden-lit ice shards raining down; boss reels back',
   continuity='Tags S09 (Rime Beams) + S11 (Judgement); whip-arm destroyed here',
   motion='track through the shatter; ice shards + gold blast; boss recoil',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#0a0f14"/>{fig(44,58,.9,ICE)}{fig(116,58,.9,GOLD)}{boss(80,38,3)}<path d="M80 34 l-8 14 l-14 -4 l9 -10z" fill="#9fd8f0"/><path d="M80 34 l8 14 l14 -2 l-8 -12z" fill="{GOLD}"/></g>'),

 # ---------------- ACT III — РАЗРЕШУВАЊЕ ----------------
 dict(id='S14',size='WIDE',angle='high-angle',move='crane-down',dur=4.5,clip_s=5.0,
   narration_mk='Разбеснет, босот го фрли својот оклоп и го разголи огненото јадро. Почна црн дожд — жежок, од жар и стакло.',dialogue_mk='',
   kf_first='High-angle wide: the enraged boss sheds its ash armor, exposing the blazing fire core; a black rain of hot ember and glass begins to fall',
   kf_last='Crane down through the falling ember-glass rain toward the two heroes bracing below',
   continuity='Boss escalates (armor off, core exposed); BLACK RAIN is new hazard',
   motion='crane-down; black rain falls; core strobes',
   scene=f'<g class="m-crane"><rect width="160" height="100" fill="#120604"/>{boss(80,34,4)}'+''.join(f'<line x1="{x}" y1="0" x2="{x+6}" y2="{y}" stroke="#3a1c0c" stroke-width="1"/>' for x,y in [(20,30),(52,26),(94,32),(128,28),(40,38)])+f'</g>'),

 dict(id='S15',size='MEDIUM',angle='eye-level',move='track',dur=4.0,clip_s=5.0,
   narration_mk='Паладинот застана неподвижен под него, а светлината го соблекуваше дождот како вода.',dialogue_mk='',
   kf_first='The Paladin stands motionless under the black rain, his golden light shedding the ember-glass like water off a shield',
   kf_last='Tracking shot circles him; rain hisses into smoke on contact with his aura',
   continuity='Paladin aura (rune light) now a shield; black rain from S14',
   motion='slow circular track; rain evaporates to smoke on aura',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#0d0906"/>{fig(80,60,1,GOLD)}<circle cx="80" cy="56" r="26" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity=".7"/><line x1="60" y1="18" x2="64" y2="34" stroke="#3a1c0c"/><line x1="100" y1="14" x2="104" y2="30" stroke="#3a1c0c"/></g>'),

 dict(id='S16',size='WIDE',angle='low-angle',move='crane-up',dur=4.5,clip_s=5.0,
   narration_mk='',dialogue_mk='Босот: „Од пепел сте — и во пепел ќе ве вратам!“ — го крена Сонцето на пепелта, супернова од жар над клисурата.',
   kf_first='The boss roars and raises the SUN OF ASH — a supernova of ember rising above the canyon, red-orange light flooding everything',
   kf_last='Crane up as the ember sun grows, dwarfing both heroes, the canyon walls cracking from the heat',
   continuity='BOSS ULTIMATE: Sun of Ash (ember supernova); ultimate stakes',
   motion='crane-up; ember sun expands; heat shimmer; walls crack',
   scene=f'<g class="m-crane"><rect width="160" height="100" fill="#1a0702"/>{boss(80,30,3.6)}<circle cx="80" cy="30" r="20" fill="#ff9d3c" opacity=".75"/><circle cx="80" cy="30" r="30" fill="none" stroke="#ff9d3c" stroke-width="1.2" opacity=".6"/>{fig(52,64,.6,ICE)}{fig(108,64,.6,GOLD)}</g>'),

 dict(id='S17',size='WIDE',angle='low-angle',move='track',dur=4.5,clip_s=5.0,
   narration_mk='Ловецот ја прифати Ледената облика, а паладинот — Одмаздничкиот гнев. Мразна и златна лента, право кон срцето на суперновата.',dialogue_mk='',
   kf_first='Side-by-side low-angle: the Hunter\'s hair erupts in white light with a turquoise ring of signs (Glacier Form); the Paladin\'s runes blaze and transparent golden wings unfold (Avenging Wrath)',
   kf_last='They launch together — a ribbon of ice and a ribbon of gold intertwined, streaking toward the heart of the ember sun',
   continuity='Both ultimates (Glacier Form + Avenging Wrath); tag Sun of Ash from S16',
   motion='track toward sun; twin ribbons spiral; wind distortion',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#0e0602"/>{fig(52,58,1,ICE)}{fig(108,58,1,GOLD)}<path d="M52 58 Q80 34 80 16" fill="none" stroke="#7fd8f0" stroke-width="1.4"/><path d="M108 58 Q80 34 80 16" fill="none" stroke="{GOLD}" stroke-width="1.4"/><circle cx="80" cy="16" r="9" fill="#ff9d3c" opacity=".8"/></g>'),

 dict(id='S18',size='CLOSE',angle='eye-level',move='shot-reverse',dur=3.5,clip_s=5.0,
   narration_mk='',dialogue_mk='„Замрзни,“ рече ловецот. „Суди,“ рече паладинот.',
   kf_first='Close on the Hunter, white-hot eyes, speaking: FREEZE. Reverse close on the Paladin, runes searing, speaking: JUDGE.',
   kf_last='The two words land as the Rime Beam and the golden Verdict strike the fire core simultaneously',
   continuity='Shot/reverse of both heroes at the decisive instant',
   motion='shot/reverse cut; core impact flash',
   scene=f'<g class="m-panr"><rect width="160" height="100" fill="#0a0d12"/>{fig(56,58,1,ICE)}{fig(116,58,1,GOLD)}<path d="M56 50 L116 50" stroke="#ffffff" stroke-width="1.4" opacity=".9"/><circle cx="86" cy="50" r="8" fill="#fff" opacity=".9"/></g>'),

 dict(id='S19',size='WIDE',angle='high-angle',move='pull-back',dur=4.5,clip_s=5.0,
   narration_mk='Јадрото се распука. Светлината надојде од внатре и ја потопи жарта. Суперновата се соблече навнатре, а круната од мртви јаглени падна.',dialogue_mk='',
   kf_first='The fire core cracks open, pure light rising from within and drowning the ember; the ember supernova collapses inward',
   kf_last='Pull-back high-angle as the crown of dead charcoals cracks and falls; the light fades to ashen calm',
   continuity='Pays off S16 Sun of Ash; boss defeated (crown falls)',
   motion='pull-back; inward collapse; light floods then subsides',
   scene=f'<g class="m-crane"><rect width="160" height="100" fill="#0c0a10"/><circle cx="80" cy="46" r="18" fill="#fff" opacity=".5"/><circle cx="80" cy="46" r="26" fill="none" stroke="#c9c2d8" stroke-width="1" opacity=".5"/><path d="M70 30 L78 24 L88 30" fill="none" stroke="#3a1f10" stroke-width="2.4"/></g>'),

 dict(id='S20',size='WIDE',angle='eye-level',move='track',dur=5.0,clip_s=5.0,
   narration_mk='',dialogue_mk='Ловецот: „Пепелта е само снег што не стигнал на време.“ — првата зора прободе низ пепелта.',
   kf_first='The ash settles: two silhouettes stand over the extinguished core, the Hunter lowering his hood and exhaling a thin stream of frost, the Paladin slinging his sword over his shoulder',
   kf_last='The first dawn light pierces through the falling ash, warming the frame to soft gold',
   continuity='Grand closing; mirrors S01 (two figures on ridge) but now dawn instead of dusk',
   motion='gentle track; ash settles; dawn light breaks; frost breath curls',
   scene=f'<g class="m-track"><rect width="160" height="100" fill="#1b130c"/><path d="M0 70 L40 58 L80 66 L120 54 L160 62 L160 100 L0 100Z" fill="#241a12"/>{fig(62,64,1,ICE)}{fig(100,64,1,GOLD)}<path d="M58 56 q4 -6 8 0" stroke="{ICE}" stroke-width="1" fill="none"/><circle cx="136" cy="18" r="9" fill="#ffd9a0" opacity=".55"/></g>'),
]

acts = [
 dict(id='act1',num='Act I',title='Заложба · Доаѓањето',color=ICE,pct=30,
   synopsis='Во изгорена клисура се среќаваат Ловецот и Паладинот; од пепелта се крева Мал’гарот, Господарот на Пепелта, и им се потсмева.',
   shots=shots[:6]),
 dict(id='act2',num='Act II',title='Пресметка · Двете сили',color=GOLD,pct=44,
   synopsis='Ловецот го покажува Ледениот ореол и мразните греди; Паладинот задава со Златната пресуда; следи првата заедничка техника — Замрзни-и-Скрши.',
   shots=shots[6:13]),
 dict(id='act3',num='Act III',title='Разрешување · Сонцето на пепелта',color=EMBER,pct=26,
   synopsis='Босот го разголува јадрото и го крева Сонцето на пепелта; хероите ги будат своите ултимативни форми и заедно го гаснат јадрото; првата зора доаѓа.',
   shots=shots[13:]),
]

data = dict(
  title_mk='Ловецот и Паладинот: Господарот на Пепелта', title_en='The Hunter & the Paladin: Lord of Ash',
  genre='Оригинална приказна · епска борба со бос · dark fantasy',
  logline='Двојца — ловецот на мраз и паладинот на светлината — заедно го гаснат Господарот на Пепелта.',
  spec=dict(aspect='16:9', resolution='1280x720', fps=24, model='SkyReels-V3-identity',
    style='photoreal', flf=True, language='mk', shot_floor=40, shot_max=60,
    seed_policy='fixed-per-shot (same seed → reproducible shot; re-roll per shot id)',
    style_anchor=['Diablo 2 cinematic','World of Warcraft cinematic','StarCraft cinematic'],
    negative_prompt='cartoon, anime, illustration, low poly, blurry, extra fingers, distorted face, watermark, text, gore, blood spray, child-unfriendly'),
  cast=[
    dict(role='Ловецот / The Hunter', trait='Две пеколни самострели; сино-тиркизни влакна што лебдат; мраз-магија', source='faces/dd_cards_final (9 enrolled) · identity_index→dd', face_lock='DD (заклучување подоцна)'),
    dict(role='Паладинот / The Paladin', trait='Ќелав, златен вез; лавиринт од руни преку лице/врат/тело; светлосна магија', source='Blagoj-shaven 454a359e · IDENTITY.md/CHARACTER_SYSTEM.md', face_lock='Blagoj (заклучување подоцна)'),
    dict(role='Мал’гарот / Mal\'garot', trait='Господар на Пепелта; роговидна пепел сенка, огнено јадро, круна од мртви јаглени', source='story-suggested', face_lock='AI-default'),
  ],
  acts=acts,
)

out = '/a0/usr/projects/vast/storybook_ocr/storyboards/41_lovecot_paladin_gospodar_pepelta.html'
html = sb.build(data)
pathlib.Path(out).write_text(html, encoding='utf-8')

import re, json as J, html as _H
raw = pathlib.Path(out).read_bytes()
m = re.search(r'<script type="application/json" id="storyboard-spec">(.*?)</script>', html, re.S)
payload = J.loads(_H.unescape(m.group(1)))
ns = sum(len(a['shots']) for a in payload['acts'])
print('wrote', out)
print('bytes', len(raw), '| section-sign bytes', raw.count(b'\xc2\xa7'))
print('embedded JSON ok | shots', ns, '| kf_first present', sum(1 for a in payload['acts'] for s in a['shots'] if s.get('kf_first')))
print('total clip render', round(sum(s['clip_s'] for a in payload['acts'] for s in a['shots']),1),'s')
print('CLEAN:', raw.count(b'\xc2\xa7')==0)
