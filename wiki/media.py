"""Progressive, server-rendered media with explicit capture/concept provenance."""
from pathlib import Path
import html
import json
import re

HERE=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
IMAGES=json.loads((HERE/'media-images.json').read_text(encoding='utf-8'))+json.loads((HERE/'media-diagrams.json').read_text(encoding='utf-8'))
BY_ID={m['id']:m for m in IMAGES}
VIDEOS=json.loads((HERE/'media-videos.json').read_text(encoding='utf-8')) if (HERE/'media-videos.json').exists() else []
VIDEO_BY_ID={m['id']:m for m in VIDEOS}
USED={}
USED_VIDEOS={}


def image(ident,eager=False):
    m=BY_ID[ident]
    if m['kind']=='diagram':
        src=f'/assets/media/{ident}.svg';srcset=''
    else:
        widths=m['variants'];src=f'/assets/media/{ident}-{max(widths)}.webp'
        srcset=' srcset="'+', '.join(f'/assets/media/{ident}-{w}.webp {w}w' for w in widths)+'" sizes="(max-width: 600px) calc(100vw - 40px), (max-width: 1000px) 85vw, 800px"'
    label='Controlled game demonstration' if m.get('controlledFixture') else {'capture':'Game capture','concept':'Original concept art · AI-assisted','diagram':'Source-based diagram'}[m['kind']]
    return f'''<figure class="guide-media media-{m['kind']}" data-media-id="{ident}"><a href="{src}" target="_blank" rel="noopener" aria-label="{E('Open full-size image: '+m['caption'])}"><img src="{src}"{srcset} width="{m['width']}" height="{m['height']}" alt="{E(m['alt'])}" loading="{'eager' if eager else 'lazy'}" decoding="async" {'fetchpriority="high"' if eager else ''}></a><figcaption><strong>{label}.</strong> {E(m['caption'])} <a href="/about/#media-credits">Credits & scope</a></figcaption></figure>'''


def gallery(ids):
    return '<div class="media-pair">'+''.join(image(i) for i in ids)+'</div>'


def video(ident):
    if ident not in VIDEO_BY_ID:return ''
    m=VIDEO_BY_ID[ident];poster=f'/assets/media/{m["poster"]}-{max(BY_ID[m["poster"]]["variants"])}.webp'
    return f'''<figure class="guide-video" data-video-id="{ident}"><h3>{E(m['title'])}</h3><video controls playsinline preload="none" width="{m['width']}" height="{m['height']}" style="--video-ratio:{m['width']}/{m['height']}" poster="{poster}" aria-label="{E(m['title'])}"><source src="/assets/media/{ident}.webm" type="video/webm"><track kind="captions" src="/assets/media/{ident}.vtt" srclang="en" label="English" default><p>Your browser cannot play this video. <a href="/assets/media/{ident}.webm">Open the WebM recording</a> or read the steps below.</p></video><p class="video-error" role="status" hidden>The video could not load. Read the transcript below or <a href="/assets/media/{ident}.webm">open the recording</a>.</p><figcaption>{E(m['description'])} Silent recording with English captions. <a href="/about/#media-credits">Capture & credits</a></figcaption><details class="video-transcript"><summary>Read the video steps</summary><ol>{''.join('<li>'+E(c['text'])+'</li>' for c in m['captions'])}</ol></details></figure>'''


def after_section(body,heading,extra):
    marker='<h2>'+heading+'</h2>'
    start=body.find(marker)
    if start<0:raise ValueError('Media placement heading missing: '+heading)
    end=body.find('</section>',start)+len('</section>')
    return body[:end]+extra+body[end:]


