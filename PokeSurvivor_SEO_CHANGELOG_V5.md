# PokéSurvivor SEO changelog V5

Date: 2026-10-20  
Reviewed game source: `018e986f4c12f414dfa84193ee35b2959b1e325c`

## Search and content changes

- Updated the English, Spanish, Italian and Traditional Chinese homepages and changed their visible review date and sitemap `lastmod` to 2026-10-20.
- Reworked `/co-op/` around four distinct stages: friendship, room invitation, peer connection and running game. The page now separates issues #233, #234 and #235, the boss-after-rift fix and the move-upgrade report instead of presenting them as one cause.
- Added a local, privacy-safe co-op checklist. It reads no account, save, IP address or WebRTC data and sends nothing to the Wiki.
- Clarified that the reviewed repository contains a prepared TURN package whose README says it is not deployed or connected to the game.
- Strengthened `/es/download/` for platform intent and direct official-site access.
- Added the official language path, `Settings → Graphics → Language`, and manual move-switching guidance to the relevant guides.
- Added issue #232 to the moves page as a player report, without presenting its sample or probability as independently reproduced.
- Improved Spanish builds/download copy and Traditional Chinese starter/move terminology with the game name and common English aliases where they help recognition.
- Normalized the `VideoObject.uploadDate` value to an ISO 8601 date-time with timezone.

## Technical SEO

- Rebuilt `sitemap.xml`: 88 unique canonical, indexable URLs; changed pages use `2026-10-20`; excluded utility and 404 pages remain outside the sitemap.
- Revalidated canonical URLs, reciprocal hreflang, index flags, JSON-LD, internal links and anchor targets across all 93 generated HTML documents.
- Kept the existing route set and winning data pages. Counts remain 966 Pokémon, 29 starters, 103 moves and 97 move evolutions.
- Added V5 build-contract checks and a four-locale analytics-consent matrix.

## GSC evidence checked in browser

- Property: `sc-domain:pokemonsurvivorwiki.com`.
- Performance snapshot shown in GSC: 157 clicks, 2,237 impressions, 7.0% CTR and average position 7.7.
- URL Inspection showed `/co-op/`, `/es/download/` and `/move-evolutions/` indexed and HTTPS/breadcrumb checks valid.
- The aggregate Page indexing report was still processing and displayed a request to return in about one day.
- `/move-evolutions/` had a noncritical video warning for an invalid upload date and missing timezone. The generated production markup now supplies `2026-10-15T00:00:00+00:00`; GSC will retain its earlier crawl result until Google recrawls it.

