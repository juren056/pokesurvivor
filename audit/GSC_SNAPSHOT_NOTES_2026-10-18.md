# GSC snapshot notes — 2026-10-18

Inspection was performed in the authenticated Google Search Console browser session for the domain property `pokemonsurvivorwiki.com`.

- `/`, `/co-op/` and `/tier-list/` each report “URL is on Google”. Crawl is allowed, fetch succeeded, indexing is allowed, Googlebot Smartphone was used, and Google selected the inspected canonical.
- Last observed crawl times: `/tier-list/` 2026-10-18 04:28:26; `/co-op/` 2026-10-18 05:48:22; `/` 2026-10-17 23:46:55.
- The aggregate Page indexing report says data is still being processed and asks to return in about one day. Exclusion reasons and affected URL lists are therefore unavailable; this must not be reported as zero excluded pages.
- The Sitemap report lists `https://pokemonsurvivorwiki.com/sitemap.xml` as successful, submitted/read 2026-10-17, with 84 discovered pages and 0 discovered videos before this release.
- URL Inspection showed a temporary sitemap-processing message in discovery details, but the dedicated Sitemap report is the authoritative current submission status and is successful.

The new sitemap is validated locally at 88 canonical, indexable URLs. Recheck the aggregate indexing report after Google finishes processing and resubmit only if the successful sitemap status changes or the production sitemap cannot be fetched.

After deployment, the production sitemap at the submitted URL contains 88 canonical URLs. GSC still shows the prior discovery count of 84 from its last read on 2026-10-17; the submission itself remains successful and Google can reread the unchanged sitemap URL.
