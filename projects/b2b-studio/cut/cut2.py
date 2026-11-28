# LTX commercial batch 2 (31 films). Reuses cut.py helpers; adds studio-demo end cards and per-shot trimming.
import os, sys, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
src = open(f"{S}/cut/cut.py").read().split("\nCOMM =")[0]; exec(src)
os.chdir(f"{S}/cut"); sys.path.insert(0, f"{S}/vo")
from batch2 import CUTS
OUT = f"{S}/final_commercials_b2"; os.makedirs(OUT, exist_ok=True)
DIRS = [f"{S}/ltx610", f"{S}/ltx25"]
def clip(cid):
    for d in DIRS:
        p = f"{d}/{cid}.mp4"
        if os.path.exists(p): return p
    raise FileNotFoundError(cid)
def seg2(clipf, vo, out, trim=None):
    cd = dur(clipf); vd = dur(vo) if vo else 0
    d = max(cd, vd + 0.9)
    if trim: d = max(trim, vd + 0.9) if vo else trim
    pad = max(0, d - cd)
    vf = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.2f}"
    a = ["ffmpeg","-v","error","-y","-i",clipf]
    if vo: a += ["-i", vo, "-filter_complex", f"[0:v]{vf}[v];[1:a]adelay=300|300,apad,atrim=0:{d:.2f},aformat=sample_rates=48000:channel_layouts=stereo[a]", "-map","[v]","-map","[a]"]
    else: a += ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-filter_complex", f"[0:v]{vf}[v]", "-map","[v]","-map","1:a"]
    run(a + ["-t", f"{d:.2f}", "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k", out])
def studio_card(out, title, tagline, d=5.0):
    vf = [f"drawtext=fontfile={FONTB}:text='{esc(title)}':fontsize=64:fontcolor=white:x=(w-tw)/2:y=190",
          f"drawtext=fontfile={FONT}:text='{esc(tagline)}':fontsize=40:fontcolor=0xf2c14e:x=(w-tw)/2:y=310",
          f"drawtext=fontfile={FONT}:text='{esc('Вашиот проект, вашите луѓе, вашиот бренд: готово за 7 до 10 дена.')}':fontsize=26:fontcolor=0xdddddd:x=(w-tw)/2:y=430",
          f"drawtext=fontfile={FONT}:text='{esc('Демо концепт на студиото. Сцените се генерирани и не прикажуваат вистински објект.')}':fontsize=20:fontcolor=0x999999:x=(w-tw)/2:y=600",
          f"drawtext=fontfile={FONT}:text='{esc('Видео изработено со вештачка интелигенција (LTX-2.5)')}':fontsize=20:fontcolor=0x888888:x=(w-tw)/2:y=640",
          "fade=t=in:st=0:d=0.5"]
    run(["ffmpeg","-v","error","-y","-f","lavfi","-i",f"color=c=0x0d0d0f:s=1280x720:r=24:d={d}","-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
         "-filter_complex","[0:v]"+",".join(vf)+"[v]","-map","[v]","-map","1:a","-t",str(d),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",out])
only = sys.argv[1:]
for c in CUTS:
    name, lang, voice, company, title, tagline, shots = c[:7]
    trim = c[8] if len(c) > 8 else None
    if only and name not in only: continue
    if os.path.exists(f"{OUT}/{name}.mp4") and not only: continue
    parts = []; li = 0
    for i, (cid, line) in enumerate(shots):
        vo = None
        if line:
            li += 1; vo = f"{TR}/b2_{name}_{li}.wav"
            if not os.path.exists(vo): print("MISSING VO", vo); vo = None
        p = f"tmp/b2_{name}_{i}.mp4"; seg2(clip(cid), vo, p, trim); parts.append(p)
    cp = f"tmp/b2_{name}_card.mp4"
    if company: card(cp, lang, company, title, tagline, None)
    else: studio_card(cp, title, tagline)
    parts.append(cp); out = f"{OUT}/{name}.mp4"; join(parts, out, 0.35); print(name, round(dur(out), 1), "s", flush=True)
