# Telekom MK films, cut exactly like the other company films so they share one look:
#   python3 cut_tk.py 169   -> final_commercials/telekom_*.mp4 (cut.py: shot = max(clip, line + 0.9), 0.4 s crossfades, 5 s end card)
#   python3 ../cut/music_mix.py <scratch>/music/ace_final telekom_magenta1 telekom_network      -> final_music/ (music bed)
#   python3 ../cut/pitch_versions.py telekom_magenta1 telekom_network                           -> pitch/ (BD intro, concept mark, outro)
#   python3 cut_tk.py v     -> native 9:16 (vertical/cut_v_all.py) from the vertical LTX shots
# Clips: <scratch>/telekom/clips/<id>.mp4 (16:9) and v_<id>.mp4 (9:16). Voice-over: <scratch>/vo/trim/<film>_<n>.wav (vo/gen_vo_tk.py).
import os, sys
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; D = f"{S}/telekom"; CL = f"{D}/clips"; HERE = os.path.dirname(os.path.abspath(__file__))
g = {}; exec(open(f"{HERE}/tk.py", encoding="utf-8").read().split("def shots")[0], g); FILMS = g["FILMS"]
COMPANY = "Македонски Телеком"

def spec(f):
    return dict(lang="mk", company=COMPANY, title=f["title"], tagline=f["tagline"], logo=None, xf=0.4, rule="cut", trim=None,
                shots=[(f"{f['id']}_{i}", f"{S}/vo/trim/{f['id']}_{i}.wav") for i in range(1, len(f["shots"]) + 1)])

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "169":
        exec(open(f"{S}/cut/cut.py").read().split("\nCOMM =")[0])   # seg / card / join / build of the other company films
        for f in FILMS:
            sp = spec(f); miss = [p for c, v in sp["shots"] for p in (f"{CL}/{c}.mp4", v) if not os.path.exists(p)]
            if miss: print("SKIP", f["id"], "missing", miss); continue
            build(f["id"], "mk", COMPANY, f["title"], [(f"{CL}/{c}.mp4", v) for c, v in sp["shots"]], f["tagline"])
    elif cmd == "v":
        os.environ.setdefault("VCLIPS", CL); sys.path.insert(0, os.path.join(HERE, "..", "vertical"))
        import cut_v_all
        for f in FILMS: cut_v_all.build(f["id"], spec(f))
