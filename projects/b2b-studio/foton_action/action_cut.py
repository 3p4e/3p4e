# Foton Tunland V9 action films: beat-snapped hard cuts + speed ramps (fast -> slow motion -> fast) inside shots.
# Runs on LTX stand-in clips locally (test) and on the H3 box (real): clip dir, prefix, output dir and credit come from args.
#   python3 action_cut.py <clipdir> <clip_prefix> <outdir> <credit> [music] [vo_dir]
# Outputs: foton_action_30s.mp4 (16:9), foton_action_reel_15s_9x16.mp4, foton_action_bumper_6s.mp4 + _9x16.
import os, sys, json, subprocess, numpy as np
CLIPS, PFX, OUT, CREDIT = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = sys.argv[5] if len(sys.argv) > 5 else f"{HERE}/music.mp3"; VO = sys.argv[6] if len(sys.argv) > 6 else f"{HERE}/vo"
TMP = f"{OUT}/tmp_action"; os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BPM = 120.0; BEAT = 60 / BPM
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def has_audio(f): return "audio" in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", f], capture_output=True, text=True).stdout
def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")
def clip(i): return f"{CLIPS}/{PFX}{i}.mp4"
def atempo(s):
    out = []
    while s < 0.5: out.append("atempo=0.5"); s /= 0.5
    while s > 2.0: out.append("atempo=2.0"); s /= 2.0
    return out + [f"atempo={s:.4f}"]

# shot spec: (clip id, [(src_a, src_b, speed, flag)], beats); flag 'adj' = this segment absorbs the timing to land on the beat
FILM = [("a01", [(0.0, 2.6, 1.4, "adj")], 4),
        ("a02", [(0.4, 2.6, 1.1, "adj")], 4),
        ("a03", [(0.0, 1.1, 1.25, ""), (1.1, 2.0, 0.32, "adj"), (2.0, 3.3, 1.7, "")], 9),
        ("a04", [(0.3, 1.5, 0.55, "adj")], 4),
        ("a05", [(0.4, 2.4, 1.0, "adj")], 4),
        ("a06", [(0.0, 1.0, 1.5, ""), (1.0, 2.2, 0.6, "adj")], 5),
        ("a07", [(0.4, 3.6, 1.3, "adj")], 5),
        ("a08", [(0.0, 0.8, 1.0, ""), (0.8, 1.6, 0.35, "adj"), (1.6, 2.7, 2.0, "")], 7),
        ("a09", [(0.0, 2.6, 1.3, "adj")], 4),
        ("a10", [(0.0, 4.6, 1.0, "adj")], 8)]
FILM_VO = [("act_1", 1.0), ("act_2", 5.4), ("act_3", 8.9), ("act_4", 10.9), ("act_5", 15.1), ("act_6", 21.1), ("act_7", 24.0), ("act_8", 27.6)]
REEL = [("a03", [(0.0, 1.1, 1.25, ""), (1.1, 2.0, 0.32, "adj"), (2.0, 3.3, 1.7, "")], 7, 0.55),
        ("a04", [(0.3, 1.5, 0.6, "adj")], 3, 0.5), ("a05", [(0.4, 2.0, 1.0, "adj")], 3, 0.62),
        ("a08", [(0.0, 0.8, 1.0, ""), (0.8, 1.6, 0.35, "adj"), (1.6, 2.7, 2.0, "")], 6, 0.5),
        ("a10", [(0.5, 4.0, 1.0, "adj")], 5, 0.5)]
REEL_VO = [("act_2", 1.4), ("act_3", 3.7), ("act_4", 5.2), ("act_7", 9.8), ("act_8", 12.4)]
BUMP = [("a03", [(0.6, 1.1, 1.0, ""), (1.1, 2.0, 0.3, "adj"), (2.0, 2.8, 1.6, "")], 7, 0.55), ("a10", [(2.0, 4.0, 1.0, "adj")], 3, 0.5)]
BUMP_VO = [("act_7", 3.6)]

def shot(name, cid, segs, beats, vertical=None):
    """Render one shot with its speed ramps; total length = beats * BEAT exactly."""
    src = clip(cid); cd = dur(src); target = beats * BEAT
    segs = [(a, min(b, cd - 0.05), s, f) for a, b, s, f in segs]
    fixed = sum((b - a) / s for a, b, s, f in segs if f != "adj"); a0, b0, _, _ = [x for x in segs if x[3] == "adj"][0]
    adj_speed = (b0 - a0) / max(0.2, target - fixed)
    aud = has_audio(src); parts = []
    for k, (a, b, s, f) in enumerate(segs):
        s = adj_speed if f == "adj" else s
        geo = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720" if vertical is None else \
              f"scale=-2:1920,crop=1080:1920:(iw-1080)*{vertical}:0"
        v = f"trim=start={a}:end={b},setpts=PTS-STARTPTS,{geo},setpts=PTS/{s:.4f}"
        v += ",minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if s < 0.9 else ",fps=24"
        p = f"{TMP}/{name}_{cid}_{k}.mp4"
        if aud:
            af = f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS," + ",".join(atempo(s)) + f",volume={0.55 if s < 0.9 else 1.0},aresample=48000"
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", f"[0:v]{v}[v];[0:a]{af}[a]", "-map", "[v]", "-map", "[a]",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", p])
        else:
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", f"[0:v]{v}[v]",
                 "-map", "[v]", "-map", "1:a", "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", p])
        parts.append(p)
    out = f"{TMP}/{name}_{cid}.mp4"; concat(parts, out, target); return out

