# PokéSurvivor measurement V5

Date: 2026-10-20

## Baseline

- GSC visible snapshot: 157 clicks, 2,237 impressions, 7.0% CTR, average position 7.7.
- The supplied 2026-10-20 workbook is a rolling snapshot rather than a single-day export.
- Historical priority evidence includes `/es/download/` (10 clicks / 231 impressions), `/mobile/` (3 / 113), home (3 / 89), `/move-evolutions/` (0 / 56), `/zh-hant/starter-tier-list/` (4 / 57) and `/es/builds/` (2 / 41).

## Events and privacy

- GA4 loads only after explicit consent on the production hostname.
- GPC suppresses loading even when an earlier granted choice exists.
- Search query strings and referrer query strings are removed from analytics page configuration.
- V5 verifies `official_game_click`, `build_share`, `diagnosis_complete` and `video_start` event hooks.
- The co-op checklist records only tool/stage/network category in its event and does not transmit the generated report.

## Follow-up windows

- After Google recrawls `/move-evolutions/`, recheck the video enhancement for the resolved ISO date-time warning.
- Compare clicks, impressions, CTR and average position after 7 and 28 days using like-for-like date windows.
- Segment the six priority routes above; do not compare the rolling 10/20 total with a single prior day.

