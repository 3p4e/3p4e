# Cathedral window take 3, final: the composite (exact fully-glazed BD silhouette pasted into the cathedral wall, window_layout.py) is
# re-rendered photoreal by Gemini, keeping the window's exact outline, the filled D, and the thick black tattoo lead lines.
import sys, os
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; K = f"{S}/logo_ai/kf_window"
os.chdir(f"{S}/vincinni"); sys.path.insert(0, f"{S}/vincinni"); from gemlib import gem
KEEP = ("Re-render this image as a photorealistic photograph. Keep the composition, the camera and the cathedral exactly. Keep the stained-glass "
        "window exactly as drawn: the same outline, every triangle (both B triangles and the big D triangle) completely filled with stained glass "
        "edge to edge, and the thick black hand-drawn lines crossing it exactly where they are, as heavy black lead cames. Turn the flat coloured "
        "pieces into real translucent antique stained glass with texture and thin lead between the pieces, set into the carved stone wall.")
gem(f"{K}/w5_a.png", KEEP + " Dawn: the glass is dim with a faint inner glow, the cathedral dark and blue. Photorealistic, 16:9, no text.", [f"{K}/w5_layout_a.png"])
gem(f"{K}/w5_b.png", KEEP + " Sunrise: brilliant sunlight blazes through the whole window, every glass piece glowing intensely, the black lead lines crisp, "
    "beams of red, gold, blue and green light streaming through the incense haze into the nave. Photorealistic, 16:9, no text.", [f"{K}/w5_layout_b.png"])
print("ok")
