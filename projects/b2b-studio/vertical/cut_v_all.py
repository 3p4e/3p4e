# Native 9:16 edit of the 22 company films (owner, 2026-11-26), same method as cut_v.py for Foton: the picture is rebuilt at 1080x1920
# from the vertical LTX shots on exactly the timeline of the 16:9 film (cut.py / cut2.py / zito_cut.py rules: shot = max(clip, line + 0.9),
# trims, crossfades, 5 s end card, BD intro 2.2 s, contact outro 3.2 s), and the 16:9 pitch film's finished soundtrack is laid under it.
# Texts are fitted to the narrow frame (long titles shrink or wrap). Run with /usr/bin/python3 (PIL).
#   python3 cut_v_all.py check              -> planned body length vs the 16:9 film, for all 22
#   python3 cut_v_all.py fake               -> centre-crop stand-in clips in $VW/fake (layout and timing test before the real render)
#   python3 cut_v_all.py build [film...]    -> $VW/out/<film>_9x16_native.mp4 + $VW/web/<film>_9x16.mp4/.jpg   (VCLIPS=dir of v_<shot>.mp4)
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import all_v
from cut_v import seg, join, intro, body_wm, PLAN, ENC, run, dur, esc, W, H, DJ, DJB, RUSSO, LOGO, B, S
from PIL import ImageFont
VW = all_v.VW; TMP = f"{VW}/tmp"; VCLIPS = os.environ.get("VCLIPS", f"{VW}/clips")
for d in (TMP, f"{VW}/out", f"{VW}/web"): os.makedirs(d, exist_ok=True)
DIS = {"mk": ("Концепт изработен само за презентација на {c}.", "Не е објавен и нема да биде објавен", "без нивно изречно писмено одобрение.", "Видео изработено со вештачка интелигенција (LTX-2.5)"),
       "sr": ("Koncept izrađen samo za prezentaciju kompaniji {c}.", "Nije objavljen i neće biti objavljen", "bez njihovog izričitog pisanog odobrenja.", "Video je napravljen uz pomoć veštačke inteligencije (LTX-2.5)"),
       "sq": ("Koncept i përgatitur vetëm për prezantim te {c}.", "Nuk është publikuar dhe nuk do të publikohet", "pa miratimin e tyre të shprehur me shkrim.", "Video e krijuar me inteligjencë artificiale (LTX-2.5)")}
WM = {"mk": "КОНЦЕПТ · НЕ Е ЗА ОБЈАВА", "sr": "KONCEPT · NIJE ZA OBJAVU", "sq": "KONCEPT · JO PËR PUBLIKIM"}
TAG = {"mk": B["tagline_mk"], "sr": B["tagline_sr"], "sq": B["tagline_sq"]}
CALL = {"mk": "Закажете 15 минути:", "sr": "Zakažite 15 minuta:", "sq": "Caktoni 15 minuta:"}
MAXW = 960

def fit(text, font, size, maxw=MAXW, min_scale=0.62):
    """Lines and font size so the text fits the frame: same size if it fits, else two lines, else smaller."""
    def w(t, s): return ImageFont.truetype(font, s).getlength(t)
    if w(text, size) <= maxw: return [text], size
    words = text.split()
    if len(words) > 1:
        best = min(range(1, len(words)), key=lambda i: max(w(" ".join(words[:i]), size), w(" ".join(words[i:]), size)))
        lines = [" ".join(words[:best]), " ".join(words[best:])]
        s = size
        while s > size * min_scale and max(w(l, s) for l in lines) > maxw: s -= 2
        return lines, s
    s = size
    while s > 20 and w(text, s) > maxw: s -= 2
    return [text], s

def texts(font, text, size, color, y, gap=1.25):
    lines, s = fit(text, font, size)
    return [f"drawtext=fontfile={font}:text='{esc(l)}':fontsize={s}:fontcolor={color}:x=(w-tw)/2:y={int(y + i * s * gap)}" for i, l in enumerate(lines)], y + len(lines) * s * gap

