# GTM Brief — Vector 3: B2B "AI-Film-as-a-Service"
> The cash engine. Evidence-grounded; cost bases from VAST box receipts + per-clip economics, market bases from Grand View Research (fetched live 2026-11-21).

---

## 1. WHAT WE SELL
Cinematic AI-generated video content for businesses that currently cannot afford it:
- **Digital signage / menu boards** for food venues (proven: Abracadabra case study)
- **Brand mascot design + animated clips** (ownable recurring character — the Fluent Device advantage)
- **Promo / product cinematics** for retail, salons, gyms, real estate, events
- **Educational / curriculum films** for schools, museums, cultural institutions (Balkan folklore is the differentiator)

**The pitch in one line:** "Studio-quality cinematic video at ~1% of the studio price, delivered in days, with an ownable brand character."

## 2. MARKET CONTEXT (GROUNDED — live fetch)
- **AI video generator market: $788.5M (2025) → $946.4M (2026) → $3,441.6M by 2033, CAGR 20.3%** (Grand View Research)
- The tooling is commoditizing fast; the **consistency + methodology + character IP** layer is where value concentrates — that is exactly what VAST owns.
- Traditional studio mascot/character animation: $10k-$50k. Traditional signage content: $500-$5,000/screen/yr. VAST's cost to produce: **under $25.**

## 3. IDEAL CUSTOMER PROFILE
| Tier | Who | Pain | Offer | Price |
|---|---|---|---|---|
| **Beachhead** | Single-location food venues (bakeries, grill bars, cafés) with 1-4 TVs | Static menu = invisible; can't afford studio video | Menu board package: board app + 10-35 item clips + 1 mascot + cinematics | $500-$1,500 setup + $50-150/mo |
| **Expansion** | Regional chains (3-15 locations) | Consistent brand across screens; HQ-controlled pricing | Multi-location package: shared assets + per-site board | $2,000-$5,000 setup + $200-500/mo |
| **Adjacent** | Retail / salons / gyms / real estate / event venues | Same attention problem, different content | Vertical-specific cinematics + mascot | $300-$2,000/project |
| **Institutional** | Schools, museums, cultural orgs | Need engaging folklore/myth/educational content | Per-film fee, curriculum licensing | $500-$5,000/film + license |

**Geographic wedge:** Macedonian-speaking market (North Macedonia + diaspora in DE/AT/CH/AU/US) — blue ocean, no scaled competitor, native-language advantage. Expand to Balkan region (Serbian, Bulgarian, Albanian, Greek) — same pipeline, swap TTS + text.

## 4. THE OFFER LADDER
```
FREE        →  5-min video call + a 1-clip sample of THEIR food/product (costs ~$0.17, zero risk)
STARTER     →  Mascot design + 5 clips                       $300-$500
CORE        →  Full menu board / signage package             $800-$1,500 + $50-150/mo
CHAIN       →  Multi-location rollout                        $2,000-$5,000 + $200-500/mo
RETAINER    →  Monthly content refresh (new promos, seasonal) $100-300/mo
INSTITUTIONAL → Curriculum film / folklore series licensing  $500-$5,000/film
```
**The free sample is the killer move:** a custom clip of the prospect's actual product costs $0.17 and ~1 hour of pipeline time. No competitor can match that demo economics.

## 5. UNIT ECONOMICS (GROUNDED)
| Item | Cost | Price | Margin |
|---|---|---|---|
| Menu board (10-35 clips + mascot + board app) | $10-25 GPU | $800-1,500 | **95-98%** |
| Mascot package (design + 5 clips) | $2-5 | $300-500 | **98-99%** |
| Monthly refresh (5-10 new clips) | $1-3 | $100-300 | **97-99%** |
| Institutional film (40-60 shots) | $8-15 | $500-5,000 | **97-99%** |

