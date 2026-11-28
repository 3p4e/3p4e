# BIG DOGMA public showreel: 16:9 1920x1080 + 9:16 1080x1920, cut to the bar grid of 8_showreel.mp3.
# 9:16 reframe: close-ups (FULL916) get a full-height 396x704 crop; every other shot keeps a gentler 560x704 (4:5) crop,
# scaled to a 1080x1358 band over a blurred, darkened cover of the same shot (same look as the 9:16 film masters).
# usage: python3 showreel.py [16x9|9x16|audio|all]
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import SUFFIX                                        # _PLACEHOLDER-CONTACT while brand.json holds placeholder contact data
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; OUT = f"{S}/launch/video"; SEG = f"{W}/seg"; os.makedirs(SEG, exist_ok=True)
FONTS = f"{S}/brand/fonts"
MUSIC = f"{S}/music/ace_final/8_showreel.mp3"; M0 = 4.10          # music in-point = first big hit
FPS = 24; BEAT = 2.0875 / 4                                       # ~115 bpm, bar = 2.0875 s
def fb(b): return round(b * BEAT * FPS)                           # beat -> frame
LOGO_B, END_B = 88, 96; END_T = 55.7
N_END = round(END_T * FPS) - fb(END_B)
def run(a, **k): subprocess.run(a, check=True, **k)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def clip(n):
    for d in ("ltx25", "ltx610"):
        p = f"{S}/{d}/{n}.mp4"
        if os.path.exists(p): return p
    raise FileNotFoundError(n)

# (beat_in, beat_out, clip, source in-point s, speed, 9:16 crop centre 0..1, fx)
EDL = [
    (0, 4, "br_c08_s2", 2.6, 1.0, .42, "dim"), (4, 5, "x_con_x2", 2.5, 1.0, .50, "dim"), (5, 6, "tl2_garden_2", 1.0, 2.0, .45, "dim"),
    (6, 7, "br_c12_s1", 2.0, 1.0, .50, "dim"), (7, 8, "x_re_x2", 3.5, 1.0, .50, "dim"),
    # tl_01_dig was dropped: its excavator and trucks melt (0.3, 1.0-1.4, 2.7-3.2, 4.0-4.4 s); tl_02_pour 0.1-1.14 s is clean
    # (its pump boom folds into a tangle from 1.4 s), so the pour gets 2 beats and the frame time-lapse 4
    (8, 10, "tl_02_pour", 0.1, 1.0, .50, ""), (10, 14, "tl_03_frame", 0.5, 2.5, .50, ""), (14, 16, "tl_06_handover", 2.0, 1.5, .45, ""),
    # x_re_x1 (lobby): only 0-0.83 s, before a dark sleeve reaches through the glass door with no body (0.85-1.75 s);
    # played at 0.8x over 2 beats (near-static moment), the rooftop x_re_x2 takes the third beat
    (16, 19, "br_c09_s3to4", 0.8, 2.5, .50, ""), (19, 21, "x_re_x1", 0.0, 0.8, .55, ""), (21, 24, "x_re_x2", 0.5, 1.0, .50, ""),
    (24, 27, "br_c10_s2to3", 0.5, 2.5, .50, ""), (27, 30, "st_03_styled", 0.5, 2.0, .55, ""), (30, 32, "x_int_x2", 1.5, 1.0, .42, ""),
    (32, 35, "x_food_x2", 1.0, 1.0, .45, ""), (35, 38, "br_c06_s2", 3.0, 1.0, .50, ""), (38, 40, "x_food_x1", 1.0, 1.0, .50, ""),
    (40, 43, "br_c07_s1", 1.0, 1.0, .60, ""), (43, 46, "br_c07_s2", 2.0, 1.0, .45, ""), (46, 48, "x_wine_x1", 3.0, 1.0, .42, ""),
    (48, 51, "br_c08_s3", 1.0, 1.0, .55, ""), (51, 54, "x_steel_x1", 1.5, 1.0, .30, ""), (54, 56, "x_steel_x2", 1.0, 1.0, .60, ""),
    (56, 60, "tl2_solar_2", 4.0, 0.95, .50, ""),                    # finished roof only: tl2_solar_1 and solar_2 before 4 s show morphing workers/panels
    (60, 64, "tl2_road_2", 0.5, 1.5, .50, "dim"),
    (64, 67, "x_prod_x1", 0.3, 1.0, .50, ""), (67, 70, "br_c12_s2", 1.0, 1.0, .50, ""), (70, 72, "x_prod_x2", 2.0, 1.0, .55, ""),
    (72, 75, "x_auto_x1", 1.0, 1.0, .40, ""), (75, 78, "x_pharma_x1", 1.0, 1.0, .50, ""), (78, 80, "br_c04_s4", 1.0, 1.0, .40, ""),
    (80, 81, "br_c03_s2to3", 3.0, 1.0, .50, "dim"), (81, 82, "x_rec_x2", 2.0, 1.0, .50, "dim"), (82, 83, "tl2_expo_2", 3.0, 1.5, .50, "dim"),
    (83, 84, "tl2_store_2", 3.5, 1.5, .50, "dim"), (84, 85, "br_c11_s1", 1.0, 1.0, .50, "dim"), (85, 86, "x_apt_x2", 3.0, 1.0, .50, "dim"),
    (86, 87, "br_c05_s2", 1.0, 1.0, .55, "dim"), (87, 88, "tl_06_handover", 4.0, 1.0, .45, "dim"),
]
SECTORS = [(8, 16, "ГРАДЕЖНИШТВО"), (16, 24, "НЕДВИЖНОСТИ"), (24, 32, "ВНАТРЕШЕН ДИЗАЈН"), (32, 40, "ХРАНА"), (40, 48, "ВИНО"),
           (48, 56, "ЧЕЛИК И ЦЕМЕНТ"), (56, 60, "ЕНЕРГЕТИКА"), (64, 72, "ЛАНСИРАЊЕ НА ПРОИЗВОДИ"), (72, 80, "ИНДУСТРИЈА")]
