# Handoff for the other agent (written 2026-11-23)

From the Claude session that built the ABRACADABRA v3 clips and the B2B research. Read this top to bottom before touching Vast.

## 1. Rules from the owner (keep them)
- Never print secret values; name env vars only.
- No Claude attribution (Co-Authored-By, "Generated with Claude Code", session links) in commits, PR bodies or comments.
- Do not stop or destroy a Vast box without the owner's say-so, unless your own standing rule says destroy after pull. Do not touch boxes you did not create.
- Check Vast credit before and after renting; stop and ask at 2x your estimate.

## 2. What exists (all in repo `3p4e/3p4e`, branch `claude/higgsfield-setup-36wadp`, draft PR #13)
| File | What |
|---|---|
| `projects/b2b-studio/B2B_RESEARCH_AND_PROMPTS.md` | North Macedonia market research (two passes, deep pass overrides) + 12 LTX 2.5 prompt sets (50 stages) |
| `projects/b2b-studio/LTX_PROMPTS.md` | the 50 prompt stages alone (generator: `gen_prompts.py`) |
| `projects/b2b-studio/FOTON_MK_PITCH.md` | Foton Macedonia (foton.mk): what their site says, pitch outline, 21 stages with keyframe concept + LTX prompt (generator: `gen_foton.py`) |
| `projects/abracadabra-menu/v3-pipeline/` | the working LTX 2.5 batch pipeline (jobs.json, batch.py, setup.sh, post_v3.sh, keyframe scripts) |
| `higgsfield/59, 64, 67` | LTX 2.5 methodology and lessons (doc 67 sec.2 = prompt structure) |

Foton keyframes (21 JPG, 1280x704, plus 2 contact sheets), temporary link:
`https://abracadabra.srv1231216.hstgr.cloud/_dl_<private-token>/FOTON_KEYFRAMES.zip`
The folder is scheduled for removal about 24 h after 2026-11-23 17:04 UTC; download it now.

## 3. Foton keyframes: status and caveats
- Made with OpenAI `gpt-image-2` (`/v1/images/edits` with reference, `/v1/images/generations` without), 1536x1024 then center-cropped to 1280x704.
- Tunland V9 frames (14) match the dealer's public product render (references only, not committed). G7 plausible. **V7 frame is wrong** (teal, different body; the site's V7 is Aurora Green): regenerate. Interior (D1-D3) and trucks/van (E1-E4) are generic, not verified Foton models: do not show as final.
- Permission: a private pitch sample for the dealer is fine. Publishing clips, or using Foton's own product images in clips, needs their written OK (and confirmation that the dealer may approve use of the Foton trademark). No logos or readable text in frames; add logo/CTA in post.
- Next: stage names map to files `A1_dawn-teaser.jpg` ... `G2_fleet-lineup.jpg`. LTX params per stage are in FOTON_MK_PITCH.md (1280x704, 121 frames, strength 0.7, steps 8, cfg 1.0).

## 4. Diagnosis of your three failed Vast rentals (SSH "Connection closed")
Based on your failure log plus what worked for me on box 62111380 (RTX A6000, same account). Hypotheses are marked.
1. **`template_hash_id` is ignored** by the rent call (repo runbook lesson). The box boots the template image without your onstart, so no key and a template without torch. Your box 62206251 (`vastai/comfy:v0.46.0`) had ComfyUI source but no torch: consistent. Destroy a broken template immediately; do not hand-patch `main.py` on a billed box (that cost you ~50 min).
2. **What worked for me:** `PUT /asks/{offer_id}/` with explicit `image` (I used `pytorch/pytorch:2.8.0-cuda12.6-cudnn9-devel`), `disk`, `label`, `runtype:"ssh"` and a minimal onstart (start sshd only if absent, never restart it). Without `image` the API answers "image must be a str". My onstart key injection did **not** work (Permission denied); I attached the public key with `POST /instances/{id}/ssh/` and connected via the proxy host/port from `GET /instances/`.
3. **"Connection closed" with no banner** (not "Permission denied") = the Vast proxy accepted TCP but could not reach the instance's sshd. Most likely sshd/container not ready yet (large image pull on a fresh host; `actual_status: running` can appear early) or sshd not running at all (hypothesis, not proven).
4. **BROKEN_HOSTS logic is wrong:** `sshN.vast.ai` resolve to shared Vast proxy IPs (e.g. 54.82.210.84, 32.196.117.67), not the GPU host. Blacklisting those IPs blocks a gateway, not a bad machine, and your third failure was on a clean IP anyway. Key the filter on `machine_id` / `public_ipaddr` from the offer.
5. **Gate every rental:** after renting, attach the key, then retry `ssh ... echo CONNECTED` every ~20 s for up to ~8-10 min, trying the proxy host/port and then `public_ipaddr` with the mapped port 22. No banner after ~10 min: destroy and blacklist that **machine_id**. After 2 failures on one image, change image or machine class, do not repeat.
6. After SSH works: install torch with `uv sync` / the package route (never hand-pin torch), then `setup/prov_ltx25_curl.sh` for weights. Full working chain is in `projects/abracadabra-menu/v3-pipeline/setup.sh` and `higgsfield/67`.
7. Runner output truncates large responses over SSH; pull clips through a temporary web folder or scp, and pull as clips finish (Vast SSH can die mid-rental).

## 5. OpenAI 401
A 401 is an invalid key, not a model problem. Put the active key (the one ending `uZEA` per the owner) into `secrets.env` as `OPENAI_API_KEY`. Model for keyframes: `gpt-image-2`; use `/v1/images/edits` (multipart, field `image[]`) when you pass references, `/v1/images/generations` (JSON) when you do not.

## 6. State I leave
- ABRACADABRA v3: live on KVM4 at `abracadabra.srv1231216.hstgr.cloud` (126 clips, MP4 + WebM). Old stacks archived under `/opt/archive` on KVM4. Old-TV USB videos re-rendered and delivered; zips on the temp download link above.
- Vast: my box 62111380 is gone (not by me). I do not own any live Vast box. Leave anything running that is not mine alone.
- Open: regenerate Foton V7 keyframe; verify truck/van keyframes against real Foton images once the dealer agrees; construction/apartment 12-clip demo is yours (jobfile and keyframes are in your tree).
