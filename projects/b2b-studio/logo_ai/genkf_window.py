# Cathedral window, take 2 (owner: "the actual logo BD must BE the vitrage"): the window opening itself is the BD mark. Three options.
import sys, os
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
REF = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; OUT = f"{S}/logo_ai/kf_window"; os.makedirs(OUT, exist_ok=True)
M = ("The stained-glass window IS the BD logo from the reference image: the window opening in the stone wall has exactly the shape of the mark "
     "(two small stacked triangles = B, one big triangle = D), and every hand-drawn line of the mark is a strip of glowing coloured stained glass "
     "(ruby, gold, sapphire, emerald) held by black lead cames; everywhere outside the lines is solid carved stone wall. No round rose window, no other windows in view.")
O = {"w1_a": f"Inside a vast dark Gothic cathedral before dawn, centred frontal view of the high stone wall above the altar. {M} The glass is still dim, only faintly glowing.",
     "w1_b": f"The same Gothic cathedral wall at sunrise, same framing. {M} Brilliant sunlight blazes through the BD-shaped stained glass, the coloured glass glows intensely, beams of red, gold and blue light cut through the incense haze.",
     "w2_a": f"Low-angle view from the nave of a world-famous Gothic cathedral like Sainte-Chapelle, tall stone columns framing the apse wall. {M} Morning light, the window glowing in jewel colours.",
     "w3_a": f"Close view of the BD-shaped stained-glass window from inside the cathedral at sunset. {M} The sunlight projects the coloured BD shape onto the stone floor of the nave in front of the camera."}
STY = " Photorealistic cinematic still, 16:9, premium lighting, no text, no letters, no watermark."
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(4) as ex: list(ex.map(lambda k: gem(f"{OUT}/{k}.png", O[k] + STY, [REF]), O))
print("done", sorted(os.listdir(OUT)))
