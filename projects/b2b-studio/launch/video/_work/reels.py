# Six vertical Reels (1080x1920) from public-safe films: burned-in Macedonian subtitles, gold monogram
# watermark top-left, 2.8 s animated BIG DOGMA outro with a sonic sting cut from 8_showreel.mp3, -14 LUFS.
# Reels 01-05: the film master is cut where its baked-in (DejaVu, 16:9-in-9:16) end card starts and a native 1080x1920
# end card (png/reelend_<topic>_A/B/C.png) runs for the same length over the film's own audio; an AI-disclosure pill sits
# in the top band for the first 3.8 s and the outro carries the disclosure too.
# Picture fixes on top of the masters (audio, subtitles and timing stay exactly as in the master):
#  reel_01: frames 0-111 (0-4.67 s) of timelapse_construction morph (an excavator melts into a blob at 0.3 s, trucks fuse into
#   a heap at 1.3 s and again at 4.0-4.4 s, mid-frame). They are replaced by two clean master frames (frame 0 = the bare plot
#   under VO line 1, frame 112 = the dug pit) with one continuous slow pull-back (zoom 1.08 -> 1.00) that lands exactly on
#   frame 112, where the time-lapse starts playing.
#  reel_04: the wire-harness hall (master frames 113-234, 4.7-9.8 s) shows an East Asian workforce under 'Направено во
#   Македонија'. It is replaced by ltx610/x_auto_x2 (inspector at the harness racks), 121 -> 140 frames (its slow first 3 s
#   stretched with frame blending), dissolving in from the exterior and out into the crimping close-up.
# usage: python3 reels.py [all|01|02|...|06]
import os, sys, json, re, subprocess
import numpy as np
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
W = f"{S}/launch/video/_work"; OUT = f"{S}/launch/video"; SEG = f"{W}/seg"; FONTS = f"{S}/brand/fonts"
FPS = 24; OUTRO_F = 67                                   # 2.79 s of seg/outro_9x16.mp4 (still lockup fading in, outro_still.py)
STING = (f"{S}/music/ace_final/8_showreel.mp3", 50.04)   # same hit the showreel logo lands on
WM = f"{W}/png/wm_110.png"; WMX, WMY = 34, 196
DISC_TOP = f"{W}/png/disc_top_9x16.png"; DISC_T = 3.8     # top-band disclosure on the reel body: 0 .. 3.8 s (fades out over the last 0.4 s)
OUTRO_DISC = f"{W}/png/outro_disc_9x16.png"
REELS = [("01", "construction", "timelapse_construction"), ("02", "real_estate", "sector_real_estate"), ("03", "food", "sector_food"),
         ("04", "automotive", "sector_automotive"), ("05", "interior_design", "timelapse_interior_design")]
# reel 05 was timelapse_renovation until the review: its VO lines landed on "before" shots and an unconvincing kitchen

def card_cut(src):
    # frame index where the master's dissolve into its own end card begins (the card's text is already in that dissolve,
    # so the body must stop before it). Found in the last 9 s of the picture band (y 660..1260): first frame that is mostly
    # card background (k25), then walk back while the band mean keeps falling (the 0.35 s dissolve); 1 frame safety margin.
    d = dur(src, "stream"); t0 = d - 9.0
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", src, "-vf", "crop=1080:600:0:660,scale=270:150,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 150, 270).astype(np.int16)
    card = (np.abs(a - 13) < 6).mean(axis=(1, 2))                 # share of pixels at the card background (#0d0d0f)
    m = a.mean(axis=(1, 2)); k = int(np.argmax(card > 0.25))
    while k > 0 and m[k - 1] - m[k] > 3.0: k -= 1
    return round(t0 * FPS) + k - 1
def run(a, **k): subprocess.run(a, check=True, **k)
def dur(f, s="format"):
    return float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", f"{s}=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip().split("\n")[0])
def tc(t):
    t = max(t, 0); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
def srt(p, shift=0.0, t_from=None, t_to=None):
    out = []
    for blk in re.split(r"\n\s*\n", open(p, encoding="utf-8-sig").read().strip()):
        L = blk.strip().split("\n"); m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)", L[1])
        g = [int(x) for x in m.groups()]; a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000; b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        if t_from is not None and (b <= t_from or a >= t_to): continue
        if t_from is not None: a, b = max(a, t_from), min(b, t_to)
        out.append((a + shift, b + shift, " ".join(L[2:])))      # let libass balance the wrap
    return out
