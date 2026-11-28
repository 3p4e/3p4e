# Foton Tunland v2: 10 energetic commercials for Foton Macedonia (LTX 2.5, 5 s clips from Gemini start keyframes).
# Design rules from RESEARCH.md: one physical proof moment per film, dust/water/snow bursts, low tracking, drone scale,
# colour-pop paint on desaturated landscapes, night-city reflections, macro montage on the beat, interior calm vs exterior storm,
# speed ramps and all type in post. Avoid for LTX: jumps, drifts, multi-vehicle action, hands, readable screens, animals.
# Claims only from foton.mk: 2.0 L VGT + 48V, 129 kW, 450 Nm, 8-speed AT, 4x4; G7 2.0 L Cummins 450 Nm; 5 y / 100,000 km warranty.
# Paint names are the eight on the dealer's site (Flare White, Galaxy Silver, Titanium Grey, Phantom Black, Fire Red,
# Diamond Blue, Lightning Purple, Aurora Green).
DISCLOSURE = "Видео изработено со вештачка интелигенција · AI-generated video"
SHOT_STYLE = ("Photorealistic premium automotive commercial cinematography, crisp detail, the pickup keeps its exact shape, "
              "wheels and paint, one pickup truck only, no other vehicles, no text.")
NEGATIVE = ("blurry, warped vehicle, melting body, morphing, deformed wheels, extra wheels, extra vehicles, duplicate truck, "
            "text, subtitles, watermark, logo overlay, flicker, low quality, cartoon, CGI look")
KF_STYLE = (" Photorealistic premium automotive commercial still, 16:9, cinematic colour grade, the pickup composed near the "
            "centre of the frame, no text, no watermark, no captions, no other vehicles, no people unless described.")
V9 = ("the Foton Tunland V9 double-cab pickup from the reference photo (same wide hexagon-mesh grille with FOTON lettering above it, "
      "slim LED headlights, colour-coded front bumper, black wheel-arch flares, black side steps, roof rails, sports bar, "
      "black multi-spoke wheels), painted {paint}; keep everything except the paint identical to the reference")
G7 = ("the blue Foton Tunland G7 double-cab pickup from the reference photo (same chrome-framed grille with FOTON lettering, "
      "headlights, bumper, body and wheels); keep it identical to the reference")
PAINT = {"red": "Fire Red, a deep glossy metallic red", "black": "Phantom Black, a deep glossy metallic black",
         "green": "Aurora Green, a rich dark metallic green", "grey": "Titanium Grey, a dark metallic gunmetal grey",
         "white": "Flare White, a bright solid white", "blue": "Diamond Blue, a vivid metallic blue",
         "purple": "Lightning Purple, a deep metallic violet", "silver": "Galaxy Silver, a bright metallic silver"}
V7 = ("the dark teal-blue Foton Tunland V7 double-cab pickup from the reference photo (same large grille, vertical LED headlights, black lower bumper, "
      "black wheel-arch flares, six-spoke black wheels, roof rails); keep it identical to the reference")
REF = {"V9": "foton/ref/v9.png", "G7": "foton/ref/g7.png", "V7": "foton/ref/v7.png"}


def veh(model, paint=None): return V9.format(paint=PAINT[paint]) if model == "V9" else (V7 if model == "V7" else G7)


# segment helpers: (src_from, src_to, speed, flag); 'adj' absorbs the timing so every shot is a whole number of beats
def N(a=0.2, b=4.6): return [(a, b, 1.0, "adj")]
def RAMP(a, p, q, b): return [(a, p, 1.25, ""), (p, q, 0.35, "adj"), (q, b, 1.7, "")]
def SLOW(a=0.4, b=2.6): return [(a, b, 0.6, "adj")]


FILMS = []


def film(fid, title, model, paint, bpm, music, card, vo, shots, accent="0xf2c14e", card_beats=8):
    """shots: (n, keyframe scene, motion prompt, segments, beats[, flag 'hit'][, strength])"""
    defs, cut = [], []
    for s in shots:
        n, kf, mo, segs, beats = s[:5]; flag = s[5] if len(s) > 5 else ""; sid = f"{fid}_s{n}"
        defs.append({"id": sid, "kf": kf, "motion": mo, "ref": REF[model], "strength": s[6] if len(s) > 6 else 0.75})
        cut.append((sid, segs, beats, 0.5, flag))
    FILMS.append({"id": fid, "title": title, "model": model, "paint": paint, "bpm": bpm, "music": music, "card": card,
                  "vo": vo, "shot_defs": defs, "shots": cut, "accent": accent, "card_beats": card_beats})


