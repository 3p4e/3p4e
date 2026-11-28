#!/bin/bash
cd /tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad/launch/video/_work
/usr/local/bin/python3 showreel.py 16x9 && rm -f seg/sr_16x9_*.mp4
/usr/local/bin/python3 showreel.py 9x16 && rm -f seg/sr_9x16_*.mp4
/usr/local/bin/python3 reels.py all
echo BUILD_ALL_DONE
