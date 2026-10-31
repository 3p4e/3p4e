#!/bin/bash
# Self-stop watchdog for Vast.ai. Stops this instance after MAX_MIN minutes total,
# or after IDLE_MIN minutes of GPU idle (util<5%) once GRACE_MIN has passed.
# Uses the container-scoped key Vast injects (CONTAINER_API_KEY / CONTAINER_ID).
mkdir -p /workspace
cat > /workspace/watchdog_loop.sh <<'LOOP'
#!/bin/bash
MAX_MIN=180; IDLE_MIN=15; GRACE_MIN=30
start=$(date +%s); idle=0
while true; do
  sleep 60
  now=$(date +%s); el=$(( (now-start)/60 ))
  u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ -z "$u" ] && u=100
  if [ "$u" -lt 5 ]; then idle=$((idle+1)); else idle=0; fi
  stop=0
  [ "$el" -ge "$MAX_MIN" ] && stop=1
  [ "$el" -ge "$GRACE_MIN" ] && [ "$idle" -ge "$IDLE_MIN" ] && stop=1
  if [ "$stop" = 1 ]; then
    echo "$(date) stop requested el=$el idle=$idle" >> /workspace/watchdog.log
    curl -s -X PUT -H "Authorization: Bearer $CONTAINER_API_KEY" -H "Content-Type: application/json" \
      -d '{"state":"stopped"}' "https://console.vast.ai/api/v0/instances/$CONTAINER_ID/" >> /workspace/watchdog.log 2>&1
    sleep 300
  fi
done
LOOP
chmod +x /workspace/watchdog_loop.sh
nohup setsid /workspace/watchdog_loop.sh >/dev/null 2>&1 &
