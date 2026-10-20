"""Release-contract checks for the October 20 V5 source sync."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))
SOURCE = '018e986f4c12f414dfa84193ee35b2959b1e325c'

assert data['source']['commit'] == SOURCE
assert len(data['dex']) == 966
assert len(data['starters']) == 29
assert len(data['moves']) == 103
assert len({m['id'] for m in data['moves']}) == 103
assert sum(bool(m.get('evolution')) for m in data['moves']) == 97
assert {'homing','bounce','charge','spin','quake','vortex','shove','stun'} <= {m['kind'] for m in data['moves']}

rules = data['rules']
assert rules['startingMove'] == {'upgradeId':'start','cost':400,'max':1,'excludesKind':'buff','defaultAlwaysAllowed':True}
assert rules['repertoire'] == {'upgradeId':'moves','cost':1500,'startMoves':2}
assert rules['singleTypeDamage']['multiplier'] == 1.2
assert rules['singleTypeDamage']['requiresSingleType'] and rules['singleTypeDamage']['requiresMatchingMoveType'] and rules['singleTypeDamage']['damagingOnly']
assert rules['cloudSave'] == {'pendingMs':1800000,'minUploadGapMs':65000}

ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
root = ET.fromstring((HERE / 'dist/sitemap.xml').read_text(encoding='utf-8'))
urls = root.findall('s:url', ns)
assert len(urls) == 88
assert len({u.findtext('s:loc', namespaces=ns) for u in urls}) == 88

for locale in ('', 'es/', 'it/', 'zh-hant/'):
    prefix = HERE / 'dist' / locale
    home = (prefix / 'index.html').read_text(encoding='utf-8')
    coop = (prefix / 'co-op/index.html').read_text(encoding='utf-8')
    moves = (prefix / 'moves/index.html').read_text(encoding='utf-8')
    evolutions = (prefix / 'move-evolutions/index.html').read_text(encoding='utf-8')
    assert '2026-10-20' in home
    assert 'data-coop-diagnostic' in coop
    assert '103' in moves and 'hyper-beam' in moves
    assert '97' in evolutions and 'hyper-beam' in evolutions

es_download = (HERE / 'dist/es/download/index.html').read_text(encoding='utf-8')
assert 'Descargar PokéSurvivor: Android, iPhone y PC' in es_download
zh_starters = (HERE / 'dist/zh-hant/starter-tier-list/index.html').read_text(encoding='utf-8')
assert '寶可夢' in zh_starters and 'Pokémon' in zh_starters

evolution_html = (HERE / 'dist/move-evolutions/index.html').read_text(encoding='utf-8')
assert 'coop-connection-check-flow' in (HERE / 'dist/co-op/index.html').read_text(encoding='utf-8')
assert '2026-10-15T00:00:00+00:00' in evolution_html
assert '2026-10-15"' not in evolution_html

print('PASS: V5 source, four locales, 103 moves, 97 evolutions, co-op tool, video date and 88 unique sitemap URLs.')
