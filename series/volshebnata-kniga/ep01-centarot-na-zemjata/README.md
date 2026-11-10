# Волшебната книга — Ep01 „Патување во центарот на Земјата“

Production files for episode 1 (2D storybook cartoon, ages 3–6, Macedonian narration).

| Folder | Contents |
|---|---|
| `Ep01_Centarot_na_Zemjata_scenario.md` | Approved script with timings |
| `voice/` | Two-voice narration pipeline (Gemini TTS: narrator Leda, professor Gacrux) + recorded parts seg01–13 |
| `images/` | 30 storybook scene prompts (generated on Higgsfield, GPT Image 2.5; reference sheet job `46a88189-1b1d-4f90-ad8a-caf7afc661bd`) |
| `animation/` | 35 Seedance 2.0 Mini clip prompts (`plan.json`, `image` = Higgsfield image job id), clip job ids (`jobs.json`, key = plan index), and `build.py` which lays the clips on the narration timeline |

Rebuild: record remaining narration (`voice/gen_voice.py`, `voice/assemble.py`), download clips by job id, then
`python3 animation/build.py voice/timeline.json voice/Ep01_narration_full.mp3 Ep01.mp4`.
