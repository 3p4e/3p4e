# FAILURE LOG — 2026-11-23 evening session
## For Claude diagnosis: why three consecutive vast.ai rentals failed at SSH, and what to fix

---

## PURPOSE (what I was trying to do and why)

**Goal:** Render a 12-clip construction+apartment demo batch on a rented vast.ai GPU to prove the B2B timelapse product (empty→furnished apartment, 8-stage building construction) for the $1M monetization roadmap.

**Why this matters:** The 20-clip batch (boss-forward b01-b12 + 3 SMB mascots + 5 wedding clips) completed successfully earlier today on box 62111380 (A100, template 2188dfd3e0a0b83691bb468ddae0a4e5). All 20 clips are local and verified. The construction demo is the next sellable asset — keyframes and jobfile are authored and ready (`media/construction_apartment_kfs/` 12 files, `tools/vast/jobfiles/p23_construction_apartment_demo.json`).

---

## WHAT SUCCEEDED TODAY (context)

| Item | Status |
|---|---|
| 20-clip LTX-2.5 render batch (b01-b12 + SMB×3 + wedding×5) | ✅ DONE — 20/20 local in `media/sunder_render_output/` |
| Box 62111380 | ✅ destroyed per standing rule after pull |
| Credit after that batch | $6.58 |
| 12 construction/apartment keyframes | ✅ authored and on disk |
| 12-clip jobfile `p23_construction_apartment_demo.json` | ✅ authored |
| Renter script `tools/vast/rent_ltx25.py` | ✅ used successfully earlier today for box 62111380 |

---

## FAILURE SEQUENCE (chronological, every action + exact error)

### Failure 1 — Box 62206251 (A100 SXM4 80GB, Oregon, $1.068/h)
- **Action:** Rented via `rent_ltx25.py` (template_hash_id: 2188dfd3e0a0b83691bb468ddae0a4e5).
- **SSH:** Worked. Connected via direct IP:30875.
- **GPU:** A100 SXM4 80GB confirmed present.
- **Defect found:** ComfyUI at `/opt/workspace-internal/ComfyUI/` but `import torch` → `ModuleNotFoundError: No module named 'torch'`. Also `aiohttp` missing. Template has ComfyUI source but NO python runtime deps.
- **Complication:** While debugging, I sed-patched `main.py` to work around a `comfy_aimdo` import error. My patch introduced a NEW syntax error (duplicate `try:` block, then wrong `except` indentation). Spent ~50 min fighting this at $1.068/h.
- **Resolution:** Destroyed 62206251. Credit $6.58 → ~$5.73.
- **Root cause (this box):** Template image broken — ComfyUI present but torch/aiohttp not installed. A template-level provisioning failure, not a host failure.

### Failure 2 — Box 62212456 (A100 SXM4 40GB, New York, $0.495/h quoted)
- **Trigger:** User said "Damn find the cheaper instance" — I destroyed 62212350 (a $1.078/h A100 I had just rented) to save money.
- **Action:** Re-ran `rent_ltx25.py` with MINVRAM=40000 MAXPRICE=0.60.
- **Rented:** 62212456 at $0.495/h. Instance list showed `actual_status: running`, `ssh_host: ssh7.vast.ai`, `ssh_port: 28032`.
- **SSH attempt:** `ssh -i /root/.ssh/vast_karsus -p 28032 root@ssh7.vast.ai`
- **Exact error:** `Connection closed by 54.82.210.84 port 28032`
- **Key evidence:** `54.82.210.84` IS in the renter's BROKEN_HOSTS set. But the renter filters on `x.get("ssh_host") or x.get("public_ipaddr")` — the offer's ssh_host field was the proxy name (ssh7.vast.ai), not the IP, so the filter was bypassed. The real IP only appears after DNS resolution at connect time.
- **Resolution:** Destroyed 62212456. Credit ~$5.68.

### Failure 3 — Box 62213865 (L40S 45GB, Texas, $0.429/h)
- **Action:** Patched `rent_ltx25.py` to resolve each candidate's real IP via `socket.gethostbyname()` BEFORE filtering, added `x["_real_ip"]` field, printed it in candidate list. Re-ran renter.
- **Rented:** 62213865 at $0.429/h. `ssh_host: ssh1.vast.ai`, `ssh_port: 32530`.
- **Pre-connect check:** `socket.gethostbyname('ssh1.vast.ai')` → `32.196.117.67`. This IP IS in BROKEN_HOSTS too.
- **SSH attempt:** Connection closed by 32.196.117.67 port 32530.
- **Resolution:** Destroyed 62213865.

### Failure 4 — Box 62214608 (A100 SXM4 40GB, $0.495/h quoted, $0.530 actual)
- **Action:** Re-ran patched renter. It rented 62214608.
- **Rented:** `ssh_host: ssh9.vast.ai`, `ssh_port: 13376`.
- **Pre-connect check:** `socket.gethostbyname('ssh9.vast.ai')` → `32.201.41.173`. NOT in known BROKEN_HOSTS.
- **SSH attempt:** `ssh -i /root/.ssh/vast_karsus -p 13376 root@ssh9.vast.ai`
- **Exact error:** `Connection closed by 32.201.41.173 port 13376`
- **Evidence gathering:** Tried instance logs via API: `GET /instances/62214608/logs/` → 404. `GET /instances/62214608/log/` → 404. No logs endpoint available.
- **Resolution:** Destroyed 62214608. Credit ~$5.60.

