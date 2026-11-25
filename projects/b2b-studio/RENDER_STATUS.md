# Render and delivery status (2026-11-25, ~08:00 UTC)

Everything that was planned is rendered, cut and delivered. No GPU box is rented.

## LTX (public-safe road)
| Deliverable | Count | Where |
|---|---|---|
| Films with music and local-language voice-over (16:9) | 45 | scratchpad `final_music/` |
| 9:16, 1:1, 4:5 versions | 45 each | `final_music_9x16/`, `final_1x1/`, `final_4x5/` |
| Pitch versions (BIG DOGMA intro, concept watermark, email outro), 16:9 and 9:16 | 45 + 45 | `pitch/`, `pitch_9x16/` |
| Posters, 6 s GIFs, silent 6 s teasers | 45 each | `previews/` |
| Offer PDFs (MK / RS / AL) | 12 | `offers_pdf/` |
| How-it's-made explainers | 5 | `explainers/` |
| Subtitles mk / sr / sq / en | 176 (44 films) | `subtitles/` in this repo |

Audio standard: all films -16 LUFS integrated, true peak <= -1.5 dBTP, 48 kHz stereo (two-pass, applied 2026-11-25 to all six film folders). Social launch reels -14 LUFS.

Pitch materials zip (all of the above for the 12 companies, brand kit, logo animation, subtitles, private outreach files with the real page links): private download folder on KVM4 (`abracadabra-v3/site/_dl_<private-token>/`). The token was rotated on 2026-11-25; the link is shared with the owner only.

## Web (KVM4, Docker + Traefik)
| Stack | URL | Notes |
|---|---|---|
| `ai-studio-pitch` | `pitch.bigdogma.tech/<private-token>/` | 12 private pages (one per company), noindex; tokens rotated 2026-11-25, real links never committed |
| `bigdogma-site` | `bigdogma.tech` | studio website MK/EN, unlisted (noindex) until launch |
| `abracadabra-v3` | `_dl_<private-token>/` | download folder |

Private backup of non-H3 masters (animated logo exports, launch videos and images): `/opt/bigdogma_backup/` on KVM4 (not served).

## MiniMax H3 (licence-restricted road)
44 H3 films, each with pitch 16:9 / 9:16, 1:1, 4:5 and subtitles mk/sr/sq/en, plus the Foton "FALCON" action set (30 s film, 15 s reel, 6 s bumpers 16:9 + 9:16) and the raw clips. Rendered on Vast boxes in permitted territory, finished on the box (`h3_post/`), downloaded by the owner (byte totals verified) and the box destroyed. H3 files exist only on the owner's computer. Rules: `MINIMAX_H3_LICENCE_AND_PLAN.md`, knowledge base §25.

## Launch kit
`launch/`: social images and captions (email-only contact), showreel 16:9 + 9:16, 6 reels, 5 posts, studio website source. Reviewed and fixed in two independent rounds.

## Open (owner)
- Outreach: 0 of 12 sent. Use the files in `outreach_private/` from the zip (real links); this repo's copies show `[PITCH_PAGE_LINK]`.
- Studio website goes public: remove the noindex header and meta (see `launch/site_work`).
- Optional: "how we work" video with sr/sq voice-over for the 7 RS/AL/XK pitch pages; Vast refund request for the faulty UAE box.
