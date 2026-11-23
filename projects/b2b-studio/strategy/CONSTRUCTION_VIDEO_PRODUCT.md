# Construction & Interior Video Product Concept

> **Corrected copy (2026-11-23).** Original by Agent Zero (from `VAST_HANDOFF_PACKAGE.zip`). Changed figures are marked **[corrected 2026-11-23]**; reasons and sources are in `../MONETIZATION_REVIEW.md`. Measured basis: 126 LTX-2.5 clips cost $4.55 of Vast credit (~$0.04/clip in batch); 48 GB-class boxes cost $0.47-0.68/h all-in; each rental adds ~$0.30-0.60 setup; labor (3-8 h per B2B film) is the main cost. Prices marked (E) are estimates to validate with the first quotes.


## Origin
Director idea (2026-11-23): timelapse-style building construction videos and empty→furnished apartment transformations for construction companies, real-estate developers, and interior-design firms.

## Technical Validation

### ❌ NOT single-clip morph
LTX-2.5 I2V with one start frame cannot hold a foundation→skyscraper state change across 121 frames — it smears/morphs.

### ✅ Stage-keyframe concat (proven pipeline)
**[corrected 2026-11-23]** 2026-11-23 run: keyframes made with gpt-image-2 by editing the previous stage's image (same camera, same plot), then one LTX-2.5 clip per stage (1280x704, 121 f, start strength 0.7); ~96 s per clip on an RTX 6000 Ada.
- Generate ONE keyframe per construction/furnishing stage (7-8 for a building: excavation → foundation → frame → shell → envelope → MEP rough → fit-out → handover; 4 for interior: empty shell → furniture wave 1 → wave 2 → styled)
- Each keyframe rendered as a subtle-motion 121f clip (camera drift, dust motes, light shift — "held ending" per 67 §2)
- Hard-concatenate clips → reads as timelapse when cut fast
- Zero new tech: exactly the keyframe-anchored pipeline that produced the Sunder fill batch

## Product Variants
| Variant | Stages | Clips | Use case |
|---|---|---|---|
| **Construction timelapse** | 7-8 (excavation → handover) | 7-8 × 121f | Developer marketing, investor decks, permit videos |
| **Empty→furnished apartment** | 3-4 (shell → styled) | 3-4 × 121f | Interior-design portfolio, real-estate staging, Airbnb listings |
| **Renovation before/after** | 2-3 (demo → rough-in → finished) | 2-3 × 121f | Contractor case studies, trade-show loops |

## Macedonian Buyer Targets **[corrected 2026-11-23]**
Verified list (see `../B2B_RESEARCH_AND_PROMPTS.md`): developers Adora Engineering, Limak, Balfin/Skopje East Gate, Granit (own projects), New Way Construction; contractors Granit AD (2024 revenue MKD 3.87bn), Krmzov-MR, Turmak, Stenton, Zikol, Energogroup; interior studios Atmosly, AMATA, KL Studio, Krug, GVRL+. In the original list below, Beton AD was delisted in 2023 after bankruptcy, Eurokompozit/Makprogres/"Inženjering" could not be verified, and Alkaloid/Makedonijaturist are not construction buyers.

### Original list (superseded)
*Live search failed today — names below are training-knowledge roster, sizes unverified. Must verify before outreach.*

### Construction / Developers
- **Granit AD Skopje** — construction, MSE-listed
- **Beton AD** — heavy civil
- **Eurokompozit** — prefab/modular
- **Makprogres** — residential/commercial
- **Inženjering** — EPC

### Real-Estate / Interior
- **Alkaloid** — own facilities, campus videos
- **Makedonijaturist** — hospitality fit-outs
- **Local interior-design studios** — portfolio reels

## Pricing (fits B2B studio vector)
- **[corrected 2026-11-23]** 8-stage construction timelapse film (40-60 s, edited, music, logo, 16:9 + 9:16): **€900-2,500** in MK (E), EU €2,500-6,000. GPU cost ≈ $1-2 per batch (~$0.04/clip + setup); the original "$15-20 unit cost" was wrong by ~400x and the price below it confused cost with price.
- **[corrected 2026-11-23]** Empty→furnished reel: **€250-600 per layout**, 3-5 layout package €900-2,000 (E). Renovation before/after: €300-800 (E).
- Delivered as MP4 + source keyframes for client archive

## Next Steps
1. Verify buyer names via live sources when search recovers
2. Build 2 demo reels (construction + apartment) after current render batch
3. Add to GTM launch kit (Berlin/London/Paris/Brussels wedge)

---
*Filed 2026-11-23 16:55 CET alongside MONETIZATION_STRATEGY_1M.md, GTM_BRIEF_B2B_STUDIO.md, B2B_CASE_STUDY_ABRACADABRA.md*
