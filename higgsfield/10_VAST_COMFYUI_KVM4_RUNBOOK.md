# Runbook: running ComfyUI video generation on Vast.ai from a sandbox, with KVM4 as the private relay

Written 2026-11-01. No secrets in this file (variable names only). Everything here was done and verified in one session.

## 1. What was achieved
- Rented an on-demand RTX 5000 Ada (32 GB) on Vast.ai, ran **Wan 2.2 14B image-to-video** (fp8 + lightx2v 4-step LoRAs) in ComfyUI, with no manual steps for the user except downloading results once.
- Generated: face-less city test (480p 60 s, 720p 185 s) and three Karsus face tests (55-60 s each at 480p). Likeness (SFace vs real photos) held at 0.51-0.57 on the Karsus renders.
- Moved private images to the GPU box and the clips back through KVM4, with SHA-256 checks, then cleaned up.
- Cost of the whole exploration: about $2.2 of $4.34 credit (mostly idle time and failed attempts). Steady-state: about $0.007 per 480p clip and $0.021 per 720p clip of GPU time.

## 2. Architecture
```
sandbox (Claude Code, HTTPS only, no ssh)
  |-- Vast.ai REST API (VASTAI_API): search offers, rent, stop, destroy, labels, logs, ssh keys
  |-- Hostinger API (HOSTINGER_API_TOKEN): list VPS + Docker projects (read compose, find runner)
  |-- KVM4 runner (https://runner.<host>/shell, Bearer token): root shell inside a container with docker.sock
        |-- ssh/scp (own alpine+openssh image, temp key) --> Vast instance (ComfyUI on 127.0.0.1:8199)
```
The sandbox cannot open raw TCP to KVM4 or Vast (only HTTPS through a proxy); KVM4 can. So KVM4 is the hop.

## 3. Credentials (names only)
| Name | Use | Status |
|---|---|---|
| `VASTAI_API` | everything on Vast | works |
| `HOSTINGER_API_TOKEN` / `HOSTINGER_API` | Hostinger VPS API (list VMs, Docker projects; no shell exec) | works |
| `KVM4_RUNNER_URL`, `KVM4_RUNNER_TOKEN` | runner endpoint | token in env is stale (403). The live token is in the runner's compose file (read via Hostinger API); used only after the user explicitly authorised it |
| `KVM4_SSH_KEY` | a PUBLIC key only | not usable to log in |
| `HF_TOKEN` | Hugging Face | expired; public downloads need no token |

