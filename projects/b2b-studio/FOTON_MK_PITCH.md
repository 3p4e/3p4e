# Foton Macedonia (foton.mk): research and LTX 2.5 prompt sets for a content pitch

Everything in the research section comes from the dealer's own website (opened 2026-11-23), so it is ✅ for what the site says and ❌ for anything not on it. The legal entity behind the site, its owners and any current video agency were NOT found; the search for a Macedonian distributor name returned nothing.

## 1. Who they are (from foton.mk)

- Site title: Foton Tunland Македонија. Text: 'Овластен дистрибутер на Foton возила во Република Северна Македонија' (authorised distributor of Foton vehicles in North Macedonia).
- Address: Ацо Шопов 58А, 1000 Скопје. Hours Mon-Fri 08:00-16:00. Phone +389 71 305 128. contact@foton.mk.
- Social: Instagram foton_macedonia, a Facebook profile (id 61577756110563). Site copyright 2026, so the push looks recent.
- Single-page style, Macedonian only, one main call to action: 'Закажи тест возење' (book a free 30-minute test drive).

## 2. Range and offers on the site

| Model | Spec on site | Price on site |
|---|---|---|
| Tunland V9 ULTRA 4x4 AT | 2.0L VGT + 48V, 129 kW, 450 Nm, 8-AT | EUR 42,900 (ex-VAT) |
| Tunland V7 ELITE 4x4 AT | 2.0L VGT + 48V, 129 kW, 450 Nm | EUR 38,000 (promo, was 39,000) |
| Tunland G7 DEMEND 4x4 AT | 2.0L Cummins diesel, 120 kW (163 hp), 450 Nm | EUR 29,000 (promo, was 30,000) |
| Auman R 2656 6x4 tractor | 553 hp, Cummins X13, ZF AMT | not listed |
| Aumark 7.5T | 156 hp, Cummins F3.8, Euro VI | not listed |
| eMe4 electric medium duty | up to 380 kW, CATL LFP 281.9 kWh, CCS2 | not listed |
| Cargo Van 3.2T | 120 kW, 380 Nm, 6MT or 8AT | not listed |

- Warranty 5 years / 100,000 km; registration in 48 hours; service network across Macedonia (claimed).
- Financing: 20% down, up to 84 months, approval in 24 hours; operating lease with service included and replacement every 5 years for companies and fleets.
- Brand claims: Foton Motor Group since 1996, 110+ countries, partners Bosch, Daimler, Cummins.

## 3. Observations that shape the pitch (my reading, not facts from them)

- The site already uses autoplay hero video (a frame sequence/autoplay hook is in the page code) but I found no brand film, owner stories or social video campaign. Treat existing video as unverified.
- Two audiences are on one page: pickup buyers (V9/V7/G7) and fleet/B2B (trucks, vans, leasing). That maps to two content tracks.
- The conversion goal is a booked test drive, so every clip should end on a held vehicle shot where a CTA can be overlaid.
- Prices and promos change; keep text out of the generated video and add prices in post so clips stay valid.

## 4. Suggested pitch package (prices are yours to set)

1. Launch film: 30-45 s, sections A + D + F. 2. Three model spots, 15 s each (V9, V7, G7), section B. 3. Off-road reel, section C, for Instagram. 4. Fleet track: Auman, Aumark, eMe4, Cargo Van, section E, for LinkedIn and B2B outreach. 5. Trust spot: warranty, finance and service, section G. Each stage below is one 5 s clip (121 frames at 24 fps); chain stages to make longer spots.

## 5. Keyframe and prompt guidance

- Use the dealer's own official vehicle renders as start keyframes only with their permission; otherwise build keyframes from public brand images you are cleared to use, or generate them with an image model from a text description plus references, then check the car shape against the real model before sending to video.
- Real vehicles must match the real model: check grille, headlight shape and bed against foton.mk before rendering.
- Do not render the Foton logo or any text in frames; add the logo and the CTA in post. Positive-only prompts (negative `watermark, text, logo`).
- Prompts follow doc 67 sec.2 (continuation-form: camera, one action, held ending, style). Seeds are deterministic; retry seed+1000, then +2000.


