"""Record disposable local guest sessions; never changes game code or user saves.

Requires the original game served at localhost:4180. Screenshots are raw browser
captures. Desktop bot uses read-only state observations and normal keyboard inputs.
"""
from pathlib import Path
import json
import time
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
RAW = HERE / 'artifacts/media-raw'
RAW.mkdir(parents=True, exist_ok=True)
SHOTS = json.loads((RAW/'shots.json').read_text(encoding='utf-8')) if (RAW/'shots.json').exists() else []


def shot(page, ident, caption, pages):
    page.screenshot(path=str(RAW / (ident + '.png')))
    SHOTS[:] = [s for s in SHOTS if s['id'] != ident]
    SHOTS.append(dict(id=ident, caption=caption, pages=pages,
                      width=page.viewport_size['width'], height=page.viewport_size['height']))
    (RAW / 'shots.json').write_text(json.dumps(SHOTS, indent=2), encoding='utf-8')
    print('Captured', ident, flush=True)


def login(page, dev=False):
    page.goto('http://127.0.0.1:4180/' + ('dev.html' if dev else ''))
    page.wait_for_timeout(1000)
    prompt = page.get_by_text('Press to start', exact=True)
    if prompt.is_visible(): prompt.click()
    page.locator('#btn-guest').wait_for(state='visible')


