# V11 release record — 2026-10-23

## Inputs reviewed

- `PokeSurvivor_2026-10-23_晚间Plan_V11.md` was treated as the requested execution plan.
- `PokeSurvivor_2026-10-23_晚间Analysis_V11.md` was treated as research and prioritization evidence.
- The game-data baseline remains source commit `6f0f4409f68adcc5bc31a77cafaf8ba9a0318397`.

## GSC diagnosis

The Coverage report last updated on 2026-10-16 showed 82 excluded URLs and 19 indexed URLs, including 64 under “Crawled — currently not indexed.” Live URL Inspection was therefore used to distinguish stale report rows from current status.

- `/zh-hant/starter-tier-list/`: **URL is on Google**, HTTPS valid, breadcrumb enhancement valid.
- `/arceus-judgment/`: **URL is on Google**, HTTPS valid, breadcrumb enhancement valid.

No redirect, `noindex`, canonical change or repeated indexing request was justified for those pages. The production sitemap remains the primary discovery signal.

## Implemented

- Added a privacy-safe cross-device coin diagnostic with separate local, pending, syncing, cloud-success and second-device-loaded states.
- Added the exact issue #305 timestamps in UTC and Asia/Shanghai, with player-report wording and no recovery guarantee.
- Added an original `coins-sync-states.svg` diagram and registered its source, rights, dimensions and sitemap placement.
- Separated connected-but-lagging behavior from initial connection and bounded reconnect behavior.
- Added the mobile-controller Manual Aim FAQ and classified #307/#313 as feature requests.
- Added the October 23 source/date matrix to Updates and refreshed affected page `dateModified` values.
- Expanded tier/build/Arceus/how-to-play context without creating new indexable URLs.
- Localized the new content, controls, diagnostic output and report labels for English, Spanish, Italian and Traditional Chinese.
- Kept the sitemap at 104 canonical, indexable URLs with reciprocal hreflang and updated `lastmod` values.

## Verification

- Static build: 109 HTML documents, 104 indexable URLs, 4,380 localized search targets.
- SEO checks: canonical, robots, reciprocal hreflang, JSON-LD, anchors, links, source hashes and sitemap separation passed.
- V10 and V11 release checks passed.
- Browser regression: 324 route/viewport checks, 14 behavior checks, no JavaScript errors.
- V11 mobile interaction check: save, co-op and mobile additions passed in all four locales at 390 px.
- Media: 108 page checks, 20 responsive media checks and 6 video playback/caption/seek checks passed.
- Network codec/co-op suite: 20 tests passed.

## Deployment and rollback

The release is deployed by pushing the release commit to `origin/main`, which triggers the existing Cloudflare Git deployment. Roll back by reverting that commit and pushing the revert to `origin/main`.
