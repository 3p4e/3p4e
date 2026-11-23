# Idea One-Pager — #2: Wedding/Anniversary Myth Films (D2C)

> **Corrected copy (2026-11-23).** Original by Agent Zero (from `VAST_HANDOFF_PACKAGE.zip`). Changed figures are marked **[corrected 2026-11-23]**; reasons and sources are in `../MONETIZATION_REVIEW.md`. Measured basis: 126 LTX-2.5 clips cost $4.55 of Vast credit (~$0.04/clip in batch); 48 GB-class boxes cost $0.47-0.68/h all-in; each rental adds ~$0.30-0.60 setup; labor (3-8 h per B2B film) is the main cost. Prices marked (E) are estimates to validate with the first quotes.

> Sharpened from the idea-refine session. Status: pre-validation. Costs GROUNDED from VAST receipts.

## Problem Statement
**How might we** turn a couple's real faces into a 60-90 second cinematic myth film — their love story rendered as Orpheus & Eurydice, Psyche & Eros, or an original legend — as a premium gift/experience at a price no studio could ever offer?

## Recommended Direction
**"Your love story, as a myth."** A personalized short film: the couple's enrolled faces on mythic heroes, their names woven into the narration (MK/EN/multi via TTS), a cinematic 40-60-shot film in the VAST house style, delivered as a 4K-ready MP4 for weddings, anniversaries, proposals, and Valentine's.

**Why this is the sharpest D2C product VAST can build:**
1. **It uses the identity stack exactly as designed** — face cards → fused masters → LoRA/Ref2VA conditioning. The casting-pool doctrine (adult consented identities: DD/KORY/OLEG pattern) applies 1:1 to a couple's photos. No minor-consent problem — the blockers that gate idea #1 do not exist here.
2. **Emotional purchase economics** — weddings/anniversaries are the classic premium-gift market: buyers happily pay $150-500 for a one-of-a-kind artifact. Production cost is ~$8-15 GPU. Margin is 95%+.
3. **The catalog supplies the stories** — Greek myth (Psyche & Eros, Orpheus), Norse, and the 40-story public-domain library give ready-made romantic arcs; an "original legend" option uses the existing storyboard pipeline with the couple's details.
4. **Built-in viral loop** — the film is *made to be shown*: played at the wedding, posted to Instagram. Every delivered film is an ad with two highly-motivated distributors (the couple).

**Offer structure:**
| Tier | What | Price | Cost (GROUNDED) |
|---|---|---|---|
| **Myth Short** | 60-90s film, 1 story arc, couple's faces, names in narration | $150-250 (MK €150-350, EU €300-700 **[corrected 2026-11-23]**) | ~$3-6 GPU + keyframes + **4-8 h labor** **[corrected 2026-11-23]** |
| **Legend Feature** | 2-3 min, richer arc, custom scene (where they met), 2 wardrobe states | $300-500 | ~$6-12 GPU + keyframes + labor **[corrected 2026-11-23]** |
| **Proposal Cut** | 30-45s teaser for the proposal moment itself | $100-150 | ~$5-10 |
| **Anniversary Edition** | re-cut of the wedding film with "N years later" epilogue scene | $80-120 | ~$5-8 |

**Delivery:** photo intake (10-20 photos per person, screened per the face-card doctrine: real photos only, ≥256px faces, coverage check) → identity enrollment → story selection from catalog → storyboard → render → TTS narration with names → delivery in ~days. All steps are existing pipeline stages.

## Key Assumptions to Validate
- [ ] **A1 — Couples will pay $150-500 for this.** Test: a one-page site + 3 sample films (use DD/KORY as the demo couple — they already exist as enrolled personas). Pass: ≥5 paid pre-orders before building any new tooling.
- [ ] **A2 — Identity quality survives the emotional-judgment bar.** A wedding film judged "it doesn't quite look like us" is a refund, not a shrug. Test: render one demo film with the DD/KORY pair and show 10 people; ask "would you gift this?" Pass: ≥7 yes.
- [ ] **A3 — The 2-person identity-lock holds in shared frames.** Two distinct faces in one shot is the hardest case in the whole pipeline. Test: render 3 shared-frame shots early. Pass: both faces read correctly in all 3.
- [ ] **A4 — Intake friction is acceptable.** 10-20 photos + story choice + names must not kill the sale. Test: run 3 friends through a Google-Form intake. Pass: all complete it in under 15 min without help.
- [ ] **A5 — Privacy/consent wording is airtight.** Two adults consenting to their own likeness is simple, but wedding context involves families; the consent + retention policy must be explicit. Test: a lawyer-reviewed (or at least carefully drafted) consent form.

## MVP Scope
**In:** 3 catalog stories (Psyche & Eros, Orpheus & Eurydice, original legend), the DD/KORY demo film, a simple order form (photo upload + story choice + names + dates), manual production per order, MP4 delivery via Drive link.
**Out:** real-time preview, multiple film styles, same-week rush pricing, group/family versions, prints/physical media, a self-serve configurator, multilingual narration beyond MK/EN (+1 more at most).

## Not Doing (and Why)
- **No real children in the films** — the minor-consent doctrine is unsolved; child characters stay AI-default even in wedding films (e.g., "the couple's future" scenes use symbolic imagery, not real kids' faces).
- **No deceased-relative memorial films yet** — emotionally powerful but the consent/rights question (who consents for the deceased?) needs legal advice first.
- **No same-day turnaround promise** — quality gates (P1 identity proof per the KB) must run on every order; promising speed over identity is how slop happens.
- **No marketplace/aggregator listings yet (Etsy/Fiverr)** — own the customer relationship first; marketplaces commoditize and take 20%+.
- **No subscription model** — this is an event purchase; forcing recurrence adds churn math to a product that doesn't need it.

## Open Questions
- Face enrollment for a *one-off* customer: build a throwaway enrollment per order, or persist the couple's identity for the Anniversary Edition re-cut (with explicit consent)?
- What is the refund policy if the couple rejects the likeness? (Recommend: one free re-render, then 50% refund — identity quality is gate-checked before full render.)
- Do we need a separate P1-style proof gate per order (one still, couple approves before the full render)? Almost certainly yes — it's the KB's own law.

## Connection to the $1M path
At 10 orders/month averaging $250: $30k/yr on ~$1k/yr GPU. At wedding-season scale (30 orders/mo): $90k/yr. More importantly, it validates the identity-as-a-service thesis that underpins Direction A and Vector 5, generates the public proof-of-work for the methodology course, and every delivered film is a two-person marketing team. It also de-risks the eventual personalized-children's-film product (#1): by the time the minor-consent doctrine is written, the D2C machinery (intake, consent, billing, delivery) is already proven on adults.
