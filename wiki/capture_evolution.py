"""Attempt normal evolution with keyboard-only play; record failure honestly."""
import json,time
from playwright.sync_api import sync_playwright
from capture_media import RAW,login,partner,shot

with sync_playwright() as p:
 b=p.chromium.launch();ctx=b.new_context(viewport={'width':1280,'height':720},locale='en-US',
     record_video_dir=str(RAW/'evolution-trial'),record_video_size={'width':1280,'height':720})
 page=ctx.new_page();page.set_default_timeout(10000);login(page,dev=True);partner(page,'Charmander')
 page.locator('#scr-menu [data-go=upgrades]').click()
 for idx in [5,2,0,0,1,3,6]:
  button=page.locator('#upg-list .upg-item').nth(idx).locator('[data-buy]')
  if button.is_enabled():button.click();page.wait_for_timeout(100)
 page.locator('[data-back]:visible').first.click()
 page.locator('#scr-menu [data-go=play]').click();start=time.monotonic();held=set();seen=set();success=False;timeline=[]
 while time.monotonic()-start<600:
  state=page.evaluate('''() => {const p=G.Game.player;if(!p)return {state:G.Game.state};
    const es=G.EnemyMgr.all().filter(e=>!e.dead);const drops=G.Pickups.all().filter(q=>['xp','xpBig','heal'].includes(q.kind));
    const near=(x,y)=>Math.min(250,...es.map(e=>Math.hypot(e.x-x,e.y-y)));
    const safe=drops.filter(q=>near(q.x,q.y)>65).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y));
    const target=safe[0];let best=-Infinity,keys=[];
    for(const [dx,dy,k] of [[0,0,[]],[1,0,['d']],[-1,0,['a']],[0,1,['s']],[0,-1,['w']],[.707,.707,['s','d']],[-.707,.707,['s','a']],[.707,-.707,['w','d']],[-.707,-.707,['w','a']]]){
     const x=p.x+dx*55,y=p.y+dy*55;if(!G.World.isFree(x,y,p.r)||!G.World.isFree(p.x+dx*25,p.y+dy*25,p.r))continue;
     const n=near(x,y);let score=Math.min(n,135)*1.5;
     if(n<100)score-=(100-n)*15;
     if(target)score-=Math.hypot(target.x-x,target.y-y)*.30;
     else score+=(dx*Math.cos(G.Game.st.time*.1)+dy*Math.sin(G.Game.st.time*.1))*5;
     if(score>best){best=score;keys=k;}
    }
    return {state:G.Game.state,time:G.Game.st.time,hp:p.hp,maxHp:p.maxHp,level:p.level,keys,moves:p.moves.map(m=>({id:m.id,lvl:m.lvl,evolved:m.evolved}))};}''')
  if state['state']=='over':break
  if state['state']=='levelup':
   for k in held:page.keyboard.up(k)
   held=set();texts=page.locator('#cards .card').all_text_contents()
   print('Level',state['level'],texts,flush=True);timeline.append({'at':round(time.monotonic()-start,2),'level':state['level'],'cards':texts})
   gold=page.locator('#cards .card.evo')
   if gold.count():
    shot(page,'golden-evolution-card','The golden evolution card offered after meeting the in-run requirements.',['move-evolutions'])
    gold.first.click();page.wait_for_timeout(800);shot(page,'evolved-active-move','The evolved attack after choosing the golden card in a normal guest run.',['move-evolutions']);success=True
    page.wait_for_timeout(8000);break
   score=[]
   for t in texts:
    n=90 if 'Ember' in t else 80 if 'Power' in t else 10
    if state['hp']/state['maxHp']<.6 and any(w in t for w in ['Vigor','Sitrus']):n=100
    elif any(w in t for w in ['Synthesis','Magnet','Reflexes','Sprint']):n=35
    score.append(n)
   if state['level'] not in seen:
    shot(page,'evolution-trial-level-'+str(state['level']),f'Actual level {state["level"]} offers while working toward an evolution.',['move-evolutions']);seen.add(state['level'])
   page.locator('#cards .card').nth(max(range(len(score)),key=lambda i:score[i])).click();page.wait_for_timeout(250);continue
  if state['state']!='playing':page.wait_for_timeout(200);continue
  keys=set(state['keys'])
  for k in held-keys:page.keyboard.up(k)
  for k in keys-held:page.keyboard.down(k)
  held=keys;page.wait_for_timeout(160)
 for k in held:page.keyboard.up(k)
 (RAW/'evolution-result.json').write_text(json.dumps({'success':success,'seconds':round(time.monotonic()-start),'lastState':state,'timeline':timeline},indent=2),encoding='utf-8')
 video=page.video;ctx.close();video.save_as(str(RAW/'evolution-trial.webm'));b.close();print('Evolution success:',success,flush=True)
