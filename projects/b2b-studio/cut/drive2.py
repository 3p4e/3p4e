# cut each batch-2 film as soon as all its voice lines exist; stop when VO generation is done and everything is cut
import os, sys, time, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
sys.path.insert(0, f"{S}/vo"); from batch2 import CUTS
while True:
    vo_done = "VO4_DONE" in open(f"{S}/vo/gen4.log").read()
    pending = []
    for c in CUTS:
        name = c[0]; n = sum(1 for _, l in c[6] if l)
        if os.path.exists(f"{S}/final_commercials_b2/{name}.mp4"): continue
        if all(os.path.exists(f"{S}/vo/trim/b2_{name}_{i}.wav") for i in range(1, n+1)) or vo_done:
            subprocess.run(["/usr/bin/python3", "cut2.py", name])
        else: pending.append(name)
    if not pending and vo_done: print("DRIVE_DONE", flush=True); break
    time.sleep(60)
