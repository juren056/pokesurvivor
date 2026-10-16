"""Dependency-free, deterministic static Wiki builder. Never writes game files."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import xml.etree.ElementTree as ET
import media
import agent_resources

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / 'dist'
SITE = 'https://pokemonsurvivorwiki.com'
DATA = json.loads((HERE / 'data/game.json').read_text(encoding='utf-8'))
CONTENT = json.loads((HERE / 'content.json').read_text(encoding='utf-8'))
REVIEWED = CONTENT['reviewed']
PAGES = {}
E = lambda s: html.escape(str(s), quote=True)
URL = lambda slug: '/' + slug + '/' if slug else '/'
MOVES = {m['id']: m for m in DATA['moves']}


def link(slug, text, cls=''):
    return f'<a class="{cls}" href="{URL(slug)}">{E(text)}</a>'


def icon(name, size=24):
    paths = {
        'arrow': '<path d="M5 12h14m-5-5 5 5-5 5"/>',
        'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
        'book': '<path d="M12 5c-3-2-6-2-9-1v15c3-1 6-1 9 1 3-2 6-2 9-1V4c-3-1-6-1-9 1Zm0 0v15"/>',
        'dex': '<rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="9" r="3"/><path d="M9 16h6M9 18h3"/>',
        'evolve': '<path d="M4 17h5V7h11m-4-4 4 4-4 4M4 12v9"/><circle cx="4" cy="8" r="2"/>',
        'fire': '<path d="M13 3c1 5-3 5-2 9 2-1 3-3 4-4 4 5 5 8 2 11-4 4-11 2-11-4 0-4 5-6 7-12Z"/>',
        'water': '<path d="M12 3C9 7 5 12 5 16a7 7 0 0 0 14 0c0-4-4-9-7-13Z"/><path d="M9 16c0 2 1 3 3 3"/>',
        'grass': '<path d="M20 4C8 3 3 8 5 15s14 6 15-11Z"/><path d="m4 21 11-11M9 16v-5m0 5h5"/>',
        'mobile': '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 5h4m-3 14h2"/>',
        'shield': '<path d="m12 3 8 3v6c0 4-5 7-8 9-3-2-8-5-8-9V6Z"/><path d="m8 12 3 3 5-6"/>',
        'layers': '<path d="m12 3 10 5-10 5L2 8Zm-9 9 9 5 9-5m-18 5 9 5 9-5"/>',
        'sort': '<path d="m8 8 4-4 4 4m-8 8 4 4 4-4"/>'
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def badges(types):
    return ''.join(f'<span class="type type-{E(t)}">{E(t.title())}</span>' for t in types)


def table(headers, rows, searchable=False, kind=''):
    filters = ''
    if searchable:
        opts = ''.join(f'<option value="{t}">{t.title()}</option>' for t in DATA['types'])
        filters = f'''<form class="table-tools" data-filter-form><label>Find in this table<input type="search" data-filter placeholder="Name, move or stat…"></label>
<label>Type<select data-type><option value="">All types</option>{opts}</select></label><button type="reset" class="button secondary">Reset</button></form>
<p class="result-count" data-count role="status" aria-live="polite"></p>'''
    head = ''.join(f'<th scope="col" aria-sort="none"><span class="sort-label">{E(h)}</span><button type="button" class="sort-control" data-sort="{i}">{E(h)}{icon("sort",14)}</button></th>' if searchable else f'<th scope="col">{E(h)}</th>' for i,h in enumerate(headers))
    body = []
    for row in rows:
        if isinstance(row, dict):
            cells, types, ident = row['cells'], row.get('types', []), row.get('id', '')
        else:
            cells, types, ident = row, [], ''
        id_attr = f' id="{E(ident)}"' if ident else ''
        body.append(f'<tr{id_attr} data-types="{E(" ".join(types))}">' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    return f'''<section class="data-section" data-table>{filters}<div class="table-scroll" role="region" aria-label="{E(kind or 'Reference table')}" tabindex="0"><table><caption class="sr-only">{E(kind or 'Reference table')}</caption><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div><p data-empty hidden>No matches. Try another name or reset the filters.</p></section>'''


def section(title, body, ident=None):
    ident = ident or '-'.join(title.lower().replace('?', '').split())
    return f'<section class="article-section" id="{E(ident)}"><h2>{E(title)}</h2>{body}</section>'


def add(slug, title, description, body, group='Guides', related=None, sources=None, index=True):
    PAGES[slug] = dict(title=title, description=description, body=body, group=group,
                       related=related or [], sources=sources or [], index=index)


def prose(p):
    body = f'<p class="lead">{E(p["intro"])}</p>'
    for s in p['sections']:
        text = ''.join(f'<p>{E(t)}</p>' for t in s.get('paragraphs', []))
        if 'steps' in s:
            text += '<ol class="steps">' + ''.join(f'<li>{E(t)}</li>' for t in s['steps']) + '</ol>'
        if 'table' in s:
            text += table(s['table']['headers'], [[E(c) for c in r] for r in s['table']['rows']])
        body += section(s['heading'], text)
    if p.get('externalSources'):
        body += section('Additional source', ''.join(f'<p><a href="{E(s["url"])}">{E(s["label"])}</a></p>' for s in p['externalSources']))
    add(p['slug'], p['title'], p['description'], body, p['group'], p['related'], p['sources'])


def reference_pages():
    rows = [dict(id=f'p{p["dex"]}', types=p['types'], cells=[f'<span class="dex-no">{p["dex"]:03}</span>', f'<strong>{E(p["name"])}</strong>', badges(p['types']), p['hp'], p['spd'], f'{p["atk"]:.2f}×', p['gen'], ('Starter / gacha' if p.get('starter') else 'Gacha') if p['gacha'] else 'Outside gacha pool']) for p in DATA['dex']]
    body = f'<p class="lead">Compare all {len(rows)} playable partners in the recorded source snapshot. HP, speed and attack multiplier are game values, not mainline Pokémon battle stats.</p>'
    body += '<p>Search a name or number, or choose a type. Dual-type entries match either type. The collection column uses the game’s regional gacha eligibility, including eligible legendary and mythical partners. Starters are also offered at the beginning. A rift encounter is separate from adding a normal partner to your collection.</p>'
    body += table(['No.', 'Pokémon', 'Type', 'HP', 'Speed', 'Attack', 'Gen', 'Collection'], rows, True, 'PokéSurvivor Pokémon stats')
    add('pokedex', 'PokéSurvivor Pokédex: stats & unlock routes', 'Search 966 PokéSurvivor partners by name or type. Compare HP, movement speed, attack multiplier and acquisition category.', body, 'Database', ['starters','tier-list','legendaries'], ['js/data/pokedex.js','js/systems/gacha.js'])
    rows = [dict(id=m['id'],types=[m['type']],cells=[f'<strong>{E(m["name"])}</strong>',badges([m['type']]), E(m['kind'].title()), E(m['damage'] if m['damage'] is not None else '—'), f'{m["cooldown"]:g}s' if m['cooldown'] else '—',m['maxLevel'], link('move-evolutions',m['evolution']['name']) if m['evolution'] else 'No evolution']) for m in DATA['moves']]
    body = '<p class="lead">Every base move, attack pattern and evolution in the source snapshot. Choose attacks by how they work as well as their numbers.</p><p>Damage and cooldown are level-one definition values, before partner multipliers and run upgrades. They are not complete DPS measurements: attack count, hit rate, duration and coverage differ between patterns. A dash, aura and projectile cannot be ranked by one raw number.</p>'
    body += table(['Move','Type','Pattern','Base damage','Cooldown','Max level','Evolution'],rows,True,'PokéSurvivor move definitions')
    add('moves','PokéSurvivor moves: damage, patterns & evolutions','Search all 64 PokéSurvivor moves with base damage, cooldown, attack pattern, maximum level and evolution links.',body,'Database',['move-evolutions','builds','types'],['js/data/moves.js'])
    rows = [dict(id=m['id'],types=[m['type']],cells=[E(m['name']), badges([m['type']]),m['maxLevel'],E(m['evolution']['requirement']), f'<strong>{E(m["evolution"]["name"])}</strong>']) for m in DATA['moves'] if m['evolution']]
    options = ''.join(f'<option value="{E(m["id"])}">{E(m["name"])}</option>' for m in DATA['moves'])
    checker = f'''<div class="tool" data-evolution><h3>Check your next evolution</h3><p>Select what you have in this run. This checker does not access your game save.</p><div class="tool-inputs"><label>Move<select id="evo-move">{options}</select></label><label>Current level<input id="evo-level" type="number" min="1" max="5" value="1" required></label></div><label class="check"><input type="checkbox" id="evo-stat"> I have taken the required stat card in this run</label><output id="evo-result" aria-live="polite"></output><noscript><p>Enable JavaScript for the checker, or use the complete table below.</p></noscript></div>'''
    body = '<p class="lead">Max the move, take its required stat upgrade in the same run, then choose the golden evolution card. Meeting the conditions makes an evolution eligible; it does not automatically evolve the move.</p>' + checker
    body += section('If the golden card is missing','<ol class="steps"><li>Check the move is at its maximum level.</li><li>Check the exact prerequisite in the table; different moves need different stat cards.</li><li>Confirm you took that stat card in this run, rather than an unrelated permanent upgrade.</li><li>Keep leveling and look for the separate golden card. An already evolved move cannot evolve again.</li></ol><p>Buffs have no evolution. Learning another move is different from evolving one you already have.</p>')
    body += table(['Move','Type','Required level','Required stat card','Evolves into'],rows,True,'Move evolution conditions')
    add('move-evolutions','PokéSurvivor move evolutions & requirement checker','Look up all 59 move evolution conditions, check your level and stat prerequisite, and troubleshoot missing golden cards.',body,'Database',['builds','moves','how-to-play'],['js/data/moves.js','js/systems/levelup.js'])
    starters = DATA['starters']
    maxhp, maxspd, maxatk = (max(p[k] for p in starters) for k in ('hp','spd','atk'))
    ranked = sorted([(round(100*(.35*p['hp']/maxhp+.25*p['spd']/maxspd+.40*p['atk']/maxatk),1),p) for p in starters],key=lambda x:(-x[0],x[1]['dex']))
    rows = [dict(types=p['types'],cells=[f'<strong>{E(p["name"])}</strong>',badges(p['types']),link('moves',MOVES[p['start']]['name']),p['hp'],p['spd'],f'{p["atk"]:.2f}×',E(MOVES[p['start']]['evolution']['requirement'])]) for p in starters]
    body = '<p class="lead">All 29 starter choices, with the starting attack and evolution prerequisite you need to plan your first run.</p><p>The personality quiz suggests a partner, but you can reject the suggestion and select another. Choose a move pattern you can position around, then use the table to plan its evolution. Partners of the same elemental type do not always share a starting move.</p>'
    body += section('Three ways to choose','<ul><li><strong>Prefer distance?</strong> Compare partners starting with Ember or Water Gun. Read the move patterns before committing.</li><li><strong>Want a different opening?</strong> Psyduck and Slowpoke start with Confusion, giving a Psychic option outside the regional starter trios.</li><li><strong>Planning an evolution?</strong> Piplup starts with Bubble and needs Sprint; a Water Gun opener needs Power instead.</li></ul><p>These are build considerations, not a claim that one choice always survives longest.</p>')
    body += table(['Partner','Type','Starting move','HP','Speed','Attack','Evolution stat'],rows,True,'Starting partners')
    add('starters','Best PokéSurvivor starters: all 29 starting options','Compare the 29 PokéSurvivor starters by starting move, HP, speed and attack, with the stat card each opening move needs.',body,'Guides',['tier-list','builds','move-evolutions'],['js/data/starters.js','js/data/pokedex.js','js/data/moves.js'])
    rows=[]
    for score,p in ranked:
        band='A' if score>=90 else 'B' if score>=82 else 'C'
        rows.append(dict(types=p['types'],cells=[f'<span class="rank rank-{band}">{band}</span>',f'<strong>{E(p["name"])}</strong>',badges(p['types']),f'{score:.1f}',p['hp'],p['spd'],f'{p["atk"]:.2f}×', E(MOVES[p['start']]['name'])]))
    body = '<p class="lead">A transparent starter stat tier list for the 29 starting partners. Use it to compare starting numbers, then check the move and matchup before picking.</p><div class="notice"><strong>Source-based ranking.</strong> These bands are not gameplay-tested rankings, a co-op meta, or a tier list of all 966 partners.</div>'
    body += section('What the score measures',f'<p>Score = 100 × (0.35 × HP / {maxhp} + 0.25 × speed / {maxspd} + 0.40 × attack / {maxatk:.2f}). Each denominator is the highest value among the 29 starters in this snapshot. A = 90 or above; B = 82 to below 90; C = below 82.</p><p>The weights are an editorial choice, not an official game formula. A higher score only means a stronger weighted starting-stat profile. It excludes move pattern, range, weather, resistances, run upgrades and player skill; an A-band partner is not guaranteed to outperform a lower-band one.</p>')
    body += table(['Band','Partner','Type','Score','HP','Speed','Attack','Starting move'],rows,True,'Starter stat score bands')
    body += section('Turn the ranking into a decision','<p>Use the starter guide to find a move you can handle. Use the evolution checker to identify its required card, and test the route in your own runs. For a durable survival-time ranking, comparable repeated runs and recorded conditions would be needed; this site does not invent those results.</p>')
    add('tier-list','PokéSurvivor tier list: starter stat rankings','Compare 29 PokéSurvivor starters with transparent stat-based tier bands, exact scoring weights and starting moves.',body,'Guides',['starters','builds','types'],['js/data/pokedex.js','js/data/starters.js'])
    options=''.join(f'<option value="{t}">{t.title()}</option>' for t in DATA['types'])
    tool=f'''<div class="tool" data-matchup><h3>Check a type matchup</h3><div class="tool-inputs"><label>Attacking type<select id="attack-type">{options}</select></label><label>Defending type<select id="defend-type">{options}</select></label><label>Second defending type<select id="defend-second"><option value="">None</option>{options}</select></label></div><output id="type-result" aria-live="polite"></output><noscript><p>Enable JavaScript for dual-type calculations. The single-type chart remains available below.</p></noscript></div>'''
    rows=[[badges([a])]+[f'<span class="mult {"good" if DATA["matrix"][a][d]>1 else "weak" if DATA["matrix"][a][d]<1 else ""}">{DATA["matrix"][a][d]:g}×</span>' for d in DATA['types']] for a in DATA['types']]
    body='<p class="lead">PokéSurvivor softens the usual Pokémon type chart: weaknesses are 1.6×, resistances 0.6× and mainline immunities 0.3×. Dual-type products are clamped between 0.3× and 2.4×.</p>'+tool
    body+=section('Read the chart correctly','<p>Rows are attacking types; columns are defending types. For two defending types, multiply their softened values, then apply the cap. For example, Water against Fire/Rock is capped at 2.4× rather than 2.56×. Normal against Ghost is 0.3×, not zero.</p><p>This is the type factor only. It does not include weather, partner attack, defensive upgrades or a move’s other effects.</p>')
    body+=table(['Attack / defend']+[t.title() for t in DATA['types']],rows,kind='Single-type damage multipliers')
    add('types','PokéSurvivor type chart & damage calculator','Calculate single and dual-type matchups with PokéSurvivor’s softened 1.6×, 0.6× and 0.3× rules and 2.4× cap.',body,'Database',['moves','builds','legendaries'],['js/data/types.js'])
    legends=[p for p in DATA['dex'] if p.get('leg')]
    rows=[dict(types=p['types'],cells=[E(p['name']),badges(p['types']),p['hp'],p['spd'],f'{p["atk"]:.2f}×']) for p in legends]
    body=f'<p class="lead">The source snapshot marks {len(legends)} legendary or mythical partners. Rifts let you fight legendary encounters; the regional gacha separately includes eligible partners for your collection.</p>'
    body+=section('Follow the rift route','<ol class="steps"><li>During a run, watch for a rift opening on the map.</li><li>Enter it to move into a separate legendary arena.</li><li>Read the enemy’s attacks, terrain and type before committing to close range.</li><li>Defeat the legendary, collect the rewards and return to the main run. Winning grants a move link; it does not automatically add the normal partner to your collection.</li></ol><p>Use the Pokédex collection column for regional gacha eligibility. The roster below identifies legendary/mythical entries, not a guaranteed spawn schedule or a list of starter choices.</p>')
    body+=table(['Partner','Type','HP','Speed','Attack'],rows,True,'Rift legendary roster')
    add('legendaries','PokéSurvivor legendaries: rifts & roster','Understand PokéSurvivor rift encounters and browse the source snapshot’s legendary and mythical partner roster.',body,'Database',['types','pokedex','move-evolutions'],['js/systems/rift.js','js/data/pokedex.js','js/systems/gacha.js'])
    body='<p class="lead">Selected game changes from the repository snapshot. These are developer changelog entries, not claims that every change was independently playtested here.</p>'
    for entry in DATA['changelog'][:8]:
        text=f'<p class="date">Game changelog: {E(entry["date"])}</p>'
        for key,label in [('new','Added'),('changed','Changed'),('fixed','Fixed')]:
            if entry[key]: text+=f'<h3>{label}</h3><ul>'+''.join(f'<li>{E(x)}</li>' for x in entry[key])+'</ul>'
        body+=section(entry['title'],text, 'update-'+entry['date'])
    add('updates','PokéSurvivor updates & source snapshot','Read recent PokéSurvivor developer changelog entries, including account recovery, co-op fixes and the Judgment of Arceus.',body,'Guides',['co-op','how-to-play','about'],['js/data/changelog.js'])


def home():
    starters = [next(p for p in DATA['starters'] if p['dex']==n) for n in (4,1,7)]
    initial = starters[0]
    move = MOVES[initial['start']]
    choices = ''.join(f'<label class="starter-choice"><input type="radio" name="opening-partner" value="{p["dex"]}" {"checked" if i==0 else ""}><span>{icon(p["types"][0],18)}{E(p["name"])}</span></label>' for i,p in enumerate(starters))
    featured=[('how-to-play','book','Make your first run count','Controls, upgrade cards and the first decisions that matter.'),('starters','grass','Find your starting partner','Compare 29 opening moves and stat profiles.'),('move-evolutions','evolve','Unlock the next evolution','The level, stat card and golden-card conditions.'),('mobile','mobile','Take the run to mobile','Touch controls, installation and keeping your save.')]
    routes=''.join(f'<a class="route" href="{URL(slug)}"><span class="route-icon">{icon(glyph)}</span><span><strong>{E(title)}</strong><span>{E(desc)}</span></span>{icon("arrow",20)}</a>' for slug,glyph,title,desc in featured)
    preview=[]
    for n in (1,4,7,25):
        p=next(p for p in DATA['dex'] if p['dex']==n)
        preview.append([f'<a href="/pokedex/#p{n}"><span class="dex-no">{n:03}</span> <strong>{E(p["name"])}</strong></a>',badges(p['types']),str(p['hp']),f'{p["atk"]:.2f}×'])
    sample=table(['Partner','Type','HP','Attack'],preview,kind='A sample of the partner reference')
    body=f'''<section class="opening"><div class="hero"><div class="hero-copy"><h1>Plan your next<br><em>PokéSurvivor run.</em></h1><p class="lead">Your independent Pokémon Survivor Wiki. Pick a partner, evolve your moves and build a route through the horde.</p>
<form class="hero-search" action="/search/" role="search"><label class="sr-only" for="home-search">Search Pokémon, moves and guides</label>{icon('search',22)}<input id="home-search" name="q" type="search" maxlength="100" placeholder="Pokémon, moves, or a question…"><button type="submit" aria-label="Search the Wiki">{icon('arrow',23)}</button></form>
<div class="actions">{link('how-to-play','Start your first run','button')}{link('tier-list','Compare starter tiers','button secondary')}</div><p class="hero-note">For jpter78’s browser game. Source-backed data, practical guides.</p></div>
<section class="starter-lab" data-starter-lab aria-labelledby="lab-title"><div class="lab-header"><h2 id="lab-title">Your opening move</h2>{link('starters','All 29 starters')}</div><fieldset class="starter-choices"><legend class="sr-only">Preview a starting partner</legend>{choices}</fieldset>
<div class="partner-profile"><div class="type-emblem" data-lab-emblem>{icon('fire',37)}</div><div><h3 data-lab-name>{E(initial['name'])}</h3><p data-lab-type>Fire · Starter partner</p></div><span class="partner-number" data-lab-number>#{initial['dex']:03}</span></div>
<dl class="partner-stats"><div><dt>HP</dt><dd data-lab-hp>{initial['hp']}</dd></div><div><dt>Movement</dt><dd data-lab-speed>{initial['spd']}</dd></div><div><dt>Attack</dt><dd data-lab-attack>{initial['atk']:.2f}×</dd></div></dl>
<div class="evolution-route" id="lab-result" aria-live="polite" aria-atomic="true"><div><span>Starting move</span><strong data-lab-move>{E(move['name'])}</strong></div>{icon('arrow',20)}<div><span>Evolution</span><strong data-lab-evolution>{E(move['evolution']['name'])}</strong></div></div><p class="lab-requirement" data-lab-requirement>Level {move['maxLevel']} + {E(move['evolution']['requirement'])} in this run, then choose the golden card.</p><a class="lab-link" data-lab-link href="/move-evolutions/#{E(move['id'])}">Plan this evolution {icon('arrow',18)}</a><noscript><p>Preview shows Charmander. Compare every option in the starter guide.</p></noscript></section></div>
<div class="topic-strip"><a href="/pokedex/">Pokédex <span>{len(DATA['dex'])} partners</span></a><a href="/moves/">Moves <span>{len(DATA['moves'])} definitions</span></a><a href="/move-evolutions/">Evolutions <span>59 conditions</span></a><a href="https://pokesurvivor.com/" class="play-topic">Play the developer’s game {icon('arrow',18)}</a></div></section>
<div class="home-content"><section class="home-section journey"><div class="section-heading"><h2>What’s stopping<br>your next run?</h2><p>Choose the problem. Find your next step.</p>{link('builds','Explore starter builds','text-link')}</div><div class="route-list">{routes}</div></section>
<section class="reference-home"><div class="reference-intro"><div class="reference-symbol">{icon('dex',38)}</div><h2>Meet the partners.<br>Know the numbers.</h2><p>Actual partner stats and type rules from the recorded game snapshot. Find a name, compare an opening, or check a difficult matchup.</p><div class="reference-types"><a href="/pokedex/?type=grass">{icon('grass',18)}Grass</a><a href="/pokedex/?type=fire">{icon('fire',18)}Fire</a><a href="/pokedex/?type=water">{icon('water',18)}Water</a></div>{link('pokedex','Open the full Pokédex','button')}</div><div class="reference-preview">{sample}<div class="database-links">{link('moves','Move patterns & base values')}{link('types','Type chart & matchup calculator')}{link('legendaries','Legendary encounters & roster')}</div></div></section>
<section class="home-section notebook"><div class="build-feature"><h2>A tier is a starting point.<br>Your build is the plan.</h2><p>Compare starting-stat profiles, then choose the move pattern and evolution route that suit your run. Our scoring method is published, so you can see what a ranking measures.</p><div class="actions">{link('tier-list','See the starter tier list','button secondary')}{link('builds','Plan a build','text-link')}</div></div><aside class="latest"><h3>Latest recorded game update</h3><p class="date">{E(DATA['changelog'][0]['date'])}</p><h4>{E(DATA['changelog'][0]['title'])}</h4><p>Account linking and co-op fixes from the source changelog.</p>{link('updates','Read the changes','text-link')}</aside></section>
<section class="trust-strip"><div>{icon('shield',25)}<p><strong>Checked against the source.</strong><span>Reference reviewed {REVIEWED}. Source inspection is separate from gameplay testing.</span></p></div>{link('about','Our sources & method','text-link')}</section>
<section class="identity"><div><h2>Different game, similar name?</h2><p>Pokémon Survivor Burst is a separate project. Identify your game before using a build or download guide.</p></div>{link('survivor-vs-burst','Compare the games','text-link')}</section></div>'''
    add('', 'Pokémon Survivor Wiki | PokéSurvivor Guides & Pokédex','An independent PokéSurvivor wiki: starter tier list, 966-partner Pokédex, 64 moves, evolution checker and mobile guides.',body,'Home')
    add('search','Search the PokéSurvivor Wiki','Search guides, Pokémon and moves in the PokéSurvivor Wiki.', '<p class="lead">Find a guide, a partner or a move.</p><form action="/search/" class="search-page"><label for="search-query">Search the Wiki</label><div><input id="search-query" type="search" name="q" maxlength="100" placeholder="Try Ember, Pikachu or mobile"><button class="button" type="submit">Search</button></div></form><p id="search-status" role="status" aria-live="polite"></p><ul id="search-results" class="search-results"></ul><noscript><p>Search needs JavaScript. Use the guide and database navigation to browse every topic.</p></noscript>','Search',index=False)


def render(slug,p):
    p={**p, 'body':media.enhance(slug,p['body'])}
    home_page=slug==''
    title=p['title']
    canonical=SITE+URL(slug)
    media_ids=media.USED.get(slug,[])
    social=''
    if media_ids:
        cover=media.BY_ID[media_ids[0]]
        image_path='/assets/media/'+cover['id']+('.svg' if cover['kind']=='diagram' else '-'+str(max(cover['variants']))+'.webp')
        if cover['kind']!='diagram':
            social=f'<meta property="og:image" content="{SITE+image_path}"><meta property="og:image:alt" content="{E(cover["alt"])}">'
    graph=[{'@type':'WebPage' if home_page else 'CollectionPage' if p['group']=='Database' else 'Article','@id':canonical+'#page','url':canonical,'name':title,'description':p['description'],'inLanguage':'en','dateModified':REVIEWED,'isPartOf':{'@id':SITE+'/#website'}}]
    if home_page: graph.append({'@type':'WebSite','@id':SITE+'/#website','url':SITE+'/','name':'Pokémon Survivor Wiki','alternateName':'PokéSurvivor Wiki','inLanguage':'en'})
    else: graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':SITE+'/'},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
    for ident in media.USED_VIDEOS.get(slug,[]):
        v=media.VIDEO_BY_ID[ident];poster=media.BY_ID[v['poster']]
        graph.append({'@type':'VideoObject','@id':canonical+'#video-'+ident,'name':v['title'],'description':v['description'],'thumbnailUrl':SITE+'/assets/media/'+v['poster']+'-'+str(max(poster['variants']))+'.webp','uploadDate':v['created'],'duration':f'PT{v["duration"]}S','contentUrl':SITE+'/assets/media/'+ident+'.webm','inLanguage':'en','isPartOf':{'@id':canonical+'#page'}})
    nav=''.join(f'<a {"aria-current=\"page\"" if slug==s else ""} href="{URL(s)}">{label}</a>' for s,label in [('how-to-play','Start here'),('tier-list','Tier list'),('pokedex','Pokédex'),('moves','Moves'),('move-evolutions','Evolutions'),('types','Types')])
    related=''
    if p['related']: related='<section class="related"><h2>Keep your run moving</h2><ul>'+''.join(f'<li>{link(s,PAGES[s]["title"])}</li>' for s in p['related'])+'</ul></section>'
    sources=''
    if p['sources']:
        src=''.join(f'<li><a href="{DATA["source"]["repository"]}/blob/{DATA["source"]["commit"]}/{E(s)}">{E(s)}</a></li>' for s in p['sources'])
        sources=f'<details class="sources"><summary>Sources & snapshot scope</summary><p>Reviewed {REVIEWED}. Mechanics and data refer to the local source snapshot <code>{DATA["source"]["commit"][:7]}</code>; later live changes may differ. Source inspection is separate from gameplay testing.</p><ul>{src}</ul></details>'
    toc=''
    import re
    headings=re.findall(r'<section class="article-section" id="([^"]+)"><h2>(.*?)</h2>',p['body'])
    if headings: toc='<details class="toc" open><summary>On this page</summary><nav aria-label="On this page">'+''.join(f'<a href="#{ident}">{text}</a>' for ident,text in headings)+'</nav></details>'
    content=p['body'] if home_page else f'<div class="breadcrumbs">{link("","Home")}<span>/</span>{E(p["group"])}</div><div class="article-heading"><h1>{E(title)}</h1><p class="date">Reference reviewed <time datetime="{REVIEWED}">{REVIEWED}</time></p></div><div class="article-layout"><article>{p["body"]}{related}{sources}</article><aside class="article-aside">{toc}<div class="aside-note"><strong>This game, this snapshot.</strong><p>These guides cover jpter78’s browser PokéSurvivor.</p>{link("survivor-vs-burst","Playing Burst instead?")}</div></aside></div>'
    dock = '<nav class="mobile-dock" aria-label="Quick navigation">' + ''.join(f'<a href="{URL(dest)}" {"aria-current=\"page\"" if slug==dest else ""}>{icon(glyph,21)}<span>{label}</span></a>' for dest,glyph,label in [('how-to-play','book','Guide'),('pokedex','dex','Pokédex'),('move-evolutions','evolve','Evolve'),('search','search','Search')]) + '</nav>'
    resource_links='<link rel="describedby" href="/llms.txt" type="text/plain">'
    if slug in agent_resources.READING_PATHS:
        resource_links += f'<link rel="alternate" href="{agent_resources.READING_PATHS[slug]}" type="text/markdown">'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(p['description'])}"><meta name="robots" content="{'index,follow,max-image-preview:large' if p['index'] else 'noindex,follow'}"><link rel="canonical" href="{canonical}">{resource_links}<meta name="theme-color" content="#f6f6ee"><meta property="og:type" content="website"><meta property="og:site_name" content="Pokémon Survivor Wiki"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(p['description'])}">{social}<meta name="twitter:card" content="{'summary_large_image' if social else 'summary'}"><link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48"><link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96"><link rel="icon" href="/assets/mark.svg" type="image/svg+xml" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180"><link rel="manifest" href="/site.webmanifest"><link rel="stylesheet" href="/assets/wiki.css"><script defer src="/assets/wiki.js"></script><script defer src="/assets/analytics.js"></script><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')}</script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="/" aria-label="Pokémon Survivor Wiki home"><img class="brand-mark" src="/assets/mark.svg" width="36" height="36" alt=""><span>Pokémon Survivor<span class="brand-sub">WIKI & GAME GUIDES</span></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button><nav id="site-nav" aria-label="Main navigation">{nav}</nav><a class="play-link" href="https://pokesurvivor.com/">Play game {icon("arrow",16)}</a><a class="search-link" href="/search/" aria-label="Search the Wiki"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg></a></header><main id="main" class="{'home' if home_page else 'document'}">{content}</main>{dock}
<footer class="site-footer"><div><a class="footer-brand" href="/">Pokémon Survivor Wiki</a><p>An independent reference for your next run.</p></div><nav aria-label="Footer">{link('about','About & sources')}{link('privacy','Privacy')}<button type="button" class="analytics-settings" data-analytics-settings>Analytics preferences</button>{link('download','Where to play')}{link('co-op','Co-op & account help')}{link('updates','Updates')}<a href="/llms.txt">Machine-readable guide</a><a href="/index.md">Markdown overview</a><a href="https://pokesurvivor.com/">Developer’s game</a></nav><p class="legal">Unofficial fan reference. Not affiliated with JPTER78, Nintendo, Creatures, GAME FREAK or The Pokémon Company. Pokémon belongs to its respective owners. Game data: JPTER78 / PokéSurvivor. <a href="/assets/LICENSE-game.txt">Code license</a> · <a href="/assets/OFL.txt">Font license</a>.</p></footer></body></html>'''


def build():
    # Do not recursively remove an output tree: overwrite only this builder's files.
    OUT.mkdir(parents=True,exist_ok=True)
    for p in CONTENT['pages']: prose(p)
    reference_pages()
    home()
    for slug,p in PAGES.items():
        dest=OUT/slug/'index.html'
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(render(slug,p),encoding='utf-8')
    assets=OUT/'assets'
    assets.mkdir(exist_ok=True)
    for f in (HERE/'public').iterdir():
        if f.is_file(): shutil.copyfile(f,assets/f.name)
        elif f.is_dir(): shutil.copytree(f,assets/f.name,dirs_exist_ok=True)
    media.export_manifest(assets/'media')
    for source, target in [("favicon.ico","favicon.ico"),("icon-96.png","favicon-96.png"),("apple-touch-icon.png","apple-touch-icon.png")]:
        shutil.copyfile(HERE/"public/icons"/source,OUT/target)
    shutil.copyfile(HERE/"public/site.webmanifest",OUT/"site.webmanifest")
    shutil.copyfile(ROOT/'assets/fonts/PixelifyPS-700.ttf',assets/'pixelify.ttf')
    shutil.copyfile(ROOT/'assets/fonts/OFL.txt',assets/'OFL.txt')
    shutil.copyfile(ROOT/'LICENSE',assets/'LICENSE-game.txt')
    (assets/'game.json').write_text(json.dumps(DATA,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    search=[dict(title=p['title'],url=URL(s),kind=p['group'],text=p['description']) for s,p in PAGES.items() if p['index']]
    search += [dict(title=p['name'],url='/pokedex/#p'+str(p['dex']),kind='Pokémon',text=' '.join(p['types'])) for p in DATA['dex']]
    search += [dict(title=m['name'],url='/moves/#'+m['id'],kind='Move',text=m['type']+' '+m['kind']) for m in DATA['moves']]
    (assets/'search.json').write_text(json.dumps(search,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',ns)
    image_ns='http://www.google.com/schemas/sitemap-image/1.1'
    ET.register_namespace('image',image_ns)
    tree=ET.Element('{'+ns+'}urlset')
    for slug,p in PAGES.items():
        if p['index']:
            el=ET.SubElement(tree,'{'+ns+'}url'); ET.SubElement(el,'{'+ns+'}loc').text=SITE+URL(slug); ET.SubElement(el,'{'+ns+'}lastmod').text=REVIEWED
            for ident in media.USED.get(slug,[]):
                m=media.BY_ID[ident]
                path='/assets/media/'+ident+('.svg' if m['kind']=='diagram' else '-'+str(max(m['variants']))+'.webp')
                img=ET.SubElement(el,'{'+image_ns+'}image');ET.SubElement(img,'{'+image_ns+'}loc').text=SITE+path
    ET.indent(tree, space='  ')
    ET.ElementTree(tree).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n',encoding='utf-8')
    (OUT/'CNAME').write_text('pokemonsurvivorwiki.com\n',encoding='utf-8')
    records=agent_resources.export(OUT,PAGES,REVIEWED,DATA['source']['commit'])
    (OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/*\n  Cache-Control: public, max-age=3600\n'+agent_resources.headers(records),encoding='utf-8')
    (OUT/'_redirects').write_text('# Hostname redirects are configured in Cloudflare Single and Bulk Redirect Rules.\n',encoding='utf-8')
    missing=dict(title='Page not found | Pokémon Survivor Wiki',description='This page could not be found. Browse the guides and databases.',body='<h1>That route ends here.</h1><p class="lead">The page you requested is missing. Start from the Wiki or search for the partner or move you need.</p>'+link('','Back to the Wiki','button'),group='Help',index=False,related=[],sources=[])
    # Render a standalone 404 without advertising it as an indexable route.
    page404=render('404',missing).replace('<h1>Page not found | Pokémon Survivor Wiki</h1>','<h1>Page not found</h1>').replace('<h1>That route ends here.</h1>','<h2>That route ends here.</h2>')
    (OUT/'404.html').write_text(page404,encoding='utf-8')
    manifest={URL(s):dict(title=p['title'],index=p['index'],modified=REVIEWED,sha256=hashlib.sha256((OUT/s/'index.html').read_bytes()).hexdigest()) for s,p in PAGES.items()}
    (OUT/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(PAGES)} pages and 404 into {OUT}; {sum(p["index"] for p in PAGES.values())} indexable URLs')


if __name__=='__main__': build()
