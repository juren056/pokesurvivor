"""Rasterize the original SVG in Chromium and export the favicon family.

Re-run only when the SVG changes. Build uses the checked-in icon files and
does not require Playwright or Pillow. No external image/model service is used.
"""
from pathlib import Path
from io import BytesIO
import json
from PIL import Image, PngImagePlugin
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PUBLIC = HERE / 'public'
ICONS = PUBLIC / 'icons'
ICONS.mkdir(exist_ok=True)


def main():
    svg = (PUBLIC / 'mark.svg').read_text(encoding='utf-8')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 512, 'height': 512}, device_scale_factor=1)
        page.set_content('<style>html,body{margin:0;background:transparent}svg{display:block;width:512px;height:512px}</style>'+svg)
        image = Image.open(BytesIO(page.locator('svg').screenshot(omit_background=True))).convert('RGBA')
        browser.close()
    info = PngImagePlugin.PngInfo()
    info.add_text('Title', 'Rift Guardian — Pokémon Survivor Wiki')
    info.add_text('Source', 'Original vector design in wiki/public/mark.svg; rasterized with Chromium. No third-party character artwork.')
    for size in [16, 32, 48, 96, 180, 192, 512]:
        image.resize((size, size), Image.Resampling.LANCZOS).save(ICONS / f'icon-{size}.png', pnginfo=info, optimize=True)
    # Apple touch icons fill the square; the OS provides the corner mask.
    apple = Image.new('RGBA', (180,180), '#213e34')
    apple.alpha_composite(image.resize((180,180),Image.Resampling.LANCZOS))
    apple.convert('RGB').save(ICONS/'apple-touch-icon.png',pnginfo=info,optimize=True)
    image.save(ICONS / 'favicon.ico', format='ICO', sizes=[(16,16),(32,32),(48,48)])
    # Maskable icons keep every meaningful part comfortably inside the safe area.
    maskable = Image.new('RGBA', (512,512), '#213e34')
    maskable.alpha_composite(image.resize((416,416),Image.Resampling.LANCZOS),(48,48))
    maskable.convert('RGB').save(ICONS/'icon-maskable-512.png',pnginfo=info,optimize=True)
    manifest = {
        'id':'/', 'name':'Pokémon Survivor Wiki', 'short_name':'Survivor Wiki',
        'description':'Independent PokéSurvivor guides, move evolutions and game reference.',
        'lang':'en', 'start_url':'/', 'scope':'/', 'display':'standalone',
        'background_color':'#f6f6ee', 'theme_color':'#213e34',
        'icons':[
            {'src':'/assets/icons/icon-192.png','sizes':'192x192','type':'image/png','purpose':'any'},
            {'src':'/assets/icons/icon-512.png','sizes':'512x512','type':'image/png','purpose':'any'},
            {'src':'/assets/icons/icon-maskable-512.png','sizes':'512x512','type':'image/png','purpose':'maskable'}
        ]
    }
    (PUBLIC/'site.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Exported SVG-based PNG 16/32/48/96/180/192/512, ICO, Apple touch and maskable icons.')


if __name__ == '__main__':
    main()