def card(out, f, d=5.0):
    PLAN[out] = d; lang = f["lang"]; l1, l2, l3, ai = DIS[lang]; l1 = l1.format(c=f["company"] or "")
    inputs = ["-f", "lavfi", "-i", f"color=c=0x0d0d0f:s={W}x{H}:r=24:d={d}"]; vf = []
    if f["logo"]:   # the official logo, as on the 16:9 card
        inputs += ["-loop", "1", "-t", str(d), "-i", f["logo"]]; fc = f"[1:v]scale=w='min(760,iw*300/ih)':h=-1[l];[0:v][l]overlay=(W-w)/2:{int(H * .22)}[b];[b]"; y = int(H * .22) + 380
    else:
        fc = "[0:v]"; t, y = texts(DJB, f["title"], 84, "white", int(H * .30)); vf += t; y += 40
    t, _ = texts(DJ, f["tagline"], 52, "0xf2c14e", y); vf += t
    y = int(H * .62)
    for s_, c_ in ((l1, "0xbbbbbb"), (l2, "0xbbbbbb"), (l3, "0xbbbbbb")):
        t, y = texts(DJ, s_, 28, c_, y, 1.55); vf += t
    t, _ = texts(DJ, ai, 24, "0x888888", y + 22); vf += t
    vf.append("fade=t=in:st=0:d=0.5")
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc + ",".join(vf) + "[v]", "-map", "[v]", "-t", str(d)] + ENC + [out])

def outro(out, lang, d=3.2):
    y = int(H * .52); vf = []
    for text, font, size, col, gap in ((TAG[lang], RUSSO, 46, "white", 100), (CALL[lang], RUSSO, 34, "0xbbbbbb", 60), (B["email"], RUSSO, 40, "0xf2c14e", 70),
                                       ("bigdogma.tech", RUSSO, 32, "0x999999", 0)):
        t, y2 = texts(font, text, size, col, y); vf += t; y = max(y2, y + gap)
    fc = f"[1:v]scale=620:-1[l];[0:v][l]overlay=(W-w)/2:{int(H * .26)}," + ",".join(vf) + ",fade=t=in:st=0:d=0.4[v]"
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0d0d0f:s={W}x{H}:r=24:d={d}", "-loop", "1", "-t", str(d), "-i", LOGO,
         "-filter_complex", fc, "-map", "[v]", "-t", str(d)] + ENC + [out])

def wm(src, out, lang):
    import cut_v; cut_v.WM.update(WM); body_wm(src, out, lang)

def src16(cid, rule):
    for d in (("ltx610",) if rule == "cut" else ("ltx610", "ltx25")):
        p = f"{S}/{d}/{cid}.mp4"
        if os.path.exists(p): return p
    raise FileNotFoundError(cid)

def tmp16(name, f, i):   # the 16:9 cut's own rendered parts (cut/tmp), whose real lengths timed its crossfades
    pre = "zito_b2_" if name == "zito_opening_film" else (f"b2_{name}_" if f["rule"] == "cut2" else f"{name}_")
    return f"{S}/cut/tmp/{pre}{i}.mp4"

def plan(f, name=None):
    """Shot lengths exactly as the 16:9 cut timed them: the real length of its rendered part when it is still on disk, else its rule."""
    ds = []
    for i, (cid, vo) in enumerate(f["shots"]):
        t = tmp16(name, f, i) if name else None
        if t and os.path.exists(t): ds.append(dur(t)); continue
        vd = dur(vo) if vo else 0; d = max(dur(src16(cid, f["rule"])), vd + 0.9)
        if f["rule"] == "cut2" and f["trim"]: d = max(f["trim"], vd + 0.9) if vo else f["trim"]
        ds.append(d)
    return ds

