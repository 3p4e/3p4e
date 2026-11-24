import sys, os; sys.path.insert(0, "../vincinni"); os.chdir(os.path.dirname(os.path.abspath(__file__)))
from gemlib import gem
from shots import SHOTS
SFX = " Photorealistic high-energy automotive commercial still, 16:9, cinematic, no text, no logos other than on the vehicle, no watermark. The pickup must match the supplied reference vehicle exactly (Foton Tunland V9: grille, headlights, body, wheels, red paint)."
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(4) as ex:
    list(ex.map(lambda s: gem(f"kf/{s[0]}.png", s[1] + SFX, ["../foton/ref/v9.png"]), SHOTS))
print("KF_DONE")
