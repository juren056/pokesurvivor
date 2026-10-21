# PokeSurvivor Blockers V7

Date: 2026-10-22

## External waiting states

- GSC Page indexing is still processing and exposes no exclusion reason rows or example URLs. Three priority URLs were individually confirmed indexed; broader exclusion diagnosis must wait for Google to populate the aggregate report.
- GSC recrawl controls when the corrected VideoObject timestamp warning disappears. Current production markup already includes a full ISO-8601 timestamp with timezone.
- The active GA4 browser session repeatedly resolved to other account properties rather than a verifiable PokeSurvivor property. No configuration was changed and V7 analytics dimensions remain unverified in the live GA4 UI.
- Cloudflare reported degraded GitHub push-event delivery, so commit `be4fbb9` did not automatically appear. The same committed build was deployed directly with Wrangler as production deployment `754bf9f2`; automatic Git deployments remain enabled.

## Evidence boundaries

- No physical iPad-to-PC session or live multi-account relay session was available. Source evidence, static contracts and targeted browser behavior are recorded separately from physical-device reproduction.
- No new third-party gameplay image or video was copied without a reusable basis. Creating new real gameplay footage remains blocked until an authorized recording source is available.
- Search Console submission confirms receipt or inspection status, not guaranteed indexing or ranking.

## V7 task status

| Task | Status |
|---|---|
| T00 source lock | complete |
| T01-T02 Save recovery and diagnostics | complete |
| T03 Traditional Chinese tier intent | complete |
| T04 co-op and relay update | complete |
| T05 query-by-URL baseline | complete; measurement pending |
| T06 moves/builds routes | complete |
| T07 mobile/evolutions verification | complete within available browser coverage |
| T08 Spanish download protection | complete |
| T09 starter tier protection | complete |
| T10 GA4 dimension verification | blocked by property identification |
| T11 locale consistency | complete |
| T12 canonical/hreflang/sitemap/indexing | complete; aggregate GSC report pending |
| T13 new real media | blocked pending authorized capture source |
| T14 issue #262 guidance | complete |
| T15 7-14 day measurement | scheduled by the experiment record; not yet due |

