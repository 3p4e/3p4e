# Delivery and licence templates

Templates for handing finished commercials to a client after a sale. Fill the `[ ]` fields per job.
These are working templates, not legal advice: have a local lawyer check the licence text once before first use.

## 1. Delivery package (per film)

| File | Spec | When |
|---|---|---|
| `<client>_<film>_16x9_1080p.mp4` | 1920×1080, H.264 High, CRF 16–18, 24/25 fps, AAC 48 kHz 320 kbps, −16 LUFS (web) | always |
| `<client>_<film>_9x16_1080p.mp4` | 1080×1920, same codecs | always |
| `<client>_<film>_1x1_1080p.mp4` | 1080×1080 (feed) | Launch / Monthly |
| `<client>_<film>_4x5_1080p.mp4` | 1080×1350 (Meta feed) | Launch / Monthly |
| `<client>_<film>_TV.mp4` / `.mov` | 1920×1080 25 fps, −23 LUFS (EBU R128), ProRes 422 HQ or H.264 at the station's spec | only if TV is licensed |
| `<client>_<film>_<lang>.srt` | subtitles, one file per language | always |
| `<client>_<film>_nomusic.mp4` | voice-over and sound only, no music | on request |
| `<client>_<film>_clean.mp4` | no voice-over, no captions (for their own edits) | Launch and above |
| `<client>_<film>_poster.jpg` | 1920×1080 thumbnail | always |
| `LICENCE_<client>_<date>.pdf` | signed licence sheet (section 3) | always |

Rules:
- Pitch copies carry the "КОНЦЕПТ" watermark and the studio intro and outro. Sale masters carry neither.
- Pitch copies are 720p. The 1080p masters are made only after the sale: upscale the approved cut, then re-check faces, text and logos frame by frame.
- Logos, packs and end cards come from the client's official files, never from AI output.
- Delivery by private link (download expires after 14 days), plus a USB stick if the client wants one.

## 2. Versions and corrections

- Included: 1 round of corrections after the key frames, and 1 round after the first cut.
- Text, voice-over, music and end-card changes are cheap. Re-generating shots costs extra: quote per shot.
- Naming: `v1` first cut, `v2` after corrections, `FINAL` after written approval. Keep every version for 12 months.

## 3. Licence sheet (one page, signed by both sides)

**Licence for AI-produced advertising video**

- Studio: [studio name, address, tax no.]
- Client: [company, address, tax no.]
- Work: [film titles, durations, versions, delivery date]
- Price paid: [€ amount, invoice no.]

1. **Use granted.** Non-exclusive / exclusive [choose] right to use the Work for advertising the Client's own business in: [ ] web and own channels [ ] social networks (organic and paid) [ ] in-store and event screens [ ] TV [ ] cinema [ ] outdoor digital.
2. **Territory.** [North Macedonia / Serbia / Albania / Kosovo / other]. See clause 7 for H3 films.
3. **Term.** [12 months / 24 months / unlimited] from delivery. Renewal at [x]% of the original price.
4. **Not included.** Selling or sublicensing the Work, using it to train AI models, and editing it so it misrepresents a person or product, unless agreed in writing.
5. **AI disclosure.** The Work was made with generative AI. People shown are AI-generated and are not real people; any resemblance is coincidental. The Client agrees to keep an "AI-generated" or similar label where a platform or law requires it (for example Meta, TikTok and YouTube labels).
6. **Client materials.** The Client confirms it owns or may use the logos, product photos, renders and texts it supplied. The Studio uses them only for this Work.
7. **Model and music.**
   - LTX films: made with LTX-Video (Lightricks), used under its licence terms for commercial output.
   - H3 films: made with MiniMax H3 (open weights). Credit: "Made with MiniMax H3". Under the H3 licence (sections V.2, V.4), the Client may not use, show or distribute an H3 film in the EU, UK, South Korea or USA, nor use it to train AI models. In practice: in-store screens, TV/cinema, events and geo-restricted posts in allowed countries only. No open YouTube, website, Instagram or LinkedIn posts, because those can be viewed from excluded countries. The Client passes this restriction on to anyone it gives the film to. See `MINIMAX_H3_LICENCE_AND_PLAN.md`.
   - Music: original tracks made with ACE-Step 1.5 (MIT licence). No third-party music, no Content ID claims expected.
   - Voice-over: [AI voice (Gemini TTS) / human voice actor: name].
8. **Credit.** The Studio may show the Work in its portfolio after the Client's campaign starts, unless the Client opts out here: [ ] opt out.
9. **Liability.** The Studio's total liability is limited to the price paid for the Work.

Signatures: Studio ______ Client ______ Date ______

## 4. Pitch-stage notice (goes with every concept)

"This is a presentation concept only. It has not been published and will not be published without your written approval. The video was made with artificial intelligence. Logos and trademarks belong to their owners and are used only to show the idea."

Macedonian, Serbian and Albanian versions are in `cut/offers.json` (`note` / `intro` fields) and are printed on every pitch page and PDF.

## 5. Hosting rule for pitch material

- LTX pitch pages and files can be hosted anywhere (currently an unlisted, noindex path on the studio server).
- H3 pitch material is shown in person (laptop, USB) only. It is never uploaded to a public page, EU servers or EU-based APIs.
- For clients who need open online use or EU export material, offer the LTX version.
