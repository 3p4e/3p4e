# ACE-Step 1.5 prompts v2: ACE-style captions (genre, exact instruments, mood, scene) + fixed metadata.
# The LM still plans the audio codes (thinking=True), but caption/metas rewriting is off so the mood cannot drift.
MOODS2 = {
 "1_family": dict(caption="warm acoustic family commercial, gentle piano melody, fingerpicked acoustic guitar, soft string section, glockenspiel sparkles, light shaker, heartfelt, tender, cozy home, sweet moments, major key, broadcast quality mix, instrumental",
                  bpm=90, key="D major", brief="warm, tender, family, acoustic, cozy"),
 "2_corporate": dict(caption="modern corporate background, clean felt piano arpeggios, warm synth pads, soft pulsing synth bass, light electronic percussion, hopeful, trustworthy, scientific, precise, minimal, broadcast quality mix, instrumental",
                  bpm=100, key="C major", brief="clean, hopeful, trustworthy, modern corporate, scientific"),
 "3_construction": dict(caption="epic cinematic orchestral build, driving staccato string ostinato, piano motif, rising taiko and snare drums, brass swells, sense of growth and progress, building a skyline, triumphant final chord, trailer, instrumental",
                  bpm=110, key="D minor", brief="epic, building, triumphant, progress, orchestral"),
 "4_automotive": dict(caption="powerful hybrid rock trailer, distorted electric guitar riffs, punchy live drums, deep sub bass, cinematic impacts and risers, bold, driving, off-road adventure, pickup truck, instrumental",
                  bpm=120, key="E minor", brief="powerful, driving, bold, rock, off-road"),
 "5_luxury": dict(caption="elegant luxury lounge, smooth Rhodes electric piano, warm analog pads, soft deep house groove, subtle shaker, upright bass, sophisticated, calm, riverside city at night, premium real estate, instrumental",
                  bpm=96, key="A minor", brief="elegant, luxurious, sophisticated, calm, lounge"),
 "6_industrial": dict(caption="industrial cinematic corporate, heavy tight percussion, metallic hits, low cello ostinato, brass swells, steel and fire, factory power, proud, determined, strong, instrumental",
                  bpm=105, key="C minor", brief="industrial, strong, determined, metallic, proud"),
 "7_upbeat": dict(caption="modern upbeat corporate pop, bright synth plucks, handclaps, funky bass, clean electric guitar, positive, energetic, teamwork, logistics on the move, career, instrumental",
                  bpm=118, key="G major", brief="upbeat, positive, modern, energetic, teamwork"),
 "8_showreel": dict(caption="inspiring cinematic showreel, building strings, epic hybrid drums, modern synth pulse, memorable piano motif, premium, exciting, confident, big finish, instrumental",
                  bpm=115, key="C major", brief="inspiring, cinematic, premium, exciting, big finish"),
}
