# #23 Perseus & Medusa — AUDIO MIX SPEC v4 (K6 native-audio master)

> v4 2026-11-15: revised for the Kandinsky-6 render. Every K6 clip ships a
> NATIVE AAC 44.1kHz stereo ambient bed (~5.05s @ 121f/24fps). The mix is
> therefore 3 layers, NOT a from-scratch build.

## Layer model
| # | Layer | Source | Treatment |
|---|---|---|---|
| 1 | Ambient bed | K6 native per-clip audio | keep; high-pass 80Hz; duck −14dB under narration via sidechain; keep fully audible in gaps |
| 2 | Narration/dialogue | MOSS-TTS (Apache-2.0, native MK) or ElevenLabs multilingual_v2 (film-grade) | per-line from `23_AUDIO_SCRIPT_MK_EN_v3_65clips.md`; cast per the v3 table; −3dB true-peak ceiling; align to each clip's 5.05s window |
| 3 | SFX + score accents | ffmpeg/sox/fluidsynth | harpe rings (F07), petrification cracks (S14/S54), ketos roar (S49–S52), wings (S33/S44), Stone Dirge motif under Act III |

## Per-clip assembly (65 clips, picture-lock order)
1. For clip i in [S01..S20, F01..F10, S26..S60]: take `p23_<tag>_k6.mp4`.
2. Extract/normalize native bed to 48kHz stereo −20 LUFS working track.
3. Lay narration line i (MK then EN pass, or dual-mix) at clip start +0.2s.
4. Sidechain-duck bed by narration RMS (ratio 4:1, threshold −30dB).
5. Add SFX accents at beat timestamps; score swells at act boundaries (S20, F10, S60).
6. Emit `audio/final/<tag>.m4a` + mux back → `clips_final/<tag>.mp4`.

## Master
- Concat 65 muxed clips (ffmpeg concat demuxer, re-encode audio only, copy video).
- Final loudness: −16 LUFS integrated (streaming target), true peak −1.5dBTP.
- Export `p23_master_k6_audio.mov` + review MP4.

## Gates before release
- Per-clip: narration present, bed ducked not muted, no clipping, MK intelligible.
- Master: loudness −16±1 LUFS; no seam pops at the 64 joins (run scan_join_glitches.py).

## Spend gate
- MOSS-TTS route: GPU-free (CPU) once OpenMontage image is up; zero external cost.
- ElevenLabs route: paid, needs a named character count + credit cap before firing.
