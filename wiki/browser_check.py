"""Behavior and responsive acceptance checks against the local Wiki server."""
from pathlib import Path
import os
import json
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
OUT=HERE/'artifacts'
OUT.mkdir(exist_ok=True)
BASE=os.environ.get('WIKI_BASE','http://127.0.0.1:4173')
manifest=json.loads((HERE/'dist/build-manifest.json').read_text(encoding='utf-8'))
report={'routes':[],'tasks':[],'errors':[]}


def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context(viewport={'width':1440,'height':1000})
        page=context.new_page()
        page.on('pageerror',lambda error:report['errors'].append(str(error)))
        for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile'),(375,500,'short-mobile')]:
            page.set_viewport_size({'width':width,'height':height})
            for route in manifest:
                response=page.goto(BASE+route)
                page.wait_for_load_state('networkidle')
                assert response.status==200,(route,response.status)
                assert page.locator('h1').count()==1,route
                overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                assert not overflow,(label,route,'root overflow')
                assert page.locator('#main').is_visible(),route
                report['routes'].append({'route':route,'viewport':label,'status':response.status,'rootOverflow':overflow})
                if route in ('','tier-list/'):pass
                if route in ('/','/move-evolutions/','/pokedex/') and label!='short-mobile':
                    page.screenshot(path=str(OUT/f'{label}-{route.strip("/") or "home"}.png'),full_page=route=='/')
        page.set_viewport_size({'width':1440,'height':1000})
        home_selectors=['.opening','.hero','.hero-copy','.hero-field','.starter-lab','.topic-strip','.journey','.route','.field-film','.reference-home','.notebook','.trust-strip','.identity','[data-media-id]','[data-video-id]','.data-section']
        home_signatures={}
        for locale,path in [('en','/'),('es','/es/'),('it','/it/'),('zh-hant','/zh-hant/')]:
            page.goto(BASE+path);page.wait_for_load_state('networkidle')
            home_signatures[locale]={selector:page.locator(selector).count() for selector in home_selectors}
        assert all(signature==home_signatures['en'] for signature in home_signatures.values()),home_signatures
        report['tasks'].append('All locale homepages match the English component, media and interaction skeleton')
        page.goto(BASE+'/pokedex/')
        page.locator('[data-filter]').fill('Pikachu')
        assert page.locator('tbody tr:visible').count()==1
        page.locator('[data-type]').select_option('fire')
        assert page.locator('[data-empty]').is_visible()
        page.get_by_role('button',name='Reset',exact=True).click()
        page.wait_for_function("document.querySelector('[data-count]').textContent === '966 of 966 entries'")
        page.locator('[data-type]').select_option('poison')
        assert 'Bulbasaur' in page.locator('tbody tr:visible').all_text_contents()[0]
        report['tasks'].append('Pokédex search, combined empty state, dual-type match and reset')
        page.goto(BASE+'/move-evolutions/')
        page.locator('#evo-move').select_option('ember')
        page.locator('#evo-level').fill('5')
        page.locator('#evo-stat').check()
        page.wait_for_function("document.querySelector('#evo-result').textContent.includes('Eligible for Fire Blast')")
        page.locator('#evo-level').fill('0')
        assert 'Enter a whole level' in page.locator('#evo-result').inner_text()
        page.locator('#evo-move').select_option('swords-dance')
        assert 'no move evolution' in page.locator('#evo-result').inner_text()
        report['tasks'].append('Evolution eligibility, invalid level and non-evolving buff')
        page.goto(BASE+'/types/')
        page.locator('#attack-type').select_option('water')
        page.locator('#defend-type').select_option('fire')
        page.locator('#defend-second').select_option('rock')
        page.wait_for_function("document.querySelector('#type-result').textContent.includes('2.4×')")
        page.locator('#attack-type').select_option('normal')
        page.locator('#defend-type').select_option('ghost')
        page.locator('#defend-second').select_option('')
        assert '0.3×' in page.locator('#type-result').inner_text()
        report['tasks'].append('Dual-type cap and softened immunity')
        page.goto(BASE+'/builds/?p=4&m=water-gun')
        page.wait_for_function("document.querySelector('#build-result').textContent.includes('Charmander starts with')")
        assert 'Water Gun' not in page.locator('#build-result').inner_text()
        page.locator('#build-secondary').select_option('tackle')
        assert 'Tackle' in page.locator('#build-result').inner_text()
        assert 'p=4' in page.locator('#build-share').get_attribute('data-url')
        report['tasks'].append('Build planner rejects incompatible shared move and creates a private-data-free share URL')
        page.goto(BASE+'/gacha-calculator/')
        page.locator('#gacha-pulls').fill('10');page.locator('#gacha-pity').fill('65')
        assert 'reaches the 70-pull hard pity' in page.locator('#gacha-result').inner_text()
        page.locator('#gacha-pulls').fill('0')
        assert 'Enter 1–1000 pulls' in page.locator('#gacha-result').inner_text()
        report['tasks'].append('Gacha base probability, pity boundary and invalid input')
        page.goto(BASE+'/save-recovery/')
        page.locator('#save-login').select_option('guest')
        page.locator('#save-copy').select_option('no')
        page.locator('#save-symptom').select_option('paused')
        page.locator('[data-diagnostic-run]').click()
        assert 'Recovery is uncertain for an unlinked guest' in page.locator('#save-result').inner_text()
        safe_report=page.locator('#save-report').input_value()
        assert 'Paused to protect your progress' in safe_report
        assert 'password' not in safe_report.lower() and 'token' not in safe_report.lower() and '@' not in safe_report
        assert not page.locator('[data-report-copy]').is_disabled()
        report['tasks'].append('Save recovery unknown branch and privacy-safe report')
        page.goto(BASE+'/search/?q=Pikachu')
        page.wait_for_selector('#search-results a')
        page.locator('#search-results a').first.click()
        assert page.url.endswith('/pokedex/#p25')
        page.go_back();page.wait_for_selector('#search-results a')
        assert page.locator('#search-query').input_value()=='Pikachu'
        page.locator('#search-query').fill('<script>alert(1)</script>')
        page.get_by_role('button',name='Search',exact=True).click()
        page.wait_for_function("document.querySelector('#search-status').textContent.startsWith('No results')")
        report['tasks'].append('Search, anchor destination, browser Back and safe query rendering')
        page.set_viewport_size({'width':375,'height':500})
        page.goto(BASE+'/')
        page.locator('.language-menu summary').click()
        assert page.locator('.language-menu nav').is_visible()
        assert page.locator('.language-menu nav a').count()==4
        page.keyboard.press('Escape')
        assert not page.locator('.language-menu').get_attribute('open')
        page.get_by_role('button',name='Menu',exact=True).click()
        assert page.locator('#site-nav').is_visible()
        assert page.locator('#site-nav a').last.is_visible()
        page.keyboard.press('Escape')
        assert page.get_by_role('button',name='Menu',exact=True).get_attribute('aria-expanded')=='false'
        report['tasks'].append('Compact language picker, short mobile menu and Escape focus return')
        locale_expectations={
            'es':{'lang':'es','count':'1 de 966 registros','eligible':'Puedes evolucionar','damage':'de daño','results':'resultados'},
            'it':{'lang':'it','count':'1 di 966 voci','eligible':'Puoi evolvere','damage':'danno','results':'risultati'},
            'zh-hant':{'lang':'zh-Hant','count':'顯示 1／966 筆','eligible':'可進化為','damage':'傷害','results':'找到 1 筆結果'},
        }
        page.set_viewport_size({'width':390,'height':844})
        for locale,expected in locale_expectations.items():
            page.goto(f'{BASE}/{locale}/pokedex/')
            assert page.locator('html').get_attribute('lang')==expected['lang']
            page.locator('[data-filter]').fill('Pikachu')
            assert page.locator('[data-count]').inner_text()==expected['count']
            assert page.locator('tbody tr:visible').count()==1
            page.goto(f'{BASE}/{locale}/move-evolutions/')
            page.locator('#evo-move').select_option('ember');page.locator('#evo-level').fill('5');page.locator('#evo-stat').check()
            assert expected['eligible'] in page.locator('#evo-result').inner_text()
            page.goto(f'{BASE}/{locale}/types/')
            page.locator('#attack-type').select_option('water');page.locator('#defend-type').select_option('fire');page.locator('#defend-second').select_option('rock')
            assert expected['damage'] in page.locator('#type-result').inner_text() and '2.4×' in page.locator('#type-result').inner_text()
            page.goto(f'{BASE}/{locale}/search/?q=Pikachu');page.wait_for_selector('#search-results a')
            assert expected['results'] in page.locator('#search-status').inner_text()
            assert page.locator('#search-results a').first.get_attribute('href').startswith(f'/{locale}/')
            page.goto(f'{BASE}/{locale}/');page.screenshot(path=str(OUT/f'mobile-home-{locale}.png'),full_page=True)
        report['tasks'].append('Spanish, Italian and Traditional Chinese filter, evolution, type calculator and localized search')
        response=page.goto(BASE+'/does-not-exist/')
        assert response.status==404
        report['tasks'].append('True HTTP 404')
        offline=context.new_page()
        offline.route('**/assets/game.json',lambda route:route.abort())
        offline.goto(BASE+'/move-evolutions/')
        offline.wait_for_function("document.querySelector('#evo-result').textContent.includes('could not load')")
        assert offline.locator('tbody tr').count()==59
        report['tasks'].append('Tool network failure keeps static evolution table')
        nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        nojs_page=nojs.new_page();nojs_page.goto(BASE+'/moves/')
        assert nojs_page.locator('#site-nav').is_visible()
        assert nojs_page.locator('tbody tr').count()==64
        report['tasks'].append('No-JavaScript navigation and complete move table')
        assert not report['errors'],report['errors']
        browser.close()
    (OUT/'browser-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {len(report["routes"])} route/viewport checks; {len(report["tasks"])} behavior checks; no JavaScript errors.')


if __name__=='__main__':main()
