import os
from huggingface_hub import HfApi
api = HfApi()
tok = os.environ.get("HF_TOKEN") or None
repos = [
    "LTX-Video/ltx-2.3-22b-distilled-1.1",
    "Lightricks/ltx-video-2.3-22b-distilled",
    "Lightricks/LTX-Video-2.3-22B-distilled",
    "Comfy-Org/ltx-2.3-22b-distilled-1.1",
    "Comfy-Org/ltx-2.3-22b-distilled-1.1_fp8_scaled",
]
for repo in repos:
    try:
        info = api.model_info(repo, token=tok)
        print("OK  ", repo, "| gated=", info.gated, "| files=", len(info.siblings or []))
    except Exception as e:
        print("FAIL", repo, "|", str(e)[:100])
