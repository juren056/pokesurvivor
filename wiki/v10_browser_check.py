"""Focused browser checks for the October 23 V10 release."""
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get('POKESURVIVOR_TEST_BASE', 'http://127.0.0.1:8765')
EXPECTED = {
    '': ('+50% damage with physical moves.', 'Manual Aim is not available on mobile'),
    'es': ('+50 % de daño con movimientos físicos.', 'En móvil, los ataques apuntan automáticamente'),
    'it': ('+50% di danni con le mosse fisiche.', 'Su mobile gli attacchi mirano automaticamente'),
    'zh-hant': ('物理招式傷害+50%。', '手機版招式一律自動瞄準'),
}

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    for locale, (effect, mobile_copy) in EXPECTED.items():
        prefix = f'/{locale}' if locale else ''
        page.goto(f'{BASE}{prefix}/abilities/', wait_until='load')
        assert effect in page.locator('#ability-huge-power').inner_text()
        assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
        page.goto(f'{BASE}{prefix}/mobile/', wait_until='load')
        assert mobile_copy in page.locator('main').inner_text()
        assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
        page.goto(f'{BASE}{prefix}/co-op/', wait_until='load')
        assert '45' in page.locator('main').inner_text()
    assert not errors, errors
    browser.close()

print('PASS: V10 ability effects, mobile correction and co-op limits render in four locales at 390px.')
