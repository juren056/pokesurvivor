"""Release-contract checks for the October 21 V7 source sync."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))
SOURCE = '40c51c178adb7af421a5c6db0f7b43c4492cc861'
assert data['source']['commit'] == SOURCE
assert data['source']['verified'] == '2026-10-21'
assert len(data['dex']) == 966 and len(data['starters']) == 29
assert len(data['moves']) == 103
assert sum(bool(m.get('evolution')) for m in data['moves']) == 97
save_rules = data['rules']['cloudSave']
assert save_rules['automaticUploads'] is False
assert save_rules['manualButton'] is True
assert save_rules['revisionConflictProtection'] is True
assert save_rules['conflictAction'] == 'read-merge-retry'

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = ET.fromstring((HERE / 'dist/sitemap.xml').read_text(encoding='utf-8')).findall('s:url', ns)
assert len(urls) == 88
assert len({u.findtext('s:loc', namespaces=ns) for u in urls}) == 88
assert all(u.find('s:lastmod', ns) is not None for u in urls)

for locale in ('', 'es/', 'it/', 'zh-hant/'):
    root = HERE / 'dist' / locale
    home = (root / 'index.html').read_text(encoding='utf-8')
    save = (root / 'save-recovery/index.html').read_text(encoding='utf-8')
    assert '2026-10-21' in home
    assert 'save-state' in save and 'save-second' in save and 'save-timing' in save
    assert f'hreflang="{("en" if not locale else "zh-Hant" if locale == "zh-hant/" else locale[:-1])}"' in home

en_save = (HERE / 'dist/save-recovery/index.html').read_text(encoding='utf-8')
es_save = (HERE / 'dist/es/save-recovery/index.html').read_text(encoding='utf-8')
it_save = (HERE / 'dist/it/save-recovery/index.html').read_text(encoding='utf-8')
zh_save = (HERE / 'dist/zh-hant/save-recovery/index.html').read_text(encoding='utf-8')
assert 'revision checking' in en_save and 'read, merge and retry' in en_save
assert 'control de versiones' in es_save and '30 minutos después' not in es_save
assert 'controllo delle revisioni' in it_save and '30 minuti dopo' not in it_save
assert 'revision 衝突保護' in zh_save and '30 分鐘排程' not in zh_save

coop = (HERE / 'dist/co-op/index.html').read_text(encoding='utf-8')
updates = (HERE / 'dist/updates/index.html').read_text(encoding='utf-8')
zh_tier = (HERE / 'dist/zh-hant/tier-list/index.html').read_text(encoding='utf-8')
how = (HERE / 'dist/how-to-play/index.html').read_text(encoding='utf-8')
assert '006257f' in coop and 'server-relay path' in coop
assert '40c51c1' in updates and 'revision' in updates
assert '寶可夢倖存者強度排行：966 名角色與配招參考' in zh_tier
assert '29 名免費開局榜' in zh_tier and '/zh-hant/move-evolutions/' in zh_tier
assert 'Game freezes after choosing an upgrade' in how and 'Clearing browser storage is not a verified fix' in how

print('PASS: V7 source revision, cross-device diagnostics, relay status, localized intent, freeze guidance and 88-URL sitemap.')
