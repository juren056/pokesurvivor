# Production release — 2026-10-15

**Current status:** Cloudflare browser deployment and DNS are complete; apex and www are Active with SSL. See [CF-LIVE.md](CF-LIVE.md). Earlier pending DNS/login observations below are historical; GSC account verification/submission and GA4 receipt are still unverified.
Current measurement release and remaining DNS/GSC work: [MEASUREMENT.md](MEASUREMENT.md). This later record supersedes earlier deployment IDs and the earlier statement that no verification request was attempted.
## Published artifact

- Project: `pokemonsurvivorwiki` (Cloudflare Pages, static assets only).
- Production URL: https://pokemonsurvivorwiki.pages.dev/
- Immutable deployment: https://0864a751.pokemonsurvivorwiki.pages.dev/
- Deployment ID: `0864a751-f6d1-45eb-b611-e107b124bc02`.
- Provider creation time: 2026-10-14 17:33:21 UTC / 2026-10-15 01:33:21 Asia/Shanghai.
- Provider deployment stage: success.
- Input: `wiki/dist`, from the locally reviewed working tree. No GitHub push was performed; the original game source commit is not a commit of the new Wiki implementation.
- The deployment ZIP was verified byte-for-byte against all 48 local output files before release. Cloudflare uploaded 46 public assets and processed `_headers` / `_redirects` separately.

## Checks against production Pages hostname

All 18 routes returned HTTP 200 with HTML SHA-256 matching the local build manifest, including the noindex search page. Sitemap, robots, 96px favicon, stylesheet and JavaScript returned 200 and matched local bytes. `/does-not-exist/` returned 404. Canonicals remain on the intended purchased domain. These checks establish delivery, not Google indexing or actual custom-domain readiness.

Local evidence: `wiki/artifacts/cloudflare-deployment.json` and `wiki/artifacts/production-http-report.json`. The published homepage was also checked in the browser: selecting Bulbasaur updates its real source-derived stats, Vine Whip evolution route and prerequisite link. Screenshot: `wiki/artifacts/published-home.png`.

## Domain and Search Console work

Both `pokemonsurvivorwiki.com` and `www.pokemonsurvivorwiki.com` were attached to the project through the Cloudflare API. The current domain validation reports pending with `CNAME record not set`. The domain zone is active in the same account. The existing CLI OAuth token has Pages write and zone read access but cannot list/edit DNS records.

GSC Wizard remains unauthorized. The browser's existing Google session works, and a domain-property verification dialog for `pokemonsurvivorwiki.com` was opened. DNS verification is not yet complete; no sitemap submission or indexing request has been performed. The exact TXT value and two CNAME records are prepared in [DNS-RECORDS.md](DNS-RECORDS.md), with a three-entry BIND file for reference. The Cloudflare dashboard login has not completed; the owner has been asked to restore login or apply those records. No DNS records have been changed.

## Deployment tool behavior

Wrangler 4.151.0 initially delegated the Pages project-create command to Workers and attempted asset upload, then rejected the absolute-source `_redirects` rule. That attempt did not deploy. The explicit legacy Pages creation path succeeded; the subsequent Pages deployment succeeded normally. The unwanted generated Workers config was removed and replaced with the scoped `wiki/wrangler.toml` Pages config.

For subsequent releases, build/check the Wiki, then from the `wiki` directory run:

```powershell
npx --yes wrangler@4.151.0 pages deploy dist --project-name pokemonsurvivorwiki --branch main --commit-dirty=true
```

Do not deploy from the repository root or use `cloudflare/wrangler.toml`, which belongs to the upstream game's TURN service. Do not repeat deployment merely to update this local release report.
