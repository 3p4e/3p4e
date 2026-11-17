#!/usr/bin/env python3
"""VAST #23 — re-author all 65 motion prompts to CONTINUATION-form (unified model-doc anti-slop standard).
Rules applied (official LTX-2 guide + note-42 + 39 + 40 + STUDY_DIGEST, captured to Open Brain):
  describe ONLY what moves next (one active present-tense verb-phrase); NEVER re-describe the scene/
  character/lighting the START keyframe already carries; identity ONCE at most; ONE flowing paragraph;
  camera sentence + post-motion endpoint; name the ONE physics violated; never contradict the keyframe;
  no generic 'motion continues' filler. Scene change = hard cut to a new keyframe, never A->B in one clip.
Reads tools/vast/jobs/p23_wan65.json (kf/seed/out); writes tools/vast/jobs/p23_k6_continuation.json.
"""
import json, os

# CONTINUATION-form prompt per shot id (authored from each shot's beat; keyframe carries identity/scene).
P = {
"1":"A seabird wheels past the citadel walls as the crane settles to a wide of the torch-lit terrace below, the storm-flattened sea glittering under bruise-dark cloud; the take resolves with the walls small beneath the moving sky and low thunder rolling in.",
"2":"Perseus kneels, then rises to one knee, lifting his chin to the king; the push-in ends tight on his set jaw, torch-flame guttering across the bronze at his shoulder, the megaron doors groaning behind them.",
"3":"His brow tightens, knuckles whitening on the spear-haft; the static frame holds as he draws one slow breath, torchlight crawling across the resolved line of his face.",
"4":"Dust sifts from the cave roof and a hair-snake lifts, tasting the dark; the crane-down settles on the coiled form as the shadows stop moving, one thin hiss threading the silence.",
"5":"A snake-hair lash crosses the frame and the slit-pupil eyes snap toward camera; the push-in ends with her breath fogging the lens, scales rippling up the throat as the hiss sharpens.",
"6":"Golden light blooms and Athena steps forward, spear grounded; the pan-left ends with her haloing the kneeling hero, wind pulling at her aegis as the crest settles.",
"7":"Athena extends the mirror-shield and Perseus takes it, thumbs finding the rim; the push-in ends on the polished bronze catching his downcast eye, torch-smoke curling between them.",
"8":"Hermes tilts the harpe so the edge flashes, winged sandals and helm set at his feet; the static close-up ends with Perseus's hand closing on the grip, a feather drifting off-frame.",
"9":"Athena turns, one hand raised, and Perseus nods; the steady two-shot ends with her lowering her arm, the words spent between them, storm-light shifting across the terrace.",
"10":"He closes his eyes, then opens them; the push-in ends on the quiet nod settling into resolve, a muscle jumping once at his jaw, the bronze going still.",
"11":"Perseus walks, cloak snapping in the ridge-wind, shield slung; the wide holds then eases in, ending with him small against the darkening mountains, gravel sliding underfoot.",
"12":"He polishes the mirror-shield in a slow arc as he walks, checking his own face in the bronze; the push-in ends with his reflection steady, the ridge dropping away behind.",
"13":"Wind pushes dust across the broken-tooth cliffs; the crane-up ends on the cave mouth swallowing the light, the scattered stone figures unmoving in the gloom.",
"14":"The pan drifts past the petrified warrior, frozen mid-step; it ends held on his stone-scream face, a loose pebble the only thing still rolling.",
"15":"Perseus's fingers tighten on the shield-strap, whitened knuckles; the push-in ends with his eyes lifting from the stone warriors to the dark beyond, breath slow and controlled.",
"16":"He closes his eyes, exhales, and opens them; the static frame holds through the beat, ending with his weight shifting forward onto the balls of his feet.",
"17":"Perseus backs into the dark, shield raised to read the cave behind; the wide eases in, ending with the light narrowing to a slit over his shoulder as the dark takes him.",
"18":"A ripple crosses the mirror-shield, the cave bending in its curve; the macro holds as the reflection stills, one hair-snake sliding through the polished bronze.",
"19":"Medusa uncoils from the stone bed, serpent-hair unfurling in slow waves; the crane-down ends with her rising to full height, dust and scale-sheen falling off her shoulders.",
"20":"She lunges, claws outstretched, the frame shuddering; the push-in ends with her jaws filling the lens, stone-chips spraying as the strike lands home.",
"F01":"Her clawed palms slam the raised Gorgon Aegis and orange sparks burst off the bronze; both fighters strain, Perseus driven to one knee, her jaws inches from the rim as the impact-ring echoes and the hair-snakes scream forward around the clash.",
"F02":"Her tail scythes low and Perseus leaps it, cloak snapping, dust exploding in the wake; the whip-pan tracks him clearing the sweep as one hair-snake strikes up and misses by a breath.",
"F03":"Six hair-snakes lash out at once from flank, overhead and low while her claws follow; Perseus weaves two, harpe deflects a third, the rest missing by centimetres, his face set in total focus.",
"F04":"She has him off the column and sliding down the cracked stone, harpe still fisted, one hand braced; the wide eases in as she coils over the impact-point, hissing, hair-snakes spread like a crown.",
"F05":"Her claw crushes his sword-wrist to the stone and her jaws descend; Perseus wedges the Aegis edge-up between them, saliva threading onto the mirrored bronze, his eyes defiant, knuckles white on the rim.",
"F06":"He goes limp, eyes half-closed, grip loose; Medusa rears high for the kill, jaws wide, weight committed — and in the foreground his free hand closes silently on the fallen harpe, his eyes open and locked on her throat.",
"F07":"Perseus explodes up in a rising diagonal slash that opens her flank in a line of black ichor; her body arches, mouth wide in the first scream of pain, the harpe extended through the follow-through, spray suspended across the torchlight.",
"F08":"He angles the Aegis so Medusa meets her own reflection; the first true fear crosses her face, her petrifying gaze thrown back, both freezing mid-exchange as the hair-snakes recoil from the mirror-image, Perseus watching over the rim.",
"F09":"The harpe's hook snags her guard and Perseus hauls with his full body-weight, boots skidding furrows in the stone; she is dragged off-balance toward him, tail thrashing for traction, hair-snakes whipping in panic, the two locked in one diagonal line of force.",
"F10":"Both hands on the harpe, Perseus raises the blade to apex, body a drawn bow of muscle, feet planted on her pinned guard; Medusa's eyes lock on the descent-path, jaw set, hair-snakes stretched in a last futile strike, the whole fight's weight held in one still.",
"26":"The harpe cleaves through and Medusa's form goes still; the push-in ends as the cavern holds its breath, dust settling through the torchlight, the echo dying.",
"27":"The serpents slow, the fateful gaze dimming in the severed head; the static close-up holds until the last coil relaxes, the green ember of the eyes cooling to grey.",
"28":"Perseus lowers the head into the kibisis and draws the cord tight; the pan-right ends with the sack settling against his hip, his hands still steady, the bronze of the Aegis catching light.",
"29":"Medusa's burning eyes find her own reflection in the polished bronze and lock, unable to look away; the static frame holds as the gaze that petrifies turns inward, the mirror holding her.",
"30":"Perseus sprints out of the dark into storm-grey light, cloak streaming; the crane-up ends with him small against the open sky, the cave-mouth exhaling dust behind him.",
"31":"Pegasus stamps and throws his head, wings half-furled; the crane-down ends on the snowy winged horse waiting under the storm-grey sky, steam blowing from his nostrils.",
"32":"Perseus extends a hand and Pegasus lowers his head into it; the push-in ends with palm against muzzle, the great wing settling over them both.",
"33":"Pegasus spreads his white wings and launches, Perseus low on his back; the crane-up ends with the pair rising into the grey, the cliff dropping away, spray kicked up by the wingbeats.",
"34":"Two Gorgon sisters burst from the cave-mouth, shrieking up at the escaping rider; the crane-down ends with their wings of shadow unfurling, claws reaching at the empty sky.",
"35":"Pegasus and Perseus soar out over the open sea, the kibisis secured; the tracking holds on the rhythm of the wingbeats, ending with the sack swinging gently against the sky.",
"36":"The crane settles down the jagged rock toward the lone chained figure, waves pounding below; it ends on the iron bright at the wrists, spray bursting white against the stone.",
"37":"Andromeda strains the chains once, then stills, wind whipping her tunic and dark hair; the push-in ends tight on her lifted chin, the sea roaring beneath the ledge.",
"38":"The two sisters burst from the deeper dark, shrieking, wings unfurling; the static frame holds as the cavern answers, stone sifting down around their rising forms.",
"39":"Andromeda's tear-streaked face turns and hope breaks across it; the static close-up ends with her lips parting, the wind catching her hair, eyes finding something off-frame.",
"40":"Perseus does not look back; he raises the Aegis against the shriek and clutches the kibisis; the push-in ends on his set jaw, the sack gripped white-knuckle tight.",
"41":"Pegasus lands on the ledge and Perseus swings down toward the chains; the crane-up ends with his boots hitting stone, wings folding behind him.",
"42":"Grey stone races up the first pursuer's body as the gaze she chased catches her; the crane-down ends with her freezing at the cave-mouth, wings mid-beat, gone to living rock.",
"43":"Perseus's hands work the iron at Andromeda's wrists, links giving; the static close-up ends with the last ring parting, her freed hands falling forward.",
"44":"Andromeda settles behind Perseus as Pegasus lifts into the open sky; the tracking holds through the ascent, ending with the rock shrinking beneath them, her arms finding his waist.",
"45":"Gratitude breaks across Andromeda's face and a tearful smile comes; the static close-up ends with her hand over her heart, the wind drying the tears on her cheeks.",
"46":"Pegasus glides high above the sea with both riders, a distant coast ahead; the crane-up ends with them small and steady against the brightening water, wing-shadow racing the waves.",
"47":"Andromeda speaks and Perseus listens, the wind taking her words; the steady two-shot ends with him turning his head a degree toward her, the horizon sliding past.",
"48":"Memory and shame cross Andromeda's eyes as she recounts her mother's offense; the push-in ends with her gaze dropping, then lifting, steadier, the sea-light moving on her face.",
"49":"The crane drops toward the sea as a scaled back breaks the surface, foam sheeting off it; it ends with the serpent churning a slow circle, the water standing up around the coil.",
"50":"The sea serpent's head rises from the foam, fanged maw opening; the push-in ends with the black gullet filling the lens, seawater sheeting off the fangs, the roar low and wet.",
"51":"Andromeda faces the memory with steady courage, chin lifting; the static frame holds as her breathing settles, fear banked behind her eyes.",
"52":"The ketos rears over the rock, a mountain of scale and foam; the crane-up ends with the sea standing up to take its offering back, spray hanging in the light.",
"53":"Perseus draws the kibisis open with one hand, eyes already turned away; the static frame holds as the terrible weight of the head swings free, the cord humming taut.",
"54":"The serpent's eyes find the head's stare across the water and the whole sea goes still; the crane-down ends with the moment held, not a ripple moving between them.",
"55":"The ketos goes grey stone mid-coil, waves breaking over the fossilised body; the static frame holds as the new reef of living-stone takes the surf, foam crawling up the frozen scales.",
"56":"The storm eases for the first time and Andromeda's hand finds Perseus's arm; the push-in ends with them turning from the sea together, the light breaking gold across the water.",
"57":"Realisation dawns across Perseus's face as the pan-right settles on him; it ends with his eyes widening, then narrowing to purpose, a breath taken and held.",
"58":"Two hands clasp above the flying horse's neck, fingers interlocking; the push-in ends with the grip tightening, the wingbeat lifting them into the resolve.",
"59":"Pegasus descends toward the white-walled city glowing at dusk; the crane-up ends with the coastal light opening beneath them, torns pricking awake along the walls.",
"60":"The family rushes the gates as Pegasus settles and the pair stand safe; the pull-back ends with the reunion small inside the glowing city, wings folding, the story closing home.",
}

def main():
    src=json.load(open('tools/vast/jobs/p23_wan65.json'))
    out=[]
    for j in src:
        sid=j['shot']
        key = sid if sid in P else (str(int(sid)) if sid.isdigit() and str(int(sid)) in P else sid.lstrip('0'))
        p = P.get(key)
        assert p, f"no continuation prompt for shot {sid} (tried {key})"
        out.append({'n':j['n'],'shot':sid,'kf':j['kf'],
                    'out':j['out'].replace('_wan','_k6c').replace('/workspace/out_wan/','/workspace/out_k6c/'),
                    'seed':j['seed'],'prompt':p})
    dst='tools/vast/jobs/p23_k6_continuation.json'
    json.dump(out,open(dst,'w'),ensure_ascii=False,indent=1)
    print(f"WROTE {dst}: {len(out)} jobs; all_prompts_len>40={all(len(j['prompt'])>40 for j in out)}")
    for j in out[:2]: print(f"  {j['shot']}: {j['prompt'][:60]}...")
    print(f"  ... F01: {out[20]['prompt'][:60]}...")

if __name__=='__main__':
    main()
