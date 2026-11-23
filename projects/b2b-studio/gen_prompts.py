"""Builds LTX_PROMPTS.md: continuation-form LTX 2.5 prompts (doc 67 sec.2) for the B2B video studio."""
import hashlib
STYLE = "Photorealistic commercial cinematography, natural light, shallow depth of field, crisp detail, subtle film grain, calm premium pacing."
C = []  # (category, note, [(name, keyframe, prompt)])
def add(cat, note, stages): C.append((cat, note, stages))

add("1. Construction Timelapse", "Same locked wide camera position for all 8 stages; each stage's end frame becomes the next stage's start keyframe.", [
 ("Excavation", "Wide elevated view of an empty urban plot at dawn, bare earth, a yellow excavator and two dump trucks at rest, surveyor stakes with orange tape.",
  "Locked wide shot from the same elevated corner. The excavator arm swings down and lifts a bucket of earth, dumps it into a truck, and repeats as the pit steadily deepens and a second truck rolls in. The pit holds at full depth with the excavator parked at its edge on the final frame. " + STYLE),
 ("Foundation", "Same wide view, deep excavated pit with rebar mats laid across the base and a concrete pump truck parked at the edge.",
  "Locked wide shot, same position. The pump boom extends over the pit and pours a gray concrete stream while workers in hard hats guide the hose and level the surface, which smooths into a flat slab. The finished slab holds, wet and glistening, on the final frame. " + STYLE),
 ("Structure", "Same wide view, ground-floor concrete columns rising from the slab with a tower crane beside them.",
  "Locked wide shot, same position. The tower crane lifts a formwork panel and swings it into place as concrete floors rise one level after another and the column grid climbs. The frame holds on a four-storey concrete skeleton against the sky. " + STYLE),
 ("Envelope", "Same wide view, completed concrete skeleton with scaffolding on the facade.",
  "Locked wide shot, same position. Facade panels and glass windows rise on the crane hook and snap onto the frame floor by floor as scaffolding slides away from the surface. The sealed building with glazed windows holds on the final frame. " + STYLE),
 ("MEP", "Same wide view, sealed glazed shell, cut-away feel showing one open floor with ducts and cable trays.",
  "Locked wide shot, same position. Electricians and pipefitters move along the open floor installing ductwork, cable trays and pipes in a quick rhythm while lights come on floor by floor. The lit, fully serviced floor holds on the final frame. " + STYLE),
 ("Fit-out", "Interior wide view of an unfinished office floor with bare walls, a few stacked plasterboard sheets and work lights.",
  "Locked interior wide shot. Plasterboard walls close in, ceilings lift into place, floors are laid and light fixtures glow on as the open shell becomes a bright finished office. The empty finished office holds on the final frame. " + STYLE),
 ("Facade finishing", "Same exterior wide view, nearly complete building with a few scaffold poles and landscaping soil around it.",
  "Locked wide shot, same position. Last scaffold poles are lowered away, paving and green lawn spread across the entrance, young trees appear along the walkway and the entrance lights switch on. The finished tower with landscaped forecourt holds on the final frame. " + STYLE),
 ("Handover", "Same wide view at golden hour, finished building with warm lit windows and a landscaped entrance.",
  "Slow locked wide shot. Warm evening light deepens, windows glow gold one after another, a few cars park and small groups of people walk toward the entrance. The glowing finished building holds centered on the final frame. " + STYLE),
])
add("2. Empty to Furnished Apartment", "Locked camera in a living room, 4 chained stages.", [
 ("Empty shell", "Bright empty living room, bare white walls, light oak floor, large window with sunlight.", "Locked wide shot from the doorway. Warm daylight slides slowly across the oak floor while dust motes drift in the window beam. The empty room holds, quiet and bright, on the final frame. " + STYLE),
 ("Furniture wave 1", "Same room, empty, with a gray sofa, rug and coffee table still in transit boxes at one side.", "Locked wide shot, same view. A gray sofa, a wool rug and a low coffee table appear in the room and settle into place in a natural arrangement. The three anchor pieces hold in position on the final frame. " + STYLE),
 ("Furniture wave 2", "Same room with sofa, rug and table in place, bare walls.", "Locked wide shot, same view. A floor lamp, a TV console, an armchair and a bookshelf appear one after another and settle into place around the sofa. The furnished layout holds on the final frame. " + STYLE),
 ("Styled", "Same furnished room, undecorated.", "Locked wide shot, same view. Framed art settles onto the wall, plants, cushions and a throw blanket appear, and the lamp glows warm as evening light replaces daylight. The fully styled room holds on the final frame. " + STYLE),
])
add("3. Renovation Before/After", "Locked camera on one room, 3 chained stages.", [
 ("Demolition", "Worn old room with peeling wallpaper, a damaged ceiling and cracked tiles, work light on a tripod.", "Locked medium-wide shot. Two workers in dust masks strip wallpaper and break out old tiles with hand tools as dust rises through the work light. The stripped bare walls and floor hold on the final frame. " + STYLE),
 ("Rough-in", "Same room stripped to brick and concrete with exposed wiring and pipes.", "Locked medium-wide shot, same view. A plasterer drags a trowel along fresh plaster and an electrician pulls a cable through a conduit while new pipes are fixed to the wall. The half-plastered wall with fresh wiring holds on the final frame. " + STYLE),
 ("Finished", "Same room, rough plastered walls and floor screed.", "Locked medium-wide shot, same view. Paint rolls across the wall in a smooth pass, new flooring slides into place, a modern light fixture and a window blind appear. The bright finished room holds on the final frame. " + STYLE),
])
add("4. Automotive Factory / Wiring Harness", "Industrial FDI-style plant; avoid showing real brand logos.", [
 ("Facility exterior", "Dawn wide shot of a modern gray industrial plant with a logo-free sign, parking lot and delivery truck.", "Slow dolly forward from the parking lot toward the plant entrance. A delivery truck backs to a loading bay and shift workers in uniforms walk in through the main door as the sun rises. The facade with its lit entrance holds on the final frame. " + STYLE),
 ("Production line", "Bright factory hall, long assembly tables with colored wire spools and workers in blue uniforms.", "Slow lateral tracking shot along the assembly tables. Workers route colored cables along wiring boards, press connectors and tape bundles with precise steady hands. The tracking slows and holds on a harness taking shape on the board. " + STYLE),
 ("Precision assembly", "Close-up of gloved hands crimping a connector on a multi-colored wire harness.", "Locked macro close-up. Hands insert a terminal into a connector housing, a crimp tool clamps, and the cable is pulled gently to test the hold. The finished connector holds sharply in focus on the final frame. " + STYLE),
 ("Testing", "Test station with a finished harness clipped to an electronic test board with glowing LEDs.", "Slow push-in toward the test board. Green indicator lights run down the connector pins one by one as an operator watches a monitor and nods. The row of green lights holds on the final frame. " + STYLE),
 ("Finished harness", "Neatly coiled finished wiring harness on a clean tabletop.", "Slow orbit around the harness. Soft light slides across the colored cables and black sleeving as the camera drifts a quarter turn. The harness holds centered and crisp on the final frame. " + STYLE),
])
add("5. Pharmaceutical Lab / Production", "Cleanroom look, no readable labels.", [
 ("Cleanroom", "White cleanroom corridor, a technician in full white suit and hood walking toward an airlock.", "Slow steady dolly back along the corridor. The technician walks forward, pauses at the airlock, and the door glides open onto a bright production hall. The open airlock with light spilling out holds on the final frame. " + STYLE),
 ("Formulation", "Stainless steel mixing vessel with a technician adding powder beside a digital scale.", "Locked medium shot. The technician pours white powder into the vessel, the stirrer starts and the liquid turns smoothly while a display ticks over. The glossy mixture swirls and holds on the final frame. " + STYLE),
 ("Quality control", "Laboratory bench with a microscope, pipettes, vials and a chromatography unit.", "Slow push-in on the bench. A chemist lifts a vial to the light, loads it into the analyzer, and a trace line draws across the screen beside her. The steady trace holds on the final frame. " + STYLE),
 ("Packaging", "Packaging line with blister packs and cartons on a clean conveyor.", "Locked side view. Blister packs slide along the conveyor, a mechanism slides them into cartons and the cartons advance in a precise rhythm. The line of finished cartons holds on the final frame. " + STYLE),
])
add("6. Food & Beverage Production", "Dairy/bakery/snack style plant.", [
 ("Raw ingredients", "Rustic table with wheat sacks, fresh milk jugs, tomatoes and herbs in morning light.", "Slow slider move left to right across the table. Golden grain pours from a scoop and a steady stream of milk fills a jug as morning light brightens. The ingredient spread holds on the final frame. " + STYLE),
 ("Processing", "Clean stainless kitchen with dough rolling through a machine and an operator in a hairnet.", "Locked medium shot. Dough passes under rollers, is cut into even shapes and slides onto trays that move toward the oven. A tray of shaped pieces holds at frame center on the final frame. " + STYLE),
 ("Packaging", "Packaging line with finished products on a conveyor, sealer and film roll.", "Locked side view. Products glide along the conveyor, the sealer closes the packs and a worker checks one against the light. The row of sealed packs holds on the final frame. " + STYLE),
 ("Finished product", "Finished product on a wooden table with fresh ingredients and a soft window light.", "Slow push-in toward the product. Steam curls up, a hand tears off a piece and light catches the texture of the crust. The product holds centered in focus on the final frame. " + STYLE),
])
add("7. Wine / Vineyard", "Tikves-style region: terraced hills, stone cellar.", [
 ("Vineyard", "Rolling vineyard rows at golden hour with ripe dark grapes on the vines.", "Slow forward drone-style glide along a vine row. Leaves ripple in a light breeze and golden light flares through the ripe clusters. The glowing rows hold toward the horizon on the final frame. " + STYLE),
 ("Harvest", "Pickers in a vineyard row filling crates with dark grapes.", "Locked medium shot. Pickers snip clusters and lay them gently in a crate, a hand lifts a bunch toward the light and dewdrops catch the sun. The full crate holds in the foreground on the final frame. " + STYLE),
 ("Fermentation", "Stone cellar with steel tanks and oak barrels, a winemaker holding a glass.", "Slow dolly forward between the barrels. The winemaker draws red wine from a barrel with a glass thief, raises the glass to the light and swirls it. The deep red glass holds in focus on the final frame. " + STYLE),
 ("Bottling", "Bottling line with dark green bottles, filler, corkers and wooden crates.", "Locked side view. Bottles fill in sequence, are corked and labeled and glide into a wooden crate. A single finished bottle with a blank label holds centered on the final frame. " + STYLE),
])
add("8. Steel / Cement Industrial", "Heavy industry at night/dusk, sparks and glow.", [
 ("Quarry", "Limestone quarry at dawn, terraced walls, a haul truck and a loader.", "Slow wide drone-style glide above the quarry. The loader fills a haul truck which pulls away along the terrace road, kicking up soft dust in the low sun. The vast terraced quarry holds on the final frame. " + STYLE),
 ("Furnace", "Interior of a steel plant with a glowing furnace, a worker in heat-protective gear.", "Locked wide shot from a safe distance. The furnace door opens and molten metal pours in an orange stream into a ladle, throwing sparks and glow across the hall. The glowing ladle holds on the final frame. " + STYLE),
 ("Forming", "Rolling mill with a glowing steel bar on rollers.", "Slow tracking shot along the mill line. A glowing bar slides through the rollers, thins and lengthens with sparks and steam rising. The glowing bar holds centered on the final frame. " + STYLE),
 ("Finished product", "Stacked bundles of rebar and steel beams in a yard at dusk.", "Slow orbit around the stack. Warm dusk light slides across the cool steel and a crane hook moves slowly overhead. The neat bundles hold on the final frame. " + STYLE),
])
add("9. Real Estate Developer Portfolio", "Single building lifecycle, 4 stages.", [
 ("Site", "Aerial view of an empty building plot with surveyor markers and hoardings.", "Slow aerial descent toward the plot. Surveyors walk across it and hoarding panels arrive and form a clean perimeter. The marked plot holds in view on the final frame. " + STYLE),
 ("Frame", "Aerial view of a building frame with cranes and concrete floors.", "Slow aerial orbit. The crane swings a load and the concrete floors rise one by one into a clear frame. The tall frame holds at center on the final frame. " + STYLE),
 ("Envelope", "Aerial view of a clad building with glass and facade, scaffold nearly down.", "Slow aerial orbit continues. Glass panels and facade cladding fill in and the scaffold drops away. The sealed building holds on the final frame. " + STYLE),
 ("Completed building", "Aerial view at golden hour of the completed residential building with landscaping and cars.", "Slow aerial pull-back. Windows light up in the golden hour and a few cars and residents move along the forecourt. The finished building with its landscaped surroundings holds on the final frame. " + STYLE),
])
add("10. Interior Design Portfolio", "Single room concept to finished, 4 stages.", [
 ("Empty", "Empty room with a large window and bare concrete walls.", "Locked wide shot. Daylight shifts slowly across the floor. The empty room holds on the final frame. " + STYLE),
 ("Concept", "Same room with a mood-board feel: a few sketches taped to a wall and fabric swatches on a stand.", "Locked wide shot, same view. Hand-drawn sketches and fabric swatches slide into place on the wall and a floor plan unrolls across a table. The concept corner holds on the final frame. " + STYLE),
 ("Furnished", "Same room with sketches, furniture still missing.", "Locked wide shot, same view. A sofa, dining table, chairs and a rug appear in place as the sketches disappear from the wall. The furnished room holds on the final frame. " + STYLE),
 ("Styled", "Same furnished room without decoration.", "Slow push-in. Art, a vase of flowers, books and warm lamps appear and evening light fills the space. The styled room holds on the final frame. " + STYLE),
])
add("11. Recruitment / Employer Branding", "People-focused; avoid readable ID badges or logos.", [
 ("Facility", "Modern factory campus exterior in morning light with employees arriving.", "Slow dolly forward toward the entrance. Employees in work clothes arrive in small groups and greet each other at the door. The entrance with the group holds on the final frame. " + STYLE),
 ("Team at work", "Team of three technicians at a bright workstation discussing a component.", "Locked medium shot. A senior technician points at a part, hands it to a younger colleague who inspects it and smiles. The shared moment holds on the final frame. " + STYLE),
 ("Culture moment", "Team lunch table in a bright canteen, laughing.", "Slow push-in on the table. The group laughs, a hand passes a dish and one raises a glass of water. The smiling circle holds on the final frame. " + STYLE),
])
add("12. Product Launch / Brand Film", "Product-agnostic; swap the item.", [
 ("Teaser", "Dark studio with a covered product on a pedestal and a thin spotlight.", "Slow push-in toward the pedestal. The cloth lifts and slides off in a smooth motion revealing a silhouette in a spotlight with faint haze. The silhouette holds on the final frame. " + STYLE),
 ("Reveal", "Product fully lit on a pedestal in a dark studio.", "Slow orbit around the product. Soft rim light sweeps across the surface and reflections glide along the edges. The hero angle holds on the final frame. " + STYLE),
 ("Lifestyle", "Product used in a warm real-world setting with a person.", "Locked medium shot. The person picks up the product, uses it naturally and glances up with a content smile. The product in hand holds in focus on the final frame. " + STYLE),
])

