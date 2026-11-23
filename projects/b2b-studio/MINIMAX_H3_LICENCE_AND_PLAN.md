# MiniMax H3: licence check and comparison plan (2026-11-23)

Source: the licence text on the model card, `hf://models/MiniMaxAI/MiniMax-H3/LICENSE` (MiniMax H3 Community Licence, dated 2 August 2026), its `docs/QA-about-License.md`, and the model card README. Not legal advice; have a lawyer confirm before a paid client job.

## 1. What the licence actually says (open weights)

| Clause | Text (summary) | What it means for you |
|---|---|---|
| Territory (I.3, I.5, II) | Rights granted "solely within the Applicable Territory" = worldwide **minus EU, UK, South Korea, USA** | North Macedonia is inside the territory. You may run the weights here. |
| Use of Outputs (V.4, AUP 1) | You may not "use, reproduce, modify, distribute, or **display** the MiniMax H3 Works **or any of their Outputs** outside the Applicable Territory" | **The video itself may not be shown in the EU/UK/KR/US.** A clip on YouTube, Facebook, Instagram or a public website is viewable from the EU, so publishing openly online is a licence risk. Safe uses: in-store screens, TV/cinema in MK and non-excluded countries, trade fairs outside the excluded territories, geo-restricted posts. |
| Revenue cap (IV.1) | Written authorisation needed if **your** commercial products and services earn more than **US$20M a year** | Applies to the licensee, i.e. **you** (the studio), not to the client. Your studio is far below it, so Alkaloid's size alone does not block you. |
| Attribution (IV.2, III.3) | "Prominently display 'MiniMax H3'" on the UI of a commercial product or service that uses it; "Powered by MiniMax H3" and an AI-generation identifier are encouraged | Credit "Made with MiniMax H3" in delivery notes, your website and the client contract. |
| Pass-through terms (V.2) | Before giving access to the works or a product incorporating them, bind each recipient to terms at least as protective as section V and the Acceptable Use Policy | Put a clause in every client contract: no display or use outside the Applicable Territory, plus the AUP. |
| AI disclosure (AUP 12) | No public posting "without clearly and prominently disclosing that such … content is machine-generated" | Label published videos as AI-generated. |
| No training (V.3) | Outputs may not be used to improve another AI model | Do not use H3 clips to train LoRAs for LTX or anything else. |
| Governing law | Hong Kong | Disputes go to Hong Kong courts. |

## 2. Which companies can it be used for

The deciding question is **where the video will be shown**, not where the company sells or how big it is.

| Use of the video | Open-weights H3 |
|---|---|
| Screens in MK factories, shops, showrooms, local TV, MK trade fairs | Allowed (with attribution and AI label) |
| Geo-restricted social posts (MK and non-excluded countries only) | Allowed if the restriction really excludes EU/UK/KR/US |
| Open YouTube / website / Instagram / LinkedIn | **Risky**: viewable from excluded territories |
| EU trade fairs, EU distributor material, EU HQ use (e.g. automotive FDI plants, Alkaloid EU sales, Tikves EU exports) | **Not allowed** without a MiniMax licence |

So for export-heavy giants (Alkaloid, Makstil, Tikves, the automotive plants) H3 open-weights output can only be used for **domestic, offline** purposes. Mainly-domestic companies (Zito Luks ~2.5% exports, Pelisterka, OKTA/Makpetrol fuel retail, Usje) are better fits, but the **online-display** problem applies to them too.

## 3. The cleaner route: the hosted API

The licence FAQ says the hosted MiniMax API "remains globally available" with MiniMax's own safeguards. H3 is also offered through Higgsfield (`minimax_h3` 2K, 4-15 s, start + end frame; `minimax_h3_max` 768p). Hosted use is governed by the provider's API terms, not by the open-weights territory clause (V: read the MiniMax platform / Higgsfield terms for output use before a paid job).

Cost on Higgsfield (quoted today): **10 credits per 5 s clip at 2K** (`minimax_h3`), 12.5 credits for `minimax_h3_max`. Current Higgsfield balance: **10.19 credits = one clip**. A 10-company comparison (2 clips each) needs ~200 credits.

## 4. Self-hosting the open weights

- H3-Base is a 33B transformer plus a 32B Qwen3-VL text encoder, BF16; the official SGLang example uses **4 GPUs**. Plan for 4×80 GB (or 2×80 GB with offloading, slower) and a ~150 GB download.
- 2K output and the "Context-IR" prompt rewriter are **not** in the open release (API only); local output is 768p.
- That box class costs several dollars an hour on Vast; current Vast credit ($3.78) does not cover a session. The current 48 GB box cannot run it.

## 5. Comparison plan (LTX-2.5 vs MiniMax H3)

1. Pick the 10 companies from the research list; for each, 2 stages (hero + process) using the same start keyframes and the same prompt per stage.
2. LTX-2.5: render on our own box (~$0.05 per clip).
3. MiniMax H3: render through the hosted API (Higgsfield or MiniMax platform) with the same start frame (and end frame where used).
4. Side-by-side sheets and a short reel per company, marked **internal test, not for publication**.
5. Score: subject accuracy, motion quality, artefacts, prompt adherence, cost per usable clip.

Needed from you: top up Higgsfield (~200 credits for 20 H3 clips) or provide a MiniMax platform API key; image API credits (OpenAI is out of credits, Gemini keys are at quota) for the keyframes of companies not yet covered.