# 1. DUST BURST: Fire Red against a grey quarry (colour pop, dust-burst reveal, low tracking, drone scale)
v = veh("V9", "red")
film("fv01_probij", "Пробиј", "V9", "red", 124, "fv_dust",
     ("TUNLAND V9", "Пробиј ги границите.", "2.0 L турбо дизел · 48V хибрид · 450 Nm · 4×4"),
     [("l1", 1), ("l2", 13), ("l3", 26), ("cta", 35)], [
      (1, f"A thick wall of grey dust hanging in a huge grey limestone quarry at golden hour, the glowing LED headlights and the red bonnet of {v} just emerging from the dust toward the camera, low angle.",
       "Low locked camera. The pickup bursts out of the dust cloud straight toward the lens, dust swirling off the bonnet and mirrors, the red paint catching the sun. The pickup fully out of the dust holds on the final frame.", RAMP(0.0, 1.4, 2.6, 3.6), 7, "hit"),
      (2, f"Low tracking shot at wheel height alongside {v} speeding across the gravel floor of a grey quarry, stones and dust kicking up from the tyres, strong motion blur on the ground.",
       "Fast low tracking shot alongside the pickup. Gravel sprays from the tyres and a long dust plume rolls behind. The pickup still at speed holds on the final frame.", N(0.3, 3.4), 6),
      (3, f"High drone shot looking down on {v} driving along a winding dirt road cut into the terraces of a vast grey quarry, a long trail of dust behind it, late afternoon light.",
       "Drone pulls back and rises, revealing the scale of the quarry as the small red pickup climbs the terraced road trailing dust. The wide view holds on the final frame.", N(0.2, 4.4), 6),
      (4, f"Extreme low close-up of the front wheel of {v} climbing over loose rock on a steep quarry ramp, dust and small stones spilling, the black wheel arch and red paint in frame.",
       "Close camera low at the wheel. The tyre grips and rolls over the loose rocks, stones tumble away, the suspension compresses. The wheel cresting the rock holds on the final frame.", SLOW(0.4, 2.6), 6),
      (5, f"Wide low hero shot of {v} standing on the rim of a grey quarry at sunset, sun flare behind it, a thin veil of golden dust drifting past, headlights on.",
       "Slow push-in toward the pickup. The drifting dust thins out and the sunset flare blooms behind the roof. The clean hero view holds on the final frame.", N(0.6, 4.8), 8)])

# 2. NIGHT CITY: Phantom Black on wet asphalt, light trails, reflections (urban premium daily)
v = veh("V9", "black")
film("fv02_nokjen_grad", "Ноќен град", "V9", "black", 124, "fv_night",
     ("TUNLAND V9", "Ноќта е твоја.", "2.0 L турбо дизел · 48V хибрид · 8-степен автоматски"),
     [("l1", 1), ("l2", 5), ("l3", 15), ("l4", 26), ("cta", 35)], [
      (1, f"Close-up of the slim LED headlight of {v} in total darkness, rain droplets on the glossy black paint, a city glow far behind.",
       "Locked macro shot. The LED headlight ignites in a sweeping line of white light, rain droplets sparkle on the black paint. The lit headlight holds on the final frame.", N(0.3, 3.0), 6, "hit"),
      (2, f"Low front three-quarter shot of {v} driving through a wet empty city boulevard at night, street lights and shop neon reflecting in puddles and along the glossy black paint, light rain.",
       "Camera tracks backward low in front of the pickup. Reflections of street lights slide across the bonnet and windscreen, spray lifts from the tyres. The pickup in the light-streaked street holds on the final frame.", N(0.2, 4.2), 7),
      (3, f"Side view of {v} crossing a modern bridge over a river at night, long-exposure feel with streaks of city light behind it, the black paint reflecting the city.",
       "Fast lateral tracking shot. The pickup glides across the bridge, city lights streak past behind it. The pickup in profile against the lit skyline holds on the final frame.", RAMP(0.0, 1.5, 2.5, 3.8), 6),
      (4, f"Top-down drone shot of {v} turning through an empty wet city intersection at night, glowing zebra crossing lines and reflections, headlights and red tail lights.",
       "Drone hovers directly overhead and slowly rotates as the pickup crosses the square, headlight beams sweeping across the wet paving. The pickup leaving the square holds on the final frame.", N(0.2, 4.4), 6),
      (5, f"Low hero shot of {v} parked on a rooftop car park at night, the lit city skyline behind it, wet floor reflecting the truck, headlights on.",
       "Slow push-in toward the pickup as a light mist drifts across the rooftop and city lights twinkle behind. The hero view holds on the final frame.", N(0.5, 4.7), 9)])

