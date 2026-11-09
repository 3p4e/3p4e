# Wan 3.0 Model Audit — VAST Deployability Research

**Date:** 2026-11-09
**Task type:** ZERO-COST research (web + HF API + GitHub only; no rentals, no spend)
**Researcher:** Agent Zero (model-audit profile)
**Judge ladder:** LTX-2.3 22B distilled (next batch candidate) > SkyReels-V3 R2V-14B (proven) > Wan2.1-FLF2V-14B (chain validated; motion needed 302MB lightx2v LoRA)

---

## Headline finding

**Wan 3.0 is officially launched but is an API-only / hosted product. There are NO public weights.** The official Hugging Face repos under the `wanvideo` org are README-only marketing pages with zero model files, zero downloads, and no licence attached. Self-hosting Wan 3.0 is impossible as of 2026-11-09. Everything else in this audit is downstream of that single fact.

---

## 1. Existence and provenance

| Question | Answer | Source |
|---|---|---|
| Does Wan 3.0 officially exist? | YES — announced and accessible as a hosted service | https://huggingface.co/wanvideo/wan-3-0-video (README), https://wan30.io/ |
| Are weights public? | **NO.** The HF repo `wanvideo/wan-3-0-video` (created 2026-09-04, last modified 2026-09-04) contains exactly 2 files: `.gitattributes` and `README.md` (4,390 bytes). `usedStorage: 0`. Downloads: 0. | https://huggingface.co/api/models/wanvideo/wan-3-0-video |
| Releasing org | Alibaba **Tongyi Wan team** — confirmed by the `wanvideo/wan-3-0-prime` model card: "the accelerated video model from Alibaba's Tongyi Wan team" | https://huggingface.co/wanvideo/wan-3-0-prime |
| Official announcement URL | https://wan30.io/ (live Next.js app, HTTP 200, ~173KB HTML) | direct probe 2026-11-09 |
| Official open-source org status | GitHub org `Wan-Video` (email `wan.ai@alibabacloud.com`, site https://wan.video) still lists **Wan2.2** as its latest repo — Wan2.2 README last pushed 2026-09-21. No Wan3 repo exists there. | https://api.github.com/orgs/Wan-Video/repos |
| Release timeline | Wan 3.0 video README repo created 2026-09-04. Wan 3.0 Prime "availability record: August 20, 2026" per model card. | HF API `createdAt` fields; prime README |

**Conclusion:** Wan 3.0 is a real, shipping, commercial product — but it ships as a cloud API (Standard, Prime, Draft Mode tiers at wan30.io), not as an open-weights model. Wan 2.2 remains the newest open-source Wan.

## 2. Weights and licence

| Question | Answer | Source |
|---|---|---|
| HF repo ID(s) | `wanvideo/wan-3-0-video`, `wanvideo/wan-3-0-prime` (both README-only) | HF API |
| Licence | **None declared.** `cardData.license: null`, no `LICENSE` file in either repo. | HF API `cardData`, siblings listing |
| Gated? | No (`gated: false`) — but there is nothing to gate; no weights exist. | HF API |
| Other HF orgs checked | `Wan-AI` org (the official org for open Wan 2.1/2.2 weights) has 27 models — all Wan2.1 / Wan2.2 variants plus `Wan-Dancer-14B`. **No Wan3 weights.** | https://huggingface.co/api/models?author=Wan-AI |
| `wanx` / `tongyi` search | No Wan3-weight repos; only AccVideo-WanX (2.x-lineage acceleration LoRAs) and unrelated Tongyi-LLM text models. | HF API search |
| EU self-host legality | **N/A — there is nothing to self-host.** The HunyuanVideo-style licence barrier is never even reached; deployability fails one step earlier at "no weights exist." | — |

**Conclusion:** No licence exists because no weights exist. Any site or repo claiming "Wan 3.0 weights download" is either an API reseller or a fake/mislabelled upload.

## 3. Model sizes / variants

| Item | Answer | Source |
|---|---|---|
| Parameter count | **Not disclosed.** Prime model card, verbatim: "Network structure and parameters: Specific architecture, layer counts, and parameter scale have not been disclosed." | https://huggingface.co/wanvideo/wan-3-0-prime |
| Variants | Three hosted tiers: **Standard** (`wan3.0-video`), **Prime** (`wan3.0-video-prime`, speed-optimised, same capability set), **Draft Mode** (very low cost). Plus a third-party "Spicy" relaxed-moderation endpoint (NOT an Alibaba tier — a MuAPI reseller wrapper). | wan-3-0-video README; prime README; https://github.com/Anil-matcha/Wan-3.0-Spicy-API |
| Distilled / fp8 | No public quantised variants exist because no base weights exist. | — |
| Download GB per variant | N/A (nothing downloadable). | — |

## 4. Capability matrix (as advertised — all hosted-API only)

| Capability | Wan 3.0 Standard | Wan 3.0 Prime |
|---|---|---|
| T2V | yes | yes |
| I2V (first frame) | yes | yes |
| FLF (first+last frame) | yes | yes |
| Reference-to-video (multimodal) | up to 20 assets: 10 images + 5 videos (15s combined cap) + 5 audio clips (15s combined cap) | same |
| Video editing | add/remove/replace elements, restyle, relight, dialogue edit | same |
| Video extension | forward / backward / bidirectional | same |
| Max duration | 2–30 s per run (smart duration + extension) | 2–30 s (input+output at most 30s) |
| Resolution / fps | 480p / 720p / 1080p at 30fps MP4 | same |
| Aspect ratios | adaptive, 16:9, 4:3, 1:1, 3:4, 9:16 | same |
| Native audio | dialogue, background music, ambient sound, action effects; can be disabled | same |
| Document/web input | Word/Excel/PowerPoint/PDF/TXT/MD/Keynote/Pages/Numbers or one public web page | same |

Sources: https://huggingface.co/wanvideo/wan-3-0-video/raw/main/README.md and https://huggingface.co/wanvideo/wan-3-0-prime/raw/main/README.md

**Note for the ladder:** on paper Wan 3.0's feature set (FLF + up to 10 identity reference images + native audio + 30s) is the closest commercial match to VAST's FLF 40-60-shot doctrine of any model audited. That is exactly why the weights question matters — and it fails there.

## 5. ComfyUI support

| Route | Status | Source |
|---|---|---|
| Kijai ComfyUI-WanVideoWrapper | **NO Wan 3.0 support.** Repo last pushed 2026-05-24 (pre-Wan3); README contains zero Wan3 references; no wan3 files in tree. Wraps Wan2.x local weights only. | https://github.com/kijai/ComfyUI-WanVideoWrapper (API + README grep) |
| ComfyUI core | No native Wan3 nodes (nothing to load weights from). | absence of evidence |
| Third-party ComfyUI | `Anil-matcha/wan-3.0-comfyui` exists — but it is an **API bridge**: "Wan 3.0 API Key node … connect it to a Wan 3.0 generation node" via MuAPI. Video is generated on MuAPI cloud; the node downloads the returned MP4 URL into `ComfyUI/output`. Nodes: T2V / I2V / R2V / Spicy variants; T2I and image-edit nodes marked "Coming soon — registered but not yet live on Muapi". | https://github.com/Anil-matcha/wan-3.0-comfyui README |

**Conclusion:** there is no local-weight ComfyUI path for Wan 3.0. The only "ComfyUI support" is a remote-API skin.

## 6. Hardware

**N/A — no self-hostable artifact exists.** There is no VRAM/RAM/disk figure to report because there is nothing to download. Any GPU-tier answer (48GB/80GB) would be invented. Vast.ai cannot run Wan 3.0 for the same reason it cannot run Sora: the model is not available.

## 7. Quality / motion reputation

| Question | Answer | Source |
|---|---|---|
| Measured motion strength vs Wan2.1-FLF2V-14B / LTX-2.3 22B | **No verifiable public benchmark.** No weights means no independent replication means no measured numbers. All quality claims are Alibaba marketing copy in the model cards. | wan-3-0-video README |
| vs Wan2.1-FLF2V-14B | Wan2.1-FLF2V needed the 302MB lightx2v LoRA to avoid crossfade degeneracy — a failure mode verified in-house. Whether Wan 3.0's hosted FLF has the same degeneracy is **unknowable without spending API money**; the model card does not address it. | VAST KB (proof_gate_and_batch_rules); wan-3-0-video README (silent on the topic) |
| Community signal | Third-party wrappers (MuAPI ecosystem) market Wan 3.0 as "high motion" and "best uncensored alternative to Seedance 2" — reseller SEO, not measurement. https://github.com/Anil-matcha/Wan-3.0-API (80 stars); spicy variant https://github.com/Anil-matcha/Wan-3.0-Spicy-API. | GitHub search |
| Known degeneracies | None publicly documented for Wan 3.0. The audio-texture and on-screen-text accuracy caveats in the official README are the only stated limitations. | wan-3-0-video README "Availability and limitations" |

## 8. VERDICT

# DEPLOYABLE-NO

**Reason:** Wan 3.0 fails the deployability gate at the first test — there are no weights. Every downstream requirement (EU self-host, Vast.ai 48-80GB lane, per-frame identity scoring, offline keyframe generation, ComfyUI local graph) fails automatically.

### Exact blockers
1. **No public weights** — HF repos are README-only (`usedStorage: 0`); Wan-AI org stops at 2.2; GitHub org has no Wan3 repo. Hard blocker, not a licence-workaround situation.
2. **No licence at all** — `license: null`; EU deployability untestable (HunyuanVideo precedent never reached).
3. **API-only access** — wan30.io hosted tiers with per-second billing (site pricing page shows per-second rates in the approx 0.0156-0.0399 USD band plus 9.90/29.90 USD subscription tiers; third-party MuAPI resellers quote 0.0329 USD/s at 480p). This is a **cloud route, not a self-host route** — same budget/privacy category as Higgsfield/Seedance, not the Vast.ai lane.
4. **Privacy bar** — Wan 3.0's headline feature is uploading up to 10 identity reference images plus audio to Alibaba-hosted infrastructure. VAST rules bar sending enrolled family faces to third-party clouds without an explicit decision; this audit grants nothing.
5. **No local ComfyUI path** — Kijai wrapper unsupported; only an API-bridge node pack exists.
6. **Unmeasurable** — no independent motion/identity benchmarks; all quality claims are vendor copy.

### Enablers (what would change the verdict)
- Alibaba releases Wan 3.0 weights under an EU-compatible licence on the `Wan-AI` HF org (the 2.1/2.2 pattern). If that happens, re-run this audit immediately — on paper (FLF + 10-image identity reference + 30s + native audio) it would jump to the top of the ladder review.

### Comparison to current ladder
| Model | Status | vs Wan 3.0 |
|---|---|---|
| LTX-2.3 22B distilled | next batch candidate, self-hostable | strictly better for us: weights exist, ComfyUI-native, EU-checkable |
| SkyReels-V3 R2V-14B | proven in-house | strictly better: same reasons |
| Wan2.1-FLF2V-14B | chain validated, LoRA-gated motion | worse features, but deployable — the only axis that counts |
| **Wan 3.0** | API-only | best paper feature set, zero deployability |

---

## What this means for the Hollow Bloom 50-clip film

1. Wan 3.0 changes nothing on the current plan — the LTX-2.3 22B distilled batch remains the next paid candidate.
2. Do not budget Wan 3.0 API credits as a substitute: per-second billing on 50 clips of about 5s each is roughly 250s of video, about 8-10 USD at advertised rates before retries, with family-face uploads to a third-party cloud — a separate, explicit approval decision, not a drift.
3. Watch the `Wan-AI` HF org for a weights drop; the moment Wan 3.0 weights appear with a usable licence, it outranks Wan2.1-FLF2V on the ladder because its reference-image capacity (10 images per shot) matches the identity doctrine.
4. If a cloud-API experiment is ever wanted, the correct shape is a single capped proof (1 clip, at most 2 USD, no family faces, generic actor card only) under the project's itemized-approval and cap rules.
5. Kijai's wrapper needing zero changes is the tell: the entire open ecosystem currently treats Wan 3.0 as somebody else's hosted model.

---

## Source list (all verified 2026-11-09)

1. https://huggingface.co/api/models/wanvideo/wan-3-0-video — repo metadata (0 storage, 0 downloads, no licence, created 2026-09-04)
2. https://huggingface.co/wanvideo/wan-3-0-video/raw/main/README.md — capability and availability text
3. https://huggingface.co/wanvideo/wan-3-0-prime/raw/main/README.md — Prime tier, Alibaba Tongyi Wan attribution, Aug 20 2026 availability, "parameters not disclosed"
4. https://huggingface.co/api/models?author=Wan-AI — official open-weights org, newest = Wan2.2
5. https://api.github.com/orgs/Wan-Video — official GitHub org (Wan2.2 only, wan.ai@alibabacloud.com)
6. https://wan30.io/ — official hosted product (HTTP 200)
7. https://wan30.io/pricing — per-second price band 0.0156-0.0399 USD, tiers 9.90 / 29.90 USD
8. https://github.com/kijai/ComfyUI-WanVideoWrapper — no Wan3 support (last push 2026-05-24)
9. https://github.com/Anil-matcha/wan-3.0-comfyui — API-bridge ComfyUI pack via MuAPI
10. https://github.com/Anil-matcha/Wan-3.0-API — third-party API SDK; 0.0329 USD/s at 480p quoted
11. https://github.com/Anil-matcha/Wan-3.0-Spicy-API — relaxed-moderation reseller tier (not an Alibaba product)
