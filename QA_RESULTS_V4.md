# QA results V4 — 2026-10-19

## Passed

- Build: 92 localized pages plus 404; 88 indexable canonical URLs.
- SEO/content checker: 93 HTML documents, 4,364 localized search targets, metadata, reciprocal hreflang, anchors, internal links, JSON-LD and source hashes.
- Machine-readable resources: 10 resources with canonical/noindex/content/link/sitemap separation.
- V4 contract: fixed source, counts, new behavior families, upgrade rules, save timing, localized tools and sitemap count.
- Analytics: opt-in, refusal, withdrawal/re-enable, query stripping, saved choice, GPC and preview isolation.
- Browser: 276 route/viewport checks and 13 behavior checks with no JavaScript errors.
- Media: 92 image-route checks, 20 layout checks and 6 video playback/caption/seek checks, including recovery and Range fallback.
- UI regression: protected SEO/data baseline, 8 intermediate-width checks and 5 behavior groups with no JavaScript errors.
- Focused planner test: Psyduck can select Confusion, buff moves are excluded, Charmander + Ember receives 1.20×, and Charmander + Tackle does not.

## Production checks

- Git release commit `7b3b87a` was pushed to `origin/main`; Cloudflare served the V4 payload on the third polling attempt.
- Home, Spanish Moves, Moves, Move Evolutions, Builds and Save Recovery returned HTTP 200.
- Home contains `2026-10-19`; Spanish Moves contains the 103-move release copy.
- Production sitemap contains 88 URLs: 60 dated 2026-10-19, 4 dated 2026-10-17 and 24 unchanged URLs dated 2026-10-15.
- The four priority English routes above expose self-referencing canonical URLs.
- GSC reports the sitemap as Success, last read 2026-10-19, with 88 discovered pages. The aggregate Page indexing report remains in processing.
