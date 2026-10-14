# Cloudflare live release — 2026-10-15

The domain and redirect configuration below remains live. Deployment is now connected to GitHub main; see [AUTO-DEPLOY.md](AUTO-DEPLOY.md). The manual-upload record below is historical.

## Browser execution

- Reauthenticated the existing owner account using Google sign-in; no new account or API token.
- Reused the existing `pokemonsurvivorwiki` Pages project. The separate similarly named Worker has no active routes and was not used.
- The purchased domain was already imported. Its only DNS records were two proxied apex A records pointing to `54.149.79.189` and `34.216.117.25`. Saved their values in ignored `artifacts/dns-before.json`, removed one and replaced the other with the Pages CNAME.
- Current records: proxied apex and www CNAMEs to `pokemonsurvivorwiki.pages.dev`; apex GSC verification TXT from the owner's prior verification dialog. No unrelated mail/verification records existed or were removed.
- Both custom domains now show **Active / SSL enabled** in Pages.
- Zone Single Redirect `030b9793c2d0489b844318f31820fc63`: HTTPS www to HTTPS apex, status 301, preserving path and query.
- Account Bulk Redirect list `pokesurvivor_pages_to_domain`, ID `1234edd0c5374ab4a5f4d26f567fc41f`; enabled rule `78b712592d194faa9223f819fcc384ab`. Source `pokemonsurvivorwiki.pages.dev`, target `https://pokemonsurvivorwiki.com`, 301; preserve query, include subdomains, match subpaths and preserve suffix all enabled. This also redirects deployment preview hostnames.
- Disabled this zone's Cloudflare RUM to remove its automatically injected beacon. Final delivered HTML has no Cloudflare beacon and matches the reviewed build exactly. Optional GA4 is retained.

## Deployment

Uploaded the verified 49-file static output ZIP through **Create deployment → Production → file → Save and deploy**. The browser showed **Success!**.

Final production deployment: `f4bde231-24af-4cb1-b645-5aadaf0ce3ab`. Its underlying Pages hostname is also covered by the canonical-domain redirect.

The first browser deployment `e620d48d-90e6-47f4-ac07-889ac0828d26` contained an attempted hostname rule in `_redirects`; live testing showed no redirect. Official Pages documentation states domain-level redirects are unsupported there, so those rules were removed. The final static `_redirects` contains only an explanatory comment; Single/Bulk Redirects perform hostname routing. Sources: https://developers.cloudflare.com/pages/configuration/redirects/ and https://developers.cloudflare.com/pages/how-to/redirect-to-custom-domain/.

The project uses direct-upload output rather than a connected Git build. No GitHub push or Git connection was performed. Do not connect the original game repository root as the Wiki output. Future browser releases must upload the contents of `wiki/dist` after building/checking.

## Final checks

- `python wiki/build.py` and `python wiki/check.py` passed: 19 HTML documents, 17 sitemap URLs, 1,047 search targets.
- All 18 routes returned 200, byte-for-byte matching their local files.
- Sitemap, robots, 96px favicon and analytics JavaScript returned 200 and matched local bytes.
- Sitemap serves 17 canonical URLs as `application/xml`.
- Missing URL returns real 404.
- HTTPS www, production pages.dev, and final deployment hostname return 301 to the same apex path with query preserved.
- Browser opened the apex homepage and confirmed the Pages hostname navigation lands on the purchased domain.

Evidence: `artifacts/custom-domain-final.json`, `artifacts/cf-browser-deploy-success.png`, `artifacts/cf-domains-active.png`, `artifacts/cf-redirect-active.png`, `artifacts/cf-pages-redirect-active.png`, `artifacts/custom-domain-home.png`.

## Measurement boundary

GSC TXT is now installed. This Cloudflare-only execution did not repeat Google ownership verification, submit the sitemap, link GSC to GA4, or claim GA4 event receipt. Those earlier account tasks remain separate from this now-successful deployment.
