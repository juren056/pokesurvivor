"""Focused browser checks for the V6 Move Master checklist."""
import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE=os.environ.get('WIKI_BASE','http://127.0.0.1:4173')
OUT=Path(__file__).resolve().parent/'artifacts'
with sync_playwright() as p:
    browser=p.chromium.launch()
    ctx=browser.new_context(viewport={'width':390,'height':844})
    page=ctx.new_page();page.goto(BASE+'/move-evolutions/')
    page.wait_for_function("document.querySelectorAll('#master-list label').length===97")
    assert '0 of 97' in page.locator('#master-count').inner_text()
    page.locator('#master-list input').first.check()
    assert '1 of 97' in page.locator('#master-count').inner_text()
    page.reload();page.wait_for_function("document.querySelector('#master-count').textContent.includes('1 of 97')")
    page.goto(BASE+'/es/move-evolutions/');page.wait_for_function("document.querySelector('#master-count').textContent.includes('1 de 97')")
    page.locator('[data-master-import]').set_input_files(files=[{'name':'bad.json','mimeType':'application/json','buffer':b'{bad'}])
    assert 'rechazada' in page.locator('#master-status').inner_text()
    payload=json.dumps({'schemaVersion':1,'datasetVersion':'old','completedMoveIds':['tackle','tackle','unknown-v9']}).encode()
    page.locator('[data-master-import]').set_input_files(files=[{'name':'moves.json','mimeType':'application/json','buffer':payload}])
    page.wait_for_function("document.querySelector('#master-count').textContent.includes('1 de 97')")
    assert '1 ID' in page.locator('#master-status').inner_text()
    page.once('dialog',lambda dialog:dialog.dismiss())
    page.locator('[data-master-reset]').click();assert '1 de 97' in page.locator('#master-count').inner_text()
    page.once('dialog',lambda dialog:dialog.accept())
    page.locator('[data-master-reset]').click();assert '0 de 97' in page.locator('#master-count').inner_text()
    ctx.close()
    blocked=browser.new_context();blocked.add_init_script("Storage.prototype.setItem=function(){throw new Error('blocked')}")
    temp=blocked.new_page();temp.goto(BASE+'/move-evolutions/');temp.wait_for_function("document.querySelectorAll('#master-list label').length===97")
    assert 'temporary memory only' in temp.locator('#master-count').inner_text()
    browser.close()
print('PASS: Move Master reload, locale sharing, invalid/duplicate/unknown import, reset cancel/accept and blocked storage.')
