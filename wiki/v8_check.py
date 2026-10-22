"""Release-contract checks for the October 22 V8 source sync."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))

assert data['source']['commit'] == 'ce5785313b0205af8b9477423f64b0a7b7039dcd'
assert data['source']['verified'] == '2026-10-22'
assert len(data['dex']) == 966 and len(data['starters']) == 29
assert len(data['moves']) == 103 and sum(bool(m.get('evolution')) for m in data['moves']) == 97
assert len(data['natures']) == 25
assert sum(n['neutral'] for n in data['natures']) == 5
assert len(data['tms']) == 58
assert len(data['naturalMoves']) == 966
assert data['shop']['dailyTmCount'] == 8
assert data['shop']['timeZone'] == 'Europe/Madrid'
assert data['shop']['items']['mint']['price'] == 1500
assert data['shop']['items']['cap']['price'] == 1500
assert data['shop']['items']['caph']['price'] == 5000
shadow = next(t for t in data['tms'] if t['id'] == 'shadow-ball')
flamethrower = next(t for t in data['tms'] if t['id'] == 'flamethrower')
assert 150 in shadow['compatibleDex'] and 54 not in flamethrower['compatibleDex']
huge_power = next(a for a in data['abilities'] if a['id'] == 'huge-power')
assert huge_power['effectType'] == 'specialized' and '50%' in huge_power['effect']
second = data['rules']['secondStartingMove']
assert second == {'upgradeId':'start2','cost':400,'max':1,'requires':'moves','cannotDuplicateFirst':True,'usesStartChoices':True}
assert data['rules']['repertoire']['cost'] == 1500

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = ET.fromstring((HERE / 'dist/sitemap.xml').read_text(encoding='utf-8')).findall('s:url', ns)
assert len(urls) == 104
assert len({u.findtext('s:loc', namespaces=ns) for u in urls}) == 104
assert all(u.find('s:lastmod', ns) is not None for u in urls)

for locale in ('', 'es/', 'it/', 'zh-hant/'):
    root = HERE / 'dist' / locale
    home = (root / 'index.html').read_text(encoding='utf-8')
    assert '2026-10-22' in home
    for slug, marker in {
        'kecleon-shop':'data-shop-preview',
        'tm-compatibility':'data-tm-checker',
        'natures':'data-nature-calculator',
        'abilities':'data-ability-checker',
    }.items():
        page = (root / slug / 'index.html').read_text(encoding='utf-8')
        assert marker in page
        assert '2026-10-22' in page

builds = (HERE / 'dist/builds/index.html').read_text(encoding='utf-8')
coop = (HERE / 'dist/co-op/index.html').read_text(encoding='utf-8')
save = (HERE / 'dist/save-recovery/index.html').read_text(encoding='utf-8')
assert all(x in builds for x in ('build-repertoire','build-second-owned','build-tm'))
assert 'Q/E' in coop and 'LB/RB' in coop and '#278' in coop
assert '#275' in save

print('PASS: V8 source, Shop, 58 TMs, 25 natures, abilities, second selector, four locales and 104-URL sitemap.')
