#!/bin/sh
# Monthly (cron, Mumbai): rebuild the H3 geo block list and reload the pitch nginx only if the new config tests clean.
cd /opt/h3/tools && python3 build_geo.py >> geo.log 2>&1 && for c in ai-studio-pitch bigdogma-site; do docker exec $c nginx -t >> geo.log 2>&1 && docker exec $c nginx -s reload >> geo.log 2>&1 || exit 1; done && echo "$(date -u) reloaded" >> geo.log
