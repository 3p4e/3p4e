# 58 — Hollow Bloom v2 — DEPENDENCIES MANIFEST (everything Grok cited, consolidated)
# 2026-11-16. Every item named in docs 53/55/56/57. Role → exact artifact → source → VRAM/notes.

## A. GENERATION STACK (primary — Wan 2.2 Fun Control, Apache 2.0)
| Artifact | Role | Source | Notes |
|---|---|---|---|
| ComfyUI latest stable + Wan2.2 Fun Control template | runtime | docs.comfy.org tutorial (doc 56) | Workflow → Browse Templates → Video |
| wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors | diffusion (first pass) | Wan2.2-Fun-A14B-Control HF repo | ~14B fp8 |
| wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors | diffusion (second pass) | same | |
| wan2.2_i2v_lightx2v_4steps_lora_v1_HIGH_noise.safetensors | 4-step acceleration | Wan_2.2_ComfyUI_Repackaged | HIGH↔HIGH only |
| wan2.2_i2v_lightx2v_4steps_lora_v1_LOW_noise.safetensors | 4-step acceleration | same | LOW↔LOW only |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | text encoder | same | offload to CPU if tight |
| wan_2.1_vae.safetensors | VAE | same | |
| GGUF Q4_K_M high/low (community) | low-VRAM fallback | community repos | swap Load Diffusion Model → GGUF loaders |
Timing (official, 4090D 24GB 640×640 81f): fp8 ≈524s → +lightx2v ≈79-138s (~6.5×).

## B. CONTROL-VIDEO STACK
| Tool | Role | Source | Notes |
|---|---|---|---|
| DWPose (whole-body pose) | pose control videos for hero body action | comfyui_controlnet_aux / ControlNet preprocessors | detect_hand+detect_body on; OpenPose-format output; DISABLE template preprocessing when feeding pre-made control |
| Reference footage (phone/stock) | DWPose input for crossbow-draw, sword-overhead-strike, vault | self-record or stock (Q2) | clean, single-subject, realistic |
| Video Depth Anything Small/Base/Large | depth control videos (space lock) | yuvraj108c/ComfyUI-Video-Depth-Anything (HF: depth-anything/Video-Depth-Anything-*) | input_size 518, max_res 1280, fp16 OK, gray colormap; Large for hero env; TGM temporal consistency — never frame-by-frame DAv2 for >2-3s (doc 55) |

## C. IDENTITY-CRITICAL FALLBACK (LTX-2.3 Dev)
| Tool | Role | Source | Notes |
|---|---|---|---|
| LTX-2.3 22B dev checkpoint + distilled + gemma-3-12b-it + distilled LoRA | CU rendering | KB §22 proven recipe | 30-40 steps CFG 3.0-3.5 start 0.7-0.8 |
| BFS Nodes (ComfyUI) | LTX Identity Transfer node | community | required by Best-Face-ID |
| LTX-Best-Face-ID LoRA (~2.47GB) | face identity lock | Alissonerdx; TASS-RoPE source_id=2 + ArcFace | prompt MUST start 'ref_t2v:' |
| LTX Likeness Guide | persistent face anchor | community node | silent-reference + bbox |
| IC-LoRA / ID-LoRA | character sheet / talking head | research | optional |

## D. VERIFICATION GATES (Q7 — must exist BEFORE batch; wired into tools/analyze_hb_slop.py)
| Gate | Threshold | Dependency |
|---|---|---|
| start-frame correlation | ≥0.92 cosine | CLIP image embeddings (open_clip / transformers) |
| drift drop | ≤15% | RAFT (torch) or Farneback (opencv — implemented) |
| face count | exact vs keyframe | InsightFace (buffalo_l) or MTCNN; YuNet = local fallback |
| palette HSV | ≤12 mean ΔHSV | OpenCV histogram |
| motion band | 2-18 px/frame | optical-flow magnitude |
| sharpness | ≥80 | Laplacian variance (implemented) |
Reject on 2+ failures per clip. Proof clips: s01 (wide), s19 (combo), s44 (CU).

## E. AUDIO/ASSEMBLY (unchanged from v1, reused)
ffmpeg · sox · edge-tts (MK voices Aleksandar/Marija) · EN TTS (existing WAVs) ·
MusicGen/transformers beds (aigen) · procedural SFX · mix timed to sync frames (#44 f28-30, #45 f24-26).

## F. BOX REQUIREMENTS
48GB GPU (RTX 4090 / A6000 / RTX 6000 class), 100GB+ disk (weights ~55GB + VDA + LTX fallback),
provision script: tools/prov_hb_v2.sh.
