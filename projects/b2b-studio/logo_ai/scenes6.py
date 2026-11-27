# Logo films round 6 (owner, 2026-11-27: "More alien spaceships."): ten more fleet films after the four of round 5 (sunrise, orbit, storm,
# below). Same method (genkf5.py): the end frame paints the three ships over a guide with the mark's three triangles at their exact places
# (B: two stacked, D: one big), the start frame is the same view a few moments earlier; LTX renders start -> end.
# ocean, peaks, gold, warp and eclipse: start frames built from the end frame by start6.py (mist / hyperspace streaks), OpenAI credit ran out
# (id, scene, what the start frame shows instead of the ships, motion, ship style or None for the dark-metal hulls of round 5)
from scenes5 import SHIP
GOLD = SHIP.replace("layered dark metal plating with fine surface detail, rows of small lights, glowing engine vents at the rear, a thin line of light along every edge",
                    "glossy black armoured plating with fine surface detail, rows of small gold lights, glowing gold engine vents at the rear, a bright gold line of light along every edge")
assert GOLD != SHIP
EMPTY_SKY = "only the empty sky and clouds (and cloud vapour where they will appear)"
EMPTY_SPACE = "only empty space and the stars where they will appear"
S6 = [
 ("ships_city", "seen from high above a vast modern city at night stretching to dark mountains, a river of lights winding through it, a ceiling of "
  "low clouds glowing orange from the city lights", "only the glowing low clouds above the city",
  "The three colossal ships descend slowly through the glowing low clouds above the city and settle into formation, searchlights from the "
  "streets sweeping across their hulls; slow push-in.", None),
 ("ships_moon", "seen from just above the grey cratered surface of the Moon, the blue and white Earth rising over the lunar horizon, black sky "
  "with stars, hard white sunlight and long crater shadows", "only the lunar horizon, the rising Earth and the stars",
  "The three colossal ships rise over the lunar horizon in front of the rising Earth and glide into formation, hard sunlight raking across "
  "their hulls; slow drift.", None),
 ("ships_desert", "seen from high above a vast red sandstone desert of mesas and deep canyons at sunset, long shadows, warm dust haze in the air",
  "only the desert, the canyons and the dusty sunset sky",
  "The three colossal ships sweep in low over the canyons, their giant shadows racing across the red sand, and slow into formation in the "
  "dusty sunset light; slow push-in.", None),
 ("ships_ocean", "low over a dark stormy ocean at dusk, heavy rolling waves and sea spray, a band of orange light on the horizon under heavy "
  "clouds, light rain", "only the stormy ocean, the spray and the clouds",
  "The drifting mist parts as the three colossal ships glide out of it low over the waves, sea spray swirling beneath them and their lights "
  "reflecting on the water, and hold formation; slow tracking shot.", None),
 ("ships_aurora", "above jagged snow-covered Arctic mountains at night under great curtains of green and violet aurora, bright stars, the snow "
  "lit green by the aurora", "only the aurora, the stars and the snowy mountains",
  "Beneath the rippling aurora the three colossal ships slide out of the night sky and settle into formation, green light rippling across "
  "their hulls; slow push-in.", None),
 ("ships_saturn", "in deep space beside Saturn, its golden banded globe and vast bright rings sweeping across the frame, glittering ice "
  "particles, black space with stars", "only Saturn, its rings and the stars",
  "The three colossal ships glide past the glittering rings of Saturn and turn into formation, ring light sliding across their hulls; slow "
  "orbiting drift.", None),
 ("ships_warp", "in deep space before a vast glowing nebula of magenta and teal gas, thousands of stars",
  "only the nebula and the stars, with three bright streaks of white-blue light stretched across the frame where they are dropping out of hyperspace",
  "Streaks of light snap short as the three colossal ships drop out of hyperspace one after another and lock into formation in front of the "
  "nebula, a faint shockwave ripple fading; slow push-in.", None),
 ("ships_peaks", "above a range of jagged snow-covered mountain peaks rising out of a sea of clouds at golden hour, warm light on the snow, "
  "deep blue sky", EMPTY_SKY,
  "The cloud parts and the three colossal ships descend out of it between the mountain peaks and settle into formation, golden light "
  "catching their edges; slow majestic push-in.", None),
 ("ships_gold", "high above a night sea of dark clouds under a huge golden full moon, faint stars, silver-gold moonlight on the cloud tops",
  "only the dark clouds, the golden moon and the stars",
  "Out of the dark clouds the three colossal black-and-gold ships rise into the moonlight and lock into formation, their gold edge lines "
  "igniting one after another; slow push-in.", GOLD),
 ("ships_eclipse", "in space above the night side of the Earth during a total solar eclipse: the Moon's black disc ringed by a blazing white "
  "corona, the Earth below dark with the lights of cities, black space with stars", "only the eclipse, the corona and the Earth's night side",
  "As the diamond ring of the eclipse flares, streaks of light snap short and the three colossal ships drop out of hyperspace into formation "
  "in front of the corona, rim light outlining every edge; slow drift.", None),
]
