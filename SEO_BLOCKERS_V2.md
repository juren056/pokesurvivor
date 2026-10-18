# SEO blockers V2 — 2026-10-18

- GSC aggregate indexing exclusions: BLOCKED by Google report processing. Recheck after the UI exposes exclusion reasons and URL samples.
- Real reproduction of issues #164, #185, #186 and #193: NOT REPRODUCED. Pages label these as player reports; no fix/cause claim is made.
- Physical-device mobile validation: existing captures use Chromium emulation. A real iOS/Android run remains separate evidence work.
- Native-speaker approval for Spanish, Italian and Traditional Chinese remains pending; semantic and structural localization review is complete.
- Production verification is pending until the final Git commit reaches Cloudflare.

## Resolved in this release

- Production deployment: release payload `ba9896e` is live; the production homepage, new recovery route and 88-URL sitemap were verified.
