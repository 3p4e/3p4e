# Cuts 5/6-shot commercials: clip + local-language VO per shot, end card (logo/name, tagline, disclaimer, AI label).
import subprocess, os, sys, json
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
sys.path.insert(0, f"{S}/vo"); os.chdir(f"{S}/vo")
from vo_lines import VO
from vo_extra import VO as VX
os.chdir(f"{S}/cut")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CLIPS = f"{S}/ltx610"; TR = f"{S}/vo/trim"; OUT = f"{S}/final_commercials"; os.makedirs(OUT, exist_ok=True); os.makedirs("tmp", exist_ok=True)
DIS = {"mk": ("Концепт изработен само за презентација на {c}.", "Не е објавен и нема да биде објавен без нивно изречно писмено одобрение.", "Видео изработено со вештачка интелигенција (LTX-2.5)"),
       "sr": ("Koncept izrađen samo za prezentaciju kompaniji {c}.", "Nije objavljen i neće biti objavljen bez njihovog izričitog pisanog odobrenja.", "Video je napravljen uz pomoć veštačke inteligencije (LTX-2.5)"),
       "sq": ("Koncept i përgatitur vetëm për prezantim te {c}.", "Nuk është publikuar dhe nuk do të publikohet pa miratimin e tyre të shprehur me shkrim.", "Video e krijuar me inteligjencë artificiale (LTX-2.5)")}
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
def esc(t): return t.replace("\\","\\\\").replace(":","\\:").replace("'","\u2019").replace("%","\\%").replace(",","\\,")
def seg(clip, vo, out, caption=None):
    cd = dur(clip); vd = dur(vo) if vo else 0
    d = max(cd, vd + 0.9); pad = max(0, d - cd)
    vf = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.2f}"
    if caption:
        vf += (f",drawbox=x=0:y=ih-110:w=iw:h=110:color=black@0.55:t=fill,"
               f"drawtext=fontfile={FONTB}:text='{esc(caption)}':fontsize=44:fontcolor=white:x=(w-tw)/2:y=h-82:alpha='min(1,max(0,(t-0.3)/0.4))'")
    a = ["ffmpeg","-v","error","-y","-i",clip]
    if vo: a += ["-i", vo, "-filter_complex", f"[0:v]{vf}[v];[1:a]adelay=350|350,apad,atrim=0:{d:.2f},aformat=sample_rates=48000:channel_layouts=stereo[a]", "-map","[v]","-map","[a]"]
    else: a += ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-filter_complex", f"[0:v]{vf}[v]", "-map","[v]","-map","1:a"]
    run(a + ["-t", f"{d:.2f}", "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k", out])
