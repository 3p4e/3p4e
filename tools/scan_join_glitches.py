#!/usr/bin/env python3
"""Frame-diff glitch scan: decode sampled frames, flag inter-frame spikes,
bucket them to nearest clip join (5.042s period). Usage: scan <video> [clip_sec]"""
import subprocess, sys, numpy as np

video = sys.argv[1]
clip = float(sys.argv[2]) if len(sys.argv) > 2 else 5.042
W = 320

p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video,
                      '-vf', f'scale={W}:-2', '-f', 'rawvideo', '-pix_fmt', 'gray', 'pipe:1'],
                     stdout=subprocess.PIPE, bufsize=10**7)

H = None; prev = None; idx = 0; diffs = []
while True:
    if H is None:
        # read one probe frame to learn height: use ffprobe
        import json as _j
        pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                             '-show_entries', 'stream=width,height', '-of', 'json', video],
                            capture_output=True, text=True)
        st = _j.loads(pr.stdout)['streams'][0]
        H = int(st['height'] * W / st['width']) // 2 * 2
        FPS = 24.0
    raw = p.stdout.read(W * H)
    if len(raw) < W * H:
        break
    f = np.frombuffer(raw, np.uint8).astype(np.float32) / 255.0
    if prev is not None and idx % 3 == 0:
        d = float(np.mean(np.abs(f - prev)))
        diffs.append((idx / FPS, d))
    if idx % 3 == 0:
        prev = f
    idx += 1
p.wait()

if not diffs:
    print('NO_FRAMES'); sys.exit(1)

vals = np.array([d for _, d in diffs])
med = float(np.median(vals))
spikes = [(t, d) for t, d in diffs if d > med + 6 * max(vals.std(), 1e-6) and d > 0.02]

print(f'frames_decoded~{idx} median_diff={med:.4f} std={vals.std():.4f}')
print(f'spikes>{len(spikes)}')
joined = {}
for t, d in spikes:
    k = round(t / clip)
    if 1 <= k <= 46:
        joined.setdefault(k, []).append((t, d))
print('JOIN_SPIKES:', sorted(joined.keys()))
for k in sorted(joined):
    ts = joined[k]
    print(f'  join s{k:02d}->s{k+1:02d} @ {ts[0][0]:.2f}s peakdiff={max(x[1] for x in ts):.4f}')
print('ANALYSIS_DONE')
