# 64 — VAST.AI + LTX-2.5 DEPLOYMENT LESSONS & GUARDS

> Hard-won, field-verified fixes for every wall hit during the Sunder/Hollow-Bloom
> deployment campaign (2026-11-17→18). **Read this before renting any box or
> touching ComfyUI-LTXVideo again.** These are not suggestions — they are the
> corrections that turned an all-night failure loop into a verified 97-frame proof
> render.

## 1. VAST.AI SSH — USE THE PROXY HOST, NEVER THE DIRECT IP

**THE error that cost ~$7 and 13+ destroyed boxes:** every box was reachable, but
only through the **`sshX.vast.ai` proxy host + the port Vast assigns**, never through
`public_ipaddr` directly. Direct IP **always times out** (the port is only open on
Vast's proxy side).

| Wrong (what we did all night) | Right |
|---|---|
| `ssh root@104.37.174.11:33808` → timeout | `ssh root@ssh6.vast.ai:19966` → SSH_OK |
| Treat proxy timeout as "box dead" | Treat direct-IP timeout as **expected** |
| Destroy on first SSH failure | Wait out boot/onstart, retry via proxy |

**Gate checks, in order:**
1. Poll `/instances/{id}` until `actual_status == running` and `ssh_port` is set.
2. SSH via **`{ssh_host}:{ssh_port}`** (the proxy) with `-p {port}`.
3. Expect `KEY_INSTALLED` + `nvidia-smi -L` output before any work.

## 2. VAST IGNORES `template_hash_id` — INJECT KEYS VIA `onstart`

- `template_hash_id` in the rent body is **silently ignored**. A box rented "with the
  proven template" never ran our `onstart` → sshd had no key → kex_closed forever.
- **Correct**: `PUT /asks/{offer_id}/` with `{"disk":200, "label":...,
  "runtype":"ssh", "onstart": "<script>"}` — the `onstart` field is what Vast actually runs.
- **The onstart must be minimal and must NOT flap sshd.** The bug that caused
  "connection closed during kex": `pkill -HUP sshd` / `service ssh restart` inside
  onstart restarts sshd mid-handshake. Write keys, start sshd **only if absent**, never
  restart it.
- Working onstart skeleton (used on box 61265703):
  ```bash
  mkdir -p /root/.ssh /workspace/out /workspace/models /workspace/stills
  chmod 700 /root/.ssh
  echo '<pub1>' > /root/.ssh/authorized_keys
  echo '<pub2>' >> /root/.ssh/authorized_keys
  chmod 600 /root/.ssh/authorized_keys
  which sshd >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq openssh-server)
  sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
  sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
  mkdir -p /run/sshd; pgrep sshd >/dev/null 2>&1 || (service ssh start || /usr/sbin/sshd || true)
  date -u > /workspace/BOOTED; echo KEY_INSTALLED > /workspace/KEYOK
  ```

## 3. NEVER RENT WITH A GUESSED IMAGE TAG — USE THE OFFER'S OWN IMAGE

- `image: "pytorch/pytorch:2.8.0"` → `manifest unknown` → box bills forever in a
  loading loop. Two such boxes died before this was caught.
- **The guaranteed-bootable image string is on the offer itself**
  (`bundles/` response → `image` / `image_uuid` fields). If you don't pass `image`,
  Vast boots the offer's default — which is usually fine and is what we used on
  61265703.
- Do **not** invent image tags from memory. Rent with `onstart` + `runtype:ssh` only.

## 4. COMFYUI-LTXVideo LOADER FOLDERS ARE THE *STANDARD* ONES

- The LTX loader nodes call `folder_paths.get_filename_list(...)` over the **standard
  model roots**, not a nested `LTXV/` dir:

  | File | Correct Comfy path |
  |---|---|
  | distilled transformer (INT8 ConvRot, 21GB) | `models/checkpoints/` **and** `models/diffusion_models/` |
  | gemma4-12b encoder (INT8 ConvRot, 15GB) | `models/text_encoders/` |
  | video VAE (1.5GB) + audio VAE (0.4GB) | `models/vae/` |
  | distilled LoRA 450 (8.3GB) | `models/loras/` |
  | latent spatial upscaler x2 (1GB) | `models/latent_upscale_models/` |

- **Symptom of wrong folder:** every loader combo box (`UNETLoader.unet_name`,
  `CLIPLoader.clip_name`, etc.) is **empty** in `/object_info`. Empty combos = weights
  in a folder the loader doesn't scan. Fix = symlink into the standard root, re-query
  `/object_info`, confirm the filename appears.

## 5. LTX-2.5 I2V NEEDS `optional_cond_indices: "0"`

- Passing a start keyframe via `optional_cond_images` on `LTXVBaseSampler` **without**
  `optional_cond_indices` crashes at `easy_samplers.py:188`:
  `TypeError: argument of type 'NoneType' is not iterable` (it does `0 in
  optional_cond_indices`).
- **Fix:** always set `optional_cond_indices: "0"` on the sampler. (The node asserts
  `len(indices) == len(images)`; one keyframe → `"0"`.)

## 6. WEIGHTS SOURCE — PUBLIC MIRROR, NOT THE GATED ORIGIN

- `Lightricks/LTX-2.5` is **gated** and our token returned 401 on some hosts.
- **Use `comfyicu/LTX-2.5` — public, no token, has ALL six files**
  (distilled INT8 + gemma4 INT8 + both VAEs + upscaler + LoRA). ~46GB.
- For **LoRA training** you additionally need the **DEV bf16 transformer (42GB)** and
  the **bf16 text encoder (26GB)** — the distilled INT8 is *inference-only*. Both are
  on the same mirror (`diffusion_models/...-dev-transformer-bf16.safetensors`).
- Verify bytes, not "process done": the 42GB DEV file truncated with a `.lock` file
  still present once. Check exact size before training.

## 7. SCP PORT FLAG IS UPPERCASE `-P` (lowercase `-p` = "preserve times")

- `scp -p 19966 ...` silently skips the port → `Permission denied`. Use `scp -P 19966`.

## 8. HEREDOC ESCAPING — WRITE LOCAL, PIPE OVER STDIN

- Nested bash heredocs around Python break on `\"` inside f-strings and JSON
  (`SyntaxError: unexpected character after line continuation`).
- **Pattern that never breaks:**
  ```bash
  ssh -i key -p PORT user@proxy 'cd /workspace && python3 -' < tools/vast/script.py
  ```
  Write the `.py` locally with `text_editor`, stream it over stdin. No nested quotes.

## 9. LTX-2.5 FRAME CONTRACT — 8n+1

- Frame count must be **divisible by 8, +1** (97 = 12×8+1; 81 = 10×8+1; 49 = 6×8+1).
- Sunder main shots = **81f**, CU inserts = **49f**; vx 70s = 105f. 24 fps.

## 10. VERIFIED PROOF-GATE NUMBERS (baseline to reproduce)

First clean LTX-2.5 proof (`ltx25_proof_s01.mp4`, shot 01, Sunder):
- 768×448, 24 fps, 97 frames, h264, 4.04s, 1.5MB
- sampler: 8 steps, Euler ancestral, CFG 1.0, scheduler max_shift 2.05 / base_shift 0.95
- I2V strength 0.8, `optional_cond_images` = kf_01_start, `optional_cond_indices` = "0"
- **Gates passed:** motion mean 10.10 (≥2.5) · 4/96 frozen · luma σ 4.11 · 0 black ·
  keyframe corr **0.943** · first→mid diff 36.18 (real motion, not slideshow).

---

## Canonical re-rent sequence (do this every time, in order)

1. `PUT /asks/{offer_id}/` with `onstart` (keys + sshd-if-absent) + `runtype:ssh`,
   **no guessed image tag**. Label unique. (Do not pass a `template_hash_id`.)
2. Poll `/instances/{id}` → `running` + `ssh_port`.
3. Wait **240s** for boot + onstart (KB §18) — do NOT destroy on early kex close.
4. SSH via **proxy** `{ssh_host}:{ssh_port}`, verify `KEY_INSTALLED` + `nvidia-smi`.
5. Save box JSON → run `snapshot_download` from `comfyicu/LTX-2.5` (background).
6. `git clone` ComfyUI + ComfyUI-LTXVideo, `pip install -r` both, symlink weights into
   **standard** model roots, start server `--listen 127.0.0.1 --port 8188`.
7. Query `/object_info` → confirm combos populated → submit proof → analyze per clip
   (stream spec, motion, luma, contact strip, keyframe-anchor) → **go batch only after
   the proof passes**.

## Guardrails (never again)

- Never test direct IP first; proxy is the only route.
- Never rent with an image tag from memory.
- Never destroy a box on first SSH failure before the 240s boot settle.
- Never author a ComfyUI workflow from memory — read `/object_info` for every node.
- Never claim "weights downloaded" without checking exact byte size + no `.lock`.
- Never trust `template_hash_id` to run anything.
- scp = `-P`; Python-over-SSH = local file piped via stdin.
