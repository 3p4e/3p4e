# New hand-drawn triangles in the style of the tattoo mark: per side a bundle of slightly wobbly, slightly
# non-parallel ink strokes that overshoot and cross at the corners, plus short inner fragments; variable pressure,
# tapered tails, ragged ink edges. Rasterised, then traced with potrace exactly like the tattoo photo.
import cv2, numpy as np, potrace, math, json, sys, re
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"

def noise1d(rng, n, cells):
    ctrl = rng.normal(0, 1, cells + 3); x = np.linspace(1, cells + 1, n)
    v = np.interp(x, np.arange(cells + 3), ctrl)
    k = max(3, (n // cells) | 1); v = cv2.GaussianBlur(v.reshape(1, -1).astype(np.float32), (k, 1), 0).ravel()
    return v / (np.abs(v).max() + 1e-6)

def value_noise(rng, h, w, cell):
    g = rng.random((h // cell + 3, w // cell + 3)).astype(np.float32)
    return cv2.resize(g, (w + 3 * cell, h + 3 * cell), interpolation=cv2.INTER_CUBIC)[:h, :w]

def stroke(img, p0, p1, w, rng):
    p0, p1 = np.array(p0, float), np.array(p1, float); L = np.linalg.norm(p1 - p0); d = (p1 - p0) / L; nr = np.array([-d[1], d[0]])
    n = max(8, int(L / (w * 0.2))); t = np.linspace(0, 1, n)
    off = rng.uniform(-1, 1) * 0.012 * L * 4 * t * (1 - t)                 # gentle bow
    off = off + noise1d(rng, n, max(3, int(L / (w * 9)))) * w * rng.uniform(0.25, 0.55)   # hand wobble
    off = off + noise1d(rng, n, max(6, int(L / (w * 2.5)))) * w * 0.12     # fine jitter
    press = 1 + 0.18 * noise1d(rng, n, max(3, int(L / (w * 6))))
    head = rng.uniform(1.0, 1.3)                                            # needle start: slightly heavier dot
    prof = press * np.where(t < 0.03, head, 1.0) * (0.55 + 0.45 * np.clip((1 - t) / rng.uniform(0.06, 0.16), 0, 1))
    pts = p0[None] + (t[:, None] * L) * d[None] + off[:, None] * nr[None]
    for (x, y), pr in zip(pts, prof):
        cv2.circle(img, (int(round(x * 4)), int(round(y * 4))), max(1, int(round(w * pr / 2 * 4))), 255, -1, lineType=cv2.LINE_AA, shift=2)

def triangle(seed, W, H, w, tip_y=None):
    rng = np.random.default_rng(seed); img = np.zeros((H, W), np.uint8)
    m = 0.06
    A = np.array([W * rng.uniform(0.21, 0.27), H * rng.uniform(0.14, 0.19)])          # top-left
    B = np.array([A[0] + W * rng.uniform(-0.03, 0.03), H * rng.uniform(0.81, 0.86)])  # bottom-left
    C = np.array([W * rng.uniform(0.74, 0.79), H * (tip_y if tip_y else rng.uniform(0.47, 0.55))])  # tip
    def bundle(P, Q, n, inside_sign, frag_p):
        L = np.linalg.norm(Q - P); d = (Q - P) / L; nr = np.array([-d[1], d[0]])
        sp = w * rng.uniform(2.8, 4.0); base = -sp * (n - 1) / 2 + rng.uniform(-0.5, 0.5) * sp
        offs = [base + i * sp + rng.uniform(-0.25, 0.25) * sp for i in range(n)]
        for o in offs:   # full strokes, overshooting both corners
            ang = math.radians(rng.uniform(-3.0, 3.0))
            dd = np.array([d[0] * math.cos(ang) - d[1] * math.sin(ang), d[0] * math.sin(ang) + d[1] * math.cos(ang)])
            s0, s1 = -rng.uniform(0.08, 0.30), 1 + rng.uniform(0.06, 0.30); mid = P + nr * o
            stroke(img, mid + dd * L * s0, mid + dd * L * s1, w * rng.uniform(0.85, 1.12), rng)
        if frag_p and rng.random() < frag_p:   # one short fragment just inside the bundle (like the tattoo's short inner strokes)
            inner = max(inside_sign * o for o in offs); o = inside_sign * (inner + sp * rng.uniform(0.8, 1.15))
            s0, s1 = rng.uniform(0.24, 0.38), rng.uniform(0.6, 0.76); mid = P + nr * o
            stroke(img, mid + d * L * s0, mid + d * L * s1, w * rng.uniform(0.85, 1.05), rng)
    # inside of the triangle relative to each side's normal; fragments only on the left and bottom sides, as in the tattoo
    cen = (A + B + C) / 3
    for P, Q, n, fp in ((A, B, rng.integers(3, 5), 0.85), (A, C, rng.integers(3, 5), 0.0), (B, C, rng.integers(3, 5), 0.5)):
        d = (Q - P) / np.linalg.norm(Q - P); nr = np.array([-d[1], d[0]]); sgn = 1 if np.dot(cen - P, nr) > 0 else -1
        bundle(P, Q, int(n), sgn, fp)
    # ragged ink edge like the traced photo
    blur = cv2.GaussianBlur(img, (0, 0), w * 0.12).astype(np.float32)
    nz = value_noise(rng, H, W, max(4, int(w * 0.6))) - 0.5
    ink = (blur + nz * 90) > 128
    return ink

def trace(ink, tx=0, ty=0):
    path = potrace.Bitmap(~ink).trace(turdsize=120, alphamax=1.15, opticurve=True, opttolerance=0.4); d = []
    for c in path:
        s = c.start_point; d.append(f"M{s.x+tx:.0f} {s.y+ty:.0f}")
        for seg in c.segments:
            d.append(f"L{seg.c.x+tx:.0f} {seg.c.y+ty:.0f}L{seg.end_point.x+tx:.0f} {seg.end_point.y+ty:.0f}" if seg.is_corner
                     else f"C{seg.c1.x+tx:.0f} {seg.c1.y+ty:.0f} {seg.c2.x+tx:.0f} {seg.c2.y+ty:.0f} {seg.end_point.x+tx:.0f} {seg.end_point.y+ty:.0f}")
        d.append("Z")
    return "".join(d)

if __name__ == "__main__":
    D = open(f"{S}/brand/mark_D_single.svg").read()
    DW, DH = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', D).groups()); dd = re.search(r' d="([^"]+)"', D).group(1)
    SW, SH = int(DW * 0.5), DH // 2; w = 40; gap = int(DW * 0.06)
    for k, (s1, s2) in enumerate([(11, 23), (31, 47), (52, 68), (75, 91)], 1):
        top = triangle(s1, SW, SH, w); bot = triangle(s2, SW, SH, w)
        d_top = trace(top, 0, 0); d_bot = trace(bot, 0, SH)
        dD = re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", lambda m: f"{float(m.group(1)) + SW + gap:.0f} {m.group(2)}", dd)
        TW = SW + gap + DW
        open(f"{S}/bd/new{k}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TW} {DH}"><path fill="currentColor" fill-rule="evenodd" d="{d_top} {d_bot} {dD}"/></svg>')
        print("ok", k)
