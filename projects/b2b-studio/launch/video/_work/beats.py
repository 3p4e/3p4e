import numpy as np, subprocess, sys
f = sys.argv[1]; sr = 22050
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
hop = 512; n = 2048
frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(frames, axis=1))
logS = np.log1p(10 * S)
flux = np.maximum(0, np.diff(logS, axis=0)).sum(1)
flux = np.concatenate([[0], flux]); flux -= np.convolve(flux, np.ones(16) / 16, 'same'); flux = np.maximum(flux, 0)
fps = sr / hop
ac = np.correlate(flux, flux, 'full')[len(flux) - 1:]
lags = np.arange(len(ac)) / fps
rng = (lags > 60 / 180) & (lags < 60 / 70)
L = np.argmax(ac * rng); bpm = 60 / lags[L]
sec = len(x) // sr
rms = np.sqrt((x[:sec * sr].reshape(sec, sr) ** 2).mean(1))
print('bpm %.1f' % bpm)
print('rms/s', ' '.join('%.2f' % v for v in rms))
period = fps * 60 / bpm
best = None
for off in np.linspace(0, period, 64, endpoint=False):
    idx = np.arange(off, len(flux) - 1, period).astype(int)
    s = flux[idx].sum()
    if best is None or s > best[0]: best = (s, off)
off = best[1] / fps
print('first beat %.3f period %.4f' % (off, 60 / bpm))
pk = np.argsort(flux)[::-1][:30]
print('top onsets', ' '.join('%.2f' % (p / fps) for p in sorted(pk)))
