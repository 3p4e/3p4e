# Foton showreel, Tunland only (owner, 2026-11-26: "remove all other trucks and pickups that are not Tunland"). Drops the four commercial-
# vehicle shots (Auman tractor, Aumark delivery truck, EME4 electric truck, cargo van) and their two voice-over lines; every other shot and
# line keeps its original take. Then the usual chain: music bed (music_mix.py) and pitch version (pitch_versions.py).
# The 16:9 films with the trucks are kept as *_with_trucks.mp4.
import os, sys, shutil, subprocess
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; NAME = "foton_showreel_v2"
DROP = ("foton_E1_", "foton_E2_", "foton_E3_", "foton_E4_")
def keep(cid): return not cid.startswith(DROP)

def shots():   # [(clip id, VO wav or None)] with the ORIGINAL line numbering (the takes are numbered by line in the full film)
    sys.path.insert(0, f"{S}/vo"); from batch2 import CUTS
    c = [c for c in CUTS if c[0] == NAME][0]; li = 0; out = []
    for cid, line in c[6]:
        vo = None
        if line: li += 1; vo = f"{S}/vo/trim/b2_{NAME}_{li}.wav"
        if keep(cid): out.append((cid, vo))
    return c, out

if __name__ == "__main__":
    for p in (f"{S}/final_commercials_b2/{NAME}.mp4", f"{S}/final_music/{NAME}.mp4", f"{S}/pitch/{NAME}_pitch.mp4"):
        b = p[:-4] + "_with_trucks.mp4"
        if os.path.exists(p) and not os.path.exists(b): shutil.copy(p, b)
    # cut2.py's helpers (seg2, card, join), without its main loop
    src = open(f"{S}/cut/cut2.py").read().split("\nonly = sys.argv")[0]; exec(src)
    c, sh = shots(); name, lang, voice, company, title, tagline = c[:6]; trim = c[8] if len(c) > 8 else None
    parts = []
    for i, (cid, vo) in enumerate(sh):
        p = f"tmp/b2_{name}_t{i}.mp4"; seg2(clip(cid), vo, p, trim); parts.append(p)
    cp = f"tmp/b2_{name}_card.mp4"; card(cp, lang, company, title, tagline, None); parts.append(cp)
    out = f"{OUT}/{name}.mp4"; join(parts, out, 0.35); print(name, len(sh), "shots", round(dur(out), 1), "s", flush=True)
    subprocess.run(["/usr/bin/python3", f"{S}/cut/music_mix.py", f"{S}/music/ace_final", name], check=True, cwd=f"{S}/cut")
    subprocess.run(["/usr/bin/python3", f"{S}/cut/pitch_versions.py", NAME], check=True, cwd=f"{S}/cut")
