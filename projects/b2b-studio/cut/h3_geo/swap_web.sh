#!/bin/bash
# Re-encode every H3 web copy into /opt/h3/web_new (MiniMax H3 mark bottom right + BD logo top left), then copy the files over the live
# ones in /opt/h3/web (same directories: the nginx containers bind-mount them). Owner, 2026-11-26.
cd /opt/h3/tools && rm -rf /opt/h3/web_new && mkdir -p /opt/h3/web_new
W=/opt/h3/web_new bash build_web.sh > web2.log 2>&1
O=/opt/h3/web_new/_site bash build_site_web.sh > site2.log 2>&1
for d in /opt/h3/web_new/*/; do t=$(basename $d); mkdir -p /opt/h3/web/$t; cp -f $d* /opt/h3/web/$t/; done
chmod -R a+rX /opt/h3/web
# the pitch container bind-mounts /opt/h3/web: if that folder was ever recreated, a running container keeps serving the old one
# (2026-11-27: it still showed the removed Foton showreel). Restart it so the mount points at the current folder.
docker restart $(docker ps --format "{{.Names}}" | grep -i pitch | head -1) >/dev/null; echo "WEB2_DONE $(find /opt/h3/web_new -name '*.mp4' | wc -l) files" >> web2.log
