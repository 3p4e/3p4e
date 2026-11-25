# Mark v3 (owner's brief): the traced tattoo D is kept exactly (its path is only translated, never redrawn); the B is two
# hand-inked triangles of the same size (original B style, gen_bd_equal.tri); nothing touches: B-to-D and top-to-bottom gaps equal
# the line-to-line spacing inside a bundle (GAP), measured on the real ink (rasterised D + B raster, dilation test).
#   python3 gen_bd_final.py <out_dir> <seed_top>,<seed_bottom> [...]
import sys, re, json, subprocess, numpy as np, cv2
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; sys.path.insert(0, f"{S}/brand"); sys.path.insert(0, "/home/user/3p4e/projects/b2b-studio/brand")
import gen_b_triangles as G
from gen_bd_equal import tri
OUT = sys.argv[1]; GAP = 120; w = 40
import os; DSRC = os.environ.get("DSRC", f"{S}/brand/mark_D_single.svg"); Dsvg = open(DSRC).read(); DW, DH = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', Dsvg).groups())
dpath = re.search(r' d="([^"]+)"', Dsvg).group(1)
mask_png = f"{OUT}/_D_mask.png"
subprocess.run(["node", f"{S}/logo2/svg2png.js", DSRC, mask_png, str(DW), "#000", "#fff"], check=True)
Dm = cv2.imread(mask_png, cv2.IMREAD_GRAYSCALE)[:DH, :DW] < 128
ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * GAP + 1, 2 * GAP + 1))
def crop(a):
    r, c = np.where(a.any(axis=1))[0], np.where(a.any(axis=0))[0]; return a[r.min():r.max() + 1, c.min():c.max() + 1]
for pair in sys.argv[2:]:
    st, sb = (int(x) for x in pair.split(","))
    SH = int(DH * 0.428); SW = int(SH * 1851 / 1795)                    # same aspect as the original B triangles
    top = crop(tri(st, SW, SH, w)[0]); bot = crop(tri(sb, SW, SH, w)[0])
    # stack: bottom triangle as close under the top one as the gap allows
    tdil = cv2.dilate(top.astype(np.uint8), ker) > 0; Wb = max(top.shape[1], bot.shape[1])
    for oy in range(0, top.shape[0] + 1, 4):
        H = max(top.shape[0], oy + bot.shape[0]) + GAP; a = np.zeros((H, Wb), bool); b = np.zeros_like(a)
        a[:tdil.shape[0], :tdil.shape[1]] = tdil[:H, :Wb]; b[oy:oy + bot.shape[0], :bot.shape[1]] = bot
        if not (a & b).any(): break
    B = np.zeros((max(top.shape[0], oy + bot.shape[0]), Wb), bool); B[:top.shape[0], :top.shape[1]] |= top; B[oy:oy + bot.shape[0], :bot.shape[1]] |= bot
    B = crop(B)
    # place B left of the D, vertically centred on the D, as close as the gap allows
    by = max(0, (DH - B.shape[0]) // 2); Bdil = cv2.dilate(B.astype(np.uint8), ker) > 0
    Hc = max(DH, by + B.shape[0]) + GAP
    for dx in range(0, B.shape[1] + GAP + 10, 4):
        Wc = dx + DW + GAP; c1 = np.zeros((Hc, Wc), bool); c2 = np.zeros_like(c1)
        c1[by:by + Bdil.shape[0], :Bdil.shape[1]] = Bdil[:Hc - by, :Wc]; c2[:DH, dx:dx + DW] = Dm
        if not (c1 & c2).any(): break
    m = 60; dB = G.trace(np.pad(B, m), -m, by - m)
    dD = re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", lambda q: f"{float(q.group(1)) + dx:.0f} {q.group(2)}", dpath)
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", dB + " " + dD)]; xs, ys = nums[0::2], nums[1::2]
    x0, y0, x1, y1 = min(xs) - 40, min(ys) - 40, max(xs) + 40, max(ys) + 40
    open(f"{OUT}/mark_{st}_{sb}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}"><path fill="currentColor" fill-rule="evenodd" d="{dB} {dD}"/></svg>')
    print("ok", pair, "B", B.shape, "stack offset", oy, "D at x", dx)
