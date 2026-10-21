# PokeSurvivor QA V7

Date: 2026-10-22

## Passed

- `python wiki/ci_build.py`: 93 HTML documents, 88 indexable URLs, 4,364 localized search targets, valid metadata, reciprocal hreflang, anchors, links, JSON-LD and source hashes.
- Machine-readable resources: 10/10 passed.
- V7 contract: source `40c51c1`, cross-device diagnostics, revision handling, relay status, localized intent, freeze guidance and 88-URL sitemap passed.
- Analytics consent contract passed for all four locales.
- Targeted Chrome QA passed for the six-field Save diagnostic and its generated report.
- Spanish and Italian Save pages no longer present obsolete 30-minute current guidance; Traditional Chinese tier-list title and full-data intent passed.
- Co-op, updates, how-to-play, moves and builds content checks passed.
- Production returned HTTP 200 for `/`, `/save-recovery/`, `/es/save-recovery/`, `/zh-hant/tier-list/`, `/updates/` and `/sitemap.xml`.
- Production `/updates/` exposes source `40c51c1`; the homepage exposes the 2026-10-21 review date; `www` returns 301 to the canonical host while preserving path and query.
- Sitemap contains 88 unique canonical URLs with a `lastmod` on every entry; 44 genuinely changed URLs use `2026-10-21`.

## Browser and console evidence

- GSC reports `/es/save-recovery/`, `/zh-hant/tier-list/` and `/move-evolutions/` as indexed with valid HTTPS and breadcrumb data.
- The aggregate Page indexing report still displays that data is processing, so it provided no unindexed examples or reason table to repair.
- The stored `/move-evolutions/` crawl showed two non-critical VideoObject `uploadDate` warnings from the older crawl. Current generated markup uses `2026-10-15T00:00:00+00:00`, so the source correction is live and awaits recrawl.
- Full local Playwright suites could not complete because the Windows Node process exhausted the available page file. Targeted Chrome tests and all static build contracts passed; extension-console errors were unrelated to site code.

