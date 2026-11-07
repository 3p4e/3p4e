#!/usr/bin/env python3
"""Build first-last-frame keyframe jobs for the Demon Hunter / Paladin boss fight.

Canon source: higgsfield/26_DEMONHUNTER_PALADIN_BOSSFIGHT_SPEC_v2.md (50 shots).
Emits one FLF job per shot with a START prompt and an END prompt.
Every prompt is composed from the locked character canon in that spec and is
validated against the 1400-character cap from 18_PROMPT_COMPOSITION_GUIDE.md.

  python3 build_bossfight_jobs.py --dry-run
  python3 build_bossfight_jobs.py --out jobfiles/bossfight_flf_jobs.json
"""
import argparse, json, sys

MAX_CHARS = 1400

# ---------------------------------------------------------------- canon locks
SCENE = ("charred obsidian gorge at dusk, cracked black rock, burnt dead trees, "
         "ash falling upward on an ember wind, distant heat shimmer, photoreal cinematic still")

DD = ("DD the demon hunter: lean male warrior in frost-rimed demon-hunter plate, hood up and face "
      "shadowed, short cropped cyan-teal hair with shaved sides and a swept top, twin infernal hand "
      "crossbows, glacial blue-white frost and violet-arcane glow about the armor")

AZ = ("Azulon the retribution paladin: bald clean-shaven strong-jawed man, a single molten-gold rune "
      "tattoo running from one brow across one eye and down the cheek to the jaw, bare head with no "
      "helmet, gold-trimmed plate, two-handed auric greatsword, gold-white holy light")

BOSS = ("Mal'garot the Ash Lord: colossal ember demon with a molten whip-arm, an exposed incandescent "
        "forge-core in the chest, a crown of dead coals, obsidian plating, swirling ash and fire, no "
        "human face and no recognizable features")

WHO = {"dd": DD, "az": AZ, "boss": BOSS}

NEG_BASE = ("duplicate face, extra face, second head, deformed hands, fused fingers, extra limbs, "
            "text, watermark, logo, cartoon, illustration, cel-shaded, low detail")
NEG_NOBEAM = NEG_BASE + ", laser beam from eye, glowing eye beam"

