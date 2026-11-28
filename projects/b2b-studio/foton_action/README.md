# Foton Tunland V9: high-energy action films (H3)

10 action shots (dune jump, river crossing, mud, gravel drift, rock climb, jump landing, dusk headlights, sunset hero skid, mountain road, riverbed tracking).
- `kf/`: key frames (Gemini image model, official V9 photo as reference; a01 regenerated to fix the grille).
- `shots.py`: key-frame and H3 motion prompts. `jobs.json`: the 10 H3 FL2VA jobs (seeds 8101-8110).
- `vo/`: Macedonian voice-over (Gemini TTS, voice Charon). Music: ACE-Step `4_automotive` (120 BPM hybrid rock trailer).
- `action_cut.py`: beat-snapped hard cuts (every shot a whole number of beats) with speed ramps inside shots (fast -> motion-interpolated slow motion -> fast); H3 engine sound follows the speed changes; VO ducking; -14 LUFS. Outputs: 30 s 16:9, 15 s 9:16 Reel, 6 s bumper 16:9 + 9:16.
- `go.sh`: runs on the H3 box after the main queue: render the 10 shots, then cut the films there. H3 outputs never leave the box except to the owner's computer (licence).
