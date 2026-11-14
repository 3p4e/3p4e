# FENRIR #13 — AUDIO PIPELINE DECISION (director: stop research, conclude)
**Date:** 2026-11-12 · **Status:** DECIDED — research phase closed, execution-ready
**Governing decisions already locked:** visuals stay as-is · audio as separate tracks · MK + EN two versions · lip-sync re-renders only S14/S31/S42–S44 · every sound element in-house where possible (no stock libraries)

---

## 1 · SPEECH — stack decided

| Layer | Decision | Why |
|---|---|---|
| **Primary TTS** | **ElevenLabs** (multilingual v2/v3) | Best Macedonian quality of the field (low-resource MK is the hard requirement); cinematic voice library; MK + EN from one stack = consistent casting across both versions; commercial license on paid tier; cheap at our volume |
| **Fallback TTS** | OpenRouter `openai/gpt-4o-mini-tts` | Second-best MK; pay-per-call; zero lock-in if ElevenLabs MK disappoints |
| **Self-host verdict** | NOT viable for MK | Piper/Kokoro/Coqui have no Macedonian; F5-TTS/XTTS zero-shot MK is demo-grade, not film-grade — privacy gain not worth the quality drop for the NARRATOR (family-photo doctrine applies to AZ assets, not to TTS) |

**Voice casting (per language — same voices both versions):**
| Character | Voice direction |
|---|---|
| **Narrator** (carries the film) | low male, resonant with gravitas, measured pace — the Odin-shadow voice |
| Odin | old seer-king, iron weariness, slow |
| Loki | young male, silvertongue warmth — **AI-chosen ElevenLabs voice** (director 2026-11-12: NOT AZ's clone; likeness only, voice is cast) |
| Týr | young warrior, restrained honor |
| Hel | one voice, two textures — warm phrase / cold phrase (the duality is acting direction, not two voices) |
| Fenrir | no speech — **the Howl is SFX, designed (§3)** |
| Dwarfs | gruff, forge-rough chorus (2–3 shared voice base, pitched apart) |

**Execution:** narration/dialogue per-shot lines written from `13_Фенрир_волкот_од_Асгард.md` (MK original + EN adaptation) → ElevenLabs per-shot WAVs → `narration/` bus. Estimated cost **$2–8** for all 46 shots both languages.

## 2 · LIP-SYNC — micro re-render passes (the only GPU audio work)
- S14, S31, S42–S44: LTX-2 quoted-dialogue prompting per `ltx2_prompting_guide.txt` — dialogue in quotes + inline voice description.
- **Two passes** on an x86 GPU box: MK pass, EN pass (same keyframes/seeds, dialogue clause swapped).
- Estimated: 4 shots × 2 languages × ~90s ≈ 12 min GPU. **Not fired yet — needs a spend GO with cap.**

## 3 · SFX — all in-house, zero stock

| Class | Tool | License |
|---|---|---|
| **Ambient beds** (hall, fire, wind, forge, ocean) | **Procedural synthesis** — python/sox filtered-noise + resonator chains | 100% owned, unlimited |
| **Action SFX** (chains, sword, footsteps, jaws clamp) | Procedural first; **ElevenLabs SFX API** as booster where procedural falls short | ElevenLabs paid = commercial OK |
| **THE HOWL** (emotional centerpiece) | 3-layer design: (1) ElevenLabs SFX prompt "giant wolf howl, mournful, norse hall reverb" ×3 takes → (2) procedural layer (sine+formant sweep, 60% wet reverb via ffmpeg aecho) ×2 → (3) mix best-of against picture, pitch -2 semitones for mass | owned output |

**Per-scene SFX map:** authored from the 46-shot list at execution time (each scene: beds + action cues + the howl placement S41) — execution detail, not a decision.

## 4 · MUSIC — original composition, license-clean
- **AI-music weights are off-limits:** MusicGen / Stable Audio Open / AudioLDM2 weights are CC-BY-NC (non-commercial) — a commercial film can't use them. Suno/Udio rights are subscription-gated and revocable. **Rejected.**
- **Decision:** original score composed in MIDI (dark Norse: minor drone, frame-drum pulse, low strings, dissonant brass swells for the binding scenes), rendered via **fluidsynth + free GM soundfont** (FluidR3_GM — composition rights granted, output owned). Layered drone textures via sox synthesis.
- Result: fully owned score, no license exposure, matches the in-house doctrine perfectly.

## 5 · MIXING — ffmpeg spec (stock tools, no DAW needed)

```
Per-shot:  ffmpeg -i clip.mp4 -i narr.wav -i sfx_bus.wav -i music.wav -filter_complex \
  "[2:a]volume=0.9[sfx]; [3:a]volume=0.16[mus]; \
   [1:a]asplit=2[nr][nrs]; [mus][nrs]sidechaincompress=threshold=0.02:ratio=8[duck]; \
   [nr][duck][sfx]amix=3:normalize=0[a]" -map 0:v -map "[a]" -c:v copy shot_mix.mp4
Master:  concat 46 → loudnorm I=-16:TP=-1.5:LRA=11 → fenrir_MK_master.mp4 / fenrir_EN_master.mp4
```
Targets: narration foreground, music bed ≈ −22 LUFS under speech, SFX transient-forward, master −16 LUFS stereo.

## 6 · Where it runs
**GB10 ARM audio box** (kept alive): procedural SFX, fluidsynth score, ffmpeg mixing — all CPU, ARM-fine. ElevenLabs is API (any box). The x86 render box stays for visuals + the two lip-sync passes.

## 7 · Open items needing the director
1. **Loki voice** — AI-chosen (director 2026-11-12: NOT AZ's clone). ✅ DECIDED
2. **Lip-sync micro-pass** — GO given; cap $0.50; targets corrected to **S13/S27/S30** (actual dialogue beats). ✅ APPROVED
3. **Score mood** — dark Norse (drone + frame drums + low strings) approved. ✅ APPROVED

## Blockers
None. Every tool chosen is available today with existing keys (ElevenLabs, OpenRouter) or stock FOSS (sox, fluidsynth, ffmpeg).

**Research phase: CLOSED. Execution order:** narration lines (MK+EN) → ElevenLabs WAVs → SFX pass → score → mix MK master → mix EN master → lip-sync micro-pass when GO'd → final mux.