def card(out, lang, company, title, tagline, logo=None, d=5.0):
    l1, l2, ai = DIS[lang]; l1 = l1.format(c=company)
    vf = []
    inputs = ["-f","lavfi","-i",f"color=c=0x0d0d0f:s=1280x720:r=24:d={d}"]
    if logo:
        inputs += ["-i", logo]
        fc = f"[1:v]scale=-1:170[l];[0:v][l]overlay=(W-w)/2:120[b];[b]"
        ty = 330
    else:
        fc = "[0:v]"; ty = 200
        vf.append(f"drawtext=fontfile={FONTB}:text='{esc(title)}':fontsize=72:fontcolor=white:x=(w-tw)/2:y=170")
        ty = 290
    vf += [f"drawtext=fontfile={FONT}:text='{esc(tagline)}':fontsize=42:fontcolor=0xf2c14e:x=(w-tw)/2:y={ty+40}",
           f"drawtext=fontfile={FONT}:text='{esc(l1)}':fontsize=22:fontcolor=0xbbbbbb:x=(w-tw)/2:y=560",
           f"drawtext=fontfile={FONT}:text='{esc(l2)}':fontsize=22:fontcolor=0xbbbbbb:x=(w-tw)/2:y=592",
           f"drawtext=fontfile={FONT}:text='{esc(ai)}':fontsize=20:fontcolor=0x888888:x=(w-tw)/2:y=650",
           "fade=t=in:st=0:d=0.5"]
    run(["ffmpeg","-v","error","-y"] + inputs + ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-filter_complex", fc + ",".join(vf) + "[v]",
         "-map","[v]","-map",f"{2 if logo else 1}:a","-t",str(d),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k", out])
def join(parts, out, xf=0.4):
    ds = [dur(p) for p in parts]; a = ["ffmpeg","-v","error","-y"]
    for p in parts: a += ["-i", p]
    v = "[0:v]"; au = "[0:a]"; off = 0; fc = []
    for i in range(1, len(parts)):
        off += ds[i-1] - xf
        fc.append(f"{v}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[v{i}]"); v = f"[v{i}]"
        fc.append(f"{au}[{i}:a]acrossfade=d={xf}[a{i}]"); au = f"[a{i}]"
    fc.append(f"{au}loudnorm=I=-16:TP=-1.5[ao]")
    run(a + ["-filter_complex", ";".join(fc), "-map", v, "-map", "[ao]", "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart", out])
def build(name, lang, company, title, shots, tagline, logo=None, captions=None):
    parts = []
    for i, (clip, vo) in enumerate(shots):
        p = f"tmp/{name}_{i}.mp4"; seg(clip, vo, p, captions[i] if captions else None); parts.append(p)
    c = f"tmp/{name}_card.mp4"; card(c, lang, company, title, tagline, logo); parts.append(c)
    out = f"{OUT}/{name}.mp4"; join(parts, out); print(name, round(dur(out), 1), "s", flush=True)

COMM = {"bw": ("Beograd na vodi", "Belgrade Waterfront"), "gener2": ("Gener 2", "GENER 2"), "concord": ("Concord Investment", "CONCORD"),
        "kam": ("КАМ", "КАМ"), "viva": ("Viva Fresh", "VIVA FRESH"), "alkaloid": ("Алкалоид", "АЛКАЛОИД"), "replek": ("Реплек", "РЕПЛЕК"),
        "millennium": ("Millennium Team", "MILLENNIUM TEAM"), "nelt": ("Nelt Group", "NELT"), "speeex": ("SPEEEX", "SPEEEX")}
only = sys.argv[1:]
for cid, (company, title) in COMM.items():
    if only and cid not in only: continue
    lang, voice, lines = VO[cid]
    build(f"{cid}_commercial", lang, company, title, [(f"{CLIPS}/comm_{cid}_{i}.mp4", f"{TR}/{cid}_{i}.wav") for i in range(1, 6)], lines[-1])
logo = f"{S}/qc/vlogo.png"
if not only or "vc1" in only:   # vc1_3 (bite close-up) dropped: unnatural composite
    build("vincinni_family_ad", "mk", "Макпрогрес / Vincinni", "Vincinni",
          [(f"{CLIPS}/vc1_{i}.mp4", f"{TR}/vincinni_vc1_{i}.wav") for i in (1, 2, 4, 5)], "Секогаш по твој вкус.", logo)
if not only or "vc2" in only:
    build("vincinni_factory_ad", "mk", "Макпрогрес / Vincinni", "Vincinni",
          [(f"{CLIPS}/vc2_{i}.mp4", f"{TR}/vincinni_vc2_{i}.wav") for i in range(1, 6)], "It's Good. It's Vincinni.", logo)
if not only or "fs" in only:
    caps = ["TUNLAND V9", "2.0 L турбо дизел + 48V хибрид", "129 kW · 450 + 50 Nm · 8-AT", "4×4 · електрична блокада", "14,6\" екран · кожни седишта", "€42.900 без ДДВ · 5 год. гаранција"]
    build("foton_tunland_v9_specs", "mk", "Foton Македонија", "FOTON · TUNLAND V9",
          [(f"{CLIPS}/fs{i}.mp4", f"{TR}/foton_specs_{i}.wav") for i in range(1, 7)], "Закажи тест возење.", None, caps)
