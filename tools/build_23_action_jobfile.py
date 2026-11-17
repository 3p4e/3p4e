#!/usr/bin/env python3
"""#23 full action-rewrite jobfile builder. Composes motion-rich prompts for all 60 shots
from the keyframe-pack beats + hand-authored motion clauses. NO 'slow motion' anywhere."""
import json, re

SPEC = open('/a0/usr/projects/vast/storybook_ocr/specs/23_GROK_60_KEYFRAME_PROMPTS.md').read()
GUARDS = ("Only the characters already visible in the start frame are present - no new people, "
          "no bystanders, no crowd. Every character keeps their exact face, armor and proportions "
          "from the start frame - no morphing, no face changes, no extra limbs. The camera move "
          "described is the only camera motion - no sudden cuts, no angle changes.")

# Hand-authored motion clauses - one per shot, active verbs, no 'slow motion'
MOTION = {
1: "Storm clouds churn and roll over the citadel, banners snap and whip on the walls, waves crash against the cliffs below sending spray upward, torch-flames gutter in the wind, gulls wheel through the grey sky.",
2: "Perseus kneels before the king, the king's hand rises and falls in a dismissive gesture, torch-flames flicker across both faces, wind stirs the king's cloak, Perseus lowers his head then lifts it.",
3: "Resolve hardens across Perseus's face - his jaw tightens, his eyes narrow, torchlight dances across his bronze armor, a gust whips his hair across his brow and he pushes it back.",
4: "Shadow smoke curls and drifts through the lair, Medusa's snake hair undulates and re-coils in continuous waves, her chest rises and falls with breath, darkness shifts at the frame edges.",
5: "Medusa's glowing slit-pupil eyes flare brighter, her serpent hair writhes and strikes at the air, shadow smoke pours off her shoulders, her lips peel back in a snarl.",
6: "Golden light blooms and expands around Athena as she appears, grass and dust ripple outward from her arrival, her cloak settles from the displacement, Perseus steps back a half-step.",
7: "Athena extends the mirror-shield forward - light plays and ripples across its polished surface, her arm is steady, wind stirs her hair, Perseus reaches toward it.",
8: "Hermes presents the bronze sword, winged sandals and helmet - the sword gleams as he turns it, the winged sandals flutter, his movements are quick and precise, light glints off each gift.",
9: "Athena counsels Perseus - her mouth moves in measured speech, her hand gestures for emphasis, Perseus nods slowly, wind moves both their cloaks, her eyes track his reactions.",
10: "The warning sinks in - Perseus's eyes shift from doubt to resolve, he gives a single quiet nod, his chest rises with a deep breath, torchlight flickers across his set jaw.",
11: "Perseus treks across the barren cliffs - his cloak streams behind him in the wind, loose stones scatter under his boots, his shield bounces against his back with each stride, distant storm clouds drift.",
12: "Perseus polishes the mirror-shield as he walks - his arm moves in circular strokes, the shield surface catches light in shifting patterns, his hair whips in the ridge-wind, dust drifts past.",
13: "The camera reveals the jagged cliff face - the dark cave mouth looms, petrified standing figures emerge from the mist, wind drives spray across the rocks, clouds scud past the peaks.",
14: "The camera pans past the warrior turned to grey stone - his frozen mid-step form fills the frame, dust and mist drift around him, his stone hair stirs almost imperceptibly in the cave-breath wind.",
15: "Perseus studies the petrified warriors - his grip tightens on the mirror-shield, knuckles whitening, his eyes move from figure to figure, his breathing quickens, wind tugs his cloak.",
16: "Perseus steels himself - his eyes close for a beat then snap open with courage, he draws a sharp breath, his shoulders square, he raises the mirror-shield a fraction higher.",
17: "Perseus walks backwards into the dark cave - his boots scrape the stone with each careful step, the mirror-shield raised to view behind him catches torch-light, darkness swallows the frame edges, dust motes drift.",
18: "The mirror-shield surface shimmers - cave shadows drift through the reflection, torch-light ripples across the polished bronze, a faint movement deep in the reflection grows slowly closer.",
19: "Medusa rises from her stone bed - her body uncoils upward, serpent hair unfurls and spreads in violent waves, stone dust cascades off her form, shadow smoke erupts around her, her eyes ignite.",
20: "Medusa lunges toward the camera - claws outstretched, her body drives forward with predatory speed, serpent hair lashes behind her, her jaw opens in a hiss, shadow smoke trails her charge.",
21: "Medusa strikes - claws rake across the raised mirror-shield with impact, bronze sparks scatter and fly in all directions, the shield rings and trembles from the blow, her arm recoils from the clash.",
22: "Perseus spins with eyes shut tight - his body whips around in a full turn, the harpe arcs through the air in a sweeping circle, his cloak flares outward with the rotation, dust blasts outward.",
23: "Medusa recoils from her own reflected gaze - her head snaps back, serpent hair lashes and whips in chaotic waves, hatred and confusion cross her face, she stumbles a half-step, shadow smoke boils.",
24: "Perseus's squeezed-shut eyes tighten further - his brow knots, his teeth clench, a bead of sweat runs down his temple, his grip whitens on the harpe, his whole face strains with concentration.",
25: "Perseus answers with the harpe - the hooked blade sweeps low past Medusa's guard in a cutting arc, his body steps through her guard in a practiced pass, his cloak whips with the turn, the blade gleams.",
26: "The decisive strike lands - the harpe cleaves through Medusa in a single clean arc, her form shudders and goes still, serpent hair drops like cut ropes, shadow smoke erupts and dissipates, her body begins to fall.",
27: "The severed head of Medusa rests - her serpents grow still one by one, the burning gaze dims and fades from her eyes, shadow smoke drifts away thin, blood pools slowly at the stone.",
28: "Perseus places the head into the leather sack - his hands work quickly, the sack mouth closes and he pulls the cord tight, double-knotting it, the sack bulges and shifts once, he slings it onto his back.",
29: "The mirror-catch burns - Medusa's final gaze locks on her own reflection in the polished bronze, the reflected eyes flare and then gutter out, the shield surface trembles, the light in it dies.",
30: "Perseus sprints out of the dark cave - his legs drive hard against the stone, the sack bounces on his back, his cloak streams behind him, the storm-grey light rushes to meet him, dust kicks up with every stride.",
31: "The camera cranes down to reveal Pegasus - the winged horse stamps and tosses its head, wings half-spread and beating once, mane ripples in the storm-wind, it turns toward the emerging Perseus.",
32: "Perseus approaches Pegasus with hand extended - the horse lowers its head toward the open palm, breath steaming from its nostrils, wings fold and settle, the golden glow pulses, Perseus closes the last steps.",
33: "Pegasus spreads its great white wings for takeoff - the wings rise and beat downward with power, dust and grass blast outward, Perseus settles into the saddle, the horse launches upward.",
34: "Two Gorgon sisters emerge from the cave shrieking - their bodies surge forward into the open, wings of shadow unfurl and beat, their shriek distorts the air, clawed hands rake the sky toward the escaping rider.",
35: "Pegasus and Perseus soar over the open sea - wings beat in powerful strokes, spray and spindrift fly past, the sack strains against its straps, Perseus leans into the flight, the coastline slides away below.",
36: "The camera cranes down toward the rock face - a lone chained figure resolves against the pounding waves, spray bursts against the rock below, the chain glints, her hair whips in the sea-wind.",
37: "Andromeda strains against the chains - her body pulls against the iron, wind whips her tunic and dark hair in continuous snapping waves, sea-spray drifts across her face, she turns her head at a sound.",
38: "The Gorgon sisters burst from the deeper dark - their shadow-wings unfurl to full span, the shriek warps the air visibly, debris and dust blast outward from their emergence, their eyes hunt.",
39: "Andromeda's tear-streaked face turns - her eyes widen, her lips part, hope breaks across her expression, fresh tears well and spill, the wind gentles for a moment around her.",
40: "Perseus does not look back - his jaw sets harder, the mirror-shield raised against the shriek, the sack clutched tighter to his chest, his cloak snaps in the storm-blast, the shield surface shimmers with the sound-waves.",
41: "Pegasus lands on the rock ledge - wings beat and flare for the landing, stone dust scatters, Perseus dismounts in one motion and strides toward the chains, Pegasus settles behind him.",
42: "The first pursuer crumbles - grey stone races up her body from the feet, her shriek dies in her throat, her wings freeze mid-beat, her reaching hands petrify, she tips and shatters against the rock.",
43: "Perseus loosens the iron chains - link by link the metal slackens around Andromeda's wrists, her hands drop free, she flexes her fingers, blood rushes back, spray drifts across both figures.",
44: "Andromeda seats herself behind Perseus as Pegasus lifts - the horse surges upward, wings beating hard, her arms find his waist, the rock drops away below, wind drives their hair and cloaks flat.",
45: "Andromeda's gratitude overflows - a tearful smile breaks across her face, her hands press together, a laugh escapes through the tears, the wind softens, light shifts warmer across her face.",
46: "Pegasus glides high above the sea with both riders - wings hold steady in the glide, clouds stream past, the distant coast draws slowly closer, spray-mist trails beneath, the sack shifts on Perseus's back.",
47: "Andromeda speaks as Perseus listens on the flying horse - her mouth moves, her hair streams behind in the flight-wind, her hands gesture as she tells her story, Perseus turns his head slightly toward her.",
48: "Andromeda recounts the offense of her mother - shame and memory move through her eyes, her hair whips in the wind, sea-spray drifts across her face catching distant lightning, her lips tremble, a tear traces her cheek.",
49: "The camera cranes down to the sea - the serpent churns the waves, its scaled back breaks the surface and submerges, foam bursts upward, the water coils and heaves, spray flies.",
50: "The sea serpent's head rises from the foam - seawater cascades off its scales in sheets, the fanged maw opens wider, foam churns below, its eyes fix upward with hunger, the neck coils.",
51: "Andromeda faces the harrowing memory - her chin lifts, fear gives way to steady courage, her eyes harden with resolve, the wind pulls at her hair, her hands steady on Perseus's waist.",
52: "The ketos rears over the rock - its body drives upward out of the sea, a mountain of scale and foam, seawater sheets off its barnacle ridge, the sea stands up around it, Andromeda's tunic whips, spray fills the air.",
53: "Perseus draws the kibisis open with one hand, eyes already turned away - the sack mouth opens, his other hand reaches inside, his jaw clenches, the fabric of the sack strains, wind snaps his cloak.",
54: "Perseus presents the severed head - the head swings up by its hair into the open air, Medusa's dead eyes open toward the sea, the ketos's gaze locks on the head, the sea goes still, light shifts and pulses with the frozen moment.",
55: "The ketos, gone grey stone - waves break against its fossilized coils and shatter into foam, seawater streams down the stone, gulls wheel and dive around the new reef, the storm light shifts.",
56: "Perseus and Andromeda turn from the sea together - her hand finds his, their heads turn as one, the storm light breaks warmer across both faces, wind softens, spray settles.",
57: "Realization dawns across Perseus's face - his eyes widen slightly, his jaw loosens, a breath escapes, distant lightning flickers across his armor, his hand tightens on the reins.",
58: "Two hands clasp in shared resolve - fingers interlock and grip, the clasp tightens, wind streams past the joined hands, the flying horse's mane whips in the foreground.",
59: "The camera cranes up with Pegasus descending toward the coastal city - the white walls glow in the dusk light, torch-points flicker alive across the city, wings beat in descent, the sea glitters below.",
60: "The reunited family at the city gates - arms open and embrace, the group closes together, Pegasus settles and folds its wings behind them, torch-light warms the scene, cloaks settle.",
}

