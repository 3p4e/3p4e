# BIG DOGMA studio showreel v2 (2026-11-27): the same music, bar grid, hook, sector captions, statement, logo close and end card as
# showreel.py, re-cut from the strongest shots of the category films v2 (catfilms/clips, 271 LTX 2.5 clips reviewed on contact sheets)
# and closed on an AI logo film. 9:16: native vertical social shots where a sector has one, else a full-height 396x704 crop
# (no blurred cover band), centre picked per shot.
# usage: python3 showreel2.py [audio|16x9|9x16|all]   -> $SR/out/bigdogma_showreel_v2_<asp>.mp4
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import SUFFIX
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; SR = os.environ.get("SR", "/dev/shm/vall/sr"); SEG = f"{SR}/seg"; OUT = f"{SR}/out"
for d in (SEG, OUT): os.makedirs(d, exist_ok=True)
FONTS = f"{S}/brand/fonts"; CLIPS = f"{S}/catfilms/clips"
MUSIC = f"{S}/music/ace_final/8_showreel.mp3"; M0 = 4.10          # music in-point = first big hit
FPS = 24; BEAT = 2.0875 / 4                                       # ~115 bpm, bar = 2.0875 s
def fb(b): return round(b * BEAT * FPS)
LOGO_B, END_B = 88, 96; END_T = 55.7
N_END = round(END_T * FPS) - fb(END_B)
# logo close: an AI logo film (16:9) from LOGO_SS for 8 beats; 9:16 (the BD mark is wider than a 9:16 crop): the end card's own lockup layer
# fading in (seg/outro_end_9x16.mp4 from outro_still.py), so the offer then simply joins it (no drawn logo animation, owner 2026-11-27)
LOGO16 = os.environ.get("LOGO16", f"{W}/seg/logo_16x9.mp4"); LOGO_SS = float(os.environ.get("LOGO_SS", "0"))
LOGO9 = f"{W}/seg/outro_end_9x16.mp4"
def run(a, **k): subprocess.run(a, check=True, **k)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

