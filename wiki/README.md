# Pokémon Survivor Wiki

Independent static Wiki for **pokemonsurvivorwiki.com**. The repository root remains the original game; deploy **only `wiki/dist`**.

## Build and preview

Requires Node 18+ and Python 3.12+. No npm dependencies for the build. Browser checks use Python Playwright.

```powershell
node wiki/export-data.cjs
python wiki/build.py
python wiki/check.py
python wiki/serve.py --port 4173
```

Open http://localhost:4173. The preview server returns a real 404 for unknown paths. `wiki/dist` is generated and ignored. Content lives in `wiki/content.json`, layout in `wiki/build.py`, styles and behavior in `wiki/public`. Export captures the local game commit and SHA-256 of source files. Re-export after reviewing a game update; do not substitute competitor data.

The original Rift Guardian favicon family is stored under `wiki/public/icons`. It builds without extra dependencies. For icon regeneration and file details see `wiki/branding/README.md`; optional icon checks use `python wiki/check_icons.py` (Pillow). See `wiki/GSC-LAUNCH.md` for the current production/GSC handoff.

The trainer handbook redesign is described in `wiki/UI-REDESIGN.md`. With the local preview running, `python wiki/browser_check.py` checks the existing routes and tools; `python wiki/redesign_check.py` checks starter previews, numeric sorting, type deep links, intermediate widths and the included SEO/data baseline. Both browser suites require Python Playwright and its Chromium runtime. Test screenshots and reports are written into ignored `wiki/artifacts/`.

## Hosting

The dedicated Cloudflare Pages project is live at https://pokemonsurvivorwiki.com/. Apex and www are Active with SSL; www and Pages hostnames redirect to the canonical apex. See [CF-LIVE.md](CF-LIVE.md) for the current browser release. See [DEPLOYMENT.md](DEPLOYMENT.md) for verified release evidence and [DNS-RECORDS.md](DNS-RECORDS.md) for the remaining records.

Automatic production deployments are connected to `juren056/pokesurvivor` on GitHub. Push reviewed changes to `main`; Cloudflare builds from root directory `wiki`, runs `python3 ci_build.py`, and publishes `dist`. See [AUTO-DEPLOY.md](AUTO-DEPLOY.md). Only the Wiki output is served. The original game's Firebase/Worker configuration is separate. DNS and hostname redirects remain in Cloudflare settings.


## Sources and content policy

Core source: https://github.com/JPTER78/pokesurvivor. The Wiki ships data and attributed code-derived mechanics; it does not distribute SpriteCollab artwork. Pixelify Sans is shipped with its OFL license. Keep repository MIT notices. Pokémon trademarks remain with their owners. This build does not certify commercial rights to other Pokémon media.

No CAPTCHA, account collection or ads are added. Owner-requested optional GA4 is now published with opt-in controls; see wiki/MEASUREMENT.md. Configure actual legal/contact details before introducing those services. Search and filters are local, and search results use `noindex`. English only at launch; do not generate empty translations or species pages. Content modification dates are editorial fields, not the build clock.

## Scope ledger

See `wiki/LAUNCH.md` for CSV coverage, evidence limitations and deployment checklist.
