# PokeSurvivor QA Results V6

Date: 2026-10-21

## Passed

- `python wiki/ci_build.py`: 93 HTML documents, 88 indexable URLs, 4,364 localized search targets, canonical/hreflang/anchors/links/JSON-LD/source hashes valid.
- V6 release contract: 966 partners, 29 starters, 103 moves, 97 evolutions, manual Save rules, TURN pilot guidance, mobile guidance, four locales and 88 unique sitemap URLs.
- Analytics contract: four-locale opt-in/refusal/withdrawal/re-enable/query-removal/saved-choice/GPC/preview isolation.
- `python wiki/v6_tool_check.py`: Move Master reload persistence, same-origin locale sharing, invalid/duplicate/unknown import handling, reset cancel/accept and blocked-storage fallback.
- `python wiki/browser_check.py`: 276 route/viewport checks and 14 behavior checks; no JavaScript errors.
- `python wiki/redesign_check.py`: protected SEO/data baseline, eight intermediate widths, five redesigned behavior groups, no JavaScript errors.
- `python wiki/media_check.py`: 92 image route checks, 20 responsive media checks, six complete video playback/caption/seek checks, failure recovery and Range fallback.
- `node --test tests/i18n.test.cjs`: 18/18 passed.
- `node --test tests/net.test.cjs`: 16/16 passed, including authorized TURN, refusal/broken fallback and guest STUN behavior.

## GSC/GA4 browser findings

- GSC page indexing displayed “processing data; check again in about one day,” so no unindexed reason or URL table was available to diagnose.
- GSC sitemap displayed Success and 88 discovered pages before V6 deployment.
- GA4 loaded the configured property and showed complete-data indicators on visible cards. The requested orange quality detail was not exposed as an orange warning in the accessible UI; no quality warning was invented.