# 3. RIVER RUN: Aurora Green through a mountain river (water bow wave, riverbed tracking, drone)
v = veh("V9", "green")
film("fv03_reka", "Река", "V9", "green", 128, "fv_river",
     ("TUNLAND V9", "Таму каде што завршува патот.", "4×4 · 450 Nm · 8-степен автоматски"),
     [("l1", 1), ("l2", 8), ("l3", 22), ("cta", 37)], [
      (1, f"A forest dirt track ending at the bank of a clear mountain river in North Macedonia, {v} arriving at the edge, morning sun through pine trees.",
       "Locked wide shot from across the river. The pickup rolls to the water's edge and noses into the river, ripples spreading. The pickup entering the water holds on the final frame.", N(0.2, 4.4), 7),
      (2, f"Front three-quarter low angle of {v} charging through a shallow mountain river, a big wave of water bursting from the front bumper, droplets glittering in the sun.",
       "The pickup powers through the river, a bow wave sprays up over the bonnet and water streams off the body. The pickup mid-river in a burst of spray holds on the final frame.", RAMP(0.0, 1.0, 2.2, 3.6), 8, "hit"),
      (3, f"Low tracking shot alongside {v} driving fast along a dry stony riverbed between green mountains, water splashing from shallow puddles, motion blur on the stones.",
       "Fast low tracking shot alongside the pickup, splashes and stones flying from the tyres. The pickup still at speed holds on the final frame.", N(0.3, 3.6), 6),
      (4, f"Top-down drone shot of {v} crossing a turquoise mountain river, white water trailing behind it, green forest on both banks.",
       "Drone moves forward overhead following the pickup across the river, white water fanning behind. The pickup reaching the far bank holds on the final frame.", N(0.2, 4.2), 7),
      (5, f"Wide hero shot of {v} standing on river rocks with water dripping from its body, a mountain valley and morning mist behind, sun rays.",
       "Slow pull-back as water drips from the body and the morning mist drifts through the valley. The hero view holds on the final frame.", N(0.5, 4.7), 9)], accent="0x5fd08b")

# 4. STORM: Titanium Grey, interior calm vs exterior chaos (Amarok logic), rain and lightning
v = veh("V9", "grey")
film("fv04_nevreme", "Невреме", "V9", "grey", 120, "fv_storm",
     ("TUNLAND V9", "Мирен во секое невреме.", "5 години или 100.000 км гаранција"),
     [("l1", 1), ("l2", 9), ("l3", 18), ("l4", 27), ("cta", 34)], [
      (1, f"Dark stormy mountain road, heavy rain sheets, a lightning bolt lighting up the sky behind {v} driving toward the camera with headlights on.",
       "Locked low camera. Lightning flashes across the sky, rain lashes the road and the pickup drives through the downpour toward the lens. The pickup in the headlight glare holds on the final frame.", N(0.2, 4.0), 7, "hit"),
      (2, f"Inside the cabin of {v} at night: calm, warm ambient lighting, leather seats, a dark dashboard with soft glow, rain streaming down the windscreen and a storm outside, no hands on the wheel visible, no readable screen text.",
       "Slow push-in toward the windscreen from the back seat. Rain streams down the glass and distant lightning flickers outside while the cabin stays calm and softly lit. The calm cabin view holds on the final frame.", N(0.3, 4.5), 9, "", 0.8),
      (3, f"Low close-up of the rear wheel of {v} pushing through a deep muddy puddle in pouring rain, a sheet of muddy water flying sideways.",
       "Low camera beside the wheel. The tyre ploughs through the puddle and a sheet of muddy water flies out in slow motion. The wheel driving on holds on the final frame.", SLOW(0.4, 2.4), 7),
      (4, f"Drone shot from behind {v} driving along a winding mountain road in a storm, red tail lights, wet road shining, dark clouds and rain curtains over the valley.",
       "Drone follows from behind and above as the pickup winds through the bends, rain curtains sweeping across the valley. The tail lights disappearing into the bend hold on the final frame.", N(0.2, 4.2), 6),
      (5, f"Hero shot of {v} parked at a mountain viewpoint as the storm clears, wet paint glistening, the first sun rays breaking through dark clouds behind it.",
       "Slow push-in as the clouds part and sun rays sweep across the wet bodywork. The hero view holds on the final frame.", N(0.5, 4.7), 8)], accent="0x9fb4c8")

# 5. WINTER PASS: Flare White in snow (snow plume, drone, sunrise)
v = veh("V9", "white")
film("fv05_zima", "Зима", "V9", "white", 124, "fv_snow",
     ("TUNLAND V9", "Подготвен за зима.", "4×4 · 2.0 L турбо дизел · 48V хибрид"),
     [("l1", 1), ("l2", 4), ("l3", 15), ("l4", 26), ("cta", 35)], [
      (1, f"Blue dawn on a snowy mountain pass, frost on {v} parked under snow-laden pine trees, headlights just switching on, breath-like mist in the cold air.",
       "Locked wide shot. The headlights flare on and snow dust drifts from the pine branches. The pickup glowing in the blue dawn holds on the final frame.", N(0.3, 3.4), 6),
      (2, f"Low front three-quarter shot of {v} ploughing through fresh deep snow on a mountain track, a big plume of powder snow exploding from the front bumper and wheels.",
       "The pickup drives through the deep snow, powder explodes from the bumper and wheels and sparkles in the light. The pickup in the snow cloud holds on the final frame.", RAMP(0.0, 1.2, 2.4, 3.8), 8, "hit"),
      (3, f"Low tracking shot alongside {v} driving along a snowy forest road, snow spraying from the tyres, white pine forest blurring past.",
       "Fast low tracking shot alongside the pickup, snow spraying from the tyres. The pickup at speed holds on the final frame.", N(0.3, 3.6), 6),
      (4, f"High drone shot of {v} climbing a serpentine snowy mountain road in a vast white landscape, tyre tracks behind it, sunrise light on the peaks.",
       "Drone rises and pulls back revealing the white mountains as the small pickup climbs the hairpins. The wide view holds on the final frame.", N(0.2, 4.4), 6),
      (5, f"Hero shot of {v} on a snowy summit at sunrise, warm golden light on the white paint, snow crystals glittering in the air, peaks behind.",
       "Slow orbit toward the front three-quarter view as snow crystals glitter in the sunrise. The hero view holds on the final frame.", N(0.5, 4.7), 9)], accent="0x8fd3ff")

