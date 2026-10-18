# Deployed state — 2026-10-18

Baseline before this change: `f688565e3d9b48ad19093668a9b1086cc31a91ea` on `main`. Production target: `https://pokemonsurvivorwiki.com/`, deployed from the GitHub repository through Cloudflare.

The source snapshot remains pinned to upstream game commit `5bbc3b29288d6af4596f21188fb8b54e0e9b739f`; data extraction remains `b297089`. The newest verified upstream changelog entry remains 2026-10-15. The editorial review date is 2026-10-18.

This release adds `/save-recovery/` in English, Spanish, Italian and Traditional Chinese; expands `/co-op/`, `/download/`, `/moves/` and `/move-evolutions/`; adds two original SVG decision diagrams and anonymous diagnostic analytics; and increases the sitemap from 84 to 88 canonical indexable URLs.

## Production verification

Release payload commit `ba9896eee34f99a7f84153f8350a1b6e9c1ceaf8` was pushed to `origin/main` and observed on production. The homepage shows the 2026-10-18 review date, `/save-recovery/` returns HTTP 200, and the production sitemap contains 88 URLs. A Playwright production smoke test passed eight key routes, all four locale homepages, 390 px mobile overflow checks and the save-recovery diagnostic.
