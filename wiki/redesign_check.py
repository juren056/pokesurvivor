"""Check redesigned interactions, intermediate widths and frozen SEO fields."""
from pathlib import Path
import hashlib
import json
import os
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
OUT=HERE/'artifacts'
BASE=os.environ.get('WIKI_BASE','http://127.0.0.1:4173')


def main():
    OUT.mkdir(exist_ok=True)
    before=json.loads((HERE/'seo-baseline.json').read_text(encoding='utf-8'))
    manifest=json.loads((HERE/'dist/build-manifest.json').read_text(encoding='utf-8'))
    after={k:{x:v[x] for x in ['title','index','modified']} for k,v in manifest.items()}
    intended_slugs={'','how-to-play','mobile','builds','download','co-op','tier-list','updates','pokedex','moves','move-evolutions','starters','starter-tier-list','arceus-judgment','save-recovery'}
    def intended(route):
        parts=[part for part in route.split('/') if part]
        if parts and parts[0] in ('es','it','zh-hant'): parts=parts[1:]
        return (parts[0] if parts else '') in intended_slugs
    for route,fields in before['routes'].items():
        if not intended(route):
            assert after.get(route)==fields,('Unexpected protected route change',route)
    assert {'/starter-tier-list/','/arceus-judgment/','/upgrades/','/gacha-calculator/'} <= set(after),'Planned routes missing'
    # Media expansion adds image discovery entries; canonical URLs and dates stay protected.
    def sitemap_pages(text):
        ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
        return [(e.findtext('s:loc',namespaces=ns),e.findtext('s:lastmod',namespaces=ns)) for e in ET.fromstring(text)]
    old=dict(sitemap_pages(before['sitemap']));new=dict(sitemap_pages((HERE/'dist/sitemap.xml').read_text(encoding='utf-8')))
    for url,date in old.items():
        route=url.removeprefix('https://pokemonsurvivorwiki.com') or '/'
        if not intended(route): assert new.get(url)==date,('Unexpected sitemap change',url)
    current_data=json.loads((HERE/'data/game.json').read_text(encoding='utf-8'))
    assert current_data['source']['commit']=='018e986f4c12f414dfa84193ee35b2959b1e325c','Unexpected game source'
    report={'seo':'Unchanged routes retain protected titles/index flags/dates; V5 routes use the locked October 20 review source','layouts':[],'tasks':[]}
    data=json.loads((HERE/'data/game.json').read_text(encoding='utf-8'))
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(BASE+'/');page.wait_for_load_state('networkidle')
        for dex in [1,7,4]:
            page.locator(f'[name="opening-partner"][value="{dex}"]').check()
            partner=next(p for p in data['starters'] if p['dex']==dex)
            move=next(m for m in data['moves'] if m['id']==partner['start'])
            assert page.locator('[data-lab-name]').inner_text()==partner['name']
            assert page.locator('[data-lab-hp]').inner_text()==str(partner['hp'])
            assert page.locator('[data-lab-evolution]').inner_text()==move['evolution']['name']
            assert page.locator('[data-lab-link]').get_attribute('href').endswith('#'+move['id'])
        report['tasks'].append('Three partner previews show source stats and exact evolution destinations')
        page.locator('#home-search').fill('Ember');page.locator('.hero-search button').click()
        page.wait_for_selector('#search-results a')
        assert page.locator('#search-query').input_value()=='Ember'
        report['tasks'].append('Homepage native search reaches results')
        page.goto(BASE+'/pokedex/?type=fire');page.wait_for_load_state('networkidle')
        assert page.locator('[data-type]').input_value()=='fire'
        visible=page.locator('tbody tr:visible')
        assert visible.count()==sum('fire' in p['types'] for p in data['dex'])
        page.locator('[data-sort="3"]').click()
        values=[int(t) for t in visible.locator('td:nth-child(4)').all_text_contents()]
        assert values==sorted(values)
        page.locator('[data-sort="3"]').click()
        values=[int(t) for t in visible.locator('td:nth-child(4)').all_text_contents()]
        assert values==sorted(values,reverse=True)
        page.get_by_role('button',name='Reset',exact=True).click()
        page.wait_for_function("document.querySelector('[data-count]').textContent === '966 of 966 entries'")
        report['tasks'].append('Type deep link, numeric ascending/descending sorting and filter reset')
        for width in [768,1024]:
            page.set_viewport_size({'width':width,'height':900})
            for route in ['/','/pokedex/','/move-evolutions/','/how-to-play/']:
                page.goto(BASE+route);page.wait_for_load_state('networkidle')
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(width,route)
                report['layouts'].append({'width':width,'route':route,'overflow':False})
        for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile')]:
            page.set_viewport_size({'width':width,'height':height})
            for route,name in [('/','home'),('/pokedex/','dex'),('/move-evolutions/','evolutions')]:
                page.goto(BASE+route);page.wait_for_load_state('networkidle')
                page.evaluate('document.fonts.ready')
                page.evaluate('Promise.all(document.getAnimations().map(a=>a.finished.catch(()=>{})))')
                page.screenshot(path=str(OUT/f'redesign-{label}-{name}.png'),full_page=False)
                if width==390:
                    assert page.locator('.mobile-dock').is_visible()
                    assert page.locator('.mobile-dock a').count()==4
        report['tasks'].append('Mobile dock exposes four native destinations without replacing page navigation')
        context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        nojs=context.new_page();nojs.goto(BASE+'/')
        assert not nojs.locator('.starter-choices').is_visible()
        assert nojs.locator('[data-lab-name]').inner_text()=='Charmander'
        assert nojs.locator('.hero-search').is_visible()
        report['tasks'].append('No-JS homepage retains real search and a complete default evolution example')
        assert not errors,errors
        browser.close()
    (OUT/'redesign-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: protected SEO/data baseline; {len(report["layouts"])} intermediate-width checks; {len(report["tasks"])} redesigned behavior groups; no JS errors.')


if __name__=='__main__':main()
