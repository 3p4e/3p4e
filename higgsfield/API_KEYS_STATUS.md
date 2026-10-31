# API keys available in the environment: status on 2026-10-30
Names only. **Never write key values into the repository.** Tested by listing models (free) and one image call.

| Variable | Result | Use |
|---|---|---|
| `GEMINI_API_KEY` | **403: reported as leaked by Google. Rotate it.** | do not use |
| `AZ_GEMINI_API_KEY` | lists models; image call: 429 quota exceeded | no image quota |
| `BN_GEMINI_API` | **works**: `gemini-3-pro-image` produced the Karsus costume still | **current image key** |
| `EP_GEMINI_API`, `UC_GEMINI_API` | list models; image quota not tested | spare |
| `BN_GOOGLE_GEMINI_API_KEY` | 400 invalid key | do not use |
| `OPENAI_API_KEY` | lists `gpt-image-2.5-flare/sunburst`, `sora-2`, `sora-2-pro`; image call: **no credits remaining** | needs billing top-up |
| `OPENAI_SERVICE_API_KEY` | incorrect key | do not use |
| `OPEN_ROUTER_API_KEY` | valid; **$0.92 left of $349** | too little for video; lists `bytedance/seedance-2.5`, `kwaivgi/kling-v3.0-pro`, `google/veo-3.1` |
| `NVIDIA_API` | valid; no image or video generator in its model list | language models only |
| `FALAI_API_KEY` | not verified (profile endpoint 404) | possible video route, untested |
| Gemini key list | no Veo models | |

Karsus costume test (Gemini `gemini-3-pro-image`, 4 reference images: Blagoj-Base front, crown, two costume references):
output `keyframes/karsus/k_gemini_BN_GEMINI_API.png` (local, git-ignored). Authenticity mean 0.508 (limit 0.50), nose-mouth geometry +32 % (full-length framing makes the face small).
