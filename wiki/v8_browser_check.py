"""Browser smoke tests for V8 tools and responsive layout."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8765'
HERE = Path(__file__).resolve().parent

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))

    checks = {
        '/kecleon-shop/': ('[data-shop-preview]', '#shop-tms li', 8),
        '/tm-compatibility/?p=150&tm=shadow-ball': ('[data-tm-checker]', '#tm-result', 1),
        '/natures/': ('[data-nature-calculator]', '#nature-result', 1),
        '/abilities/': ('[data-ability-checker]', '#ability-result', 1),
        '/builds/?p=4&r=1&u2=1&v=8': ('[data-build-planner]', '#build-result', 1),
    }
    for path, (tool, result, count) in checks.items():
        page.goto(BASE + path, wait_until='networkidle')
        assert page.locator(tool).count() == 1, path
        assert page.locator(result).count() == count, path
        assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth'), path
        text = page.locator(result).first.inner_text()
        assert 'Loading' not in text and 'could not load' not in text, (path, text)

    page.goto(BASE + '/tm-compatibility/?p=54&tm=flamethrower', wait_until='networkidle')
    assert 'incompatible' in page.locator('#tm-result').inner_text().lower()
    page.goto(BASE + '/tm-compatibility/?p=150&tm=shadow-ball', wait_until='networkidle')
    assert 'compatible' in page.locator('#tm-result').inner_text().lower()

    for locale in ('es', 'it', 'zh-hant'):
        page.goto(f'{BASE}/{locale}/kecleon-shop/', wait_until='networkidle')
        assert page.locator('[data-shop-preview]').count() == 1
        assert page.locator('#shop-tms li').count() == 8
        assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')

    page.goto(BASE + '/', wait_until='networkidle')
    page.screenshot(path=str(HERE / 'qa-v8-mobile.png'), full_page=False)
    assert not errors, errors
    browser.close()

print('PASS: V8 tools execute, TM known pairs agree, four locales render, and 390px pages do not overflow.')
