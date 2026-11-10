# Record only the missing parts with gemini-2.5-flash-preview-tts (3.8 daily quota exhausted).
import os, json
import tts
from script import SEGMENTS
tts.MODELS = ["gemini-2.5-flash-preview-tts"]
tts.PREFIX = {
    "narrator": "Say softly and warmly, like a gentle young woman telling a story to small children, in Macedonian:\n\n",
    "professor": "Say in Macedonian, as an excited, warm, slightly funny old professor:\n\n",
}
VOICES = {"narrator": "Leda", "professor": "Gacrux"}
log = []
for s, parts in SEGMENTS:
    for i, (role, text) in enumerate(parts):
        fn = f"parts/seg{s}_{i}_{role}.mp3"
        if os.path.exists(fn):
            continue
        try:
            score, model, heard = tts.take(fn, text, VOICES[role], role, tries=2)
            d = os.path.getsize(fn) * 8 / 128000
            print(s, i, role, round(score, 2), f"{d:.1f}s/{len(text.split())}w", heard[:60], flush=True)
            log.append({"seg": s, "i": i, "role": role, "model": model, "match": score})
        except Exception as e:
            print(s, i, role, "FAILED", str(e)[:120], flush=True)
json.dump(log, open("fill_log.json", "w"), ensure_ascii=False, indent=1)
