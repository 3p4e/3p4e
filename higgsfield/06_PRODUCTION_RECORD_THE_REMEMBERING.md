# Production record: *The Remembering* v1 (2026-10-30)

**Output:** `output/The_Remembering_v1.mp4` (local, not in git). 91.0 s, 1920×1080, 24 fps, H.264 + AAC, −16.6 LUFS integrated.
**Edit list:** `keyframes/film4_v4/edl.json`. **Job ledger:** `keyframes/film4_v4/ledger.json`. **Assembly:** `tools/assemble_film.py`.

## Cut (20 shots)
1 eclipse over shrine → 2 angels drink the moon (canon design) → 3 circlet macro → 4 pilgrim walks → 5 ★ Azulon CU → 6 angels rise (canon, OTS) → 7 corruption wave stopped → 8 ★ CU → 9 eclipse pulse → **F1 flashback: Shards chained in the Sanctum of Shar** → 10 ★ prayer → 11 angel CU (canon) → 12 eclipse slips → 13 silver tide / white radiance (canon) → 14 transformation (start + end frame) → **B1 bond restored (silver thread)** → 15 Ysolde opens her eyes → 16 ★ CU → 17 seven stars → 18 three figures, fade.
★ = the hero's face (Soul Cinema `b3ba42a8…`), always alone in frame.

## Voices (ElevenLabs Voice Design, eleven_ttv_v3)
| Character | Voice | Pick rationale (measured) |
|---|---|---|
| Azulon | saved `azvZ1e4ESkFJBQljyj23` | 79 Hz, slowest, darkest of 3 |
| Shar | saved `fVAgjfbrqAnDt9gAct91` | 120 Hz, breathiest, slowest |
| Aelyra (fallen) | saved `RiJ99IDOJaFRrr92IRbN` | 143 Hz, lowest, darkest |
| Ysolde (fallen) | preview audio (plan limit: 3 saved voices) | 216 Hz, thin, distinct from Aelyra |
| Ysolde (restored) | preview audio | 208 Hz, brightest |
| Selûne | preview audio | slowest, warmest |
All 10 lines verified by Whisper transcription of the final mix.

## Score
ElevenLabs Music v2.5, 85 s, instrumental (no words detected), time-stretched to 91 s, ducked under dialogue.

## QC
- Likeness (SFace cosine vs training set, frames at 2 fps): shot 5 mean 0.77, shot 8 0.72, shot 16 0.71, shot 10 0.56 (one frame at 0.498).
- Known weaknesses: in shots 8 and 16 the expression reads as a broad grin, not the directed strain/quiet smile; shot 1 shows 6 standing and 2 fallen pillars instead of 5 + 2.

## Changes during production
- Angels of decay redesigned to the user's reference images (spiked iron halos, hooked claws, tattered-skin wings, rot-blistered skin, purple flame, yellow-green steam). Shots 2, 6, 11 and 13 re-rendered; the v1 clips are kept in `clips/v1_old/`.
- New inserts from the references: F1 (Sanctum of Shar flashback) and B1 (the Shards' telepathic bond restored).
- Shot 6 wardrobe fixed with a Nano Banana Pro edit (a modern hoodie replaced by a wool pilgrim's cloak).
