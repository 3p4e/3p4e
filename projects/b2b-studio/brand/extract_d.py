# Extracts the D from the full-resolution tattoo photo (sharpest: d78b831f, 1836x4080) instead of the 830 px close-up:
# shading removal (divide by a large blur), ink threshold, arm hair removed by width (opening + component filter), gentle edge
# smoothing, potrace with smooth corners. Output viewBox is scaled so the D is 3590 units tall (same as the earlier D).
#   python3 extract_d.py <photo> <out.svg> <x0,y0,x1,y1 crop> [smooth=2.0]
import sys, numpy as np, cv2, potrace
from PIL import Image, ImageOps
src, out, box = sys.argv[1], sys.argv[2], [int(v) for v in sys.argv[3].split(",")]; SM = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
im = np.array(ImageOps.exif_transpose(Image.open(src)).convert("RGB")).astype(np.float32)[box[1]:box[3], box[0]:box[2]]
g = cv2.medianBlur(cv2.GaussianBlur(im.min(axis=2), (0, 0), 1.6).astype(np.uint8), 5).astype(np.float32)  # denoised;                                              # ink is dark in every channel; skin is bright in red
bg = cv2.GaussianBlur(g, (0, 0), 35); r = g / (bg + 1)           # flatten skin shading and shadows
TH = float(sys.argv[5]) if len(sys.argv) > 5 else .88
ink = (r < TH).astype(np.uint8)
H0, W0 = ink.shape
if len(sys.argv) > 6:                                            # remove the arm's edge shadow: everything below the line y = a + b*x
    a, b = (float(v) for v in sys.argv[6].split(",")); yy, xx = np.mgrid[:H0, :W0]; ink[yy > a + b * xx] = 0
ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
# join dotted faint strokes only along their own direction (line kernels at the tattoo's three stroke angles)
def lk(angle, L=31):
    k = np.zeros((L, L), np.uint8); c = L // 2; dx, dy = np.cos(np.radians(angle)), -np.sin(np.radians(angle))
    cv2.line(k, (int(round(c - dx * c)), int(round(c - dy * c))), (int(round(c + dx * c)), int(round(c + dy * c))), 1, 1); return k
joined = ink.copy()
for ang in (list(range(-34, -14, 4)) + list(range(36, 58, 4)) + list(range(80, 100, 4)) if "--join" in sys.argv else []):
    joined |= cv2.morphologyEx(ink, cv2.MORPH_CLOSE, lk(ang))
ink = joined
n, lab, st, _ = cv2.connectedComponentsWithStats(ink, 8)
keep = np.zeros_like(ink)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if a > 700 and max(w, h) > 80: keep[lab == i] = 1            # drop specks, hairs and short fragments
sm = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), SM) > .5   # smooth ragged edges a little
ys, xs = np.where(sm); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max(); sm = np.pad(sm, 30)[y0 + 10:y1 + 51, x0 + 10:x1 + 51]
dist = cv2.distanceTransform(sm.astype(np.uint8), cv2.DIST_L2, 5); from skimage.morphology import skeletonize
sk = skeletonize(sm); sw = float(np.median(dist[sk]) * 2)
S = 3590 / sm.shape[0]
path = potrace.Bitmap(~sm).trace(turdsize=200, alphamax=1.25, opticurve=True, opttolerance=.35); d = []
for c in path:
    s = c.start_point; d.append(f"M{s.x * S:.0f} {s.y * S:.0f}")
    for seg in c.segments:
        d.append(f"L{seg.c.x * S:.0f} {seg.c.y * S:.0f}L{seg.end_point.x * S:.0f} {seg.end_point.y * S:.0f}" if seg.is_corner else
                 f"C{seg.c1.x * S:.0f} {seg.c1.y * S:.0f} {seg.c2.x * S:.0f} {seg.c2.y * S:.0f} {seg.end_point.x * S:.0f} {seg.end_point.y * S:.0f}")
    d.append("Z")
open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sm.shape[1] * S:.0f} 3590"><path fill="currentColor" fill-rule="evenodd" d="{"".join(d)}"/></svg>')
print("D", sm.shape, "stroke width (px)", round(sw, 1), "-> units", round(sw * S, 1), "components", n - 1)
