# PokeSurvivor V7 Changelog

Date: 2026-10-21  
Production deployment: 2026-10-22 00:36 CST  
Release commit: `be4fbb9`  
Cloudflare deployment: `754bf9f2`

## Source and current behavior

- Merged the official game source at `40c51c178adb7af421a5c6db0f7b43c4492cc861` and rebuilt the 966-partner, 29-starter, 103-move and 97-evolution dataset.
- Rewrote Save recovery around revision conflict protection: read, merge and retry when another device has already advanced the cloud revision.
- Added an iPad Safari to PC Chrome handoff path and a six-field diagnostic covering device handoff, account state, original-device completion, save state, second-device collection state and before/after difference.
- Updated co-op guidance from the earlier pilot wording to the official October 21 server-relay behavior and TURN optimization, with fallback boundaries retained.
- Added safe guidance for the known freeze report tracked as issue #262 without presenting an unverified universal cause.

## Content and localization

- Reworked the Traditional Chinese tier-list intent and title to `寶可夢倖存者強度排行：966 名角色與配招參考` and exposed source-backed examples from the full 966-entry dataset.
- Expanded moves and builds route content and localized the V7 Save, co-op, tier, move and build changes across English, Spanish, Italian and Traditional Chinese.
- Kept the homepage review date at 2026-10-21 and updated its release message to Save revisions and server relay.
- Preserved existing traceable captures and original assets. No unlicensed third-party image or video was added.

## Technical SEO and release

- Rebuilt 92 localized pages plus the 404 page and published 88 unique indexable URLs.
- Regenerated canonical tags, reciprocal hreflang, structured data, robots and sitemap metadata. Forty-four sitemap URLs now carry `2026-10-21` as their genuine modification date.
- Published through Cloudflare Pages. GitHub automatic deployments remain enabled; a direct Wrangler deployment was used because Cloudflare reported degraded GitHub push-event delivery.

