"""Release-contract checks for the October 19 V4 source sync."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))
SOURCE = '5a23d49a99a795f9262d2fb24a9842f0858a0b50'

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

moves = {m['id']: m for m in data['moves']}
assert moves['tackle']['damage'] == 16 and moves['tackle']['radius'] == 60
assert moves['nasty-plot']['category'] is None and moves['swords-dance']['category'] is None
psyduck = next(s for s in data['starters'] if s['name'] == 'Psyduck')
assert psyduck['baseStart'] == 'confusion' and 'confusion' in psyduck['startChoices']
assert 'nasty-plot' not in psyduck['startChoices'] and 'swords-dance' not in psyduck['startChoices']

ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
root = ET.fromstring((HERE / 'dist/sitemap.xml').read_text(encoding='utf-8'))
assert len(root.findall('s:url', ns)) == 88
for locale in ('es','it','zh-hant'):
    moves_html = (HERE / f'dist/{locale}/moves/index.html').read_text(encoding='utf-8')
    evolutions_html = (HERE / f'dist/{locale}/move-evolutions/index.html').read_text(encoding='utf-8')
    builds_html = (HERE / f'dist/{locale}/builds/index.html').read_text(encoding='utf-8')
    assert '103' in moves_html and 'hyper-beam' in moves_html
    assert '97' in evolutions_html and 'hyper-beam' in evolutions_html
    assert 'build-starting' in builds_html and 'build-start-owned' in builds_html

print('PASS: V4 source, 103 moves, 97 evolutions, upgrade rules, save timing, locales and 88-URL sitemap.')
