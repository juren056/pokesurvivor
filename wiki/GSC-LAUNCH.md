# Search launch handoff — 2026-10-15

**Current status:** Cloudflare browser deployment and DNS are complete; apex and www are Active with SSL. See [CF-LIVE.md](CF-LIVE.md). Earlier pending DNS/login observations below are historical; GSC account verification/submission and GA4 receipt are still unverified.
Current measurement release and remaining DNS/GSC work: [MEASUREMENT.md](MEASUREMENT.md). This later record supersedes earlier deployment IDs and the earlier statement that no verification request was attempted.
## Completed locally

- All 19 HTML documents declare stable raster favicon, SVG, Apple touch and manifest URLs.
- Google-facing PNG: `https://pokemonsurvivorwiki.com/favicon-96.png`, 96×96. Multi-resolution ICO includes 16/32/48. The homepage and every guide use the same identity.
- Manifest icons: 192×192, 512×512 and maskable 512×512. No new service worker or offline claim.
- Local sitemap contains 17 canonical, indexable pages. Search and 404 remain noindex.
- Local HTML/links/sitemap validation and icon-file validation pass. The browser shows the new header mark without mobile root overflow.

## Current release status

The Wiki is now published to the dedicated Cloudflare Pages project. All 18 routes and key public assets match the local build over HTTPS; unknown URLs return 404. Both custom domains are attached, but provider validation still reports `CNAME record not set`. See [DEPLOYMENT.md](DEPLOYMENT.md).

The existing Google browser session opened domain verification for `pokemonsurvivorwiki.com`; its TXT value and the two website CNAME records are prepared in [DNS-RECORDS.md](DNS-RECORDS.md). The CLI token lacks DNS editing permission and the Cloudflare dashboard login has not completed. The owner has been asked to restore that login or apply the prepared records. GSC Wizard still needs reconnection, but the signed-in browser can complete verification once DNS is present. No sitemap or indexing request has been submitted.

## Earlier observations — superseded by the release status above

- GSC Wizard `list_sites` returned `UNAUTHORIZED`: “This app connection requires reauthentication. Reconnect the app and try again.” No property data was available, and no sitemap was submitted.
- Standard Python HTTP requests to homepage, robots.txt and sitemap.xml returned 403; the homepage response identified Cloudflare and body `error code: 1010`.
- A normal headless Chromium homepage navigation timed out after 20 seconds before DOMContentLoaded.
- These observations apply to this session’s requests. They do not prove that Googlebot is blocked, that the domain has no deployment, or that the local Wiki build is live.

## Remaining launch actions

1. Restore the Cloudflare dashboard login or apply the three prepared DNS records, preserving unrelated records.
2. Verify both custom domains are active, the apex serves the intended build over HTTPS, www redirects to apex, and robots/sitemap/favicon and real 404 behavior are correct.
3. Complete domain verification in the owner's Search Console session.
4. Submit `https://pokemonsurvivorwiki.com/sitemap.xml`, inspect the homepage and key guides, and request indexing for a few complete core pages. URL Inspection API status alone does not submit indexing requests.

Submission is discovery, not guaranteed indexing. Do not repeatedly resubmit the same URL to try to accelerate crawling. No generic Indexing API workaround, purchased indexing service or mass ping was used.

## References

- Google favicon requirements: https://developers.google.com/search/docs/appearance/favicon-in-search
- Google recrawl requests and sitemap guidance: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