# (beat_in, beat_out, 16:9 shot (clip, in-point s, speed), 9:16 shot or None, 9:16 crop centre 0..1 when None, fx)
# clips are catfilms/clips/cf_<name>.mp4, 5.04 s: story/explainer/transform shots are 1280x704; *_social_* shots are native 704x1280,
# so the 9:16 cut uses them where a sector has one and crops a 396x704 window out of the 16:9 shot otherwise
H = lambda n, ss=1.5, sp=1.0: (n, ss, sp)
EDL = [
    # hook: "ОВА НЕ Е СНИМЕНО." over molten metal, then four one-beat cuts under "ОВА Е AI."
    (0, 4, H("steel_cement_1_explainer_s1", 2.0), H("industry_showreel_2_social_s1", 2.6), .5, "dim"),
    (4, 5, H("horeca_2_story_s2", 2.0), None, .62, "dim"),
    (5, 6, H("it_3_explainer_s3", 2.0), H("wine_1_social_s1", 1.6), .5, "dim"),
    (6, 7, H("road_2_story_s6", 2.0), H("automotive_1_social_s3", 2.0), .5, "dim"),
    (7, 8, H("it_1_story_s6", 2.0), H("it_2_social_s1", 3.2), .5, "dim"),
    # construction: empty land -> structure (time-lapse 2.4x), frame -> brick, the finished block at night
    (8, 12, H("construction_1_transform_s1", 0.0, 2.4), None, .55, ""),
    (12, 14, H("construction_1_transform_s2", 2.6), None, .5, ""),
    (14, 16, H("construction_1_transform_s4", 3.0), None, .5, ""),
    # real estate: ruin -> lakeside villa, balcony over the city / penthouse terrace, lake hotel / the city at night
    (16, 20, H("developer_2_transform_s2", 0.0, 2.4), None, .6, ""),
    (20, 22, H("real_estate_2_explainer_s6", 1.5), H("construction_2_social_s3", 0.5), .5, ""),
    (22, 24, H("recruitment_1_story_s1", 2.0), H("real_estate_1_social_s3", 2.0), .62, ""),
    # interior design: bare room -> furnished, bedroom over the lake / armchair at sunset, pool terrace / pampas table
    (24, 28, H("interior_design_1_transform_s1", 0.0, 2.4), None, .55, ""),
    (28, 30, H("interior_design_2_story_s2", 1.5), H("apartment_staging_2_social_s3", 1.5), .4, ""),
    (30, 32, H("interior_design_2_story_s6", 1.5), H("apartment_staging_2_social_s2", 1.5), .55, ""),
    # food: roasting peppers, steaks over embers / the grill, latte pour, steak plate / yoghurt pour
    (32, 34, H("food_1_story_s4", 1.5), None, .5, ""),
    (34, 36, H("horeca_3_transform_s2", 2.5), H("horeca_1_social_s1", 2.5), .5, ""),
    (36, 38, H("horeca_2_story_s4", 2.0), None, .55, ""),
    (38, 40, H("horeca_2_story_s3", 2.0), H("food_2_social_s2", 2.0), .5, ""),
    # wine: misty vineyard / vine at sunset, grapes into the crate, decanter / barrel cellar
    (40, 43, H("wine_2_story_s1", 1.0), H("wine_1_social_s2", 1.5), .5, ""),
    (43, 45, H("wine_2_story_s3", 2.0), None, .52, ""),
    (45, 48, H("wine_2_story_s5", 1.5), H("wine_1_social_s3", 1.5), .64, ""),
    # steel and cement: glowing slabs / demolition, concrete pour, the plant under the mountains / the silo
    (48, 51, H("steel_cement_1_explainer_s2", 1.5), H("steel_cement_2_social_s2", 1.5), .5, ""),
    (51, 53, H("steel_cement_1_explainer_s5", 2.0), None, .5, ""),
    (53, 56, H("steel_cement_1_explainer_s4", 1.0), H("steel_cement_2_social_s1", 1.5), .42, ""),
    # energy: tiles -> solar roof, sunset over the panels / the solar farm from above
    (56, 58, H("solar_2_transform_s1", 0.5, 2.0), None, .5, ""),
    (58, 60, H("solar_1_explainer_s7", 2.0), H("industry_showreel_2_social_s3", 2.0), .5, ""),
    # musical break: "БЕЗ КАМЕРА. / БЕЗ ЕКИПА. / БЕЗ ЧЕКАЊЕ." over the sea of clouds
    (60, 64, H("tourism_3_explainer_s7", 0.5), None, .55, "dim"),
    # product launch: powder burst / sneaker over the city, espresso drip / sneaker on wet asphalt, espresso pour / headphones
    (64, 67, H("product_launch_2_explainer_s3", 1.0), H("product_launch_1_social_s1", 1.5), .5, ""),
    (67, 69, H("product_launch_2_explainer_s4", 2.0), H("product_launch_1_social_s2", 2.0), .55, ""),
    (69, 72, H("product_launch_2_explainer_s5", 1.5), H("it_2_social_s2", 1.5), .5, ""),
    # tourism: misty lake at dawn / cocoa above the snowy peaks, the boat, the lantern boardwalk
    (72, 75, H("tourism_2_story_s1", 1.0), H("tourism_1_social_s1", 1.5), .6, ""),
    (75, 77, H("tourism_2_story_s2", 2.0), None, .45, ""),
    (77, 80, H("tourism_2_story_s6", 1.5), None, .35, ""),
    # one-beat montage under "ВАШАТА ПРИКАЗНА Е СЛЕДНА."
    (80, 81, H("industry_showreel_1_story_s1", 2.5), None, .45, "dim"),
    (81, 82, H("it_3_explainer_s7", 2.0), H("it_2_social_s3", 3.0), .45, "dim"),
    (82, 83, H("store_fitout_1_transform_s3", 3.4), None, .5, "dim"),
    (83, 84, H("expo_stand_1_transform_s1", 2.8), H("health_2_social_s1", 3.0), .5, "dim"),
    (84, 85, H("pharma_1_explainer_s3", 2.0), None, .5, "dim"),
    (85, 86, H("automotive_2_explainer_s3", 2.0), H("automotive_1_social_s1", 2.5), .5, "dim"),
    (86, 87, H("textile_3_story_s1", 2.0), H("textile_2_social_s2", 2.5), .5, "dim"),
    (87, 88, H("landscaping_1_transform_s1", 3.6), None, .5, "dim"),
]
SECTORS = [(8, 16, "ГРАДЕЖНИШТВО"), (16, 24, "НЕДВИЖНОСТИ"), (24, 32, "ВНАТРЕШЕН ДИЗАЈН"), (32, 40, "ГАСТРОНОМИЈА"), (40, 48, "ВИНО"),
           (48, 56, "ЧЕЛИК И ЦЕМЕНТ"), (56, 60, "ЕНЕРГЕТИКА"), (64, 72, "ЛАНСИРАЊЕ НА ПРОИЗВОДИ"), (72, 80, "ТУРИЗАМ")]
