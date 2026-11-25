# Asks Gemini 3 Pro Image to draw the BIG DOGMA "BD" mark exactly as the owner briefed it, with the tattoo photo and the extracted D
# as references. Writes N variants (PNG) + nothing else. The API key is read from the scratchpad file, never printed.
#   python3 gemini_logo.py <out_dir> [n=6]
import sys, os, json, base64, io, urllib.request, time
from concurrent.futures import ThreadPoolExecutor
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"; KEY = open(f"{S}/.gemini_paid").read().strip()
OUT = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 6; os.makedirs(OUT, exist_ok=True)
BRIEF = """Design a logo mark: the monogram "BD" for the studio BIG DOGMA, drawn as hand-made tattoo ink, black on a pure white background.

THE D: use the triangle tattoo from the reference photo (and its black-and-white extraction) as the letter D, exactly as it is: one big triangle pointing to the right like a play button, its left side vertical. Each side is a bundle of 2 to 4 roughly straight, slightly shaky hand-tattooed ink lines that run past the corners and cross each other there; short extra strokes beside the left side; ink pooling into small dark blobs where lines cross or nearly touch. Keep its line style, thickness and character exactly.

THE B: to the left of the D, draw two triangles of exactly the same size stacked one above the other, both pointing right with their left sides vertical and aligned, so together they read as the letter B. Draw them by the same hand and in exactly the same tattoo style as the D: bundles of 2 to 4 roughly straight, slightly shaky ink lines per side that overshoot and cross at the corners, the same line thickness as the D, ink pooling at the crossings. The two B triangles together are as tall as the D.

SPACING: nothing touches. The gap between the B and the D, and between the two B triangles, is the same as the gap between two neighbouring lines inside a bundle.

FORMAT: flat solid black ink only, no grey, no shading, no skin texture, no paper texture, no colour, no text, no letters, no frame, no watermark. Centered, generous white margin, the whole mark visible. It must look like a clean scan of a real tattoo design, ready to be vectorised."""
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
REFS = [("image/jpeg", f"{S}/glogo/ref_tattoo.jpg"), ("image/png", f"{S}/glogo/ref_D.png")]
def one(k):
    out = f"{OUT}/gem_bd_{k}.png"
    if os.path.exists(out): return
    body = {"contents": [{"parts": [{"text": BRIEF + f"\n\nVariant {k}: draw your own hand for the B triangles (different stroke placement from other variants)."}]
                          + [{"inline_data": {"mime_type": m, "data": b64(p)}} for m, p in REFS]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "4:3"}}}
    for a in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={KEY}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=300).read())
            d = [p for p in r["candidates"][0]["content"]["parts"] if "inlineData" in p][0]
            open(out, "wb").write(base64.b64decode(d["inlineData"]["data"])); print("ok", k, flush=True); return
        except Exception as e: print("retry", k, str(e)[:120], flush=True); time.sleep(10)
with ThreadPoolExecutor(3) as ex: list(ex.map(one, range(1, N + 1)))
print("GEMINI_LOGO_DONE")
