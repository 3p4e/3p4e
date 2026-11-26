# Cathedral window take 3 layout (owner: the WHOLE BD silhouette is stained glass, the D's inside too; the black tattoo lines are the lead):
# fills the triangles closed by the mark's crossing strokes, cuts the area into Voronoi glass pieces in jewel colours with thin lead lines,
# and draws the mark's own ink on top as thick black lead. Output: window_layout.png (RGBA) for the keyframe composite.
import sys, numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd
from scipy.spatial import cKDTree
OUT = sys.argv[1]
a = np.array(Image.open("/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png").convert("RGB")).mean(axis=2)
ink = a < 128; ys, xs = np.where(ink); P = 20
ink = np.pad(ink, P)[ys.min():ys.max() + 2 * P, xs.min():xs.max() + 2 * P]
s = 1100 / ink.shape[0]; ink = cv2.resize(ink.astype(np.uint8) * 255, (int(ink.shape[1] * s), 1100), interpolation=cv2.INTER_AREA) > 100
cl = cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
fill = nd.binary_fill_holes(cl)
n, lab = cv2.connectedComponents(fill.astype(np.uint8)); sil = np.zeros(fill.shape, np.uint8)
for i in range(1, n):
    cnt, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); c = max(cnt, key=cv2.contourArea)
    if cv2.contourArea(c) < 3000: continue
    cv2.fillPoly(sil, [cv2.convexHull(c)], 1)   # the triangle, inside included
h, w = sil.shape; rng = np.random.default_rng(7); pts = rng.integers(0, [w, h], size=(320, 2))
yy, xx = np.mgrid[0:h, 0:w]; _, idx = cKDTree(pts).query(np.c_[xx.ravel(), yy.ravel()]); idx = idx.reshape(h, w)
pal = np.array([[178, 20, 30], [214, 150, 30], [25, 60, 170], [20, 130, 70], [120, 30, 140], [230, 190, 80], [40, 110, 200], [190, 60, 40]], np.float32)
col = pal[rng.integers(0, len(pal), len(pts))][idx] * (0.75 + 0.5 * rng.random(len(pts)))[idx][..., None]
lead = cv2.dilate((cv2.Laplacian(idx.astype(np.float32), cv2.CV_32F) != 0).astype(np.uint8), np.ones((3, 3))) > 0
img = np.zeros((h, w, 4), np.uint8); img[..., :3] = np.clip(col, 0, 255); img[..., :3][lead] = 22
ink_d = cv2.dilate(ink.astype(np.uint8), np.ones((5, 5))) > 0; img[..., :3][ink_d] = 8
img[..., 3] = ((sil > 0) | ink_d).astype(np.uint8) * 255
Image.fromarray(img).save(OUT); print("components", n - 1, "silhouette", round(float(sil.mean()), 3), img.shape)
