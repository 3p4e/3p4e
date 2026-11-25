# BIG DOGMA public site: build all web media from PUBLIC-SAFE sources only.
# Output: S/launch/site/{media,films,subs}. Heavy intermediates in /dev/shm (root disk is nearly full).
import os, sys, json, re, shutil, subprocess
from concurrent.futures import ThreadPoolExecutor
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
OUT = f"{S}/launch/site"; TMP = "/dev/shm/bd_site"; os.makedirs(TMP, exist_ok=True)
for d in ("media", "films", "subs"): os.makedirs(f"{OUT}/{d}", exist_ok=True)
NICE = ["nice", "-n", "10"]
def run(a): subprocess.run(NICE + a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
FF = ["ffmpeg", "-v", "error", "-y"]
# web audio: AAC-LC 48 kHz (decoders such as Windows Media Foundation reject > 48 kHz; the film masters are 96 kHz), 160 kb/s,
# every site video normalised to one loudness target (-16 LUFS integrated, true peak <= -1 dBTP on the final AAC).
# Method (same as the social kit's reels): measure, gain + brick-wall limiter at -1.9 dBFS, measure again, one corrective gain.
# Two-pass loudnorm was tried first: on the quieter films it falls back to its dynamic mode, lands 1-1.5 LU off and let one
# film overshoot to +0.9 dBTP after AAC encoding.
LUFS = -16.0
AAC = ["-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
LIM = "alimiter=limit=0.80:attack=3:release=60:level=disabled:asc=1"
def measure(src):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
def norm_audio(src, key):
    # -> 48 kHz stereo WAV in TMP at LUFS (the source masters are 96 kHz)
    out = f"{TMP}/{key}_norm.wav"; tmp = f"{TMP}/{key}_tmp.wav"
    g = LUFS - measure(src)
    subprocess.run(FF + ["-i", src, "-vn", "-af", f"aresample=48000,volume={g:.2f}dB,{LIM}", "-ac", "2", "-c:a", "pcm_s16le", tmp], check=True)
    g += LUFS - measure(tmp)
    subprocess.run(FF + ["-i", src, "-vn", "-af", f"aresample=48000,volume={g:.2f}dB,{LIM}", "-ac", "2", "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp); return out
def av(src, key):
    # input args + maps: picture from src, normalised audio from the WAV
    return ["-i", src, "-i", norm_audio(src, key), "-map", "0:v:0", "-map", "1:a:0"]
X264 = ["-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1", "-threads", "2"]
FILMS = ["sector_automotive", "sector_pharma", "sector_food", "sector_wine", "sector_steel_cement", "sector_recruitment", "sector_product_launch", "sector_real_estate",
         "timelapse_construction", "timelapse_developer", "timelapse_apartment_staging", "timelapse_interior_design", "timelapse_office_fitout",
         "timelapse_landscaping", "timelapse_store_fitout", "timelapse_expo_stand", "timelapse_solar", "timelapse_road", "showreel_macedonian_industry"]
# timelapse_renovation is left out on purpose: its VO lines land on "before" shots (same reason it left the social kit)
THUMB_AT = {}  # per-film override of the thumbnail time (fraction of duration)
def thumb_t(n, du): return du - 7.0 if n.startswith("timelapse_") else THUMB_AT.get(n, 0.3) * du  # timelapses: finished state, before the end card
step = sys.argv[1] if len(sys.argv) > 1 else "all"

def hero():
    # 6 generic LTX clips, 2.3 s each, 0.5 s dissolves, seamless loop (the last dissolve lands back on clip 1)
    clips = [("ltx25", "br_c08_s2", 0.6), ("ltx610", "x_con_x1", 0.8), ("ltx610", "tl2_road_2", 0.8), ("ltx610", "x_wine_x2", 0.8), ("ltx610", "x_re_x2", 0.8), ("ltx610", "x_steel_x2", 0.8)]
    L, D = 2.3, 0.5
    seq = clips + [clips[0]]
    ins, fl = [], []
    for i, (d, n, ss) in enumerate(seq):
        ins += ["-ss", str(ss), "-t", str(L), "-i", f"{S}/{d}/{n}.mp4"]
        fl.append(f"[{i}:v]scale=-2:720,crop=1280:720,fps=24,format=yuv420p,setsar=1,settb=AVTB[v{i}]")
    prev = "v0"
    for k in range(1, len(seq)):
        fl.append(f"[{prev}][v{k}]xfade=transition=fade:duration={D}:offset={k * (L - D):.3f}[x{k}]"); prev = f"x{k}"
    T = (len(seq) - 1) * (L - D)
    fl.append(f"[{prev}]trim=start={D}:duration={T:.3f},setpts=PTS-STARTPTS[out]")
    run(FF + ins + ["-filter_complex", ";".join(fl), "-map", "[out]", "-an", "-crf", "25"] + X264 + ["-g", "48", f"{OUT}/media/hero.mp4"])
    run(FF + ["-i", f"{OUT}/media/hero.mp4", "-frames:v", "1", "-q:v", "4", f"{OUT}/media/hero.jpg"])
    print("hero", dur(f"{OUT}/media/hero.mp4"), flush=True)

def showreel():
    src = f"{S}/launch/video/bigdogma_showreel_16x9.mp4"; src9 = f"{S}/launch/video/bigdogma_showreel_9x16.mp4"
    run(FF + av(src, "showreel") + ["-vf", "scale=1280:-2", "-crf", "25"] + X264 + AAC + ["-shortest", f"{OUT}/media/showreel.mp4"])
    run(FF + ["-ss", "1.6", "-i", src, "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "3", f"{OUT}/media/showreel.jpg"])
    if os.path.exists(src9):
        run(FF + av(src9, "showreel9") + ["-vf", "scale=720:-2", "-crf", "26"] + X264 + AAC + ["-shortest", f"{OUT}/media/showreel_9x16.mp4"])
        run(FF + ["-ss", "1.6", "-i", src9, "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", f"{OUT}/media/showreel_9x16.jpg"])
    for k in ("showreel", "showreel9"):
        if os.path.exists(f"{TMP}/{k}_norm.wav"): os.remove(f"{TMP}/{k}_norm.wav")
    print("showreel done", flush=True)

def srt2vtt(src, dst):
    t = open(src, encoding="utf-8").read().replace("\r", "").strip()
    t = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", t)
    open(dst, "w", encoding="utf-8").write("WEBVTT\n\n" + t + "\n")

def film(n):
    src = f"{S}/final_music/{n}.mp4"; du = dur(src)
    run(FF + av(src, n) + ["-vf", "scale=1280:-2", "-crf", "26"] + X264 + AAC + ["-shortest", f"{OUT}/films/{n}.mp4"])
    os.remove(f"{TMP}/{n}_norm.wav")
    at = thumb_t(n, du)
    run(FF + ["-ss", f"{at:.2f}", "-i", src, "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "4", f"{OUT}/films/{n}.jpg"])
    for L in ("mk", "en"):
        s = f"{S}/subs/srt/{n}.{L}.srt"
        if os.path.exists(s): srt2vtt(s, f"{OUT}/subs/{n}.{L}.vtt")
    print("film", n, os.path.getsize(f"{OUT}/films/{n}.mp4") // 1024, "KB", flush=True)

def thumbs():
    for n in FILMS:
        src = f"{S}/final_music/{n}.mp4"; at = thumb_t(n, dur(src))
        run(FF + ["-ss", f"{at:.2f}", "-i", src, "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "4", f"{OUT}/films/{n}.jpg"])

def howto():
    # how-it-works film: the 16:9 rebuild from howto169.py (title card with the AI disclosure, step 3 = the finished building
    # with its closing VO). Poster = the title card, so the disclosure is visible before play.
    src = f"{S}/launch/site_work/howto/howto_16x9.mp4"
    if not os.path.exists(src): subprocess.run(["/usr/local/bin/python3", f"{S}/launch/site_work/howto169.py"], check=True)
    run(FF + av(src, "howto") + ["-vf", "scale=1280:-2", "-crf", "25"] + X264 + AAC + ["-shortest", f"{OUT}/media/howto.mp4"])
    run(FF + ["-ss", "0.6", "-i", src, "-frames:v", "1", "-q:v", "3", f"{OUT}/media/howto.jpg"])
    os.remove(f"{TMP}/howto_norm.wav")

def compare():
    # "from one image to AI video" slider: key frame extras/kf/re_x2.png and its LTX image-to-video clip ltx610/x_re_x2.mp4.
    # Static rooftop scene, no people or machines: the light goes from sunset to dusk and the lamps come on, the composition
    # stays on the key frame (ECC alignment of frame 0 vs the key frame = identity). Both 1280x704. The clip plays forward and
    # then backward (10 s) so the loop has no jump.
    run(FF + ["-i", f"{S}/extras/kf/re_x2.png", "-vf", "scale=1280:704", "-q:v", "3", f"{OUT}/media/kf_terrace.jpg"])
    run(FF + ["-i", f"{S}/ltx610/x_re_x2.mp4", "-an", "-filter_complex",
              "[0:v]fps=24,scale=1280:704,setsar=1,trim=end_frame=120,setpts=PTS-STARTPTS,split[a][b];[b]reverse,trim=start_frame=1:end_frame=119,setpts=PTS-STARTPTS[r];[a][r]concat=n=2:v=1:a=0[v]",
              "-map", "[v]", "-crf", "24"] + X264 + ["-g", "48", f"{OUT}/media/ai_terrace.mp4"])
    for old in ("ai_excavation.mp4", "kf_excavation.jpg"):
        if os.path.exists(f"{OUT}/media/{old}"): os.remove(f"{OUT}/media/{old}")

def extras():
    howto(); compare()
    # brand files, OG image
    shutil.copy(f"{S}/brand/logo.png", f"{OUT}/media/logo.png")
    shutil.copy(f"{S}/brand/icon_512.png", f"{OUT}/icon.png")
    for s in ("i32", "i64"): shutil.copy(f"{S}/brand/{s}.png", f"{OUT}/{s}.png")
    # OG / link-preview image 1200x630: darkened steel frame + lockup
    run(FF + ["-ss", "1.2", "-i", f"{S}/ltx25/br_c08_s2.mp4", "-i", f"{S}/brand/logo.png", "-filter_complex",
              "[0:v]scale=1200:630:force_original_aspect_ratio=increase,crop=1200:630,eq=brightness=-0.18:saturation=0.9,boxblur=2[b];[1:v]scale=960:-2[l];[b][l]overlay=(W-w)/2:(H-h)/2",
              "-frames:v", "1", "-q:v", "3", f"{OUT}/media/og.jpg"])
    print("extras done", flush=True)


def gallery():
    # AI gallery / sector shots / image-to-motion / build-up viewer: brand-neutral LTX clips from gallery_data.py.
    # 960x528 (the 1280x704 masters at 3/4), 5 s, CRF 28, no audio, faststart; a 640 px poster per clip; key frames as JPEG.
    sys.path.insert(0, f"{S}/launch/site_work"); import gallery_data as G
    os.makedirs(f"{OUT}/media/g", exist_ok=True); os.makedirs(f"{OUT}/media/k", exist_ok=True)
    def enc(cid):
        src = f"{S}/{G.SRC[cid]}/{cid}.mp4"; out = f"{OUT}/media/g/{cid}.mp4"
        if not os.path.exists(out):
            run(FF + ["-i", src, "-an", "-t", "5", "-vf", "scale=960:528,fps=24,setsar=1", "-c:v", "libx264", "-preset", "slow", "-crf", "28",
                      "-pix_fmt", "yuv420p", "-g", "48", "-movflags", "+faststart", "-map_metadata", "-1", "-threads", "2", out])
        run(FF + ["-ss", "1.5", "-i", src, "-frames:v", "1", "-vf", "scale=640:352", "-q:v", "6", f"{OUT}/media/g/{cid}.jpg"])
    with ThreadPoolExecutor(3) as ex: list(ex.map(enc, list(G.SRC)))
    for k in G.KEYFRAMES:
        kid = G.kf_id(k)
        run(FF + ["-i", f"{S}/{k}", "-vf", "scale=960:528", "-q:v", "4", f"{OUT}/media/k/{kid}.jpg"])
        run(FF + ["-i", f"{S}/{k}", "-vf", "scale=320:176", "-q:v", "6", f"{OUT}/media/k/{kid}_t.jpg"])
    for cid, *_ in G.I2V:   # image -> motion: the poster is the clip's last frame, so the "AI video" panel shows the result before it plays
        run(FF + ["-sseof", "-0.2", "-i", f"{S}/{G.SRC[cid]}/{cid}.mp4", "-frames:v", "1", "-vf", "scale=640:352", "-q:v", "6", f"{OUT}/media/g/{cid}_end.jpg"])
    keep = {f"{c}.mp4" for c in G.SRC} | {f"{c}.jpg" for c in G.SRC} | {f"{c}_end.jpg" for c, *_ in G.I2V}
    for f in os.listdir(f"{OUT}/media/g"):
        if f not in keep: os.remove(f"{OUT}/media/g/{f}")
    print("gallery", len(G.SRC), "clips", len(G.KEYFRAMES), "key frames", flush=True)

if step in ("all", "hero"): hero()
if step in ("all", "extras"): extras()
if step == "howto": howto()
if step == "compare": compare()
if step in ("all", "films"):
    with ThreadPoolExecutor(2) as ex: list(ex.map(film, FILMS))
    for gone in ("timelapse_renovation",):                     # films that left the site: remove their web files
        for f in (f"{OUT}/films/{gone}.mp4", f"{OUT}/films/{gone}.jpg", f"{OUT}/subs/{gone}.mk.vtt", f"{OUT}/subs/{gone}.en.vtt"):
            if os.path.exists(f): os.remove(f)
if step in ("all", "showreel"): showreel()
if step == "thumbs": thumbs()
if step in ("all", "gallery"): gallery()
print("MEDIA_DONE", step, flush=True)
