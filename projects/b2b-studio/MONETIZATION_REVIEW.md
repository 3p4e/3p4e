# Monetization review and corrections (2026-11-23)

Reviewed: Agent Zero's `MONETIZATION_STRATEGY_1M.md`, `GTM_BRIEF_B2B_STUDIO.md`, `CONSTRUCTION_VIDEO_PRODUCT.md`, `IDEA_C_SMB_MASCOT_RETAINER.md`, `IDEA_2_WEDDING_MYTH_FILMS.md`, `G1_LAUNCH_KIT_BER_LON_PAR_BRU.md`, `B2B_CASE_STUDY_ABRACADABRA.md` (from `VAST_HANDOFF_PACKAGE.zip`) and the "$1M roadmap" answer in the Agent Zero chat.

Verdict: the strategy's direction is sound (sell production as a service first, use the Abracadabra board as proof, validate before scaling). The numbers are not. Costs are understated, prices for B2B video are set far too low, labor is missing from every margin, and the $1M target is not reachable by one operator in North Macedonia on the stated plan. Corrections below; replace the affected figures in those documents.

Labels: **M** = measured in this project, **E** = my estimate (validate), **V** = needs verification before use.

---

## 1. Corrected cost base

| Item | Agent Zero docs say | Correct figure | Basis |
|---|---|---|---|
| GPU hourly rate | A6000 ~$0.20/h, 3090 ~$0.18/h | **$0.47-0.68/h** all-in (`dph_total`) for 48 GB-class boxes today; cheapest suitable offers start ~$0.50/h | M: today's rentals 62111380 (~$0.47/h), 62218733 ($0.68/h), 62228169 ($0.62/h) |
| GPU cost per LTX-2.5 clip | "$15-20/clip" (construction doc, your brief) and "$0.01-0.03" (case study) | **~$0.04 per clip in a batch**, including setup | M: 126 Abracadabra v3 clips (169-193 frames) cost $4.55 Vast credit in total |
| Session overhead | not counted | **~$0.30-0.60 per rental** (boot + ~35 GB weight download + ComfyUI start, 20-40 min) | M: today's provisioning times |
| Failed rentals | not counted | **real and recurring**: today's SSH failures and the broken template cost the account roughly $3-4 before a clip was rendered | M: credit went $12.03 → $4.89 across the day for ~126 delivered clips plus failures |
| Keyframe images | "~$1-3" / not counted | **paid per image**, OpenAI `gpt-image-2` high quality at 1536x1024; take the exact rate from your OpenAI billing page | V: per-image price not tracked in this project |
| "Free sample costs $0.17" | $0.17 | **~$1-3 in cash plus 30-60 min of your time** for a one-off sample (rental overhead dominates); ~$0.30 each only when 5-10 samples share one rental | E from M above |
| "$0.40 for the 12-clip construction batch" | $0.40 | **~$0.80-1.20** for the batch on one box, plus keyframes | E: ~1.2-1.8 h at $0.62/h |

**The "$15-20 per clip" figure is wrong by about 400x** and was then used as the *price* in `CONSTRUCTION_VIDEO_PRODUCT.md` ("8-clip timelapse ~$120-160"). That is cost and price confused, and it would underprice the product by an order of magnitude.

What actually drives cost is **your time**: brief, keyframe iterations (expect 2-4 rounds per stage), QC, edit, music, logo/CTA, revisions, delivery. Plan **3-8 hours per B2B film**, more for the first ones.

## 2. Margins: what "95-98%" really means

The docs quote 95-99% margins by dividing GPU cost by price. That is GPU-only gross margin. A real margin has to include, per project:
- labor (above), the dominant cost
- keyframe image API, GPU incl. overhead and failures
- tools/subscriptions (OpenAI, Higgsfield, hosting, KVM4), music licences
- sales time (outreach, meetings, proposals), revisions, VAT/taxes, payment fees

Restated: GPU + API are ~1-3% of price; **contribution margin after your time is what matters**, and it depends entirely on hours per project. Track hours from the first client.

## 3. Pricing corrections (North Macedonia first; EU in brackets)

All **E**, to be validated with the first 5 quotes. Price on the value to the buyer (what a local agency or video crew charges), not on GPU cost.

| Product | Agent Zero price | Suggested starting price | Note |
|---|---|---|---|
| Construction timelapse film (8 stages, 40-60 s, edited, music, logo, 16:9 + 9:16 cut) | $120-160 | **€900-2,500** (EU €2,500-6,000) | developers spend far more on renders and drone footage; this replaces both for pre-launch marketing |
| Empty→furnished apartment reel (per layout) | $60-80 | **€250-600 per layout**, package of 3-5 layouts €900-2,000 | sold to developers and agencies per project |
| Renovation before/after | none | **€300-800** | contractors, trade-show loops |
| Car dealer launch pack (e.g. Foton: launch film + 3 model spots + 10 social cuts) | none | **€1,500-3,500** + optional **€400-900/mo** content | brand permission required, see §6 |
| Industrial / FDI recruitment or brand film | "$20K/project" | **€2,000-6,000** in MK; €20K is only realistic with EU HQ budgets via their agencies | most FDI plants' marketing is decided at HQ |
| Menu board (Abracadabra-type) | $500-2,000 + $50-150/mo | **€600-1,500 setup + €40-100/mo** in MK | proven; keep |
| SMB mascot + monthly clips | $100-300/mo | **€120-250/mo** in MK, 3-month minimum | churn is the risk |
| Wedding myth film | $150-500 | MK **€150-350**; EU €300-700 | needs a likeness-approval step before full render |