GOLD = "&H4EC1F2&"
FULL916 = {"br_c08_s2", "x_food_x2", "br_c07_s2", "x_steel_x1", "br_c12_s2"}   # close-ups that hold a full 9:16 crop
BAND_H = 1358; BAND_Y = (1920 - BAND_H) // 2                        # 560x704 -> 1080x1358 (1.93x instead of 2.73x)

def seg(i, e, asp):
    b0, b1, name, ss, sp, cx, fx = e
    n = fb(b1) - fb(b0); src = clip(name); need = n / FPS * sp
    if ss + need > dur(src) - 0.05: ss = max(0.0, dur(src) - 0.05 - need)
    assert ss + need <= dur(src), (name, ss, need)
    grade = ",eq=brightness=-0.045:contrast=1.04,vignette=angle=PI/4.5" if fx == "dim" else ""
    pre = f"setpts=(PTS-STARTPTS)/{sp},fps={FPS}"
    x = min(max(round(cx * 1280 - 198), 0), 1280 - 396)
    if asp == "16x9": vf = f"{pre},scale=1964:1080:flags=lanczos,crop=1920:1080,unsharp=5:5:0.35{grade},setsar=1"
    elif name in FULL916 or b0 >= 80:                                # close-ups and the one-beat closing montage
        vf = f"{pre},crop=396:704:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5{grade},setsar=1"
    else:
        xb = min(max(round(cx * 1280 - 280), 0), 1280 - 560)
        vf = (f"{pre},split[a][b];[a]crop=396:704:{x}:0,scale=270:480,boxblur=10:2,eq=brightness=-0.2:saturation=0.85,scale=1080:1920[bg];"
              f"[b]crop=560:704:{xb}:0,scale=1080:{BAND_H}:flags=lanczos,unsharp=5:5:0.4[fg];[bg][fg]overlay=0:{BAND_Y}{grade},setsar=1")
    out = f"{SEG}/sr_{asp}_{i:02d}.mp4"
    run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", src, "-filter_complex", vf,
         "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out])
    return out

