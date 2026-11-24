# Idea One-Pager — C: SMB Mascot + Content Retainer (beyond food)

> **Corrected copy (2026-11-23).** Original by Agent Zero (from `VAST_HANDOFF_PACKAGE.zip`). Changed figures are marked **[corrected 2026-11-23]**; reasons and sources are in `../MONETIZATION_REVIEW.md`. Measured basis: 126 LTX-2.5 clips cost $4.55 of Vast credit (~$0.04/clip in batch); 48 GB-class boxes cost $0.47-0.68/h all-in; each rental adds ~$0.30-0.60 setup; labor (3-8 h per B2B film) is the main cost. Prices marked (E) are estimates to validate with the first quotes.

> Sharpened from the idea-refine session. Status: pre-validation. Costs GROUNDED from VAST receipts.

## Problem Statement
**How might we** give any local SMB (salon, gym, bakery, retail shop) an ownable animated brand character with a steady stream of cinematic social content, at a price a traditional studio can't come close to and a DIY AI tool can't match in consistency?

## Recommended Direction
Productize the Abracadabra mascot pipeline as a standalone offer, minus the menu board:
**"Your business gets a living brand character + 4-8 fresh cinematic clips a month."**

The proof already exists: Абра (the wand) was designed, keyframed, animated, and deployed for a real venue — the hardest parts (character consistency, anti-slop quality, motion rendering at **[corrected 2026-11-23]** ~$0.04/clip (LTX-2.5 batch, measured), batch prompt templates in `clip_specification.json`) are solved and documented. A non-food SMB has the same attention problem as a restaurant: a static Instagram grid or printed poster is invisible, and $10k+ studio mascot work is out of reach.

**Offer structure:**
| Tier | What | Price **[corrected 2026-11-23]** (MK: about 60-80% of these; retainer €120-250/mo) | Cost to deliver (GPU/API only; add ~1 h labor/client/month) |
|---|---|---|---|
| **Character design** | Mascot concept → 3 options → client picks → locked design sheet (the VAST face/look-card method) | $200-400 | ~$1-3 keyframes |
| **Starter clips** | 5 signature clips (intro, product-in-action, promo, seasonal) | $300-600 | ~$1-2 clips |
| **Monthly retainer** | 4-8 new clips/mo + 2 stills, delivered as social-ready MP4s | $100-300/mo | $1-6 GPU/mo |
| **Refresh/redesign** | Seasonal wardrobe/stage variant of the mascot | $100-200 | ~$1-3 |

**Delivery is the existing pipeline:** mascot keyframes **[corrected 2026-11-23]** (gpt-image-2 or Qwen-Image-Edit) → motion clips (LTX-2.5, Kandinsky 6 fallback) → watermark-free MP4s → client posts. No board app, no hosting, no screens needed — which makes this the *lightest* VAST product (pure content, zero deployment).

**Beachhead (diaspora wedge, per the GTM brief):** Balkan-owned businesses in Berlin/London/Brussels/Paris — barbers, beauty salons, gyms, bakeries — where the pitch can be made in MK/Albanian/Serbian + local language and where an ownable character is a genuine novelty. Then general SMBs in the same cities.

## Key Assumptions to Validate
- [ ] **A1 — SMB owners perceive mascot content as worth $100-300/mo.** Test: 10 walk-ins/DMs with a phone-screen sample clip (cost ~$0.17 each). Pass: ≥2 ask for pricing.
- [ ] **A2 — Quality bar holds without a venue context.** The Abracadabra clips were graded against a real brand brief; generic SMB clips have no such anchor. Test: render 3 generic clips (barber chair, gym kettlebell, bakery croissant) and A/B them against the Абра clips with 5 non-involved viewers. Pass: rated comparably.
- [ ] **A3 — Churn stays low.** Retainer economics die if clients cancel after month 1. Test: structure first 3 clients on a 3-month minimum. Pass: ≥2 renew past month 3.
- [ ] **A4 — Production stays under ~1h/client/month.** Test: time the full monthly cycle for pilot clients. Pass: ≤1h excluding render wait (render is unattended).
- [ ] **A5 — Clients can self-serve posting.** Test: deliver MP4s via a shared Drive folder. Pass: zero "how do I post this?" support requests.

## MVP Scope
**In:** one mascot concept pipeline (design sheet → 5 starter clips), 3 pilot clients from the diaspora wedge, shared-folder delivery, manual monthly cycle (no dashboard), the 3-month-minimum retainer structure.
**Out:** self-serve portal, subscription billing automation, vertical-specific templates beyond the pilot 3, multi-mascot bundles, advertising clips for paid media (rights questions), white-label licensing to agencies.

## Not Doing (and Why)
- **No menu boards / screens** — that's the food-vertical product; mixing them confuses the offer.
- **No real-time / interactive content** — different engineering, no demand evidence.
- **No usage-based pricing** — flat monthly is what an SMB owner can reason about; metering adds friction with no upside at this scale.
- **No child-facing mascots for third parties yet** — the minor-consent doctrine question is unsolved; adult-audience SMBs only.
- **No custom audio/jingles per client** — MK/EN TTS exists but bespoke music rights are a rabbit hole; music-free or licensed-track clips first.

## Open Questions
- Who is the legal counterparty for EU consumer-facing brand content — does any client contract need GDPR/GDPR-adjacent clauses for their customer data (likely no, since we only handle the client's brand assets)?
- Can the Абра prompt templates be abstracted into a mascot-agnostic template (theme/gesture slots) in under a day of tooling?
- Do we watermark pilot clips, and at what client tier does the watermark drop?

## Connection to the $1M path
Direction C is the cash-flow engine: 20 retainer clients at $150/mo average = $36k/yr recurring on ~$500/yr GPU cost. It also seeds the audience and proof for Direction A (personalized films) and the methodology course (Vector 4).

