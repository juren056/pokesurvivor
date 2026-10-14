---
name: Pokémon Survivor Wiki
description: A trainer expedition handbook with forest-night identity and calm reference surfaces.
colors:
  paper: "#f5f5ed"
  white: "#fffef8"
  ink: "#203b33"
  muted: "#53685c"
  line: "#cfd9ca"
  forest: "#142f28"
  forest-deep: "#10261f"
  forest-line: "#355348"
  forest-muted: "#c0d2c3"
  gold: "#f2c66d"
  gold-hover: "#ffda8d"
  red: "#a73727"
  leaf: "#e4eddd"
typography:
  display:
    fontFamily: "Pixelify, Arial, sans-serif"
    fontSize: "clamp(2.7rem, 4.9vw, 4.4rem)"
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: "-.025em"
  article-title:
    fontFamily: "Pixelify, Arial, sans-serif"
    fontSize: "clamp(2.2rem, 4vw, 3.5rem)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-.025em"
  headline:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "clamp(1.7rem, 3vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.17
    letterSpacing: "-.025em"
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "16px"
    lineHeight: 1.7
  label:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "12px"
    fontWeight: 700
  table:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "13px"
rounded:
  badge: "4px"
  choice: "5px"
  control: "7px"
  search: "8px"
  disclosure: "10px"
  surface: "14px"
spacing:
  tight: "8px"
  control-gap: "12px"
  field-gap: "16px"
  mobile-inset: "20px"
  tablet-inset: "26px"
  desktop-inset: "40px"
  section: "60px"
components:
  button-primary:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.white}"
    rounded: "{rounded.control}"
    padding: "12px 21px"
  button-hero:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.forest-deep}"
    rounded: "{rounded.control}"
    padding: "12px 21px"
  button-hero-hover:
    backgroundColor: "{colors.gold-hover}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "12px 21px"
  button-secondary-hover:
    backgroundColor: "{colors.leaf}"
  input:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "11px 13px"
  tool:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.white}"
    rounded: "{rounded.surface}"
    padding: "27px 30px"
  starter-lab:
    backgroundColor: "#1e3d32"
    textColor: "{colors.white}"
    rounded: "{rounded.surface}"
    padding: "25px 27px"
  table-heading:
    backgroundColor: "#dde8d6"
    textColor: "{colors.ink}"
    padding: "13px 11px"
---

# Design System: Pokémon Survivor Wiki

## Overview

**Creative North Star: "The Trainer Expedition Handbook"**

Forest-night framing, gold actions and warm paper give the Wiki a game identity while leaving reference content calm and readable. Pixelify identifies the world; plain sans-serif text carries explanations, controls and data. The original Rift Guardian mark anchors the independent Wiki identity.

Density follows the task: ruled lists and real tables support quick comparison, while tools gather related controls into a distinct forest panel. Elemental colors accompany written types. This system is extracted from the implemented stylesheet and desktop/mobile renders after the authorized redesign.

**Key Characteristics:**

- Forest-night frame with gold actions and warm reading surfaces.
- Pixel identity paired with readable reference typography.
- Native controls, useful source-backed previews and real tables.

## Colors

### Primary

Forest and forest-deep frame the opening, masthead, footer and mobile navigation. Gold marks opening actions, selected partner choices, dark-surface links and active navigation; gold-hover supplies action feedback. On paper, the filled primary button uses forest with warm-white lettering.

### Secondary

Red supports ordinary link hover, list markers, field accents and carets. Leaf separates notices and outlined-button hover states from paper. Forest-line divides dark regions; forest-muted supports secondary dark-surface text. Elemental badges use the semantic fills and foregrounds in the stylesheet, always with written type names.

### Neutral

Paper is the reading canvas, white fills fields, ink carries reading text and muted supports descriptions and dates. Line provides subtle paper-surface divisions. The token frontmatter is normative; additional local panel and elemental colors remain documented in the source stylesheet.

**The Contextual Action Rule.** Use gold actions on the forest opening and forest actions on paper; preserve their context-specific text and focus colors.

## Typography

Display and article titles use locally served Pixelify (700), falling back to Arial and sans-serif. Partner names, partner stat values, the brand and tool titles also use Pixelify. Body text, section headings, labels, navigation and tables use Arial, Helvetica and sans-serif. Keep the font's OFL with its local asset.

The frontmatter records the desktop hierarchy. General headings have balanced wrapping and compact line height. Paragraph measure is bounded (72ch); opening description is narrower (46ch). The opening heading reduces to 3.8rem at 1180px, 3.1rem at 850px and 3.15rem at 600px. Mobile article titles use 2.35rem. Tables and numerical identifiers use tabular numerals. The brand subtitle is small tracked uppercase; ordinary controls use sentence case.

**The Two Reading Speeds Rule.** Pixelify carries identity and selected numeric highlights; Arial carries long explanations and comparison data.

## Layout

