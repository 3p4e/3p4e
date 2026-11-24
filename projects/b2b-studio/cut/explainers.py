# "How it's made" explainers (~15 s, Macedonian): 1 your photo/render -> 2 keyframe for approval -> 3 AI animation -> 4 finished ad.
import os, json, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUT = f"{S}/explainers"; TMP = f"{S}/cut/tmp_expl"; os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
FONT = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/brand/fonts/RussoOne-400.ttf"; FONTB = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/brand/fonts/RussoOne-400.ttf"; LOGO = f"{S}/brand/logo.png"
B = json.load(open(f"{S}/brand/brand.json"))
def esc(t): return t.replace("\\","\\\\").replace(":","\\:").replace("'","\u2019").replace("%","\\%").replace(",","\\,")
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
ENC = ["-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","24"]
def label(n, txt): return (f"drawbox=x=0:y=0:w=iw:h=86:color=black@0.6:t=fill,drawtext=fontfile={FONTB}:text='{n}':fontsize=44:fontcolor=0xf2c14e:x=36:y=20,"
                          f"drawtext=fontfile={FONTB}:text='{esc(txt)}':fontsize=32:fontcolor=white:x=100:y=27")
def still(img, n, txt, out, d=3.2, fit="pad"):
    sc = ("scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x1a1a1f" if fit == "pad" else "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720")
    run(["ffmpeg","-v","error","-y","-framerate","24","-loop","1","-t",str(d),"-i",img,"-vf",f"{sc},zoompan=z='min(1+0.0008*on,1.06)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24,{label(n, txt)},fade=t=in:st=0:d=0.3","-an"] + ENC + [out])
def clipseg(src, n, txt, out, ss=0.5, d=3.6):
    run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(d),"-i",src,"-vf",f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,{label(n, txt)}","-an"] + ENC + [out])
def build(name, title, steps, music, film, film_ss):
    parts = []; film_ss = round(dur(film) * 0.4, 2)
    run(["ffmpeg","-v","error","-y","-f","lavfi","-i","color=c=0x0d0d0f:s=1280x720:r=24:d=2","-loop","1","-t","2","-i",LOGO,"-filter_complex",
         f"[1:v]scale=420:-1[l];[0:v][l]overlay=(W-w)/2:200,drawtext=fontfile={FONTB}:text='{esc('Како настанува рекламата')}':fontsize=46:fontcolor=white:x=(w-tw)/2:y=380,"
         f"drawtext=fontfile={FONT}:text='{esc(title)}':fontsize=30:fontcolor=0xf2c14e:x=(w-tw)/2:y=450","-an"] + ENC + [f"{TMP}/{name}_0.mp4"]); parts.append(f"{TMP}/{name}_0.mp4")
    for i, s in enumerate(steps, 1):
        p = f"{TMP}/{name}_{i}.mp4"
        if s[0] == "img": still(s[1], str(i), s[2], p, fit=s[3] if len(s) > 3 else "pad")
        else: clipseg(s[1], str(i), s[2], p, s[3] if len(s) > 3 else 0.5)
        parts.append(p)
    fin = f"{TMP}/{name}_fin.mp4"
    run(["ffmpeg","-v","error","-y","-ss",str(film_ss),"-t","4.5","-i",film,"-vf",f"scale=1280:720,{label(str(len(steps)+1), 'Готова реклама: глас, музика, 16:9 и 9:16')}","-an"] + ENC + [fin]); parts.append(fin)
    lst = f"{TMP}/{name}.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    silent = f"{TMP}/{name}_v.mp4"; run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c","copy",silent])
    d = dur(silent); fa = d - 4.5
    run(["ffmpeg","-v","error","-y","-i",silent,"-i",music,"-ss",str(film_ss),"-t","4.5","-i",film,"-filter_complex",
         f"[1:a]atrim=0:{d:.2f},volume=0.5,afade=t=in:st=0:d=0.6,afade=t=out:st={fa-0.6:.2f}:d=1.2[m];[2:a]adelay={int(fa*1000)}|{int(fa*1000)},afade=t=out:st={d-0.8:.2f}:d=0.8[f];"
         f"[m][f]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5,aresample=48000[a]",
         "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",f"{OUT}/{name}.mp4"])
    print("OK", name, round(dur(f"{OUT}/{name}.mp4"), 1), flush=True)
M = f"{S}/music/ace_final"; F = f"{S}/final_music"; L6 = f"{S}/ltx610"; L25 = f"{S}/ltx25"
build("howto_automotive", "Автомобили · Foton Tunland V9",
      [("img", f"{S}/foton/ref/v9.png", "Ваша официјална фотографија"), ("img", f"{S}/fotonspec/kf/fs1.png", "Клучен кадар за ваше одобрување", "crop"),
       ("clip", f"{L6}/fs1.mp4", "AI анимација")], f"{M}/4_automotive.mp3", f"{F}/foton_tunland_v9_specs.mp4", 36.5)
build("howto_fmcg", "Прехранбена индустрија · Vincinni",
      [("img", f"{S}/vincinni/assets/a009.png", "Ваше вистинско пакување"), ("img", f"{S}/vincinni/kf/vc1_2.png", "Клучен кадар за ваше одобрување", "crop"),
       ("clip", f"{L6}/vc1_2.mp4", "AI анимација")], f"{M}/1_family.mp3", f"{F}/vincinni_family_ad.mp4", 22.5)
build("howto_construction", "Градежништво · timelapse",
      [("img", f"{S}/construction/kf/con_01_excavation_start.png", "Ваш рендер или фотографија од плацот", "crop"),
       ("clip", f"{L25}/tl_03_frame.mp4", "AI timelapse по фази", 1.0)], f"{M}/3_construction.mp3", f"{F}/timelapse_construction.mp4", 33.0)
build("howto_retail", "Малопродажба · Жито маркети",
      [("img", f"{S}/comm/kf/kam_2.png", "Клучен кадар за ваше одобрување", "crop"), ("clip", f"{L6}/comm_kam_2.mp4", "AI анимација")],
      f"{M}/1_family.mp3", f"{F}/zito_commercial.mp4", 27.5)
build("howto_pharma", "Фармација · Алкалоид",
      [("img", f"{S}/comm/kf/alkaloid_2.png", "Клучен кадар за ваше одобрување", "crop"), ("clip", f"{L6}/comm_alkaloid_2.mp4", "AI анимација")],
      f"{M}/2_corporate.mp3", f"{F}/alkaloid_commercial.mp4", 27.5)
print("EXPLAINERS_DONE")
