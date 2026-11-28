# Telekom MK private page: builds the token folder exactly like the other company pages (same file names and encodes), so pitch_v3.py
# renders it with generic(): films (pitch versions) + native 9:16, 10 AI shots (x/cNN 872x480 + keyframe x/kNN), montage x/m.mp4,
# GIF teasers, hero loop, offer PDF, and a classic.html source (films, shot captions, the offer block shared with Žito: same bundles).
#   python3 page_tk.py build      -> /dev/shm/vall/tk/<token>/ (+ pv3/13_telekom_MK/{classic.html,files.txt})
#   python3 page_tk.py upload     -> token folder on the server (shared scripts/fonts copied from an existing page)
import os, sys, json, re, glob, shutil, secrets, string, subprocess, tarfile
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; D = f"{S}/telekom"; CID = "13_telekom_MK"
HERE = os.path.dirname(os.path.abspath(__file__)); g = {}; exec(open(f"{HERE}/tk.py", encoding="utf-8").read().split("def shots")[0], g)
FILMS = g["FILMS"]; TOKF = f"{S}/cut/page_tokens.json"; T = json.load(open(TOKF))
if CID not in T: T[CID] = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)); json.dump(T, open(TOKF, "w"), indent=1)
TOK = T[CID]; W = f"/dev/shm/vall/tk/{TOK}"; SRC = f"{S}/pv3/{CID}"
TITLES = {"telekom_magenta1": "Magenta 1 Unlimited: поврзани со она што е важно", "telekom_network": "Ја градиме мрежата на Македонија"}
CAPS = ["Изгрејсонце над Скопје од Кале, селфи со градот.", "Баба во Маврово, видеоповик со внуците.", "Пријатели на кејот во Охрид, гол на телефон.",
        "Цело семејство онлајн истовремено, оптика дома.", "Три генерации на балкон, Скопје ноќе.", "Техничар на столб над Охридското Езеро.",
        "Спојување оптички кабел во сервисното возило.", "Земјоделец во Струмица ја следи нивата од телефон.", "Видеопреглед со специјалист во селска амбуланта.",
        "Ноќна Македонија, поврзана со светлина."]
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
SHOTS = [f"{f['id']}_{i}" for f in FILMS for i in range(1, len(f["shots"]) + 1)]

