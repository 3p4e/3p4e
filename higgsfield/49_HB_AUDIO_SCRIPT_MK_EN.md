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

## 2. Selectable language tracks — container recipe (ALIGNED with the Perseus #23 dual-track pipeline)

Same architecture as #23: ONE container, TWO tagged audio streams, MK default + EN one click away.
Master container = **MKV** (most robust multi-audio across VLC/mpv/QuickTime; MP4 multi-audio is
finicky in QuickTime/mobile browsers). Deliver the MKV as master + an MP4 twin if a player needs it.

Pattern: mix ONE master WAV per language first (full film length, A/V-synced to the picture lock,
−16 LUFS, beds ducked −12 dB under voice), then map both masters:

```
ffmpeg -i picture_lock.mp4 \
       -i mk_master.wav -i en_master.wav \
       -map 0:v:0 -map 1:a:0 -map 2:a:0 \
       -c:v copy -c:a aac -b:a 192k \
       -metadata:s:a:0 language=mkd -metadata:s:a:0 title="Македонски" \
       -metadata:s:a:1 language=eng -metadata:s:a:1 title="English" \
       -disposition:a:0 default \
       hollow_bloom_DUAL.mkv
# optional twin: -map 0:v:0 -map 1:a -map 2:a ... hollow_bloom_DUAL.mp4
```

Result: player shows **Audio → Македонски / English**. No re-render, no duplicated video.
Voice/SFX/ambience stems: tts_mk + tts_en (7 line-shots each), sfx per spec §6 map, P1/P2/P3
music beds — one mixer pass per language (tools/mix_23_k6_audio.py pattern), both masters −16 LUFS.
TTS stack note: #23 uses edge-TTS for EN; Hollow Bloom keeps ElevenLabs eleven_multilingual_v2
(verified MK+EN) or MOSS-TTS for MK — engine variance is fine, MK line quality gets a render-day check.
