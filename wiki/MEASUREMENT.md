# GSC, GA4 and sitemap — 2026-10-15

**Current status:** Cloudflare browser deployment and DNS are complete; apex and www are Active with SSL. See [CF-LIVE.md](CF-LIVE.md). Earlier pending DNS/login observations below are historical; GSC account verification/submission and GA4 receipt are still unverified.
## Implemented and published

- GA4 account: existing owner account `389162355`.
- New property: Pokémon Survivor Wiki, `559046998`.
- Web stream: Pokémon Survivor Wiki — Web, `16129695053`.
- Measurement ID: `G-GEQDCG9L1K`; configured URL `https://pokemonsurvivorwiki.com`.
- Reporting timezone: China (GMT+08:00); currency CNY, inherited defaults selected during setup.
- Only page-view enhanced measurement remains enabled; automatic form/search/outbound/video/download/scroll measurement is disabled.
- The website loads the tag only on apex/www, after opt-in. Pages preview and localhost are excluded. Query strings/fragments are omitted from configured page location/referrer. Advertising storage/personalization and Google signals are disabled. Global Privacy Control prevents starting the tag. Withdrawal disables measurement and clears accessible GA cookies; the footer can reopen preferences.
- Privacy content describes the actual service and local preference key.
- Sitemap is generated from the indexable route inventory, formatted XML, 17 canonical absolute URLs, excluding search/404. robots.txt declares the apex sitemap. Existing editorial lastmod dates are preserved.

## Release and validation

Active Pages deployment: `9eabe488-b59b-4671-8a52-a02dd1ae42b1`, immutable URL https://9eabe488.pokemonsurvivorwiki.pages.dev/; provider stage success, created 2026-10-14 17:49:00 UTC.

`python build.py`, `python check.py`, `node --check public/analytics.js`, and `node analytics_check.cjs` passed from the wiki directory. The analytics check covers no pre-consent tag, refusal, withdrawal/re-enable, query removal, saved choice, GPC and preview exclusion. Final HTML checks cover 19 documents and the 17 sitemap entries.

One deployment (`c903e4d8`) preceded the final withdrawal/preview correction because pre-deploy commands used the wrong working directory; those commands failed visibly. The correct directory was used to rebuild and validate, and `9eabe488` supersedes it. No GitHub push occurred.

Evidence: `artifacts/measurement-release.json`, `artifacts/ga4-stream.png`. The GA4 UI shows the new property and measurement ID but no data received. Do not claim Realtime receipt or a successful tag-installation test.

## Unresolved external state

Cloudflare API confirms both apex and www are pending with `CNAME record not set`. Dashboard remains at security verification; the CLI token has no DNS editing permission. Prepared records are in [DNS-RECORDS.md](DNS-RECORDS.md). No DNS record was changed.

GSC domain verification was attempted in the signed-in browser and failed explicitly: verification token not found in DNS TXT. No sitemap submission or indexing request occurred. GSC-to-GA4 product linking is pending verified ownership.

Fresh shell HTTP probes returned 403 for both Pages and apex; the browser loaded the Pages homepage, but direct sitemap navigation was blocked by the browser client and apex navigation timed out. These are observations from this environment, not proof of Googlebot behavior. The provider's successful deployment is separate from custom-domain delivery and indexing.

Once the owner completes the Cloudflare security verification/login: apply the three reviewed records, check apex HTTPS and sitemap/robots/404 plus www redirect, verify GSC, submit the apex sitemap, link this exact GA4 property/stream, then check a consented real page visit in Realtime. Do not submit the preview hostname sitemap under the purchased domain.