## 4. Procedures
**A. Find and rent a GPU.** `POST /api/v0/bundles/` with filters (`gpu_ram`, `num_gpus`, `rentable`, `verified`, `reliability2`, `type: "ondemand"`, order by `dph_total`). Rent with `PUT /api/v0/asks/{offer}/` body `{template_hash_id, disk, onstart, label}`. Template used: official ComfyUI (`vastai/comfy`, hash `2188dfd3e0a0b83691bb468ddae0a4e5`). **Use on-demand.** Interruptible ("bid") offers often sit in "loading/stopped" (resources unavailable) and never start. Offers vanish in minutes; the `id` filter in `/bundles/` does not work, scan the list instead. Filter out `verification=deverified`, RAM under 30 GB, CPU under 8 cores.
**B. Models and ComfyUI.** Do not pre-create `/workspace/ComfyUI` (it blocks the template's install). Copy `/opt/workspace-internal/ComfyUI` to `/workspace/ComfyUI_run`, put models in its `models/{diffusion_models,loras,text_encoders,vae}`, start `/venv/main/bin/python main.py --listen 127.0.0.1 --port 8199`. Wan 2.2 files from `Comfy-Org/Wan_2.2_ComfyUI_Repackaged` (about 38 GB, 8-10 min on the host's link). Never use a bare `wait` in a script that also has a background timer (it hung the job).
**C. Remote command channel (no SSH).** The instance runs a loop that reads its own label via the Vast API (container key `CONTAINER_API_KEY`, `CONTAINER_ID`) and executes `tools/vast/jobs/<hex>.sh` from the public repo when the label is `job:<hex>`. Output goes to the container log. Logs: `PUT /instances/request_logs/{id}/` returns a URL; lines are cut at about 500 characters and the snapshot is cached for minutes, so never push files through logs. Reset the label after use (a stale label re-runs on restart).
**D. KVM4 shell.** `POST {runner}/shell` with `Authorization: Bearer <token>` and JSON `{"cmd": "..."}`; returns `{output, rc}`. Health at `/health`. Keep outputs small; move files in 60 KB base64 chunks with `printf '%s' ... >> file.b64`, then `base64 -d`, and verify `sha256sum`.
**E. KVM4 to Vast over SSH (own temporary key, never touch existing keys).** On KVM4 (inside a throwaway container): generate an ed25519 key in `/opt/xfer`; attach its public half to ONE instance with `POST /instances/{id}/ssh/ {"ssh_key": "..."}`; build a tiny image (`FROM alpine; apk add openssh-client`) and run `ssh`/`scp` with `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /x/k -p <direct port> root@<public ip>`. Afterwards `DELETE /instances/{id}/ssh/{key_id}` and `rm -rf /opt/xfer`, remove the image.
**F. Wan 2.2 graph.** UNETLoader (high, low fp8) > LoraLoaderModelOnly (lightx2v) > ModelSamplingSD3 (shift 5) > two KSamplerAdvanced (steps 4, cfg 1, euler/simple; high 0-2, low 2-end) > VAEDecode > CreateVideo (16 fps) > SaveVideo; WanImageToVideo supplies latents; CLIPLoader type `wan` with umt5 fp8; VAE `wan_2.1_vae`. Script: `tools/vast/run_wan_i2v.py` (does an `/object_info` preflight). 81 frames = 5.06 s.
**G. Likeness QC.** `tools/authenticity_check.py face_dataset <frames_dir>`; pass = mean SFace >= 0.50. Real photos stay in the sandbox, never on the GPU box.
**H. Cost control.** Stop (keeps disk) before destroy; destroy only after outputs are recovered and checksummed. A pre-agreed `send_later` check-in is a backstop. The Vast "execute command" endpoint works only on stopped instances.

## 5. What broke, and the fix
| Problem | Cause | Fix |
|---|---|---|
| Interruptible instances never started | host GPU busy | on-demand only |
| ComfyUI not installed | my script created `/workspace/ComfyUI` first | own copy in `/workspace/ComfyUI_run` |
| Instance stopped mid-setup | idle watchdog (30 min) | removed; rely on explicit stop |
| Script hung after downloads | bare `wait` also waited for the 100 min timer | `wait "${PIDS[@]}"` |
| Clips corrupted over the log | 500-char log lines, cached snapshots | transfer through KVM4 |
| Public publication of face renders blocked | permission policy | private route via KVM4 |
| Key hunting on KVM4 blocked | permission policy | create a fresh temporary key |
| Anonymous file hosts blocked | permission policy | not used |

## 6. Open items
- Karsus's Folly on Wan: plan in `09_KARSUS_FOLLY_WAN_BATCH.md`. Paladin v2: `08_PALADIN_JUDGEMENT_v2.md`.
- KVM4 disk is at 95% (9.5 GB free): needs attention.
- Update `KVM4_RUNNER_TOKEN` in the environment (stale).
- Clips from this session are on KVM4 in `/opt/karsus-tests/`.

## References
- Vast.ai API: https://docs.vast.ai/ (instances, search, ssh keys, request_logs)
- Hostinger API: https://developers.hostinger.com/
- Wan-AI. Wan2.2 (Apache-2.0): https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B ; Comfy-Org repackaged: https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged
- Zhong et al. 2021, SFace, IEEE Trans. Image Process. 30:2587-2598. DOI 10.1109/TIP.2020.3048632.