Even at 10 clients on the CORE tier: $8k-15k setup + $500-1,500/mo recurring, against ~$100-250/mo GPU cost. **Service margin is not the constraint — client acquisition is.**

## 6. SALES MOTION
**Channel 1 — Direct outreach (beachhead):**
- Walk-in / DM to 20 food venues in one city. Offer the free 1-clip sample.
- The Abracadabra board is the live proof: "go look at it on their TVs."
- Close 1-3 from 20 touches (INFERRED conversion — validate).

**Channel 2 — Referral / word-of-mouth:**
- Every board is a live demo visible to every neighboring business. Put a tiny "Made by VAST" watermark or QR on the board's idle screen.

**Channel 3 — Signage installers / AV integrators:**
- Partner with the companies that already sell and install commercial displays. They need content; VAST supplies it. Revenue-share per referral.

**Channel 4 — Institutional RFPs:**
- Museums, schools, cultural ministries periodically fund folklore/educational media. The 40-story public-domain catalog + the "Волшебната книга" season blueprint is a ready-made proposal asset.

## 7. DELIVERY OPERATIONS (leverages existing VAST tooling)
1. Client fills a form (items + prices + brand colors + mascot preference)
2. Pipeline generates food/product keyframes (Qwen-Image-Edit) + mascot keyframes
3. Motion clips rendered on vast.ai (LTX-2.5 primary, Kandinsky 6 / Wan 2.2 fallback) — ~$0.01-0.17/clip (LTX-2.5 est. on A6000; Wan2.1 lead route $0.166 grounded, KB §9)
4. Board HTML configured with client data (menu-data.js swap)
5. Deployed on client VPS, USB stick, or a VAST-hosted KVM4 container
6. Client edits prices via Google Sheet CSV — zero ongoing VAST labor
7. Monthly retainer: generate new promo clips, update board

**Delivery is the existing pipeline, not new engineering.**

## 8. RISKS & MITIGATIONS
| Risk | Mitigation |
|---|---|
| Service revenue scales linearly with attention | Productize: the board app + clip_spec template should require near-zero custom code per client; prioritize monthly-retainer (low labor) over one-off builds |
| Client acquisition slower than projected | The free-sample demo is nearly free; volume outreach is cheap; signage-installer partnerships bypass direct sales entirely |
| Model deprecation breaks the pipeline | Model-agnostic design (already proven on 6 models); keyframes are model-independent assets that survive any motion-model swap |
| Price erosion as AI video gets cheaper | VAST's moat is the methodology + character IP + consistency, not the raw clip. Compete on the ownable mascot + reliability, not per-clip price. |
| Privacy/IP exposure from client assets | Same doctrine as the film work: consent, hash-locked assets, no biometrics committed. |

## 9. VALIDATION GATES (do not scale on hope)
| Gate | Test | Pass signal |
|---|---|---|
| G1 | 20 direct outreach + free samples | ≥1 paying client |
| G2 | 3 paying clients | ≥1 agrees to a monthly retainer |
| G3 | 90 days of operation | Delivery time per client decreasing (productization working) |
| G4 | 10 paying clients | CAC payback < 90 days |
| G5 | 1 signage-installer partnership signed | Referral pipeline producing qualified leads |

**Pivot trigger:** if G1 fails across 60+ touches in 2 cities, the B2B menu-board wedge is wrong — pivot to institutional/educational films (higher price, longer cycle, less competition) or to Vector 5 (personalized films D2C).

## 10. CONNECTION TO THE $1M PATH
B2B studio is the cash engine that funds the slower-compounding vectors:
- B2B revenue funds the 23-episode children's season (Vector 1) production.
- The B2B client roster becomes the audience/proof for the methodology course (Vector 4).
- The mascot/identity capability proven in B2B becomes the personalized-film product (Vector 5).
- Target: $150k-$500k revenue over the plan horizon (per MONETIZATION_STRATEGY_1M.md §4), at 95%+ gross margin.