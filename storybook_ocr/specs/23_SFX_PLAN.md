# #23 Perseus & Medusa — SOUND DESIGN PLAN
> Spatial SFX + restrained music + dialogue per the KB §7 scaffold.
> Sources: freesound.org (CC0) + synthesized layers; no non-free licences.
> Assembly: ffmpeg per-clip stems, mix at 24fps timeline, loudness -16 LUFS.

## Stem structure (per shot)
  1. BED     - continuous scene bed (storm / cavern drone / sea)
  2. SFX     - 1-4 event sounds tied to beats
  3. FOLEY   - cloth, armor, steps, chains
  4. VOX     - narration (center) + dialogue (per-character, slight L/R pan)
  5. MUSIC   - one restrained motif only (see below)

## Scene beds
| Scenes | Bed | Notes |
|--------|-----|-------|
| S01-S14 | low storm rumble + distant sea + palace room-tone | Seriphos; keep -20dB under VOX |
| S15-S30 | cavern drone (sub 40Hz) + dripping + stone-creak | tension rises with Medusa's hiss layer |
| S31-S45 | open wind + wingbeats + sea below | wingbeat = 1 per second, felt not heard |
| S46-S60 | storm breaking + surf + gulls sparse | final scene: near-silence bed |

## Key event SFX (map to shots)
| Shot | Event | SFX |
|------|-------|-----|
| S03 | king's demand | marble knock, one note |
| S08 | harpe handed | metal shing, cold reverb |
| S10 | shield handed | bronze hum, low |
| S19 | Medusa rises | stone grinding + serpent hiss |
| S21 | claws on shield | metal scrape + ring |
| S26 | decisive strike | wet impact (muted, no gore splatter) + stone-crack |
| S29 | mirror-catch | crystalline shimmer, 1s |
| S34/S38 | Gorgon shriek | processed female cry + reverse-reverb tail (no jump-scare peak; keep under -6dB of VOX) |
| S42 | pursuer petrifies | stone-race crackle, rising then dead-silent stop |
| S43 | chains loosen | iron clink, close, dry |
| S49 | ketos surfaces | huge water displacement + sub-boom |
| S53 | sack opens | leather + soft dread tone |
| S54 | the gaze | ALL SFX cut to silence for 0.8s, then low petrifying drone |
| S55 | waves on stone reef | surf over rock, regular, calm |
| S58 | hands clasp | soft leather grip, intimate |
| S59/S60 | arrival | gulls + distant city bell, one |

## Music rule
One motif only: a low female-voice drone (Medusa's theme) that enters at S19,
breaks apart at S29, and resolves to a warm string drone at S56.
No hero fanfare, no trailer hits. Grimdark restraint (Dark Souls rule).

## Output contract
- Per-shot stems: audio/s##_{BED,SFX,FOLEY,VOX}.wav 48kHz
- Master per language: 23_master_MK.wav / 23_master_EN.wav
- Forced 44100 Hz at final mp4 mux (per operating rules).
