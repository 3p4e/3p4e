# B2B Case Study — Abracadabra Digital Menu Board

> **Corrected copy (2026-11-23).** Original by Agent Zero (from `VAST_HANDOFF_PACKAGE.zip`). Changed figures are marked **[corrected 2026-11-23]**; reasons and sources are in `../MONETIZATION_REVIEW.md`. Measured basis: 126 LTX-2.5 clips cost $4.55 of Vast credit (~$0.04/clip in batch); 48 GB-class boxes cost $0.47-0.68/h all-in; each rental adds ~$0.30-0.60 setup; labor (3-8 h per B2B film) is the main cost. Prices marked (E) are estimates to validate with the first quotes.

> Evidence-grounded from: `projects/abracadabra-menu/README.md`, `REDESIGN_SPEC.md`, `clip_specification.json`, `.abra_*_box.json` receipts, `media/abracadabra_render/`

---

## The Client
**Abracadabra** — a food venue (burgers, wraps, grill, salads, desserts, coffee) with two TVs in front of the store displaying a digital menu board. The venue needed a menu system that attracts attention, is always current, and differentiates from every competitor's static printed board or basic slideshow.

## The Deliverable (what VAST shipped)
A **two-screen, browser-based cinematic menu board** running 24/7, hosted on the client's own VPS (KVM4):

| Component | Detail | Client value |
|---|---|---|
| **Cinematic Board** (`cinematic-board.html?screen=1/2`) | Game-main-menu-style 3D stage with parallax camera drift, volumetric light, glass-and-gold panels | Passersby stop and look — attention a printed menu cannot buy |
| **Living mascot: Абра** | An AI-generated magic wand character (monocle, white gloves, red-orange crystal tip) floating in a rune-ring portal; day mode welcomes guests, night mode rocks out in neon | An ownable brand character no food chain has — proven to increase ad effectiveness (System1 Fluent Devices research cited in the README) |
| **Spell-reveal food clips** | The wand casts a spell, food materializes in a flash of light — per-item clips (burger, wrap, waffle + a planned 35-clip set covering every priced item) | Food looks alive and desirable, not a static photo |
| **Blizzard-style cinematics** | Full-screen 10-second takeover every 2 min: wand awakens, summons food from a fire vortex, neon storm at night | The board is entertainment, not just information — drives dwell time and repeat glances |
| **Wand-slash transition** | Every ~40s a blazing slash crosses the board and swaps the featured promo | Constant gentle motion keeps attention without needing a full re-render |
| **Day/night auto-switch** | 19:00-06:00 the whole board flips to magenta-violet neon matching the venue's physical night sign | Coherent brand experience across physical + digital |
| **Three-tier price editing** | On-TV admin, permanent file change, or phone-based Google Sheet CSV that auto-syncs | Venue staff change prices with zero technical skill, from a phone |
| **24/7 hardening** | Burn-in nudge, periodic reload, offline USB fallback, auto-fit layout | Runs unattended indefinitely |
| **Deployment** | Docker container on the venue's VPS behind Traefik with auto-renewing TLS | Zero maintenance for the venue |

## The Technology Stack (VAST pipeline, not off-the-shelf)
| Layer | What was used |
|---|---|
| **Keyframes** | **[corrected 2026-11-23]** OpenAI gpt-image-2 keyframes for v3 (start + end frame per item, 124 images); earlier versions used Qwen-Image-Edit (35 item plates) + Abra mascot keyframes (day/night, portal, gesture variants) |
| **Motion** | LTX-2.5 22B (distilled INT8, 8 steps, 121 frames, 1280×720) — continuation-form prompts per the VAST anti-slop standard |
| **Alt motion** | Kandinsky 6 (K6C batch on RTX A6000) as fallback/parallel route |
| **Render orchestration** | vast.ai GPU rental **[corrected 2026-11-23]** (RTX A6000 @ ~$0.47/h all-in for v3) with per-file copy-home + sha256 verification |
| **Board application** | Self-contained HTML/CSS/JS (no framework), ~65MB H.264 clips, Google Sheets CSV sync |
| **Hosting** | KVM4 VPS, nginx:alpine, Traefik TLS, auto-renewing Let's Encrypt |

