# Pitch versions of every LTX film: 2.2 s studio logo intro + film with a small language-matched "CONCEPT" watermark
# + 3 s contact outro. 16:9 and 9:16. Brand/contact come from brand/brand.json (swap the placeholder, re-run).
import os, sys, json, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
B = json.load(open(f"{S}/brand/brand.json")); LOGO = f"{S}/brand/logo.png"
SRC = f"{S}/final_music"; OUT = f"{S}/pitch"; VOUT = f"{S}/pitch_9x16"; TMP = f"{S}/cut/tmp_pitch"
for d in (OUT, VOUT, TMP): os.makedirs(d, exist_ok=True)
FONT = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/brand/fonts/RussoOne-400.ttf"; FONTB = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/brand/fonts/RussoOne-400.ttf"
sys.path.insert(0, f"{S}/vo"); from vo_lines import VO; from batch2 import CUTS
LANG = {f"{k}_commercial": v[0] for k, v in VO.items()}
LANG.update({"zito_commercial": "mk", "vincinni_family_ad": "mk", "vincinni_factory_ad": "mk", "foton_tunland_v9_specs": "mk", "studio_showreel_ltx": "mk"})
LANG.update({c[0]: c[1] for c in CUTS})
WM = {"mk": "КОНЦЕПТ · НЕ Е ЗА ОБЈАВА", "sr": "KONCEPT · NIJE ZA OBJAVU", "sq": "KONCEPT · JO PËR PUBLIKIM"}
TAG = {"mk": B["tagline_mk"], "sr": B["tagline_sr"], "sq": B["tagline_sq"]}
CALL = {"mk": "Закажете 15 минути:", "sr": "Zakažite 15 minuta:", "sq": "Caktoni 15 minuta:"}
def esc(t): return t.replace("\\","\\\\").replace(":","\\:").replace("'","\u2019").replace("%","\\%").replace(",","\\,")
def run(a): subprocess.run(a, check=True)
def enc(): return ["-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000"]
def intro(out, d=2.2):
    fc = (f"[1:v]scale=840:-1,format=rgba,fade=t=in:st=0.15:d=0.6:alpha=1[l];[0:v][l]overlay=(W-w)/2:(H-h)/2-10,"
          f"drawbox=x='-300+t*900':y=0:w=120:h=ih:color=white@0.06:t=fill,fade=t=out:st={d-0.35}:d=0.35[v]")
    run(["ffmpeg","-v","error","-y","-f","lavfi","-i",f"color=c=0x0d0d0f:s=1280x720:r=24:d={d}","-loop","1","-t",str(d),"-i",LOGO,
         "-f","lavfi","-t",str(d),"-i","anullsrc=r=48000:cl=stereo","-filter_complex",fc,"-map","[v]","-map","2:a","-t",str(d)] + enc() + [out])
def outro(out, lang, d=3.2):
    lines = [f"drawtext=fontfile={FONT}:text='{esc(TAG[lang])}':fontsize=36:fontcolor=white:x=(w-tw)/2:y=360",
             f"drawtext=fontfile={FONT}:text='{esc(CALL[lang])}':fontsize=26:fontcolor=0xbbbbbb:x=(w-tw)/2:y=440",
             f"drawtext=fontfile={FONTB}:text='{esc(B['phone'] + '  ·  ' + B['email'])}':fontsize=30:fontcolor=0xf2c14e:x=(w-tw)/2:y=485",
             f"drawtext=fontfile={FONT}:text='{esc(B['web'])}':fontsize=24:fontcolor=0x999999:x=(w-tw)/2:y=540"]
    fc = f"[1:v]scale=600:-1[l];[0:v][l]overlay=(W-w)/2:110," + ",".join(lines) + ",fade=t=in:st=0:d=0.4[v]"
    run(["ffmpeg","-v","error","-y","-f","lavfi","-i",f"color=c=0x0d0d0f:s=1280x720:r=24:d={d}","-loop","1","-t",str(d),"-i",LOGO,
         "-f","lavfi","-t",str(d),"-i","anullsrc=r=48000:cl=stereo","-filter_complex",fc,"-map","[v]","-map","2:a","-t",str(d)] + enc() + [out])
def body(src, out, lang):
    vf = (f"drawtext=fontfile={FONTB}:text='{esc(WM[lang])}':fontsize=20:fontcolor=white@0.55:x=w-tw-24:y=22:box=1:boxcolor=black@0.25:boxborderw=8")
    run(["ffmpeg","-v","error","-y","-i",src,"-vf",vf] + enc() + [out])
def concat(parts, out):
    lst = f"{TMP}/list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c","copy","-movflags","+faststart",out])
def vertical(src, out):
    run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex","[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2",
         "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",out])
intro(f"{TMP}/intro.mp4")
for lang in ("mk", "sr", "sq"): outro(f"{TMP}/outro_{lang}.mp4", lang)
only = sys.argv[1:]
for f in sorted(os.listdir(SRC)):
    n = f[:-4]
    if only and n not in only: continue
    lang = LANG.get(n, "mk"); out = f"{OUT}/{n}_pitch.mp4"
    body(f"{SRC}/{f}", f"{TMP}/{n}_body.mp4", lang)
    concat([f"{TMP}/intro.mp4", f"{TMP}/{n}_body.mp4", f"{TMP}/outro_{lang}.mp4"], out)
    vertical(out, f"{VOUT}/{n}_pitch_9x16.mp4"); os.remove(f"{TMP}/{n}_body.mp4")
    print("OK", n, lang, flush=True)
print("PITCH_DONE")
