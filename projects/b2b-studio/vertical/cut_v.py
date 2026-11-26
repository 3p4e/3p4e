# Native 9:16 edit of a pitch film (owner, 2026-11-26). The picture is rebuilt at 1080x1920 from the vertical LTX shots on exactly the
# timeline of the 16:9 film (same shot lengths, crossfades, end card, BD intro and contact outro, all laid out for a phone), and the 16:9
# pitch film's finished soundtrack (voice-over + music, already mixed) is laid under it unchanged.
#   python3 cut_v.py foton_tunland_v9_specs | foton_showreel_v2
import os, sys, json, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; V = f"{S}/vertical"; TMP = f"{V}/tmp"; os.makedirs(TMP, exist_ok=True)
VCLIPS = os.environ.get("VCLIPS", f"{V}/clips"); TR = f"{S}/vo/trim"; W, H = 1080, 1920
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RUSSO = f"{S}/brand/fonts/RussoOne-400.ttf"; LOGO = "/home/user/3p4e/projects/b2b-studio/outreach/email/assets/bd_logo_header.png"   # BIG / DOGMA lockup
B = json.load(open(f"{S}/brand/brand.json"))
DIS = {"mk": ("Концепт изработен само за презентација на {c}.", "Не е објавен и нема да биде објавен", "без нивно изречно писмено одобрение.", "Видео изработено со вештачка интелигенција (LTX-2.5)")}
WM = {"mk": "КОНЦЕПТ · НЕ Е ЗА ОБЈАВА"}; TAG = {"mk": B["tagline_mk"]}; CALL = {"mk": "Закажете 15 минути:"}
def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
ENC = ["-an", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", "24"]

def seg(clip, d, out, caption=None):   # vertical shot, held on its last frame if the line is longer; caption in the phone-safe zone
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps=24"
    pad = max(0, d - dur(clip))
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.2f}"
    if caption:   # Reels/TikTok cover the bottom ~22 % and a strip on the right: the caption sits above that, centred
        vf += (f",drawbox=x=0:y={int(H*.60)}:w=iw:h=150:color=black@0.5:t=fill,"
               f"drawtext=fontfile={DJB}:text='{esc(caption)}':fontsize=50:fontcolor=white:x=(w-tw)/2:y={int(H*.60)+48}:alpha='min(1,max(0,(t-0.3)/0.4))'")
    run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", vf, "-t", f"{d:.3f}"] + ENC + [out])

def card(out, lang, company, title, tagline, d=5.0):
    l1, l2, l3, ai = DIS[lang]; l1 = l1.format(c=company); y0 = int(H * .30)
    vf = [f"drawtext=fontfile={DJB}:text='{esc(title)}':fontsize=84:fontcolor=white:x=(w-tw)/2:y={y0}",
          f"drawtext=fontfile={DJ}:text='{esc(tagline)}':fontsize=52:fontcolor=0xf2c14e:x=(w-tw)/2:y={y0+150}",
          f"drawtext=fontfile={DJ}:text='{esc(l1)}':fontsize=28:fontcolor=0xbbbbbb:x=(w-tw)/2:y={int(H*.62)}",
          f"drawtext=fontfile={DJ}:text='{esc(l2)}':fontsize=28:fontcolor=0xbbbbbb:x=(w-tw)/2:y={int(H*.62)+44}",
          f"drawtext=fontfile={DJ}:text='{esc(l3)}':fontsize=28:fontcolor=0xbbbbbb:x=(w-tw)/2:y={int(H*.62)+88}",
          f"drawtext=fontfile={DJ}:text='{esc(ai)}':fontsize=24:fontcolor=0x888888:x=(w-tw)/2:y={int(H*.62)+150}", "fade=t=in:st=0:d=0.5"]
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0d0d0f:s={W}x{H}:r=24:d={d}", "-vf", ",".join(vf), "-t", str(d)] + ENC + [out])

def join(parts, out, xf):
    ds = [dur(p) for p in parts]; a = ["ffmpeg", "-v", "error", "-y"]
    for p in parts: a += ["-i", p]
    v = "[0:v]"; off = 0; fc = []
    for i in range(1, len(parts)):
        off += ds[i - 1] - xf; fc.append(f"{v}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.3f}[v{i}]"); v = f"[v{i}]"
    run(a + ["-filter_complex", ";".join(fc), "-map", v] + ENC + [out])

def intro(out, d=2.2):   # BD lockup fades in, a light sweep crosses, fade out
    fc = (f"[1:v]scale=760:-1,format=rgba,fade=t=in:st=0.15:d=0.6:alpha=1[l];[0:v][l]overlay=(W-w)/2:(H-h)/2-40,"
          f"drawbox=x='-300+t*800':y=0:w=120:h=ih:color=white@0.06:t=fill,fade=t=out:st={d-0.35}:d=0.35[v]")
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0d0d0f:s={W}x{H}:r=24:d={d}", "-loop", "1", "-t", str(d), "-i", LOGO,
         "-filter_complex", fc, "-map", "[v]", "-t", str(d)] + ENC + [out])

