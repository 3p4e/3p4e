# H3 finishing on the GPU box

Runs only on the H3 box. H3 output never leaves it except by the owner's own `scp` download.

- `drive_pull.py`: pulls the H3 clips from the shared Drive folder straight onto the box (`/workspace/old_box_h3out`).
- `post_chain.sh`: cuts every buildable H3 film with `cut_h3.py`, runs `h3_post.py`, and runs it again after the 41-shot batch.
- `h3_post.py`: for each film in `/workspace/h3_commercials`, makes
  - a pitch version (BIG DOGMA intro, concept watermark, email outro) in 16:9 and 9:16
  - 1:1 and 4:5 feed versions
  - mk/sr/sq/en subtitles, timed by cross-correlating the voice-over files against the film soundtrack (`sub_map.json`).
- `verify.sh`: text-only checks of counts, sizes, audio streams, durations and subtitle hits.
- `pack.sh <name>`: hard-links the new outputs into one download folder with a licence README.