# 6. PRECISION: Diamond Blue macro montage on the beat (studio)
v = veh("V9", "blue")
film("fv06_detali", "Детали", "V9", "blue", 124, "fv_detail",
     ("TUNLAND V9", "Изграден до детал.", "129 kW · 450 Nm · 8-степен автоматски"),
     [("l1", 1), ("l2", 9), ("l3", 17), ("l4", 26), ("cta", 35)], [
      (1, f"Dark studio, extreme close-up of the slim LED headlight and the edge of the hexagon-mesh grille of {v}, a thin line of light grazing the blue paint.",
       "Slow lateral slide along the headlight. A sweep of light runs across the grille mesh and the headlight ignites. The lit headlight holds on the final frame.", N(0.2, 2.2), 4, "hit"),
      (2, f"Dark studio, macro shot of the black multi-spoke wheel and the black wheel-arch flare of {v}, rim light on the blue paint, thin haze.",
       "The wheel turns slowly as a rim light sweeps across the spokes and the arch. The wheel at rest holds on the final frame.", N(0.3, 3.6), 4),
      (3, f"Dark studio, macro shot along the shoulder line and side mirror of {v}, a strip light reflection gliding along the glossy metallic blue paint.",
       "Slow dolly along the body side, the strip light reflection travels along the paint and mirror. The mirror in focus holds on the final frame.", N(0.3, 3.6), 4),
      (4, f"Interior macro only, no exterior visible: tight close-up of a black diamond-stitched leather front seat and the edge of a softly glowing centre console inside the cabin of {v}, warm ambient light strip, shallow depth of field, no readable text, no other car visible.",
       "Slow push-in across the stitching as the ambient light shifts from warm to cool. The stitching in focus holds on the final frame.", N(0.3, 3.6), 4, "", 0.92),
      (5, f"Dark studio, low rear three-quarter of {v}, the tail light lit, thin smoke drifting along the floor, strong rim light on the blue paint.",
       "The tail lights glow brighter and smoke rolls along the floor as the camera slides low around the corner. The rear three-quarter view holds on the final frame.", N(0.3, 3.6), 4),
      (6, f"Dark studio, wide front three-quarter hero shot of {v} on a glossy black floor, a ring of light overhead, smoke clearing, headlights on.",
       "Slow push-in as the smoke clears and the overhead ring light brightens, reflections spread across the floor. The hero view holds on the final frame.", N(0.4, 4.6), 10, "hit")], accent="0x4aa3ff")

# 7. LIGHTNING PURPLE: tunnel, neon car park, bold urban (colour as identity)
v = veh("V9", "purple")
film("fv07_molnja", "Молња", "V9", "purple", 126, "fv_purple",
     ("TUNLAND V9", "Во боја на молња.", "8 бои · 48V хибрид · 4×4"),
     [("l1", 1), ("l2", 13), ("l3", 26), ("cta", 35)], [
      (1, f"Night city tunnel, low front three-quarter shot of {v} speeding toward the camera, LED headlights blazing, streaks of orange tunnel lights reflecting along the glossy paint, motion blur on the walls.",
       "Camera tracks backward fast in front of the pickup through the tunnel, the tunnel lights streak over the paint. The pickup bursting toward the tunnel exit holds on the final frame.", RAMP(0.0, 1.3, 2.4, 3.8), 7, "hit"),
      (2, f"Empty multi-storey car park lit with magenta and cyan neon strips, {v} parked diagonally, neon reflecting in the glossy violet paint and the polished concrete floor.",
       "Slow low orbit around the front of the pickup, neon reflections slide across the bonnet and doors. The front three-quarter view holds on the final frame.", N(0.3, 4.3), 6),
      (3, f"Low side tracking shot of {v} driving along a wet street lined with neon shop signs at night, purple and blue reflections on the road, light rain.",
       "Fast lateral tracking shot, neon lights streak past behind the pickup and spray lifts from the tyres. The pickup in profile holds on the final frame.", N(0.2, 3.6), 6),
      (4, f"Close-up of the violet bonnet and windscreen of {v} driving under a row of bright overhead city lights at night, light bars sliding across the paint.",
       "Locked camera on the bonnet as lines of light slide rhythmically across the violet paint and the glass. The glowing bonnet holds on the final frame.", N(0.3, 3.6), 6),
      (5, f"Hero shot of {v} parked at the top of a city parking deck at night, lightning flashing in the distant clouds, city lights below, headlights on.",
       "Slow push-in as distant lightning flashes and briefly lights the violet paint. The hero view holds on the final frame.", N(0.5, 4.7), 9, "hit")], accent="0xb36bff")

