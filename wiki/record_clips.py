"""Create distinct silent UI/game recordings and timed English caption tracks."""
from pathlib import Path
import json,time,subprocess
from playwright.sync_api import sync_playwright
from capture_media import RAW,login,partner

HERE=Path(__file__).resolve().parent
OUT=HERE/'public/media'
FFMPEG=Path.home()/'AppData/Local/ms-playwright/ffmpeg-1011/ffmpeg-win64.exe'
RECORDS=[]


def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'


def save(raw,ident,title,description,poster,pages,start,duration,width,height,captions,scope):
    subprocess.run([str(FFMPEG),'-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(raw),'-t',str(duration),'-c:v','libvpx','-b:v','1200k','-crf','24','-deadline','realtime','-cpu-used','5',str(OUT/(ident+'.webm'))],check=True)
    cues=[]
    for i,(at,text) in enumerate(captions):
        end=captions[i+1][0] if i+1<len(captions) else duration
        cues.append({'start':at,'end':end,'text':text})
    (OUT/(ident+'.vtt')).write_text('WEBVTT\n\n'+'\n\n'.join(stamp(c['start'])+' --> '+stamp(c['end'])+'\n'+c['text'] for c in cues)+'\n',encoding='utf-8')
    RECORDS.append(dict(id=ident,title=title,description=description,poster=poster,pages=pages,width=width,height=height,duration=duration,captions=cues,created='2026-10-15',source='Local game snapshot b297089, fresh disposable guest session',scope=scope,rights='Noncommercial game guide capture; JPTER78 / PokéSurvivor; embedded SpriteCollab sprites CC BY-NC 4.0; individual artists linked in /about/#media-credits. Pokémon belongs to its owners.'))
    (HERE/'media-videos.json').write_text(json.dumps(RECORDS,indent=2)+'\n',encoding='utf-8')
    print('Prepared video',ident,flush=True)


with sync_playwright() as p:
 b=p.chromium.launch()
 # Deliberately paced onboarding; no existing user account is touched.
 ctx=b.new_context(viewport={'width':1280,'height':720},locale='en-US',record_video_dir=str(RAW/'first-session'),record_video_size={'width':1280,'height':720})
 page=ctx.new_page();clock=time.monotonic();login(page);start=time.monotonic()-clock;captions=[]
 def cue(text):captions.append((round(time.monotonic()-clock-start,2),text))
 cue('Choose Play as guest for a fresh local trial.');page.wait_for_timeout(3500);page.locator('#btn-guest').click();page.wait_for_timeout(500)
 cue('Answer the eight personality questions. The result is a recommendation.')
 for _ in range(8):page.locator('#test-a button').first.click();page.wait_for_timeout(1100)
 cue('Accept the suggested partner or choose another.');page.wait_for_timeout(3500);page.locator('#res-other').click();page.wait_for_timeout(3000)
 cue('Read the starting move, then confirm a partner.');page.locator('#starter-grid .cell').filter(has_text='Charmander').click();page.wait_for_timeout(4000);page.locator('#starter-ok').click();page.wait_for_timeout(3500)
 cue('Choose Play to enter the dungeon.');page.locator('#scr-menu [data-go=play]').click();page.wait_for_timeout(5000)
 cue('Move with WASD. The active attack fires automatically.');page.keyboard.down('d');page.wait_for_timeout(4000);page.keyboard.up('d');page.wait_for_timeout(1500)
 duration=round(time.monotonic()-clock-start,2);v=page.video;ctx.close();raw=RAW/'first-session.webm';v.save_as(str(raw))
 save(raw,'first-session','Start a fresh guest run','Login, personality questions, partner selection and the opening of a normal run.','guest-login',['how-to-play'],start,duration,1280,720,captions,'Desktop Chromium; paced automated mouse and keyboard inputs; no gameplay-state editing.')
 # A distinct starter-selection task, not a repeated combat montage.
 ctx=b.new_context(viewport={'width':1280,'height':720},locale='en-US',record_video_dir=str(RAW/'starter-selection'),record_video_size={'width':1280,'height':720})
 page=ctx.new_page();clock=time.monotonic();login(page);page.locator('#btn-guest').click();page.wait_for_timeout(300)
 for _ in range(8):page.locator('#test-a button').first.click();page.wait_for_timeout(150)
 page.locator('#res-other').click();start=time.monotonic()-clock;captions=[]
 cue('You can choose a different partner after the personality result.');page.wait_for_timeout(3500)
 for name,text in [('Bulbasaur','Bulbasaur opens with Vine Whip. Read the move before confirming.'),('Squirtle','Squirtle opens with Water Gun. Its evolution needs Power.'),('Charmander','Charmander opens with Ember. Plan Power and move level five.')]:
  page.locator('#starter-grid .cell').filter(has_text=name).click();cue(text);page.wait_for_timeout(6000)
 cue('Confirm your choice, then use the build guide for its exact route.');page.locator('#starter-ok').click();page.wait_for_timeout(3500)
 duration=round(time.monotonic()-clock-start,2);v=page.video;ctx.close();raw=RAW/'starter-selection.webm';v.save_as(str(raw))
 save(raw,'starter-selection','Compare three opening partners','Read the actual in-game starting-move labels before choosing a partner; this is not a survival-time comparison.','starter-roster',['builds','starters'],start,duration,1280,720,captions,'Desktop starter-selector recording. No claim of comparative build performance.')
 # Dedicated movement and pause controls, separate from starter selection.
 ctx=b.new_context(viewport={'width':1280,'height':720},locale='en-US',record_video_dir=str(RAW/'desktop-controls'),record_video_size={'width':1280,'height':720})
 page=ctx.new_page();clock=time.monotonic();login(page);partner(page);page.locator('#scr-menu [data-go=play]').click();page.wait_for_timeout(2000);start=time.monotonic()-clock;captions=[]
 cue('Move with WASD or the arrow keys. Attacks fire automatically.')
 for key in ['d','s','a','w']:
  page.keyboard.down(key);page.wait_for_timeout(2000);page.keyboard.up(key)
 cue('Use 1–4 or Q / E to choose a learned active slot. This fresh run has one attack.');page.keyboard.press('1');page.wait_for_timeout(4000)
 cue('Press Escape to pause solo play.');page.keyboard.press('Escape');page.wait_for_timeout(4000)
 page.locator('#btn-pause-settings').click();page.locator('#set-tabs [data-t=ctl]').click();cue('Settings lists the available keyboard controls.');page.wait_for_timeout(5000)
 duration=round(time.monotonic()-clock-start,2);v=page.video;ctx.close();raw=RAW/'desktop-controls.webm';v.save_as(str(raw))
 save(raw,'desktop-controls','Move, attack and pause','Normal keyboard movement followed by the actual pause and controls settings screens.','keyboard-controls',['how-to-play'],start,duration,1280,720,captions,'Desktop Chromium keyboard controls. No second move is claimed in the fresh run.')
 b.close()

save(RAW/'gameplay.webm','gameplay-preview','A first look at the battlefield','An excerpt from an unmodified Charmander guest trial: movement, automatic Ember attacks and experience pickups.','ember-combat',[''],19,22,1280,720,[(0,'Ember fires automatically while the partner moves.'),(7,'Keep space around the partner and approach dropped experience.'),(14,'Upgrade offers and outcomes vary between runs.')],'Unbundled dev.html source build; read-only observations drive normal keyboard input; no stat or card edits.')
save(RAW/'mobile-touch.webm','mobile-touch','Landscape touch controls','A touch-enabled Chromium demonstration of the game layout, drag joystick and portrait rotation prompt. This is browser emulation, not a physical-device test.','mobile-landscape',['mobile'],0,21.6,844,390,[(0,'Chromium touch emulation: landscape 844 × 390.'),(6,'The run uses the same guest profile flow.'),(10,'Drag the play area to reveal and move the virtual joystick.'),(17,'Portrait orientation displays the rotation prompt.')],'Chromium touch emulation via browser input events. No physical iPhone/Android, installation, FPS or offline certification.')
