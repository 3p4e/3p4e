# H3 commercial batch, built ON the Japan box (H3 output may not leave the permitted territory).
# Same structure as the LTX batches: shots + local-language VO + ACE-Step music bed + end card, plus H3's native ambient
# sound under everything and a "Made with MiniMax H3" credit on every end card. Films whose VO shots lack an H3 clip are skipped.
import os, sys, subprocess, json
W = "/workspace/h3cut"; sys.path.insert(0, f"{W}/vo")
from vo_lines import VO
from batch2 import CUTS
CLIPDIRS = ["/workspace/h3out", "/workspace/old_box_h3out"]
OUT = "/workspace/h3_commercials"; VOUT = "/workspace/h3_commercials_9x16"; TMP = f"{W}/tmp"
for d in (OUT, VOUT, TMP): os.makedirs(d, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TR = f"{W}/vo/trim"; MUS = f"{W}/music"
CREDIT = "Made with MiniMax H3 · AI-generated video"
DIS = {"mk": ("Концепт изработен само за презентација на {c}.", "Не е објавен и нема да биде објавен без нивно изречно писмено одобрение."),
       "sr": ("Koncept izrađen samo za prezentaciju kompaniji {c}.", "Nije objavljen i neće biti objavljen bez njihovog izričitog pisanog odobrenja."),
       "sq": ("Koncept i përgatitur vetëm për prezantim te {c}.", "Nuk është publikuar dhe nuk do të publikohet pa miratimin e tyre të shprehur me shkrim.")}
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
def esc(t): return t.replace("\\","\\\\").replace(":","\\:").replace("'","\u2019").replace("%","\\%").replace(",","\\,")
def clip(cid):
    for name in (f"h3_{cid}", "h3_" + cid.replace("ltx_t2v_", "t2v_")):
        for d in CLIPDIRS:
            p = f"{d}/{name}.mp4"
            if os.path.exists(p): return p
    return None
def has_audio(f): return bool(subprocess.run(["ffprobe","-v","error","-select_streams","a","-show_entries","stream=index","-of","csv=p=0",f],capture_output=True,text=True).stdout.strip())
def seg(c, vo, out, trim=None, caption=None):
    cd = dur(c); vd = dur(vo) if vo else 0
    d = max(cd, vd + 0.9) if not trim else (max(trim, vd + 0.9) if vo else trim)
    pad = max(0, d - cd)
    vf = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.2f}"
    if caption: vf += (f",drawbox=x=0:y=ih-110:w=iw:h=110:color=black@0.55:t=fill,drawtext=fontfile={FONTB}:text='{esc(caption)}':fontsize=44:fontcolor=white:x=(w-tw)/2:y=h-82")
    amb = "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.2,apad" if has_audio(c) else "anullsrc=r=48000:cl=stereo"
    a = ["ffmpeg","-v","error","-y","-i",c]
    if vo:
        a += ["-i", vo, "-filter_complex", f"[0:v]{vf}[v];{amb}[amb];[1:a]adelay=300|300,apad,aformat=sample_rates=48000:channel_layouts=stereo[vo];[amb][vo]amix=inputs=2:duration=first:normalize=0,atrim=0:{d:.2f}[a]", "-map","[v]","-map","[a]"]
    else:
        a += ["-filter_complex", f"[0:v]{vf}[v];{amb},atrim=0:{d:.2f}[a]", "-map","[v]","-map","[a]"]
    run(a + ["-t", f"{d:.2f}", "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k", out])
def card(out, lang, company, title, tagline, logo=None, d=5.0):
    lines = []
    if company:
        l1, l2 = DIS[lang]; lines = [l1.format(c=company), l2]
    else:
        lines = ["Вашиот проект, вашите луѓе, вашиот бренд: готово за 7 до 10 дена.", "Демо концепт на студиото. Сцените се генерирани и не прикажуваат вистински објект."]
    inputs = ["-f","lavfi","-i",f"color=c=0x0d0d0f:s=1280x720:r=24:d={d}"]; vf = []
    if logo:
        inputs += ["-i", logo]; fc = "[1:v]scale=-1:170[l];[0:v][l]overlay=(W-w)/2:110[b];[b]"; ty = 320
    else:
        fc = "[0:v]"; ty = 280; vf.append(f"drawtext=fontfile={FONTB}:text='{esc(title)}':fontsize=64:fontcolor=white:x=(w-tw)/2:y=170")
    vf += [f"drawtext=fontfile={FONT}:text='{esc(tagline)}':fontsize=40:fontcolor=0xf2c14e:x=(w-tw)/2:y={ty+40}",
           f"drawtext=fontfile={FONT}:text='{esc(lines[0])}':fontsize=22:fontcolor=0xbbbbbb:x=(w-tw)/2:y=540",
           f"drawtext=fontfile={FONT}:text='{esc(lines[1])}':fontsize=22:fontcolor=0xbbbbbb:x=(w-tw)/2:y=572",
           f"drawtext=fontfile={FONTB}:text='{esc(CREDIT)}':fontsize=22:fontcolor=0xdddddd:x=(w-tw)/2:y=640","fade=t=in:st=0:d=0.5"]
    run(["ffmpeg","-v","error","-y"] + inputs + ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-filter_complex", fc + ",".join(vf) + "[v]",
         "-map","[v]","-map",f"{2 if logo else 1}:a","-t",str(d),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k", out])
def join(parts, out, music, xf=0.35):
    ds = [dur(p) for p in parts]; a = ["ffmpeg","-v","error","-y"]
    for p in parts: a += ["-i", p]
    a += ["-i", music]; mi = len(parts)
    v = "[0:v]"; au = "[0:a]"; off = 0; fc = []
    for i in range(1, len(parts)):
        off += ds[i-1] - xf
        fc.append(f"{v}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[v{i}]"); v = f"[v{i}]"
        fc.append(f"{au}[{i}:a]acrossfade=d={xf}[a{i}]"); au = f"[a{i}]"
    total = sum(ds) - xf * (len(parts) - 1); fo = max(0, total - 2.5)
    fc.append(f"{au}asplit=2[mix][key]")
    fc.append(f"[{mi}:a]aloop=loop=-1:size=2e9,atrim=0:{total:.2f},volume=0.14,afade=t=in:st=0:d=0.8,afade=t=out:st={fo:.2f}:d=2.5,aformat=sample_rates=48000:channel_layouts=stereo[m]")
    fc.append("[m][key]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=400[md]")
    fc.append("[mix][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[ao]")
    run(a + ["-filter_complex", ";".join(fc), "-map", v, "-map", "[ao]", "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart", out])
def vertical(src, out):
    run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex","[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2",
         "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",out])
