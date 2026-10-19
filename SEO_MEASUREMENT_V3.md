# SEO measurement V3

## Baseline

Use the supplied 2026-10-19 workbook as the frozen pre-release baseline. Keep query, page, country, device and date dimensions separate; totals can differ because of GSC privacy and aggregation.

## Anonymous GA4 events

- `official_game_click`: click to `pokesurvivor.com`.
- `build_share`: build-planner share action.
- `diagnosis_complete`: save-recovery decision helper completed.
- `video_start`: a registered guide video begins playback.

Events run only after analytics consent and exclude search text, room codes, account state, email and save data.

## GSC follow-up

1. Recheck Page indexing when aggregate processing completes.
2. Compare exclusion sample URLs against canonical, robots, response status and sitemap membership before editing content.
3. Inspect `/moves/`, `/pokedex/`, `/arceus-judgment/`, `/tier-list/` and the corresponding priority locale pages after deployment.
4. Compare 7/28-day page and query changes against this release date; do not interpret the old discovered count as indexed-page count.
