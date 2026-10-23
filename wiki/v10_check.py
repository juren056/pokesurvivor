"""Release-contract checks for the October 23 V10 source and content review."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))
DIST = HERE / 'dist'

assert DATA['source']['commit'] == '6f0f4409f68adcc5bc31a77cafaf8ba9a0318397'
assert DATA['source']['verified'] == '2026-10-23'
assert len(DATA['dex']) == 966 and len(DATA['moves']) == 103
assert sum(bool(move.get('evolution')) for move in DATA['moves']) == 97
assert len(DATA['abilities']) == 271
for ability in DATA['abilities']:
    assert set(ability['effects']) == {'en', 'es', 'it', 'zh-hant'}
    assert all(ability['effects'][locale].strip() for locale in ability['effects'])

by_id = {ability['id']: ability for ability in DATA['abilities']}
assert by_id['huge-power']['effects'] == {
    'es': '+50 % de daño con movimientos físicos.',
    'en': '+50% damage with physical moves.',
    'it': '+50% di danni con le mosse fisiche.',
    'zh-hant': '物理招式傷害+50%。',
}
assert 'under 1/3' in by_id['blaze']['effects']['en']
assert '+10%' in by_id['super-luck']['effects']['en']

locale_expectations = {
    '': ('+50% damage with physical moves.', 'Manual Aim is not available on mobile'),
    'es/': ('+50 % de daño con movimientos físicos.', 'En móvil, los ataques apuntan automáticamente'),
    'it/': ('+50% di danni con le mosse fisiche.', 'Su mobile gli attacchi mirano automaticamente'),
    'zh-hant/': ('物理招式傷害+50%。', '手機版招式一律自動瞄準'),
}
for prefix, (ability_text, mobile_text) in locale_expectations.items():
    root = DIST / prefix
    home = (root / 'index.html').read_text(encoding='utf-8')
    abilities = (root / 'abilities/index.html').read_text(encoding='utf-8')
    mobile = (root / 'mobile/index.html').read_text(encoding='utf-8')
    coop = (root / 'co-op/index.html').read_text(encoding='utf-8')
    updates = (root / 'updates/index.html').read_text(encoding='utf-8')
    assert '2026-10-23' in home
    assert ability_text in abilities
    assert mobile_text in mobile
    assert '2026-10-23' in abilities and '2026-10-23' in mobile
    assert '45' in coop and '2026-10-23' in coop
    assert '6f0f440' in updates and '2026-10-23' in updates

es_mobile = (DIST / 'es/mobile/index.html').read_text(encoding='utf-8')
assert 'Activa Apuntar a mano' not in es_mobile
assert 'Accesibilidad para Mira manual' not in es_mobile

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = ET.fromstring((DIST / 'sitemap.xml').read_text(encoding='utf-8')).findall('s:url', ns)
assert len(urls) == 104
lastmods = {u.findtext('s:loc', namespaces=ns): u.findtext('s:lastmod', namespaces=ns) for u in urls}
for locale in ('', 'es/', 'it/', 'zh-hant/'):
    for slug in ('', 'abilities/', 'mobile/', 'co-op/', 'updates/'):
        assert lastmods[f'https://pokemonsurvivorwiki.com/{locale}{slug}'] == '2026-10-23'
assert all(not url.endswith(('llms.txt', 'index.md')) for url in lastmods)

print('PASS: V10 source, four-language ability effects, mobile correction, co-op recovery, homepage dates and 104-URL sitemap.')