def build():
    os.makedirs(f"{W}/x", exist_ok=True); os.makedirs(SRC, exist_ok=True); os.makedirs(f"{SRC}/out", exist_ok=True)
    for f in FILMS:   # films: the pitch versions (BD intro, concept mark, outro), poster from the middle of shot 3 (never a crossfade)
        n = f["id"]; m = f"{S}/pitch/{n}_pitch.mp4"; shutil.copy(m, f"{W}/{n}.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "14.0", "-i", m, "-frames:v", "1", "-vf", "scale=1280:720", "-q:v", "3", f"{W}/{n}.jpg"])
        for ext in ("mp4", "jpg"): shutil.copy(f"/dev/shm/vall/web/{n}_9x16.{ext}", f"{W}/{n}_9x16.{ext}")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "14.0", "-i", m, "-frames:v", "1", "-vf", "scale=1280:720", "-q:v", "3", f"{S}/previews/{n}_poster.jpg"])
    for k, sid in enumerate(SHOTS, 1):   # AI shots, as on the other pages: 872x480, no sound, poster + the keyframe it was made from
        c = f"{D}/clips/{sid}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", c, "-an", "-vf", "scale=872:480:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", f"{W}/x/c{k:02d}.mp4"])
        run(["ffmpeg", "-v", "error", "-y", "-ss", "2.5", "-i", c, "-frames:v", "1", "-vf", "scale=872:480", "-q:v", "4", f"{W}/x/c{k:02d}.jpg"])
        run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/kf/{sid}.png", "-vf", "scale=872:480", "-q:v", "3", f"{W}/x/k{k:02d}.jpg"])
    lst = f"{W}/mlist.txt"; parts = []   # montage: 0.9 s of every shot
    for k, sid in enumerate(SHOTS, 1):
        p = f"{W}/m{k}.mp4"; parts.append(p)
        run(["ffmpeg", "-v", "error", "-y", "-ss", "1.5", "-t", "0.9", "-i", f"{D}/clips/{sid}.mp4", "-an", "-vf", "scale=872:480,fps=24", "-c:v", "libx264", "-crf", "22", "-pix_fmt", "yuv420p", p])
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{W}/x/m.mp4"])
    [os.remove(p) for p in parts]; os.remove(lst)
    run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", f"{W}/x/m.mp4", "-frames:v", "1", "-q:v", "4", f"{W}/x/m.jpg"])
    hero = [f"{D}/clips/{s}.mp4" for s in ("telekom_magenta1_1", "telekom_network_1", "telekom_magenta1_3", "telekom_network_5")]   # hero loop, 8 s
    fc = "".join(f"[{i}:v]trim=0.6:2.6,setpts=PTS-STARTPTS,scale=1280:720,fps=24[v{i}];" for i in range(4)) + "".join(f"[v{i}]" for i in range(4)) + "concat=n=4:v=1[o]"
    run(["ffmpeg", "-v", "error", "-y"] + sum([["-i", h] for h in hero], []) + ["-filter_complex", fc, "-map", "[o]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "23",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{W}/hero.mp4"])
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", f"{W}/hero.mp4", "-frames:v", "1", "-q:v", "3", f"{W}/hero.jpg"])
    for i, f in enumerate(FILMS, 1):   # GIF teasers (6 s from a quarter in, 400 px, 10 fps), as posters_teasers.py
        m = f"{W}/{f['id']}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur(m) * .25:.2f}", "-t", "6", "-i", m, "-vf",
             "fps=10,scale=400:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4", f"{W}/x/t{i}.gif"])
    # classic.html: the source generic() reads (films, captions, offer); the offer block is Žito's (same two bundles: seasonal campaign, employer brand)
    z = open(f"{S}/pv3/01_zito_marketi_MK/classic.html", encoding="utf-8").read(); offer = re.search(r'<section id="offer".*?</section>', z, re.S).group(0)
    arts = "".join(f'<article class="film rv"><div class="vw"><video controls playsinline preload="none" poster="{f["id"]}.jpg" src="{f["id"]}.mp4"></video></div>'
                   f'<div class="meta"><h3>{TITLES[f["id"]]} ({round(dur(f"{W}/{f["id"]}.mp4"))} сек.)</h3></div></article>' for f in FILMS)
    figs = "".join(f'<figure class="tile rv"><video muted loop playsinline preload="none" poster="x/c{k:02d}.jpg" data-lz="x/c{k:02d}.mp4" aria-label="AI видео {k:02d}"></video>'
                   f'<div class="b"><i class="ai">AI</i><i>Кадар {k:02d}</i></div><figcaption><span>{CAPS[k - 1]}</span></figcaption></figure>' for k in range(1, len(SHOTS) + 1))
    html = (f'<!doctype html><html lang="mk"><head><meta charset="utf-8"><title>Македонски Телеком</title><style>:root{{--ac:#e20074}}</style></head><body>'
            f'<header><h1>Концепт-видео за <em>Македонски Телеком</em></h1></header><section id="films">{arts}</section><section id="shots">{figs}</section>{offer}</body></html>')
    open(f"{SRC}/classic.html", "w", encoding="utf-8").write(html); shutil.copy(f"{SRC}/classic.html", f"{W}/classic.html")
    files = sorted(os.path.relpath(p, W).replace("x/", "") for p in glob.glob(f"{W}/**/*", recursive=True) if os.path.isfile(p))
    open(f"{SRC}/files.txt", "w").write(" ".join(files)); print("built", TOK, len(files), "files", sum(os.path.getsize(p) for p in glob.glob(f"{W}/**/*", recursive=True) if os.path.isfile(p)) // 1048576, "MB")

def upload():
    shutil.copy(f"{S}/offers_pdf/{CID}_offer.pdf", f"{W}/offer.pdf")
    tp = f"/dev/shm/vall/tk_{TOK}.tar"
    with tarfile.open(tp, "w") as t: t.add(W, arcname=".")
    for _ in range(3):
        if "CHECKSUM MATCH" in subprocess.run(["python3", "rput_par.py", tp, "/opt/stacks/_upload", f"tk_{TOK}.tar"], cwd=S, capture_output=True, text=True).stdout: break
    else: raise SystemExit("upload failed")
    zt = T["01_zito_marketi_MK"]; site = "/opt/stacks/ai-studio-pitch/site"
    out = subprocess.run(["python3", "rsh.py", f"cat /opt/stacks/_upload/tk_{TOK}.tar | /opt/bigdogma_vps/bd.sh 'set -e; mkdir -p {site}/{TOK}; cd {site}/{TOK}; tar xf -; "
                          f"for f in dogma_logo.js fx.css fx.js icon.png logo.png mark.js russo.ttf logo_loop.mp4; do cp -p {site}/{zt}/$f . ; done; chmod -R a+rX . ; ls | wc -l; echo PLACED'; "
                          f"rm -f /opt/stacks/_upload/tk_{TOK}.tar", "600"], cwd=S, capture_output=True, text=True).stdout
    assert "PLACED" in out, out[-400:]; os.remove(tp); print("uploaded", TOK)

if __name__ == "__main__": {"build": build, "upload": upload}[sys.argv[1]]()
