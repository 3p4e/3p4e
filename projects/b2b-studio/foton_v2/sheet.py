# contact sheet per film of the start keyframes (QC): sheet.py <film_id> [...]
import sys, os, glob
from PIL import Image, ImageDraw
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
for fid in sys.argv[1:]:
    fs = sorted(glob.glob(f"{S}/fv2/kf/{fid}_s*.png")); W, H = 640, 352; cols = 3; rows = (len(fs) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, H * rows), "black"); d = ImageDraw.Draw(sh)
    for i, f in enumerate(fs):
        im = Image.open(f).convert("RGB").resize((W, H)); sh.paste(im, ((i % cols) * W, (i // cols) * H))
        d.rectangle([(i % cols) * W, (i // cols) * H, (i % cols) * W + 120, (i // cols) * H + 26], fill="black"); d.text(((i % cols) * W + 6, (i // cols) * H + 6), os.path.basename(f)[:-4].split("_")[-1], fill="white")
    sh.save(f"{S}/fv2/sheets/{fid}.jpg", quality=78); print("sheet", fid, len(fs))
