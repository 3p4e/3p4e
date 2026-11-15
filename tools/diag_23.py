import re
p='/a0/usr/projects/vast/storybook_ocr/specs/23_23_perseus_defeats_medusa_data_GROK_START_KEYFRAME_PROMPTS.md'
kf=open(p).read()
bl=re.split(r'## SHOT ', kf)[1:]
for b in bl:
    hdr=b.split('\n')[0]
    attach=re.search(r'\*\*Attach:\*\* (.+)', b).group(1).strip()
    has_canon='Canon:' in b
    refs=[r.strip() for r in attach.split(',')] if not attach.startswith('none') else []
    known={'hero_Perseus','boss_Medusa','goddess_Athena','hermes','pegasus','andromeda','king','weapon_shield','weapon_sword','weapon_sack','stone_warrior','gorgons','sea_serpent','chain'}
    unknown=[r for r in refs if r not in known]
    if refs and not has_canon:
        print('MISSING CANON:', hdr, '| attach:', attach, '| unknown refs:', unknown)
    if unknown:
        print('UNKNOWN REF:', hdr, '|', unknown)
print('---done---')