def partner(page, name='Charmander', capture=False):
    page.locator('#btn-guest').click()
    page.wait_for_timeout(300)
    if capture: shot(page, 'personality-quiz', 'The personality quiz recommends a partner; it does not lock your choice.', ['how-to-play'])
    for _ in range(8):
        page.locator('#test-a button').first.click()
        page.wait_for_timeout(150)
    if capture: shot(page, 'quiz-result', 'Accept the recommended partner or choose another.', ['how-to-play'])
    page.locator('#res-other').click()
    if capture:
        shot(page, 'starter-roster', 'The starter selection screen in a fresh guest session.', ['starters', 'tier-list'])
        for mon in ['Bulbasaur', 'Squirtle', 'Charmander']:
            page.locator('#starter-grid .cell').filter(has_text=mon).click()
            shot(page, 'starter-' + mon.lower(), f'{mon} selected: read the starting move before confirming.', ['builds', 'starters'])
    page.locator('#starter-grid .cell').filter(has_text=name).click()
    page.locator('#starter-ok').click()
    page.wait_for_timeout(2500)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width':1280,'height':720},locale='en-US',
                                  record_video_dir=str(RAW/'onboarding'), record_video_size={'width':1280,'height':720})
        page = ctx.new_page(); page.set_default_timeout(12000)
        login(page)
        shot(page, 'guest-login', 'Choose Play as guest for a disposable local trial; sign in separately for cloud progress.', ['how-to-play', 'download'])
        partner(page, capture=True)
        shot(page, 'partner-menu', 'A fresh Charmander guest profile before the first run.', ['', 'how-to-play'])
        # Screens reached only through the actual game controls.
        for dest, ident, caption, pages in [
            ('dex','collection','The in-game collection shows the selected partner and collection progress.',['pokedex']),
            ('upgrades','permanent-upgrades','Permanent upgrades are a separate menu from the cards chosen during a run.',['builds','move-evolutions']),
            ('gacha','regional-gacha','The regional gacha menu is separate from rift encounters.',['legendaries','pokedex']),
            ('goals','missions','The missions screen tracks goals and achievements.',['how-to-play']),
        ]:
            page.locator(f'#scr-menu [data-go={dest}]').click();page.wait_for_timeout(700)
            shot(page,ident,caption,pages)
            back=page.locator('[data-back]:visible').first
            if back.count(): back.click()
            else: raise RuntimeError('No visible back control: '+dest)
        page.locator('#scr-menu [data-go=settings]').click()
        for tab,ident,caption,pages in [
            ('ctl','keyboard-controls','The game settings list its desktop controls.',['how-to-play']),
            ('gfx','graphics-settings','Graphics settings let you adjust presentation on this device.',['mobile']),
            ('acc','guest-account','Guest account settings: a guest trial is not a cloud account.',['co-op','mobile']),
        ]:
            page.locator(f'#set-tabs [data-t={tab}]').click();page.wait_for_timeout(400)
            shot(page,ident,caption,pages)
        page.locator('#set-close').click()
        ctx.storage_state(path=str(RAW/'guest-state.json'))
        video=page.video;ctx.close();video.save_as(str(RAW/'onboarding.webm'))
        # A new recording context reuses only this disposable guest trial.
        run=browser.new_context(viewport={'width':1280,'height':720},locale='en-US',storage_state=str(RAW/'guest-state.json'),
                                record_video_dir=str(RAW/'run'),record_video_size={'width':1280,'height':720})
        page=run.new_page();login(page, dev=True)
        # Guest mode is intentionally not persistent: begin another untouched run.
        partner(page)
        page.locator('#scr-menu [data-go=play]').click();page.wait_for_timeout(4000)
        shot(page,'first-run','The opening of a normal Charmander run: HP, timer and active move are visible.',['','how-to-play'])
        start=time.monotonic(); held=set(); captured_levels=set(); evolved=False
        while time.monotonic()-start < 360:
            state=page.evaluate('''() => {const p=G.Game.player;return {state:G.Game.state,time:G.Game.st.time,
                x:p?.x,y:p?.y,hp:p?.hp,level:p?.level,moves:p?.moves,
                pickups:G.Pickups.all().filter(o=>o.kind==='xp'||o.kind==='xpBig'||o.kind==='heal').map(o=>({x:o.x,y:o.y})),
                enemies:G.EnemyMgr?.all?.().slice(0,100).map(o=>({x:o.x,y:o.y}))||[]};}''')
            if state['state']=='over':
                shot(page,'run-summary','The end-of-run screen reports this trial, not a benchmark ranking.',['builds']);break
            if state['state']=='levelup':
                for key in held:page.keyboard.up(key)
                held=set();level=state['level']
                if level not in captured_levels:
                    shot(page,f'level-{level}-cards',f'Actual level {level} upgrade choices in this guest run.',['how-to-play','builds'])
                    captured_levels.add(level)
                cards=page.locator('#cards .card'); texts=cards.all_text_contents();best=0;score=-999
                for i,t in enumerate(texts):
                    s=100 if 'Fire Blast' in t else 80 if 'Ember' in t else 60 if 'Power' in t else 20 if 'Recover' in t else 0
                    if s>score:score=s;best=i
                if any('Fire Blast' in t for t in texts):
                    shot(page,'golden-evolution-card','A golden Fire Blast evolution card actually offered during this run.',['move-evolutions'])
                    evolved=True
                cards.nth(best).click();page.wait_for_timeout(400)
                if evolved:
                    shot(page,'fire-blast-evolved','Fire Blast selected in this recorded guest run.',['move-evolutions']);break
                continue
            if state['state']!='playing':page.wait_for_timeout(200);continue
            # Seek nearby experience while repelling nearby enemies. No stat/save edits.
            x,y=state['x'],state['y']; pickups=state['pickups']; enemies=state['enemies']
            dx,dy=0,0
            if pickups:
                target=min(pickups,key=lambda q:(q['x']-x)**2+(q['y']-y)**2)
                dx,dy=target['x']-x,target['y']-y
                length=max(1,(dx*dx+dy*dy)**.5);dx/=length;dy/=length
            else:
                import math
                dx,dy=math.cos(state['time']*.2),math.sin(state['time']*.2)
            for enemy in enemies:
                ex,ey=x-enemy['x'],y-enemy['y'];dist=max(1,(ex*ex+ey*ey)**.5)
                if dist<100:dx+=ex/dist*(100-dist)/45;dy+=ey/dist*(100-dist)/45
            keys=set()
            if dx>.2:keys.add('d')
            if dx<-.2:keys.add('a')
            if dy>.2:keys.add('s')
            if dy<-.2:keys.add('w')
            for key in held-keys:page.keyboard.up(key)
            for key in keys-held:page.keyboard.down(key)
            held=keys
            elapsed=time.monotonic()-start
            for threshold,ident,caption in [(15,'ember-combat','Ember attacks automatically while the partner moves.'),(35,'experience-route','Move toward experience without closing your escape route.'),(65,'run-progress','A later checkpoint in the same unmodified guest trial.')]:
                if elapsed>=threshold and ident not in captured_levels:
                    shot(page,ident,caption,['','how-to-play','builds']);captured_levels.add(ident)
            page.wait_for_timeout(200)
        for key in held:page.keyboard.up(key)
        if page.evaluate("G.Game.state")=='playing':
            page.keyboard.press('Escape');page.wait_for_timeout(300)
            shot(page,'pause-menu','Pause a solo run before changing settings.',['how-to-play','mobile'])
        (RAW/'trial-result.json').write_text(json.dumps({'evolved':evolved,'seconds':round(time.monotonic()-start),'lastState':state},indent=2),encoding='utf-8')
        video=page.video;run.close();video.save_as(str(RAW/'gameplay.webm'))
        browser.close()


if __name__=='__main__':main()
