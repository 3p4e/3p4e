# Find where each voice-over line sits in every finished LTX film (final_music/*.mp4) by cross-correlating the line's
# audio with the film soundtrack. Output: subs/timing.json {film: {"lang":..., "lines":[{"t0","t1","text"}...]}}
import os, sys, json, subprocess, numpy as np
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
sys.path.insert(0, f"{S}/vo"); os.chdir(f"{S}/vo")
from vo_lines import VO as VA
from vo_extra import VO as VB
from batch2 import CUTS
TR = f"{S}/vo/trim"; FM = f"{S}/final_music"; SR = 8000
def pcm(f):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32) / 32768
FILMS = {}
for cid in ("bw", "gener2", "concord", "viva", "alkaloid", "replek", "millennium", "nelt", "speeex"):
    lang, _, lines = VA[cid]; FILMS[f"{cid}_commercial"] = (lang, [(f"{TR}/{cid}_{i}.wav", t) for i, t in enumerate(lines, 1)])
lang, _, lines = VA["zito"]; FILMS["zito_commercial"] = (lang, [(f"{TR}/zito_{i}.wav", t) for i, t in enumerate(lines, 1)])
for k, film in (("vincinni_vc1", "vincinni_family_ad"), ("vincinni_vc2", "vincinni_factory_ad"), ("foton_specs", "foton_tunland_v9_specs")):
    lang, _, lines = VB[k]; FILMS[film] = (lang, [(f"{TR}/{k}_{i}.wav", t) for i, t in enumerate(lines, 1)])
for c in CUTS:
    name, lang, shots = c[0], c[1], c[6]; li = 0; L = []
    for _, line in shots:
        if line: li += 1; L.append((f"{TR}/b2_{name}_{li}.wav", line))
    FILMS[name] = (lang, L)
os.makedirs(f"{S}/subs", exist_ok=True); out = {}
for film, (lang, cands) in sorted(FILMS.items()):
    fp = f"{FM}/{film}.mp4"
    if not os.path.exists(fp): print("NOFILM", film); continue
    a = pcm(fp); n = len(a); found = []
    for wav, text in cands:
        if not os.path.exists(wav): print("NOWAV", wav); continue
        v = pcm(wav); m = len(v)
        if m >= n: continue
        N = 1 << int(np.ceil(np.log2(n + m)))
        cc = np.fft.irfft(np.fft.rfft(a, N) * np.conj(np.fft.rfft(v, N)), N)[: n - m + 1]
        e = np.sqrt(np.convolve(a * a, np.ones(m, np.float32), "valid")) * np.linalg.norm(v) + 1e-9
        sc = cc / e; k = int(np.argmax(sc))
        if sc[k] > 0.25: found.append(dict(t0=round(k / SR, 3), t1=round((k + m) / SR, 3), text=text, score=round(float(sc[k]), 3)))
        else: print("WEAK", film, os.path.basename(wav), round(float(sc[k]), 3))
    found.sort(key=lambda x: x["t0"]); out[film] = dict(lang=lang, lines=found)
    print(film, lang, len(found), "/", len(cands), [l["score"] for l in found], flush=True)
json.dump(out, open(f"{S}/subs/timing.json", "w"), ensure_ascii=False, indent=1)
print("TIMING_DONE", len(out))
