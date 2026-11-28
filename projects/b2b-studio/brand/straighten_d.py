# Straightens the traced tattoo D "a bit" without redrawing it: every outline point of the D path that lies along a stroke is pulled
# toward that stroke's straight centre line so its sideways wobble shrinks by ALPHA, while its distance to the centre line keeps the
# stroke's own mean half-width (thickness, ends, crossings, flicks stay). Points near crossings/ends or far from any stroke stay put.
#   python3 straighten_d.py <in.svg> <out.svg> [alpha=0.5]
import sys, re, subprocess, numpy as np, cv2
from skimage.morphology import skeletonize
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
src, dst = sys.argv[1], sys.argv[2]; ALPHA = float(sys.argv[3]) if len(sys.argv) > 3 else .5
svg = open(src).read(); W, H = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups()); d = re.search(r' d="([^"]+)"', svg).group(1)
png = "/dev/shm/_d.png"; subprocess.run(["node", f"{S}/logo2/svg2png.js", src, png, str(int(W)), "#000", "#fff"], check=True)
ink = cv2.imread(png, cv2.IMREAD_GRAYSCALE)[:int(H), :int(W)] < 128
sk = skeletonize(ink).astype(np.uint8) * 255
L = cv2.HoughLinesP(sk, 1, np.pi / 360, threshold=22, minLineLength=int(W * .03), maxLineGap=int(W * .02))
segs = [list(map(float, np.array(l).ravel()[:4])) for l in L]
# merge collinear duplicates
merged = []
for s in sorted(segs, key=lambda s: -np.hypot(s[2] - s[0], s[3] - s[1])):
    p, q = np.array(s[:2]), np.array(s[2:]); a = np.arctan2(*(q - p)[::-1]) % np.pi; keep = True
    for m in merged:
        mp, mq = np.array(m[:2]), np.array(m[2:]); b = np.arctan2(*(mq - mp)[::-1]) % np.pi
        if min(abs(a - b), np.pi - abs(a - b)) > np.radians(3): continue
        dv = (mq - mp) / np.linalg.norm(mq - mp); nv = np.array([-dv[1], dv[0]])
        if abs(np.dot(p - mp, nv)) < 12 and abs(np.dot(q - mp, nv)) < 12:
            t = sorted([0, np.dot(mq - mp, dv), np.dot(p - mp, dv), np.dot(q - mp, dv)]); m[:2] = list(mp + dv * t[0]); m[2:] = list(mp + dv * t[-1]); keep = False; break
    if keep: merged.append(s)
dist = cv2.distanceTransform(ink.astype(np.uint8), cv2.DIST_L2, 5)
SEG = []
for s in merged:
    p, q = np.array(s[:2]), np.array(s[2:]); Ls = np.linalg.norm(q - p); dv = (q - p) / Ls; nv = np.array([-dv[1], dv[0]])
    ts = np.linspace(.1, .9, 15); hw = np.median([dist[int(np.clip(p[1] + dv[1] * Ls * t, 0, H - 1)), int(np.clip(p[0] + dv[0] * Ls * t, 0, W - 1))] for t in ts])
    SEG.append((p, dv, nv, Ls, max(hw, 4.0)))
pts = re.findall(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", d); moved = 0
def fix(m):
    global moved
    x, y = float(m.group(1)), float(m.group(2)); P = np.array([x, y]); best = None
    for p, dv, nv, Ls, hw in SEG:
        t = np.dot(P - p, dv); e = np.dot(P - p, nv)
        if t < Ls * .03 or t > Ls * .97 or abs(e) > hw * 2.8: continue     # only along the body of a stroke
        if best is None or abs(e) / hw < abs(best[1]) / best[4]: best = (p, e, dv, nv, hw, t)
    if best is None: return m.group(0)
    p, e, dv, nv, hw, t = best; tgt = np.sign(e) * hw; e2 = e + (tgt - e) * ALPHA; moved += 1
    Q = p + dv * t + nv * e2; return f"{Q[0]:.0f} {Q[1]:.0f}"
d2 = re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", fix, d)
open(dst, "w").write(svg.replace(d, d2)); print("strokes", len(SEG), "points moved", moved, "of", len(pts))
