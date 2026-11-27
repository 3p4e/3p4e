# 16:9 "how an ad is made" film for the public site (replaces explainers/howto_construction.mp4 there).
# Same steps and sources as reel_06 (launch/video/_work/reels.py howto()), rebuilt natively at 1280x720:
#   title card with the AI disclosure (first frame, so it is also the poster) -> step 1 key frame -> step 2 AI time-lapse
#   -> step 3 the finished ad: timelapse_construction from 28.70 s (finished building + closing VO, subtitled)
#   -> 3 s animated BIG DOGMA outro with the disclosure again and the kit's sonic sting.
# Output: site_work/howto/howto_16x9.mp4 (master; build_media.py extras encodes it for the web at -16 LUFS).
# Run: /usr/local/bin/python3 howto169.py
import os, re, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
WORK = f"{S}/launch/site_work"; OUTD = f"{WORK}/howto"; TMP = "/dev/shm/bd_howto"; FONTS = f"{S}/brand/fonts"
os.makedirs(OUTD, exist_ok=True); os.makedirs(TMP, exist_ok=True)
FPS = 24; Wd, Ht = 1280, 720
FILM = f"{S}/final_music/timelapse_construction.mp4"; FILM_SS = 28.70
LOGO_SEG = f"{S}/launch/video/_work/seg/logo_16x9.mp4"                 # horizontal lockup ignition (same as the showreel close)
STING = (f"{S}/music/ace_final/8_showreel.mp3", 50.04)                  # same sting as the reels' outro
DISC = "Видео изработено со вештачка интелигенција · AI-generated video"
T0, T1, T2, T3, T4 = 2.2, 3.2, 3.6, 4.6, 3.0                           # title, step 1, step 2, step 3, outro
n0, n1, n2, n3, n4 = [round(x * FPS) for x in (T0, T1, T2, T3, T4)]
o1 = n0 / FPS; o2 = (n0 + n1) / FPS; o3 = (n0 + n1 + n2) / FPS; o4 = (n0 + n1 + n2 + n3) / FPS; total = o4 + n4 / FPS

def run(a): subprocess.run(["nice", "-n", "10"] + a, check=True)
def tc(t): t = max(t, 0); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
def srt(p, shift, t_from, t_to):
    out = []
    for blk in re.split(r"\n\s*\n", open(p, encoding="utf-8-sig").read().strip()):
        L = blk.strip().split("\n"); m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)", L[1]); g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000; b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        if b <= t_from or a >= t_to: continue
        out.append((max(a, t_from) + shift, min(b, t_to) + shift, " ".join(L[2:])))
    return out

# ---------- text layer (libass): title, step kickers + captions, VO subtitle, outro disclosure
GOLD = "&H004EC1F2"
HEAD = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Title,Russo One,60,&H00FFFFFF,&H00FFFFFF,&H50000000,&H90000000,0,0,0,0,100,100,1,0,1,2,3,8,0,0,0,1\n"
        f"Style: Topic,Oswald,32,{GOLD},&H00FFFFFF,&H70000000,&H90000000,1,0,0,0,100,100,3,0,1,1.5,2,8,0,0,0,1\n"
        "Style: Disc,Oswald,27,&H00C6D1D6,&H00FFFFFF,&H80000000,&H90000000,0,0,0,0,100,100,0.6,0,1,1.2,1.5,2,0,0,0,1\n"
        "Style: Tag,Oswald,34,&H00E6EFF3,&H00FFFFFF,&H90000000,&H90000000,1,0,0,0,100,100,8,0,1,0.8,1.5,5,0,0,0,1\n"
        f"Style: Kick,Oswald,28,{GOLD},&H00FFFFFF,&H200F0D0D,&H00000000,1,0,0,0,100,100,4,0,3,9,0,7,0,0,0,1\n"
        "Style: Step,Russo One,34,&H00FFFFFF,&H00FFFFFF,&H70000000,&H90000000,0,0,0,0,100,100,0.5,0,1,2.4,2.5,7,0,0,0,1\n"
        "Style: Sub,Russo One,36,&H00FFFFFF,&H00FFFFFF,&H30000000,&H90000000,0,0,0,0,100,100,0.5,0,1,2.6,2,2,80,80,46,1\n"
        "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
ev = [f"Dialogue: 1,{tc(0)},{tc(o1 - 0.02)},Title,,0,0,0,,{{\\pos(640,318)}}Како настанува рекламата",
      f"Dialogue: 1,{tc(0)},{tc(o1 - 0.02)},Topic,,0,0,0,,{{\\pos(640,404)}}ГРАДЕЖНИШТВО · ТАЈМЛАПС",
      f"Dialogue: 1,{tc(0)},{tc(o1 - 0.02)},Disc,,0,0,0,,{{\\pos(640,640)}}{DISC}",
      f"Dialogue: 1,{tc(o4 + 0.6)},{tc(total)},Disc,,0,0,0,,{{\\pos(640,696)\\fad(400,0)}}{DISC}",
      f"Dialogue: 1,{tc(o4 + 1.0)},{tc(total)},Tag,,0,0,0,,{{\\pos(640,548)\\fad(450,0)\\c&H4EC1F2&}}—  {{\\c&HE6EFF3&}}BREAK THE DOGMA.{{\\c&H4EC1F2&}}  —"]
