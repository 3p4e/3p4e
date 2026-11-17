#!/usr/bin/env bash
# Robust transfer of the seed-814 corrected clip from instance 59086740.
# Sanitizes the spaces-in-filename remote path to /tmp/o814.mp4 first, then
# downloads to an ABSOLUTE local path, then prints verification markers.
SSHOPT=(-i /root/.ssh/vast_karsus -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=15 -o LogLevel=ERROR -p 18280)
HOST=root@ssh3.vast.ai
LOCAL=/a0/usr/projects/vast/media/vast11111/clips/or_08_sphere_of_annihilation_v2.mp4

echo "[1] sanitizing remote name -> /tmp/o814.mp4"
ssh "${SSHOPT[@]}" "$HOST" 'cp "$(ls /workspace/origami_out/*_814_*.mp4 | head -1)" /tmp/o814.mp4 && ls -l /tmp/o814.mp4 && md5sum /tmp/o814.mp4' 2>&1

echo "[2] downloading"
scp "${SSHOPT[@]}" "$HOST:/tmp/o814.mp4" "$LOCAL" 2>&1

echo "[3] verification"
echo "LOCAL_SIZE=$(stat -c%s "$LOCAL" 2>/dev/null)"
echo "EXPECTED_MD5=a88d0f092b97a20cc362054489e48287"
md5sum "$LOCAL" 2>&1
echo "DONE"