MOOD = json.load(open(f"{W}/mood_map.json"))
def build(name, lang, company, title, tagline, shots, logo=None, captions=None, trim=None):
    out = f"{OUT}/{name}_H3.mp4"
    if os.path.exists(out): return
    parts = []; skipped = []
    for i, (cid, vo) in enumerate(shots):
        c = clip(cid)
        if not c:
            if vo: print("SKIP", name, "missing", cid, flush=True); return
            skipped.append(cid); continue
        p = f"{TMP}/{name}_{i}.mp4"; seg(c, vo, p, trim, captions[i] if captions else None); parts.append(p)
    cp = f"{TMP}/{name}_card.mp4"; card(cp, lang, company, title, tagline, logo); parts.append(cp)
    join(parts, out, f"{MUS}/{MOOD[name]}.mp3"); vertical(out, f"{VOUT}/{name}_H3_9x16.mp4")
    print("OK", name, round(dur(out), 1), "s", ("(dropped " + ",".join(skipped) + ")") if skipped else "", flush=True)
COMM = {"bw": ("Beograd na vodi", "Belgrade Waterfront"), "gener2": ("Gener 2", "GENER 2"), "concord": ("Concord Investment", "CONCORD"),
        "viva": ("Viva Fresh", "VIVA FRESH"), "alkaloid": ("Алкалоид", "АЛКАЛОИД"), "replek": ("Реплек", "РЕПЛЕК"),
        "millennium": ("Millennium Team", "MILLENNIUM TEAM"), "nelt": ("Nelt Group", "NELT"), "speeex": ("SPEEEX", "SPEEEX")}
for cid, (company, title) in COMM.items():
    lang, voice, lines = VO[cid]
    build(f"{cid}_commercial", lang, company, title, lines[-1], [(f"comm_{cid}_{i}", f"{TR}/{cid}_{i}.wav") for i in range(1, 6)])
build("zito_commercial", "mk", "Жито маркети", "Жито маркети", "Свежината започнува тука.", [(f"comm_kam_{i}", f"{TR}/zito_{i}.wav") for i in range(1, 6)], f"{W}/qc/zlogo.png")
build("vincinni_family_ad", "mk", "Макпрогрес / Vincinni", "Vincinni", "Секогаш по твој вкус.", [(f"vc1_{i}", f"{TR}/vincinni_vc1_{i}.wav") for i in (1, 2, 4, 5)], f"{W}/qc/vlogo.png")
build("vincinni_factory_ad", "mk", "Макпрогрес / Vincinni", "Vincinni", "It's Good. It's Vincinni.", [(f"vc2_{i}", f"{TR}/vincinni_vc2_{i}.wav") for i in range(1, 6)], f"{W}/qc/vlogo.png")
caps = ["TUNLAND V9", "2.0 L турбо дизел + 48V хибрид", "129 kW · 450 + 50 Nm · 8-AT", "4×4 · електрична блокада", "14,6\" екран · кожни седишта", "€42.900 без ДДВ · 5 год. гаранција"]
build("foton_tunland_v9_specs", "mk", "Foton Македонија", "FOTON · TUNLAND V9", "Закажи тест возење.", [(f"fs{i}", f"{TR}/foton_specs_{i}.wav") for i in range(1, 7)], None, caps)
for c in CUTS:
    name, lang, voice, company, title, tagline, shots = c[:7]
    if name.endswith("_film"): continue          # company second films use proposal shots that were not rendered on H3
    trim = c[8] if len(c) > 8 else None
    li = 0; sh = []
    for cid, line in shots:
        vo = None
        if line: li += 1; vo = f"{TR}/b2_{name}_{li}.wav"
        sh.append((cid, vo))
    build(name, lang, company, title, tagline, sh, None, None, trim)
print("H3_CUT_DONE", len([f for f in os.listdir(OUT) if f.endswith(".mp4")]), "films")
