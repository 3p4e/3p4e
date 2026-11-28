# Keyframes for the AI logo films: Gemini 3 Pro Image with the approved mark as reference; 1280x704 (LTX size).
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scenes import S as SC
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
REF = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; OUT = f"{S}/logo_ai/kf"; os.makedirs(OUT, exist_ok=True)
STY = " Photorealistic cinematic still, 16:9, premium commercial lighting, no text, no words, no watermark, no other logos."
todo = []
for sid, cap, a, b, mo in SC:
    todo.append((f"{OUT}/{sid}_a.png", a + STY))
    if b: todo.append((f"{OUT}/{sid}_b.png", b + STY))
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(5) as ex: list(ex.map(lambda t: gem(t[0], t[1], [REF]), todo))
print("KF_DONE", len(todo))
