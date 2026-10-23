"""Release-contract checks for the October 23 evening V11 review."""
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
DIST = HERE / 'dist'

expected = {
    '': {
        'coins': 'Coins missing or not syncing between phone and PC?',
        'lag': 'Still connected but lagging?',
        'mobile': 'Why is Manual Aim unavailable with a controller on mobile?',
        'updates': 'Review map: date, source and evidence',
        'home': 'Coins safety & V11 tool review',
    },
    'es/': {
        'coins': '¿Faltan monedas o no se sincronizan entre el móvil y el PC?',
        'lag': '¿Sigue habiendo lag después de la reconexión?',
        'mobile': '¿Por qué no aparece Apuntar a mano con mando en móvil?',
        'updates': 'Fechas y fuentes',
        'home': 'Seguridad de monedas y revisión V11',
    },
    'it/': {
        'coins': 'Monete mancanti o non sincronizzate tra telefono e PC?',
        'lag': 'Lag anche dopo la correzione?',
        'mobile': 'Perché Mira manuale non appare con un controller su mobile?',
        'updates': 'Date e fonti',
        'home': 'Sicurezza monete e verifica V11',
    },
    'zh-hant/': {
        'coins': '手機與電腦金幣不同步，或突然顯示 0？',
        'lag': '重連修正後仍然卡頓？',
        'mobile': '為什麼手機接手把後仍沒有手動瞄準？',
        'updates': '核查日期與來源',
        'home': '金幣安全與 V11 工具核查',
    },
}

for prefix, text in expected.items():
    root = DIST / prefix
    home = (root / 'index.html').read_text(encoding='utf-8')
    save = (root / 'save-recovery/index.html').read_text(encoding='utf-8')
    coop = (root / 'co-op/index.html').read_text(encoding='utf-8')
    mobile = (root / 'mobile/index.html').read_text(encoding='utf-8')
    updates = (root / 'updates/index.html').read_text(encoding='utf-8')
    assert text['home'] in home and '2026-10-23' in home
    assert text['coins'] in save and 'coins_differ' in save and 'shiny_missing' in save
    assert text['lag'] in coop and 'value="lag"' in coop and 'value="disconnect"' in coop
    assert text['mobile'] in mobile
    assert text['updates'] in updates
    assert all(commit in updates for commit in ('40c51c1', 'ce57853', '6f0f440'))
    assert 'guaranteed recovery' not in save.lower()

english_save = (DIST / 'save-recovery/index.html').read_text(encoding='utf-8')
assert '/assets/media/coins-sync-states.svg' in english_save
assert (DIST / 'assets/media/coins-sync-states.svg').is_file()

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = ET.fromstring((DIST / 'sitemap.xml').read_text(encoding='utf-8')).findall('s:url', ns)
assert len(urls) == 104
lastmods = {u.findtext('s:loc', namespaces=ns): u.findtext('s:lastmod', namespaces=ns) for u in urls}
for locale in ('', 'es/', 'it/', 'zh-hant/'):
    for slug in ('', 'save-recovery/', 'updates/', 'mobile/', 'co-op/', 'tier-list/', 'builds/', 'move-evolutions/', 'arceus-judgment/', 'how-to-play/'):
        assert lastmods[f'https://pokemonsurvivorwiki.com/{locale}{slug}'] == '2026-10-23'

print('PASS: V11 coins safety, co-op lag, mobile controller, source map, four-language content and sitemap dates.')
