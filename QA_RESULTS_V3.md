# QA results V3 — 2026-10-19

## Build and data

- `python wiki/ci_build.py`: PASS.
- 92 localized pages plus 404 built; 88 canonical indexable URLs.
- 4,212 localized search targets; metadata, reciprocal hreflang, anchors, links, JSON-LD and source hashes valid.
- V3 mechanics check: source lock `b8e843f`, 966 partners, 65 moves, 59 evolutions, four-stat schema, Nasty Plot and category exceptions, one-time melee adjustment and exact tier-band populations all pass.
- Analytics consent and event-source checks pass.

## Browser and responsive

- `python wiki/browser_check.py`: PASS after final UI update.
- 276 route/viewport checks across desktop, 390 px mobile and short mobile.
- 13 interaction groups pass, including locale skeleton parity, filters/sorting, evolution, build share parameters, Nasty Plot route, search, recovery helper and no-JavaScript fallback.
- No JavaScript page errors and no root overflow.
- `python wiki/redesign_check.py`: PASS; 8 intermediate-width checks and 5 interaction groups.

## Media

- `python wiki/media_check.py`: PASS.
- 92 image-route checks, 20 media-layout checks and 6 complete video playback/caption/seek checks.
- Failure recovery and Range fallback verified.

## Search Console after release

- Aggregate Page indexing is still processing; reason rows and sample URLs remain unavailable. This remains an external reporting blocker, not evidence of zero exclusions.
- URL Inspection reports `/moves/`, `/pokedex/`, `/arceus-judgment/` and `/es/arceus-judgment/` are indexed. Each result also reports HTTPS and one valid breadcrumb item.
- GSC reread `https://pokemonsurvivorwiki.com/sitemap.xml` on 2026-10-19. Status is Successful, with 88 discovered pages and 0 discovered videos.

## Production

- Release commit `b072b8799bbc7286d7082069fe15380086a0b9a3` was pushed to `origin/main` and observed on production.
- 13 priority production routes returned HTTP 200 with one H1 and the 2026-10-19 review date.
- Production `sitemap.xml` contains 88 URLs; `assets/game.json` contains 65 moves and 966 partners and reports source `b8e843f`.
- Evidence: `wiki/artifacts/production-smoke-v3.json`.

