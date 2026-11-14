#!/usr/bin/env python3
"""Build p23_batch60_v4.json — high-contrast ACTION rewrite of all 60 motion prompts.
Director decree 2026-11-14: NO PowerPoint zoom stills. Every clip = visible physical action,
hard chiaroscuro contrast, environmental dynamics, motion blur. 'Slow motion' banned.
Base beats extracted from storybook_ocr/specs/23_GROK_60_KEYFRAME_PROMPTS.md."""
import json, re

ROOT = '/a0/usr/projects/vast'
PACK = ROOT + '/storybook_ocr/specs/23_GROK_60_KEYFRAME_PROMPTS.md'
OUT = ROOT + '/tools/vast/jobs/p23_batch60_v4.json'

# Per-shot VISCERAL motion clauses — subject acts, world reacts, camera energised.
# Keyed by shot number. Each replaces the bland 'continuation' phrasing of v2.
V4 = {
 1: "Violent storm-action: wind SLAMS Perseus's cloak flat against his body and whips it sideways in gusts, rain streaks diagonally across frame in hard sheets, his hand rises to shield his eyes, lightning FLASHES and freezes the spray mid-air, his jaw sets with resolve — the sea heaves white-capped behind him",
 2: "Kinetic hall-scene: Perseus STRIDES to the megaron centre and plants his feet wide, fist clenched over his heart, firelight FLARES as the brazier gusts, embers spiral upward past his face, his voice drives the vow — dust motes swirl in hard shafts of window light, his shadow lunges on the columns behind",
 3: "Supernatural entrance: storm light EXPLODES white as Athena materialises, air pressure visibly distorts in a shock-ring, her cloak snaps taut in the blast, her owl SCREECHES and drops onto her shoulder with wings still beating, her eyes lock onto Perseus with divine intensity — debris and leaves spiral in the vortex",
 4: "Horror reveal with kinetic dread: the cave BREATHES — steam jets from cracks in sharp bursts, water drips strike the stone in visible splashes, Medusa's hair-snakes HISS and strike at the air in snapping motions, her tail coils and uncoils with heavy muscular waves, torchlight JITTERS from Perseus's trembling grip",
 5: "Explosive arrival: Hermes CRASHES down through the storm in a controlled dive, winged sandals kicking up a pressure-burst of spray and dust, he lands in a crouch that cracks the flagstone, his caduceus SPARKS with sharp electric arcs, he springs upright with restless energy — rain boils off his heat-shimmer",
 6: "Ritual action: Athena SLAMS the harpe onto the stone table point-first so it quivers, Hermes SNAPS the kibisis open with both hands, fabric CRACKS like a sail, gifts slide across the table in a cascade — torch flames ROAR sideways in the draught, every face lit by hard flicker",
 7: "Weapon focus: Perseus's fist CLOSES around the harpe grip, knuckles whitening, he hefts it and the adamant edge CATCHS the light in a hard specular streak, he makes a practice slash that SINGS through the air — the blade's reflection whips across his face",
 8: "Gear action: the kibisis CRACKS open, bronze catches firelight in hot glints, Perseus tests the strap with a sharp tug, the sack's mouth gapes like a living thing — dust puffs from its folds as it snaps taut",
 9: "Shield reveal: the Gorgon Aegis is RAISED into frame and the mirrored face REFLECTS the whole room in warped distortion, Perseus pivots it and the reflection sweeps the walls, torchlight detonates across the polished bronze in a roaming highlight",
 10: "The helmet of Hades is slammed down and SHADOW ERUPTS from it in visible rolling waves, swallowing the light around Perseus's silhouette — the darkness churns like smoke as he turns his head testing the gloom",
 11: "The winged sandals STRAP on and the wings BLUR into motion with a hummingbird beat, Perseus's feet leave the stone in a kick-off that scatters dust, he HOVER-bounces testing lift — feathers shed and spiral in the torch-draught",
 12: "Full-armour sequence: Perseus SNAPS the kibisis onto his belt, twists the harpe into his grip, rolls his shoulders so the cloak whips — every motion crisp and weaponised, his eyes burning under the helmet brim — the complete kill-kit assembled in flowing action",
 13: "Launch: Perseus SPRINGS off the cliff-edge and the sandals CATCH with a wing-burst, spray erupts from the kick-off point below, he CLIMBS hard against the storm, rain lashing horizontally past camera — a true flight start, not a drift",
 14: "Flight-action: Perseus DRIVES forward over a heaving black sea, wave-tops EXPLODE white below him, he banks hard and the horizon tilts, cloud-walls rip past at speed — the camera races to keep pace",
 15: "Island approach in violent motion: the skiff SLAMS into swells and spray sheets over the prow, Perseus braces legs wide against the roll, the island's cliffs LOOM with waterfalls blown sideways by wind, gulls TUMBLE past in the gale",
 16: "Cave-mouth dread in motion: the entrance gapes like a throat, steam PULSES outward in rhythm, the petrified sentries' frozen cloaks still strain in the wind, Perseus SLIPS between them in a low combat crouch, harpe half-drawn — ash and grit stream across the floor",
 17: "Petrified-warrior sequence: Perseus MOVES through the statue-field in quick wary steps, his torch REFLECTIONS race across carved eyes, a frozen warrior's spear points at his throat — he ducks under it in real time, cloak snapping, dust exploding from the stone at his touch",
 18: "Shield-reflection scene with kinetic tension: the mirror-shield's surface TREMBLES in Perseus's grip, the reflected Medusa shifts as he inches forward step by silent step, a hair-snake STRIKES the shield's rim in the reflection and he FLINCHES hard — sweat drops fly",
 19: "Stalking action: Perseus creeps in a combat crouch, each footfall placed with deliberate care, the harpe RISES to strike-angle, his breathing visible in sharp mist-bursts, torch smoke whips past — coiled-spring energy in every muscle",
 20: "AMBUSH EXPLOSION: Medusa's eyes SNAP open in a lightning-flash, her tail THUNDERS as she lunges across the stone, jaws wide, claws extended, debris scattering — the attack is a full-body ballistic strike, hair-snakes screaming forward like spears",
 21: "IMPACT COMBAT: her claws RAKE across the raised shield in a shower of orange sparks, the bronze RINGS and vibrates, Perseus is driven back two sliding steps, boots carving dust-trails, his counter-slash WHISTLES through empty air where her head was — sparks and dust fill the frame",
 22: "Blade-storm: Perseus SPINS in a full arc, harpe tracing a silver circle, three hair-snakes STRIKE simultaneously and are severed — their bodies thrash and spasm on the stone, ichor sprays in black arcs, Medusa recoils with a mouth-wide scream",
 23: "Weapon-catch action: the harpe's hook SNAGS Medusa's guard and Perseus YANKS her off-balance, her claws SCRABBLE and gouge stone tracks, their momentum spins them both across the cavern in a brutal grapple-dance — dust and pebbles cascading from the ceiling",
 24: "First blood: the harpe's tip GRAZES Medusa's shoulder in a fast flick, ichor JETS in a thin black arc, she SNAPS back with a recoil that slams her tail against the wall, stone fragments ricochet — Perseus's eyes widen at the wound he drew",
 25: "Second hook: Perseus feints left then RIPS the harpe up in a rising diagonal, the hook CATCHES her jaw-guard and her head is wrenched sideways, hair-snakes whip in panic-strikes that crack the air — his boots skid as he hauls on the blade",
 26: "THE KILL: Perseus puts his full body-weight behind a single descending CLEAVE — the harpe shears through in a decisive arc, ichor ERUPTS in a fountain, Medusa's body CRASHES to the stone and convulses, the severed head TUMBLES in slow-arcing horror — the frame shakes with the impact",
 27: "Terror aftermath: the Gorgons SHRIEK in unison, the cave's bats EXPLODE from the roost in a panicked black cloud, stone dust RAINS from the cracked ceiling, Perseus sprints through the chaos with the head held high like a torch — everything moves at once",
 28: "Miracle-burst: the stump ERUPTS and Pegasus VIOLENCE-BURSTS forth in a spray of ichor, wings UNFURL in one thunderclap, he rears and SCREAMS, hooves flailing sparks from stone, and LAUNCHES upward with a thrust that shatters the ground — a true explosion of birth",
 29: "Escape-flight under pursuit: Pegasus CLIMBS steeply, Perseus flattened against the neck, the Gorgons' spears THUNK into rock below, the island drops away fast, wind RIPS at the cloak — full-speed aerial chase energy",
 30: "Pursuit-action: a Gorgon HURLS a javelin that spears past camera-close, Pegasus banks HARD and the horizon rolls 40 degrees, Perseus nearly loses the kibisis and claws it shut mid-turn — sky, sea and fury in motion",
 31: "Open-sea flight: Pegasus levels out and DRIVES forward, spray whipped off wave-tops in horizontal streamers, Perseus rises to a crouch on the saddle testing balance, the horizon JUDDERS with speed — pure velocity",
 32: "PEGASUS APPROACH — VIOLENT DESCENT: the winged horse DIVES out of storm-cloud at full tilt, wings BEATING the air in powerful downstrokes that kick visible vortices, spray ERUPTS from the sea beneath the wingtips, Perseus LEANS into the dive gripping the mane — the beach and chained figure RUSH up to meet them",
 33: "Landing-impact: Pegasus's hooves STRIKE the shingle in an explosion of stones and spray, skids three metres carving furrows, wings folding in whip-cracks — Perseus dismounts in a running leap before they fully stop",
 34: "Confrontation: Perseus MARCHES up the beach toward the crowd, harpe raised so the edge flashes, his voice carrying over the surf, the crowd RECOILS step by step, a priest's staff RATTLES as his hands shake — hard push-pull blocking in motion",
 35: "The sea BOILS: the ketos's back BROACHES the surface in a slow-mountain surge, water SHEETS off barnacled hide in waterfalls, the creature's exhale BLASTS a mist column ten metres high — scale and power made kinetic",
 36: "Roar-and-recoil: the ketos OPENS a cavernous maw and ROARS, the sound-blast flattens the surf outward in a ring, gulls TUMBLE from the sky, the crowd SCATTERS screaming, chains RATTLE against the rock — everything reacts to the sound",
 37: "Chain-action: Andromeda YANKS against the bronze chains in desperation, the links CLANG taut and score the rock, her feet slip on spray-slick stone, the ketos's shadow LOOMS over her growing with each swell — struggle made physical",
 38: "The vow in motion: Perseus STEPS onto the sacrificial rock, points the harpe at the sea-beast, then turns and SPEARS the chains apart in three ringing strikes — links SPIN away in glittering arcs, Andromeda's arms drop free — decisive chained-action",
 39: "Battle-join: the ketos STRIKES like a whip, Perseus DIVES aside in a combat-roll, spray ERUPTS where he stood, he comes up slashing — the blade SKIMS scales in a line of sparks, the beast's tail SMASHES the rock where Andromeda cowered",
 40: "Mid-battle beat: Perseus and the ketos CIRCLE each other in the foam, the harpe weaving figure-eights of reflected light, the serpent's head TRACKS it like a mesmerised snake, spray fills the air between them — coiled mutual violence",
 41: "The tail-blow: the ketos's tail SCYTHES horizontally, Perseus LEAPS over it in a tucked jump, the tail DETONATES the rock-face behind in a burst of shrapnel — he lands already running toward the head",
 42: "Climb-and-strike: Perseus SCALES the beast's own back as it rears, digging the harpe in as a piton, ichor streaming, reaches the skull and RAISES the blade — the ketos thrashes to throw him, sea erupting around them",
 43: "The fall: the ketos SLAMS its own back against the rock to dislodge him — Perseus is FLUNG into the surf in an explosion of white, comes up gasping with the harpe still in fist, spitting blood and salt — the beast wheels for the kill-bite",
 44: "Desperation-move: Perseus FUMBLES the kibisis open one-handed while swimming, the head's face SLIDES into view, he twists to keep his own eyes averted, the ketos's maw GAPES above him descending — timed to the half-second",
 45: "PRESENTATION: Perseus HURLS the kibisis wide and swings the severed head up by its hair in one continuous whip-motion, the head's dead eyes SWEEP toward the beast, the ketos's pupils SNAP into contact — the freeze-frame moment is EARNED by the violent wind-up",
 46: "Gaze-lock aftermath: petrification RACES across the ketos's hide as a visible grey WAVE, the thrash decays strike by strike, the maw FREEZES millimetres from Perseus — water cascades off the arresting body in sheets",
 47: "Shatter-scene: the petrified ketos CRACKS from within, fractures RACE across the stone-hide, and the whole mass COLLAPSES into the sea in a thunderburst of shards and foam — the splash reaches camera",
 48: "Andromeda's recount — KINETIC EMOTIONAL BEAT: her hands GESTURE the telling in sharp arcs, tears and sea-spray mix and fly from her chin as she shakes her head, wet hair SLAPS her shoulders in wind-gusts, her breath comes in visible sobs, the chains' broken ends still SWING beside her — grief in full-body motion, no stillness",
 49: "Aftermath connect: Perseus and Andromeda stand in the settling foam, both breathing hard, chests heaving, he reaches to steady her and she flinches then accepts the grip — small human motion against the epic wreckage, gulls wheeling in",
 50: "Crowd reversal: the scattered crowd CREEPS back in ones and twos, a fisherman DROPS to his knees in the shingle, others raise arms in disbelieving praise, the priest's staff CLATTERS down the rock — movement from flight to worship",
 51: "The reef revealed: waves BREAK over the petrified coils in rhythmic white bursts, gulls LAND on the stone-beast's snout and peck, spray JETS from the nostril-hollows with each swell — the dead monster as living seascape",
 52: "KETOS REAR — ESCALATED: the ketos VIOLENTLY EXPLODES upward from the foam in a full towering rear, water ERUPTS off its coiling length in cascading sheets, the maw GAPES wide with the roar visible as a pressure-distortion, eyes BLAZE with fixated rage, the sea surface BOILS white around the thrashing coils — maximum-creature violence",
 53: "Kibisis action: Perseus RIPS the sack open with a two-hand tear, the severed head SLIDES into his grip and he swings it free by the hair in one whip-arc, his own face TWISTED away — the weapon deployed in committed motion",
 54: "THE GAZE ACROSS THE WATER: Perseus THRUSTS the head forward at full arm-extension, the head's dead stare BORES across the sea, the ketos's raging eyes SNAP into lock-on and its whole body CONVULSES mid-lunge — two forces meeting across the spray",
 55: "Petrification-wave: grey stone-arrest RACES up the ketos's body in visible ripples, each coil FREEZES mid-thrash in sequence, spray hangs frozen around the arresting mass — transformation as action",
 56: "Collapse-of-stone: the petrified bulk SAGS, cracks THUNDER across it, and it DISINTEGRATES into the sea with a world-ending splash that drenches camera — the end of the threat as violent as its life",
 57: "Release-action: Perseus's harpe RINGS against the last chain-link and it SPINS away, Andromeda's freed arms FALL forward around his neck in a sudden grab, both drop to their knees in the wash — rescue completed in motion",
 58: "Storm-break: the clouds TEAR open in fast-moving rifts, sunlight SPEARS down in moving shafts across the water, the wind DROPS and the sea's rage visibly flattens — weather as actor in transition",
 59: "Return-flight: Pegasus ASCENDS in a climbing spiral, the coast FALLS away, both riders lean into the turn, wet cloaks STREAMING, the reef shrinking below — homeward velocity",
 60: "Final image in motion: they RIDE the last light toward the horizon, Pegasus's wings beating in slow powerful strokes, the sun-flare SWEEPING the lens as they cross it, sea glittering in hard speculars — an ending that moves until the cut",
}