HEAD = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        # subtitles: top-anchored (an8) at y=1282, right under the picture band of the masters (y 656-1264); a two-line event
        # ends near y 1420, above TikTok's bottom ad zone (~1436). 170 px side margins: text column x 170..910, clear of the right rail
        "Style: Sub,Russo One,54,&H00FFFFFF,&H00FFFFFF,&H30000000,&H90000000,0,0,0,0,100,100,1,0,1,3.5,2,8,170,170,1282,1\n"
        # reel_06 step kicker: gold on an opaque dark box (BorderStyle 3), readable on bright skies
        "Style: Kick,Oswald,44,&H004EC1F2,&H00FFFFFF,&H200F0D0D,&H00000000,1,0,0,0,100,100,5,0,3,13,0,2,0,0,0,1\n"
        "Style: Step,Russo One,52,&H00FFFFFF,&H00FFFFFF,&H70000000,&H90000000,0,0,0,0,100,100,1,0,1,3,3,2,0,0,0,1\n"
        "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
def write_ass(p, subs, extra=()):
    with open(p, "w", encoding="utf-8") as f:
        f.write(HEAD)
        for a, b, t in subs: f.write(f"Dialogue: 0,{tc(a)},{tc(b)},Sub,,0,0,0,,{{\\fad(120,120)}}{t}\n")
        for line in extra: f.write(line + "\n")

def measure(src):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
def loudnorm(src, out, I=-14.0):
    # gain to target, brick-wall limiter at -1.9 dBFS (headroom for AAC overs), then one corrective pass
    lim = "alimiter=limit=0.80:attack=3:release=60:level=disabled:asc=1"
    g = I - measure(src); tmp = out + ".tmp.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"volume={g:.2f}dB,{lim}", "-c:a", "pcm_s16le", tmp])
    g += I - measure(tmp)
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"volume={g:.2f}dB,{lim},aresample=48000", "-c:a", "pcm_s16le", out]); os.remove(tmp)

def sting_filter(idx, at):
    # 2.8 s sting starting on the music hit, delayed to the outro start
    ms = int(round(at * 1000))
    return f"[{idx}:a]atrim=0:2.85,asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:st=0:d=0.015,afade=t=out:st=1.85:d=0.95,volume=0.85,adelay={ms}|{ms}[st]"

def outro_chain(idx, disc=None):
    f = f"[{idx}:v]trim=start_frame=0:end_frame={OUTRO_F},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p,setsar=1"
    if disc: f += f"[oa];[{disc}:v]format=rgba,fade=t=in:st=0.6:d=0.5:alpha=1[od];[oa][od]overlay=0:0:format=auto:shortest=1,format=yuv420p"
    return f + f",fade=t=in:st=0:d=0.18,fade=t=out:st={OUTRO_F / FPS - 0.3:.3f}:d=0.3[out]"

def cover(inp, out, n=None):
    # 16:9 clip -> 9:16 frame laid out like the masters: 1080x608 picture band at y 656 (fill-scaled to 1105x608, centre crop)
    # over a blurred, slightly darkened cover of the same picture
    t = f",trim=end_frame={n}" if n else ""
    return (f"[{inp}]fps={FPS}{t},setpts=PTS-STARTPTS,scale=1105:608:flags=lanczos,crop=1080:608,setsar=1,split[{out}f][{out}g];"
            f"[{out}g]scale=-2:1920,crop=1080:1920,boxblur=32:2,eq=brightness=-0.16:saturation=0.8[{out}b];"
            f"[{out}b][{out}f]overlay=0:656,format=yuv420p,setsar=1,settb=1/{FPS}")

def still(inp, frame, n, k0, kr, z0, out):
    # one master frame held for n frames; the background stays put, the picture band pulls back from z0 to 1.0 at frame kr
    # (eased: z = 1 + (z0-1)(1-k/kr)^2, k = k0 + output frame), supersampled 4x so the move is smooth
    z = f"1+{z0 - 1:.4f}*pow(1-(on+{k0})/{kr},2)"
    return (f"[{inp}]trim=start_frame={frame}:end_frame={frame + 1},setpts=PTS-STARTPTS,format=yuv420p,setsar=1,split[{out}a][{out}b];"
            f"[{out}a]loop=loop={n - 1}:size=1,setpts=N/{FPS}/TB[{out}bg];"
            f"[{out}b]crop=1080:608:0:656,scale=4320:2432:flags=lanczos,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s=1080x608:fps={FPS}[{out}z];"
            f"[{out}bg][{out}z]overlay=0:656,format=yuv420p,setsar=1,settb=1/{FPS}[{out}]")

