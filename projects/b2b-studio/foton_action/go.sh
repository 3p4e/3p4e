#!/bin/bash
# waits for the 41-shot queue (h3x) to finish, renders the 10 Foton action shots, then cuts the action films on the box
cd /workspace
until grep -q H3_BATCH_END /workspace/h3jobs2.log 2>/dev/null; do sleep 60; done
mkdir -p /data/minimax-h3 && cp /workspace/h3act/media/* /data/minimax-h3/
python3 /workspace/h3act/run_jobs.py >> /workspace/h3act.log 2>&1
cd /workspace/h3act && nice -n 10 python3 action_cut.py /workspace/h3act_out h3_ /workspace/h3_foton_action "Made with MiniMax H3 · Видео изработено со вештачка интелигенција" /workspace/h3act/music.mp3 /workspace/h3act/vo >> /workspace/h3act.log 2>&1
echo H3ACT_ALL_DONE >> /workspace/h3act.log