### A. Tunland V9 flagship hero (V9 ULTRA 4x4)

_Colors on the dealer's site: Fire Red, Diamond Blue, Aurora Green, Lightning Purple, Phantom Black, Titanium Grey, Galaxy Silver, Flare White. Pick one per clip._

#### Stage 1: Dawn teaser
**Start keyframe concept**: Dark empty road at dawn, a red Foton Tunland V9 pickup parked in haze with low headlights on, mist at the wheels.

**LTX 2.5 continuation prompt**:
> Locked low wide shot from the front. Headlights brighten slowly and mist drifts across the road around the front wheels as first sunrise light slides up the hood. The truck holds centered with glowing headlights on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=47941

#### Stage 2: Drive-by
**Start keyframe concept**: Same red Tunland V9 on a mountain road at golden hour.

**LTX 2.5 continuation prompt**:
> Camera tracks alongside at wheel height. The pickup accelerates smoothly along the road, dust lifting from the shoulder and sunlight flaring across the windshield. The pickup holds in a three-quarter front view on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=58631

#### Stage 3: Studio turn
**Start keyframe concept**: Same Tunland V9 on a dark reflective studio floor with a soft rim light.

**LTX 2.5 continuation prompt**:
> Slow orbit around the pickup. Rim light sweeps along the roofline, wheel arches and tailgate while reflections glide across the glossy floor. The three-quarter hero angle holds on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=26375


### B. Three characters, one name (V9, V7, G7)

_Matches the site's tagline: V9 flagship, V7 everyday, G7 workhorse._

#### Stage 1: V9 character
**Start keyframe concept**: Tunland V9 on a city street at dusk, premium and sleek.

**LTX 2.5 continuation prompt**:
> Slow push-in from the front. Street lights reflect along the hood and the LED headlights blink awake. The V9 holds centered, calm and confident, on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=88088

#### Stage 2: V7 character
**Start keyframe concept**: Tunland V7 in a green countryside lane, family and daily-use feel.

**LTX 2.5 continuation prompt**:
> Locked medium-wide shot. The pickup rolls slowly past a farm gate, a hand raises in greeting from the driver window and trees sway in the breeze. The V7 holds in a three-quarter view on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=26287

#### Stage 3: G7 character
**Start keyframe concept**: Blue Tunland G7 at a gravel work site with tools in the bed.

**LTX 2.5 continuation prompt**:
> Camera tracks low alongside. The G7 pulls forward across gravel, bed tools rattle slightly and dust lifts behind the tires. The G7 holds in side profile on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=39700


### C. Where the asphalt ends (4x4 capability)

_Uses the site's off-road mud imagery as the reference mood._

#### Stage 1: Approach
**Start keyframe concept**: Tunland V9 at the edge of a muddy forest track, asphalt behind it.

**LTX 2.5 continuation prompt**:
> Locked wide shot from the track ahead. The pickup rolls off the asphalt onto the mud and the tires bite into the track. The truck holds mid-track with mud on its tires on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=80525

#### Stage 2: Climb
**Start keyframe concept**: Same Tunland V9 climbing a rocky incline.

**LTX 2.5 continuation prompt**:
> Camera tracks low in front. The pickup crawls up the incline with steady power, one wheel flexing over a rock and mud spraying off the tires. The truck holds at the crest on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=23293

#### Stage 3: Summit
**Start keyframe concept**: Same truck at a mountain overlook at sunrise.

**LTX 2.5 continuation prompt**:
> Slow pull-back. The pickup rolls to a stop at the viewpoint and warm sunrise light rims the roof and mirrors. The truck holds against the valley on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=95891


### D. Cabin and technology

_14.6-inch infotainment, CNC knobs, diamond-stitch seats, ambient lighting, panoramic roof (per site)._

#### Stage 1: Cockpit reveal
**Start keyframe concept**: Dark interior of a Tunland, dashboard dim.

**LTX 2.5 continuation prompt**:
> Slow push-in toward the dashboard. The 14.6 inch display wakes with a soft glow, ambient lighting ripples along the doors and the dials come alive. The lit dashboard holds on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=2361