CONTRAST = ("High-contrast cinematic action: bold chiaroscuro lighting, hard rim-light carving subjects "
            "from deep shadow, hot specular highlights on wet metal and spray, deep crushed blacks, "
            "visible motion blur on all fast-moving elements, 35mm anamorphic energy. ")
GUARDS = (" No new people, no bystanders appear. Faces, armour and proportions remain exactly as the start frame "
          "- no morphing, no drift. The camera movement named above is the only camera motion.")

text = open(PACK).read()
# Extract beats per shot: camera line + environment line from each block
jobs = []
for n in range(1, 61):
    pat = re.compile(rf"## SHOT {n:02d}.*?(?=## SHOT {n+1:02d}|\Z)", re.S)
    m = pat.search(text)
    if not m:
        print(f"MISSING SHOT {n}"); continue
    blk = m.group(0)
    cam = re.search(r"Camera: ([^\n]+)", blk)
    env = re.search(r"Environment: ([^\n]+)", blk)
    cam_s = cam.group(1).strip() if cam else ""
    env_s = env.group(1).strip() if env else ""
    motion = V4[n]
    prompt = (CONTRAST + motion + ". " + env_s + ". Camera: " + cam_s +
              " - continuous, no cuts, no angle changes." + GUARDS)
    jobs.append({
        "n": n,
        "kf": f"/workspace/keyframes/kf_{n:02d}_start.png",
        "out": f"/workspace/out/p23_s{n:02d}_v4.mp4",
        "seed": 200 + n,
        "prompt": prompt,
    })

assert len(jobs) == 60, f"jobs={len(jobs)}"
lens = [len(j['prompt']) for j in jobs]
print(f"jobs={len(jobs)} prompt_min={min(lens)} prompt_max={max(lens)} prompt_avg={sum(lens)//60}")
print("slow-motion check:", any('slow motion' in j['prompt'].lower() or 'slow-motion' in j['prompt'].lower() for j in jobs))
json.dump(jobs, open(OUT, 'w'), indent=1)
print("wrote", OUT)
