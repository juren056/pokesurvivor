"""October 24 V12 acceptance checks."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
DIST=HERE/'dist'
data=json.loads((HERE/'data/game.json').read_text(encoding='utf-8'))
manifest=json.loads((DIST/'build-manifest.json').read_text(encoding='utf-8'))

assert data['source']['commit']=='d567c6da88e4ef66634ab54a01b5a3607501e03a'
assert data['source']['verified']=='2026-10-24'
assert len(data['dex'])==966 and len(data['moves'])==103
assert sum(bool(m['evolution']) for m in data['moves'])==97
meteor=next(m for m in data['moves'] if m['id']=='meteor-mash')
assert (meteor['damage'],meteor['radius'],meteor['evolution']['name'],meteor['evolution']['historicalName'])==(24,48,'Meteor Mash +','Magnet Bomb')
assert len(data['orbs']['items'])==6 and data['orbs']['slots']==4 and data['orbs']['stack']==3
assert len(manifest)==112 and sum(x['index'] for x in manifest.values())==108

for locale in ('','es/','it/','zh-hant/'):
    for slug in ('orbs/','gacha-calculator/','arceus-judgment/'):
        route='/'+locale+slug
        assert manifest[route]['index'] and manifest[route]['modified']=='2026-10-24'
        text=(DIST/route.lstrip('/')/'index.html').read_text(encoding='utf-8')
        assert 'canonical' in text and 'hreflang' in text

home=(DIST/'index.html').read_text(encoding='utf-8')
assert '2026-10-24' in home and 'Judgment Plates, Orbs & ×100 gacha' in home
zh_tier=(DIST/'zh-hant/tier-list/index.html').read_text(encoding='utf-8')
assert 'https://pokemonsurvivorwiki.com/zh-hant/tier-list/' in zh_tier and '966' in zh_tier

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
tree=ET.parse(DIST/'sitemap.xml')
urls=tree.findall('s:url',ns)
assert len(urls)==108
lastmods={u.find('s:loc',ns).text:u.find('s:lastmod',ns).text for u in urls}
for locale in ('','es/','it/','zh-hant/'):
    assert lastmods['https://pokemonsurvivorwiki.com/'+locale+'orbs/']=='2026-10-24'

print('PASS V12: source lock, 966/103/97 data, Meteor Mash migration, six Orbs, 108-URL sitemap and four-language system pages valid.')
