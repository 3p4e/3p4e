import re, json

NEG_STD="duplicate face, extra limbs, extra fingers, deformed hands, text, watermark, logo, cartoon, anime, illustration, cel-shaded, 3d render, plastic skin, gore, blood"
GRIM_NEG=NEG_STD+", bright cheerful daylight, saturated cheerful colors, clean sterile look, glossy beauty-shot lighting, modern clothing, whimsical, cute"
GRADE="Photoreal grimdark Greek horror cinematic grade, Diablo 2 / Dark Souls aesthetic, 35mm anamorphic, real skin and scale texture, visible film grain, low-key dramatic horror lighting"

ENV={
 'S01':"a storm-lashed island citadel at dusk, lightning over a black churning Aegean",
 'S02':"a decaying torchlit megaron hall, shadows pooling like oil, bronze tarnished to black",
 'S03':"guttering torchlight against storm-dark stone, rain weeping down the walls",
 'S04':"a lightning-split sky over the citadel, carrion birds wheeling",
 'S05':"the tarnished bronze shield catching one sickly torch-flame",
 'S06':"a windswept ridge under bruised storm clouds, thorn scrub clawing at the wind",
 'S07':"Hermes descending through storm-cloud, rain streaking his winged sandals",
 'S08':"a storm-lashed terrace, brazier flames whipped sideways by the wind",
 'S09':"Athena materializing from storm-mist, owl-shadow circling",
 'S10':"torchlight guttering in a draught, darkness pressing close",
 'S11':"a barren cliff path under bruised storm sky, fog coiling between rocks",
 'S12':"storm-light on black rock, the shield mirror reflecting a bruised sky",
 'S13':"a jagged cliff face like broken teeth, a cave mouth breathing cold air",
 'S14':"a petrified warrior half-merged with living rock, weeping mineral stains",
 'S15':"the field of petrified warriors, ash-dust falling like snow",
 'S16':"the cave threshold exhaling cold breath, darkness absolute beyond",
 'S17':"walking backwards into a throat of blackness, torchlight failing",
 'S18':"the mirror-shield reflecting a weeping cavern of stone fangs",
 'S19':"a weeping cavern interior, stalactites like fangs, black pools",
 'S20':"the Gorgon lunging through shadow and falling dust",
 'S21':"a blur of desperate motion in torchlit dark, dust exploding",
 'S22':"eyes squeezed shut against the dark, sweat and rain",
 'S23':"the decisive blow in shadow, stone-dust bursting where she falls",
 'S24':"the Gorgon at rest, stone-still, her serpent hair gone cold",
 'S25':"the head secured in a stained leather sack, dust settling",
 'S26':"the cave mouth yawning behind, darkness breathing out",
 'S27':"Pegasus bursting from the cave into storm, wings thundering",
 'S28':"the two Gorgon sisters waking in the dark, stone-eyes igniting",
 'S29':"the Gorgons rising on wings of night, shrieking into the storm",
 'S30':"a high storm vista of the island, lightning sketching the coast",
 'S31':"skimming low over black heaving waves, salt spray like shrapnel",
 'S32':"a drowned coast of jagged rock, wreckage of old ships",
 'S33':"a jagged sea-rock like an altar, chains gone green with age",
 'S34':"a tear-streaked face lit by storm-split silver",
 'S35':"Pegasus landing hard on the rock, wings folding like a shroud",
 'S36':"rusted chains and white wrists, the sea growling below",
 'S37':"lifting off into a wall of storm, the rock shrinking beneath",
 'S38':"a tearful smile in grey storm-light",
 'S39':"gliding over a black heaving sea, the coast a bruise on the horizon",
 'S40':"two figures against a void of storm, mane and hair whipping",
 'S41':"shame and memory in eyes lit by distant lightning",
 'S42':"a sea serpent churning the waves, scales black as wet slate",
 'S43':"the serpent rising from foam like a nightmare given shape",
 'S44':"steady courage against the memory of the deep",
 'S45':"realization dawning in storm-grey light",
 'S46':"two hands clasping in shared resolve above the void",
 'S47':"a drowned-ruin coast at dusk, fog crawling up the cliffs",
 'S48':"a fog-drowned city gate, the storm finally spent",
}