def picture(num, src):
    # -> (extra ffmpeg inputs, which start at index 9; filter that leaves the reel's picture in [pv]); None = master as is
    if num == "01":
        KR, XS, XD, Z0 = 112, 82, 12, 1.08      # film plays from frame 112; dissolve frame 0 -> frame 112 at 3.42-3.92 s
        fc = (still("9:v", 0, XS + XD, 0, KR, Z0, "sa") + ";" + still("10:v", KR, KR - XS, XS, KR, Z0, "sb") + ";"
              f"[sa][sb]xfade=transition=fade:duration={XD / FPS:.4f}:offset={XS / FPS:.4f},settb=1/{FPS}[sab];"
              f"[0:v]trim=start_frame={KR},setpts=PTS-STARTPTS,format=yuv420p,setsar=1,settb=1/{FPS}[sc];[sab][sc]concat=n=2:v=1:a=0[pv]")
        return ["-i", src, "-i", src], fc
    if num == "04":
        A, B, X = 113, 235, 9                   # keep master frames 0-112 (exterior) and 235- (crimping); 9-frame dissolves
        n = B + X - (A - X)                     # 140 frames of insert
        fc = (f"[0:v]split[m1][m2];[m1]trim=end_frame={A},setpts=PTS-STARTPTS,format=yuv420p,setsar=1,settb=1/{FPS}[ma];"
              f"[m2]trim=start_frame={B},setpts=PTS-STARTPTS,format=yuv420p,setsar=1,settb=1/{FPS}[mb];"
              # x_auto_x2 has 121 frames: its slow first 3 s (frames 0-71: inspector reading her tablet) are stretched to
              # 91 frames with frame blending, the faster rest (she reaches for the harness, camera pans) plays at 1x
              f"[9:v]split[xa][xb];[xa]trim=end_frame=72,setpts=(PTS-STARTPTS)*{n - 49}/72,framerate=fps={FPS},"
              f"tpad=stop_mode=clone:stop_duration=0.5,trim=end_frame={n - 49},setpts=PTS-STARTPTS,settb=1/{FPS}[xa2];"
              f"[xb]trim=start_frame=72,setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS}[xb2];[xa2][xb2]concat=n=2:v=1:a=0[ins0];"
              + cover("ins0", "ins", n) + "[ins];"
              f"[ma][ins]xfade=transition=fade:duration={X / FPS:.4f}:offset={(A - X) / FPS:.4f},settb=1/{FPS}[mi];"
              f"[mi][mb]xfade=transition=fade:duration={X / FPS:.4f}:offset={B / FPS:.4f},settb=1/{FPS}[pv]")
        return ["-i", f"{S}/ltx610/x_auto_x2.mp4"], fc
    return None

