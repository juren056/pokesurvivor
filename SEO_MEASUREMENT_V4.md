# SEO measurement V4

Use non-overlapping comparison windows after release. Record clicks, impressions, CTR and average position by page, query, country and device. Keep the supplied rolling GSC snapshots as baselines, not as day-over-day deltas.

Primary cohorts:

- `/moves/` and `/move-evolutions/`: queries around the 38 new moves and 97 evolutions.
- `/builds/` and `/upgrades/`: Starting Move, Repertoire and mono-type bonus queries.
- `/save-recovery/`: 30-minute pending and 65-second minimum-upload-gap questions.
- Locales: English, Spanish, Italian and Traditional Chinese measured separately.

GA4 events used for behavior evidence: `starting_move_select`, `build_share`, `evolution_check`, `diagnosis_complete`, `official_game_click` and `video_start`. Do not interpret events as proof of gameplay outcomes.
