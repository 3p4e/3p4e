import re
p='/a0/usr/projects/vast/storybook_ocr/specs/23_23_perseus_defeats_medusa_data_GROK_START_KEYFRAME_PROMPTS.md'
src=open(p).read()

canon={
 'hero_Perseus':"Perseus - BRONZE VOW loadout per approved look card look_01_perseus.png (face = AZ, bronze hoplite, mirrored shield, harpe)",
 'boss_Medusa':"Medusa - GORGON CURSE loadout per approved look card look_02_medusa.png (face = feminized DD, snake-hair, golden eyes, snake-tail, no gore)",
 'goddess_Athena':"Athena - WISDOM AEGIS loadout per approved look card look_03_athena.png",
 'hermes':"Hermes - WINGED MESSENGER loadout per approved look card look_04_hermes.png",
 'pegasus':"Pegasus - WINGED STEED loadout per approved look card (look_05 panel A)",
 'andromeda':"Andromeda - CHAINED MAIDEN loadout per approved look card (look_05 panel B)",
 'king':"the King - ISLE SOVEREIGN loadout per approved look card (look_05 panel C)",
 'weapon_shield':"the mirrored bronze shield",
 'weapon_sword':"the adamantine harpe",
 'weapon_sack':"the leather sack for Medusa head",
 'stone_warrior':"a petrified stone warrior (statue)",
 'gorgons':"Medusa Gorgon sisters (match look_02_medusa.png)",
 'sea_serpent':"Poseidon sea serpent (AI-default creature, design per shot)",
 'chain':"bronze chains",
}

parts=re.split(r'(## SHOT )', src)
out=parts[0]
fixed=0
for i in range(1,len(parts),2):
    hdr=parts[i]; body=parts[i+1]
    m=re.search(r'\*\*Attach:\*\* (.+)', body)
    attach=m.group(1).strip() if m else 'none'
    refs=[r.strip() for r in attach.split(',')] if not attach.startswith('none') else []
    if refs and 'Canon:' not in body:
        cans=[canon[r] for r in refs if r in canon]
        if cans:
            body=body.replace('Action:', 'Canon: ' + '; '.join(cans) + '.\nAction:', 1)
            fixed+=1
    out+=hdr+body

open(p,'w').write(out)
print('fixed blocks:', fixed)

kf=open(p).read()
bl=re.split(r'## SHOT ', kf)[1:]
missing=[b.split('\n')[0] for b in bl if '**Attach:** none' not in b and 'Canon:' not in b]
print('still missing canon:', missing if missing else 'NONE')
print('total shots:', len(bl))