# 8. TOW PROOF: Galaxy Silver pulls a boat out of Lake Ohrid (one truck, one trailer, outcome not hitching)
v = veh("V9", "silver")
film("fv08_vlecna_sila", "Влечна сила", "V9", "silver", 118, "fv_tow",
     ("TUNLAND V9", "Влече без напор.", "450 Nm · 8-степен автоматски · 4×4"),
     [("l1", 1), ("l2", 13), ("l3", 25), ("cta", 34)], [
      (1, f"A wet concrete boat ramp on a calm lake at sunrise, mountains on the far shore, {v} with a white motor boat on a trailer behind it rising out of the water up the ramp, water pouring off the trailer.",
       "Locked low camera at the top of the ramp. The pickup pulls the boat steadily up out of the lake, water pours off the hull and trailer. The boat clear of the water holds on the final frame.", N(0.2, 4.4), 8, "hit"),
      (2, f"Low close-up of the rear wheel of {v} gripping the wet ramp, water spraying lightly, the trailer wheel behind it.",
       "Low camera beside the wheel. The tyre bites into the wet ramp and turns steadily as water drips away. The turning wheel holds on the final frame.", SLOW(0.4, 2.6), 6),
      (3, f"Drone shot of {v} towing a white motor boat on a trailer along a lakeside road at golden hour, the blue lake and mountains beside the road.",
       "Drone tracks alongside and above as the pickup and trailer cruise along the lakeside road. The pickup and boat on the road holds on the final frame.", N(0.2, 4.4), 7),
      (4, f"Rear three-quarter shot of {v} towing the boat trailer up a steep hill road out of the lake town, the lake glittering below.",
       "Camera tracks alongside as the pickup tows the boat steadily along the road above the city. The pickup and boat on the road hold on the final frame.", N(0.2, 4.4), 6),
      (5, f"Hero shot of {v} with the boat trailer parked on a hill above the lake at sunset, warm light on the silver paint, the lake and mountains behind.",
       "Slow push-in as the sun sets over the lake and warm light slides along the silver body. The hero view holds on the final frame.", N(0.5, 4.7), 8)], accent="0xc9d1d9")

# 9. WORK SHIFT: Tunland G7 (blue, as on the dealer's site) at dawn on a construction site (Navara 'grit shift' realism)
v = veh("G7")
film("fv09_raboten_den", "Работен ден", "G7", None, 122, "fv_work",
     ("TUNLAND G7", "Работи колку и ти.", "2.0 L Cummins дизел · 450 Nm · 4×4"),
     [("l1", 1), ("l2", 5), ("l3", 16), ("l4", 27), ("cta", 35)], [
      (1, f"5 a.m. pre-dawn at a construction site, work floodlights on, {v} parked with its headlights on, light fog, steel frames and a crane silhouette behind.",
       "Locked wide shot. The headlights flare on and the floodlights hum as fog drifts through the light beams. The pickup glowing in the fog holds on the final frame.", N(0.3, 3.6), 6),
      (2, f"Low tracking shot alongside {v} driving across a muddy construction site at dawn, mud splashing from the tyres, lumber and steel in the load bed.",
       "Fast low tracking shot alongside the pickup, mud flies from the tyres and the load shifts slightly in the bed. The pickup at speed holds on the final frame.", N(0.3, 3.6), 7, "hit"),
      (3, f"Rear three-quarter close shot of the load bed of {v} loaded with cement bags, the suspension settling under the weight, a worker's silhouette walking away in the background, dawn light.",
       "Locked camera. The suspension settles as the load sits in the bed and dust drifts in the dawn light. The loaded bed holds on the final frame.", N(0.3, 3.6), 6),
      (4, f"Drone shot of {v} driving out of a construction site onto a road at sunrise, long shadows, the city skyline in the distance.",
       "Drone pulls up and back as the pickup leaves the site and heads toward the city. The pickup on the road at sunrise holds on the final frame.", N(0.2, 4.4), 7),
      (5, f"Hero shot of {v} parked by the half-built steel frame at sunrise, the sun breaking through the structure behind it, dust in the air.",
       "Slow push-in as sun rays break through the steel frame and the dust glows. The hero view holds on the final frame.", N(0.5, 4.7), 8)], accent="0x3b82f6")

# 10. EIGHT COLOURS: one hero move per colour, two beats each, ending on the line-up
SC = [("white", "a white salt flat at noon"), ("silver", "a steel-and-glass modern architecture plaza"), ("grey", "a dark basalt rock canyon"),
      ("black", "a wet night street with neon reflections"), ("red", "a grey limestone quarry with dust in the air"),
      ("blue", "a mountain lake shore at morning"), ("purple", "a city tunnel at night with streaking lights"), ("green", "a pine forest track with sun rays")]
