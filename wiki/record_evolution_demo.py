"""Clearly labeled controlled-engine demonstration, never an unassisted run."""
from pathlib import Path
import json,time,subprocess
from playwright.sync_api import sync_playwright
from capture_media import RAW,login,partner,shot

HERE=Path(__file__).resolve().parent;OUT=HERE/'public/media'
FFMPEG=Path.home()/'AppData/Local/ms-playwright/ffmpeg-1011/ffmpeg-win64.exe'
with sync_playwright() as p:
 b=p.chromium.launch();ctx=b.new_context(viewport={'width':1280,'height':720},locale='en-US',record_video_dir=str(RAW/'evolution-demo'),record_video_size={'width':1280,'height':720})
 page=ctx.new_page();clock=time.monotonic();login(page,dev=True);partner(page);page.locator('#scr-menu [data-go=play]').click();page.wait_for_timeout(800)
 page.evaluate('''() => {const label=document.createElement('div');label.textContent='CONTROLLED MECHANICS DEMO · prerequisites preconfigured · developer level-up trigger';Object.assign(label.style,{position:'fixed',top:'80px',left:'20px',right:'20px',padding:'14px',background:'#f2c66d',color:'#10261f',font:'bold 18px Arial',textAlign:'center',zIndex:'99999',borderRadius:'8px',pointerEvents:'none'});document.body.append(label);}''')
 start=time.monotonic()-clock;page.wait_for_timeout(4000)
 # Actual source-engine methods; the visible editorial label remains for the whole clip.
 page.evaluate('''() => {const p=G.Game.player,m=p.moves.find(m=>m.id==='ember');while(m.lvl<5)G.Moves.levelUp(m);const stat=G.LevelUp.STATS.find(s=>s.id==='atk');stat.apply(p);p.statsTaken.atk=1;G.Game.debugLevelUp();}''')
 page.locator('#cards .card.evo').wait_for(state='visible')
 assert 'Fire Blast' in page.locator('#cards .card.evo').first.inner_text()
 shot(page,'controlled-golden-card','Controlled mechanics demo: Ember level 5 and Power were preconfigured; the developer level-up trigger produces the golden Fire Blast offer.',['move-evolutions'])
 page.wait_for_timeout(6500);page.locator('#cards .card.evo').first.click();page.wait_for_timeout(1000)
 observed=page.evaluate('G.Game.player.moves.map(m=>({id:m.id,name:m.name,lvl:m.lvl,evolved:m.evolved}))')
 assert any(m.get('evolved') for m in observed),observed
 shot(page,'controlled-evolved-move','Controlled mechanics demo after selecting Fire Blast. This does not document earning the prerequisites through normal play.',['move-evolutions'])
 page.keyboard.down('d');page.wait_for_timeout(5000);page.keyboard.up('d');page.wait_for_timeout(3000)
 duration=round(time.monotonic()-clock-start,2);v=page.video;ctx.close();raw=RAW/'controlled-evolution.webm';v.save_as(str(raw));b.close()
subprocess.run([str(FFMPEG),'-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(raw),'-t',str(duration),'-c:v','libvpx','-b:v','1200k','-crf','24','-deadline','realtime','-cpu-used','5',str(OUT/'evolution-route.webm')],check=True)
captions=[{'start':0,'end':4,'text':'Controlled demo: prerequisites will be preconfigured. This is not an unassisted run.'},{'start':4,'end':11,'text':'Ember level five + Power in this run. The developer level-up trigger opens the genuine golden Fire Blast offer.'},{'start':11,'end':duration,'text':'Select the golden card to evolve the move. This demonstrates the engine response, not earning the prerequisites.'}]
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(OUT/'evolution-route.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(stamp(c['start'])+' --> '+stamp(c['end'])+'\n'+c['text'] for c in captions)+'\n',encoding='utf-8')
records=json.loads((HERE/'media-videos.json').read_text(encoding='utf-8'))
records=[r for r in records if r['id']!='evolution-route']
records.append(dict(id='evolution-route',title='Golden evolution card: controlled demonstration',description='Prerequisites are preconfigured in a disposable local session: Ember level five and Power, followed by the developer level-up trigger. The game then offers Fire Blast and evolves the move when selected. This is not an unassisted run.',poster='controlled-golden-card',pages=['move-evolutions'],width=1280,height=720,duration=duration,captions=captions,created='2026-10-15',source='Local unbundled dev.html engine, source snapshot b297089',scope='Controlled test fixture. G.Moves.levelUp applied until Ember level 5; Power applied via the real stat method; statsTaken.atk set to 1; G.Game.debugLevelUp triggers the offer. Golden card selected through the real UI. Visible editorial label is present throughout.',rights='Noncommercial guide capture; JPTER78 / PokéSurvivor; SpriteCollab CC BY-NC 4.0; artist credits linked in /about/#media-credits.',observed=observed))
(HERE/'media-videos.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');print('Recorded controlled evolution, duration',duration)
