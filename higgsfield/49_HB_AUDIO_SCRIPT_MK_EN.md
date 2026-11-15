# 49 — Hollow Bloom bilingual audio script (MK + EN) + two-track delivery recipe
2026-11-15 · zero-GPU prep. Fills the EN half of spec §5's 7 MK lines so the K6 batch
can generate BOTH language stems, and records the selectable-track container recipe (48).

## 1. Lines (generation grammar per 47_AUDIO_STACK_PLAN: `**SNN** SPEAKER: „MK" / "EN"`)

| # | Shot | Speaker | MK (canon, spec §5) | EN (delivery translation) |
|---|---|---|---|---|
| D1 | after #07 | Bloom (spore-voice, subtitle) | „Дојдовте да расцветате во мене, како сите што дојдоа пред вас.“ | "You came to bloom within me, like all who came before you." |
| D2 | after #19 | Bloom | „Мразот само го успорува гнилежот.“ | "Frost only slows the rot." |
| D3 | #26 | Paladin (under breath) | „Светлината не се гаси.“ | "The light does not go out." |
| D4 | #36 | Bloom | „Од трева сте — и во трева ќе ве вратам!" | "From grass you are — and to grass I will return you!" |
| D5 | #44 | DD | „Замрзни.“ | "Freeze." |
| D6 | #45 | Paladin | „Суди.“ | "Judge." |
| D7 | #49 | DD (epilogue, whispered) | „И во најтоплото мочуриште, зимата наоѓа пат.“ | "And even in the warmest marsh, winter finds a way." |

Length budget (47): callouts ≤14 EN words, narration ≤~16 EN words — all 7 pass.
TTS: ElevenLabs `eleven_multilingual_v2` (MK+EN one model, verified #13/#23) or MOSS-TTS for MK;
per-shot 48 kHz PCM16 mono WAV stems. D5/D6 are hard-synced to #44/#45 in both languages.

## 2. Selectable language tracks — the container recipe (from 48_BILINGUAL_DELIVERY_SPEC)

One MP4, TWO audio streams; SFX + ambience shared, TTS stem swapped per track:

```
ffmpeg -i picture_lock.mp4 -i narration_mk.wav -i narration_en.wav \
  -i sfx.wav -i ambience_music.wav \
  -filter_complex "[1:a][3:a][4:a]amix=inputs=3[a_mk];[2:a][3:a][4:a]amix=inputs=3[a_en]" \
  -map 0:v -map "[a_mk]" -map "[a_en]" \
  -c:v copy -c:a aac -b:a 192k \
  -metadata:s:a:0 language=mkd -metadata:s:a:0 title="Macedonian" \
  -metadata:s:a:1 language=eng -metadata:s:a:1 title="English" \
  -disposition:a:0 default \
  hollow_bloom_final.mp4
```

Result: VLC / browser / QuickTime show a **track selector (Macedonian / English)** —
standard MP4 multi-audio, no player hacks. Rule carried from spec §6: in EACH mix the
score never masks voice or SFX; duck −12 dB under dialogue.

Stems to produce per clip: tts_mk/SNN.wav, tts_en/SNN.wav (only the 7 line-shots),
sfx/SNN.wav (spec §6 map), ambience+music per phase (P1/P2/P3 beds). The mixer
(tools/mix_23_k6_audio.py pattern) amixes per language; the assembler maps the two
finished mixes as streams 1 and 2.