def concat(parts, out, exact=None):
    lst = out + ".txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    a = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst]
    if exact: a += ["-t", f"{exact:.3f}"]
    run(a + ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out])

def card(out, d, vertical=False):
    W, H = (1080, 1920) if vertical else (1280, 720); y0 = H // 2 - (160 if vertical else 120)
    lines = [(FONTB, "FOTON · TUNLAND V9", 64 if vertical else 66, "white", y0), (FONT, "Закажи тест возење.", 44, "0xf2c14e", y0 + 100),
             (FONT, "2.0 L турбо дизел · 48V хибрид · 4×4", 30 if vertical else 28, "0xdddddd", y0 + 175),
             (FONT, "Концепт изработен само за презентација на Foton Македонија.", 20 if vertical else 18, "0x999999", H - (190 if vertical else 110)),
             (FONT, "Не е објавен и нема да биде објавен без нивно изречно писмено одобрение.", 20 if vertical else 18, "0x999999", H - (160 if vertical else 84)),
             (FONT, CREDIT, 20 if vertical else 18, "0x888888", H - (130 if vertical else 58))]
    vf = ",".join(f"drawtext=fontfile={f}:text='{esc(t)}':fontsize={s}:fontcolor={c}:x=(w-tw)/2:y={y}" for f, t, s, c, y in lines) + ",fade=t=in:st=0:d=0.25"
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0d0d0f:s={W}x{H}:r=24:d={d}", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
         "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "1:a", "-t", str(d), "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out])

def build(name, spec, vos, card_beats, vertical=False, music_start=0.0):
    parts = [shot(name, s[0], s[1], s[2], (s[3] if vertical else None) if len(s) > 3 or vertical else None) for s in spec]
    cp = f"{TMP}/{name}_card.mp4"; card(cp, card_beats * BEAT, vertical); parts.append(cp)
    total = sum(s[2] for s in spec) * BEAT + card_beats * BEAT
    pic = f"{TMP}/{name}_pic.mp4"; concat(parts, pic, total)
    ins = ["-i", pic, "-ss", f"{music_start:.3f}", "-i", MUSIC]; fc = []; vo_tags = []
    for k, (vid, t) in enumerate(vos):
        vf = f"{VO}/{vid}.wav"
        if not os.path.exists(vf): print("MISSING VO", vid, flush=True); continue
        ins += ["-i", vf]; n = 2 + len(vo_tags); ms = int(t * 1000)
        fc.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms},volume=1.6[vo{k}]"); vo_tags.append(f"[vo{k}]")
    fo = max(0, total - 1.6)
    fc.append(f"[1:a]atrim=0:{total:.3f},aformat=sample_rates=48000:channel_layouts=stereo,volume=0.62,afade=t=in:st=0:d=0.3,afade=t=out:st={fo:.2f}:d=1.6[mus]")
    fc.append(f"[0:a]volume=0.5[amb]")
    if vo_tags:
        fc.append(f"{''.join(vo_tags)}amix=inputs={len(vo_tags)}:normalize=0,apad,atrim=0:{total:.3f},asplit=3[voA][voK1][voK2]")
        fc.append("[mus][voK1]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350[musd]")
        fc.append("[amb][voK2]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=300[ambd]")
        fc.append("[musd][ambd][voA]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.0,aresample=48000[ao]")
    else:
        fc.append("[mus][amb]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.0,aresample=48000[ao]")
    out = f"{OUT}/{name}.mp4"
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[ao]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-t", f"{total:.3f}", out])
    print("OK", name, round(dur(out), 2), "s", flush=True); return out

def downbeat(music):
    """first strong downbeat of the 120 BPM track (energy comb over 4-beat bars), so cuts land on hits"""
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", music, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(b, np.int16).astype(np.float32); hop = 80; e = np.sqrt(np.add.reduceat(x * x, np.arange(0, len(x), hop)) / hop)
    on = np.maximum(0, np.diff(e, prepend=e[0])); bar = int(4 * BEAT * 100)
    sc = [on[ph::bar][:16].sum() for ph in range(bar)]; ph = int(np.argmax(sc)) / 100.0
    return ph + bar / 100 * 2   # skip the intro: start two bars after the first strong downbeat phase

if __name__ == "__main__":
    ms = downbeat(MUSIC); print("music start", round(ms, 2), flush=True)
    build("foton_action_30s", FILM, FILM_VO, 7, False, ms)
    build("foton_action_reel_15s_9x16", REEL, REEL_VO, 6, True, ms)
    build("foton_action_bumper_6s", BUMP, BUMP_VO, 3, False, ms)
    build("foton_action_bumper_6s_9x16", BUMP, BUMP_VO, 3, True, ms)
    print("ACTION_DONE")
