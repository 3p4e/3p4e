# Music beds (LTX road)

- **Chosen model:** ACE-Step 1.5 (MIT licence; output owned outright), turbo DiT + 5Hz LM planner, on a rented RTX A4000 (~$0.10 per session).
- **Prompts v2 (`moods2.py`):** ACE-style captions (genre, exact instruments, mood, scene) plus fixed BPM, key and 4/4. LM caption/metadata rewriting is off (`use_cot_caption/metas=false`) so the mood cannot drift. `[Instrumental]` as lyrics. 70 s.
- **Selection:** 3 seeds per mood; Gemini scores mood match and quality (`pick_best.py`); best take kept. All 8 winners scored 9–10 for mood match, with no vocals or issues.
- **Mix (`cut/music_mix.py`):** music at about −16 dB (volume 0.16) under the VO, sidechain-ducked by the VO, 0.8 s fade-in, 2.5 s fade-out, −16 LUFS. Mood per film is in `MAP`.
- **Box notes:** use a CUDA ≥ 12.8 driver; the small `nvidia/cuda:12.8.1-cudnn-runtime` image (pulls in about a minute); install ffmpeg, or MP3 export fails silently (we use WAV).
- **Alternative tested:** Gemini Lyria 3.5 (`lyria_gen.py`, paid Gemini key), also 9/10. Kept as a fallback.
