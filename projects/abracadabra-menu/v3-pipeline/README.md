# v3 clips (LTX-2.5 22B, start+end keyframes)

Per menu item: a wand-cast clip (768x1024, 193 f) and a summon clip (1280x704, 169 f), 24 fps.
Same method as the original Higgsfield cinematics: the wand is in both the first and last frame
(`LTXVBaseSampler` with `optional_cond_images` + indices `0,<frames-1>`, strength 0.8), so it stays on-model.

- `jobs.json` - 126 jobs (prompt, keyframes, size, frames)
- `oai_kf.py` / `compose_kf.py` - keyframes (OpenAI image edits; Pillow fallback)
- `setup.sh` / `batch.py` - ComfyUI + LTX setup and batch runner on a rented GPU
- `post_v3.sh` - raw -> H.264 MP4 + VP9 WebM
- `assets/clip-map-v3.js` maps `category::item` -> clip names; `cinematic-board.html` uses it.
Clips are deployment artifacts and are not committed.