shots10 = []
for i, (p, place) in enumerate(SC, 1):
    shots10.append((i, f"{veh('V9', p).capitalize()} in {place}, low front three-quarter angle, dramatic light on the paint, dynamic composition.",
                    "Fast push-in toward the front three-quarter view as light sweeps across the paint. The pickup holds sharply on the final frame.",
                    N(0.2, 3.0), 4 if i < 8 else 6, "hit" if i in (1, 5) else ""))
film("fv10_osum_boi", "Осум бои", "V9", "multi", 124, "fv_colour",
     ("TUNLAND V9", "Осум бои. Еден карактер.", "8 бои · 2.0 L турбо дизел · 48V хибрид · 4×4"),
     [("l1", 1), ("l2", 17), ("l3", 26), ("cta", 35)], shots10)



# 11. PELISTER EYES (owner's request): Tunland V7 on Pelister / Baba mountain above Bitola; ends at a viewpoint over the two glacial
# lakes (Pelister is a national park: mountain road and tracks only, never driving to the lake shore)
v = veh("V7")
film("fv11_pelisterski_oci", "Пелистерски Очи", "V7", None, 120, "fv_alpine",
     ("TUNLAND V7", "Погледни подалеку.", "2.0 L турбо дизел · 48V хибрид · 450 Nm · 4×4"),
     [("l1", 1), ("l2", 11), ("l3", 25), ("cta", 35)], [
      (1, f"Dawn in a forest of tall Macedonian pine (molika) on Pelister mountain, mist between the trunks, sun rays, {v} climbing a gravel mountain road with headlights on.",
       "Low tracking shot alongside the pickup as it climbs through the pine forest, sun rays flicker through the trunks and dust lifts from the gravel. The pickup climbing holds on the final frame.", N(0.2, 4.2), 7),
      (2, f"Above the treeline on Pelister mountain, a rough rocky track through granite boulder fields, low front angle of {v} crawling over the rocks, one front wheel lifted, alpine grass and big sky.",
       "Low camera in front. The pickup crawls steadily over the granite rocks, the wheels articulate and the body tilts and settles. The pickup over the rocks holds on the final frame.", SLOW(0.4, 2.8), 7, "hit"),
      (3, f"Epic high drone shot of {v} small on a winding mountain road along the ridge of Baba mountain (Pelister), a sea of clouds in the valleys below, golden morning light.",
       "Drone pulls back and rises as the small pickup follows the ridge road above the sea of clouds. The vast mountain view holds on the final frame.", N(0.2, 4.4), 7),
      (4, f"Low tracking shot alongside {v} on a high alpine gravel track on Pelister, granite boulders and alpine meadow, dust trail, deep blue sky.",
       "Fast low tracking shot alongside the pickup, gravel and dust kick up from the tyres. The pickup at speed holds on the final frame.", RAMP(0.0, 1.4, 2.4, 3.8), 7),
      (5, f"Golden hour hero shot from behind and above {v} parked at a rocky mountain viewpoint on Pelister, looking down at the two small glacial lakes, Pelister Eyes (the Big Lake and the Small Lake), dark blue water in a granite cirque far below, peaks around.",
       "Slow crane up over the pickup, revealing the two glacial lakes in the granite cirque below as golden light spreads across the peaks. The view of the lakes beyond the pickup holds on the final frame.", N(0.5, 4.7), 9, "hit")], accent="0x6ec6ff")

# 12-15: made from existing keyframes only (no new image credits); generic motion as rendered
GM = "The pickup moves smoothly through the scene, or stays parked while the camera glides slowly around it; natural dust, water or light; the truck keeps its exact shape and badges."
v = veh("V7")
film("fv12_patuvanje", "Патување", "V7", None, 128, "fv_river",
     ("TUNLAND V7", "Секој пат е твој.", "2.0 L турбо дизел · 48V хибрид · 450 Nm · 4×4"),
     [("l1", 1), ("l2", 11), ("l3", 25), ("cta", 35)], [
      (1, f"Dawn on an open country road, {v} driving toward the camera, soft mist and warm low sun.", GM, N(0.2, 4.4), 7),
      (2, f"{v} on a winding mountain road, forested slopes and peaks behind.", GM, N(0.2, 4.4), 7),
      (3, f"{v} crossing an old stone bridge over a mountain river.", GM, SLOW(0.4, 2.8), 7, "hit"),
      (4, f"{v} on a lakeside road, calm water and mountains behind.", GM, N(0.2, 4.4), 7),
      (5, f"Hero shot of {v} parked by a lake at golden hour.", GM, N(0.5, 4.7), 9, "hit")], accent="0x6ec6ff")
