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

# --- Model downloads for the Wan 2.2 14B I2V test (fp8 + lightx2v 4-step LoRAs), ~38 GB, Apache-2.0
cat > /workspace/fetch_wan.sh <<'FETCH'
#!/bin/bash
B=https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files
M=/workspace/ComfyUI/models
mkdir -p $M/diffusion_models $M/loras $M/text_encoders $M/vae
get(){ wget -q -c --tries=5 -O "$2/$(basename $1)" "$B/$1" && echo "$(date) ok $1" >> /workspace/fetch.log || echo "$(date) FAIL $1" >> /workspace/fetch.log; }
get diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors $M/diffusion_models
get diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors $M/diffusion_models
get loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors $M/loras
get loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors $M/loras
get text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors $M/text_encoders
get vae/wan_2.1_vae.safetensors $M/vae
echo "$(date) ALL DONE" >> /workspace/fetch.log
FETCH
chmod +x /workspace/fetch_wan.sh
nohup setsid /workspace/fetch_wan.sh >/dev/null 2>&1 &
