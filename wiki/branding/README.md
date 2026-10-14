# Rift Guardian icon family

Original vector identity for Pokémon Survivor Wiki, created 2026-10-15.

The companion face represents the player’s partner; the interrupted orbit suggests surviving and escaping the horde; the gold spark suggests a rare find or breakthrough. The shape uses angular ears and generous eye cutouts so it remains recognizable in a browser tab. It does not reproduce a named Pokémon, official ball mark or competitor logo.

## Files

- Master: `wiki/public/mark.svg`, scalable 64×64 viewBox.
- PNG: `wiki/public/icons/icon-{16,32,48,96,180,192,512}.png`.
- ICO: `wiki/public/icons/favicon.ico`, embedded 16×16, 32×32 and 48×48 images.
- Apple: `wiki/public/icons/apple-touch-icon.png`, opaque 180×180 background.
- Maskable: `wiki/public/icons/icon-maskable-512.png`, opaque 512×512 with inset artwork.
- Manifest: `wiki/public/site.webmanifest`.
- Preview: `wiki/branding/preview.html` and `wiki/branding/preview.png`.

Palette: forest `#213e34`, paper `#f6f6ee`, orbit coral `#ee785f`, survival spark `#f2c66d`, leaf `#aabd91`, nose red `#b73d2c`.

PNG files include origin metadata. To regenerate exports after editing the SVG, run `python wiki/make_icons.py` (requires Python Playwright, Chromium and Pillow). Ordinary site builds use the committed exports without those dependencies.

The build publishes stable root URLs `/favicon.ico`, `/favicon-96.png`, `/apple-touch-icon.png` and `/site.webmanifest`, plus SVG and application assets under `/assets/`. All pages declare the icon family, including the noindex search/404 documents. The header uses the same vector master. Raster favicon is explicitly linked for crawler compatibility; the SVG supplies a crisp browser option.

A web manifest and icons do not themselves implement offline support, guarantee installability, or accelerate indexing. No service worker was added.