v = veh("V9", "black")
film("fv13_sumrak", "Самрак", "V9", "black", 124, "fv_night",
     ("TUNLAND V9", "Градот е твој.", "2.0 L турбо дизел · 48V хибрид · 8-степен автоматик"),
     [("l1", 1), ("l2", 9), ("l3", 23), ("cta", 35)], [
      (1, f"{v} on a city street at dusk, lit facades and glowing street lights.", GM, N(0.2, 4.4), 7),
      (2, f"{v} crossing a lit bridge at night, reflections on the river.", GM, N(0.2, 4.4), 7, "hit"),
      (3, f"{v} driving through the city at night, light streaks.", GM, RAMP(0.0, 1.4, 2.4, 3.8), 7),
      (4, f"{v} with the night skyline behind.", GM, N(0.2, 4.4), 7),
      (5, f"Hero shot of {v} parked above the city lights at night.", GM, N(0.5, 4.7), 9, "hit")], accent="0xb9c2d0")
v = veh("V9", "red")
film("fv14_ekspedicija", "Експедиција", "V9", "red", 124, "fv_dust",
     ("TUNLAND V9", "Таму каде што патот исчезнува.", "450 Nm · погон 4×4 · блокада на диференцијал"),
     [("l1", 1), ("l2", 11), ("l3", 25), ("cta", 35)], [
      (1, f"{v} driving through a dusty canyon, dust trail behind.", GM, RAMP(0.0, 1.4, 2.4, 3.8), 7, "hit"),
      (2, f"{v} on a high ridge track, wide sky.", GM, N(0.2, 4.4), 7),
      (3, f"{v} crossing a river, water splashing from the wheels.", GM, SLOW(0.4, 2.8), 7, "hit"),
      (4, f"{v} climbing a rocky trail toward the summit.", GM, N(0.2, 4.4), 7),
      (5, f"Hero shot of {v} on the summit at golden hour.", GM, N(0.5, 4.7), 9, "hit")], accent="0xff5a4e")
v = veh("G7")
film("fv15_nosivost", "Носивост", "G7", None, 122, "fv_work",
     ("TUNLAND G7", "Товари повеќе. Стигни подалеку.", "2.0 L турбо дизел · 4×4 · голема товарна површина"),
     [("l1", 1), ("l2", 9), ("l3", 23), ("cta", 35)], [
      (1, f"{v} with a loaded cargo bed, ready for the road.", GM, N(0.2, 4.4), 7),
      (2, f"{v} on the highway with cargo in the bed.", GM, RAMP(0.0, 1.4, 2.4, 3.8), 7),
      (3, f"{v} at a port container terminal, stacked containers.", GM, N(0.2, 4.4), 7, "hit"),
      (4, f"{v} at dusk, long shadows, cargo secured.", GM, N(0.2, 4.4), 7),
      (5, f"Hero shot of {v} under the port cranes.", GM, N(0.5, 4.7), 9, "hit")], accent="0x4aa3ff")

