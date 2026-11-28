# End-to-end build of the ten lead pages, one company at a time (resumable: finished keys are listed in the scratchpad leads10/done.txt).
# Per company: restore its 6 clips from the India backup, cut 2 films (cut_leads.py), append the logo outro, build page + email (build_pages.py),
# offer PDF, hero loop, publish the token folder on the India pitch site, verify, clean up /dev/shm.   python3 run_all.py [key ...]
import os, sys, json, subprocess, shutil
R = "/home/user/3p4e/projects/b2b-studio"; S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; W = "/dev/shm/vall/ld"
CFG = json.load(open(f"{S}/leads10/cfg.json", encoding="utf-8")); DONE = f"{S}/leads10/done.txt"
SEG = f"{S}/launch/video/_work/seg"
def run(c, **kw): return subprocess.run(c, check=True, **kw)
def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True)
done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
keys = sys.argv[1:] or [c["key"] for c in CFG["companies"]]
for k in keys:
    if k in done: print("skip", k, flush=True); continue
    print("==", k, flush=True)
    for d in ("clips", "films", "final"): shutil.rmtree(f"{W}/{d}", ignore_errors=True); os.makedirs(f"{W}/{d}")
    names = ",".join(f"l_{k}_{i}.mp4" for i in range(1, 7))
    run(["python3", f"{S}/leads10/ipull.py", "/opt/bd_work/leads10/clips", f"{W}/clips", names])
    run(["/usr/bin/python3", f"{R}/leads10/cut_leads.py", f"{W}/clips", f"{W}/films"], env=dict(os.environ, ONLY=k))
    for x in "ab": run(["bash", f"{R}/launch/video/_work/add_sting.sh", f"{W}/films/l_{k}_{x}_16x9.mp4", f"{W}/final/l_{k}_{x}_16x9.mp4", f"{SEG}/outro_16x9.mp4", f"{SEG}/outro_9x16.mp4"])
    run(["/usr/bin/python3", f"{R}/leads10/build_pages.py", k], env=dict(os.environ, PITCH_FIN=f"{W}/final"))
    tok = json.load(open(f"{S}/cut/page_tokens_new.json"))[k]; pub = f"/dev/shm/pub/{tok}"
    run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-t", "8", "-i", f"{pub}/{k}_film_a.mp4", "-an", "-vf", "scale=1280:-2", "-c:v", "libx264", "-crf", "27", "-preset", "medium", "-movflags", "+faststart", f"{pub}/hero.mp4"])
    run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", f"{pub}/{k}_film_a.mp4", "-frames:v", "1", "-vf", "scale=1280:-2", f"{pub}/hero.jpg"])
    tar = f"/dev/shm/pub_{k}.tar"; run(["tar", "cf", tar, "-C", "/dev/shm/pub", tok])
    run(["python3", f"{S}/rput_par.py", tar, "/opt/stacks/_upload", f"pub_{k}.tar"], cwd=S, capture_output=True)
    run(["python3", f"{S}/rsh.py", f"cat /opt/stacks/_upload/pub_{k}.tar | /opt/bigdogma_vps/bd.sh 'cd /opt/stacks/ai-studio-pitch/site && tar xf - && cp mh40CJuLNCeMzLTm/icon.png mh40CJuLNCeMzLTm/russo.ttf {tok}/ && chmod -R a+rX {tok}'; rm -f /opt/stacks/_upload/pub_{k}.tar", "280"], cwd=S, capture_output=True)
    code = sh(f"curl -s -o /dev/null -w '%{{http_code}}' https://pitch.bigdogma.tech/{tok}/").stdout
    print(k, "page", code, flush=True)
    if code == "200":
        open(DONE, "a").write(k + "\n")
        for p in (pub, tar): shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)
print("ALL_DONE", flush=True)