steps = [("КОРАК 1", "Ваш рендер или фотографија од плацот", o1, o2), ("КОРАК 2", "AI тајмлапс по фази", o2, o3),
         ("КОРАК 3", "Готова реклама: глас, музика, 16:9 и 9:16", o3, o4)]
for kick, txt, a, b in steps:
    ev.append(f"Dialogue: 1,{tc(a + 0.08)},{tc(b - 0.06)},Kick,,0,0,0,,{{\\pos(48,36)\\fad(150,120)}}{kick}")
    ev.append(f"Dialogue: 1,{tc(a + 0.12)},{tc(b - 0.06)},Step,,0,0,0,,{{\\fad(180,120)\\move(48,98,48,86,0,260)}}{txt}")
for a, b, t in srt(f"{S}/subs/srt/timelapse_construction.mk.srt", o3 - FILM_SS, FILM_SS, FILM_SS + T3):
    ev.append(f"Dialogue: 0,{tc(a)},{tc(b)},Sub,,0,0,0,,{{\\fad(120,120)}}{t}")
ASS = f"{TMP}/howto169.ass"; open(ASS, "w", encoding="utf-8").write(HEAD + "\n".join(ev) + "\n")

# ---------- audio: construction music under title + steps 1-2, the film's own audio (VO) under step 3, sting on the outro
aud = f"{TMP}/howto169_mix.wav"
st_ms = int(round(o4 * 1000)); f_ms = int(round(o3 * 1000))
run(["ffmpeg", "-v", "error", "-y", "-i", f"{S}/music/ace_final/3_construction.mp3", "-ss", str(FILM_SS), "-t", str(T3 + 0.2), "-i", FILM,
     "-ss", str(STING[1]), "-i", STING[0], "-filter_complex",
     f"[0:a]atrim=0:{o3 + 0.8:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume=0.5,afade=t=in:st=0:d=0.4,afade=t=out:st={o3 - 0.4:.3f}:d=1.2[m];"
     f"[1:a]atrim=0:{T3:.3f},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:st=0:d=0.35,afade=t=out:st={T3 - 0.5:.3f}:d=0.5,adelay={f_ms}|{f_ms}[f];"
     f"[2:a]atrim=0:2.95,asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:st=0:d=0.015,afade=t=out:st=1.9:d=1.0,volume=0.85,adelay={st_ms}|{st_ms}[st];"
     f"[m][f][st]amix=inputs=3:duration=longest:normalize=0,apad=whole_dur={total:.4f},atrim=0:{total:.4f}[a]",
     "-map", "[a]", "-ac", "2", "-c:a", "pcm_s16le", aud])

# ---------- picture
out = f"{OUTD}/howto_16x9.mp4"
fit = f"scale={Wd}:{Ht}:force_original_aspect_ratio=increase,crop={Wd}:{Ht}"
fc = (f"[0:v]fps={FPS},trim=end_frame={n0},setpts=PTS-STARTPTS,{fit},boxblur=14:2,eq=brightness=-0.24:saturation=0.8[tbg];"
      f"[1:v]scale=520:-2[lg];[tbg][lg]overlay=(W-w)/2:132,setsar=1,format=yuv420p,settb=1/{FPS}[p0];"
      f"[2:v]{fit},zoompan=z='1+0.0009*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={Wd}x{Ht}:fps={FPS},trim=end_frame={n1},setpts=PTS-STARTPTS,setsar=1,format=yuv420p,settb=1/{FPS}[p1];"
      f"[3:v]fps={FPS},trim=end_frame={n2},setpts=PTS-STARTPTS,{fit},setsar=1,format=yuv420p,settb=1/{FPS}[p2];"
      f"[4:v]fps={FPS},trim=end_frame={n3},setpts=PTS-STARTPTS,{fit},setsar=1,format=yuv420p,settb=1/{FPS}[p3];"
      f"[5:v]fps={FPS},trim=end_frame={n4},setpts=PTS-STARTPTS,scale={Wd}:{Ht}:flags=lanczos,fade=t=in:st=0:d=0.2,fade=t=out:st={T4 - 0.35:.3f}:d=0.35,setsar=1,format=yuv420p,settb=1/{FPS}[p4];"
      f"[p0][p1][p2][p3][p4]concat=n=5:v=1:a=0,ass={ASS}:fontsdir={FONTS},format=yuv420p[v]")
run(["ffmpeg", "-v", "error", "-y",
     "-ss", "1.0", "-i", f"{S}/ltx25/tl_06_handover.mp4",                              # 0 title background (finished building, blurred)
     "-i", f"{S}/brand/logo.png",                                                     # 1 lockup on the title
     "-loop", "1", "-framerate", str(FPS), "-t", "4", "-i", f"{S}/construction/kf/con_01_excavation_start.png",  # 2 step 1 key frame
     "-ss", "1.0", "-i", f"{S}/ltx25/tl_03_frame.mp4",                                 # 3 step 2 AI time-lapse
     "-ss", str(FILM_SS), "-i", FILM,                                                  # 4 step 3 finished ad (16:9 master)
     "-i", LOGO_SEG,                                                                   # 5 outro
     "-i", aud,                                                                        # 6 audio
     "-filter_complex", fc, "-map", "[v]", "-map", "6:a", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
     "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out])
print("OK", out, f"{total:.2f} s; step 3 at {o3:.2f} s, outro at {o4:.2f} s", flush=True)