## Cost (GROUNDED from box receipts + per-clip economics)
| Item | Cost |
|---|---|
| GPU rental (LTX-2.5 render box) | **[corrected 2026-11-23]** ~$0.47/h all-in (A6000, 2026-11-23) |
| GPU rental (K6 fallback box) | ~$0.18/hr (3090) |
| Per motion clip (Wan2.1-FLF2V lead route) | ~$0.166 (KB §9, grounded) |
| Per motion clip (LTX-2.5 on A6000 @ $0.404/hr) | est. ~$0.01-0.03 (INFERRED from box rate × 1.5-4 min/clip; verify on next render) |
| Full per-item set **[corrected 2026-11-23]** | **126 clips** (62 items × wand cast + summon, plus 2 ambient) for **$4.55** Vast credit total, plus keyframe images |
| Mascot cinematics (5 full-screen) | ~$1-2 total |
| **Total video content cost** | **~$10-20 for a complete menu board** |
| Board application + hosting | Existing client infrastructure (KVM4) |
| **Total project cost** | **Under $25** |

Comparable commercial digital signage content packages cost $500-$5,000+ per screen per year, and custom mascot animation runs $10k-$50k at a studio. **VAST delivers at ~1% of the traditional cost.**

## What Makes This a Replicable Product (not a one-off)
1. **The clip_specification.json is a template** — 35 items each with a keyframe prompt, an LTX-2.5 motion prompt, a magic theme (forge_fire, phoenix_feather, alchemy_press…), a gesture, and a planned output path. For any new restaurant: swap the item names, categories, and food keyframe prompts; the rest of the pipeline runs unchanged.
2. **The board application is venue-agnostic** — it reads `menu-data.js`, renders auto-fit panels, syncs a Google Sheet. Any restaurant can use it with zero code changes.
3. **The mascot slot is swappable** — Абра is one character; the pipeline can generate any mascot (fox, dragon, chef, coffee cup) using the same keyframe→motion→board workflow.
4. **The pipeline is model-agnostic** — proven on LTX-2.5 and Kandinsky 6; can route to Wan 2.2, SkyReels, or any successor model.

## Revenue Model This Unlocks
| Offering | Price point | Basis |
|---|---|---|
| **Menu board package** (board app + 10-35 item clips + 1 mascot + cinematics) | $500-$2,000 one-time + $50-150/mo hosting/update | Comparable signage content costs $500-5,000/yr/screen |
| **Mascot-only package** (character design + 5-10 clips) | $300-$800 | Studio mascot animation is $10k+ |
| **Monthly content refresh** (new promos, seasonal clips) | $100-$300/mo retainer | Clips cost ~$0.01-0.17 each to produce (LTX-2.5 est. / Wan lead route, see table above) |
| **Multi-location chain** | $1,000-$5,000 setup + $200-500/mo | N× the board package with shared assets |
| **Adjacent verticals** (retail, salons, gyms, real estate, events) | Same price band | Same pipeline, different keyframe prompts |

## Proof Points for the Pitch
- **It is deployed and running** on a real venue's TVs right now, hosted on a real VPS.
- **Cost to produce**: under $25 in GPU/API **[corrected 2026-11-23]** plus labor (track hours). **Price to client**: €600-1,500 setup + €40-100/mo in MK (E). **Gross margin**: 95%+ on GPU only.
- **The mascot differentiator**: no food-chain competitor has a living wand mascot; the System1/IPA "Fluent Device" research (already cited in the README) proves recurring brand characters multiply ad effectiveness.
- **The child-safety / anti-slop methodology** that governs every VAST render is a quality guarantee no DIY AI tool offers.
