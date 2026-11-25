#!/bin/bash
# Deploy launch/site + site_deploy/nginx.conf to /opt/stacks/bigdogma-site on the VPS (via the kvm4 runner).
# The previous site folder is kept on the host as site.prev-<UTC time>.
set -e
S=/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad
TAR=/dev/shm/bigdogma_site.tar; TS=$(date -u +%Y%m%d%H%M)
cd $S/launch && tar cf $TAR site -C site_deploy nginx.conf
cd $S && python3 rput_par.py $TAR /opt/stacks/_upload bigdogma_site.tar | tail -3
python3 rsh.py "set -e; cd /opt/stacks/bigdogma-site; mkdir stage-$TS; tar xf /opt/stacks/_upload/bigdogma_site.tar -C stage-$TS; \
  chmod -R a+rX stage-$TS/site; mv site site.prev-$TS; mv stage-$TS/site site; cat stage-$TS/nginx.conf > nginx.conf; \
  rm -f stage-$TS/nginx.conf /opt/stacks/_upload/bigdogma_site.tar; rmdir stage-$TS; \
  docker compose restart >/dev/null 2>&1; sleep 2; docker exec bigdogma-site nginx -t 2>&1 | tail -1; docker ps --filter name=bigdogma-site --format '{{.Status}}'; ls site/media; ls site/films | wc -l" 300
rm -f $TAR
