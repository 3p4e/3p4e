# Construction & Interior Video Product Concept

## Origin
Director idea (2026-11-23): timelapse-style building construction videos and empty→furnished apartment transformations for construction companies, real-estate developers, and interior-design firms.

## Technical Validation

### ❌ NOT single-clip morph
LTX-2.5 I2V with one start frame cannot hold a foundation→skyscraper state change across 121 frames — it smears/morphs.

### ✅ Stage-keyframe concat (proven pipeline)
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

## Macedonian Buyer Targets (verification pending)
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
- 8-clip construction timelapse: ~$120-160 (8 × $15-20 unit cost at A6000)
- 4-clip apartment fill: ~$60-80
- Delivered as MP4 + source keyframes for client archive

## Next Steps
1. Verify buyer names via live sources when search recovers
2. Build 2 demo reels (construction + apartment) after current render batch
3. Add to GTM launch kit (Berlin/London/Paris/Brussels wedge)

---
*Filed 2026-11-23 16:55 CET alongside MONETIZATION_STRATEGY_1M.md, GTM_BRIEF_B2B_STUDIO.md, B2B_CASE_STUDY_ABRACADABRA.md*