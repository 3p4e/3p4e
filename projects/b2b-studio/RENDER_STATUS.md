# Render status (2026-11-24, ~01:00 UTC)

## LTX-2.5 (two Vast boxes)
| Batch | Content | Clips | Status |
|---|---|---|---|
| 2–3 | timelapse transitions, construction fixes | 41 | done, on KVM4 `/opt/abra-v3/ltx_out` |
| 4 | branch commercials | 46 | done, on KVM4 |
| 5 | extras | 20 | done, on KVM4 |
| 6 | Balkan 5-shot commercials | 44 | 18 done (KVM4); rest rendering on new box 62264286 |
| 7 | timelapse sets (tl2) | 50 | queued on new box after batch 6 |
| 8 | Vincinni ads | 10 | queued on old box 62228169 |
| 9 | Foton fix shots | 4 | queued on old box |
| 10 | Foton V9 specs film + extras | 16 | rendering first on old box |

Old box 62228169 was stopped by the host, then restarted on its own; all its finished clips were pulled. Scripts: `render/`.

## MiniMax-H3 (self-hosted, Japan)
Comparison set 22/22 done (downloaded by the owner). Main queue 158 clips, ~7.5 min each; outputs stay in the permitted territory.

## Voice-over (Gemini TTS, verified by transcription)
66/66 lines: 10 Balkan commercials (mk/sr/sq), Vincinni vc1 + vc2 (mk), Foton specs (mk, numbers spelled out). Concord line 1 changed to "Gjithçka fillon si një ide." Scripts: `vo/`.

## Next
Pull and QC batches 6–10 → cut commercials with VO, logo end card, "concept only" disclaimer and AI label.
