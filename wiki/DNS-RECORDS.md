# Records needed for the purchased domain

**Current status:** Cloudflare browser deployment and DNS are complete; apex and www are Active with SSL. See [CF-LIVE.md](CF-LIVE.md). Earlier pending DNS/login observations below are historical; GSC account verification/submission and GA4 receipt are still unverified.
Domain: `pokemonsurvivorwiki.com`. Cloudflare Pages project: `pokemonsurvivorwiki`.

| Type | Name | Value | Proxy |
| --- | --- | --- | --- |
| CNAME | `@` | `pokemonsurvivorwiki.pages.dev` | Proxied |
| CNAME | `www` | `pokemonsurvivorwiki.pages.dev` | Proxied |
| TXT | `@` | `google-site-verification=Y7rH8qRgDoAApzDcpDkYH7V3gFdRKKoOpIyX2-GmTbc` | DNS only |

The TXT value was read from the signed-in Google Search Console domain-verification dialog for this domain on 2026-10-15. It is a public DNS ownership-verification value, not an API token or account password.

Both custom domains are already attached to the Pages project. Cloudflare currently reports `CNAME record not set`; the CLI OAuth login cannot edit DNS, and the dashboard session needs a working login. The site itself is already published at https://pokemonsurvivorwiki.pages.dev/.

Review existing records for the exact `@` and `www` website names before changing them. If a website A/AAAA/CNAME already occupies the name, replace the website routing deliberately rather than adding conflicting records. Preserve mail-related records and other TXT verification records. The accompanying `dns-records.bind` contains only the three requested entries; do not import it as a replacement for the whole zone.

After the records are applied: verify both custom domains become active, check actual HTTPS responses and www→apex redirect, then complete Google domain verification. Submit `https://pokemonsurvivorwiki.com/sitemap.xml` only after its actual response is reachable and correct. No sitemap has yet been submitted.