The centered main frame is bounded (1360px) with desktop horizontal insets (40px). Header/footer padding follows a 1280px content frame with at least 24px inset. The full-width forest opening contains a 1.12fr/1fr hero grid (70px gap) and a ruled topic strip. Regular home sections have 60px vertical padding. Article layout pairs a flexible reading column with a 210px directory (58px gap); its aside sticks 115px below the viewport top.

At 1180px, columns, gaps and navigation tighten. At 850px, the menu button appears and navigation wraps below the masthead. With JavaScript, the menu opens on demand with a 45vh scrolling limit; without it, links remain visible. The hero stays two columns until 600px. Journey/reference regions and the article directory stack at 850px; the directory becomes a native disclosure above the article and loses sticky positioning. Main/tablet insets use 26px.

At 600px, the hero, route list and notebook stack; main insets use 20px and home sections use 36px vertical padding. A fixed bottom navigation exposes Guide, Pokédex, Evolve and Search. Its lower padding includes env(safe-area-inset-bottom); body reserves calc(66px + env(safe-area-inset-bottom)) so final content remains reachable.

Keep tables within bounded scrolling wrappers with stable scrollbar gutters. Preserve their real columns and headers instead of widening the page. Filter controls wrap and mobile search fields may take a full row.

## Elevation & Depth

Tonal regions and thin rules provide most separation. The starter lab has a restrained ambient shadow (0 14px 35px rgba(2,16,10,.15)). Mobile navigation has an upward shadow (0 -5px 18px rgba(6,22,13,.1)) and a top rule. Ordinary routes, reading surfaces and tables remain flat; they respond with color and row fill rather than lifted motion.

## Shapes

Tools, the starter lab, reference panels, notices and aside notes use the surface radius (14px). Controls use tighter corners (7px), search containers 8px, disclosures/filter groups 10px, choices/ranks 5px and type badges 4px. Thin straight rules organize data and lists. The type emblem uses a clipped pointed shield silhouette.

The original Rift Guardian mark combines an angular companion, broken coral orbit and gold survival spark in a 64×64 viewBox. The master is wiki/public/mark.svg; the generated header asset, favicon PNG/ICO and device icons derive from it. Preserve original-vector provenance and embedded raster origin metadata.

## Components

- **Buttons:** filled forest on paper, gold in the opening, or outlined secondary actions. Default minimum height is 47px; padding is 12px 21px. Background feedback takes .16s. Hero outlined actions use warm text and a dark green hover fill.
- **Fields and tools:** native inputs/selects have warm-white fill, visible labels and 7px corners. Tools use forest panels with gold outputs and native checkboxes. Their layout wraps without concealing labels. Loading, invalid-input and failed-load states use explicit text.
- **Search:** a real GET form targets /search/ with a named q field. The opening form combines an inline magnifier, native search input and a gold submit control with an accessible name. Search results require JavaScript; no-script text routes readers to guides and databases.
- **Starter lab:** three labeled native radios select source-backed Charmander, Bulbasaur or Squirtle previews. The transparent input owns the full clickable hit area; checked state paints the adjacent label gold and keyboard focus outlines it. The panel updates real stats, move, requirement and destination, with a polite atomic evolution announcement. Without JavaScript the choices are hidden, the initial Charmander preview remains readable, and the starter-guide link provides all options.
- **Navigation:** sticky forest-deep masthead, plain bold links, gold underlined current-page state and an accessible search destination. At compact widths the native menu button reflects aria-expanded; links remain available without JavaScript. Mobile bottom links retain visible icon and text labels.
- **Tables and badges:** compact left-aligned tables, tabular numbers, pale green headers and row hover/target fills. Enhanced headers expose native buttons, aria-sort and directional SVG feedback; no-script headers retain plain text. Preserve numeric sorting and bounded horizontal overflow. Type/rank colors always accompany words or letters; result counts and empty states explain filters.
- **Disclosures and focus:** native details/summary preserves source and contents access. Interactive elements receive a 3px visible outline offset by 4px; paper surfaces use the coral focus color, dark header/opening/tool/dock contexts use gold. Search-input focus has its local ink outline. The skip link appears when focused.
- **Motion:** only the starter lab receives the desktop arrive reveal at min-width 1000px (.55s, cubic-bezier(.16,1,.3,1), opacity .85 to 1 and clipped inset 5% to 0). Reduced-motion preference removes this animation, button transitions and smooth scrolling.

## Do's and Don'ts

### Do:

- Do preserve the forest-night frame, gold opening actions and calm paper reading surfaces.
- Do keep Pixelify for identity and selected highlights, and Arial for readable reference text.
- Do preserve native controls, visible focus, written type labels and bounded table scrolling.
- Do retain the Rift Guardian master and provenance on its derived icon exports.
- Do keep mobile navigation clear of device safe areas and reserve space below the document.

### Don't:

- Don't replace native radio selection, sortable header buttons or disclosures with decorative controls.
- Don't conceal navigation or the initial partner reference when JavaScript is unavailable.
- Don't add repeated motion to reading surfaces or animate when reduced motion is requested.
- Don't invent gameplay evidence or substitute third-party character art for the original mark.
