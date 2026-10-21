"""Release-contract checks for the October 21 V6 source sync."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'data/game.json').read_text(encoding='utf-8'))
SOURCE='3c9641c9e782cf74afbde490f39cd60adf59e32b'
assert data['source']['commit']==SOURCE and data['source']['verified']=='2026-10-21'
assert len(data['dex'])==966 and len(data['starters'])==29 and len(data['moves'])==103
assert len({m['id'] for m in data['moves']})==103
assert sum(bool(m.get('evolution')) for m in data['moves'])==97
assert data['rules']['cloudSave']=={'automaticUploads':False,'manualButton':True,'beforeUpdate':True,'beforeLogout':True,'minUploadGapMs':65000}

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=ET.fromstring((HERE/'dist/sitemap.xml').read_text(encoding='utf-8')).findall('s:url',ns)
assert len(urls)==88 and len({u.findtext('s:loc',namespaces=ns) for u in urls})==88
for locale in ('','es/','it/','zh-hant/'):
    root=HERE/'dist'/locale
    home=(root/'index.html').read_text(encoding='utf-8')
    evo=(root/'move-evolutions/index.html').read_text(encoding='utf-8')
    assert '2026-10-21' in home
    assert 'data-move-master' in evo and '97' in evo
    assert f'hreflang="{("en" if not locale else "zh-Hant" if locale=="zh-hant/" else locale[:-1])}"' in home

save=(HERE/'dist/save-recovery/index.html').read_text(encoding='utf-8')
mobile=(HERE/'dist/mobile/index.html').read_text(encoding='utf-8')
coop=(HERE/'dist/co-op/index.html').read_text(encoding='utf-8')
updates=(HERE/'dist/updates/index.html').read_text(encoding='utf-8')
assert 'cloud upload is manual' in save and '65 seconds' in save
assert 'Manual Aim is not available on mobile' in mobile and '#259' in mobile and '#258' in mobile
assert 'three-minute room invitation' in coop and '3c9641c' in coop and '#260' in coop and '#253' in coop
assert 'Manual Save &amp; TURN Pilot' in updates and '2026-10-21' in updates

print('PASS: V6 source, manual Save, TURN pilot, mobile guidance, Move Master, four locales and 88 unique sitemap URLs.')