GOLD = "&H4EC1F2&"

def seg(i, e, asp):
    b0, b1, h, v9, cx, fx = e
    vert = asp == "9x16" and v9 is not None
    name, ss, sp = v9 if vert else h
    n = fb(b1) - fb(b0); src = f"{CLIPS}/cf_{name}.mp4"; need = n / FPS * sp; d = dur(src)
    if ss + need > d - 0.05: ss = max(0.0, d - 0.05 - need)
    assert ss + need <= d, (name, ss, need)
    grade = ",eq=brightness=-0.045:contrast=1.04,vignette=angle=PI/4.5" if fx == "dim" else ""
    pre = f"setpts=(PTS-STARTPTS)/{sp},fps={FPS}"
    if asp == "16x9": vf = f"{pre},scale=1964:1080:flags=lanczos,crop=1920:1080,unsharp=5:5:0.35{grade},setsar=1"
    elif vert: vf = f"{pre},scale=1080:1964:flags=lanczos,crop=1080:1920,unsharp=5:5:0.35{grade},setsar=1"    # native 704x1280
    else:
        x = min(max(round(cx * 1280 - 198), 0), 1280 - 396)
        vf = f"{pre},crop=396:704:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5{grade},setsar=1"
    out = f"{SEG}/s2_{asp}_{i:02d}.mp4"
    run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", src, "-filter_complex", vf,
         "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out])
    return out

def logo16():
    """8 beats of the AI logo film from LOGO_SS, 1920x1080, ending on the resolved mark."""
    n = fb(END_B) - fb(LOGO_B); out = f"{SEG}/s2_logo_16x9.mp4"
    if LOGO16.endswith("logo_16x9.mp4"): return LOGO16
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{LOGO_SS:.3f}", "-i", LOGO16, "-vf", f"fps={FPS},scale=1920:1080:flags=lanczos,unsharp=5:5:0.3,setsar=1",
         "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out])
    assert abs(dur(out) - n / FPS) < 0.05, ("logo film too short from", LOGO_SS)
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
    ev(0.0, T(4) - 0.04, "Big", "{\\an5\\pos(%d,%d)\\fad(0,120)}ОВА НЕ Е%sСНИМЕНО." % (cxp, cyp, " " if v else "\\N"))
    ev(T(4), T(8) - 0.04, "Big", "{\\an5\\pos(%d,%d)%s}ОВА Е {\\c%s}AI." % (cxp, cyp, punch, GOLD))
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
    lines = ["БЕЗ КАМЕРА.", "БЕЗ ЕКИПА.", f"{{\\c{GOLD}}}БЕЗ ЧЕКАЊЕ."]
    for k, txt in enumerate(lines):
        y = (cyp - 125 + k * 125) if v else (cyp - 130 + k * 130)
        ev(T(60 + k), T(64) - 0.04, "Big", "{\\an5\\pos(%d,%d)\\fs%d%s}%s" % (cxp, y, 100 if v else 96, punch, txt))
    ev(T(80), T(88) - 0.04, "Big", "{\\an5\\pos(%d,%d)%s}ВАШАТА ПРИКАЗНА\\N{\\c%s}Е СЛЕДНА." % (cxp, cyp, punch, GOLD) if v else
       "{\\an5\\pos(%d,%d)%s}ВАШАТА\\NПРИКАЗНА\\N{\\c%s}Е СЛЕДНА." % (cxp, cyp, punch, GOLD))
    p = f"{SR}/showreel2_{asp}.ass"; open(p, "w", encoding="utf-8").write("\n".join(L) + "\n"); return p

