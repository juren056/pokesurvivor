"""Cross-check the V3 exported mechanics and rendered SEO surface."""
from collections import Counter
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))
moves = {m['id']: m for m in data['moves']}

assert data['source']['commit'] == 'b8e843ffb8b07b95020fb77c4e9aca007d9a1e8d'
assert data['source']['verified'] == '2026-10-19'
assert len(data['dex']) == 966 and len(moves) == 65
assert all(all(k in p for k in ('pa', 'sa', 'df', 'sd')) for p in data['dex'])
assert moves['nasty-plot']['type'] == 'normal' and moves['nasty-plot']['category'] is None and moves['nasty-plot']['buffStat'] == 'satk'
assert moves['swords-dance']['buffStat'] == 'patk' and moves['dragon-dance']['buffStat'] == 'patk'
assert moves['toxic']['category'] == 'special' and moves['spikes']['category'] == 'physical'
# The exported values include the source's one-time melee adjustment: 13 -> 16 and 48 -> 60.
assert moves['tackle']['damage'] == 16 and moves['tackle']['radius'] == 60

tier = (HERE / 'dist/tier-list/index.html').read_text(encoding='utf-8')
bands = Counter(re.findall(r'class="rank rank-([SABC])"', tier))
assert bands == Counter({'C': 386, 'B': 290, 'A': 193, 'S': 97}), bands

sitemap = (HERE / 'dist/sitemap.xml').read_text(encoding='utf-8')
assert sitemap.count('<url>') == 88
assert '<lastmod>2026-10-19</lastmod>' in sitemap
assert 'https://pokemonsurvivorwiki.com/moves/' in sitemap

for locale in ('es', 'it', 'zh-hant'):
    html = (HERE / f'dist/{locale}/moves/index.html').read_text(encoding='utf-8')
    assert '65' in html and 'nasty-plot' in html and '2026-10-19' in html

print('PASS: V3 source lock, four-stat schema, move categories, one-time melee values, tier bands, locales and 88-URL sitemap.')
