# Keyframes for logo films round 6 (scenes6.py), with the round-5 ship method of genkf5.py (guide from the mark file -> gpt-image-2).
# Five scenes in parallel; end frame first, then the start frame as an edit of it.   python3 genkf6.py [id ...]
# Output 1280x704 PNG: <scratch>/logo_ai/kf6/<id>_a.png (start), <id>_b.png (end).
import os, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import genkf5 as G
from scenes6 import S6, SHIP
G.OUT = OUT = f"{G.S}/logo_ai/kf6"; os.makedirs(OUT, exist_ok=True)
GUIDE = G.ship_guide()

def one(sc):
    sid, scene, empty, motion, style = sc; A, B = f"{OUT}/{sid}_a.png", f"{OUT}/{sid}_b.png"
    if not os.path.exists(B):
        G.fit(G.oa_image(f"Turn this layout guide into a photograph. Use the guide ONLY for where the three ships are and how big they are; replace "
                         f"the three shaded grey shapes with {style or SHIP}. They must not look flat or pasted on: real 3D hulls lit by the scene's light. "
                         f"The scene: {scene}. Keep all three ships fully inside the frame with space around them." + G.STY, refs=[GUIDE])).save(B)
    if not os.path.exists(A):
        ref = f"{OUT}/_ref_{sid}.png"; big = Image.open(B).resize((1536, 846), Image.LANCZOS)
        pad = Image.new("RGB", (1536, 1024)); pad.paste(big, (0, 89)); pad.save(ref)
        G.fit(G.oa_image("The exact same view, scenery, light, colours and camera as this image, a few moments earlier: the three spaceships are "
                         f"not there yet, {empty}." + G.STY, refs=[ref])).save(A)
        os.remove(ref)
    print("ok", sid, flush=True); return sid

if __name__ == "__main__":
    only = set(sys.argv[1:]); todo = [s for s in S6 if not only or s[0] in only]
    with ThreadPoolExecutor(5) as ex: list(ex.map(one, todo))
    print("KF6_DONE", sum(os.path.exists(f"{OUT}/{s[0]}_{x}.png") for s in S6 for x in "ab"), "/", 2 * len(S6))
