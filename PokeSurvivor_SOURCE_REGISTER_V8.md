# PokeSurvivor Source Register V8

| Scope | Evidence | Use and boundary |
|---|---|---|
| Current game source | `ce5785313b0205af8b9477423f64b0a7b7039dcd` | Shop, TMs, natures, abilities, second starting move and co-op spectating |
| Kecleon Shop | `js/data/shop.js`, `js/data/tms.js`, `js/systems/mons.js` | prices, eight-offer rule, Europe/Madrid date and partner replacement |
| Nature and ability data | `js/data/natures.js`, `js/data/abilities.js`, `js/data/ability-fx.js` | 25 natures, slots and game-specific effects |
| Build rules | `js/data/upgrades.js`, `js/data/starters.js`, `js/systems/mons.js` | 400/1,500/400 coin unlock model and TM teaching |
| GSC aggregate | live UI, updated 2026-10-16 | 82 excluded, including 64 crawled-not-indexed; lagging report |
| GSC URL inspection | live UI, 2026-10-22 | `/zh-hant/starter-tier-list/`, `/arceus-judgment/`, `/es/gacha-calculator/` indexed with valid HTTPS and breadcrumb data |
| Existing media | existing project credit register and original site assets | no V8 third-party media copied without a reusable basis |
| V8 system illustrations | four original AI-assisted source images generated 2026-10-22; prompts and source filenames recorded in `wiki/media-images.json` | concept visuals for Shop, TM compatibility, natures and abilities; explicitly not gameplay screenshots |

