# Logo films round 5 (owner, 2026-11-27): "another try with the energy blades", "3 alien massive spaceships in formation like the logo BD over
# earth clouds (several videos)", "Nazca lines BD variant". Every film is start keyframe -> end keyframe (LTX first/last frame).
# The logo's exact form is never left to the image model: blade and Nazca end frames are drawn from the mark file itself (genkf5.py), the
# ships are painted over a guide with the three triangles of the mark (B: two stacked, D: one big) at their exact places.
# (id, kind, start prompt, end prompt, motion)
SHIP = ("three colossal three-dimensional alien motherships, each a massive arrowhead-shaped hull many kilometres long with real thickness and "
        "volume: bevelled armoured edges, layered dark metal plating with fine surface detail, rows of small lights, glowing engine vents at the "
        "rear, a thin line of light along every edge; seen in slight perspective so their depth and undersides show, with atmospheric haze, "
        "cloud wisps passing in front of them and shadows for scale. They hold formation like the three shapes of the guide image: two smaller "
        "ships stacked on the left (top and bottom), one huge ship on the right, all pointing right")
S5 = [
 ("blades2_red_blue", "blades", "A huge cinematic close view inside a black void with drifting haze: dozens of long glowing energy blades, red on the left and "
  "blue on the right, white-hot cores, slashing across the whole frame in a furious duel, the blades crossing in big X shapes, bright white "
  "spark showers where red meets blue, motion streaks, the blades fill the entire picture.", ("red", "blue"),
  "The red and the blue energy blades slash and clash across the whole frame in bursts of white sparks, then fly apart and lock one by one into "
  "the exact strokes of the logo, red blades forming the B and blue blades forming the D; the sparks settle and the glow hums; slow push-in."),
 ("blades2_blue_red", "blades", "A huge cinematic close view inside a black void with drifting haze: dozens of long glowing energy blades, blue on the left and "
  "red on the right, white-hot cores, slashing across the whole frame in a furious duel, the blades crossing in big X shapes, bright white "
  "spark showers where blue meets red, motion streaks, the blades fill the entire picture.", ("blue", "red"),
  "The blue and the red energy blades slash and clash across the whole frame in bursts of white sparks, then fly apart and lock one by one into "
  "the exact strokes of the logo, blue blades forming the B and red blades forming the D; the sparks settle and the glow hums; slow push-in."),
 ("ships_sunrise", "ships", "seen from high above an endless sea of white clouds at sunrise, golden light on the cloud tops, deep blue sky, Earth's horizon "
  "softly curved far away", None,
  "The three colossal ships rise slowly out of the sea of clouds, cloud vapour pouring off their hulls, and settle into formation in the golden "
  "sunrise light, their edge lights igniting; slow majestic push-in."),
 ("ships_orbit", "ships", "seen from the edge of space: the curve of the Earth below with swirling white cloud bands over a blue ocean, the thin glowing "
  "atmosphere line, black starry sky above, the Sun just rising over the horizon", None,
  "The three colossal ships glide in from the darkness above the Earth and slow into formation over the clouds, sunlight sliding across their "
  "hulls and their edge lights glowing; slow drift."),
 ("ships_storm", "ships", "inside a towering canyon of dark storm clouds high above the Earth, lightning flickering inside the clouds, rain veils, "
  "dramatic blue-grey light", None,
  "Lightning flashes as the three colossal ships emerge from the storm clouds and hold formation, their glowing edge lines cutting through the "
  "rain and mist; slow push-in."),
 ("ships_below", "ships", "seen from the ground looking straight up at a thick grey cloud ceiling breaking open, the edges of the clouds lit gold by the "
  "evening sun, a few birds", None,
  "The cloud ceiling slowly tears open and the undersides of the three colossal ships slide into view in formation, their edge lights glowing "
  "through the drifting clouds; slow upward tilt."),
 ("nazca_lines", "nazca", "A straight-down aerial photograph of the Nazca desert in Peru at midday: flat reddish-brown stony plain (pampa) with dark "
  "oxidised pebbles over pale yellowish ground, a few faint ancient straight lines crossing the plain, no figures, no people, no roads.", "top",
  "Wind sweeps across the desert and the dark pebbles slide away, uncovering the pale lines of the giant geoglyph stroke by stroke until the "
  "whole drawing lies on the plain; the camera slowly rises like a small plane climbing."),
 ("nazca_dawn", "nazca", "An oblique aerial photograph from a small plane over the Nazca desert in Peru at dawn: a vast flat reddish-brown stony plain "
  "stretching to low bare hills on the horizon, long soft shadows, warm low sunlight, faint ancient straight lines on the ground, no figures, "
  "no people, no roads.", "oblique",
  "Dawn light slides across the desert and the pale lines of the giant geoglyph appear stroke by stroke as the dark stones roll aside, long "
  "shadows shrinking; the plane banks slowly past."),
]
