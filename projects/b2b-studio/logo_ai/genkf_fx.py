# Keyframes for the header-logo effect clips (Gemini 3 Pro Image, approved mark as reference, pure black background).
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fx_scenes import FX, BG
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
REF = "/home/user/3p4e/projects/b2b-studio/brand/mark_bd_M2_P3.png"; OUT = f"{S}/logo_ai/kf_fx"; os.makedirs(OUT, exist_ok=True)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(5) as ex: list(ex.map(lambda f: gem(f"{OUT}/{f[0]}.png", f[1] + BG + " Photorealistic, 16:9, no watermark.", [REF]), FX))
print("KF_DONE", len(FX))
