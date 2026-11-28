# Foton Tunland v2 commercials (LTX 2.5): beat-snapped hard cuts with speed ramps, synthesized whoosh/impact design,
# AI disclosure from frame 1, branded end card, 16:9 and 9:16 from the same edit, -14 LUFS (social).
#   python3 cut_v2.py <clipdir> <outdir> [film_id ...]
# Clips: <clipdir>/<shot_id>.mp4 (LTX 2.5, 1280x704, 121 f, silent). Music: music/<film music>.wav at the film's BPM.
import os, sys, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from films import FILMS, DISCLOSURE
CLIPS, OUT = sys.argv[1], sys.argv[2]; ONLY = set(sys.argv[3:])
TMP = f"{OUT}/tmp"; os.makedirs(TMP, exist_ok=True)
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
FONT_H = f"{S}/brand/fonts/Oswald-700.ttf"; FONT_M = f"{S}/brand/fonts/Oswald-600.ttf"; FONT_R = f"{S}/brand/fonts/Oswald-400.ttf"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p"]
AENC = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]


def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")


def sfx():
    """whoosh (0.45 s band-passed noise swell, panned) and impact (sub drop + noise burst), made once."""
    w, h = f"{TMP}/whoosh.wav", f"{TMP}/hit.wav"
    if not os.path.exists(w):
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.45:c=pink:r=48000:a=0.9", "-af",
             "highpass=f=500,lowpass=f=6000,afade=t=in:st=0:d=0.32:curve=exp,afade=t=out:st=0.32:d=0.13,"
             "aformat=channel_layouts=stereo,apulsator=hz=1.6:amount=0.6,volume=1.2", w])
    if not os.path.exists(h):
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "aevalsrc='0.9*sin(2*PI*(38+60*exp(-9*t))*t)*exp(-4.5*t)':d=0.9:s=48000",
             "-f", "lavfi", "-i", "anoisesrc=d=0.12:c=brown:r=48000:a=0.8", "-filter_complex",
             "[1:a]lowpass=f=1800,afade=t=out:st=0.02:d=0.1[n];[0:a][n]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo,alimiter=limit=0.9", h])
    return w, h


def shot(tag, cid, segs, beats, beat, vertical=None):
    """one shot with its speed ramps; exact length = beats * beat. Segment flag 'adj' absorbs the timing."""
    src = f"{CLIPS}/{cid}.mp4"; cd = dur(src); target = beats * beat
    segs = [(a, min(b, cd - 0.05), s, f) for a, b, s, f in segs]
    fixed = sum((b - a) / s for a, b, s, f in segs if f != "adj"); a0, b0, _, _ = [x for x in segs if x[3] == "adj"][0]
    adj = (b0 - a0) / max(0.2, target - fixed); parts = []
    for k, (a, b, s, f) in enumerate(segs):
        s = adj if f == "adj" else s
        geo = ("scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720" if vertical is None
               else f"scale=-2:1920,crop=1080:1920:(iw-1080)*{vertical}:0")
        v = f"trim=start={a}:end={b},setpts=PTS-STARTPTS,{geo},setpts=PTS/{s:.4f}"
        v += ",minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if s < 0.9 else ",fps=24"
        p = f"{TMP}/{tag}_{cid}_{k}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", f"[0:v]{v}[v]", "-map", "[v]", "-an"] + ENC + [p]); parts.append(p)
    out = f"{TMP}/{tag}_{cid}.mp4"; concat(parts, out, target); return out


def concat(parts, out, exact=None):
    lst = out + ".txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    a = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst]
    if exact: a += ["-t", f"{exact:.3f}"]
    run(a + ["-an"] + ENC + ["-r", "24", out])


def card(out, d, film, vertical):
    W, H = (1080, 1920) if vertical else (1280, 720); cy = H // 2 - (150 if vertical else 95)
    acc = film.get("accent", "0xf2c14e")
    head, tag, spec = film["card"]
    L = [(FONT_H, head, 86 if vertical else 74, "white", cy, 0.15), (FONT_M, tag, 46 if vertical else 40, acc, cy + (118 if vertical else 96), 0.45),
         (FONT_R, spec, 32 if vertical else 26, "0xd8d8d8", cy + (196 if vertical else 160), 0.7),
         (FONT_M, "Закажи тест возење · foton.mk", 36 if vertical else 30, "white", cy + (290 if vertical else 228), 0.9),
         (FONT_R, "Концепт за презентација на Foton Македонија. Не е објавен без нивно писмено одобрение.", 24 if vertical else 17, "0x9a9a9a", H - (170 if vertical else 60), 0.3),
         (FONT_R, DISCLOSURE, 24 if vertical else 17, "0x9a9a9a", H - (134 if vertical else 36), 0.3)]
    vf = ",".join(f"drawtext=fontfile={f}:text='{esc(t)}':fontsize={s}:fontcolor={c}:x=(w-tw)/2:y={y}:alpha='min(1,max(0,(t-{a})/0.25))'"
                  for f, t, s, c, y, a in L)
    bar = f"drawbox=x=(iw-{220 if vertical else 180})/2:y={cy - 34}:w={220 if vertical else 180}:h=5:color={acc}:t=fill"
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b0b0d:s={W}x{H}:r=24:d={d:.3f}",
         "-vf", f"{bar},{vf},fade=t=in:st=0:d=0.2", "-an"] + ENC + [out])


