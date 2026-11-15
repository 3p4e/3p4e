# 48 — Bilingual Delivery Spec (MK + EN dual audio tracks)

> Verified locally 2026-11-15: dual-track MP4 mux works with ffmpeg 8.0.1
> using the existing #13 Fenrir MK+EN stems as the test pair.

## 1. Container answer: YES — selectable EN/MK audio tracks are standard

Every delivered film carries **two audio streams in one MP4**:

```bash
ffmpeg -i picture_lock.mp4 -i narration_mk.wav -i narration_en.wav \
  -i sfx_bus.wav -i amb_bus.wav \
  -filter_complex "[1:a][3:a][4:a]amix=inputs=3[a_mk];[2:a][3:a][4:a]amix=inputs=3[a_en]" \
  -map 0:v -map "[a_mk]" -map "[a_en]" \
  -c:v copy -c:a aac -b:a 192k \
  -metadata:s:a:0 language=mkd -metadata:s:a:0 title="Macedonian" \
  -metadata:s:a:1 language=eng -metadata:s:a:1 title="English" \
  film_NN_dual.mp4
```

| Layer | What the viewer gets |
| --- | --- |
| Stream 0 (video) | h264/h265 copy of the picture lock |
| Stream 1 (audio) | MK mix: MK TTS + SFX + ambience |
| Stream 2 (audio) | EN mix: EN TTS + same SFX + ambience |

Viewer switching works in **VLC, mpv, Plex, Infuse, Jellyfin, and any
hardware player that respects ISO-639 tags**. Default track = MK
(stream order); EN is one remote-click away.

### Language tags (verified correct values)
- Macedonian = `mkd` (ISO 639-2/T) — NOT `mkv` (that is the Matroska container name; caught in the 2026-11-15 demo and corrected here)
- English = `eng`

### Web-player caveat (honest)
HTML5 `<video>` has no universal audio-track switcher — each browser
device ships its own UI (Safari best, Chrome/Firefox spotty). For a web
player we control, the player must implement `audioTracks` selection or
ship two files (`film_NN_mk.mp4` / `film_NN_en.mp4`). Both variants are
produced from the same stems, so the cost is only mux time, not re-render.

## 2. Mix topology (applies to both languages)
```
TTS stem (MK or EN) ─┐
SFX bus ─────────────┼─ amix −14 LUFS −> aac 192k
Ambience bed ────────┘
```
SFX + ambience are **language-independent** — one render serves both mixes.

## 3. Per-story deliverables at picture-lock
- `film_NN_dual.mp4` — dual-track master (above)
- `film_NN_mk.mp4` / `film_NN_en.mp4` — web-player split variants
- `audio/narration/sNN_MK.wav` + `sNN_EN.wav` — the bilingual TTS stems
- `NN_AUDIO_MIX_SPEC.md` — per-story bus map, modelled on 23_AUDIO_MIX_SPEC_v4_K6.md

## 4. Status
- Container demo: ✅ verified (`/tmp/dual_track_demo.mp4`, 2 audio streams probed)
- #13 Fenrir: MK+EN stems already exist (99 files) — ready to mux at picture lock
- #23 Perseus: MK+EN stems scripted (v3 65-clip) — generation gated on GO
- Stories 01–40 (excl. 13/23): MK lines authored; **EN translation pass pending director GO** (see cost estimate in chat)
