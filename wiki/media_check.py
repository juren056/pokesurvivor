"""Rendered media acceptance: images, sitemap, playback, captions and recovery."""
from pathlib import Path
import os
import hashlib,json,urllib.request,xml.etree.ElementTree as ET
import urllib.error
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent;DIST=HERE/'dist';OUT=HERE/'artifacts';BASE=os.environ.get('WIKI_BASE','http://127.0.0.1:4173')
report={'images':[],'videos':[],'layouts':[],'failures':[]}
manifest=json.loads((DIST/'assets/media/manifest.json').read_text(encoding='utf-8'))
routes=json.loads((DIST/'build-manifest.json').read_text(encoding='utf-8'))
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
tree=ET.parse(DIST/'sitemap.xml')
indexed={u.findtext('s:loc',namespaces=ns):[i.text for i in u.findall('i:image/i:loc',ns)] for u in tree.getroot()}

with sync_playwright() as p:
 browser=p.chromium.launch();ctx=browser.new_context(viewport={'width':1440,'height':1000});page=ctx.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 for route in routes:
  requests=[];listener=lambda req:requests.append(req.url);page.on('request',listener)
  page.goto(BASE+route);page.wait_for_load_state('networkidle')
  assert not any('.webm' in u for u in requests),(route,'video downloaded before play')
  page.remove_listener('request',listener)
  # Force only test loading of below-fold images, not production eager loading.
  page.locator('img').evaluate_all("els=>els.forEach(e=>e.loading='eager')")
  page.wait_for_function("Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)")
  for img in page.locator('.guide-media img').all():
   assert img.get_attribute('width') and img.get_attribute('height')
   assert img.get_attribute('alt')
  if route!='/search/':
   sources=page.locator('.guide-media img').evaluate_all('(els)=>els.map(e=>new URL(e.src).pathname)')
   assert all('https://pokemonsurvivorwiki.com'+s in indexed['https://pokemonsurvivorwiki.com'+route] for s in sources)
  report['images'].append({'route':route,'loaded':page.locator('.guide-media img').count(),'idleVideoDownloads':0})
 for width,height,label in [(1440,1000,'desktop'),(768,900,'tablet'),(390,844,'mobile'),(375,500,'short-mobile')]:
  page.set_viewport_size({'width':width,'height':height})
  for route in ['/','/how-to-play/','/move-evolutions/','/mobile/','/builds/']:
   page.goto(BASE+route);page.wait_for_load_state('networkidle')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(route,width,'overflow')
   for v in page.locator('video').all():
    box=v.bounding_box();assert box['width']<=width,(route,width,'video bounds')
   report['layouts'].append({'route':route,'width':width,'height':height,'overflow':False})
  if label in ['desktop','mobile']:
   page.goto(BASE+'/');page.wait_for_load_state('networkidle');page.screenshot(path=str(OUT/f'media-{label}-home.png'))
   page.goto(BASE+'/mobile/');page.wait_for_load_state('networkidle');page.screenshot(path=str(OUT/f'media-{label}-guide.png'))
 page.set_viewport_size({'width':1280,'height':900})
 for record in manifest['videos']:
  route=record['pages'][0];page.goto(BASE+route);v=page.locator(f'[data-video-id="{record["id"]}"] video');v.scroll_into_view_if_needed()
  v.evaluate('(v)=>v.play()');page.wait_for_timeout(700)
  page.wait_for_function('(id)=>{const v=document.querySelector(`[data-video-id="${id}"] video`);return v.currentTime>0.2 && v.videoWidth>0}',arg=record['id'])
  assert v.evaluate('v=>v.textTracks.length')==1
  page.wait_for_function('(id)=>document.querySelector(`[data-video-id="${id}"] video`).textTracks[0].cues?.length>0',arg=record['id'])
  duration=v.evaluate('v=>v.duration');assert duration>5 and abs(duration-record['duration'])<1.6,(record['id'],duration)
  # Exercise seeking, decoding at another timestamp, and completed playback.
  v.evaluate('v=>{v.currentTime=v.duration/2}');page.wait_for_timeout(500)
  frames=v.evaluate('v=>v.getVideoPlaybackQuality().totalVideoFrames');assert frames>0
  v.evaluate('v=>{v.currentTime=Math.max(0,v.duration-.3);v.play()}')
  page.wait_for_function('(id)=>document.querySelector(`[data-video-id="${id}"] video`).ended',arg=record['id'],timeout=60000)
  assert not v.evaluate('v=>v.error')
  transcript=page.locator(f'[data-video-id="{record["id"]}"] .video-transcript');transcript.locator('summary').click();assert transcript.locator('li').first.is_visible()
  report['videos'].append({'id':record['id'],'duration':duration,'framesDecoded':frames,'playback':'started, seeked, ended','captions':'loaded','transcript':'opened'})
 broken=ctx.new_page();broken.route('**/*.webm',lambda r:r.abort());broken.goto(BASE+'/');v=broken.locator('video');v.evaluate('v=>{v.load();v.play().catch(()=>{})}')
 broken.locator('.video-error').wait_for(state='visible');assert broken.locator('.video-transcript').is_visible();report['errorRecovery']='Aborted video shows recovery text and retains transcript'
 assert not errors,errors
 browser.close()

# Accept a correct partial transfer or a complete-body fallback, never an error body.
video=manifest['videos'][0]['id']+'.webm';raw=(DIST/'assets/media'/video).read_bytes()
request=urllib.request.Request(BASE+'/assets/media/'+video,headers={'Range':'bytes=0-1023'})
with urllib.request.urlopen(request) as response:
 body=response.read();status=response.status
 assert (status==206 and body==raw[:1024]) or (status==200 and body==raw)
 report['range']={'environment':'local Python preview','status':status,'mode':'partial 206' if status==206 else 'complete original file 200 fallback','verified':True}
try:
 with urllib.request.urlopen(urllib.request.Request(BASE+'/assets/media/'+video,headers={'Range':f'bytes={len(raw)+1}-'})) as response:
  body=response.read();assert response.status==200 and body==raw
  report['range']['invalidRange']='local preview ignored Range and returned the complete original file'
except urllib.error.HTTPError as error:
 assert error.code==416 and error.headers['Content-Range']==f'bytes */{len(raw)}'
 report['range']['invalidRange']='416 with actual file size'
report['publishedImages']=len(manifest['images']);report['publishedVideos']=len(manifest['videos'])
report['imageKinds']={kind:sum(m['kind']==kind for m in manifest['images']) for kind in ['capture','concept','diagram']}
(OUT/'media-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(report["images"])} image route checks, {len(report["layouts"])} media layout checks, {len(report["videos"])} complete video playback/caption/seek checks; failure recovery and Range fallback verified.')
