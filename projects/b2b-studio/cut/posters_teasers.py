# Per film: poster (1280x720 JPG: strongest mid-film frame + title + studio logo) and a 6 s teaser (silent MP4 loop + 480 px GIF)
# for email/WhatsApp/LinkedIn previews. Teasers carry the CONCEPT mark.
import os, sys, json, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
SRC = f"{S}/final_music"; OUT = f"{S}/previews"; os.makedirs(OUT, exist_ok=True)
LOGO = f"{S}/brand/logo.png"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TITLES = {"zito_commercial": "Жито маркети", "zito_opening_film": "Жито маркети", "alkaloid_commercial": "Алкалоид", "alkaloid_employer_film": "Алкалоид · Кариера",
 "replek_commercial": "Реплек", "replek_export_film": "Реплек · Извоз", "vincinni_family_ad": "Vincinni", "vincinni_factory_ad": "Vincinni · Фабрика",
 "foton_tunland_v9_specs": "Foton Tunland V9", "foton_showreel_v2": "Foton Македонија", "bw_commercial": "Beograd na vodi", "bw_riverside_film": "Beograd na vodi",
 "millennium_commercial": "Millennium Team", "millennium_capability_film": "Millennium Team", "nelt_commercial": "Nelt Group", "nelt_logistics_film": "Nelt Group",
 "gener2_commercial": "Gener 2", "gener2_builder_film": "Gener 2", "concord_commercial": "Concord", "concord_offplan_film": "Concord",
 "viva_commercial": "Viva Fresh", "viva_expansion_film": "Viva Fresh", "speeex_commercial": "SPEEEX", "speeex_recruitment_film": "SPEEEX · Karriera",
 "studio_showreel_ltx": "AI видео за вашиот бизнис", "showreel_macedonian_industry": "Македонска индустрија"}
def esc(t): return t.replace("\\","\\\\").replace(":","\\:").replace("'","\u2019").replace("%","\\%").replace(",","\\,")
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
def title_for(n):
    if n in TITLES: return TITLES[n]
    return n.replace("timelapse_", "Timelapse · ").replace("sector_", "Демо · ").replace("_", " ").title()
for f in sorted(os.listdir(SRC)):
    n = f[:-4]; src = f"{SRC}/{f}"; d = dur(src); t = esc(title_for(n))
    pf = f"{OUT}/{n}_poster.jpg"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{d*0.35:.2f}","-i",src,"-i",LOGO,"-filter_complex",
        f"[0:v]scale=1280:720,drawbox=x=0:y=ih-150:w=iw:h=150:color=black@0.6:t=fill,drawtext=fontfile={FONTB}:text='{t}':fontsize=54:fontcolor=white:x=50:y=h-112[b];"
        f"[1:v]scale=300:-1[l];[b][l]overlay=W-w-30:H-h-25","-frames:v","1","-q:v","3",pf], check=True)
    st = max(0.0, d * 0.25)
    mp = f"{OUT}/{n}_teaser6s.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{st:.2f}","-t","6","-i",src,"-vf",
        f"scale=960:540,drawtext=fontfile={FONTB}:text='{t}':fontsize=40:fontcolor=white:x=30:y=h-70:box=1:boxcolor=black@0.45:boxborderw=10,fade=t=in:st=0:d=0.3,fade=t=out:st=5.6:d=0.4",
        "-an","-c:v","libx264","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",mp], check=True)
    gif = f"{OUT}/{n}_teaser6s.gif"
    subprocess.run(["ffmpeg","-v","error","-y","-i",mp,"-vf","fps=12,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4",gif], check=True)
    print("OK", n, flush=True)
print("PREVIEWS_DONE")
