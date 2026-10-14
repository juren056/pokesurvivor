# Wiki launch record — 2026-10-15

**Current status:** Cloudflare browser deployment and DNS are complete; apex and www are Active with SSL. See [CF-LIVE.md](CF-LIVE.md). Earlier pending DNS/login observations below are historical; GSC account verification/submission and GA4 receipt are still unverified.
## Product and boundary

- Domain: `pokemonsurvivorwiki.com`.
- Scope: English independent reference for JPTER78’s browser PokéSurvivor.
- Pokémon Survivor Burst is a separate ClessioTV project. Do not reuse these databases as Burst data.
- Original root game files, domains, accounts, saves and infrastructure are preserved. Deploy only `wiki/dist`.
- The supplied CSV was treated as a task inventory and research leads, not evidence of demand or authority to alter accounts.

## CSV coverage

| Original task | Decision | Implemented destination / remaining condition |
| --- | --- | --- |
| P0 Tier List | CHANGE → implemented | `/tier-list/`; transparent starter-stat scoring, no invented playtesting |
| P0 Home/Wiki | CREATE → implemented | `/`; game identity, primary player tasks, database entrances |
| P0 How to play/mobile | CREATE → implemented | `/how-to-play/`, `/mobile/` |
| P1 Dex | CREATE → implemented | `/pokedex/`; 966 static rows, type and text filters |
| P1 Starters | CREATE → implemented | `/starters/`; 29 partners, starting moves and evolution prerequisites |
| P1 Download/APK | CONSOLIDATE → implemented | `/download/`; verified browser/source route; no unverified APK mirror |
| P1 Moves | CREATE → implemented | `/moves/`; 64 source-defined moves |
| P2 Types | CREATE → implemented | `/types/`; static chart plus dual-type calculator |
| P2 Legendary capture | CHANGE → implemented | `/legendaries/`; distinguish rift encounters/rewards from collection eligibility |
| P2 Codes | WATCH | No established redemption system in reviewed evidence; no speculative code page |
| P2 Discord/password | CONSOLIDATE → implemented | `/co-op/` account recovery and developer links; no guessed Discord invite |
| P2 iOS/Android | CONSOLIDATE → implemented | `/mobile/`; platform-specific home-screen instructions, no fabricated native release |
| P2 What is/release | CONSOLIDATE → implemented | Home and `/survivor-vs-burst/`; no unsupported release-date claim |
| P2 ES/PT mirrors | WATCH | Deferred until English quality and language-maintenance capacity justify expansion |
| Added evolution/build tasks | CREATE → implemented | `/move-evolutions/` with eligibility checker; `/builds/` with source-based routes |
| Source transparency/supporting pages | CREATE → implemented | `/about/`, `/privacy/`, `/updates/` |
| Search | CREATE → implemented | `/search/`, noindex; 1,047 valid guide/entity/move targets |

## Sources and maintenance

Original snapshot: `b29708900da26b34e70d2dc07ad1659a719f4a78`. The adapter records exact SHA-256 hashes in `wiki/data/game.json`. It refuses uncommitted edits in source evidence, and source-related Git history determines source links rather than later Wiki-only commits.

Competitor references inspected on 2026-10-15:

- https://pokesurvivorwiki.com/ — grouped guide/database navigation and tool discovery.
- https://pokesurvivor.org/ — concise mechanic entrances and reference categories.

No competitor prose, CSS, branding or image assets were copied. No traffic, KD or ranking estimates have been independently validated. Primary mechanics come from the supplied game source; visual brand mark is original SVG geometry. Pixelify Sans is bundled with OFL; original Pokémon sprites are not distributed in the Wiki build.

Important correction: `leg` classifies a Pokémon; it does not prove rift-only acquisition. The regional gacha pool checks generation, rarity and sprite availability, without a legendary exclusion. The Wiki exports actual pool eligibility and explains that rift victory grants rewards and move links rather than normal partner ownership.

Content review dates are editorial constants in `content.json`; builds do not replace them with the current clock. When updating a topic, review its affected source files, content, internal summaries and tools together. Do not change a date merely because the site was rebuilt. Track page-level dates separately when future updates affect only a subset of pages.

## Validation

- Build: `node wiki/export-data.cjs`, `python wiki/build.py`.
- Final-output checks: `python wiki/check.py` — metadata, self-canonical URLs, index policy, source hashes, JSON-LD, IDs, internal links, anchors, sitemap and search destinations.
- Browser checks: `python wiki/browser_check.py` against `python wiki/serve.py --port 4173`. Covers 18 routes × 3 viewports: 1440×1000, 390×844, 375×500. Separate checks cover filters/reset, empty state, evolution eligibility/invalid input/buffs, dual-type cap/immunity, search/back/query escaping, mobile menu/Escape, true HTTP 404, failed-tool static fallback and no-JavaScript navigation/tables.
- Evidence: ignored `wiki/artifacts/` contains browser report and desktop/mobile captures. Recreate it by running the browser checks.
- One Impeccable mechanical scan completed; the only finding was an Arial overused-font warning. Arial is confined to readable body/interface text, with self-hosted Pixelify branding/display; the warning is not a failed accessibility check.
- Independent finish review identified the acquisition error above; the final verdict scored it **resolved**, with disposition **ship at this fix scope**. This confirms that correction, not gameplay or production certification. Gameplay and real-device compatibility were not tested.
- Design documentation completed in `wiki/DESIGN.md` and `wiki/.impeccable/design.json`; all eight canonical sections and schema-version-2 JSON were verified.

## Production release and remaining account work

The dedicated Cloudflare Pages release succeeded on 2026-10-15. All 18 routes and key assets were checked against the local build over HTTPS, including real 404 behavior. The published URL is https://pokemonsurvivorwiki.pages.dev/. Both apex and www are attached to the project but await CNAME records. The Google domain-verification TXT value has also been prepared. See [DEPLOYMENT.md](DEPLOYMENT.md) and [DNS-RECORDS.md](DNS-RECORDS.md).

The CLI token cannot edit DNS and the Cloudflare dashboard login has not completed. Remaining steps are the prepared DNS changes, custom-domain HTTPS/redirect checks, Google domain verification and sitemap submission. No DNS change, sitemap submission, indexing request, GitHub push, analytics setup or ad account change has been performed.

If collecting site feedback later, add the real site-owner contact route. No email address, author credentials or business identity has been invented.
