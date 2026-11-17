# 47 — VAST Audio Stack Plan (all storybook stories, 2026-11-15)

Scope: all 40 Macedonian story packages EXCLUDING #13 (Fenrir, done) and #23
(Perseus, done). The DH+Paladin boss fight has its own audio workstream.
Source corpus: 1,997 shots — 1,786 with Macedonian narration, 316 with dialogue.

---

## 1. Narration / Dialogue TTS

| Item | Decision | Precedent |
|---|---|---|
| Engine | ElevenLabs `eleven_multilingual_v2` (MK + EN in ONE model — verified on #13/#23) | `tools/gen_narration_tts.py`, `tools/gen_23_narration.py` |
| Output | 48 kHz PCM16 mono WAV stems per shot | #23 pipeline |
| Voice casting | narrator = Brian (deep, resonant); per-story cast map derived from each story's `cast` block (archetype → probed voice_id) | `gen_narration_tts.py` VOICES table |
| Language pair | MK line + EN line per shot, `**SNN** CHAR: „MK…" / "EN…"` grammar | `23_AUDIO_SCRIPT_MK_EN_v3_65clips.md` |
| Length budget | 121 frames @ 24 fps ≈ 5.05 s/clip → dialogue ≤ 14 EN words, narration ≤ ~16 EN words | #23 v3 script |
| Spend gate | DRY RUN manifest first (zero API); `--generate` only on director's explicit GO; every run its own ledger | VAST operating rules |

Script source: per-shot `narration_mk` / `dialogue_mk` fields already in every
data JSON ( doctrine step 2 satisfied — narration written BEFORE visuals).
Missing MK lines are derived from the shot's beat text, never invented.

## 2. Sound Effects (SFX)

Deterministic per-shot SFX layer, keyword-derived from the shot's own
action/motion/beat text (nothing invented):

| Family | Keywords | SFX layer |
|---|---|---|
| combat | strike, slash, clash, lunge, parry, impact | metal ring + whoosh + body-fall |
| movement | run, chase, gallop, ride, sprint | footfall/hoofbeat bed |
| water | sea, wave, storm, rain, river | ocean/water bed |
| fire | flame, torch, ember, burn | crackle bed |
| wind | gale, breeze, gust, storm | wind bed |
| magic | glow, rune, aura, spell, transform | shimmer/riser |
| creature | roar, hiss, growl, snarl | creature vocal |
| door/gate | open, creak, gate, door | stone/wood groan |
| ambient quiet | (none matched) | room-tone / nature floor |

## 3. Ambience / Music

| Layer | Rule |
|---|---|
| Ambience bed | one continuous per-act bed from the story's dominant env motif (ocean/hall/forest/gate/cavern/spires/peaks) |
| Music | no score at TTS stage; music is a POST decision after picture lock (mirrors #23 v3: picture lock first, mix spec after) |
| Mix spec | one `AUDIO_MIX_SPEC.md` per story AFTER its render pass, modelled on `23_AUDIO_MIX_SPEC_v4_K6.md` (native-audio stems + TTS stems + SFX buses, −14 LUFS target, MK+EN dual stems) |

## 4. Deliverables per story NN

- `storybook_ocr/specs/NN_AUDIO_SCRIPT_MK_EN.md` — per-shot MK/EN lines + per-shot SFX tag + act ambience tag (authored by `tools/build_audio_scripts.py`, deterministic, zero-cost)
- `media/story_assets/audio/narration/sNN_{MK,EN}.wav` — TTS stems (gated, paid)
- `media/story_assets/audio/sfx/` — SFX stems (gated, paid or library)
- `NN_AUDIO_MIX_SPEC.md` — written at mix time, after the story's render pass

## 5. Execution order (zero-GPU until the director's GO)

1. `tools/build_audio_scripts.py` → all 37 audio scripts (this pass, zero cost)
2. Director review of script drafts
3. DRY-RUN TTS manifest per story (zero cost)
4. Director GO → `--generate` run per story, its own ledger
5. After each story's K6 render pass → mix spec + final mix