out = ["# LTX 2.5 22B keyframe prompts for the B2B video studio\n",
 "Continuation-form per doc 67 sec.2: camera, scene (brief), ONE action, held ending, style anchors. One paragraph per stage. Start keyframe carries identity; prompts only describe what moves. Positive language only (negative prompt: `watermark, text, logo`).\n",
 "Parameters for every stage: resolution 1280x704, frames 121, 24 fps, steps 8, cfg 1.0, start-frame strength 0.7 (0.5 for subtle moves, 0.85 for strong lock). Chain stages by using the last frame of stage N as the start keyframe of stage N+1 (or the keyframe concept below).\n",
 "Style note: these use photorealistic commercial anchors, not the menu's 3D-animated look. Do not put real company names or logos in keyframes (they are not stylable and risk trademark issues); the client logo is added in post.\n",
 "Seeds are deterministic per stage; retry ladder seed+1000, then +2000.\n"]
n = 0
for cat, note, st in C:
    out.append(f"\n## {cat} - LTX 2.5 Keyframe Prompts\n\n_{note}_\n")
    for i, (name, kf, pr) in enumerate(st, 1):
        n += 1
        seed = int(hashlib.sha1(f"{cat}{name}".encode()).hexdigest()[:6], 16) % 100000
        out.append(f"### Stage {i}: {name}\n**Start keyframe concept**: {kf}\n\n**LTX 2.5 continuation prompt**:\n> {pr}\n\n**Parameters**: resolution=1280x704, frames=121, strength=0.7, seed={seed}, cfg=1.0, steps=8\n")
open("/home/user/3p4e/projects/b2b-studio/LTX_PROMPTS.md", "w").write("\n".join(out))
print(len(C), "categories", n, "stages")
