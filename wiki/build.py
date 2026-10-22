"""Dependency-free, deterministic static Wiki builder. Never writes game files."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import xml.etree.ElementTree as ET
import media
import agent_resources
import localization

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
CSS_VERSION = hashlib.sha256((HERE/'public/wiki.css').read_bytes()).hexdigest()[:10]
JS_VERSION = hashlib.sha256((HERE/'public/wiki.js').read_bytes()).hexdigest()[:10]
ANALYTICS_VERSION = hashlib.sha256((HERE/'public/analytics.js').read_bytes()).hexdigest()[:10]


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


def add(slug, title, description, body, group='Guides', related=None, sources=None, index=True,
        modified='2026-10-15', source_commit=None):
    PAGES[slug] = dict(title=title, description=description, body=body, group=group,
                       related=related or [], sources=sources or [], index=index,
                       modified=modified, source_commit=source_commit or DATA['source']['commit'])


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
    add(p['slug'], p['title'], p['description'], body, p['group'], p['related'], p['sources'],
        modified=p.get('modified', '2026-10-15'), source_commit=p.get('sourceCommit'))


def reference_pages():
    rows = [dict(id=f'p{p["dex"]}', types=p['types'], cells=[f'<span class="dex-no">{p["dex"]:03}</span>', f'<strong>{E(p["name"])}</strong>', badges(p['types']), p['hp'], p['spd'], f'{p["pa"]:.2f}×', f'{p["sa"]:.2f}×', p['df'], p['sd'], p['gen'], ('Starter / gacha' if p.get('starter') else 'Gacha') if p['gacha'] else 'Outside gacha pool']) for p in DATA['dex']]
    body = f'<p class="lead">Compare all {len(rows)} playable partners in the recorded source snapshot. The October 18 system separates Attack, Special Attack, Defense and Special Defense; these are PokéSurvivor values, not mainline battle stats.</p>'
    body += '<p>Search a name or number, or choose a type. Dual-type entries match either type. The collection column uses the game’s regional gacha eligibility, including eligible legendary and mythical partners. Starters are also offered at the beginning. A rift encounter is separate from adding a normal partner to your collection.</p>'
    body += table(['No.', 'Pokémon', 'Type', 'HP', 'Speed', 'Attack', 'Sp. Atk', 'Defense', 'Sp. Def', 'Gen', 'Collection'], rows, True, 'PokéSurvivor Pokémon stats')
    body += section('Collection filter reports','<p>Issue #209 reports an unexpected result when Type and Unowned filters are combined. Its cause and fix are not confirmed. If it repeats, record the selected type, ownership state and any other active filter without sharing account or save data.</p><p>Issue #210 currently provides only a title about a missing shiny and no reproducible body. This Wiki does not invent a recovery case from that title.</p>')
    add('pokedex', 'PokéSurvivor Pokédex: physical & special stats', 'Search 966 PokéSurvivor partners and compare HP, speed, Attack, Special Attack, Defense, Special Defense and acquisition.', body, 'Database', ['starters','tier-list','legendaries'], ['js/data/pokedex.js','js/systems/stats.js','js/systems/gacha.js'], modified='2026-10-19')
    rows = [dict(id=m['id'],types=[m['type']],cells=[f'<strong>{E(m["name"])}</strong>',badges([m['type']]), E(m['kind'].title()), E(m['category'].title() if m['category'] else 'Buff'), E(m['buffStat'] or '—'), E(m['damage'] if m['damage'] is not None else '—'), f'{m["cooldown"]:g}s' if m['cooldown'] else '—',m['maxLevel'], link('move-evolutions',m['evolution']['name']) if m['evolution'] else 'No evolution']) for m in DATA['moves']]
    body = f'<p class="lead">The October 19 reference contains {len(DATA["moves"])} moves and {sum(bool(m["evolution"]) for m in DATA["moves"])} move evolutions. Search by name, element, damage category or attack pattern, then check the required in-run card before planning a route.</p><div class="notice"><strong>Category and behavior are separate fields.</strong> Physical moves use Attack, special moves use Special Attack, and buffs deal no direct damage. A homing move is not automatically special. Toxic is special and Spikes is physical in this game; Nasty Plot raises Special Attack.</div><p>Damage and cooldown are level-one definition values after the source’s one-time melee adjustment and before partner multipliers or run upgrades. They are not complete DPS measurements: hit rate, duration and coverage differ between patterns.</p>'
    body += section('Eight new attack behaviors','<div class="pattern-grid"><article><strong>Homing</strong><span>Projectiles steer toward a target.</span></article><article><strong>Bounce</strong><span>Shots can jump between enemies.</span></article><article><strong>Charge</strong><span>A beam releases after a charge cue.</span></article><article><strong>Spin</strong><span>Repeated hits sweep around the player.</span></article><article><strong>Quake</strong><span>Ground waves advance in sequence.</span></article><article><strong>Vortex</strong><span>A field pulls targets toward its centre.</span></article><article><strong>Shove</strong><span>An area wave pushes ordinary enemies.</span></article><article><strong>Stun</strong><span>A warned zone damages and briefly stops targets.</span></article></div><p>These are source-backed behavior descriptions, not measured DPS comparisons.</p>')
    body += section('Newly learned and melee moves','<p>The October 19 update no longer switches to a newly learned move automatically; the currently active move stays selected until you switch. If an already active melee move repeatedly stops while targets are in range, that is a separate symptom. Player report #208 describes intermittent melee attacks, but its cause and fix are not confirmed.</p><p><a href="https://github.com/JPTER78/pokesurvivor/issues/208">Read player report #208</a>.</p>')
    body += section('Reported upgrade issues','<p>Player report #232, dated October 19, describes unexpected first-upgrade behavior for Energy Ball, Ice Shard and Draining Kiss, and compares Mist Ball with Confusion. This Wiki has not independently reproduced every case. Record the move level, evolution state, partner, mode and visible game version before comparing results.</p><p>Source-defined values describe the reviewed implementation; they are not a substitute for a controlled gameplay test. The report’s 4/15 estimate is not treated as a confirmed probability.</p><p><a href="https://github.com/JPTER78/pokesurvivor/issues/232">Read player report #232</a>.</p>', 'known-issues')
    body += section('From partner choice to a saved route','<ol class="steps"><li>Choose a partner you own or compare the 29 free starters.</li><li>Check which moves are legal for that partner and whether they scale from Attack or Special Attack.</li><li>Confirm the exact evolution card before spending level choices.</li><li>Build and share the route, then press Save in the official game and wait for cloud success before changing devices.</li></ol>')
    body += table(['Move','Type','Pattern','Category','Buff stat','Base damage','Cooldown','Max level','Evolution'],rows,True,'PokéSurvivor move definitions')
    add('moves','PokéSurvivor Moves & Evolutions: All 103 Moves','Search all 103 PokéSurvivor moves by type, behavior and physical/special category, including 38 October 19 additions and 97 evolution links.',body,'Database',['move-evolutions','builds','pokedex','types'],['js/data/moves.js','js/entities/player.js','js/systems/combat.js'],modified='2026-10-21')
    rows = [dict(id=m['id'],types=[m['type']],cells=[E(m['name']), badges([m['type']]),m['maxLevel'],E(m['evolution']['requirement']), f'<strong>{E(m["evolution"]["name"])}</strong>']) for m in DATA['moves'] if m['evolution']]
    options = ''.join(f'<option value="{E(m["id"])}">{E(m["name"])}</option>' for m in DATA['moves'])
    checker = f'''<div class="tool" data-evolution><h3>Check your next evolution</h3><p>Select what you have in this run. This checker does not access your game save.</p><div class="tool-inputs"><label>Move<select id="evo-move">{options}</select></label><label>Current level<input id="evo-level" type="number" min="1" max="5" value="1" required></label></div><label class="check"><input type="checkbox" id="evo-stat"> I have taken the required stat card in this run</label><output id="evo-result" aria-live="polite"></output><noscript><p>Enable JavaScript for the checker, or use the complete table below.</p></noscript></div>'''
    tracker = '''<div class="tool move-master" data-move-master><h3>Move Master checklist</h3><p>Track the 97 move evolutions completed in this browser. This is a Wiki checklist, not a game save, cloud record or official achievement.</p><div class="tool-inputs"><label>Search moves<input id="master-search" type="search" maxlength="60" placeholder="Move or evolution"></label><label>Show<select id="master-filter"><option value="all">All recipes</option><option value="open">Incomplete</option><option value="done">Completed</option></select></label></div><p id="master-count" role="status" aria-live="polite">Loading checklist…</p><div class="master-list" id="master-list"></div><div class="actions"><button class="button secondary" type="button" data-master-export>Export JSON</button><label class="button secondary master-import">Import JSON<input type="file" accept="application/json" data-master-import></label><button class="text-link danger" type="button" data-master-reset>Reset checklist</button></div><output id="master-status" aria-live="polite"></output><noscript><p>JavaScript is needed for the checklist. The complete static table remains below.</p></noscript></div>'''
    body = f'<p class="lead">This table tracks {len(rows)} move-evolution recipes in the October 21 reference. Max the move, take its required stat upgrade in the same run, then choose the golden evolution card. Meeting the conditions makes an evolution eligible; it does not automatically evolve the move.</p>' + checker + tracker
    body += section('What evolves: the move or the Pokémon?','<p>Here, “evolution” means upgrading an equipped move into its evolved attack during a run. It does not evolve the partner species. The partner remains the Pokémon you selected while the move changes after its maximum level, required stat card and golden-card choice are satisfied.</p>')
    body += section('If the golden card is missing','<ol class="steps"><li>Check the move is at its maximum level.</li><li>Check the exact prerequisite in the table; different moves need different stat cards.</li><li>Confirm you took that stat card in this run, rather than an unrelated permanent upgrade.</li><li>Keep leveling and look for the separate golden card. An already evolved move cannot evolve again.</li></ol><p>Eligibility adds the evolution to the possible offer pool; it does not force the next level-up to show it. Buffs have no evolution. Learning another move is different from evolving one you already have.</p>')
    body += table(['Move','Type','Required level','Required stat card','Evolves into'],rows,True,'Move evolution conditions')
    add('move-evolutions','PokéSurvivor Move Evolutions: 97 Recipes & Move Master','Look up all 97 move evolution recipes, check requirements and track completed evolutions locally with the Move Master checklist.',body,'Database',['builds','moves','how-to-play'],['js/data/moves.js','js/systems/levelup.js'],modified='2026-10-21')
    starters = DATA['starters']
    rows = [dict(types=p['types'],cells=[f'<strong>{E(p["name"])}</strong>',badges(p['types']),link('moves',MOVES[p['start']]['name']),E((MOVES[p['start']]['category'] or 'buff').title()),p['hp'],p['spd'],f'{p["pa"]:.2f}×',f'{p["sa"]:.2f}×',p['df'],p['sd'],E(MOVES[p['start']]['evolution']['requirement'])]) for p in starters]
    body = '<p class="lead">All 29 starter choices, with the starting attack and evolution prerequisite you need to plan your first run.</p><p>The personality quiz suggests a partner, but you can reject the suggestion and select another. Choose a move pattern you can position around, then use the table to plan its evolution. Partners of the same elemental type do not always share a starting move.</p>'
    body += section('Three ways to choose','<ul><li><strong>Prefer distance?</strong> Compare partners starting with Ember or Water Gun. Read the move patterns before committing.</li><li><strong>Want a different opening?</strong> Psyduck and Slowpoke start with Confusion, giving a Psychic option outside the regional starter trios.</li><li><strong>Planning an evolution?</strong> Piplup starts with Bubble and needs Sprint; a Water Gun opener needs Power instead.</li></ul><p>These are build considerations, not a claim that one choice always survives longest.</p>')
    body += table(['Partner','Type','Starting move','Category','HP','Speed','Attack','Sp. Atk','Defense','Sp. Def','Evolution stat'],rows,True,'Starting partners')
    add('starters','Best PokéSurvivor starters: all 29 starting options','Compare all 29 starters by opening move category, HP, speed, Attack, Special Attack and both defenses.',body,'Guides',['tier-list','builds','move-evolutions'],['js/data/starters.js','js/data/pokedex.js','js/data/moves.js'], modified='2026-10-19')

    def scenario_scores(roster):
        fields={'HP':lambda p:p['hp'],'Speed':lambda p:p['spd'],'Offense':lambda p:max(p['pa'],p['sa']),'Bulk':lambda p:(p['df']+p['sd'])/2}
        ranks={name:{p['dex']:100*sum(fn(q)<=fn(p) for q in roster)/len(roster) for p in roster} for name,fn in fields.items()}
        return {p['dex']:round(sum(ranks[name][p['dex']] for name in fields)/4,1) for p in roster}

    starter_scores=scenario_scores(starters)
    starter_order=sorted(starters,key=lambda p:(-starter_scores[p['dex']],p['dex']))
    starter_rows=[]
    for position,p in enumerate(starter_order):
        score=starter_scores[p['dex']]
        band='S' if position < 3 else 'A' if position < 9 else 'B' if position < 19 else 'C'
        starter_rows.append(dict(types=p['types'],cells=[f'<span class="rank rank-{band}">{band}</span>',f'<strong>{E(p["name"])}</strong>',badges(p['types']),f'{score:.1f}',p['hp'],p['spd'],f'{p["pa"]:.2f}×',f'{p["sa"]:.2f}×',p['df'],p['sd'], E(MOVES[p['start']]['name'])]))
    body = '<p class="lead">A transparent comparison of all 29 starting partners, including their opening move and weighted starting attributes.</p><div class="notice"><strong>Editorial starter recommendation.</strong> This score is useful for comparing openings, but it is not measured survival time, win rate or an official game tier.</div>'
    body += section('What the score measures','<p>For the 29 starters, each partner receives a percentile for HP, Speed, best offensive side (the higher of Attack and Special Attack), and balanced bulk (the mean of Defense and Special Defense). The displayed score is the equal-weight mean of those four percentiles. Bands use roster positions: S = top 3, A = next 6, B = next 10, C = remaining 10.</p><p>This reproducible profile is not an official formula or a win-rate claim. It still excludes move pattern, range, weather, upgrades and player skill.</p>')
    body += table(['Band','Partner','Type','Profile','HP','Speed','Attack','Sp. Atk','Defense','Sp. Def','Starting move'],starter_rows,True,'Starter four-dimension percentile bands')
    body += section('Turn the ranking into a decision','<p>Use the starter guide to find a move you can handle. Use the evolution checker to identify its required card, and test the route in your own runs. For a durable survival-time ranking, comparable repeated runs and recorded conditions would be needed; this site does not invent those results.</p>')
    add('starter-tier-list','PokéSurvivor Starter Tier List: All 29 Starters','Compare 29 starters with reproducible HP, speed, physical/special offense and defense percentiles.',body,'Guides',['tier-list','starters','builds'],['js/data/pokedex.js','js/data/starters.js','js/data/moves.js','js/systems/stats.js'],modified='2026-10-20')

    all_scores=scenario_scores(DATA['dex'])
    all_order=sorted(DATA['dex'],key=lambda p:(-all_scores[p['dex']],p['dex']))
    rows=[]
    for position,p in enumerate(all_order):
        band='S' if position < 97 else 'A' if position < 290 else 'B' if position < 580 else 'C'
        rows.append(dict(id=f'rank-p{p["dex"]}',types=p['types'],cells=[f'<span class="rank rank-{band}">{band}</span>',f'<span class="dex-no">{p["dex"]:03}</span> <strong>{E(p["name"])}</strong>',badges(p['types']),f'{all_scores[p["dex"]]:.1f}',p['hp'],p['spd'],f'{p["pa"]:.2f}×',f'{p["sa"]:.2f}×',p['df'],p['sd'],('Starter / gacha' if p.get('starter') else 'Gacha') if p['gacha'] else 'Outside gacha pool']))
    body='<p class="lead">Compare all 966 partners, then choose by what you own, physical or special offense, attack range and evolution route. This is the complete roster, not the separate list of 29 free starters or the 400-coin Starting Move selector.</p><div class="notice"><strong>Stat ranking, not a win-rate leaderboard.</strong> The list uses source attributes only. It does not claim that 966 partners were run-tested or that an S band guarantees a longer run.</div>'
    sample=[]
    for p in all_order[:8]:
        direction='special' if p['sa'] > p['pa'] else 'physical' if p['pa'] > p['sa'] else 'mixed'
        access='Regional gacha pool' if p.get('gacha') else 'Outside the current gacha pool'
        sample.append(f'<article><h3>{E(p["name"])} <span>#{p["dex"]:03}</span></h3><p>{badges(p["types"])} · {direction.title()} direction</p><p>{access}. A high profile score does not measure range, cooldown or run consistency.</p><p><a href="/moves/">Check legal move patterns</a> · <a href="/move-evolutions/">Check evolutions</a></p></article>')
    body+=section('Choose a strong partner for the run you have','<p>Start with access: if you need a free opening, use the 29-starter list. For an unlocked partner, decide whether its higher side is Attack or Special Attack, then check a move pattern you can control at the required range. These examples are source-data shortcuts, not recorded win-rate winners.</p><div class="recommendation-grid">'+''.join(sample)+'</div>')
    body+=section('How the full-roster profile works','<p>Each partner receives a roster percentile for HP, Speed, best offensive side (Attack or Special Attack) and balanced bulk (mean of both defenses). The Profile is their equal-weight mean. S is the top 10% (97 partners), A the next 20% (193), B the next 30% (290), and C the remaining 40% (386), so every band has a useful population.</p><p>Move category matters: a high physical Attack does not strengthen a special move. Range, cooldown, evolutions, weather, enemy type, upgrades, co-op and control can reverse a stat-only result.</p>')
    body+=table(['Band','Partner','Type','Profile','HP','Speed','Attack','Sp. Atk','Defense','Sp. Def','Collection'],rows,True,'All 966 partner four-dimension rankings')
    body+=section('Use a tier as the first filter','<ol class="steps"><li>Filter by a type that fits the enemy or weather you expect.</li><li>Open the move database and compare the partner’s available attack patterns.</li><li>Check the evolution requirement before committing upgrade cards.</li><li>Use the build planner to record a legal route, then judge it in your own runs.</li></ol>')
    body+=section('When the single-type bonus applies','<p>A single-type partner gets a 1.20× damage factor only when a damaging move matches that partner’s sole type. It is not a flat Attack increase. A Fire-only partner using Ember qualifies; the same partner using Tackle does not. Dual-type partners and buff moves do not receive this specific factor.</p>')
    add('tier-list','PokéSurvivor Tier List (2026): 966 Pokémon & Build Guide','Compare all 966 partners, then choose by unlock status, offense, range, legal moves and evolution route.',body,'Guides',['starter-tier-list','builds','moves','move-evolutions','types'],['js/data/pokedex.js','js/systems/stats.js'],modified='2026-10-21')
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
    body='<p class="lead">Verified developer changes through October 21, 2026, locked to source commit <code>40c51c1</code>. Source review, production deployment and live gameplay reproduction are recorded separately.</p>'
    newest='<p class="date">Game changelog: 2026-10-19</p><h3>Added</h3><ul><li>38 moves bring the reference to 103 moves and 97 move evolutions.</li><li>New behaviors include homing, bounce, charge, spin, quake, vortex, shove and stun.</li><li>Starting Move costs 400 coins once per partner; legal choices exclude buffs and always retain the default move.</li></ul><h3>Changed</h3><ul><li>Single-type partners deal 20% more damage only with matching damaging moves.</li><li>Learning a new move no longer switches the active slot automatically.</li><li>The 30-minute pending upload described by this historical revision was superseded by the October 21 manual Save behavior above.</li></ul><p><a href="https://github.com/JPTER78/pokesurvivor/blob/018e986f4c12f414dfa84193ee35b2959b1e325c/js/data/changelog.js">Read the historical October 19 source</a>.</p>'
    body+=section('38 new moves and Starting Move',newest,'update-2026-10-19')
    body+=section('October 21 Save revision protection and server relay','<h3>Save behavior</h3><ul><li>Normal progress stays local until the player presses Save; the game also uploads before a required update and before logout.</li><li>Pending, syncing, success, offline and local are distinct states. Successful uploads remain separated by at least 65 seconds.</li><li>Each new upload carries a revision. If an older device conflicts with a newer cloud revision, the client can read, merge and retry instead of blindly replacing it.</li><li>The earlier automatic 10-minute and 30-minute schedules are historical behavior.</li></ul><h3>Co-op relay</h3><ul><li>Accepted friends can be invited without an Online indicator; a room invitation expires after three minutes.</li><li>The published October 21 notes describe server relay when a direct connection fails. The client can remember peers that needed TURN during the current session.</li><li>A relayed room can show “Connected (via server)”. Published capability is not proof that every account, network or mid-run disconnect was tested here.</li></ul><p><a href="https://github.com/JPTER78/pokesurvivor/blob/40c51c178adb7af421a5c6db0f7b43c4492cc861/js/data/changelog.js">Read the locked October 21 source</a>.</p>', 'update-2026-10-21')
    body+=section('October 20 gameplay fixes','<ul><li>Guest Ominous Wind, Sand Tomb and Whirlpool now attract targets in co-op; guest Hex applies its extra damage.</li><li>The ten newer homing or bounce attacks keep their direction after evolution, and +1 projectile adds one.</li><li>Co-op level cards reopen if closed without a choice. Mobile Manual Aim was removed.</li></ul><p>These are official source/changelog statements. They are not presented as independent live reproduction on every device.</p>', 'update-2026-10-20')
    latest='<p class="date">Game changelog: 2026-10-18</p><h3>Added</h3><ul><li>Physical and special attacks now use separate Attack and Special Attack; both defenses are also separate.</li><li>Nasty Plot raises Special Attack, while Swords Dance and Dragon Dance raise physical Attack.</li><li>Controller support, optional manual aim, a pause-screen run summary and an immediate Save button were added.</li></ul><h3>Historical note</h3><ul><li>This revision described automatic cloud saves every 10 minutes. October 19 changed that to 30 minutes, and October 21 replaced ordinary automatic upload with explicit Save.</li><li>Mobile Manual Aim was removed in the October 20 source.</li></ul>'
    body+=section('Physical/special, controller and Save',latest,'update-2026-10-18')
    for entry in DATA['changelog'][:8]:
        if entry['date'] in ('2026-10-21','2026-10-20','2026-10-19','2026-10-18'): continue
        text=f'<p class="date">Game changelog: {E(entry["date"])}</p>'
        for key,label in [('new','Added'),('changed','Changed'),('fixed','Fixed')]:
            if entry[key]: text+=f'<h3>{label}</h3><ul>'+''.join(f'<li>{E(x)}</li>' for x in entry[key])+'</ul>'
        body+=section(entry['title'],text, 'update-'+entry['date'])
    add('updates','PokéSurvivor October 21 Update: Save Revisions & Server Relay','Read the verified October 21 source review: cloud-save revision protection, published server relay, manual Save and gameplay fixes.',body,'Guides',['moves','builds','move-evolutions','mobile','co-op','save-recovery'],['js/data/changelog.js','js/data/moves.js','js/core/db.js','js/net/net.js','js/net/social.js'],modified='2026-10-21')

    body='<p class="lead">At 30:00 in the official browser game, Arceus moves the run to the Ruins of Judgment. Arceus is invincible: the goal is to dodge, survive and defeat the legendary reinforcements needed for the achievements.</p><div class="notice"><strong>October 18 rules.</strong> This guide is locked to commit <code>b8e843f</code>. A contact hit becomes lethal around total run minute 40 as pressure scales; the game does not automatically end at a fixed 40:00.</div>'
    body+=section('When the Judgment starts','<div class="judgment-timeline" role="img" aria-label="Timeline: new rifts stop at 28 minutes and Judgment of Arceus begins at 30 minutes"><div><strong>28:00</strong><span>No new rifts open</span></div><div><strong>30:00</strong><span>Ruins of Judgment begins</span></div><div><strong>+5 sec</strong><span>Legendary reinforcements continue</span></div></div><p>The October 13 official changelog says new rifts stop from minute 28 so the Judgment cannot begin while you are inside one. At minute 30 Arceus descends and moves the run to the Ruins.</p>')
    body+=section('What changes in the Ruins','<p>Arceus cannot be defeated in the official browser build. Movement speed has a soft cap, so excess speed contributes much less; legendary reinforcements run nearly as fast as the player. Poison remains percentage-based but scales down against their extremely large HP.</p>')
    body+=section('30–40 minute pressure curve','<div class="judgment-timeline" role="img" aria-label="Arceus pressure: Judgment begins at 30 minutes, acceleration increases around 35 minutes, contact damage scales around 37 minutes, and can knock out in one hit around 40 minutes"><div><strong>30:00</strong><span>Judgment begins</span></div><div><strong>~35:00</strong><span>Arceus accelerates continuously</span></div><div><strong>~37:00</strong><span>Contact damage keeps rising</span></div><div><strong>~40:00</strong><span>Contact can cause a one-hit KO</span></div></div><p>The last three marks convert five and seven minutes of Judgment to total run time. “Around 40” describes the contact-damage curve, not a fixed timer that ends every run.</p>')
    body+=section('Read the four attack warnings','<div class="attack-grid"><article><strong>Pillars</strong><span>Leave marked impact zones.</span></article><article><strong>Beams</strong><span>Cross the lane before it closes.</span></article><article><strong>Shockwaves</strong><span>Keep space to read expanding danger.</span></article><article><strong>Contact</strong><span>Do not let the invincible pursuer pin your route.</span></article></div><p>The official changelog confirms pillars, beams, shockwaves and severe contact damage. These diagrams explain movement choices; they are not game screenshots and do not invent exact frame timings.</p>')
    body+=section('Legendary reinforcement timeline','<p>A legendary joins about every five seconds, and each new reinforcement is described as having twice the HP and damage of the previous one. The useful decision is to keep a clear movement lane while focusing enough damage to finish three reinforcements in one run for Divine challenge.</p>')
    body+=section('The three achievements','<div class="achievement-grid"><article><strong>The Judgment</strong><span>Reach minute 30.</span></article><article><strong>Before the Creator</strong><span>Survive 60 seconds against Arceus.</span></article><article><strong>Divine challenge</strong><span>Defeat three reinforcement legendaries in one run.</span></article></div><p>Achievement conditions are verified from the developer changelog. This page does not list a reward until the current achievement data is separately verified.</p>')
    body+=section('Survival approach','<ol class="steps"><li>Finish rift decisions before 28:00 and protect an open movement lane.</li><li>Enter 30:00 with movement and cooldown improvements that help you reposition without stopping.</li><li>React to the warning area first; damage comes after avoiding Arceus and the next telegraphed attack.</li><li>For Divine challenge, focus one reinforcement at a time without letting Arceus close the escape route.</li></ol><p>This is a source-derived approach, not a claimed first-person 60-second clear.</p>')
    body+=section('Solo, co-op and Android ports','<p>The official changelog defines the browser version. Co-op positioning and connection quality can change how easy warnings are to read; the source does not justify claiming a separate co-op spawn schedule here. A third-party Android port or Pokémon Survivor Burst is a different build and may contain a defeatable Arceus or another mode.</p>')
    body+=section('Arceus FAQ','<h3>Can you defeat Arceus?</h3><p>Not in the verified official browser build; Arceus is invincible.</p><h3>Does Judgment begin at 30 minutes?</h3><p>Yes. New rifts stop at 28:00 and Judgment starts at 30:00.</p><h3>What should I prepare?</h3><p>Prioritize controllable movement, clear lanes and a legal evolved build before minute 30. Use the build, move-evolution and type tools for the parts this page can verify.</p>')
    add('arceus-judgment','PokéSurvivor Arceus Guide: 30–40 Minute Judgment Timeline','Survive Judgment of Arceus with the verified speed cap, poison scaling, acceleration and contact-damage timeline.',body,'Guides',['updates','legendaries','builds','co-op','moves','move-evolutions','types'],['js/data/changelog.js','js/systems/judgment.js','js/data/achievements.js'],modified='2026-10-19',source_commit='b8e843ffb8b07b95020fb77c4e9aca007d9a1e8d')

    upgrades=[(u['name'],u['unit'],u['max'],u['base'],u['grow']) for u in DATA['upgrades']]
    upgrade_rows=[]
    for name,effect,maximum,base,growth in upgrades:
        costs=[round(base*(growth**level)/10)*10 for level in range(maximum)]
        upgrade_rows.append([E(name),E(effect),maximum,base,' · '.join(str(c) for c in costs)])
    body='<p class="lead">Permanent upgrades are bought per partner. Starting Move costs 400 coins once and then lets that partner choose a supported non-buff opening attack. Repertoire is a different 1,500-coin upgrade that starts a run with two moves.</p>'
    body+=section('How upgrade prices scale','<p>The next level costs <code>round(base × growth^current level / 10) × 10</code> coins. The price row lists level purchases from the first level through the cap. Values are per partner, so plan the Pokémon you use before spending.</p>')
    body+=table(['Upgrade','Effect per level','Max','First cost','All level costs'],upgrade_rows,kind='Permanent upgrade definitions and prices')
    body+=section('Starting Move versus Repertoire','<p>Before Starting Move is purchased, the partner uses its default opening. After purchase, the legal selector contains non-buff moves from that partner’s learnable pool plus its default move, even when the default is outside its usual types. Psyduck can therefore return to Confusion. Nasty Plot and Swords Dance may be learned in a run but are not legal selected starting moves.</p>')
    body+=section('Priority without invented win rates','<p>Movement and cooldown improve control and consistency; Strength and Critical Hit improve damage; Reroll and Ban improve card choice. The best order depends on the partner, build and player, so this page does not claim a universal measured survival ranking.</p>')
    add('upgrades','PokéSurvivor Upgrades: Starting Move, Costs & Caps','Compare every permanent PokéSurvivor upgrade, including the 400-coin Starting Move and 1,500-coin Repertoire, with exact caps and costs.',body,'Database',['builds','moves','arceus-judgment'],['js/data/upgrades.js','js/data/starters.js'],modified='2026-10-19')

    calc='<div class="tool" data-gacha><h3>Gacha probability calculator</h3><p>Enter future pulls and your current banner pity. Each regional banner tracks its own pity.</p><div class="tool-inputs"><label>Future pulls<input id="gacha-pulls" type="number" min="1" max="1000" value="10"></label><label>Current pity<input id="gacha-pity" type="number" min="0" max="69" value="0"></label></div><output id="gacha-result" aria-live="polite"></output><noscript><p>Base five-star rate is 1.5%, shiny chance is 1%, and pity guarantees a five-star at 70 pulls.</p></noscript></div>'
    body='<p class="lead">PokéSurvivor regional banners use rarity weights of 45%, 30%, 17%, 6.5% and 1.5%. A ten-pull guarantees at least rarity 4 on its final slot if the first nine did not produce one, and a banner-specific pity guarantees rarity 5 at 70.</p>'+calc
    body+=section('Rules the calculator uses','<ul><li>Five-star base chance: 1.5% per ordinary pull.</li><li>Shiny chance: 1 in 100 when the selected Pokémon has a shiny sprite.</li><li>Pity is stored separately for each of nine regional banners and resets on a rarity-5 result.</li><li>Ten-pull protection affects the last slot if no rarity-4-or-5 result appeared earlier.</li><li>A repeated shiny is replaced by a missing shiny of the same rarity when one exists; otherwise the result becomes normal.</li></ul><p>The summary reports simple base chances plus whether the entered pull window reaches hard pity. It does not simulate a specific banner pool or promise a particular Pokémon.</p>')
    add('gacha-calculator','PokéSurvivor Gacha Calculator: Rates, Pity & Shiny Odds','Calculate PokéSurvivor base five-star and shiny odds, check the 70-pull banner pity and understand ten-pull protection.',body,'Tools',['pokedex','upgrades','shiny-guide' if 'shiny-guide' in PAGES else 'updates'],['js/systems/gacha.js'],modified='2026-10-17',source_commit='5bbc3b29288d6af4596f21188fb8b54e0e9b739f')


def new_system_pages():
    partner_options=''.join(f'<option value="{p["dex"]}">{E(p["name"])}</option>' for p in DATA['dex'])
    tm_options=''.join(f'<option value="{t["id"]}">{E(t["name"])}</option>' for t in DATA['tms'])
    nature_options=''.join(f'<option value="{n["id"]}">{E(n["names"]["en"])}</option>' for n in DATA['natures'])

    shop_tool=f'''<div class="tool" data-shop-preview><h3>Rule-based daily TM preview</h3><p>Choose a partner to model the reviewed shop rule. This uses the Europe/Madrid calendar date and the recorded source snapshot; it does not read an account or connect to the official shop.</p><div class="tool-inputs"><label>Partner<select id="shop-partner">{partner_options}</select></label></div><output id="shop-result" aria-live="polite">Loading the source-backed preview…</output><ul id="shop-tms" class="tool-results"></ul><noscript><p>The preview needs JavaScript. The fixed prices and shop rules remain below.</p></noscript></div>'''
    shop_rows=[[E('Mint'), '1,500', 'Choose a nature for one owned partner'],[E('Regular Ability Capsule'), '1,500', 'Choose another legal regular slot'],[E('Hidden Ability Capsule'), '5,000', 'Choose another legal slot, including hidden when available']]
    body='<p class="lead">The Kecleon Shop uses in-game coins inside JPTER78’s browser game. A Mint and regular Ability Capsule each cost 1,500 coins; a Hidden Ability Capsule costs 5,000. TM prices depend on the move.</p>'+shop_tool
    body+=section('How the eight daily TMs are selected','<p>The base list contains eight TMs generated from the calendar date in <code>Europe/Madrid</code>. If none can currently be taught to the selected partner, the eighth offer can be replaced with a compatible move. Natural moves and TMs already taught are excluded from that compatibility decision, so a partner-specific result can differ from the shared base list.</p><p>The preview below uses an empty “already taught” assumption. Check the official game before spending coins; this Wiki does not inspect inventory, coins or a live shop.</p>')
    body+=table(['Item','Price in coins','Use'],shop_rows,kind='Kecleon Shop fixed item prices')
    body+=section('Buy, then use from the collection','<ol class="steps"><li>Open the Shop from the official game menu.</li><li>Check the selected partner and whether the item has a legal effect.</li><li>Buy with in-game coins. The item or TM enters the Bag.</li><li>Open that partner in the collection and use the item there.</li><li>For a TM, confirm the move is compatible, is not already natural and has not already been taught.</li></ol><p>These are game resources, not payments to this Wiki.</p>')
    add('kecleon-shop','PokéSurvivor Kecleon Shop: Mints, Capsules & Daily TMs','Check PokéSurvivor Kecleon Shop prices, the Europe/Madrid daily TM rule, partner-specific replacement and safe item use.',body,'Guides',['tm-compatibility','natures','abilities','builds'],['js/data/shop.js','js/systems/mons.js','js/data/tms.js'],modified='2026-10-22')

    tm_tool=f'''<div class="tool" data-tm-checker><h3>TM compatibility checker</h3><p>Select a partner and TM. “Already taught” is an optional local planning assumption and is never read from a game account.</p><div class="tool-inputs"><label>Partner<select id="tm-partner">{partner_options}</select></label><label>TM<select id="tm-move">{tm_options}</select></label><label class="check"><input id="tm-taught" type="checkbox"> Model this TM as already taught</label></div><output id="tm-result" aria-live="polite">Loading compatibility data…</output><div class="actions"><button class="button" id="tm-share" type="button">Copy share link</button></div><noscript><p>JavaScript is needed for the checker. Use the source-backed table below.</p></noscript></div>'''
    tm_rows=[]
    for t in DATA['tms']:
        tm_rows.append(dict(id='tm-'+t['id'],cells=[f'<strong>{E(t["name"])}</strong>',f'{t["price"]:,}',str(len(t['compatibleDex']))]))
    body='<p class="lead">Check both directions: which TMs a partner can learn, and which playable partners can learn a selected TM. Compatibility does not mean owned, taught or naturally available.</p>'+tm_tool
    body+=section('Five states that must stay separate','<ul><li><strong>Natural:</strong> the move is already in the partner’s normal pool and does not need a TM.</li><li><strong>Compatible:</strong> the current source maps the TM to that playable partner, but the item still must be obtained.</li><li><strong>In the Bag:</strong> the account owns an unused copy; this Wiki cannot see that inventory.</li><li><strong>Taught:</strong> one copy was consumed and the move became part of that partner’s learned pool.</li><li><strong>Incompatible:</strong> the reviewed game mapping does not allow that pair.</li></ul><p>Mewtwo → Shadow Ball is a supported example. Psyduck → Flamethrower is not compatible in this snapshot. Main-series learnsets are not substituted for the game’s mapping.</p>')
    body+=table(['TM','Shop price','Compatible playable partners'],tm_rows,True,'PokéSurvivor TM reference')
    add('tm-compatibility','PokéSurvivor TM Compatibility Checker','Check PokéSurvivor TM compatibility by partner or move, distinguish natural, compatible, taught and incompatible states, and share a local planning link.',body,'Tools',['kecleon-shop','moves','builds','pokedex'],['js/data/tms.js','js/systems/mons.js','js/data/moves.js'],modified='2026-10-22')

    nature_tool=f'''<div class="tool" data-nature-calculator><h3>Nature stat calculator</h3><p>Choose a partner and nature. The result is a comparison assumption, not a claim that the Wiki detected your account’s nature.</p><div class="tool-inputs"><label>Partner<select id="nature-partner">{partner_options}</select></label><label>Nature<select id="nature-choice">{nature_options}</select></label></div><output id="nature-result" aria-live="polite">Loading nature data…</output><noscript><p>JavaScript is needed for the calculator. Use the complete table below.</p></noscript></div>'''
    stat={'pa':'Attack','sa':'Special Attack','df':'Defense','sd':'Special Defense','spd':'Speed'}
    nature_rows=[]
    for n in DATA['natures']:
        effect='Neutral' if n['neutral'] else f'+10% {stat[n["up"]]} / −10% {stat[n["down"]]}'
        nature_rows.append([f'<strong>{E(n["names"]["en"])}</strong><br><small>{E(n["names"]["es"])} · {E(n["names"]["it"])} · {E(n["names"]["zh-hant"])}</small>',E(effect),'HP unchanged'])
    body='<p class="lead">All 25 PokéSurvivor natures are listed here: 20 raise one combat stat by 10% and lower another by 10%, while five are neutral. HP never changes.</p>'+nature_tool
    body+=section('How nature assignment works','<p>A partner’s initial nature is fixed from the account creation seed and Pokédex number. Repeating a pull does not independently reroll it. A Mint lets the player choose another nature for that owned partner. The calculator changes a copy of the displayed base values only; it does not alter the Pokédex dataset or a game save.</p>')
    body+=table(['Nature and aliases','Effect','HP'],nature_rows,True,'All 25 PokéSurvivor natures')
    add('natures','PokéSurvivor Natures: 25 Effects & Mint Guide','Compare all 25 PokéSurvivor natures, the five neutral options, exact 10% stat effects and a source-backed partner calculator.',body,'Database',['kecleon-shop','abilities','builds','pokedex'],['js/data/natures.js','js/systems/mons.js'],modified='2026-10-22')

    ability_tool=f'''<div class="tool" data-ability-checker><h3>Partner ability slots</h3><p>Select a partner to see its regular and hidden slots in this snapshot. The Wiki does not detect the ability assigned to your account.</p><div class="tool-inputs"><label>Partner<select id="ability-partner">{partner_options}</select></label></div><output id="ability-result" aria-live="polite">Loading ability slots…</output><noscript><p>JavaScript is needed for the slot checker. The ability reference remains below.</p></noscript></div>'''
    ability_rows=[]
    for a in DATA['abilities']:
        ability_rows.append(dict(id='ability-'+a['id'],cells=[f'<strong>{E(a["names"]["en"])}</strong><br><small>{E(a["names"]["es"])} · {E(a["names"]["it"])} · {E(a["names"]["zh-hant"])}</small>',E('Specialized effect' if a['effectType']=='specialized' else 'Primary-type fallback'),E(a['effect'])]))
    body='<p class="lead">This reference uses PokéSurvivor’s own ability implementation. It does not copy main-series effects into mechanics the browser game does not implement.</p>'+ability_tool
    body+=section('Regular and hidden capsules','<p>A regular Ability Capsule can select another legal regular slot. A Hidden Ability Capsule may also select a legal hidden slot. A partner with one regular slot, duplicated slots or no hidden slot may have fewer valid choices, and selecting the current slot is not a change. Initial nature and ability assignment is fixed for an account and partner; the documented 1-in-20 hidden chance applies only when a hidden slot exists.</p>')
    body+=section('Specialized effect or fallback','<p>Abilities with a dedicated implementation use that effect. Huge Power, for example, gives +50% damage to physical moves in this game; it is not described as doubling Attack. An ability without a dedicated effect uses the current fallback: +8% damage for moves matching the partner’s primary type.</p>')
    body+=table(['Ability and aliases','Implementation','Effect in PokéSurvivor'],ability_rows,True,'PokéSurvivor ability effects')
    add('abilities','PokéSurvivor Abilities: Regular & Hidden Effects','Find regular and hidden PokéSurvivor ability slots, distinguish specialized effects from the 8% primary-type fallback, and check capsule limits.',body,'Database',['kecleon-shop','natures','builds','pokedex'],['js/data/abilities.js','js/data/ability-fx.js','js/systems/mons.js'],modified='2026-10-22')


def enhance_content_pages():
    starter_options=''.join(f'<option value="{p["dex"]}">{E(p["name"])}</option>' for p in DATA['starters'])
    move_options=''.join(f'<option value="{m["id"]}">{E(m["name"])}</option>' for m in DATA['moves'])
    planner=f'''<div class="tool build-planner" data-build-planner><h3>Starting move & build planner</h3><p>Model the default opening, the first 400-coin selector, Repertoire, and the separate 400-coin second selector. Optional taught TMs are a local assumption; this tool never reads or changes an account.</p><div class="tool-inputs"><label>Partner<select id="build-starter">{starter_options}</select></label><label class="check"><input id="build-start-owned" type="checkbox"> First Starting Move selector purchased</label><label>Selected first move<select id="build-starting">{move_options}</select></label><label class="check"><input id="build-repertoire" type="checkbox"> Repertoire purchased (1,500 coins)</label><label class="check"><input id="build-second-owned" type="checkbox"> Second Starting Move selector purchased (400 coins)</label><label>Second move<select id="build-secondary">{move_options}</select></label><label>Taught TM assumption<select id="build-tm"><option value="">None</option>{move_options}</select></label></div><output id="build-result" aria-live="polite">Loading build data…</output><div class="actions"><button class="button" id="build-share" type="button">Copy share link</button><a class="text-link" href="/tm-compatibility/">Check TM compatibility</a><a class="text-link" href="/move-evolutions/">Check every evolution</a></div><noscript><p>The planner needs JavaScript. Use the route notes and evolution table below.</p></noscript></div>'''
    PAGES['builds']['body']=PAGES['builds']['body'].replace('</p>','</p>'+planner,1)
    PAGES['builds']['body']+=section('Two selectors, Repertoire and taught TMs','<ul><li><strong>First selector:</strong> 400 coins per partner; choose the first legal non-buff opening.</li><li><strong>Repertoire:</strong> 1,500 coins per partner; starts with two moves, with the second random until its selector is unlocked.</li><li><strong>Second selector:</strong> another 400 coins and requires Repertoire. A partner starting from neither unlock needs 1,900 coins to choose only the second move, or 2,300 coins to choose both.</li><li><strong>Taught TM:</strong> a compatible TM becomes part of the legal pool only after it has been taught in the game. The planner’s checkbox is a local assumption.</li><li><strong>Validation:</strong> the second move cannot duplicate the first; buffs remain excluded. The partner’s special default exception remains available.</li></ul><p>Old shared links using <code>p</code> and <code>m</code> still open. V8 links add versioned fields only when new choices are modelled.</p>')
    PAGES['builds']['related']=['tm-compatibility','kecleon-shop','natures','abilities','moves','move-evolutions','starter-tier-list']
    PAGES['builds']['title']='PokéSurvivor Builds: Starting Moves & Upgrade Routes'
    PAGES['builds']['description']='Plan a legal PokéSurvivor route with the default opening, 400-coin Starting Move choice, Repertoire second move, evolutions and conditional single-type bonus.'
    PAGES['builds']['modified']='2026-10-22'
    PAGES['builds']['source_commit']=DATA['source']['commit']
    diagnostic='''<div class="tool save-diagnostic" data-save-diagnostic><h3>Build a privacy-safe recovery report</h3><p>Choose only non-sensitive facts. This tool runs in your browser and does not inspect or upload a save.</p><div class="tool-inputs"><label>Device handoff<select id="save-game"><option value="ipad-pc">iPad Safari → PC Chrome</option><option value="android-pc">Android → PC</option><option value="other">Other devices</option><option value="unknown">Unknown</option></select></label><label>Account state<select id="save-login"><option value="linked">Google or linked account</option><option value="password">Username/password; linkage unknown</option><option value="other">Other account type</option><option value="unknown">Unknown</option></select></label><label>Original device still has complete progress<select id="save-copy"><option value="yes">Yes</option><option value="no">No</option><option value="unknown">Unknown</option></select></label><label>Original device save state<select id="save-state"><option value="local">Saved locally</option><option value="pending">Pending upload</option><option value="syncing">Syncing</option><option value="success">Cloud save successful</option><option value="offline">Offline</option><option value="unknown">Unknown</option></select></label><label>Second device shows the same collection<select id="save-second"><option value="yes">Yes</option><option value="no">No</option><option value="unknown">Unknown</option></select></label><label>Difference appeared<select id="save-timing"><option value="before">Before pressing Save</option><option value="after">After pressing Save</option><option value="unknown">Unknown</option></select></label></div><div class="actions"><button class="button" type="button" data-diagnostic-run>Show safest next step</button></div><output id="save-result" aria-live="polite">Select what you know, then run the checklist.</output><label class="report-label" for="save-report">Non-sensitive report</label><textarea id="save-report" rows="9" readonly></textarea><button class="button secondary" type="button" data-report-copy disabled>Copy report</button><noscript><p>JavaScript is required for the decision helper. Use the safety table above without entering private information.</p></noscript></div>'''
    PAGES['save-recovery']['body']=PAGES['save-recovery']['body'].replace('</p>','</p>'+diagnostic,1)
    coop='''<div class="tool coop-diagnostic" data-coop-diagnostic><h3>Build a privacy-safe co-op checklist</h3><p>Choose only non-sensitive categories. This tool does not inspect your network, contact the game server or read an account.</p><div class="tool-inputs"><label>Where the game is open<select id="coop-site"><option value="official">Official game opened directly</option><option value="embedded">Inside another site or copied version</option><option value="unknown">Not sure</option></select></label><label>Stage that failed<select id="coop-stage"><option value="friend">Friend or invitation is missing</option><option value="connecting">Connecting / Reconnecting / Could not connect</option><option value="boss">Already playing: boss missing after a rift</option><option value="move">A move behaves unexpectedly</option></select></label><label>Network comparison<select id="coop-network"><option value="unknown">Not checked / not sure</option><option value="same">Players are on the same network</option><option value="different">Players are on different networks</option></select></label></div><div class="actions"><button class="button" type="button" data-coop-run>Show safe checks</button></div><output id="coop-result" aria-live="polite">Select the failed stage, then run the checklist.</output><label class="report-label" for="coop-report">Non-sensitive checklist</label><textarea id="coop-report" rows="7" readonly></textarea><button class="button secondary" type="button" data-coop-copy disabled>Copy checklist</button><noscript><p>Use the four-stage table below: friendship, room invitation, peer connection and running game. Open the official site directly, keep the host active, preserve site data and report only non-sensitive facts.</p></noscript></div>'''
    PAGES['co-op']['body']=PAGES['co-op']['body'].replace('</p>','</p>'+coop,1)
    PAGES['download']['body']=PAGES['download']['body'].replace('</p>','</p><p><a class="button" href="https://pokesurvivor.com/" rel="noopener">Play the official browser game</a></p>',1)
    PAGES['mobile']['body']+=section('Current collection systems on mobile','<p>The October 21 game update adds the Kecleon Shop, partner natures, abilities and TMs. Use the collection screen to apply a Mint, capsule or compatible TM. The Wiki tools remain local and do not inspect the game account.</p><p><a href="/kecleon-shop/">Read the Shop rules</a> · <a href="/tm-compatibility/">Check TM compatibility</a></p>')
    PAGES['mobile']['modified']='2026-10-22'; PAGES['mobile']['source_commit']=DATA['source']['commit']
    PAGES['upgrades']['body']+=section('Second Starting Move selector','<p>Repertoire costs 1,500 coins and enables a second opening move. The separate Second Starting Move selector costs 400 coins per partner and requires Repertoire. It chooses that second move instead of leaving it random. Selecting the first opening is still its own 400-coin upgrade.</p>')
    PAGES['upgrades']['related']=['builds','tm-compatibility','moves','arceus-judgment']; PAGES['upgrades']['modified']='2026-10-22'; PAGES['upgrades']['source_commit']=DATA['source']['commit']
    PAGES['co-op']['body']+=section('Spectate a living teammate after falling','<p>After your partner falls in co-op, switch the camera among teammates who are still active with the on-screen buttons, Q/E on keyboard, or LB/RB on a controller. This changes only the view: it does not control a teammate or revive the fallen partner.</p><p>Player report #278 describes a different symptom—a run ending for one player after several minutes. Its cause is not confirmed, so record the visible version, host/join role and approximate time separately from spectating.</p>')
    PAGES['co-op']['modified']='2026-10-22'; PAGES['co-op']['source_commit']=DATA['source']['commit']
    PAGES['save-recovery']['body']+=section('Current evidence: cross-device report #275','<p>Player report #275 describes the same Google login on another device not showing the expected collection while the original device still retained progress. It is a player report, not proof of one universal cause. Preserve the original browser profile, distinguish local/pending/syncing/cloud-success states, and avoid uploading an older copy while collecting non-sensitive facts.</p>')
    PAGES['save-recovery']['modified']='2026-10-22'; PAGES['save-recovery']['source_commit']=DATA['source']['commit']
    PAGES['arceus-judgment']['body']+=section('Arceus speed report #281','<p>Issue #281 reports an Arceus speed or ranking concern and also proposes future features. The speed symptom is not independently reproduced here and must be compared with the existing soft-cap behavior before naming a cause. Suggestions such as a 12-move limit, Mega forms or DLC are requests, not current game rules.</p>')
    PAGES['arceus-judgment']['modified']='2026-10-22'; PAGES['arceus-judgment']['source_commit']=DATA['source']['commit']
    PAGES['updates']['body']+=section('October 21 systems update','<p>Official source commit <code>ce57853</code> adds the Kecleon Shop, Mints, regular and hidden Ability Capsules, eight daily TMs, partner natures and abilities, TM teaching, the Second Starting Move selector and co-op spectating after a partner falls. The changelog is dated October 21; the commit reached the reviewed repository at 2026-10-22 01:38 Beijing time.</p><p><a href="/kecleon-shop/">Shop guide</a> · <a href="/tm-compatibility/">TM checker</a> · <a href="/natures/">Nature reference</a> · <a href="/abilities/">Ability reference</a></p>')
    PAGES['updates']['body']=PAGES['updates']['body'].replace('Verified developer changes through October 21, 2026, locked to source commit <code>40c51c1</code>.','Verified developer changes reviewed October 22, 2026, locked to source commit <code>ce57853</code>.')
    PAGES['updates']['title']='PokéSurvivor October 22 Review: Shop, TMs & Abilities'
    PAGES['updates']['description']='Read the October 22 source review covering Kecleon Shop prices, daily TMs, natures, abilities, second starting moves, Save revisions and co-op spectating.'
    PAGES['updates']['related']=['kecleon-shop','tm-compatibility','natures','abilities','builds','co-op','save-recovery']
    PAGES['updates']['modified']='2026-10-22'; PAGES['updates']['source_commit']=DATA['source']['commit']


def home():
    starters = [next(p for p in DATA['starters'] if p['dex']==n) for n in (4,1,7)]
    initial = starters[0]
    move = MOVES[initial['start']]
    choices = ''.join(f'<label class="starter-choice"><input type="radio" name="opening-partner" value="{p["dex"]}" {"checked" if i==0 else ""}><span>{icon(p["types"][0],18)}{E(p["name"])}</span></label>' for i,p in enumerate(starters))
    featured=[('kecleon-shop','layers','Use the Kecleon Shop','Prices, daily TMs and Bag rules.'),('tm-compatibility','book','Check TM compatibility','Natural, compatible and taught states.'),('builds','fire','Plan a legal build','First and second starting moves.'),('save-recovery','shield','Protect or recover progress','Use the safe account and save checklist.')]
    routes=''.join(f'<a class="route" href="{URL(slug)}"><span class="route-icon">{icon(glyph)}</span><span><strong>{E(title)}</strong><span>{E(desc)}</span></span>{icon("arrow",20)}</a>' for slug,glyph,title,desc in featured)
    preview=[]
    for n in (1,4,7,25):
        p=next(p for p in DATA['dex'] if p['dex']==n)
        preview.append([f'<a href="/pokedex/#p{n}"><span class="dex-no">{n:03}</span> <strong>{E(p["name"])}</strong></a>',badges(p['types']),str(p['hp']),f'{p["pa"]:.2f}× / {p["sa"]:.2f}×'])
    sample=table(['Partner','Type','HP','Attack / Sp. Atk'],preview,kind='A sample of the partner reference')
    body=f'''<section class="opening"><div class="hero"><div class="hero-copy"><h1>PokéSurvivor Wiki:<br><em>tiers, builds & guides.</em></h1><p class="lead">Your independent Pokémon Survivor Wiki for the 966-partner Pokédex, tier lists, legal builds, co-op fixes and Judgment of Arceus.</p>
<form class="hero-search" action="/search/" role="search"><label class="sr-only" for="home-search">Search Pokémon, moves and guides</label>{icon('search',22)}<input id="home-search" name="q" type="search" maxlength="100" placeholder="Pokémon, moves, or a question…"><button type="submit" aria-label="Search the Wiki">{icon('arrow',23)}</button></form>
<div class="actions">{link('tier-list','Explore the full tier list','button')}{link('arceus-judgment','Survive Arceus','button secondary')}</div><p class="hero-note">Independent guide for JPTER78’s browser game. No game login, download charge or in-game purchase is offered here.</p></div>
<section class="starter-lab" data-starter-lab aria-labelledby="lab-title"><div class="lab-header"><h2 id="lab-title">Your opening move</h2>{link('starters','All 29 starters')}</div><fieldset class="starter-choices"><legend class="sr-only">Preview a starting partner</legend>{choices}</fieldset>
<div class="partner-profile"><div class="type-emblem" data-lab-emblem>{icon('fire',37)}</div><div><h3 data-lab-name>{E(initial['name'])}</h3><p data-lab-type>Fire · Starter partner</p></div><span class="partner-number" data-lab-number>#{initial['dex']:03}</span></div>
<dl class="partner-stats"><div><dt>HP</dt><dd data-lab-hp>{initial['hp']}</dd></div><div><dt>Movement</dt><dd data-lab-speed>{initial['spd']}</dd></div><div><dt>Atk / Sp. Atk</dt><dd data-lab-attack>{initial['pa']:.2f}× / {initial['sa']:.2f}×</dd></div></dl>
<div class="evolution-route" id="lab-result" aria-live="polite" aria-atomic="true"><div><span>Starting move</span><strong data-lab-move>{E(move['name'])}</strong></div>{icon('arrow',20)}<div><span>Evolution</span><strong data-lab-evolution>{E(move['evolution']['name'])}</strong></div></div><p class="lab-requirement" data-lab-requirement>Level {move['maxLevel']} + {E(move['evolution']['requirement'])} in this run, then choose the golden card.</p><a class="lab-link" data-lab-link href="/move-evolutions/#{E(move['id'])}">Plan this evolution {icon('arrow',18)}</a><noscript><p>Preview shows Charmander. Compare every option in the starter guide.</p></noscript></section></div>
<div class="topic-strip"><a href="/pokedex/">Pokédex <span>{len(DATA['dex'])} partners</span></a><a href="/moves/">Moves <span>{len(DATA['moves'])} definitions</span></a><a href="/move-evolutions/">Evolutions <span>{sum(bool(m['evolution']) for m in DATA['moves'])} conditions</span></a><a href="https://pokesurvivor.com/" class="play-topic">Play the developer’s game {icon('arrow',18)}</a></div></section>
<div class="home-content"><section class="home-section journey"><div class="section-heading"><h2>What’s stopping<br>your next run?</h2><p>Choose the problem. Find your next step.</p>{link('builds','Explore starter builds','text-link')}</div><div class="route-list">{routes}</div></section>
<section class="reference-home"><div class="reference-intro"><div class="reference-symbol">{icon('dex',38)}</div><h2>Meet the partners.<br>Know the numbers.</h2><p>Actual partner stats and type rules from the recorded game snapshot. Find a name, compare an opening, or check a difficult matchup.</p><div class="reference-types"><a href="/pokedex/?type=grass">{icon('grass',18)}Grass</a><a href="/pokedex/?type=fire">{icon('fire',18)}Fire</a><a href="/pokedex/?type=water">{icon('water',18)}Water</a></div>{link('pokedex','Open the full Pokédex','button')}</div><div class="reference-preview">{sample}<div class="database-links">{link('moves','Move patterns & base values')}{link('types','Type chart & matchup calculator')}{link('legendaries','Legendary encounters & roster')}</div></div></section>
<section class="home-section notebook"><div class="build-feature"><h2>A tier is a starting point.<br>Your build is the plan.</h2><p>Compare physical and special offense, both defenses and speed across all 966 partners, then connect legal TMs, nature, ability and both opening moves.</p><div class="actions">{link('tier-list','See all 966 ranked','button secondary')}{link('starter-tier-list','Compare starters','text-link')}{link('builds','Plan a build','text-link')}</div></div><aside class="latest"><h3>Latest verified source review</h3><p class="date">2026-10-22</p><h4>Shop, natures, abilities & TMs</h4><p>The reviewed source adds the Kecleon Shop, partner natures and abilities, TM teaching, a second starting-move selector and co-op spectating.</p>{link('updates','Read the verified changes','text-link')}</aside></section>
<section class="trust-strip"><div>{icon('shield',25)}<p><strong>Checked against the source.</strong><span>Reference reviewed {REVIEWED}. Source inspection is separate from gameplay testing.</span></p></div>{link('about','Our sources & method','text-link')}</section>
<section class="identity"><div><h2>Different game, similar name?</h2><p>Pokémon Survivor Burst is a separate project. Identify your game before using a build or download guide.</p></div>{link('survivor-vs-burst','Compare the games','text-link')}</section></div>'''
    add('', 'PokéSurvivor Wiki (2026) – Tier List, Builds & Game Guides','Independent PokéSurvivor wiki reviewed October 22 with 966 Pokémon, 103 moves, 97 evolution recipes, Shop, TM, nature, ability and build tools.',body,'Home',modified='2026-10-22')
    add('search','Search the PokéSurvivor Wiki','Search guides, Pokémon and moves in the PokéSurvivor Wiki.', '<p class="lead">Find a guide, a partner or a move.</p><form action="/search/" class="search-page"><label for="search-query">Search the Wiki</label><div><input id="search-query" type="search" name="q" maxlength="100" placeholder="Try Ember, Pikachu or mobile"><button class="button" type="submit">Search</button></div></form><p id="search-status" role="status" aria-live="polite"></p><ul id="search-results" class="search-results"></ul><noscript><p>Search needs JavaScript. Use the guide and database navigation to browse every topic.</p></noscript>','Search',index=False)


def render(slug,p,locale='en',pages=None):
    pages = pages or PAGES
    if locale == 'en' or p.get('preserve_media_layout'):
        enhanced=media.enhance(slug,p['body'])
        if locale != 'en': enhanced=localization.localize_home_media(enhanced,locale)
        p={**p,'body':enhanced}
    ui = localization.UI.get(locale, {
        'start':'Start here','tier':'Tier list','arceus':'Arceus','dex':'Pokédex','moves':'Moves','evolutions':'Evolutions',
        'home':'Home','menu':'Menu','main_nav':'Main navigation','play':'Play game','search':'Search','skip':'Skip to content',
        'guide':'Guide','evolve':'Evolve','quick':'Quick navigation','related':'Keep your run moving','sources':'Sources & snapshot scope',
        'reviewed':'Reference reviewed','snapshot':'This game, this snapshot.','snapshot_text':'These guides cover jpter78’s browser PokéSurvivor.','burst':'Playing Burst instead?',
        'on_page':'On this page','footer':'Footer','tagline':'An independent reference for your next run.','about':'About & sources','privacy':'Privacy',
        'analytics':'Analytics preferences','where':'Where to play','coop':'Co-op & account help','updates':'Updates','machine':'Machine-readable guide','markdown':'Markdown overview',
        'developer':'Developer’s game','language':'Language','legal':'Unofficial fan reference. Not affiliated with JPTER78, Nintendo, Creatures, GAME FREAK or The Pokémon Company. Pokémon belongs to its respective owners. Game data: JPTER78 / PokéSurvivor.',
        'code_license':'Code license','font_license':'Font license','brand_sub':'WIKI & GAME GUIDES','source_note':'Mechanics and data were checked against the named source snapshot. Source inspection is separate from gameplay testing.',
        'groups':{'Guides':'Guides','Database':'Database','Home':'Home','Search':'Search','Help':'Help'}
    })
    route=lambda s: localization.url(locale,s)
    local_link=lambda s,text,cls='': f'<a class="{cls}" href="{route(s)}">{E(text)}</a>'
    home_page=slug==''
    title=p['title']
    canonical=SITE+route(slug)
    media_ids=media.USED.get(slug,[]) if locale == 'en' or p.get('preserve_media_layout') else []
    social=''
    if media_ids:
        cover=media.BY_ID[media_ids[0]]
        image_path='/assets/media/'+cover['id']+('.svg' if cover['kind']=='diagram' else '-'+str(max(cover['variants']))+'.webp')
        if cover['kind']!='diagram':
            social=f'<meta property="og:image" content="{SITE+image_path}"><meta property="og:image:alt" content="{E(cover["alt"])}">'
    modified=p['modified']
    in_language=localization.LANG[locale]
    graph=[{'@type':'WebPage' if home_page else 'CollectionPage' if p['group']=='Database' else 'Article','@id':canonical+'#page','url':canonical,'name':title,'description':p['description'],'inLanguage':in_language,'dateModified':modified,'isPartOf':{'@id':SITE+'/#website'}}]
    if home_page: graph.append({'@type':'WebSite','@id':canonical+'#website','url':canonical,'name':'Pokémon Survivor Wiki','alternateName':'PokéSurvivor Wiki','inLanguage':in_language})
    else: graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':ui['home'],'item':SITE+route('')},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
    for ident in media.USED_VIDEOS.get(slug,[]) if locale == 'en' or p.get('preserve_media_layout') else []:
        v=media.VIDEO_BY_ID[ident];poster=media.BY_ID[v['poster']]
        uploaded=v['created']+'T00:00:00+00:00' if len(v['created'])==10 else v['created']
        graph.append({'@type':'VideoObject','@id':canonical+'#video-'+ident,'name':v['title'],'description':v['description'],'thumbnailUrl':SITE+'/assets/media/'+v['poster']+'-'+str(max(poster['variants']))+'.webp','uploadDate':uploaded,'duration':f'PT{v["duration"]}S','contentUrl':SITE+'/assets/media/'+ident+'.webm','inLanguage':'en','isPartOf':{'@id':canonical+'#page'}})
    nav=''.join(f'<a {"aria-current=\"page\"" if slug==s else ""} href="{route(s)}">{label}</a>' for s,label in [('how-to-play',ui['start']),('tier-list',ui['tier']),('arceus-judgment',ui['arceus']),('pokedex',ui['dex']),('moves',ui['moves']),('move-evolutions',ui['evolutions'])])
    related=''
    if p['related']: related=f'<section class="related"><h2>{ui["related"]}</h2><ul>'+''.join(f'<li>{local_link(s,pages[s]["title"])}</li>' for s in p['related'])+'</ul></section>'
    sources=''
    if p['sources']:
        src=''.join(f'<li><a href="{DATA["source"]["repository"]}/blob/{p["source_commit"]}/{E(s)}">{E(s)}</a></li>' for s in p['sources'])
        sources=f'<details class="sources"><summary>{ui["sources"]}</summary><p>{ui["reviewed"]} {modified}. {ui["source_note"]} <code>{p["source_commit"][:7]}</code>.</p><ul>{src}</ul></details>'
    toc=''
    import re
    headings=re.findall(r'<section class="article-section" id="([^"]+)"><h2>(.*?)</h2>',p['body'])
    if headings: toc=f'<details class="toc" open><summary>{ui["on_page"]}</summary><nav aria-label="{ui["on_page"]}">'+''.join(f'<a href="#{ident}">{text}</a>' for ident,text in headings)+'</nav></details>'
    group=ui['groups'].get(p['group'],p['group'])
    content=p['body'] if home_page else f'<div class="breadcrumbs">{local_link("",ui["home"])}<span>/</span>{E(group)}</div><div class="article-heading"><h1>{E(title)}</h1><p class="date">{ui["reviewed"]} <time datetime="{modified}">{modified}</time></p></div><div class="article-layout"><article>{p["body"]}{related}{sources}</article><aside class="article-aside">{toc}<div class="aside-note"><strong>{ui["snapshot"]}</strong><p>{ui["snapshot_text"]}</p>{local_link("survivor-vs-burst",ui["burst"])}</div></aside></div>'
    dock = f'<nav class="mobile-dock" aria-label="{ui["quick"]}">' + ''.join(f'<a href="{route(dest)}" {"aria-current=\"page\"" if slug==dest else ""}>{icon(glyph,21)}<span>{label}</span></a>' for dest,glyph,label in [('how-to-play','book',ui['guide']),('pokedex','dex',ui['dex']),('move-evolutions','evolve',ui['evolve']),('search','search',ui['search'])]) + '</nav>'
    resource_links=''
    if locale == 'en': resource_links='<link rel="describedby" href="/llms.txt" type="text/plain">'
    if locale == 'en' and slug in agent_resources.READING_PATHS:
        resource_links += f'<link rel="alternate" href="{agent_resources.READING_PATHS[slug]}" type="text/markdown">'
    alternates=''
    language_nav=''
    if slug != '404':
        alternates=''.join(f'<link rel="alternate" hreflang="{localization.LANG[loc]}" href="{SITE+localization.url(loc,slug)}">' for loc in localization.LOCALE_ORDER)
        alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE+localization.url("en",slug)}">'
        short={'en':'EN','es':'ES','it':'IT','zh-hant':'繁中'}
        options=''.join(f'<a href="{localization.url(loc,slug)}" hreflang="{localization.LANG[loc]}" lang="{localization.LANG[loc]}" {"aria-current=\"page\"" if loc==locale else ""}><span>{localization.LABEL[loc]}</span><small>{short[loc]}</small></a>' for loc in localization.LOCALE_ORDER)
        language_nav=f'<details class="language-menu"><summary aria-label="{ui["language"]}: {localization.LABEL[locale]}"><span>{short[locale]}</span><svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4.5 3 3 3-3"/></svg></summary><nav aria-label="{ui["language"]}">{options}</nav></details>'
    runtime=f'<script>window.WIKI_LOCALE={json.dumps(locale)};window.WIKI_I18N={json.dumps(localization.JS.get(locale,{}),ensure_ascii=False).replace("<","\\u003c")}</script>'
    return f'''<!doctype html>
<html lang="{in_language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(p['description'])}"><meta name="robots" content="{'index,follow,max-image-preview:large' if p['index'] else 'noindex,follow'}"><link rel="canonical" href="{canonical}">{alternates}{resource_links}<meta name="theme-color" content="#f6f6ee"><meta property="og:type" content="website"><meta property="og:site_name" content="Pokémon Survivor Wiki"><meta property="og:locale" content="{in_language}"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(p['description'])}">{social}<meta name="twitter:card" content="{'summary_large_image' if social else 'summary'}"><link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48"><link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96"><link rel="icon" href="/assets/mark.svg" type="image/svg+xml" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180"><link rel="manifest" href="/site.webmanifest"><link rel="stylesheet" href="/assets/wiki.css?v={CSS_VERSION}">{runtime}<script defer src="/assets/wiki.js?v={JS_VERSION}"></script><script defer src="/assets/analytics.js?v={ANALYTICS_VERSION}"></script><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')}</script></head>
<body><a class="skip" href="#main">{ui['skip']}</a><header class="site-header"><a class="brand" href="{route('')}" aria-label="Pokémon Survivor Wiki {ui['home']}"><img class="brand-mark" src="/assets/mark.svg" width="36" height="36" alt=""><span>Pokémon Survivor<span class="brand-sub">{ui['brand_sub']}</span></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">{ui['menu']}</button><nav id="site-nav" aria-label="{ui['main_nav']}">{nav}</nav><a class="play-link" href="https://pokesurvivor.com/">{ui['play']} {icon("arrow",16)}</a><a class="search-link" href="{route('search')}" aria-label="{ui['search']}"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg></a>{language_nav}</header><main id="main" class="{'home' if home_page else 'document'}">{content}</main>{dock}
<footer class="site-footer"><div><a class="footer-brand" href="{route('')}">Pokémon Survivor Wiki</a><p>{ui['tagline']}</p></div><nav aria-label="{ui['footer']}">{local_link('about',ui['about'])}{local_link('privacy',ui['privacy'])}<button type="button" class="analytics-settings" data-analytics-settings>{ui['analytics']}</button>{local_link('download',ui['where'])}{local_link('co-op',ui['coop'])}{local_link('updates',ui['updates'])}<a href="/llms.txt">{ui['machine']}</a><a href="/index.md">{ui['markdown']}</a><a href="https://pokesurvivor.com/">{ui['developer']}</a></nav><p class="legal">{ui['legal']} <a href="/assets/LICENSE-game.txt">{ui['code_license']}</a> · <a href="/assets/OFL.txt">{ui['font_license']}</a>.</p></footer></body></html>'''


def build():
    # Do not recursively remove an output tree: overwrite only this builder's files.
    OUT.mkdir(parents=True,exist_ok=True)
    for p in CONTENT['pages']: prose(p)
    reference_pages()
    new_system_pages()
    enhance_content_pages()
    home()
    locale_pages={'en':PAGES}
    for locale in localization.LOCALE_ORDER[1:]:
        locale_pages[locale]=localization.make_pages(PAGES,locale)
    for locale,pages in locale_pages.items():
        for slug,p in pages.items():
            route=localization.url(locale,slug)
            dest=OUT/route.lstrip('/')/'index.html'
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(render(slug,p,locale,pages),encoding='utf-8')
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
    for locale,pages in locale_pages.items():
        search=[dict(title=p['title'],url=localization.url(locale,s),kind=localization.UI.get(locale,{}).get('groups',{}).get(p['group'],p['group']),text=p['description']) for s,p in pages.items() if p['index']]
        search += [dict(title=p['name'],url=localization.url(locale,'pokedex')+'#p'+str(p['dex']),kind='Pokémon',text=' '.join(localization.TYPE_NAMES.get(locale,{}).get(t,t) for t in p['types'])) for p in DATA['dex']]
        search += [dict(title=m['name'],url=localization.url(locale,'moves')+'#'+m['id'],kind=localization.UI.get(locale,{}).get('moves','Move'),text=localization.TYPE_NAMES.get(locale,{}).get(m['type'],m['type'])+' '+m['kind']) for m in DATA['moves']]
        name='search.json' if locale=='en' else f'search-{locale}.json'
        (assets/name).write_text(json.dumps(search,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',ns)
    image_ns='http://www.google.com/schemas/sitemap-image/1.1'
    ET.register_namespace('image',image_ns)
    xhtml_ns='http://www.w3.org/1999/xhtml'
    ET.register_namespace('xhtml',xhtml_ns)
    tree=ET.Element('{'+ns+'}urlset')
    for locale,pages in locale_pages.items():
        for slug,p in pages.items():
            if p['index']:
                el=ET.SubElement(tree,'{'+ns+'}url'); ET.SubElement(el,'{'+ns+'}loc').text=SITE+localization.url(locale,slug); ET.SubElement(el,'{'+ns+'}lastmod').text=p['modified']
                for alt in localization.LOCALE_ORDER:
                    ET.SubElement(el,'{'+xhtml_ns+'}link',{'rel':'alternate','hreflang':localization.LANG[alt],'href':SITE+localization.url(alt,slug)})
                ET.SubElement(el,'{'+xhtml_ns+'}link',{'rel':'alternate','hreflang':'x-default','href':SITE+localization.url('en',slug)})
                if locale == 'en' or p.get('preserve_media_layout'):
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
    missing=dict(title='Page not found | Pokémon Survivor Wiki',description='This page could not be found. Browse the guides and databases.',body='<h1>That route ends here.</h1><p class="lead">The page you requested is missing. Start from the Wiki or search for the partner or move you need.</p>'+link('','Back to the Wiki','button'),group='Help',index=False,related=[],sources=[],modified='2026-10-15',source_commit=DATA['source']['commit'])
    # Render a standalone 404 without advertising it as an indexable route.
    page404=render('404',missing,'en',PAGES).replace('<h1>Page not found | Pokémon Survivor Wiki</h1>','<h1>Page not found</h1>').replace('<h1>That route ends here.</h1>','<h2>That route ends here.</h2>')
    (OUT/'404.html').write_text(page404,encoding='utf-8')
    manifest={}
    for locale,pages in locale_pages.items():
        for s,p in pages.items():
            route=localization.url(locale,s)
            manifest[route]=dict(title=p['title'],index=p['index'],modified=p['modified'],locale=locale,sha256=hashlib.sha256((OUT/route.lstrip('/')/'index.html').read_bytes()).hexdigest())
    (OUT/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(manifest)} localized pages and 404 into {OUT}; {sum(p["index"] for pages in locale_pages.values() for p in pages.values())} indexable URLs')


if __name__=='__main__': build()
