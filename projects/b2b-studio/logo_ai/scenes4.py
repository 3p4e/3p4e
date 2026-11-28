# Logo films round 4 (owner, 2026-11-26): energy-blade duel. Every line of the BD mark is a glowing energy blade (lightsaber style, no
# franchise names or symbols on the site); the B blades and the D blades duel, then lay down in the exact form of the logo.
# (id, capability, start keyframe, end keyframe, motion)
from scenes import LOGO
def duel(cb, cd): return (f"A pitch-black void with light haze, dozens of glowing energy blades (white-hot cores, {cb} glow on the left side, {cd} glow on the right) "
                          f"crossing and clashing mid-air in a dynamic duel, bright white sparks bursting where the {cb} and {cd} blades meet, motion streaks.")
def rest(cb, cd): return (f"The same pitch-black void: the glowing energy blades now lie perfectly still, arranged exactly as {LOGO}: every line of the B is a "
                          f"{cb} glowing blade and every line of the D is a {cd} glowing blade, white-hot cores, soft glow, a few last sparks settling.")
MOVE = ("The {cb} and {cd} energy blades swing, cross and clash with bursts of white sparks, then slow down and lay themselves down one by one "
        "into the exact shape of the logo, the glow settling; slow push-in.")
S4 = [(f"blades_{k}", "action: energy-blade duel", duel(cb, cd), rest(cb, cd), MOVE.format(cb=cb, cd=cd))
      for k, cb, cd in (("red_blue", "red", "blue"), ("blue_red", "blue", "red"), ("green_purple", "green", "purple"))]