# ---------------------------------------------------------------- shot table
# (id, size, dur, camera, present, start staging, end staging)
SHOTS = [
 (1,"W",3.0,"dolly-in, embers drifting toward lens",["dd","az"],
  "two warriors stand small on a ridge above the gorge, seen wide, DD left in hooded frost plate, Azulon right with greatsword point-down",
  "the same two figures have stepped forward to the ridge lip, wind pulling ash past the lens"),
 (2,"W",2.5,"slow push-in, heat shimmer distortion",["dd","az"],
  "both warriors stand at the cliff edge, wide, full bodies in frame, ash gusting between them",
  "the same framing holds but the footing has cracked into spreading fissures as their weight shifts"),
 (3,"I",2.5,"insert, frost spreading across metal",["dd"],
  "extreme close insert on DD's gauntleted hand cocking a crossbow, frost crystals on the knuckles",
  "a crystalline frost-arrow has fully formed in the crossbow groove, rime spreading outward"),
 (4,"I",2.5,"insert, hair drifting like water",["dd"],
  "close insert of DD's short cropped cyan-teal hair, strands hanging still in the ember light",
  "the same hair now rolls in a slow weightless wave, its neon teal brightening as if lit from within"),
 (5,"I",2.5,"insert, light travelling along the arm",["az"],
  "close insert of Azulon's gauntleted hand gripping the greatsword hilt, bare wrist showing pale skin",
  "an ember-gold rune tattoo has woken along the wrist and forearm, light travelling up beneath the skin"),
 (6,"W",3.0,"low rise, ash falling upward",["boss"],
  "a wide low-angle shot of a mound of ash and coals in the gorge, nothing yet standing",
  "the Ash Lord has unfolded upward out of the ash into full height, crown of coals burning, torso looming"),
 (7,"C",2.5,"whip crack, camera shake",["boss"],
  "close shot on the Ash Lord's molten whip-arm coiled tight against its flank, glowing seams",
  "the whip-arm has snapped out straight toward the camera, trailing a hard wake of sparks"),
 (8,"M",2.5,"aura bloom, camera pulls back",["dd"],
  "medium shot of DD in hooded frost plate raising one arm, palm open, no effect yet",
  "a ring of white-blue frost has bloomed outward from his palm and is expanding across frame"),
 (9,"W",3.0,"whip-pan following the strike",["dd","boss"],
  "wide shot of the arena floor, DD braced low at left, the Ash Lord's whip-arm drawn back at right",
  "the whip has struck the ground near DD, gouging a long fire-furrow that sprays molten rock"),
 (10,"M",2.5,"sprint smear, whip-pan chase",["dd"],
  "medium shot of DD crouched to spring, crossbows low, frost gathering at his boots",
  "DD has launched into a rime-comet sprint, a hard streak of ice trailing behind him across the rock"),
 (11,"C",2.5,"bolts, slow-motion into real time",["dd"],
  "close shot over DD's shoulder, both crossbows levelled, strings still vibrating",
  "three crystalline frost-bolts streak away from the crossbows in a fan, frost contrails behind them"),
 (12,"I",2.5,"impact, crash-zoom",["boss"],
  "insert on the Ash Lord's obsidian cloak surface, seams glowing dull orange",
  "the cloak has flash-frozen in a hard white patch, ember spray curdling to snow at the edges"),
 (13,"W",2.5,"gold ring, low hold",["az"],
  "wide low shot of Azulon planting his greatsword tip to the rock, both hands on the pommel",
  "a gold shockwave ring has burst from the blade point, cracking the floor outward in a circle"),
 (14,"M",3.0,"orbit around the swing",["az","boss"],
  "medium shot of Azulon mid-windup, greatsword drawn back behind his shoulder, gold light gathering",
  "the Templar's Verdict arc has detonated on the Ash Lord's flank in a burst of gold-white light"),
 (15,"C",2.5,"recoil, push-in on the face plate",["boss"],
  "close shot of the Ash Lord's featureless mask of obsidian, intact and unmarked",
  "the mask has cracked across, and the forge-core in its chest flares bright enough to rim the cracks"),
 (16,"W",3.0,"sweep and vault, cross-cut framing",["dd","az","boss"],
  "wide shot of the Ash Lord drawing its ash-whip across the whole arena, both heroes grounded",
  "both heroes are airborne, vaulting in opposite directions, the whip sweeping beneath them"),
 (17,"M",2.5,"flip and land, whip-pan",["dd"],
  "medium shot of DD upside-down mid backflip, cape and hood trailing a frost wake",
  "DD has landed in a low crouch, one knee down, frost-smoke boiling off the impact point"),
 (18,"C",3.0,"beam ignition, rack focus",["dd"],
  "close shot of DD's shadowed face inside his hood, eyes dark and unlit",
  "both of DD's eyes have ignited and twin white-blue rime lances slash outward from them"),
 (19,"W",3.5,"tracking shot along the beam to the shatter",["dd","az","boss"],
  "wide shot of the Ash Lord's whip-arm mid-swing with DD's rime beam locking onto it, Azulon closing in",
  "the whip-arm has shattered, golden shockwave tearing through the ice and spraying frozen fragments wide"),
 (20,"M",2.5,"recoil, push",["boss"],
  "medium shot of the Ash Lord staggering back, frozen arm hanging wrong, cracks packed with ice",
  "the Ash Lord has thrown its head back and roars, the frozen arm fracturing apart at the shoulder"),
 (21,"W",3.0,"explosion of shards, wide",["boss"],
  "wide shot of the Ash Lord armored and intact, obsidian plates sealed across its chest",
  "the armour has blown off, the forge-core fully exposed and blazing, obsidian shards raining down around it"),
 (22,"C",2.5,"blade descending, tilt up",["az"],
  "close shot of Azulon raising his greatsword overhead, gold light gathering along the blade",
  "a colossal light-blade has summoned above him, hanging point-down, ready to descend"),
 (23,"M",3.0,"blade drop followed by a pan",["az","boss"],
  "medium shot of the summoned light-blade hanging above the Ash Lord, both in frame",
  "the light-blade has plunged through and the Ash Lord staggers inside a white pillar of light"),
 (24,"W",3.0,"crane up over the shockwave",["boss"],
  "wide shot of the Ash Lord rearing up, both fists raised above the rock floor",
  "both fists have slammed the ground and a black rain of embers is falling across the whole gorge"),
 (25,"M",2.5,"close on the wings, shield hiss",["dd"],
  "medium close shot of DD curling down behind his spread Immortal wings, membrane taut",
  "embers are hissing to snow on the wing membrane, white steam curling off in ribbons"),
 (26,"M",3.0,"dolly-back as he advances",["az"],
  "medium shot of Azulon walking forward through falling ember rain, sword low at his side",
  "he has advanced further, gold light shedding the embers off him like water, unharmed"),
 (27,"I",2.5,"flame column insert",["boss"],
  "insert on the Ash Lord's throat and jaw plates, seams glowing hot",
  "a column of obsidian-shot flame has erupted from its mouth and is blasting down-frame"),
 (28,"W",3.0,"split-action framing, wide",["dd","az","boss"],
  "wide shot of a gout of flame cutting the arena in two, DD left, Azulon right",
  "DD is vaulting clean over the gout while Azulon charges through its shadow beneath him"),
 (29,"W",3.0,"cone sweep across the floor",["az"],
  "wide shot of Azulon standing square, greatsword raised, holy light building at his feet",
  "a white flame cone has scoured outward across the ground, ash burning to clean glass in its path"),
 (30,"C",3.0,"wind-up, push-in on the coils",["dd"],
  "close shot of DD in hooded plate, wings half-furled, snow spiralling slowly around him",
  "his wings have folded tight and the snow coils have concentrated into a hard spinning halo at his shoulders"),
 (31,"W",3.5,"aerial dive, crater impact",["dd"],
  "wide aerial shot of DD high above the gorge, crossbows first, body angled down",
  "DD has lanced down into the ground, a frozen trail behind him and a crater opening at the impact"),
 (32,"M",3.0,"impact and kneel, camera shake",["boss"],
  "medium shot of the Ash Lord upright, forge-core flickering weakly in its chest",
  "the Ash Lord is forced down to one knee inside the impact crater, core sputtering"),
 (33,"C",3.5,"orbit through mark, freeze and detonation",["dd","az","boss"],
  "close shot of a gold Execution Sentence rune burning onto the exposed forge-core",
  "the rune has detonated in a column of light through DD's locking ice, blasting the core white-hot"),
 (34,"C",2.5,"grip and runes, orbit",["az"],
  "close shot of Azulon's hands re-gripping the greatsword hilt, knuckles pale",
  "holy runes have blazed to life up the length of the blade, gold light pouring off the steel"),
 (35,"W",3.0,"swell into vortex, wide",["boss"],
  "wide shot of the Ash Lord wounded and kneeling, embers drifting loose around it",
  "it has swollen larger, embers spiralling into a burning vortex that fills the gorge"),
 (36,"C",2.5,"mask close-up for the line",["boss"],
  "close shot of the Ash Lord's cracked mask, no human features, ember light behind the cracks",
  "the mask has shifted as it speaks, the cracks glowing brighter, ash spilling from the seams"),
 (37,"W",3.5,"supernova rise, crane up",["boss"],
  "wide shot of the Ash Lord with arms spread, forge-core building a hard white point",
  "a supernova of embers has risen off it, a burning dome climbing over the entire gorge"),
 (38,"M",3.0,"wing flare, orbit",["dd"],
  "medium shot of DD grounded with wings tight to his back, crossbows held low",
  "his wings have flared wide to full span and his crossbows are raised, glacier energy peaking in blue-white"),
 (39,"M",3.0,"tattoo surge, rack focus to wings",["az"],
  "medium shot of Azulon planting both hands together, bald head down, tattoo dull gold",
  "his rune tattoo is surging from gold to white-hot and great golden wings have bloomed from his back"),
 (40,"W",2.5,"held wide, embers only",["dd","az","boss"],
  "wide held shot of both heroes facing the Ash Lord, ember-nova burning above them",
  "the same held wide composition, nothing moved but the embers drifting through frame"),
 (41,"M",3.0,"leap into full form, aerial",["dd"],
  "medium shot of DD crouched, wings folded, snow gathering at his feet",
  "DD has leapt into full Glacier Form, Immortal wings spread wide, a snowstorm breaking around him"),
 (42,"M",3.0,"rise and halo, tilt",["az"],
  "medium shot of Azulon kneeling, greatsword point-down, head bowed",
  "he has risen off the ground, radiant, greatsword burning white-gold, a halo of light behind his head"),
 (43,"W",3.0,"twin dive, aerial",["dd","az","boss"],
  "wide aerial shot of both heroes launching from opposite sides toward the burning core",
  "a fel-frost streak and a gold streak are winding around each other as they drive at the core"),
 (44,"C",3.0,"beam and shot, slow motion",["dd","boss"],
  "close shot of DD mid-air, eyes igniting and all crossbows aimed at the exposed core",
  "a violet-white lance has punched through the core as every crossbow fires at once, slow-motion debris"),
 (45,"C",3.0,"final slash, core splits",["az","boss"],
  "close shot of Azulon at the apex of his final Verdict arc, blade white-gold and screaming",
  "the core has split open along the slash and blinding light is flooding out of it"),
 (46,"W",3.0,"collapse, wide pull-back",["dd","az","boss"],
  "wide shot of the ember supernova at full bloom, both heroes silhouetted against it",
  "the supernova has collapsed inward on itself, light and ember crushing down to a single point"),
 (47,"I",2.5,"crown cracks and falls, inset",["boss"],
  "inset on the Ash Lord's crown of dead coals, still seated and glowing dull",
  "the crown has cracked through and is falling apart, coals dropping away in pieces"),
 (48,"W",3.0,"ash drift, wide",["dd","az","boss"],
  "wide shot of the extinguished core smoking at the centre of the arena, ash thick in the air",
  "the ash has settled over two standing silhouettes above the dead core, everything grey and still"),
 (49,"C",3.0,"hood lowered, breath and frost, close-up",["dd"],
  "close shot of DD standing with hood up, embers guttering low around him",
  "DD has lowered his hood revealing his face, and he exhales a thin wisp of frost into the cold air"),
 (50,"W",3.0,"turn and walk, dolly following",["az"],
  "wide shot of Azulon facing away over the dead core, greatsword resting point-down",
  "he has turned and walks away with the greatsword over his shoulder as dawn light pierces the ash"),
]