def reel(num, topic, film):
    src = f"{S}/final_music_9x16/{film}_9x16.mp4"; d = dur(src, "stream"); nf = round(d * FPS)
    a = f"{W}/reel_{num}.ass"; write_ass(a, srt(f"{S}/subs/srt/{film}.mk.srt"))
    aud = f"{SEG}/reel_{num}_mix.wav"; audn = f"{SEG}/reel_{num}_norm.wav"; total = (nf + OUTRO_F) / FPS
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", str(STING[1]), "-i", STING[0], "-filter_complex",
         f"[0:a]atrim=0:{nf / FPS:.4f},asetpts=PTS-STARTPTS,aresample=48000,afade=t=out:st={nf / FPS - 0.25:.3f}:d=0.25[f];{sting_filter(1, nf / FPS)};"
         f"[f][st]amix=inputs=2:duration=longest:normalize=0,apad=whole_dur={total:.4f},atrim=0:{total:.4f}[a]", "-map", "[a]", "-ac", "2", aud])
    loudnorm(aud, audn)
    out = f"{OUT}/reel_{num}_{topic}.mp4"
    # body = frames [0, nc) of the master; the native card (ne frames) dissolves in over the body's last X frames, so the
    # picture length (nf) and the film audio under it stay exactly as in the master
    X = 9; nc = card_cut(src); ne = nf - nc + X; te = ne / FPS; E = f"{W}/png/reelend_{topic}"
    print(f"reel_{num}: film card cut at {nc / FPS:.3f} s, native end card {te:.2f} s", flush=True)
    pic = picture(num, src); pin, pfc = pic if pic else ([], "")
    fc = (pfc + (";" if pfc else "") +
          f"[{'pv' if pic else '0:v'}]trim=end_frame={nc},setpts=PTS-STARTPTS,ass={a}:fontsdir={FONTS}[s];[1:v]format=rgba,colorchannelmixer=aa=0.85[wm];"
          f"[s][wm]overlay={WMX}:{WMY}:format=auto:shortest=1[s2];"
          f"[4:v]format=rgba,fade=t=out:st={DISC_T - 0.4:.2f}:d=0.4:alpha=1[dt];[s2][dt]overlay=0:0:format=auto:eof_action=pass,"
          f"format=yuv420p,setsar=1,settb=1/{FPS}[main];"
          f"[5:v]fps={FPS},trim=end_frame={ne},setpts=PTS-STARTPTS,format=rgba[ea];"
          f"[6:v]fps={FPS},trim=end_frame={ne},setpts=PTS-STARTPTS,format=rgba,fade=t=in:st=0.5:d=0.45:alpha=1[eb];"
          f"[7:v]fps={FPS},trim=end_frame={ne},setpts=PTS-STARTPTS,format=rgba,fade=t=in:st=1.1:d=0.5:alpha=1[ec];"
          f"[ea][eb]overlay=x=0:y='max(0,22-22*(t-0.5)/0.45)':format=auto[e1];[e1][ec]overlay=0:0:format=auto,format=yuv420p,"
          f"fade=t=out:st={te - 0.25:.3f}:d=0.25,setsar=1,settb=1/{FPS}[end];"
          f"[main][end]xfade=transition=fade:duration={X / FPS:.4f}:offset={(nc - X) / FPS:.4f},settb=1/{FPS}[me];"
          f"{outro_chain(2, disc=8)};[out]settb=1/{FPS}[o2];[me][o2]concat=n=2:v=1:a=0[v]")
    run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-t", str(d + 1), "-i", WM, "-i", f"{SEG}/outro_9x16.mp4", "-i", audn,
         "-loop", "1", "-t", f"{DISC_T}", "-i", DISC_TOP,                                    # 4 disclosure pill (top band)
         "-loop", "1", "-t", f"{te + 1:.2f}", "-i", f"{E}_A.png", "-loop", "1", "-t", f"{te + 1:.2f}", "-i", f"{E}_B.png",
         "-loop", "1", "-t", f"{te + 1:.2f}", "-i", f"{E}_C.png",                           # 5-7 native end card layers
         "-loop", "1", "-t", "4", "-i", OUTRO_DISC,                                          # 8 disclosure on the outro
         *pin,                                                                               # 9- picture fixes (see picture())
         "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out])
    print("OK", out, round(dur(out), 2), flush=True)

def band(idx, label, n, push=False):
    # 16:9 picture in a 1080 px wide band centred on y=960, blurred cover background (same look as the 9:16 masters)
    z = (f",zoompan=z='1+0.0009*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x704:fps={FPS}" if push else "")
    return (f"[{idx}:v]fps={FPS}{z},trim=end_frame={n},setpts=PTS-STARTPTS,split[{label}a][{label}b];"
            f"[{label}a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.2:saturation=0.85[{label}bg];"
            f"[{label}b]scale=1080:594:flags=lanczos[{label}fg];[{label}bg][{label}fg]overlay=0:663,setsar=1,format=yuv420p,settb=1/{FPS}[{label}]")

