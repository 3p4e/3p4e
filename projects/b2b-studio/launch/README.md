# BIG DOGMA launch kit (public-safe)

Only studio demo material and generic clips; no client films, no client brands, no MiniMax H3. The only contact everywhere is the email from `brand/brand.json` (inf.unit@bigdogma.tech).

- `static/`: profile pictures, covers and banners (Facebook, LinkedIn, X, YouTube), `social_copy.md` (bios, captions, X versions, YouTube titles, posting calendar, rules), render scripts in `_work/`.
- `video/`: post images (offer, 3-slide carousel, hello), README with every video's duration and loudness, build scripts in `_work/`. The videos themselves (showreel 16:9 and 9:16, reels 01-06) are not in git; rebuild them with the scripts in `_work/`.
- `site_work/`: source of the unlisted studio website (bigdogma.tech, noindex): `gen_site.py`, `build_media.py`, `site.js`, `site.css`, `deploy_site.sh`, `verify.js`. Site media are built from the studio demo films and are not in git.

Each part went through a build, an independent review and a fix round, then a second review and fix round.
