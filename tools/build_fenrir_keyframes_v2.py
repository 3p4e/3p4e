#!/usr/bin/env python3
"""Rebuild the Fenrir 46 START-keyframe Grok pack with DIRECTOR LOOK LOCKS baked in.

Every prompt now: (1) names the character once with the LOCKED director-look
constant (VOID-SEER Odin / INK OF CHAOS Loki / VOID MAW Fenrir / FINAL OATH Tyr /
HALF-GOD HALF-DEAD Hel), (2) attaches the canonical P1 card + identity anchor
(az/ol master sheet) per shot, (3) carries the story guards (Tyr right hand intact
pre-S40, empty sleeve S40+; Fenrir pup S04; no gore). Also mirrors each aligned
image_prompt_start back into the data JSON. Zero GPU; deterministic; no LLM.
"""
import json, pathlib, re

ROOT = pathlib.Path('/a0/usr/projects/vast')
DATA = ROOT/'storybook_ocr/data/13_fenrir_the_wolf_of_asgard_data.json'
PACK = ROOT/'storybook_ocr/specs/13_GROK_46_START_KEYFRAME_PROMPTS.md'

STYLE = ("Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, "
         "35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting.")
NEG = ("duplicate face, extra limbs, extra fingers, deformed hands, text, watermark, logo, "
       "cartoon, anime, illustration, cel-shaded, 3d render, plastic skin, gore, blood")
NEG_TYR_INTACT = NEG + ", missing hand, amputee, severed limb"

# ---- DIRECTOR LOOK LOCKS (2026-11-12) ------------------------------------
# One-sentence identity constants; stated once per prompt (39/43), never restated.
LOOK = {
 'odin': "Odin the All-Father, the dark seer-king of the VOID-SEER look - iron-grey hair and beard in neat braids, his left eye covered by a plain dark eyepatch, austere dark royal Norse attire in charcoal and deep midnight-blue with restrained antique-gold knotwork, a raven-feather mantle on one shoulder",
 'loki': "Loki the trickster, the INK OF CHAOS look - the man from the AZ face sheet exactly, lean and light in build, near-black layered leather-and-linen tunic with an asymmetric high collar and warm ember-bronze accent embroidery tracing serpent motifs along the seams, soft black boots, no armor, no cloak",
 'fenrir_adult': "Fenrir, the VOID MAW giant wolf - a colossal near-black monstrous wolf with faint silver-grey guard hairs along spine and shoulders, scarred grey-black muzzle, long fangs, striking amber eyes with a faint supernatural glow, dense matte-black fur",
 'fenrir_pup': "Fenrir here is a SMALL WOLF CUB roughly 8 weeks old - the same near-black fur and same amber eye colour as the adult VOID MAW, oversized paws, bright curious expression (the pup of the reference, not the adult)",
 'tyr': "Tyr the war-god, the FINAL OATH look - the man from the OL face sheet exactly, sandy-blond hair tied at the nape, short neat blond beard, practical honorable ember-gold and steel Norse war-gear with a muted steel-blue surcoat, leather bracers with iron studs",
 'hel': "Hel, the HALF-GOD HALF-DEAD - a quiet pale young woman, eerily calm, her face split vertically in one clean division: left half living with soft pale skin, ash-brown hair and a gentle grey eye, right half dead with ash-grey skin, a hollow cheek, faint dark veins and a dull eye, a dark ash-grey gown with muted bronze and bone accents, twin blade sheaths crossed at her back",
 'jorm': "Jormungandr, the world serpent - the titanic head and coiling neck of a sea serpent in deep sea-green scales with silver belly plates and golden reptilian eyes",
 'dwarfs': "the dwarf smiths - two stocky broad-shouldered dwarf master smiths with soot-marked weathered faces and long braided beards, dark leather aprons over rough wool",
}

CARD = {
 'odin':'odin_card_p1.png','loki':'loki_card_p1.png','fenrir':'fenrir_card_p1.png',
 'tyr':'tyr_card_p1.png','hel':'hel_card_p1.png','jorm':'jormungandr_card_p1.png',
 'dwarfs':'dwarfs_card_p1.png',
}
ROOT_REF = {  # asset_ref stem -> character key
 'odin':'odin','loki':'loki','fenrir':'fenrir','tyr':'tyr',
 'jorm':'jorm','hel':'hel','dwarfs':'dwarfs',
}
ENV_LINE = {
 'asgard_realm_env':'the golden realm of Asgard above the clouds - towering marble halls, a shining rainbow bridge, spires catching dawn light',
 'asgard_hall_env':'the great hall of Asgard - carved dark-wood pillars, golden knotwork banners, tall hearths, shafts of cold northern light through high windows',
 'ocean_env':'a vast churning northern ocean under a storm sky, spray and foam',
 'underworld_env':'a dim cold underworld of grey stone steps and pale mist',
 'landscape_env':'a rocky open Norse landscape under a wide sky',
 'nidavellir_env':'the dark caverns of Nidavellir, forge-fire glowing far below, sparks and ember light',
 'mountain_env':'a dark mountain fastness under an overcast northern sky',
}