# ---- Skopje setting (owner's request): city and nearby-nature shots placed in and around Skopje, plus three QC fixes
SKP = "in Skopje, North Macedonia"
SKOPJE = {
 # night city: Vardar quay, Stone Bridge, Macedonia Square, Vodno with the lit Millennium Cross
 "fv02_nokjen_grad_s1": "Close-up of the slim LED headlight of {v} at night on the Vardar river quay in Skopje, rain droplets on the glossy black paint, the lit Stone Bridge blurred in the background.",
 "fv02_nokjen_grad_s2": "Low front three-quarter shot of {v} driving along a wet, empty boulevard in central Skopje at night, the illuminated Stone Bridge and Skopje Fortress walls behind, street lights reflecting in puddles and along the glossy black paint, light rain.",
 "fv02_nokjen_grad_s3": "Side view of {v} driving along the riverside road on the Vardar quay in Skopje at night (on the road, not on the pedestrian Stone Bridge), the lit Stone Bridge beside it, streaks of city light behind it, the lit Skopje Fortress (Kale) on the hill in the background, the black paint reflecting the city.",
 "fv02_nokjen_grad_s4": "Top-down drone shot of {v} driving across the empty wet Macedonia Square in Skopje at night, glowing paving patterns and reflections, the large equestrian statue on its fountain at the edge of frame.",
 "fv02_nokjen_grad_s5": "Low hero shot of {v} parked on a rooftop car park in Skopje at night, the city lights below and Vodno mountain with the lit Millennium Cross on its summit behind, wet floor reflecting the truck, headlights on.",
 # lightning purple: Skopje streets and parking deck, no foreign signage
 "fv07_molnja_s1": "Night underpass on a Skopje boulevard, low front three-quarter shot of {v} speeding toward the camera, LED headlights blazing, streaks of orange lights reflecting along the glossy paint, motion blur on the walls.",
 "fv07_molnja_s3": "Low side tracking shot of {v} driving along a wet street in central Skopje at night, illuminated neoclassical facades and the Vardar quay lights behind, purple and blue reflections on the road, light rain, signs without readable text.",
 "fv07_molnja_s5": "Hero shot of {v} parked at the top of a city parking deck in Skopje at night, lightning flashing over Vodno mountain and the lit Millennium Cross, city lights below, headlights on.",
 # storm above the city: Vodno road
 "fv04_nevreme_s1": "Dark stormy road on Vodno mountain above Skopje, heavy rain sheets, a lightning bolt over the city lights in the valley behind {v} driving toward the camera with headlights on.",
 "fv04_nevreme_s2": "Inside the cabin of {v} at night, left-hand drive (steering wheel on the left side): calm, warm ambient lighting, leather seats, a dark dashboard with soft glow, rain streaming down the windscreen, the lights of Skopje blurred beyond the glass during a storm, no hands, no readable screen text.",
 "fv04_nevreme_s4": "Drone shot from behind {v} driving along the winding Vodno mountain road in a storm, red tail lights, wet road shining, rain curtains over Skopje in the valley below.",
 "fv04_nevreme_s5": "Hero shot of {v} parked at a viewpoint on Vodno mountain as the storm clears, wet paint glistening, Skopje spread out in the valley below, the first sun rays breaking through dark clouds.",
 # river: Matka Canyon and the Treska river just outside Skopje
 "fv03_reka_s1": "A dirt track ending at the bank of the Treska river in Matka Canyon near Skopje, steep limestone canyon walls, {v} arriving at the water's edge, morning sun.",
 "fv03_reka_s2": "Front three-quarter low angle of {v} charging through a shallow stretch of the Treska river below the limestone walls of Matka Canyon near Skopje, a big wave of water bursting from the front bumper, droplets glittering in the sun.",
 "fv03_reka_s4": "Top-down drone shot of {v} crossing the turquoise Treska river in Matka Canyon near Skopje, white water trailing behind it, steep green canyon walls on both banks.",
 "fv03_reka_s5": "Wide hero shot of {v} standing on river rocks in Matka Canyon near Skopje with water dripping from its body, the canyon walls and morning mist behind, sun rays.",
 # winter: Vodno in snow above Skopje
 "fv05_zima_s4": "High drone shot of {v} climbing the snowy serpentine road up Vodno mountain, tyre tracks behind it, Skopje in the valley below at sunrise.",
 "fv05_zima_s5": "Hero shot of {v} on the snowy summit of Vodno at sunrise next to the large white Millennium Cross, warm golden light on the white paint, snow crystals glittering, Skopje far below.",
 # tow: Lake Treska (Matka) near Skopje; s4 trailer straight behind the truck
 "fv08_vlecna_sila_s1": "A wet concrete boat ramp on calm Lake Treska near Skopje at sunrise, wooded hills on the far shore, {v} with a white motor boat on a trailer directly behind it rising out of the water up the ramp, water pouring off the trailer.",
 "fv08_vlecna_sila_s4": "Rear three-quarter shot of {v} towing a white motor boat on a trailer hitched directly behind it in a straight line, climbing a hill road above Skopje, the city and Vodno mountain below.",
 # work shift: Skopje construction site and skyline
 "fv09_raboten_den_s1": "5 a.m. pre-dawn at a construction site in Skopje, work floodlights on, {v} parked with its headlights on, light fog, steel frames and a crane silhouette behind, Vodno mountain with the Millennium Cross faint in the distance.",
 "fv09_raboten_den_s4": "Drone shot of {v} driving out of a construction site onto a road at sunrise, long shadows, the Skopje skyline and Vodno mountain with the Millennium Cross in the distance.",
 # eight colours: two of the city scenes in Skopje
 "fv10_osum_boi_s2": "{V} on Macedonia Square in Skopje, neoclassical facades behind (no statue in frame, no text anywhere on buildings or monuments), low front three-quarter angle, dramatic light on the paint, dynamic composition.",
 "fv10_osum_boi_s4": "{V} on a wet street by the Vardar river quay in Skopje at night, the lit Stone Bridge behind, neon reflections, low front three-quarter angle, dramatic light on the paint, dynamic composition.",
}
_V = {f["id"]: f for f in FILMS}
for sid, txt in SKOPJE.items():
    fid = sid.rsplit("_s", 1)[0]; f = _V[fid]
    paint = dict(zip(range(1, 9), [p for p, _ in SC]))[int(sid.rsplit("_s", 1)[1])] if fid == "fv10_osum_boi" else f["paint"]
    vv = veh(f["model"], paint)
    d = [x for x in f["shot_defs"] if x["id"] == sid][0]; d["kf"] = txt.format(v=vv, V=vv[0].upper() + vv[1:])

if __name__ == "__main__":
    tot = 0
    for f in FILMS:
        beat = 60 / f["bpm"]; secs = (sum(s[2] for s in f["shots"]) + f["card_beats"]) * beat; tot += len(f["shots"])
        for sid, segs, beats, _, _ in f["shots"]:
            fixed = sum((b - a) / s for a, b, s, fl in segs if fl != "adj"); a0, b0 = [(a, b) for a, b, s, fl in segs if fl == "adj"][0]
            adj = (b0 - a0) / max(0.2, beats * beat - fixed)
            if not 0.3 <= adj <= 1.9: print("  CHECK speed", sid, round(adj, 2))
        print(f["id"], f["model"], f["paint"], f["bpm"], "bpm", len(f["shots"]), "shots", round(secs, 1), "s")
    print("total clips", tot)
