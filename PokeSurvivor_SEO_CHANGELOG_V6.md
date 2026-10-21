# PokeSurvivor SEO Changelog V6

Date: 2026-10-21

## Source and content

- Merged and locked the game reference to upstream commit `3c9641c9e782cf74afbde490f39cd60adf59e32b`.
- Replaced current 10/30-minute automatic cloud-upload guidance with the current manual Save model, retaining older timings only as clearly labelled history.
- Documented local, pending, syncing, success and offline as distinct states, the 65-second successful-upload gap, and the safe sequential-device handoff.
- Removed mobile Manual Aim instructions and added separate, evidence-bounded notes for player reports #258 and #259.
- Removed the friend Online prerequisite, recorded the three-minute invite expiry, and documented the direct-first authorized TURN pilot without claiming universal availability.
- Separated initial connection report #260 from mid-run disconnect report #253.
- Added the October 20 co-op/move fixes and October 21 TURN pilot to the update page.
- Updated the homepage review date and metadata to 2026-10-21.

## Product and localization

- Added a Move Master checklist to `/move-evolutions/` with search, completed/incomplete filters, local persistence, JSON export/import, unknown-ID retention, size/schema validation, reset confirmation, blocked-storage fallback and consent-gated low-sensitivity analytics.
- Exposed the same checklist and storage key under English, Spanish, Italian and Traditional Chinese routes.
- Completed the Spanish download comparison table instead of leaving English headers and rows.
- Updated the original co-op stage diagram for the three-minute invite and direct/server-relay distinction.

## Technical SEO

- Rebuilt 92 localized pages plus the 404 page.
- Kept 88 unique indexable URLs with reciprocal hreflang, canonical tags, structured data and matching sitemap URLs.
- Updated every changed page `dateModified`/sitemap `lastmod` to the real review date without adding keyword-only URLs.
- Google Suggest collector ran in read-only mode: 31 observed rows from 11 seeds; empty results were preserved as empty and were not synthesized.

