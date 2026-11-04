#!/usr/bin/env bash
# Retry-loop download of the seed-814 corrected clip (verified remote md5).
set -u
SSHOPT=(-i /root/.ssh/vast_karsus -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=15 -o LogLevel=ERROR -p 18280)
HOST=root@ssh3.vast.ai
TMP=/tmp/local_o814.mp4
EXPECT_BYTES=8758316
EXPECT_MD5=a88d0f092b97a20cc362054489e48287
rm -f "$TMP"
for i in 1 2 3 4 5 6 7 8 9 10; do
  echo "=== attempt $i ==="
  scp "${SSHOPT[@]}" "$HOST:/tmp/o814.mp4" "$TMP" 2>&1 | tail -2
  sz=$(stat -c%s "$TMP" 2>/dev/null || echo 0)
  md=$(md5sum "$TMP" 2>/dev/null | cut -d' ' -f1)
  echo "size=$sz md5=$md"
  if [ "$sz" = "$EXPECT_BYTES" ] && [ "$md" = "$EXPECT_MD5" ]; then
    echo "TRANSFER_OK"
    exit 0
  fi
  sleep 5
done
echo "TRANSFER_FAILED"
exit 1
