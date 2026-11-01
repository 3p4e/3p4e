#!/usr/bin/env python3
"""Karsus's Folly, Wan 2.2 batch. Runs ON the Vast instance (stdlib only).
Reads start stills from ComfyUI input/ (k_*.png), renders 21 segments of 5.06 s, chains each set piece
by feeding the last frame of one clip as the start of the next, and logs to /workspace/batch.log.
Resumable: a segment whose output file exists is skipped.
  /venv/main/bin/python batch_karsus.py [--w 832 --h 480]
"""
import argparse, os, subprocess, sys, time, glob
ap = argparse.ArgumentParser(); ap.add_argument("--w", type=int, default=832); ap.add_argument("--h", type=int, default=480)
a = ap.parse_args()
R = "/workspace/ComfyUI_run"; IN = f"{R}/input"; OUT = f"{R}/output"
NEG = "blurry, distorted, extra objects, helicopters, birds, boats, flickering, text, watermark, jitter, morphing, extra people"
P = {
 "sp1": "The camera glides slowly forward above a calm ocean of white clouds. Three white stone cities with gold domes hang motionless on huge inverted mountains of dark rock. The clouds stay flat and unchanged far below. Warm sunrise light.",
 "sp2a": "Pale scorpion-like monsters feed on glowing threads of magic that they pull out of the trees and the river. A pale desert spreads outward from them. The camera pushes slowly forward.",
 "sp2b": "The monsters keep feeding. The green forest in front of them turns grey and collapses into sand. The camera holds steady.",
 "sp2c": "More monsters pour out of the sand across the valley while the land behind them turns to desert. The camera rises slowly.",
 "sp3a": "The man stands with open arms. Concentric rings of glowing blue-white glyphs expand slowly outward across the clouds around him. The camera pushes slowly in.",
 "sp3b": "The sky slowly darkens into a vast vortex above the man while the glowing rings keep expanding across the clouds.",
 "sp3c": "Bolts of lightning fall from the dark vortex into the glowing rings around the man. The camera holds steady.",
 "sp3d": "Distant floating cities dim one by one as thin streams of light flow across the sky toward the man.",
 "sp3e": "The glow around the man intensifies into a blinding blue-white light. The camera holds steady.",
 "sp4a": "White light streams from the vast golden goddess into the small man in the blue cloak. Lightning flickers in the dark clouds. The camera pushes slowly in.",
 "sp4b": "The man raises his arms and the beams of white light flow into him. The camera holds steady.",
 "sp4c": "A blinding white glow grows around the man until it fills the frame.",
 "sp4wa": "Columns of white and golden magic fall from the sky across the desert and vaporise the swarm of monsters into light. The camera holds wide.",
 "sp4wb": "Waves of golden fire sweep outward across the dunes and burn the remaining monsters to ash. The camera holds wide.",
 "sp5sa": "A blinding white flash grows as grey stone spreads up the man's body from his feet and hands. The camera pushes slowly in.",
 "sp5sb": "The stone figure falls to the ground in a cloud of dust and fading white light.",
 "sp5a": "Every light in the city goes out at once. The camera does not move.",
 "sp5b": "A vast white stone city on an inverted mountain tilts slowly and drops straight down through the sea of clouds. The camera follows the fall.",
 "sp6": "The camera pushes slowly in through a sunlit green forest clearing toward a moss-covered grey stone statue of a man with raised arms.",
}
# (id, set piece, start still or 'prev', prompt key, end still)
SEGS = [
 ("sp1a","sp1","k_sp1.jpg","sp1",None), ("sp1b","sp1","prev","sp1",None), ("sp1c","sp1","prev","sp1",None),
 ("sp2a","sp2","k_sp2.jpg","sp2a",None), ("sp2b","sp2","prev","sp2b",None), ("sp2c","sp2","prev","sp2c",None),
 ("sp3a","sp3","k_sp3.jpg","sp3a",None), ("sp3b","sp3","prev","sp3b",None), ("sp3c","sp3","prev","sp3c",None),
 ("sp3d","sp3","prev","sp3d",None), ("sp3e","sp3","prev","sp3e",None),
 ("sp4a","sp4","k_sp4.jpg","sp4a",None), ("sp4b","sp4","prev","sp4b",None), ("sp4c","sp4","prev","sp4c",None),
 ("sp4wa","sp4w","k_sp4w.jpg","sp4wa",None), ("sp4wb","sp4w","prev","sp4wb",None),
 ("sp5sa","sp5s","k_stone_a.jpg","sp5sa",None), ("sp5sb","sp5s","prev","sp5sb","k_stone_b.jpg"),
 ("sp5a","sp5a","k_sp5a_start.jpg","sp5a","k_sp5a_end.jpg"),
 ("sp5b1","sp5b","k_sp5a_end.jpg","sp5b",None), ("sp5b2","sp5b","prev","sp5b",None), ("sp5b3","sp5b","prev","sp5b",None),
 ("sp6a","sp6","k_sp6.jpg","sp6",None), ("sp6b","sp6","prev","sp6",None), ("sp6c","sp6","prev","sp6",None),
]
def log(m):
    line = f"[BATCH {time.strftime('%H:%M:%S')}] {m}"; print(line, flush=True); open("/workspace/batch.log", "a").write(line + "\n")
def out_of(tag): 
    f = sorted(glob.glob(f"{OUT}/wan22_{tag}_{a.w}x{a.h}_*.mp4")); return f[-1] if f else None
prev_last = None; t_all = time.time(); done = 0
for i, (sid, sp, start, pk, end) in enumerate(SEGS):
    if start == "prev": start = prev_last
    f = out_of(sid)
    if not f:
        t0 = time.time()
        cmd = ["/venv/main/bin/python", "/workspace/run_wan_i2v.py", "--host", "http://127.0.0.1:8199", "--imagefile", start, "--tag", sid,
               "--w", str(a.w), "--h", str(a.h), "--seed", str(100 + i), "--negative", NEG, "--prompt", P[pk]]
        if end: cmd += ["--endimage", end]
        r = subprocess.run(cmd, capture_output=True, text=True)
        txt = (r.stdout + r.stderr).strip().splitlines()
        f = out_of(sid)
        log(f"{sid} {'OK' if f else 'FAILED'} in {time.time()-t0:.0f}s :: {' | '.join(l for l in txt if any(k in l for k in ('DONE','ERROR','REJECTED','PREFLIGHT')))[:300]}")
        if not f: sys.exit(1)
    else:
        log(f"{sid} exists, skipped")
    last = f"{sid}_last.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.2", "-i", f, "-update", "1", "-frames:v", "1", f"{IN}/{last}"])
    prev_last = last; done += 1
log(f"ALL DONE: {done} segments in {time.time()-t_all:.0f}s")
