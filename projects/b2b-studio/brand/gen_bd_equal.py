# Mark v2b (owner's brief): the B is two hand-inked triangles of exactly the same size (same corner points, different strokes),
# the D is one big triangle in the same hand. Style = gen_b_triangles.py (near-straight wobbly bundles that overshoot and cross,
# short inner fragments, ragged ink). The two B triangles stack in the D's height; the D keeps the stroke width.
#   python3 gen_bd_equal.py <out_dir> <b_seed_top>,<b_seed_bottom> <d_seed> [...]
import sys, re, math, numpy as np, cv2
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; sys.path.insert(0, f"{S}/brand")
import gen_b_triangles as G
CORNERS = ((0.20, 0.10), (0.20, 0.90), (0.84, 0.50))          # A top-left, B bottom-left, C tip: identical for every triangle


PAD = 0.22   # room for the overshooting strokes so no tip is cut off by the canvas edge


def tri(seed, W, H, w):
    """returns (ink, pad_x, pad_y): the canvas is padded on every side; geometry is relative to the unpadded W x H box"""
    rng = np.random.default_rng(seed); px, py = int(W * PAD), int(H * PAD); img = np.zeros((H + 2 * py, W + 2 * px), np.uint8)
    A, B, C = (np.array([W * x + px, H * y + py]) for x, y in CORNERS)
    A = A + rng.uniform(-0.006, 0.006, 2) * [W, H]; B = B + rng.uniform(-0.006, 0.006, 2) * [W, H]; C = C + rng.uniform(-0.006, 0.006, 2) * [W, H]
    cen = (A + B + C) / 3
    for P, Q, n, fp in ((A, B, rng.integers(3, 5), 0.85), (A, C, rng.integers(3, 5), 0.0), (B, C, rng.integers(3, 5), 0.5)):
        L = np.linalg.norm(Q - P); d = (Q - P) / L; nr = np.array([-d[1], d[0]]); sgn = 1 if np.dot(cen - P, nr) > 0 else -1
        sp = w * rng.uniform(2.8, 4.0); base = -sp * (int(n) - 1) / 2 + rng.uniform(-0.5, 0.5) * sp
        offs = [base + i * sp + rng.uniform(-0.25, 0.25) * sp for i in range(int(n))]
        for o in offs:
            ang = math.radians(rng.uniform(-3.0, 3.0)); dd = np.array([d[0] * math.cos(ang) - d[1] * math.sin(ang), d[0] * math.sin(ang) + d[1] * math.cos(ang)])
            s0, s1 = -rng.uniform(0.08, 0.26), 1 + rng.uniform(0.06, 0.26); mid = P + nr * o
            G.stroke(img, mid + dd * L * s0, mid + dd * L * s1, w * rng.uniform(0.85, 1.12), rng)
        if fp and rng.random() < fp:
            inner = max(sgn * o for o in offs); o = sgn * (inner + sp * rng.uniform(0.8, 1.15)); s0, s1 = rng.uniform(0.24, 0.38), rng.uniform(0.6, 0.76); mid = P + nr * o
            G.stroke(img, mid + d * L * s0, mid + d * L * s1, w * rng.uniform(0.85, 1.05), rng)
    blur = cv2.GaussianBlur(img, (0, 0), w * 0.12).astype(np.float32); nz = G.value_noise(rng, img.shape[0], img.shape[1], max(4, int(w * 0.6))) - 0.5
    return (blur + nz * 90) > 128, px, py


def paste(canvas, ink, x, y):
    h, w = ink.shape; canvas[y:y + h, x:x + w] |= ink


if __name__ == "__main__":
    OUT = sys.argv[1]; bt, bb = (int(x) for x in sys.argv[2].split(",")); DH = 3590; w = 40
    SW, SH = 1851, DH // 2; DW = 3703; VGAP = int(DH * 0.05); HGAP = int(SW * 0.40)
    (top, tpx, tpy), (bot, bpx, bpy) = tri(bt, SW, SH, w), tri(bb, SW, SH, w)
    for ds in (int(x) for x in sys.argv[3:]):
        Dk, dpx, dpy = tri(ds, DW, DH + VGAP, w)
        # layout in unpadded coordinates: top B box at (0,0), bottom B box below it with a small gap, D box to the right
        dx = int(SW * CORNERS[2][0]) + HGAP - int(DW * CORNERS[0][0])
        P = max(tpx, bpx, dpx, tpy, bpy, dpy) + 10
        Wc, Hc = dx + DW + 2 * P + dpx, DH + VGAP + 2 * P
        canvas = np.zeros((Hc, Wc), bool)
        paste(canvas, top, P - tpx, P - tpy); paste(canvas, bot, P - bpx, P + SH + VGAP - bpy); paste(canvas, Dk, P + dx - dpx, P - dpy)
        rows, cols = np.where(canvas.any(axis=1))[0], np.where(canvas.any(axis=0))[0]
        canvas = canvas[rows.min() - 30:rows.max() + 30, cols.min() - 30:cols.max() + 30]
        d = G.trace(canvas, 0, 0)                                    # one trace of the union: no fill-rule holes where strokes cross
        open(f"{OUT}/bde_{bt}_{bb}_D{ds}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas.shape[1]} {canvas.shape[0]}"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></svg>')
        print("ok", ds)