def tc(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def ass(asp):
    v = asp == "16x9"; PX, PY = (1920, 1080) if v else (1080, 1920)
    T = lambda b: b * BEAT
    L = [f"[Script Info]\nScriptType: v4.00+\nPlayResX: {PX}\nPlayResY: {PY}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n",
         "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         f"Style: Big,Russo One,{124 if v else 116},&H00FFFFFF,&H00FFFFFF,&H70000000,&H90000000,0,0,0,0,100,100,2,0,1,3,5,5,0,0,0,1",
         f"Style: Sector,Russo One,{68 if v else 76},&H00FFFFFF,&H00FFFFFF,&H70000000,&H90000000,0,0,0,0,100,100,2,0,1,2.5,4,1,0,0,0,1",
         f"Style: Kick,Oswald,{32 if v else 34},&H004EC1F2,&H00FFFFFF,&H90000000,&H90000000,1,0,0,0,100,100,6,0,1,2,2,1,0,0,0,1",
         "Style: Bar,Russo One,10,&H004EC1F2,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
         "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    def ev(t0, t1, st, txt, layer=1): L.append(f"Dialogue: {layer},{tc(t0)},{tc(t1)},{st},,0,0,0,,{txt}")
    punch = r"\fad(90,140)\fscx120\fscy120\t(0,190,\fscx100\fscy100)"
    cxp, cyp = PX // 2, PY // 2 - (0 if v else 60)
    # hook
    ev(0.0, T(4) - 0.04, "Big", "{\\an5\\pos(%d,%d)\\fad(0,120)}ОВА НЕ Е%sСНИМЕНО." % (cxp, cyp, " " if v else "\\N"))
    ev(T(4), T(8) - 0.04, "Big", "{\\an5\\pos(%d,%d)%s}ОВА Е {\\c%s}AI." % (cxp, cyp, punch, GOLD))
    # sector captions: gold kicker "AI ВИДЕО ЗА" + sector name + growing gold bar
    for b0, b1, name in SECTORS:
        t0, t1 = T(b0) + 0.12, T(b1) - 0.10
        if v:
            x, ybase = 110, 990; nm = name; kick_y = ybase - 82; bar_y = ybase + 18
        else:
            lines = name.split(" ", 1) if len(name) > 12 else [name]; nm = "\\N".join(lines)
            x, ybase = 70, 1410; kick_y = ybase - 88 * len(lines) - 14; bar_y = ybase + 16
        ev(t0, t1, "Kick", "{\\an1\\pos(%d,%d)\\fad(160,140)}AI ВИДЕО ЗА" % (x + 4, kick_y))
        ev(t0 + 0.06, t1, "Sector", "{\\an1\\move(%d,%d,%d,%d,0,240)\\fad(180,140)}%s" % (x - 40, ybase, x, ybase, nm))
        ev(t0 + 0.06, t1, "Bar", "{\\an7\\pos(%d,%d)\\fad(0,140)\\fscx0\\t(60,420,\\fscx100)\\p1}m 0 0 l 150 0 150 7 0 7{\\p0}" % (x + 4, bar_y))
    # statement in the musical break
    lines = ["БЕЗ КАМЕРА.", "БЕЗ ЕКИПА.", f"{{\\c{GOLD}}}БЕЗ ЧЕКАЊЕ."]
    for k, txt in enumerate(lines):
        y = (cyp - 125 + k * 125) if v else (cyp - 130 + k * 130)
        ev(T(60 + k), T(64) - 0.04, "Big", "{\\an5\\pos(%d,%d)\\fs%d%s}%s" % (cxp, y, 100 if v else 96, punch, txt))
    # final montage line
    ev(T(80), T(88) - 0.04, "Big", "{\\an5\\pos(%d,%d)%s}ВАШАТА ПРИКАЗНА\\N{\\c%s}Е СЛЕДНА." % (cxp, cyp, punch, GOLD) if v else
       "{\\an5\\pos(%d,%d)%s}ВАШАТА\\NПРИКАЗНА\\N{\\c%s}Е СЛЕДНА." % (cxp, cyp, punch, GOLD))
    p = f"{W}/showreel_{asp}.ass"; open(p, "w", encoding="utf-8").write("\n".join(L) + "\n"); return p

def audio():
    raw = f"{SEG}/sr_audio_raw.wav"; out = f"{SEG}/sr_audio.wav"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(M0), "-t", str(END_T), "-i", MUSIC, "-af",
         f"afade=t=in:st=0:d=0.012,afade=t=out:st=54.0:d=0.8,apad=whole_dur={END_T},aresample=48000", "-ac", "2", raw])
    loudnorm(raw, out)
    return out
