#!/usr/bin/env python3
"""Deep per-clip defect analysis for Perseus #23  v1, v4, fight clips.
Measures: spec, motion (mean/max/static), sharpness (blur), flicker,
luma (mean/std/black), face stability (appear/disappear events).
Writes combined JSON + contact strips for flagged clips.
"""
import cv2, os, json, glob, subprocess, re
import numpy as np

ROOT = '/a0/usr/projects/vast/media/perseus_assets'
OUT = os.path.join(ROOT, 'analysis')
DEEP = os.path.join(OUT, 'deep')
STRIP = os.path.join(OUT, 'strips_deep')
os.makedirs(DEEP, exist_ok=True)
os.makedirs(STRIP, exist_ok=True)

SETS = {
    'v1':    os.path.join(ROOT, 'clips'),
    'v4':    os.path.join(ROOT, 'clips_v4'),
    'fight': os.path.join(ROOT, 'clips_fight'),
}

YUNET = '/a0/usr/projects/vast/tools/models/face_detection_yunet_2023mar.onnx'

# thresholds
BLUR_THRESH = 40.0      # Laplacian variance below this = soft/blurry frame
FLICKER_DLUM = 14.0     # abs frame-to-frame luma change = flicker event
STATIC_MD = 0.35
BLACK_LUM = 5.0
FACE_STRIDE = 6         # detect face every 6th frame


def shot_num(fname):
    b = os.path.basename(fname)
    m = re.search(r'[sSfF](\d{2,3})', b)
    if not m:
        return None
    k = int(m.group(1))
    # fight clips: p23_f* -> tag fight; keep numeric as-is but mark prefix
    return k


def analyze(f, setname, detector):
    cap = cv2.VideoCapture(f)
    if not cap.isOpened():
        return None
    fc = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = os.path.getsize(f)

    diffs, lumas, laps = [], [], []
    statics = blacks = blurry = flickers = 0
    prev_gray = None
    prev_luma = None
    face_counts = []
    idx = 0
    frames = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        lum = float(gray.mean())
        lumas.append(lum)
        lap = cv2.Laplacian(gray, cv2.CV_64F).var()
        laps.append(lap)
        if lap < BLUR_THRESH:
            blurry += 1
        if lum < BLACK_LUM:
            blacks += 1
        if prev_gray is not None:
            d = float(cv2.absdiff(gray, prev_gray).mean())
            diffs.append(d)
            if d < STATIC_MD:
                statics += 1
        if prev_luma is not None and abs(lum - prev_luma) > FLICKER_DLUM:
            flickers += 1
        prev_gray = gray
        prev_luma = lum
        # face detection on stride
        if detector is not None and idx % FACE_STRIDE == 0:
            try:
                h2, w2 = fr.shape[:2]
                det = detector.detect(fr, h2, w2)
                n = 0 if det[1] is None else len(det[1])
                face_counts.append(n)
            except Exception:
                face_counts.append(-999)
        if idx in (0, fc // 4, fc // 2, 3 * fc // 4, fc - 1):
            frames.append(fr.copy())
        idx += 1
    cap.release()

    md = float(np.mean(diffs)) if diffs else 0.0
    mx = float(np.max(diffs)) if diffs else 0.0
    lm = float(np.mean(lumas)) if lumas else 0.0
    ls = float(np.std(lumas)) if lumas else 0.0
    lap_mean = float(np.mean(laps)) if laps else 0.0
    lap_min = float(np.min(laps)) if laps else 0.0

    # face stability
    fc_valid = [c for c in face_counts if c >= 0]
    face_events = 0
    if len(fc_valid) >= 2:
        prev = fc_valid[0]
        for c in fc_valid[1:]:
            if c != prev:
                face_events += 1
            prev = c
    face_min = min(fc_valid) if fc_valid else -1
    face_max = max(fc_valid) if fc_valid else -1

    rec = {
        'frames': fc, 'width': w, 'height': h, 'fps': round(fps, 2), 'size_kb': round(size / 1024, 1),
        'motion_mean': round(md, 2), 'motion_max': round(mx, 1),
        'static_pct': round(100 * statics / max(1, fc - 1), 1),
        'sharpness_mean': round(lap_mean, 1), 'sharpness_min': round(lap_min, 1),
        'blurry_pct': round(100 * blurry / max(1, fc), 1),
        'flicker_events': flickers, 'flicker_pct': round(100 * flickers / max(1, fc - 1), 1),
        'luma_mean': round(lm, 1), 'luma_std': round(ls, 2), 'black_pct': round(100 * blacks / max(1, fc), 1),
        'face_min': face_min, 'face_max': face_max, 'face_events': face_events,
    }
    # contact strip
    if frames:
        fh, fw = frames[0].shape[:2]
        th = 130
        tw = max(1, int(fw * th / fh))
        smalls = [cv2.resize(x, (tw, th)) for x in frames]
        strip_img = np.hstack(smalls)
        b = os.path.basename(f).replace('.mp4', '')
        cv2.imwrite(os.path.join(STRIP, f'{setname}_{b}.jpg'), strip_img,
                    [cv2.IMWRITE_JPEG_QUALITY, 85])
    return rec


def main():
    detector = None
    if os.path.exists(YUNET):
        det = cv2.FaceDetectorYN_create(YUNET, '', (320, 320), 0.7, 0.3, 5000)
        detector = det

    results = {}
    log = open(os.path.join(DEEP, 'run.log'), 'w')
    for setname, d in SETS.items():
        if not os.path.isdir(d):
            log.write(f'{setname}: dir missing {d}\n')
            continue
        files = sorted(glob.glob(os.path.join(d, '*.mp4')))
        log.write(f'{setname}: {len(files)} clips\n')
        results[setname] = {}
        for f in files:
            n = shot_num(f)
            if n is None:
                continue
            key = f'{setname}_{n:02d}'
            rec = analyze(f, setname, detector)
            if rec:
                rec['file'] = os.path.basename(f)
                results[setname][key] = rec
                line = (f"{key}: {rec['frames']}f sharp={rec['sharpness_mean']} "
                        f"blur={rec['blurry_pct']}% flick={rec['flicker_events']} "
                        f"motion={rec['motion_mean']} static={rec['static_pct']}% "
                        f"black={rec['black_pct']}% face_ev={rec['face_events']}")
                print(line, flush=True)
                log.write(line + '\n')
                log.flush()
    json.dump(results, open(os.path.join(DEEP, 'deep_analysis.json'), 'w'),
              indent=2, sort_keys=True)
    log.write('DONE\n')
    log.close()
    print('WROTE', os.path.join(DEEP, 'deep_analysis.json'))


if __name__ == '__main__':
    main()
