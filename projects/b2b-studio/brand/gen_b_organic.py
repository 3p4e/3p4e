# B mark v2: two triangles in the hand of the tattoo D (organic, wandering, ragged ink), small triangle on top, big one below,
# placed left of the traced D. Owner's brief: the v1 B lines were too straight; B = two different-size triangles, D = the third.
# Each side is 2-3 bowed, wandering, tapered ink strokes (sometimes broken), overshooting the corners; splayed flicks past the tip;
# a short inner fragment now and then; ragged edges like the traced tattoo photo. Rasterised, then traced with potrace.
#   python3 gen_b_organic.py <out_dir> [n_variants]
import cv2, numpy as np, potrace, math, re, sys, os
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{S}/logo3"; NV = int(sys.argv[2]) if len(sys.argv) > 2 else 6
os.makedirs(OUT, exist_ok=True)


def noise1d(rng, n, cells):
    ctrl = rng.normal(0, 1, cells + 3); x = np.linspace(1, cells + 1, n)
    v = np.interp(x, np.arange(cells + 3), ctrl); k = max(3, (n // max(cells, 1)) | 1)
    v = cv2.GaussianBlur(v.reshape(1, -1).astype(np.float32), (k, 1), 0).ravel()
    return v / (np.abs(v).max() + 1e-6)


def value_noise(rng, h, w, cell):
    g = rng.random((h // cell + 3, w // cell + 3)).astype(np.float32)
    return cv2.resize(g, (w + 3 * cell, h + 3 * cell), interpolation=cv2.INTER_CUBIC)[:h, :w]


def stroke(img, p0, p1, w, rng, flick=False):
    """one organic ink stroke: bow + slow S-wander + hand wobble + jitter, pressure varies, tapered tail (and head if flick)."""
    p0, p1 = np.array(p0, float), np.array(p1, float); L = np.linalg.norm(p1 - p0)
    if L < 4: return
    d = (p1 - p0) / L; nr = np.array([-d[1], d[0]]); n = max(10, int(L / (w * 0.15))); t = np.linspace(0, 1, n)
    off = rng.uniform(-1, 1) * rng.uniform(0.02, 0.05) * L * 4 * t * (1 - t)                       # bow
    off += rng.uniform(0.006, 0.016) * L * np.sin(2 * math.pi * (t * rng.uniform(0.7, 1.4) + rng.random()))  # S-wander
    off += noise1d(rng, n, max(3, int(L / (w * 10)))) * w * rng.uniform(1.0, 1.5)                  # slow hand drift
    off += noise1d(rng, n, max(6, int(L / (w * 3.5)))) * w * rng.uniform(0.55, 0.8)               # beginner's tremor
    off += noise1d(rng, n, max(10, int(L / (w * 1.4)))) * w * 0.28                                # needle shake
    kinks = np.cumsum((rng.random(n) < 2.5 / n) * rng.normal(0, w * 0.5, n))                      # small sudden corrections
    off += kinks - np.linspace(0, kinks[-1], n)
    press = 1 + 0.38 * noise1d(rng, n, max(4, int(L / (w * 3))))
    tail = np.clip((1 - t) / rng.uniform(0.08, 0.22), 0, 1); head = np.clip(t / (0.25 if flick else rng.uniform(0.01, 0.05)), 0, 1)
    prof = press * (0.35 + 0.65 * tail) * (0.4 + 0.6 * head)
    pts = p0[None] + (t[:, None] * L) * d[None] + off[:, None] * nr[None]
    for (x, y), pr in zip(pts, prof):
        cv2.circle(img, (int(round(x * 4)), int(round(y * 4))), max(1, int(round(w * pr / 2 * 4))), 255, -1, lineType=cv2.LINE_AA, shift=2)


def broken(img, P, Q, w, rng):
    """a stroke that is sometimes broken into two with a small gap, like a needle lifting."""
    if rng.random() < 0.3:
        c = rng.uniform(0.35, 0.65); g = rng.uniform(0.03, 0.07)
        stroke(img, P, P + (Q - P) * (c - g / 2), w, rng); stroke(img, P + (Q - P) * (c + g / 2), Q, w * rng.uniform(0.85, 1.05), rng)
    else: stroke(img, P, Q, w, rng)


def triangle(rng, W, H, w):
    img = np.zeros((H, W), np.uint8)
    A = np.array([W * rng.uniform(0.16, 0.22), H * rng.uniform(0.09, 0.15)])                     # top-left
    B = np.array([A[0] + W * rng.uniform(-0.04, 0.04), H * rng.uniform(0.85, 0.91)])            # bottom-left
    C = np.array([W * rng.uniform(0.80, 0.86), H * rng.uniform(0.46, 0.56)])                     # tip (right)
    cen = (A + B + C) / 3
    for P, Q, frag in ((A, B, 0.7), (A, C, 0.25), (B, C, 0.45)):
        L = np.linalg.norm(Q - P); d = (Q - P) / L; nr = np.array([-d[1], d[0]]); sgn = 1 if np.dot(cen - P, nr) > 0 else -1
        n = int(rng.choice([2, 2, 3, 3, 3])); sp = w * rng.uniform(2.2, 3.6)
        offs = [(-sp * (n - 1) / 2 + i * sp) * rng.uniform(0.8, 1.25) + rng.uniform(-0.3, 0.3) * sp for i in range(n)]
        for o in offs:
            ang = math.radians(rng.uniform(-4.5, 4.5)); dd = np.array([d[0] * math.cos(ang) - d[1] * math.sin(ang), d[0] * math.sin(ang) + d[1] * math.cos(ang)])
            s0, s1 = -rng.uniform(0.04, 0.24), 1 + rng.uniform(0.03, 0.22); mid = P + nr * o
            broken(img, mid + dd * L * s0, mid + dd * L * s1, w * rng.uniform(0.8, 1.15), rng)
        if rng.random() < frag:   # short inner fragment
            o = sgn * (max(sgn * x for x in offs) + sp * rng.uniform(0.9, 1.3)); s0 = rng.uniform(0.2, 0.4); s1 = s0 + rng.uniform(0.2, 0.35); mid = P + nr * o
            stroke(img, mid + d * L * s0, mid + d * L * s1, w * rng.uniform(0.75, 1.0), rng)
    # splayed flicks past the tip, like the D
    for k in range(int(rng.integers(2, 4))):
        a = math.atan2(C[1] - cen[1], C[0] - cen[0]) + math.radians(rng.uniform(-38, 38)); ln = W * rng.uniform(0.06, 0.13)
        st = C + np.array([math.cos(a), math.sin(a)]) * W * rng.uniform(-0.02, 0.03)
        stroke(img, st, st + np.array([math.cos(a), math.sin(a)]) * ln, w * rng.uniform(0.6, 0.85), rng, flick=True)
    blur = cv2.GaussianBlur(img, (0, 0), w * 0.1).astype(np.float32)
    nz = (value_noise(rng, H, W, max(3, int(w * 0.3))) - 0.5) * 110 + (value_noise(rng, H, W, max(6, int(w * 1.2))) - 0.5) * 50
    return (blur + nz) > 128


def trace(ink, tx=0, ty=0):
    path = potrace.Bitmap(~ink).trace(turdsize=150, alphamax=1.2, opticurve=True, opttolerance=0.4); d = []
    for c in path:
        s = c.start_point; d.append(f"M{s.x + tx:.0f} {s.y + ty:.0f}")
        for seg in c.segments:
            d.append(f"L{seg.c.x + tx:.0f} {seg.c.y + ty:.0f}L{seg.end_point.x + tx:.0f} {seg.end_point.y + ty:.0f}" if seg.is_corner else
                     f"C{seg.c1.x + tx:.0f} {seg.c1.y + ty:.0f} {seg.c2.x + tx:.0f} {seg.c2.y + ty:.0f} {seg.end_point.x + tx:.0f} {seg.end_point.y + ty:.0f}")
        d.append("Z")
    return "".join(d)


if __name__ == "__main__":
    D = open(f"{S}/brand/mark_D_single.svg").read()
    DW, DH = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', D).groups()); dd = re.search(r' d="([^"]+)"', D).group(1)
    w = 50                                            # stroke width matched to the D's ink weight at this scale
    for k in range(1, NV + 1):
        rng = np.random.default_rng(1000 + 37 * k)
        HT = int(DH * rng.uniform(0.36, 0.40)); HB = DH - HT                 # clearly smaller top triangle above a bigger bottom one
        WB = int(DW * rng.uniform(0.62, 0.70)); WT = int(WB * rng.uniform(0.56, 0.64))
        top = triangle(rng, WT, HT, w); bot = triangle(rng, WB, HB, w * 1.08)
        gap = int(DW * 0.03)
        d_top = trace(top, int((WB - WT) * rng.uniform(0.0, 0.25)), 0); d_bot = trace(bot, 0, HT - int(HT * 0.06))
        dD = re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", lambda m: f"{float(m.group(1)) + WB + gap:.0f} {m.group(2)}", dd)
        TW = WB + gap + DW
        open(f"{OUT}/bd_v{k}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TW} {DH}"><path fill="currentColor" fill-rule="evenodd" d="{d_top} {d_bot} {dD}"/></svg>')
        print("ok", k, "top", WT, HT, "bottom", WB, HB)
