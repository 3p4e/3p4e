import json
HEADER = ('High-contrast cinematic action: bold chiaroscuro lighting, hard rim-light carving '
 'subjects from deep shadow, hot specular highlights on wet metal and spray, deep crushed '
 'blacks, visible motion blur on all fast-moving elements, 35mm anamorphic energy. ')
GUARD = (' - continuous, no cuts, no angle changes. No new people, no bystanders appear. Faces, '
 'armour and proportions remain exactly as the start frame - no morphing, no drift. The camera '
 'movement named above is the only camera motion.')
C = {'F01':'CLOSE-UP','F02':'WIDE','F03':'MEDIUM','F04':'WIDE','F05':'CLOSE-UP',
     'F06':'CLOSE-UP','F07':'MEDIUM','F08':'CLOSE-UP','F09':'WIDE','F10':'CLOSE-UP'}
A = {
'F01':"The instant AFTER her ambush lunge connects, Medusa's clawed palms SMASH down onto the raised Gorgon Aegis, the impact point BURSTING orange sparks that scatter and fall like embers, both fighters STRUGGLING full-body against each other, Perseus driven to one knee with veins standing out, her jaws inches from the shield rim, hair-snakes lunging forward around the clash.",
'F02':"Medusa's massive snake-tail SCYTHES horizontally at ankle height toward Perseus, loose stone and dust EXPLODING in its wake, Perseus mid-leap above it with cloak snapping, one hair-snake striking up at him as he clears the sweep.",
'F03':"Medusa REARS and her hair-snakes lash out in SIX directions at once - from both flanks, overhead, low at the legs - while her claws follow through, Perseus weaving between two strikes, the harpe deflecting a third, the remaining snakes missing by centimetres, torch flames flattening in the flurry's wind.",
'F04':"Medusa has CAUGHT Perseus mid-air and HURLED him into a grotto column, Perseus slamming into the cracked stone and sliding down through the dust, harpe still in his fist, while she stands over the impact point coiling and hissing, hair-snakes spread like a crown.",
'F05':"Medusa has Perseus PINNED on his back, one clawed hand crushing his sword-wrist to the stone, her jaws DESCENDING toward his face while Perseus wedges the Gorgon Aegis edge-up between them as the last barrier, her saliva dripping onto the mirrored bronze, his knuckles white on the shield rim.",
'F06':"Perseus has gone LIMP under her - eyes half-closed, grip loosened, apparently finished; Medusa REARS BACK for the killing strike, coiled high with jaws wide - and in the foreground his free hand CLOSES silently around the fallen harpe's grip, his eyes not closed but locked on her throat.",
'F07':"The comeback: Perseus EXPLODES up from the ground in a rising diagonal slash that OPENS Medusa's flank in a line of black ichor, her body arching in recoil with mouth wide in the first scream of pain, the harpe extended through the follow-through, ichor spray suspended across the torchlight.",
'F08':"Perseus ANGLES the Gorgon Aegis so Medusa SEES her own reflection in the mirrored bronze, the first true fear crossing her face as her own petrifying stare is thrown back at her, both freezing mid-exchange while her hair-snakes recoil from the mirror-image, Perseus watching over the shield rim.",
'F09':"The harpe's hook has SNAGGED Medusa's jaw-ridge and Perseus HAULS on the blade with his full body-weight, boots planted and skidding furrows in the stone, her body dragged off-balance toward him with tail thrashing for traction, both locked in one diagonal line of force.",
'F10':"The half-second before the cleave: Perseus has both hands on the harpe, the blade RAISED to apex, his whole body a drawn bow of muscle, while Medusa's eyes stay locked on the blade's descent-path with hair-snakes stretched toward him in a last futile strike.",
}
CAM = {
'F01':"Camera: CLOSE-UP shot at low angle, both faces over the shield rim, a rack-focus punch-in frozen at impact - subject sharp, background softly blurred, shallow depth of field.",
'F02':"Camera: WIDE shot at ground level, a whip-pan frozen at its midpoint, the tail crossing frame like a whip with Perseus airborne above it, motion streaks at the frame edges.",
'F03':"Camera: MEDIUM shot at eye level, Perseus centre-frame with attack vectors converging from all sides, a swish-pan frozen mid-motion - readable chaos, shallow depth of field.",
'F04':"Camera: WIDE shot at high angle looking down the column, a crash-zoom settling on Medusa's silhouette dominating frame centre.",
'F05':"Camera: CLOSE-UP shot at ground level beside Perseus's head, a slow push-in tightening the claustrophobia - the near-death frame.",
'F06':"Camera: CLOSE-UP shot at eye level, a shallow-focus rack from her rearing form to his hand in the foreground - held-breath stillness in a still.",
'F07':"Camera: MEDIUM shot at low angle, the slash cutting frame on the rising diagonal, a whip-tilt frozen at the reversal - motion streaks at the frame edges.",
'F08':"Camera: CLOSE-UP shot over Medusa's shoulder falling INTO the reflection, a slow push-in on the mirrored face.",
'F09':"Camera: WIDE shot side-on, both bodies in profile, a tracking shot frozen mid-pull as the force-line drags across frame.",
'F10':"Camera: CLOSE-UP shot at low angle looking UP the blade-line at Perseus, a slow push-in on the raised apex, Medusa's face in the deep background.",
}
NE = {
'F01':"duplicate face, extra limbs, merged bodies, her claws through the shield, text, watermark, cartoon, anime, bright light",
'F02':"duplicate face, extra limbs, tail passing through Perseus, floating body, text, watermark, cartoon, anime",
'F03':"merged snakes, snakes fused with face, extra heads, extra swords, text, watermark, cartoon, anime",
'F04':"broken body, gore, blood spray, impalement, text, watermark, cartoon, anime",
'F05':"bite connecting, blood, broken shield, duplicate faces, text, watermark, cartoon, anime",
'F06':"Medusa aware of the hand, second weapon materialising, text, watermark, cartoon, anime",
'F07':"dismemberment, gore fountain, duplicate blades, text, watermark, cartoon, anime",
'F08':"Medusa petrified, stone texture on her, text, watermark, cartoon, anime",
'F09':"blade snapping, rope instead of blade, merged bodies, text, watermark, cartoon, anime",
'F10':"blade already mid-swing, severed head, gore, text, watermark, cartoon, anime",
}
jobs=[]
for i,f in enumerate(['F01','F02','F03','F04','F05','F06','F07','F08','F09','F10'], start=1):
    prompt = HEADER + A[f] + ' ' + CAM[f] + GUARD + ' Negative: ' + NE[f] + '.'
    jobs.append({'kf':f'/workspace/keyframes/kf_{f}_start.jpg','n':i,'out':f'/workspace/out/p23_{f}_v4.mp4','prompt':prompt,'seed':300+i})
json.dump(jobs, open('tools/vast/jobs/p23_fight10_v4.json','w'), indent=1)
print('jobfile written:', len(jobs), 'jobs')
print('sample F04 prompt len:', len([j for j in jobs if j['n']==4][0]['prompt']))