def grim_transform(p):
    s=open(p).read()
    s=s.replace(NEG_STD, GRIM_NEG)
    s=re.sub(r'Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, 35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting', GRADE.replace('skin and scale texture','skin and fur texture'), s)
    s=re.sub(r'Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, 35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting', GRADE, s)
    # insert grim environment into the Environment slot
    def envsub(m):
        sid=m.group(1)
        return "Environment: "+ENV.get(sid,"storm-gloom, creeping fog, low-key horror light")+", matched to the shot's grim palette and light direction."
    s=re.sub(r'Environment: the story setting, matched to the shot\'s palette and light direction\.', lambda m: envsub_env(m), s)
    open(p,'w').write(s)

def envsub_env(m):
    return m.group(0)

# need per-shot id; do it block-wise instead
p='/a0/usr/projects/vast/storybook_ocr/specs/23_23_perseus_defeats_medusa_data_GROK_START_KEYFRAME_PROMPTS.md'
s=open(p).read()
s=s.replace(NEG_STD, GRIM_NEG)
s=s.replace('Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, 35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting', GRADE.replace('skin and scale texture','skin and fur texture'))
parts=re.split(r'(## SHOT )', s)
out=parts[0]
for i in range(1,len(parts),2):
    hdr=parts[i]; body=parts[i+1]
    sid=re.match(r'S(\d{2})', body).group(0)
    body=re.sub(r'Environment: the story setting, matched to the shot\'s palette and light direction\.',
                'Environment: '+ENV.get(sid,'storm-gloom, creeping fog, low-key horror light')+", matched to the shot's grim palette and low-key light direction.", body)
    out+=hdr+body
s=out
# grim header note
anchor='> Character reference: Perseus/Medusa = DIRECTOR-PROVIDED canon sheets (faces baked in, canon by delivery); AI-default cast = look cards from the design-look run.'
s=s.replace(anchor, anchor+'\n> AESTHETIC PIVOT 2026-11-12: grimdark Greek horror — desaturated cold palette, low-key motivated light, fog/ash/carrion textures, weird-art dread. NOT gore.')
open(p,'w').write(s)
print('KF pack: grim applied')

# ---- data JSON ----
d=json.load(open('/a0/usr/projects/vast/storybook_ocr/data/23_perseus_defeats_medusa_data.json'))
for a in d['acts']:
    a['palette']=["#3a4a4a","#1a1c22","#5a6b7a"]  # cold grey / near-black / bruised blue
    a['light_direction']='low-key motivated horror light, storm-gloom or torch or sickly cave reflections'
    for sh in a['shots']:
        sid=sh['id']
        sh['kf_first']=sh['kf_first']+', grimdark Greek horror, storm-gloom, desaturated cold palette'
        sh['kf_last']=sh['kf_last']+', dread atmosphere, low-key light'
        sh['continuity']=sh['continuity']+', grim horror register'
        sh['motion']=sh['motion']+', oppressive dread'
        sh['image_prompt_start']=re.sub(r'Photoreal Diablo 2 / World of Warcraft / StarCraft cinematic grade, 35mm anamorphic, real skin and fur texture, visible film grain, dramatic cinematic lighting',
            GRADE.replace('skin and scale texture','skin and fur texture'), sh['image_prompt_start'])
        sh['ltx_prompt']=sh['ltx_prompt']+', grimdark Greek horror, oppressive dread'
        sh['video_prompt_start']=sh['video_prompt_start']+', dread atmosphere'
        sh['video_prompt_end']=sh['video_prompt_end']+', dread atmosphere'
json.dump(d, open('/a0/usr/projects/vast/storybook_ocr/data/23_perseus_defeats_medusa_data.json','w'), indent=1, ensure_ascii=False)
print('data JSON: grim applied')

# verify
kf=open(p).read()
bl=re.split(r'## SHOT ', kf)[1:]
def plen(b): return len(b.split('**Negative:**')[0].split('**Prompt:**')[1].strip())
print('shots:', len(bl), '| max chars:', max(plen(b) for b in bl), '| over1450:', sum(1 for b in bl if plen(b)>1450))
print('grim env inserted:', kf.count("matched to the shot's grim palette"))
print('old grade remaining:', kf.count('World of Warcraft'))
