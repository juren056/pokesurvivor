# V10 release evidence — 2026-10-23

## GSC review

- The Pages indexing summary was last updated on 2026-10-16 and showed 82 excluded URLs: 64 crawled but not indexed, 10 alternate canonicals, 4 intentional noindex pages, 3 redirects and 1 404.
- The crawled-not-indexed examples were last crawled on 2026-10-17, so that aggregate is stale relative to the current release.
- Live URL Inspection on 2026-10-23 reports both `/abilities/` and `/es/mobile/` as indexed, served over HTTPS, with one valid breadcrumb item.
- Current Search performance for the last 24 hours showed 187 clicks, 2,754 impressions, 6.8% CTR and average position 6.9. Existing winners such as `/co-op/` and Traditional Chinese tier/move pages keep their URLs and core titles.

## Changes shipped

- Synced upstream source commit `6f0f440`, including the bounded 45-second direct-connection recovery behavior and room waiting behavior.
- Exported all 271 used ability IDs with stable IDs and English, Spanish, Italian and Traditional Chinese effect text from the official locale dictionaries.
- Corrected mobile guidance in all four site languages; the Spanish page no longer tells mobile players to enable Manual Aim.
- Updated co-op and update pages with clear boundaries between a room-server state interruption, a direct host connection interruption and an unrecovered disconnect. Player reports and feature requests remain labeled as such.
- Updated only the homepage, abilities, mobile, co-op and updates families to `2026-10-23`; the sitemap still contains 104 canonical HTML URLs with reciprocal hreflang.
- Repaired the build planner's Repertoire preview and restored the reachable Guest/unlinked branch in the privacy-safe save diagnostic.

## Validation

- `python wiki/ci_build.py`
- `python wiki/browser_check.py`: 324 route/viewport checks, 14 behavior checks, no JavaScript errors.
- `python wiki/v10_browser_check.py`: four-language ability, mobile and co-op checks at 390 px.
- `python wiki/media_check.py`

No arbitrary third-party screenshot or video was copied. Existing gameplay captures and original concept art retain their source and scope labels; GitHub changelog, commits and issues are linked as evidence.
