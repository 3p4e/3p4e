import re
p='/a0/usr/projects/vast/storybook_ocr/specs/23_23_perseus_defeats_medusa_data_GROK_START_KEYFRAME_PROMPTS.md'
src=open(p).read()

src=src.replace('> Generator: Grok (image). Characters STORY-GENERIC (AI-default, no enrolled faces).',
 '> Generator: Grok (image). Casting CONFIRMED 2026-11-12: Perseus = AZ (enrolled face), Medusa = feminized DD (enrolled face), all others AI-default.')

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
for i in range(1,len(parts),2):
    hdr=parts[i]; body=parts[i+1]
    lines=body.split('\n')
    attach=''
    for l in lines:
        if l.startswith('**Attach:**'):
            attach=l.split(':',1)[1].strip(); break
    refs=[r.strip() for r in attach.split(',')] if attach and not attach.startswith('none') else []
    keep=[l for l in lines if not re.match(r'^(Loadout|Materials|Abilities|Weapon):', l)]
    for j,l in enumerate(keep):
        if l.startswith('Action:'):
            cans=[canon[r] for r in refs if r in canon]
            if cans:
                keep.insert(j+1, 'Canon: ' + '; '.join(cans) + '.')
            break
    out+=hdr+'\n'.join(keep)

open(p,'w').write(out)

kf=open(p).read()
bl=re.split(r'## SHOT ', kf)[1:]
def plen(b):
    return len(b.split('**Negative:**')[0].split('**Prompt:**')[1].strip())
long=[b.split('\n')[0] for b in bl if plen(b)>1450]
print('shots:', len(bl))
print('prompts >1450:', long if long else 'NONE')
print('stale boilerplate remaining:', len(re.findall(r'The Line Does Not Break|What the Dark Bred|Quiet That Outlasts|Older Than the Name', kf)))
print('max prompt chars:', max(plen(b) for b in bl))
print('canon coverage ok:', all(('Canon:' in b) or ('**Attach:** none' in b) for b in bl))
