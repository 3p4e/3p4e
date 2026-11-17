#!/usr/bin/env python3
"""Build the six PHOTOREAL keyframe jobs for Susanoo & Orochi.

Supersedes the cel-shaded storybook spec (story.md §1) with the photoreal
cinematic language used by the accepted Paladin and Karsus films.

Kory now points at the verified female card set (faces/kory_cards_final),
not the bearded legacy card.

  python3 tools/build_photoreal_jobs.py <out.json>
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KORY_CARD = "Kushinada_bust.png"  # staged from kory_cards_final/kory_final_01_front.png

# Shared photoreal style lock — replaces "cel-shaded watercolor storybook".
PHOTOREAL = (
    "Photorealistic cinematic film still, shot on 35 mm anamorphic, "
    "real human skin with visible pores and fine detail, natural subsurface "
    "scattering, shallow depth of field, cinematic colour grade, "
    "dramatic volumetric light, film grain, high dynamic range. "
)

NEG = (
    "cartoon, anime, cel-shaded, watercolor, illustration, painting, drawing, "
    "3d render, cgi, plastic skin, waxy skin, airbrushed, "
    "duplicate face, extra face, two heads, extra limbs, extra fingers, "
    "deformed hands, blurry, lowres, jpeg artifacts, text, watermark, signature, "
    "logo, gore, blood, horror, tiny face, distant figure, different face"
)

JOBS = [
    {
        "tag": "kf_1_descent",
        "seed": 9101,
        "image1": "Susanoo_bust.png",
        "image2": None,
        "prompt": (
            "Chest-up portrait of the man in Picture 1, same real face, completely hairless smooth "
            "shaved head, clean-shaven, light grey-green eyes, his face large and filling the lower "
            "half of the frame, sharp skin detail, calm fierce gaze looking downward as he descends "
            "through parting storm clouds, wearing a dark indigo storm-god cloak with a lightning-blue "
            "sash, wind lifting the cloak edge, rain droplets on his skin. Deep in the background, far "
            "below, a colossal eight-headed crimson dragon coils across misty valleys and hills, its "
            "many necks rising like hills, soft and out of focus. Low-angle heroic framing. "
            "Palette: deep teal, slate grey, crimson, electric blue. " + PHOTOREAL
        ),
        "negative": NEG,
    },
    {
        "tag": "kf_1_thunder",
        "seed": 9102,
        "image1": "Susanoo_bust.png",
        "image2": None,
        "prompt": (
            "Chest-up close portrait of the man in Picture 1, same real face, completely hairless smooth "
            "shaved head, clean-shaven, light grey-green eyes, his face large and filling most of the "
            "frame, sharp skin detail, looking up with fierce determination; dressed as a Japanese storm "
            "god in a dark indigo cloak with a lightning-blue sash. He raises both hands high and claps "
            "them hard above his head, arms lifting into frame, a ring of pale-blue lightning forking "
            "across the stormy night sky behind him, rain streaking through the light. Background softly "
            "blurred: dark pine forest clearing and the huge coiled crimson eight-headed dragon Orochi "
            "distant and out of focus. Chest-up heroic framing. "
            "Palette: deep teal, slate grey, crimson, electric blue. " + PHOTOREAL
        ),
        "negative": NEG,
    },
    {
        "tag": "kf_3_argument",
        "seed": 9103,
        "image1": "Susanoo_bust.png",
        "image2": None,
        "prompt": (
            "Chest-up dramatic portrait of the man in Picture 1, same real face, completely hairless "
            "smooth shaved head, clean-shaven, light grey-green eyes, his face large and clearly visible "
            "with sharp skin detail, standing fearless with one hand raised pointing forward, dark indigo "
            "cloak billowing in the wind, rain on his shoulders. Behind him in the lower background, eight "
            "crimson dragon heads rear up from the valley, fanged mouths open letting out smoke and "
            "sparks, ember light rimming their scales, softly blurred. Chest-up dramatic framing. "
            "Palette: deep teal, slate grey, crimson, ember orange. " + PHOTOREAL
        ),
        "negative": NEG,
    },
    {
        "tag": "kf_4_decision",
        "seed": 9104,
        "image1": "Susanoo_bust.png",
        "image2": KORY_CARD,
        "image3": "two_shot_start.png",
        "prompt": (
            "Intimate two-shot: the man in Picture 1, same real face, completely hairless smooth shaved "
            "head, clean-shaven, light grey-green eyes, and the woman in Picture 2, same real face, long "
            "red-black hair, smooth hairless female face, pale kimono, both faces large and clearly "
            "visible in the centre of the frame with sharp skin detail. He stands tall and resolute; she "
            "stands slightly behind him clasping her hands with hope. Pale dawn light breaks over the "
            "valley behind them, distant crimson dragon coiling and fading into shadow on a far hill. "
            "Intimate two-shot framing. Palette: soft gold dawn, deep teal, pale rose, slate grey. " + PHOTOREAL
        ),
        "negative": NEG,
    },
    {
        "tag": "kf_2_sword",
        "seed": 9105,
        "image1": "Susanoo_bust.png",
        "image2": KORY_CARD,
        "prompt": (
            "Waist-up medium action shot of the man in Picture 1, same real face, completely hairless "
            "smooth shaved head, clean-shaven, light grey-green eyes, his face large and clearly visible, "
            "sharp skin detail, lunging forward and swinging a gleaming white divine sword in a wide arc, "
            "cloak flaring, motion blur on the blade. Behind him a crashing wave of eight crimson dragon "
            "heads rears back, fanged mouths open, red scales glinting in dawn light. A woman with long "
            "red-black hair, smooth hairless female face, in a pale kimono, watches from behind a rock in "
            "the background corner, smaller and softly out of focus. Waist-up heroic action framing. "
            "Palette: deep teal, crimson, soft gold dawn, bone white. " + PHOTOREAL
        ),
        "negative": NEG,
    },
    {
        "tag": "kf_3_wedding",
        "seed": 9106,
        "image1": "Susanoo_bust.png",
        "image2": KORY_CARD,
        "image3": "two_shot_start.png",
        "prompt": (
            "Intimate medium close-up of the man in Picture 1, same real face, completely hairless smooth "
            "shaved head, clean-shaven, light grey-green eyes, in a clean indigo kimono with a "
            "lightning-blue sash, standing hand in hand beside the woman in Picture 2, long red-black "
            "hair, smooth hairless female face, in a pale wedding kimono, both faces large and clearly "
            "visible with sharp skin detail, smiling softly at each other. Background softly blurred: "
            "sunlit shrine courtyard with a red torii gate and villagers clapping and tossing white flower "
            "petals. Intimate two-shot framing. "
            "Palette: warm cream, indigo, crimson accents, spring green, sky blue. " + PHOTOREAL
        ),
        "negative": NEG,
    },
]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tools/vast/photoreal_jobs.json"
    for j in JOBS:
        n = len(j["prompt"])
        if n > 1400:
            raise SystemExit(f"{j['tag']}: prompt {n} chars exceeds the 1400 truncation limit")
    out.write_text(json.dumps(JOBS, indent=2))
    print(f"wrote {out} ({len(JOBS)} jobs)")
    for j in JOBS:
        print(f"  {j['tag']:16s} {len(j['prompt']):4d} chars  img1={j['image1']} img2={j['image2']} img3={j.get('image3')}")


if __name__ == "__main__":
    main()
