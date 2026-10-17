# Baseline and risk — 2026-10-17

- Static Python builder: `wiki/build.py`; build command: `python3 ci_build.py` from `wiki/`; output: `wiki/dist`.
- Production: Cloudflare Pages from GitHub `juren056/pokesurvivor`, branch `main`.
- Canonical host: `https://pokemonsurvivorwiki.com`; Search is deliberately `noindex`; canonical content routes are listed in the generated sitemap.
- Starting HEAD: `ca29d9f`; upstream official game HEAD checked: `5bbc3b2` dated 2026-10-15.
- Protected winning routes retained: `/`, `/co-op/`, `/download/`, `/tier-list/`, `/builds/`, `/mobile/`, `/pokedex/`, `/moves/`, `/move-evolutions/`, `/starters/`, `/types/`, `/legendaries/`, `/updates/`.
- Main risks: current GSC coverage aggregate is still processing; post-`b297089` game code is noncommercial; SpriteCollab sprites are CC BY-NC; third-party APK/port claims are not official; gameplay advice derived from source is not first-person testing.
- Release rule: no route deletion, slug change, blanket redirect, copied competitor asset or false `lastmod` refresh.
