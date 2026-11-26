# Puts the native 9:16 films on the company pages: web copy + poster into each page's token folder (the old blur-fill *_9x16.mp4 there is
# backed up first), full-quality masters into a private server folder, and the film ids into native_v.json (pitch_v3.py shows the 9:16
# button only for films listed there). Then run loud/pub_pitch.sh.
#   python3 upload_v.py [film...]     (default: every film with a web copy in $VW/web)
import os, sys, json, subprocess, tarfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import all_v
S = all_v.S; VW = all_v.VW; MAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "native_v.json")
TOK = json.load(open(f"{S}/cut/page_tokens.json")); SITE = "/opt/stacks/ai-studio-pitch/site"
def sh(cmd, t=600): return subprocess.run(["python3", "rsh.py", cmd, str(t)], cwd=S, capture_output=True, text=True).stdout
def put(local, name):
    for _ in range(3):
        if "CHECKSUM MATCH" in subprocess.run(["python3", "rput_par.py", local, "/opt/stacks/_upload", name], cwd=S, capture_output=True, text=True).stdout: return
    raise RuntimeError("upload failed " + name)

films = sys.argv[1:] or sorted(f[:-9] for f in os.listdir(f"{VW}/web") if f.endswith("_9x16.mp4"))
done = json.load(open(MAN)) if os.path.exists(MAN) else []
for co, fs in all_v.PAGES.items():
    mine = [f for f in fs if f in films and os.path.exists(f"{VW}/web/{f}_9x16.mp4")]
    if not mine: continue
    tok = TOK[co]; tp = f"/dev/shm/up_{tok}.tar"
    with tarfile.open(tp, "w") as t:
        for f in mine:
            for ext in ("mp4", "jpg"): t.add(f"{VW}/web/{f}_9x16.{ext}", arcname=f"{f}_9x16.{ext}")
    put(tp, f"v_{tok}.tar"); os.remove(tp)
    out = sh(f"cat /opt/stacks/_upload/v_{tok}.tar | /opt/bigdogma_vps/bd.sh 'set -e; cd {SITE}/{tok}; mkdir -p /opt/stacks/ai-studio-pitch/backup/blur_9x16/{tok}; "
             f"for f in {' '.join(m + '_9x16.mp4' for m in mine)}; do [ -f $f ] && [ ! -f /opt/stacks/ai-studio-pitch/backup/blur_9x16/{tok}/$f ] && cp -p $f /opt/stacks/ai-studio-pitch/backup/blur_9x16/{tok}/; done; "
             f"tar xf - && chmod a+r *_9x16.* && echo PLACED'; rm -f /opt/stacks/_upload/v_{tok}.tar")
    assert "PLACED" in out, out[-300:]
    done += [f for f in mine if f not in done]; print("page", co, mine, flush=True)
json.dump(sorted(done), open(MAN, "w"), indent=1)
# full-quality masters, private (not under the web root)
nat = [f for f in films if os.path.exists(f"{VW}/out/{f}_9x16_native.mp4")]
if nat:
    tp = "/dev/shm/up_masters.tar"
    with tarfile.open(tp, "w") as t:
        for f in nat: t.add(f"{VW}/out/{f}_9x16_native.mp4", arcname=f"{f}_9x16_native.mp4")
    put(tp, "v_masters.tar"); os.remove(tp)
    print(sh("cat /opt/stacks/_upload/v_masters.tar | /opt/bigdogma_vps/bd.sh 'mkdir -p /opt/bd_masters/vertical && cd /opt/bd_masters/vertical && tar xf - && ls | wc -l'; "
             "rm -f /opt/stacks/_upload/v_masters.tar").strip().splitlines()[-1], "masters on the server")
print("UPLOAD_DONE", len(done), "films listed in native_v.json")