#### Stage 2: Details
**Start keyframe concept**: Close-up on the CNC-finished control dial and gear selector.

**LTX 2.5 continuation prompt**:
> Locked macro shot. A hand rotates the metal dial one click and the display responds with a smooth glow. The dial holds sharply in focus on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=82553

#### Stage 3: Seats
**Start keyframe concept**: Diamond-stitched leather seat in soft cabin light.

**LTX 2.5 continuation prompt**:
> Slow lateral slide across the seats. Ambient light shifts from warm to cool along the stitching. The seat holds in focus on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=88078


### E. Trucks and fleet (B2B)

_Range per the site: Auman R 2656 6x4 tractor (553 HP), Aumark 7.5T, eMe4 electric medium duty, Cargo Van._

#### Stage 1: Auman tractor
**Start keyframe concept**: Foton Auman R 2656 tractor-trailer on a highway at sunrise.

**LTX 2.5 continuation prompt**:
> Camera tracks alongside at cab height. The tractor pulls steadily down the highway, trailer following in line while morning light flares across the grille. The rig holds in a three-quarter front view on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=91896

#### Stage 2: Aumark city delivery
**Start keyframe concept**: Foton Aumark light truck at a warehouse dock.

**LTX 2.5 continuation prompt**:
> Locked medium-wide shot. A worker closes the cargo door and the truck pulls out of the dock into a city street. The truck holds mid-street on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=60785

#### Stage 3: eMe4 electric
**Start keyframe concept**: Foton eMe4 electric truck at a charging depot at dusk.

**LTX 2.5 continuation prompt**:
> Slow push-in. A charging cable clicks into the port and a soft blue indicator pulses along the connector. The truck with its lit indicator holds on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=51009

#### Stage 4: Cargo Van
**Start keyframe concept**: Foton Cargo Van parked at a small shop front, morning.

**LTX 2.5 continuation prompt**:
> Locked wide shot. The rear doors swing open, a courier lifts a box and walks it to the shop door. The van holds with open doors on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=38251


### F. Test drive and handover (conversion)

_Ties to the site's 'Book a free 30-minute test drive' CTA. No readable text in frame; the CTA is added in post._

#### Stage 1: Showroom arrival
**Start keyframe concept**: Bright showroom floor with a Tunland V9 and a sales advisor beside it.

**LTX 2.5 continuation prompt**:
> Locked wide shot. The advisor opens the driver door with a welcoming gesture and a customer steps toward the vehicle. The open door holds on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=49075

#### Stage 2: Test drive
**Start keyframe concept**: Customer at the wheel of a Tunland V9 on a city boulevard, advisor in passenger seat.

**LTX 2.5 continuation prompt**:
> Camera tracks alongside through the window. The customer drives, smiles and glances at the display while the advisor points out a feature. The smiling driver holds in frame on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=99037

#### Stage 3: Key handover
**Start keyframe concept**: Handover moment in the showroom, a hand passing a key to the new owner, vehicle behind.

**LTX 2.5 continuation prompt**:
> Slow push-in. The advisor places the key in the owner's hand and both shake hands as warm light catches the vehicle behind. The handshake holds in focus on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=34678


### G. Warranty, finance and service (trust)

_Site claims: 5 years or 100,000 km warranty, 48-hour registration, financing with 20% down and up to 84 months, operating lease for fleets._

#### Stage 1: Service bay
**Start keyframe concept**: Clean service bay with a Tunland on a lift and a technician with a tablet.

**LTX 2.5 continuation prompt**:
> Locked medium-wide shot. The technician inspects underneath, nods and lowers the vehicle as the bay lights glint along the chassis. The lowered truck holds on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=47287

#### Stage 2: Fleet lineup
**Start keyframe concept**: Five Tunland pickups parked in a row in a fleet yard at dawn.

**LTX 2.5 continuation prompt**:
> Slow lateral track along the row. Headlights switch on one after another and morning light flares across the hoods. The aligned row holds on the final frame. Photorealistic automotive commercial cinematography, natural light, glossy reflections, shallow depth of field, crisp detail, calm premium pacing.

**Parameters**: resolution=1280x704, frames=121, strength=0.7, cfg=1.0, steps=8, seed=33570
