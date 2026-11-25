# Header-logo effect clips: the same AI effects as the logo films, but only on the logo itself, on pure black (no scene), locked camera,
# so the black can be dropped with a screen blend and the logo stays exactly in place in the site header.
# (id, start keyframe, motion prompt)
L = ("the exact BD logo mark from the reference image (B = two separate equal triangles stacked, D = one big triangle, hand-tattooed "
     "ink-line bundles crossing at the corners), centred, filling about 70% of the frame, on a pure black background")
BG = " Nothing else in the frame: pure black background, no floor, no reflections, no scene, no text."
FX = [
 ("gold", f"{L}, made of glowing molten gold, bright liquid metal with a few sparks.", "Molten gold flows along every line of the logo, bright highlights travelling through the metal, a few sparks flying."),
 ("fire", f"{L}, every line burning with bright orange flames.", "Flames lick upward from every line of the logo, flickering and curling, embers rising."),
 ("ice", f"{L}, made of clear blue ice crystal with frost and a cold glow.", "Frost crystals grow along the ice lines, cold light shimmering through the crystal, tiny ice particles drifting."),
 ("neon", f"{L}, as gold neon glass tubes, glowing.", "The neon tubes flicker and buzz, then glow steadily with a soft pulsing halo."),
 ("lightning", f"{L}, made of crackling violet-white electricity.", "Electric arcs crackle and jump along every line of the logo, flashing and branching."),
 ("embers", f"{L}, made of glowing red-orange embers with thin smoke.", "The embers pulse brighter and dimmer like breathing, sparks drifting up, thin smoke curling off the lines."),
 ("chrome", f"{L}, as polished mirror chrome with bright studio highlights.", "Bright highlights glide across the chrome lines as if lights pass by, reflections sliding."),
 ("hologram", f"{L}, as a cyan hologram with scanlines and light flicker.", "The hologram flickers, scanlines roll through it and small glitches shift the lines before they settle."),
 ("galaxy", f"{L}, filled with a swirling purple and blue galaxy of stars.", "Stars and nebula clouds swirl slowly inside the lines of the logo, tiny stars twinkling."),
 ("water", f"{L}, made of clear flowing water with light caustics.", "Water flows and ripples along the lines of the logo, light caustics dancing through it, droplets glinting."),
 ("lava", f"{L}, made of cracked black rock with glowing lava in the cracks.", "Lava glows and pulses through the cracks in the rock lines, heat shimmer above."),
 ("plasma", f"{L}, made of glowing pink and blue plasma energy.", "Plasma energy surges and pulses through the lines, colours shifting between pink and blue."),
 ("frost_fire", f"{L}, the B in blue frost and the D in orange fire.", "Fire flickers on the D while frost sparkles on the B, the two glows breathing."),
 ("sparks", f"{L}, glowing white-hot metal throwing sparks like a grinder.", "Showers of bright sparks shoot from the lines of the logo, the metal glowing white-hot."),
 ("gold_thread", f"{L}, embroidered in shiny gold thread.", "Light glints and travels along the gold thread stitches, a soft shimmer moving across the logo."),
 ("aurora", f"{L}, filled with green and violet aurora light.", "Aurora curtains wave and flow inside the lines of the logo, colours rippling."),
 ("toxic", f"{L}, made of glowing green radioactive liquid with bubbles.", "Green glowing liquid bubbles and flows inside the lines, small bubbles rising."),
 ("rainbow", f"{L}, made of glowing rainbow-coloured light.", "Rainbow colours flow along the lines of the logo, the hues cycling smoothly."),
 ("smoke", f"{L}, made of thick white smoke shaped as the lines.", "Wisps of smoke curl and drift off the lines while the logo shape holds."),
 ("ink", f"{L}, made of wet glossy black ink with gold rim light.", "The wet ink shimmers, small drips run and gold rim light slides along the lines."),
]