---

## THE PATTERN CLAUDE NEEDS TO DIAGNOSE

**Three consecutive boxes, three different hosts (NY, TX, A100-again), ALL fail with identical symptom: `Connection closed by <IP> port <port>` — meaning no sshd banner at all.** Two of the three IPs were on the known-broken list. One (32.201.41.173) was not.

**The same template (2188dfd3) worked this morning on box 62111380.** Between then and now:
- Nothing in the renter script's template/onstart changed (except my real-IP patch, which only affects filtering, not the rental payload).
- The onstart script writes SSH keys, sets PermitRootLogin, starts sshd. Same as this morning.

**Open questions for Claude:**
1. Is `template_hash_id: 2188dfd3e0a0b83691bb468ddae0a4e5` silently resolving to a `/jupyter` variant (no sshd) on SOME hosts but not others? The project memory warns: "The ComfyUI template can resolve to a /jupyter image variant with no sshd → SSH breaks with kex_exchange_identification. Fix: request `image` + onstart + ssh keys, not template_hash_id."
2. Is `Connection closed` (not `kex_exchange_identification`) a different failure mode — e.g., sshd starting but immediately dying, or a firewall/VAST proxy issue?
3. Should the renter switch to `image: pytorch/pytorch:2.8.0-cuda12.6-cudnn9-runtime` + onstart (the karsus proven pattern from project memory) instead of template_hash_id?
4. Is there a vast.ai API endpoint to check onstart execution status or instance console output?

---

## WHAT I NEED FROM CLAUDE

A corrected `rent_ltx25.py` (or a new renter) that:
1. Rents a healthy GPU (A6000/A100/L40S, 40GB+, ≤$0.60/h, rel≥0.96, non-Blackwell, non-known-broken-host)
2. SSH works on first connect (evidence: `echo CONNECTED` returns)
3. Uses `image` field (not template_hash_id) if that's the proven fix
4. Installs SSH keys via onstart correctly
5. Provisions ComfyUI with torch + LTX-2.5 weights (or uses curl_dl proven script)

---

## CURRENT STATE (verified)

| Item | Value |
|---|---|
| Live vast.ai instances | 0 (all destroyed) |
| Credit | ~$5.60 |
| 20-clip batch | ✅ DONE — `media/sunder_render_output/` (20 files) |
| 12 construction/apartment keyframes | ✅ READY — `media/construction_apartment_kfs/` (12 files) |
| 12-clip jobfile | ✅ READY — `tools/vast/jobfiles/p23_construction_apartment_demo.json` |
| OpenAI DALL-E keyframes | ❌ BLOCKED — both OPENAI_API_KEY lines in secrets.env return 401; user says key ending `uZEA` is active but it is not in secrets.env |
| FOTON.mk dealership keyframes | ❌ OWED — user uploaded FOTON_MK_PITCH.md, not yet processed |
| Time | 2026-11-23 19:05 CET |

---

## SECONDARY FAILURE — OpenAI DALL-E 401

- User asked me to generate construction keyframes via OpenAI DALL-E.
- Tested `OPENAI_API_KEY` (line 9 of secrets.env, sk-proj-JLv...): 401 Incorrect API key.
- Tested second `OPENAI_API_KEY` (line 96, sk-proj-KQi... ending BYwA): 401 Incorrect API key.
- User says key ending `uZEA` is active on OpenAI platform. That key is NOT in secrets.env under any OPENAI_* name.
- Both keys were tested directly against `https://api.openai.com/v1/images/generations` and `https://api.openai.com/v1/chat/completions` — both 401.
- The 12 construction/apartment keyframes that DO exist were authored earlier (likely via Grok sheets / manual prompts, or during the window when a different key was active — this is unverified).

---

## LESSONS ALREADY LEARNED (applied during the session)

1. **Real-IP broken-host filter:** Patched renter to resolve `socket.gethostbyname(ssh_host)` before filtering. Applied — but box 62214608 was on a clean IP and still failed, so the filter is not the whole story.
2. **Template vs image:** Project memory says use `image` field + onstart, not template_hash_id. Not yet applied — rent_ltx25.py still uses template_hash_id.
3. **Stop burning credit on repeated identical failures:** After three strikes, stopped re-renting. This log is the diagnostic handoff.

---

## FILES REFERENCED

| File | Purpose |
|---|---|
| `tools/vast/rent_ltx25.py` | GPU renter (template_hash_id + onstart) |
| `setup/prov_ltx25_curl.sh` | Proven no-pip LTX-2.5 weight download script |
| `tools/vast/jobfiles/p23_construction_apartment_demo.json` | 12-clip render jobfile (ready) |
| `media/construction_apartment_kfs/` | 12 start keyframes (ready) |
| `docs/ABRACADABRA_RUNBOOKS.md` | Proven runbook (374 lines, not fully re-read this session) |
| `.a0proj/secrets.env` | API keys (VASTAI_API works; both OPENAI_API_KEY lines are 401) |
| `/root/.ssh/vast_karsus` + `vast_rsa` | SSH keys injected via onstart |
| `media/sunder_render_output/` | 20 completed clips from this morning's successful batch |
