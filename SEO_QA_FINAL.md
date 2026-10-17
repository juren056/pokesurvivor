# SEO QA — 2026-10-17

Local final results before deployment:

- `python wiki/ci_build.py`: PASS; 23 HTML documents, 21 indexable URLs, 1,051 search targets, metadata/links/JSON-LD/source hashes and 10 machine-readable resources valid.
- `wiki/browser_check.py`: PASS; 66 route/viewport checks and 10 behavior checks, including the build planner and Gacha boundaries.
- `wiki/media_check.py`: PASS; 22 image-route checks, 20 media layouts and six complete video playback/caption/seek checks, plus failure recovery and byte ranges.
- `wiki/redesign_check.py`: PASS; protected unchanged routes/data, eight intermediate-width checks and five interaction groups.

Production gates after Git deployment:

- Build and existing deterministic check suite.
- Canonical, robots, sitemap membership, one H1, unique metadata and internal links.
- Tier filters/sorts, build planner, gacha calculator and mobile navigation.
- Desktop and narrow viewport screenshots for Home, Tier List, Arceus, Co-op and Builds.
- Production HTTP for all sitemap URLs, assets, robots, sitemap, real 404, HTTPS and host redirects.
- Git commit → Cloudflare active deployment → main domain evidence.

GSC indexing and GA4 receipt are reported independently from deterministic QA.