def howto():
    # natively vertical rebuild of explainers/howto_construction.mp4 (same steps and sources, VO line kept whole)
    T1, T2, T3, T4 = 2.0, 3.2, 3.6, 4.6; n1, n2, n3, n4 = [round(x * FPS) for x in (T1, T2, T3, T4)]
    o2, o3, o4 = n1 / FPS, (n1 + n2) / FPS, (n1 + n2 + n3) / FPS; o5 = (n1 + n2 + n3 + n4) / FPS
    # step 3 = the finished building and the closing VO "Од празен плац до вашите клучеви." (SRT 28.843-31.785), ends before the film's card (~34 s)
    FILM_SS = 28.70; film = f"{S}/final_music_9x16/timelapse_construction_9x16.mp4"
    steps = [("КОРАК 1", "Ваш рендер или\\Nфотографија од плацот", o2, o3), ("КОРАК 2", "AI тајмлапс\\Nпо фази", o3, o4),
             ("КОРАК 3", "Готова реклама: глас,\\Nмузика, 16:9 и 9:16", o4, o5)]
    extra = []
    for k, (kick, txt, a, b) in enumerate(steps):
        extra.append(f"Dialogue: 1,{tc(a + 0.08)},{tc(b - 0.06)},Kick,,0,0,0,,{{\\an2\\pos(540,462)\\fad(150,120)}}{kick}")
        extra.append(f"Dialogue: 1,{tc(a + 0.12)},{tc(b - 0.06)},Step,,0,0,0,,{{\\an2\\pos(540,628)\\fad(180,120)\\move(540,652,540,628,0,260)}}{txt}")
    subs = srt(f"{S}/subs/srt/timelapse_construction.mk.srt", shift=o4 - FILM_SS, t_from=FILM_SS, t_to=FILM_SS + T4)
    a = f"{W}/reel_06.ass"; write_ass(a, subs, extra)
    total = o5 + OUTRO_F / FPS
    aud = f"{SEG}/reel_06_mix.wav"; audn = f"{SEG}/reel_06_norm.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{S}/music/ace_final/3_construction.mp3", "-ss", str(FILM_SS), "-t", str(T4 + 0.2), "-i", film,
         "-ss", str(STING[1]), "-i", STING[0], "-filter_complex",
         f"[0:a]atrim=0:{o4 + 0.8:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume=0.5,afade=t=in:st=0:d=0.6,afade=t=out:st={o4 - 0.4:.3f}:d=1.2[m];"
         f"[1:a]atrim=0:{T4:.3f},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:st=0:d=0.35,afade=t=out:st={T4 - 0.5:.3f}:d=0.5,adelay={int(o4 * 1000)}|{int(o4 * 1000)}[f];"
         f"{sting_filter(2, o5)};[m][f][st]amix=inputs=3:duration=longest:normalize=0,apad=whole_dur={total:.4f},atrim=0:{total:.4f}[a]",
         "-map", "[a]", "-ac", "2", aud])
    loudnorm(aud, audn)
    out = f"{OUT}/reel_06_howto_construction.mp4"
    fc = (f"[0:v]fps={FPS},trim=end_frame={n1},setpts=PTS-STARTPTS,scale=-2:1920,crop=1080:1920,boxblur=18:2,eq=brightness=-0.22:saturation=0.8[tbg];"
          f"[1:v]format=rgba[tt];[tbg][tt]overlay=0:0:format=auto:shortest=1,setsar=1,format=yuv420p,settb=1/{FPS}[p1];"
          + band(2, "p2", n2, push=True) + ";" + band(3, "p3", n3) + ";"
          f"[4:v]fps={FPS},trim=end_frame={n4},setpts=PTS-STARTPTS,setsar=1,format=yuv420p,settb=1/{FPS}[p4];"
          f"[p1][p2][p3][p4]concat=n=4:v=1:a=0,ass={a}:fontsdir={FONTS}[c];[5:v]format=rgba,colorchannelmixer=aa=0.85[wm];"
          f"[c][wm]overlay={WMX}:{WMY}:format=auto:shortest=1,format=yuv420p,settb=1/{FPS}[main];"
          + outro_chain(6, disc=8) + f";[out]settb=1/{FPS}[o2];[main][o2]concat=n=2:v=1:a=0[v]")
    run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y",
         "-ss", "1.0", "-i", f"{S}/ltx25/tl_06_handover.mp4",                         # 0 title background
         "-loop", "1", "-t", "3", "-i", f"{W}/png/howto_title_9x16_t.png",             # 1 title text layer
         "-loop", "1", "-t", "4", "-i", f"{S}/construction/kf/con_01_excavation_start.png",  # 2 step 1 still
         "-ss", "1.0", "-i", f"{S}/ltx25/tl_03_frame.mp4",                             # 3 step 2 clip
         "-ss", str(FILM_SS), "-i", film,                                              # 4 step 3 finished ad (9:16 master)
         "-loop", "1", "-t", "20", "-i", WM,                                           # 5 watermark
         "-i", f"{SEG}/outro_9x16.mp4",                                                 # 6 outro
         "-i", audn,                                                                   # 7 audio
         "-loop", "1", "-t", "4", "-i", f"{W}/png/outro_disc_9x16.png",                # 8 disclosure on outro
         "-filter_complex", fc, "-map", "[v]", "-map", "7:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out])
    print("OK", out, round(dur(out), 2), flush=True)

if __name__ == "__main__":
    w = sys.argv[1] if len(sys.argv) > 1 else "all"
    for num, topic, film in REELS:
        if w in ("all", num): reel(num, topic, film)
    if w in ("all", "06"): howto()
