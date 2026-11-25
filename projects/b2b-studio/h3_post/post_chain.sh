#!/bin/bash
# Cut every buildable H3 film now, then pitch/feed/subtitle versions. After the 41-shot batch finishes
# (H3X_ALL_DONE in h3cut.log), run the finishing step again for the films that become buildable.
cd /workspace/h3cut && nice -n 15 python3 cut_h3.py >> /workspace/h3cut_now.log 2>&1
cd /workspace/h3post && nice -n 15 python3 h3_post.py >> /workspace/h3post.log 2>&1
until grep -q H3X_ALL_DONE /workspace/h3cut.log 2>/dev/null; do sleep 120; done
cd /workspace/h3post && nice -n 15 python3 h3_post.py >> /workspace/h3post.log 2>&1
echo POST_CHAIN_DONE >> /workspace/h3post.log