def env_for(refs):
    for r in refs:
        stem = re.sub(r'_[A-Z]\d+_prop$','',r)
        if stem in ENV_LINE: return ENV_LINE[stem]
    return "the story setting, matched to the shot's palette and light direction"

def shot_n(sid): return int(re.match(r'^S(\d+)$',sid).group(1))

def build():
    d = json.load(open(DATA,encoding='utf-8'))
    acts = {a['id']:a for a in d['acts']}
    act_names = {a['id']:a.get('title',a['id']) for a in d['acts']}
    lines=[]
    A=lines.append
    A('# 13 — FENRIR, THE WOLF OF ASGARD — 46 START KEYFRAME PROMPTS FOR GROK')
    A('')
    A('> Generator: Grok (image). Output: the 46 START keyframes `kf_01_start.png` … `kf_46_start.png`.')
    A('> Strategy: N-clip START-FRAME-ONLY (43 sec.2) — every keyframe is a START frame; each drives one ~5 s clip.')
    A('> **DIRECTOR LOOK LOCKS 2026-11-12** — every character prompt below carries the locked look (VOID-SEER Odin / INK OF CHAOS Loki / VOID MAW Fenrir / FINAL OATH Tyr / HALF-GOD HALF-DEAD Hel). The attached P1 card + master sheet ARE the look; the text names it once (39/43).')
    A('> End keyframes (`kf_NN_end`) are a SECOND pass, drawn to match approved starts; not part of this batch.')
    A('> Zero GPU. Authoring only — this pack grants no render and no spend.')
    A('')
    A('## ATTACH TABLE — what to send Grok with this pack')
    A('')
    A('| File | Character | Role |')
    A('|---|---|---|')
    A('| `odin_card_p1.png` | ODIN | canonical P1 card (VOID-SEER look) |')
    A('| `loki_card_p1.png` | LOKI | canonical P1 card (INK OF CHAOS look) |')
    A('| `az_master_sheet.jpg` | LOKI face | IDENTITY ANCHOR — enrolled AZ identity (media/dhpf_master_sheets/) |')
    A('| `fenrir_card_p1.png` | FENRIR | canonical P1 card (VOID MAW adult + pup inset) |')
    A('| `tyr_card_p1.png` | TYR | canonical P1 card (FINAL OATH look) |')
    A('| `ol_master_sheet.jpg` | TYR face | IDENTITY ANCHOR — enrolled OL identity (awaited; full written design in card) |')
    A('| `hel_card_p1.png` | HEL | canonical P1 card (HALF-GOD HALF-DEAD look) |')
    A('| `jormungandr_card_p1.png` | JORMUNGANDR | canonical P1 card (story-generic sea-serpent look) |')
    A('| `dwarfs_card_p1.png` | DWARF SMITHS | canonical P1 card (story-generic smith look) |')
    A('')
    A('- **Face lock rule:** whenever `az_master_sheet.jpg` or `ol_master_sheet.jpg` is attached, the face in the frame must match that sheet exactly — eyes, nose, mouth, jaw, skin tone, facial hair. Only costume/pose/light change.')
    A('- **Kit separation:** Loki carries no paladin elements; Tyr carries no royal crown/eyepatch; each palette stays owned by its character.')
    A('')
    A('## NAMING — save every image EXACTLY like this (file <-> shot rectification list)')
    A('')
    A('| Keyframe file | Shot | Act |')
    A('|---|---|---|')
    rows=[]
    for act in d['acts']:
        for s in act['shots']:
            n=shot_n(s['id']); rows.append((n,s,act))
    for n,s,act in rows:
        A(f"| `kf_{n:02d}_start.png` | {s['id']} | {act['id']} |")
    A('')
    A('- `kf_NN` = shot number, ALWAYS two digits (01…46). `_start` = the frozen opening frame of that shot.')
    A('- 46 files total. Nothing else in the filename - no spaces, no suffixes.')
    A('')
    A('---')
    A('')
    pairing=[]
    for n,s,act in rows:
        refs=s.get('asset_refs',[])
        chars=[]
        for r in refs:
            stem=re.sub(r'_[A-Z]\d+_fused$','',r)
            stem=re.sub(r'_[A-Z]\d+_sheet$','',stem)
            if stem in ROOT_REF and ROOT_REF[stem] not in chars: chars.append(ROOT_REF[stem])
        # build identity sentence
        ident=[]
        for c in chars:
            if c=='fenrir':
                ident.append(LOOK['fenrir_pup'] if n==4 else LOOK['fenrir_adult'])
            else:
                ident.append(LOOK[c])
        idtxt = '; '.join(ident)
        # guards
        extra=[]
        neg=NEG
        if n==4: extra.append('FENRIR IS THE PUP in this shot - do not render the adult.')
        if 'tyr' in chars and n<40: extra.append("Tyr's RIGHT HAND is fully present and intact - both hands healthy and whole.")
        if n>=40 and 'tyr' in chars: extra.append("Tyr's right sleeve hangs EMPTY - the hand is already lost (no gore, no wound shown).")
        if 'tyr' in chars and n<40: neg=NEG_TYR_INTACT
        if n in (39,40): extra.append('No gore, no blood - the loss is implied, never shown.')
        if 'loki' in chars: extra.append('The face must match az_master_sheet.jpg exactly.')
        if 'tyr' in chars: extra.append('The face must match ol_master_sheet.jpg exactly.')
        kf=(s.get('kf_first') or '').strip()
        kf=re.sub(r',?\s*\d{3,4}x\d{3,4}\s*$','',kf)
        kf=re.sub(r',?\s*photoreal.*$','',kf,flags=re.I).strip().rstrip('.,')
        env=env_for(refs)
        cam=(f"Camera: {s.get('size','medium').lower()} shot at {s.get('angle','eye-level')}, composed as the frozen "
             f"opening frame of a {s.get('move','static')} move - subject sharp, background softly blurred, shallow depth of field.")
        attach=[]
        for c in chars: attach.append(CARD[c])
        if 'loki' in chars: attach.append('az_master_sheet.jpg')
        if 'tyr' in chars: attach.append('ol_master_sheet.jpg')
        # de-dup keep order
        seen=set(); attach=[a for a in attach if not (a in seen or seen.add(a))]
        prompt_lines=[f"Cinematic film still, photoreal: {kf}.",
                      f"Identity: {idtxt}." if idtxt else None]
        prompt_lines=[p for p in prompt_lines if p]
        for e in extra: prompt_lines.append(e)
        prompt_lines.append(f"Environment: {env}.")
        prompt_lines.append(cam)
        prompt_lines.append(STYLE)
        prompt='\n'.join(prompt_lines)
        A(f"## SHOT {n:02d} ({s['id']}) — {s.get('size','MEDIUM').upper()} · {s.get('angle','eye-level')} · {s.get('move','static')}")
        A('')
        A(f"### kf_{n:02d}_start.png")
        A(f"**Attach:** {', '.join(attach) if attach else 'none — environment/establishing frame'}")
        A('**Prompt:**')
        A(prompt)
        A(f"**Negative:** {neg}")
        A('')
        # mirror into data JSON
        s['image_prompt_start']=prompt
        cont=(s.get('continuation_prompt') or s.get('video_prompt_start') or '').strip()
        pairing.append((n,s['id'],cont))
    json.dump(d,open(DATA,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    # pairing table
    A('---')
    A('')
    A('## VIDEO-GEN PAIRING — one keyframe + its row = one clip job (43 sec.3b)')
    A('')
    A('| Keyframe file | Shot | Video continuation prompt |')
    A('|---|---|---|')
    for n,sid,cont in pairing:
        A(f"| `kf_{n:02d}_start.png` | {sid} | {cont} |")
    A('')
    A('## WORKFLOW AFTER GROK RETURNS THE 46 FILES')
    A('')
    A('1. All 46 files are READ here before any flagging (read-before-flag).')
    A('2. Identity gate: Loki frames vs az_master_sheet.jpg; Tyr frames vs ol_master_sheet.jpg.')
    A('3. Guard sweep: Tyr right hand intact on S15-S34 (kf_15..kf_34); empty sleeve on kf_40/42/43/44; Fenrir is a PUP on kf_04; no gore on kf_39/kf_40.')
    A('4. Approved starts -> SECOND PASS: kf_01_end … kf_46_end drawn to match (board law 28).')
    A('5. 92 keyframes hash-locked -> jobfile -> P6 price check -> P7 one-scene proof -> P8 full run ONLY on your approval.')
    A('')
    PACK.write_text('\n'.join(lines),encoding='utf-8')
    print('pack written:',PACK)
    print('shots:',len(rows))

build()
