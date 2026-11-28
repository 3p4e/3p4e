# Cathedral window take 3 (owner): the WHOLE BD silhouette is the stained-glass window, the D triangle filled as fully as the B
# triangles, and the mark's black hand-drawn tattoo lines run across the glass as the lead cames, clearly visible.
import sys, os
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
REF = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; W1 = f"{S}/logo_ai/kf_window"; OUT = W1
M = ("The window opening in the stone wall is the complete filled silhouette of the BD logo from the first reference image: the two stacked "
     "triangles of the B AND the whole big triangle of the D are each ENTIRELY filled with stained glass from edge to edge (the inside of the D "
     "triangle is glass too, not stone). Over the glass, the black hand-drawn tattoo lines of the logo run exactly as in the reference and act as "
     "thick black lead cames, clearly visible, dividing the glass into pieces of ruby red, gold, sapphire blue and emerald green. Outside the BD "
     "silhouette is solid carved stone. Same Gothic cathedral and same frontal framing as the second reference image.")
O = {"w4_a": f"{M} Dawn: the glass is still dim, faintly glowing, the cathedral dark.",
     "w4_b": f"{M} Sunrise: brilliant sunlight blazes through the whole BD-shaped window, every glass piece glowing intensely with the black lead lines crisp, beams of red, gold and blue light streaming through the incense haze into the nave."}
STY = " Photorealistic cinematic still, 16:9, premium lighting, no text, no watermark."
gem(f"{OUT}/w4_a.png", O["w4_a"] + STY, [REF, f"{W1}/w1_a.png"])
gem(f"{OUT}/w4_b.png", O["w4_b"] + STY, [REF, f"{OUT}/w4_a.png"])
print("ok")