## 4. The $1M target, recomputed

Agent Zero's table ("400 SMB retainers at $200/mo = $960K", "50 enterprise projects at $20K") ignores capacity and market size:
- 400 retainers at the doc's own ≤1 h/client/month = **400 h/month = ~2.5 full-time people** just for production, plus sales to win and replace churned clients.
- 50 × $20K projects in North Macedonia: the research found ~100 named enterprise prospects in total; most will not buy, and few will pay $20K for AI video.
- The strategy says "$1M profit" but every table is **revenue**; costs (labor, team, tools, tax) are never subtracted.

Realistic year-1 for one operator (**E**): e.g. 12 B2B projects × €1,500 + 8 retainers × €200 × 12 + 2 menu boards ≈ **€40-50K revenue**. $1M revenue needs roughly 400-500 projects a year at ~€2K (about 9 a week), i.e. a team of 5-8 and clients outside North Macedonia: a 3-5 year build, not a first-year plan. Keep $1M as the long-term goal; manage to quarterly targets (first paying client, first retainer, €5K/month run rate, then hire).

## 5. Focus corrections

1. **Too many fronts for one operator.** The docs run 7 vectors, 3 product ideas and a 4-city EU walk-in campaign at once. Pick **one beachhead**: North Macedonian B2B (construction/developers, car dealers, F&B), where you speak the language, can visit in person, and have the Abracadabra proof and the research list.
2. **Drop the Berlin/London/Paris/Brussels walk-in plan for now.** Walk-ins in four foreign cities from Skopje are not executable cheaply; revisit with remote diaspora outreach once MK has 3+ paying clients and a portfolio.
3. **TAM framing is wrong.** "AI video generator market $788.5M" is the market for *tools* (who sells software), not for your service. Your market is local video production and marketing spend of MK companies; size it bottom-up from the prospect list × realistic budget.
4. **Demo reels before outreach.** Build the construction and apartment reels (rendering now), the Foton pitch pack, and one industrial clip; use them in every pitch.
5. **Kids' YouTube (Vector 1) is the weakest stream.** Made-for-kids videos earn very low ad revenue, discovery is slow, and YouTube's monetization policy targets mass-produced/repetitive content (V: re-read the current YPP policy before investing). Treat it as long-term brand building, not cash.

## 6. Legal and licence checks (do before selling)

- **LTX-2.5 licence** (V): confirm the commercial-use terms and any revenue threshold in the current Lightricks licence for the model you deploy; record it in the repo.
- **Image API outputs** (V): confirm your OpenAI plan's terms for commercial use of generated images (generally allowed; verify for your account).
- **Real brands and products** (Foton, Alkaloid etc.): private pitch samples are fine; publishing or using their product images needs written permission (dealer plus confirmation they may approve use of the trademark).
- **AI disclosure** (V): the EU AI Act transparency rules for AI-generated or manipulated content apply from 2 August 2026; North Macedonia aligns with EU law and many clients sell into the EU. Add a "contains AI-generated imagery" line to contracts and, where required, to the video.
- **Faces / personal likeness** (wedding films, recruitment films with real staff): written consent, retention period, deletion on request (GDPR in EU; North Macedonia's personal data protection law is GDPR-aligned).
- **Music**: licensed tracks only; note licence per delivery.
- **Avoid MiniMax-H3** for anything published: its licence excludes several territories and prohibits display there.

## 7. Corrections to `B2B_CASE_STUDY_ABRACADABRA.md`

- Clip count: the live board now has **126 per-item and ambient clips** (62 items × wand cast + summon, plus 2 ambient), not "35 planned".
- Keyframes for v3 were made with **OpenAI gpt-image-2**, not Qwen-Image-Edit.
- GPU rate: **$0.47/h** (A6000, `dph_total`), not $0.20/h; total v3 Vast spend **$4.55**.
- "Under $25 total project cost" is GPU-only; state labor separately.
- The System1 "Fluent Device" claim: keep only with a citation link (V).

## 8. Next 30 days (replaces the G1 launch kit for now)

1. Finish the construction + apartment demo reels (box rendering now) and cut a 45 s showreel.
2. Fix the Foton V7 and truck keyframes; render the Foton pitch clips; get the dealer meeting.
3. Make a one-page price sheet from §3 (MKD and EUR).
4. Contact 15 MK prospects from the research list (5 developers, 5 contractors/interior studios, 5 F&B/retail), in person or by phone where possible.
5. Track per project: hours, GPU/API cost, price, outcome. Re-price after the first 5 quotes.

Gate: by day 30, at least 2 paid projects or 1 retainer. If not, change the offer (price, format, vertical) before spending more on GPU.
