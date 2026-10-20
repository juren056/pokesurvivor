# PokéSurvivor QA results V5

Date: 2026-10-20

## Automated acceptance

- Build: 92 localized pages plus a true 404; 88 indexable URLs.
- Search index: 4,364 localized targets.
- Source contract: 966 Pokémon, 29 starters, 103 unique moves and 97 evolutions from `018e986`.
- SEO: metadata, canonical URLs, reciprocal hreflang, anchors, internal links, JSON-LD and source hashes passed.
- Analytics: default-off, refusal, withdrawal/re-enable, saved consent, Global Privacy Control and preview-host isolation passed for English, Spanish, Italian and Traditional Chinese paths.
- Media: route placement, layout, complete playback, captions, seeking, failure recovery and Range fallback passed.
- Responsive UI: 276 route/viewport checks and 14 behavior groups passed without root overflow or JavaScript errors.
- Upstream source regression: 18 language/localization tests and 13 network-codec/co-op tests passed.
- Sitemap: 88 unique canonical URLs and valid XML.

## Manual browser acceptance

- GSC URL inspection confirmed the three priority URLs are indexed.
- The right-side language control remains compact and the localized homepages retain the English component skeleton.
- Co-op diagnostic output was checked for the embedded-site and cross-network branches and produces only a non-sensitive report.
- No index-request button was used because the inspected URLs were already indexed.

## Production acceptance

Production deployment and HTTP checks are recorded after the Git push in the release commit history and Cloudflare Pages status.

