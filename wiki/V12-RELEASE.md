# V12 release record — 2026-10-24

## Evidence reviewed

- Execution source: `PokeSurvivor_2026-10-24_Plan_V12.md`.
- Advisory evidence: `PokeSurvivor_2026-10-24_Analysis_V12.md`.
- Official game source locked to `d567c6da88e4ef66634ab54a01b5a3607501e03a`.
- GSC Coverage snapshot was last updated 2026-10-16: 82 not indexed, 19 indexed. Live inspection on 2026-10-24 showed `/zh-hant/gacha-calculator/` indexed; prior live checks also showed `/arceus-judgment/` and `/zh-hant/starter-tier-list/` indexed. The bulk “crawled, currently not indexed” report is therefore stale and was not used to bulk-noindex or redirect valid pages.
- The sole sampled 404 was a malformed external URL containing Chinese promotional copy after the hostname. It is not an internal route and no doorway page was created for it.

## Shipped

- Four-language Orbs guide and four-slot planner.
- Four-language Judgment rewrite with 17-Plate lookup, damage/survival leaderboard split, 35:00 item break, 1.25× HP and 1.15× damage scaling, and fixed status-damage guidance.
- Regional ×10/×100 gacha calculator with banner pity, Epic-protected final slot, ticket costs and explicit Shiny Charm scope.
- Official move snapshot updated to 103 moves and 97 evolutions. Evolved names retain `+`; stable IDs and historical display names remain available. Meteor Mash is 24 damage and radius 48.
- Homepage and source review date updated to 2026-10-24.
- Sitemap expanded to 108 canonical, indexable URLs with reciprocal four-language hreflang.
- Shop report #320 is recorded as a report, not a universal diagnosis.

## Media policy

Only repository-authorized official source data, existing licensed assets, original diagrams and clearly labelled concept art are published. No third-party image or video was copied without reuse rights, and no fake gameplay or `VideoObject` markup was added.

## Acceptance

`check.py`, `v12_check.py`, rendered mobile routes and interactive tool checks pass before deployment.
