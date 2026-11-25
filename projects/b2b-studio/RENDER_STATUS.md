# Render and delivery status (2026-11-25, ~08:00 UTC)

Everything that was planned is rendered, cut and delivered. No GPU box is rented.

## LTX (public-safe road)
| Deliverable | Count | Where |
|---|---|---|
| Films with music and local-language voice-over (16:9) | 45 | scratchpad `final_music/` |
| 9:16, 1:1, 4:5 versions | 45 each | `final_music_9x16/`, `final_1x1/`, `final_4x5/` |
| Pitch versions (BIG DOGMA intro, concept watermark, email outro), 16:9 and 9:16 | 45 + 45 | `pitch/`, `pitch_9x16/` |
| Posters, 6 s GIFs, silent 6 s teasers | 45 each | `previews/` |
| Offer PDFs (MK / RS / AL), with the matching sector bundles | 12 | `offers_pdf/` |
| How-it's-made explainers | 5 MK by sector + 7 sr/sq, one per RS/AL/XK company (`cut/explainers.py intl`) | `explainers/` |
| Subtitles mk / sr / sq / en | 176 (44 films) | `subtitles/` in this repo |

Audio standard: all films -16 LUFS integrated, true peak <= -1.5 dBTP, 48 kHz stereo (two-pass, applied 2026-11-25 to all six film folders). Social launch reels -14 LUFS.

Pitch materials zip `BIG_DOGMA_LTX.zip` (3.3 GB: all of the above, brand kit, logo animation, subtitles, launch kit, private outreach files with the real page links): `dl.bigdogma.tech/_dl_<private-token>/`. The token was rotated on 2026-11-25; the link is shared with the owner only.

## Web (bigdogma.tech: Hostinger KVM 1, Mumbai, Docker + Traefik + Let's Encrypt; old KVM4 addresses redirect here)
| Stack | URL | Notes |
|---|---|---|
| `ai-studio-pitch` | `pitch.bigdogma.tech/<private-token>/` | 12 private pages (one per company), noindex; tokens rotated 2026-11-25, real links never committed |
| `bigdogma-site` | `bigdogma.tech` | studio website MK/EN, public and indexable since 2026-11-25 (canonical, sitemap.xml; config `launch/site_work/site_nginx.conf`) |
| `bigdogma-dl` | `dl.bigdogma.tech/_dl_<private-token>/` | private downloads, no listing, noindex |

Private backup of non-H3 masters (animated logo exports, launch videos and images): `/opt/bigdogma_backup/` on KVM4 (not served). The old KVM4 copies (pitch pages, studio site, the old download folder, the package staging folder) were deleted on 2026-11-25; the old KVM4 addresses only redirect.

The zip was refreshed on 2026-11-25 (`cut/pkg_update2.py`: new offer PDFs, 7 new explainers). `BIG_DOGMA_LTX_update_20261125.zip` (31 MB, only those 19 files) sits next to it: unzip it over `~/Videos/BIG_DOGMA_LTX` and run the organiser again.

## MiniMax H3 (licence-restricted road)
44 H3 films, each with pitch 16:9 / 9:16, 1:1, 4:5 and subtitles mk/sr/sq/en, plus the Foton "FALCON" action set (30 s film, 15 s reel, 6 s bumpers 16:9 + 9:16) and the raw clips. Rendered on Vast boxes in permitted territory, finished on the box (`h3_post/`), downloaded by the owner (byte totals verified) and the box destroyed. H3 files exist only on the owner's computer and, optionally, in the private `/opt/h3` folder on the Mumbai server (India is outside the restricted regions; never served on the web). Rules: `MINIMAX_H3_LICENCE_AND_PLAN.md`, knowledge base §25.

## Launch kit
`launch/`: social images and captions (email-only contact), showreel 16:9 + 9:16, 6 reels, 5 posts, studio website source. Reviewed and fixed in two independent rounds.

## Open (owner)
- Outreach: 0 of 12 sent. Use the files in `outreach_private/` from the zip (real links); this repo's copies show `[PITCH_PAGE_LINK]`.
- Outreach needs the contact person and email per company (the tracker has roles only) and the sender name in the signature; send from inf.unit@bigdogma.tech.
