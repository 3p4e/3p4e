#!/bin/sh
# Monthly (cron, Mumbai): rebuild the H3 geo block list and reload the pitch nginx only if the new config tests clean.
cd /opt/h3/tools && python3 build_geo.py >> geo.log 2>&1 && docker exec ai-studio-pitch nginx -t >> geo.log 2>&1 && docker exec ai-studio-pitch nginx -s reload >> geo.log 2>&1 && echo "$(date -u) reloaded" >> geo.log
