#!/usr/bin/env python3
"""Hollow Bloom (DD vs AZ vs Hollow Bloom) K6-distilled jobfile — 50 shots, start-frame-only.
Applies 44 D-rules: D5 high-contrast action register, D2 resolution directive (in keyframe prompt ref),
44 A-rules (no invented props, one phase, body-form guards, crowd no-people, full-body motion).
K6: Kandinsky6TI2VAPipeline, start-only, 121f, 16 steps, guidance 1.0, native audio, 832x480.
"""
import json
HEADER = ('High-contrast cinematic action: bold chiaroscuro lighting, hard rim-light carving subjects '
 'from deep shadow, hot specular highlights on wet metal and ice, deep crushed blacks, visible motion '
 'blur on all fast-moving elements, 35mm anamorphic energy. ')
GUARD = (' - one continuous phase, no cuts, no angle changes. No new people, no bystanders appear. Faces, '
 'armour, weapons and proportions remain exactly as the start frame - no morphing, no drift. The camera '
 'movement named is the only camera motion.')
NE_BASE = ('duplicate face, extra limbs, extra fingers, text, watermark, logo, cartoon, anime, '
 'new people, bystanders, morphing, drift')
SHOTS = {
 1:('W','Fungal marsh at dusk, teal water, giant mushroom towers; DD (bare-headed demon hunter, glowing teal hair, frost-arcane armor) and AZ (full-plate paladin, greatsword) stand on a hummock at the corruption ring edge, spore-mist drifting','slow dolly-in, mist drifts'),
 2:('W','both heroes at the grey corruption edge; the blight visibly creeps a hand-width toward them, black veins pulsing','slow push-in, veins pulse'),
 3:('I','extreme close-up: DD bare hand cocks the twin crossbow; a crystalline frost-arrow materialises in the groove, frost spreading','insert, macro, frost spreads'),
 4:('I','extreme close-up: DD glowing teal hair rolls in a slow weightless wave; neon teal brightens, nearby spores freeze and fall','insert, hair drifts like water'),
 5:('I','extreme close-up: AZ gauntleted hand grips the greatsword hilt; the molten-gold rune-tattoo wakes along his forearm','insert, light travels up the arm'),
 6:('W','the Hollow Bloom boss rises from the corrupted patch, spore-sacs inflating, then stands with maw opening; spores fall upward','low rise, spores drift up'),
 7:('C','a blight tendril coils tight then SNAPS forward like a whip-crack; marsh debris shakes','whip crack, camera shake'),
 8:('M','DD raises one arm; a Glacial Aura frost-ring blooms outward, drifting spores crystallising to snow in the air','aura bloom, camera pull-back'),
 9:('W','the whip-tendril slams the marsh near the heroes; a blight-furrow gouges the teal water, scorch and spray','whip impact, whip-pan'),
 10:('M','DD kicks off in a Frost Rush, becoming a comet of rime streaking low over the teal water','sprint smear, whip-pan'),
 11:('C','DD fires BOTH crossbows; three crystalline frost-bolts streak out trailing ice','bolts, slow-mo to realtime'),
 12:('I','the frost-bolts slam a tendril; flash-freeze spreads, the vine goes brittle white and cracks','impact, crash-zoom'),
 13:('W','AZ plants the greatsword tip into the ground; a gold shockwave cracks outward across the corrupted floor','ring shock, low hold'),
 14:('M','AZ swings Templar Verdict; a light-arc detonates on the Hollow Bloom, gold fire blooming','swing and boom, orbit'),
 15:('C','the Hollow Bloom reels, its maw twisting; spore-sacs flare brighter in agitation','recoil, push-in'),
 16:('W','the Bloom sweeps a tendril across the whole arena; DD and AZ vault in OPPOSITE directions to evade','sweep and vault, cross-cut'),
 17:('M','DD flips backward and lands in a low crouch, frost-smoke pooling at her boots','flip and land, whip-pan'),
 18:('C','DD eyes ignite; twin white-blue Rime Beam lances slash out across the marsh','beam and freeze, rack-focus'),
 19:('W','COMBO Freeze-and-Sunder: DD Rime Beams flash-freeze a tendril mid-swing, then AZ Verdict shatters it, golden shockwave ripping through the ice','beam then shatter, track'),
 20:('M','the Bloom staggers, its frozen vine fracturing; the maw opens in a silent roar','recoil, push-in'),
 21:('W','the Bloom hunches; its spore-sacs rupture one after another, green spore-mushrooms blooming','burst and sacs, wide'),
 22:('C','AZ raises the greatsword; a Blade of Justice light-blade summons above him, descending','blade descend, tilt-up'),
 23:('M','the light-blade plunges down; the Bloom staggers under a white pillar of holy light','blade and pillar, pan'),
 24:('W','the Bloom slams its root-feet; Spore Rain begins, the sky dimming sickly green','rain and shock, crane-up'),
 25:('M','DD curls under her frost-wings; the Glacial Aura membrane shields her as spores hiss to snow on it','shield and hiss, close'),
 26:('M','AZ strides forward through the spore rain; his holy light sheds the spores like water, ground flushing teal at his boots','walk and light, dolly-back'),
 27:('I','the Bloom exhales a choking green spore-gout; a thick green column blasts outward','gout, insert'),
 28:('W','GROUP: DD vaults OVER the spore-gout while AZ charges THROUGH its shadow, both converging on the Bloom','split-action, wide'),
 29:('W','AZ stands square; a Wake of Light white-gold cone scours the ground, blight receding in a wave before him','cone and purge, sweep'),
 30:('C','DD winds up The Hunt; her frost-wings fold, snow coils concentrating around her','wind-up, push-in'),
 31:('W','DD executes The Hunt dive; a lance down crossbows-first, leaving a frozen trail, crater on impact','dive and crater, aerial'),
 32:('M','the impact crater erupts; spore-sacs flicker, the Bloom forced down to one root-knee','impact and kneel, shake'),
 33:('C','COMBO Hoarfrost Judgement: AZ marks the sac-cluster with an Execution Sentence rune; DD frost locks it; the rune detonates in a light-column through the ice','mark freeze boom, orbit'),
 34:('C','AZ regrips the greatsword two-handed; holy runes blaze up the blade length','grip and runes, orbit'),
 35:('W','the Bloom ENRAGES; it swells open, spores spiralling into a rising vortex','swell and vortex, wide'),
 36:('CU','the Bloom maw fills frame; it speaks (subtitle beat), spore-light pulsing in its throat','maw, close-up'),
 37:('W','the Bloom ignites the Pollen Nova; a spore supernova rises, marsh light drowning in green','nova, crane-up'),
 38:('M','DD wing-flares, both crossbows raised; glacier energy peaking around her, hair blazing teal','flare and shift, orbit'),
 39:('M','AZ plants both hands; Avenging Wrath surges his tattoo gold-to-white, golden wings blooming at his back','surge and wings, rack-focus'),
 40:('W','GROUP still-beat: DD and AZ hold side by side under the rising spore-nova, only spores moving','held wide, spores only'),
 41:('M','DD leaps in full Glacier Form, Immortal wings wide, a personal snowstorm blasting against the spores','leap and form, aerial'),
 42:('M','AZ rises radiant, the greatsword burning white-gold, a halo of light at his back','rise and halo, tilt-up'),
 43:('W','COMBO Blizzard and Verdict: both launch together, a frost streak and a gold streak winding around each other toward the Bloom','twin dive, aerial'),
 44:('C','DD fires Rime Beams and both crossbows at once; a violet-white lance punches through the Bloom heart','beam and shot, slow-mo'),
 45:('C','AZ final Verdict arc; the greatsword splits the Bloom, holy light flooding out of the wound','slash and split, crash'),
 46:('W','the Pollen Nova collapses inward; light versus spore in a tightening sphere','collapse, wide pull'),
 47:('I','the corpse-flower head cracks and folds shut, wilting, spore-sacs going dark','crown and fall, inset'),
 48:('W','spores settle like grey snow; two silhouettes stand over the purifying patch','drift, wide'),
 49:('C','DD exhales a wisp of frost, her glowing hair dimming to an idle gradient; she almost smiles','breath and frost, close-up'),
 50:('W','AZ turns, greatsword over his shoulder; dawn breaks, the marsh water glowing teal again, purified','walk and light, dolly'),
}
CAM_SZ = {'W':'WIDE','M':'MEDIUM','C':'CLOSE-UP','CU':'CLOSE-UP','I':'INSERT'}
jobs=[]
for n,(sz,action,cam) in SHOTS.items():
    prompt=(HEADER + action + '. Camera: ' + CAM_SZ[sz] + ' shot, ' + cam + '.' + GUARD +
            ' Negative: ' + NE_BASE + '.')
    jobs.append({'n':n,'shot':n,'kf':f'/workspace/keyframes/kf_{n:02d}_start.png',
                 'out':f'/workspace/out_k6/hb_s{n:02d}_k6.mp4','seed':700+n,'prompt':prompt})
import os; os.makedirs('tools/vast/jobs', exist_ok=True)
json.dump(jobs, open('tools/vast/jobs/p23_hb_k6_50.json','w'), indent=1)
print('WROTE', len(jobs), 'jobs -> tools/vast/jobs/p23_hb_k6_50.json')
print('sample shot19 len:', len([j for j in jobs if j['n']==19][0]['prompt']))
print('sample shot19:', [j for j in jobs if j['n']==19][0]['prompt'][:220])
