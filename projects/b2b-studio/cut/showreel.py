# 60-second studio showreel from the best LTX shots, with Macedonian sector captions; studio card at both ends.
import os, sys
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
exec(open(f"{S}/cut/cut2.py").read().split("\nonly = sys.argv")[0])
SHOTS = [("fs1","Автомобили"),("tl_03_frame","Градежништво"),("vc2_2","Прехранбена индустрија"),("comm_bw_3","Недвижности"),
         ("br_c10_s3to4","Внатрешен дизајн"),("br_c04_s3","Автомобилска индустрија"),("comm_alkaloid_2","Фармација"),("x_wine_x1","Винарии"),
         ("tl2_solar_2","Енергетика"),("fs3","Автомобили"),("comm_gener2_1","Градежништво"),("st_03_styled","Опремување станови"),
         ("br_c08_s2","Челик и цемент"),("comm_viva_3","Малопродажба"),("tl2_road_2","Инфраструктура"),("x_prod_x1","Лансирање производи")]
def shot(cid, cap, out, d=3.4):
    c = clip(cid); cd = dur(c); ss = max(0, (cd - d) / 2)
    vf = (f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24,"
          f"drawtext=fontfile={FONTB}:text='{esc(cap)}':fontsize=34:fontcolor=white:x=60:y=h-90:box=1:boxcolor=black@0.45:boxborderw=14")
    run(["ffmpeg","-v","error","-y","-ss",f"{ss:.2f}","-i",c,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-filter_complex",f"[0:v]{vf}[v]",
         "-map","[v]","-map","1:a","-t",str(d),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",out])
def title(out, l1, l2, d=3.0):
    vf = [f"drawtext=fontfile={FONTB}:text='{esc(l1)}':fontsize=60:fontcolor=white:x=(w-tw)/2:y=280",
          f"drawtext=fontfile={FONT}:text='{esc(l2)}':fontsize=34:fontcolor=0xf2c14e:x=(w-tw)/2:y=380","fade=t=in:st=0:d=0.4"]
    run(["ffmpeg","-v","error","-y","-f","lavfi","-i",f"color=c=0x0d0d0f:s=1280x720:r=24:d={d}","-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
         "-filter_complex","[0:v]"+",".join(vf)+"[v]","-map","[v]","-map","1:a","-t",str(d),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",out])
parts = []
title("tmp/sr_open.mp4", "AI видео за вашиот бизнис", "Ваши производи. Ваши луѓе. Ваши проекти."); parts.append("tmp/sr_open.mp4")
for i, (cid, cap) in enumerate(SHOTS):
    p = f"tmp/sr_{i}.mp4"; shot(cid, cap, p); parts.append(p)
studio_card("tmp/sr_card.mp4", "Од идеја до реклама", "Пилот · Лансирање · Месечна содржина"); parts.append("tmp/sr_card.mp4")
out = f"{S}/final_commercials_b2/studio_showreel_ltx.mp4"; join(parts, out, 0.3); print("showreel", round(dur(out), 1))
