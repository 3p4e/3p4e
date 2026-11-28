#!/bin/bash
# Re-convert films whose web copy changed after the main HLS run (outro tagline, 2026-11-27): their stale HLS is removed
# first so players fall back to the new MP4, then the list is rebuilt once the running hls_build.sh has finished.
SITE=/opt/stacks/bigdogma-site/site
printf '%s\n' $SITE/media/showreel.mp4 $SITE/media/showreel_9x16.mp4 $SITE/media/howto.mp4 > /opt/stacks/hls_redo.lst
rm -rf $SITE/media/hls/showreel $SITE/media/hls/showreel_9x16 $SITE/media/hls/howto
while pgrep -f "^bash /opt/stacks/hls_build.sh" >/dev/null || pgrep -f "^/bin/bash /opt/stacks/hls_build.sh" >/dev/null; do sleep 20; done
bash /opt/stacks/hls_build.sh /opt/stacks/hls_redo.lst