def music_start(music, beat):
    """first strong downbeat (energy comb over 4-beat bars), then skip one bar of intro, so cuts land on hits."""
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", music, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(b, np.int16).astype(np.float32); hop = 80; e = np.sqrt(np.add.reduceat(x * x, np.arange(0, len(x), hop)) / hop)
    on = np.maximum(0, np.diff(e, prepend=e[0])); bar = int(round(4 * beat * 100))
    ph = int(np.argmax([on[p::bar][:16].sum() for p in range(bar)])) / 100.0
    return ph + bar / 100


def build(film, vertical):
    beat = 60.0 / film["bpm"]; tag = film["id"] + ("_9x16" if vertical else "")
    parts = [shot(tag, s[0], s[1], s[2], beat, (s[3] if len(s) > 3 else 0.5) if vertical else None) for s in film["shots"]]
    cb = film.get("card_beats", 6); cp = f"{TMP}/{tag}_card.mp4"; card(cp, cb * beat, film, vertical); parts.append(cp)
    starts = np.cumsum([0] + [s[2] for s in film["shots"]]) * beat; total = starts[-1] + cb * beat
    pic = f"{TMP}/{tag}_pic.mp4"; concat(parts, pic, total)
    # disclosure on frame 1 (first 2.6 s), small, bottom centre
    W, H = (1080, 1920) if vertical else (1280, 720)
    disc = (f"drawbox=x=0:y={H - (150 if vertical else 46)}:w=iw:h={70 if vertical else 46}:color=black@0.35:t=fill:enable='lt(t,2.6)',"
            f"drawtext=fontfile={FONT_R}:text='{esc(DISCLOSURE)}':fontsize={26 if vertical else 18}:fontcolor=white@0.92:x=(w-tw)/2:"
            f"y={H - (126 if vertical else 32)}:enable='lt(t,2.6)'")
    music = f"{HERE}/music/{film['music']}.wav"; ms = music_start(music, beat); w, h = sfx()
    ins = ["-i", pic, "-ss", f"{ms:.3f}", "-i", music]; fc = [f"[0:v]{disc}[v]"]; tags = []
    cuts = [(t, "hit" if (k < len(film["shots"]) and len(film["shots"][k]) > 4 and film["shots"][k][4] == "hit") else "whoosh") for k, t in enumerate(starts[1:])]
    for k, (t, kind) in enumerate(cuts):
        ins += ["-i", h if kind == "hit" or k == len(cuts) - 1 else w]; n = 2 + k
        at = max(0.0, t - (0.0 if kind == "hit" or k == len(cuts) - 1 else 0.36)); ms_ = int(at * 1000)
        fc.append(f"[{n}:a]adelay={ms_}|{ms_},volume={0.55 if kind == 'whoosh' else 0.8}[s{k}]"); tags.append(f"[s{k}]")
    vo_tags = []; base = 2 + len(cuts)
    for k, (vid, bpos) in enumerate(film["vo"]):
        vf = f"{HERE}/vo/{film['id']}_{vid}.wav"
        if not os.path.exists(vf): print("MISSING VO", film["id"], vid, flush=True); continue
        if vid == "cta": bpos = sum(s[2] for s in film["shots"]) + 1.5   # always just after the end card appears
        ins += ["-i", vf]; n = base + len(vo_tags); ms_ = int(bpos * beat * 1000)
        fc.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms_}|{ms_},volume=1.7[vo{k}]"); vo_tags.append(f"[vo{k}]")
    fo = max(0, total - 1.4)
    fc.append(f"[1:a]atrim=0:{total:.3f},aformat=sample_rates=48000:channel_layouts=stereo,volume=0.7,afade=t=in:st=0:d=0.15,afade=t=out:st={fo:.2f}:d=1.4[mus]")
    fc.append(f"{''.join(tags)}amix=inputs={len(tags)}:normalize=0,apad,atrim=0:{total:.3f}[sfx]")
    if vo_tags:
        fc.append(f"{''.join(vo_tags)}amix=inputs={len(vo_tags)}:normalize=0,apad,atrim=0:{total:.3f},asplit=2[voA][voK]")
        fc.append("[mus][voK]sidechaincompress=threshold=0.03:ratio=5:attack=12:release=320[musd]")
        fc.append("[musd][sfx][voA]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.0,aresample=48000[ao]")
    else:
        fc.append("[mus][sfx]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.0,aresample=48000[ao]")
    out = f"{OUT}/{tag}.mp4"
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[ao]"] + ENC
        + ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}", out])
    print("OK", tag, round(dur(out), 2), "s", flush=True)


if __name__ == "__main__":
    for f in FILMS:
        if ONLY and f["id"] not in ONLY: continue
        missing = [s[0] for s in f["shots"] if not os.path.exists(f"{CLIPS}/{s[0]}.mp4")]
        if missing: print("SKIP", f["id"], "missing clips", missing, flush=True); continue
        build(f, False); build(f, True)
    print("CUT_V2_DONE")