def body_len(f, ds): return sum(ds) + 5.0 - f["xf"] * len(ds)
def vdur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def build(name, f):
    lang = f["lang"]; parts = []
    for i, ((cid, _), d) in enumerate(zip(f["shots"], plan(f, name))):
        p = f"{TMP}/{name}_{i}.mp4"; seg(f"{VCLIPS}/v_{cid}.mp4", d, p); parts.append(p)
    cp = f"{TMP}/{name}_card.mp4"; card(cp, f); parts.append(cp)
    j = f"{TMP}/{name}_join.mp4"; join(parts, j, f["xf"]); [os.remove(p) for p in parts]
    b = f"{TMP}/{name}_body.mp4"; wm(j, b, lang); os.remove(j)
    tail = dur(f"{S}/final_music/{name}.mp4") - dur(b)   # the 16:9 body's soundtrack runs past its last frame; the end card holds as long
    if tail > 0.02:
        bp = f"{TMP}/{name}_bodyp.mp4"; run(["ffmpeg", "-v", "error", "-y", "-i", b, "-vf", f"tpad=stop_mode=clone:stop_duration={tail:.3f}"] + ENC + [bp]); os.replace(bp, b)
    if not os.path.exists(f"{TMP}/intro.mp4"): intro(f"{TMP}/intro.mp4")
    o = f"{TMP}/outro_{lang}.mp4"
    if not os.path.exists(o): outro(o, lang)
    lst = f"{TMP}/{name}_list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in (f"{TMP}/intro.mp4", b, o)))
    pic = f"{TMP}/{name}_pic.mp4"; run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic]); os.remove(b)
    master = f"{S}/pitch/{name}_pitch.mp4"; out = f"{VW}/out/{name}_9x16_native.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", master, "-filter_complex", "[0:v]tpad=stop_mode=clone:stop_duration=0.3[v]", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", "-movflags", "+faststart", out])
    pd, md, od = dur(pic), dur(master), dur(out); os.remove(pic)
    web = f"{VW}/web/{name}_9x16.mp4"   # page copy, as for Foton
    run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "scale=720:-2", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", web])
    run(["ffmpeg", "-v", "error", "-y", "-ss", "4.5", "-i", web, "-frames:v", "1", "-q:v", "4", web[:-4] + ".jpg"])
    print(f"{name}: picture {pd:.2f} s | 16:9 master {md:.2f} s | out {od:.2f} s | web {os.path.getsize(web) // 1024} KB", flush=True)
    return abs(pd - md) < 0.35

if __name__ == "__main__":
    F = all_v.films(); cmd = sys.argv[1]; names = sys.argv[2:] or sorted(F)
    if cmd == "check":
        bad = 0
        for n in names:
            ds = plan(F[n], n); src = sum(os.path.exists(tmp16(n, F[n], i)) for i in range(len(ds))); want = vdur(f"{S}/final_music/{n}.mp4"); got = body_len(F[n], ds)
            ok = abs(got - want) < 0.09; bad += not ok
            print(f"{'OK ' if ok else 'OFF'} {n}: planned picture {got:.3f} s | 16:9 picture {want:.3f} s | {src}/{len(ds)} lengths from the 16:9 parts")
        print("CHECK", "all aligned" if not bad else f"{bad} off")
    elif cmd == "fake":
        os.makedirs(f"{VW}/fake", exist_ok=True)
        for cid in all_v.shot_ids(F):
            o = f"{VW}/fake/v_{cid}.mp4"
            if os.path.exists(o): continue
            rule = next(F[n]["rule"] for n in F if cid in [c for c, _ in F[n]["shots"]])
            run(["ffmpeg", "-v", "error", "-y", "-i", src16(cid, rule), "-an", "-vf", "crop=ih*9/16:ih,scale=704:1280", "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "30", o])
        print("fake clips", len(os.listdir(f"{VW}/fake")))
    elif cmd == "build":
        res = [build(n, F[n]) for n in names]; print("BUILD", sum(res), "of", len(res), "aligned with the master")
