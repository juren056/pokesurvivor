# V17 release evidence — 2026-10-30

## Search Console review

- The Pages report was last updated on 2026-10-23: 104 indexed URLs and 30 not indexed URLs.
- The non-indexed groups shown were 10 alternate pages with a proper canonical, 4 `noindex` pages, 3 redirects, 1 not-found URL, and 12 crawled-but-not-indexed URLs.
- All eight V17 watch URLs were individually inspected and reported as indexed: `/`, `/tier-list/`, `/co-op/`, `/kecleon-shop/`, `/es/abilities/`, `/it/natures/`, `/zh-hant/abilities/`, and `/zh-hant/tier-list/`.
- Live tests for `/es/orbs/` and `/zh-hant/survivor-vs-burst/` reported that each URL can be indexed. Their content was strengthened instead of changing canonical URLs.
- Manual Actions and Security Issues both reported no issues. Removals showed no requests in the preceding six months.
- `https://pokemonsurvivorwiki.com/sitemap.xml` reported Success, was last read on 2026-10-29, and exposed 108 discovered pages.

No indexing request, sitemap resubmission, removal, or Search Console setting was changed during this review.

## Content and source review

- Mobile guidance now records restored Manual Aim, the Anchored option, and Floating as the default.
- Save and download guidance now records the 25-second minimum between normal successful cloud uploads. The 21-second value is limited to the special scheduled path.
- The Halloween window is recorded as 2026-10-30 through 2026-11-02 in Madrid, inclusive, with an exclusive UTC end at 2026-11-02 23:00.
- First-run routes, tier-list methodology, co-op issue status, orb guidance, and two representative crawled-but-not-indexed pages received answer-first additions.
- When the current upstream main branch lacks its changelog source, builds retain the last validated source snapshot and reject empty or malformed evidence.
- Media and factual evidence are limited to original, official, public-domain, licensed, or otherwise authorized material. Competitor assets are not copied.

## Release gates

- `python wiki/ci_build.py`
- `python wiki/browser_check.py`
- `python wiki/v17_browser_check.py`
- `python wiki/v17_check.py`
- `git diff --check`

Only pages with substantive V17 changes receive a `2026-10-30` sitemap `lastmod`. Existing URL paths and canonical targets remain stable.