def enhance(slug,body):
    if slug=='':
        body=body.replace('<section class="starter-lab"','<div class="hero-field">'+image('rift-guardian',True)+'<section class="starter-lab"',1)
        body=body.replace('</noscript></section></div>','</noscript></section></div></div>',1)
        body=body.replace('<p class="hero-note">For jpter78’s browser game. Source-backed data, practical guides.</p>','<p class="hero-note">For jpter78’s browser game. Source-backed data, practical guides.</p>'+image('first-run'),1)
        marker='<section class="reference-home">'
        film='<section class="home-section field-film" id="see-the-game"><div><h2>See the run.<br>Read the next move.</h2><p>Real captures from a fresh local guest session. Watch the automatic attack, then follow the guide for your next upgrade.</p><a class="text-link" href="/how-to-play/">Learn the controls</a></div><div>'+video('gameplay-preview')+'</div></section><div class="home-field-shots">'+image('ember-combat')+'</div>'
        body=body.replace(marker,film+marker,1)
    elif slug=='how-to-play':
        body=after_section(body,'Start a first run',image('first-run-flow')+video('first-session')+gallery(['guest-login','personality-quiz'])+gallery(['quiz-result','partner-menu']))
        body=after_section(body,'Learn these controls first',image('controls-map')+image('keyboard-controls')+video('desktop-controls'))
        body=after_section(body,'Choose upgrades with a destination',image('level-2-cards'))
    elif slug=='mobile':
        body=after_section(body,'Set up touch controls',image('touch-map')+video('mobile-touch')+gallery(['mobile-landscape','mobile-joystick']))
        body=after_section(body,'If the run feels slow',gallery(['mobile-touch-settings','graphics-settings']))
        body+=gallery(['mobile-paused','mobile-rotate'])+image('mobile-expedition')
    elif slug=='move-evolutions':
        body=after_section(body,'If the golden card is missing',image('evolution-conditions')+gallery(['ember-evolution','bubble-evolution'])+video('evolution-route'))
        body+=image('evolution-notebook')
        if 'golden-evolution-card' in BY_ID:body+=gallery(['golden-evolution-card','evolved-active-move'])
    elif slug=='builds':
        body=after_section(body,'Four routes to start with',image('build-route')+video('starter-selection'))
        body+=gallery(['fire-trail','water-trail'])+image('grass-trail')+gallery(['experience-route','run-summary'])+image('permanent-upgrades')
    elif slug=='starters':
        body=after_section(body,'Three ways to choose',image('starter-roster')+gallery(['starter-bulbasaur','starter-squirtle'])+image('starter-charmander'))
    elif slug=='tier-list':body+=image('build-route')
    elif slug=='types':body=after_section(body,'Read the chart correctly',image('type-products'))
    elif slug=='pokedex':body=body.replace('<section class="data-section"',image('collection')+'<section class="data-section"',1)
    elif slug=='legendaries':body=after_section(body,'Follow the rift route',image('regional-gacha')+image('rift-atlas'))
    elif slug=='co-op':body=after_section(body,'Could not connect: what to check first',image('coop-connection-check-flow'))+image('co-op-camp')+image('guest-account')
    elif slug=='save-recovery':body=after_section(body,'Safety rules before troubleshooting',image('save-safety-decision-flow'))
    elif slug=='download':body+=image('mobile-expedition')
    elif slug=='about':
        body+='''<section class="article-section" id="media-credits"><h2>Capture and artwork credits</h2><p>Game screenshots and silent recordings were captured on 15 October 2026 from fresh, disposable local guest sessions of the JPTER78 source snapshot <code>b297089</code>. Normal combat uses automated keyboard inputs and the unbundled <code>dev.html</code> build without modifying game stats, drops, cards or save progress. The separately labeled controlled evolution demonstration preconfigures Ember level five and Power, then uses the developer level-up trigger and the real golden-card UI. Its visible label, caption and manifest distinguish it from an unassisted run. Touch captures use Chromium emulation, not physical iPhone or Android hardware. These clips illustrate the recorded steps, not comparative performance benchmarks.</p><p>Game: <a href="https://github.com/JPTER78/pokesurvivor">JPTER78 / PokéSurvivor</a>. Embedded sprites: SpriteCollab, <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>; <a href="https://github.com/JPTER78/pokesurvivor/blob/b29708900da26b34e70d2dc07ad1659a719f4a78/CREDITS.md">individual artist credits</a>. These noncommercial guide captures preserve game artwork and do not grant a commercial media license. Pokémon © Nintendo / Creatures / GAME FREAK.</p><p>Forest, elemental trail, camp and portal pictures are original AI-assisted concept illustrations made for this Wiki, not official environments or gameplay screenshots. Mechanic diagrams are original source-derived SVGs. <a href="/assets/media/manifest.json">Read the media source and production manifest</a>.</p></section>'''
    video_ids=re.findall(r'data-video-id="([^"]+)"',body)
    USED_VIDEOS[slug]=video_ids
    USED[slug]=list(dict.fromkeys(re.findall(r'data-media-id="([^"]+)"',body)+[VIDEO_BY_ID[v]['poster'] for v in video_ids]))
    return body


def export_manifest(dest):
    records=[]
    for m in IMAGES:
        placed=[slug for slug,ids in USED.items() if m['id'] in ids]
        if placed:records.append({**m,'pages':['/'+s+'/' if s else '/' for s in placed]})
    videos=[{**m,'pages':['/'+s+'/' if s else '/' for s,ids in USED_VIDEOS.items() if m['id'] in ids]} for m in VIDEOS]
    (dest/'manifest.json').write_text(json.dumps({'images':records,'videos':videos},indent=2)+'\n',encoding='utf-8')