def outro(out, lang, d=3.2):
    y = int(H * .52)
    lines = [f"drawtext=fontfile={RUSSO}:text='{esc(TAG[lang])}':fontsize=46:fontcolor=white:x=(w-tw)/2:y={y}",
             f"drawtext=fontfile={RUSSO}:text='{esc(CALL[lang])}':fontsize=34:fontcolor=0xbbbbbb:x=(w-tw)/2:y={y+100}",
             f"drawtext=fontfile={RUSSO}:text='{esc(B['email'])}':fontsize=40:fontcolor=0xf2c14e:x=(w-tw)/2:y={y+160}",
             f"drawtext=fontfile={RUSSO}:text='bigdogma.tech':fontsize=32:fontcolor=0x999999:x=(w-tw)/2:y={y+230}"]
    fc = f"[1:v]scale=620:-1[l];[0:v][l]overlay=(W-w)/2:{int(H*.26)}," + ",".join(lines) + ",fade=t=in:st=0:d=0.4[v]"
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0d0d0f:s={W}x{H}:r=24:d={d}", "-loop", "1", "-t", str(d), "-i", LOGO,
         "-filter_complex", fc, "-map", "[v]", "-t", str(d)] + ENC + [out])

def body_wm(src, out, lang):   # same "concept" mark as the 16:9 pitch film, top right below the phone's status area
    vf = f"drawtext=fontfile={RUSSO}:text='{esc(WM[lang])}':fontsize=26:fontcolor=white@0.55:x=w-tw-36:y=150:box=1:boxcolor=black@0.25:boxborderw=10"
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf] + ENC + [out])

def first_existing(*ps):
    for p in ps:
        if os.path.exists(p): return p
    raise FileNotFoundError(ps[0])

def build(name):
    parts = []
    if name == "foton_tunland_v9_specs":
        caps = ["TUNLAND V9", "2.0 L турбо дизел + 48V хибрид", "129 kW · 450 + 50 Nm · 8-AT", "4×4 · електрична блокада", "14,6\" екран · кожни седишта", "€42.900 без ДДВ · 5 год. гаранција"]
        for i in range(1, 7):   # 16:9 rule (cut.py seg): d = max(clip, line + 0.9), from the 16:9 clip so the soundtrack lines up
            d = max(dur(f"{S}/ltx610/fs{i}.mp4"), dur(f"{TR}/foton_specs_{i}.wav") + 0.9)
            p = f"{TMP}/{name}_{i}.mp4"; seg(f"{VCLIPS}/v_fs{i}.mp4", d, p, caps[i - 1]); parts.append(p)
        title, tagline, xf = "FOTON · TUNLAND V9", "Закажи тест возење.", 0.4
    else:
        sys.path.insert(0, f"{S}/vo"); from batch2 import CUTS
        c = [c for c in CUTS if c[0] == name][0]; shots, trim = c[6], (c[8] if len(c) > 8 else None); li = 0
        for i, (cid, line) in enumerate(shots):   # 16:9 rule (cut2.py seg2)
            vo = None
            if line: li += 1; vo = f"{TR}/b2_{name}_{li}.wav"
            src16 = first_existing(f"{S}/ltx610/{cid}.mp4", f"{S}/ltx25/{cid}.mp4"); vd = dur(vo) if vo else 0
            d = max(dur(src16), vd + 0.9)
            if trim: d = max(trim, vd + 0.9) if vo else trim
            p = f"{TMP}/{name}_{i}.mp4"; seg(f"{VCLIPS}/v_{cid}.mp4", d, p); parts.append(p)
        title, tagline, xf = c[4], c[5], 0.35
    cp = f"{TMP}/{name}_card.mp4"; card(cp, "mk", "Foton Македонија", title, tagline); parts.append(cp)
    j = f"{TMP}/{name}_join.mp4"; join(parts, j, xf); b = f"{TMP}/{name}_body.mp4"; body_wm(j, b, "mk")
    intro(f"{TMP}/intro.mp4"); outro(f"{TMP}/outro_mk.mp4", "mk")
    lst = f"{TMP}/{name}_list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in (f"{TMP}/intro.mp4", b, f"{TMP}/outro_mk.mp4")))
    pic = f"{TMP}/{name}_pic.mp4"; run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic])
    master = f"{S}/pitch/{name}_pitch.mp4"; out = f"{V}/{name}_9x16_native.mp4"
    # hold the last frame a few frames so the soundtrack (the master's audio) is never cut
    run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", master, "-filter_complex", "[0:v]tpad=stop_mode=clone:stop_duration=0.3[v]", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", "-movflags", "+faststart", out])
    print(name, "picture", round(dur(pic), 2), "s | 16:9 master", round(dur(master), 2), "s | out", round(dur(out), 2), "s")

if __name__ == "__main__": build(sys.argv[1])
