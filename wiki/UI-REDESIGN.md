# Trainer expedition handbook redesign

## Research and decisions — 2026-10-15

The user requested a stronger game identity and innovative layout informed by competing sites. The existing local Wiki is the implementation target; production access and GSC authentication are separate outstanding account tasks.

| Reference | Useful observed pattern | Application here |
| --- | --- | --- |
| https://pokesurvivorwiki.com/ | Separate guide, database and utility entrances; player-problem routes | Clear topic navigation, task-first homepage and discoverable evolution tool |
| https://pokesurvivor.org/ | Immediate explanation of the game and mechanic categories | Identify the browser project clearly, keep guide answers and source scope visible |
| https://pokesurvivor.games/ | Prominent destination for playing and explanation of adjacent games | Direct developer-game link, concise game identity and Burst disambiguation |
| https://pokesurvivor.com/ | Partner selection, elemental identity and compact gameplay information | Source-derived starter selector, elemental color coding and readable stat/evolution relationships |

These observations are structural references, not evidence of competitor traffic or ranking. No competitor code, prose or artwork is copied. No SpriteCollab sprite is added.

## Scope

Replace the broad editorial landing page with a trainer handbook: dark forest opening, original Rift Guardian identity, gold actions, colored elemental symbols and calm cream reading surfaces. Keep the source-backed Wiki as an actual reference rather than a simulated game dashboard.

Add meaningful interactions: starter preview with real source stats and evolution conditions, database sorting, and type shortcut links into the existing Pokédex. Keep native controls and a no-JavaScript reading/navigation fallback.

Preserve all canonical paths, page titles, index policies, source data, article facts and sitemap membership. Metadata and data baselines are saved in ignored `wiki/artifacts/redesign-seo-before.json`. Visual changes alone do not justify changing editorial review dates.

## Validation record

- Build and final HTML checks passed for 19 HTML documents, 17 indexable URLs and 1,047 search destinations.
- All icon formats remain valid and are declared on every page.
- Existing browser suite: 54 route/viewport checks and eight behavior groups passed.
- Redesign suite: eight intermediate-width checks (768/1024px), five behavior groups and exact SEO/data baseline comparisons passed.
- A first attempt to target the custom-styled radio directly timed out because its visual label intercepted clicks. The native input hit area was corrected, then all three real starter choices and their source data/destinations passed.
- The mechanical detector ran once. It reported an Arial body-font warning and design-token advisories relative to the previous design documentation. Those are expected during an authorized redesign; the new observed system is documented at finish.

Independent finish review returned **ship**, with no material defect found within the local rendered and code evidence. Minor suggestions concerned richer live announcements in the starter preview and earlier filter placement for frequent database users; neither was a required fix. The review did not certify production behavior, assistive-technology behavior or gameplay testing.

The reproducible protected-field snapshot is included in `wiki/seo-baseline.json`; only update it when intentionally changing reviewed SEO/data fields. The original before-snapshot and six final viewport images remain in ignored artifacts. Design documentation was refreshed from the new CSS: all eight canonical sections, current forest/paper tokens, schema-version-2 sidecar and original icon provenance were verified. Production deployment and indexing are not implied by local UI completion.
