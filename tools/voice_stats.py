#!/usr/bin/env python3
"""Compare voice previews: median pitch (Hz), speaking pace and brightness.

  python3 tools/voice_stats.py <label>=<audio_url_or_path> [...]
"""
import subprocess
import sys

import numpy as np

SR = 16000


def load(src):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def pitch_track(x, frame=1024, hop=256, fmin=60, fmax=400):
    f0 = []
    for i in range(0, len(x) - frame, hop):
        w = x[i:i + frame] * np.hanning(frame)
        if np.sqrt(np.mean(w ** 2)) < 0.01:
            continue
        ac = np.correlate(w, w, "full")[frame - 1:]
        lo, hi = SR // fmax, SR // fmin
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.3 * ac[0]:
            f0.append(SR / lag)
    return np.array(f0)


for arg in sys.argv[1:]:
    label, src = arg.split("=", 1)
    x = load(src)
    f0 = pitch_track(x)
    voiced = len(f0) * 256 / SR
    spec = np.abs(np.fft.rfft(x[: SR * 10]))
    freqs = np.fft.rfftfreq(len(x[: SR * 10]), 1 / SR)
    centroid = float((spec * freqs).sum() / spec.sum())
    print(f"{label:6} dur {len(x)/SR:5.1f}s  median F0 {np.median(f0) if len(f0) else 0:6.1f} Hz  "
          f"F0 spread {np.std(f0) if len(f0) else 0:5.1f}  voiced {voiced/(len(x)/SR):4.0%}  brightness {centroid:6.0f} Hz")
