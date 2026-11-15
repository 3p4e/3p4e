import cv2, os, json, subprocess, glob
import numpy as np

CLIPS = sorted(glob.glob('/a0/usr/projects/vast/media/perseus_assets/clips_v4/p23_s*.mp4'))
OUT = '/a0/usr/projects/vast/media/perseus_assets/analysis'
STRIPDIR = os.path.join(OUT, 'strips_v4')
os.makedirs(STRIPDIR, exist_ok=True)

results = {}
for f in CLIPS:
    n = int(os.path.basename(f).split('_s')[1].split('_')[0])
    cap = cv2.VideoCapture(f)
    fc = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    diffs = []; lumas = []; statics = 0; blacks = 0
    prev = None; frames = []
    idx = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        lumas.append(float(gray.mean()))
        if gray.mean() < 5.0: blacks += 1
        if prev is not None:
            d = float(cv2.absdiff(gray, prev).mean())
            diffs.append(d)
            if d < 0.35: statics += 1
        prev = gray
        if idx in (0, fc//4, fc//2, 3*fc//4, fc-1):
            frames.append(fr.copy())
        idx += 1
    cap.release()
    md = np.mean(diffs) if diffs else 0.0
    mx = np.max(diffs) if diffs else 0.0
    lm = np.mean(lumas) if lumas else 0.0
    ls = np.std(lumas) if lumas else 0.0
    # 5-frame contact strip (fit into 1216-wide)
    if frames:
        fh, fw = frames[0].shape[:2]
        th = 140; tw = int(fw * th / fh)
        smalls = [cv2.resize(x, (tw, th)) for x in frames]
        strip = np.hstack(smalls)
        sp = os.path.join(STRIPDIR, f'v4_s{n:02d}_strip.jpg')
        cv2.imwrite(sp, strip, [cv2.IMWRITE_JPEG_QUALITY, 88])
    results[n] = {'frames': fc, 'width': w, 'height': h, 'fps': round(fps,2),
                  'motion_mean': round(md,2), 'motion_max': round(mx,1),
                  'static_frames': statics, 'static_pct': round(100*statics/max(1,fc-1),1),
                  'black_frames': blacks, 'luma_mean': round(lm,1), 'luma_std': round(ls,2)}
    print(f"s{n:02d}: {fc}f {w}x{h}@{fps:.0f}fps motion={md:.2f} max={mx:.1f} static={statics}/{fc-1}({100*statics/max(1,fc-1):.0f}%) black={blacks} luma={lm:.0f}±{ls:.1f}")

json.dump(results, open(os.path.join(OUT,'v4_analysis.json'),'w'), indent=2, sort_keys=True)
print('\nWROTE', os.path.join(OUT,'v4_analysis.json'), '| strips in', STRIPDIR)
# summary thresholds
bad = {k:v for k,v in results.items() if v['static_pct'] > 70 or v['black_frames'] > 0}
print('FLAGGED (static>70% or black frames):', sorted(bad.keys()))
