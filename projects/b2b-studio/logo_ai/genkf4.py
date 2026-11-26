# Keyframes for logo films round 4 (energy blades) + the cathedral window take 3, Gemini 3 Pro Image, approved mark as reference.
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scenes4 import S4
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
REF = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; OUT = f"{S}/logo_ai/kf"
STY = " Photorealistic cinematic still, 16:9, premium lighting, no text, no letters, no symbols, no watermark."
for sid, cap, a, b, mo in S4:
    if not os.path.exists(f"{OUT}/{sid}_a.png"): gem(f"{OUT}/{sid}_a.png", a + STY, [REF])
    if not os.path.exists(f"{OUT}/{sid}_b.png"): gem(f"{OUT}/{sid}_b.png", b + STY, [REF])
subprocess.run(["/usr/bin/python3", f"{HERE}/genkf_window2.py"])
print("KF4_DONE", sum(os.path.exists(f"{OUT}/{s[0]}_{k}.png") for s in S4 for k in "ab"), "/", 2 * len(S4))