def loudnorm(src, out, I=-14.0, TP=-1.0):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={I}:TP={TP}:LRA=20:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af",
         f"loudnorm=I={I}:TP={TP}:LRA=20:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000",
         "-c:a", "pcm_s16le", out])

def build(asp):
    v = asp == "16x9"; PX, PY = (1920, 1080) if v else (1080, 1920)
    segs = [seg(i, e, asp) for i, e in enumerate(EDL)]
    lst = f"{SEG}/sr_{asp}.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    a = ass(asp); wm, wx, wy = (f"{W}/png/wm_96.png", 30, 24) if v else (f"{W}/png/wm_110.png", 34, 196)
    disc = f"{W}/png/disc_top_{asp}.png"; DT = fb(8) / FPS - 0.02       # AI-disclosure pill over the hook, 0 .. 4.15 s (fades out over the last 0.4 s)
    E = f"{W}/png/end_{asp}"; nb = fb(LOGO_B); nl = fb(END_B) - fb(LOGO_B); X = 10   # crossfade frames logo->card
    tb = nb / FPS; tl = nl / FPS; te = (N_END + X) / FPS
    fc = (f"[0:v]ass={a}:fontsdir={FONTS}[b0];[4:v]format=rgba,colorchannelmixer=aa=0.85[wm];[b0][wm]overlay={wx}:{wy}:format=auto:shortest=1,setsar=1[bw];"
          f"[7:v]format=rgba,fade=t=out:st={DT - 0.4:.3f}:d=0.4:alpha=1[dp];[bw][dp]overlay=0:0:format=auto:eof_action=pass,setsar=1[body];"
          f"[1:v]trim=start_frame=0:end_frame={nl},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[lg];"
          f"[2:v]fps={FPS},trim=end_frame={N_END + X},setpts=PTS-STARTPTS,format=rgba[ea];"
          f"[5:v]fps={FPS},trim=end_frame={N_END + X},setpts=PTS-STARTPTS,format=rgba,fade=t=in:st=0.45:d=0.45:alpha=1[eb];"
          f"[6:v]fps={FPS},trim=end_frame={N_END + X},setpts=PTS-STARTPTS,format=rgba,fade=t=in:st=1.0:d=0.5:alpha=1[ec];"
          f"[ea][eb]overlay=x=0:y='max(0,24-24*(t-0.45)/0.45)':format=auto[e1];[e1][ec]overlay=0:0:format=auto,format=yuv420p,fade=t=out:st={te - 0.45:.3f}:d=0.45,settb=1/{FPS},setsar=1[end];"
          f"[lg][end]xfade=transition=fade:duration={X / FPS:.4f}:offset={(nl - X) / FPS:.4f}[le];"
          f"[body][le]concat=n=2:v=1:a=0,format=yuv420p[v]")
    out = f"{OUT}/bigdogma_showreel_{asp}{SUFFIX}.mp4"
    run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", f"{SEG}/logo_{asp}.mp4",
         "-loop", "1", "-t", "8", "-i", f"{E}_A.png", "-i", f"{SEG}/sr_audio.wav", "-loop", "1", "-t", "50", "-i", wm, "-loop", "1", "-t", "8", "-i", f"{E}_B.png", "-loop", "1", "-t", "8", "-i", f"{E}_C.png",
         "-loop", "1", "-t", f"{DT:.3f}", "-i", disc,                                     # 7 disclosure pill on the hook
         "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-t", f"{END_T:.3f}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out])
    print("OK", out, round(dur(out), 2), flush=True)

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("frames body", fb(LOGO_B), "logo", fb(END_B) - fb(LOGO_B), "end", N_END)
    if what in ("audio", "all"): audio()
    for asp in ("16x9", "9x16"):
        if what in (asp, "all"): build(asp)