def loudnorm(src, out, I=-14.0, TP=-1.0):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={I}:TP={TP}:LRA=20:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af",
         f"loudnorm=I={I}:TP={TP}:LRA=20:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000",
         "-c:a", "pcm_s16le", out])
def audio():
    raw = f"{SEG}/s2_audio_raw.wav"; out = f"{SEG}/s2_audio.wav"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(M0), "-t", str(END_T), "-i", MUSIC, "-af",
         f"afade=t=in:st=0:d=0.012,afade=t=out:st=54.0:d=0.8,apad=whole_dur={END_T},aresample=48000", "-ac", "2", raw])
    loudnorm(raw, out); return out

def build(asp):
    v = asp == "16x9"
    segs = [seg(i, e, asp) for i, e in enumerate(EDL)]
    lst = f"{SEG}/s2_{asp}.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    a = ass(asp); wm, wx, wy = (f"{W}/png/wm_96.png", 30, 24) if v else (f"{W}/png/wm_110.png", 34, 196)
    disc = f"{W}/png/disc_top_{asp}.png"; DT = fb(8) / FPS - 0.02
    E = f"{W}/png/end_{asp}"; nl = fb(END_B) - fb(LOGO_B); X = 10
    te = (N_END + X) / FPS; logo = logo16() if v else LOGO9
    fc = (f"[0:v]ass={a}:fontsdir={FONTS}[b0];[4:v]format=rgba,colorchannelmixer=aa=0.85[wm];[b0][wm]overlay={wx}:{wy}:format=auto:shortest=1,setsar=1[bw];"
          f"[7:v]format=rgba,fade=t=out:st={DT - 0.4:.3f}:d=0.4:alpha=1[dp];[bw][dp]overlay=0:0:format=auto:eof_action=pass,setsar=1[body];"
          f"[1:v]trim=start_frame=0:end_frame={nl},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[lg];"
          f"[2:v]fps={FPS},trim=end_frame={N_END + X},setpts=PTS-STARTPTS,format=rgba[ea];"
          f"[5:v]fps={FPS},trim=end_frame={N_END + X},setpts=PTS-STARTPTS,format=rgba,fade=t=in:st=0.45:d=0.45:alpha=1[eb];"
          f"[6:v]fps={FPS},trim=end_frame={N_END + X},setpts=PTS-STARTPTS,format=rgba,fade=t=in:st=1.0:d=0.5:alpha=1[ec];"
          f"[ea][eb]overlay=x=0:y='max(0,24-24*(t-0.45)/0.45)':format=auto[e1];[e1][ec]overlay=0:0:format=auto,format=yuv420p,fade=t=out:st={te - 0.45:.3f}:d=0.45,settb=1/{FPS},setsar=1[end];"
          f"[lg][end]xfade=transition=fade:duration={X / FPS:.4f}:offset={(nl - X) / FPS:.4f}[le];"
          f"[body][le]concat=n=2:v=1:a=0,format=yuv420p[v]")
    out = f"{OUT}/bigdogma_showreel_v2_{asp}{SUFFIX}.mp4"
    run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", logo,
         "-loop", "1", "-t", "8", "-i", f"{E}_A.png", "-i", f"{SEG}/s2_audio.wav", "-loop", "1", "-t", "50", "-i", wm, "-loop", "1", "-t", "8", "-i", f"{E}_B.png", "-loop", "1", "-t", "8", "-i", f"{E}_C.png",
         "-loop", "1", "-t", f"{DT:.3f}", "-i", disc,
         "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-t", f"{END_T:.3f}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out])
    for p in segs: os.remove(p)
    print("OK", out, round(dur(out), 2), flush=True)

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    print("shots", len(EDL), "| frames body", fb(LOGO_B), "logo", fb(END_B) - fb(LOGO_B), "end", N_END)
    assert [e[0] for e in EDL[1:]] == [e[1] for e in EDL[:-1]] and EDL[-1][1] == LOGO_B, "EDL must tile the body"
    if what in ("audio", "all"): audio()
    for asp in ("16x9", "9x16"):
        if what in (asp, "all"): build(asp)
