"""Gentle procedural music-box bed: loud in intro/outro, quiet under narration."""
import sys, wave
import numpy as np

SR = 44100


def note(freq, dur, amp=0.3):
    t = np.arange(int(SR * dur)) / SR
    tone = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t)
            + 0.12 * np.sin(2 * np.pi * 3 * freq * t))
    env = np.exp(-t * 3.2) * np.minimum(1, t / 0.005)
    return amp * tone * env


def midi(n):
    return 440 * 2 ** ((n - 69) / 12)


def render(total, intro_end, outro_start):
    beat = 60 / 92
    # C-major pentatonic lullaby, 8 bars of 4 beats (None = rest)
    melody = [72, 76, 79, 76, 74, 72, 74, None, 76, 79, 81, 79, 76, 74, 72, None,
              72, 74, 76, 79, 81, 79, 76, None, 74, 76, 74, 72, 67, 69, 72, None]
    bass = [48, 48, 55, 55, 53, 53, 48, 48]
    out = np.zeros(int(SR * (total + 3)))
    t = 0.0
    while t < total:
        for i, m in enumerate(melody):
            if m is not None:
                s = note(midi(m), 1.6, 0.22)
                a = int(SR * (t + i * beat)); out[a:a + len(s)] += s[:max(0, len(out) - a)]
        for j, b in enumerate(bass):
            s = note(midi(b), 3.0, 0.16)
            a = int(SR * (t + j * 4 * beat)); out[a:a + len(s)] += s[:max(0, len(out) - a)]
        t += len(melody) * beat
    out = out[:int(SR * total)]
    tt = np.arange(len(out)) / SR
    loud, quiet = 0.9, 0.13
    gain = np.full(len(out), quiet)
    gain[tt < intro_end] = loud
    ramp = (tt >= intro_end) & (tt < intro_end + 0.8)
    gain[ramp] = loud + (quiet - loud) * (tt[ramp] - intro_end) / 0.8
    ramp = (tt >= outro_start - 0.8) & (tt < outro_start)
    gain[ramp] = quiet + (loud - quiet) * (tt[ramp] - (outro_start - 0.8)) / 0.8
    gain[tt >= outro_start] = loud
    fade = tt > total - 2.0
    gain[fade] *= (total - tt[fade]) / 2.0
    out = out * gain
    out = out / max(1e-9, np.abs(out).max()) * 0.6 * (out.max() > 0)
    return out


if __name__ == "__main__":
    total, intro_end, outro_start, fn = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    pcm = (render(total, intro_end, outro_start) * 32767).astype(np.int16)
    with wave.open(fn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(fn, total)
