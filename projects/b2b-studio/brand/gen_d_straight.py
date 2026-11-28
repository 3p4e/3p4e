# D mark v2 (owner's choice): keep the original B (two hand-inked triangles from gen_b_triangles.py, as in mark.svg) and redraw the
# big D in the same style: one big triangle of slightly wobbly, near-straight ink-stroke bundles that overshoot and cross at the
# corners, short inner fragments, ragged edges, same stroke width as the B. Rasterised and traced with potrace like the B.
#   python3 gen_d_straight.py <out_dir> <seed> [<seed> ...]
import sys, re, numpy as np
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; sys.path.insert(0, f"{S}/brand")
from gen_b_triangles import triangle, trace
OUT = sys.argv[1]; SEEDS = [int(x) for x in sys.argv[2:]] or [101, 202, 303, 404]
M = open(f"{S}/brand/mark.svg").read(); TW, TH = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', M).groups())
subs = re.findall(r"M[^M]*", re.search(r' d="([^"]+)"', M).group(1))
B = [p for p in subs if float(re.match(r"M(-?[\d.]+)", p).group(1)) < 1900]           # the B: everything left of the old D
bx = max(float(x) for p in B for x in re.findall(r"(-?\d+(?:\.\d+)?) -?\d+(?:\.\d+)?", p))  # right edge of the B ink
for sd in SEEDS:
    W, H = 3703, TH; ink = triangle(sd, W, H, 40)
    cols = np.where(ink.any(axis=0))[0]; left = cols.min(); right = cols.max()
    tx = int(bx + 150 - left)                                                           # same gap as between the B's ink and the old D
    d_D = trace(ink, tx, 0); NW = tx + right + 60
    open(f"{OUT}/bd_D{sd}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {NW} {TH}"><path fill="currentColor" fill-rule="evenodd" d="{"".join(B)} {d_D}"/></svg>')
    print("ok", sd, NW)