# Blocking law from higgsfield/28_BLOCKING_AND_STAGING_LAW.md — mandatory preamble.
# A fight is a geometry problem: prompt geometry before costume.
BLOCKING = ("Blocking: 3/4 side cam, low 24mm, never frontal. "
            "DD+Azulon torso+head at boss, weapons to boss; Azulon half-step back. "
            "Boss faces them centre-right, clear silhouette. "
            "Sightlines converge, no body faces lens. ")


def compose(shot, phase):
    sid, size, dur, cam, who, start, end = shot
    body = start if phase == "start" else end
    cast = " ".join(WHO[w] for w in who)
    frame = "first frame" if phase == "start" else "final frame"
    tail = (f"{frame} of a photoreal cinematic shot in {SCENE}. "
            f"Present: {cast}. "
            f"Action: {body}. "
            f"Camera/motion: {cam}. "
            f"Style: photoreal, anamorphic, high detail, 1280x720.")
    return BLOCKING + tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="jobfiles/bossfight_flf_jobs.json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    jobs, errors = [], []
    total_dur = 0.0
    for s in SHOTS:
        sid, size, dur, cam, who, start, end = s
        total_dur += dur
        for phase in ("start", "end"):
            p = compose(s, phase)
            if not p.startswith("Blocking:"):
                errors.append(f"shot {sid:02d} {phase}: missing blocking preamble")
            if len(p) > MAX_CHARS:
                errors.append(f"shot {sid:02d} {phase}: {len(p)} chars > {MAX_CHARS}")
            neg = NEG_NOBEAM if ("az" in who and sid not in (18,)) else NEG_BASE
            if sid == 18:
                neg = NEG_BASE
            jobs.append({
                "id": f"bf_{sid:02d}_{phase}",
                "shot": sid, "phase": phase, "size": size, "duration": dur,
                "cast": who, "prompt": p, "negative_prompt": neg,
                "width": 1280, "height": 720, "steps": 40,
            })

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print("  ", e)
        return 1

    ids = [j["id"] for j in jobs]
    assert len(ids) == len(set(ids)) == 100, f"expected 100 unique jobs, got {len(set(ids))}"
    print(f"shots              {len(SHOTS)}")
    print(f"jobs (start+end)   {len(jobs)}")
    print(f"runtime            {total_dur:.1f} s  (spec target ~150 s)")
    print(f"max prompt chars   {max(len(j['prompt']) for j in jobs)}")
    print(f"min prompt chars   {min(len(j['prompt']) for j in jobs)}")
    print(f"with DD            {sum(1 for j in jobs if 'dd' in j['cast'])}")
    print(f"with Azulon        {sum(1 for j in jobs if 'az' in j['cast'])}")
    print(f"with boss          {sum(1 for j in jobs if 'boss' in j['cast'])}")

    if a.dry_run:
        print("\n--- sample: shot 19 start ---")
        print(next(j["prompt"] for j in jobs if j["id"] == "bf_19_start"))
        print("\nDRY RUN OK")
        return 0

    import os
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        json.dump({"model": "Wan2.1-FLF2V-14B-720P", "license": "apache-2.0",
                   "shots": len(SHOTS), "jobs": jobs}, f, indent=1)
    print(f"\nwrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
