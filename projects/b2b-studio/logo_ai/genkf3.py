# Keyframes for header effects round 2 (FX2, kf_fx2/) and logo films round 3 (S3, kf/), Gemini 3 Pro Image, approved mark as reference.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fx_scenes2 import FX2
from fx_scenes import BG
from scenes3 import S3
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
REF = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; os.makedirs(f"{S}/logo_ai/kf_fx2", exist_ok=True)
STY = " Photorealistic cinematic still, 16:9, premium commercial lighting, no text, no words, no watermark, no other logos."
todo = [(f"{S}/logo_ai/kf_fx2/{i}.png", p + BG + " Photorealistic, 16:9, no watermark.") for i, p, _ in FX2]
for sid, cap, a, b, mo in S3:
    todo.append((f"{S}/logo_ai/kf/{sid}_a.png", a + STY))
    if b: todo.append((f"{S}/logo_ai/kf/{sid}_b.png", b + STY))
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(4) as ex: list(ex.map(lambda t: os.path.exists(t[0]) or gem(t[0], t[1], [REF]), todo))
print("KF_DONE", sum(os.path.exists(t[0]) for t in todo), "/", len(todo))
