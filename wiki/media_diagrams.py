"""Source-derived instructional diagrams, not fabricated game screenshots."""
from pathlib import Path
import html
import json

HERE=Path(__file__).resolve().parent
OUT=HERE/'public/media'
OUT.mkdir(parents=True,exist_ok=True)

SPECS=[
 ('first-run-flow','Your first run',['Choose guest or sign in','Quiz suggests a partner','Accept or choose another','Move, collect XP, upgrade'],'A guest trial and a cloud account are separate.',['how-to-play']),
 ('controls-map','Desktop controls',['W A S D / arrows: move','1–4: choose active slot','Q / E: cycle active slots','Esc / P: pause solo play'],'The selected attack fires automatically.',['how-to-play']),
 ('evolution-conditions','Three evolution checkpoints',['Max the selected move','Take its required stat card','Keep leveling for the offer','Choose the golden card'],'Eligibility is not automatic evolution.',['move-evolutions']),
 ('ember-evolution','Ember → Fire Blast',['Start with Ember','Reach move level 5','Take Power in this run','Choose Fire Blast when offered'],'Power is the attack-stat prerequisite.',['move-evolutions','builds']),
 ('bubble-evolution','Bubble → Surf',['Start with Bubble','Reach move level 5','Take Sprint in this run','Choose the golden evolution'],'Bubble and Water Gun have different prerequisites.',['move-evolutions','builds']),
 ('build-route','Plan the opening, then adapt',['Choose a move pattern','Find the evolution stat','Improve that move in-run','Keep a matchup alternative'],'A stat tier is not a survival-time benchmark.',['builds','tier-list']),
 ('touch-map','Touch controls in landscape',['Rotate to landscape','Drag play area to move','Tap the active move slot','Pause before changing settings'],'Browser emulation does not certify a physical device.',['mobile']),
 ('type-products','Read this game’s type factors',['Weakness: 1.6×','Resistance: 0.6×','Softened immunity: 0.3×','Dual-type product: 0.3–2.4×'],'Water → Fire/Rock: min(1.6 × 1.6, 2.4) = 2.4×',['types']),
 ('new-move-patterns','Eight new attack behaviors',['Homing / bounce: guided or chained shots','Charge / spin: timed beam or radial hits','Quake / vortex: traveling wave or pull field','Shove / stun: displacement or control zone'],'Behavior is not the same as physical or special category.',['moves']),
 ('starting-move-rules','Starting Move decision path',['Default move works before purchase','Pay 400 once for that partner','Choose a legal non-buff move','Default remains available even off-type'],'Repertoire is separate and costs 1,500 coins.',['builds','upgrades']),
 ('save-safety-decision-flow','Protect a surviving save',['Keep the working browser unchanged','Check account and visible sync state','Separate pending, wait, offline and done','Report only non-sensitive facts'],'Do not clear the only browser copy while diagnosing.',['save-recovery']),
 ('coop-connection-check-flow','Co-op connection checks',['Confirm the current build and sign-in','Record host, guest and exact message','Try one fresh room after reloading','Preserve account and save data'],'Switching networks is not a guaranteed fix.',['co-op']),
]


def build():
    records=[]
    for ident,title,steps,note,pages in SPECS:
        esc=html.escape
        lines=''
        for i,text in enumerate(steps):
            y=142+i*83
            number='' if ident in ('controls-map','type-products') else f'<text x="78" y="{y+43}" text-anchor="middle" fill="#142f28" font-size="29" font-weight="700">{i+1}</text>'
            lines+=f'<rect x="40" y="{y}" width="880" height="66" rx="12" fill="#213f34"/><circle cx="78" cy="{y+33}" r="{8 if not number else 20}" fill="#f2c66d"/>{number}<text x="118" y="{y+43}" fill="#fffef8" font-size="30">{esc(text)}</text>'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="580" viewBox="0 0 960 580" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(". ".join(steps)+". "+note)}</desc><rect width="960" height="580" rx="16" fill="#142f28"/><g font-family="Arial,Helvetica,sans-serif"><text x="40" y="70" fill="#f2c66d" font-size="39" font-weight="700">{esc(title)}</text><text x="40" y="110" fill="#d2e0cf" font-size="22">PokéSurvivor Wiki · source-based diagram</text>{lines}<text x="40" y="536" fill="#d2e0cf" font-size="23">{esc(note)}</text></g></svg>'
        (OUT/(ident+'.svg')).write_text(svg,encoding='utf-8')
        records.append(dict(id=ident,kind='diagram',caption=title+'. '+note,alt='; '.join(steps),pages=pages,width=960,height=580,created='2026-10-19',source='Pinned game source 5a23d49; js/data/moves.js, js/data/starters.js, js/data/upgrades.js, js/data/types.js, js/systems/levelup.js',rights='Original SVG diagram authored for this Wiki; source-derived mechanics, no third-party sprite artwork.'))
    (HERE/'media-diagrams.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    return records


if __name__=='__main__':build()
