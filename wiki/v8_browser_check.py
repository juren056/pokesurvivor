"""Browser smoke tests for V8 tools and responsive layout."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get('POKESURVIVOR_TEST_BASE', 'http://127.0.0.1:8765')
HERE = Path(__file__).resolve().parent

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))

    checks = {
        '/kecleon-shop/': ('[data-shop-preview]', '#shop-tms li', 8, 'kecleon-shop-concept'),
        '/tm-compatibility/?p=150&tm=shadow-ball': ('[data-tm-checker]', '#tm-result', 1, 'tm-compatibility-concept'),
        '/natures/': ('[data-nature-calculator]', '#nature-result', 1, 'nature-balance-concept'),
        '/abilities/': ('[data-ability-checker]', '#ability-result', 1, 'ability-slots-concept'),
        '/builds/?p=4&r=1&u2=1&v=8': ('[data-build-planner]', '#build-result', 1, None),
    }
    for path, (tool, result, count, media_id) in checks.items():
        page.goto(BASE + path, wait_until='domcontentloaded')
        assert page.locator(tool).count() == 1, path
        assert page.locator(result).count() == count, path
        assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth'), path
        text = page.locator(result).first.inner_text()
        assert 'Loading' not in text and 'could not load' not in text, (path, text)
        if media_id:
            image = page.locator(f'[data-media-id="{media_id}"] img')
            image.scroll_into_view_if_needed()
            assert image.count() == 1, (path, media_id)
            assert image.evaluate('(img) => img.complete && img.naturalWidth > 0'), (path, media_id)
            assert image.get_attribute('srcset') and image.get_attribute('loading') == 'lazy'

    page.goto(BASE + '/tm-compatibility/?p=54&tm=flamethrower', wait_until='domcontentloaded')
    assert 'incompatible' in page.locator('#tm-result').inner_text().lower()
    page.goto(BASE + '/tm-compatibility/?p=150&tm=shadow-ball', wait_until='domcontentloaded')
    assert 'compatible' in page.locator('#tm-result').inner_text().lower()

    localized_media = {
        'kecleon-shop': 'kecleon-shop-concept',
        'tm-compatibility': 'tm-compatibility-concept',
        'natures': 'nature-balance-concept',
        'abilities': 'ability-slots-concept',
    }
    for locale in ('es', 'it', 'zh-hant'):
        for slug, media_id in localized_media.items():
            page.goto(f'{BASE}/{locale}/{slug}/', wait_until='domcontentloaded')
            image = page.locator(f'[data-media-id="{media_id}"] img')
            image.scroll_into_view_if_needed()
            assert image.count() == 1
            assert image.evaluate('(img) => img.complete && img.naturalWidth > 0')
            assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')

    page.set_viewport_size({'width': 1440, 'height': 1100})
    page.goto(BASE + '/kecleon-shop/', wait_until='domcontentloaded')
    page.locator('[data-media-id="kecleon-shop-concept"]').scroll_into_view_if_needed()
    page.screenshot(path=str(HERE / 'qa-v8-shop-media.png'), full_page=False)

    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(BASE + '/', wait_until='domcontentloaded')
    page.screenshot(path=str(HERE / 'qa-v8-mobile.png'), full_page=False)
    assert not errors, errors
    browser.close()

print('PASS: V8 tools execute, TM known pairs agree, four original images load in four locales, and 390px pages do not overflow.')
