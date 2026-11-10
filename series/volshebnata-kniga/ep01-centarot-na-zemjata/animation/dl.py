import json, sys, subprocess
plan = json.load(open("plan.json"))
for pair in sys.argv[1:]:
    i, url = pair.split("=", 1)
    fn = f"clip_{plan[int(i)]['clip']}.mp4"
    subprocess.run(["curl", "-sS", "-o", fn, url], check=True)
    print(fn)
