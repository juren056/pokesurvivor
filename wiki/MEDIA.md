# Media expansion — 15 October 2026

## Delivered scope

40 distinct images placed in article/homepage figures: 24 normal game captures, 8 original AI-assisted concept illustrations and 8 source-derived SVG diagrams. A separate, visibly labeled controlled-evolution capture is used as a video poster. The published manifest therefore contains 41 image assets. Six distinct silent recordings have English WebVTT captions, visible scope descriptions, native controls and HTML transcripts.

| Recording | Approximate duration | Evidence scope |
| --- | ---: | --- |
| Start a fresh guest run | 39s | Actual login, quiz, partner choice and opening, paced automatic UI inputs |
| Compare three opening partners | 25s | Actual starter selection; no performance ranking claim |
| Move, attack and pause | 22s | Actual keyboard controls and settings; fresh run has one attack |
| First battlefield preview | 22s | Actual normal combat, automated keyboard inputs |
| Landscape touch controls | 22s | Chromium touch emulation, not a physical-phone test |
| Golden evolution card | 20s | Clearly labeled controlled mechanics demonstration; prerequisites preconfigured |

Home, how-to-play, mobile, evolution, builds, starters, tier list, types, Pokédex, legendary, co-op and download pages receive relevant media. Existing text, URLs, titles, descriptions, primary headings, source data, calculators, account/analytics identifiers and indexing policy are preserved. The 17 canonical sitemap pages stay the same; image discovery entries are added. VideoObject metadata matches the real recordings; no standalone video watch-page or Google video-indexing claim is made.

## Original art and files

Built-in imagegen produced all eight illustration masters. The scene/prompt set is [media-art.json](media-art.json): Rift Guardian, fire trail, water trail, grass trail, rift atlas, co-op camp, evolution notebook and mobile expedition. Original PNG masters were copied into ignored `artifacts/media-originals/`; production WebP variants are committed in `public/media/`. Sharp performs mechanical responsive encoding, without synthesizing gameplay or modifying competitor artwork. The hero's 1440px version is 206,676 bytes; the browser selects smaller variants when appropriate.

Original diagrams: first-run flow, desktop controls, evolution checkpoints, Ember → Fire Blast, Bubble → Surf, build planning, touch controls and softened type factors. The diagram generator is `media_diagrams.py`. Mechanic names and prerequisites were checked against `data/game.json` and the pinned source.

## Capture and rights record

Game source: JPTER78 / PokéSurvivor, snapshot `b29708900da26b34e70d2dc07ad1659a719f4a78`. Disposable guest sessions only; original game files and existing user progress were not changed. Windows Playwright Chromium supplied automated mouse/keyboard inputs. Desktop normal combat used the unbundled `dev.html` source build and read-only state observations to drive keyboard movement. Touch clips used emulated mobile input at 844 × 390 and the portrait rotation prompt at 390 × 844.

Embedded SpriteCollab artwork remains CC BY-NC 4.0, with the original source and individual artist credits linked in `/about/#media-credits`. The site has no ads; these captures do not clear future commercial use. Competitor layouts/topics informed placement; no competitor image files were copied or hotlinked. Pokémon ownership notices remain intact.

`media-images.json`, `media-diagrams.json` and `media-videos.json` retain source, rights, captions, dimensions, build/platform scope, generation prompts where relevant, and controlled-test details. The build exports actual placements to `/assets/media/manifest.json`.

## Evidence differences from the initial shot plan

- Three normal automated guest trials reached levels 4, 6 and 5 without completing an evolution. The natural complete-evolution shot is **NOT_OBSERVED**.
- The published evolution clip is an actual engine/UI demonstration with preconfigured Ember level five and Power, using the developer's exposed level-up trigger. A large visible controlled-demo label stays in the picture; captions, transcript, description and manifest repeat its scope. It proves the golden-card/evolution response in that fixture, not earning the prerequisites through normal play.
- Physical iPhone/Android testing, home-screen installation/offline certification and comparable before/after build benchmarks are **NOT_RUN**. No FPS, survival-time superiority or real-device certification is claimed. The build clip instead demonstrates the actual starter-selection decision.

## Acceptance completed locally

- `python wiki/ci_build.py`: source export, production build, final HTML/link/schema/indexing checks and analytics-consent checks passed.
- `python wiki/browser_check.py`: 54 route/viewport checks and 8 task groups passed, no page JavaScript errors.
- `python wiki/redesign_check.py`: protected SEO/data fields, 8 intermediate-width checks and 5 interaction groups passed. The sitemap comparison preserves canonical pages/dates while allowing the planned image extension.
- `python wiki/media_check.py`: all 18 routes' images loaded, 20 critical route/viewport checks passed, all 6 videos decoded, started, sought to another time and ended; captions loaded and transcripts opened. Failed-video recovery retained the transcript. No WebM downloaded before deliberate play.
- Local preview Range requests returned the correct 206 bytes; an unsatisfiable range returned 416 and the actual file size. Production behavior requires its own post-release check.
- Source diff confirms no original game code/assets were edited. Original source snapshot hashes remain valid.

During verification, stream-copy trimming retained keyframe pre-roll, so final clips were re-encoded to align starts and captions. A stale preview process and missing Range support initially prevented seeking; the old local server was replaced and proper range handling added. Final playback checks passed after those fixes. The design detector reported advisory typography/palette findings on the incumbent stylesheet; the established Pixelify identity and Arial reading font were retained, as documented in DESIGN.md.

Screenshots and machine reports are in ignored `artifacts/media-*.png`, `artifacts/media-report.json`, `browser-report.json` and `redesign-report.json`. This document records local acceptance; the post-push production version and HTTP/playback evidence are recorded separately in `artifacts/media-production.json` after deployment, without triggering another build for a report-only commit.