MOVE_MAP = {'push-in':'pushes in steadily','pull-back':'pulls back steadily','crane-down':'cranes down steadily','crane-up':'cranes up steadily','pan-left':'pans left steadily','pan-right':'pans right steadily','swish-pan':'whips in a fast pan','track':'tracks steadily','static':'holds static','two-shot':'holds on the two-shot','behind':'tracks from behind'}

def camera_sentence(cam):
    parts = [p.strip() for p in cam.split('·')]
    angle = parts[1].lower() if len(parts) > 1 else ''
    move = parts[2].lower() if len(parts) > 2 else 'static'
    mv = MOVE_MAP.get(move, f'moves in a {move}')
    ang = f' at {angle}' if angle else ''
    return f"The camera {mv}{ang} throughout the clip - continuous, no cuts, no angle changes."

def compose(n, cam):
    scale = cam.split('·')[0].strip().title()
    return (f"{scale} shot continuing from the start frame: {MOTION[n]} "
            f"{camera_sentence(cam)}\n{GUARDS}")

jobs = []
for n in range(1, 61):
    cam_m = re.search(rf'## SHOT {n:02d} \(([^)]+)\)', SPEC)
    cam = cam_m.group(1) if cam_m else 'MEDIUM · eye-level · static'
    jobs.append({'n': n,
                 'kf': f'/workspace/keyframes/kf_{n:02d}_start.png',
                 'out': f'/workspace/out/p23_s{n:02d}_v2.mp4',
                 'seed': 200 + n,
                 'prompt': compose(n, cam)})

out = '/a0/usr/projects/vast/tools/vast/jobs/p23_batch60_v2.json'
json.dump(jobs, open(out, 'w'), indent=1)
print('wrote', out, len(jobs), 'jobs')
for j in jobs[:2] + jobs[20:22] + jobs[47:49]:
    print(f"--- S{j['n']:02d} seed={j['seed']}")
    print(j['prompt'][:260])
    print()
